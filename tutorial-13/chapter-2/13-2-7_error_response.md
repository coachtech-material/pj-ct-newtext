# Tutorial 13-2-7: 親切なエラーレスポンスの作成

## 🎯 このセクションで学ぶこと

- 親切なエラーレスポンスとは何かを理解する
- クライアントが使いやすいエラー形式を定義する方法を学ぶ
- 404 Not Found時にJSONでエラーを返す設定を学ぶ
- エラーハンドリングのベストプラクティスを理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜCRUD実装の後に『エラーレスポンス』を整備するのか？」

CRUD APIが完成したら、次は「エラーレスポンス」です。

---

### 理由1: 正常系だけでは不十分

これまでは主に「正常系」を実装してきました。

しかし、実際のAPIでは**エラーが発生する**ことがあります。

| エラーの種類 | 説明 |
|-------------|------|
| バリデーションエラー | 入力値が不正 |
| 認証エラー | ログインが必要 |
| 存在しないリソース | 404 Not Found |
| サーバーエラー | 500 Internal Server Error |

---

### 理由2: 一貫したエラー形式

エラーレスポンスも、**一貫した形式**であるべきです。

```json
{
    "message": "入力内容に誤りがあります",
    "error": "VALIDATION_ERROR",
    "status": 422
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
| Step 1 | エラーレスポンスの設計 | 統一フォーマットを決める |
| Step 2 | 例外ハンドラーのカスタマイズ | Handler.phpの編集 |
| Step 3 | ベストプラクティス | 本番環境での対応 |

> 💡 **ポイント**: 良いAPIは、エラー時にも適切な情報を返します。

---

## Step 1: エラーレスポンスの設計

### 1-1. エラーレスポンスの基本形式

```json
{
  "message": "エラーメッセージ",
  "error": "エラーコード",
  "status": 404
}
```

**例**:

```json
{
  "message": "Resource not found",
  "error": "RESOURCE_NOT_FOUND",
  "status": 404
}
```

---

### 1-2. find() と findOrFail() の違い

404エラーの処理方法には2つのアプローチがあります。

| メソッド | 見つからない場合 | エラー処理の場所 |
|----------|------------------|------------------|
| `find()` | `null`を返す | Controller内で判定 |
| `findOrFail()` | 例外を投げる | Handlerで一元処理 |

---

#### find() を使う場合（Controllerで処理）

```php
public function show(string $id): JsonResponse
{
    $task = Task::find($id);
    
    if (!$task) {
        return response()->json([
            'message' => 'Task not found',
            'error' => 'TASK_NOT_FOUND',
            'status' => 404
        ], 404);
    }
    
    return response()->json(['data' => $task], 200);
}
```

**特徴**: 各Controllerで404の処理を書く必要がある

---

#### findOrFail() を使う場合（Handlerで一元処理）

```php
public function show(string $id): JsonResponse
{
    $task = Task::findOrFail($id);
    
    return response()->json(['data' => $task], 200);
}
```

**特徴**: Controllerは正常系のみ、404はHandlerで一括処理

---

### 1-3. 推奨: findOrFail() + Handlerで一元処理

このカリキュラムでは、**findOrFail() を使い、Handlerで404を一元処理**する方法を推奨します。

| メリット | 説明 |
|----------|------|
| コードが簡潔 | Controllerは正常系のみに集中 |
| 一貫性 | すべての404が同じ形式で返る |
| 保守性 | エラー形式の変更が1箇所で済む |

**コントローラーの例**:

```php
public function show(string $id): JsonResponse
{
    // findOrFail()は見つからない場合にModelNotFoundExceptionを投げる
    $task = Task::findOrFail($id);
    
    return response()->json(['data' => $task], 200);
}

public function update(Request $request, string $id): JsonResponse
{
    $task = Task::findOrFail($id);
    
    $validated = $request->validate([...]);
    $task->update($validated);
    
    return response()->json(['data' => $task], 200);
}

public function destroy(string $id): JsonResponse
{
    $task = Task::findOrFail($id);
    $task->delete();
    
    return response()->json(null, 204);
}
```

> 💡 **ポイント**: `findOrFail()`はデータが見つからない場合に`ModelNotFoundException`を投げます。この例外はStep 2でHandlerによってキャッチされ、JSONエラーレスポンスに変換されます。

---

### 1-3. バリデーションエラーのレスポンス

Laravelでは、バリデーションエラーが発生すると、以下の形式でレスポンスが返されます。

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

| フィールド | 説明 |
|-----------|------|
| message | エラーの概要 |
| errors | フィールドごとのエラーメッセージ |

---

### 1-4. エラーコードの一覧

| エラーコード | HTTPステータス | 説明 |
|------------|--------------|------|
| TASK_NOT_FOUND | 404 | タスクが見つからない |
| USER_NOT_FOUND | 404 | ユーザーが見つからない |
| VALIDATION_ERROR | 422 | バリデーションエラー |
| UNAUTHORIZED | 401 | 認証エラー |
| FORBIDDEN | 403 | 権限エラー |
| INTERNAL_SERVER_ERROR | 500 | サーバーエラー |

---

## Step 2: 例外ハンドラーのカスタマイズ

### 2-1. Handler.phpの編集

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
    public function register(): void
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

---

### 2-2. コードリーディング

| コード | 説明 |
|--------|------|
| `ModelNotFoundException` | `findOrFail()`でモデルが見つからない場合に投げられる |
| `NotFoundHttpException` | エンドポイントが見つからない場合 |
| `$request->is('api/*')` | APIリクエストの場合だけ適用 |
| `renderable()` | 例外をキャッチしてカスタムレスポンスを返す |

---

### 2-3. 処理の流れ

```
Controller
    ↓
findOrFail(9999)  ← データが見つからない
    ↓
ModelNotFoundExceptionが投げられる
    ↓
Handlerがキャッチ
    ↓
JSONエラーレスポンスを返す
```

> 💡 **ポイント**: Controllerで`findOrFail()`を使うことで、この流れが機能します。`find()`を使うと例外が投げられないため、Handlerではキャッチされません。

---

### 2-4. Thunder Clientでテスト

> 📌 **前提**: Controllerで`findOrFail()`を使用していることを確認してください。認証が必要な場合は、AuthタブでBearerトークンを設定してください。

**1. リソースが見つからない場合**

- メソッド: `GET`
- URL: `http://localhost/api/tasks/9999`
- Auth: Bearerトークンを設定（認証が必要な場合）
- 期待:

```json
{
  "message": "Resource not found",
  "error": "RESOURCE_NOT_FOUND",
  "status": 404
}
```

**2. エンドポイントが見つからない場合**

- メソッド: `GET`
- URL: `http://localhost/api/invalid-endpoint`
- 期待:

```json
{
  "message": "Endpoint not found",
  "error": "ENDPOINT_NOT_FOUND",
  "status": 404
}
```

---

## Step 3: ベストプラクティス

### 3-1. 一貫性を保つ

すべてのエラーレスポンスで、同じ形式を使います。

```json
{
  "message": "エラーメッセージ",
  "error": "エラーコード",
  "status": 404
}
```

---

### 3-2. 詳細なエラーメッセージを返す

ユーザーが理解しやすいエラーメッセージを返します。

```json
{
  "message": "タスクが見つかりませんでした",
  "error": "TASK_NOT_FOUND",
  "status": 404
}
```

---

### 3-3. 本番環境では詳細なエラーを隠す

本番環境では、詳細なエラーメッセージを隠します。

**ファイル**: `.env`

```
APP_DEBUG=true  # 開発環境
APP_DEBUG=false # 本番環境
```

**本番環境のエラーレスポンス**:

```json
{
  "message": "An error occurred while processing your request",
  "error": "INTERNAL_SERVER_ERROR",
  "status": 500
}
```

---

### 3-4. クライアント側での処理例（JavaScript）

```javascript
fetch('http://localhost/api/tasks/9999', {
  headers: {
    'Accept': 'application/json',
    'Authorization': 'Bearer 発行したトークン',
  },
})
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

## 🚨 よくある間違い

### 間違い1: find()とfindOrFail()を混同する

**問題**: Handlerでの一元処理が機能しない

```php
// ❌ 間違い（Handlerでキャッチされない）
$task = Task::find($id);
// find()はnullを返すだけで例外を投げない

// ✅ 正しい（Handlerでキャッチされる）
$task = Task::findOrFail($id);
// findOrFail()はModelNotFoundExceptionを投げる
```

---

### 間違い2: エラーメッセージを返さない

**問題**: クライアントがエラーの内容を判断できない

```php
// ❌ 間違い
return response()->json([], 404);

// ✅ 正しい
return response()->json([
    'message' => 'Resource not found',
    'error' => 'RESOURCE_NOT_FOUND',
    'status' => 404
], 404);
```

---

### 間違い3: 500エラーをそのまま返す

**問題**: ユーザーに不親切

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

### 間違い4: 本番環境で詳細なエラーを返す

**問題**: セキュリティリスク

```php
// ❌ 間違い（本番環境）
return response()->json([
    'message' => 'SQLSTATE[42S02]: Base table or view not found',
], 500);

// ✅ 正しい（本番環境）
return response()->json([
    'message' => 'An error occurred while processing your request',
], 500);
```

---

## 💡 TIP: デバッグモードを切り替える

開発環境では詳細なエラーメッセージを表示し、本番環境では隠します。

| 環境 | APP_DEBUG | 詳細なエラー |
|------|-----------|-------------|
| 開発環境 | true | 表示する |
| 本番環境 | false | 隠す |

---

## ✨ まとめ

このセクションでは、親切なエラーレスポンスの作成を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | エラーレスポンスの基本形式とエラーコード |
| Step 2 | 例外ハンドラーのカスタマイズ |
| Step 3 | 本番環境でのベストプラクティス |

これで、Chapter 2（RESTful APIの実装）は完了です。次のChapter 3では、API認証とセキュリティについて学びます。

---
