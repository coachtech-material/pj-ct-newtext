# 9-1-6_c1: リクエストとレスポンス

## 対象Section
- Tutorial 9-1-6: リクエストとレスポンスの基礎
- 説明: HTTPリクエスト/レスポンスの流れを示す概念図

## リサーチメモ
- HTTP: Hypertext Transfer Protocol（ステートレスなリクエスト/レスポンス）
- リクエスト: メソッド（GET/POST等）、URL、ヘッダー、ボディ
- レスポンス: ステータスコード（200, 404等）、ヘッダー、ボディ
- Laravelでは Illuminate\Http\Request, Illuminate\Http\Response を使用
- 図解パターン: 双方向矢印（User ↔ Server）が業界標準
- Sources: [MDN HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP), [Laravel Docs](https://laravel.com/docs/requests)

## プロンプト

```
Create a clean, modern educational diagram explaining "HTTP Request and Response" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with bidirectional flow
- Colors: 3-color palette (blue for user/browser, orange for server, green for data)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"リクエストとレスポンス" centered at top
Subtitle: "〜Webアプリの会話〜"

## Elements
Left: ユーザー（ブラウザ）
Right: サーバー
Between: Two arrows showing request/response

## Flow
① リクエスト（お願い）: 「名前を送るよ」→
② レスポンス（返事）: ←「こんにちは、〇〇さん」

## Data examples
- Request: フォームデータ、URL、HTTPメソッド
- Response: HTML、JSON、画像など

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      リクエストとレスポンス                           │
│                                                                     │
│      【ブラウザ】                             【サーバー】            │
│                                                                     │
│      ┌──────────────┐                    ┌──────────────┐          │
│      │              │     リクエスト      │              │          │
│      │              │ ─────────────────→ │              │          │
│      │   ユーザー    │   URL, メソッド,    │   Laravel    │          │
│      │              │   フォームデータ    │              │          │
│      │              │                    │              │          │
│      │              │     レスポンス      │              │          │
│      │              │ ←───────────────── │              │          │
│      │              │   HTML, JSON等     │              │          │
│      └──────────────┘                    └──────────────┘          │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show bidirectional communication clearly
- List what's included in request and response
- Emphasize the cycle: Input → Process → Output
- Simple conversational metaphor
```
