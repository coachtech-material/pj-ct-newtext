# 8-3-4_c1: JOIN句

## 対象Section
- Tutorial 8-3-4: JOIN句によるテーブルの結合
- 説明: テーブル結合（INNER JOIN/LEFT JOIN）の概念図

## リサーチメモ
- JOINの視覚化にはベン図（Venn Diagram）が業界標準
- INNER JOIN: 両テーブルで一致するレコードのみ（交差部分）
- LEFT JOIN: 左テーブル全て + 右テーブルの一致するもの（一致なしはNULL）
- RIGHT JOIN: 右テーブル全て + 左テーブルの一致するもの
- FULL OUTER JOIN: 両テーブル全て（一致なしはNULL）
- インタラクティブツール: sql-joins.leopard.in.ua, joins.spathon.com
- Sources: [Coding Horror](https://blog.codinghorror.com/a-visual-explanation-of-sql-joins/), [Atlassian](https://www.atlassian.com/data/sql/sql-join-types-explained-visually), [LearnSQL](https://learnsql.com/blog/sql-joins/)

## プロンプト

```
Create a clean, modern educational diagram explaining "SQL JOIN" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with Venn diagram style
- Colors: 3-color palette (blue for table A, orange for table B, green for result)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"JOINによるテーブル結合" centered at top
Subtitle: "〜分割したデータをつなぎ合わせる〜"

## Elements
Two sections:

1. INNER JOIN
- Two overlapping circles (Venn diagram)
- Only intersection highlighted
- Label: "両方に存在するデータのみ"

2. LEFT JOIN
- Two overlapping circles
- Left circle fully highlighted + intersection
- Label: "左側のテーブルは全て + 右側は一致するもの"

## Result table examples
Show before (2 tables) and after (joined result)

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                     JOINによるテーブル結合                           │
│                   〜分割したデータをつなぎ合わせる〜                    │
│                                                                     │
│   【結合前】2つのテーブル              【結合後】1つの結果            │
│                                                                     │
│   users           posts               →    name   │ title          │
│  ┌─────┐        ┌─────────┐              山田   │ Laravel入門    │
│  │id│name│       │id│user_id│title│         山田   │ SQL基本       │
│  │1 │山田│       │1 │  1   │...  │                                 │
│  │2 │鈴木│       │2 │  1   │...  │                                 │
│  └─────┘        └─────────┘                                        │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│    【INNER JOIN】                    【LEFT JOIN】                   │
│                                                                     │
│       ┌───────────────┐                 ┌───────────────┐          │
│      /       ┌───────┼───┐             /███████┌───────┼───┐       │
│     /        │███████│   │            /████████│███████│   │       │
│    │  users  │██一致██│posts          │██users██│██一致██│posts     │
│     \        │███████│   │            \████████│███████│   │       │
│      \       └───────┼───┘             \███████└───────┼───┘       │
│       └───────────────┘                 └───────────────┘          │
│                                                                     │
│    両方に存在する                    左側は全部残す                   │
│    データのみ返す                    右側がなければNULL               │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│    SELECT u.name, p.title                                           │
│    FROM users AS u                                                  │
│    INNER JOIN posts AS p ON u.id = p.user_id;                       │
│    ──────────────────────                                           │
│           ON句 = 結合の「接着剤」                                    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show Venn diagram style for INNER vs LEFT JOIN
- Include simple SQL syntax
- Emphasize ON clause as "glue"
- Show practical example with users/posts
```
