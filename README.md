# Freeway Claude Code Toolkit

**Diving Service Freeway (佐渡・新潟) 専用の Claude Code セットアップキット**

初期作成: 株式会社 DBA Japan / 川島 智行 (外部者として)
対象: 小出 博之 様 (佐渡) / 安藤 均 様 (新潟) / 矢吹 様 (新潟)

---

## ⚠️ このリポの位置づけ (重要)

このリポは **川島という外部者が作った初期版** です。

- 中身の **CLAUDE.md / docs / settings.json / ルール類は全て叩き台**
- これから **フリーウェイの皆様が編集していく** ことが前提
- 「川島がこう書いた」を理由に押し付けるためのものではない
- 業務をしながら「うちはこうじゃない」と気づいたら、皆様の手で書き換えてください

つまり、このリポは「川島の解釈のスナップショット → 皆様の業務文脈に進化させる出発点」です。

---

## 1. このリポは何か

フリーウェイの業務 (予約処理・前日連絡・顧客カルテ等) を Claude Code と一緒に進めるための、**個社専用パッケージの叩き台**です。

7-9 月の繁忙期前にスタッフ 3 名様の PC に Claude Code を入れ、すぐに使える状態を作るのが目的。

含まれているもの:

- **マスト 5 選 MCP** (Playwright / Exa / Context7 / Repomix / Document Skills)
- **Document Skills 本体同梱** (`skills/pdf` `skills/docx` `skills/xlsx` `skills/pptx`)。Word / Excel / PowerPoint / PDF を成果物として直接生成・編集・読み取りできる。Microsoft Office 中心のフリーウェイ業務でそのまま使える
- **PowerPoint 作成ルール** (`rules/powerpoint-composition.md`)。読みやすい文章・崩れないレイアウト・python-pptx の技術ノウハウを蓄積。**配色やデザインの趣味はあえて入れていない** (見た目は皆様が決める前提)
- **humanizer スキル** (`skills/humanizer`)。AI が書いた文章を、人が書いた自然な文章に整える。新潟店のメール返信で「丁寧な文章を AI に手伝ってもらう」時に効く
- **メール返信プレイブック** (`docs/11_email_reply_playbook.md`)。新潟店の実態 (矢吹さん聞き取り) ベース。コース説明・予約受付・初心者対応・悪天候中止の返信テンプレ + AI 下書きから humanizer で整える流れ
- **Google 系 MCP の設定サンプル** (Sheets / Calendar / Drive)
- **学習教材** (川島マスト 5 選を NotebookLM で音声化して聞ける)
- **顧客情報を守る 5 箇条**
- **使うほど育つ OS 層** (auto-memory / instinct / save-session / skill-creator / Hooks)

**含まれていないもの (意図的)**:

- 業務スキル本体 (`/予約まとめ` `/前日連絡` `/カルテ` 等) は**作っていません**。スキル候補のアイデアだけ `docs/04_skill_ideas.md` にあります。**皆様の手で `/skill-creator` を使って作っていく前提**
- スライドの**配色・デザインの趣味・ロゴの見せ方**は入れていません。`rules/powerpoint-composition.md` は文章と作り方 (技術) だけ。見た目はフリーウェイの皆様が自由に決めてください

---

## 2. はじめての方へ (受講者向けクイックスタート)

### Step 1. インストール (10 分)

PowerShell を **管理者として実行** で開いて:

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

## 3. このリポの育て方

このリポは「使うほど育つ」設計です。

1. **CLAUDE.md を読んで違和感を直す** — 業務をしながら「この前提違うな」と感じたら、その場で書き換えてください
2. **`docs/04_skill_ideas.md` を見て、必要だと思ったスキルを `/skill-creator` で作る** — 川島が決めた名前・粒度ではなく、皆様の体に馴染む形で
3. **auto-memory が貯めるメモを定期的に整理する** — `/self-improving-agent` (月 1 回)
4. **困った時は川島まで LINE** — 卒業期 (11 月) までは伴走します

---

## 4. 学習教材 (おすすめの予習方法)

`docs/01_must5_claude_code.md` を Google NotebookLM の「Sources」に貼り付けて、「Audio Overview」機能で 12-15 分の対談ポッドキャストを作って、通勤中・移動中に音声で聞いてください。

7 月本研修開始前に音声で予習しておくと、研修初日のスタート位置が一段上がります。

---

## 5. 困った時

| 症状 | 対処 |
|---|---|
| `/doctor` で MCP が赤い | `docs/00_onboarding.md` のトラブルシューティング参照 |
| 業務スキルがない | まだ作ってません。`docs/04_skill_ideas.md` を見て、必要なら `/skill-creator` で作ってください |
| 自動化が壊れた・元に戻したい | 既存の Excel / じゃらん管理画面 / Outlook はそのまま残してあるので、いつでも戻れます |

困ったら川島まで LINE で連絡ください。

---

## 6. このリポのファイル構成

```
freeway-claude-toolkit/
├── README.md                  # このファイル (叩き台・編集歓迎)
├── CLAUDE.md                  # Claude Code が読み込む業務文脈 (叩き台・編集歓迎)
├── install.ps1 / install.sh   # インストーラ
├── settings.json              # hooks + 権限設定
│
├── docs/                      # 学習教材・運用ガイド (全部叩き台)
│   ├── 00_onboarding.md
│   ├── 01_must5_claude_code.md  # 川島マスト 5 選教材 (NotebookLM 用)
│   ├── 02_workflow_examples.md
│   ├── 03_security_basics.md
│   └── 04_skill_ideas.md        # スキル候補メモ (本体は未実装)
│
├── skills/                    # OS 層スキル (汎用)
│   ├── skill-creator/         # 新スキル作成支援 (Anthropic 公式)
│   └── self-improving-agent/  # メモリ整理・パターン抽出
│
├── mcp-config/                # MCP 設定サンプル
├── hooks/                     # save-session / auto-memory 系
├── rules/                     # 絶対ルール (DBA 6 本は外部者思想・Freeway 専用 2 本)
└── memory/                    # auto-memory テンプレート
```

---

## 7. 開発・実装状況 (2026-05-28 時点)

- ✅ リポ作成・OS 層配置
- ✅ 教材同梱
- ✅ MCP 設定サンプル
- ⏸ **業務スキル本体: 意図的に未作成** (皆様の手で `/skill-creator` で作る)
- 🚧 **CLAUDE.md は叩き台**: 訪問中の対話で皆様が書き加える

5/28-31 の訪問中に CLAUDE.md を読み合わせし、皆様の業務文脈で書き換えていきます。

---

**Copyright** 株式会社 DBA Japan / Diving Service Freeway 様向け専用パッケージ

ただし、**中身は皆様の手で書き換えていく前提のテンプレート**です。
