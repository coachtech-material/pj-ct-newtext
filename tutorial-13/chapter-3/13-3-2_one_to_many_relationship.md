# Tutorial 13-3-2: 1対多リレーションシップ

## 🎯 このセクションで学ぶこと

- UserモデルとBookモデルの1対多リレーションシップを実装する
- `hasMany`と`belongsTo`の使い方を復習する
- リレーションを使ったデータ取得を実践する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜリレーションシップを実装するのか？」

認証機能ができたら、次は「誰がどの書籍を登録したか」を管理する必要があります。

```
1人のユーザー → 複数の書籍（1対多）
```

これにより、**ログインユーザーの書籍のみを表示**できるようになります。

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

### 1-3. コードリーディング

| コード | 説明 |
|:---|:---|
| `foreignId('user_id')` | 外部キーカラムを作成 |
| `->after('id')` | idカラムの後に配置 |
| `->constrained()` | usersテーブルのidを参照する外部キー制約 |
| `->onDelete('cascade')` | ユーザー削除時に書籍も削除 |

### 1-4. マイグレーションを実行

```bash
sail artisan migrate
```

---

## Step 2: リレーションの設定

### 2-1. Userモデルにリレーションを追加

**ファイル**: `app/Models/User.php`

```php
use App\Models\Book;

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
use App\Models\User;

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

## Step 3: Tinkerで動作確認

### 3-1. Tinkerを起動

```bash
sail artisan tinker
```

### 3-2. リレーションを使ったデータ取得

```php
use App\Models\User;
use App\Models\Book;

// ユーザーを取得
$user = User::first();

// ユーザーの書籍を取得（hasMany）
$user->books;

// 書籍からユーザーを取得（belongsTo）
$book = Book::first();
$book->user;

// ユーザー経由で書籍を作成
$user->books()->create([
    'title' => 'テスト書籍',
    'author' => 'テスト著者',
    'rating' => 5,
]);
```

---

## Step 4: コントローラーの修正

### 4-1. indexメソッド（自分の書籍のみ表示）

**ファイル**: `app/Http/Controllers/BookController.php`

```php
public function index()
{
    // ログインユーザーの書籍のみ取得
    $books = auth()->user()->books()->latest()->get();
    
    return view('books.index', compact('books'));
}
```

### 4-2. storeメソッド（user_idを自動設定）

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'author' => 'required|max:255',
        'rating' => 'required|integer|min:1|max:5',
        'review' => 'nullable|max:10000',
    ]);

    // ログインユーザーの書籍として作成
    auth()->user()->books()->create($validated);

    return redirect()
        ->route('books.index')
        ->with('success', '書籍を登録しました。');
}
```

---

## 🚨 よくある間違い

### 間違い1: リレーションメソッドを()なしで呼び出す

```php
// ❌ 間違い: コレクションが返る
$user->books->create([...]); // エラー

// ✅ 正解: リレーションビルダーが返る
$user->books()->create([...]); // 成功
```

### 間違い2: fillableにuser_idを追加し忘れる

**エラー例**:
```
Add [user_id] to fillable property to allow mass assignment on [App\Models\Book].
```

---

## ✨ まとめ

このセクションでは、1対多リレーションシップについて学びました。

| Step | 学んだこと |
|:---|:---|
| Step 1 | user_idカラムの追加（マイグレーション） |
| Step 2 | hasMany/belongsToリレーションの設定 |
| Step 3 | Tinkerでの動作確認 |
| Step 4 | コントローラーでのリレーション活用 |

次のセクションでは、ユーザーの書籍のみを表示・編集できるようにする認可機能を実装します。

---
