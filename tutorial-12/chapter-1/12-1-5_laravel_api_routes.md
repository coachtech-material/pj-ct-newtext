# Tutorial 12-1-5: LaravelでのAPI開発の準備

## 🎯 このセクションで学ぶこと

- routes/api.phpとは何かを理解する
- APIルートの基本的な書き方を学ぶ
- routes/web.phpとroutes/api.phpの違いを理解する
- APIコントローラーの作成方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ開発ツールの後に『APIルート』を学ぶのか？」

開発ツールが使えるようになったら、次は「APIルート」です。

---

### 理由1: APIの入口を定義

ルートは**APIの入口**です。どのURLでどの処理を行うかを定義します。

```php
Route::get('/api/tasks', [TaskController::class, 'index']);
```

---

### 理由2: RESTfulな設計

REST APIでは、**リソースとHTTPメソッドの組み合わせ**でルートを設計します。

| メソッド | URL | 処理 |
|----------|-----|------|
| GET | /api/tasks | 一覧取得 |
| POST | /api/tasks | 新規作成 |
| GET | /api/tasks/{id} | 詳細取得 |
| PUT | /api/tasks/{id} | 更新 |
| DELETE | /api/tasks/{id} | 削除 |

---

### 理由3: api.phpの特徴

`routes/api.php`は、**APIミドルウェアが自動適用**されます。

- `/api`プレフィックスが自動付与
- セッション認証ではなくトークン認証向け

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | api.phpの確認 | APIルートファイルの特徴を理解 |
| Step 2 | APIコントローラーの作成 | CRUD用のコントローラー |
| Step 3 | ルートの定義と確認 | `apiResource`の使い方 |

> 💡 **ポイント**: `Route::apiResource()`を使うと、CRUD用のルートを一括で定義できます。

---

## Step 1: routes/api.phpの理解

### 1-1. routes/api.phpとは

**routes/api.php**は、**API用のルート**を定義するファイルです。

| 特徴 | 説明 |
|------|------|
| URLの先頭に`/api`が自動的に付く | `/tasks`は`/api/tasks`になる |
| セッションを使わない | ステートレス |
| CSRFトークンのチェックがない | APIはトークン認証を使う |

---

### 1-2. routes/web.phpとの違い

| 項目 | routes/web.php | routes/api.php |
|------|----------------|----------------|
| 用途 | Webページ | API |
| URLの先頭 | なし | `/api` |
| セッション | あり | なし |
| CSRFトークン | あり | なし |
| ミドルウェア | `web` | `api` |

---

### 1-3. APIルートの基本的な書き方

**ファイル**: `routes/api.php`

```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\TaskController;

Route::get('/tasks', [TaskController::class, 'index']);
```

**アクセス**: `http://localhost/api/tasks`

---

## Step 2: APIコントローラーの作成

> 💡 **Tutorial 12-1-2で既に作成済みの場合**
>
> Tutorial 12-1-2で`Api/TaskController`を既に作成している場合は、このステップはスキップしてください。
> ただし、「2-2. コントローラーの実装」では、既存のコードに**メソッドを追加・修正**する必要があります。

### 2-1. コントローラーを生成する

**新規作成の場合**：

```bash
sail artisan make:controller Api/TaskController --api
```

**ポイント**:

- `--api`オプションを付けると、API用のメソッドが生成される
- `Api/`ディレクトリに作成すると、整理しやすい

> ⚠️ **既にファイルが存在する場合**は、コマンドを実行するとエラーになります。その場合は次の「2-2. コントローラーの実装」に進んでください。

---

### 2-2. コントローラーの実装

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

> 💡 **Tutorial 12-1-2で既に作成済みの場合**
>
> Tutorial 12-1-2で作成した`TaskController`には、ダミーデータを返す実装がされています。
> ここでは、**データベースから実際のデータを取得する実装**に書き換えます。
>
> **修正が必要なメソッド**:
> - `index()`: `Task::all()`を使って全タスクを取得
> - `show()`: `Task::findOrFail($id)`を使って特定のタスクを取得

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Task;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;

class TaskController extends Controller
{
    public function index(): JsonResponse
    {
        // データベースから全タスクを取得
        $tasks = Task::all();
        return response()->json($tasks);
    }

    public function store(Request $request): JsonResponse
    {
        // タスクを作成（後のセクションで実装）
    }

    public function show(string $id): JsonResponse
    {
        // データベースから特定のタスクを取得
        $task = Task::findOrFail($id);
        return response()->json($task);
    }

    public function update(Request $request, string $id): JsonResponse
    {
        // タスクを更新（後のセクションで実装）
    }

    public function destroy(string $id): JsonResponse
    {
        // タスクを削除（後のセクションで実装）
    }
}
```

**Tutorial 12-1-2との違い**:

| 項目 | Tutorial 12-1-2 | このセクション |
|------|----------------|----------------|
| `index()` | ダミーデータを返す | `Task::all()`でDBから取得 |
| `show()` | ダミーデータを返す | `Task::findOrFail()`でDBから取得 |

---

## Step 3: ルートの定義と確認

> 💡 **Tutorial 12-1-2で既に定義済みの場合**
>
> Tutorial 12-1-2で`Route::apiResource('tasks', TaskController::class)`を既に定義している場合は、このステップはスキップしてください。
> 「3-3. ルートを確認する」で、ルートが正しく定義されているか確認しましょう。

このステップでは、APIルートの定義方法を詳しく学びます。

### 3-1. 個別にルートを定義する（参考）

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

### 3-2. Route::apiResourceを使う

上記のルートは、`Route::apiResource()`で一括定義できます。

```php
Route::apiResource('tasks', TaskController::class);
```

**自動的に定義されるルート**:

| HTTPメソッド | URL | メソッド | 用途 |
|-------------|-----|---------|------|
| GET | /api/tasks | index | 一覧取得 |
| POST | /api/tasks | store | 作成 |
| GET | /api/tasks/{task} | show | 詳細取得 |
| PUT/PATCH | /api/tasks/{task} | update | 更新 |
| DELETE | /api/tasks/{task} | destroy | 削除 |

---

### 3-3. ルートを確認する

```bash
sail artisan route:list --path=api
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

### 3-4. 実践演習

以下のルートを定義してください。

- **GET /api/users**: ユーザー一覧を取得
- **POST /api/users**: ユーザーを作成
- **GET /api/users/{id}**: ユーザー詳細を取得

**解答例**:

```bash
sail artisan make:controller Api/UserController --api
```

```php
Route::apiResource('users', UserController::class)->only(['index', 'store', 'show']);
```

---

### 3-5. APIのバージョニング

```php
Route::prefix('v1')->group(function () {
    Route::apiResource('tasks', TaskController::class);
});
```

**アクセス**: `http://localhost/api/v1/tasks`

---

## 🚨 よくある間違い

### 間違い1: routes/web.phpにAPIルートを書く

**問題**: セッションやCSRF保護が適用されてしまう

```php
// ❌ 間違い（routes/web.php）
Route::get('/api/tasks', [TaskController::class, 'index']);

// ✅ 正しい（routes/api.php）
Route::get('/tasks', [TaskController::class, 'index']);
```

---

### 間違い2: /apiを付ける

**問題**: routes/api.phpでは、URLの先頭に`/api`が自動的に付く

```php
// ❌ 間違い
Route::get('/api/tasks', [TaskController::class, 'index']);

// ✅ 正しい
Route::get('/tasks', [TaskController::class, 'index']);
```

---

### 間違い3: --apiオプションを付けない

**問題**: API用のメソッドが生成されない

```bash
# ❌ 間違い
sail artisan make:controller TaskController

# ✅ 正しい
sail artisan make:controller Api/TaskController --api
```

---

## 💡 TIP: ルート名を付ける

ルートに名前を付けると、リダイレクトやURLの生成が簡単になります。

```php
Route::get('/tasks', [TaskController::class, 'index'])->name('api.tasks.index');
```

---

## ✨ まとめ

このセクションでは、LaravelでのAPI開発の準備を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | routes/api.phpの特徴とweb.phpとの違い |
| Step 2 | APIコントローラーの作成 |
| Step 3 | Route::apiResourceの使い方とルートの確認 |

次のセクションでは、CORSについて学びます。

---
