# Tutorial 11-2-7: エラーレスポンスの設計

## 🎯 このセクションで学ぶこと

- APIにおけるエラーレスポンスの重要性を理解する
- 一貫性のあるエラーレスポンスの設計方法を学ぶ
- HTTPステータスコードの適切な使い分けを学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜCRUD実装の後に『エラーレスポンス』を学ぶのか？」

CRUD APIが完成したら、次は「エラーレスポンスの設計」です。

---

### 理由1: クライアントがエラーを処理できるようにする

APIがエラーを返す場合、クライアント（フロントエンド）がそのエラーを処理できる必要があります。

| 問題 | 説明 |
|------|------|
| エラーの種類がわからない | 何が問題なのか判断できない |
| エラーメッセージがない | ユーザーに何を伝えればいいかわからない |
| 形式がバラバラ | 処理が複雑になる |

---

### 理由2: 一貫性のあるレスポンス

すべてのエラーレスポンスを**同じ形式**で返すと、クライアント側の処理が簡単になります。

```json
{
  "message": "タスクが見つかりません",
  "error_code": "TASK_NOT_FOUND"
}
```

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | エラーレスポンスの設計 | 形式を決める |
| Step 2 | コントローラーでの実装 | 各メソッドでエラーを返す |
| Step 3 | テスト | 正常系と異常系を確認 |

> 💡 **ポイント**: エラーレスポンスは「クライアントへのメッセージ」です。

---

## Step 1: エラーレスポンスの設計

### 1-1. エラーレスポンスの形式

すべてのエラーレスポンスを以下の形式で統一します。

```json
{
  "message": "エラーメッセージ",
  "error_code": "ERROR_CODE"
}
```

| フィールド | 説明 |
|-----------|------|
| `message` | 人間が読めるエラーメッセージ |
| `error_code` | プログラムで判定できるエラーコード |

---

### 1-2. エラーコードの一覧

| エラーコード | ステータスコード | 説明 |
|-------------|----------------|------|
| `TASK_NOT_FOUND` | 404 | タスクが見つからない |
| `VALIDATION_ERROR` | 422 | バリデーションエラー |
| `SERVER_ERROR` | 500 | サーバーエラー |

---

### 1-3. なぜエラーコードが必要か

**メッセージだけでは不十分**な理由:

| 問題 | 説明 |
|------|------|
| メッセージは変わる可能性がある | 「タスクが見つかりません」→「Task not found」 |
| 多言語対応が難しい | 日本語と英語で異なるメッセージ |
| プログラムで判定しにくい | 文字列の比較は不安定 |

**エラーコードがあると**:

```javascript
if (data.error_code === 'TASK_NOT_FOUND') {
  // タスクが見つからない場合の処理
}
```

---

## Step 2: コントローラーでの実装

### 2-1. 404エラーの実装

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function show(string $id)
{
    $task = Task::where('user_id', 1)->find($id);

    if (!$task) {
        return response()->json([
            'message' => 'タスクが見つかりません',
            'error_code' => 'TASK_NOT_FOUND'
        ], 404);
    }

    return response()->json(['data' => $task], 200);
}
```

---

### 2-2. コードリーディング

#### `if (!$task)`

```php
if (!$task) {
    return response()->json([
        'message' => 'タスクが見つかりません',
        'error_code' => 'TASK_NOT_FOUND'
    ], 404);
}
```

| 部分 | 説明 |
|------|------|
| `!$task` | `$task`がnull（falsy）の場合 |
| `'message' => '...'` | 人間が読めるメッセージ |
| `'error_code' => '...'` | プログラムで判定できるコード |
| `404` | HTTPステータスコード（Not Found） |

---

### 2-3. 全メソッドでの統一

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    public function index()
    {
        $tasks = Task::where('user_id', 1)->get();

        return response()->json(['data' => $tasks], 200);
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'due_date' => 'nullable|date',
        ]);

        $data = array_merge($validated, [
            'user_id' => 1,
            'status' => 'pending',
        ]);
        
        $task = Task::create($data);

        return response()->json([
            'message' => 'タスクを作成しました',
            'data' => $task
        ], 201);
    }

    public function show(string $id)
    {
        $task = Task::where('user_id', 1)->find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません',
                'error_code' => 'TASK_NOT_FOUND'
            ], 404);
        }

        return response()->json(['data' => $task], 200);
    }

    public function update(Request $request, string $id)
    {
        $task = Task::where('user_id', 1)->find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません',
                'error_code' => 'TASK_NOT_FOUND'
            ], 404);
        }

        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'status' => 'required|in:pending,in_progress,completed',
            'due_date' => 'nullable|date',
        ]);

        $task->update($validated);

        return response()->json([
            'message' => 'タスクを更新しました',
            'data' => $task
        ], 200);
    }

    public function destroy(string $id)
    {
        $task = Task::where('user_id', 1)->find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません',
                'error_code' => 'TASK_NOT_FOUND'
            ], 404);
        }

        $task->delete();

        return response()->json(null, 204);
    }
}
```

---

### 2-4. バリデーションエラーのレスポンス

Laravelの`$request->validate()`は、バリデーションエラー時に自動的に422レスポンスを返します。

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

## Step 3: テスト

### 3-1. Thunder Clientでテスト

**1. タスクが見つからない場合（404）**

- メソッド: `GET`
- URL: `http://localhost/api/tasks/9999`
- 期待: ステータスコード `404 Not Found`

**レスポンス例**:

```json
{
  "message": "タスクが見つかりません",
  "error_code": "TASK_NOT_FOUND"
}
```

---

**2. バリデーションエラーの場合（422）**

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
fetch('http://localhost/api/tasks/9999', {
  headers: {
    'Accept': 'application/json',
  },
})
  .then(response => {
    if (!response.ok) {
      return response.json().then(data => {
        // エラーコードで判定
        if (data.error_code === 'TASK_NOT_FOUND') {
          throw new Error('タスクが見つかりません');
        }
        throw new Error(data.message);
      });
    }
    return response.json();
  })
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error('エラー:', error.message);
  });
```

---

## 🚨 よくある間違い

### 間違い1: エラーメッセージを返さない

**問題**: クライアントがエラーの内容を判断できない

```php
// ❌ 間違い
return response()->json([], 404);

// ✅ 正しい
return response()->json([
    'message' => 'タスクが見つかりません',
    'error_code' => 'TASK_NOT_FOUND'
], 404);
```

---

### 間違い2: 常に200を返す

**問題**: クライアントがエラーかどうか判断できない

```php
// ❌ 間違い
return response()->json([
    'success' => false,
    'message' => 'Task not found'
], 200);

// ✅ 正しい
return response()->json([
    'message' => 'タスクが見つかりません',
    'error_code' => 'TASK_NOT_FOUND'
], 404);
```

---

### 間違い3: エラーコードが統一されていない

**問題**: クライアント側での処理が複雑になる

```php
// ❌ 間違い（バラバラ）
'error_code' => 'NOT_FOUND'
'error_code' => 'task_not_found'
'error_code' => 'TaskNotFound'

// ✅ 正しい（統一）
'error_code' => 'TASK_NOT_FOUND'
```

---

## 💡 TIP: HTTPステータスコードの一覧

| コード | 名前 | 説明 |
|--------|------|------|
| 200 | OK | リクエスト成功 |
| 201 | Created | リソース作成成功 |
| 204 | No Content | 成功（レスポンスボディなし） |
| 400 | Bad Request | リクエストが不正 |
| 401 | Unauthorized | 認証が必要 |
| 403 | Forbidden | アクセス権限がない |
| 404 | Not Found | リソースが見つからない |
| 422 | Unprocessable Entity | バリデーションエラー |
| 500 | Internal Server Error | サーバーエラー |

---

## ✨ まとめ

このセクションでは、エラーレスポンスの設計を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | エラーレスポンスの形式とエラーコード |
| Step 2 | コントローラーでの統一的な実装 |
| Step 3 | Thunder Clientでのテスト方法 |

**エラーレスポンスのポイント**:

1. **一貫性のある形式**を使う
2. **適切なHTTPステータスコード**を返す
3. **エラーコード**でプログラムが判定できるようにする

---
