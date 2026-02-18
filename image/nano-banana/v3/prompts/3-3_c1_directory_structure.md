# 3-3_c1: ディレクトリ構造

## 対象Section
- Tutorial 3-3: ディレクトリ構造の理解
- 説明: ファイルシステムのツリー構造を示す概念図

## リサーチメモ
- ファイルシステムは逆さの木構造（ルートが上、下に広がる）
- / = ルート（最上位）、~ = ホーム、. = カレント、.. = 親
- treeコマンドで可視化（│, ├──, └── のボックス描画文字使用）
- Unix系OSの標準構造: /Users, /Applications, /System など
- 図解パターン: 垂直ツリー構造（上から下へ）が業界標準
- Sources: [GeeksforGeeks](https://www.geeksforgeeks.org/linux-unix/tree-command-unixlinux/), [NIU CS](https://faculty.cs.niu.edu/~mcmahon/CS241/Notes/Unix_Reference/file_structure.html)

## プロンプト

```
Create a clean, modern educational diagram explaining "Directory Structure (Tree)" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with minimal elements
- Colors: 3-color palette (blue for root, orange for directories, green for files)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"ディレクトリ構造" centered at top
Subtitle: "〜コンピュータのファイルは木構造〜"

## Elements
Tree diagram showing file system hierarchy:
- Root "/" at top (blue circle, largest)
- Second level: "Users", "Applications", "System" (orange rounded rectangles)
- Third level under Users: "YourName" (orange)
- Fourth level under YourName: "Desktop", "Documents", "Downloads" (orange)
- Fifth level under Desktop: "hello-world" folder with "index.html" file (green for file)

## Labels (Japanese)
- "/" → "ルート（根っこ）"
- "~" symbol near YourName → "ホーム（自分の部屋）"
- Current position indicator → "カレント（今いる場所）"
- ".." arrow pointing up → "親ディレクトリ（一つ上）"

## Layout
- Vertical tree structure, top to bottom
- Lines connecting parent-child relationships
- Clear indentation showing depth
- Legend box showing 4 special directories: /, ~, ., ..

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                     ディレクトリ構造                                  │
│                   〜コンピュータのファイルは木構造〜                    │
│                                                                     │
│                          [ / ]  ← ルート（根っこ）                   │
│                            │                                        │
│            ┌───────────────┼───────────────┐                        │
│            │               │               │                        │
│        [Users]        [Applications]   [System]                     │
│            │                                                        │
│       [YourName]  ← ホーム ~ （自分の部屋）                          │
│            │                                                        │
│    ┌───────┼───────┐                                                │
│    │       │       │                                                │
│ [Desktop] [Documents] [Downloads]                                   │
│    │                                                                │
│ [hello-world]  ← カレント . （今いる場所）                           │
│    │                                                                │
│ 📄index.html                                                        │
│                                                                     │
│  ┌─────────────────────────────────────┐                           │
│  │ 記号    │  意味                      │                           │
│  │─────────│────────────────────────────│                           │
│  │   /     │  ルート（最上位）           │                           │
│  │   ~     │  ホーム（自分の部屋）       │                           │
│  │   .     │  カレント（今いる場所）     │                           │
│  │   ..    │  親（一つ上の階層）         │                           │
│  └─────────────────────────────────────┘                           │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Tree grows downward (root at top)
- Clear visual hierarchy with indentation
- Color-coded: blue=root, orange=directories, green=files
- Legend table essential for understanding special symbols
- Japanese labels must be clear and readable
```
