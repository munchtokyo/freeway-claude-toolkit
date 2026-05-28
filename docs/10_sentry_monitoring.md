# フリーウェイの Web サイト常時バグ監視ガイド（Sentry 入門）

> 「予約フォームが急に動かなくなった」「お客様が見ているページでエラーが出ている」を **発生した瞬間に検知**できる仕組みを、フリーウェイの Web サイトに導入する話です。
>
> 技術詳細は DBA Japan 側で実装します。本書は **「何が嬉しいか」「個人情報はどう守るか」「通知が来たらどう動くか」** をフリーウェイのスタッフ向けに平易に説明したものです。

---

## §0. この教材の対象

| 読者 | 読み方 |
|---|---|
| 小出様・矢吹様・安藤様（フリーウェイ受講者） | §1〜§5 を読む。技術詳細（§6 以降）は飛ばして OK |
| 川島・DBA Japan 側 | 全章。特に §6〜§9 は実装時に参照 |

---

## §1. Sentry とは何か（平易な説明）

### 1.1 一言で言うと

**Web サイト専属の「警備員 兼 看護師」** です。

- **警備員**としての役割: サイトのどこかで異常（バグ・エラー）が起きた瞬間に検知して、すぐ知らせてくれる
- **看護師**としての役割: 異常が起きた状況（誰が・どのページで・何をしようとして・どんな順序で）を記録して、原因究明を手伝ってくれる

### 1.2 何が変わるか

**今までのフリーウェイ Web サイト運用（仮想）**:
```
お客様が予約フォームでエラーに遭遇
   ↓
お客様が諦めて電話してくる or 諦めて去る
   ↓
小出様が「あれ、最近予約少ないな…」と気づく（数日〜数週間後）
   ↓
原因不明のまま時間が経つ
```

**Sentry 導入後**:
```
お客様が予約フォームでエラーに遭遇
   ↓
Sentry が即座に検知
   ↓
川島 or DBA に通知（Slack/メール）
   ↓
当日中に原因特定 → 修正
   ↓
お客様の予約完了率が下がらない
```

### 1.3 業界での使われ方

Sentry は世界で 100,000 社以上が使っている定番ツールです（Disney・Microsoft・GitHub 等の大手も利用）。

- **公式サイト**: https://sentry.io/
- **料金**: 個人・小規模事業は **Developer プランで月 $26〜**（月間 50,000 エラーまで）
- **無料プラン**: 月 5,000 エラーまで無料（フリーウェイ規模なら無料枠で十分始められる）

---

## §2. なぜ予約フォームに必要か

### 2.1 フリーウェイの業務上の重要度

予約フォームは、フリーウェイのお客様接点の **最初の関門**です。ここが壊れていると：

| 影響 | 例 |
|---|---|
| **直接の機会損失** | 予約しようとしたお客様が、エラーで諦める |
| **問い合わせ電話の急増** | 「ネットで予約できない」と電話が殺到 |
| **信頼の毀損** | 「このお店、ちゃんと運営してるのかな」と不安にさせる |
| **リピートの減少** | 一度悪い体験をしたお客様は二度と戻ってこない可能性 |

### 2.2 予約フォームで起きやすいエラー

| エラー種別 | 発生原因の例 | Sentry でどう見えるか |
|---|---|---|
| **送信ボタンが反応しない** | JavaScript エラー、サーバー側 API 不通 | 「送信時にエラー」「API 500 エラー」として通知 |
| **入力欄が表示されない** | スマホ特定機種で表示崩れ | 「画面表示時エラー（iPhone Safari 18 で発生）」 |
| **「お名前」を入れても次に進めない** | バリデーションロジックの不具合 | 「フォーム送信前検証で停止」 |
| **完了画面が出ない** | 送信は成功したが完了表示処理で失敗 | 「完了画面レンダリング時エラー」 |
| **データベース書き込み失敗** | DB 側の障害 | 「予約データ保存失敗」 |

### 2.3 営業時間外でも検知できる

例えば 23 時にバグが入っても、Sentry が即時通知するので、翌朝小出様が出社した時には DBA 側で修正済み or 状況把握済みの状態にできます。

---

## §3. 何が検知できるか（具体例）

### 3.1 自動で検知できるもの

- **JavaScript エラー**: ブラウザ側で起きるエラー全般
- **API エラー**: サーバーとの通信失敗
- **ページ表示の遅延**: ページ読み込みに 3 秒以上かかる等
- **Core Web Vitals 悪化**: Google 検索順位にも影響する指標
- **ユーザーが遭遇した「動かない」状況**: クリックしても何も起きない等

### 3.2 設定で検知できるもの

- **予約フォームの送信失敗率**: 全体の何 % が送信に失敗しているか
- **特定ページのエラー率急増**: 普段 0.1% のエラー率が 5% に跳ねた瞬間に通知
- **特定ブラウザ・デバイスでの障害**: 「iPhone iOS 18 でのみ発生」等
- **デプロイ後のエラー増加**: 新機能リリース直後にエラーが増えた → 即ロールバック判断

### 3.3 検知できないもの

- **ビジネスロジックの誤り**: 「予約料金の計算式が間違っている」等は、エラーは出ないので Sentry では検知不可
- **悪意ある操作**: 不正アクセス系は別のツール（WAF・セキュリティサービス）が必要
- **コンテンツの間違い**: 「営業時間の表記ミス」等は人間の目で確認

---

## §4. 個人情報を Sentry に送らない設定（最重要）

### 4.1 なぜこれが最優先か

Sentry はエラー発生時の「状況」を記録するため、設定を間違えると **お客様の個人情報が Sentry のサーバーに送られてしまう** リスクがあります。

例えば予約フォームで「お名前: 山田太郎、電話: 080-1234-5678」と入力された瞬間にエラーが起きると、デフォルト設定ではその入力内容ごと Sentry に送られる可能性があります。

これは **`rules/customer-data-handling.md`（顧客データ取り扱い）に違反**します。

### 4.2 DBA 側で実装する scrub（マスキング）設定

DBA Japan 側で以下の自動マスキング設定を必ず入れます。

**マスキング対象**:

| 種別 | パターン | 送信時の表示 |
|---|---|---|
| メールアドレス | `xxx@yyy.zzz` | `[REDACTED-EMAIL]` |
| 電話番号 | `090-xxxx-xxxx`, `080-...`, `070-...`, `03-...` 等 | `[REDACTED-PHONE]` |
| クレジットカード番号 | 16 桁数字パターン | `[REDACTED-CARD]` |
| 住所 | 入力フィールド名が `address`, `住所` 等 | `[REDACTED-ADDRESS]` |
| 氏名 | 入力フィールド名が `name`, `氏名`, `お名前` 等 | `[REDACTED-NAME]` |
| パスワード（管理画面） | フィールド名が `password`, `pwd` 等 | `[REDACTED-PWD]` |
| Cookie / セッション | 全 Cookie・Authorization ヘッダ | `[REDACTED-AUTH]` |

### 4.3 全フィールドの自動マスキング

具体的なフィールド名指定では漏れる場合があるので、追加で **「あらゆる field を再帰的にチェックして個人情報パターンを REDACTED 化」** する処理を入れます（deepScrub）。

これは Basehi.ai という DBA の別プロダクトで本番運用済みのコードを移植します。

### 4.4 Sentry サーバーの所在

Sentry はデフォルトでアメリカ・サンフランシスコのサーバーに送信されますが、**マスキング処理は送信前にブラウザ側で実行される**ため、生の個人情報が国境を越えることはありません。

それでも不安な場合は、Sentry の EU サーバーオプションを使うことも可能です（料金は同じ）。

---

## §5. 通知が来たらどう動くか（運用フロー）

### 5.1 通知の種類

| 緊急度 | トリガー | 通知先 | 対応時間 |
|---|---|---|---|
| 🔴 緊急 | 予約フォーム送信失敗率 > 10% | 川島 LINE + DBA Slack + 小出様メール | 即時（30 分以内） |
| 🟡 警戒 | エラー率の前日比 +500% | 川島 LINE + DBA Slack | 当日中（営業時間内） |
| 🟢 情報 | 月次のエラーサマリー | DBA Slack のみ | 月次レビュー時 |

### 5.2 緊急通知が来た時のフロー

```
🔴 通知発生
   ↓
川島 or DBA 担当者が Sentry ダッシュボードでエラー内容確認（5 分以内）
   ↓
[ケース A] 自分達で即修正可能
   → 修正 → 動作確認 → 小出様に「直しました」連絡
   
[ケース B] 一時的にフォームを停止すべき
   → 小出様に連絡「予約フォームを一時的に止めて、電話受付に切り替えてください」
   → 修正 → テスト → 再開
   
[ケース C] 原因特定に時間が必要
   → 小出様に状況連絡「○○の原因調査中、夜までに対応します」
   → 並行して継続調査
```

### 5.3 小出様にお願いしたいこと

- **電話で「ネット予約できない」と問い合わせがあった時**: 「いつ・どの画面で」を聞いて川島に LINE で連絡してください。Sentry に届いていない種類の不具合の可能性があります
- **月次レビュー**: 月 1 回 30 分、川島と一緒に Sentry の月次レポートを見て「今月どんなエラーがあったか」「予約フォームの送信成功率」を確認します

---

## §6. 技術詳細（DBA 側実装担当向け）

> ここから先は実装担当向けです。フリーウェイのスタッフは読み飛ばして §10 に進んで構いません。

### 6.1 Sentry SDK の選定

フリーウェイのサイト構成に応じて以下を組み合わせ：

| サイト構成 | 使う SDK | パッケージ |
|---|---|---|
| 静的 HTML / WordPress | Browser SDK | `@sentry/browser` |
| Next.js | Next.js SDK | `@sentry/nextjs` |
| Node.js サーバー | Node SDK | `@sentry/node` |
| Netlify Functions | Serverless SDK | `@sentry/serverless` |

### 6.2 環境分離

- **production**: 本番サイト（dsn 別、エラー通知 ON）
- **preview**: ステージング・PR プレビュー（dsn 別、通知 OFF・観測のみ）
- **development**: ローカル開発（dsn なし、Sentry 完全 OFF）

```ts
// 環境別 DSN 設定例
const dsn = process.env.NODE_ENV === 'production'
  ? process.env.SENTRY_DSN_PRODUCTION
  : process.env.NODE_ENV === 'preview'
  ? process.env.SENTRY_DSN_PREVIEW
  : undefined;
```

### 6.3 段階導入（silent enable パターン）

Basehi.ai の運用で確立した方式。**いきなり通知 ON にしない**。

**Stage 1**: SDK インストール + DSN 設定、ただし `SENTRY_ENABLED=false` で起動
- → イベントは送信されない、設定のみ確認

**Stage 2**: 1 ページのみで `SENTRY_ENABLED=true`、24-48 時間観測
- → PII リーク有無を確認、誤検知パターン把握

**Stage 3**: 全ページに展開、通知 ON
- → 本番運用開始

### 6.4 deepScrub の実装（PII マスキング）

```ts
// src/lib/sentry/scrub.ts
const SENSITIVE_KEYS = [
  'email', 'mail', 'メール',
  'phone', 'tel', '電話',
  'name', 'お名前', '氏名',
  'address', '住所',
  'password', 'pwd', 'パスワード',
  'card', 'credit',
  'cookie', 'authorization', 'token',
];

const EMAIL_RE = /[\w._%+-]+@[\w.-]+\.[A-Za-z]{2,}/g;
const PHONE_RE = /\b0\d{1,4}[-\s]?\d{1,4}[-\s]?\d{3,4}\b/g;
const CARD_RE = /\b(?:\d[ -]*?){13,16}\b/g;

export function deepScrub(obj: unknown, depth = 0): unknown {
  if (depth > 10) return '[MAX_DEPTH]';
  if (obj == null) return obj;
  if (typeof obj === 'string') {
    return obj
      .replace(EMAIL_RE, '[REDACTED-EMAIL]')
      .replace(PHONE_RE, '[REDACTED-PHONE]')
      .replace(CARD_RE, '[REDACTED-CARD]');
  }
  if (typeof obj !== 'object') return obj;
  if (Array.isArray(obj)) return obj.map((v) => deepScrub(v, depth + 1));

  const result: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(obj as Record<string, unknown>)) {
    const keyLower = k.toLowerCase();
    if (SENSITIVE_KEYS.some((s) => keyLower.includes(s))) {
      result[k] = '[REDACTED]';
    } else {
      result[k] = deepScrub(v, depth + 1);
    }
  }
  return result;
}
```

### 6.5 Sentry init での scrub 適用

```ts
// sentry.client.config.ts
import * as Sentry from '@sentry/nextjs';
import { deepScrub } from '@/lib/sentry/scrub';

Sentry.init({
  dsn: process.env.SENTRY_DSN_PRODUCTION,
  enabled: process.env.SENTRY_ENABLED === 'true',
  environment: process.env.NODE_ENV,
  release: process.env.NEXT_PUBLIC_RELEASE_VERSION,

  tracesSampleRate: 0.1,
  replaysSessionSampleRate: 0.0,
  replaysOnErrorSampleRate: 1.0,

  beforeSend(event) {
    if (event.message) event.message = deepScrub(event.message) as string;
    if (event.user) event.user = deepScrub(event.user) as typeof event.user;
    if (event.tags) event.tags = deepScrub(event.tags) as typeof event.tags;
    if (event.extra) event.extra = deepScrub(event.extra) as typeof event.extra;
    if (event.contexts) event.contexts = deepScrub(event.contexts) as typeof event.contexts;
    if (event.breadcrumbs) {
      event.breadcrumbs = event.breadcrumbs.map((b) => deepScrub(b)) as typeof event.breadcrumbs;
    }
    if (event.request) event.request = deepScrub(event.request) as typeof event.request;
    return event;
  },

  beforeBreadcrumb(breadcrumb) {
    return deepScrub(breadcrumb) as typeof breadcrumb;
  },
});
```

### 6.6 PII テスト（必須）

実装後、本番反映前に必ず実行：

```ts
// __tests__/sentry-pii.test.ts
import { deepScrub } from '@/lib/sentry/scrub';

describe('deepScrub', () => {
  test('メールアドレスを REDACTED 化', () => {
    expect(deepScrub('連絡先: test@example.com'))
      .toBe('連絡先: [REDACTED-EMAIL]');
  });

  test('電話番号を REDACTED 化', () => {
    expect(deepScrub('080-1234-5678 まで')).toBe('[REDACTED-PHONE] まで');
    expect(deepScrub('03-1234-5678 です')).toBe('[REDACTED-PHONE] です');
  });

  test('クレジットカード番号を REDACTED 化', () => {
    expect(deepScrub('4111-1111-1111-1111')).toBe('[REDACTED-CARD]');
  });

  test('ネストした user.email も REDACTED', () => {
    const event = { user: { email: 'foo@bar.com', name: '山田' } };
    expect(deepScrub(event)).toEqual({
      user: { email: '[REDACTED]', name: '[REDACTED]' }
    });
  });

  test('フォーム入力データもマスキング', () => {
    const formData = {
      お名前: '山田太郎',
      電話: '090-1234-5678',
      予約日: '2026-06-15',
    };
    const result = deepScrub(formData) as Record<string, unknown>;
    expect(result.お名前).toBe('[REDACTED]');
    expect(result.電話).toBe('[REDACTED]');
    expect(result.予約日).toBe('2026-06-15');
  });
});
```

### 6.7 source map upload

エラーが発生した時、minify されたコードのままだと原因特定が困難。source map を Sentry にアップロードして、本物のソースコードでスタックトレースを見られるようにする。

```yaml
# netlify.toml or build script
[build.environment]
  SENTRY_AUTH_TOKEN = "..." # Netlify 環境変数
  SENTRY_ORG = "dba-japan"
  SENTRY_PROJECT = "freeway-web"

[[plugins]]
  package = "@sentry/netlify-build-plugin"
```

### 6.8 アラート設定

Sentry ダッシュボードで以下のアラートを設定：

| アラート名 | 条件 | 通知先 |
|---|---|---|
| 予約フォーム送信失敗率高 | `tag:form=reservation AND error.rate > 10%` over 15min | LINE + Slack |
| エラー前日比急増 | `event.count` 日次が前日の 5 倍以上 | Slack |
| 新規エラー出現 | `is:unresolved AND age:<1h` | Slack |
| Core Web Vitals 悪化 | LCP > 4s on 25% of sessions | Slack |
| デプロイ後エラー増 | release deploy 後 30 分以内に新規エラー | LINE + Slack |

---

## §7. 予約フォーム特化の監視設計

### 7.1 計測すべきイベント

予約フォーム上で発生する全イベントを Sentry の breadcrumb として記録（個人情報マスキング前提）：

| イベント | 計測タイミング | 記録する情報 |
|---|---|---|
| フォーム表示 | ページ表示時 | ページ URL、ユーザーエージェント |
| フィールド入力開始 | 各 input フォーカス時 | フィールド名のみ（内容は記録しない） |
| バリデーション失敗 | 送信時 | どのフィールドで失敗したか |
| 送信ボタン押下 | submit イベント | タイムスタンプ |
| 送信成功 | API 200 応答時 | レスポンス時間 |
| 送信失敗 | API 4xx/5xx 応答時 | ステータスコード、エラーメッセージ（マスキング後） |
| 完了画面表示 | 完了画面到達時 | 完了までの所要時間 |

### 7.2 Custom transaction での予約フローの可視化

```ts
import * as Sentry from '@sentry/nextjs';

async function submitReservation(formData: ReservationForm) {
  const transaction = Sentry.startTransaction({
    name: 'reservation-submit',
    op: 'form.submit',
  });

  Sentry.getCurrentHub().configureScope((scope) => scope.setSpan(transaction));

  try {
    const span = transaction.startChild({ op: 'validation' });
    validate(formData);
    span.finish();

    const apiSpan = transaction.startChild({ op: 'http.client', description: 'POST /api/reservation' });
    const response = await fetch('/api/reservation', {
      method: 'POST',
      body: JSON.stringify(formData),
    });
    apiSpan.setData('status_code', response.status);
    apiSpan.finish();

    if (!response.ok) {
      throw new Error(`Reservation API failed: ${response.status}`);
    }
  } catch (error) {
    Sentry.captureException(error, {
      tags: { form: 'reservation', flow: 'submit' },
    });
    throw error;
  } finally {
    transaction.finish();
  }
}
```

### 7.3 月次レポート出力

月初に以下のレポートを Sentry から自動生成して小出様に共有：

- 予約フォームの全送信回数
- 送信成功率（目標: 99% 以上）
- 失敗時の主な原因 Top 3
- 平均レスポンス時間
- 新規発生したエラー一覧（解決済み・未解決）

---

## §8. 料金設計

### 8.1 Sentry 料金プラン（2026-05 時点）

| プラン | 月額 | 月間イベント数 | source map | 推奨対象 |
|---|---|---|---|---|
| Developer | 無料 | 5,000 | OK | 検証・最初の 1 ヶ月 |
| Team | $26/月 | 50,000 | OK | フリーウェイ本番運用に推奨 |
| Business | $80/月〜 | 100,000+ | OK | 大規模サイト |

### 8.2 フリーウェイの試算

- 月間予約フォーム送信数の想定: 数百件
- エラー率想定: 1-5%
- → 月間エラーイベント: 数件〜数十件
- → **Developer 無料プランで十分**スタート可能

### 8.3 オプション

- **Performance Monitoring**: トランザクション計測（含む）
- **Session Replay**: エラー時の画面録画（個人情報マスキング前提で慎重に検討）
- **Profiling**: パフォーマンス詳細分析（必要に応じて）

---

## §9. 落とし穴・運用上の注意

Basehi.ai の Sentry 統合（2026-05-28 完了）で得た教訓。

### 9.1 段階導入を絶対省略しない

「動作確認したから一気に本番投入」は禁止。最低 24-48 時間の silent observation を必ず挟む。

**理由**: PII マスキングの設定漏れは、本番投入してから発覚すると個人情報漏洩事故になります。

### 9.2 deepScrub は再帰的に全 field 適用

特定フィールド名だけのマスキングでは漏れます。`message` `user` `tags` `extra` `contexts` `breadcrumbs` `request` の **全 field** に deepScrub を適用する。

### 9.3 環境変数の管理

`SENTRY_DSN` `SENTRY_AUTH_TOKEN` `SENTRY_ENABLED` を Netlify 環境変数で管理。**git に絶対コミットしない**。

### 9.4 source map のアップロード

これがないと、エラーが起きても minify されたコードが見えるだけで原因究明できない。デプロイ時に必ず upload する CI/CD 設定を組む。

### 9.5 自社サイト改修と他施策の同時進行に注意

Sentry でエラー率が下がっても、それが「Sentry 導入で修正が早くなったから」なのか「他の施策（SEO 改善等）で来訪ユーザー層が変わったから」なのか区別困難。**施策の開始日は 2 週間ずらす**（`docs/09_seo_aeo_geo.md` §9 と同様の原則）。

### 9.6 通知疲れ対策

最初は全エラーが通知されてうるさく感じるが、1-2 週間で「無視していい誤検知」が判明する。Sentry の inbox 機能で archive すれば再発時のみ通知される。

---

## §10. フリーウェイ向け 4 週間導入プラン

### 第 1 週（基盤）

- [ ] DBA 側で Sentry アカウント作成・プロジェクト作成
- [ ] DSN 取得・環境変数設定
- [ ] SDK インストール（`SENTRY_ENABLED=false` で起動）
- [ ] PII マスキング（deepScrub）実装 + テスト

### 第 2 週（silent observation）

- [ ] preview 環境のみ `SENTRY_ENABLED=true`
- [ ] 24-48 時間観測
- [ ] PII リーク有無を全 event で確認
- [ ] 誤検知パターンを archive

### 第 3 週（本番投入）

- [ ] production 環境で `SENTRY_ENABLED=true`
- [ ] 予約フォーム特化のアラート設定
- [ ] 通知先を川島 LINE + DBA Slack + 小出様メールに設定
- [ ] 小出様への運用説明（30 分セッション）

### 第 4 週（運用定着）

- [ ] 月次レポートのテンプレ作成
- [ ] フリーウェイ社内の運用フロー確定
- [ ] 初回の月次レビュー実施
- [ ] 改善点を次月にフィードバック

---

## §11. 関連ドキュメント

- `docs/03_security_basics.md`: 個人情報を守る 5 箇条（本書 §4 と整合）
- `docs/09_seo_aeo_geo.md`: SEO/AEO/GEO 教材（Core Web Vitals は Sentry でも計測対象）
- `docs/06_freeway_todo.md`: フリーウェイ向け TODO リスト
- `rules/customer-data-handling.md`: 顧客データ取り扱いルール（厳守）

---

## §12. よくある質問

### Q1. Sentry に送られたデータは消せますか？

A. はい。Sentry ダッシュボードから個別イベント削除・プロジェクト全データ削除が可能。また、データの保管期間は 30 日（デフォルト）。

### Q2. 月額料金を超えたらどうなりますか？

A. 超過分のイベントは Sentry サーバーで rate-limit されて受信されません（料金は発生しない）。ダッシュボードで使用量を常に監視できます。

### Q3. お客様にバレますか？

A. Sentry はサイト訪問者から見えません。バックグラウンドで動く監視ツールなので、訪問者体験に影響はありません（読み込み速度の影響は 1-3KB 程度の追加 JS のみ）。

### Q4. 個人情報漏洩のリスクは本当にゼロですか？

A. ゼロとは言い切れません。設定漏れや新規パターンの個人情報が紛れる可能性は常にあります。だからこそ §4 のマスキング + §9.1 の段階導入を厳守します。万一の漏洩時は速やかに Sentry サポートに削除依頼します。

### Q5. もし Sentry を解約したくなったら？

A. いつでも解約可能。SDK を外せばデータ送信停止。Sentry に蓄積されたデータも削除依頼できます。ベンダーロックインなし。

---

## 改版履歴

| 日付 | 版 | 変更内容 |
|---|---|---|
| 2026-05-28 | v1.0 | 初版。Basehi.ai の Sentry 統合経験（2026-05-28 完走）を Freeway 予約フォーム監視に応用 |
