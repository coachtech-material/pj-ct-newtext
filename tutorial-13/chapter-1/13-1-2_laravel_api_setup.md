# Tutorial 13-1-2: LaravelでAPIを開発する準備

## 🎯 このセクションで学ぶこと

- LaravelでAPI開発を行うための準備を学ぶ
- APIルーティングの設定方法を理解する
- APIレスポンスの基本的な返し方を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ概念理解の後に『環境構築』を行うのか？」

APIの概念を理解したら、次は「環境構築」です。

---

### 理由1: 手を動かして理解を深める

概念だけでは理解が浅くなります。**実際に環境を作って動かす**ことで理解が深まります。

---

### 理由2: LaravelのAPI機能を有効化

Laravelには**API開発用の機能**が用意されています。

| 機能 | 説明 |
|------|------|
| `api.php`ルートファイル | API専用のルーティング |
| APIミドルウェア | レート制限など |
| JSON レスポンス | 自動的なJSON変換 |

これらを有効化して、API開発の準備を整えます。

---

### 理由3: 開発環境の統一

チームで開発する場合、**環境が統一されている**ことが重要です。

このセクションで、API開発の標準的な環境を構築します。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | APIルーティングの設定 | `api.php`の使い方を学ぶ |
| Step 2 | APIコントローラーの作成 | RESTfulなコントローラー |
| Step 3 | APIレスポンスの返し方 | JSON形式のレスポンス |

> 💡 **ポイント**: LaravelはAPI開発に必要な機能が最初から揃っています。

---

## Step 1: APIルーティングの設定

### 1-1. APIルートファイル

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

### 1-2. APIルーティングの特徴

| 特徴 | 説明 |
|------|------|
| `/api`プレフィックス | `/user`は`/api/user`になる |
| `api`ミドルウェア | レート制限などが適用される |
| ステートレス | セッションは使用しない |

---

### 1-3. 簡単なAPIの作成

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
Route::get('/hello/{name}', function (string $name) {
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

### 1-4. curlでのテスト

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

## Step 2: APIコントローラーの作成

### 2-1. APIコントローラーを生成する

```bash
php artisan make:controller Api/TaskController --api
```

`--api`オプションを付けることで、API用のコントローラーが作成されます。

---

### 2-2. コントローラーの実装

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class TaskController extends Controller
{
    public function index(): JsonResponse
    {
        return response()->json([
            'data' => [
                ['id' => 1, 'title' => 'タスク1'],
                ['id' => 2, 'title' => 'タスク2'],
            ]
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        return response()->json([
            'message' => 'タスクを作成しました',
            'data' => [
                'id' => 3,
                'title' => $request->input('title'),
            ]
        ], 201);
    }

    public function show(string $id): JsonResponse
    {
        return response()->json([
            'data' => [
                'id' => $id,
                'title' => "タスク{$id}",
            ]
        ]);
    }

    public function update(Request $request, string $id): JsonResponse
    {
        return response()->json([
            'message' => 'タスクを更新しました',
            'data' => [
                'id' => $id,
                'title' => $request->input('title'),
            ]
        ]);
    }

    public function destroy(string $id): JsonResponse
    {
        return response()->json(null, 204);
    }
}
```

---

### 2-3. APIルーティングの設定

**ファイル**: `routes/api.php`

```php
<?php

use App\Http\Controllers\Api\TaskController;
use Illuminate\Support\Facades\Route;

Route::apiResource('tasks', TaskController::class);
```

---

### 2-4. apiResourceで作成されるルーティング

| HTTPメソッド | URL | アクション |
|---|---|---|
| GET | `/api/tasks` | index |
| POST | `/api/tasks` | store |
| GET | `/api/tasks/{id}` | show |
| PUT | `/api/tasks/{id}` | update |
| PATCH | `/api/tasks/{id}` | update |
| DELETE | `/api/tasks/{id}` | destroy |

---

### 2-5. ルーティングの確認

```bash
php artisan route:list --path=api
```

---

## Step 3: APIレスポンスの返し方

### 3-1. 基本的な使い方

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

### 3-2. エラーレスポンスの返し方

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

### 3-3. APIのバージョニング

**方法1: URLにバージョンを含める**

```php
Route::prefix('v1')->group(function () {
    Route::apiResource('tasks', TaskController::class);
});

// /api/v1/tasks
```

**方法2: ヘッダーでバージョンを指定する**

```
Header: Accept: application/vnd.api+json; version=v1
```

---

## 🚨 よくある間違い

### 間違い1: routes/web.phpにAPIを定義する

**問題**: セッションやCSRF保護が適用されてしまう

**対処法**: APIは`routes/api.php`に定義します。

---

### 間違い2: セッションを使おうとする

**問題**: APIはステートレスであるべき

**対処法**: 認証にはトークン（Sanctum）を使います。

---

### 間違い3: CORSの設定を忘れる

**問題**: フロントエンドからAPIにアクセスできない

**対処法**: `config/cors.php`でCORSを設定します。

---

## 💡 TIP: CORS（Cross-Origin Resource Sharing）の設定

フロントエンドとバックエンドが異なるドメインで動作する場合、**CORS**の設定が必要です。

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

## ✨ まとめ

このセクションでは、LaravelでAPI開発を行うための準備を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | APIルーティングの設定と特徴 |
| Step 2 | APIコントローラーの作成とapiResource |
| Step 3 | JSON形式のレスポンスとエラーハンドリング |

次のセクションでは、JSON形式について詳しく学びます。

---
