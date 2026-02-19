# 3-5_c1: 絶対パスと相対パス

## 対象Section
- Tutorial 3-5: パスの概念
- 説明: 絶対パスと相対パスの違いを示す概念図

## リサーチメモ
- 絶対パス: ルート(/)から始まる完全な住所、どこからでも同じ場所を指す
- 相対パス: 現在地を基準にした道順、短く書けるが現在地で変わる
- 特殊記号: `.`=カレントディレクトリ、`..`=親ディレクトリ
- 比喩: 絶対パス=完全な住所、相対パス=道順の説明

## プロンプト

```
Create a clean, modern educational diagram comparing "Absolute Path vs Relative Path" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design with 2-column comparison
- Colors: Blue for absolute path, Orange for relative path
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"絶対パス vs 相対パス" centered at top
Subtitle: "〜ファイルの住所の2つの書き方〜"

## Layout
Top: Shared directory tree
Bottom: 2-column comparison

## Elements

### Directory Tree (top, shared)
/
└── Users
    └── YourName
        └── Desktop ← 現在地 (orange highlight)
            └── hello-world
                └── index.html ← 目的地 (blue highlight)

### Left Column: 絶対パス (blue)
- Icon: Map pin
- Example: /Users/YourName/Desktop/hello-world/index.html
- Features:
  - 必ず / から始まる
  - どこからでも同じ場所を指す
  - 長くなりがち

### Right Column: 相対パス (orange)
- Icon: Footsteps
- Example: hello-world/index.html
- Features:
  - / から始まらない
  - 現在地によって変わる
  - 短く書ける

### Special symbols box (bottom)
- . = 現在地
- .. = 一つ上

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      絶対パス vs 相対パス                            │
│                   〜ファイルの住所の2つの書き方〜                     │
│                                                                     │
│                    【ディレクトリ構造】                               │
│                        /                                            │
│                        └── Users                                    │
│                            └── YourName                             │
│                                └── Desktop ← 現在地                 │
│                                    └── hello-world                  │
│                                        └── index.html               │
│                                                                     │
│   ┌─────────────────────┐       ┌─────────────────────┐            │
│   │     絶対パス         │       │     相対パス         │            │
│   │  📍 完全な住所       │       │  👣 道順の説明       │            │
│   │                     │       │                     │            │
│   │ /Users/YourName/    │       │ hello-world/        │            │
│   │ Desktop/hello-world/│       │ index.html          │            │
│   │ index.html          │       │                     │            │
│   │                     │       │                     │            │
│   │ ✓ / から始まる      │       │ ✓ / から始まらない   │            │
│   │ ✓ どこでも同じ場所  │       │ ✓ 現在地で変わる    │            │
│   │ ✓ 長い             │       │ ✓ 短い             │            │
│   └─────────────────────┘       └─────────────────────┘            │
│                                                                     │
│   【特殊記号】 . = 現在地  /  .. = 一つ上                            │
│                                                                     │
│   ★ 絶対パス=確実だが長い / 相対パス=短いが現在地を把握必要          │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show directory tree at top with current location highlighted
- Two-column comparison below
- Clear color distinction: blue vs orange
- Include special symbols (. and ..)
```
