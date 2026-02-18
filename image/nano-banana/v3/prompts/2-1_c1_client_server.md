# 2-1_c1: クライアントサーバーモデル

## 対象Section
- Tutorial 2-1: 開発環境とは
- 説明: クライアントサーバーモデルの概念図

## リサーチメモ
- クライアントサーバーモデル: リクエスト→レスポンスの基本アーキテクチャ
- クライアント = サービスを要求する側（ブラウザ、アプリ）
- サーバー = サービスを提供する側（Webサーバー、DBサーバー）
- 1サーバーが複数クライアントにサービス提供
- HTTP/HTTPS通信でリクエスト/レスポンスをやり取り
- 図解パターン: 左右分割（Client | Server）で双方向矢印が業界標準
- Sources: [GeeksforGeeks](https://www.geeksforgeeks.org/system-design/client-server-model/), [Cloudflare](https://www.cloudflare.com/learning/serverless/glossary/client-side-vs-server-side/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Client-Server Model" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with minimal elements
- Colors: 3-color palette (blue for client, orange for arrows, green for server)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"クライアントサーバーモデル" centered at top
Subtitle: "〜Webの基本的な仕組み〜"

## Elements (2 main components)
1. Client (left): Computer/browser icon, label "クライアント（ブラウザ）"
2. Server (right): Server rack icon, label "サーバー"

## Flow (bidirectional arrows)
① Client → Server: "リクエスト（ページをください）"
② Server → Client: "レスポンス（HTMLデータ）"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                   クライアントサーバーモデル                          │
│                     〜Webの基本的な仕組み〜                          │
│                                                                     │
│      【クライアント】                          【サーバー】          │
│                                                                     │
│   ┌──────────────────┐                    ┌──────────────────┐     │
│   │                  │                    │                  │     │
│   │   🖥️ ブラウザ    │      ① リクエスト  │   🖥️ Webサーバー │     │
│   │                  │  ─────────────────→│                  │     │
│   │  （Chrome など）  │  「ページください」 │   （データ保管）  │     │
│   │                  │                    │                  │     │
│   │                  │  ←─────────────────│                  │     │
│   │   表示する       │      ② レスポンス  │   データを送る    │     │
│   │                  │   「HTMLをどうぞ」  │                  │     │
│   └──────────────────┘                    └──────────────────┘     │
│                                                                     │
│   ★ クライアント = サービスを要求する側                             │
│   ★ サーバー = サービスを提供する側                                 │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Simple left-to-right layout
- Clear request/response arrows with Japanese labels
- Icons for client (browser) and server
- Emphasize the bidirectional communication
```
