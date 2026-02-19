# 9-1-4_c1: ルーティングの基礎

## 対象Section
- Tutorial 9-1-4: ルーティングの基礎
- 説明: URLとコントローラーの対応を示す概念図

## リサーチメモ
- ルーティング = URLと処理先の対応表（道案内役）
- routes/web.php でルーティングを定義
- 流れ: URL → ルーティング → コントローラー → ビュー
- 名前付きルート: route('users.index') で名前からURL生成

## プロンプト

```
Create a clean, modern educational diagram explaining "Laravel Routing Basics" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design with flow diagram
- Colors: Blue for request, Green for routing, Orange for controller
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"ルーティング（Routing）" centered at top
Subtitle: "〜URLとControllerをつなぐ道案内〜"

## Layout
Left-to-right flow: Request → Routing → Controller

## Elements

### Left: Request (blue)
- Browser icon
- URL: /users
- Label: リクエスト

### Center: routes/web.php (green, emphasized)
- Sign post icon
- Table showing URL → Controller mapping:
  | URL     | Controller      |
  |---------|-----------------|
  | /users  | UserController  |
  | /tasks  | TaskController  |
- Label: 道案内役

### Right: Controller (orange)
- Building icon
- UserController
- TaskController
- Label: 処理を実行

### Flow arrows
Request → Routing → Controller

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      ルーティング（Routing）                         │
│                   〜URLとControllerをつなぐ道案内〜                   │
│                                                                     │
│                                                                     │
│   リクエスト              routes/web.php            コントローラー   │
│                                                                     │
│   ┌─────────┐           ┌─────────────────┐        ┌─────────┐     │
│   │         │           │                 │        │         │     │
│   │ 🌐      │           │  🪧 道案内役    │        │ 🏢      │     │
│   │ /users  │  ───────→ │                 │ ─────→ │ User    │     │
│   │         │           │ /users → User   │        │Controller│     │
│   └─────────┘           │ /tasks → Task   │        │         │     │
│                         │                 │        │ Task    │     │
│   「どこに              │                 │        │Controller│     │
│    行けばいい？」        └─────────────────┘        │         │     │
│                                                    └─────────┘     │
│                          ここで行き先を                             │
│                            決める！                 「処理を        │
│                                                      実行！」      │
│                                                                     │
│   ★ routes/web.php = URLと処理先の対応表                            │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show 3-step flow: Request → Routing → Controller
- Emphasize routes/web.php as the central "signpost"
- Include URL to Controller mapping table
- Use icons to represent each component
```
