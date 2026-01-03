# Tutorial 13-2-6: DELETE APIの実装（削除）

## 🎯 このセクションで学ぶこと

- タスクを削除するDELETE APIを実装する方法を学ぶ
- HTTPステータスコード（204 No Content、404 Not Found）を理解する
- なぜそのステータスコードを使うのかを学ぶ
- 200 OKと204 No Contentの違いを理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ更新APIの後に『削除API』を実装するのか？」

更新APIができたら、次は「削除API」です。

---

### 理由1: CRUDの最後

CRUD（Create, Read, Update, Delete）の最後は「削除」です。

これでCRUD APIが完成します。

---

### 理由2: 削除は慎重に

削除は**取り消しができない**操作です。

| 考慮事項 | 説明 |
|----------|------|
| 本当に削除していいか確認 | フロントエンドで確認ダイアログ |
| 論理削除（soft delete）の検討 | データを残す場合 |
| 関連データの処理 | 外部キー制約 |

---

### 理由3: 適切なレスポンス

削除成功時は、**204 No Content**を返すのが一般的です。

```php
$task->delete();
return response()->json(null, 204);
```

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | destroyメソッドの実装 | 削除のロジック |
| Step 2 | HTTPステータスコード | 204と404の使い分け |
| Step 3 | 応用テクニック | ソフトデリートなど |

> 💡 **ポイント**: DELETEリクエストは「削除」に使います。

---

## Step 1: destroyメソッドの実装

### 1-1. タスクを削除するAPI

**エンドポイント**: `DELETE /api/tasks/{id}`

**レスポンス例（成功時）**:

- ステータスコード: `204 No Content`
- ボディ: なし

---

### 1-2. コントローラーの実装

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function destroy(string $id): JsonResponse
{
    $task = Task::where('user_id', Auth::id())->find($id);
    
    if (!$task) {
        return response()->json([
            'message' => 'Task not found'
        ], 404);
    }
    
    $task->delete();
    
    return response()->json(null, 204);
}
```

---

### 1-3. コードリーディング

| コード | 説明 |
|--------|------|
| `Task::where('user_id', Auth::id())->find($id)` | ログインユーザーのタスクを取得 |
| `$task->delete()` | タスクを削除する |
| `response()->json(null, 204)` | 204 No Contentを返す |

---

## Step 2: HTTPステータスコード

### 2-1. 204 No Content

**204 No Content**は、**リクエストが成功したが、レスポンスボディがない**ことを示します。

| 使用場面 | 説明 |
|----------|------|
| リソースが正常に削除された | タスクが削除された |
| 処理が正常に完了したが、返すデータがない | レスポンスボディ不要 |

```php
return response()->json(null, 204);
// または
return response()->noContent();
```

---

### 2-2. 404 Not Found

**404 Not Found**は、**リソースが見つからなかった**ことを示します。

```php
return response()->json([
    'message' => 'Task not found'
], 404);
```

---

### 2-3. 200 OKと204 No Contentの違い

| ステータスコード | レスポンスボディ | 用途 |
|----------------|----------------|------|
| 200 OK | あり | 削除されたリソースのデータを返す |
| 204 No Content | なし | 削除が成功したことだけを伝える |

**推奨**: DELETEリクエストでは、**204 No Content**を使う

---

### 2-4. Thunder Clientでテスト

**1. 成功する場合**

- メソッド: `DELETE`
- URL: `http://localhost:8000/api/tasks/1`
- 期待: ステータスコード `204 No Content`

**2. タスクが見つからない場合**

- メソッド: `DELETE`
- URL: `http://localhost:8000/api/tasks/9999`
- 期待: ステータスコード `404 Not Found`

---

## Step 3: 応用テクニック

### 3-1. response()->noContent()を使う

Laravelでは、`response()->noContent()`を使うと、204 No Contentを返せます。

```php
public function destroy(string $id): Response
{
    $task = Task::where('user_id', Auth::id())->findOrFail($id);
    $task->delete();
    
    return response()->noContent();
}
```

---

### 3-2. 削除されたリソースのデータを返す場合

削除されたリソースのデータを返す場合は、**200 OK**を使います。

```php
public function destroy(string $id): JsonResponse
{
    $task = Task::where('user_id', Auth::id())->findOrFail($id);
    $deletedTask = $task->toArray();
    $task->delete();
    
    return response()->json([
        'message' => '削除しました',
        'data' => $deletedTask
    ], 200);
}
```

---

### 3-3. ソフトデリート

**ソフトデリート**を使うと、データを物理的に削除せず、論理的に削除できます。

**マイグレーション**:

```php
$table->softDeletes();
```

**モデル**:

```php
use Illuminate\Database\Eloquent\SoftDeletes;

class Task extends Model
{
    use SoftDeletes;
}
```

**削除**:

```php
$task->delete(); // deleted_atに日時が設定される
```

**完全削除**:

```php
$task->forceDelete(); // データベースから完全に削除される
```

---

### 3-4. クライアント側での処理例（JavaScript）

```javascript
fetch('http://localhost:8000/api/tasks/1', {
  method: 'DELETE',
})
  .then(response => {
    if (response.status === 204) {
      console.log('削除されました');
    } else if (response.status === 404) {
      return response.json().then(data => {
        throw new Error(data.message);
      });
    }
  })
  .catch(error => {
    console.error('エラー:', error);
  });
```

---

## 🚨 よくある間違い

### 間違い1: 200 OKを返す

**問題**: 削除が成功した場合は204を返すのが推奨

```php
// ❌ 間違い
return response()->json(['message' => 'Deleted'], 200);

// ✅ 正しい
return response()->noContent();
```

---

### 間違い2: 204でレスポンスボディを返す

**問題**: 204 No Contentの場合はレスポンスボディなし

```php
// ❌ 間違い
return response()->json(['message' => 'Deleted'], 204);

// ✅ 正しい
return response()->json(null, 204);
```

---

### 間違い3: 存在しないタスクを削除しようとした場合に200を返す

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

## 💡 TIP: ステータスコードの重要性

適切なステータスコードを返すことで、クライアント側で以下のことができます。

| 判断 | 説明 |
|------|------|
| 成功・失敗を判断する | 204なら削除成功、404ならリソースが存在しない |
| エラー処理を行う | 404の場合は「タスクが見つかりません」と表示 |
| リトライを判断する | 404の場合はリトライしない |

---

## ✨ まとめ

このセクションでは、タスクを削除するDELETE APIを実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | destroyメソッドの実装 |
| Step 2 | 204 No Contentと404 Not Foundの使い分け |
| Step 3 | ソフトデリートなどの応用テクニック |

次のセクションでは、親切なエラーレスポンスの作成について学びます。

---
