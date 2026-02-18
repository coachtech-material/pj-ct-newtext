# 9-5-2_c2: 中間テーブルの実装

## 対象Section
- Tutorial 9-5-2: 多対多のリレーションシップ（belongsToMany）
- 説明: 中間テーブルによる多対多の実装を示す概念図

## リサーチメモ
- 中間テーブル（ピボットテーブル）: 両モデルのFKを持つ
- attach(): 関連を追加（中間テーブルにレコード挿入）
- detach(): 関連を削除（中間テーブルからレコード削除）
- sync(): 指定IDのみを残し、他は削除（差分更新）
- toggle(): 存在すれば削除、なければ追加
- 命名規則: モデル名の単数形をアルファベット順で結合（role_user）
- 図解パターン: 3テーブル（ModelA | Pivot | ModelB）と操作メソッド
- Sources: [Laravel Docs](https://laravel.com/docs/eloquent-relationships#updating-many-to-many-relationships)

## プロンプト

```
Create a clean, modern educational diagram explaining "Pivot Table for Many-to-Many" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with table structure visualization
- Colors: 4-color palette (blue for users, orange for pivot, green for roles, gray for methods)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"中間テーブルの操作" centered at top
Subtitle: "〜attach / detach / sync〜"

## Elements
Three tables showing actual data:
- users: id=1 山田, id=2 鈴木
- role_user: user_id, role_id pairs
- roles: id=1 admin, id=2 editor

## Methods
- attach(): 関連を追加
- detach(): 関連を削除
- sync(): 関連を同期（差分更新）

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                       中間テーブルの操作                              │
│                                                                     │
│   【users】            【role_user】           【roles】              │
│                                                                     │
│  ┌─────────────┐      ┌─────────────┐      ┌─────────────┐        │
│  │ id │ name   │      │user_id│role_id│      │ id │ name   │        │
│  ├────┼────────┤      ├───────┼───────┤      ├────┼────────┤        │
│  │ 1  │ 山田   │←────│  1   │   1   │─────→│ 1  │ admin  │        │
│  │ 2  │ 鈴木   │←────│  1   │   2   │─────→│ 2  │ editor │        │
│  └─────────────┘      └─────────────┘      └─────────────┘        │
│                                                                     │
│  【操作メソッド】                                                     │
│                                                                     │
│  attach() : 関連を追加                                               │
│  detach() : 関連を削除                                               │
│  sync()   : 指定IDのみ残す                                           │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show 3 tables with actual data
- Demonstrate attach/detach/sync methods
- Use arrows to show relationships
- Explain pivot table naming convention
```
