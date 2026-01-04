# Tutorial 10-2-2: カスタムミドルウェアの作成

## 🎯 このセクションで学ぶこと

*   独自のミドルウェアを作成できるようになる。
*   ミドルウェアをルートに適用できるようになる。
*   パラメータを受け取るミドルウェアを作成できるようになる。

---

## 導入：「独自の門番」を作る

前のセクションで、Laravelの標準ミドルウェアについて学びました。しかし、アプリケーション固有の処理を実装したい場合、**カスタムミドルウェア**を作成する必要があります。

このセクションでは、独自のミドルウェアを作成し、ルートに適用する方法を学びます。

---

## 詳細解説

### 🔧 ステップ1: ミドルウェアを生成

```bash
sail artisan make:middleware CheckAge
```

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
        // ミドルウェアの処理をここに書く
        return $next($request);
    }
}
```

---

### 🔧 ステップ2: ミドルウェアを実装

```php
public function handle(Request $request, Closure $next)
{
    if ($request->age < 18) {
        return response()->json([
            'message' => 'You must be 18 or older.',
        ], 403);
    }

    return $next($request);
}
```

**コードリーディング（1行ずつ分解）**

| コード | 演算子 | 意味 |
|:---|:---:|:---|
| `$request->age` | `->` | Requestインスタンスの`age`プロパティ（リクエストパラメータ）にアクセス |
| `$next($request)` | - | 次のミドルウェアまたはコントローラーにリクエストを渡す |

> **💡 Tutorial 7の復習**: `$request`はRequestクラスのインスタンスなので、`->`でプロパティやメソッドにアクセスします。`$next`はクロージャ（無名関数）なので、関数として`()`で呼び出します。

---

### 🔧 ステップ3: ミドルウェアを登録

**`app/Http/Kernel.php`**

```php
protected $middlewareAliases = [
    'auth' => \App\Http\Middleware\Authenticate::class,
    'guest' => \App\Http\Middleware\RedirectIfAuthenticated::class,
    'check.age' => \App\Http\Middleware\CheckAge::class, // 追加
];
```

---

### 🔧 ステップ4: ミドルウェアを適用

```php
Route::middleware('check.age')->group(function () {
    Route::get('/adult-content', [ContentController::class, 'show']);
});
```

---

### 🚀 実践例1: APIキーチェックミドルウェア

#### ステップ1: ミドルウェアを生成

```bash
sail artisan make:middleware CheckApiKey
```

#### ステップ2: ミドルウェアを実装

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class CheckApiKey
{
    public function handle(Request $request, Closure $next)
    {
        $apiKey = $request->header('X-API-Key');

        if ($apiKey !== config('app.api_key')) {
            return response()->json([
                'message' => 'Invalid API key.',
            ], 401);
        }

        return $next($request);
    }
}
```

#### ステップ3: ミドルウェアを登録

```php
protected $middlewareAliases = [
    'api.key' => \App\Http\Middleware\CheckApiKey::class,
];
```

#### ステップ4: ミドルウェアを適用

```php
Route::middleware('api.key')->group(function () {
    Route::get('/posts', [PostController::class, 'index']);
});
```

---

### 🚀 実践例2: ログ記録ミドルウェア

#### ステップ1: ミドルウェアを生成

```bash
sail artisan make:middleware LogRequests
```

#### ステップ2: ミドルウェアを実装

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
        // リクエストの前処理
        Log::info('Request received', [
            'url' => $request->url(),
            'method' => $request->method(),
            'ip' => $request->ip(),
            'user_agent' => $request->userAgent(),
        ]);

        $response = $next($request);

        // レスポンスの後処理
        Log::info('Response sent', [
            'status' => $response->status(),
        ]);

        return $response;
    }
}
```

**コードリーディング（Requestインスタンスのメソッド）**

| コード | 演算子 | 戻り値 | 意味 |
|:---|:---:|:---|:---|
| `$request->url()` | `->` | 文字列 | リクエストURLを取得 |
| `$request->method()` | `->` | 文字列 | HTTPメソッド（GET/POST等）を取得 |
| `$request->ip()` | `->` | 文字列 | クライアントIPアドレスを取得 |
| `$request->userAgent()` | `->` | 文字列 | User-Agentヘッダーを取得 |
| `$response->status()` | `->` | 整数 | HTTPステータスコードを取得 |

> **💡 ポイント**: `$request`と`$response`はどちらもインスタンスなので、`->`でメソッドを呼び出します。`Log::info()`はファサードの静的メソッドなので`::`を使います。

---

### 🔧 パラメータを受け取るミドルウェア

ミドルウェアは、パラメータを受け取ることができます。

#### ステップ1: ミドルウェアを生成

```bash
sail artisan make:middleware CheckRole
```

#### ステップ2: ミドルウェアを実装

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
            return response()->json([
                'message' => 'Unauthorized.',
            ], 403);
        }

        return $next($request);
    }
}
```

#### ステップ3: ミドルウェアを登録

```php
protected $middlewareAliases = [
    'role' => \App\Http\Middleware\CheckRole::class,
];
```

#### ステップ4: ミドルウェアを適用

```php
Route::middleware('role:admin')->group(function () {
    Route::get('/admin/dashboard', [AdminController::class, 'index']);
});
```

---

### 🚀 実践例3: 複数のパラメータを受け取る

#### ミドルウェアの実装

```php
public function handle(Request $request, Closure $next, $role, $permission)
{
    if (!$request->user() || 
        $request->user()->role !== $role || 
        !$request->user()->hasPermission($permission)) {
        return response()->json([
            'message' => 'Unauthorized.',
        ], 403);
    }

    return $next($request);
}
```

#### ミドルウェアの適用

```php
Route::middleware('role:admin,manage_users')->group(function () {
    Route::get('/admin/users', [AdminController::class, 'users']);
});
```

---

### 🚀 実践例4: IPアドレス制限ミドルウェア

#### ステップ1: ミドルウェアを生成

```bash
sail artisan make:middleware RestrictIp
```

#### ステップ2: ミドルウェアを実装

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class RestrictIp
{
    protected $allowedIps = [
        '127.0.0.1',
        '192.168.1.1',
    ];

    public function handle(Request $request, Closure $next)
    {
        if (!in_array($request->ip(), $this->allowedIps)) {
            return response()->json([
                'message' => 'Access denied.',
            ], 403);
        }

        return $next($request);
    }
}
```

---

### 🚀 実践例5: メンテナンスモードミドルウェア

#### ステップ1: ミドルウェアを生成

```bash
sail artisan make:middleware CheckMaintenance
```

#### ステップ2: ミドルウェアを実装

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class CheckMaintenance
{
    public function handle(Request $request, Closure $next)
    {
        if (config('app.maintenance_mode')) {
            return response()->json([
                'message' => 'Service is currently under maintenance.',
            ], 503);
        }

        return $next($request);
    }
}
```

---

### 💡 TIP: グローバルミドルウェアとして登録

全てのリクエストに適用したい場合、グローバルミドルウェアとして登録します。

**`app/Http/Kernel.php`**

```php
protected $middleware = [
    \App\Http\Middleware\LogRequests::class, // 追加
];
```

---

### 💡 TIP: ミドルウェアグループに追加

既存のミドルウェアグループに追加することもできます。

**`app/Http/Kernel.php`**

```php
protected $middlewareGroups = [
    'api' => [
        'throttle:api',
        \Illuminate\Routing\Middleware\SubstituteBindings::class,
        \App\Http\Middleware\LogRequests::class, // 追加
    ],
];
```

---

### 🚀 実践例6: CORS設定ミドルウェア

#### ステップ1: ミドルウェアを生成

```bash
sail artisan make:middleware Cors
```

#### ステップ2: ミドルウェアを実装

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class Cors
{
    public function handle(Request $request, Closure $next)
    {
        $response = $next($request);

        $response->headers->set('Access-Control-Allow-Origin', '*');
        $response->headers->set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
        $response->headers->set('Access-Control-Allow-Headers', 'Content-Type, Authorization');

        return $response;
    }
}
```

---

### 🚨 よくある間違い

#### 間違い1: ミドルウェアを登録し忘れる

```php
// Kernel.phpに登録していない
Route::middleware('check.age')->group(function () {
    // エラーになる
});
```

**対処法**: `Kernel.php`に登録します。

---

#### 間違い2: パラメータの順序を間違える

```php
public function handle(Request $request, Closure $next, $role, $permission)
{
    // ...
}

// パラメータの順序が逆
Route::middleware('role:manage_users,admin')->group(function () {
    // ...
});
```

**対処法**: パラメータの順序を確認します。

```php
Route::middleware('role:admin,manage_users')->group(function () {
    // OK
});
```

---

## ✨ まとめ

このセクションでは、カスタムミドルウェアの作成方法を学びました。

*   `sail artisan make:middleware`を使って、ミドルウェアを生成できる。
*   `handle()`メソッドを実装して、ミドルウェアの処理を定義できる。
*   `Kernel.php`に登録して、ミドルウェアを使用できるようにする。
*   パラメータを受け取るミドルウェアを作成できる。

次のセクションでは、HTTPライフサイクルを体験する実践演習を行います。

---
