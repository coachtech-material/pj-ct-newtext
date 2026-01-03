# Tutorial 13-2-1: タスクAPIの実装（CRUD）

## 🎯 このセクションで学ぶこと

- データベースを使ったRESTful APIの実装方法を学ぶ
- CRUD操作（Create、Read、Update、Delete）をAPIで実装する
- 適切なHTTPステータスコードの選択方法を理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜAPI基礎の後に『CRUD API』を実装するのか？」

API基礎を学んだら、次は「CRUD API」の実装です。

---

### 理由1: 基本を実践で確認

概念を学んだら、**実際に手を動かして**理解を深めます。

Tutorial 11で作ったタスク管理アプリを、APIで操作できるようにします。

---

### 理由2: 既存のモデルを活用

新しいモデルを作るのではなく、**既存のTaskモデルを活用**します。

これにより、WebアプリとAPIで**同じデータを共有**できます。

---

### 理由3: まずは全体像を把握

個別のAPIを詳しく見る前に、**CRUD全体の設計**を確認します。

| メソッド | URL | 処理 |
|----------|-----|------|
| GET | /api/tasks | 一覧取得 |
| GET | /api/tasks/{id} | 詳細取得 |
| POST | /api/tasks | 新規作成 |
| PUT | /api/tasks/{id} | 更新 |
| DELETE | /api/tasks/{id} | 削除 |

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | モデルとマイグレーション | データベースの準備 |
| Step 2 | APIコントローラーの作成 | CRUD処理の実装 |
| Step 3 | ルーティングとテスト | 動作確認 |

> 💡 **ポイント**: `sail artisan make:controller Api/TaskController --api`でAPI用のコントローラーを作成できます。

---

## Step 1: モデルとマイグレーション

### 1-1. マイグレーションとモデルの作成

```bash
sail artisan make:model Task -m
```

---

### 1-2. マイグレーションファイル

**ファイル**: `database/migrations/xxxx_xx_xx_xxxxxx_create_tasks_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('tasks', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->cascadeOnDelete();
            $table->string('title');
            $table->text('description')->nullable();
            $table->enum('status', ['pending', 'in_progress', 'completed'])->default('pending');
            $table->date('due_date')->nullable();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('tasks');
    }
};
```

---

### 1-3. モデルファイル

**ファイル**: `app/Models/Task.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Task extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'title',
        'description',
        'status',
        'due_date',
    ];

    protected $casts = [
        'due_date' => 'date',
    ];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }
}
```

---

## Step 2: APIコントローラーの作成

### 2-1. コントローラーを生成する

```bash
sail artisan make:controller Api/TaskController --api
```

---

### 2-2. コントローラーの実装

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Task;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Auth;

class TaskController extends Controller
{
    public function index(): JsonResponse
    {
        $tasks = Task::where('user_id', Auth::id())->get();

        return response()->json([
            'data' => $tasks
        ], 200);
    }

    public function store(Request $request): JsonResponse
    {
        $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'due_date' => 'nullable|date',
        ]);

        $task = Task::create([
            'user_id' => Auth::id(),
            'title' => $request->title,
            'description' => $request->description,
            'status' => 'pending',
            'due_date' => $request->due_date,
        ]);

        return response()->json([
            'message' => 'タスクを作成しました',
            'data' => $task
        ], 201);
    }

    public function show(string $id): JsonResponse
    {
        $task = Task::where('user_id', Auth::id())->find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        return response()->json([
            'data' => $task
        ], 200);
    }

    public function update(Request $request, string $id): JsonResponse
    {
        $task = Task::where('user_id', Auth::id())->find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'status' => 'required|in:pending,in_progress,completed',
            'due_date' => 'nullable|date',
        ]);

        $task->update($request->only(['title', 'description', 'status', 'due_date']));

        return response()->json([
            'message' => 'タスクを更新しました',
            'data' => $task
        ], 200);
    }

    public function destroy(string $id): JsonResponse
    {
        $task = Task::where('user_id', Auth::id())->find($id);

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

### 2-3. コードリーディング

| コード | 説明 |
|--------|------|
| `Task::where('user_id', Auth::id())->get()` | ログインユーザーのタスクのみを取得 |
| `response()->json(['data' => $tasks], 200)` | 200（OK）でタスク一覧を返す |
| `response()->json([...], 201)` | 201（Created）で作成したタスクを返す |
| `response()->json([...], 404)` | 404（Not Found）でエラーを返す |
| `response()->json(null, 204)` | 204（No Content）でレスポンスボディなし |

---

### 2-4. HTTPステータスコードの選択

| ステータスコード | 意味 | 使用場面 |
|---|---|---|
| 200 | OK | リクエスト成功（データあり） |
| 201 | Created | リソースが作成された |
| 204 | No Content | リクエスト成功（データなし） |
| 400 | Bad Request | リクエストが不正 |
| 401 | Unauthorized | 認証が必要 |
| 403 | Forbidden | 権限がない |
| 404 | Not Found | リソースが見つからない |
| 422 | Unprocessable Entity | バリデーションエラー |
| 500 | Internal Server Error | サーバーエラー |

---

## Step 3: ルーティングとテスト

### 3-1. ルーティングの設定

**ファイル**: `routes/api.php`

```php
<?php

use App\Http\Controllers\Api\TaskController;
use Illuminate\Support\Facades\Route;

Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('tasks', TaskController::class);
});
```

---

### 3-2. curlでのテスト

```bash
# タスク一覧を取得
curl -X GET http://localhost/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN"

# タスクを作成
curl -X POST http://localhost/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "新しいタスク", "description": "これは新しいタスクです"}'

# タスク詳細を取得
curl -X GET http://localhost/api/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN"

# タスクを更新
curl -X PUT http://localhost/api/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "更新されたタスク", "status": "completed"}'

# タスクを削除
curl -X DELETE http://localhost/api/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 3-3. バリデーションエラーのレスポンス

バリデーションエラーが発生した場合、Laravelは自動的に422ステータスコードを返します。

```json
{
  "message": "The given data was invalid.",
  "errors": {
    "title": [
      "The title field is required."
    ]
  }
}
```

---

## 🚨 よくある間違い

### 間違い1: 全てのエラーで500を返す

**問題**: クライアントがエラーの種類を判別できない

**対処法**: 適切なHTTPステータスコードを返します。

---

### 間違い2: HTMLエラーページを返す

**問題**: APIクライアントがパースできない

**対処法**: JSON形式でエラーを返します。

---

### 間違い3: 他のユーザーのタスクにアクセスできる

**問題**: セキュリティリスク

**対処法**: `where('user_id', Auth::id())`で、ログインユーザーのタスクのみを取得します。

---

## 💡 TIP: エラーハンドリングの改善

より詳細なエラーメッセージを返すために、カスタムエラーハンドリングを実装できます。

```php
// app/Exceptions/Handler.php
public function render($request, Throwable $exception)
{
    if ($request->is('api/*')) {
        if ($exception instanceof ModelNotFoundException) {
            return response()->json([
                'message' => 'リソースが見つかりません'
            ], 404);
        }
    }

    return parent::render($request, $exception);
}
```

---

## ✨ まとめ

このセクションでは、タスクAPIの実装（CRUD）について学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | モデルとマイグレーションの作成 |
| Step 2 | APIコントローラーの実装とHTTPステータスコード |
| Step 3 | ルーティングとAPIのテスト |

次のセクションでは、APIリソースを使ったレスポンスの整形について学びます。

---
