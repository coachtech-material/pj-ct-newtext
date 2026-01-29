# Tutorial 13-3-4: カテゴリ機能の実装

## 🎯 このセクションで学ぶこと

- カテゴリテーブルを作成し、書籍とのリレーションシップを実装する
- 1対多のリレーションシップをもう一度実践する
- プルダウンメニューでカテゴリを選択できるようにする

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ認可の次にカテゴリ機能なのか？」

基本的なCRUDと認可が整ったら、次は**カテゴリ機能**を追加します。

### 理由1: リレーションの繰り返し練習

```
ユーザー → 書籍（1対多）  ← これをやった
カテゴリ → 書籍（1対多）  ← 同じパターンで繰り返し
```

### 理由2: マスタデータの学習

カテゴリは「マスタデータ」（事前に登録しておくデータ）です。シーダーで登録する方法を学びます。

---

### このセクションの実装順序

| 順番 | 作業 | 理由 |
|:---:|:---|:---|
| 1 | カテゴリテーブル作成 | マスタデータ用テーブル |
| 2 | リレーション設定 | hasMany/belongsToを定義 |
| 3 | シーダーで登録 | マスタデータを投入 |
| 4 | コントローラー修正 | カテゴリ一覧をビューに渡す |
| 5 | ビュー修正 | プルダウンを追加 |
| 6 | Eagerローディング | N+1問題を解決 |

---

## Step 1: カテゴリテーブルの作成

### 1-1. マイグレーションとモデルを作成

```bash
sail artisan make:model Category -m
```

### 1-2. マイグレーションファイルを編集

**ファイル**: `database/migrations/xxxx_xx_xx_xxxxxx_create_categories_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('categories', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('categories');
    }
};
```

### 1-3. booksテーブルにcategory_idを追加

```bash
sail artisan make:migration add_category_id_to_books_table
```

**ファイル**: `database/migrations/xxxx_xx_xx_xxxxxx_add_category_id_to_books_table.php`

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
            $table->foreignId('category_id')->nullable()->after('user_id')->constrained()->onDelete('set null');
        });
    }

    public function down(): void
    {
        Schema::table('books', function (Blueprint $table) {
            $table->dropForeign(['category_id']);
            $table->dropColumn('category_id');
        });
    }
};
```

### 1-4. マイグレーションを実行

```bash
sail artisan migrate
```

---

## Step 2: リレーションの設定

### 2-1. Categoryモデルを編集

**ファイル**: `app/Models/Category.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Category extends Model
{
    use HasFactory;

    protected $fillable = ['name'];

    /**
     * カテゴリに属する書籍
     */
    public function books()
    {
        return $this->hasMany(Book::class);
    }
}
```

### 2-2. Bookモデルにリレーションを追加

**ファイル**: `app/Models/Book.php`

```php
use App\Models\Category;

protected $fillable = [
    'user_id',
    'category_id',
    'title',
    'author',
    'rating',
    'review',
];

/**
 * 書籍が属するカテゴリ
 */
public function category()
{
    return $this->belongsTo(Category::class);
}
```

---

## Step 3: シーダーでカテゴリを登録

### 3-1. CategorySeederを作成

```bash
sail artisan make:seeder CategorySeeder
```

### 3-2. CategorySeederを編集

**ファイル**: `database/seeders/CategorySeeder.php`

```php
<?php

namespace Database\Seeders;

use App\Models\Category;
use Illuminate\Database\Seeder;

class CategorySeeder extends Seeder
{
    public function run(): void
    {
        $categories = [
            'プログラミング',
            'ビジネス',
            '小説',
            '自己啓発',
            'その他',
        ];

        foreach ($categories as $name) {
            Category::create(['name' => $name]);
        }
    }
}
```

### 3-3. DatabaseSeederに登録

**ファイル**: `database/seeders/DatabaseSeeder.php`

```php
public function run(): void
{
    $this->call([
        CategorySeeder::class,
    ]);
}
```

### 3-4. シーダーを実行

```bash
sail artisan db:seed --class=CategorySeeder
```

---

## Step 4: コントローラーの修正

### 4-1. createメソッド

```php
use App\Models\Category;

public function create()
{
    $categories = Category::all();
    
    return view('books.create', compact('categories'));
}
```

### 4-2. storeメソッド

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'author' => 'required|max:255',
        'category_id' => 'nullable|exists:categories,id',
        'rating' => 'required|integer|min:1|max:5',
        'review' => 'nullable|max:10000',
    ]);

    auth()->user()->books()->create($validated);

    return redirect()
        ->route('books.index')
        ->with('success', '書籍を登録しました。');
}
```

### 4-3. editメソッド

```php
public function edit(Book $book)
{
    $this->authorize('update', $book);
    
    $categories = Category::all();
    
    return view('books.edit', compact('book', 'categories'));
}
```

---

## Step 5: ビューの修正

### 5-1. 登録フォームにカテゴリ選択を追加

**ファイル**: `resources/views/books/create.blade.php`

```blade
{{-- カテゴリ --}}
<div class="mb-4">
    <label for="category_id" class="block text-gray-700 font-medium mb-2">カテゴリ</label>
    <select name="category_id" id="category_id"
        class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
        <option value="">選択してください</option>
        @foreach ($categories as $category)
            <option value="{{ $category->id }}" {{ old('category_id') == $category->id ? 'selected' : '' }}>
                {{ $category->name }}
            </option>
        @endforeach
    </select>
    @error('category_id')
        <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
    @enderror
</div>
```

### 5-2. 一覧画面にカテゴリを表示

**ファイル**: `resources/views/books/index.blade.php`

```blade
<p class="text-gray-600">
    {{ $book->author }}
    @if ($book->category)
        <span class="ml-2 px-2 py-1 bg-gray-200 rounded text-sm">{{ $book->category->name }}</span>
    @endif
</p>
```

### 5-3. 詳細画面にカテゴリを表示

**ファイル**: `resources/views/books/show.blade.php`

```blade
@if ($book->category)
    <p class="text-gray-600 mb-4">
        カテゴリ: <span class="px-2 py-1 bg-gray-200 rounded">{{ $book->category->name }}</span>
    </p>
@endif
```

---

## Step 6: Eagerローディング

### 6-1. N+1問題とは

一覧画面で各書籍のカテゴリを表示すると、書籍の数だけSQLが発行されます。

```php
// N+1問題が発生するコード
$books = auth()->user()->books()->latest()->get();

// 1回目: SELECT * FROM books WHERE user_id = 1
// 2回目: SELECT * FROM categories WHERE id = 1
// 3回目: SELECT * FROM categories WHERE id = 2
// ...
```

### 6-2. withでEagerローディング

```php
// Eagerローディングで解決
$books = auth()->user()->books()->with('category')->latest()->get();

// 1回目: SELECT * FROM books WHERE user_id = 1
// 2回目: SELECT * FROM categories WHERE id IN (1, 2, 3, ...)
```

### 6-3. indexメソッドを修正

```php
public function index()
{
    $books = auth()->user()->books()->with('category')->latest()->get();
    
    return view('books.index', compact('books'));
}
```

### コードリーディング

#### `->with('category')`の分解

| 部分 | 説明 |
|:---|:---|
| `with('category')` | categoryリレーションを事前に読み込み |
| 効果 | N+1問題を解決 |

#### メソッドチェーンの流れ

```
auth()->user()  → Userインスタンス
  ->books()     → HasManyビルダー
  ->with()      → Eagerローディングを追加
  ->latest()    → 最新順にソート
  ->get()       → Collectionを取得
```

---

## ✨ まとめ

このセクションでは、カテゴリ機能の実装について学びました。

| Step | 学んだこと |
|:---|:---|
| Step 1 | カテゴリテーブルの作成 |
| Step 2 | hasMany/belongsToリレーション |
| Step 3 | シーダーでマスタデータ登録 |
| Step 4-5 | コントローラー・ビューの修正 |
| Step 6 | Eagerローディングでパフォーマンス改善 |

これで、書籍にカテゴリを設定できるようになりました。

---
