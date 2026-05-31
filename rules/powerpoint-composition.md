# PowerPoint 作成ルール（文章・構成・技術編）

コンサルの小河原さんが川島に出してくれた PowerPoint 作法と、DBA Japan が python-pptx で
スライドを量産する中で蓄積した技術ノウハウを、フリーウェイの皆様向けにまとめた叩き台です。

## このファイルの位置づけ（最初に読む）

- ここに入っているのは **文章の書き方・情報の並べ方・python での作り方（技術）** だけ
- **配色・デザインの趣味・ブランドの見た目は意図的に抜いています**。そこは皆様の自由
- 「小河原さんはこう言った」を理由に押し付けるためのものではない
- 業務で「うちはこの方が読みやすい」と気づいたら、皆様の手で書き換えてください

つまり「中身（文章・構成・技術）は再利用価値が高いので渡す。見た目は各自で決めてください」という分担です。

---

## 1. スライド作法 8つの鉄則（小河原さん由来）

コンサルの現場で磨かれたスライドの作り方。読みやすさに直結する部分。

| # | ルール | 具体的にどうするか |
|---|--------|----------|
| 1 | オブジェクト間の余白は狭い方が洗練される | 要素どうしの隙間を広げすぎない。広いと素人っぽく見える |
| 2 | 同じ要素の位置はページを跨いでも揃える | ロゴ・ページ番号・見出しの開始位置を全ページで固定する |
| 3 | 情報の並び順は「①左上 → ②右上 → ③左下 → ④右下」 | Z型の視線誘導。一番見せたい情報を左上に置く |
| 4 | 文末に「。」をつけない | 体言止め、または「〜する」で終わる。箇条書きは特に句点なし |
| 5 | 料金説明以外は「です・ます」を使わない | 体言止めの方がすっきりする。「実施する」「対応」など |
| 6 | オブジェクトの上にテキストを重ねない | 文字は専用のテキストボックスに置く。重ね配置は避ける |
| 7 | 位置調整にスペースやフォントサイズ変更を使わない | 別のオブジェクトで揃える。空白文字でインデントしない |
| 8 | リード文は1文でそのスライドの要点をまとめる | タイトル直下に、太字1行で言い切る |

### 小河原さんの追加フィードバック（汎用化版）

- 繰り返し出てくる要素（ロゴ・社名・ページ番号）の位置は全ページで揃える
- 大見出しと小見出しの開始位置を揃える（スペースで揃えず、別オブジェクトで揃える）
- リード文の太字・非太字を全ページで統一する（基本は常に太字）
- 重要な情報ほど大きく表示する（上下に分けるなら、重要な方を大きく）
- 実績や事例は1件ずつスライドを分ける（情報の粒度を揃える）
- 事例は「サマリ1枚 ＋ 詳細1枚ずつ」の構成が読みやすい
- 「必須」などのバッジは枠からはみ出さないように収める
- 見出しが2回出てこないように注意する（黒帯に「目次」と書いた上でさらに目次ラベルを出す、など）

---

## 2. 文章の書き方ルール

### 句読点・語尾

- スライドの文末に「。」をつけない（体言止め、または動詞止め）
- 「です・ます」は料金説明など丁寧さが要る箇所だけ。それ以外は体言止め
- お願い系・締めの文だけは「です・ます」で柔らかくしてよい（強すぎる断定を避ける）

### 改行・1文の長さ

- リード文は必ず1文で完結させる（2文に割らない）
- 長い文は短く割る。スライドは「読ませる」より「見て分かる」が優先
- 「×」や「/」で並ぶフレーズは1つの文ではなく**タグの列**。本文として流すと崩れる（後述の技術編参照）

### 敬語・印象（相手に失礼にならない言い換え）

| 避ける表現 | 置き換え |
|---|---|
| 教える | お伝えする / 身につけていただく |
| 過度な自己卑下（「及ばない」「未熟」を何度も） | 1回までに絞り、あとは行動・貢献の言葉に変える |
| 全部解決します / 自走できます（大きな約束） | 「できることであれば」など限定詞を1つ入れる |
| 具体的すぎる約束（できなかった時にバツが悪い） | 約束の幅を少し広く取る |

理由: スライドや提案資料は相手が経営者や取引先のことが多い。言い切りすぎ・約束しすぎは、
守れなかった時に逆効果になる。控えめで事実ベースの方が信頼されやすい。

---

## 3. 技術編：python-pptx で日本語スライドを作る時の落とし穴

ここからは「Claude にスライドを作ってもらう時、なぜか文字が縦に割れる・はみ出す」を防ぐための
技術的な決まりごと。実際に15枚生成して186箇所手直しになった事故から確立したものです。

### なぜ崩れるのか（根本原因）

python-pptx は「決めた座標にそのまま文字を置く道具」ではなく、
**PowerPoint のフォント表示に依存したレイアウトエンジン**です。次の3つを無視すると崩れます。

- テキストボックスの内部余白（左右にマージンがある）
- フォント代替（Yu Gothic / Hiragino / Meiryo で文字の幅が違う）
- 日本語の文字単位での強制折り返し（「×」「/」「。」「、」「（」「）」「:」の前後で改行が起きる）

### レイアウト原則 7か条（必ず守る）

```
1. 文字列の長さを信用しない（実測 + 安全係数 1.25〜1.35）
2. 短いラベルほど最低幅を持たせる
3. 数字と単位を別の位置に固定しない（同じボックス内で run 分割）
4. 日本語の本文は必ず最大行数・最大文字数を決めておく
5. はみ出す文章は縮小ではなく編集する（タグ化・短文化）
6. 生成後は PPTX ではなくレンダリング画像で検査する
7. フォントを固定し、環境差を前提に安全係数を持つ
```

### 最低幅ルール（絶対値）

| 種類 | 最低幅 | 根拠 |
|---|---|---|
| 1文字の単位ラベル（「室」「軒」） | 0.55 inch | 内部余白 ＋ 自動折り返し判定 |
| 2〜3文字のラベル（「万円」「時間」） | 0.75 inch | 字間 ＋ 内部余白 |
| 曜日「(木)」（記号＋1文字＋記号） | 0.65 inch | 0.4 inch では3行に分断される |
| プロフィール等の右カラム | 5.5 inch | 4.7 inch で全件崩壊を確認 |
| 数字＋単位の合算横幅 | 数字フォント実測値 × 1.4 | Pillow で計測する |
| 本文テキスト幅 | 実測値 × 1.30 ＋ マージン | 安全係数 |

0.5 inch 未満のテキストボックスは原則として作らない（短い記号でも厳守）。

### 日本語の折り返しの実態

- `tf.word_wrap = True` は日本語では**文字単位**で強制的に折り返す
- 英語のような単語の切れ目での折り返しではない
- 「×」「/」「。」「、」「（」「）」「:」の前後で改行が起きる
- 「単語単位の幅で足りる」という前提は日本語ではほぼ確実に崩れる

### 数字＋単位の正しい作り方

```python
# NG（破綻パターン）: 数字と単位を別シェイプで固定位置に置く
add_textbox(slide, x, y, Inches(2.0), Inches(1.6),
            "20", font_size=80, bold=True)
add_textbox(slide, x + Inches(2.0), y + Inches(0.5),  # 数字の幅を仮定して破綻
            Inches(0.95), Inches(0.6),
            "軒", font_size=24)

# OK（推奨）: 1つのボックス内で run を分割する
add_number_with_unit(slide, x, y, "20", "軒",
                     num_size=80, unit_size=24)
```

### タグの列と本文の見分け方

「承継直後 × 建設業オーナー × 改修期 × 文化財」のように「×」で並ぶフレーズは、
本文ではなく**タグの列**です。本文ボックスに流すと「×」の前後で改行されて崩壊します。

```python
# NG（本文として流す → 破綻）
add_multiline_textbox(slide, x, y, w, h,
    ["承継直後 × 建設業オーナー × 改修期 × 文化財"], font_size=10)

# OK（タグの列として1個ずつ配置）
for tag in ["承継直後", "建設業オーナー", "改修期", "文化財"]:
    add_tag_pill(slide, x, y, tag)
    x += tag_width
```

または「承継直後」「建設業オーナー」「改修期」「文化財」を改行で短く分解する。

---

## 4. 必須ヘルパー関数（コピーして使えるコード）

```python
from PIL import ImageFont
from pptx.util import Inches, Pt

# macOS の主要日本語フォント
JP_FONT_CANDIDATES = [
    "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
    "/System/Library/Fonts/Supplemental/Hiragino Sans GB.ttc",
    "/Library/Fonts/Arial Unicode.ttf",
]


def estimate_text_width_inches(text, font_size_pt, safety=1.30):
    """テキストの必要幅をインチ単位で推定（Pillow 実測 + 安全係数）"""
    font = None
    for path in JP_FONT_CANDIDATES:
        try:
            font = ImageFont.truetype(path, int(font_size_pt))
            break
        except Exception:
            pass
    if not font:
        # フォールバック: 日本語1文字 ≒ font_size × 0.014 inch
        return len(text) * font_size_pt * 0.014 * safety
    bbox = font.getbbox(text)
    width_pt = bbox[2] - bbox[0]
    return (width_pt / 72) * safety


def validate_textbox_fit(text, width_inches, font_size_pt, label=""):
    """ボックス幅にテキストが収まるか確認し、収まらなければ警告を出す"""
    needed = estimate_text_width_inches(text, font_size_pt)
    if needed > width_inches:
        print(f"WIDTH WARN [{label}]: '{text[:40]}' "
              f"needs {needed:.2f}in > box {width_inches:.2f}in "
              f"(font={font_size_pt}pt)")
        return False
    return True


def add_number_with_unit(slide, x, y, num, unit,
                         num_size=80, unit_size=24,
                         num_color=None, unit_color=None,
                         font_name="Meiryo UI"):
    """数字+単位を1ボックス内の run 分割で配置（位置ズレを完全回避）"""
    from pptx.dml.color import RGBColor
    DEFAULT_NUM = RGBColor(0, 0, 0)
    DEFAULT_UNIT = RGBColor(0x44, 0x44, 0x44)
    num_color = num_color or DEFAULT_NUM
    unit_color = unit_color or DEFAULT_UNIT

    total_w = (estimate_text_width_inches(num, num_size, safety=1.20)
               + estimate_text_width_inches(unit, unit_size, safety=1.30)
               + 0.20)
    height = num_size * 1.4 / 72  # ベースライン余白込み

    txBox = slide.shapes.add_textbox(x, y, Inches(total_w), Inches(height))
    tf = txBox.text_frame
    tf.word_wrap = False  # 数字+単位は折り返さない
    p = tf.paragraphs[0]

    r1 = p.add_run()
    r1.text = num
    r1.font.size = Pt(num_size); r1.font.bold = True
    r1.font.color.rgb = num_color; r1.font.name = font_name

    r2 = p.add_run()
    r2.text = unit
    r2.font.size = Pt(unit_size)
    r2.font.color.rgb = unit_color; r2.font.name = font_name
    return txBox


def render_to_pdf_for_review(pptx_path, out_dir):
    """LibreOffice headless で PPTX を PDF 化して目視確認用に保存"""
    import subprocess, os, shutil
    soffice = shutil.which("soffice") or shutil.which("libreoffice")
    if not soffice:
        print(f"LibreOffice 未インストール。{pptx_path} を PowerPoint で開いて確認してください。")
        return None
    subprocess.run([soffice, "--headless", "--convert-to", "pdf",
                    "--outdir", out_dir, pptx_path], check=True)
    out = os.path.join(out_dir, os.path.basename(pptx_path).replace(".pptx", ".pdf"))
    print(f"Rendered: {out}")
    return out
```

### 生成後のレビュー工程（必ず実行）

PPTX を生成したら、次を必ずやる。

1. `validate_textbox_fit()` を全テキストシェイプに対して呼ぶ（生成スクリプトの末尾に入れる）
2. `render_to_pdf_for_review()` で実際にレンダリングして確認する（LibreOffice があれば）
3. PowerPoint で開いて目視確認する
4. 直す時は「ボックス幅を広げる」より「文章を編集する」を優先する

---

## 5. 既存 PPTX に大量のスライドを追加する時のレシピ

既存ファイルに5枚以上を途中挿入する時は、次の順で進める。
python-pptx には「途中挿入」のAPIがなく、末尾追加 ＋ XML 並び替えが唯一の方法です。

### 手順

1. 既存スタイル抽出: 挿入位置の周辺スライドのシェイプを走査し、座標・フォント・色を辞書に書き出す。新規スライドはその値を流用する
2. 構成提案 → 承認待ち: 「どこに何枚入れるか」を先に提示してOKをもらう
3. 末尾に追加: `prs.slides.add_slide(layout)` で新規スライドを全部末尾に足す
4. XML 並び替え: `prs.slides._sldIdLst` をリスト化し、希望の順に並べ直す
5. フッターを修正: ページ番号「n / 旧total」を新しい total に書き換える

```python
from pptx import Presentation

prs = Presentation(SRC)

# 2) 末尾に追加
for fac in DATA:
    s = prs.slides.add_slide(prs.slide_layouts[6])
    build_facility_slide(s, fac, page_num, TOTAL)

# 3) XML 並び替え（既存14枚 → 新規25枚 → 旧クロージング の順）
xml_slides = prs.slides._sldIdLst
slide_elements = list(xml_slides)
existing_1to14 = slide_elements[0:14]
existing_closing = slide_elements[14]
new_25 = slide_elements[15:40]
for sld in slide_elements:
    xml_slides.remove(sld)
for sld in existing_1to14 + new_25 + [existing_closing]:
    xml_slides.append(sld)

# 4) フッター patch
def patch_footer(slide, page_num, total):
    for shape in slide.shapes:
        if shape.has_text_frame:
            for para in shape.text_frame.paragraphs:
                for run in para.runs:
                    if run.text and run.text.strip().endswith('/ 15'):
                        run.text = f'{page_num} / {total}'

prs.save(DST)
```

ポイント:
- フッターの total を直し忘れると「14 / 15」のまま残り、ページ番号が崩れる
- 1〜2枚の追加なら、手順3と4は簡略化してよい
- 実行前に必ずバックアップ `cp original.pptx original.bak.pptx` を取る

---

## 6. 手動編集した PPTX を上書きしない（事故防止）

PowerPoint で開いて手で直した PPTX に対し、生成スクリプトを素のまま再実行しない。
過去に、本番ファイルを生成スクリプトで上書きして手動編集が消えかけた事故があります。

理由:
- PPTX は1つのバイナリファイル。git のように履歴で巻き戻せない
- 生成スクリプトの再実行は、手で直した内容を完全に消す不可逆操作

再実行する前に、次のいずれかを必ずやる。

1. 出力先を別パスにする（検証用は `/tmp/...pptx` へ）
2. 先にバックアップを取る（`cp final.pptx final.bak.pptx`）
3. 上書きガードを入れる:

```python
if os.path.exists(out_path) and os.environ.get("OVERWRITE_OK") != "1":
    sys.exit(f"既存ファイルあり: {out_path}\n  OVERWRITE_OK=1 で再実行してください")
```

教訓: 「差分を見たい」「学びを抽出したい」という真っ当な動機でも、結果として手動編集を消すのは事故です。
真っ当な動機 ＋ 危険な操作の組み合わせほどガードが要ります。

---

## 7. 生成後チェックリスト（文章・構成・技術）

### 文章・構成

- [ ] 文末に「。」がついていないか（体言止め or 動詞止め）
- [ ] 「です・ます」を使っていないか（料金説明など丁寧さが要る箇所を除く）
- [ ] リード文が全スライドで1文にまとまっているか
- [ ] 繰り返し要素（ロゴ・社名・ページ番号）の位置が全ページで揃っているか
- [ ] 大見出しと小見出しの開始位置が揃っているか（スペースで揃えていないか）
- [ ] 「教える」など上から目線の言葉を言い換えたか
- [ ] 言い切りすぎ・約束しすぎの表現がないか
- [ ] 実績・事例が1件1枚で粒度が揃っているか
- [ ] 同じ見出しが二重に出ていないか

### 技術・レイアウト

- [ ] 全テキストボックスに `validate_textbox_fit()` を呼んだか
- [ ] 警告が0件で完了したか（残るなら幅拡張または文章編集）
- [ ] 単位ラベル（「室」「軒」「万円」「時間」「(木)」）が最低幅を満たしているか
- [ ] 数字＋単位は `add_number_with_unit()` で1ボックス内 run 分割になっているか
- [ ] 「×」区切りのタグ列を本文ボックスに流していないか
- [ ] `render_to_pdf_for_review()` または PowerPoint で実際に目視確認したか
- [ ] 手動編集済みファイルを上書きしていないか

---

## デザイン・配色について（あえて入れていない理由）

配色・フォントの趣味・ロゴの見せ方・図解の装飾といった「見た目のデザイン」は、
このファイルにあえて入れていません。

理由: 見た目の正解は相手や業種で変わるし、好みの世界だからです。
フリーウェイの皆様が「ダイビングサービスらしい色・雰囲気」を自分たちで決めてください。
ここで渡しているのは、その土台になる「読みやすい文章・崩れない作り方」だけです。
