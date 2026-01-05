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

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ詳細の次に編集機能なのか？」

詳細画面ができたら、次は**編集機能**を作ります。

### 理由1: 詳細から編集への流れが自然

```
❌ 削除から作る
→ 「このデータを削除したい」より「修正したい」が先

✅ 編集を先に作る
→ 詳細画面で「ここを直したい」と思う
→ 編集ボタンを押す流れが自然
```

### 理由2: CRUDの「U」（更新）を実装

作成（C）、読み取り（R）が終わったので、次は更新（U）です。

---

### このセクションの実装順序

| 順番 | 作業 | 理由 |
|:---:|:---|:---|
| 1 | editメソッド実装 | 編集画面を表示するため |
| 2 | updateメソッド実装 | フォーム送信を受け取るため |
| 3 | 動作確認 | 更新が正しく動くかテスト |

---

### コードの実装順序（updateメソッド）

```php
public function update(Request $request, Book $book)
{
    // ① まずバリデーション
    $validated = $request->validate([...]);
    
    // ② 既存データを更新
    $book->update($validated);
    
    // ③ 詳細にリダイレクト
    return redirect()->route('books.show', $book)->with('success', '...');
}
```

| 順番 | コード | 考え方 |
|:---:|:---|:---|
| ① | `$request->validate([...])` | 「入力は正しいか？」を確認 |
| ② | `$book->update($validated)` | 「既存データを更新」 |
| ③ | `return redirect()...` | 「結果を見せる」 |

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

#### `$book->update($validated)`の分解

| 部分 | 説明 |
|:---|:---|
| `$book` | ルートモデルバインディングで取得したBookインスタンス |
| `->` | インスタンスメソッド呼び出し |
| `update($validated)` | 検証済みデータで更新 |

> 💡 **createとupdateの違い**: `Book::create()`は新規作成（静的メソッド）、`$book->update()`は既存更新（インスタンスメソッド）です。

#### `route('books.show', $book)`の分解

| 部分 | 説明 |
|:---|:---|
| `route('books.show', ...)` | books.showルートのURLを生成 |
| `$book` | ルートパラメータとしてBookインスタンスを渡す |

```php
// この2つは同じ意味
route('books.show', $book)      // ← モデルを渡す（推奨）
route('books.show', $book->id)  // ← IDを渡す
```

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
