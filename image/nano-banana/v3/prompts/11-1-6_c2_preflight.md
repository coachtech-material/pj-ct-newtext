# 11-1-6_c2: プリフライトリクエスト

## 対象Section
- Tutorial 11-1-6: CORSとは
- 説明: プリフライトリクエストの流れを示す概念図

## リサーチメモ
- プリフライト = 本リクエストの前に送信される「事前確認」
- OPTIONSメソッドで「これ送っていい？」と確認
- 許可されれば本リクエスト、拒否されればブロック

## プロンプト

```
Create a clean, modern educational diagram explaining "Preflight Request" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design sequence diagram
- Colors: 3-color (blue for browser, green for server, orange for preflight)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"プリフライトリクエスト" centered at top
Subtitle: "〜本リクエスト前の事前確認〜"

## Layout
Vertical sequence diagram: Browser on left, Server on right

## Flow
Step 1: Browser sends OPTIONS request ("送っていい？")
Step 2: Server responds with OK or NG
Step 3: If OK, Browser sends actual request
Step 4: Server responds with data

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                     プリフライトリクエスト                           │
│                   〜本リクエスト前の事前確認〜                        │
│                                                                     │
│   ブラウザ                                      サーバー             │
│   ┌─────┐                                      ┌─────┐             │
│   │     │                                      │     │             │
│   │     │  ① OPTIONS「送っていい？」            │     │             │
│   │     │  ─────────────────────────────────→  │     │             │
│   │     │                                      │     │             │
│   │     │  ←─────────────────────────────────  │     │             │
│   │     │           「OK」                     │     │             │
│   │     │                                      │     │             │
│   │     │  ② 本リクエスト（POST/PUT等）         │     │             │
│   │     │  ─────────────────────────────────→  │     │             │
│   │     │                                      │     │             │
│   │     │  ←─────────────────────────────────  │     │             │
│   │     │           データ                     │     │             │
│   └─────┘                                      └─────┘             │
│                                                                     │
│   ★ 複雑なリクエスト（POST等）は事前確認してから本番                   │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show 2-step flow clearly: preflight → actual
- Emphasize OPTIONS method for step 1
- Show that step 2 only happens if step 1 is OK
```
