# 9-1-3: MVCアーキテクチャ（v2簡潔版）

## プロンプト本文

```
プログラミング教材向けの技術図解「MVCアーキテクチャ」を作成してください。

【配置】横長レイアウト（16:9）、白背景、プロフェッショナルな技術図解スタイル

【構成要素】
- User（左端）: 水色ボックス、パソコンアイコン
- Routing（上部）: オレンジボックス、「振り分け」、web.php
- Controller（中央・最大）: 青色ボックス、「司令塔」、UserController
- Model（右下）: 緑色ボックス、「データ処理」、User::all()、隣にDatabase円筒
- View（右）: ピンクボックス、「表示」、index.blade.php

【データフロー】番号付き太矢印で描く
①User→Routing ②Routing→Controller ③Controller→Model ④Model↔Database ⑤Model→Controller ⑥Controller→View ⑦View→User

【重要】
- Controllerを最も大きく中央に配置
- ViewとModelは直接接続しない
- 技術用語（CONTROLLER等）は大きく太い英字
- 凡例を右下に表示

【避ける】複雑な装飾、ごちゃごちゃした背景、ViewとModelの直接接続
```
