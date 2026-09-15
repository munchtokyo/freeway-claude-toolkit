# セットアップ手順 (Windows / Mac)

所要時間は 30 分ほど。1 台につき 1 回だけやれば済みます。

---

## 1. Python を入れる

すでに Claude Code が動いている PC なら Python も入っている可能性が高いです。PowerShell で確認:

```powershell
python --version
```

`3.10` 以上が表示されれば OK。出ない場合は [python.org](https://www.python.org/downloads/windows/) からインストーラを落として、**「Add python.exe to PATH」にチェックを入れて**インストールしてください。

## 2. 必要なライブラリを入れる

```powershell
pip install faster-whisper openpyxl
```

ffmpeg の別途インストールは不要です。faster-whisper が音声の読み込みを内部で処理します。

## 3. 文字起こしモデルを落とす (初回のみ)

初めて実行した時に、自動でモデルが落ちてきます。large-v3 で約 3GB あるので、回線が細い時は時間がかかります。

```powershell
cd $env:USERPROFILE\Desktop\freeway-claude-toolkit
python skills\call-log\scripts\transcribe.py recordings\テスト.m4a --model large-v3 --vocab skills\call-log\references\vocab.txt
```

**落とし終われば、以降はネット接続なしで動きます。** 顧客の音声は一切ネットに出ません。

モデルの保存先:

```
Windows: %USERPROFILE%\.cache\huggingface\hub
Mac:     ~/.cache/huggingface/hub
```

店の回線でダウンロードが通らない場合、通る PC で一度実行してこのフォルダごとコピーすれば動きます。

### モデルの選び方

| モデル | サイズ | CPU での目安 | 使いどころ |
|---|---|---|---|
| `small` | 約 0.5GB | 実時間の 1 倍程度 | とりあえず試す |
| `medium` | 約 1.5GB | 実時間の 1 倍から 2 倍 | 日常運用の現実解 |
| `large-v3` | 約 3GB | 実時間の 2 倍から 4 倍 | 精度を優先したい時 |

「実時間の 2 倍」は、10 分の通話に 20 分かかるという意味です。繁忙期に 1 日 20 件の通話を回すなら `medium` から始めて、精度が足りなければ `large-v3` に上げてください。

GPU 搭載機なら自動で GPU を使うので、large-v3 でも実時間の数分の 1 で終わります。

## 4. フォルダを用意する

```
freeway-claude-toolkit\
├── recordings\      音声ファイルを置く場所 (git 管理外)
├── transcripts\     文字起こしの出力先 (git 管理外)
└── 通話ログ.xlsx     台帳 (git 管理外)
```

`recordings` と `transcripts` は `.gitignore` に入れてあります。顧客の声と会話内容が GitHub に出ることはありません。

## 5. 台帳を作る

```powershell
python skills\call-log\scripts\append_call_log.py --excel 通話ログ.xlsx --init
```

`通話ログ.xlsx` ができます。列はあとから自由に足して構いません。列を足しても並べ替えても、スクリプトは列名を見て書き込むので壊れません。

---

## 録音機材

### 固定電話 (0259-52-5781)

**受話器用録音アダプタ + IC レコーダー** が最も安定します。

1. 受話器と本体の間のカールコードを抜く
2. アダプタを挟んで、両側を接続し直す
3. アダプタから出ているプラグを IC レコーダーのマイク端子に挿す

電池も電源も工事も不要です。自分の声と相手の声の両方が、部屋の反響なしに録れます。電話音声としては最良の品質になります。

アダプタは 4 極 4 芯対応のものを選んでください。エルパ TEA-041 などが該当します。お店の電話機の受話器コードが 4 極 4 芯かどうか、購入前に確認を。

IC レコーダーの代わりに、PC のマイク端子に挿して録音ソフトで録っても構いません。

### LINE 通話

こちらは機械的にきれいな音を取る方法がありません。詳しくは `docs/12_call_transcription.md` を読んでください。実用的なのは次の 2 つです。

- **Android**: 画面録画で音声ソースを「メディア音声とマイク」にして通話する
- **iPhone**: スピーカーホンにして、別の機械 (IC レコーダーや古いスマホのボイスメモ) で録る

### 来店時の口頭予約

スマホのボイスメモをテーブルに置いて録るだけで足ります。LINE 通話のスピーカー録音と同じ扱いです。

---

## 動作確認

適当に 1 分ほど独り言を録音して、一連の流れを通してみてください。

```powershell
python skills\call-log\scripts\transcribe.py recordings\テスト.m4a --model medium --vocab skills\call-log\references\vocab.txt
```

`transcripts\テスト.txt` ができていれば成功です。

そのあと Claude Code で:

```
/call-log transcripts\テスト.md を台帳に入れて
```

---

## うまくいかない時

| 症状 | 原因と対処 |
|---|---|
| `faster-whisper が入っていません` | `pip install faster-whisper` を実行 |
| `openpyxl が入っていません` | `pip install openpyxl` を実行 |
| `モデルを読み込めませんでした: 403` など | ネットに出られていません。手順 3 のキャッシュコピーを試してください |
| 途中で止まる、極端に遅い | `--model small` に落としてください。メモリ不足の可能性があります |
| 文字起こしが空になる | 録音の音量が小さすぎます。録音機材の位置を電話機に近づけてください |
| 同じ文が何度も繰り返される | 無音部分での誤作動です。録音の前後の無音を切ってから再実行してください |
| 数字や固有名詞がよく間違う | 仕様です。`vocab.txt` に正しい表記を足すと改善します。数字は人間が聞き直す前提で運用してください |
| `通話ログ.xlsx` が開けない | Excel で開いたままだと書き込めません。閉じてから実行してください |
