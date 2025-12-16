# Tutorial 12-2-4: POST APIの実装（作成）

## 🎯 このセクションで学ぶこと

*   タスクを作成するPOST APIを実装する方法を学ぶ。
*   HTTPステータスコード（201 Created、422 Unprocessable Entity）を理解する。
*   なぜそのステータスコードを使うのかを学ぶ。
*   バリデーションの実装方法を学ぶ。

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
| 1 | storeメソッドの実装 | 作成のロジック |
| 2 | バリデーションの追加 | 不正なデータを弾く |
| 3 | 適切なレスポンス | 201ステータスコードを返す |

> 💡 **ポイント**: POSTリクエストは「新規作成」に使います。

---

## 導入：なぜ201 Createdを使うのか

リソースを作成した場合、**200 OK**ではなく、**201 Created**を返すのが正しいです。

*   **200 OK**: リクエストが成功した（一般的な成功）
*   **201 Created**: リソースが作成された（作成の成功）

**201 Created**を使うことで、**リソースが作成された**ことを明確に伝えられます。

---

## 詳細解説

### 🔍 タスクを作成するAPI

タスクを作成するAPIを実装します。

**エンドポイント**: `POST /api/tasks`

**リクエストボディ**:

```json
{
  "title": "新しいタスク",
  "description": "テスト説明",
  "status": "pending",
  "priority": 3
}
```

**レスポンス例（成功時）**:

```json
{
  "id": 1,
  "title": "新しいタスク",
  "description": "テスト説明",
  "status": "pending",
  "priority": 3,
  "created_at": "2024-01-01T00:00:00.000000Z",
  "updated_at": "2024-01-01T00:00:00.000000Z"
}
```

---

### 🔍 コントローラーの実装

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
    
    $task = Task::create($validated);
    
    return response()->json($task, 201);
}
```

**ポイント**:
*   `$request->validate()`で、バリデーションを行う
*   `Task::create()`で、タスクを作成する
*   **201 Created**を返す

---

### 🔍 HTTPステータスコード: 201 Created

**201 Created**は、**リソースが作成された**ことを示します。

**いつ使うか**:
*   POSTリクエストでリソースが作成された
*   PUTリクエストでリソースが作成された（稀）

**なぜ201を使うのか**:
*   クライアント側で「リソースが作成された」と判断できる
*   200 OKとは区別できる
*   RESTful APIの標準

**例**:

```php
return response()->json($task, 201);
```

---

### 🔍 HTTPステータスコード: 422 Unprocessable Entity

**422 Unprocessable Entity**は、**リクエストは正しいが、内容が不正**であることを示します。

**いつ使うか**:
*   バリデーションエラーが発生した
*   リクエストボディの内容が不正

**なぜ422を使うのか**:
*   クライアント側で「バリデーションエラーが発生した」と判断できる
*   400 Bad Requestとは区別できる（400は構文エラー、422は意味エラー）

**例**:

```json
{
  "message": "The given data was invalid.",
  "errors": {
    "title": [
      "The title field is required."
    ],
    "priority": [
      "The priority must be between 1 and 5."
    ]
  }
}
```

---

### 🔍 200、201、422の使い分け

| ステータスコード | 状況 | レスポンスボディ |
|----------------|------|----------------|
| **200 OK** | リクエストが成功した（更新など） | リソースのデータ |
| **201 Created** | リソースが作成された | 作成されたリソースのデータ |
| **422 Unprocessable Entity** | バリデーションエラー | エラーメッセージ |

---

### 🔍 バリデーションエラーのレスポンス

Laravelでは、バリデーションエラーが発生すると、自動的に**422 Unprocessable Entity**が返されます。

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

### 🔍 実践演習: タスク作成APIをテストしてください

Thunder Clientで、以下のリクエストを送信してください。

**1. 成功する場合**

*   メソッド: `POST`
*   URL: `http://localhost:8000/api/tasks`
*   Body（JSON）:

```json
{
  "title": "新しいタスク",
  "description": "テスト説明",
  "status": "pending",
  "priority": 3
}
```

**期待されるレスポンス**:

*   ステータスコード: `201 Created`
*   ボディ: 作成されたタスクのデータ

---

**2. バリデーションエラーが発生する場合**

*   メソッド: `POST`
*   URL: `http://localhost:8000/api/tasks`
*   Body（JSON）:

```json
{
  "title": "",
  "description": "テスト説明",
  "status": "pending",
  "priority": 10
}
```

**期待されるレスポンス**:

*   ステータスコード: `422 Unprocessable Entity`
*   ボディ: エラーメッセージ

---

### 🔍 ステータスコードの重要性

**適切なステータスコードを返す**ことで、クライアント側で以下のことができます。

*   **成功・失敗を判断する**: 201なら作成成功、422ならバリデーションエラー
*   **エラー処理を行う**: 422の場合はエラーメッセージを表示
*   **リトライを判断する**: 422の場合はリトライしない（ユーザーに修正を促す）

---

### 🔍 クライアント側での処理例（JavaScript）

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
    priority: 3,
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

### 🔍 Locationヘッダーを返す

201 Createdを返す場合、**Locationヘッダー**を返すのが推奨されます。

**Locationヘッダー**は、**作成されたリソースのURL**を示します。

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
        'priority' => 'required|integer|min:1|max:5',
    ]);
    
    $task = Task::create($validated);
    
    return response()->json($task, 201)
        ->header('Location', url("/api/tasks/{$task->id}"));
}
```

---

### 💡 TIP: FormRequestを使う

バリデーションロジックを分離するには、FormRequestを使います。

```bash
php artisan make:request TaskRequest
```

**ファイル**: `app/Http/Requests/TaskRequest.php`

```php
public function rules()
{
    return [
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
        'priority' => 'required|integer|min:1|max:5',
    ];
}
```

**コントローラー**:

```php
public function store(TaskRequest $request)
{
    $task = Task::create($request->validated());
    return response()->json($task, 201);
}
```

---

### 🚨 よくある間違い

#### 間違い1: 200 OKを返す

リソースを作成した場合は、**201 Created**を返します。

```php
// ❌ 間違い
return response()->json($task, 200);

// ✅ 正しい
return response()->json($task, 201);
```

---

#### 間違い2: バリデーションエラーで200を返す

バリデーションエラーの場合は、**422 Unprocessable Entity**を返します。

Laravelでは、`$request->validate()`を使うと、自動的に422が返されます。

---

#### 間違い3: ステータスコードを省略する

ステータスコードを省略すると、デフォルトで200が返されます。

```php
// ❌ 間違い
return response()->json($task); // 200が返される

// ✅ 正しい
return response()->json($task, 201); // 明示的に201を指定
```

---

## ✨ まとめ

このセクションでは、タスクを作成するPOST APIを実装しました。

*   **201 Created**: リソースが作成された場合に返す
*   **422 Unprocessable Entity**: バリデーションエラーの場合に返す
*   適切なステータスコードを返すことで、クライアント側で適切な処理ができる

次のセクションでは、PUT APIの実装について学びます。

---

## 📝 学習のポイント

- [ ] タスクを作成するAPIを実装した。
- [ ] 201 Createdを理解した。
- [ ] 422 Unprocessable Entityを理解した。
- [ ] なぜそのステータスコードを使うのかを理解した。
- [ ] バリデーションを実装した。
