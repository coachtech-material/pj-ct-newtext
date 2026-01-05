# Tutorial 13-4-2: ユーザーと書籍の関連付け

## 🎯 このセクションで学ぶこと

- booksテーブルにuser_idカラムを追加する
- UserモデルとBookモデルのリレーションを設定する
- ログインユーザーの書籍のみを表示・編集できるようにする

---

## Step 0: 開発の準備（チケット駆動）

### 0-1. GitHubでIssueを確認

GitHubで `#8 ユーザー別レビュー管理` のIssueを確認します。

### 0-2. ブランチを作成

```bash
git checkout main
git pull origin main
git switch -c feature/issue-8-user-books
```

---

## Step 1: マイグレーションでuser_idを追加

### 1-1. マイグレーションファイルを作成

```bash
sail artisan make:migration add_user_id_to_books_table
```

### 1-2. マイグレーションファイルを編集

**ファイル**: `database/migrations/xxxx_xx_xx_xxxxxx_add_user_id_to_books_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('books', function (Blueprint $table) {
            $table->foreignId('user_id')->after('id')->constrained()->onDelete('cascade');
        });
    }

    public function down(): void
    {
        Schema::table('books', function (Blueprint $table) {
            $table->dropForeign(['user_id']);
            $table->dropColumn('user_id');
        });
    }
};
```

### 1-3. マイグレーションを実行

```bash
sail artisan migrate
```

---

## Step 2: リレーションの設定

### 2-1. Userモデルにリレーションを追加

**ファイル**: `app/Models/User.php`

```php
/**
 * ユーザーが持つ書籍
 */
public function books()
{
    return $this->hasMany(Book::class);
}
```

### 2-2. Bookモデルにリレーションを追加

**ファイル**: `app/Models/Book.php`

```php
/**
 * 書籍を所有するユーザー
 */
public function user()
{
    return $this->belongsTo(User::class);
}
```

### 2-3. fillableにuser_idを追加

**ファイル**: `app/Models/Book.php`

```php
protected $fillable = [
    'user_id',
    'title',
    'author',
    'rating',
    'review',
];
```

---

## Step 3: コントローラーの修正

### 3-1. indexメソッド（自分の書籍のみ表示）

**ファイル**: `app/Http/Controllers/BookController.php`

```php
public function index()
{
    $books = auth()->user()->books()->latest()->get();
    
    return view('books.index', compact('books'));
}
```

### 3-2. storeメソッド（user_idを自動設定）

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'author' => 'required|max:255',
        'rating' => 'required|integer|min:1|max:5',
        'review' => 'nullable|max:10000',
    ]);

    auth()->user()->books()->create($validated);

    return redirect()
        ->route('books.index')
        ->with('success', '書籍を登録しました。');
}
```

### 3-3. show/edit/update/destroyメソッド（所有者チェック）

```php
public function show(Book $book)
{
    $this->authorize('view', $book);
    
    return view('books.show', compact('book'));
}

public function edit(Book $book)
{
    $this->authorize('update', $book);
    
    return view('books.edit', compact('book'));
}

public function update(Request $request, Book $book)
{
    $this->authorize('update', $book);
    
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

public function destroy(Book $book)
{
    $this->authorize('delete', $book);
    
    $book->delete();

    return redirect()
        ->route('books.index')
        ->with('success', '書籍を削除しました。');
}
```

---

## Step 4: Policyの作成

### 4-1. BookPolicyを生成

```bash
sail artisan make:policy BookPolicy --model=Book
```

### 4-2. BookPolicyを編集

**ファイル**: `app/Policies/BookPolicy.php`

```php
<?php

namespace App\Policies;

use App\Models\Book;
use App\Models\User;

class BookPolicy
{
    /**
     * 書籍を閲覧できるか
     */
    public function view(User $user, Book $book): bool
    {
        return $user->id === $book->user_id;
    }

    /**
     * 書籍を更新できるか
     */
    public function update(User $user, Book $book): bool
    {
        return $user->id === $book->user_id;
    }

    /**
     * 書籍を削除できるか
     */
    public function delete(User $user, Book $book): bool
    {
        return $user->id === $book->user_id;
    }
}
```

---

## Step 5: 動作確認

### 5-1. 新しいユーザーで書籍を登録

1. ログアウト
2. 新しいユーザーを登録
3. 書籍を登録

### 5-2. 他のユーザーの書籍にアクセス

1. 別のユーザーでログイン
2. 先ほど登録した書籍のURLに直接アクセス（例: `/books/1`）
3. 403エラー（Forbidden）が表示されることを確認

---

## Step 6: コミット、PR、マージ

### 6-1. コミット

```bash
git add .
git commit -m "feat: ユーザー別レビュー管理の実装 (Closes #8)"
```

### 6-2. プッシュ、PR、マージ

```bash
git push origin feature/issue-8-user-books
```

GitHubでPRを作成し、セルフレビュー後にマージします。

---

## ✨ まとめ

このセクションでは、ユーザーと書籍の関連付けについて学びました。

| Step | 学んだこと |
|:---|:---|
| Step 1 | user_idカラムの追加（マイグレーション） |
| Step 2 | hasMany/belongsToリレーション |
| Step 3 | コントローラーでの所有者チェック |
| Step 4 | Policyによる認可 |
| Step 5-6 | 動作確認、コミット、PR、マージ |

これで、書籍レビューアプリの主要機能が完成しました。

---
