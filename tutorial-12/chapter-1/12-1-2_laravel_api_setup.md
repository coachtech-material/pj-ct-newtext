# Tutorial 12-1-2: LaravelでAPIを開発する準備

## 🎯 このセクションで学ぶこと

*   LaravelでAPI開発を行うための準備を学ぶ。
*   APIルーティングの設定方法を理解する。
*   APIレスポンスの基本的な返し方を学ぶ。

---

## 導入：LaravelでのAPI開発

Laravelは、**API開発に適したフレームワーク**です。

Laravelには、以下のようなAPI開発に便利な機能があります。

*   **APIルーティング**: `/api`プレフィックスが自動的に付与される
*   **APIリソース**: JSON形式のレスポンスを簡単に作成できる
*   **Sanctum**: API認証を簡単に実装できる
*   **レート制限**: APIへのアクセス回数を制限できる

このセクションでは、LaravelでAPI開発を行うための準備を学びます。

---

## 詳細解説

### 🔍 APIルーティングの設定

Laravelでは、`routes/api.php`にAPIのルーティングを定義します。

**ファイル**: `routes/api.php`

```php
<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');
```

---

### 🔍 APIルーティングの特徴

`routes/api.php`に定義したルーティングは、以下のような特徴があります。

*   **`/api`プレフィックスが自動的に付与される**: `/user`は`/api/user`になる
*   **`api`ミドルウェアグループが適用される**: レート制限などが適用される
*   **セッションは使用しない**: ステートレスなAPIを実現する

---

### 🔍 簡単なAPIの作成

まずは、簡単なAPIを作成してみましょう。

**ファイル**: `routes/api.php`

```php
<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

// 簡単なHello World API
Route::get('/hello', function () {
    return response()->json([
        'message' => 'Hello, World!'
    ]);
});

// パラメータを受け取るAPI
Route::get('/hello/{name}', function ($name) {
    return response()->json([
        'message' => "Hello, {$name}!"
    ]);
});

// POSTリクエストを受け取るAPI
Route::post('/echo', function (Request $request) {
    return response()->json([
        'message' => $request->input('message')
    ]);
});
```

---

### 🔍 APIのテスト

APIをテストするには、以下のツールを使います。

*   **Postman**: GUIでAPIをテストできる
*   **curl**: コマンドラインでAPIをテストできる
*   **Laravelのテスト機能**: 自動テストを書ける

---

#### curlでのテスト

```bash
# GETリクエスト
curl http://localhost/api/hello

# パラメータ付きGETリクエスト
curl http://localhost/api/hello/Taro

# POSTリクエスト
curl -X POST http://localhost/api/echo \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello from curl"}'
```

---

### 🔍 APIコントローラーの作成

実際のAPI開発では、コントローラーを使ってAPIを実装します。

```bash
php artisan make:controller Api/TaskController --api
```

`--api`オプションを付けることで、API用のコントローラーが作成されます。

---

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        return response()->json([
            'data' => [
                ['id' => 1, 'title' => 'タスク1'],
                ['id' => 2, 'title' => 'タスク2'],
            ]
        ]);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request)
    {
        return response()->json([
            'message' => 'タスクを作成しました',
            'data' => [
                'id' => 3,
                'title' => $request->input('title'),
            ]
        ], 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        return response()->json([
            'data' => [
                'id' => $id,
                'title' => "タスク{$id}",
            ]
        ]);
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id)
    {
        return response()->json([
            'message' => 'タスクを更新しました',
            'data' => [
                'id' => $id,
                'title' => $request->input('title'),
            ]
        ]);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id)
    {
        return response()->json([
            'message' => 'タスクを削除しました'
        ], 204);
    }
}
```

---

### 🔍 APIルーティングの設定

**ファイル**: `routes/api.php`

```php
<?php

use App\Http\Controllers\Api\TaskController;
use Illuminate\Support\Facades\Route;

Route::apiResource('tasks', TaskController::class);
```

`apiResource`を使うことで、以下のルーティングが自動的に作成されます。

| HTTPメソッド | URL | アクション |
|---|---|---|
| GET | `/api/tasks` | index |
| POST | `/api/tasks` | store |
| GET | `/api/tasks/{id}` | show |
| PUT | `/api/tasks/{id}` | update |
| PATCH | `/api/tasks/{id}` | update |
| DELETE | `/api/tasks/{id}` | destroy |

---

### 🔍 ルーティングの確認

```bash
php artisan route:list --path=api
```

これにより、`/api`で始まるルーティングの一覧が表示されます。

---

### 🔍 APIレスポンスの返し方

Laravelでは、`response()->json()`を使ってJSON形式のレスポンスを返します。

```php
// 基本的な使い方
return response()->json([
    'message' => 'Success'
]);

// ステータスコードを指定
return response()->json([
    'message' => 'Created'
], 201);

// ヘッダーを指定
return response()->json([
    'message' => 'Success'
], 200, [
    'X-Custom-Header' => 'Value'
]);
```

---

### 🔍 エラーレスポンスの返し方

```php
// 404 Not Found
return response()->json([
    'message' => 'Task not found'
], 404);

// 422 Unprocessable Entity（バリデーションエラー）
return response()->json([
    'message' => 'The given data was invalid.',
    'errors' => [
        'title' => ['The title field is required.']
    ]
], 422);

// 500 Internal Server Error
return response()->json([
    'message' => 'Server error'
], 500);
```

---

### 🔍 CORS（Cross-Origin Resource Sharing）の設定

フロントエンドとバックエンドが異なるドメインで動作する場合、**CORS**の設定が必要です。

Laravelでは、`config/cors.php`でCORSの設定を行います。

**ファイル**: `config/cors.php`

```php
<?php

return [
    'paths' => ['api/*', 'sanctum/csrf-cookie'],
    'allowed_methods' => ['*'],
    'allowed_origins' => ['*'],
    'allowed_origins_patterns' => [],
    'allowed_headers' => ['*'],
    'exposed_headers' => [],
    'max_age' => 0,
    'supports_credentials' => false,
];
```

---

### 💡 TIP: APIのバージョニング

APIは、バージョンを管理することが重要です。

**方法1: URLにバージョンを含める**

```php
Route::prefix('v1')->group(function () {
    Route::apiResource('tasks', TaskController::class);
});

// /api/v1/tasks
```

---

**方法2: ヘッダーでバージョンを指定する**

```php
Route::middleware('api.version:v1')->group(function () {
    Route::apiResource('tasks', TaskController::class);
});

// Header: Accept: application/vnd.api+json; version=v1
```

---

### 🚨 よくある間違い

#### 間違い1: `routes/web.php`にAPIを定義する

**対処法**: APIは`routes/api.php`に定義します。

---

#### 間違い2: セッションを使おうとする

**対処法**: APIはステートレスであるべきです。認証にはトークンを使います。

---

#### 間違い3: CORSの設定を忘れる

**対処法**: フロントエンドとバックエンドが異なるドメインの場合、CORSの設定が必要です。

---

## ✨ まとめ

このセクションでは、LaravelでAPI開発を行うための準備を学びました。

*   LaravelのAPIルーティングは、`routes/api.php`に定義する。
*   `/api`プレフィックスが自動的に付与される。
*   `response()->json()`を使ってJSON形式のレスポンスを返す。
*   `apiResource`を使うことで、RESTful APIのルーティングを簡単に作成できる。
*   CORSの設定が必要な場合がある。

次のセクションでは、実際にデータベースを使ったAPIを実装します。

---

## 📝 学習のポイント

- [ ] LaravelでAPI開発を行うための準備を学んだ。
- [ ] APIルーティングの設定方法を理解した。
- [ ] APIレスポンスの基本的な返し方を学んだ。
