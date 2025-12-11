# Tutorial 9-9-2: ゲートの基礎

## 🎯 このセクションで学ぶこと

*   Gateを使って、シンプルな認可ロジックを実装できるようになる。
*   `Gate::define()`を使って、認可ルールを定義できるようになる。
*   `Gate::allows()`や`Gate::denies()`を使って、認可チェックを実行できるようになる。

---

## 導入：「ゲート」とは何か？

前のセクションで、認可とポリシーの基礎について学びました。Laravelでは、**ゲート（Gate）**を使って、シンプルな認可ロジックを実装できます。

**ゲートとは？**

ゲートとは、**特定のアクションを実行する権限があるかをチェックする仕組み**です。例えば、以下のような認可ロジックを実装できます。

*   管理者のみが投稿を削除できる
*   自分の投稿のみを編集できる
*   特定のロールを持つユーザーのみがアクセスできる

このセクションでは、Gateを使って、シンプルな認可ロジックを実装します。

---

## 詳細解説

### 🔧 ゲートの定義

ゲートは、`AuthServiceProvider`で定義します。

**`app/Providers/AuthServiceProvider.php`**

```php
<?php

namespace App\Providers;

use Illuminate\Foundation\Support\Providers\AuthServiceProvider as ServiceProvider;
use Illuminate\Support\Facades\Gate;

class AuthServiceProvider extends ServiceProvider
{
    public function boot()
    {
        $this->registerPolicies();

        Gate::define('delete-post', function ($user, $post) {
            return $user->id === $post->user_id;
        });
    }
}
```

**コードリーディング**

*   `Gate::define('delete-post', ...)`: `delete-post`という名前のゲートを定義
*   クロージャの第1引数: 認証済みユーザー
*   クロージャの第2引数: チェック対象のモデル（オプション）
*   戻り値: `true`（許可）または`false`（拒否）

---

### 🔍 ゲートのチェック

#### `Gate::allows()`

```php
use Illuminate\Support\Facades\Gate;

if (Gate::allows('delete-post', $post)) {
    // 削除を許可
    $post->delete();
} else {
    // 削除を拒否
    abort(403);
}
```

---

#### `Gate::denies()`

```php
if (Gate::denies('delete-post', $post)) {
    abort(403);
}

$post->delete();
```

---

#### `Gate::authorize()`

```php
Gate::authorize('delete-post', $post);

// 許可されない場合、自動的に403エラーが返される
$post->delete();
```

---

### 🚀 実践例1: 管理者のみが投稿を削除できる

#### ゲートの定義

```php
Gate::define('delete-post', function ($user) {
    return $user->is_admin;
});
```

#### コントローラー

```php
public function destroy($id)
{
    $post = Post::findOrFail($id);

    if (Gate::denies('delete-post')) {
        return response()->json(['message' => 'Unauthorized'], 403);
    }

    $post->delete();

    return response()->json(['message' => 'Post deleted successfully']);
}
```

---

### 🚀 実践例2: 自分の投稿のみを編集できる

#### ゲートの定義

```php
Gate::define('update-post', function ($user, $post) {
    return $user->id === $post->user_id;
});
```

#### コントローラー

```php
public function update(Request $request, $id)
{
    $post = Post::findOrFail($id);

    Gate::authorize('update-post', $post);

    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'content' => 'required|string',
    ]);

    $post->update($validated);

    return response()->json(['message' => 'Post updated successfully', 'post' => $post]);
}
```

---

### 💡 TIP: `$user`ヘルパー

コントローラー内では、`$request->user()`の代わりに、ゲート内で自動的に認証済みユーザーが渡されます。

---

### 🚀 実践例3: 複数の条件をチェック

#### ゲートの定義

```php
Gate::define('publish-post', function ($user, $post) {
    return $user->id === $post->user_id && $user->is_verified;
});
```

---

### 🚀 実践例4: ゲストユーザーを許可

デフォルトでは、ゲストユーザー（未ログイン）は全てのゲートで拒否されます。ゲストユーザーを許可する場合は、`?User`を使います。

#### ゲートの定義

```php
use App\Models\User;

Gate::define('view-post', function (?User $user, $post) {
    if ($post->is_published) {
        return true; // 公開済みの投稿は誰でも閲覧可能
    }

    return $user && $user->id === $post->user_id; // 下書きは自分のみ閲覧可能
});
```

---

### 🔍 `before`と`after`フック

#### `before`: 全てのゲートの前に実行

```php
Gate::before(function ($user, $ability) {
    if ($user->is_admin) {
        return true; // 管理者は全てのアクションを許可
    }
});
```

---

#### `after`: 全てのゲートの後に実行

```php
Gate::after(function ($user, $ability, $result) {
    if ($user->is_super_admin) {
        return true; // スーパー管理者は全てのアクションを許可
    }
});
```

---

### 🚀 実践例5: ロールベースの認可

#### ゲートの定義

```php
Gate::define('manage-users', function ($user) {
    return in_array($user->role, ['admin', 'moderator']);
});

Gate::define('delete-users', function ($user) {
    return $user->role === 'admin';
});
```

#### コントローラー

```php
public function index()
{
    Gate::authorize('manage-users');

    $users = User::all();

    return response()->json(['users' => $users]);
}

public function destroy($id)
{
    Gate::authorize('delete-users');

    $user = User::findOrFail($id);
    $user->delete();

    return response()->json(['message' => 'User deleted successfully']);
}
```

---

### 💡 TIP: Bladeでゲートを使う

```blade
@can('delete-post', $post)
    <button>削除</button>
@endcan

@cannot('delete-post', $post)
    <p>削除する権限がありません</p>
@endcannot
```

---

### 🚀 実践例6: パラメータなしのゲート

#### ゲートの定義

```php
Gate::define('access-admin-panel', function ($user) {
    return $user->is_admin;
});
```

#### コントローラー

```php
public function index()
{
    if (Gate::denies('access-admin-panel')) {
        return response()->json(['message' => 'Unauthorized'], 403);
    }

    // 管理画面の処理
}
```

---

### 🚨 よくある間違い

#### 間違い1: ゲートの名前を間違える

```php
Gate::define('delete-post', function ($user, $post) {
    return $user->id === $post->user_id;
});

// 間違った名前
if (Gate::allows('delete-posts', $post)) { // NG: 's'が余分
    // ...
}
```

**対処法**: ゲートの名前を正確に指定します。

---

#### 間違い2: `Gate::allows()`と`Gate::authorize()`を混同

```php
// Gate::allows()は、booleanを返す
if (Gate::allows('delete-post', $post)) {
    $post->delete();
}

// Gate::authorize()は、許可されない場合に例外を投げる
Gate::authorize('delete-post', $post);
$post->delete();
```

---

## ✨ まとめ

このセクションでは、Gateを使って、シンプルな認可ロジックを実装しました。

*   `Gate::define()`を使って、認可ルールを定義できる。
*   `Gate::allows()`や`Gate::denies()`を使って、認可チェックを実行できる。
*   `Gate::authorize()`を使って、許可されない場合に自動的に403エラーを返せる。
*   `before`や`after`フックを使って、全てのゲートの前後に処理を実行できる。

次のセクションでは、ポリシーの作成方法を学びます。

---

## 📝 学習のポイント

- [ ] `Gate::define()`を使って、認可ルールを定義できる。
- [ ] `Gate::allows()`や`Gate::denies()`を使って、認可チェックを実行できる。
- [ ] `Gate::authorize()`を使って、許可されない場合に自動的に403エラーを返せる。
- [ ] `before`や`after`フックを使える。
