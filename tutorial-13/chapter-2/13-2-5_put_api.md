# Tutorial 13-2-5: PUT APIの実装（更新）

## 🎯 このセクションで学ぶこと

- タスクを更新するPUT APIを実装する方法を学ぶ
- HTTPステータスコード（200 OK、404 Not Found、422 Unprocessable Entity）を理解する
- なぜそのステータスコードを使うのかを学ぶ
- PUTとPATCHの違いを理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ作成APIの後に『更新API』を実装するのか？」

作成APIができたら、次は「更新API」です。

---

### 理由1: 既存データの変更

作成は「新規追加」でしたが、更新は**「既存データの変更」**です。

IDで特定したレコードを更新します。

---

### 理由2: PUTとPATCHの違い

| メソッド | 用途 |
|----------|------|
| PUT | リソース全体を置き換える |
| PATCH | リソースの一部を更新する |

Laravelでは、どちらも`update`メソッドで処理することが多いです。

---

### 理由3: 存在確認が必要

更新対象が存在しない場合、**404エラー**を返す必要があります。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | updateメソッドの実装 | 更新のロジック |
| Step 2 | HTTPステータスコード | 200、404、422の使い分け |
| Step 3 | PUTとPATCHの違い | 部分更新の実装 |

> 💡 **ポイント**: PUTリクエストは「更新」に使います。

---

## Step 1: updateメソッドの実装

### 1-1. タスクを更新するAPI

**エンドポイント**: `PUT /api/tasks/{id}`

**リクエストボディ**:

```json
{
  "title": "更新されたタスク",
  "description": "更新された説明",
  "status": "completed"
}
```

**レスポンス例（成功時）**:

```json
{
  "message": "タスクを更新しました",
  "data": {
    "id": 1,
    "title": "更新されたタスク",
    "description": "更新された説明",
    "status": "completed",
    "created_at": "2024-01-01 00:00:00",
    "updated_at": "2024-01-02 00:00:00"
  }
}
```

---

### 1-2. コントローラーの実装

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
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

    // レスポンスを返す
    return response()->json([
        'message' => 'タスクを更新しました',
        'data' => $task
    ], 200);
}
```

---

### 1-3. コードリーディング

#### `public function update(Request $request, string $id)`

```php
public function update(Request $request, string $id)
```

| 部分 | 説明 |
|------|------|
| `Request $request` | リクエストオブジェクト（リクエストボディを含む） |
| `string $id` | URLパラメータ（`/api/tasks/{id}`の`{id}`部分） |

---

#### `Task::where('user_id', 1)->find($id)`

```php
$task = Task::where('user_id', 1)->find($id);
```

| 部分 | 説明 |
|------|------|
| `Task::where('user_id', 1)` | user_idが1のレコードに絞り込む |
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

#### `$task->update($validated)`

```php
$task->update($validated);
```

| 部分 | 説明 |
|------|------|
| `$task->update(...)` | タスクを更新してデータベースに保存 |
| `$validated` | バリデーション済みのデータ |

---

## Step 2: HTTPステータスコード

### 2-1. 200 OK

**200 OK**は、**リクエストが成功した**ことを示します。

| 使用場面 | 説明 |
|----------|------|
| リソースが正常に更新された | タスクが更新された |
| 処理が正常に完了した | 更新されたリソースのデータを返す |

```php
return response()->json(['data' => $task], 200);
```

---

### 2-2. 404 Not Found

**404 Not Found**は、**リソースが見つからなかった**ことを示します。

```php
return response()->json([
    'message' => 'タスクが見つかりません'
], 404);
```

---

### 2-3. 422 Unprocessable Entity

**422 Unprocessable Entity**は、**バリデーションエラー**を示します。

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

### 2-4. 200、404、422の使い分け

| ステータスコード | 状況 | レスポンスボディ |
|----------------|------|----------------|
| 200 OK | タスクが更新された | 更新されたタスクのデータ |
| 404 Not Found | タスクが見つからなかった | エラーメッセージ |
| 422 Unprocessable Entity | バリデーションエラー | エラーメッセージ |

---

## Step 3: PUTとPATCHの違い

### 3-1. PUTとPATCHの比較

| HTTPメソッド | 用途 | 特徴 |
|-------------|------|------|
| PUT | リソース全体を更新 | すべてのフィールドを送信する |
| PATCH | リソースの一部を更新 | 更新するフィールドだけを送信する |

---

### 3-2. PUTの実装例

**すべてのフィールドを送信する**:

```json
{
  "title": "更新されたタスク",
  "description": "更新された説明",
  "status": "completed"
}
```

---

### 3-3. PATCHの実装例

**更新するフィールドだけを送信する**:

```json
{
  "status": "completed"
}
```

**コントローラー**:

```php
public function update(Request $request, string $id)
{
    $task = Task::where('user_id', 1)->find($id);

    if (!$task) {
        return response()->json([
            'message' => 'タスクが見つかりません'
        ], 404);
    }

    $validated = $request->validate([
        'title' => 'sometimes|required|string|max:255',
        'description' => 'nullable|string',
        'status' => 'sometimes|required|in:pending,in_progress,completed',
        'due_date' => 'nullable|date',
    ]);

    $task->update($validated);

    return response()->json([
        'message' => 'タスクを更新しました',
        'data' => $task
    ], 200);
}
```

> 💡 **ポイント**: `sometimes`を使うと、フィールドが存在する場合だけバリデーションを行います。

---

### 3-4. Thunder Clientでテスト

**1. 成功する場合**

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

**2. タスクが見つからない場合**

- メソッド: `PUT`
- URL: `http://localhost/api/tasks/9999`
- Headers: `Content-Type: application/json`
- Body（JSON）:

```json
{
  "title": "更新されたタスク",
  "status": "completed"
}
```

- 期待: ステータスコード `404 Not Found`

**3. バリデーションエラーが発生する場合**

- メソッド: `PUT`
- URL: `http://localhost/api/tasks/1`
- Headers: `Content-Type: application/json`
- Body（JSON）:

```json
{
  "title": "",
  "status": "invalid"
}
```

- 期待: ステータスコード `422 Unprocessable Entity`

---

## 🚨 よくある間違い

### 間違い1: 常に200を返す

**問題**: タスクが見つからない場合は404を返すべき

```php
// ❌ 間違い
if (!$task) {
    return response()->json(['message' => 'Task not found'], 200);
}

// ✅ 正しい
if (!$task) {
    return response()->json(['message' => 'Task not found'], 404);
}
```

---

### 間違い2: バリデーションを忘れる

**問題**: 不正なデータがデータベースに保存される

```php
// ❌ 間違い
$task->update($request->all());

// ✅ 正しい
$validated = $request->validate([...]);
$task->update($validated);
```

---

### 間違い3: ステータスコードを省略する

**問題**: 明示的でないコード

```php
// ❌ 間違い
return response()->json($task);

// ✅ 正しい
return response()->json($task, 200);
```

---

## 💡 TIP: findOrFailを使う

`findOrFail()`を使うと、コードが簡潔になります。

```php
public function update(Request $request, string $id)
{
    $task = Task::where('user_id', 1)->findOrFail($id);

    $validated = $request->validate([...]);
    $task->update($validated);

    return response()->json(['data' => $task], 200);
}
```

> 📌 **注意**: `findOrFail()`を使う場合、404エラーのレスポンス形式はLaravelのデフォルト形式になります。

---

## ✨ まとめ

このセクションでは、タスクを更新するPUT APIを実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | updateメソッドの実装とバリデーション |
| Step 2 | 200 OK、404 Not Found、422 Unprocessable Entityの使い分け |
| Step 3 | PUTとPATCHの違いとsometimesルール |

次のセクションでは、DELETE APIの実装について学びます。

---
