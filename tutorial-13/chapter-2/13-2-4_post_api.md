# Tutorial 13-2-4: POST APIの実装（作成）

## 🎯 このセクションで学ぶこと

- タスクを作成するPOST APIを実装する方法を学ぶ
- HTTPステータスコード（201 Created、422 Unprocessable Entity）を理解する
- なぜそのステータスコードを使うのかを学ぶ
- バリデーションの実装方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ詳細取得の後に『作成API』を実装するのか？」

詳細取得APIができたら、次は「作成API」です。

---

### 理由1: データを作成する最初のAPI

詳細取得は「読み取り」でしたが、作成は**「書き込み」**です。

データベースに新しいレコードを追加します。

---

### 理由2: バリデーションが必要

作成APIでは、**リクエストデータのバリデーション**が必要です。

```php
$validated = $request->validate([
    'title' => 'required|max:255',
    'description' => 'nullable',
]);
```

---

### 理由3: HTTPステータスコード

作成成功時は、**201 Created**を返すのが一般的です。

```php
return response()->json($task, 201);
```

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | storeメソッドの実装 | 作成のロジック |
| Step 2 | HTTPステータスコード | 201と422の使い分け |
| Step 3 | テストと改善 | 正常系と異常系を確認 |

> 💡 **ポイント**: POSTリクエストは「新規作成」に使います。

---

## Step 1: storeメソッドの実装

### 1-1. タスクを作成するAPI

**エンドポイント**: `POST /api/tasks`

**リクエストボディ**:

```json
{
  "title": "新しいタスク",
  "description": "テスト説明",
  "status": "pending"
}
```

**レスポンス例（成功時）**:

```json
{
  "data": {
    "id": 1,
    "title": "新しいタスク",
    "description": "テスト説明",
    "status": "pending",
    "created_at": "2024-01-01 00:00:00",
    "updated_at": "2024-01-01 00:00:00"
  }
}
```

---

### 1-2. コントローラーの実装

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function store(Request $request): JsonResponse
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
        'due_date' => 'nullable|date',
    ]);
    
    $task = Task::create([
        'user_id' => Auth::id(),
        ...$validated,
    ]);
    
    return response()->json([
        'message' => 'タスクを作成しました',
        'data' => $task
    ], 201);
}
```

---

### 1-3. コードリーディング

| コード | 説明 |
|--------|------|
| `$request->validate([...])` | バリデーションを行う |
| `Auth::id()` | ログイン中のユーザーIDを取得 |
| `...$validated` | スプレッド構文で配列を展開 |
| `Task::create([...])` | タスクを作成する |
| `response()->json([...], 201)` | 201 Createdを返す |

---

### 1-4. スプレッド構文（`...`）の解説

`...$validated`は**スプレッド構文**と呼ばれ、配列を展開して別の配列にマージします。

```php
// $validatedの中身
$validated = [
    'title' => '新しいタスク',
    'description' => 'テスト説明',
    'status' => 'pending',
];

// スプレッド構文で展開
Task::create([
    'user_id' => Auth::id(),
    ...$validated,
]);

// 上記は以下と同じ意味
Task::create([
    'user_id' => Auth::id(),
    'title' => '新しいタスク',
    'description' => 'テスト説明',
    'status' => 'pending',
]);
```

| ポイント | 説明 |
|----------|------|
| `user_id` | ログインユーザーのIDを追加 |
| `...$validated` | バリデーション済みのデータを展開 |

> 💡 **ポイント**: スプレッド構文を使うと、バリデーション済みのデータに`user_id`を追加するコードが簡潔に書けます。

---

### 1-5. 認証の前提条件

`Auth::id()`を使うためには、**ユーザーが認証されている必要**があります。

以下の2つの設定が必要です。

---

#### 前提⚠️①: APIルートに認証ミドルウェアを適用

**ファイル**: `routes/api.php`

```php
<?php

use App\Http\Controllers\Api\TaskController;
use Illuminate\Support\Facades\Route;

Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('tasks', TaskController::class);
});
```

| コード | 説明 |
|--------|------|
| `middleware('auth:sanctum')` | Sanctum認証を適用 |
| `group(function () {...})` | グループ内のルートにミドルウェアを適用 |

> 📌 **注意**: 前のセクションで認証なしでテストしていた場合は、ここでミドルウェアを追加してください。

---

#### 前提⚠️②: トークンを発行する

APIリクエストには、**Bearerトークン**をヘッダーに添える必要があります。

**トークンの発行手順**:

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

#### Thunder Clientでトークンを設定する

Thunder Clientで認証ヘッダーを設定する方法です。

1. Thunder Clientで新しいリクエストを作成
2. **Auth**タブをクリック
3. **Type**で`Bearer`を選択
4. **Token**欄に発行したトークンを貼り付け

| 設定項目 | 値 |
|----------|------|
| Type | Bearer |
| Token | 発行したトークン |

> 💡 **ポイント**: Headersタブで`Authorization: Bearer トークン`を直接設定することもできますが、Authタブを使う方が簡単です。

---

## Step 2: HTTPステータスコード

### 2-1. 201 Created

**201 Created**は、**リソースが作成された**ことを示します。

| 使用場面 | 説明 |
|----------|------|
| POSTリクエストでリソースが作成された | タスクが作成された |
| 200 OKとは区別できる | 作成の成功を明確に伝える |

```php
return response()->json($task, 201);
```

---

### 2-2. 422 Unprocessable Entity

**422 Unprocessable Entity**は、**リクエストは正しいが、内容が不正**であることを示します。

| 使用場面 | 説明 |
|----------|------|
| バリデーションエラーが発生した | 必須項目が空など |
| リクエストボディの内容が不正 | 形式は正しいが値が不正 |

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

### 2-3. 200、201、422の使い分け

| ステータスコード | 状況 | レスポンスボディ |
|----------------|------|----------------|
| 200 OK | リクエストが成功した（更新など） | リソースのデータ |
| 201 Created | リソースが作成された | 作成されたリソースのデータ |
| 422 Unprocessable Entity | バリデーションエラー | エラーメッセージ |

---

## Step 3: テストと改善

### 3-1. Thunder Clientでテスト

> 📌 **前提**: 1-5で設定した認証ミドルウェアとトークンが必要です。AuthタブでBearerトークンを設定してください。

**1. 成功する場合**

- メソッド: `POST`
- URL: `http://localhost/api/tasks`
- Auth: Bearerトークンを設定
- Body（JSON）:

```json
{
  "title": "新しいタスク",
  "description": "テスト説明",
  "status": "pending"
}
```

- 期待: ステータスコード `201 Created`

**2. バリデーションエラーが発生する場合**

- メソッド: `POST`
- URL: `http://localhost/api/tasks`
- Auth: Bearerトークンを設定
- Body（JSON）:

```json
{
  "title": "",
  "status": "invalid"
}
```

- 期待: ステータスコード `422 Unprocessable Entity`

---

### 3-2. Locationヘッダーを返す

201 Createdを返す場合、**Locationヘッダー**を返すのが推奨されます。

```php
public function store(Request $request): JsonResponse
{
    $validated = $request->validate([...]);
    
    $task = Task::create([
        'user_id' => Auth::id(),
        ...$validated,
    ]);
    
    return response()->json(['data' => $task], 201)
        ->header('Location', url("/api/tasks/{$task->id}"));
}
```

---

### 3-3. FormRequestを使う

バリデーションロジックを分離するには、FormRequestを使います。

```bash
sail artisan make:request TaskRequest
```

**ファイル**: `app/Http/Requests/TaskRequest.php`

```php
public function rules(): array
{
    return [
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
        'due_date' => 'nullable|date',
    ];
}
```

**コントローラー**:

```php
public function store(TaskRequest $request): JsonResponse
{
    $task = Task::create([
        'user_id' => Auth::id(),
        ...$request->validated(),
    ]);
    
    return response()->json(['data' => $task], 201);
}
```

---

### 3-4. クライアント側での処理例（JavaScript）

```javascript
fetch('http://localhost/api/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Bearer 発行したトークン',
  },
  body: JSON.stringify({
    title: '新しいタスク',
    description: 'テスト説明',
    status: 'pending',
  }),
})
  .then(response => {
    if (response.status === 201) {
      return response.json();
    } else if (response.status === 422) {
      return response.json().then(data => {
        throw new Error(JSON.stringify(data.errors));
      });
    }
  })
  .then(data => {
    console.log('作成されたタスク:', data);
  })
  .catch(error => {
    console.error('エラー:', error);
  });
```

---

## 🚨 よくある間違い

### 間違い1: 200 OKを返す

**問題**: リソースを作成した場合は201を返すべき

```php
// ❌ 間違い
return response()->json($task, 200);

// ✅ 正しい
return response()->json($task, 201);
```

---

### 間違い2: バリデーションエラーで200を返す

**問題**: バリデーションエラーの場合は422を返すべき

Laravelでは、`$request->validate()`を使うと、自動的に422が返されます。

---

### 間違い3: ステータスコードを省略する

**問題**: デフォルトで200が返される

```php
// ❌ 間違い
return response()->json($task);

// ✅ 正しい
return response()->json($task, 201);
```

---

## 💡 TIP: ステータスコードの重要性

適切なステータスコードを返すことで、クライアント側で以下のことができます。

| 判断 | 説明 |
|------|------|
| 成功・失敗を判断する | 201なら作成成功、422ならバリデーションエラー |
| エラー処理を行う | 422の場合はエラーメッセージを表示 |
| リトライを判断する | 422の場合はリトライしない |

---

## ✨ まとめ

このセクションでは、タスクを作成するPOST APIを実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | storeメソッドの実装とバリデーション |
| Step 2 | 201 Createdと422 Unprocessable Entityの使い分け |
| Step 3 | FormRequestとLocationヘッダー |

次のセクションでは、PUT APIの実装について学びます。

---
