# 9-1-4: ルーティング基礎

**Gem**: v4.1 | **テンプレート**: シンプル図解 | **ステータス**: テスト用

## プロンプト本文

```
Laravelのルーティングを、シンプルな教育インフォグラフィックとして図解してください。

## デザインスタイル
- 明るいクリーム色の背景
- カラフルな紙吹雪風の装飾枠（四隅に星・丸・リボン）
- 色分けされた要素
- 太い矢印で流れを表現

## タイトル（上部中央・大きく）
「ルーティング（Routing）」
サブタイトル: 「URLとControllerをつなぐ道案内」

## メイン構成

【左側】リクエスト
- ブラウザのアイコン 🌐
- URL例: `/users`
- ラベル: 「どこに行けばいい？」

【中央・大きく強調】routes/web.php - 緑色の看板風ボックス
- 道路標識のアイコン 🪧
- テーブル形式で表示:
  | URL | → | Controller |
  |-----|---|------------|
  | /users | → | UserController |
  | /tasks | → | TaskController |
  | /about | → | PageController |
- 強調: 「ここで行き先を決める！」

【右側】Controller（目的地）
- 建物アイコン 🏢
- UserController
- TaskController
- PageController
- ラベル: 「目的地に到着！」

## 矢印フロー（左→中央→右）
① /users リクエスト →（青矢印）→ routes/web.php
② routes/web.php →（緑矢印）→ UserController

## 下部にポイント（1行で）
「routes/web.php = URLと処理先の対応表（道案内役）」

## キャラクター（右下に小さく1人）
- シンプルなイラスト調の開発者
- 吹き出し:「URLを見て振り分け！」
```
