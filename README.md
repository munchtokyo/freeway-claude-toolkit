# Freeway Claude Code Toolkit

**Diving Service Freeway（佐渡・新潟）専用の Claude Code セットアップキット**

提供: 株式会社 DBA Japan / 川島 智行
対象: 小出 博之 様（佐渡）/ 安藤 均 様（新潟）/ 矢吹 様（新潟）

---

## 1. このリポは何か

Freeway さんの業務（予約処理・前日連絡・顧客カルテ）を Claude Code で半自動化するための、**個社専用パッケージ**です。

7-9 月の繁忙期前にスタッフ 3 名様の PC に Claude Code を入れ、すぐに使える状態を作るのが目的。

含まれているもの:

- **マスト 5 選 MCP**（Playwright / Exa / Context7 / Repomix / Document Skills）
- **Google 系 MCP**（Sheets / Calendar / Drive）
- **業務直結スキル 6 本**（予約統合 / 前日連絡 / 顧客カルテ / 休業日カレンダー / 器材マッチング / 多言語返信）
- **学習教材**（マスト 5 選を NotebookLM で音声化して聞ける）
- **顧客情報を守るセキュリティガード**
- **使うほど育つ OS 層**（auto-memory / instinct / skill-creator）

---

## 2. はじめての方へ（受講者向けクイックスタート）

### Step 1. インストール（10 分）

PowerShell を**管理者として実行**で開いて以下を貼り付け:

```powershell
cd $env:USERPROFILE\Desktop
git clone https://github.com/munchtokyo/freeway-claude-toolkit.git
cd freeway-claude-toolkit
.\install.ps1
```

Mac の方は Terminal で:

```bash
cd ~/Desktop
git clone https://github.com/munchtokyo/freeway-claude-toolkit.git
cd freeway-claude-toolkit
./install.sh
```

### Step 2. Claude Code を起動

```powershell
claude
```

### Step 3. 動作確認

```
/doctor
```

すべての MCP が緑になっていれば OK。

---

## 3. 業務で使うスキル（覚えるのは 3 つだけ）

| コマンド | やってくれること |
|---|---|
| `/yoyaku-merge` | HP・電話・口頭・個人 LINE・じゃらん の予約を 1 つのスプレッドシートにまとめる |
| `/zenjitsu-renraku` | 翌日のお客様への連絡（メール・LINE・電話原稿・カレンダー）を一度に下書き |
| `/karte` | お客様の暗黙知（過去の挙動・好み・講師相性）を音声 or テキストで記録 |

他に「あったら便利」スキル: `/kyugyo-calendar`（休業日反映）、`/kizai-match`（器材サイズ提案）、`/tagengo-reply`（多言語返信）。

詳しい使い方は `docs/02_workflow_examples.md` を読んでください。

---

## 4. 学習教材（おすすめの予習方法）

`docs/01_must5_claude_code.md` を Google NotebookLM の「Sources」に貼り付けて、「Audio Overview」機能で 12-15 分の対談ポッドキャストを作って、通勤中・移動中に音声で聞いてください。

7 月本研修開始前に音声で予習しておくと、研修初日のスタート位置が一段上がります。

---

## 5. 困った時

| 症状 | 対処 |
|---|---|
| `/doctor` で MCP が赤い | `docs/00_onboarding.md` のトラブルシューティング参照 |
| カルテに書いた情報が見つからない | `/karte 検索 ○○さん` と聞く |
| 自動化が壊れた・元に戻したい | 既存の Excel / じゃらん管理画面に戻れば全く同じ業務が回せます。Claude Code は「補助」であって「置き換え」ではありません |

困ったら川島まで LINE で連絡ください。

---

## 6. このリポのファイル構成

```
freeway-claude-toolkit/
├── README.md                  # このファイル
├── CLAUDE.md                  # Claude Code が読み込む業務文脈
├── install.ps1 / install.sh   # インストーラ
├── settings.json              # hooks + 権限設定
│
├── docs/                      # 学習教材・運用ガイド
│   ├── 00_onboarding.md       # はじめての方向け
│   ├── 01_must5_claude_code.md # マスト5選教材（NotebookLM用）
│   ├── 02_workflow_examples.md # 業務での具体的使い方
│   └── 03_security_basics.md  # 顧客情報を守る5箇条
│
├── skills/                    # 業務スキル本体
├── mcp-config/                # MCP設定ファイル
├── hooks/                     # セキュリティ・学習フック
├── rules/                     # 絶対ルール
├── templates/                 # メール・LINE・カルテのテンプレート
└── gas/                       # Google Apps Script 連携
```

---

## 7. 開発・実装状況（2026-05-28 時点）

- ✅ リポ作成
- ✅ README / CLAUDE.md / docs / 教材同梱
- 🚧 install.ps1 / install.sh
- 🚧 ★3 スキル（yoyaku-merge / zenjitsu-renraku / karte）
- 🚧 ○3 スキル（kyugyo-calendar / kizai-match / tagengo-reply）
- 🚧 hooks / rules / templates / gas

5/29 の佐渡現地作業で Google Sheets × GAS 連携を検証しながら ★3 スキルを順次実装します。

---

**Copyright** 株式会社 DBA Japan / Diving Service Freeway 様向け専用パッケージ
