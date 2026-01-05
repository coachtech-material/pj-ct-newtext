# Tutorial 12-2-3: GET APIの実装（詳細取得）

## 🎯 このセクションで学ぶこと

- タスク詳細を取得するGET APIを実装する方法を学ぶ
- HTTPステータスコード（200 OK、404 Not Found）を理解する
- なぜそのステータスコードを使うのかを学ぶ
- エラーハンドリングの方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜAPI Resourcesの後に『詳細取得API』を実装するのか？」

API Resourcesを学んだら、次は「詳細取得API」です。

---

### 理由1: 最もシンプルなAPI

詳細取得（GET /api/tasks/{id}）は、**最もシンプルなAPI**です。

| 特徴 | 説明 |
|------|------|
| データを取得して返すだけ | 処理がシンプル |
| バリデーションが不要 | 入力データがない |
| 副作用がない | データを変更しない |

---

### 理由2: エラーハンドリングの基礎

存在しないIDを指定された場合、**404エラー**を返す必要があります。

この「存在チェック → エラーレスポンス」のパターンは、他のAPIでも使います。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | showメソッドの実装 | 詳細取得のロジック |
| Step 2 | HTTPステータスコード | 200と404の使い分け |
| Step 3 | テストと改善 | 正常系と異常系を確認 |

> 💡 **ポイント**: GETリクエストは「読み取り専用」です。データを変更しません。

---

## Step 1: showメソッドの実装

### 1-1. タスク詳細を取得するAPI

**エンドポイント**: `GET /api/tasks/{id}`

**レスポンス例（成功時）**:

```json
{
  "data": {
    "id": 1,
    "title": "Laravelを学ぶ",
    "description": "Tutorial 12を完了する",
    "status": "pending",
    "due_date": "2024-12-31",
    "created_at": "2024-01-01 00:00:00",
    "updated_at": "2024-01-01 00:00:00"
  }
}
```

---

### 1-2. コントローラーの実装

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
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

    // タスクを返す
    return response()->json([
        'data' => $task
    ], 200);
}
```

---

### 1-3. コードリーディング

#### `public function show(string $id)`

```php
public function show(string $id)
```

| 部分 | 説明 |
|------|------|
| `public function` | 公開メソッド |
| `show` | メソッド名（詳細取得を表す慣例的な名前） |
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

#### `response()->json([...], 200)`

```php
return response()->json([
    'data' => $task
], 200);
```

| 部分 | 説明 |
|------|------|
| `response()->json([...])` | 配列をJSON形式に変換 |
| `'data' => $task` | `data`キーにタスクを格納 |
| `, 200` | HTTPステータスコード（200 OK） |

---

## Step 2: HTTPステータスコード

### 2-1. 200 OK

**200 OK**は、**リクエストが成功した**ことを示します。

| 使用場面 | 説明 |
|----------|------|
| リソースが正常に取得できた | タスクが見つかった |
| 処理が正常に完了した | レスポンスボディにデータが含まれる |

```php
return response()->json(['data' => $task], 200);
```

---

### 2-2. 404 Not Found

**404 Not Found**は、**リソースが見つからなかった**ことを示します。

| 使用場面 | 説明 |
|----------|------|
| 指定されたIDのリソースが存在しない | タスクが見つからない |
| URLが間違っている | 存在しないエンドポイント |

```php
return response()->json([
    'message' => 'タスクが見つかりません'
], 404);
```

---

### 2-3. 200と404の使い分け

| ステータスコード | 状況 | レスポンスボディ |
|----------------|------|----------------|
| 200 OK | タスクが見つかった | タスクのデータ |
| 404 Not Found | タスクが見つからなかった | エラーメッセージ |

---

## Step 3: テストと改善

### 3-1. Thunder Clientでテスト

**1. タスクが見つかる場合**

- メソッド: `GET`
- URL: `http://localhost/api/tasks/1`
- 期待: ステータスコード `200 OK`

**2. タスクが見つからない場合**

- メソッド: `GET`
- URL: `http://localhost/api/tasks/9999`
- 期待: ステータスコード `404 Not Found`

---

### 3-2. findOrFailを使った実装

`findOrFail()`を使うと、タスクが見つからない場合に自動的に例外を投げます。

```php
public function show(string $id)
{
    $task = Task::where('user_id', 1)->findOrFail($id);

    return response()->json(['data' => $task], 200);
}
```

| メリット | デメリット |
|----------|------------|
| コードが簡潔になる | エラーメッセージをカスタマイズしにくい |
| エラーハンドリングを書く必要がない | |

> 📌 **注意**: `findOrFail()`を使う場合、404エラーのレスポンス形式はLaravelのデフォルト形式になります。カスタムメッセージを返したい場合は、`find()`を使って自分でエラーハンドリングを書きます。

---

### 3-3. カスタムエラーメッセージを返す

```php
public function show(string $id)
{
    $task = Task::where('user_id', 1)->find($id);

    if (!$task) {
        return response()->json([
            'message' => 'タスクが見つかりませんでした',
            'error' => 'TASK_NOT_FOUND'
        ], 404);
    }

    return response()->json(['data' => $task], 200);
}
```

---

### 3-4. クライアント側での処理例（JavaScript）

```javascript
fetch('http://localhost/api/tasks/1', {
  headers: {
    'Accept': 'application/json',
  },
})
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

## 🚨 よくある間違い

### 間違い1: 常に200を返す

**問題**: タスクが見つからない場合でも200を返す

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

### 間違い2: ステータスコードを省略する

**問題**: デフォルトで200が返される

```php
// ❌ 間違い
return response()->json($task);

// ✅ 正しい
return response()->json($task, 200);
```

---

### 間違い3: エラーメッセージを返さない

**問題**: クライアントがエラーの内容を判断できない

```php
// ❌ 間違い
return response()->json([], 404);

// ✅ 正しい
return response()->json(['message' => 'Task not found'], 404);
```

---

## 💡 TIP: ステータスコードの定数を使う

```php
use Symfony\Component\HttpFoundation\Response;

return response()->json($task, Response::HTTP_OK);
return response()->json(['message' => 'Task not found'], Response::HTTP_NOT_FOUND);
```

---

## ✨ まとめ

このセクションでは、タスク詳細を取得するGET APIを実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | showメソッドの実装とfind()の使い方 |
| Step 2 | 200 OKと404 Not Foundの使い分け |
| Step 3 | findOrFail()とカスタムエラーメッセージ |

次のセクションでは、POST APIの実装について学びます。

---
