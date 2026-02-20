# 9-2-4_c2: @extends/@section/@yield

## 対象Section
- Tutorial 9-2-4: Bladeファイルの読み解き方（レイアウトとコンポーネント）
- 説明: @extends/@section/@yieldの関係を示す概念図

## リサーチメモ
- @yield('name'): 親側で「穴」を定義（子からコンテンツが入る場所）
- @section('name', 'value'): 1行で値を差し込む（短い値向け）
- @section('name') ... @endsection: 複数行のコンテンツを差し込む
- マッピング: @yield('content') ← @section('content')
- 図解パターン: 左右比較（親 | 子）で対応関係を矢印で表示
- Sources: [Laravel Docs](https://laravel.com/docs/blade#defining-a-layout)

## プロンプト

```
Create a clean, modern educational diagram explaining "Blade @extends, @section, @yield" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with mapping visualization
- Colors: 3-color palette (blue for @yield, orange for @section, green for result)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"@extends / @section / @yield" centered at top
Subtitle: "〜コンテンツの差し込み方〜"

## Elements
Show mapping between:
- @yield('title') ← @section('title', 'ページタイトル')
- @yield('content') ← @section('content') ... @endsection

## Code examples
Layout side: @yield
Child side: @section

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                    @extends / @section / @yield                     │
│                                                                     │
│  【レイアウト側】                    【子ビュー側】                   │
│                                                                     │
│  ┌──────────────────────┐         ┌──────────────────────┐        │
│  │                      │         │ @extends             │        │
│  │ <title>              │         │                      │        │
│  │   @yield('title')    │←───────│ @section('title')    │        │
│  │ </title>             │   差込  │                      │        │
│  │                      │         │                      │        │
│  │ <main>               │         │ @section('content')  │        │
│  │   @yield('content')  │←───────│   コンテンツ          │        │
│  │ </main>              │   差込  │ @endsection          │        │
│  │                      │         │                      │        │
│  └──────────────────────┘         └──────────────────────┘        │
│                                                                     │
│  @yield = 穴を開ける     @section = 穴に差し込む                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show clear mapping between @yield and @section
- Two forms: inline @section('name', 'value') and block @section...@endsection
- Use arrows to show insertion
- Keep code examples minimal and clear
```
