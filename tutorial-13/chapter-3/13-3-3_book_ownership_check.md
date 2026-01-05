# Tutorial 13-3-3: 所有者チェック（Policy）

## 🎯 このセクションで学ぶこと

- Policyを使った認可機能を実装する
- 他のユーザーの書籍にアクセスできないようにする
- `$this->authorize()`の使い方を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜリレーションの次に認可なのか？」

リレーションができたら、次は**所有者チェック**を実装します。

### 理由1: URL直接入力で他人のデータにアクセスできてしまう

```
❌ 認可なし
→ http://localhost/books/1 で他人の書籍が見れる
→ 他人の書籍を編集・削除できてしまう

✅ 認可あり
→ 自分の書籍のみアクセス可能
→ 他人の書籍にアクセスすると403エラー
```

### 理由2: 認証と認可の違い

| 用語 | 英語 | 意味 |
|:---|:---|:---|
| 認証 | Authentication | 「誰か」を確認する |
| 認可 | Authorization | 「できるか」を確認する |

---

### このセクションの実装順序

| 順番 | 作業 | 理由 |
|:---:|:---|:---|
| 1 | BookPolicy作成 | 認可ルールを定義 |
| 2 | コントローラーで使用 | authorize()でチェック |
| 3 | 動作確認 | 403エラーが出るかテスト |

---

## Step 1: BookPolicyの作成

### 1-1. Policyを生成

```bash
sail artisan make:policy BookPolicy --model=Book
```

### 1-2. BookPolicyを編集

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

### 1-3. コードリーディング

#### `public function view(User $user, Book $book): bool`の分解

| 部分 | 説明 |
|:---|:---|
| `public function view` | 閲覧権限をチェックするメソッド |
| `User $user` | ログインユーザー（自動で注入される） |
| `Book $book` | チェック対象の書籍 |
| `: bool` | 戻り値の型（true/false） |

#### `$user->id === $book->user_id`の分解

| 部分 | 説明 |
|:---|:---|
| `$user->id` | ログインユーザーのID |
| `===` | 厳密な比較（型も一致） |
| `$book->user_id` | 書籍の所有者ID |

> 💡 **ポイント**: `===`は`==`より厳密な比較です。型も一致しないと`false`になります。

---

## Step 2: コントローラーでPolicyを使用

### 2-1. showメソッド

**ファイル**: `app/Http/Controllers/BookController.php`

```php
public function show(Book $book)
{
    $this->authorize('view', $book);
    
    return view('books.show', compact('book'));
}
```

### 2-2. editメソッド

```php
public function edit(Book $book)
{
    $this->authorize('update', $book);
    
    return view('books.edit', compact('book'));
}
```

### 2-3. updateメソッド

```php
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
```

### 2-4. destroyメソッド

```php
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

## Step 3: $this->authorize()の詳細解説

### 3-1. コードの流れ

```php
$this->authorize('view', $book);
```

| ステップ | 処理内容 |
|:---|:---|
| 1 | `$this`（コントローラー）の`authorize`メソッドを呼び出す |
| 2 | `'view'`に対応するPolicyメソッド（`BookPolicy::view`）を探す |
| 3 | `$book`の型（Book）から`BookPolicy`を自動的に特定 |
| 4 | `BookPolicy::view($user, $book)`を実行 |
| 5 | falseが返ったら403エラー、trueなら処理を続行 |

### 3-2. Policyの自動検出

Laravelは以下の規則でPolicyを自動検出します。

| モデル | Policy |
|:---|:---|
| `App\Models\Book` | `App\Policies\BookPolicy` |
| `App\Models\User` | `App\Policies\UserPolicy` |

---

## Step 4: 動作確認

### 4-1. 他のユーザーの書籍にアクセス

1. ユーザーAでログインし、書籍を登録
2. ログアウト
3. ユーザーBで新規登録・ログイン
4. ユーザーAの書籍URL（例: `/books/1`）に直接アクセス
5. **403 Forbidden**が表示されることを確認

### 4-2. 自分の書籍にアクセス

1. ユーザーBで書籍を登録
2. その書籍の詳細・編集・削除が正常に動作することを確認

---

## 🚨 よくある間違い

### 間違い1: authorizeを呼び忘れる

```php
// ❌ 間違い: 認可チェックなし
public function show(Book $book)
{
    return view('books.show', compact('book'));
}

// ✅ 正解: 認可チェックあり
public function show(Book $book)
{
    $this->authorize('view', $book);
    return view('books.show', compact('book'));
}
```

### 間違い2: Policyメソッド名とauthorizeの第1引数が一致しない

```php
// Policy
public function view(User $user, Book $book): bool { ... }

// ❌ 間違い: メソッド名が違う
$this->authorize('show', $book);

// ✅ 正解: Policyのメソッド名と一致
$this->authorize('view', $book);
```

---

## ✨ まとめ

このセクションでは、所有者チェック（Policy）について学びました。

| Step | 学んだこと |
|:---|:---|
| Step 1 | BookPolicyの作成 |
| Step 2 | コントローラーでの`$this->authorize()` |
| Step 3 | Policyの自動検出の仕組み |
| Step 4 | 403エラーの動作確認 |

次のセクションでは、カテゴリ機能を実装します。

---
