# Tutorial 13-2-5: 書籍編集機能の実装

## 🎯 このセクションで学ぶこと

- 書籍編集画面のedit/updateメソッドを実装する
- old()関数でフォームの初期値を設定する方法を学ぶ
- イシュー駆動開発のフローを継続する

---

## Step 0: 開発の準備（チケット駆動）

### 0-1. GitHubでIssueを確認

GitHubで `#4 書籍編集機能` のIssueを確認します。

### 0-2. ブランチを作成

```bash
git checkout main
git pull origin main
git switch -c feature/issue-4-book-edit
```

---

## Step 1: editメソッドの実装

### 1-1. BookControllerを編集

**ファイル**: `app/Http/Controllers/BookController.php`

```php
/**
 * 書籍編集画面を表示
 */
public function edit(Book $book)
{
    return view('books.edit', compact('book'));
}
```

---

## Step 2: updateメソッドの実装

### 2-1. updateメソッドを実装

**ファイル**: `app/Http/Controllers/BookController.php`

```php
/**
 * 書籍を更新
 */
public function update(Request $request, Book $book)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'author' => 'required|max:255',
        'rating' => 'required|integer|min:1|max:5',
        'review' => 'nullable|max:10000',
    ]);

    $book->update($validated);

    return redirect()
        ->route('books.show', $book)
        ->with('success', '書籍を更新しました。');
}
```

---

### 2-2. コードリーディング

| コード | 説明 |
|:---|:---|
| `$book->update($validated)` | 既存のモデルを更新 |
| `route('books.show', $book)` | 詳細画面にリダイレクト |

---

## Step 3: old()関数の動作

Bladeテンプレートでは、`old()`関数を使ってフォームの初期値を設定しています。

```blade
<input type="text" name="title" value="{{ old('title', $book->title) }}">
```

**動作**:

1. バリデーションエラー時: `old('title')`が返される（入力値が復元される）
2. 初回表示時: `$book->title`が返される（既存の値が表示される）

---

## Step 4: 動作確認

### 4-1. ブラウザで確認

1. `http://localhost/books`にアクセス
2. 書籍の「編集」ボタンをクリック
3. フォームに既存の値が表示されていることを確認
4. 値を変更して「更新」をクリック
5. 詳細画面にリダイレクトされ、変更が反映されていることを確認

---

## Step 5: コミット、PR、マージ

### 5-1. コミット

```bash
git add .
git commit -m "feat: 書籍編集機能の実装 (Closes #4)"
```

### 5-2. プッシュ、PR、マージ

```bash
git push origin feature/issue-4-book-edit
```

GitHubでPRを作成し、セルフレビュー後にマージします。

### 5-3. ローカルの更新

```bash
git checkout main
git pull origin main
git branch -d feature/issue-4-book-edit
```

---

## ✨ まとめ

このセクションでは、書籍編集機能の実装について学びました。

| Step | 学んだこと |
|:---|:---|
| Step 0 | イシュー駆動開発の流れ |
| Step 1-2 | edit/updateメソッドの実装 |
| Step 3 | old()関数の動作 |
| Step 4-5 | 動作確認、コミット、PR、マージ |

次のセクションでは、書籍削除機能を実装します。

---
