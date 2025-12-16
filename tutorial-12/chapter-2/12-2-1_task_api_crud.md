# Tutorial 12-2-1: タスクAPIの実装（CRUD）

## 🎯 このセクションで学ぶこと

*   データベースを使ったRESTful APIの実装方法を学ぶ。
*   CRUD操作（Create、Read、Update、Delete）をAPIで実装する。
*   適切なHTTPステータスコードの選択方法を理解する。

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

- 一覧取得（GET /api/tasks）
- 詳細取得（GET /api/tasks/{id}）
- 新規作成（POST /api/tasks）
- 更新（PUT /api/tasks/{id}）
- 削除（DELETE /api/tasks/{id}）

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| 1 | APIコントローラーの作成 | `--api`オプションで作成 |
| 2 | ルートの定義 | `Route::apiResource()`を使用 |
| 3 | 基本的なCRUD実装 | 各メソッドの雛形を作成 |

> 💡 **ポイント**: `php artisan make:controller TaskApiController --api`でAPI用のコントローラーを作成できます。

---

## 導入：RESTful APIの実装

このセクションでは、**タスク管理システムのAPI**を実装します。

実装する機能は以下の通りです。

*   **タスク一覧の取得**: GET `/api/tasks`
*   **タスク詳細の取得**: GET `/api/tasks/{id}`
*   **タスクの作成**: POST `/api/tasks`
*   **タスクの更新**: PUT `/api/tasks/{id}`
*   **タスクの削除**: DELETE `/api/tasks/{id}`

---

## 詳細解説

### 🔍 マイグレーションとモデルの作成

まず、タスクのマイグレーションとモデルを作成します。

```bash
php artisan make:model Task -m
```

---

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

**ファイル**: `app/Models/Task.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

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

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

---

### 🔍 APIコントローラーの作成

```bash
php artisan make:controller Api/TaskController --api
```

---

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Task;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class TaskController extends Controller
{
    /**
     * タスク一覧を取得する
     */
    public function index()
    {
        $tasks = Task::where('user_id', Auth::id())->get();

        return response()->json([
            'data' => $tasks
        ], 200);
    }

    /**
     * タスクを作成する
     */
    public function store(Request $request)
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

    /**
     * タスク詳細を取得する
     */
    public function show(string $id)
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

    /**
     * タスクを更新する
     */
    public function update(Request $request, string $id)
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

    /**
     * タスクを削除する
     */
    public function destroy(string $id)
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

### 🔍 コードリーディング

#### `Task::where('user_id', Auth::id())->get()`

*   ログインユーザーのタスクのみを取得します。
*   他のユーザーのタスクは取得できません。

---

#### `return response()->json(['data' => $tasks], 200)`

*   HTTPステータスコード200（OK）で、タスク一覧を返します。

---

#### `return response()->json(['message' => 'タスクを作成しました', 'data' => $task], 201)`

*   HTTPステータスコード201（Created）で、作成したタスクを返します。
*   201は、リソースが正常に作成されたことを示します。

---

#### `return response()->json(['message' => 'タスクが見つかりません'], 404)`

*   HTTPステータスコード404（Not Found）で、エラーメッセージを返します。
*   404は、リソースが見つからないことを示します。

---

#### `return response()->json(null, 204)`

*   HTTPステータスコード204（No Content）で、レスポンスボディなしで返します。
*   204は、リクエストが成功したが、返すデータがないことを示します。

---

### 🔍 HTTPステータスコードの選択

APIでは、**適切なHTTPステータスコード**を返すことが重要です。

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

### 🔍 なぜ適切なステータスコードが重要なのか

適切なステータスコードを返すことで、以下のようなメリットがあります。

1. **クライアントが適切に処理できる**: フロントエンドで、エラーの種類に応じた処理ができる
2. **デバッグがしやすい**: ログを見たときに、何が起きたのかが分かりやすい
3. **RESTful APIの原則に従う**: 標準的なAPIの設計になる

---

### 🔍 ルーティングの設定

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

### 🔍 APIのテスト

#### curlでのテスト

```bash
# タスク一覧を取得
curl -X GET http://localhost/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN"

# タスクを作成
curl -X POST http://localhost/api/tasks \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "新しいタスク",
    "description": "これは新しいタスクです",
    "due_date": "2024-12-31"
  }'

# タスク詳細を取得
curl -X GET http://localhost/api/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN"

# タスクを更新
curl -X PUT http://localhost/api/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "更新されたタスク",
    "description": "更新しました",
    "status": "completed",
    "due_date": "2024-12-31"
  }'

# タスクを削除
curl -X DELETE http://localhost/api/tasks/1 \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### 🔍 バリデーションエラーのレスポンス

バリデーションエラーが発生した場合、Laravelは自動的に422ステータスコードとエラーメッセージを返します。

**例**:

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

HTTPステータスコード: `422 Unprocessable Entity`

---

### 💡 TIP: エラーハンドリングの改善

より詳細なエラーメッセージを返すために、カスタムエラーハンドリングを実装することもできます。

**ファイル**: `app/Exceptions/Handler.php`

```php
public function render($request, Throwable $exception)
{
    if ($request->is('api/*')) {
        if ($exception instanceof ModelNotFoundException) {
            return response()->json([
                'message' => 'リソースが見つかりません'
            ], 404);
        }

        if ($exception instanceof AuthenticationException) {
            return response()->json([
                'message' => '認証が必要です'
            ], 401);
        }
    }

    return parent::render($request, $exception);
}
```

---

### 🚨 よくある間違い

#### 間違い1: 全てのエラーで500を返す

**対処法**: 適切なHTTPステータスコードを返します。

---

#### 間違い2: HTMLエラーページを返す

**対処法**: APIでは、JSON形式でエラーを返します。

---

#### 間違い3: 他のユーザーのタスクにアクセスできる

**対処法**: `where('user_id', Auth::id())`で、ログインユーザーのタスクのみを取得します。

---

## ✨ まとめ

このセクションでは、タスクAPIの実装（CRUD）について学びました。

*   データベースを使ったRESTful APIの実装方法を学んだ。
*   CRUD操作（Create、Read、Update、Delete）をAPIで実装した。
*   適切なHTTPステータスコード（200、201、204、404、422）の選択方法を理解した。
*   バリデーションエラーは、自動的に422ステータスコードで返される。

次のセクションでは、APIリソースを使ったレスポンスの整形について学びます。

---

## 📝 学習のポイント

- [ ] データベースを使ったRESTful APIの実装方法を学んだ。
- [ ] CRUD操作（Create、Read、Update、Delete）をAPIで実装した。
- [ ] 適切なHTTPステータスコードの選択方法を理解した。
