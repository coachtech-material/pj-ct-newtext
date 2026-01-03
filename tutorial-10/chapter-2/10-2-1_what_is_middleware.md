# Tutorial 10-2-1: ミドルウェアとは

## 🎯 このセクションで学ぶこと

*   ミドルウェアが何であるか、その役割を理解する。
*   Laravelのリクエストライフサイクルにおけるミドルウェアの位置づけを理解する。
*   カスタムミドルウェアを作成し、特定の処理を挟み込めるようになる。

---

## 導入：リクエストとレスポンスの「間」に処理を挟む

これまでのセクションで、ルーティング、コントローラー、認証など、Laravelの様々な機能を学んできました。しかし、実際のWebアプリケーションでは、「リクエストがコントローラーに到達する前」や「レスポンスがクライアントに返される前」に、共通の処理を実行したいことがあります。

例えば、以下のような処理です。

*   **認証チェック**: ログインしていないユーザーを弾く
*   **権限チェック**: 管理者以外のアクセスを拒否する
*   **ログ記録**: 全てのリクエストをログに記録する
*   **CORS設定**: クロスオリジンリクエストを許可する
*   **メンテナンスモード**: メンテナンス中は全てのリクエストを拒否する

これらの処理を、全てのコントローラーに書くのは非効率です。そこで、Laravelでは、**ミドルウェア（Middleware）**という仕組みを使って、リクエストとレスポンスの「間」に処理を挟み込むことができます。

---

## 詳細解説

### 🔄 ミドルウェアとは？

ミドルウェアとは、**リクエストがコントローラーに到達する前、またはレスポンスがクライアントに返される前に実行される処理**です。ミドルウェアは、リクエストをフィルタリングしたり、レスポンスを加工したりすることができます。

#### リクエストライフサイクルにおけるミドルウェアの位置

```
クライアント
   ↓
【リクエスト】
   ↓
ミドルウェア1（例：CORS設定）
   ↓
ミドルウェア2（例：認証チェック）
   ↓
ミドルウェア3（例：権限チェック）
   ↓
コントローラー（ビジネスロジック）
   ↓
【レスポンス】
   ↓
ミドルウェア3（レスポンス加工）
   ↓
ミドルウェア2（レスポンス加工）
   ↓
ミドルウェア1（レスポンス加工）
   ↓
クライアント
```

ミドルウェアは、**玉ねぎの層**のように、リクエストとレスポンスを包み込みます。これを「ミドルウェアスタック」と呼びます。

---

### 📝 Laravelの標準ミドルウェア

Laravelには、いくつかのミドルウェアが標準で用意されています。

| ミドルウェア | 説明 |
|:---|:---|
| `auth` | 認証されていないユーザーをログインページにリダイレクト |
| `auth:sanctum` | Sanctumトークンで認証されていないユーザーを拒否 |
| `guest` | 認証済みユーザーをホームページにリダイレクト |
| `throttle` | リクエストのレート制限（1分間に60回まで、など） |
| `verified` | メールアドレスが確認されていないユーザーを拒否 |

これらのミドルウェアは、`app/Http/Kernel.php`に登録されています。

---

### 🛠️ カスタムミドルウェアの作成

独自のミドルウェアを作成してみましょう。例として、「管理者以外のアクセスを拒否する」ミドルウェアを作成します。

#### ステップ1: ミドルウェアを生成する

```bash
sail artisan make:middleware AdminMiddleware
```

これにより、`app/Http/Middleware/AdminMiddleware.php`が生成されます。

#### ステップ2: ミドルウェアのロジックを実装する

**`app/Http/Middleware/AdminMiddleware.php`**

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class AdminMiddleware
{
    /**
     * Handle an incoming request.
     */
    public function handle(Request $request, Closure $next)
    {
        // ユーザーが認証されていない、または管理者でない場合
        if (!$request->user() || !$request->user()->is_admin) {
            return response()->json([
                'message' => 'アクセス権限がありません'
            ], 403);
        }

        // 次のミドルウェアまたはコントローラーに処理を渡す
        return $next($request);
    }
}
```

**コードリーディング**

*   `handle(Request $request, Closure $next)`: ミドルウェアのメインメソッドです。
*   `$request`: 現在のHTTPリクエスト
*   `$next`: 次のミドルウェアまたはコントローラーを呼び出すクロージャ
*   `$request->user()`: 現在認証されているユーザーを取得します。
*   `$request->user()->is_admin`: ユーザーが管理者かどうかをチェックします（`users`テーブルに`is_admin`カラムがあると仮定）。
*   `return $next($request)`: 次のミドルウェアまたはコントローラーに処理を渡します。

#### ステップ3: ミドルウェアを登録する

ミドルウェアを使うには、`bootstrap/app.php`に登録する必要があります。

**`bootstrap/app.php`**

```php
<?php

use Illuminate\Foundation\Application;
use Illuminate\Foundation\Configuration\Exceptions;
use Illuminate\Foundation\Configuration\Middleware;

return Application::configure(basePath: dirname(__DIR__))
    ->withRouting(
        web: __DIR__.'/../routes/web.php',
        api: __DIR__.'/../routes/api.php',
        commands: __DIR__.'/../routes/console.php',
        health: '/up',
    )
    ->withMiddleware(function (Middleware $middleware) {
        // ミドルウェアのエイリアスを登録
        $middleware->alias([
            'admin' => \App\Http\Middleware\AdminMiddleware::class,
        ]);
    })
    ->withExceptions(function (Exceptions $exceptions) {
        //
    })->create();
```

これにより、`admin`という名前でミドルウェアを使えるようになります。

#### ステップ4: ルートにミドルウェアを適用する

**`routes/api.php`**

```php
Route::middleware(['auth:sanctum', 'admin'])->group(function () {
    Route::get('/admin/users', [AdminController::class, 'index']);
    Route::delete('/admin/users/{id}', [AdminController::class, 'destroy']);
});
```

これにより、`/admin/users`エンドポイントは、認証されており、かつ管理者であるユーザーだけがアクセスできるようになります。

---

### 🔍 ミドルウェアの実行順序

複数のミドルウェアを適用した場合、以下の順序で実行されます。

```php
Route::middleware(['first', 'second', 'third'])->group(function () {
    Route::get('/example', [ExampleController::class, 'index']);
});
```

**実行順序**

```
リクエスト
   ↓
first（リクエスト処理）
   ↓
second（リクエスト処理）
   ↓
third（リクエスト処理）
   ↓
コントローラー
   ↓
third（レスポンス処理）
   ↓
second（レスポンス処理）
   ↓
first（レスポンス処理）
   ↓
レスポンス
```

---

### 🎯 レスポンスを加工するミドルウェア

ミドルウェアは、レスポンスを加工することもできます。

**例：全てのレスポンスに`X-Custom-Header`ヘッダーを追加する**

```php
public function handle(Request $request, Closure $next)
{
    // 次のミドルウェアまたはコントローラーを実行
    $response = $next($request);

    // レスポンスにカスタムヘッダーを追加
    $response->headers->set('X-Custom-Header', 'MyValue');

    return $response;
}
```

---

## 💡 TIP: グローバルミドルウェア

全てのリクエストに適用したいミドルウェアは、`bootstrap/app.php`の`withMiddleware`メソッドで登録できます。

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->append(\App\Http\Middleware\LogRequests::class);
})
```

---

## ✨ まとめ

このセクションでは、Laravelのミドルウェアの概念と、カスタムミドルウェアの作成方法を学びました。

*   ミドルウェアとは、リクエストがコントローラーに到達する前、またはレスポンスがクライアントに返される前に実行される処理である。
*   ミドルウェアは、認証チェック、権限チェック、ログ記録、CORS設定などに使われる。
*   `php artisan make:middleware`でカスタムミドルウェアを作成できる。
*   `$next($request)`で、次のミドルウェアまたはコントローラーに処理を渡す。
*   ミドルウェアは、`bootstrap/app.php`に登録し、ルートに適用する。

次のセクションでは、認可（Authorization）とポリシー（Policy）について学びます。

---
