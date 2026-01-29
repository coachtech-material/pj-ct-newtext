# Tutorial 13-5-1: コードの整理とDRY原則

## 🎯 このセクションで学ぶこと

- コードの整理方法を学ぶ
- DRY（Don't Repeat Yourself）原則を理解する
- リファクタリングの重要性と実践方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ機能実装の後に『リファクタリング』を行うのか？」

機能が完成したら、次は「リファクタリング」です。なぜこのタイミングなのでしょうか？

### 理由1: 動くコードを先に書く

最初から完璧なコードを書こうとすると、**なかなか進まない**ことがあります。
まずは動くコードを書いて、その後で**きれいにする**のが効率的です。

### 理由2: 問題点が見えてくる

コードを書いていると、「ここ、同じこと書いてるな」「このメソッド長すぎるな」と気づきます。
機能が完成した後なら、**全体を見渡して問題点を把握**できます。

### 理由3: DRY原則から始める理由

DRY（Don't Repeat Yourself）は、**最も基本的なリファクタリング原則**です。
重複コードを見つけて共通化することで、コードの品質が大幅に向上します。

---

## Step 1: DRY原則を理解する

### 1-1. DRY原則とは

**DRY（Don't Repeat Yourself）原則**とは、**同じコードを繰り返し書かない**という原則です。

同じコードを繰り返し書くと、以下のような問題が発生します。

| 問題 | 説明 |
|:---|:---|
| メンテナンスが大変 | 1箇所を修正すると、他の箇所も修正する必要がある |
| バグが発生しやすい | 修正漏れが発生する |
| コードが長くなる | 可読性が低下する |

---

### 1-2. 悪い例（コードの重複）

```php
// 書籍一覧
public function index()
{
    $books = Book::where('user_id', Auth::id())->get();
    return view('books.index', compact('books'));
}

// 書籍詳細
public function show(Book $book)
{
    if ($book->user_id !== Auth::id()) {
        abort(403);
    }
    return view('books.show', compact('book'));
}

// 書籍編集
public function edit(Book $book)
{
    if ($book->user_id !== Auth::id()) {
        abort(403);
    }
    return view('books.edit', compact('book'));
}
```

**問題点**: `$book->user_id !== Auth::id()` のチェックが重複しています。

---

### 1-3. 良い例（Policyで共通化）

```php
// BookPolicy.php
public function view(User $user, Book $book): bool
{
    return $user->id === $book->user_id;
}

// BookController.php
public function show(Book $book)
{
    $this->authorize('view', $book);  // 1行で済む
    return view('books.show', compact('book'));
}
```

---

## Step 2: FormRequestで共通化

### 2-1. バリデーションの重複

```php
// storeメソッド
$validated = $request->validate([
    'title' => 'required|max:255',
    'author' => 'required|max:255',
    'category_id' => 'nullable|exists:categories,id',
    'rating' => 'required|integer|min:1|max:5',
    'review' => 'nullable|max:10000',
]);

// updateメソッド（同じルールが重複）
$validated = $request->validate([
    'title' => 'required|max:255',
    'author' => 'required|max:255',
    'category_id' => 'nullable|exists:categories,id',
    'rating' => 'required|integer|min:1|max:5',
    'review' => 'nullable|max:10000',
]);
```

### 2-2. StoreBookRequestを作成

```bash
sail artisan make:request StoreBookRequest
```

**ファイル**: `app/Http/Requests/StoreBookRequest.php`

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreBookRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'title' => 'required|max:255',
            'author' => 'required|max:255',
            'category_id' => 'nullable|exists:categories,id',
            'rating' => 'required|integer|min:1|max:5',
            'review' => 'nullable|max:10000',
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => 'タイトルは必須です。',
            'author.required' => '著者名は必須です。',
            'rating.required' => '評価は必須です。',
            'rating.min' => '評価は1以上を選択してください。',
            'rating.max' => '評価は5以下を選択してください。',
        ];
    }
}
```

### 2-3. コントローラーを修正

```php
use App\Http\Requests\StoreBookRequest;

public function store(StoreBookRequest $request)
{
    auth()->user()->books()->create($request->validated());

    return redirect()
        ->route('books.index')
        ->with('success', '書籍を登録しました。');
}

public function update(StoreBookRequest $request, Book $book)
{
    $this->authorize('update', $book);
    
    $book->update($request->validated());

    return redirect()
        ->route('books.show', $book)
        ->with('success', '書籍を更新しました。');
}
```

### コードリーディング

#### `StoreBookRequest $request`の分解

| 部分 | 説明 |
|:---|:---|
| `StoreBookRequest` | カスタムFormRequestクラス |
| `$request` | バリデーション済みのリクエスト |

> 💡 **ポイント**: 引数の型を`Request`から`StoreBookRequest`に変えるだけで、自動的にバリデーションが実行されます。

#### `$request->validated()`の分解

| 部分 | 説明 |
|:---|:---|
| `$request` | FormRequestインスタンス |
| `->validated()` | バリデーション済みデータを配列で取得 |

---

## Step 3: Bladeコンポーネントで共通化

### 3-1. フォームの重複

登録画面と編集画面で、同じフォームフィールドが重複しています。

### 3-2. フォームコンポーネントを作成

**ファイル**: `resources/views/components/book-form.blade.php`

```blade
@props(['book' => null, 'categories'])

{{-- タイトル --}}
<div class="mb-4">
    <label for="title" class="block text-gray-700 font-medium mb-2">タイトル</label>
    <input type="text" name="title" id="title" 
        value="{{ old('title', $book?->title) }}"
        class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
    @error('title')
        <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
    @enderror
</div>

{{-- 著者 --}}
<div class="mb-4">
    <label for="author" class="block text-gray-700 font-medium mb-2">著者</label>
    <input type="text" name="author" id="author" 
        value="{{ old('author', $book?->author) }}"
        class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
    @error('author')
        <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
    @enderror
</div>

{{-- カテゴリ --}}
<div class="mb-4">
    <label for="category_id" class="block text-gray-700 font-medium mb-2">カテゴリ</label>
    <select name="category_id" id="category_id"
        class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
        <option value="">選択してください</option>
        @foreach ($categories as $category)
            <option value="{{ $category->id }}" 
                {{ old('category_id', $book?->category_id) == $category->id ? 'selected' : '' }}>
                {{ $category->name }}
            </option>
        @endforeach
    </select>
</div>

{{-- 評価 --}}
<div class="mb-4">
    <label for="rating" class="block text-gray-700 font-medium mb-2">評価</label>
    <select name="rating" id="rating"
        class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
        @for ($i = 5; $i >= 1; $i--)
            <option value="{{ $i }}" {{ old('rating', $book?->rating) == $i ? 'selected' : '' }}>
                {{ str_repeat('★', $i) }}{{ str_repeat('☆', 5 - $i) }} ({{ $i }})
            </option>
        @endfor
    </select>
</div>

{{-- レビュー --}}
<div class="mb-6">
    <label for="review" class="block text-gray-700 font-medium mb-2">レビュー</label>
    <textarea name="review" id="review" rows="5"
        class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">{{ old('review', $book?->review) }}</textarea>
</div>
```

### 3-3. コンポーネントを使用

**登録画面**: `resources/views/books/create.blade.php`

```blade
<form action="{{ route('books.store') }}" method="POST">
    @csrf
    <x-book-form :categories="$categories" />
    <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
        登録
    </button>
</form>
```

**編集画面**: `resources/views/books/edit.blade.php`

```blade
<form action="{{ route('books.update', $book) }}" method="POST">
    @csrf
    @method('PUT')
    <x-book-form :book="$book" :categories="$categories" />
    <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
        更新
    </button>
</form>
```

---

## ✨ まとめ

このセクションでは、コードの整理とDRY原則について学びました。

| 重複の種類 | 解決方法 |
|:---|:---|
| 認可チェックの重複 | Policy |
| バリデーションの重複 | FormRequest |
| ビューの重複 | Bladeコンポーネント |

DRY原則を守ることで、保守性の高いコードを書くことができます。

---
