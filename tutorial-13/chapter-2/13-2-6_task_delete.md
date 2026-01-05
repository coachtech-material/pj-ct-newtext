# Tutorial 13-2-6: タスク削除の実装

## 🎯 このセクションで学ぶこと

- 提供された削除ボタンを読み解き、削除処理の流れを理解する方法を学ぶ
- DELETEメソッドを使ってリソースを削除する方法を学ぶ
- Tinkerで削除処理を確認してから、コントローラーを実装する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 削除機能の特徴

「削除」は、**データを取得して削除するだけ**です。フォームもバリデーションも不要なので、CRUDの中で**最もシンプル**です。

ただし、削除は**元に戻せない操作**なので、確認ダイアログを表示するのが一般的です。

今回も「提供コードありき」のフローで進めます：

```
1. 画面アクセス＆エラー確認（削除ボタンの確認）
2. Bladeの解読（削除フォームの構造を確認）
3. Tinker検証（削除処理を確認）
4. バックエンド実装
```

---

## Step 1: 画面アクセス＆エラー確認

### 1-1. 詳細画面で削除ボタンを確認する

```
http://localhost/tasks/1
```

詳細画面に削除ボタンが表示されていることを確認します。

### 1-2. 削除ボタンをクリックする

削除ボタンをクリックすると、以下のエラーが表示されます：

```
The DELETE method is not supported for route tasks/1.
```

**読み解き**：`destroy`アクションがまだ実装されていないため、エラーになっています。

---

## Step 2: Bladeの解読

### 2-1. 削除フォームを読む

`resources/views/tasks/show.blade.php`の削除ボタン部分を確認します。

```blade
<form action="{{ route('tasks.destroy', $task) }}" method="POST" 
      onsubmit="return confirm('本当に削除しますか？')">
    @csrf
    @method('DELETE')
    <button type="submit" class="btn-danger">削除</button>
</form>
```

### 2-2. 削除フォームの構造を理解する

| 要素 | 説明 |
|:---|:---|
| `action="{{ route('tasks.destroy', $task) }}"` | 削除先のURL（`/tasks/1`） |
| `method="POST"` | HTMLフォームはPOSTで送信 |
| `@csrf` | CSRF保護トークン |
| `@method('DELETE')` | LaravelにDELETEリクエストとして処理させる |
| `onsubmit="return confirm(...)"` | 確認ダイアログを表示 |

### 2-3. @method('DELETE')の仕組み

HTMLフォームは`GET`と`POST`しかサポートしていません。`DELETE`を使うには、`@method`ディレクティブを使います。

```blade
@method('DELETE')
```

これにより、フォームに隠しフィールドが追加されます：

```html
<input type="hidden" name="_method" value="DELETE">
```

Laravelはこの隠しフィールドを見て、`DELETE`リクエストとして処理します。

---

## Step 3: Tinker検証

コントローラーを実装する前に、**Tinkerで削除処理を確認**します。

### 3-1. Tinkerを起動する

```bash
sail artisan tinker
```

### 3-2. タスクを確認する

```php
>>> App\Models\Task::count();
```

**期待する結果**：

```
=> 5  // 現在のタスク数
```

### 3-3. タスクを削除する

```php
>>> $task = App\Models\Task::find(1);
>>> $task->delete();
>>> App\Models\Task::count();
```

**期待する結果**：

```
=> true
=> 4  // 1件減っている
```

### 3-4. 削除したタスクを確認する

```php
>>> App\Models\Task::find(1);
```

**期待する結果**：

```
=> null  // 削除されているのでnull
```

> **💡 ポイント**: `delete()`メソッドは`true`を返し、データベースからレコードが削除されます。

---

## Step 4: バックエンド実装

### 4-1. destroyアクションを実装する

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
/**
 * Remove the specified resource from storage.
 */
public function destroy(Task $task)
{
    // タスクを削除
    $task->delete();
    
    return redirect()->route('tasks.index')
        ->with('success', 'タスクを削除しました');
}
```

**コードリーディング**：

```php
public function destroy(Task $task)
```
→ ルートモデルバインディングで`$task`を取得します。存在しないIDの場合は自動的に404エラーになります。

```php
$task->delete();
```
→ データベースからレコードを削除します。

```php
return redirect()->route('tasks.index')
```
→ 削除後は**一覧ページにリダイレクト**します。詳細ページにリダイレクトすると、削除したタスクが存在しないため404エラーになります。

---

## Step 5: 動作確認

### 5-1. 詳細ページから削除する

```
http://localhost/tasks/1
```

1. 「削除」ボタンをクリック
2. 確認ダイアログが表示される
3. 「OK」をクリック

| 確認項目 | 期待する結果 |
|:---|:---|
| 一覧ページにリダイレクトされる | `/tasks`に遷移 |
| フラッシュメッセージが表示される | 「タスクを削除しました」と表示 |
| 削除したタスクが消えている | 一覧に表示されない |

### 5-2. 確認ダイアログでキャンセルする

1. 「削除」ボタンをクリック
2. 確認ダイアログが表示される
3. 「キャンセル」をクリック

| 確認項目 | 期待する結果 |
|:---|:---|
| タスクが削除されない | そのまま詳細画面に留まる |

### 5-3. 存在しないタスクを削除しようとする

```
http://localhost/tasks/9999
```

| 確認項目 | 期待する結果 |
|:---|:---|
| 404エラーが表示される | ルートモデルバインディングが自動で404を返す |

---

## 💡 TIP: 一覧ページからも削除できるようにする

一覧ページにも削除ボタンを追加すると、操作の効率が上がります。

`resources/views/tasks/index.blade.php`の操作列に追加：

```blade
<td>
    <a href="{{ route('tasks.show', $task) }}">詳細</a>
    <a href="{{ route('tasks.edit', $task) }}">編集</a>
    <form action="{{ route('tasks.destroy', $task) }}" method="POST" 
          style="display: inline;" 
          onsubmit="return confirm('本当に削除しますか？')">
        @csrf
        @method('DELETE')
        <button type="submit">削除</button>
    </form>
</td>
```

---

## 💡 TIP: ソフトデリート

**ソフトデリート**は、データを物理的に削除せず、**削除フラグを立てる**機能です。

### マイグレーションに追加

```php
$table->softDeletes();  // deleted_atカラムを追加
```

### モデルに追加

```php
use Illuminate\Database\Eloquent\SoftDeletes;

class Task extends Model
{
    use SoftDeletes;
}
```

### 操作方法

| 操作 | コード | 結果 |
|:---|:---|:---|
| 削除 | `$task->delete()` | `deleted_at`に現在時刻が設定される |
| 復元 | `$task->restore()` | `deleted_at`がNULLに戻る |
| 完全削除 | `$task->forceDelete()` | 物理的に削除される |

ソフトデリートを使うと、誤って削除したデータを復元できます。

---

## 💡 TIP: リソースコントローラー

ここまでで、CRUDの7つのルーティングを個別に定義しました。Laravelには、これを1行で定義できる**リソースコントローラー**があります。

```php
Route::resource('tasks', TaskController::class);
```

この1行で、以下のルーティングが自動生成されます：

| HTTPメソッド | URI | アクション | ルート名 |
|:---|:---|:---|:---|
| GET | /tasks | index | tasks.index |
| GET | /tasks/create | create | tasks.create |
| POST | /tasks | store | tasks.store |
| GET | /tasks/{task} | show | tasks.show |
| GET | /tasks/{task}/edit | edit | tasks.edit |
| PUT/PATCH | /tasks/{task} | update | tasks.update |
| DELETE | /tasks/{task} | destroy | tasks.destroy |

---

## ✨ まとめ

このセクションでは、「提供コードありき」の開発フローでタスク削除を実装しました。

| ステップ | 学んだこと |
|:---|:---|
| Step 1 | 削除ボタンの確認とエラーの確認 |
| Step 2 | Bladeを読み解いて、@method('DELETE')と確認ダイアログを理解 |
| Step 3 | Tinkerで削除処理を確認 |
| Step 4 | destroyアクションを実装 |
| Step 5 | 動作確認と確認ダイアログの確認 |

これで**CRUD操作が完成**しました。次のセクションでは、検索機能の実装について学びます。

---
