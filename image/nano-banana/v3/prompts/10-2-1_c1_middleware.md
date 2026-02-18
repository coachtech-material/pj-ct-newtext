# 10-2-1_c1: ミドルウェア

## 対象Section
- Tutorial 10-2-1: ミドルウェアとは
- 説明: リクエスト/レスポンスにおけるミドルウェアの位置を示す概念図

## リサーチメモ
- 一般的な図解パターン: パイプライン/玉ねぎモデル（onion model）
- リクエスト時は上→下、レスポンス時は下→上（逆順）
- Short-circuiting: 認証失敗時などはコントローラーに到達せず即座にレスポンス
- 教材の比喩: 「玉ねぎの層」のようにリクエストとレスポンスを包み込む
- Sources: [Microsoft Learn](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/), [Slim Framework](https://www.slimframework.com/docs/v4/concepts/middleware.html)

## プロンプト

```
Create a clean, modern educational diagram explaining "Middleware in Request/Response Pipeline" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with onion/layered model
- Colors: 4-color palette (blue for request flow, green for response flow, orange for middleware layers, gray for controller)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"ミドルウェア" centered at top
Subtitle: "〜リクエストとレスポンスを包む層〜"

## Layout
Horizontal onion/nested layers showing:
- Outer layer: First middleware
- Middle layers: Additional middleware
- Inner core: Controller

## Elements
Show the "onion model" with:
1. Client (left side)
2. Middleware 1 (CORS) - outermost layer
3. Middleware 2 (Auth) - middle layer
4. Middleware 3 (Log) - inner layer
5. Controller (center/core)

## Flow with arrows
- Blue arrows: Request flow (outside → inside)
- Green arrows: Response flow (inside → outside)
- Show numbered order: Request 1→2→3→Controller, Response 3→2→1

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                         ミドルウェア                                 │
│                                                                     │
│                                                                     │
│  リクエスト →                               ← レスポンス             │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Middleware 1                                               │   │
│  │    ┌───────────────────────────────────────────────────┐    │   │
│  │    │  Middleware 2                                     │    │   │
│  │    │    ┌───────────────────────────────────────────┐  │    │   │
│  │    │    │  Middleware 3                             │  │    │   │
│  │    │    │    ┌───────────────────────────────────┐  │  │    │   │
│  │    │    │    │         Controller                │  │  │    │   │
│  │    │    │    └───────────────────────────────────┘  │  │    │   │
│  │    │    └───────────────────────────────────────────┘  │    │   │
│  │    └───────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│                        玉ねぎのように層を通過                         │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show onion/nested layer model clearly
- Indicate bidirectional flow (request inward, response outward)
- Show execution order reversal between request and response
- Mention short-circuiting concept (auth failure = immediate redirect)
- Use "玉ねぎの層" metaphor from the textbook
```
