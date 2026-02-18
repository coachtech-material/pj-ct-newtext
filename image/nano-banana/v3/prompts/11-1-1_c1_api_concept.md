# 11-1-1_c1: Web認証 vs API認証

## 対象Section
- Tutorial 11-1-1: APIとは何か
- 説明: Web認証とAPI認証の違いを示す概念図

## リサーチメモ
- Web認証: Cookie/Session方式、ステートフル、ブラウザが自動でCookie送信
- API認証: Token方式、ステートレス、クライアントが明示的にTokenを送信
- 教材の重要ポイント: 「セッションを使わない」「Tokenで認証する」

## プロンプト

```
Create a clean, modern educational diagram comparing "Web Authentication vs API Authentication" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with minimal elements
- Colors: 3-color palette (blue for Web, green for API, orange for highlight)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Web認証 vs API認証" centered at top
Subtitle: "〜認証方式の違い〜"

## Layout
Two-column comparison with clear visual distinction

## Elements (2 boxes, side by side)
1. Web認証 (blue): Large rounded rectangle, label "Web認証"
   - Sub-label: "ステートフル"
   - Icon: Browser icon
   - Flow: Cookie with Session ID
2. API認証 (green): Large rounded rectangle, label "API認証"
   - Sub-label: "ステートレス"
   - Icon: Mobile/App icon
   - Flow: Token (Bearer)

## Flow (for each column)
Left (Web認証):
- ブラウザ → サーバー: "ログイン"
- サーバー → ブラウザ: "Cookie発行"
- ブラウザ → サーバー: "自動送信"

Right (API認証):
- クライアント → サーバー: "ログイン"
- サーバー → クライアント: "Token発行"
- クライアント → サーバー: "明示的に送信"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                       Web認証 vs API認証                            │
│                       〜認証方式の違い〜                             │
│                                                                     │
│   【Web認証（Cookie/Session）】       【API認証（Token）】           │
│                                                                     │
│   ブラウザ         サーバー         クライアント        サーバー     │
│   ┌─────┐        ┌─────┐          ┌─────┐           ┌─────┐       │
│   │     │        │ユーザー│          │Token │           │     │       │
│   │ID:abc│        │情報保存│          │(情報 │           │検証  │       │
│   │     │        │     │          │含む) │           │のみ  │       │
│   └──┬──┘        └──┬──┘          └──┬──┘           └──┬──┘       │
│      │   Cookie自動  │              │   Token手動    │            │
│      │─────────────→│              │─────────────→ │            │
│      │   送信        │              │   送信         │            │
│      │               │              │                │            │
│      │   セッション   │              │   署名検証     │            │
│      │   照合        │              │   のみ         │            │
│                                                                     │
│   サーバーが情報を保持            トークンが情報を持つ              │
│                                                                     │
│   ★ Cookie=IDだけ渡す / Token=情報ごと渡す                          │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show WHERE data is stored: Server (Cookie) vs Token itself (JWT)
- Cookie: only ID in browser, server does lookup
- Token: self-contained, server only verifies signature
- Clear flow: automatic vs manual sending
```
