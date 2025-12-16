# Tutorial 11-2-3: タスク作成の実装

## 🎯 このセクションで学ぶこと

- タスク作成フォームを実装する方法を学ぶ
- バリデーションを実装し、不正なデータを防ぐ方法を学ぶ
- フラッシュメッセージを表示し、ユーザーに操作結果を伝える方法を学ぶ

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
| Step 1 | ルーティングの追加 | フォーム表示と保存の2つのURLが必要 |
| Step 2 | createメソッドの実装 | フォームを表示するメソッド |
| Step 3 | 作成フォームのビュー作成 | ユーザーが入力する画面 |
| Step 4 | storeメソッドの実装 | データを保存するメソッド |
| Step 5 | フラッシュメッセージの表示 | 操作結果をユーザーに伝える |
| Step 6 | 動作確認 | 正しく動作するか確認する |

> 💡 **ポイント**: 「作成」機能は2つのルートが必要です。フォーム表示（GET）とデータ保存（POST）です。

---

## Step 1: ルーティングの追加

### 1-1. 作成用のルートを定義する

タスク作成には2つのルートが必要です。

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

### 1-2. コードリーディング

#### `Route::get('/tasks/create', ...)->name('tasks.create')`

- `GET /tasks/create`にアクセスすると、`create`メソッドが実行されます
- このルートは**フォームを表示する**ためのものです

---

#### `Route::post('/tasks', ...)->name('tasks.store')`

- `POST /tasks`にデータを送信すると、`store`メソッドが実行されます
- このルートは**データを保存する**ためのものです

---

#### なぜ2つのルートが必要なのか？

| ルート | HTTPメソッド | 役割 |
|--------|-------------|------|
| `/tasks/create` | GET | フォームを表示する |
| `/tasks` | POST | データを保存する |

フォーム表示と保存を分けることで、**責務が明確**になります。

---

## Step 2: createメソッドの実装

### 2-1. フォーム表示メソッドを追加する

タスク作成フォームを表示する`create`メソッドを追加します。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function create()
{
    return view('tasks.create');
}
```

---

### 2-2. コードリーディング

#### `return view('tasks.create')`

- `resources/views/tasks/create.blade.php`ファイルを表示します
- `create`メソッドはフォームを表示するだけなので、シンプルです

---

## Step 3: 作成フォームのビュー作成

### 3-1. ビューファイルを作成する

タスク作成フォームのビューを作成します。

**ファイル**: `resources/views/tasks/create.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>タスク作成</title>
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
            background-color: #4CAF50;
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
    <h1>タスク作成</h1>

    @if ($errors->any())
        <div class="error">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form method="POST" action="{{ route('tasks.store') }}">
        @csrf

        <div class="form-group">
            <label for="title">タイトル</label>
            <input type="text" id="title" name="title" value="{{ old('title') }}" required>
        </div>

        <div class="form-group">
            <label for="description">説明</label>
            <textarea id="description" name="description" rows="4">{{ old('description') }}</textarea>
        </div>

        <div class="form-group">
            <label for="due_date">期限</label>
            <input type="date" id="due_date" name="due_date" value="{{ old('due_date') }}">
        </div>

        <div class="form-group">
            <label for="status">ステータス</label>
            <select id="status" name="status">
                <option value="pending" {{ old('status') == 'pending' ? 'selected' : '' }}>未着手</option>
                <option value="in_progress" {{ old('status') == 'in_progress' ? 'selected' : '' }}>進行中</option>
                <option value="completed" {{ old('status') == 'completed' ? 'selected' : '' }}>完了</option>
            </select>
        </div>

        <button type="submit">作成</button>
        <a href="{{ route('tasks.index') }}" class="cancel-link">キャンセル</a>
    </form>
</body>
</html>
```

---

### 3-2. コードリーディング

#### `@csrf`

- **CSRF（クロスサイトリクエストフォージェリ）対策**のためのトークンを生成します
- フォームを送信するときに、このトークンがないとエラーになります
- Laravelが自動的にトークンを検証し、不正なリクエストを防ぎます

---

#### `{{ old('title') }}`

- `old()`ヘルパー関数は、**バリデーションエラー時に入力した値を保持**します
- エラーが発生しても、ユーザーが入力した値が消えないので、再入力の手間が省けます

---

#### `@if ($errors->any())`

- バリデーションエラーがある場合、エラーメッセージを表示します
- `$errors`は、Laravelが自動的にビューに渡すエラーバッグです

---

## Step 4: storeメソッドの実装

### 4-1. データ保存メソッドを追加する

タスクを保存する`store`メソッドを追加します。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'description' => 'nullable|string',
        'due_date' => 'nullable|date',
        'status' => 'required|in:pending,in_progress,completed',
    ]);

    $validated['user_id'] = auth()->id();

    Task::create($validated);

    return redirect()->route('tasks.index')->with('success', 'タスクを作成しました。');
}
```

---

### 4-2. コードリーディング

#### `$request->validate([...])`

- リクエストデータをバリデーションします
- バリデーションに失敗すると、自動的に前のページにリダイレクトされます

---

#### バリデーションルールの解説

| フィールド | ルール | 説明 |
|---|---|---|
| `title` | `required` | 必須項目 |
| `title` | `string` | 文字列型 |
| `title` | `max:255` | 最大255文字 |
| `description` | `nullable` | 空でも良い |
| `due_date` | `date` | 日付形式 |
| `status` | `in:pending,in_progress,completed` | 指定した値のみ許可 |

---

#### `$validated['user_id'] = auth()->id()`

- ログインしているユーザーのIDを取得し、`user_id`に設定します
- これにより、タスクがどのユーザーのものか紐付けられます

---

#### `Task::create($validated)`

- バリデーション済みのデータを使って、新しいタスクを作成します
- `create()`メソッドは、データベースにレコードを挿入します

---

#### `return redirect()->route('tasks.index')->with('success', '...')`

- タスク一覧ページにリダイレクトします
- `with('success', '...')`で、フラッシュメッセージをセッションに保存します

---

## Step 5: フラッシュメッセージの表示

### 5-1. 一覧画面にメッセージ表示を追加する

タスク作成後に、フラッシュメッセージを表示します。

**ファイル**: `resources/views/tasks/index.blade.php`

一覧画面の`<h1>`タグの下に、以下のコードを追加します。

```blade
@if (session('success'))
    <div style="color: green; margin-bottom: 15px; padding: 10px; background-color: #e8f5e9; border-radius: 4px;">
        {{ session('success') }}
    </div>
@endif

<a href="{{ route('tasks.create') }}" style="display: inline-block; margin-bottom: 15px; padding: 10px 20px; background-color: #4CAF50; color: white; text-decoration: none; border-radius: 4px;">新規作成</a>
```

---

### 5-2. コードリーディング

#### `session('success')`

- セッションから`success`キーの値を取得します
- `with('success', '...')`で保存した値が取得できます
- フラッシュメッセージは**1回のリクエストでのみ有効**です

---

## Step 6: 動作確認

### 6-1. フォーム表示を確認する

ブラウザで`http://localhost/tasks/create`にアクセスし、タスク作成フォームが表示されることを確認します。

---

### 6-2. タスクを作成する

1. タイトルに「新しいタスク」と入力
2. 説明に「これは新しいタスクの説明です。」と入力
3. 期限に「2024-12-31」と入力
4. ステータスに「未着手」を選択
5. 「作成」ボタンをクリック

タスク一覧ページにリダイレクトされ、「タスクを作成しました。」というメッセージが表示されることを確認します。

---

### 6-3. バリデーションエラーを確認する

1. タイトルを空にして「作成」ボタンをクリック
2. 「タイトルは必須です。」というエラーメッセージが表示される

---

## 🚨 よくある間違い

### 間違い1: @csrfを忘れる

**エラー**:

```
419 | Page Expired
```

**対処法**: フォームに`@csrf`を追加します。

---

### 間違い2: user_idを設定していない

**エラー**:

```
SQLSTATE[HY000]: General error: 1364 Field 'user_id' doesn't have a default value
```

**対処法**: `store`メソッドで`user_id`を設定します。

```php
$validated['user_id'] = auth()->id();
```

---

### 間違い3: バリデーションエラーが表示されない

**対処法**: ビューに`@if ($errors->any())`を追加します。

---

## 💡 TIP: バリデーションルールのカスタマイズ

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

## ✨ まとめ

このセクションでは、タスク作成機能を実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | 作成機能には2つのルート（GET/POST）が必要 |
| Step 2 | `create`メソッドでフォームを表示する |
| Step 3 | フォームには`@csrf`と`old()`が必要 |
| Step 4 | `store`メソッドでバリデーションと保存を行う |
| Step 5 | フラッシュメッセージで操作結果を伝える |
| Step 6 | 動作確認とエラー確認の方法 |

次のセクションでは、タスク詳細の実装について学びます。

---

## 📝 学習のポイント

- [ ] タスク作成フォームを実装した
- [ ] バリデーションを実装した
- [ ] フラッシュメッセージを表示した
- [ ] `old()`ヘルパー関数を使った
- [ ] `@csrf`の役割を理解した
