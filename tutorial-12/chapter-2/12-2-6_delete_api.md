# Tutorial 12-2-6: DELETE APIの実装（削除）

## 🎯 このセクションで学ぶこと

- タスクを削除するDELETE APIを実装する方法を学ぶ
- HTTPステータスコード（204 No Content、404 Not Found）を理解する
- なぜそのステータスコードを使うのかを学ぶ
- 削除APIの設計パターンを学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ更新APIの後に『削除API』を実装するのか？」

更新APIができたら、最後は「削除API」です。

---

### 理由1: CRUDの完成

CRUD（Create, Read, Update, Delete）の最後の操作です。

| 順序 | 操作 | 完了 |
|------|------|------|
| 1 | Read（一覧・詳細） | ✅ |
| 2 | Create | ✅ |
| 3 | Update | ✅ |
| 4 | Delete | 今回 |

---

### 理由2: 204 No Contentの使い方

削除成功時は、**204 No Content**を返すのが一般的です。

```php
return response()->json(null, 204);
```

---

### 理由3: 最もシンプルなAPI

削除APIは、**バリデーションが不要**で最もシンプルです。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | destroyメソッドの実装 | 削除のロジック |
| Step 2 | HTTPステータスコード | 204と404の使い分け |
| Step 3 | テスト | Thunder Clientで動作確認 |

> 💡 **ポイント**: DELETEリクエストは「削除」に使います。

---

## Step 1: destroyメソッドの実装

### 1-1. タスクを削除するAPI

**エンドポイント**: `DELETE /api/tasks/{id}`

**レスポンス例（成功時）**:

ステータスコード: `204 No Content`

レスポンスボディ: なし

---

### 1-2. コントローラーの実装

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function destroy(string $id)
{
    // タスクを取得
    $task = Task::where('user_id', 1)->find($id);

    // タスクが見つからない場合
    if (!$task) {
        return response()->json([
            'message' => 'タスクが見つかりません'
        ], 404);
    }

    // タスクを削除
    $task->delete();

    // レスポンスを返す（204 No Content）
    return response()->json(null, 204);
}
```

---

### 1-3. コードリーディング

#### `public function destroy(string $id)`

```php
public function destroy(string $id)
```

| 部分 | 説明 |
|------|------|
| `public function` | 公開メソッド |
| `destroy` | メソッド名（削除を表す慣例的な名前） |
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

#### `$task->delete()`

```php
$task->delete();
```

| 部分 | 説明 |
|------|------|
| `$task->delete()` | タスクをデータベースから削除 |

---

#### `response()->json(null, 204)`

```php
return response()->json(null, 204);
```

| 部分 | 説明 |
|------|------|
| `null` | レスポンスボディなし |
| `204` | HTTPステータスコード（No Content） |

---

## Step 2: HTTPステータスコード

### 2-1. 204 No Content

**204 No Content**は、**リクエストが成功し、レスポンスボディがない**ことを示します。

| 使用場面 | 説明 |
|----------|------|
| リソースが正常に削除された | タスクが削除された |
| レスポンスボディが不要 | 削除後に返すデータがない |

```php
return response()->json(null, 204);
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

### 2-3. 204と200の違い

| ステータスコード | レスポンスボディ | 使用場面 |
|----------------|----------------|----------|
| 204 No Content | なし | 削除成功、返すデータがない |
| 200 OK | あり | 削除成功、削除したデータを返す |

---

### 2-4. 200 OKで削除結果を返すパターン

削除したデータを返す場合は、200 OKを使います。

```php
public function destroy(string $id)
{
    $task = Task::where('user_id', 1)->find($id);

    if (!$task) {
        return response()->json([
            'message' => 'タスクが見つかりません'
        ], 404);
    }

    $task->delete();

    return response()->json([
        'message' => 'タスクを削除しました',
        'data' => $task
    ], 200);
}
```

---

## Step 3: テスト

### 3-1. Thunder Clientでテスト

**1. 成功する場合**

- メソッド: `DELETE`
- URL: `http://localhost/api/tasks/1`
- 期待: ステータスコード `204 No Content`

**2. タスクが見つからない場合**

- メソッド: `DELETE`
- URL: `http://localhost/api/tasks/9999`
- 期待: ステータスコード `404 Not Found`

---

### 3-2. クライアント側での処理例（JavaScript）

```javascript
fetch('http://localhost/api/tasks/1', {
  method: 'DELETE',
  headers: {
    'Accept': 'application/json',
  },
})
  .then(response => {
    if (response.status === 204) {
      console.log('タスクを削除しました');
    } else if (response.status === 404) {
      throw new Error('タスクが見つかりません');
    }
  })
  .catch(error => {
    console.error('エラー:', error.message);
  });
```

---

## 🚨 よくある間違い

### 間違い1: 常に200を返す

**問題**: 削除成功時は204を返すのが一般的

```php
// ❌ 間違い
return response()->json(['message' => 'Deleted'], 200);

// ✅ 正しい
return response()->json(null, 204);
```

---

### 間違い2: タスクが見つからない場合に200を返す

**問題**: 存在しないリソースの削除は404を返すべき

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

### 間違い3: 204でレスポンスボディを返す

**問題**: 204はレスポンスボディがないことを示す

```php
// ❌ 間違い
return response()->json(['message' => 'Deleted'], 204);

// ✅ 正しい
return response()->json(null, 204);
```

---

## 💡 TIP: 論理削除（ソフトデリート）

物理的に削除するのではなく、削除フラグを立てる方法もあります。

**モデル**:

```php
use Illuminate\Database\Eloquent\SoftDeletes;

class Task extends Model
{
    use SoftDeletes;
}
```

**マイグレーション**:

```php
$table->softDeletes();
```

**コントローラー**:

```php
$task->delete();  // deleted_atに日時が設定される
```

---

## ✨ まとめ

このセクションでは、タスクを削除するDELETE APIを実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | destroyメソッドの実装 |
| Step 2 | 204 No Contentと404 Not Foundの使い分け |
| Step 3 | Thunder Clientでのテスト方法 |

これでCRUD APIが完成しました！

| HTTPメソッド | エンドポイント | 操作 | ステータスコード |
|-------------|---------------|------|----------------|
| GET | /api/tasks | 一覧取得 | 200 |
| GET | /api/tasks/{id} | 詳細取得 | 200 / 404 |
| POST | /api/tasks | 作成 | 201 / 422 |
| PUT | /api/tasks/{id} | 更新 | 200 / 404 / 422 |
| DELETE | /api/tasks/{id} | 削除 | 204 / 404 |

次のセクションでは、エラーレスポンスの設計について学びます。

---
