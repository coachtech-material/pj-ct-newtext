# Tutorial 10-2-2: カスタムミドルウェアの作成

## 🎯 このセクションで学ぶこと

*   独自のミドルウェアを作成できるようになる。
*   グローバルミドルウェア、ミドルウェアグループ、ルートミドルウェアの実装方法を理解する。
*   パラメータを受け取るミドルウェアを作成できるようになる。

---

## 導入：「独自の門番」を作る

前のセクションで、ミドルウェアの概念と3つの種類（グローバル、グループ、ルート）について学びました。このセクションでは、**カスタムミドルウェアの作成方法**と、それぞれの種類の**具体的な実装方法**を学びます。

---

## 詳細解説

### 🤔 いつカスタムミドルウェアを作るべきか？

Laravelには多くの標準ミドルウェアが用意されていますが、以下のような場合はカスタムミドルウェアを作成します。

| ケース | 例 |
|:---|:---|
| アプリケーション固有のチェックが必要 | 年齢確認、メンテナンスモード、特定の国からのアクセス制限 |
| 複数のルートで同じ処理を共有したい | リクエストのログ記録、レスポンスへのヘッダー追加 |
| 標準ミドルウェアをカスタマイズしたい | 認証失敗時のリダイレクト先を変更 |

---

### 🔧 カスタムミドルウェアの基本的な作成手順

**ステップ1: ミドルウェアを生成**

```bash
sail artisan make:middleware CheckAge
```

このコマンドで、`app/Http/Middleware/CheckAge.php`が生成されます。

**ステップ2: ミドルウェアを実装**

**`app/Http/Middleware/CheckAge.php`**

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class CheckAge
{
    public function handle(Request $request, Closure $next)
    {
        if ($request->age < 18) {
            return redirect('/')->with('error', '18歳以上の方のみアクセスできます。');
        }

        return $next($request);
    }
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `namespace App\Http\Middleware;` | このクラスが属する名前空間を宣言します |
| `use Closure;` | クロージャ（無名関数）を使用するための宣言です |
| `use Illuminate\Http\Request;` | Requestクラスを使用するための宣言です |
| `public function handle(...)` | ミドルウェアのメイン処理を定義するメソッドです |
| `Request $request` | 現在のHTTPリクエストを受け取ります |
| `Closure $next` | 次のミドルウェアまたはコントローラーを呼び出すクロージャです |
| `$request->age` | リクエストパラメータの`age`にアクセスします |
| `return redirect('/')->with(...)` | 条件を満たさない場合、リダイレクトします |
| `return $next($request);` | 条件を満たす場合、次の処理に進みます |

**ステップ3: ミドルウェアを登録**

**`app/Http/Kernel.php`**

```php
protected $middlewareAliases = [
    'auth' => \App\Http\Middleware\Authenticate::class,
    'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
    'check.age' => \App\Http\Middleware\CheckAge::class, // 追加
];
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `protected $middlewareAliases` | ルートミドルウェアのエイリアス（別名）を定義する配列です |
| `'check.age' => ...` | `check.age`という名前でミドルウェアを登録します |
| `\App\Http\Middleware\CheckAge::class` | ミドルウェアクラスの完全修飾名を指定します |

**ステップ4: ミドルウェアを適用**

```php
Route::middleware('check.age')->group(function () {
    Route::get('/adult-content', [ContentController::class, 'show']);
});
```

---

### 🌐 グローバルミドルウェアの実装

**全てのリクエスト**に対して実行されるミドルウェアです。

**🚀 実践例: リクエストログミドルウェア**

全てのリクエストをログに記録するミドルウェアを作成します。

**ステップ1: ミドルウェアを生成**

```bash
sail artisan make:middleware LogRequests
```

**ステップ2: ミドルウェアを実装**

**`app/Http/Middleware/LogRequests.php`**

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class LogRequests
{
    public function handle(Request $request, Closure $next)
    {
        // リクエスト情報をログに記録
        Log::info('Request received', [
            'method' => $request->method(),
            'url' => $request->fullUrl(),
            'ip' => $request->ip(),
            'user_agent' => $request->userAgent(),
        ]);

        return $next($request);
    }
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `use Illuminate\Support\Facades\Log;` | ログ機能を使用するための宣言です |
| `Log::info('Request received', [...])` | infoレベルでログを記録します |
| `$request->method()` | HTTPメソッド（GET、POSTなど）を取得します |
| `$request->fullUrl()` | クエリパラメータを含む完全なURLを取得します |
| `$request->ip()` | クライアントのIPアドレスを取得します |
| `$request->userAgent()` | ブラウザのUser-Agent情報を取得します |

**ステップ3: グローバルミドルウェアとして登録**

**`app/Http/Kernel.php`**

```php
protected $middleware = [
    // 既存のミドルウェア...
    \App\Http\Middleware\LogRequests::class, // 追加
];
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `protected $middleware` | グローバルミドルウェアを定義する配列です |
| `\App\Http\Middleware\LogRequests::class` | 全てのリクエストで実行されるミドルウェアを追加します |

> **💡 ポイント**: グローバルミドルウェアは`$middleware`配列に追加するだけで、全てのリクエストに自動的に適用されます。ルート定義で指定する必要はありません。

---

### 📦 ミドルウェアグループの実装

**複数のミドルウェアをまとめて**適用する方法です。

**🚀 実践例: APIグループにミドルウェアを追加**

APIルート用のミドルウェアグループにカスタムミドルウェアを追加します。

**`app/Http/Kernel.php`**

```php
protected $middlewareGroups = [
    'web' => [
        \App\Http\Middleware\EncryptCookies::class,
        \Illuminate\Cookie\Middleware\AddQueuedCookiesToResponse::class,
        \Illuminate\Session\Middleware\StartSession::class,
        \Illuminate\View\Middleware\ShareErrorsFromSession::class,
        \App\Http\Middleware\VerifyCsrfToken::class,
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],

    'api' => [
        \Illuminate\Routing\Middleware\ThrottleRequests::class.':api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        \App\Http\Middleware\LogRequests::class, // 追加
    ],
];
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `protected $middlewareGroups` | ミドルウェアグループを定義する配列です |
| `'web' => [...]` | Webルート用のミドルウェアグループです |
| `'api' => [...]` | APIルート用のミドルウェアグループです |
| `ThrottleRequests::class.':api'` | レート制限ミドルウェアにパラメータを渡しています |

> **💡 ポイント**: `routes/web.php`のルートには自動的に`web`グループが、`routes/api.php`のルートには自動的に`api`グループが適用されます。

---

### 🎯 ルートミドルウェアの実装

**特定のルートにのみ**適用するミドルウェアです。

**🚀 実践例1: 管理者チェックミドルウェア**

管理者以外のアクセスを拒否するミドルウェアを作成します。

**ステップ1: ミドルウェアを生成**

```bash
sail artisan make:middleware AdminMiddleware
```

**ステップ2: ミドルウェアを実装**

**`app/Http/Middleware/AdminMiddleware.php`**

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class AdminMiddleware
{
    public function handle(Request $request, Closure $next)
    {
        if (!$request->user() || !$request->user()->is_admin) {
            return redirect('/')->with('error', '管理者権限が必要です。');
        }

        return $next($request);
    }
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$request->user()` | 現在認証されているユーザーを取得します。未認証の場合は`null`を返します |
| `!$request->user()` | ユーザーが認証されていない場合に`true`になります |
| `$request->user()->is_admin` | ユーザーの`is_admin`プロパティにアクセスします |
| `redirect('/')->with('error', ...)` | エラーメッセージをセッションに保存してリダイレクトします |

**ステップ3: ルートミドルウェアとして登録**

**`app/Http/Kernel.php`**

```php
protected $middlewareAliases = [
    'auth' => \App\Http\Middleware\Authenticate::class,
    'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
    'admin' => \App\Http\Middleware\AdminMiddleware::class, // 追加
];
```

**ステップ4: ルートに適用**

```php
Route::middleware(['auth', 'admin'])->group(function () {
    Route::get('/admin/dashboard', [AdminController::class, 'index']);
    Route::get('/admin/users', [AdminController::class, 'users']);
});
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `Route::middleware(['auth', 'admin'])` | `auth`と`admin`の2つのミドルウェアを適用します |
| `->group(function () { ... })` | グループ内の全ルートにミドルウェアが適用されます |

---

### 🔧 パラメータを受け取るミドルウェア

ミドルウェアは、パラメータを受け取ることができます。

**🚀 実践例2: ロールチェックミドルウェア**

指定されたロール（役割）を持つユーザーのみアクセスを許可するミドルウェアを作成します。

**ステップ1: ミドルウェアを生成**

```bash
sail artisan make:middleware CheckRole
```

**ステップ2: ミドルウェアを実装**

**`app/Http/Middleware/CheckRole.php`**

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class CheckRole
{
    public function handle(Request $request, Closure $next, $role)
    {
        if (!$request->user() || $request->user()->role !== $role) {
            return redirect('/')->with('error', 'アクセス権限がありません。');
        }

        return $next($request);
    }
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `public function handle(..., $role)` | 第3引数でパラメータを受け取ります |
| `$request->user()->role !== $role` | ユーザーのロールと指定されたロールを比較します |

**ステップ3: ルートミドルウェアとして登録**

**`app/Http/Kernel.php`**

```php
protected $middlewareAliases = [
    'role' => \App\Http\Middleware\CheckRole::class,
];
```

**ステップ4: ルートに適用（パラメータ付き）**

```php
// 管理者のみアクセス可能
Route::middleware('role:admin')->group(function () {
    Route::get('/admin/dashboard', [AdminController::class, 'index']);
});

// 編集者のみアクセス可能
Route::middleware('role:editor')->group(function () {
    Route::get('/editor/posts', [EditorController::class, 'posts']);
});
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `'role:admin'` | `role`ミドルウェアに`admin`というパラメータを渡します |
| `:` | ミドルウェア名とパラメータの区切り文字です |

---

### 🔧 複数のパラメータを受け取るミドルウェア

カンマ区切りで複数のパラメータを渡すことができます。

**ミドルウェアの実装**

```php
public function handle(Request $request, Closure $next, $role, $permission)
{
    if (!$request->user() || 
        $request->user()->role !== $role || 
        !$request->user()->hasPermission($permission)) {
        return redirect('/')->with('error', 'アクセス権限がありません。');
    }

    return $next($request);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$role, $permission` | 2つのパラメータを受け取ります |
| `hasPermission($permission)` | Userモデルで定義した権限チェックメソッドを呼び出します |

**ルートに適用**

```php
Route::middleware('role:admin,manage_users')->group(function () {
    Route::get('/admin/users', [AdminController::class, 'users']);
});
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `'role:admin,manage_users'` | `admin`と`manage_users`の2つのパラメータを渡します |
| `,` | パラメータ同士の区切り文字です |

---

### 🚨 よくある間違い

**間違い1: ミドルウェアを登録し忘れる**

```php
// Kernel.phpに登録していない
Route::middleware('check.age')->group(function () {
    // エラーになる
});
```

**対処法**: `app/Http/Kernel.php`の`$middlewareAliases`に登録します。

---

**間違い2: パラメータの順序を間違える**

```php
public function handle(Request $request, Closure $next, $role, $permission)
{
    // $roleが最初、$permissionが2番目
}

// パラメータの順序が逆
Route::middleware('role:manage_users,admin')->group(function () {
    // manage_usersが$roleに、adminが$permissionに入ってしまう
});
```

**対処法**: パラメータの順序を確認します。

```php
Route::middleware('role:admin,manage_users')->group(function () {
    // OK: adminが$roleに、manage_usersが$permissionに入る
});
```

---

## ✨ まとめ

このセクションでは、カスタムミドルウェアの作成方法と3種類のミドルウェアの実装方法を学びました。

*   `sail artisan make:middleware`でミドルウェアを生成できる。
*   `handle()`メソッドでミドルウェアの処理を定義する。
*   グローバルミドルウェアは`$middleware`配列に登録し、全リクエストに適用される。
*   ミドルウェアグループは`$middlewareGroups`配列で定義し、複数のミドルウェアをまとめて適用できる。
*   ルートミドルウェアは`$middlewareAliases`配列に登録し、特定のルートに適用できる。
*   パラメータを受け取るミドルウェアは、`role:admin`のように`:`で区切って指定する。

次のセクションでは、HTTPライフサイクルの詳細について学びます。

---
