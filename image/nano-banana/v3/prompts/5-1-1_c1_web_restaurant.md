# 5-1-1_c1: Webページの仕組み（レストラン比喩）

## 対象Section
- Tutorial 5-1-1: Webページの仕組み
- 説明: レストラン比喩によるクライアントサーバーモデルの概念図

## リサーチメモ
- クライアントサーバーモデル: リクエスト→レスポンスのフロー
- クライアント = サービスを要求する側（ブラウザ）
- サーバー = サービスを提供する側（Webサーバー）
- HTTP通信: TCP接続を確立 → リクエスト送信 → レスポンス受信
- 1つのサーバーが複数クライアントにサービス提供
- 図解パターン: 左右分割（Client | Server）で双方向矢印
- Sources: [ToolsQA](https://toolsqa.com/client-server/client-server-architecture-and-model), [GeeksforGeeks](https://www.geeksforgeeks.org/system-design/client-server-model/)

## プロンプト

```
Create a clean, modern educational diagram explaining "How Web Pages Work" for programming beginners using a restaurant metaphor.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with minimal elements
- Colors: 3-color palette (blue for client, orange for internet, green for server)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Webページの仕組み" centered at top
Subtitle: "〜レストランに例えると〜"

## Elements (left to right flow)
1. Client (blue): Computer/browser icon, label "クライアント（お客さん）"
2. Internet (orange): Cloud/network icon, label "インターネット（ウェイター）"
3. Server (green): Server rack icon, label "サーバー（キッチン）"

## Flow (bidirectional arrows)
① Client → Server: "リクエスト（注文）"
② Server → Client: "レスポンス（料理）"

## Sub-labels
- Client: "ページをください！"
- Server: "はい、どうぞ！"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      Webページの仕組み                               │
│                     〜レストランに例えると〜                          │
│                                                                     │
│   【クライアント】           【インターネット】          【サーバー】   │
│   （お客さん）               （ウェイター）              （キッチン）   │
│                                                                     │
│   ┌──────────────┐        ┌──────────────┐        ┌──────────────┐ │
│   │   🖥️         │   ①   │    🌐        │   ①   │    🖥️        │ │
│   │   ブラウザ    │ ────→ │              │ ────→ │   Webサーバー │ │
│   │              │リクエスト│              │        │              │ │
│   │ 「ページを    │ (注文)  │    運ぶ      │        │  HTMLを準備   │ │
│   │  ください！」 │        │              │        │              │ │
│   │              │ ←──── │              │ ←──── │ 「はい、     │ │
│   │   表示する   │レスポンス│              │   ②   │  どうぞ！」  │ │
│   │              │ (料理)  │              │        │              │ │
│   └──────────────┘        └──────────────┘        └──────────────┘ │
│                                                                     │
│   ★ クライアント = サービスを要求する側（ブラウザ）                   │
│   ★ サーバー = サービスを提供する側（Webサーバー）                    │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Clear restaurant metaphor (customer, waiter, kitchen)
- Request/Response flow with numbered arrows
- Simple icons for each role
- Japanese labels must be clear and readable
```
