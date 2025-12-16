# Tutorial 11-2-3: タスク作成の実装

## 🎯 このセクションで学ぶこと

*   タスク作成フォームを実装する方法を学ぶ。
*   バリデーションを実装し、不正なデータを防ぐ方法を学ぶ。
*   フラッシュメッセージを表示し、ユーザーに操作結果を伝える方法を学ぶ。

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ一覧表示の次に『作成』を実装するのか？」

一覧画面ができたら、次は「作成」機能です。なぜ「詳細」や「編集」ではなく「作成」なのでしょうか？

---

### 理由1: データがないと他の機能をテストできない

現在、データベースにはテストデータしかありません。

「作成」機能があれば、**画面からデータを追加できる**ようになります。これにより、「詳細」「編集」「削除」のテストがしやすくなります。

---

### 理由2: フォームの基本を学べる

「作成」機能では、以下の重要な概念を学びます：

- **フォームの作成**：ユーザーからの入力を受け付ける
- **バリデーション**：不正なデータを防ぐ
- **リダイレクト**：保存後に一覧画面に戻る
- **フラッシュメッセージ**：操作結果をユーザーに伝える

これらは「編集」機能でも使うので、**先に「作成」で学んでおくと効率的**です。

---

### 理由3: 一覧画面で動作確認できる

「作成」機能を実装したら、一覧画面で**新しいデータが表示されるか確認**できます。

これが、一覧表示を先に作った理由の一つです。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| 1 | ルーティング追加 | フォーム表示と保存の2つのURLが必要 |
| 2 | コントローラー実装 | create()とstore()の2つのメソッド |
| 3 | バリデーション追加 | 不正なデータを防ぐ |
| 4 | ビュー作成 | フォームを表示する |

> 💡 **ポイント**: 「作成」機能は2つのルートが必要です。フォーム表示（GET）とデータ保存（POST）です。

---

## 導入：なぜタスク作成機能が重要なのか

**タスク作成機能**は、タスク管理システムの中核となる機能です。

タスク作成機能を実装することで、ユーザーは新しいタスクを追加できるようになります。

---

## 詳細解説

### 🔍 ルーティングの追加

タスク作成のルーティングを追加します。

**ファイル**: `routes/web.php`

```php
use App\Http\Controllers\TaskController;

Route::middleware(['auth'])->group(function () {
    Route::get('/tasks', [TaskController::class, 'index'])->name('tasks.index');
    Route::get('/tasks/create', [TaskController::class, 'create'])->name('tasks.create');
    Route::post('/tasks', [TaskController::class, 'store'])->name('tasks.store');
});
```

---

### 🔍 コントローラーのcreateメソッド

タスク作成フォームを表示する`create`メソッドを追加します。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function create()
{
    return view('tasks.create');
}
```

---

### 🔍 タスク作成フォームのビュー

タスク作成フォームのビューを作成します。

**ファイル**: `resources/views/tasks/create.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>タスク作成</title>
</head>
<body>
    <h1>タスク作成</h1>

    @if ($errors->any())
        <div style="color: red;">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form method="POST" action="{{ route('tasks.store') }}">
        @csrf

        <div>
            <label for="title">タイトル</label>
            <input type="text" id="title" name="title" value="{{ old('title') }}" required>
        </div>

        <div>
            <label for="description">説明</label>
            <textarea id="description" name="description">{{ old('description') }}</textarea>
        </div>

        <div>
            <label for="due_date">期限</label>
            <input type="date" id="due_date" name="due_date" value="{{ old('due_date') }}">
        </div>

        <div>
            <label for="status">ステータス</label>
            <select id="status" name="status">
                <option value="未完了" {{ old('status') == '未完了' ? 'selected' : '' }}>未完了</option>
                <option value="完了" {{ old('status') == '完了' ? 'selected' : '' }}>完了</option>
            </select>
        </div>

        <button type="submit">作成</button>
        <a href="{{ route('tasks.index') }}">キャンセル</a>
    </form>
</body>
</html>
```

---

### 🔍 コントローラーのstoreメソッド

タスクを保存する`store`メソッドを追加します。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'description' => 'nullable|string',
        'due_date' => 'nullable|date',
        'status' => 'required|in:未完了,完了',
    ]);

    $validated['user_id'] = auth()->id();

    Task::create($validated);

    return redirect()->route('tasks.index')->with('success', 'タスクを作成しました。');
}
```

---

### 🔍 バリデーションルールの解説

バリデーションルールを詳しく見ていきます。

| フィールド | ルール | 説明 |
|---|---|---|
| `title` | `required` | 必須項目 |
| `title` | `string` | 文字列型 |
| `title` | `max:255` | 最大255文字 |
| `description` | `nullable` | 空でも良い |
| `description` | `string` | 文字列型 |
| `due_date` | `nullable` | 空でも良い |
| `due_date` | `date` | 日付形式 |
| `status` | `required` | 必須項目 |
| `status` | `in:未完了,完了` | 「未完了」または「完了」のみ |

---

### 🔍 old()ヘルパー関数

`old()`ヘルパー関数は、**バリデーションエラー時に、入力した値を保持する**ための関数です。

```blade
<input type="text" id="title" name="title" value="{{ old('title') }}" required>
```

バリデーションエラーが発生した場合、ユーザーが入力した値が保持されるため、再入力の手間が省けます。

---

### 🔍 フラッシュメッセージの表示

タスク作成後に、フラッシュメッセージを表示します。

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>タスク一覧</title>
</head>
<body>
    <h1>タスク一覧</h1>

    @if (session('success'))
        <div style="color: green;">
            {{ session('success') }}
        </div>
    @endif

    <a href="{{ route('tasks.create') }}">新規作成</a>

    <table border="1">
        <thead>
            <tr>
                <th>ID</th>
                <th>タイトル</th>
                <th>期限</th>
                <th>ステータス</th>
            </tr>
        </thead>
        <tbody>
            @foreach ($tasks as $task)
                <tr>
                    <td>{{ $task->id }}</td>
                    <td>{{ $task->title }}</td>
                    <td>{{ $task->due_date }}</td>
                    <td>{{ $task->status }}</td>
                </tr>
            @endforeach
        </tbody>
    </table>
</body>
</html>
```

---

### 🔍 動作確認

ブラウザで `http://localhost/tasks/create` にアクセスし、タスク作成フォームが表示されることを確認します。

1. タイトルに「新しいタスク」と入力
2. 説明に「これは新しいタスクの説明です。」と入力
3. 期限に「2024-12-31」と入力
4. ステータスに「未完了」を選択
5. 「作成」ボタンをクリック

タスク一覧ページにリダイレクトされ、「タスクを作成しました。」というメッセージが表示されることを確認します。

---

### 🔍 バリデーションエラーの確認

バリデーションエラーが正しく表示されるか確認します。

1. タイトルを空にして「作成」ボタンをクリック
2. 「タイトルは必須です。」というエラーメッセージが表示される

---

### 💡 TIP: バリデーションルールのカスタマイズ

バリデーションルールは、カスタマイズできます。

**例**: タイトルを10文字以上にする

```php
$validated = $request->validate([
    'title' => 'required|string|min:10|max:255',
]);
```

**例**: 期限を今日以降にする

```php
$validated = $request->validate([
    'due_date' => 'nullable|date|after_or_equal:today',
]);
```

---

### 🚨 よくある間違い

#### 間違い1: @csrfを忘れる

**対処法**: フォームに`@csrf`を追加します。

---

#### 間違い2: user_idを設定していない

**対処法**: `store`メソッドで`user_id`を設定します。

```php
$validated['user_id'] = auth()->id();
```

---

#### 間違い3: バリデーションエラーが表示されない

**対処法**: ビューに`@if ($errors->any())`を追加します。

---

## ✨ まとめ

このセクションでは、タスク作成機能を実装しました。

*   タスク作成フォームを実装し、ユーザーが新しいタスクを追加できるようにした。
*   バリデーションを実装し、不正なデータを防いだ。
*   フラッシュメッセージを表示し、ユーザーに操作結果を伝えた。

次のセクションでは、タスク詳細の実装について学びます。

---

## 📝 学習のポイント

- [ ] タスク作成フォームを実装した。
- [ ] バリデーションを実装した。
- [ ] フラッシュメッセージを表示した。
- [ ] old()ヘルパー関数を使った。
