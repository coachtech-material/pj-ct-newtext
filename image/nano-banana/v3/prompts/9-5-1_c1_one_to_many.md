# 9-5-1_c1: 1対多のリレーションシップ

## 対象Section
- Tutorial 9-5-1: 1対多のリレーションシップ（hasMany、belongsTo）
- 説明: 1対多のリレーションシップを示す概念図

## リサーチメモ
- 1対多 = 親テーブル1件に対して子テーブルが複数紐づく
- 例: 1人のユーザー → 複数の投稿
- 外部キー（FK）で関連付け: posts.user_id → users.id
- IE記法: 1側は縦棒「|」、多側は鳥の足記号「<」
- hasMany(): 親→子（User→Posts）
- belongsTo(): 子→親（Post→User）
- Webで標準的なER図の構図を参考

## プロンプト

```
Create a clean, modern educational diagram explaining "One-to-Many Relationship" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: ER diagram style with crow's foot notation
- Colors: Blue for parent table (User), Orange for child table (Posts)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"1対多のリレーションシップ" centered at top
Subtitle: "〜親1件に子が複数紐づく〜"

## Layout
Left: Parent table (users) - blue
Right: Child table (posts) - orange
Center: Connection line with crow's foot notation

## Elements

### Left: users table (blue, parent)
Table with columns:
- id (PK) ← 主キー
- name
Show 1 record: id=1, name=山田太郎

### Right: posts table (orange, child)
Table with columns:
- id (PK)
- title
- user_id (FK) ← 外部キー
Show 3 records all with user_id=1

### Connection Line
- From users.id to posts.user_id
- Use crow's foot notation:
  - Users side: single line (|) = 1
  - Posts side: crow's foot (<) = many
- Label: 外部キー (FK)

### Visual explanation
- 1 user record connects to 3 post records
- Arrow showing the relationship direction

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                  1対多のリレーションシップ                           │
│                  〜親1件に子が複数紐づく〜                           │
│                                                                     │
│                                                                     │
│   【users】親テーブル                  【posts】子テーブル           │
│                                                                     │
│   ┌─────────────────┐                 ┌─────────────────────────┐  │
│   │  id   │  name   │                 │  id  │ title  │ user_id │  │
│   │ (PK)  │         │                 │ (PK) │        │  (FK)   │  │
│   ├───────┼─────────┤    1      多    ├──────┼────────┼─────────┤  │
│   │   1   │山田太郎 │────|────<──────│  1   │ 記事1  │    1    │  │
│   │       │         │                 │  2   │ 記事2  │    1    │  │
│   └─────────────────┘                 │  3   │ 記事3  │    1    │  │
│                                       └─────────────────────────┘  │
│         ↑ 主キー                              ↑ 外部キー           │
│        (PK)                                  (FK)                  │
│                                                                     │
│   【記号の意味】                                                     │
│    |  = 1（1件）      <  = 多（複数件）                             │
│                                                                     │
│   ★ 外部キー(user_id)が主キー(id)を参照して紐づく                    │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Use crow's foot notation (| for 1, < for many)
- Show PK (Primary Key) and FK (Foreign Key) labels
- Display actual data to show 1 user linked to 3 posts
- All posts have same user_id value (1) to show the relationship
```
