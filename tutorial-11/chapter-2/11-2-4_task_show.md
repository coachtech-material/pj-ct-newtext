# Tutorial 11-2-4: タスク詳細の実装

## 🎯 このセクションで学ぶこと

- タスク詳細ページを実装する方法を学ぶ
- ルートモデルバインディングを使って、コードを簡潔にする方法を学ぶ
- 認可を実装し、他のユーザーのタスクを表示できないようにする方法を学ぶ

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
| Step 1 | ルーティングの追加 | `/tasks/{id}`のようなパラメータ付きURL |
| Step 2 | showメソッドの実装 | ルートモデルバインディングで1件取得 |
| Step 3 | 詳細ビューの作成 | タスク情報を表示する画面 |
| Step 4 | 一覧からのリンク追加 | 詳細ページへの導線を作る |
| Step 5 | 動作確認 | 正しく動作するか確認する |

> 💡 **ポイント**: ルートモデルバインディングを使うと、データが存在しない場合に自動で404エラーを返します。

---

## Step 1: ルーティングの追加

### 1-1. 詳細表示用のルートを定義する

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

### 1-2. コードリーディング

#### `Route::get('/tasks/{task}', ...)`

- `{task}`は**ルートパラメータ**です
- URLの`/tasks/1`にアクセスすると、`1`が`{task}`に入ります
- この値はコントローラーで受け取ることができます

---

#### ルートの順番に注意

```php
Route::get('/tasks/create', ...);  // 先に定義
Route::get('/tasks/{task}', ...);  // 後に定義
```

`/tasks/create`を先に定義しないと、`create`が`{task}`パラメータとして解釈されてしまいます。

---

## Step 2: showメソッドの実装

### 2-1. コントローラーにshowメソッドを追加する

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

### 2-2. コードリーディング

#### ルートモデルバインディングとは

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

引数に`Task $task`と型ヒントを書くだけで、**URLのIDから自動的にモデルを取得**してくれます。

---

#### `if ($task->user_id !== auth()->id())`

- タスクの所有者とログインユーザーが一致するか確認します
- 一致しない場合は、403エラーを返します
- これにより、**他のユーザーのタスクを見られない**ようにします

---

#### `abort(403, '...')`

- `abort()`関数は、**HTTPエラーを返す関数**です
- `403`は「Forbidden（禁止）」を意味するHTTPステータスコードです
- 第2引数はエラーメッセージです

---

## Step 3: 詳細ビューの作成

### 3-1. ビューファイルを作成する

タスク詳細のビューを作成します。

**ファイル**: `resources/views/tasks/show.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>タスク詳細</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            width: 150px;
        }
        .back-link {
            display: inline-block;
            margin-top: 20px;
            color: #2196f3;
            text-decoration: none;
        }
        .status-pending {
            color: #ff9800;
        }
        .status-in_progress {
            color: #2196f3;
        }
        .status-completed {
            color: #4caf50;
        }
    </style>
</head>
<body>
    <h1>タスク詳細</h1>

    <table>
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
            <td>{{ $task->description ?? '未設定' }}</td>
        </tr>
        <tr>
            <th>期限</th>
            <td>{{ $task->due_date ? $task->due_date->format('Y年m月d日') : '未設定' }}</td>
        </tr>
        <tr>
            <th>ステータス</th>
            <td class="status-{{ $task->status }}">
                @if($task->status === 'pending')
                    未着手
                @elseif($task->status === 'in_progress')
                    進行中
                @elseif($task->status === 'completed')
                    完了
                @endif
            </td>
        </tr>
        <tr>
            <th>作成日時</th>
            <td>{{ $task->created_at->format('Y年m月d日 H:i:s') }}</td>
        </tr>
        <tr>
            <th>更新日時</th>
            <td>{{ $task->updated_at->format('Y年m月d日 H:i:s') }}</td>
        </tr>
    </table>

    <a href="{{ route('tasks.index') }}" class="back-link">← 一覧に戻る</a>
</body>
</html>
```

---

### 3-2. コードリーディング

#### `{{ $task->description ?? '未設定' }}`

- `??`は**Null合体演算子**です
- `$task->description`がNULLの場合、「未設定」を表示します

---

#### `$task->due_date->format('Y年m月d日')`

- `due_date`はCarbonオブジェクトなので、`format()`メソッドが使えます
- `Y年m月d日`の形式で日付を表示します

---

## Step 4: 一覧からのリンク追加

### 4-1. 一覧ページに詳細リンクを追加する

タスク一覧ページに、タスク詳細へのリンクを追加します。

**ファイル**: `resources/views/tasks/index.blade.php`

テーブルの`<thead>`に「操作」列を追加し、`<tbody>`に詳細リンクを追加します。

```blade
<table>
    <thead>
        <tr>
            <th>ID</th>
            <th>タイトル</th>
            <th>ステータス</th>
            <th>期限</th>
            <th>操作</th>
        </tr>
    </thead>
    <tbody>
        @foreach($tasks as $task)
            <tr>
                <td>{{ $task->id }}</td>
                <td>{{ $task->title }}</td>
                <td class="status-{{ $task->status }}">
                    @if($task->status === 'pending')
                        未着手
                    @elseif($task->status === 'in_progress')
                        進行中
                    @elseif($task->status === 'completed')
                        完了
                    @endif
                </td>
                <td>{{ $task->due_date ? $task->due_date->format('Y年m月d日') : '未設定' }}</td>
                <td>
                    <a href="{{ route('tasks.show', $task) }}">詳細</a>
                </td>
            </tr>
        @endforeach
    </tbody>
</table>
```

---

### 4-2. コードリーディング

#### `route('tasks.show', $task)`

- `tasks.show`という名前のルートにURLを生成します
- 第2引数に`$task`を渡すと、自動的に`$task->id`がURLに埋め込まれます
- 結果: `/tasks/1`のようなURLが生成されます

---

## Step 5: 動作確認

### 5-1. 詳細ページを表示する

1. ブラウザでタスク一覧ページにアクセスする
2. 任意のタスクの「詳細」リンクをクリックする
3. タスク詳細ページが表示され、全ての情報が表示されることを確認する

---

### 5-2. 認可チェックを確認する

他のユーザーのタスクにアクセスできないか確認します。

1. ユーザーAでログインし、タスクを作成する
2. ログアウトする
3. ユーザーBでログインする
4. ブラウザで`http://localhost/tasks/1`にアクセスする
5. 「このタスクにアクセスする権限がありません。」というエラーが表示される

---

### 5-3. 存在しないタスクにアクセスする

1. ブラウザで`http://localhost/tasks/9999`にアクセスする
2. 404エラーが表示される

ルートモデルバインディングを使うと、存在しないIDにアクセスした場合、自動的に404エラーが返されます。

---

## 🚨 よくある間違い

### 間違い1: 認可チェックを忘れる

**問題**: 他のユーザーのタスクが見えてしまう

**対処法**: `show`メソッドで、ログインユーザーのタスクかどうかを確認します。

```php
if ($task->user_id !== auth()->id()) {
    abort(403, 'このタスクにアクセスする権限がありません。');
}
```

---

### 間違い2: ルートの順番が間違っている

**問題**: `/tasks/create`にアクセスすると404エラーになる

**対処法**: `/tasks/create`を`/tasks/{task}`より先に定義します。

---

### 間違い3: 型ヒントを忘れる

**問題**: ルートモデルバインディングが動作しない

**対処法**: `show(Task $task)`のように、型ヒントを書きます。

---

## 💡 TIP: ルートモデルバインディングのカスタマイズ

デフォルトでは`id`カラムで検索しますが、カスタマイズできます。

**例**: `slug`カラムで検索する

**ファイル**: `app/Models/Task.php`

```php
public function getRouteKeyName()
{
    return 'slug';  // slugカラムで検索
}
```

これにより、`/tasks/my-first-task`のようなURLでアクセスできます。

---

## ✨ まとめ

このセクションでは、タスク詳細機能を実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | ルートパラメータ`{task}`の使い方 |
| Step 2 | ルートモデルバインディングで自動的にモデルを取得 |
| Step 3 | 詳細ビューでタスク情報を表示 |
| Step 4 | `route()`ヘルパーでURLを生成 |
| Step 5 | 認可チェックと404エラーの確認 |

次のセクションでは、タスク編集の実装について学びます。

---

## 📝 学習のポイント

- [ ] タスク詳細ページを実装した
- [ ] ルートモデルバインディングを使った
- [ ] 認可チェックを実装した
- [ ] `abort()`関数を使った
- [ ] ルートパラメータの仕組みを理解した
