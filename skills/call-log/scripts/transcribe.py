#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
通話録音の文字起こし (完全ローカル・オフライン)

faster-whisper を使って、録音ファイルを日本語テキストに変換する。
音声データは一切ネットに出ない。モデルの初回ダウンロードだけ通信が必要で、
以降はオフラインで動く。

使い方:
    python transcribe.py recordings/20260915_1430_電話.m4a
    python transcribe.py recordings/*.wav --model medium
    python transcribe.py recordings/ --outdir transcripts --vocab ../references/vocab.txt

出力 (--outdir 配下、既定は transcripts/):
    <元ファイル名>.txt       全文 (タイムスタンプなし・Claude に読ませる用)
    <元ファイル名>.md        タイムスタンプ付き (聞き直したい箇所を探す用)
    <元ファイル名>.json      区間データ (機械処理用)

電話音声は 8kHz 帯域で圧縮もかかるため、会議録音より精度は落ちる。
数字 (日付・人数・電話番号) と固有名詞は誤る前提で使うこと。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

AUDIO_SUFFIXES = {
    ".wav", ".mp3", ".m4a", ".mp4", ".aac", ".flac",
    ".ogg", ".opus", ".wma", ".amr", ".3gp", ".mkv", ".mov",
}

INSTALL_HINT = """
faster-whisper が入っていません。以下を実行してください。

    pip install faster-whisper

ffmpeg の別途インストールは不要です (faster-whisper が内部で音声を解析します)。
GPU がなくても CPU で動きます。CPU の場合 large-v3 は実時間の 2 倍から 4 倍ほど
かかるので、まずは --model medium で試すのをおすすめします。
"""


MODEL_LOAD_HINT = """
よくある原因と対処:

1. 初回実行でネットに出られない
   モデルは Hugging Face から取得します。社内ネットやプロキシで塞がれている場合、
   ネットに出られる PC で一度だけ実行してモデルを落とし、キャッシュフォルダごと
   業務 PC にコピーしてください。
       Windows: %USERPROFILE%\\.cache\\huggingface\\hub
       Mac    : ~/.cache/huggingface/hub
   コピー後はオフラインのまま動きます。

2. メモリ不足
   large-v3 は 4GB 前後のメモリを使います。--model medium か --model small で試してください。

3. モデル名の打ち間違い
   使えるのは tiny / base / small / medium / large-v3 です。
"""


def load_vocab(vocab_path: Path | None) -> str:
    """固有名詞リストを initial_prompt 用の 1 行に変換する。

    Whisper は直前の文脈に引っ張られる性質があるので、店名・コース名・
    ポイント名をあらかじめ渡しておくと、その表記に寄せてくれる。
    """
    if vocab_path is None:
        return ""
    if not vocab_path.exists():
        print(f"[警告] 辞書が見つかりません: {vocab_path}", file=sys.stderr)
        return ""

    words: list[str] = []
    for raw in vocab_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        # 「表記, 読み」形式にも対応。左側だけ使う。
        words.append(line.split(",")[0].strip())

    if not words:
        return ""
    # initial_prompt は長すぎると効きが悪くなる。先頭 200 語までに絞る。
    return "ダイビングサービスの電話応対です。" + "、".join(words[:200]) + "。"


def collect_inputs(paths: list[str]) -> list[Path]:
    found: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            found.extend(
                sorted(f for f in p.iterdir() if f.suffix.lower() in AUDIO_SUFFIXES)
            )
        elif p.is_file():
            found.append(p)
        else:
            print(f"[警告] 見つかりません: {p}", file=sys.stderr)
    return found


def hhmmss(seconds: float) -> str:
    total = int(seconds)
    return f"{total // 3600:02d}:{(total % 3600) // 60:02d}:{total % 60:02d}"


def pick_device(requested: str) -> tuple[str, str]:
    """(device, compute_type) を決める。GPU があれば使う。"""
    if requested != "auto":
        return requested, ("float16" if requested == "cuda" else "int8")
    try:
        import ctranslate2

        if ctranslate2.get_cuda_device_count() > 0:
            return "cuda", "float16"
    except Exception:
        pass
    return "cpu", "int8"


def transcribe_one(model, audio: Path, outdir: Path, args, initial_prompt: str) -> dict:
    print(f"\n[文字起こし] {audio.name}")

    segments, info = model.transcribe(
        str(audio),
        language=args.lang,
        beam_size=args.beam_size,
        initial_prompt=initial_prompt or None,
        # 電話音声は無音区間が多い。VAD で切ると幻聴 (無音部の作文) が減る。
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 700},
        # 直前テキストに引っ張られた同一フレーズの無限反復を防ぐ。
        condition_on_previous_text=False,
        no_speech_threshold=0.6,
        temperature=[0.0, 0.2, 0.4, 0.6, 0.8, 1.0],
    )

    print(f"  判定言語: {info.language} (確度 {info.language_probability:.2f})")

    rows: list[dict] = []
    plain: list[str] = []
    timed: list[str] = []

    for seg in segments:
        text = seg.text.strip()
        if not text:
            continue
        rows.append({"start": seg.start, "end": seg.end, "text": text})
        plain.append(text)
        timed.append(f"`{hhmmss(seg.start)}` {text}")
        print(f"  {hhmmss(seg.start)} {text}")

    outdir.mkdir(parents=True, exist_ok=True)
    stem = audio.stem

    txt_path = outdir / f"{stem}.txt"
    txt_path.write_text("\n".join(plain) + "\n", encoding="utf-8")

    md_path = outdir / f"{stem}.md"
    header = [
        f"# 通話文字起こし: {audio.name}",
        "",
        f"- 音声ファイル: `{audio}`",
        f"- 長さ: {hhmmss(info.duration)}",
        f"- モデル: {args.model}",
        "",
        "> 電話音声のため、数字 (日付・人数・電話番号) と固有名詞は誤変換の可能性があります。",
        "> 確定情報として使う前に、該当タイムスタンプの音声を聞き直してください。",
        "",
    ]
    md_path.write_text("\n".join(header + timed) + "\n", encoding="utf-8")

    json_path = outdir / f"{stem}.json"
    payload = {
        "audio_file": str(audio),
        "duration_sec": round(info.duration, 2),
        "language": info.language,
        "model": args.model,
        "segments": rows,
        "text": "\n".join(plain),
    }
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print(f"  → {txt_path}")
    print(f"  → {md_path}")
    print(f"  → {json_path}")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="通話録音をローカルで文字起こしする (faster-whisper)",
    )
    parser.add_argument("inputs", nargs="+", help="音声ファイル、またはフォルダ")
    parser.add_argument(
        "--model",
        default="large-v3",
        help="Whisper モデル (tiny / base / small / medium / large-v3)。既定 large-v3",
    )
    parser.add_argument("--outdir", default="transcripts", help="出力先フォルダ")
    parser.add_argument("--vocab", default=None, help="固有名詞リスト (1 行 1 語)")
    parser.add_argument("--lang", default="ja", help="言語コード。既定 ja")
    parser.add_argument(
        "--device", default="auto", choices=["auto", "cpu", "cuda"], help="実行デバイス"
    )
    parser.add_argument("--beam-size", type=int, default=5, help="ビーム幅。既定 5")
    args = parser.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        print(INSTALL_HINT, file=sys.stderr)
        return 2

    audios = collect_inputs(args.inputs)
    if not audios:
        print("[エラー] 音声ファイルが 1 件も見つかりませんでした。", file=sys.stderr)
        return 1

    device, compute_type = pick_device(args.device)
    print(f"[モデル読み込み] {args.model} / {device} / {compute_type}")
    print("  初回はモデルのダウンロードが走ります (large-v3 で約 3GB)。")
    try:
        model = WhisperModel(args.model, device=device, compute_type=compute_type)
    except Exception as exc:
        print(f"\n[エラー] モデルを読み込めませんでした: {exc}", file=sys.stderr)
        print(MODEL_LOAD_HINT, file=sys.stderr)
        return 3

    initial_prompt = load_vocab(Path(args.vocab) if args.vocab else None)
    if initial_prompt:
        print(f"[辞書] {len(initial_prompt)} 文字を初期プロンプトに投入")

    outdir = Path(args.outdir)
    failures = 0
    for audio in audios:
        try:
            transcribe_one(model, audio, outdir, args, initial_prompt)
        except Exception as exc:  # 1 件失敗しても残りは続行する
            failures += 1
            print(f"[エラー] {audio.name}: {exc}", file=sys.stderr)

    done = len(audios) - failures
    print(f"\n完了: {done} 件成功 / {failures} 件失敗")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
