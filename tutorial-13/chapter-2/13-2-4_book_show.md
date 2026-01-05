# Tutorial 13-2-4: 書籍詳細画面の実装

## 🎯 このセクションで学ぶこと

- 書籍詳細画面のshowメソッドを実装する
- ルートモデルバインディングを理解する
- イシュー駆動開発のフローを継続する

---

## Step 0: 開発の準備（チケット駆動）

### 0-1. GitHubでIssueを確認

GitHubで `#3 書籍詳細機能` のIssueを確認します。

### 0-2. ブランチを作成

```bash
git checkout main
git pull origin main
git switch -c feature/issue-3-book-show
```

---

## Step 1: showメソッドの実装

### 1-1. BookControllerを編集

**ファイル**: `app/Http/Controllers/BookController.php`

```php
/**
 * 書籍詳細を表示
 */
public function show(Book $book)
{
    return view('books.show', compact('book'));
}
```

---

### 1-2. ルートモデルバインディングとは

`show(Book $book)`の引数に注目してください。

```php
// URLが /books/1 の場合
public function show(Book $book)
{
    // $book には id=1 の Book モデルが自動的に注入される
    // Book::find(1) を書く必要がない！
}
```

Laravelは、URLの`{book}`部分を見て、自動的に`Book::find($id)`を実行し、結果を`$book`に注入します。これを**ルートモデルバインディング**と呼びます。

**メリット**:
- コードがシンプルになる
- 存在しないIDの場合、自動的に404エラーを返す

---

## Step 2: 動作確認

### 2-1. ブラウザで確認

1. `http://localhost/books`にアクセス
2. 書籍のタイトルをクリック
3. 詳細画面が表示されることを確認

### 2-2. 存在しないIDでアクセス

`http://localhost/books/999`にアクセスすると、404エラーが表示されることを確認します。

---

## Step 3: コミット、PR、マージ

### 3-1. コミット

```bash
git add .
git commit -m "feat: 書籍詳細画面の実装 (Closes #3)"
```

### 3-2. プッシュ、PR、マージ

```bash
git push origin feature/issue-3-book-show
```

GitHubでPRを作成し、セルフレビュー後にマージします。

### 3-3. ローカルの更新

```bash
git checkout main
git pull origin main
git branch -d feature/issue-3-book-show
```

---

## ✨ まとめ

このセクションでは、書籍詳細画面の実装について学びました。

| Step | 学んだこと |
|:---|:---|
| Step 0 | イシュー駆動開発の流れ |
| Step 1 | showメソッドとルートモデルバインディング |
| Step 2-3 | 動作確認、コミット、PR、マージ |

次のセクションでは、書籍編集機能を実装します。

---
