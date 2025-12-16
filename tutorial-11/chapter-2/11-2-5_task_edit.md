# Tutorial 11-2-5: タスク編集の実装

## 🎯 このセクションで学ぶこと

- タスク編集フォームを実装する方法を学ぶ
- 既存のデータをフォームに表示する方法を学ぶ
- タスクを更新する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ『詳細表示』の次に『編集』を実装するのか？」

詳細表示ができたら、次は「編集」機能です。なぜ「削除」ではないのでしょうか？

---

### 理由1: 「作成」と「詳細」の知識を組み合わせる

「編集」機能は、**「作成」と「詳細」の組み合わせ**です。

- **「作成」から**: フォーム、バリデーション、保存処理
- **「詳細」から**: IDで1件取得、ルートパラメータ

これまでの知識を活かせるので、スムーズに実装できます。

---

### 理由2: 既存データの表示が必要

編集画面では、**現在のデータをフォームに表示**する必要があります。

```php
// 編集画面：既存データを取得してフォームに表示
$task = Task::findOrFail($id);
return view('tasks.edit', compact('task'));
```

これは「詳細表示」で学んだ知識を応用しています。

---

### 理由3: HTTPメソッドの違いを学ぶ

「作成」と「編集」では、HTTPメソッドが異なります。

| 機能 | HTTPメソッド | 理由 |
|------|-------------|------|
| 作成 | POST | 新しいリソースを作る |
| 編集 | PUT/PATCH | 既存のリソースを更新する |

LaravelではBladeで`@method('PUT')`を使って、PUTリクエストを送信します。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | ルーティングの追加 | edit()とupdate()の2つのルート |
| Step 2 | editメソッドの実装 | 既存データを取得してフォームに表示 |
| Step 3 | 編集フォームのビュー作成 | 既存データを表示したフォーム |
| Step 4 | updateメソッドの実装 | データを更新するメソッド |
| Step 5 | 詳細ページに編集リンクを追加 | 編集ページへの導線を作る |
| Step 6 | 動作確認 | 正しく動作するか確認する |

> 💡 **ポイント**: 「作成」との違いは、①既存データの取得、②HTTPメソッド（PUT）、③更新処理の3点です。

---

## Step 1: ルーティングの追加

### 1-1. 編集用のルートを定義する

タスク編集には2つのルートが必要です。

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

### 1-2. コードリーディング

#### `Route::get('/tasks/{task}/edit', ...)->name('tasks.edit')`

- `GET /tasks/1/edit`にアクセスすると、`edit`メソッドが実行されます
- このルートは**編集フォームを表示する**ためのものです

---

#### `Route::put('/tasks/{task}', ...)->name('tasks.update')`

- `PUT /tasks/1`にデータを送信すると、`update`メソッドが実行されます
- このルートは**データを更新する**ためのものです

---

#### 作成と編集の比較

| 機能 | フォーム表示 | データ保存 |
|------|-------------|-----------|
| 作成 | GET `/tasks/create` | POST `/tasks` |
| 編集 | GET `/tasks/{task}/edit` | PUT `/tasks/{task}` |

---

## Step 2: editメソッドの実装

### 2-1. フォーム表示メソッドを追加する

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

### 2-2. コードリーディング

#### `edit(Task $task)`

- ルートモデルバインディングで、URLのIDから自動的にタスクを取得します
- 取得したタスクをビューに渡します

---

#### 認可チェック

- `show`メソッドと同様に、ログインユーザーのタスクかどうかを確認します
- 他のユーザーのタスクを編集できないようにします

---

## Step 3: 編集フォームのビュー作成

### 3-1. ビューファイルを作成する

タスク編集フォームのビューを作成します。

**ファイル**: `resources/views/tasks/edit.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>タスク編集</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"],
        input[type="date"],
        textarea,
        select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .error {
            color: red;
            margin-bottom: 15px;
        }
        button {
            background-color: #2196f3;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .cancel-link {
            margin-left: 10px;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>タスク編集</h1>

    @if ($errors->any())
        <div class="error">
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

        <div class="form-group">
            <label for="title">タイトル</label>
            <input type="text" id="title" name="title" value="{{ old('title', $task->title) }}" required>
        </div>

        <div class="form-group">
            <label for="description">説明</label>
            <textarea id="description" name="description" rows="4">{{ old('description', $task->description) }}</textarea>
        </div>

        <div class="form-group">
            <label for="due_date">期限</label>
            <input type="date" id="due_date" name="due_date" value="{{ old('due_date', $task->due_date?->format('Y-m-d')) }}">
        </div>

        <div class="form-group">
            <label for="status">ステータス</label>
            <select id="status" name="status">
                <option value="pending" {{ old('status', $task->status) == 'pending' ? 'selected' : '' }}>未着手</option>
                <option value="in_progress" {{ old('status', $task->status) == 'in_progress' ? 'selected' : '' }}>進行中</option>
                <option value="completed" {{ old('status', $task->status) == 'completed' ? 'selected' : '' }}>完了</option>
            </select>
        </div>

        <button type="submit">更新</button>
        <a href="{{ route('tasks.show', $task) }}" class="cancel-link">キャンセル</a>
    </form>
</body>
</html>
```

---

### 3-2. コードリーディング

#### `@method('PUT')`

- HTMLフォームは、`GET`と`POST`しかサポートしていません
- `@method('PUT')`を追加すると、Laravelは`POST`リクエストを`PUT`リクエストとして扱います
- これにより、RESTfulなルーティングを実現できます

---

#### `old('title', $task->title)`

- `old()`関数の第2引数は**デフォルト値**です
- バリデーションエラーがある場合: `old('title')`が返される（ユーザーが入力した値）
- バリデーションエラーがない場合: `$task->title`が返される（既存のデータ）

---

#### `$task->due_date?->format('Y-m-d')`

- `?->`は**Nullセーフ演算子**です
- `due_date`がNULLの場合、エラーにならずにNULLを返します
- `<input type="date">`には`Y-m-d`形式の値が必要です

---

## Step 4: updateメソッドの実装

### 4-1. データ更新メソッドを追加する

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
        'status' => 'required|in:pending,in_progress,completed',
    ]);

    $task->update($validated);

    return redirect()->route('tasks.show', $task)->with('success', 'タスクを更新しました。');
}
```

---

### 4-2. コードリーディング

#### `update(Request $request, Task $task)`

- 第1引数`$request`でフォームデータを受け取ります
- 第2引数`$task`でルートモデルバインディングにより対象のタスクを取得します

---

#### `$task->update($validated)`

- `update()`メソッドは、モデルのデータを更新します
- バリデーション済みのデータのみを更新するので、安全です

---

#### `store()`と`update()`の違い

| メソッド | 処理 |
|---------|------|
| `store()` | `Task::create($validated)` - 新規作成 |
| `update()` | `$task->update($validated)` - 既存データを更新 |

---

## Step 5: 詳細ページに編集リンクを追加

### 5-1. 編集リンクを追加する

タスク詳細ページに、編集リンクを追加します。

**ファイル**: `resources/views/tasks/show.blade.php`

テーブルの下に、以下のコードを追加します。

```blade
@if (session('success'))
    <div style="color: green; margin-bottom: 15px; padding: 10px; background-color: #e8f5e9; border-radius: 4px;">
        {{ session('success') }}
    </div>
@endif

<!-- テーブルの後に追加 -->
<div style="margin-top: 20px;">
    <a href="{{ route('tasks.edit', $task) }}" style="display: inline-block; padding: 10px 20px; background-color: #2196f3; color: white; text-decoration: none; border-radius: 4px;">編集</a>
    <a href="{{ route('tasks.index') }}" style="margin-left: 10px; color: #666;">← 一覧に戻る</a>
</div>
```

---

### 5-2. コードリーディング

#### `route('tasks.edit', $task)`

- `tasks.edit`という名前のルートにURLを生成します
- 結果: `/tasks/1/edit`のようなURLが生成されます

---

## Step 6: 動作確認

### 6-1. 編集フォームを表示する

1. ブラウザでタスク詳細ページにアクセスする
2. 「編集」リンクをクリックする
3. タスク編集フォームが表示され、既存のデータが入力されていることを確認する

---

### 6-2. タスクを更新する

1. タイトルを「更新されたタスク」に変更
2. 「更新」ボタンをクリック
3. タスク詳細ページにリダイレクトされる
4. 「タスクを更新しました。」というメッセージが表示される
5. タイトルが「更新されたタスク」に変更されていることを確認する

---

### 6-3. バリデーションエラーを確認する

1. タイトルを空にして「更新」ボタンをクリック
2. エラーメッセージが表示される
3. 他のフィールドの値が保持されていることを確認する

---

## 🚨 よくある間違い

### 間違い1: @method('PUT')を忘れる

**エラー**:

```
The PUT method is not supported for route tasks/{task}. Supported methods: GET, HEAD, POST.
```

**対処法**: フォームに`@method('PUT')`を追加します。

---

### 間違い2: old()の第2引数を忘れる

**問題**: 編集画面を開いたとき、フォームが空になる

**対処法**: `old('title', $task->title)`のように、第2引数にデフォルト値を指定します。

---

### 間違い3: 認可チェックを忘れる

**問題**: 他のユーザーのタスクを編集できてしまう

**対処法**: `edit`メソッドと`update`メソッドの両方で、認可チェックを行います。

---

## 💡 TIP: fill()メソッド

`update()`メソッドの代わりに、`fill()`メソッドと`save()`メソッドを使うこともできます。

```php
$task->fill($validated);
$task->save();
```

`fill()`は値をセットするだけで、`save()`を呼ぶまでデータベースに保存されません。

---

## ✨ まとめ

このセクションでは、タスク編集機能を実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | 編集機能には2つのルート（GET/PUT）が必要 |
| Step 2 | `edit`メソッドで既存データを取得してフォームに表示 |
| Step 3 | `@method('PUT')`でHTTPメソッドを指定 |
| Step 4 | `$task->update()`でデータを更新 |
| Step 5 | 詳細ページから編集ページへの導線を作る |
| Step 6 | 動作確認とエラー確認の方法 |

次のセクションでは、タスク削除の実装について学びます。

---

## 📝 学習のポイント

- [ ] タスク編集フォームを実装した
- [ ] `@method('PUT')`を使った
- [ ] `old()`の第2引数を使った
- [ ] 認可チェックを実装した
- [ ] 作成と編集の違いを理解した
