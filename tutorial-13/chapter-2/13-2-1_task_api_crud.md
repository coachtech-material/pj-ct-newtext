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

### 1-1. 既存のモデルとマイグレーションを確認

Tutorial 11で既に`Task`モデルとマイグレーションを作成済みです。

**新たに作成する必要はありません。**

ここでは、既存のファイルの内容を確認しましょう。

---

### 1-2. マイグレーションファイル（確認）

**ファイル**: `database/migrations/xxxx_xx_xx_xxxxxx_create_tasks_table.php`

Tutorial 11で作成したマイグレーションファイルは以下のようになっています。

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
            $table->foreignId('category_id')->nullable()->constrained()->onDelete('set null');
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

| カラム | 説明 |
|--------|------|
| `user_id` | タスクの所有者（ユーザー削除時にタスクも削除） |
| `category_id` | カテゴリー（任意、カテゴリー削除時はnullに） |
| `title` | タスクのタイトル |
| `description` | タスクの説明（任意） |
| `status` | ステータス（pending/in_progress/completed） |
| `due_date` | 期限日（任意） |

---

### 1-3. モデルファイル（確認）

**ファイル**: `app/Models/Task.php`

Tutorial 11・12で作成したモデルファイルは以下のようになっています。

```php
<?php

namespace App\Models;

use App\Models\Scopes\UserScope;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Auth;

class Task extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'user_id',
        'category_id',
        'title',
        'description',
        'status',
        'due_date',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'due_date' => 'date',
    ];

    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new UserScope);
    }

    /**
     * タスクが属するユーザー（多対1）
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    /**
     * このタスクが属するカテゴリー
     */
    public function category()
    {
        return $this->belongsTo(Category::class);
    }

    /**
     * このタスクに付いているタグ
     */
    public function tags()
    {
        return $this->belongsToMany(Tag::class);
    }

    /**
     * ログインユーザーのタスクのみを取得するスコープ
     */
    public function scopeForCurrentUser($query)
    {
        return $query->where('user_id', Auth::id());
    }

    /**
     * 完了したタスクのみを取得するスコープ
     */
    public function scopeCompleted($query)
    {
        return $query->where('status', 'completed');
    }

    /**
     * 未完了のタスクのみを取得するスコープ
     */
    public function scopePending($query)
    {
        return $query->where('status', 'pending');
    }
}
```

---

### 1-4. モデルのポイント

| ポイント | 説明 |
|----------|------|
| `$fillable` | 一括代入を許可するカラム（`category_id`も含む） |
| `$casts` | 日付型への自動変換 |
| `booted()` | グローバルスコープでユーザーフィルタリング |
| リレーション | `user()`, `category()`, `tags()`で関連データを取得 |
| ローカルスコープ | `scopeCompleted()`, `scopePending()`でクエリを簡潔に |

> 💡 **ポイント**: 既存のモデルにはグローバルスコープ（`UserScope`）が設定されているため、自動的にログインユーザーのタスクのみが取得されます。APIコントローラーでもこの機能が活用されます。

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

Route::apiResource('tasks', TaskController::class);
```

> **📌 認証について**
> 
> このカリキュラムではAPI認証の実装は扱いません。実際の開発では、認証が必要な場合はミドルウェアを適用します。

---

### 3-2. トークンの発行（認証が必要な場合）

APIに認証をかけている場合、リクエストには**トークン**が必要です。

Laravel Sanctumを使ってトークンを発行するには、`tinker`を使います。

```bash
sail artisan tinker
```

`tinker`内で以下を実行します。

```php
$user = App\Models\User::first();
$token = $user->createToken('test-token')->plainTextToken;
echo $token;
```

表示されたトークンをコピーしておきます。

---

### 3-3. curlでのテスト

APIリクエストでは、以下のヘッダーが重要です。

| ヘッダー | 説明 |
|----------|------|
| `Authorization: Bearer トークン` | 認証用のトークン（認証が必要な場合） |
| `Content-Type: application/json` | リクエストボディのJSON形式を指定 |
| `Accept: application/json` | レスポンスをJSON形式で受け取る |

> 💡 **ポイント**: `Accept: application/json`がないと、認証失敗時にHTMLのリダイレクトが返されることがあります。APIリクエストでは必ず指定しましょう。

---

#### タスク一覧を取得

```bash
curl -X GET http://localhost/api/tasks \
  -H "Authorization: Bearer 発行したトークン" \
  -H "Accept: application/json"
```

---

#### タスクを作成

```bash
curl -X POST http://localhost/api/tasks \
  -H "Authorization: Bearer 発行したトークン" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"title": "新しいタスク", "description": "これは新しいタスクです"}'
```

---

#### タスク詳細を取得

```bash
curl -X GET http://localhost/api/tasks/1 \
  -H "Authorization: Bearer 発行したトークン" \
  -H "Accept: application/json"
```

---

#### タスクを更新

```bash
curl -X PUT http://localhost/api/tasks/1 \
  -H "Authorization: Bearer 発行したトークン" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"title": "更新されたタスク", "status": "completed"}'
```

---

#### タスクを削除

```bash
curl -X DELETE http://localhost/api/tasks/1 \
  -H "Authorization: Bearer 発行したトークン" \
  -H "Accept: application/json"
```

---

### 3-4. 認証失敗時のレスポンス

トークンが無効または未指定の場合、以下のJSONが返されます。

```json
{"message": "Unauthenticated."}
```

| ステータスコード | 意味 |
|------------------|------|
| 401 Unauthorized | 認証が必要または失敗 |

---

### 3-5. バリデーションエラーのレスポンス

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
