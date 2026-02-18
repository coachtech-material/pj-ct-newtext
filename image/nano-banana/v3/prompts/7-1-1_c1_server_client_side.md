# 7-1-1_c1: サーバーサイド vs クライアントサイド

## 対象Section
- Tutorial 7-1-1: PHPとは何か
- 説明: サーバーサイド言語とクライアントサイド言語の役割を示す概念図

## リサーチメモ
- Server-side (PHP, Python, Ruby): サーバーで実行、DB連携、HTML生成
- Client-side (JavaScript, CSS): ブラウザで実行、UI操作、アニメーション
- サーバーサイドはコードが見えない（セキュア）、クライアントサイドは見える
- PHPはサーバーで処理後、HTMLだけをブラウザに返す
- JavaScriptはNode.jsでサーバーサイドでも実行可能
- 図解パターン: 左右比較（Server | Client）が業界標準
- Sources: [Cloudflare](https://www.cloudflare.com/learning/serverless/glossary/client-side-vs-server-side/), [MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Server-side/First_steps/Introduction)

## プロンプト

```
Create a clean, modern educational diagram explaining "Server-side vs Client-side Languages" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with comparison layout
- Colors: 3-color palette (blue for server-side, orange for client-side, green for flow)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"サーバーサイドとクライアントサイド" centered at top
Subtitle: "〜キッチンとホールの役割分担〜"

## Elements
Left: Server-side (blue)
- PHP icon
- Label: "サーバーサイド（PHP）"
- Role: "キッチン（調理担当）"
- Tasks: "データベース連携、認証、HTML生成"

Right: Client-side (orange)
- JavaScript icon
- Label: "クライアントサイド（JavaScript）"
- Role: "ホール（接客担当）"
- Tasks: "アニメーション、入力検証、画面操作"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                 サーバーサイドとクライアントサイド                    │
│                    〜キッチンとホールの役割分担〜                     │
│                                                                     │
│   【サーバーサイド】                    【クライアントサイド】        │
│   （キッチン・裏方）                    （ホール・表側）             │
│                                                                     │
│   ┌──────────────────────┐          ┌──────────────────────┐      │
│   │                      │          │                      │      │
│   │   🐘 PHP             │          │   🟨 JavaScript      │      │
│   │   Ruby, Python など   │          │                      │      │
│   │                      │          │                      │      │
│   │  実行場所:            │          │  実行場所:            │      │
│   │  Webサーバー          │          │  ブラウザ（ユーザーPC）│      │
│   │                      │          │                      │      │
│   │  主な役割:            │          │  主な役割:            │      │
│   │  • データベース連携   │          │  • アニメーション     │      │
│   │  • ユーザー認証      │          │  • 入力の検証        │      │
│   │  • HTMLの動的生成    │          │  • 画面の操作        │      │
│   │  • ビジネスロジック  │          │  • 非同期通信        │      │
│   │                      │          │                      │      │
│   │  ユーザーから見えない │          │  ユーザーが直接触れる │      │
│   │                      │          │                      │      │
│   └──────────────────────┘          └──────────────────────┘      │
│                                                                     │
│   ★ PHP = 裏側の本質的な処理（調理）                                │
│   ★ JavaScript = 表側の演出（接客）                                 │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Clear comparison between server-side and client-side
- Restaurant metaphor (kitchen vs hall)
- List of responsibilities for each
- Emphasize where each runs (server vs browser)
```
