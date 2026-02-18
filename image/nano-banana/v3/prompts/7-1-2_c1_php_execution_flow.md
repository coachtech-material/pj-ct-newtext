# 7-1-2_c1: PHP実行フロー

## 対象Section
- Tutorial 7-1-2: PHPの実行環境
- 説明: PHPコードの実行フロー（リクエスト→PHP実行→HTML生成→レスポンス）の概念図

## リサーチメモ
- フロー: Browser → Request → Web Server → PHP Interpreter → Output → Response
- Webサーバー（Apache/Nginx）が .php ファイルをPHPインタプリタに渡す
- PHP実行の4段階: Lexing → Parsing → Compilation → Interpretation
- Zend Engine が PHP を Opcodes にコンパイルして実行
- 最終的にHTMLがブラウザに返される（PHPコードは見えない）
- 図解パターン: 線形フロー（左から右）が業界標準
- Sources: [FastComet](https://www.fastcomet.com/tutorials/php-executions-optimization/how-it-works), [Stillat](https://stillat.com/blog/2014/04/02/how-does-php-work-with-the-web-server-and-browser)

## プロンプト

```
Create a clean, modern educational diagram explaining "PHP Execution Flow" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with linear flow
- Colors: 4-color scheme (blue for browser, orange for webserver, green for PHP, gray for HTML)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"PHPの実行フロー" centered at top
Subtitle: "〜リクエストからレスポンスまで〜"

## Elements (left to right flow)
1. Browser (blue): "ブラウザ"
2. Web Server (orange): "Webサーバー"
3. PHP Engine (green): "PHP実行環境"
4. Generated HTML (gray): "HTML"
5. Back to Browser: "表示"

## Flow
① Browser → Web Server: "リクエスト（index.phpください）"
② Web Server → PHP: ".phpファイルなのでPHPに依頼"
③ PHP processes and generates HTML
④ HTML → Browser: "レスポンス（生成されたHTML）"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                       PHPの実行フロー                               │
│                    〜リクエストからレスポンスまで〜                   │
│                                                                     │
│  ① リクエスト                                                       │
│   「index.phpください」                                              │
│                                                                     │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐  │
│  │         │  ①  │         │  ②  │         │  ③  │         │  │
│  │ブラウザ │ ──→ │  Web    │ ──→ │  PHP    │ ──→ │  HTML   │  │
│  │         │      │ サーバー │      │ 実行環境 │      │  生成   │  │
│  │         │      │         │      │         │      │         │  │
│  └────┬────┘      └─────────┘      └─────────┘      └────┬────┘  │
│       │                                                   │        │
│       │                    ④ レスポンス                   │        │
│       │                 「はい、HTMLをどうぞ」             │        │
│       └───────────────────────────────────────────────────┘        │
│                                                                     │
│   ┌────────────────────────────────────────────────────┐           │
│   │  ① ブラウザがWebサーバーにリクエストを送る         │           │
│   │  ② Webサーバーが.phpファイルをPHP実行環境に渡す    │           │
│   │  ③ PHPがコードを実行してHTMLを生成する            │           │
│   │  ④ 生成されたHTMLがブラウザに返される              │           │
│   └────────────────────────────────────────────────────┘           │
│                                                                     │
│   ★ ブラウザが受け取るのは「HTMLだけ」                              │
│   ★ PHPコードはブラウザには見えない（サーバー側で実行済み）         │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Linear flow from browser to server to PHP to HTML back to browser
- Numbered steps for clarity
- Emphasize that browser only sees HTML, not PHP code
- Clear step-by-step explanation
```
