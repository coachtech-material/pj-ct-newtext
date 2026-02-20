# 9-1-3: MVCアーキテクチャ

## プロンプト本文

```
Create an educational flowchart diagram explaining Laravel's MVC (Model-View-Controller)
architecture for programming beginners.

Layout: Horizontal flow from left to right on a white background.

The flow starts with a "ユーザー" icon (a person silhouette) on the far left,
who sends a "リクエスト" arrow to a box labeled "ルーティング (routes/web.php)".

From ルーティング, an arrow flows right to a large rounded rectangle labeled
"コントローラー (Controller)" in orange.
Inside this box, show a small gear icon and the text "リクエストを受け取り処理を振り分ける".

From the Controller, two arrows branch:
- One arrow goes DOWN to a rounded rectangle labeled "モデル (Model)" in blue,
  with a small database icon and text "データの取得・保存・バリデーション".
  Below the Model box, show a cylinder labeled "データベース (MySQL)" connected
  with a bidirectional arrow.
- One arrow goes UP to a rounded rectangle labeled "ビュー (View)" in green,
  with a small browser icon and text "Bladeテンプレートで画面を生成".

From the Model, a return arrow goes back up to the Controller labeled "データ".
From the Controller, an arrow goes to the View labeled "データを渡す".
From the View, a final arrow goes right back to the ユーザー labeled "レスポンス (HTML)".

Style: Clean, modern flat design with soft pastel colors (light orange, light blue,
light green). Rounded corners on all boxes. Clear, legible Japanese text.
Arrows are dark gray with labels. No 3D effects.
Format: 16:9
```
