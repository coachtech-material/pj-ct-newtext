# 13-4-1_c1: マイグレーション作成

## 対象Section
- Tutorial 16-4-1: マイグレーション作成
- 説明: テーブル作成順序と外部キー制約の概念図

## リサーチメモ
- 外部キー制約: 参照先テーブルを先に作成する必要がある
- 作成順序: 親テーブル → 子テーブル（外部キーを持つ側）
- 今回の順序: users → categories → tasks
- tasksがuser_idとcategory_idで両テーブルを参照
- Webでよく使われる構図: テーブル間の参照関係を矢印で示す

## プロンプト

```
Create a clean, modern educational diagram explaining "Migration Order for Foreign Keys" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Table creation order with arrows showing dependencies
- Colors: Blue for users, Orange for categories, Green for tasks
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"マイグレーションの作成順序" centered at top
Subtitle: "〜外部キーの参照先を先に作成する〜"

## Layout
Show 3 tables in creation order: 1→2→3
Arrows showing foreign key references

## Elements

### Step 1: users table (blue)
- First to create (no dependencies)
- id (PK), name, email, password
- Label: ① 最初に作成

### Step 2: categories table (orange)
- Second to create
- id (PK), name
- Label: ② 次に作成

### Step 3: tasks table (green)
- Last to create (has foreign keys)
- id, user_id (FK), category_id (FK), title
- Arrows pointing to users.id and categories.id
- Label: ③ 最後に作成

### Why box
- Reason: 外部キーは参照先が存在しないと作成できない
- ❌ tasks → users (usersがない！) エラー
- ✅ users → tasks (usersがある) OK

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                    マイグレーションの作成順序                         │
│                 〜外部キーの参照先を先に作成する〜                    │
│                                                                     │
│   作成順序 ①→②→③                                                   │
│                                                                     │
│   ① users          ② categories        ③ tasks                    │
│   ┌──────────┐     ┌──────────┐       ┌─────────────────┐         │
│   │ id (PK)  │     │ id (PK)  │       │ id              │         │
│   │ name     │←────│ name     │←──────│ user_id (FK) ───┼─→①参照  │
│   │ email    │     └──────────┘       │ category_id(FK)─┼─→②参照  │
│   │ password │                        │ title           │         │
│   └──────────┘                        └─────────────────┘         │
│       ↑                  ↑                    ↑                    │
│    親テーブル          親テーブル            子テーブル              │
│   （参照される）      （参照される）       （外部キーを持つ）          │
│                                                                     │
│   【なぜ順序が重要？】                                               │
│   ┌─────────────────────────────────────────────────────┐          │
│   │ ❌ tasks → users の順で作成しようとすると…            │          │
│   │    「usersテーブルがない！」エラー                    │          │
│   │                                                     │          │
│   │ ✅ users → categories → tasks の順なら OK            │          │
│   │    外部キーの参照先が存在する                        │          │
│   └─────────────────────────────────────────────────────┘          │
│                                                                     │
│   ★ 外部キーを持つテーブルは、参照先テーブルの後に作成する            │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show 3 tables with creation order numbers (①②③)
- Show FK arrows from tasks to users and categories
- Explain why order matters (reference must exist)
- Use parent/child table labels
```
