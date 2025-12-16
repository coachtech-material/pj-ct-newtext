# Tutorial 12-2-7: 親切なエラーレスポンスの作成

## 🎯 このセクションで学ぶこと

*   親切なエラーレスポンスとは何かを理解する。
*   単に500エラーを返すのではなく、クライアントが使いやすいエラー形式を定義する方法を学ぶ。
*   404 Not Found時にJSONで`{ "message": "User not found" }`を返す設定を学ぶ。
*   エラーハンドリングのベストプラクティスを理解する。

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜCRUD実装の後に『エラーレスポンス』を整備するのか？」

CRUD APIが完成したら、次は「エラーレスポンス」です。

---

### 理由1: 正常系だけでは不十分

これまでは主に「正常系」を実装してきました。

しかし、実際のAPIでは**エラーが発生する**ことがあります。

- バリデーションエラー
- 認証エラー
- 存在しないリソース
- サーバーエラー

---

### 理由2: 一貫したエラー形式

エラーレスポンスも、**一貫した形式**であるべきです。

```json
{
    "error": {
        "code": "VALIDATION_ERROR",
        "message": "入力内容に誤りがあります",
        "details": {
            "title": ["タイトルは必須です"]
        }
    }
}
```

---

### 理由3: フロントエンドでの処理

フロントエンドは、**エラーレスポンスを解析**してユーザーに表示します。

一貫した形式なら、エラー処理のコードを共通化できます。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| 1 | エラーレスポンスの設計 | 統一フォーマットを決める |
| 2 | 例外ハンドラーのカスタマイズ | `Handler.php`の編集 |
| 3 | 各種エラーのテスト | バリデーション、404など |

> 💡 **ポイント**: 良いAPIは、エラー時にも適切な情報を返します。

---

## 導入：なぜ親切なエラーレスポンスが重要なのか

**エラーレスポンス**は、**クライアント側でエラー処理を行うために重要**です。

**悪い例**:

```
Internal Server Error
```

**良い例**:

```json
{
  "message": "Task not found",
  "error": "TASK_NOT_FOUND",
  "status": 404
}
```

**親切なエラーレスポンス**を返すことで、クライアント側で適切なエラー処理ができます。

---

## 詳細解説

### 🔍 エラーレスポンスの基本形式

エラーレスポンスは、以下の形式で返すのが一般的です。

```json
{
  "message": "エラーメッセージ",
  "error": "エラーコード",
  "status": HTTPステータスコード
}
```

**例**:

```json
{
  "message": "Task not found",
  "error": "TASK_NOT_FOUND",
  "status": 404
}
```

---

### 🔍 404 Not Foundのエラーレスポンス

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function show($id)
{
    $task = Task::find($id);
    
    if (!$task) {
        return response()->json([
            'message' => 'Task not found',
            'error' => 'TASK_NOT_FOUND',
            'status' => 404
        ], 404);
    }
    
    return response()->json($task, 200);
}
```

---

### 🔍 バリデーションエラーのレスポンス

Laravelでは、バリデーションエラーが発生すると、以下の形式でレスポンスが返されます。

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

**ポイント**:
*   `message`: エラーの概要
*   `errors`: フィールドごとのエラーメッセージ

---

### 🔍 500 Internal Server Errorのエラーレスポンス

**500 Internal Server Error**は、**サーバー側のエラー**を示します。

**悪い例**:

```
Internal Server Error
```

**良い例**:

```json
{
  "message": "An error occurred while processing your request",
  "error": "INTERNAL_SERVER_ERROR",
  "status": 500
}
```

---

### 🔍 例外ハンドラーをカスタマイズする

Laravelでは、例外ハンドラーをカスタマイズして、エラーレスポンスを統一できます。

**ファイル**: `app/Exceptions/Handler.php`

```php
<?php

namespace App\Exceptions;

use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;
use Illuminate\Database\Eloquent\ModelNotFoundException;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use Throwable;

class Handler extends ExceptionHandler
{
    public function register()
    {
        $this->renderable(function (ModelNotFoundException $e, $request) {
            if ($request->is('api/*')) {
                return response()->json([
                    'message' => 'Resource not found',
                    'error' => 'RESOURCE_NOT_FOUND',
                    'status' => 404
                ], 404);
            }
        });
        
        $this->renderable(function (NotFoundHttpException $e, $request) {
            if ($request->is('api/*')) {
                return response()->json([
                    'message' => 'Endpoint not found',
                    'error' => 'ENDPOINT_NOT_FOUND',
                    'status' => 404
                ], 404);
            }
        });
    }
}
```

**ポイント**:
*   `ModelNotFoundException`: モデルが見つからない場合
*   `NotFoundHttpException`: エンドポイントが見つからない場合
*   `$request->is('api/*')`: APIリクエストの場合だけ適用

---

### 🔍 実践演習: エラーレスポンスをテストしてください

Thunder Clientで、以下のリクエストを送信してください。

**1. リソースが見つからない場合**

*   メソッド: `GET`
*   URL: `http://localhost:8000/api/tasks/9999`

**期待されるレスポンス**:

```json
{
  "message": "Resource not found",
  "error": "RESOURCE_NOT_FOUND",
  "status": 404
}
```

---

**2. エンドポイントが見つからない場合**

*   メソッド: `GET`
*   URL: `http://localhost:8000/api/invalid-endpoint`

**期待されるレスポンス**:

```json
{
  "message": "Endpoint not found",
  "error": "ENDPOINT_NOT_FOUND",
  "status": 404
}
```

---

### 🔍 エラーコードの一覧

エラーコードを定義しておくと、クライアント側で処理しやすくなります。

| エラーコード | HTTPステータス | 説明 |
|------------|--------------|------|
| `TASK_NOT_FOUND` | 404 | タスクが見つからない |
| `USER_NOT_FOUND` | 404 | ユーザーが見つからない |
| `VALIDATION_ERROR` | 422 | バリデーションエラー |
| `UNAUTHORIZED` | 401 | 認証エラー |
| `FORBIDDEN` | 403 | 権限エラー |
| `INTERNAL_SERVER_ERROR` | 500 | サーバーエラー |

---

### 🔍 エラーレスポンスのベストプラクティス

**1. 一貫性を保つ**

すべてのエラーレスポンスで、同じ形式を使います。

```json
{
  "message": "エラーメッセージ",
  "error": "エラーコード",
  "status": HTTPステータスコード
}
```

---

**2. 詳細なエラーメッセージを返す**

ユーザーが理解しやすいエラーメッセージを返します。

```json
{
  "message": "タスクが見つかりませんでした",
  "error": "TASK_NOT_FOUND",
  "status": 404
}
```

---

**3. エラーコードを使う**

エラーコードを使うと、クライアント側で処理しやすくなります。

```json
{
  "message": "Task not found",
  "error": "TASK_NOT_FOUND",
  "status": 404
}
```

---

**4. 本番環境では詳細なエラーを隠す**

本番環境では、詳細なエラーメッセージを隠します。

```json
{
  "message": "An error occurred while processing your request",
  "error": "INTERNAL_SERVER_ERROR",
  "status": 500
}
```

---

### 🔍 クライアント側での処理例（JavaScript）

```javascript
fetch('http://localhost:8000/api/tasks/9999')
  .then(response => {
    if (!response.ok) {
      return response.json().then(data => {
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

### 💡 TIP: デバッグモードを切り替える

開発環境では、詳細なエラーメッセージを表示し、本番環境では隠します。

**ファイル**: `.env`

```
APP_DEBUG=true  # 開発環境
APP_DEBUG=false # 本番環境
```

---

### 🚨 よくある間違い

#### 間違い1: エラーメッセージを返さない

エラーが発生した場合は、エラーメッセージを返します。

```php
// ❌ 間違い
return response()->json([], 404);

// ✅ 正しい
return response()->json([
    'message' => 'Task not found',
    'error' => 'TASK_NOT_FOUND',
    'status' => 404
], 404);
```

---

#### 間違い2: 500エラーをそのまま返す

500エラーの場合は、親切なエラーメッセージを返します。

```php
// ❌ 間違い
throw new Exception('Database error');

// ✅ 正しい
return response()->json([
    'message' => 'An error occurred while processing your request',
    'error' => 'INTERNAL_SERVER_ERROR',
    'status' => 500
], 500);
```

---

#### 間違い3: 本番環境で詳細なエラーを返す

本番環境では、詳細なエラーメッセージを隠します。

```php
// ❌ 間違い（本番環境）
return response()->json([
    'message' => 'SQLSTATE[42S02]: Base table or view not found',
    'error' => 'DATABASE_ERROR',
    'status' => 500
], 500);

// ✅ 正しい（本番環境）
return response()->json([
    'message' => 'An error occurred while processing your request',
    'error' => 'INTERNAL_SERVER_ERROR',
    'status' => 500
], 500);
```

---

## ✨ まとめ

このセクションでは、親切なエラーレスポンスの作成を学びました。

*   単に500エラーを返すのではなく、クライアントが使いやすいエラー形式を定義した。
*   404 Not Found時にJSONで`{ "message": "Task not found" }`を返す設定を学んだ。
*   エラーハンドリングのベストプラクティスを理解した。

これで、Chapter 2（RESTful APIの実装）は完了です。次のChapter 3では、API認証とセキュリティについて学びます。

---

## 📝 学習のポイント

- [ ] 親切なエラーレスポンスを作成した。
- [ ] 404 Not Foundのエラーレスポンスを返した。
- [ ] 例外ハンドラーをカスタマイズした。
- [ ] エラーコードを定義した。
- [ ] エラーレスポンスのベストプラクティスを理解した。
