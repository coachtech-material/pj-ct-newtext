# 10-1-4_c1: ログイン・ログアウトフロー

## 対象Section
- Tutorial 10-1-4: ログイン・ログアウト機能を理解する
- 説明: ログイン/ログアウトフローの概念図

## リサーチメモ
- 一般的な図解パターン: credential entry → verification → error/success branching → access approval
- ログアウト: セッション無効化 + Cookie削除 + リダイレクト
- 教材のフロー: /login → フォーム表示 → POST → 認証 → セッション作成 → リダイレクト
- Sources: [SmartDraw](https://www.smartdraw.com/flowchart/examples/login-process-flowchart/), [Auth0](https://auth0.com/blog/the-not-so-easy-art-of-logging-out/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Login and Logout Flow" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with two parallel flows
- Colors: 3-color palette (blue for login flow, red for logout flow, green for session/success)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"ログイン・ログアウト" centered at top
Subtitle: "〜セッションの開始と終了〜"

## Layout
Two-column layout:
- Left: Login flow (vertical)
- Right: Logout flow (vertical)

## Elements

### Login Flow (Left)
1. /login にアクセス
2. ログインフォーム表示
3. メール・パスワード送信 (POST)
4. Fortifyが認証処理
5. 分岐: 成功 → セッション作成 → ダッシュボードへ / 失敗 → エラー表示

### Logout Flow (Right)
1. ログアウトボタン (POST)
2. セッション無効化
3. CSRFトークン再生成
4. ログインページへリダイレクト

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      ログイン・ログアウト                            │
│                                                                     │
│                                                                     │
│   【ログイン】                            【ログアウト】              │
│                                                                     │
│       /login                                  POST                  │
│          │                                      │                   │
│          ▼                                      ▼                   │
│   ┌─────────────┐                        ┌─────────────┐            │
│   │  認証処理   │                        │セッション削除│            │
│   └──────┬──────┘                        └──────┬──────┘            │
│     ┌────┴────┐                                 │                   │
│     ↓         ↓                                 ▼                   │
│   ❌失敗    ✅成功                          /login へ               │
│     │         │                                                     │
│     ↓         ↓                                                     │
│  エラー表示  セッション作成                                          │
│              → ダッシュボード                                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Two-column layout: Login (left) and Logout (right)
- Show branching at authentication (success/failure)
- Emphasize POST method for logout (security)
- Include CSRF token requirement
- Session creation on login, session invalidation on logout
```
