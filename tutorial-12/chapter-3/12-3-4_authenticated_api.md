# Tutorial 12-3-4: 認証が必要なAPIの実装

## 🎯 このセクションで学ぶこと

- authミドルウェアを使って、認証が必要なAPIを実装する方法を学ぶ
- 認証済みユーザーの情報を取得する方法を学ぶ
- 401 Unauthorizedエラーを理解する
- ユーザーごとのデータを取得する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜログインAPIの後に『認証済みAPI』を実装するのか？」

ログインAPIでトークンを発行できるようになったら、次は「認証済みAPI」です。

---

### 理由1: トークンの検証

発行したトークンを使って、**APIリクエストを認証**します。

クライアントは、リクエストヘッダーにトークンを含めて送信します。

```
Authorization: Bearer {token}
```

---

### 理由2: ミドルウェアで保護

Sanctumの`auth:sanctum`ミドルウェアを使うと、**認証が必要なルートを保護**できます。

```php
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('tasks', TaskApiController::class);
});
```

---

### 理由3: 認証ユーザーの取得

認証済みのリクエストでは、`auth()->user()`で**現在のユーザー**を取得できます。

これにより、ユーザーごとのデータを返すことができます。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | ミドルウェアの適用 | auth:sanctumを設定 |
| Step 2 | 認証済みAPIの実装 | ユーザーごとのデータ取得 |
| Step 3 | 認可の実装 | 所有権チェック |

> 💡 **ポイント**: 認証済みAPIでは、ユーザーごとにデータをフィルタリングできます。

---

## Step 1: ミドルウェアの適用

### 1-1. authミドルウェアの適用

**ファイル**: `routes/api.php`

```php
use App\Http\Controllers\Api\TaskController;
use App\Http\Controllers\Api\AuthController;

Route::post('/login', [AuthController::class, 'login']);

Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::apiResource('tasks', TaskController::class);
});
```

---

### 1-2. 認証が必要なAPIと不要なAPI

| API | 認証 | 理由 |
|-----|------|------|
| ログイン | 不要 | 認証前にアクセスする |
| ユーザー登録 | 不要 | 認証前にアクセスする |
| タスクの作成・更新・削除 | 必要 | ユーザーのデータを操作する |
| ログアウト | 必要 | 認証済みユーザーのみ |

---

### 1-3. Thunder Clientでテスト

**1. トークンなしでリクエストを送信**

- メソッド: `GET`
- URL: `http://localhost:8000/api/tasks`
- 期待: ステータスコード `401 Unauthorized`

```json
{
  "message": "Unauthenticated."
}
```

**2. トークンありでリクエストを送信**

- メソッド: `GET`
- URL: `http://localhost:8000/api/tasks`
- Headers: `Authorization: Bearer トークン`
- 期待: ステータスコード `200 OK`

---

## Step 2: 認証済みAPIの実装

### 2-1. 認証済みユーザーの情報を取得する

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function index(Request $request): JsonResponse
{
    $user = $request->user();
    $tasks = Task::where('user_id', $user->id)->get();
    
    return response()->json(['data' => $tasks], 200);
}
```

---

### 2-2. コードリーディング

| コード | 説明 |
|--------|------|
| `$request->user()` | 認証済みユーザーを取得 |
| `Task::where('user_id', $user->id)` | ユーザーのタスクだけを取得 |

---

### 2-3. タスクを作成する（認証済みユーザー）

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function store(Request $request): JsonResponse
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
    ]);
    
    $task = $request->user()->tasks()->create($validated);
    
    return response()->json(['data' => $task], 201);
}
```

> 💡 **ポイント**: `$request->user()->tasks()->create()`で、`user_id`は自動的に設定されます。

---

### 2-4. Userモデルにリレーションを追加する

**ファイル**: `app/Models/User.php`

```php
public function tasks(): HasMany
{
    return $this->hasMany(Task::class);
}
```

---

### 2-5. Taskモデルにリレーションを追加する

**ファイル**: `app/Models/Task.php`

```php
public function user(): BelongsTo
{
    return $this->belongsTo(User::class);
}
```

---

## Step 3: 認可の実装

### 3-1. 他人のタスクを更新できないようにする

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function update(Request $request, string $id): JsonResponse
{
    $task = Task::findOrFail($id);
    
    if ($task->user_id !== $request->user()->id) {
        return response()->json([
            'message' => 'Forbidden'
        ], 403);
    }
    
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
    ]);
    
    $task->update($validated);
    
    return response()->json(['data' => $task], 200);
}
```

---

### 3-2. 401と403の違い

| ステータスコード | 状況 | 対処法 |
|----------------|------|--------|
| 401 Unauthorized | 認証が必要 | ログインする |
| 403 Forbidden | 権限がない | アクセス権限を確認する |

---

### 3-3. ポリシーを使った認可

ポリシーを使うと、認可ロジックを分離できます。

```bash
php artisan make:policy TaskPolicy --model=Task
```

**ファイル**: `app/Policies/TaskPolicy.php`

```php
public function update(User $user, Task $task): bool
{
    return $user->id === $task->user_id;
}
```

**コントローラー**:

```php
public function update(Request $request, string $id): JsonResponse
{
    $task = Task::findOrFail($id);
    
    $this->authorize('update', $task);
    
    $validated = $request->validate([...]);
    $task->update($validated);
    
    return response()->json(['data' => $task], 200);
}
```

---

### 3-4. 実践演習: 他人のタスクを更新してみてください

1. ユーザーAでログインして、タスクを作成する
2. ユーザーBでログインする
3. ユーザーBで、ユーザーAのタスクを更新しようとする

**期待されるレスポンス**:

- ステータスコード: `403 Forbidden`
- ボディ: `{"message": "Forbidden"}`

---

## 🚨 よくある間違い

### 間違い1: authミドルウェアを適用し忘れる

**問題**: 認証なしでAPIにアクセスできてしまう

```php
// ❌ 間違い
Route::apiResource('tasks', TaskController::class);

// ✅ 正しい
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('tasks', TaskController::class);
});
```

---

### 間違い2: 所有権をチェックしない

**問題**: 他人のリソースにアクセスできてしまう

```php
// ❌ 間違い
public function update(Request $request, string $id)
{
    $task = Task::findOrFail($id);
    $task->update($request->validated());
    return response()->json($task, 200);
}

// ✅ 正しい
public function update(Request $request, string $id)
{
    $task = Task::findOrFail($id);
    
    if ($task->user_id !== $request->user()->id) {
        return response()->json(['message' => 'Forbidden'], 403);
    }
    
    $task->update($request->validated());
    return response()->json($task, 200);
}
```

---

### 間違い3: 401と403を混同する

| コード | 意味 |
|--------|------|
| 401 Unauthorized | 認証が必要 |
| 403 Forbidden | 権限がない |

---

## 💡 TIP: auth()ヘルパーを使う

`auth()`ヘルパーを使うと、認証済みユーザーを取得できます。

```php
$user = auth()->user();
$tasks = auth()->user()->tasks;
```

---

## ✨ まとめ

このセクションでは、認証が必要なAPIの実装を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | authミドルウェアの適用 |
| Step 2 | 認証済みユーザーの情報取得とリレーション |
| Step 3 | 所有権チェックとポリシーによる認可 |

次のセクションでは、APIセキュリティのベストプラクティスについて学びます。

---
