# 8-1-2_c1: RDBの概念

## 対象Section
- Tutorial 8-1-2: リレーショナルデータベースの概念
- 説明: テーブル分割と関係性（リレーション）を示す概念図

## リサーチメモ
- RDB (Relational Database): テーブル間をキーで関連付けるデータベース
- 正規化: 冗長性を取り除くためにテーブルを分割（1NF → 2NF → 3NF）
- Primary Key (PK): テーブル内でレコードを一意に識別
- Foreign Key (FK): 他テーブルのPKを参照して関係を構築
- JOIN: 分割されたテーブルをキーを使って結合
- 図解パターン: Before（重複あり）→ After（分割後）の比較が効果的
- Sources: [Visual Paradigm](https://www.visual-paradigm.com/guide/data-modeling/what-is-entity-relationship-diagram/), [GeeksforGeeks](https://www.geeksforgeeks.org/dbms/introduction-of-er-model/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Relational Database Concept" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with before/after comparison
- Colors: 4-color palette (red for problem, blue for customers, orange for orders, green for products)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"リレーショナルデータベース" centered at top
Subtitle: "〜テーブル分割と関係性〜"

## Elements
Top: Bad example (one giant table with duplicates)
- Label: "❌ 1枚の巨大シート（問題あり）"
- Show repeated data (same customer info multiple times)

Bottom: Good example (separated tables with relationships)
- customers table (blue)
- orders table (orange)
- products table (green)
- Lines connecting via IDs

## Problem indicators
- データの重複
- 更新の手間

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                    リレーショナルデータベース                         │
│                     〜テーブル分割と関係性〜                          │
│                                                                     │
│  ❌ 1枚の巨大シート（問題あり）                                       │
│  ┌──────────────────────────────────────────────────────┐          │
│  │注文ID│ 顧客名    │ メール       │ 商品名 │ 単価 │ 数量│          │
│  │ 101  │ 山田太郎  │taro@...     │ りんご │ 150 │  3 │          │
│  │ 101  │ 山田太郎  │taro@...     │ みかん │ 100 │  5 │ ←重複!   │
│  │ 102  │ 鈴木花子  │hanako@...   │ ぶどう │ 500 │  1 │          │
│  └──────────────────────────────────────────────────────┘          │
│                                                                     │
│                        ▼ テーブルを分割 ▼                           │
│                                                                     │
│  ✅ 関係で繋がった複数のテーブル                                      │
│                                                                     │
│  【顧客テーブル】      【注文テーブル】      【商品テーブル】          │
│  ┌────────────┐      ┌────────────┐      ┌────────────┐          │
│  │ id │ 顧客名 │      │注文ID│顧客ID│      │ id │ 商品名 │          │
│  │  1 │ 山田   │←────│ 101 │  1   │────→│ P01│ りんご │          │
│  │  2 │ 鈴木   │←────│ 102 │  2   │      │ P02│ みかん │          │
│  └────────────┘      └────────────┘      └────────────┘          │
│                                                                     │
│  ★ 正規化: テーブルを分割して重複をなくす                             │
│  ★ JOIN: IDを使って元の情報を復元する                                │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show problem of duplication clearly
- Demonstrate table separation solution
- Use connecting lines between related IDs
- Mention "正規化" and "JOIN" as key concepts
```
