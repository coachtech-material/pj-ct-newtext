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

**コードリーディング（`::class`の意味）**

| コード | 演算子 | 意味 |
|:---|:---:|:---|
| `Post::class` | `::` | Postクラスの完全修飾名を文字列で取得（例: `"App\Models\Post"`） |
| `PostPolicy::class` | `::` | PostPolicyクラスの完全修飾名を文字列で取得 |

> **💡 Tutorial 7の復習**: `::class`はクラス定数で、クラスの完全修飾名（名前空間付きのクラス名）を文字列として取得します。これはインスタンスを作成せずにクラス名を参照するために使います。

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

**コードリーディング（コントローラー）**：

| コード | 説明 |
|:---|:---|
| `Post::findOrFail($id)` | 指定されたIDの投稿を取得します。存在しない場合は自動で404エラーを返します |
| `$this->authorize('view', $post)` | Policyクラスの `view` メソッドを呼び出し、閲覧権限があるか検証します |
| `$this->authorize('update', $post)` | Policyの `update` メソッドを検証し、許可されない場合は403エラーを返します |
| `$this->authorize('delete', $post)` | Policyの `delete` メソッドを検証し、作成者本人以外の削除をブロックします |
| `$post->update($validated)` | バリデーション済みのデータを使って、データベースのレコードを更新します |
| `$post->delete()` | データベースから対象のレコードを削除します |
| `response()->json(...)` | 処理結果をJSON形式で返します。API開発における標準的なレスポンス方法です |

---

### 💡 TIP: `$this->authorize()`

コントローラー内では、`$this->authorize()`を使うことで、ポリシーのメソッドを簡単に呼び出せます。

**コードリーディング**

| コード | 演算子 | 意味 |
|:---|:---:|:---|
| `$this->authorize('update', $post)` | `->` | コントローラーインスタンス（`$this`）の`authorize`メソッドを呼び出し |

> **💡 ポイント**: `$this`は現在のコントローラーインスタンスを指します。Tutorial 7で学んだように、`$this`はクラス内で自分自身を参照するために使います。

---


### 🚀 実践例2: `before`メソッド

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

**コードリーディング（ポリシーの実装）**：

| コード | 説明 |
|:---|:---|
| `public function before(...)` | ポリシー内の他のどのチェックよりも先に実行される「特権的なメソッド」です |
| `User $user` | 現在ログインしているユーザー情報が自動的に渡されます |
| `$ability` | 実行されようとしているアクション名（'update' や 'delete' など）が渡されます |
| `$user->is_admin` | ユーザーが管理者かどうかを判定するフラグ（カラム）をチェックします |
| `return true;` | ここで `true` を返すと、以降の個別メソッドの判定をスキップして即座に認可されます |

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
