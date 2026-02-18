# 9-4-1_c1: Eloquent ORM

## 対象Section
- Tutorial 9-4-1: Eloquent ORMとは
- 説明: ORM（テーブル↔オブジェクト対応）の概念図

## リサーチメモ
- ORM = Object-Relational Mapping（オブジェクトとRDBの橋渡し）
- 「インピーダンスミスマッチ」問題を解決（OOPとRDBの構造の違い）
- マッピング: クラス↔テーブル、インスタンス↔行、プロパティ↔カラム
- Eloquent = LaravelのActiveRecord実装
- メリット: SQLを書かずにDB操作、型安全、リレーション管理が容易
- デメリット: 複雑なクエリでは生SQLより遅い場合あり
- Sources: [FreeCodeCamp](https://www.freecodecamp.org/news/what-is-an-orm-the-meaning-of-object-relational-mapping-database-tools/), [Visual Paradigm](https://www.visual-paradigm.com/support/documents/vpuserguide/3563/3581/85424_whatisobject.html), [AltexSoft](https://www.altexsoft.com/blog/orm-object-relational-mapping/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Eloquent ORM" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with mapping visualization
- Colors: 3-color palette (blue for PHP/Model, orange for SQL, green for Database)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Eloquent ORM" centered at top
Subtitle: "〜テーブルをオブジェクトとして扱う〜"

## Elements
Left: PHP Model (User class)
Center: Eloquent ORM (translation layer)
Right: Database table (users)

## Mapping
- Model class → Table
- Instance → Row/Record
- Property → Column

## Code comparison
SQL: SELECT * FROM users WHERE id = 1;
Eloquent: $user = User::find(1);

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                         Eloquent ORM                                │
│                                                                     │
│   【PHPコード】              【ORM】           【データベース】        │
│                                                                     │
│   ┌──────────────┐        ┌────────┐      ┌──────────────┐        │
│   │ class User   │        │        │      │ users テーブル│        │
│   │ {            │        │  変換   │      │              │        │
│   │   $name      │←──────│        │──────→│ name カラム  │        │
│   │   $email     │        │        │      │ email カラム │        │
│   │ }            │        │        │      │              │        │
│   └──────────────┘        └────────┘      └──────────────┘        │
│                                                                     │
│   【対応関係】                                                       │
│                                                                     │
│   クラス      ←→  テーブル                                          │
│   インスタンス ←→  1行のレコード                                     │
│   プロパティ   ←→  カラム                                           │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show clear mapping between PHP and Database
- Class ↔ Table, Instance ↔ Row, Property ↔ Column
- Compare SQL vs Eloquent syntax
- Emphasize simplicity of Eloquent approach
```
