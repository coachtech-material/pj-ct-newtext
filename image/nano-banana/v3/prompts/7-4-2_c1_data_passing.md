# 7-4-2_c1: ファイル間のデータ受け渡し

## 対象Section
- Tutorial 7-4-2: PHPファイル間のデータ受け渡し
- 説明: 複数PHPファイル間のデータ受け渡しフローの概念図

## リサーチメモ
- Webアプリの基本パターン: 入力→処理→完了の3ページフロー
- POST: フォームデータをサーバーに送信（$_POSTで受け取る）
- GET: URLパラメータで送信（$_GETで受け取る）
- header("Location: ..."): PHPでのリダイレクト
- PRG（Post/Redirect/Get）パターン: 二重送信を防ぐ定石
- 図解パターン: 3ページの線形フロー（input → process → complete）
- Sources: [PHP Documentation](https://www.php.net/manual/en/reserved.variables.post.php)

## プロンプト

```
Create a clean, modern educational diagram explaining "Data Passing Between PHP Files" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with flow diagram
- Colors: 4-color scheme (blue for input, orange for process, green for complete, gray for data flow)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"PHPファイル間のデータ受け渡し" centered at top
Subtitle: "〜ページ遷移とデータの流れ〜"

## Elements (3-page flow)
1. Input page (blue): "input.php（入力画面）"
2. Process page (orange): "process.php（処理画面）"
3. Complete page (green): "complete.php（完了画面）"

## Flow with data
- Input → Process: "POST送信（フォームデータ）"
- Process → Complete: "リダイレクト（header）"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                  PHPファイル間のデータ受け渡し                       │
│                    〜ページ遷移とデータの流れ〜                       │
│                                                                     │
│   【入力画面】              【処理画面】              【完了画面】   │
│    input.php                process.php              complete.php  │
│                                                                     │
│   ┌──────────────┐        ┌──────────────┐        ┌──────────────┐ │
│   │              │        │              │        │              │ │
│   │  📝 フォーム │   ①   │  ⚙️ データ処理│   ②   │  ✅ 完了表示 │ │
│   │              │ ────→ │              │ ────→ │              │ │
│   │  名前: [   ] │  POST  │ $_POST で受取│ header │  登録完了！  │ │
│   │  [送信]     │  送信   │  DB保存など  │リダイレクト│             │ │
│   │              │        │              │        │              │ │
│   └──────────────┘        └──────────────┘        └──────────────┘ │
│                                                                     │
│   ┌────────────────────────────────────────────────────┐           │
│   │  ① フォーム送信（POST）                            │           │
│   │     <form action="process.php" method="post">      │           │
│   │     → $_POST["name"] でデータを受け取る            │           │
│   │                                                    │           │
│   │  ② リダイレクト                                    │           │
│   │     header("Location: complete.php");              │           │
│   │     exit;                                          │           │
│   └────────────────────────────────────────────────────┘           │
│                                                                     │
│   ★ $_POST: フォームデータの受け渡し                                │
│   ★ $_GET: URLパラメータの受け渡し                                  │
│   ★ header(): ページの自動遷移（リダイレクト）                      │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show 3-page flow common in web applications
- POST for form data, header() for redirect
- Include code snippets for key operations
- Clear numbered steps
```
