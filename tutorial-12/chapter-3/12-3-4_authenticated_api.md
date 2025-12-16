# Tutorial 12-3-4: 認証が必要なAPIの実装

## 🎯 このセクションで学ぶこと

*   authミドルウェアを使って、認証が必要なAPIを実装する方法を学ぶ。
*   認証済みユーザーの情報を取得する方法を学ぶ。
*   401 Unauthorizedエラーを理解する。
*   ユーザーごとのデータを取得する方法を学ぶ。

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
| 1 | ミドルウェアの適用 | `auth:sanctum`を設定 |
| 2 | 認証ユーザーの取得 | `auth()->user()`を使用 |
| 3 | ユーザーごとのデータ | 自分のタスクだけを返す |

> 💡 **ポイント**: 認証済みAPIでは、ユーザーごとにデータをフィルタリングできます。

---

## 導入：なぜ認証が必要なのか

APIでは、**認証が必要なエンドポイント**と**認証が不要なエンドポイント**があります。

*   **認証が不要**: ログイン、ユーザー登録
*   **認証が必要**: タスクの作成、更新、削除

**認証が必要なAPI**には、**authミドルウェア**を適用します。

---

## 詳細解説

### 🔍 authミドルウェアの適用

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

**ポイント**:
*   `auth:sanctum`ミドルウェアを適用する
*   認証が必要なAPIは、このグループ内に定義する
*   ログインAPIは、認証が不要なので、グループ外に定義する

---

### 🔍 認証済みユーザーの情報を取得する

認証済みユーザーの情報を取得するには、`$request->user()`を使います。

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function index(Request $request)
{
    $user = $request->user();
    $tasks = Task::where('user_id', $user->id)->get();
    
    return response()->json($tasks, 200);
}
```

**ポイント**:
*   `$request->user()`で、認証済みユーザーを取得する
*   `Task::where('user_id', $user->id)`で、ユーザーのタスクだけを取得する

---

### 🔍 実践演習: 認証が必要なAPIをテストしてください

Thunder Clientで、以下のリクエストを送信してください。

**1. トークンなしでリクエストを送信**

*   メソッド: `GET`
*   URL: `http://localhost:8000/api/tasks`

**期待されるレスポンス**:

*   ステータスコード: `401 Unauthorized`
*   ボディ: `{"message": "Unauthenticated."}`

---

**2. トークンありでリクエストを送信**

*   メソッド: `GET`
*   URL: `http://localhost:8000/api/tasks`
*   Headers:
    *   キー: `Authorization`
    *   値: `Bearer トークン`

**期待されるレスポンス**:

*   ステータスコード: `200 OK`
*   ボディ: タスク一覧

---

### 🔍 HTTPステータスコード: 401 Unauthorized

**401 Unauthorized**は、**認証が必要**であることを示します。

**いつ使うか**:
*   トークンが提供されていない
*   トークンが無効

**なぜ401を使うのか**:
*   クライアント側で「認証が必要」と判断できる
*   ログイン画面にリダイレクトできる

**例**:

```json
{
  "message": "Unauthenticated."
}
```

---

### 🔍 タスクを作成する（認証済みユーザー）

タスクを作成する際、認証済みユーザーのIDを自動的に設定します。

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
        'priority' => 'required|integer|min:1|max:5',
    ]);
    
    $task = $request->user()->tasks()->create($validated);
    
    return response()->json($task, 201);
}
```

**ポイント**:
*   `$request->user()->tasks()->create()`で、タスクを作成する
*   `user_id`は自動的に設定される

---

### 🔍 Userモデルにリレーションを追加する

**ファイル**: `app/Models/User.php`

```php
public function tasks()
{
    return $this->hasMany(Task::class);
}
```

---

### 🔍 Taskモデルにリレーションを追加する

**ファイル**: `app/Models/Task.php`

```php
public function user()
{
    return $this->belongsTo(User::class);
}
```

---

### 🔍 他人のタスクを更新できないようにする

他人のタスクを更新できないようにします。

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function update(Request $request, $id)
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
        'priority' => 'required|integer|min:1|max:5',
    ]);
    
    $task->update($validated);
    
    return response()->json($task, 200);
}
```

**ポイント**:
*   `$task->user_id !== $request->user()->id`で、所有権をチェックする
*   所有権がない場合は、**403 Forbidden**を返す

---

### 🔍 HTTPステータスコード: 403 Forbidden

**403 Forbidden**は、**権限がない**ことを示します。

**いつ使うか**:
*   認証はされているが、権限がない
*   他人のリソースにアクセスしようとした

**なぜ403を使うのか**:
*   クライアント側で「権限がない」と判断できる
*   401 Unauthorizedとは区別できる

**例**:

```json
{
  "message": "Forbidden"
}
```

---

### 🔍 401と403の違い

| ステータスコード | 状況 | 対処法 |
|----------------|------|--------|
| **401 Unauthorized** | 認証が必要 | ログインする |
| **403 Forbidden** | 権限がない | アクセス権限を確認する |

---

### 🔍 実践演習: 他人のタスクを更新してみてください

Thunder Clientで、以下のリクエストを送信してください。

1.  ユーザーAでログインして、タスクを作成する
2.  ユーザーBでログインする
3.  ユーザーBで、ユーザーAのタスクを更新しようとする

**期待されるレスポンス**:

*   ステータスコード: `403 Forbidden`
*   ボディ: `{"message": "Forbidden"}`

---

### 🔍 ポリシーを使った認可

ポリシーを使うと、認可ロジックを分離できます。

```bash
php artisan make:policy TaskPolicy --model=Task
```

**ファイル**: `app/Policies/TaskPolicy.php`

```php
public function update(User $user, Task $task)
{
    return $user->id === $task->user_id;
}
```

**コントローラー**:

```php
public function update(Request $request, $id)
{
    $task = Task::findOrFail($id);
    
    $this->authorize('update', $task);
    
    $validated = $request->validate([...]);
    $task->update($validated);
    
    return response()->json($task, 200);
}
```

---

### 💡 TIP: auth()ヘルパーを使う

`auth()`ヘルパーを使うと、認証済みユーザーを取得できます。

```php
$user = auth()->user();
$tasks = auth()->user()->tasks;
```

---

### 🚨 よくある間違い

#### 間違い1: authミドルウェアを適用し忘れる

認証が必要なAPIには、`auth:sanctum`ミドルウェアを適用します。

```php
// ❌ 間違い
Route::apiResource('tasks', TaskController::class);

// ✅ 正しい
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('tasks', TaskController::class);
});
```

---

#### 間違い2: 所有権をチェックしない

他人のリソースにアクセスできないように、所有権をチェックします。

```php
// ❌ 間違い
public function update(Request $request, $id)
{
    $task = Task::findOrFail($id);
    // 所有権をチェックしていない
    $task->update($request->validated());
    return response()->json($task, 200);
}

// ✅ 正しい
public function update(Request $request, $id)
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

#### 間違い3: 401と403を混同する

*   **401 Unauthorized**: 認証が必要
*   **403 Forbidden**: 権限がない

---

## ✨ まとめ

このセクションでは、認証が必要なAPIの実装を学びました。

*   authミドルウェアを使って、認証が必要なAPIを実装した。
*   認証済みユーザーの情報を取得した。
*   401 Unauthorizedと403 Forbiddenを理解した。
*   ユーザーごとのデータを取得した。

次のセクションでは、APIセキュリティのベストプラクティスについて学びます。

---

## 📝 学習のポイント

- [ ] authミドルウェアを適用した。
- [ ] 認証済みユーザーの情報を取得した。
- [ ] 401 Unauthorizedを理解した。
- [ ] 403 Forbiddenを理解した。
- [ ] 所有権をチェックした。
