# Tutorial 10-3-3: ポリシーの作成

## 🎯 このセクションで学ぶこと

*   ポリシーを作成し、モデルに対する認可ロジックを定義できるようになる。
*   ポリシーとゲートの違いを理解する。
*   ポリシーのメソッドを実装できるようになる。

---

## 導入：「ポリシー」とは何か？

前のセクションで、ゲートを使って、シンプルな認可ロジックを実装しました。しかし、**特定のモデルに対する認可ロジック**が複雑になると、ゲートでは管理が難しくなります。

Laravelでは、**ポリシー（Policy）**を使って、モデルに対する認可ロジックを整理できます。

**ポリシーとは？**

ポリシーとは、**特定のモデルに対する認可ロジックをまとめたクラス**です。例えば、`Post`モデルに対するポリシーを作成すると、以下のような認可ロジックを定義できます。

*   投稿を表示できるか（`view`）
*   投稿を作成できるか（`create`）
*   投稿を更新できるか（`update`）
*   投稿を削除できるか（`delete`）

このセクションでは、ポリシーの作成方法を学びます。

---

## 詳細解説

### 🔧 ステップ1: ポリシーを生成

```bash
sail artisan make:policy PostPolicy --model=Post
```

**`app/Policies/PostPolicy.php`**

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    public function view(User $user, Post $post)
    {
        // 投稿を表示できるか
    }

    public function create(User $user)
    {
        // 投稿を作成できるか
    }

    public function update(User $user, Post $post)
    {
        // 投稿を更新できるか
    }

    public function delete(User $user, Post $post)
    {
        // 投稿を削除できるか
    }
}
```

---

### 🔧 ステップ2: ポリシーを実装

```php
public function view(User $user, Post $post)
{
    // 公開済みの投稿は誰でも閲覧可能
    if ($post->is_published) {
        return true;
    }

    // 下書きは自分のみ閲覧可能
    return $user->id === $post->user_id;
}

public function create(User $user)
{
    // 認証済みユーザーは投稿を作成できる
    return true;
}

public function update(User $user, Post $post)
{
    // 自分の投稿のみ更新できる
    return $user->id === $post->user_id;
}

public function delete(User $user, Post $post)
{
    // 自分の投稿のみ削除できる
    return $user->id === $post->user_id;
}
```

---

### 🔧 ステップ3: ポリシーを登録

**`app/Providers/AuthServiceProvider.php`**

```php
<?php

namespace App\Providers;

use App\Models\Post;
use App\Policies\PostPolicy;
use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;

class AuthServiceProvider extends ServiceProvider
{
    protected $policies = [
        Post::class => PostPolicy::class,
    ];

    public function boot()
    {
        $this->registerPolicies();
    }
}
```

---

### 🚀 実践例1: ポリシーを使った認可チェック

#### コントローラー

```php
public function show($id)
{
    $post = Post::findOrFail($id);

    $this->authorize('view', $post);

    return response()->json(['post' => $post]);
}

public function update(Request $request, $id)
{
    $post = Post::findOrFail($id);

    $this->authorize('update', $post);

    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'content' => 'required|string',
    ]);

    $post->update($validated);

    return response()->json(['message' => 'Post updated successfully', 'post' => $post]);
}

public function destroy($id)
{
    $post = Post::findOrFail($id);

    $this->authorize('delete', $post);

    $post->delete();

    return response()->json(['message' => 'Post deleted successfully']);
}
```

---

### 💡 TIP: `$this->authorize()`

コントローラー内では、`$this->authorize()`を使うことで、ポリシーのメソッドを簡単に呼び出せます。

---

### 🚀 実践例2: 管理者は全ての投稿を削除できる

#### ポリシーの実装

```php
public function delete(User $user, Post $post)
{
    // 管理者は全ての投稿を削除できる
    if ($user->is_admin) {
        return true;
    }

    // 自分の投稿のみ削除できる
    return $user->id === $post->user_id;
}
```

---

### 🚀 実践例3: `before`メソッド

#### ポリシーの実装

```php
public function before(User $user, $ability)
{
    // 管理者は全てのアクションを許可
    if ($user->is_admin) {
        return true;
    }
}
```

**コードリーディング**

*   `before`メソッドは、全てのポリシーメソッドの前に実行される
*   `true`を返すと、他のポリシーメソッドはスキップされる

---

### 🚀 実践例4: ゲストユーザーを許可

#### ポリシーの実装

```php
public function view(?User $user, Post $post)
{
    // 公開済みの投稿は誰でも閲覧可能
    if ($post->is_published) {
        return true;
    }

    // 下書きは自分のみ閲覧可能
    return $user && $user->id === $post->user_id;
}
```

---

### 💡 TIP: `viewAny`メソッド

```php
public function viewAny(User $user)
{
    // 認証済みユーザーは投稿一覧を閲覧できる
    return true;
}
```

---

### 🚀 実践例5: コメントのポリシー

#### ステップ1: ポリシーを生成

```bash
sail artisan make:policy CommentPolicy --model=Comment
```

#### ステップ2: ポリシーを実装

```php
<?php

namespace App\Policies;

use App\Models\Comment;
use App\Models\User;

class CommentPolicy
{
    public function update(User $user, Comment $comment)
    {
        // 自分のコメントのみ更新できる
        return $user->id === $comment->user_id;
    }

    public function delete(User $user, Comment $comment)
    {
        // 自分のコメント、または投稿の所有者は削除できる
        return $user->id === $comment->user_id || $user->id === $comment->post->user_id;
    }
}
```

#### ステップ3: ポリシーを登録

```php
protected $policies = [
    Post::class => PostPolicy::class,
    Comment::class => CommentPolicy::class,
];
```

---

### 🔍 ポリシーとゲートの違い

| 項目 | ゲート | ポリシー |
|------|--------|----------|
| 用途 | シンプルな認可ロジック | モデルに対する認可ロジック |
| 定義場所 | `AuthServiceProvider` | 専用のポリシークラス |
| 管理 | 全てのゲートが1箇所に集まる | モデルごとにファイルが分かれる |
| 推奨 | グローバルな権限チェック | CRUD操作の権限チェック |

---

### 🚨 よくある間違い

#### 間違い1: ポリシーを登録し忘れる

```php
// AuthServiceProviderに登録していない
$this->authorize('update', $post); // エラーになる
```

**対処法**: `AuthServiceProvider`に登録します。

---

#### 間違い2: メソッド名を間違える

```php
// ポリシーのメソッド名は'update'
public function update(User $user, Post $post)
{
    return $user->id === $post->user_id;
}

// 間違ったメソッド名
$this->authorize('edit', $post); // NG: 'edit'ではなく'update'
```

---

## ✨ まとめ

このセクションでは、ポリシーの作成方法を学びました。

*   `php artisan make:policy`を使って、ポリシーを生成できる。
*   ポリシーのメソッドを実装して、認可ロジックを定義できる。
*   `AuthServiceProvider`にポリシーを登録する必要がある。
*   `$this->authorize()`を使って、ポリシーのメソッドを簡単に呼び出せる。

次のセクションでは、ポリシーの適用方法を学びます。

---
