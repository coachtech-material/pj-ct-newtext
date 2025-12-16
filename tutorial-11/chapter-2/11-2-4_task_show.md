# Tutorial 11-2-4: タスク詳細の実装

## 🎯 このセクションで学ぶこと

*   タスク詳細ページを実装する方法を学ぶ。
*   ルートモデルバインディングを使って、コードを簡潔にする方法を学ぶ。
*   認可を実装し、他のユーザーのタスクを表示できないようにする方法を学ぶ。

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ『作成』の次に『詳細表示』を実装するのか？」

「作成」機能ができたら、次は「詳細表示」です。なぜ「編集」や「削除」ではないのでしょうか？

---

### 理由1: 個別データの取得パターンを学ぶ

一覧表示では`Task::all()`で全件取得しました。詳細表示では`Task::find($id)`で**1件だけ取得**します。

この「IDで1件取得」というパターンは、「編集」「削除」でも使うので、**先に詳細表示で学んでおくと効率的**です。

---

### 理由2: ルートパラメータを学ぶ

詳細表示では、URLに`/tasks/1`のように**IDを含めます**。

```
/tasks/{id}  ← このIDをコントローラーで受け取る
```

このルートパラメータの仕組みは、「編集」「削除」でも使います。

---

### 理由3: 存在しないデータへのアクセスを考える

「IDが存在しない場合はどうなる？」という問題に初めて直面します。

ここで**404エラーの処理**を学びます。これも「編集」「削除」で必要な知識です。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| 1 | ルーティング追加 | `/tasks/{id}`のようなパラメータ付きURL |
| 2 | コントローラー実装 | `find()`で1件取得 |
| 3 | ビュー作成 | 詳細情報を表示 |

> 💡 **ポイント**: `findOrFail()`を使うと、データが存在しない場合に自動で404エラーを返します。

---

## 導入：なぜタスク詳細機能が重要なのか

**タスク詳細機能**は、タスクの詳細情報を表示する機能です。

タスク詳細機能を実装することで、ユーザーはタスクの全ての情報を確認できるようになります。

---

## 詳細解説

### 🔍 ルーティングの追加

タスク詳細のルーティングを追加します。

**ファイル**: `routes/web.php`

```php
Route::middleware(['auth'])->group(function () {
    Route::get('/tasks', [TaskController::class, 'index'])->name('tasks.index');
    Route::get('/tasks/create', [TaskController::class, 'create'])->name('tasks.create');
    Route::post('/tasks', [TaskController::class, 'store'])->name('tasks.store');
    Route::get('/tasks/{task}', [TaskController::class, 'show'])->name('tasks.show');
});
```

---

### 🔍 ルートモデルバインディング

`{task}`は、**ルートモデルバインディング**と呼ばれる機能です。

ルートモデルバインディングを使うと、**URLのIDから自動的にモデルを取得**できます。

**従来の方法**:

```php
public function show($id)
{
    $task = Task::findOrFail($id);
    return view('tasks.show', compact('task'));
}
```

**ルートモデルバインディングを使った方法**:

```php
public function show(Task $task)
{
    return view('tasks.show', compact('task'));
}
```

ルートモデルバインディングを使うことで、コードが簡潔になります。

---

### 🔍 コントローラーのshowメソッド

タスク詳細を表示する`show`メソッドを追加します。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function show(Task $task)
{
    // 認可チェック：ログインユーザーのタスクかどうか
    if ($task->user_id !== auth()->id()) {
        abort(403, 'このタスクにアクセスする権限がありません。');
    }

    return view('tasks.show', compact('task'));
}
```

---

### 🔍 タスク詳細のビュー

タスク詳細のビューを作成します。

**ファイル**: `resources/views/tasks/show.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>タスク詳細</title>
</head>
<body>
    <h1>タスク詳細</h1>

    <table border="1">
        <tr>
            <th>ID</th>
            <td>{{ $task->id }}</td>
        </tr>
        <tr>
            <th>タイトル</th>
            <td>{{ $task->title }}</td>
        </tr>
        <tr>
            <th>説明</th>
            <td>{{ $task->description }}</td>
        </tr>
        <tr>
            <th>期限</th>
            <td>{{ $task->due_date }}</td>
        </tr>
        <tr>
            <th>ステータス</th>
            <td>{{ $task->status }}</td>
        </tr>
        <tr>
            <th>作成日時</th>
            <td>{{ $task->created_at }}</td>
        </tr>
        <tr>
            <th>更新日時</th>
            <td>{{ $task->updated_at }}</td>
        </tr>
    </table>

    <a href="{{ route('tasks.index') }}">一覧に戻る</a>
</body>
</html>
```

---

### 🔍 タスク一覧からタスク詳細へのリンク

タスク一覧ページに、タスク詳細へのリンクを追加します。

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
                </td>
            </tr>
        @endforeach
    </tbody>
</table>
```

---

### 🔍 動作確認

ブラウザでタスク一覧ページにアクセスし、「詳細」リンクをクリックします。

タスク詳細ページが表示され、タスクの全ての情報が表示されることを確認します。

---

### 🔍 認可チェックの動作確認

他のユーザーのタスクにアクセスできないか確認します。

1. ユーザーAでログインし、タスクを作成する
2. ログアウトする
3. ユーザーBでログインする
4. ブラウザで `http://localhost/tasks/1` にアクセスする
5. 「このタスクにアクセスする権限がありません。」というエラーが表示される

---

### 🔍 abort()関数

`abort()`関数は、**HTTPエラーを返す関数**です。

```php
abort(403, 'このタスクにアクセスする権限がありません。');
```

*   `403`: HTTPステータスコード（Forbidden）
*   `'このタスクにアクセスする権限がありません。'`: エラーメッセージ

---

### 🔍 日付のフォーマット

日付をフォーマットして表示します。

**ファイル**: `resources/views/tasks/show.blade.php`

```blade
<tr>
    <th>期限</th>
    <td>{{ $task->due_date ? \Carbon\Carbon::parse($task->due_date)->format('Y年m月d日') : '未設定' }}</td>
</tr>
<tr>
    <th>作成日時</th>
    <td>{{ $task->created_at->format('Y年m月d日 H:i:s') }}</td>
</tr>
<tr>
    <th>更新日時</th>
    <td>{{ $task->updated_at->format('Y年m月d日 H:i:s') }}</td>
</tr>
```

---

### 💡 TIP: ルートモデルバインディングのカスタマイズ

ルートモデルバインディングは、カスタマイズできます。

**例**: `id`以外のカラムで検索する

**ファイル**: `app/Models/Task.php`

```php
public function getRouteKeyName()
{
    return 'slug';  // slugカラムで検索
}
```

---

### 🚨 よくある間違い

#### 間違い1: 認可チェックを忘れる

**対処法**: `show`メソッドで、ログインユーザーのタスクかどうかを確認します。

---

#### 間違い2: ルートモデルバインディングを使っていない

**対処法**: `show(Task $task)`のように、型ヒントを使います。

---

#### 間違い3: 存在しないタスクにアクセスした場合のエラー処理

**対処法**: ルートモデルバインディングを使うと、存在しないタスクにアクセスした場合、自動的に`404 Not Found`エラーが返されます。

---

## ✨ まとめ

このセクションでは、タスク詳細機能を実装しました。

*   タスク詳細ページを実装し、タスクの全ての情報を表示できるようにした。
*   ルートモデルバインディングを使って、コードを簡潔にした。
*   認可を実装し、他のユーザーのタスクを表示できないようにした。

次のセクションでは、タスク編集の実装について学びます。

---

## 📝 学習のポイント

- [ ] タスク詳細ページを実装した。
- [ ] ルートモデルバインディングを使った。
- [ ] 認可チェックを実装した。
- [ ] abort()関数を使った。
