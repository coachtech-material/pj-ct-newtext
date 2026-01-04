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

スターターキットに含まれるTaskモデルを使って、APIで操作できるようにします。

---

### 理由2: 既存のモデルを活用

新しいモデルを作るのではなく、**スターターキットのTaskモデルを活用**します。

これにより、すでにデータがある状態でAPIを試せます。

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
| Step 1 | モデルとマイグレーションの確認 | データベースの構造を理解 |
| Step 2 | APIコントローラーの作成 | CRUD処理の実装 |
| Step 3 | ルーティングとテスト | 動作確認 |

> 💡 **ポイント**: `sail artisan make:controller Api/TaskController --api`でAPI用のコントローラーを作成できます。

---

## Step 1: モデルとマイグレーションの確認

### 1-1. スターターキットに含まれるファイル

スターターキットには、以下のファイルが含まれています。

| ファイル | 説明 |
|----------|------|
| `database/migrations/xxxx_create_tasks_table.php` | tasksテーブルを作成 |
| `app/Models/Task.php` | Taskモデル |
| `database/seeders/TaskSeeder.php` | テストデータを投入 |

---

### 1-2. マイグレーションファイル（確認）

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

| カラム | 説明 |
|--------|------|
| `id` | 主キー（自動採番） |
| `user_id` | タスクの所有者 |
| `title` | タスクのタイトル |
| `description` | タスクの説明（任意） |
| `status` | ステータス（pending/in_progress/completed） |
| `due_date` | 期限日（任意） |
| `timestamps` | created_at, updated_at |

---

### 1-3. モデルファイル（確認）

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

### 1-4. コードリーディング

#### `protected $fillable = [...]`

```php
protected $fillable = [
    'user_id',
    'title',
    'description',
    'status',
    'due_date',
];
```

| 部分 | 説明 |
|------|------|
| `protected` | このクラス内とサブクラスからアクセス可能 |
| `$fillable` | 一括代入を許可するカラムの配列 |

`$fillable`に指定したカラムだけが、`Task::create([...])`で一括代入できます。

---

#### `protected $casts = [...]`

```php
protected $casts = [
    'due_date' => 'date',
];
```

| 部分 | 説明 |
|------|------|
| `$casts` | カラムの型変換を定義 |
| `'due_date' => 'date'` | `due_date`をCarbonの日付オブジェクトに変換 |

---

#### `public function user()`

```php
public function user()
{
    return $this->belongsTo(User::class);
}
```

| 部分 | 説明 |
|------|------|
| `public function user()` | リレーションを定義するメソッド |
| `$this->belongsTo(User::class)` | 「このタスクは1人のユーザーに属する」 |

---

### 1-5. シーダーで投入されるデータ

`sail artisan migrate:fresh --seed`を実行すると、テストデータが投入されます。

| データ | 内容 |
|--------|------|
| ユーザー | 1名（ID: 1） |
| タスク | 10件程度 |

> 💡 **ポイント**: シーダーでデータが投入されているので、すぐにAPIをテストできます。

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

class TaskController extends Controller
{
    /**
     * タスク一覧を取得
     */
    public function index()
    {
        // user_id = 1 のタスクを取得
        $tasks = Task::where('user_id', 1)->get();

        return response()->json([
            'data' => $tasks
        ], 200);
    }

    /**
     * タスクを作成
     */
    public function store(Request $request)
    {
        // バリデーション
        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'due_date' => 'nullable|date',
        ]);

        // タスクを作成
        $data = array_merge($validated, [
            'user_id' => 1,  // 本来は認証ユーザーのIDが入る
            'status' => 'pending',
        ]);
        
        $task = Task::create($data);

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
        // タスクを取得
        $task = Task::where('user_id', 1)->find($id);

        // タスクが見つからない場合
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
        // タスクを取得
        $task = Task::where('user_id', 1)->find($id);

        // タスクが見つからない場合
        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        // バリデーション
        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'status' => 'required|in:pending,in_progress,completed',
            'due_date' => 'nullable|date',
        ]);

        // タスクを更新
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
        // タスクを取得
        $task = Task::where('user_id', 1)->find($id);

        // タスクが見つからない場合
        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        // タスクを削除
        $task->delete();

        return response()->json(null, 204);
    }
}
```

---

### 2-3. コードリーディング（index メソッド）

```php
public function index()
{
    $tasks = Task::where('user_id', 1)->get();

    return response()->json([
        'data' => $tasks
    ], 200);
}
```

---

#### `Task::where('user_id', 1)`

```php
$tasks = Task::where('user_id', 1)->get();
```

**コードリーディング（メソッドチェーンの分解）**

| ステップ | コード | 演算子 | 戻り値 | 意味 |
|:---:|:---|:---:|:---|:---|
| 1 | `Task::where('user_id', 1)` | `::` | クエリビルダ | Taskモデルの静的メソッドで条件を指定 |
| 2 | `->get()` | `->` | Collection | クエリビルダのインスタンスメソッドで結果を取得 |

> **💡 Tutorial 7の復習**: `Task::where()`は静的メソッドなので`::`を使います。このメソッドはクエリビルダインスタンスを返すので、その後は`->`でインスタンスメソッドを呼び出します。

> 📌 **注意**: 本来は`Auth::id()`で認証ユーザーのIDを取得しますが、このチュートリアルでは簡略化のため`1`を固定で使用しています。

---

#### `response()->json([...], 200)`

```php
return response()->json([
    'data' => $tasks
], 200);
```

**コードリーディング（メソッドチェーンの分解）**

| ステップ | コード | 演算子 | 戻り値 | 意味 |
|:---:|:---|:---:|:---|:---|
| 1 | `response()` | - | ResponseFactory | レスポンスファクトリーを取得 |
| 2 | `->json([...], 200)` | `->` | JsonResponse | JSONレスポンスを作成 |

> **💡 ポイント**: `response()`はヘルパー関数で、ResponseFactoryインスタンスを返します。その後は`->`でインスタンスメソッドを呼び出します。

---

### 2-4. コードリーディング（store メソッド）

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'description' => 'nullable|string',
        'due_date' => 'nullable|date',
    ]);

    $data = array_merge($validated, [
        'user_id' => 1,
        'status' => 'pending',
    ]);
    
    $task = Task::create($data);

    return response()->json([
        'message' => 'タスクを作成しました',
        'data' => $task
    ], 201);
}
```

---

#### `$request->validate([...])`

```php
$validated = $request->validate([
    'title' => 'required|string|max:255',
    'description' => 'nullable|string',
    'due_date' => 'nullable|date',
]);
```

| 部分 | 説明 |
|------|------|
| `$request` | リクエストオブジェクト |
| `->validate([...])` | バリデーションを実行 |
| `'title' => 'required|string|max:255'` | titleは必須、文字列、最大255文字 |
| `'nullable'` | nullを許可（任意項目） |

バリデーションに失敗すると、自動的に422エラーが返されます。

---

#### `array_merge($validated, [...])`

```php
$data = array_merge($validated, [
    'user_id' => 1,
    'status' => 'pending',
]);
```

| 部分 | 説明 |
|------|------|
| `array_merge()` | 2つの配列を結合するPHP関数 |
| `$validated` | バリデーション済みのデータ |
| `['user_id' => 1, ...]` | 追加するデータ |

**結合後の`$data`の例**:

```php
[
    'title' => '新しいタスク',
    'description' => 'テスト説明',
    'due_date' => null,
    'user_id' => 1,
    'status' => 'pending',
]
```

---

#### `Task::create($data)`

```php
$task = Task::create($data);
```

| コード | 演算子 | 戻り値 | 意味 |
|:---|:---:|:---|:---|
| `Task::create($data)` | `::` | Taskインスタンス | 新しいタスクを作成してDBに保存 |

> **💡 Tutorial 7の復習**: `Task::create()`は静的メソッドなので`::`を使います。インスタンスを作成せずにクラスから直接呼び出しています。

---

### 2-5. コードリーディング（show メソッド）

```php
public function show(string $id)
{
    $task = Task::where('user_id', 1)->find($id);

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

---

#### `->find($id)`

```php
$task = Task::where('user_id', 1)->find($id);
```

| 部分 | 説明 |
|------|------|
| `->find($id)` | 指定したIDのレコードを取得 |
| 見つからない場合 | `null`を返す |

---

#### `if (!$task)`

```php
if (!$task) {
    return response()->json([
        'message' => 'タスクが見つかりません'
    ], 404);
}
```

| 部分 | 説明 |
|------|------|
| `!$task` | `$task`がnull（falsy）の場合 |
| `404` | HTTPステータスコード（Not Found） |

---

### 2-6. HTTPステータスコードの選択

| ステータスコード | 意味 | 使用場面 |
|---|---|---|
| 200 | OK | リクエスト成功（データあり） |
| 201 | Created | リソースが作成された |
| 204 | No Content | リクエスト成功（データなし） |
| 400 | Bad Request | リクエストが不正 |
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

---

### 3-2. ルーティングの確認

```bash
sail artisan route:list --path=api
```

---

### 3-3. Thunder Clientでテスト

#### タスク一覧を取得

- メソッド: `GET`
- URL: `http://localhost/api/tasks`
- 期待: ステータスコード `200 OK`

---

#### タスクを作成

- メソッド: `POST`
- URL: `http://localhost/api/tasks`
- Headers: `Content-Type: application/json`
- Body（JSON）:

```json
{
  "title": "新しいタスク",
  "description": "これは新しいタスクです"
}
```

- 期待: ステータスコード `201 Created`

---

#### タスク詳細を取得

- メソッド: `GET`
- URL: `http://localhost/api/tasks/1`
- 期待: ステータスコード `200 OK`

---

#### タスクを更新

- メソッド: `PUT`
- URL: `http://localhost/api/tasks/1`
- Headers: `Content-Type: application/json`
- Body（JSON）:

```json
{
  "title": "更新されたタスク",
  "description": "更新された説明",
  "status": "completed"
}
```

- 期待: ステータスコード `200 OK`

---

#### タスクを削除

- メソッド: `DELETE`
- URL: `http://localhost/api/tasks/1`
- 期待: ステータスコード `204 No Content`

---

### 3-4. バリデーションエラーのレスポンス

バリデーションエラーが発生した場合、Laravelは自動的に422ステータスコードを返します。

**テスト方法**:

- メソッド: `POST`
- URL: `http://localhost/api/tasks`
- Headers: `Content-Type: application/json`
- Body（JSON）:

```json
{
  "title": ""
}
```

**レスポンス例**:

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

### 間違い3: ステータスコードを省略する

**問題**: デフォルトで200が返される

```php
// ❌ 間違い
return response()->json($task);

// ✅ 正しい
return response()->json($task, 200);
```

---

## ✨ まとめ

このセクションでは、タスクAPIの実装（CRUD）について学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | モデルとマイグレーションの確認 |
| Step 2 | APIコントローラーの実装とHTTPステータスコード |
| Step 3 | ルーティングとAPIのテスト |

次のセクションでは、APIリソースを使ったレスポンスの整形について学びます。

---
