# Onboarding — はじめての方へ

**対象**: 小出 様 / 安藤 様 / 矢吹 様
**所要時間**: 30 分

> ⚠️ **このドキュメントは叩き台です**。川島が外部者として書いた超初期の入門編で、皆様の業務に合わない部分は遠慮なく書き換え・追加してください。設定ファイル `settings.json` と密接に関係する内容なので、設定変更時はここも併せて更新を。

このドキュメントを最初に読んでください。

---

## 1. Claude Code とは何か（1 分で）

Claude Code = AI（Claude）と話しながら **自分の PC のファイルを直接編集してくれる相棒** です。

何ができるか:

- Excel・スプレッドシートの整理を AI に頼める
- メール・LINE の下書きを AI が作ってくれる
- Web サイトのスクショや料金調べを AI が自動でやる
- 過去の顧客の情報を音声で吐き出すと AI が記録してくれる

**プログラミングは要りません**。日本語で話しかけるだけです。

---

## 2. 必要なもの

| もの | 確認方法 |
|---|---|
| Windows 10/11 または Mac | 起動できれば OK |
| Node.js | `node --version` で v18 以上 |
| Git | `git --version` でバージョン出る |
| Claude 課金プラン | Pro $20 以上推奨（チームで 1 アカ共有可） |

Windows の方で Node.js / Git が入ってない場合:

```powershell
winget install OpenJS.NodeJS
winget install Git.Git
```

---

## 3. インストール

### Windows

PowerShell を**管理者として実行**で開いて:

```powershell
cd $env:USERPROFILE\Desktop
git clone https://github.com/munchtokyo/freeway-claude-toolkit.git
cd freeway-claude-toolkit
.\install.ps1
```

### Mac

Terminal で:

```bash
cd ~/Desktop
git clone https://github.com/munchtokyo/freeway-claude-toolkit.git
cd freeway-claude-toolkit
./install.sh
```

インストールが終わったら:

```bash
claude
```

で Claude Code が起動します。

---

## 4. 最初の動作確認

Claude Code が起動したら、次の 3 つを試してください。

### ① ファイルが読めるか

```
README.md を読んで、このリポの目的を1行で教えて
```

### ② Web が見えるか（Playwright チェック）

```
https://www.google.com のスクリーンショットを撮って
```

### ③ Google スプレッドシートが読めるか（後日設定後）

```
Freeway予約台帳スプレッドシートの今日の予約を教えて
```

---

## 5. 業務で使うコマンド 3 つ

| コマンド | 場面 |
|---|---|
| `/yoyaku-merge` | 朝、その日入ってきた予約をまとめる時 |
| `/zenjitsu-renraku` | 夕方、翌日のお客様への連絡を準備する時 |
| `/karte` | ダイビング終了後、お客様の様子を記録する時 |

詳しい使い方は `docs/02_workflow_examples.md` を読んでください。

---

## 6. トラブルシューティング

### `claude` コマンドが見つからない

```bash
npm install -g @anthropic-ai/claude-code
```

### `/doctor` で赤い項目がある

赤い MCP の名前を Claude に伝えて、「これがエラー出てる、直して」と頼んでください。

### 何か壊れた気がする

**慌てなくて大丈夫**。Claude Code は「補助」であって、既存の Excel・じゃらん管理画面・現行サイトはそのまま動いています。困ったら川島まで LINE で。

---

## 7. 守ってほしいこと

`docs/03_security_basics.md` の **5 箇条** を必ず読んでください。お客様の個人情報を扱う以上、ここだけは外せません。

---

## 8. 学習ロードマップ

| 時期 | やること |
|---|---|
| 5/28-31 | 川島と一緒に環境構築・★3 スキル動作確認 |
| 6 月中 | `docs/01_must5_claude_code.md` を NotebookLM で音声化して通勤中に聞く |
| 7/10 | 本研修 開始 |
| 8 月 | 実業務で繁忙期を乗り切る |

---

困ったら遠慮なく川島まで。
