# 13-7-1_c1: 公開API

## 対象Section
- Tutorial 13-7-1: 公開API実装
- 説明: WebコントローラとAPIコントローラの違いの概念図

## リサーチメモ
- WebコントローラとAPIコントローラの違い:
  - Web: HTMLビュー返却、セッション認証、routes/web.php
  - API: JSON返却、トークン認証（今回は認証なし）、routes/api.php
- APIリソース: レスポンス形式を統一
- 配置: app/Http/Controllers/Api/
- 今回: 認証なしの公開API

## プロンプト

```
Create a clean, modern educational diagram comparing "Web Controller vs API Controller" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: 2-column comparison
- Colors: Blue for Web, Orange for API
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"WebコントローラとAPIコントローラ" centered at top
Subtitle: "〜HTMLを返すか、JSONを返すか〜"

## Layout
2-column comparison: Web (left) vs API (right)

## Elements

### Web Controller (blue, left)
- Request → Controller → HTML View
- routes/web.php
- Response: HTML
- 認証: セッション（Cookie）
- 用途: ブラウザ表示用

### API Controller (orange, right)
- Request → Controller → JSON
- routes/api.php
- Response: JSON
- 認証: トークン（今回は認証なし）
- 用途: プログラムからのアクセス

### Request/Response visualization
Web: Browser → Server → HTML page
API: Client App → Server → JSON data

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                WebコントローラとAPIコントローラ                       │
│                 〜HTMLを返すか、JSONを返すか〜                        │
│                                                                     │
│   ┌──────────────────────┐     ┌──────────────────────┐            │
│   │   Webコントローラ     │     │   APIコントローラ     │            │
│   │                      │     │                      │            │
│   │   🌐 → HTML          │     │   📱 → JSON          │            │
│   │                      │     │                      │            │
│   └──────────────────────┘     └──────────────────────┘            │
│                                                                     │
│   ┌──────────────────────┬──────────────────────┐                  │
│   │   Webコントローラ     │   APIコントローラ     │                  │
│   ├──────────────────────┼──────────────────────┤                  │
│   │ レスポンス: HTML      │ レスポンス: JSON      │                  │
│   │ return view(...)    │ return response()->   │                  │
│   │                      │          json(...)   │                  │
│   ├──────────────────────┼──────────────────────┤                  │
│   │ ルート: web.php      │ ルート: api.php       │                  │
│   │ URL: /tasks         │ URL: /api/tasks       │                  │
│   ├──────────────────────┼──────────────────────┤                  │
│   │ 認証: セッション      │ 認証: トークン        │                  │
│   │ （Cookie）           │ （または認証なし）     │                  │
│   ├──────────────────────┼──────────────────────┤                  │
│   │ 用途:                │ 用途:                 │                  │
│   │ ブラウザ表示         │ 外部アプリ連携        │                  │
│   │                      │ モバイルアプリ        │                  │
│   └──────────────────────┴──────────────────────┘                  │
│                                                                     │
│   【APIレスポンス例】                                                │
│   {                                                                 │
│     "id": 1,                                                        │
│     "title": "会議の準備",                                          │
│     "priority_label": "高"                                          │
│   }                                                                 │
│                                                                     │
│   ★ Web = 人が見るHTML / API = プログラムが使うJSON                   │
└─────────────────────────────────────────────────────────────────────┘

## Important
- 2-column comparison format
- Show HTML vs JSON response difference
- Include route file difference (web.php vs api.php)
- Show JSON response example
```
