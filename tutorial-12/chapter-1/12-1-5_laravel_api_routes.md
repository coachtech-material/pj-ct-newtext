# Tutorial 12-1-5: LaravelでのAPI開発の準備

## 🎯 このセクションで学ぶこと

*   routes/api.phpとは何かを理解する。
*   APIルートの基本的な書き方を学ぶ。
*   routes/web.phpとroutes/api.phpの違いを理解する。
*   APIコントローラーの作成方法を学ぶ。

---

## 導入：なぜroutes/api.phpを使うのか

Laravelには、**routes/web.php**と**routes/api.php**の2つのルートファイルがあります。

*   **routes/web.php**: Webページ用のルート
*   **routes/api.php**: API用のルート

API開発では、**routes/api.php**を使います。

---

## 詳細解説

### 🔍 routes/api.phpとは

**routes/api.php**は、**API用のルート**を定義するファイルです。

**特徴**:
*   **URLの先頭に`/api`が自動的に付く**
*   **セッションを使わない**（ステートレス）
*   **CSRFトークンのチェックがない**

---

### 🔍 routes/web.phpとroutes/api.phpの違い

| 項目 | routes/web.php | routes/api.php |
|------|----------------|----------------|
| **用途** | Webページ | API |
| **URLの先頭** | なし | `/api` |
| **セッション** | あり | なし |
| **CSRFトークン** | あり | なし |
| **ミドルウェア** | `web` | `api` |

---

### 🔍 APIルートの基本的な書き方

**ファイル**: `routes/api.php`

```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\TaskController;

Route::get('/tasks', [TaskController::class, 'index']);
```

**ポイント**:
*   `Route::get()`で、GETリクエストのルートを定義する
*   第1引数は、URL（`/api`は自動的に付く）
*   第2引数は、コントローラーとメソッド

**アクセス**: `http://localhost:8000/api/tasks`

---

### 🔍 APIコントローラーの作成

APIコントローラーを作成します。

```bash
php artisan make:controller Api/TaskController --api
```

**ポイント**:
*   `--api`オプションを付けると、API用のメソッドが生成される
*   `Api/`ディレクトリに作成すると、整理しやすい

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    public function index()
    {
        $tasks = Task::all();
        return response()->json($tasks);
    }

    public function store(Request $request)
    {
        // タスクを作成
    }

    public function show($id)
    {
        $task = Task::find($id);
        return response()->json($task);
    }

    public function update(Request $request, $id)
    {
        // タスクを更新
    }

    public function destroy($id)
    {
        // タスクを削除
    }
}
```

---

### 🔍 ルートを定義する

**ファイル**: `routes/api.php`

```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\TaskController;

Route::get('/tasks', [TaskController::class, 'index']);
Route::post('/tasks', [TaskController::class, 'store']);
Route::get('/tasks/{id}', [TaskController::class, 'show']);
Route::put('/tasks/{id}', [TaskController::class, 'update']);
Route::delete('/tasks/{id}', [TaskController::class, 'destroy']);
```

---

### 🔍 Route::apiResourceを使う

上記のルートは、`Route::apiResource()`で一括定義できます。

```php
Route::apiResource('tasks', TaskController::class);
```

**自動的に定義されるルート**:

| HTTPメソッド | URL | メソッド | 用途 |
|-------------|-----|---------|------|
| GET | /api/tasks | index | 一覧取得 |
| POST | /api/tasks | store | 作成 |
| GET | /api/tasks/{id} | show | 詳細取得 |
| PUT/PATCH | /api/tasks/{id} | update | 更新 |
| DELETE | /api/tasks/{id} | destroy | 削除 |

---

### 🔍 ルートを確認する

定義したルートを確認するには、以下のコマンドを実行します。

```bash
php artisan route:list
```

**出力例**:

```
GET|HEAD   api/tasks ................ tasks.index › Api\TaskController@index
POST       api/tasks ................ tasks.store › Api\TaskController@store
GET|HEAD   api/tasks/{task} ......... tasks.show › Api\TaskController@show
PUT|PATCH  api/tasks/{task} ......... tasks.update › Api\TaskController@update
DELETE     api/tasks/{task} ......... tasks.destroy › Api\TaskController@destroy
```

---

### 🔍 実践演習: APIルートを定義してください

以下のルートを定義してください。

*   **GET /api/users**: ユーザー一覧を取得
*   **POST /api/users**: ユーザーを作成
*   **GET /api/users/{id}**: ユーザー詳細を取得

---

**解答例**:

```bash
php artisan make:controller Api/UserController --api
```

**ファイル**: `routes/api.php`

```php
use App\Http\Controllers\Api\UserController;

Route::get('/users', [UserController::class, 'index']);
Route::post('/users', [UserController::class, 'store']);
Route::get('/users/{id}', [UserController::class, 'show']);
```

または、`Route::apiResource()`を使う:

```php
Route::apiResource('users', UserController::class)->only(['index', 'store', 'show']);
```

---

### 🔍 APIのバージョニング

APIのバージョンを管理するには、URLに`/v1`を付けます。

```php
Route::prefix('v1')->group(function () {
    Route::apiResource('tasks', TaskController::class);
});
```

**アクセス**: `http://localhost:8000/api/v1/tasks`

---

### 🔍 ミドルウェアを適用する

APIルートには、ミドルウェアを適用できます。

```php
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('tasks', TaskController::class);
});
```

**ポイント**:
*   `auth:sanctum`は、Laravel Sanctumの認証ミドルウェア
*   認証が必要なAPIに適用する

---

### 💡 TIP: ルート名を付ける

ルートに名前を付けると、リダイレクトやURLの生成が簡単になります。

```php
Route::get('/tasks', [TaskController::class, 'index'])->name('api.tasks.index');
```

---

### 🚨 よくある間違い

#### 間違い1: routes/web.phpにAPIルートを書く

APIルートは、**routes/api.php**に書きます。

```php
// ❌ 間違い（routes/web.php）
Route::get('/api/tasks', [TaskController::class, 'index']);

// ✅ 正しい（routes/api.php）
Route::get('/tasks', [TaskController::class, 'index']);
```

---

#### 間違い2: /apiを付ける

routes/api.phpでは、**URLの先頭に`/api`が自動的に付く**ので、付ける必要はありません。

```php
// ❌ 間違い
Route::get('/api/tasks', [TaskController::class, 'index']);

// ✅ 正しい
Route::get('/tasks', [TaskController::class, 'index']);
```

---

#### 間違い3: --apiオプションを付けない

APIコントローラーを作成する際は、`--api`オプションを付けます。

```bash
# ❌ 間違い
php artisan make:controller TaskController

# ✅ 正しい
php artisan make:controller Api/TaskController --api
```

---

## ✨ まとめ

このセクションでは、LaravelでのAPI開発の準備を学びました。

*   routes/api.phpとは何かを理解した。
*   APIルートの基本的な書き方を学んだ。
*   APIコントローラーの作成方法を学んだ。
*   Route::apiResourceを使った。

次のセクションでは、CORSについて学びます。

---

## 📝 学習のポイント

- [ ] routes/api.phpを理解した。
- [ ] APIルートを定義した。
- [ ] APIコントローラーを作成した。
- [ ] Route::apiResourceを使った。
- [ ] ルートを確認した。
