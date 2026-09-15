#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通話メモを Excel 台帳に 1 行追記する。

文字起こしから項目を読み取るのは Claude の仕事。このスクリプトは
「読み取った結果を Excel に安全に足す」ところだけを担当する。

使い方:
    # JSON ファイルから
    python append_call_log.py --excel 通話ログ.xlsx --json 通話メモ.json

    # 標準入力から (Claude が直接流し込む時)
    echo '{"お客様名": "..."}' | python append_call_log.py --excel 通話ログ.xlsx --json -

    # 複数件をまとめて (JSON 配列)
    python append_call_log.py --excel 通話ログ.xlsx --json 本日分.json

    # 台帳を作るだけ
    python append_call_log.py --excel 通話ログ.xlsx --init

設計方針:
  - 既存の月別予約 Excel は触らない。この台帳は独立した「通話の受け皿」。
    予約本体への転記は、人間が内容を確認してから手で行う。
  - 台帳をすでに手で編集していた場合、列の並びや追加列を壊さない。
    ヘッダー行を読んで列名でマッチングし、知らない列は空のまま残す。
  - 同じ音声ファイルの二重登録は既定で弾く。
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from openpyxl import Workbook, load_workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
except ImportError:
    print(
        "openpyxl が入っていません。以下を実行してください。\n\n    pip install openpyxl\n",
        file=sys.stderr,
    )
    raise SystemExit(2)

SHEET_NAME = "通話ログ"

# (列名, 幅, 折り返すか)
COLUMNS: list[tuple[str, int, bool]] = [
    ("受付日時", 18, False),
    ("チャネル", 12, False),
    ("お客様名", 16, False),
    ("電話番号", 16, False),
    ("用件", 12, False),
    ("希望日", 14, False),
    ("人数", 6, False),
    ("コース", 22, True),
    ("経験・ランク", 20, True),
    ("要望・メモ", 46, True),
    ("要確認", 34, True),
    ("対応者", 10, False),
    ("ステータス", 14, False),
    ("文字起こしファイル", 30, False),
    ("音声ファイル", 30, False),
    ("登録日時", 18, False),
]

HEADER_NAMES = [name for name, _, _ in COLUMNS]

CHANNELS = ["固定電話", "LINE通話", "携帯", "来店口頭", "じゃらん", "HPフォーム", "その他"]
YOUKEN = ["新規予約", "予約変更", "キャンセル", "問い合わせ", "その他"]
STATUSES = ["未処理", "確認中", "Excel反映済", "折り返し待ち", "対応不要"]


def build_sheet(wb: Workbook):
    ws = wb.active
    ws.title = SHEET_NAME

    header_fill = PatternFill("solid", fgColor="1F4E79")
    header_font = Font(name="Meiryo", bold=True, color="FFFFFF", size=10)

    for idx, (name, width, _) in enumerate(COLUMNS, start=1):
        cell = ws.cell(row=1, column=idx, value=name)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        ws.column_dimensions[get_column_letter(idx)].width = width

    ws.row_dimensions[1].height = 24
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:{get_column_letter(len(COLUMNS))}1"
    return ws


def read_header(ws) -> dict[str, int]:
    """ヘッダー行を読んで {列名: 列番号} を返す。"""
    mapping: dict[str, int] = {}
    for col in range(1, ws.max_column + 1):
        value = ws.cell(row=1, column=col).value
        if value is None:
            continue
        mapping[str(value).strip()] = col
    return mapping


def existing_audio_files(ws, header: dict[str, int]) -> set[str]:
    col = header.get("音声ファイル")
    if col is None:
        return set()
    seen: set[str] = set()
    for row in range(2, ws.max_row + 1):
        value = ws.cell(row=row, column=col).value
        if value:
            seen.add(Path(str(value)).name)
    return seen


def normalize(record: dict) -> dict:
    """値を文字列に整えつつ、未指定の列に既定値を入れる。"""
    out = {k: ("" if v is None else v) for k, v in record.items()}
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # 空文字も「未指定」として扱う。Claude が不明な項目を "" で渡してくるため。
    if not str(out.get("受付日時", "")).strip():
        out["受付日時"] = now
    if not str(out.get("ステータス", "")).strip():
        out["ステータス"] = "未処理"
    out["登録日時"] = now

    if not out.get("要確認"):
        out["要確認"] = "(なし)"
    return out


def warn_unknown_values(record: dict) -> list[str]:
    """選択肢から外れた値を警告する。弾かずに通す (現場の言葉を優先)。"""
    notes: list[str] = []
    for field, allowed in (("チャネル", CHANNELS), ("用件", YOUKEN), ("ステータス", STATUSES)):
        value = str(record.get(field, "")).strip()
        if value and value not in allowed:
            notes.append(f"{field}「{value}」は想定リスト外です ({' / '.join(allowed)})")
    return notes


def append_row(ws, header: dict[str, int], record: dict) -> int:
    row = ws.max_row + 1
    wrap_cols = {name for name, _, wrap in COLUMNS if wrap}

    unknown = [k for k in record if k not in header]
    if unknown:
        print(f"[警告] 台帳に無い項目は書き込みませんでした: {', '.join(unknown)}", file=sys.stderr)

    for name, col in header.items():
        value = record.get(name, "")
        cell = ws.cell(row=row, column=col, value=value if value != "" else None)
        cell.font = Font(name="Meiryo", size=10)
        cell.alignment = Alignment(
            vertical="top", wrap_text=name in wrap_cols
        )
    return row


def load_records(source: str) -> list[dict]:
    raw = sys.stdin.read() if source == "-" else Path(source).read_text(encoding="utf-8")
    data = json.loads(raw)
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return data
    raise ValueError("JSON はオブジェクトか、オブジェクトの配列にしてください。")


def main() -> int:
    parser = argparse.ArgumentParser(description="通話メモを Excel 台帳に追記する")
    parser.add_argument("--excel", required=True, help="台帳ファイルのパス (.xlsx)")
    parser.add_argument("--json", help="追記するメモの JSON。'-' で標準入力")
    parser.add_argument("--init", action="store_true", help="台帳を作るだけで終了する")
    parser.add_argument(
        "--allow-duplicate",
        action="store_true",
        help="同じ音声ファイルでも重複登録を許可する",
    )
    parser.add_argument("--dry-run", action="store_true", help="保存せず内容だけ表示する")
    args = parser.parse_args()

    excel_path = Path(args.excel)

    if excel_path.exists():
        wb = load_workbook(excel_path)
        ws = wb[SHEET_NAME] if SHEET_NAME in wb.sheetnames else wb.active
        created = False
    else:
        wb = Workbook()
        ws = build_sheet(wb)
        created = True

    header = read_header(ws)
    if not header:
        print("[エラー] ヘッダー行が読めません。1 行目に列名がある台帳を指定してください。", file=sys.stderr)
        return 1

    if args.init:
        if args.dry_run:
            print(f"[dry-run] 台帳を作成します: {excel_path}")
            return 0
        wb.save(excel_path)
        state = "作成しました" if created else "既に存在します"
        print(f"台帳を{state}: {excel_path}")
        print(f"  列: {' / '.join(header.keys())}")
        return 0

    if not args.json:
        print("[エラー] --json か --init のどちらかを指定してください。", file=sys.stderr)
        return 1

    records = load_records(args.json)
    already = existing_audio_files(ws, header)

    added = 0
    skipped = 0
    for record in records:
        record = normalize(record)

        audio = str(record.get("音声ファイル", "")).strip()
        if audio and not args.allow_duplicate:
            name = Path(audio).name
            if name in already:
                print(f"[スキップ] 登録済みの音声です: {name}")
                skipped += 1
                continue
            already.add(name)

        for note in warn_unknown_values(record):
            print(f"[確認] {note}", file=sys.stderr)

        row = append_row(ws, header, record)
        added += 1
        label = record.get("お客様名") or "(氏名未確定)"
        print(f"[追記] {row} 行目: {record.get('受付日時')} / {record.get('チャネル')} / {label}")
        if record.get("要確認") and record["要確認"] != "(なし)":
            print(f"        要確認: {record['要確認']}")

    if args.dry_run:
        print(f"\n[dry-run] 保存していません。追記予定 {added} 件 / スキップ {skipped} 件")
        return 0

    if added:
        wb.save(excel_path)
        print(f"\n保存しました: {excel_path} (追記 {added} 件 / スキップ {skipped} 件)")
    else:
        print(f"\n追記はありませんでした (スキップ {skipped} 件)")

    print("\n次にやること: 台帳の「要確認」欄を音声で確かめてから、月別予約 Excel に転記してください。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
