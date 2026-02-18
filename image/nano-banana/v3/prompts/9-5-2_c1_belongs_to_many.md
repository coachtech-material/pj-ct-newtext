# 9-5-2_c1: belongsToMany

## 対象Section
- Tutorial 9-5-2: 多対多のリレーションシップ（belongsToMany）
- 説明: 多対多リレーションシップの概念図

## リサーチメモ
- 多対多: 両方のモデルが複数の相手を持てる関係
- belongsToMany: Eloquentの多対多リレーション定義メソッド
- 両モデルで belongsToMany を定義（双方向）
- 中間テーブル: アルファベット順の単数形（role_user）
- 使用例: $user->roles, $role->users
- 図解パターン: 双方向矢印で両モデルを接続
- Sources: [Laravel Docs](https://laravel.com/docs/eloquent-relationships#many-to-many)

## プロンプト

```
Create a clean, modern educational diagram explaining "Many-to-Many Relationship with belongsToMany" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with relationship visualization
- Colors: 3-color palette (blue for users, orange for roles, green for pivot table)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"多対多リレーションシップ" centered at top
Subtitle: "〜belongsToMany〜"

## Elements
Example: Users and Roles
- One user can have multiple roles
- One role can belong to multiple users

Three tables:
- users
- role_user (pivot)
- roles

## Model definitions
User: belongsToMany(Role::class)
Role: belongsToMany(User::class)

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                    多対多リレーションシップ                           │
│                                                                     │
│   【User】                                    【Role】               │
│                                                                     │
│   ┌──────────────────┐                  ┌──────────────────┐       │
│   │                  │   belongsToMany  │                  │       │
│   │  User モデル     │ ←──────────────→ │  Role モデル     │       │
│   │                  │                  │                  │       │
│   │  roles()         │                  │  users()         │       │
│   │                  │                  │                  │       │
│   └──────────────────┘                  └──────────────────┘       │
│                                                                     │
│   1人のユーザー = 複数の役割                                         │
│   1つの役割 = 複数のユーザー                                         │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show bidirectional relationship
- Both models use belongsToMany
- Use concrete example (users and roles)
- Show how to access related data
```
