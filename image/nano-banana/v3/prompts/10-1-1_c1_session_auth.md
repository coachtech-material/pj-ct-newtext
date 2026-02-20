# 10-1-1_c1: セッションベース認証

## 対象Section
- Tutorial 10-1-1: Laravel Fortifyとは
- 説明: セッションベース認証の全体フローを示す概念図

## リサーチメモ
- 一般的な図解パターン: クライアント（ブラウザ）→ サーバー → セッションストレージの3コンポーネント
- 7ステップの流れ: ログインリクエスト → 認証 → セッションID生成 → Cookie保存 → 以降のリクエストでCookie送信
- 教材の比喩: 「図書館の貸出カード」（セッションID = 会員を識別するカード）
- Sources: [ByteByteGo](https://blog.bytebytego.com/p/password-session-cookie-token-jwt), [roadmap.sh](https://roadmap.sh/guides/session-based-authentication)

## プロンプト

```
Create a clean, modern educational diagram explaining "Session-Based Authentication Flow" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with sequential flow
- Colors: 3-color palette (blue for client/browser, green for server, orange for session storage/cookie)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"セッションベース認証" centered at top
Subtitle: "〜ログイン状態を維持する仕組み〜"

## Layout
Left to right flow with three main components:
- Browser (left)
- Server (center)
- Session Storage (right, connected to server)

## Elements and Flow
1. ブラウザ → サーバー: "① ログインリクエスト（メール・パスワード）"
2. サーバー → Session Storage: "② セッション作成・保存"
3. サーバー → ブラウザ: "③ セッションID（Cookie）を返す"
4. ブラウザ（Cookie保存を示す）
5. ブラウザ → サーバー: "④ 以降のリクエスト（Cookieを自動送信）"
6. サーバー → Session Storage: "⑤ セッションIDで照合"
7. サーバー → ブラウザ: "⑥ 認証済みとして応答"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      セッションベース認証                            │
│                                                                     │
│                                                                     │
│  ┌──────────┐                               ┌──────────┐           │
│  │          │  ──── ID + パスワード ────→   │          │           │
│  │ ブラウザ  │                               │  サーバー │           │
│  │          │  ←── セッションID(Cookie) ──  │          │           │
│  └──────────┘                               └────┬─────┘           │
│       │                                          │                  │
│       │                                     ┌────▼─────┐           │
│  ┌────▼─────┐                               │ Session  │           │
│  │  Cookie   │  ←─────── 紐付け ───────→    │ Storage  │           │
│  │ (ID保存)  │                               │(データ保存)│           │
│  └──────────┘                               └──────────┘           │
│                                                                     │
│      ブラウザ側                                サーバー側             │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show clear two-phase flow: Login phase and Subsequent access phase
- Emphasize Cookie as the carrier of Session ID
- Session Storage connected to Server
- Numbered arrows (①②③④⑤⑥) showing the sequential flow
- Include the library card metaphor at the bottom
```
