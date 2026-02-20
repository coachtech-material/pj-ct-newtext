# 9-2-4_c1: Bladeレイアウト継承

## 対象Section
- Tutorial 9-2-4: Bladeファイルの読み解き方（レイアウトとコンポーネント）
- 説明: レイアウト継承の仕組みを示す概念図

## リサーチメモ
- Blade: Laravelのテンプレートエンジン
- レイアウト継承: 共通部分（ヘッダー、フッター）を親で定義、個別部分を子で差し込み
- @extends: 親レイアウトを継承
- @yield: 子から挿入される場所（プレースホルダー）
- @section: @yieldに差し込むコンテンツを定義
- DRY原則（Don't Repeat Yourself）の実践
- 図解パターン: 親→子の継承関係と最終出力を表示
- Sources: [Laravel Docs](https://laravel.com/docs/blade)

## プロンプト

```
Create a clean, modern educational diagram explaining "Blade Layout Inheritance" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with inheritance visualization
- Colors: 3-color palette (blue for parent layout, orange for child view, green for shared parts)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Bladeレイアウト継承" centered at top
Subtitle: "〜共通部分を1箇所で管理〜"

## Elements
Left/Top: Parent layout (layouts/app.blade.php)
- Header (shared)
- @yield('content') placeholder
- Footer (shared)

Right/Bottom: Child view (users/index.blade.php)
- @extends('layouts.app')
- @section('content') with actual content

## Key concept
- 共通部分（ヘッダー、フッター）を1箇所で管理
- 個別コンテンツだけを差し替え

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      Bladeレイアウト継承                             │
│                                                                     │
│    【親レイアウト】                   【子ビュー】                    │
│                                                                     │
│    ┌─────────────────────┐         ┌─────────────────────┐         │
│    │ <header>           │         │ @extends            │         │
│    │   共通ナビ          │   継承   │                     │         │
│    ├─────────────────────┤ ←────── │ @section('content') │         │
│    │                     │         │   個別コンテンツ     │         │
│    │   @yield('content') │ ← 挿入  │ @endsection         │         │
│    │                     │         │                     │         │
│    ├─────────────────────┤         └─────────────────────┘         │
│    │ <footer>           │                                          │
│    │   共通フッター       │                                          │
│    └─────────────────────┘                                          │
│                                                                     │
│                          ↓ 結合                                      │
│                                                                     │
│    ┌─────────────────────────────────────────┐                     │
│    │ <header> 共通ナビ </header>              │                     │
│    │ <main> 個別コンテンツ </main>            │                     │
│    │ <footer> 共通フッター </footer>          │                     │
│    └─────────────────────────────────────────┘                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show parent-child relationship clearly
- Demonstrate @yield as placeholder
- Show final combined result
- Emphasize DRY principle (Don't Repeat Yourself)
```
