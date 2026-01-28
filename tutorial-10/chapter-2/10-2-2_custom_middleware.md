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

### 🚀 実践例1: メンテナンスモードミドルウェア

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

**コードリーディング（ミドルウェア）**：

| コード | 説明 |
|:---|:---|
| `config('app.maintenance_mode')` | `config/app.php` などの設定ファイルから、メンテナンス状態の値を取得します |
| `if (config(...))` | 設定値が `true`（メンテナンス中）であれば、`if` 文の中の処理を実行します |
| `response()->json([...])` | クライアントに対して、JSON形式でエラーメッセージを返します（API開発で一般的） |
| `503` | HTTPステータスコード「503 (Service Unavailable)」を返し、一時的に利用不可であることを示します |
| `return $next($request);` | メンテナンス中でない場合は、通常通りリクエストを次の処理（コントローラーなど）へ通します |

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

### 🚀 実践例2: 複数のパラメータを受け取る

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

**コードリーディング（ミドルウェアの実装）**：

| コード | 説明 |
|:---|:---|
| `$role, $permission` | ルート定義の `role:admin,edit` のようにコロン以降に渡した引数を受け取ります |
| `!$request->user()` | ユーザーがログインしていない（認証されていない）状態をチェックします |
| `$request->user()->role !== $role` | ログインユーザーの役割（role）が、期待される役割と一致するかを比較します |
| `hasPermission($permission)` | Userモデルなどで定義した、特定の権限（編集、削除など）の有無を判定するメソッドです |
| `response()->json([...], 403)` | 権限不足の場合、403（Forbidden）エラーをJSON形式で即座に返します |
| `return $next($request);` | 全てのチェックを通過した場合に、リクエストを次の処理（コントローラーなど）へ渡します |


#### ミドルウェアの適用

```php
Route::middleware('role:admin,manage_users')->group(function () {
    Route::get('/admin/users', [AdminController::class, 'users']);
});
```

**コードリーディング（ルートへの適用）**：

| コード | 説明 |
|:---|:---|
| `middleware('role:...')` | 「role」という名前で登録されたミドルウェアを呼び出します。名前の後の `:` は引数の開始合図です |
| `'admin,manage_users'` | ミドルウェアに渡す具体的な引数です。カンマ区切りで複数の値を渡せます |
| `group(function () { ... })` | このグループ内のすべてのルートに、一括で権限チェック（adminかつmanage_users権限）を適用します |
| `'/admin/users'` | ブラウザからアクセスするパスです |
| `[AdminController::class, 'users']` | 条件（ミドルウェア）をクリアしたときだけ、AdminController の users メソッドが実行されます |

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
