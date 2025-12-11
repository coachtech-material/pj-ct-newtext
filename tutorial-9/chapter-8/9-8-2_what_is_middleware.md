# Tutorial 9-8-2: ミドルウェアとは

## 🎯 このセクションで学ぶこと

*   ミドルウェアの役割を理解する。
*   リクエストの前後処理を実装できるようになる。
*   Laravelの標準ミドルウェアを理解する。

---

## 導入：「門番」としてのミドルウェア

前のセクションで、HTTPライフサイクルについて学びました。その中で、**ミドルウェア**という概念が登場しました。

ミドルウェアとは、**リクエストとレスポンスの間に入る処理**です。例えば、以下のような処理を実装できます。

*   **認証チェック**: ログインしているかを確認
*   **ログ記録**: リクエストの内容を記録
*   **CORS設定**: クロスオリジンリクエストを許可
*   **メンテナンスモード**: メンテナンス中はアクセスを拒否

このセクションでは、ミドルウェアの役割と、Laravelの標準ミドルウェアについて学びます。

---

## 詳細解説

### 🔍 ミドルウェアとは？

ミドルウェアとは、**リクエストがコントローラーに到達する前**、または**レスポンスがブラウザに返される前**に実行される処理です。

**イメージ**

```
リクエスト → ミドルウェア1 → ミドルウェア2 → コントローラー → レスポンス
```

---

### 🚪 ミドルウェアの役割

#### 1. 認証チェック

```php
// ログインしていない場合、ログインページにリダイレクト
if (!auth()->check()) {
    return redirect('/login');
}
```

#### 2. 認可チェック

```php
// 管理者でない場合、403エラーを返す
if (!auth()->user()->is_admin) {
    abort(403);
}
```

#### 3. ログ記録

```php
// リクエストの内容をログに記録
Log::info('Request received', [
    'url' => $request->url(),
    'method' => $request->method(),
]);
```

#### 4. CORS設定

```php
// クロスオリジンリクエストを許可
return $response->header('Access-Control-Allow-Origin', '*');
```

---

### 📝 Laravelの標準ミドルウェア

Laravelには、多くの標準ミドルウェアが用意されています。

#### `auth`: 認証チェック

```php
Route::middleware('auth')->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
});
```

#### `guest`: 未認証チェック

```php
Route::middleware('guest')->group(function () {
    Route::get('/login', [AuthController::class, 'showLoginForm']);
});
```

#### `throttle`: レート制限

```php
Route::middleware('throttle:60,1')->group(function () {
    Route::get('/api/posts', [PostController::class, 'index']);
});
```

*   `60`: 1分間に60回まで
*   `1`: 1分間

---

### 🔍 ミドルウェアの種類

#### 1. グローバルミドルウェア

**全てのリクエスト**に適用されるミドルウェアです。

**`app/Http/Kernel.php`**

```php
protected $middleware = [
    \App\Http\Middleware\TrustProxies::class,
    \Illuminate\Http\Middleware\HandleCors::class,
    \App\Http\Middleware\PreventRequestsDuringMaintenance::class,
    \Illuminate\Foundation\Http\Middleware\ValidatePostSize::class,
    \App\Http\Middleware\TrimStrings::class,
    \Illuminate\Foundation\Http\Middleware\ConvertEmptyStringsToNull::class,
];
```

---

#### 2. ルートミドルウェア

**特定のルート**に適用されるミドルウェアです。

**`app/Http/Kernel.php`**

```php
protected $middlewareAliases = [
    'auth' => \App\Http\Middleware\Authenticate::class,
    'auth.basic' => \Illuminate\Auth\Middleware\AuthenticateWithBasicAuth::class,
    'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
    'throttle' => \Illuminate\Routing\Middleware\ThrottleRequests::class,
];
```

---

### 🚀 実践例1: 認証ミドルウェア

#### ルート

```php
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/profile', [ProfileController::class, 'show']);
    Route::put('/profile', [ProfileController::class, 'update']);
});
```

#### 動作

*   ログインしている場合: コントローラーが実行される
*   ログインしていない場合: 401エラーが返される

---

### 🚀 実践例2: レート制限ミドルウェア

#### ルート

```php
Route::middleware('throttle:10,1')->group(function () {
    Route::post('/api/posts', [PostController::class, 'store']);
});
```

#### 動作

*   1分間に10回まで: 正常にリクエストが処理される
*   1分間に11回目: 429エラー（Too Many Requests）が返される

---

### 🔍 ミドルウェアの実装

ミドルウェアは、`handle()`メソッドを実装します。

**`app/Http/Middleware/Authenticate.php`**

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Auth\Middleware\Authenticate as Middleware;

class Authenticate extends Middleware
{
    public function handle($request, Closure $next, ...$guards)
    {
        // 認証チェック
        if (!auth()->check()) {
            return response()->json(['message' => 'Unauthenticated'], 401);
        }

        // 次のミドルウェアまたはコントローラーに処理を渡す
        return $next($request);
    }
}
```

**コードリーディング**

*   `$request`: HTTPリクエスト
*   `$next`: 次のミドルウェアまたはコントローラー
*   `$guards`: ガード名（オプション）

---

### 🔍 前処理と後処理

#### 前処理（Before Middleware）

```php
public function handle($request, Closure $next)
{
    // リクエストの前処理
    Log::info('Request received');

    return $next($request);
}
```

#### 後処理（After Middleware）

```php
public function handle($request, Closure $next)
{
    $response = $next($request);

    // レスポンスの後処理
    Log::info('Response sent');

    return $response;
}
```

---

### 🚀 実践例3: ログ記録ミドルウェア

```php
public function handle($request, Closure $next)
{
    // リクエストの前処理
    Log::info('Request received', [
        'url' => $request->url(),
        'method' => $request->method(),
        'ip' => $request->ip(),
    ]);

    $response = $next($request);

    // レスポンスの後処理
    Log::info('Response sent', [
        'status' => $response->status(),
    ]);

    return $response;
}
```

---

### 💡 TIP: ミドルウェアの順序

ミドルウェアは、**定義された順番**に実行されます。

```php
Route::middleware(['auth', 'throttle:60,1'])->group(function () {
    // 1. auth ミドルウェアが実行される
    // 2. throttle ミドルウェアが実行される
    // 3. コントローラーが実行される
});
```

---

### 🚀 実践例4: メンテナンスモードミドルウェア

```php
public function handle($request, Closure $next)
{
    if (app()->isDownForMaintenance()) {
        return response()->json([
            'message' => 'Service Unavailable',
        ], 503);
    }

    return $next($request);
}
```

---

### 🔍 ミドルウェアグループ

複数のミドルウェアをグループ化できます。

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
        'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
    ],
];
```

**使用例**

```php
Route::middleware('web')->group(function () {
    // webミドルウェアグループが適用される
});
```

---

### 🚨 よくある間違い

#### 間違い1: `$next($request)`を返さない

```php
public function handle($request, Closure $next)
{
    if (!auth()->check()) {
        return response()->json(['message' => 'Unauthenticated'], 401);
    }
    
    // $next($request)を返さない
}
```

**対処法**: 必ず`$next($request)`を返します。

```php
public function handle($request, Closure $next)
{
    if (!auth()->check()) {
        return response()->json(['message' => 'Unauthenticated'], 401);
    }
    
    return $next($request); // OK
}
```

---

## ✨ まとめ

このセクションでは、ミドルウェアの役割と、Laravelの標準ミドルウェアについて学びました。

*   ミドルウェアは、リクエストとレスポンスの間に入る処理である。
*   認証チェック、ログ記録、CORS設定などを実装できる。
*   Laravelには、`auth`、`guest`、`throttle`などの標準ミドルウェアが用意されている。
*   ミドルウェアは、`handle()`メソッドを実装する。

次のセクションでは、カスタムミドルウェアの作成方法を学びます。

---

## 📝 学習のポイント

- [ ] ミドルウェアの役割を理解した。
- [ ] Laravelの標準ミドルウェアを使える。
- [ ] ミドルウェアの前処理と後処理を理解した。
- [ ] ミドルウェアの順序を理解した。
