# Tutorial 11-2-4: POST APIの実装（作成）

## 🎯 このセクションで学ぶこと

- タスクを作成するPOST APIを実装する方法を学ぶ
- HTTPステータスコード（201 Created、422 Unprocessable Entity）を理解する
- なぜそのステータスコードを使うのかを学ぶ
- バリデーションの実装方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ詳細取得APIの後に『作成API』を実装するのか？」

詳細取得APIができたら、次は「作成API」です。

---

### 理由1: CRUDの順序

CRUD（Create, Read, Update, Delete）の順序で学ぶと理解しやすいです。

| 順序 | 操作 | 説明 |
|------|------|------|
| 1 | Read（一覧・詳細） | データを取得する |
| 2 | Create | データを作成する |
| 3 | Update | データを更新する |
| 4 | Delete | データを削除する |

---

### 理由2: バリデーションの導入

作成APIでは、**入力データのバリデーション**が必要です。

| バリデーション | 説明 |
|----------------|------|
| 必須チェック | titleは必須 |
| 型チェック | titleは文字列 |
| 長さチェック | titleは255文字以内 |

---

### 理由3: 201 Createdの使い方

リソースを作成した場合は、**201 Created**を返します。

```php
return (new TaskResource($task))
    ->additional(['message' => 'タスクを作成しました'])
    ->response()
    ->setStatusCode(201);
```

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | storeメソッドの実装 | 作成のロジック |
| Step 2 | HTTPステータスコード | 201と422の使い分け |
| Step 3 | テスト | Thunder Clientで動作確認 |

> 💡 **ポイント**: POSTリクエストは「新規作成」に使います。

---

## Step 1: storeメソッドの実装

### 1-1. タスクを作成するAPI

**エンドポイント**: `POST /api/tasks`

**リクエストボディ**:

```json
{
  "title": "新しいタスク",
  "description": "これは新しいタスクです",
  "due_date": "2024-12-31"
}
```

**レスポンス例（成功時）**:

```json
{
  "data": {
    "id": 1,
    "title": "新しいタスク",
    "description": "これは新しいタスクです",
    "status": "pending",
    "status_label": "未着手",
    "due_date": "2024-12-31",
    "created_at": "2024-01-01 00:00:00",
    "updated_at": "2024-01-01 00:00:00"
  },
  "message": "タスクを作成しました"
}
```

---

### 1-2. コントローラーの実装

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
use App\Http\Resources\TaskResource;

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
        'user_id' => 1,
        'status' => 'pending',
    ]);
    
    $task = Task::create($data);

    // レスポンスを返す（TaskResourceで整形）
    return (new TaskResource($task))
        ->additional(['message' => 'タスクを作成しました'])
        ->response()
        ->setStatusCode(201);
}
```

---

### 1-3. コードリーディング

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
| `$validated` | バリデーション済みのデータ（配列） |

バリデーションに失敗すると、自動的に422エラーが返されます。

---

#### バリデーションルールの詳細

| ルール | 説明 |
|--------|------|
| `required` | 必須項目 |
| `string` | 文字列であること |
| `max:255` | 最大255文字 |
| `nullable` | nullを許可（任意項目） |
| `date` | 日付形式であること |

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

**処理の流れ**:

```php
// $validated の内容
[
    'title' => '新しいタスク',
    'description' => 'テスト説明',
    'due_date' => '2024-12-31',
]

// array_merge() で追加
[
    'user_id' => 1,
    'status' => 'pending',
]

// 結合後の $data
[
    'title' => '新しいタスク',
    'description' => 'テスト説明',
    'due_date' => '2024-12-31',
    'user_id' => 1,
    'status' => 'pending',
]
```

> 📌 **なぜarray_merge()を使うのか**: バリデーション済みのデータ（`$validated`）に、システムが設定するデータ（`user_id`、`status`）を追加するためです。`user_id`と`status`はユーザーが入力するものではなく、サーバー側で設定します。

---

#### `Task::create($data)`

```php
$task = Task::create($data);
```

| 部分 | 説明 |
|------|------|
| `Task::create(...)` | 新しいタスクを作成してデータベースに保存 |
| `$data` | 保存するデータの配列 |
| `$task` | 作成されたタスクのインスタンス |

---

#### `(new TaskResource($task))->additional([...])->response()->setStatusCode(201)`

```php
return (new TaskResource($task))
    ->additional(['message' => 'タスクを作成しました'])
    ->response()
    ->setStatusCode(201);
```

**コードリーディング（メソッドチェーンの分解）**

| ステップ | コード | 戻り値 | 意味 |
|:---:|:---|:---|:---|
| 1 | `new TaskResource($task)` | TaskResourceインスタンス | タスクをResourceに変換 |
| 2 | `->additional(['message' => '...'])` | TaskResourceインスタンス | レスポンスに追加データを含める |
| 3 | `->response()` | JsonResponseインスタンス | レスポンスオブジェクトを取得 |
| 4 | `->setStatusCode(201)` | JsonResponseインスタンス | ステータスコードを201に設定 |

> **💡 Tutorial 11-2-2の復習**: `additional()`メソッドを使うと、`data`キー以外に追加のデータ（`message`など）を含めることができます。

**レスポンス例**:

```json
{
  "data": {
    "id": 1,
    "title": "新しいタスク",
    "status": "pending",
    "status_label": "未着手",
    ...
  },
  "message": "タスクを作成しました"
}
```

---

## Step 2: HTTPステータスコード

### 2-1. 201 Created

**201 Created**は、**リソースが正常に作成された**ことを示します。

| 使用場面 | 説明 |
|----------|------|
| 新しいリソースが作成された | タスクが作成された |
| 処理が正常に完了した | 作成されたリソースのデータを返す |

```php
return (new TaskResource($task))
    ->additional(['message' => 'タスクを作成しました'])
    ->response()
    ->setStatusCode(201);
```

---

### 2-2. 422 Unprocessable Entity

**422 Unprocessable Entity**は、**バリデーションエラー**を示します。

| 使用場面 | 説明 |
|----------|------|
| 入力データが不正 | titleが空、日付形式が不正など |
| バリデーションに失敗 | Laravelが自動的に返す |

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

### 2-3. 201と422の使い分け

| ステータスコード | 状況 | レスポンスボディ |
|----------------|------|----------------|
| 201 Created | タスクが作成された | 作成されたタスクのデータ（TaskResource） |
| 422 Unprocessable Entity | バリデーションエラー | エラーメッセージ |

---

## Step 3: テスト

### 3-1. Thunder Clientでテスト

#### 成功する場合

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

#### バリデーションエラーが発生する場合

- メソッド: `POST`
- URL: `http://localhost/api/tasks`
- Headers: `Content-Type: application/json`
- Body（JSON）:

```json
{
  "title": ""
}
```

- 期待: ステータスコード `422 Unprocessable Entity`

---

### 3-2. クライアント側での処理例（JavaScript）

```javascript
fetch('http://localhost/api/tasks', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  },
  body: JSON.stringify({
    title: '新しいタスク',
    description: 'これは新しいタスクです',
  }),
})
  .then(response => {
    if (response.status === 201) {
      return response.json();
    } else if (response.status === 422) {
      return response.json().then(data => {
        throw new Error(data.message);
      });
    }
  })
  .then(data => {
    console.log('作成されたタスク:', data);
  })
  .catch(error => {
    console.error('エラー:', error.message);
  });
```

---

## 🚨 よくある間違い

### 間違い1: 常に200を返す

**問題**: リソースを作成した場合は201を返すべき

```php
// ❌ 間違い
return (new TaskResource($task))->response()->setStatusCode(200);

// ✅ 正しい
return (new TaskResource($task))
    ->additional(['message' => 'タスクを作成しました'])
    ->response()
    ->setStatusCode(201);
```

---

### 間違い2: バリデーションを忘れる

**問題**: 不正なデータがデータベースに保存される

```php
// ❌ 間違い
$task = Task::create($request->all());

// ✅ 正しい
$validated = $request->validate([...]);
$task = Task::create($validated);
```

---

### 間違い3: TaskResourceを使わない

**問題**: レスポンス形式が統一されない

```php
// ❌ 間違い（response()->json()を直接使用）
return response()->json([
    'message' => 'タスクを作成しました',
    'data' => $task
], 201);

// ✅ 正しい（TaskResourceを使用）
return (new TaskResource($task))
    ->additional(['message' => 'タスクを作成しました'])
    ->response()
    ->setStatusCode(201);
```

---

## 💡 TIP: バリデーションエラーメッセージの日本語化

`resources/lang/ja/validation.php`を作成すると、エラーメッセージを日本語にできます。

```php
return [
    'required' => ':attributeは必須です。',
    'string' => ':attributeは文字列で入力してください。',
    'max' => [
        'string' => ':attributeは:max文字以内で入力してください。',
    ],
    'attributes' => [
        'title' => 'タイトル',
        'description' => '説明',
    ],
];
```

---

## ✨ まとめ

このセクションでは、タスクを作成するPOST APIを実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | storeメソッドの実装とTaskResourceの使い方 |
| Step 2 | 201 Createdと422 Unprocessable Entityの使い分け |
| Step 3 | Thunder Clientでのテスト方法 |

次のセクションでは、PUT APIの実装について学びます。

---
