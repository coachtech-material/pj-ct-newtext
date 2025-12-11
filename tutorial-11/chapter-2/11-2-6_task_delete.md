# Tutorial 11-2-6: タスク削除の実装

## 🎯 このセクションで学ぶこと

*   タスク削除機能を実装する方法を学ぶ。
*   JavaScriptで確認ダイアログを表示する方法を学ぶ。
*   DELETEメソッドを使ってリソースを削除する方法を学ぶ。

---

## 導入：なぜタスク削除機能が重要なのか

**タスク削除機能**は、不要になったタスクを削除する機能です。

タスク削除機能を実装することで、ユーザーはタスクを整理できるようになります。

---

## 詳細解説

### 🔍 ルーティングの追加

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

### 🔍 コントローラーのdestroyメソッド

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

### 🔍 タスク詳細ページに削除ボタンを追加

タスク詳細ページに、削除ボタンを追加します。

**ファイル**: `resources/views/tasks/show.blade.php`

```blade
<h1>タスク詳細</h1>

@if (session('success'))
    <div style="color: green;">
        {{ session('success') }}
    </div>
@endif

<table border="1">
    <!-- ... -->
</table>

<a href="{{ route('tasks.edit', $task) }}">編集</a>

<form method="POST" action="{{ route('tasks.destroy', $task) }}" style="display:inline;" onsubmit="return confirm('本当に削除しますか?');">
    @csrf
    @method('DELETE')
    <button type="submit">削除</button>
</form>

<a href="{{ route('tasks.index') }}">一覧に戻る</a>
```

---

### 🔍 確認ダイアログ

`onsubmit="return confirm('本当に削除しますか?');"`は、**JavaScriptの確認ダイアログ**を表示します。

*   ユーザーが「OK」をクリックした場合: フォームが送信される
*   ユーザーが「キャンセル」をクリックした場合: フォームが送信されない

---

### 🔍 動作確認

ブラウザでタスク詳細ページにアクセスし、「削除」ボタンをクリックします。

確認ダイアログが表示され、「OK」をクリックすると、タスクが削除されることを確認します。

---

### 🔍 タスク一覧ページに削除ボタンを追加

タスク一覧ページにも、削除ボタンを追加できます。

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<table border="1">
    <thead>
        <tr>
            <th>ID</th>
            <th>タイトル</th>
            <th>期限</th>
            <th>ステータス</th>
            <th>操作</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($tasks as $task)
            <tr>
                <td>{{ $task->id }}</td>
                <td>{{ $task->title }}</td>
                <td>{{ $task->due_date }}</td>
                <td>{{ $task->status }}</td>
                <td>
                    <a href="{{ route('tasks.show', $task) }}">詳細</a>
                    <a href="{{ route('tasks.edit', $task) }}">編集</a>
                    <form method="POST" action="{{ route('tasks.destroy', $task) }}" style="display:inline;" onsubmit="return confirm('本当に削除しますか?');">
                        @csrf
                        @method('DELETE')
                        <button type="submit">削除</button>
                    </form>
                </td>
            </tr>
        @endforeach
    </tbody>
</table>
```

---

### 🔍 ソフトデリート

**ソフトデリート**は、データを物理的に削除せず、**削除フラグを立てる**機能です。

ソフトデリートを使うと、削除したデータを復元できます。

**マイグレーション**:

```php
Schema::create('tasks', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->string('title');
    $table->text('description')->nullable();
    $table->date('due_date')->nullable();
    $table->string('status')->default('未完了');
    $table->timestamps();
    $table->softDeletes();  // deleted_atカラムを追加
});
```

**モデル**:

```php
use Illuminate\Database\Eloquent\SoftDeletes;

class Task extends Model
{
    use SoftDeletes;

    protected $fillable = [
        'user_id',
        'title',
        'description',
        'due_date',
        'status',
    ];
}
```

**削除**:

```php
$task->delete();  // deleted_atに現在時刻が設定される
```

**復元**:

```php
$task->restore();  // deleted_atがNULLに戻る
```

**完全削除**:

```php
$task->forceDelete();  // 物理的に削除される
```

---

### 💡 TIP: リソースコントローラー

Laravelには、**リソースコントローラー**という機能があります。

リソースコントローラーを使うと、CRUD操作のルーティングとコントローラーメソッドを自動生成できます。

**ルーティング**:

```php
Route::resource('tasks', TaskController::class);
```

これにより、以下のルーティングが自動生成されます。

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

### 🚨 よくある間違い

#### 間違い1: @method('DELETE')を忘れる

**対処法**: フォームに`@method('DELETE')`を追加します。

---

#### 間違い2: 確認ダイアログを忘れる

**対処法**: `onsubmit="return confirm('本当に削除しますか?');"`を追加します。

---

#### 間違い3: 認可チェックを忘れる

**対処法**: `destroy`メソッドで、ログインユーザーのタスクかどうかを確認します。

---

## ✨ まとめ

このセクションでは、タスク削除機能を実装しました。

*   タスク削除機能を実装し、不要なタスクを削除できるようにした。
*   JavaScriptで確認ダイアログを表示し、誤削除を防いだ。
*   DELETEメソッドを使ってリソースを削除した。

次のセクションでは、ページネーションの実装について学びます。

---

## 📝 学習のポイント

- [ ] タスク削除機能を実装した。
- [ ] @method('DELETE')を使った。
- [ ] 確認ダイアログを表示した。
- [ ] 認可チェックを実装した。
