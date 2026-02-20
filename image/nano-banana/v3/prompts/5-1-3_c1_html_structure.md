# 5-1-3_c1: HTML基本構造

## 対象Section
- Tutorial 5-1-3: HTMLの基本構造
- 説明: HTML文書の基本構造（DOCTYPE・html・head・body）の概念図

## リサーチメモ
- HTML文書はツリー構造（階層構造）
- DOCTYPE: HTML5宣言（HTMLのバージョンを示す）
- html: ルート要素（head と body を含む）
- head: メタデータ（title, meta, link など）- 画面に表示されない
- body: 表示コンテンツ（実際にブラウザに表示される内容）
- 図解パターン: 入れ子ボックス構造（nested boxes）が業界標準
- Sources: [W3C](https://www.w3.org/TR/html401/struct/global.html), [web.dev](https://web.dev/learn/html/document-structure), [MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/Structuring_documents)

## プロンプト

```
Create a clean, modern educational diagram explaining "HTML Document Structure" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with nested boxes
- Colors: 4-color scheme (gray for DOCTYPE, blue for html, orange for head, green for body)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"HTML文書の基本構造" centered at top
Subtitle: "〜4つの重要なパーツ〜"

## Elements (nested structure)
1. DOCTYPE (gray bar at top): "<!DOCTYPE html>" - 「HTML5宣言」
2. html (blue outer box): "<html>" - 「文書全体を囲む」
3. head (orange inner box, top): "<head>" - 「裏方の情報」
4. body (green inner box, bottom): "<body>" - 「表示される内容」

## Labels
- DOCTYPE: "おまじない（HTML5ですよ宣言）"
- html: "ルート要素（一番外側）"
- head: "メタ情報（タイトル、文字コードなど）※画面には表示されない"
- body: "本体（実際に画面に表示される内容）"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                     HTML文書の基本構造                               │
│                      〜4つの重要なパーツ〜                            │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  <!DOCTYPE html>  ← おまじない（HTML5ですよ宣言）             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ <html>  ← ルート要素（一番外側）                              │   │
│  │  ┌───────────────────────────────────────────────────────┐  │   │
│  │  │ <head>  ← 裏方の情報                                   │  │   │
│  │  │                                                        │  │   │
│  │  │  • <meta charset="UTF-8">  文字コード                  │  │   │
│  │  │  • <title>ページタイトル</title>  タブに表示            │  │   │
│  │  │                                                        │  │   │
│  │  │  ※ 画面には表示されない                                │  │   │
│  │  └───────────────────────────────────────────────────────┘  │   │
│  │                                                              │   │
│  │  ┌───────────────────────────────────────────────────────┐  │   │
│  │  │ <body>  ← 本体（実際に表示される内容）                  │  │   │
│  │  │                                                        │  │   │
│  │  │  • <h1>見出し</h1>                                     │  │   │
│  │  │  • <p>段落</p>                                         │  │   │
│  │  │  • 画像、リンク、など...                                │  │   │
│  │  │                                                        │  │   │
│  │  │  ※ ここに書いた内容がブラウザに表示される               │  │   │
│  │  └───────────────────────────────────────────────────────┘  │   │
│  │                                                              │   │
│  │ </html>                                                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show nested box structure (html contains head and body)
- Color-coded sections for easy identification
- Clear distinction between head (hidden) and body (visible)
- Japanese labels explaining each part's role
```
