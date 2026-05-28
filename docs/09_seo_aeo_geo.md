# フリーウェイの SEO / AEO / GEO 教科書

> 「貴社のサイトが、Google 検索でも、ChatGPT でも、Perplexity でも、ちゃんと見つけてもらえる状態」を作るための運用書です。
>
> AI 時代の Web 集客の核は「新しい呪文」ではなく「事業情報を AI に拾われやすい形に整える」こと。本教材は **14 本の一次ソース**（Google・Bing・OpenAI・Anthropic 公式 + Princeton/Toronto/MIT 学術論文 + Adobe/Ahrefs 等の実証データ）を統合し、信頼度マーカー [確定] / 【仮説】 / 【未検証】で全主張をラベルしています。

---

## §0. この教材の使い方

### 0.1 用語

| 用語 | 意味 |
|---|---|
| **SEO** (Search Engine Optimization) | Google / Bing 等の従来検索エンジン向けの最適化 |
| **AEO** (Answer Engine Optimization) | ChatGPT / Perplexity / Claude 等「質問に答えるエンジン」向けの最適化 |
| **GEO** (Generative Engine Optimization) | AI が生成する回答に引用される（cite される）ための最適化 |
| **AI Overviews** | Google 検索結果の上に出る「AI の要約回答」枠 |
| **citation** | AI 回答内で「出典」として自社サイトが言及・リンクされること |
| **earned media** | 第三者メディア（業界誌・地方紙・じゃらん・YouTube 等）に自社が掲載されること |
| **YMYL** (Your Money or Your Life) | 健康・金融・法律など、誤情報が利用者の生活に重大な影響を与える分野 |

### 0.2 一次ソース台帳（信頼度ランク付き）

本教材の全主張は以下 14 本の一次ソースに基づきます。営業煽り・代理店記事は採用していません。

| # | ソース | 種類 | 公開日 | 信頼度 |
|---|---|---|---|---|
| 1 | Google Search Central — Optimizing for generative AI | 公式ドキュメント | 2026-05-15 | [確定] |
| 2 | Bing Webmaster Guidelines（GEO 正式明文化） | 公式ドキュメント | 2026-02-27 | [確定] |
| 3 | OpenAI Crawler Documentation（OAI-SearchBot / GPTBot 仕様） | 公式ドキュメント | 継続更新 | [確定] |
| 4 | Anthropic Web Search docs（Claude Citations） | 公式ドキュメント | 継続更新 | [確定] |
| 5 | Princeton GEO（Aggarwal et al., KDD 2024）arxiv 2311.09735 | 査読論文 | 2024-08 | [確定] |
| 6 | Toronto "GEO: How to Dominate AI Search"（Chen et al.）arxiv 2509.08919 | プレプリント | 2025-09 | [確定] |
| 7 | MIT/Bagga E-GEO Testbed arxiv 2511.20867 | プレプリント | 2025-11 | [確定] |
| 8 | Northwestern Spiegel Research（Collinger & Malthouse） | 査読研究 | 2017 | [確定] |
| 9 | Adobe AI Traffic Report 2026 Q2 | 業界実証データ | 2026-04-16 | [確定] |
| 10 | Ahrefs 75,000-Brand Study（YouTube 言及 r=0.737） | 業界実証データ | 2026-05-27 | [確定] |
| 11 | Cyrus Shepard "23 AI Citation Factors"（54 研究集約） | 業界メタ分析 | 2026-05-07 | [確定] |
| 12 | Lily Ray "It Works Until It Doesn't"（220+ サイト追跡） | 業界実証 | 2026-05-13 | [確定] |
| 13 | Aleyda Solis "AI Search Winning Brands"（10 特性） | 業界フレーム | 2026-03-31 | [確定] |
| 14 | Rand Fishkin / Datos Q1 2026 State of Search | 業界実証データ | 2026-04-27 | [確定] |

### 0.3 信頼度マーカー

本教材内のすべての主張に必ず付けています。フリーウェイ社内でこの教材を使う時も同じルールでお願いします。

| 区分 | 意味 | 表記 |
|---|---|---|
| 確定 | 査読論文・公式ドキュメント・複数一次ソース一致 | [確定] |
| 仮説 | 業界紙・コンサル発信・1 ソースのみ | 【仮説】 |
| 未検証 | 出典曖昧・営業煽り由来 | 【未検証】 |

---

## §1. 一文結論

> **AEO/GEO は新しい呪文ではない。事業情報を AI に拾われやすい形に整える運用である。Google 公式（2026-05-15）と Bing 公式（2026-02-27）はいずれも「AEO/GEO は still SEO」と明言しており、特別な技術や AI 専用書き換えは不要。**

### 一次引用 [確定]

> "From Google Search's perspective, optimizing for generative AI search is optimizing for the search experience, **and thus still SEO**."
> — Google Search Central, 2026-05-15

> "Bing and Copilot search experiences rely on **the same core crawling, indexing, and ranking foundation** as traditional search."
> — Bing Webmaster Guidelines, 2026-02-27

> "Simply use normal SEO practices. **You don't need GEO, LLMO, or anything else.**"
> — Gary Illyes（Google Search Central Live, 2025-07）

> "Good SEO is good GEO, or AEO, AI SEO, LLM SEO, or LMNOPEO."
> — Danny Sullivan（Google, WordCamp 2025-09）

### つまり

**フリーウェイがやるべきことは**：
1. SEO 基礎を死守する（後述の §6 施策 1）
2. 第三者メディアに掲載される（§6 施策 2）
3. 質問に対する答えをサイトに明示する（§6 施策 3）
4. レビューを 5 件以上集める（§6 施策 4）
5. 業種別の構造化データ（schema）を入れる（§6 施策 5）

**やらなくていいこと**：
- AI 専用の特殊マークアップ
- `llms.txt` への過度な投資（Google 公式は不要と明言）[確定]
- 「3 ヶ月で AI 引用率○倍」を保証する商材【未検証】

---

## §2. AI 検索プラットフォーム別の挙動

### 2.1 Google AI Overviews

| 観点 | 内容 |
|---|---|
| 索引源 | Google 検索インデックス |
| 重要シグナル | Search Rank（上位 10 件から 38% が citation 選出）[確定] |
| Schema 影響 | 「特別な schema は不要」と Google 公式 [確定] |
| 取られ方 | 通常検索の上位ページから AI が要約 |

### 2.2 ChatGPT Search

| 観点 | 内容 |
|---|---|
| 索引源 | Bing インデックス（OAI-SearchBot 経由） |
| 重要シグナル | BLUF（Bottom Line Up Front）= 最初の 100 語で結論を述べる構造【仮説】 |
| 取られ方 | 質問文に対する直接の回答を持つページが優先 |

### 2.3 Perplexity

| 観点 | 内容 |
|---|---|
| 索引源 | Bing インデックス + 独自クローラー |
| 重要シグナル | Schema 有り 47% vs 無し 28% の citation 率【仮説】、freshness 30 日以内優遇【仮説】 |
| 取られ方 | 引用元を必ず明示するので「引用されたい度」が高い |

### 2.4 Claude (Anthropic)

| 観点 | 内容 |
|---|---|
| 索引源 | Brave Search API |
| 重要シグナル | 構造化された情報・公式情報源 |
| 取られ方 | 検索結果から要約。Citations 機能でリンク返却 |

### 2.5 Bing Copilot

| 観点 | 内容 |
|---|---|
| 索引源 | Bing インデックス |
| 重要シグナル | data-snippet 属性で AI に取らせる部分を制御可能 [確定]、single-topic + schema が grounding 最適 |
| 取られ方 | Bing 検索結果 + 公式 Webmaster Tools の AI Performance dashboard で計測可能 |

---

## §3. 矛盾点・両論併記（最重要）

ソース間で意見が割れる論点を全部洗い出しました。**信頼度が高い側 = 採用判断のデフォルト**として記載。

### 3.1 「コンテンツのチャンク化」

| 立場 | ソース | 主張 |
|---|---|---|
| **不要** [確定] | Google 公式（2026-05-15）, Danny Sullivan | 「AI のために小分けする必要なし」 |
| **必要だが解釈次第** [確定] | Aleyda Solis, Yotpo, ZipTie | 「BLUF が必要」「Definition Lists で +30-40% citation」 |

**統合解釈（採用判断）**:
- **AI 専用の chunking マークアップ・llms.txt 系の小分け化は不要**（Google 公式に従う）
- **人間にも読みやすい passage 構造（明確な見出し、BLUF、1 段落 1 主張、self-contained）は有効**（複数学術論文が裏付け）
- → **「人間向けの可読性を最大化する書き方をすれば、AI 向けに別途やる必要はない」**

### 3.2 「llms.txt」

| 立場 | ソース | 主張 |
|---|---|---|
| **不要** [確定] | Google 公式, Cyrus Shepard（Score 2.0/10） | Google ranking に影響なし |
| **AI assistant 用としては可能性** 【仮説】 | AI-Visibility.org.uk | brand identity 取得時に参照される可能性 |

**統合解釈**: フリーウェイは **優先度低**で扱う。新規制作で時間が余れば追加可、優先施策には入れない。

### 3.3 「構造化データ（Schema / JSON-LD）」

| 立場 | ソース | 主張 |
|---|---|---|
| **必須ではない** [確定 Google] | Google 公式 | 「AI 検索のための structured data は要らない」 |
| **特定エンジン・特定業種で有効** [確定 Perplexity / Bing] | ZipTie, Bing 公式, E-GEO 論文 | Perplexity: schema 有 47% vs 無 28% citation 率 |

**統合解釈**: Google AI Overviews だけ見るなら最優先ではない。Perplexity / Bing Copilot を含めると中優先。**業種別に適用**するのが正解。

### 3.4 「AI traffic は重要か」

| 立場 | ソース | 主張 |
|---|---|---|
| **絶対量はまだ小さい** [確定] | Rand Fishkin/Datos Q1 2026 | desktop visit の **<2%** |
| **業種により急成長** [確定] | Adobe AI Traffic Report Q1 2026 | retail に対し AI traffic **+393% YoY**、CVR **+42%** better |

**統合解釈**:
- **全体量はまだ小さいが、特定業種で爆発的成長**
- **AI traffic の質（CVR）は通常検索より高い**: 既に AI で比較・絞り込んだユーザーが到達するため pre-qualified

### 3.5 「AI ranking 追跡は意味あるか」

| 立場 | ソース | 主張 |
|---|---|---|
| **無意味** [確定] | Rand Fishkin/SparkToro | 2,961 prompts × 12 categories の実験で、同じ prompt が **1/100 未満で同じ brand list**、**1/1000 未満で同じ順序**。"provably nonsensical" |
| **Visibility % は有効** [確定] | Fishkin 自身, Jason Barnard | 「visibility percentage（多数 prompt 中の登場率）」は統計的に意味あり |

**統合解釈**: 「AI で何位？」は問わない、「AI で X% のクエリに登場する？」を問う。

### 3.6 「YouTube 言及 r=0.737 は因果か相関か」

| 立場 | ソース | 主張 |
|---|---|---|
| **YouTube 言及こそ最強の AI Visibility 信号** | Ahrefs 75,000 ブランド研究 | Spearman r=0.737、backlinks より強相関 |
| **相関であって因果ではない** | Codex セカンドオピニオン（2026-05-28） | 「YouTube に出る brand = もともと有名」だけかもしれない。動画量産は逆効果の可能性 |

**統合解釈（フリーウェイ向け）**:
- **YouTube 動画の量産だけを目的にしない**
- 「お客様の体験・口コミ導線との整合」が先にあって、その結果として YouTube 言及が増える順序を守る
- 例: 「自社のダイビング体験を YouTube に出す」ではなく、「お客様が YouTube 動画を作りたくなる体験設計 → 結果として言及される」
- **指名検索数の増加**を真の KPI にする

---

## §4. 業界・クエリ適性判定

AEO/GEO は全業種に効くわけではありません。まず適性判定をしてから施策に進みます。

### 4.1 6 軸判定マトリクス

以下 6 軸のうち 4 つ以上 Yes なら高効果業界。

| # | 判定軸 | 質問 |
|---|---|---|
| 1 | 比較可能性 | 顧客は複数社を比較するか |
| 2 | 料金関心 | 料金・コストを事前に知りたがるか |
| 3 | 地域性 | 「○○ + 地名」で検索されるか |
| 4 | 口コミ存在 | レビュー・口コミが集まる業界か |
| 5 | 専門性 | 専門知識・資格・実績が問われるか |
| 6 | 予約・問合せ直結 | サイト → 予約・問合せ・購入に直結するか |

### 4.2 フリーウェイ（ダイビング・体験型観光）の判定

| 軸 | Yes/No | 根拠 |
|---|---|---|
| 1. 比較可能性 | **Yes** | 顧客は複数のダイビングショップ・体験プランを比較する |
| 2. 料金関心 | **Yes** | 体験料・器材レンタル・宿泊込みプランの料金透明性を顧客が求める |
| 3. 地域性 | **Yes** | 「佐渡 ダイビング」「新潟 体験ダイビング」等、地名 + 業種で検索される |
| 4. 口コミ存在 | **Yes** | じゃらん・トリップアドバイザー・Google レビューに口コミが集まる業界 |
| 5. 専門性 | **Yes** | インストラクター資格・安全実績・コブダイ等の地域固有体験 |
| 6. 予約・問合せ直結 | **Yes** | サイトから予約フォーム or 電話に直結 |

→ **6/6 で「高効果業界」判定**。AEO/GEO 投資のリターンが大きい業種です。

### 4.3 Earned Media 戦略（Toronto 論文の指摘）[確定]

Toronto 論文（arxiv 2509.08919）は「AI Search は Earned Media（第三者・権威メディア）を Brand-owned / Social より圧倒的に重視する」と発見。

**フリーウェイで効く earned media**:
- 自治体観光協会（佐渡市・新潟県観光協会）
- 地方紙（新潟日報・佐渡毎日）への寄稿・取材
- じゃらん net・楽天トラベル・Booking.com 等の OTA レビュー
- ダイビング業界誌（マリンダイビング・ダイバー等）への寄稿
- 旅行系 YouTuber とのコラボ動画
- お客様自身が撮影・投稿する SNS

---

## §5. 5+1 施策の詳細（学術裏付け強化版）

### 施策 1: Search Rank 死守（最優先）

**根拠**: Cyrus Shepard Score 9.4、Ahrefs データ「AI Overview citations の 38% が Google top 10」、Lily Ray "ranking #1 on Google gets you more citations" [確定]

**実装**:
- [ ] **Core Web Vitals**: LCP <2.5s, INP <200ms, CLS <0.1
- [ ] Mobile-friendly + responsive（スマホで予約フォームが操作可能か）
- [ ] サイトマップ + robots.txt 適切設定
- [ ] 内部リンク構造
- [ ] HTTPS / セキュリティ
- [ ] JS が critical content を隠していない（server-side rendering 推奨）

### 施策 2: Earned Media 構築（日本では最重要）

**根拠**: Toronto 論文の earned media bias、Ahrefs YouTube 言及 r=0.737、Aleyda Solis §6 Corroborated [確定]

**フリーウェイでの実装**:
- [ ] **YouTube 言及戦略**: 旅行系・ダイビング系 YouTuber へのインタビュー出演、自社チャンネル運営、コラボ動画
- [ ] **地方紙・業界誌寄稿**: 月 1 本ペース（新潟日報・マリンダイビング等）
- [ ] **GBP 100% 完備**: 写真・営業時間・属性・サービス・投稿全部
- [ ] **OTA プロフィール完全記入**（じゃらん・楽天トラベル・Booking.com・トリップアドバイザー）
- [ ] **自治体観光協会・業界団体登録**（佐渡観光協会・PADI Japan 等）
- [ ] **顧客レビュー獲得施策**（自然発生のみ、買収禁止）

### 施策 3: BLUF + Extractable コンテンツ

**根拠**: Perplexity 90% top citations が first 100 words 内回答、ZipTie 研究、Aleyda Solis §4 Extractable 【仮説】

**実装**:
- [ ] **H1 の直後 100 語以内で核心の答え**（例: ページ冒頭で「いつ・どこに・誰向けの・いくらの・どんなダイビングか」を明示）
- [ ] **各セクションも段落 1 文目で結論**
- [ ] **定義文の自立性**: 「コブダイダイビングとは、佐渡近海でしか出会えない大型魚との水中体験のこと」と単独で成立する書き方
- [ ] **テーブル・箇条書き活用**（ただし飾り記号は使わない、Bing 公式が警告）
- [ ] **Q&A セクション**: FAQPage schema + 可視 Q&A
- [ ] **見出し階層**: h1 → h2 → h3 を飛ばさない

### 施策 4: レビュー集積（5 件の壁）

**根拠**: Northwestern Spiegel 研究「5 件で購買率約 4 倍（270% CVR up）」[確定]、Google 評価者ガイドライン §3.3、E-GEO 論文

**実装**:
- [ ] **最初の 5 件**を集中獲得（自社サイト + GBP + じゃらん）
- [ ] **星評価のスイートスポット 4.2-4.7**を狙う（4.7-5.0 より購買率高い）[確定]
- [ ] **認証済み購入者レビュー**（匿名より半点〜1 点高評価）[確定]
- [ ] **外部ドメイン（じゃらん・楽天・トリップアドバイザー）**にもレビュー集積
- [ ] **Review schema 実装**（業種に応じて）

**フリーウェイ向け補足**:
- 体験後 24 時間以内にお礼メール + レビュー依頼（タイミングが命）
- 「Google レビュー or じゃらん どちらでも」と選択肢を提示
- 写真付きレビューを優遇（写真ありは AI に拾われやすい【仮説】）

### 施策 5: Schema 戦略（業種別）

**根拠**: ZipTie/Perplexity「schema 有 47% vs 無 28% citation rate」、Bing 公式「single-topic + schema が grounding 最適」【仮説】

**フリーウェイ向け Schema 設計**:

```
ダイビング・体験型観光:
- LocalBusiness + SportsActivityLocation
- Service + Offer（プラン・料金）
- Review + AggregateRating
- FAQPage
- ImageObject（水中写真・店舗・宿泊施設）
- BreadcrumbList
- Organization
- sameAs（じゃらん・楽天・GBP・PADI 等）
- TouristAttraction（地域観光資源との紐付け）
```

### 施策 5+1: カテゴリ所有コンテンツ

**根拠**: Princeton GEO 論文「Cite Sources + Quotation + Statistics で +30-40% PAWC」、+4-5 位ページで +115% 上昇 [確定]

**実装**:
- [ ] **比較ページ**: 「初心者向け vs ライセンス保持者向け」「日帰り vs 宿泊込み」「冬季 vs 夏季」
- [ ] **業界別ガイド**: 「佐渡ダイビングの選び方」「コブダイに会える季節」
- [ ] **カテゴリリスティクル**: 「佐渡で見られる魚 30 種」
- [ ] **専門家プロフィール厚化**: インストラクターの経歴・資格・潜行回数・救助実績
- [ ] **統計データ掲載**: 自社実績数字（来店者数・リピート率・安全実績年数）
- [ ] **引用文**: お客様の声・専門家コメント・地元漁業組合のコメント引用

### 施策 0: Agent Operability（旧 accessibility）

**根拠**: OpenAI Publishers FAQ で用語確立、Aleyda Solis §1 Accessible [確定]

**実装**:
- [ ] HTML5 セマンティックタグ
- [ ] 全画像に alt 属性
- [ ] ARIA ラベル
- [ ] heading 階層論理的
- [ ] リンクテキスト具体的
- [ ] フォーム要素に label

---

## §6. AI クローラーの許可設定（robots.txt）

### 6.1 推奨設定

```text
# 学習データ提供は拒否、検索 in は許可、のパターン

User-agent: GPTBot
Disallow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Perplexity-User
Allow: /

User-agent: CCBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: *
Allow: /
```

### 6.2 各クローラーの意味

| クローラー | 許可/拒否 | 理由 |
|---|---|---|
| `GPTBot` | Disallow | OpenAI の **学習データ**に使われない |
| `OAI-SearchBot` | Allow | ChatGPT Search の **citation 候補に残る** |
| `ChatGPT-User` | Allow | ChatGPT で利用者が URL を読ませた時に取得される |
| `Claude-SearchBot` | Allow | Claude の検索結果に登場可能 |
| `ClaudeBot` | Allow | Anthropic の AI 検索全般 |
| `PerplexityBot` | Allow | Perplexity の検索 |
| `Perplexity-User` | Allow | Perplexity で利用者が URL を読ませた時 |
| `CCBot` | Disallow | Common Crawl（多くの LLM の学習データ源）拒否 |
| `Google-Extended` | Disallow | Gemini の学習に使われない（Google Search ranking には影響なし）[確定] |
| `*` | Allow | 通常のクローラー全て |

### 6.3 注意

**`Google-Extended` を `Disallow` にしても Google 検索の順位には一切影響しません** [確定]。これは Google が公式に明言しています。Gemini の学習に使われないだけ。

---

## §7. ダイビング・体験型観光業の AEO/GEO 戦略

### 7.1 優先 7 施策（フリーウェイ向け）

1. **LocalBusiness + SportsActivityLocation schema** + Review + AggregateRating + FAQPage
2. **多言語**: 英語（hreflang 適切実装）。インバウンド需要が高い佐渡では中国語・韓国語の検討も
3. **GBP / じゃらん / 楽天トラベル / トリップアドバイザー / Booking.com 完備**（earned media）
4. **「佐渡 + ダイビング + 比較」「佐渡 + ダイビング + 初心者」「コブダイ + ダイビング」等の関連クエリページ**
5. **YouTube**: 水中映像・コブダイ遭遇シーン・お客様体験ダイジェスト（YouTube 言及 r=0.737）
6. **BLUF**: トップページの最初 100 語で「いつ・どこに・誰向けの・いくらの・どんなダイビングか」明示
7. **レビュー集積**: じゃらん × 自社 × Google で最低 5 件×3 サイト

### 7.2 KPI（毎月測定）

| 指標 | 計測方法 | 目標 |
|---|---|---|
| Perplexity「佐渡 ダイビング」での citation 率 | 月 1 回手動で 5-10 クエリ叩く | 5 クエリ中 2 回以上 |
| Google AI Mode「佐渡 観光」「新潟 体験」での出現率 | 同上 | 3 ヶ月後に出現開始 |
| YouTube 言及数（自社名 or 「佐渡ダイビング」） | YouTube 検索 + Google アラート | 月 1 件以上の言及 |
| 指名検索数 | Google Search Console「フリーウェイ」 | 前月比増加 |
| GBP プロフィール完成度 | Google ビジネスプロフィール管理画面 | 100% |

### 7.3 季節性への対応

ダイビング業は季節需要が大きい業種です。

- **オフシーズン（冬季）**: コンテンツ整備・ブログ更新・スキルアップ情報配信に注力
- **オンシーズン（春〜秋）**: 顧客対応に集中、レビュー獲得の最大化
- **freshness 維持**: AI 検索は「30 日以内更新」を優遇する傾向【仮説】。月 1 回は何らかの更新を入れる

---

## §8. 共通テンプレ（全業種・新規 Web 制作で必ず実装）

```
[ ] Organization schema（自社情報）
[ ] FAQPage schema + 可視 Q&A
[ ] LocalBusiness または該当業種 schema
[ ] sitemap.xml + robots.txt
[ ] meta description / OG / Twitter Card
[ ] semantic HTML（header/main/section/article/footer/nav）
[ ] 全画像 alt 属性
[ ] H1 直後 100 語以内で BLUF
[ ] h1 → h2 → h3 階層論理的
[ ] last_updated メタ + 可視日付
[ ] Google Search Console 検証
[ ] Bing Webmaster Tools 検証
[ ] GBP 連携
[ ] Mobile-friendly + Core Web Vitals 基準クリア
[ ] AI クローラー allow（OAI-SearchBot / Claude-SearchBot / PerplexityBot）
```

---

## §9. 計測 KPI 4 Tier

**Rand Fishkin の指摘「AI ranking は無意味」を踏まえ、ranking ベースではなく visibility / brand / business 連動の指標で計測**。

### Tier 1: AI Visibility（プレゼンス）

- **Perplexity citation 出現率**: 指定 10 クエリ中、何 % で自社が cited されるか
- **ChatGPT Search 言及率**: 同上
- **Google AI Mode 引用率**: 同上
- **Bing AI Performance dashboard**: total citations / cited pages / grounding queries
- **Brand Radar (Ahrefs) / AI Visibility (Semrush)**: share of voice

### Tier 2: AI Traffic & CVR（パフォーマンス）

- **AI 経由 traffic**: GA4 で Referrer 別 (chat.openai.com / perplexity.ai / claude.ai 等)
- **AI 経由 session 時間**: Adobe データで非 AI より 48% 長い [確定]
- **AI 経由 CVR**: Adobe データで非 AI より 42% better [確定]
- **AI 経由 Revenue per Visit**: +37% [確定]

### Tier 3: Brand & Earned Media（土台）

- **YouTube 言及数**: 自社名 + 業種が動画タイトル・字幕・概要に出る回数（r=0.737）
- **業界紙・地方紙掲載数**: 月 1 本目標
- **GBP プロフィール完成度**: 100% 必達
- **Google Search Console**: organic impressions / clicks / position
- **指名検索数**: SparkToro / Google Trends で計測

### Tier 4: Business Outcome（最終）

- **問い合わせ数**
- **予約数**
- **成約数**
- **平均客単価**
- **リピート率**

### アトリビューションの罠（同時施策時の盲点）

**問題**: サイト改修 + 研修 + 営業を同時に走らせると、**何が成果要因か分からなくなります**。

例:
- サイト改修で予約増 → 改修効果か、AI 引用増か、季節要因か区別不能
- YouTube 公開後の指名検索増 → 動画効果か、業界紙露出か区別不能

**回避策**:
1. **施策ごとに開始日を 2 週間ずらす**（同時投入禁止）
2. **GA4 + Search Console + Bing Webmaster Tools の 3 つ全部に annotation 入れる**（「2026-06-01: LocalBusiness schema 追加」「2026-06-15: YouTube 動画公開」等）
3. **同質期間で前後比較**（前 4 週 vs 後 4 週）
4. **Tier 3 指名検索数**を真の北極星に置く（他 KPI は all noisy）

---

## §10. NG パターン（営業煽り・代理店トーク）

以下のフレーズが提案書・営業メールに出てきたら **要警戒**。データに基づいていない可能性が高いです。

### 【未検証】の典型

| フレーズ | なぜ NG か |
|---|---|
| 「3 ヶ月で AI 引用率○倍」 | 保証不能。Lily Ray の 220+ サイト追跡では 40-95% トラフィック減のサイトも多数 |
| 「ほとんどの競合はこれに気づいてない」 | 煽り。事実ベースで競合 3 社の現状を見せる方が信頼される |
| 「Schema を入れれば AI に選ばれる」 | 単純化しすぎ。Search Rank 9.4 vs Structured Data 5.6（Cyrus Shepard）[確定] |
| 「AI 専用の○○マークアップが必須」 | Google 公式が「不要」と明言 [確定] |
| 「llms.txt を入れないと AI に無視される」 | 影響実証なし。Cyrus Shepard Score 2.0/10 [確定] |
| 「by 2028, AI が 50% の検索を担当」 | Gartner 予測。原典数値要確認【仮説】 |

### OK パターン

- 「貴社の現状はこうです。競合はこうです。この差分を埋めるとこういう変化が【仮説として】期待できます」
- 「Google 公式は AEO/GEO を still SEO と呼んでいて、貴社の SEO 基盤も同時に強化されます」
- 「3 ヶ月で計測可能な変化が出る項目と、半年〜1 年で出る項目を分けています」

---

## §11. AI 生成記事の罠（Lily Ray の警告）

### 11.1 何が起きているか

Lily Ray が 220+ サイトを追跡した結果、**2026 年 1-4 月で 40-95% トラフィック減のサイトが多発** [確定]。

> "short-term GEO tactics: they work, they spread, they get patched"
> （短期的な GEO 手法は、効いて、広まって、Google にパッチされる）

### 11.2 やってはいけないこと

- **AI 生成記事の量産**（特に独自情報・体験談・専門家監修なしのもの）
- **薄い情報のページを大量公開**
- **キーワード詰め込み**
- **他社サイトの言い換えコピー**

### 11.3 やるべきこと

- **一次情報を持つ**: 実際の体験・自社実績・顧客の声・地元情報
- **専門家の監修**: インストラクター本人の言葉で書く
- **写真・動画**: 自社撮影の素材を使う
- **定期更新**: 月 1 回は何らかの更新（季節情報・実績更新・レビュー反映）

---

## §12. AI 検索向けのコンテンツ品質基準

### 12.1 Aleyda Solis 10 特性自己診断

各項目 1-5 点で自己採点（5 が最高）。

| # | 特性 | チェック観点 |
|---|---|---|
| 1 | Accessible | クローラーが読める。HTML5 セマンティック、alt 属性、ARIA |
| 2 | Authoritative | 専門性・権威性。著者プロフィール、資格、実績 |
| 3 | Comprehensive | 主題に関する情報が網羅的 |
| 4 | Extractable | AI が取り出しやすい構造（BLUF、見出し、表、Q&A） |
| 5 | Fresh | 更新日が明示され、定期更新されている |
| 6 | Corroborated | 第三者ソースで裏付けられる（earned media） |
| 7 | Original | 独自情報・一次データを含む |
| 8 | Structured | schema.org マークアップ、論理的見出し |
| 9 | Trustworthy | HTTPS、運営者情報、問い合わせ先明示 |
| 10 | User-Centric | ユーザーの質問に答える構造 |

**フリーウェイの当面の目標**: 全項目で 3 点以上。次に 4 点。

### 12.2 23 AI Citation Factors（Cyrus Shepard 整理・上位 10）

54 研究を集約した citation 要因 23 個のうち、影響度上位 10。

| 順位 | 要因 | スコア（10 点満点） |
|---|---|---|
| 1 | Search Rank（通常検索の順位） | 9.4 |
| 2 | Topical Authority（主題権威性） | 8.7 |
| 3 | Content Quality | 8.5 |
| 4 | Brand Strength | 8.2 |
| 5 | Earned Mentions（YouTube・業界誌・SNS） | 8.0 |
| 6 | First Hand Experience | 7.8 |
| 7 | Citations & References | 7.5 |
| 8 | E-E-A-T シグナル | 7.2 |
| 9 | Statistics & Data | 7.0 |
| 10 | Quotations from Experts | 6.8 |

**観察**:
- **Search Rank が圧倒的 1 位** → SEO 基礎を死守すれば AEO/GEO の大部分が達成される
- **schema は 5.6 点で中位** → 重要だが最優先ではない
- **llms.txt は 2.0 点で下位** → 優先度低

---

## §13. 鮮度（Freshness）戦略

### 13.1 AI 検索は鮮度を重視する【仮説】

- Perplexity は 30 日以内の更新を優遇する傾向【仮説】
- Google AI Mode も「最新の情報」を意識した回答を生成

### 13.2 月 1 回の更新ネタ候補

フリーウェイなら以下のような更新を回せます：

| 月 | 更新ネタ案 |
|---|---|
| 1 月 | 「今年のダイビングシーズン予測」「冬季メンテナンス情報」 |
| 2 月 | 「春のダイビング準備ガイド」 |
| 3 月 | 「シーズン開幕情報・新プラン告知」 |
| 4-5 月 | 「ゴールデンウィーク予約状況・体験レポート」 |
| 6-7 月 | 「コブダイ遭遇シーズン情報・水温情報」 |
| 8 月 | 「夏休み体験レポート・お客様の声特集」 |
| 9-10 月 | 「秋のダイビング・透明度情報」 |
| 11-12 月 | 「シーズン振り返り・来年の予約開始」 |

### 13.3 更新時の注意

- **更新日を可視化**: ページ内に「最終更新: 2026-06-15」と明記
- **意味のある更新**: 日付だけ変えて中身が同じは Google に検知される
- **構造化データの dateModified も更新**

---

## §14. リスク・矛盾・四半期再点検

### 14.1 未検証数字リスト（営業・社内で使う時は【仮説】明記）

| 数字 | 出典 | 検証ステータス |
|---|---|---|
| AI traffic +393% YoY (retail Q1 2026) | Adobe AI Traffic Report | [確定] |
| AI traffic CVR +42% better | Adobe AI Traffic Report | [確定] |
| YouTube 言及 r=0.737 | Ahrefs 75,000-brand study | [確定] |
| Northwestern 5 件レビュー = 4 倍購買率 | Spiegel Research Center | [確定] |
| Princeton GEO +30-40% PAWC | Aggarwal et al. KDD 2024 | [確定] |
| Perplexity BLUF 90% top citations | LLM Clicks AI / ZipTie | 【仮説】複数研究で一貫 |
| AI tools desktop visit <2% | Datos/SparkToro Q1 2026 | [確定] |
| 「3 ヶ月で AI 引用率○倍」 | LLMO コンサル | 【未検証】営業煽り |
| 「by 2028, AI が 50% 検索担当」 | Gartner 予測 | 【仮説】 |
| ChatGPT CVR は Google organic の 9 倍 | 代理店記事 | 【仮説】 |

### 14.2 陳腐化リスクの高い項目

| 項目 | 陳腐化リスク | 理由 |
|---|---|---|
| AI traffic +393% YoY | 中 | 業種・季節依存。再計測必須 |
| AI 検索プラットフォーム別の戦術値全般 | **最高** | 2026 年 7-12 月は仕様・露出面・参照元が変わりやすい |
| Perplexity ranking 仕様（30 日 freshness） | **高** | アルゴリズムは月次更新 |
| Princeton +30-40% PAWC | 低 | 査読論文の根本ロジックは安定 |
| OAI-SearchBot vs GPTBot 区別 | 低 | OpenAI 公式 stable |
| robots.txt 推奨設定 | 中 | 新 crawler 出現で更新必要 |
| Schema 推奨業種別 | 低 | schema.org は安定 |
| AEO/GEO 用語自体 | **高** | 業界用語は 6-12 ヶ月で交代する |

### 14.3 四半期再確認チェックリスト（次回: 2026-08-28）

```
[ ] Google AI 最適化ガイドの更新有無
[ ] Bing Webmaster Guidelines の更新
[ ] OpenAI Crawler Documentation の更新
[ ] Anthropic Web Search docs の更新
[ ] Cyrus Shepard 23 Factors の新版
[ ] Lily Ray の最新ペナルティ事例
[ ] Aleyda Solis の最新 checklist
[ ] Adobe AI Traffic Report の新四半期版
[ ] Ahrefs / Semrush の新研究
[ ] フリーウェイ自社サイトの検証ログレビュー
```

### 14.4 AI エージェント代理購買の注意書き

```
AI エージェントによる代理購買（ChatGPT Atlas、Google Business Agent 等）は、
2026-05 時点では本格普及前の移行期です。
今すぐの目的は「AI が正しく理解・比較・引用・遷移できる状態」を作ることであり、
代理購買による売上を保証するものではありません。
```

### 14.5 この教材の限界

- 日本語 LLM 固有の引用挙動は実証研究がまだ薄い（J-STAGE/CiNii で査読論文の蓄積待ち）
- ダイビング・体験型観光業の AEO/GEO 実証データは限定的
- AI 検索アルゴリズムは月次変動の可能性あり、3 ヶ月ごとに再点検必須

---

## §15. AI っぽさ解毒

AEO/GEO 施策で書かれるコンテンツが「AI 生成丸出し」になると、Lily Ray が報告した「40-95% トラフィック減」の罠に落ちます。

### 即座に避けるべき 5 つ

1. **絵文字を散らさない**（特にビジネス・予約系で）
2. **均一すぎる構成にしない**（h2 を全部同じパターンにする等）
3. **カード多用を避ける**
4. **デザインの一貫性を盲信しない**（業種ごとに最適解は違う）
5. **テンプレ感の強いフレーズを使わない**

### ダッシュ全廃

「— en dash」「-- ハイフン」「ーー 長音」は使わない。`、`「。」「｜」「／」「（カッコ）」「改行」で代替。

### 確認のフレーズ

書いた文章を読み返して、以下に該当したら書き直し：

- 「〜することができます」が連発
- 「〜について」が見出しに連発
- 同じ語尾（〜です。〜です。〜です。）が 3 文連続
- 「ぜひ」「お気軽に」「結論から申し上げますと」がテンプレ的

---

## §16. 今すぐやることリスト（30 日プラン）

優先順位順に並べています。

### 第 1 週（基礎診断）

- [ ] 現状の Perplexity 検索 5 クエリ実施（「佐渡 ダイビング」「新潟 体験ダイビング」「コブダイ ダイビング」「ダイビングショップ 佐渡」「インバウンド ダイビング 日本」）
- [ ] 現状の Google AI Mode 同 5 クエリ実施
- [ ] 競合 3 社の同クエリでの出現状況を記録
- [ ] GBP の完成度確認（100% でなければ列挙）

### 第 2 週（schema + robots.txt）

- [ ] サイトの robots.txt を §6.1 推奨設定に更新
- [ ] LocalBusiness schema を全ページに実装
- [ ] FAQPage schema を新規追加（よくある質問 5-10 個）
- [ ] Review schema をレビュー集積ページに実装

### 第 3 週（コンテンツ強化）

- [ ] トップページの最初 100 語を BLUF 化（「いつ・どこに・誰向けの・いくらの・どんなダイビングか」明示）
- [ ] インストラクタープロフィールページの厚化（資格・経歴・潜行回数・救助実績）
- [ ] 「コブダイに会える季節」等の業界別ガイドページ 1 本追加

### 第 4 週（earned media + 計測基盤）

- [ ] OTA プロフィール（じゃらん・楽天・トリップアドバイザー）を 100% 完備
- [ ] 自治体観光協会（佐渡観光協会）の掲載確認
- [ ] Google Search Console + Bing Webmaster Tools 連携
- [ ] 月次計測テンプレ作成（§9 Tier 1-4 を Excel/スプレッドシートで）

---

## §17. 関連ドキュメント

- `docs/00_onboarding.md`: Claude Code と一緒に進める基本
- `docs/01_must5_claude_code.md`: Claude Code の MUST 5
- `docs/02_workflow_examples.md`: 業務ワークフロー実例
- `docs/03_security_basics.md`: 個人情報を守る 5 箇条
- `docs/06_freeway_todo.md`: フリーウェイ向け TODO リスト
- `docs/10_sentry_monitoring.md`: Web サイト常時バグ監視（次の教材）

---

## 改版履歴

| 日付 | 版 | 変更内容 |
|---|---|---|
| 2026-05-28 | v1.0 | 初版。AEO/GEO 教材を Freeway 向けに再編。一次ソース 14 本統合、信頼度マーカー付き、ダイビング・体験型観光業向けに業種テンプレ作成 |
