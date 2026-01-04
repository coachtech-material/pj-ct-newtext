# Tutorial 13-2-8: ハンズオン - タスク管理APIのCRUD実装

## 🎯 このハンズオンで学ぶこと

- タスクリソースのCRUD操作を実装する
- Thunder Clientで各操作のステータスコードとレスポンスを確認する
- バリデーションエラーと404エラーの挙動を確認する

---

## 🛠️ 事前準備

このハンズオンは、**Chapter 1のハンズオン（13-1-7）で構築した環境**を使用します。

まだ環境構築が完了していない場合は、先に13-1-7を完了してください。

---

## Step 1: コントローラーの作成

### 1-1. TaskControllerを作成

ターミナルで以下のコマンドを実行します。

```bash
sail artisan make:controller TaskController --api
```

| 部分 | 説明 |
|------|------|
| `make:controller` | コントローラーを作成 |
| `TaskController` | コントローラー名 |
| `--api` | APIリソース用のメソッドを自動生成 |

---

### 1-2. 生成されるメソッド

`--api`オプションを付けると、以下のメソッドが自動生成されます。

| メソッド | HTTPメソッド | 用途 |
|----------|-------------|------|
| `index()` | GET | 一覧取得 |
| `store()` | POST | 新規作成 |
| `show()` | GET | 詳細取得 |
| `update()` | PUT/PATCH | 更新 |
| `destroy()` | DELETE | 削除 |

---

## Step 2: CRUDメソッドの実装

### 2-1. TaskControllerを編集

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    /**
     * タスク一覧を取得
     */
    public function index()
    {
        $tasks = Task::all();

        return response()->json([
            'data' => $tasks
        ], 200);
    }

    /**
     * タスクを新規作成
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
        ]);

        $task = Task::create([
            'user_id' => 1,
            'title' => $validated['title'],
            'description' => $validated['description'] ?? null,
            'status' => 'pending',
        ]);

        return response()->json([
            'message' => 'タスクを作成しました',
            'data' => $task
        ], 201);
    }

    /**
     * タスク詳細を取得
     */
    public function show(string $id)
    {
        $task = Task::find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        return response()->json([
            'data' => $task
        ], 200);
    }

    /**
     * タスクを更新
     */
    public function update(Request $request, string $id)
    {
        $task = Task::find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'status' => 'required|in:pending,in_progress,completed',
        ]);

        $task->update($validated);

        return response()->json([
            'message' => 'タスクを更新しました',
            'data' => $task
        ], 200);
    }

    /**
     * タスクを削除
     */
    public function destroy(string $id)
    {
        $task = Task::find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        $task->delete();

        return response()->json(null, 204);
    }
}
```

---

### 2-2. コードリーディング

#### indexメソッド

```php
public function index()
{
    $tasks = Task::all();

    return response()->json([
        'data' => $tasks
    ], 200);
}
```

| 部分 | 説明 |
|------|------|
| `Task::all()` | 全てのタスクを取得 |
| `'data' => $tasks` | レスポンスのキー名を`data`に統一 |
| `200` | ステータスコード（OK） |

---

#### storeメソッド

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'description' => 'nullable|string',
    ]);

    $task = Task::create([
        'user_id' => 1,
        'title' => $validated['title'],
        'description' => $validated['description'] ?? null,
        'status' => 'pending',
    ]);

    return response()->json([
        'message' => 'タスクを作成しました',
        'data' => $task
    ], 201);
}
```

| 部分 | 説明 |
|------|------|
| `$request->validate()` | バリデーションを実行 |
| `'user_id' => 1` | ユーザーIDを1に固定 |
| `$validated['description'] ?? null` | descriptionがなければnull |
| `201` | ステータスコード（Created） |

---

#### showメソッド

```php
public function show(string $id)
{
    $task = Task::find($id);

    if (!$task) {
        return response()->json([
            'message' => 'タスクが見つかりません'
        ], 404);
    }

    return response()->json([
        'data' => $task
    ], 200);
}
```

| 部分 | 説明 |
|------|------|
| `Task::find($id)` | IDでタスクを検索（見つからなければnull） |
| `if (!$task)` | タスクが見つからない場合 |
| `404` | ステータスコード（Not Found） |

---

#### destroyメソッド

```php
public function destroy(string $id)
{
    $task = Task::find($id);

    if (!$task) {
        return response()->json([
            'message' => 'タスクが見つかりません'
        ], 404);
    }

    $task->delete();

    return response()->json(null, 204);
}
```

| 部分 | 説明 |
|------|------|
| `$task->delete()` | タスクを削除 |
| `null` | レスポンスボディなし |
| `204` | ステータスコード（No Content） |

---

## Step 3: ルーティングの設定

### 3-1. api.phpを編集

**ファイル**: `routes/api.php`

```php
<?php

use App\Http\Controllers\TaskController;
use Illuminate\Support\Facades\Route;

Route::get('/hello', function () {
    return response()->json(['message' => 'Hello, API!']);
});

Route::apiResource('tasks', TaskController::class);
```

---

### 3-2. apiResourceが生成するルート

`Route::apiResource('tasks', TaskController::class);`は、以下のルートを自動生成します。

| HTTPメソッド | URL | コントローラーメソッド |
|-------------|-----|---------------------|
| GET | /api/tasks | index |
| POST | /api/tasks | store |
| GET | /api/tasks/{id} | show |
| PUT/PATCH | /api/tasks/{id} | update |
| DELETE | /api/tasks/{id} | destroy |

---

## Step 4: Thunder Clientで動作確認

### 4-1. タスク一覧を取得（GET）

- メソッド: `GET`
- URL: `http://localhost/api/tasks`
- 期待: ステータスコード `200 OK`

**レスポンス例**:

```json
{
  "data": []
}
```

> 💡 **ポイント**: まだタスクがないので、空の配列が返ります。

---

### 4-2. タスクを作成（POST）

- メソッド: `POST`
- URL: `http://localhost/api/tasks`
- Headers:
  - `Content-Type: application/json`
- Body（JSON）:

```json
{
  "title": "最初のタスク",
  "description": "これはテストタスクです"
}
```

- 期待: ステータスコード `201 Created`

**レスポンス例**:

```json
{
  "message": "タスクを作成しました",
  "data": {
    "id": 1,
    "user_id": 1,
    "title": "最初のタスク",
    "description": "これはテストタスクです",
    "status": "pending",
    "created_at": "2024-01-01T00:00:00.000000Z",
    "updated_at": "2024-01-01T00:00:00.000000Z"
  }
}
```

---

### 4-3. タスク詳細を取得（GET）

- メソッド: `GET`
- URL: `http://localhost/api/tasks/1`
- 期待: ステータスコード `200 OK`

---

### 4-4. タスクを更新（PUT）

- メソッド: `PUT`
- URL: `http://localhost/api/tasks/1`
- Headers:
  - `Content-Type: application/json`
- Body（JSON）:

```json
{
  "title": "更新されたタスク",
  "description": "説明も更新しました",
  "status": "completed"
}
```

- 期待: ステータスコード `200 OK`

---

### 4-5. タスクを削除（DELETE）

- メソッド: `DELETE`
- URL: `http://localhost/api/tasks/1`
- 期待: ステータスコード `204 No Content`

---

## Step 5: エラーケースの確認

### 5-1. バリデーションエラー（422）

- メソッド: `POST`
- URL: `http://localhost/api/tasks`
- Headers:
  - `Content-Type: application/json`
  - `Accept: application/json`
- Body（JSON）:

```json
{
  "title": ""
}
```

- 期待: ステータスコード `422 Unprocessable Entity`

**レスポンス例**:

```json
{
  "message": "The title field is required.",
  "errors": {
    "title": [
      "The title field is required."
    ]
  }
}
```

> 💡 **ポイント**: `Accept: application/json`ヘッダーを付けることで、エラーがJSON形式で返ります。

---

### 5-2. 存在しないタスク（404）

- メソッド: `GET`
- URL: `http://localhost/api/tasks/9999`
- 期待: ステータスコード `404 Not Found`

**レスポンス例**:

```json
{
  "message": "タスクが見つかりません"
}
```

---

## 🚨 うまくいかない場合

### エラー1: 500 Internal Server Error

**原因**: Taskモデルの`$fillable`が設定されていない可能性

**対処法**: `app/Models/Task.php`を確認

```php
protected $fillable = [
    'user_id',
    'title',
    'description',
    'status',
];
```

---

### エラー2: HTMLが返ってくる

**原因**: `Accept: application/json`ヘッダーがない

**対処法**: Thunder ClientのHeadersタブで`Accept: application/json`を追加

---

### デバッグの方法

```php
public function store(Request $request)
{
    \Log::info('リクエストデータ:', $request->all());
    
    // ... 以下省略
}
```

```bash
sail logs
```

---

## ✨ まとめ

このハンズオンでは、タスク管理APIのCRUD操作を実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | コントローラーの作成 |
| Step 2 | CRUDメソッドの実装 |
| Step 3 | ルーティングの設定 |
| Step 4 | Thunder Clientでの動作確認 |
| Step 5 | エラーケースの確認 |

**実装したAPI**:

| HTTPメソッド | URL | 操作 | ステータスコード |
|-------------|-----|------|----------------|
| GET | /api/tasks | 一覧取得 | 200 |
| POST | /api/tasks | 作成 | 201 / 422 |
| GET | /api/tasks/{id} | 詳細取得 | 200 / 404 |
| PUT | /api/tasks/{id} | 更新 | 200 / 404 / 422 |
| DELETE | /api/tasks/{id} | 削除 | 204 / 404 |

次のChapter 3では、このAPIにセキュリティ対策を追加します。

---
