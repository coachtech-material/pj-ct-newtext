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

// デフォルトでは空のファイルです
// ここにAPIルートを定義します
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

**curl（カール）とは？**

`curl`は、**コマンドラインからHTTPリクエストを送信できるツール**です。ブラウザを使わずに、ターミナルから直接APIをテストできます。

| 特徴 | 説明 |
|------|------|
| ブラウザ不要 | ターミナルから直接リクエストを送信 |
| HTTPメソッド指定 | GET, POST, PUT, DELETEなどを指定可能 |
| ヘッダー設定 | Content-Typeなどのヘッダーを設定可能 |
| データ送信 | JSONデータをリクエストボディとして送信可能 |

> 💡 **ポイント**: API開発では、curlを使って素早く動作確認を行うのが一般的です。

**基本的なオプション**:

| オプション | 説明 | 例 |
|------|------|------|
| `-X` | HTTPメソッドを指定 | `-X POST` |
| `-H` | ヘッダーを設定 | `-H "Content-Type: application/json"` |
| `-d` | リクエストボディのデータ | `-d '{"title":"test"}'` |

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
sail artisan make:controller Api/TaskController --api
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

### 2-3. コードリーディング

| コード | 説明 |
|--------|------|
| `namespace App\Http\Controllers\Api` | API用コントローラーの名前空間（`Api`ディレクトリ内） |
| `JsonResponse` | JSONレスポンスの型ヒント（戻り値の型を明示） |
| `response()->json([...])` | 配列をJSON形式に変換してレスポンスを返す |
| `response()->json([...], 201)` | 第2引数でHTTPステータスコードを指定 |
| `response()->json(null, 204)` | ボディなしのレスポンス（削除成功時など） |
| `$request->input('title')` | リクエストボディから`title`の値を取得 |
| `string $id` | ルートパラメータ`{id}`の値を受け取る |

**各メソッドの役割**:

| メソッド | HTTPメソッド | 役割 | ステータスコード |
|--------|------|------|------|
| `index()` | GET | 一覧取得 | 200 |
| `store()` | POST | 新規作成 | 201 |
| `show()` | GET | 詳細取得 | 200 |
| `update()` | PUT/PATCH | 更新 | 200 |
| `destroy()` | DELETE | 削除 | 204 |

> 💡 **ポイント**: `--api`オプションで生成すると、`create()`と`edit()`メソッドが含まれません。これらはHTMLフォーム表示用なので、APIでは不要です。

---

### 2-4. APIルーティングの設定

**ファイル**: `routes/api.php`

```php
<?php

use App\Http\Controllers\Api\TaskController;
use Illuminate\Support\Facades\Route;

Route::apiResource('tasks', TaskController::class);
```

---

### 2-5. apiResourceで作成されるルーティング

| HTTPメソッド | URL | アクション |
|---|---|---|
| GET | `/api/tasks` | index |
| POST | `/api/tasks` | store |
| GET | `/api/tasks/{id}` | show |
| PUT | `/api/tasks/{id}` | update |
| PATCH | `/api/tasks/{id}` | update |
| DELETE | `/api/tasks/{id}` | destroy |

---

### 2-6. ルーティングの確認

```bash
sail artisan route:list --path=api
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

**対処法**: APIではセッションを使わず、トークンベースの認証を使います。

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
    'paths' => ['api/*'],
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
