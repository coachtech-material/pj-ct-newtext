# 9-1-3: MVCアーキテクチャ（ハイブリッドv2）

**テンプレート**: ハイブリッド | **ステータス**: テスト中

## リサーチ結果

**検索キーワード**: MVC アーキテクチャ 図解 / MVC diagram standard layout

**標準的な構図パターン**:
- Controller が中央上部（ハブ役・司令塔）
- View（左下）と Model（右下）は Controller 経由でやり取り
- User/Browser は左端、Database は右端（Model と接続）
- View ↔ Model は直接やり取りしない（重要）

**参考**: [freeCodeCamp](https://www.freecodecamp.org/news/model-view-architecture/), [Wikipedia](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)

---

## プロンプト本文

```
MVCアーキテクチャ（Model-View-Controller）の役割分担を技術図解として描いてください。

## 構成要素（5つのボックス）

【User】左端
- パソコン/ブラウザのアイコン（🌐）
- シンプルな四角形

【Routing】オレンジ色ボックス
- ラベル: 「Routing」（大きく）
- サブラベル: 「振り分け」
- コード例: web.php

【Controller】青色ボックス（中央・最も大きく）
- ラベル: 「Controller」（最も大きく・太く）
- サブラベル: 「司令塔」
- コード例: UserController
- ※図の中心に配置し、視覚的に強調

【Model】緑色ボックス（右上）
- ラベル: 「Model」（大きく）
- サブラベル: 「データ処理」
- コード例: User::all()
- 隣にDatabase（円筒形💾）を配置

【View】ピンク/紫色ボックス（右下）
- ラベル: 「View」（大きく）
- サブラベル: 「表示」
- コード例: index.blade.php

## データフロー（番号付き矢印・太め）

① User → Routing（リクエスト）
② Routing → Controller（振り分け）
③ Controller → Model（データ要求）
④ Model ↔ Database（データ取得/保存）
⑤ Model → Controller（データ返却）
⑥ Controller → View（データ渡し）
⑦ View → User（画面表示/レスポンス）

## 重要ポイント
- View と Model は直接やり取りしない（必ず Controller 経由）
- Controller が中心的存在であることを視覚的に強調
- 各要素の技術用語（Routing, Controller, Model, View）を大きく太い文字で描く
- 矢印は太めで番号付き（①〜⑦）、方向が明確

## スタイル
- 技術図解として見やすい構成
- 背景は白または薄いグレー
- 色分け: Routing=オレンジ, Controller=青, Model=緑, View=ピンク
- 全体的にプロフェッショナルで教材向けの印象

タイトル: 「MVCアーキテクチャ」
```

## 構図イメージ（ASCIIアート）

```
┌───────────────────────────────────────────────────────────────────────┐
│                     「MVCアーキテクチャ」                               │
│                                                                       │
│                                          ┌─ Model ─────────┐  ┌──────┐│
│                                    ③→   │    緑色          │  │  💾  ││
│                                   ←⑤    │ 「データ処理」   │←④→│  DB  ││
│                                          │  User::all()    │  └──────┘│
│  ┌────┐  ①   ┌─ Routing ─┐  ②  ┌─ Controller ─┐  └─────────────────┘         │
│  │ 🌐 │ ──→ │  オレンジ  │ ──→ │    青色       │                            │
│  │User│      │ 「振り分け」│     │  「司令塔」   │  ┌─ View ─────────┐        │
│  └────┘      │  web.php   │      │ UserController│  │   ピンク        │        │
│      ↑       └────────────┘      └───────┬───────┘  │ 「表示」        │        │
│      │                                   │ ⑥→      │ index.blade.php │        │
│      └─────────────────────────⑦─────────┴─────────→└─────────────────┘        │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

## 挿入情報

- ファイル: `curriculums/tutorial-9.../chapter-1.../9-1-3_mvc_architecture.md`
- 挿入位置: 「🔄 注文から料理が届くまでの流れ」の直後（L122付近）
- 画像ファイル名: `9-1-3_c1.png`

## 確認項目

- [ ] 技術用語のラベルが正確か（Routing, Controller, Model, View, Database）
- [ ] フローの番号（①〜⑦）が正しい順序で全て見えるか
- [ ] Controllerが図の中央に最も大きく配置されているか
- [ ] 各ボックスにコード例が含まれているか
- [ ] View と Model が直接接続されていないか（Controller 経由のみ）
