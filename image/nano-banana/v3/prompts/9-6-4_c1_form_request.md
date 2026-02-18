# 9-6-4_c1: フォームリクエスト

## 対象Section
- Tutorial 9-6-4: フォームリクエスト
- 説明: バリデーションロジックの分離を示す概念図

## リサーチメモ
- FormRequest: バリデーションロジックを分離するクラス
- php artisan make:request StorePostRequest で生成
- rules(): バリデーションルールを定義
- authorize(): 認可ロジックを定義
- バリデーション失敗時は自動でリダイレクト
- Single Responsibility Principle（単一責任の原則）の実践
- 図解パターン: Before（Fat Controller）→ After（分離）の比較
- Sources: [Laravel Docs](https://laravel.com/docs/validation#form-request-validation)

## プロンプト

```
Create a clean, modern educational diagram explaining "Form Request for Validation" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with before/after comparison
- Colors: 3-color palette (red for fat controller, green for clean separation, blue for form request)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"フォームリクエスト" centered at top
Subtitle: "〜バリデーションの分離〜"

## Elements
Before: Fat Controller
- Controller with long validate() call

After: Clean separation
- FormRequest class (handles validation)
- Controller (only business logic)

## Flow
Request → FormRequest (validation) → Controller

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                       フォームリクエスト                              │
│                                                                     │
│   ❌ Before                           ✅ After                       │
│                                                                     │
│   ┌───────────────────────┐         ┌───────────────────────┐     │
│   │ Controller            │         │ FormRequest          │     │
│   │                       │         │ （バリデーション）     │     │
│   │ validate([            │    →    └───────────┬───────────┘     │
│   │   'title' => ...,     │                     ↓                  │
│   │   'content' => ...,   │         ┌───────────────────────┐     │
│   │   ...長いルール...     │         │ Controller            │     │
│   │ ]);                   │         │ （ロジックのみ）       │     │
│   │ // 本来の処理         │         │                       │     │
│   └───────────────────────┘         └───────────────────────┘     │
│                                                                     │
│   コントローラーが太る                 役割分担でスッキリ              │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Clear before/after comparison
- Show separation of concerns
- FormRequest handles validation automatically
- Controller becomes cleaner
```
