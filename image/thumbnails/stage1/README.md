# Stage 1 追加教材のサムネイル

Stage 1 で新設した Tutorial 13〜16 のカリキュラム一覧用サムネイル。規格は既存 v2〜v4 と同じ **1264×848（3:2）**、様式も踏襲している（白面＋四辺の極太テーマカラー帯／中央に主役ビジュアル／下部に太字ゴシックのタイトル／右上・左下にドットグリッド）。

## どれが権威か

**配布物は `output/*.png`、その生成元は `html/*.html`。** PNG を直接編集せず、HTML を直して再生成する。

`prompts/*.md` は**画像生成AIで作り直す場合の指示書**で、既存 v2〜v4 と様式を揃えるために残している。HTML から派生させた仕様の記述であり、PNG の生成元ではない。デザインを変えるときは HTML を正とし、prompts を追従させる。

## 構成

| ファイル | 内容 | テーマカラー |
|---|---|---|
| `output/t13.png` | システム設計（Tutorial13） | `#455A64` ブルーグレー |
| `output/t14.png` | AI駆動開発（Tutorial14） | `#D97757` コーラル |
| `output/t15.png` | 開発の仕組み化（Tutorial15） | `#7E57C2` パープル |
| `output/t16.png` | 総合アプリケーション開発（Tutorial16） | `#D4A017` ゴールド |
| `html/base.css` | 4枚共通のレイアウト（枠・ドットグリッド・タイトル） | — |
| `html/t1{3,4,5,6}.html` | 各サムネイルのテーマカラーと中央ビジュアル | — |
| `html/logos/*.svg` | ブランドロゴ（simple-icons 由来） | — |
| `prompts/t1{3,4,5,6}.md` | 画像生成AI用のプロンプト | — |

テーマカラーは既存13枚が使っていない色域から選んでいる（既存は緑 `#66BB6A` / 青 `#42A5F5` / Git橙 `#F05032` / Docker青 `#2496ED` / 薄紫 `#9FA8DA` / 濃青 `#0277BD` / 赤 `#FF5252` / ティール `#26A69A` / 橙 `#FFA726` を使用済み）。

## Tutorial16 と旧 Tutorial13 の区別

新 Tutorial16 は旧 Tutorial13 と**同名の総仕上げ教材**だが、LMS 上では旧 Tutorial13 がアーカイブとして残り続けるため、一覧に2つ並ぶ。

**旧 Tutorial13 のアイキャッチは変更しない方針**なので、区別は新 Tutorial16 側で作っている。旧 Tutorial13 のサムネイル（Laravel・Docker・MySQL・GitHub の4ロゴ／`../v4/output/t13.png`）に対し、新 Tutorial16 は**中心に Claude を据えた5要素の構図**にした。「学んだ技術を AI とともに統合する」という新カリキュラムの主題とも一致する。

## 再生成のしかた

Chrome のヘッドレスでスクリーンショットを撮る。画像生成AIは「四隅を直角に」「枠を極太に」「枠の外に余白を入れない」といった指示を守りきらないため、HTML で作図している（既存プロンプトにこれらの厳守事項が並んでいるのはその苦労の跡）。

```bash
cd image/thumbnails/stage1
for n in 13 14 15 16; do
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu --hide-scrollbars --allow-file-access-from-files \
    --force-device-scale-factor=1 --window-size=1264,848 \
    --screenshot="output/t${n}.png" \
    "file://$(pwd)/html/t${n}.html"
done
```

`html/logos/` のブランドロゴは [simple-icons](https://github.com/simple-icons/simple-icons) から取得したもの。取り直す場合:

```bash
cd image/thumbnails/stage1/html/logos
for n in claude laravel docker github; do
  curl -sS -o "$n.svg" "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons/$n.svg"
done
```

MySQL は simple-icons のものがロゴタイプ（"MySQL" の文字）入りで他と揃わないため、`t16.html` 内でデータベースの円柱を自前で描いている。

## LMS への反映

同期（`POST /deploy/sections/upsert`）は**アイキャッチを空で登録し、既存レコードのアイキャッチは上書きしない**。よってこれらの画像は**管理画面から手動でアップロードする**。公開オペレーション（アイキャッチ設定 → 表示順 → 章の一括公開 → 教材の公開）の最初のステップに当たる。
