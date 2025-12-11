# Tutorial 12-2-3: GET APIの実装（詳細取得）

## 🎯 このセクションで学ぶこと

*   タスク詳細を取得するGET APIを実装する方法を学ぶ。
*   HTTPステータスコード（200 OK、404 Not Found）を理解する。
*   なぜそのステータスコードを使うのかを学ぶ。
*   エラーハンドリングの方法を学ぶ。

---

## 導入：なぜHTTPステータスコードが重要なのか

APIでは、**HTTPステータスコード**を使って、**リクエストの結果を伝える**ことが重要です。

*   **200 OK**: リクエストが成功した
*   **404 Not Found**: リソースが見つからなかった

**適切なステータスコードを返す**ことで、クライアント側で適切な処理ができます。

---

## 詳細解説

### 🔍 タスク詳細を取得するAPI

タスク詳細を取得するAPIを実装します。

**エンドポイント**: `GET /api/tasks/{id}`

**レスポンス例（成功時）**:

```json
{
  "id": 1,
  "title": "Laravelを学ぶ",
  "description": "Tutorial 12を完了する",
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
public function show($id)
{
    $task = Task::find($id);
    
    if (!$task) {
        return response()->json([
            'message' => 'Task not found'
        ], 404);
    }
    
    return response()->json($task, 200);
}
```

**ポイント**:
*   `Task::find($id)`で、タスクを取得する
*   タスクが見つからない場合は、**404 Not Found**を返す
*   タスクが見つかった場合は、**200 OK**を返す

---

### 🔍 HTTPステータスコード: 200 OK

**200 OK**は、**リクエストが成功した**ことを示します。

**いつ使うか**:
*   リソースが正常に取得できた
*   処理が正常に完了した

**なぜ200を使うのか**:
*   クライアント側で「成功した」と判断できる
*   レスポンスボディにデータが含まれている

**例**:

```php
return response()->json($task, 200);
```

---

### 🔍 HTTPステータスコード: 404 Not Found

**404 Not Found**は、**リソースが見つからなかった**ことを示します。

**いつ使うか**:
*   指定されたIDのリソースが存在しない
*   URLが間違っている

**なぜ404を使うのか**:
*   クライアント側で「リソースが存在しない」と判断できる
*   ユーザーに適切なエラーメッセージを表示できる

**例**:

```php
return response()->json([
    'message' => 'Task not found'
], 404);
```

---

### 🔍 200と404の使い分け

| ステータスコード | 状況 | レスポンスボディ |
|----------------|------|----------------|
| **200 OK** | タスクが見つかった | タスクのデータ |
| **404 Not Found** | タスクが見つからなかった | エラーメッセージ |

---

### 🔍 実践演習: タスク詳細取得APIをテストしてください

Thunder Clientで、以下のリクエストを送信してください。

**1. タスクが見つかる場合**

*   メソッド: `GET`
*   URL: `http://localhost:8000/api/tasks/1`

**期待されるレスポンス**:

*   ステータスコード: `200 OK`
*   ボディ: タスクのデータ

---

**2. タスクが見つからない場合**

*   メソッド: `GET`
*   URL: `http://localhost:8000/api/tasks/9999`

**期待されるレスポンス**:

*   ステータスコード: `404 Not Found`
*   ボディ: `{"message": "Task not found"}`

---

### 🔍 findOrFailを使った実装

`findOrFail()`を使うと、タスクが見つからない場合に自動的に404エラーを返します。

```php
public function show($id)
{
    $task = Task::findOrFail($id);
    return response()->json($task, 200);
}
```

**ポイント**:
*   `findOrFail()`は、タスクが見つからない場合に`ModelNotFoundException`をスローする
*   Laravelが自動的に404エラーを返す

---

### 🔍 findOrFailのメリットとデメリット

**メリット**:
*   コードが簡潔になる
*   エラーハンドリングを書く必要がない

**デメリット**:
*   エラーメッセージをカスタマイズできない

---

### 🔍 カスタムエラーメッセージを返す

エラーメッセージをカスタマイズする場合は、`find()`を使います。

```php
public function show($id)
{
    $task = Task::find($id);
    
    if (!$task) {
        return response()->json([
            'message' => 'タスクが見つかりませんでした',
            'error' => 'TASK_NOT_FOUND'
        ], 404);
    }
    
    return response()->json($task, 200);
}
```

---

### 🔍 ステータスコードの重要性

**適切なステータスコードを返す**ことで、クライアント側で以下のことができます。

*   **成功・失敗を判断する**: 200なら成功、404なら失敗
*   **エラー処理を行う**: 404の場合は「タスクが見つかりません」と表示
*   **リトライを判断する**: 404の場合はリトライしない

---

### 🔍 クライアント側での処理例（JavaScript）

```javascript
fetch('http://localhost:8000/api/tasks/1')
  .then(response => {
    if (response.status === 200) {
      return response.json();
    } else if (response.status === 404) {
      throw new Error('タスクが見つかりません');
    }
  })
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error(error);
  });
```

---

### 💡 TIP: ステータスコードの定数を使う

ステータスコードは、定数を使うと分かりやすくなります。

```php
use Symfony\Component\HttpFoundation\Response;

return response()->json($task, Response::HTTP_OK);
return response()->json(['message' => 'Task not found'], Response::HTTP_NOT_FOUND);
```

---

### 🚨 よくある間違い

#### 間違い1: 常に200を返す

タスクが見つからない場合でも、200を返すのは間違いです。

```php
// ❌ 間違い
public function show($id)
{
    $task = Task::find($id);
    
    if (!$task) {
        return response()->json([
            'message' => 'Task not found'
        ], 200); // 200は間違い
    }
    
    return response()->json($task, 200);
}

// ✅ 正しい
public function show($id)
{
    $task = Task::find($id);
    
    if (!$task) {
        return response()->json([
            'message' => 'Task not found'
        ], 404); // 404が正しい
    }
    
    return response()->json($task, 200);
}
```

---

#### 間違い2: ステータスコードを省略する

ステータスコードを省略すると、デフォルトで200が返されます。

```php
// ❌ 間違い
return response()->json($task); // 200が返される

// ✅ 正しい
return response()->json($task, 200); // 明示的に200を指定
```

---

#### 間違い3: エラーメッセージを返さない

404エラーの場合は、エラーメッセージを返します。

```php
// ❌ 間違い
return response()->json([], 404);

// ✅ 正しい
return response()->json([
    'message' => 'Task not found'
], 404);
```

---

## ✨ まとめ

このセクションでは、タスク詳細を取得するGET APIを実装しました。

*   **200 OK**: タスクが見つかった場合に返す
*   **404 Not Found**: タスクが見つからなかった場合に返す
*   適切なステータスコードを返すことで、クライアント側で適切な処理ができる

次のセクションでは、POST APIの実装について学びます。

---

## 📝 学習のポイント

- [ ] タスク詳細を取得するAPIを実装した。
- [ ] 200 OKを理解した。
- [ ] 404 Not Foundを理解した。
- [ ] なぜそのステータスコードを使うのかを理解した。
- [ ] findOrFailを使った。
