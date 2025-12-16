# Tutorial 11-2-6: タスク削除の実装

## 🎯 このセクションで学ぶこと

- タスク削除機能を実装する方法を学ぶ
- JavaScriptで確認ダイアログを表示する方法を学ぶ
- DELETEメソッドを使ってリソースを削除する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ『編集』の次に『削除』を実装するのか？」

CRUDの最後は「削除」機能です。なぜ最後なのでしょうか？

---

### 理由1: 最もシンプルな機能

「削除」は、**データを取得して削除するだけ**です。

```php
$task = Task::findOrFail($id);
$task->delete();
```

フォームもバリデーションも不要なので、CRUDの中で**最もシンプル**です。

---

### 理由2: 危険な操作なので最後に

「削除」は**元に戻せない操作**です。

実務では、削除機能は慎重に実装します。そのため、他の機能が安定してから実装するのが一般的です。

---

### 理由3: 確認ダイアログを学ぶ

削除ボタンを押したら、**本当に削除していいか確認**する必要があります。

```html
<form onsubmit="return confirm('本当に削除しますか？')">
```

このようなUXの考慮も、削除機能で学びます。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | ルーティングの追加 | DELETEメソッドを使用 |
| Step 2 | destroyメソッドの実装 | データを取得して削除 |
| Step 3 | 詳細ページに削除ボタンを追加 | 削除ボタンと確認ダイアログ |
| Step 4 | 一覧ページに削除ボタンを追加 | 一覧からも削除できるように |
| Step 5 | 動作確認 | 正しく動作するか確認する |

> 💡 **ポイント**: HTMLフォームはGETとPOSTしかサポートしていないので、`@method('DELETE')`を使います。

---

## Step 1: ルーティングの追加

### 1-1. 削除用のルートを定義する

タスク削除のルーティングを追加します。

**ファイル**: `routes/web.php`

```php
Route::middleware(['auth'])->group(function () {
    Route::get('/tasks', [TaskController::class, 'index'])->name('tasks.index');
    Route::get('/tasks/create', [TaskController::class, 'create'])->name('tasks.create');
    Route::post('/tasks', [TaskController::class, 'store'])->name('tasks.store');
    Route::get('/tasks/{task}', [TaskController::class, 'show'])->name('tasks.show');
    Route::get('/tasks/{task}/edit', [TaskController::class, 'edit'])->name('tasks.edit');
    Route::put('/tasks/{task}', [TaskController::class, 'update'])->name('tasks.update');
    Route::delete('/tasks/{task}', [TaskController::class, 'destroy'])->name('tasks.destroy');
});
```

---

### 1-2. コードリーディング

#### `Route::delete('/tasks/{task}', ...)->name('tasks.destroy')`

- `DELETE /tasks/1`にリクエストを送信すると、`destroy`メソッドが実行されます
- DELETEメソッドは、**リソースを削除する**ときに使用します

---

#### CRUDルーティングの全体像

| 機能 | HTTPメソッド | URI | メソッド |
|------|-------------|-----|---------|
| 一覧 | GET | /tasks | index |
| 作成フォーム | GET | /tasks/create | create |
| 作成 | POST | /tasks | store |
| 詳細 | GET | /tasks/{task} | show |
| 編集フォーム | GET | /tasks/{task}/edit | edit |
| 更新 | PUT | /tasks/{task} | update |
| 削除 | DELETE | /tasks/{task} | destroy |

これで**CRUD操作のルーティングが完成**しました。

---

## Step 2: destroyメソッドの実装

### 2-1. 削除メソッドを追加する

タスクを削除する`destroy`メソッドを追加します。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function destroy(Task $task)
{
    // 認可チェック：ログインユーザーのタスクかどうか
    if ($task->user_id !== auth()->id()) {
        abort(403, 'このタスクを削除する権限がありません。');
    }

    $task->delete();

    return redirect()->route('tasks.index')->with('success', 'タスクを削除しました。');
}
```

---

### 2-2. コードリーディング

#### `$task->delete()`

- モデルの`delete()`メソッドを呼び出すと、データベースからレコードが削除されます
- ルートモデルバインディングで取得した`$task`を削除します

---

#### リダイレクト先

- 削除後は**一覧ページにリダイレクト**します
- 詳細ページにリダイレクトすると、削除したタスクが存在しないため404エラーになります

---

## Step 3: 詳細ページに削除ボタンを追加

### 3-1. 削除フォームを追加する

タスク詳細ページに、削除ボタンを追加します。

**ファイル**: `resources/views/tasks/show.blade.php`

テーブルの下に、以下のコードを追加します。

```blade
<div style="margin-top: 20px;">
    <a href="{{ route('tasks.edit', $task) }}" style="display: inline-block; padding: 10px 20px; background-color: #2196f3; color: white; text-decoration: none; border-radius: 4px;">編集</a>
    
    <form method="POST" action="{{ route('tasks.destroy', $task) }}" style="display: inline;" onsubmit="return confirm('本当に削除しますか？');">
        @csrf
        @method('DELETE')
        <button type="submit" style="padding: 10px 20px; background-color: #f44336; color: white; border: none; border-radius: 4px; cursor: pointer;">削除</button>
    </form>
    
    <a href="{{ route('tasks.index') }}" style="margin-left: 10px; color: #666;">← 一覧に戻る</a>
</div>
```

---

### 3-2. コードリーディング

#### `@method('DELETE')`

- HTMLフォームは、`GET`と`POST`しかサポートしていません
- `@method('DELETE')`を追加すると、Laravelは`POST`リクエストを`DELETE`リクエストとして扱います

---

#### `onsubmit="return confirm('本当に削除しますか？');"`

- フォーム送信前に**JavaScriptの確認ダイアログ**を表示します
- ユーザーが「OK」をクリックした場合: フォームが送信される
- ユーザーが「キャンセル」をクリックした場合: フォームが送信されない

---

#### `style="display: inline;"`

- フォームをインライン要素として表示します
- これにより、編集リンクと削除ボタンが横並びになります

---

## Step 4: 一覧ページに削除ボタンを追加

### 4-1. 一覧ページにも削除フォームを追加する

タスク一覧ページにも、削除ボタンを追加します。

**ファイル**: `resources/views/tasks/index.blade.php`

操作列に削除ボタンを追加します。

```blade
<td>
    <a href="{{ route('tasks.show', $task) }}">詳細</a>
    <a href="{{ route('tasks.edit', $task) }}">編集</a>
    <form method="POST" action="{{ route('tasks.destroy', $task) }}" style="display: inline;" onsubmit="return confirm('本当に削除しますか？');">
        @csrf
        @method('DELETE')
        <button type="submit" style="background: none; border: none; color: #f44336; cursor: pointer;">削除</button>
    </form>
</td>
```

---

### 4-2. コードリーディング

#### 一覧ページでの削除

- 一覧ページからも削除できるようにすることで、**操作の効率が上がります**
- ただし、誤削除を防ぐために確認ダイアログは必須です

---

## Step 5: 動作確認

### 5-1. 詳細ページから削除する

1. ブラウザでタスク詳細ページにアクセスする
2. 「削除」ボタンをクリックする
3. 確認ダイアログが表示される
4. 「OK」をクリックする
5. タスク一覧ページにリダイレクトされる
6. 「タスクを削除しました。」というメッセージが表示される
7. 削除したタスクが一覧から消えていることを確認する

---

### 5-2. 一覧ページから削除する

1. ブラウザでタスク一覧ページにアクセスする
2. 任意のタスクの「削除」リンクをクリックする
3. 確認ダイアログが表示される
4. 「キャンセル」をクリックする
5. タスクが削除されないことを確認する

---

### 5-3. 認可チェックを確認する

1. ユーザーAでログインし、タスクを作成する
2. ログアウトする
3. ユーザーBでログインする
4. ブラウザで`http://localhost/tasks/1`にアクセスする
5. 削除ボタンをクリックしても、403エラーが表示される

---

## 🚨 よくある間違い

### 間違い1: @method('DELETE')を忘れる

**エラー**:

```
The DELETE method is not supported for route tasks/{task}. Supported methods: GET, HEAD, POST.
```

**対処法**: フォームに`@method('DELETE')`を追加します。

---

### 間違い2: 確認ダイアログを忘れる

**問題**: 誤ってクリックしただけでデータが削除される

**対処法**: `onsubmit="return confirm('本当に削除しますか？');"`を追加します。

---

### 間違い3: 認可チェックを忘れる

**問題**: 他のユーザーのタスクを削除できてしまう

**対処法**: `destroy`メソッドで、ログインユーザーのタスクかどうかを確認します。

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
|------|-------|------|
| 削除 | `$task->delete()` | `deleted_at`に現在時刻が設定される |
| 復元 | `$task->restore()` | `deleted_at`がNULLに戻る |
| 完全削除 | `$task->forceDelete()` | 物理的に削除される |

---

## 💡 TIP: リソースコントローラー

Laravelには、**リソースコントローラー**という機能があります。

```php
Route::resource('tasks', TaskController::class);
```

この1行で、CRUD操作の7つのルーティングが自動生成されます。

| HTTPメソッド | URI | アクション | ルート名 |
|---|---|---|---|
| GET | /tasks | index | tasks.index |
| GET | /tasks/create | create | tasks.create |
| POST | /tasks | store | tasks.store |
| GET | /tasks/{task} | show | tasks.show |
| GET | /tasks/{task}/edit | edit | tasks.edit |
| PUT/PATCH | /tasks/{task} | update | tasks.update |
| DELETE | /tasks/{task} | destroy | tasks.destroy |

---

## ✨ まとめ

このセクションでは、タスク削除機能を実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | DELETEメソッドのルーティング |
| Step 2 | `$task->delete()`でデータを削除 |
| Step 3 | `@method('DELETE')`と確認ダイアログ |
| Step 4 | 一覧ページからも削除できるようにする |
| Step 5 | 動作確認と認可チェックの確認 |

これで**CRUD操作が完成**しました。次のセクションでは、検索機能の実装について学びます。

---

## 📝 学習のポイント

- [ ] タスク削除機能を実装した
- [ ] `@method('DELETE')`を使った
- [ ] 確認ダイアログを表示した
- [ ] 認可チェックを実装した
- [ ] ソフトデリートの概念を理解した
- [ ] リソースコントローラーの存在を知った
