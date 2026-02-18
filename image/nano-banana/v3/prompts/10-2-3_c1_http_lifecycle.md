# 10-2-3_c1: HTTPライフサイクル

## 対象Section
- Tutorial 10-2-3: HTTPライフサイクルの詳細解説
- 説明: LaravelのHTTPライフサイクル全体を示す概念図

## リサーチメモ
- 一般的な図解パターン: 直線的なパイプライン形式（左→右 or 上→下）
- Laravel公式: Request → index.php → Kernel → Bootstrappers → Middleware → Router → Controller → Response → Middleware（逆順） → Browser
- 「Kernelは大きなブラックボックス」: HTTPリクエストを受け取りHTTPレスポンスを返す
- 教材の比喩: 「空港のセキュリティチェック」
- Sources: [Laravel Docs](https://laravel.com/docs/12.x/lifecycle), [Medium](https://medium.com/@ankitatejani84/laravel-request-lifecycle-7c2145aa1257)

## プロンプト

```
Create a clean, modern educational diagram explaining "Laravel HTTP Request Lifecycle" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with horizontal pipeline flow
- Colors: 4-color palette (blue for request, green for response, orange for processing stages, gray for kernel box)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"LaravelのHTTPライフサイクル" centered at top
Subtitle: "〜リクエストからレスポンスまでの旅〜"

## Layout
Horizontal flow from left (Browser) to right (Browser), showing:
- Request path (top arrow, blue)
- Response path (bottom arrow, green)
- Processing stages in between

## Elements (numbered stages)
1. ブラウザ (entry)
2. public/index.php (エントリーポイント)
3. HTTP Kernel (大きなボックス)
4. Middleware (リクエスト処理)
5. Router
6. Controller
7. View (Blade)
8. Response生成
9. Middleware (レスポンス処理、逆順)
10. ブラウザ (exit)

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                    LaravelのHTTPライフサイクル                       │
│                                                                     │
│                                                                     │
│  ブラウザ                                                ブラウザ   │
│     │                                                       ↑      │
│     │ リクエスト                                    レスポンス │      │
│     ▼                                                       │      │
│  ┌──────────────────────────────────────────────────────────┐      │
│  │                      HTTP Kernel                         │      │
│  │                                                          │      │
│  │  Middleware → Router → Controller → View → Response      │      │
│  │                                                          │      │
│  └──────────────────────────────────────────────────────────┘      │
│                                                                     │
│                                                                     │
│       すべてのリクエストは index.php を通過                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show HTTP Kernel as a large encompassing box
- Indicate entry point (public/index.php) clearly
- Show middleware executing twice (request and response phases)
- Include all major components: Middleware, Router, Controller, View
- Emphasize the "black box" concept of the Kernel
```
