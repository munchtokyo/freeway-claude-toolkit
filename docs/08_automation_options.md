# 自動化の選択肢: Google 環境 vs Microsoft 環境

> ⚠️ 川島の整理による叩き台です。実装は皆様が `/skill-creator` で作る前提。**どちらの環境を選ぶかは皆様の判断**。「やりたいことは変わらない、環境はどちらでもいい」が川島さんの基本方針。

---

## 「予約の一連の流れ」の本質

フリーウェイの最大ペインは予約処理から前日連絡までの**一連の手作業**。

```
予約発生 (HP / 電話 / 口頭 / 個人 LINE / じゃらん)
  ↓ 【手入力】
Excel 月別ファイル × 日別シート
  ↓ 【手入力】
カレンダー (頭の中 or 別途)
  ↓ 【手作業】
お客様へメール / 電話で集合場所・時間案内
  ↓ 【手作業】
当日対応
```

**この流れを半自動化する**ことが目的。
Google でやろうが Microsoft でやろうが、**やりたいことは同じ**:

1. 予約データの **集約**
2. Excel への **自動入力**
3. **PDF 生成**
4. お客様へ **メール / LINE 送信**
5. **カレンダー反映**

---

## A. Google 環境で半自動化するパターン

すでに freeway-demo (営業用 Web サイト・50 ページ・3 言語) では実装済みの方式。

```
予約フォーム (HP)
  ↓ Netlify Forms
GAS POST
  ↓ Google Sheets に自動記録
  ↓ Apps Script でトリガー
PDF 生成 (Google Docs テンプレ)
  ↓ メール / LINE Messaging API
顧客 + 店舗に通知
  ↓ Google Calendar API
来店予定日に自動登録
```

### Google 環境のメリット
- 既存 freeway-demo に組み込み済み (動作実績あり)
- GAS は無料・上限緩い
- どの PC からでもブラウザでアクセス可
- スマホでも見られる

### Google 環境のデメリット
- フリーウェイは Google Workspace 未導入
- 個人 Gmail / 個人 Google アカウントを業務に使うのは推奨されない
- 既存業務 (Outlook / Excel 月別ファイル) と二重管理になる

---

## B. Microsoft 環境で半自動化するパターン

フリーウェイの**現状資産を生かす**方式。

```
予約フォーム (HP)
  ↓ Power Automate or Excel COM API (pywin32)
Excel 月別ファイルに自動入力
  ↓ Excel マクロ / Power Automate
PDF 生成 (Word テンプレ)
  ↓ Outlook COM (pywin32) / Power Automate
顧客 + 店舗に Outlook メール
  ↓ Outlook カレンダー API
来店予定日に自動登録
```

### Microsoft 環境のメリット
- **現状資産 (Excel・Outlook) を生かしたまま** 自動化できる
- 顧客データの居場所が変わらない → スタッフの慣れを壊さない
- Microsoft 365 サブスクは既に支払い済み (個人プランで Power Automate Free を使う前提だが要確認)
- 日本企業の伝統業務環境と相性が良い

### Microsoft 環境のデメリット
- Power Automate の有料機能を使う場合、月額数百円〜数千円かかる可能性
- Excel COM API は Windows 専用 (Mac では動かない)
- 実装事例が Google 系より少ない

---

## C. ハイブリッド (両環境の良いとこ取り)

予約フォームのバックエンドだけ Google、業務本体は Excel という形も可能。

```
予約フォーム → Google Sheets (一時バッファ)
  ↓ Claude Code (Python) で取得
Excel 月別ファイルに反映 (pywin32)
  ↓ Outlook で連絡
```

→ **「予約取り込みは Google、業務本体は Excel」** の二刀流。
既存業務環境を壊さず、フォーム連携の便利さも享受できる。

---

## どう決めるか

訪問中の対話で**皆様が決める**。判断材料:

| 質問 | YES なら Microsoft 側 | YES なら Google 側 |
|---|---|---|
| 既存 Excel 月別ファイル運用を変えたくない | ✓ | |
| スタッフ全員が新しいツール操作を覚えるのは負担 | ✓ | |
| 既に GAS で予約フォーム連携が動いている | | ✓ |
| スマホでデータ見たい | | ✓ |
| 月額固定費を増やしたくない | △ (Power Automate Free 限界あり) | ✓ (GAS 無料) |
| Excel の使い心地が好き | ✓ | |
| Google Calendar をすでに使っている | | ✓ |

---

## Claude Code の役割 (どちらの環境でも変わらない)

どちらを選んでも、Claude Code の役割は同じ:

1. **データ取得**: HP フォーム / LINE スクショ OCR / じゃらん CSV から構造化データを抽出
2. **データ整形**: 重複チェック・必須項目チェック・既存顧客マッチング
3. **下書き生成**: メール / LINE / 電話原稿 / PDF 自動生成
4. **カレンダー反映**: 来店日・休業日のイベント登録
5. **暗黙知蓄積**: 顧客カルテ・講師相性の継続記録
6. **自走支援**: 「これ毎週やってるからスキル化しませんか」を提案

つまり Claude Code は**環境非依存**で、Google でも MS でも動く。
皆様が **どちらの環境で業務するかを決めれば、Claude Code がそれに合わせて動く**。

---

## 5/28-31 訪問中の確認事項

1. フリーウェイの Microsoft 365 サブスク状況 (Power Automate Free が使えるか)
2. freeway-demo の GAS 連携の現状 (どこまで動いているか・じゃらん連携の実態)
3. 「Excel 月別ファイルを残す前提か / 別運用に移行するか」の皆様の感覚
4. Outlook と HP メールの使い分け (freeway@cocos.ocn.ne.jp は Outlook で受信?)
5. スマホ業務の必要性 (現場でスマホ見るシーンはあるか)

これらを確認した上で、A / B / C のどれを軸にするか決める。
