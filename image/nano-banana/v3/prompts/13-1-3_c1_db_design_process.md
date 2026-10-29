# 13-1-3_c1: DB設計プロセス

## 対象Section
- Tutorial 16-1-3: DB設計
- 説明: エンティティ抽出からテーブル設計までの4ステップを示す概念図

## リサーチメモ
- DB設計プロセス: 要件 → 概念設計（ER図） → 論理設計 → 物理設計
- 4ステップ: エンティティ抽出 → リレーションシップ定義 → ER図作成 → テーブル設計
- ER図: Entity-Relationship Diagram（エンティティ間の関係を視覚化）
- 1対多リレーションシップ: 外部キー（FK）で表現
- Sources: [Lucidchart](https://www.lucidchart.com/pages/er-diagrams), [Visual Paradigm](https://www.visual-paradigm.com/guide/data-modeling/what-is-entity-relationship-diagram/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Database Design Process" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic showing 4-step process
- Colors: 4-color palette (blue for entities, orange for relationships, green for ER diagram, purple for table design)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"データベース設計の流れ" centered at top
Subtitle: "〜要件からテーブル設計へ〜"

## Layout
4 steps in horizontal flow with example at bottom

## Elements

### 4-Step Process
① エンティティの抽出
   - User, Task, Category を特定

② リレーションシップの定義
   - User → Task (1対多)
   - Category → Task (1対多)

③ ER図の作成
   - 視覚的に構造を確認

④ テーブル設計
   - カラム、データ型、制約を決定

### Example ER Diagram
[users] ─1:多─→ [tasks] ←─1:多─ [categories]

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      データベース設計の流れ                          │
│                       〜要件からテーブル設計へ〜                       │
│                                                                     │
│  【4ステップの流れ】                                                 │
│                                                                     │
│  ① エンティティの     ② リレーション      ③ ER図の        ④ テーブル  │
│     抽出                シップの定義          作成             設計     │
│  ┌──────────┐      ┌──────────┐      ┌──────────┐     ┌──────────┐│
│  │ 機能要件  │  →   │ 関係を    │  →   │ 視覚的に  │  →  │ カラム   ││
│  │ から抽出  │      │ 定義する  │      │ 確認する  │     │ データ型 ││
│  └──────────┘      └──────────┘      └──────────┘     │ 制約を定義││
│                                                        └──────────┘│
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【具体例：タスク管理アプリ】                                         │
│                                                                     │
│  ① 抽出したエンティティ                                              │
│                                                                     │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐                        │
│  │   User   │   │   Task   │   │ Category │                        │
│  │ユーザー  │   │  タスク  │   │カテゴリー │                        │
│  └──────────┘   └──────────┘   └──────────┘                        │
│                                                                     │
│  ② リレーションシップ                                                │
│                                                                     │
│  User ────1:多────→ Task ←────1:多──── Category                     │
│  「1人のユーザーは       「1つのカテゴリーには                         │
│   複数のタスクを持つ」    複数のタスクが属する」                       │
│                                                                     │
│  ③ ER図（外部キー）                                                  │
│                                                                     │
│  [users]                  [tasks]                 [categories]      │
│    id (PK)                  id (PK)                  id (PK)        │
│    name                     user_id (FK) ────→       name           │
│    email                    category_id (FK) ←────                  │
│                             title                                   │
│                                                                     │
│  ④ テーブル設計                                                      │
│  ┌──────────┬──────────┬──────────┐                                │
│  │ カラム名  │ データ型  │ 制約      │                                │
│  ├──────────┼──────────┼──────────┤                                │
│  │ user_id  │ BIGINT   │ FK, NOT NULL │                            │
│  │ title    │ VARCHAR  │ NOT NULL │                                │
│  │ priority │ TINYINT  │ DEFAULT 2│                                │
│  └──────────┴──────────┴──────────┘                                │
│                                                                     │
│  ★ データ構造を先に決める → マイグレーション・モデル設計がスムーズに   │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show 4 clear steps in order
- Use task management app as concrete example
- Show 1:many relationships visually
- Include PK (Primary Key) and FK (Foreign Key) notation
- Emphasize: decide data structure before coding
```

