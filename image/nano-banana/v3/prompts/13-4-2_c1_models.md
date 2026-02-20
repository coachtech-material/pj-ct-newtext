# 13-4-2_c1: モデルとリレーション

## 対象Section
- Tutorial 13-4-2: モデル作成とリレーション定義
- 説明: hasMany/belongsToのリレーション定義の概念図

## リサーチメモ
- モデル = テーブルとPHPコードをつなぐ
- リレーション定義:
  - hasMany(): 1対多の「1」側（親→子）
  - belongsTo(): 1対多の「多」側（子→親）
- 今回の構造:
  - User hasMany Tasks
  - Category hasMany Tasks
  - Task belongsTo User, Category
- $user->tasks でタスク一覧取得、$task->user で作成者取得

## プロンプト

```
Create a clean, modern educational diagram explaining "Eloquent Relations (hasMany/belongsTo)" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Model relationship diagram with method labels
- Colors: Blue for User, Orange for Category, Green for Task
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"リレーションの定義" centered at top
Subtitle: "〜hasMany と belongsTo〜"

## Layout
Center: Three models connected with relationship arrows
Show method names and access syntax

## Elements

### User Model (blue)
- hasMany(Task::class)
- Access: $user->tasks

### Category Model (orange)
- hasMany(Task::class)
- Access: $category->tasks

### Task Model (green)
- belongsTo(User::class)
- belongsTo(Category::class)
- Access: $task->user, $task->category

### Connection arrows
- User →→→ Task (hasMany: 1対多)
- Category →→→ Task (hasMany: 1対多)
- Task → User (belongsTo: 多対1)
- Task → Category (belongsTo: 多対1)

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      リレーションの定義                              │
│                   〜hasMany と belongsTo〜                          │
│                                                                     │
│                                                                     │
│   User                                    Category                  │
│   ┌──────────────────┐                   ┌──────────────────┐      │
│   │  User Model      │                   │  Category Model  │      │
│   │                  │                   │                  │      │
│   │ hasMany(Task)    │                   │ hasMany(Task)    │      │
│   │                  │                   │                  │      │
│   │ $user->tasks     │                   │ $category->tasks │      │
│   └────────┬─────────┘                   └────────┬─────────┘      │
│            │ 1対多                               │ 1対多           │
│            │                                     │                 │
│            ↓                                     ↓                 │
│   ┌─────────────────────────────────────────────────────────┐      │
│   │                      Task Model                         │      │
│   │                                                         │      │
│   │  belongsTo(User::class)    belongsTo(Category::class)   │      │
│   │                                                         │      │
│   │  $task->user               $task->category              │      │
│   └─────────────────────────────────────────────────────────┘      │
│                                                                     │
│   【使い方】                                                        │
│   ┌─────────────────────────┬─────────────────────────────┐        │
│   │      親 → 子            │       子 → 親              │        │
│   ├─────────────────────────┼─────────────────────────────┤        │
│   │ $user->tasks            │ $task->user                │        │
│   │ ユーザーの全タスク取得  │ タスクの作成者を取得        │        │
│   └─────────────────────────┴─────────────────────────────┘        │
│                                                                     │
│   ★ hasMany = 「複数を持つ」/ belongsTo = 「〜に属する」            │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show User and Category both having hasMany to Task
- Show Task having belongsTo to both
- Include Eloquent access syntax ($user->tasks, $task->user)
- Show parent→child vs child→parent directions
```
