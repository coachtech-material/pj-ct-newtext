# 9-4-6_c1: データの更新と削除

## 対象Section
- Tutorial 9-4-6: データの更新と削除
- 説明: Eloquentによるデータ更新・削除フローの概念図

## リサーチメモ
- save(): インスタンスのプロパティ変更後に保存
- update(): 配列で一度に複数カラムを更新
- delete(): インスタンスから削除（->で呼び出し）
- destroy(): クラスメソッドでIDから直接削除（::で呼び出し）
- 演算子の違い: :: はクラスメソッド、-> はインスタンスメソッド
- 図解パターン: 更新/削除の2セクション、各2メソッドの比較
- Sources: [Laravel Docs](https://laravel.com/docs/eloquent#deleting-models)

## プロンプト

```
Create a clean, modern educational diagram explaining "Eloquent Update and Delete" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with method comparison
- Colors: 3-color palette (blue for update methods, orange for delete methods, green for database)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Eloquentの更新と削除" centered at top
Subtitle: "〜save(), update(), delete(), destroy()〜"

## Elements
Two sections:

Update methods:
- save(): プロパティ変更 → save()で保存
- update(): 配列で一度に更新

Delete methods:
- delete(): インスタンスから削除
- destroy(): IDで直接削除

## Operator distinction
:: (static method) vs -> (instance method)

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      Eloquentの更新と削除                            │
│                                                                     │
│  【更新】                                                            │
│                                                                     │
│  ┌─────────────────────────┐    ┌─────────────────────────┐       │
│  │ save()                  │    │ update()                │       │
│  │                         │    │                         │       │
│  │ $user->name = '新名前'; │    │ $user->update([...]);   │       │
│  │ $user->save();          │    │                         │       │
│  └─────────────────────────┘    └─────────────────────────┘       │
│                                                                     │
│  【削除】                                                            │
│                                                                     │
│  ┌─────────────────────────┐    ┌─────────────────────────┐       │
│  │ delete()                │    │ destroy()               │       │
│  │                         │    │                         │       │
│  │ $user->delete();        │    │ User::destroy(1);       │       │
│  │ インスタンスから削除     │    │ IDで直接削除            │       │
│  └─────────────────────────┘    └─────────────────────────┘       │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show 4 main methods: save, update, delete, destroy
- Distinguish :: (class) vs -> (instance)
- Include code examples for each
- Clear visual separation between update and delete
```
