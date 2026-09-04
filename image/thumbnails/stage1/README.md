# Stage 1 追加教材のサムネイル

Stage 1 で新設した Tutorial 13〜16 のカリキュラム一覧用サムネイル。規格は既存 v2〜v4 と同じ **1264×848（3:2）**。

## どれが権威か

**配布物は `output/*.png`、その生成元は `html/*.html`。** PNG を直接編集せず、HTML を直して再生成する。

`prompts/*.md` は**画像生成AIで作り直す場合の指示書**で、既存 v2〜v4 と様式を揃えるために残している。HTML から派生させた仕様の記述であり、PNG の生成元ではない。デザインを変えるときは HTML を正として、必要なら prompts も追従させる。

## 構成

| ファイル | 内容 |
|---|---|
| `output/t13.png` | システム設計（Tutorial13） |
| `output/t14.png` | AI駆動開発（Tutorial14） |
| `output/t15.png` | 開発の仕組み化（Tutorial15） |
| `output/t16.png` | 総合アプリケーション開発（Tutorial16）※ `../v4/output/t13.png` の複製 |
| `html/base.css` | 3枚共通のレイアウト（枠・ドットグリッド・タイトル） |
| `html/t1{3,4,5}.html` | 各サムネイルのテーマカラーと中央ビジュアル |
| `prompts/t1{3,4,5}.md` | 画像生成AI用のプロンプト |

### t16 が複製である理由

新 Tutorial16「総仕上げ！学んだ技術をフル活用してアプリケーションを作ってみよう🔥」は、旧 Tutorial13 と**同じ位置づけの総仕上げ教材**なので、旧 Tutorial13 用に作った「総合アプリケーション開発」（`v4/output/t13.png`）をそのまま流用している。

ただし LMS 上では旧 Tutorial13 も併存し続けるため、**両方に同じ絵柄を設定すると一覧で見分けがつかない**。旧 Tutorial13 側には別のアイキャッチを当てるか、そもそも設定しない運用にするかを公開前に決めること。

## 再生成のしかた

Chrome のヘッドレスでスクリーンショットを撮る（画像生成AIは「四隅を直角に」「枠を極太に」といった指示を守りきらないため、HTML で作図している）。

```bash
cd image/thumbnails/stage1
for n in 13 14 15; do
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu --hide-scrollbars --allow-file-access-from-files \
    --force-device-scale-factor=1 --window-size=1264,848 \
    --screenshot="output/t${n}.png" \
    "file://$(pwd)/html/t${n}.html"
done
```

## テーマカラー

既存13枚と重複しない色域を選んでいる。

| 教材 | 色 | 既存との関係 |
|---|---|---|
| T13 システム設計 | `#455A64` ブルーグレー | 未使用の色域。製図・設計図の質感 |
| T14 AI駆動開発 | `#D97757` コーラル | 既存の赤（`#FF5252` / `#EF5350`）と色相・彩度が異なる |
| T15 開発の仕組み化 | `#7E57C2` パープル | 既存の薄紫（`#9FA8DA` PHP入門）より濃く、混同しない |
| T16 総合開発 | `#D4A017` ゴールド | v4 から流用 |

## LMS への反映

同期（`POST /deploy/sections/upsert`）は**アイキャッチを空で登録し、既存レコードのアイキャッチは上書きしない**。よってこれらの画像は**管理画面から手動でアップロードする**。公開オペレーション（アイキャッチ設定 → 表示順 → 章の一括公開 → 教材の公開）の最初のステップに当たる。
