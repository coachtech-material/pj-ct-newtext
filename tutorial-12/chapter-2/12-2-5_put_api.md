# Tutorial 12-2-5: PUT APIの実装（更新）

## 🎯 このセクションで学ぶこと

*   タスクを更新するPUT APIを実装する方法を学ぶ。
*   HTTPステータスコード（200 OK、404 Not Found、422 Unprocessable Entity）を理解する。
*   なぜそのステータスコードを使うのかを学ぶ。
*   PUTとPATCHの違いを理解する。

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

- **PUT**: リソース全体を置き換える
- **PATCH**: リソースの一部を更新する

Laravelでは、どちらも`update`メソッドで処理することが多いです。

---

### 理由3: 存在確認が必要

更新対象が存在しない場合、**404エラー**を返す必要があります。

Route Model Bindingを使えば、自動的に処理されます。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| 1 | updateメソッドの実装 | 更新のロジック |
| 2 | バリデーションの追加 | 不正なデータを弾く |
| 3 | 適切なレスポンス | 更新後のデータを返す |

> 💡 **ポイント**: PUTリクエストは「更新」に使います。

---

## 導入：なぜ200 OKを使うのか

リソースを更新した場合、**200 OK**を返すのが一般的です。

*   **200 OK**: リソースが更新された
*   **404 Not Found**: リソースが見つからなかった
*   **422 Unprocessable Entity**: バリデーションエラーが発生した

**適切なステータスコードを返す**ことで、クライアント側で適切な処理ができます。

---

## 詳細解説

### 🔍 タスクを更新するAPI

タスクを更新するAPIを実装します。

**エンドポイント**: `PUT /api/tasks/{id}`

**リクエストボディ**:

```json
{
  "title": "更新されたタスク",
  "description": "更新された説明",
  "status": "completed",
  "priority": 5
}
```

**レスポンス例（成功時）**:

```json
{
  "id": 1,
  "title": "更新されたタスク",
  "description": "更新された説明",
  "status": "completed",
  "priority": 5,
  "created_at": "2024-01-01T00:00:00.000000Z",
  "updated_at": "2024-01-02T00:00:00.000000Z"
}
```

---

### 🔍 コントローラーの実装

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function update(Request $request, $id)
{
    $task = Task::find($id);
    
    if (!$task) {
        return response()->json([
            'message' => 'Task not found'
        ], 404);
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
*   `Task::find($id)`で、タスクを取得する
*   タスクが見つからない場合は、**404 Not Found**を返す
*   `$request->validate()`で、バリデーションを行う
*   バリデーションエラーの場合は、自動的に**422 Unprocessable Entity**が返される
*   `$task->update()`で、タスクを更新する
*   **200 OK**を返す

---

### 🔍 HTTPステータスコード: 200 OK

**200 OK**は、**リクエストが成功した**ことを示します。

**いつ使うか**:
*   リソースが正常に更新された
*   処理が正常に完了した

**なぜ200を使うのか**:
*   クライアント側で「更新が成功した」と判断できる
*   更新されたリソースのデータを返す

**例**:

```php
return response()->json($task, 200);
```

---

### 🔍 HTTPステータスコード: 404 Not Found

**404 Not Found**は、**リソースが見つからなかった**ことを示します。

**いつ使うか**:
*   指定されたIDのリソースが存在しない

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

### 🔍 HTTPステータスコード: 422 Unprocessable Entity

**422 Unprocessable Entity**は、**リクエストは正しいが、内容が不正**であることを示します。

**いつ使うか**:
*   バリデーションエラーが発生した

**なぜ422を使うのか**:
*   クライアント側で「バリデーションエラーが発生した」と判断できる
*   エラーメッセージを表示できる

**例**:

```json
{
  "message": "The given data was invalid.",
  "errors": {
    "priority": [
      "The priority must be between 1 and 5."
    ]
  }
}
```

---

### 🔍 200、404、422の使い分け

| ステータスコード | 状況 | レスポンスボディ |
|----------------|------|----------------|
| **200 OK** | タスクが更新された | 更新されたタスクのデータ |
| **404 Not Found** | タスクが見つからなかった | エラーメッセージ |
| **422 Unprocessable Entity** | バリデーションエラー | エラーメッセージ |

---

### 🔍 実践演習: タスク更新APIをテストしてください

Thunder Clientで、以下のリクエストを送信してください。

**1. 成功する場合**

*   メソッド: `PUT`
*   URL: `http://localhost:8000/api/tasks/1`
*   Body（JSON）:

```json
{
  "title": "更新されたタスク",
  "description": "更新された説明",
  "status": "completed",
  "priority": 5
}
```

**期待されるレスポンス**:

*   ステータスコード: `200 OK`
*   ボディ: 更新されたタスクのデータ

---

**2. タスクが見つからない場合**

*   メソッド: `PUT`
*   URL: `http://localhost:8000/api/tasks/9999`
*   Body（JSON）:

```json
{
  "title": "更新されたタスク",
  "description": "更新された説明",
  "status": "completed",
  "priority": 5
}
```

**期待されるレスポンス**:

*   ステータスコード: `404 Not Found`
*   ボディ: `{"message": "Task not found"}`

---

**3. バリデーションエラーが発生する場合**

*   メソッド: `PUT`
*   URL: `http://localhost:8000/api/tasks/1`
*   Body（JSON）:

```json
{
  "title": "",
  "description": "更新された説明",
  "status": "completed",
  "priority": 10
}
```

**期待されるレスポンス**:

*   ステータスコード: `422 Unprocessable Entity`
*   ボディ: エラーメッセージ

---

### 🔍 PUTとPATCHの違い

**PUT**と**PATCH**は、どちらもリソースを更新するHTTPメソッドですが、違いがあります。

| HTTPメソッド | 用途 | 特徴 |
|-------------|------|------|
| **PUT** | リソース全体を更新 | すべてのフィールドを送信する |
| **PATCH** | リソースの一部を更新 | 更新するフィールドだけを送信する |

---

### 🔍 PUTの実装例

**すべてのフィールドを送信する**:

```json
{
  "title": "更新されたタスク",
  "description": "更新された説明",
  "status": "completed",
  "priority": 5
}
```

---

### 🔍 PATCHの実装例

**更新するフィールドだけを送信する**:

```json
{
  "status": "completed"
}
```

**コントローラー**:

```php
public function update(Request $request, $id)
{
    $task = Task::findOrFail($id);
    
    $validated = $request->validate([
        'title' => 'sometimes|required|max:255',
        'description' => 'nullable',
        'status' => 'sometimes|required|in:pending,in_progress,completed',
        'priority' => 'sometimes|required|integer|min:1|max:5',
    ]);
    
    $task->update($validated);
    
    return response()->json($task, 200);
}
```

**ポイント**:
*   `sometimes`を使うと、フィールドが存在する場合だけバリデーションを行う

---

### 🔍 ステータスコードの重要性

**適切なステータスコードを返す**ことで、クライアント側で以下のことができます。

*   **成功・失敗を判断する**: 200なら更新成功、404ならリソースが存在しない、422ならバリデーションエラー
*   **エラー処理を行う**: 404の場合は「タスクが見つかりません」と表示、422の場合はエラーメッセージを表示
*   **リトライを判断する**: 404の場合はリトライしない、422の場合はユーザーに修正を促す

---

### 💡 TIP: findOrFailを使う

`findOrFail()`を使うと、コードが簡潔になります。

```php
public function update(Request $request, $id)
{
    $task = Task::findOrFail($id);
    
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

---

### 🚨 よくある間違い

#### 間違い1: 常に200を返す

タスクが見つからない場合は、**404 Not Found**を返します。

```php
// ❌ 間違い
public function update(Request $request, $id)
{
    $task = Task::find($id);
    
    if (!$task) {
        return response()->json([
            'message' => 'Task not found'
        ], 200); // 200は間違い
    }
    
    // ...
}

// ✅ 正しい
public function update(Request $request, $id)
{
    $task = Task::find($id);
    
    if (!$task) {
        return response()->json([
            'message' => 'Task not found'
        ], 404); // 404が正しい
    }
    
    // ...
}
```

---

#### 間違い2: バリデーションを忘れる

更新する場合も、バリデーションを行います。

```php
// ❌ 間違い
$task->update($request->all());

// ✅ 正しい
$validated = $request->validate([...]);
$task->update($validated);
```

---

#### 間違い3: ステータスコードを省略する

ステータスコードを省略すると、デフォルトで200が返されます。

```php
// ❌ 間違い（明示的でない）
return response()->json($task);

// ✅ 正しい（明示的）
return response()->json($task, 200);
```

---

## ✨ まとめ

このセクションでは、タスクを更新するPUT APIを実装しました。

*   **200 OK**: タスクが更新された場合に返す
*   **404 Not Found**: タスクが見つからなかった場合に返す
*   **422 Unprocessable Entity**: バリデーションエラーの場合に返す
*   PUTとPATCHの違いを理解した

次のセクションでは、DELETE APIの実装について学びます。

---

## 📝 学習のポイント

- [ ] タスクを更新するAPIを実装した。
- [ ] 200 OKを理解した。
- [ ] 404 Not Foundを理解した。
- [ ] 422 Unprocessable Entityを理解した。
- [ ] PUTとPATCHの違いを理解した。
