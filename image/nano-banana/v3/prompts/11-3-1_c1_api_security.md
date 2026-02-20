# 11-3-1_c1: APIセキュリティ

## 対象Section
- Tutorial 11-3-1: APIのセキュリティ対策
- 説明: レート制限とAPIセキュリティの概念図

## リサーチメモ
- レート制限 = 一定時間内のリクエスト数を制限
- 目的: DoS攻撃防止、サーバー負荷軽減、公平性確保
- 超過時: 429 Too Many Requests
- Webでよく使われる構図: リクエストがゲートを通過する図
- Laravel: ThrottleRequests ミドルウェア、デフォルト60回/分
- APIセキュリティ3要素: レート制限、バリデーション、HTTPS

## プロンプト

```
Create a clean, modern educational diagram explaining "API Rate Limiting" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Gate/checkpoint diagram showing request filtering
- Colors: Blue for normal requests, Red for blocked, Green for allowed
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"レート制限（Rate Limiting）" centered at top
Subtitle: "〜リクエスト数を制限してAPIを守る〜"

## Layout
Left: Multiple incoming requests
Center: Rate limit gate (counter: 60回/分)
Right: Success or blocked response

## Elements

### Left: Incoming Requests
Multiple API request arrows
- Normal user: 10回/分
- Heavy user: 100回/分
- Attacker: 1000回/分

### Center: Rate Limit Gate
Gate with counter display
- 制限: 60回/分
- 残り: X回
- Throttle middleware

### Right: Responses
Success (green): 200 OK → データ取得
Blocked (red): 429 Too Many Requests → エラー

### Flow
Normal user → passes gate → 200 OK
Attacker → blocked at gate → 429 Error

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                   レート制限（Rate Limiting）                        │
│               〜リクエスト数を制限してAPIを守る〜                     │
│                                                                     │
│                                                                     │
│   リクエスト              レート制限                レスポンス       │
│                                                                     │
│   ┌──────────┐           ┌───────────┐          ┌──────────┐      │
│   │ 通常ユーザー │ ────────→ │           │ ────────→ │ ✅ 200 OK│      │
│   │  10回/分   │           │   🚧      │          │  データ取得│      │
│   └──────────┘           │  ゲート    │          └──────────┘      │
│                          │           │                            │
│   ┌──────────┐           │ 制限:     │          ┌──────────┐      │
│   │  攻撃者   │ ────×───→ │ 60回/分   │          │ ❌ 429   │      │
│   │ 1000回/分 │ ブロック！ │           │          │Too Many  │      │
│   └──────────┘           └───────────┘          │Requests  │      │
│                                                 └──────────┘      │
│                                                                     │
│   【レート制限の効果】                                               │
│   ┌────────────────────┬──────────────────────────────┐            │
│   │     目的          │         効果               │            │
│   ├────────────────────┼──────────────────────────────┤            │
│   │ DoS攻撃の防止     │ 大量リクエストをブロック     │            │
│   │ サーバー負荷軽減   │ 過負荷によるダウンを防ぐ     │            │
│   │ 公平性の確保       │ 特定ユーザーの独占を防ぐ     │            │
│   └────────────────────┴──────────────────────────────┘            │
│                                                                     │
│   ★ 一定時間（1分）あたりのリクエスト数を制限して不正利用を防ぐ       │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show gate metaphor for rate limiting
- Contrast normal user (passes) vs attacker (blocked)
- Include 429 Too Many Requests response
- Show 3 benefits table (DoS prevention, load reduction, fairness)
```
