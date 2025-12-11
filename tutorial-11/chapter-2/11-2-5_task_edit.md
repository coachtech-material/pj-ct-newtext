# Tutorial 11-2-5: タスク編集の実装

## 🎯 このセクションで学ぶこと

*   タスク編集フォームを実装する方法を学ぶ。
*   既存のデータをフォームに表示する方法を学ぶ。
*   タスクを更新する方法を学ぶ。

---

## 導入：なぜタスク編集機能が重要なのか

**タスク編集機能**は、既存のタスクを更新する機能です。

タスク編集機能を実装することで、ユーザーはタスクの情報を変更できるようになります。

---

## 詳細解説

### 🔍 ルーティングの追加

タスク編集のルーティングを追加します。

**ファイル**: `routes/web.php`

```php
Route::middleware(['auth'])->group(function () {
    Route::get('/tasks', [TaskController::class, 'index'])->name('tasks.index');
    Route::get('/tasks/create', [TaskController::class, 'create'])->name('tasks.create');
    Route::post('/tasks', [TaskController::class, 'store'])->name('tasks.store');
    Route::get('/tasks/{task}', [TaskController::class, 'show'])->name('tasks.show');
    Route::get('/tasks/{task}/edit', [TaskController::class, 'edit'])->name('tasks.edit');
    Route::put('/tasks/{task}', [TaskController::class, 'update'])->name('tasks.update');
});
```

---

### 🔍 コントローラーのeditメソッド

タスク編集フォームを表示する`edit`メソッドを追加します。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function edit(Task $task)
{
    // 認可チェック：ログインユーザーのタスクかどうか
    if ($task->user_id !== auth()->id()) {
        abort(403, 'このタスクを編集する権限がありません。');
    }

    return view('tasks.edit', compact('task'));
}
```

---

### 🔍 タスク編集フォームのビュー

タスク編集フォームのビューを作成します。

**ファイル**: `resources/views/tasks/edit.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>タスク編集</title>
</head>
<body>
    <h1>タスク編集</h1>

    @if ($errors->any())
        <div style="color: red;">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form method="POST" action="{{ route('tasks.update', $task) }}">
        @csrf
        @method('PUT')

        <div>
            <label for="title">タイトル</label>
            <input type="text" id="title" name="title" value="{{ old('title', $task->title) }}" required>
        </div>

        <div>
            <label for="description">説明</label>
            <textarea id="description" name="description">{{ old('description', $task->description) }}</textarea>
        </div>

        <div>
            <label for="due_date">期限</label>
            <input type="date" id="due_date" name="due_date" value="{{ old('due_date', $task->due_date) }}">
        </div>

        <div>
            <label for="status">ステータス</label>
            <select id="status" name="status">
                <option value="未完了" {{ old('status', $task->status) == '未完了' ? 'selected' : '' }}>未完了</option>
                <option value="完了" {{ old('status', $task->status) == '完了' ? 'selected' : '' }}>完了</option>
            </select>
        </div>

        <button type="submit">更新</button>
        <a href="{{ route('tasks.show', $task) }}">キャンセル</a>
    </form>
</body>
</html>
```

---

### 🔍 @method('PUT')

HTMLフォームは、`GET`と`POST`しかサポートしていません。

`PUT`や`DELETE`を使うには、`@method('PUT')`を追加します。

```blade
@method('PUT')
```

これにより、Laravelは`POST`リクエストを`PUT`リクエストとして扱います。

---

### 🔍 old()の第2引数

`old()`関数の第2引数は、**デフォルト値**です。

```blade
<input type="text" id="title" name="title" value="{{ old('title', $task->title) }}" required>
```

*   バリデーションエラーがある場合: `old('title')`が返される
*   バリデーションエラーがない場合: `$task->title`が返される

---

### 🔍 コントローラーのupdateメソッド

タスクを更新する`update`メソッドを追加します。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function update(Request $request, Task $task)
{
    // 認可チェック：ログインユーザーのタスクかどうか
    if ($task->user_id !== auth()->id()) {
        abort(403, 'このタスクを編集する権限がありません。');
    }

    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'description' => 'nullable|string',
        'due_date' => 'nullable|date',
        'status' => 'required|in:未完了,完了',
    ]);

    $task->update($validated);

    return redirect()->route('tasks.show', $task)->with('success', 'タスクを更新しました。');
}
```

---

### 🔍 タスク詳細ページに編集リンクを追加

タスク詳細ページに、編集リンクを追加します。

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
<a href="{{ route('tasks.index') }}">一覧に戻る</a>
```

---

### 🔍 動作確認

ブラウザでタスク詳細ページにアクセスし、「編集」リンクをクリックします。

タスク編集フォームが表示され、既存のデータが入力されていることを確認します。

1. タイトルを「更新されたタスク」に変更
2. 「更新」ボタンをクリック

タスク詳細ページにリダイレクトされ、「タスクを更新しました。」というメッセージが表示されることを確認します。

---

### 💡 TIP: fill()メソッド

`update()`メソッドの代わりに、`fill()`メソッドと`save()`メソッドを使うこともできます。

```php
$task->fill($validated);
$task->save();
```

---

### 🚨 よくある間違い

#### 間違い1: @method('PUT')を忘れる

**対処法**: フォームに`@method('PUT')`を追加します。

---

#### 間違い2: old()の第2引数を忘れる

**対処法**: `old('title', $task->title)`のように、第2引数にデフォルト値を指定します。

---

#### 間違い3: 認可チェックを忘れる

**対処法**: `edit`メソッドと`update`メソッドで、ログインユーザーのタスクかどうかを確認します。

---

## ✨ まとめ

このセクションでは、タスク編集機能を実装しました。

*   タスク編集フォームを実装し、既存のデータを表示できるようにした。
*   タスクを更新する機能を実装した。
*   認可を実装し、他のユーザーのタスクを編集できないようにした。

次のセクションでは、タスク削除の実装について学びます。

---

## 📝 学習のポイント

- [ ] タスク編集フォームを実装した。
- [ ] @method('PUT')を使った。
- [ ] old()の第2引数を使った。
- [ ] 認可チェックを実装した。
