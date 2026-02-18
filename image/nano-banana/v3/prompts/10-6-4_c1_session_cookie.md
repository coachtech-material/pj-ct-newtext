# 10-6-4_c1: セッションとCookieによる状態管理

## 対象Section
- Tutorial 10-6-4: 認証とセッション管理
- 説明: セッション/Cookieによる状態管理の概念図

## リサーチメモ
- HTTPはステートレス（各リクエストは独立、前の情報を覚えていない）
- Cookie: ブラウザ側に保存（セッションIDを保持）
- セッション: サーバー側に保存（ユーザー情報を保持）
- フロー: ログイン → サーバーがセッションID発行 → Cookieに保存 → 以降のリクエストでCookie送信
- 教材の比喩: 「映画館のチケット」
- Sources: [OWASP](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html), [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/Cookies)

## プロンプト

```
Create a clean, modern educational diagram explaining "Session and Cookie State Management" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic showing client-server interaction
- Colors: 3-color palette (blue for browser/client, green for server, orange for cookie/session)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"セッションとCookie" centered at top
Subtitle: "〜ログイン状態を維持する仕組み〜"

## Layout
Two main sections:
- Top: Comparison of Cookie vs Session (where data is stored)
- Bottom: Flow diagram showing the complete lifecycle

## Elements

### Comparison Section
Two boxes side by side:
- Cookie: Browser-side storage (small data, session ID)
- Session: Server-side storage (user data, secure)

### Flow Diagram (numbered steps)
1. User accesses site (first time)
2. Server creates session, issues session ID
3. Session ID stored in Cookie (browser)
4. User logs in
5. Server stores user info in session
6. User navigates to new page
7. Browser sends Cookie (session ID)
8. Server identifies user from session
9. User logs out
10. Session invalidated

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                       セッションとCookie                            │
│                                                                     │
│                                                                     │
│       ブラウザ側                           サーバー側                │
│                                                                     │
│   ┌───────────────┐                   ┌───────────────┐            │
│   │               │                   │               │            │
│   │    Cookie     │ ←───── 紐付け ───→│   セッション   │            │
│   │               │                   │               │            │
│   │  セッションID  │                   │ ユーザー情報   │            │
│   │  (小さいデータ) │                   │ (大きいデータ)  │            │
│   │               │                   │               │            │
│   └───────────────┘                   └───────────────┘            │
│                                                                     │
│                                                                     │
│         CookieのIDでサーバーのセッションを特定                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Clearly show Cookie (client-side) vs Session (server-side)
- Illustrate the stateless nature of HTTP
- Show the complete flow from first access to logout
- Emphasize that Session ID in Cookie links browser to server session
- Include the "movie ticket" metaphor from textbook
```
