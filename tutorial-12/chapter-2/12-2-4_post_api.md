# Tutorial 12-2-4: POST APIの実装（作成）

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
| `Task::create($validated)` | タスクを作成する |
| `response()->json([...], 201)` | 201 Createdを返す |

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

**1. 成功する場合**

- メソッド: `POST`
- URL: `http://localhost:8000/api/tasks`
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
- URL: `http://localhost:8000/api/tasks`
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
php artisan make:request TaskRequest
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
fetch('http://localhost:8000/api/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
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
