# Tutorial 9-9-1: 認可とポリシーの基礎

## 🎯 このセクションで学ぶこと

*   認証（Authentication）と認可（Authorization）の違いを理解する。
*   Laravelのポリシー（Policy）を使って、リソースへのアクセス権限を管理できるようになる。
*   `can()`メソッドと`@can`ディレクティブを使って、権限チェックを実装できるようになる。

---

## 導入：「誰か」を識別するだけでは不十分

前のチャプターで、Laravel Sanctumを使った**認証（Authentication）**を学びました。認証とは、「このユーザーは誰か」を識別する仕組みです。しかし、実際のWebアプリケーションでは、「誰か」を識別するだけでは不十分です。

例えば、ブログアプリケーションで、以下のような要件があるとします。

*   **投稿の作成**: ログインしているユーザーなら誰でもできる
*   **投稿の編集**: 投稿の作成者だけができる
*   **投稿の削除**: 投稿の作成者、または管理者だけができる
*   **ユーザーの削除**: 管理者だけができる

このように、「誰がアクセスしているか」だけでなく、「そのユーザーが特定のアクションを実行する権限を持っているか」をチェックする必要があります。これが**認可（Authorization）**です。

---

## 詳細解説

### 🔐 認証 vs 認可

| 概念 | 英語 | 意味 | 例 |
|:---|:---|:---|:---|
| 認証 | Authentication | 「誰か」を識別する | ログイン、トークン検証 |
| 認可 | Authorization | 「何ができるか」を判断する | 投稿の編集権限、管理者権限 |

**覚え方**

*   **認証（Authentication）**: 「あなたは誰ですか？」
*   **認可（Authorization）**: 「あなたはこれをしても良いですか？」

---

### 🛡️ Laravelのポリシー（Policy）

Laravelでは、**ポリシー（Policy）**というクラスを使って、リソースへのアクセス権限を管理します。ポリシーは、「特定のモデル（例：`Post`）に対して、特定のアクション（例：`update`, `delete`）を実行する権限があるか」を判断するロジックをまとめたものです。

#### ポリシーの作成

例として、`Post`モデルに対するポリシーを作成してみましょう。

```bash
docker compose exec php php artisan make:policy PostPolicy --model=Post
```

これにより、`app/Policies/PostPolicy.php`が生成されます。

**`app/Policies/PostPolicy.php`**

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    /**
     * ユーザーが投稿を表示できるか
     */
    public function view(User $user, Post $post): bool
    {
        // 公開されている投稿、または自分の投稿なら表示できる
        return $post->is_published || $post->user_id === $user->id;
    }

    /**
     * ユーザーが投稿を更新できるか
     */
    public function update(User $user, Post $post): bool
    {
        // 投稿の作成者だけが更新できる
        return $post->user_id === $user->id;
    }

    /**
     * ユーザーが投稿を削除できるか
     */
    public function delete(User $user, Post $post): bool
    {
        // 投稿の作成者、または管理者だけが削除できる
        return $post->user_id === $user->id || $user->is_admin;
    }
}
```

**コードリーディング**

*   各メソッドは、`User`と`Post`を引数に取り、`bool`（真偽値）を返します。
*   `true`を返すと、そのアクションが許可されます。
*   `false`を返すと、そのアクションが拒否されます。

---

### 🔍 ポリシーの使用

ポリシーを定義したら、コントローラーで`authorize()`メソッドを使って権限チェックを行います。

#### 例：投稿の更新

**`app/Http/Controllers/PostController.php`**

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function update(Request $request, Post $post)
    {
        // ポリシーで権限チェック
        $this->authorize('update', $post);

        // バリデーション
        $validated = $request->validate([
            'title' => 'required|max:255',
            'content' => 'required',
        ]);

        // 投稿を更新
        $post->update($validated);

        return response()->json($post);
    }
}
```

**コードリーディング**

*   `$this->authorize('update', $post)`: `PostPolicy`の`update`メソッドを呼び出し、権限をチェックします。
*   権限がない場合、自動的に`403 Forbidden`エラーが返されます。
*   権限がある場合、次の処理に進みます。

---

### 🎨 Bladeでの権限チェック

Bladeテンプレートでも、`@can`ディレクティブを使って権限チェックができます。

**例：編集ボタンを表示する**

```blade
<h2>{{ $post->title }}</h2>
<p>{{ $post->content }}</p>

@can('update', $post)
    <a href="{{ route('posts.edit', $post) }}">編集</a>
@endcan

@can('delete', $post)
    <form method="POST" action="{{ route('posts.destroy', $post) }}">
        @csrf
        @method('DELETE')
        <button type="submit">削除</button>
    </form>
@endcan
```

**コードリーディング**

*   `@can('update', $post)`: ユーザーが`$post`を更新する権限を持っている場合、編集ボタンを表示します。
*   `@can('delete', $post)`: ユーザーが`$post`を削除する権限を持っている場合、削除ボタンを表示します。

---

### 🔑 ゲートとポリシーの違い

Laravelには、ポリシーの他に、**ゲート（Gate）**という仕組みもあります。

| 概念 | 用途 |
|:---|:---|
| **ポリシー** | 特定のモデル（`Post`, `User`など）に対する権限管理 |
| **ゲート** | モデルに依存しない、汎用的な権限管理（例：「管理画面にアクセスできるか」） |

#### ゲートの定義

ゲートは、`app/Providers/AppServiceProvider.php`の`boot`メソッドで定義します。

```php
use Illuminate\Support\Facades\Gate;

public function boot(): void
{
    Gate::define('access-admin', function (User $user) {
        return $user->is_admin;
    });
}
```

#### ゲートの使用

```php
if (Gate::allows('access-admin')) {
    // 管理画面にアクセスできる
}

if (Gate::denies('access-admin')) {
    // 管理画面にアクセスできない
}
```

**Bladeでの使用**

```blade
@can('access-admin')
    <a href="/admin">管理画面</a>
@endcan
```

---

### 🚀 ポリシーの自動検出

Laravelは、モデル名から自動的にポリシーを検出します。例えば、`Post`モデルに対しては、`PostPolicy`が自動的に適用されます。

もし、カスタムのポリシー名を使いたい場合は、`app/Providers/AuthServiceProvider.php`で明示的に登録します。

```php
protected $policies = [
    Post::class => PostPolicy::class,
];
```

---

## 💡 TIP: `authorize`メソッドの代わりに`Gate`ファサードを使う

`$this->authorize()`の代わりに、`Gate`ファサードを使うこともできます。

```php
use Illuminate\Support\Facades\Gate;

if (Gate::allows('update', $post)) {
    // 更新処理
} else {
    abort(403);
}
```

---

## ✨ まとめ

このセクションでは、Laravelの認可（Authorization）とポリシー（Policy）の基礎を学びました。

*   認証（Authentication）は「誰か」を識別し、認可（Authorization）は「何ができるか」を判断する。
*   ポリシーは、特定のモデルに対するアクセス権限を管理するクラスである。
*   `$this->authorize()`を使って、コントローラーで権限チェックを行える。
*   `@can`ディレクティブを使って、Bladeで権限チェックを行える。
*   ゲートは、モデルに依存しない汎用的な権限管理に使う。

次のセクションでは、デバッグとエラーハンドリングについて学びます。

---
