# 10-1-3_c1: ユーザー登録フロー

## 対象Section
- Tutorial 10-1-3: ユーザー登録機能を理解する
- 説明: ユーザー登録フローの概念図

## リサーチメモ
- 一般的な図解パターン: エントリーポイント → フォーム入力 → バリデーション（分岐） → 成功時ダッシュボードへ
- 教材のフロー: /register アクセス → ビュー表示 → POST → CreateNewUser アクション → バリデーション → ハッシュ化 → DB保存 → 自動ログイン → リダイレクト
- 重要ポイント: Fortifyがコントローラー不要でルートを自動登録
- Sources: [Creately](https://creately.com/diagram/example/s4RR1stVpyd/user-registration-flow-diagram), [Venngage](https://venngage.com/templates/diagrams/user-flowchart-for-login-and-registration-3714b52d-2002-4e21-ad6d-fd7ab909b4ef)

## プロンプト

```
Create a clean, modern educational diagram explaining "User Registration Flow with Laravel Fortify" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design flowchart with vertical flow
- Colors: 3-color palette (blue for user actions, green for server processing, orange for validation/branching)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"ユーザー登録フロー" centered at top
Subtitle: "〜Fortifyによる自動処理〜"

## Layout
Vertical flowchart from top to bottom with clear branching at validation step

## Elements and Flow
1. User accesses /register (entry point)
2. Fortify returns registration form view
3. User fills form and submits (POST)
4. Fortify calls CreateNewUser action
5. Validation (branching point)
   - Error → Return to form with error messages
   - Success → Continue
6. Password hashing with Hash::make()
7. Save to database (User::create)
8. Auto-login and redirect to dashboard

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      ユーザー登録フロー                              │
│                                                                     │
│                                                                     │
│   /register ──→ フォーム表示 ──→ 入力・送信                          │
│                                      │                              │
│                                      ▼                              │
│                              ┌───────────────┐                      │
│                              │ バリデーション │                      │
│                              └───────┬───────┘                      │
│                            ┌─────────┴─────────┐                    │
│                            ↓                   ↓                    │
│                        ❌ エラー            ✅ 成功                  │
│                            │                   │                    │
│                            ↓                   ↓                    │
│                      フォームへ戻る       DB保存 + 自動ログイン       │
│                                                │                    │
│                                                ↓                    │
│                                          ダッシュボード              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Vertical flowchart with clear step numbers
- Show validation as a branching point (error vs success)
- Emphasize Fortify's automatic handling (no controller needed)
- Include Hash::make() for password hashing
- Show auto-login after successful registration
```
