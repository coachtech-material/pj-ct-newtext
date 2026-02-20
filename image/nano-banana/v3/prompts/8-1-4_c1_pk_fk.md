# 8-1-4_c1: 主キーと外部キー

## 対象Section
- Tutorial 8-1-4: 主キー（Primary Key）と外部キー（Foreign Key）
- 説明: PK/FKによるテーブル間の関連付けを示す概念図

## リサーチメモ
- ER図での標準的な表記: 実線で接続、PK/FK属性をラベル
- 実線 = 識別関係（identifying relationship）
- 点線 = 非識別関係（non-identifying relationship）
- Crow's foot記法: 直感的で最も広く使用される
- 4種類のカーディナリティ: 1対1、1対多、多対1、多対多
- ツール: Lucidchart, Creately, dbdiagram.io
- Sources: [Lucidchart](https://www.lucidchart.com/pages/ER-diagram-symbols-and-meaning), [Creately](https://creately.com/guides/foreign-key-in-er-diagram/), [Codefinity](https://codefinity.com/courses/v2/5ac24d9d-4a16-45b3-8856-07dec028c5e9/3d6c4ab0-f470-4b5d-ad0e-5f76d28ca0af/0b84a806-5981-44fa-b3e7-e3279b0ab8e5)

## プロンプト

```
Create a clean, modern educational diagram explaining "Primary Key and Foreign Key" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with table relationship visualization
- Colors: 3-color palette (blue for PK, orange for FK, green for connection)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"主キーと外部キー" centered at top
Subtitle: "〜テーブルをつなぐ仕組み〜"

## Elements
Left: Parent table (customers) with Primary Key highlighted
- PK column marked with key icon
- Label: "主キー（PK）= 背番号"

Right: Child table (orders) with Foreign Key highlighted
- FK column marked with link icon
- Label: "外部キー（FK）= 参照"

Arrow connecting PK to FK

## Rules
- PK: 重複不可、NULL不可
- FK: 親テーブルに存在する値のみ

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                        主キーと外部キー                              │
│                      〜テーブルをつなぐ仕組み〜                        │
│                                                                     │
│      【親テーブル: customers】         【子テーブル: orders】         │
│                                                                     │
│      ┌───────────────────────┐      ┌───────────────────────┐     │
│      │ 🔑 id │ name  │ email │      │ id │ date │ 🔗customer_id│    │
│      │   (PK)│       │       │      │(PK)│      │    (FK)      │    │
│      ├───────┼───────┼───────┤      ├────┼──────┼──────────────┤    │
│      │   1   │ 山田  │ @...  │←────┤ 101│10/26 │      1       │    │
│      │   2   │ 鈴木  │ @...  │←────┤ 102│10/27 │      2       │    │
│      │   3   │ 佐藤  │ @...  │←────┤ 103│10/28 │      1       │    │
│      └───────────────────────┘      └───────────────────────────┘   │
│                                                                     │
│    ┌─────────────────────────────────────────────────────┐         │
│    │                                                     │         │
│    │  🔑 主キー（PK）              🔗 外部キー（FK）      │         │
│    │  ────────────────            ────────────────────   │         │
│    │  • 背番号のようなもの         • 他テーブルのPKを参照  │         │
│    │  • 重複不可                  • 参照先に存在する値のみ│         │
│    │  • NULL不可                  • 「関係」を作る        │         │
│    │                                                     │         │
│    └─────────────────────────────────────────────────────┘         │
│                                                                     │
│    ★ PK = 「私はID 1の山田です」と名乗る                             │
│    ★ FK = 「この注文はID 1の山田さんからです」と指し示す              │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show two tables with clear PK and FK columns
- Use arrows to show the reference relationship
- Explain rules for each key type
- Use metaphor: PK = ID badge, FK = pointer
```
