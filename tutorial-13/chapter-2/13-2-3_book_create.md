# Tutorial 13-2-3: 書籍登録機能の実装

## 🎯 このセクションで学ぶこと

- 書籍登録画面のcreate/storeメソッドを実装する
- バリデーションを設定する
- イシュー駆動開発のフローを継続する

---

## Step 0: 開発の準備（チケット駆動）

### 0-1. GitHubでIssueを確認

GitHubで `#2 書籍登録機能` のIssueを確認します。

### 0-2. mainブランチを最新化

```bash
git checkout main
git pull origin main
```

### 0-3. Issue番号付きブランチを作成

```bash
git switch -c feature/issue-2-book-create
```

---

## Step 1: createメソッドの実装

### 1-1. BookControllerを編集

**ファイル**: `app/Http/Controllers/BookController.php`

```php
/**
 * 書籍登録画面を表示
 */
public function create()
{
    return view('books.create');
}
```

---

## Step 2: storeメソッドの実装

### 2-1. storeメソッドを実装

**ファイル**: `app/Http/Controllers/BookController.php`

```php
/**
 * 書籍を登録
 */
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'author' => 'required|max:255',
        'rating' => 'required|integer|min:1|max:5',
        'review' => 'nullable|max:10000',
    ]);

    Book::create($validated);

    return redirect()
        ->route('books.index')
        ->with('success', '書籍を登録しました。');
}
```

---

### 2-2. コードリーディング

| コード | 説明 |
|:---|:---|
| `$request->validate([...])` | バリデーションを実行し、成功したら検証済みデータを返す |
| `'required'` | 必須項目 |
| `'max:255'` | 最大255文字 |
| `'integer\|min:1\|max:5'` | 1〜5の整数 |
| `'nullable'` | NULL許可（任意項目） |
| `Book::create($validated)` | 検証済みデータで書籍を作成 |
| `->with('success', ...)` | フラッシュメッセージをセッションに保存 |

---

## Step 3: 動作確認

### 3-1. ブラウザで確認

1. `http://localhost/books`にアクセス
2. 「新規登録」ボタンをクリック
3. フォームに入力して「登録」をクリック
4. 一覧画面にリダイレクトされ、成功メッセージが表示されることを確認

### 3-2. バリデーションエラーの確認

1. タイトルを空にして「登録」をクリック
2. エラーメッセージが表示されることを確認

---

## Step 4: コミット、PR、マージ

### 4-1. コミット

```bash
git add .
git commit -m "feat: 書籍登録機能の実装 (Closes #2)"
```

### 4-2. プッシュ

```bash
git push origin feature/issue-2-book-create
```

### 4-3. PR作成とマージ

1. GitHubでPRを作成
2. セルフレビュー（Diff確認）
3. マージ
4. Issue #2が自動クローズされることを確認

### 4-4. ローカルの更新

```bash
git checkout main
git pull origin main
git branch -d feature/issue-2-book-create
```

---

## 🚨 よくある間違い

### 間違い1: バリデーションエラーが表示されない

**対処法**: Bladeテンプレートに`@error`ディレクティブがあるか確認します。

```blade
@error('title')
    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
@enderror
```

---

### 間違い2: old()で入力値が復元されない

**対処法**: inputタグに`value="{{ old('title') }}"`が設定されているか確認します。

---

## ✨ まとめ

このセクションでは、書籍登録機能の実装について学びました。

| Step | 学んだこと |
|:---|:---|
| Step 0 | イシュー駆動開発の流れ（ブランチ作成） |
| Step 1-2 | create/storeメソッドの実装 |
| Step 3 | バリデーションの動作確認 |
| Step 4 | コミット、PR、マージ |

次のセクションでは、書籍詳細画面を実装します。

---
