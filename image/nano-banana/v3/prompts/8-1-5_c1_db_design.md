# 8-1-5_c1: DB設計の基礎

## 対象Section
- Tutorial 8-1-5: データベース設計の基礎（正規化とER図）
- 説明: 正規化とER図の概念を示す概念図

## リサーチメモ
- 正規化: 1NF（1セル1値）→ 2NF（部分依存排除）→ 3NF（推移依存排除）
- ER図: Entity-Relationship Diagram（エンティティ間の関係を可視化）
- IE記法（Information Engineering）: Crow's foot notation（||--o{）
- Chen記法: 菱形で関係を表現（学術的）
- カーディナリティ: 1対1, 1対多, 多対多
- 図解パターン: 左右分割（正規化ステップ | ER図サンプル）
- Sources: [Wikipedia](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model), [Lucidchart](https://www.lucidchart.com/pages/ER-diagram-symbols-and-meaning)

## プロンプト

```
Create a clean, modern educational diagram explaining "Database Design Basics" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with two-part layout
- Colors: 3-color palette (blue for normalization, orange for ER diagram, green for entities)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"データベース設計の基礎" centered at top
Subtitle: "〜正規化とER図〜"

## Elements
Left section: Normalization process
- 第1正規形: 1セル1値
- 第2正規形: 部分依存の分離
- 第3正規形: 推移依存の分離
- Arrow showing progression

Right section: ER diagram basics
- Entity boxes (customers, orders)
- Relationship line with cardinality (1対多)
- Simple IE notation (|| and o{)

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      データベース設計の基礎                          │
│                        〜正規化とER図〜                              │
│                                                                     │
│  【正規化】テーブルを整理整頓              【ER図】設計図             │
│                                                                     │
│  ┌─────────────────────────┐          ┌─────────────────────────┐  │
│  │                         │          │                         │  │
│  │  第1正規形               │          │  ┌─────────────┐        │  │
│  │  ───────────            │          │  │  customers  │        │  │
│  │  1つのマスに1つの値      │          │  │ ─────────── │        │  │
│  │                         │          │  │ id (PK)     │        │  │
│  │          ↓              │          │  │ name        │        │  │
│  │                         │          │  │ email       │        │  │
│  │  第2正規形               │          │  └──────┬──────┘        │  │
│  │  ───────────            │          │         │               │  │
│  │  部分依存をなくす        │          │         │ 1対多         │  │
│  │                         │          │         │ (||--o{)      │  │
│  │          ↓              │          │         ↓               │  │
│  │                         │          │  ┌─────────────┐        │  │
│  │  第3正規形               │          │  │   orders    │        │  │
│  │  ───────────            │          │  │ ─────────── │        │  │
│  │  推移依存をなくす        │          │  │ id (PK)     │        │  │
│  │                         │          │  │ customer_id │        │  │
│  │          ↓              │          │  │ (FK)        │        │  │
│  │                         │          │  │ order_date  │        │  │
│  │  重複なし・一貫性◎       │          │  └─────────────┘        │  │
│  │                         │          │                         │  │
│  └─────────────────────────┘          └─────────────────────────┘  │
│                                                                     │
│  ★ 正規化 = テーブルを適切に分割するルール                           │
│  ★ ER図 = テーブルと関係を可視化した設計図                           │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show 3 normalization forms as steps
- Include simple ER diagram with two entities
- Show cardinality notation (1対多)
- Keep explanations brief and clear
```
