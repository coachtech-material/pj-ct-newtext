# Tutorial 13-5-1: リファクタリング基礎

## 🎯 このセクションで学ぶこと

- リファクタリングの目的と重要性を理解する
- バリデーションロジックをFormRequestに切り出す
- コードの重複を減らす方法を学ぶ

---

## リファクタリングとは

**リファクタリング**とは、**外部から見た動作を変えずに、コードの内部構造を改善すること**です。

### なぜリファクタリングが必要か

| 問題 | 影響 |
|:---|:---|
| コードの重複 | 修正漏れ、バグの原因 |
| 長すぎるメソッド | 理解しにくい、テストしにくい |
| 不明確な命名 | 意図が伝わらない |

---

## Step 1: FormRequestの作成

### 1-1. 現在のコントローラーの問題点

`store`と`update`メソッドに同じバリデーションルールが重複しています。

```php
// storeメソッド
$validated = $request->validate([
    'title' => 'required|max:255',
    'author' => 'required|max:255',
    'rating' => 'required|integer|min:1|max:5',
    'review' => 'nullable|max:10000',
]);

// updateメソッド（同じルールが重複）
$validated = $request->validate([
    'title' => 'required|max:255',
    'author' => 'required|max:255',
    'rating' => 'required|integer|min:1|max:5',
    'review' => 'nullable|max:10000',
]);
```

### 1-2. StoreBookRequestを作成

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

### 1-3. コントローラーを修正

**ファイル**: `app/Http/Controllers/BookController.php`

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

---

## Step 2: リファクタリングのメリット

### Before（リファクタリング前）

```php
// コントローラーが肥大化
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'author' => 'required|max:255',
        'rating' => 'required|integer|min:1|max:5',
        'review' => 'nullable|max:10000',
    ]);

    auth()->user()->books()->create($validated);
    // ...
}
```

### After（リファクタリング後）

```php
// コントローラーがスッキリ
public function store(StoreBookRequest $request)
{
    auth()->user()->books()->create($request->validated());
    // ...
}
```

| 項目 | Before | After |
|:---|:---|:---|
| バリデーションルール | コントローラーに直書き | FormRequestに分離 |
| 重複 | store/updateで重複 | 1箇所で管理 |
| テスト | コントローラー全体をテスト | FormRequest単体でテスト可能 |

---

## ✨ まとめ

このセクションでは、リファクタリング基礎について学びました。

- リファクタリングは「動作を変えずに構造を改善」すること
- FormRequestでバリデーションロジックを分離
- コードの重複を減らすことで保守性が向上

---
