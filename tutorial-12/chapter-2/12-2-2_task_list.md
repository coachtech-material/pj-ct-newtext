# Tutorial 12-2-2: タスク一覧の実装

## 🎯 このセクションで学ぶこと

- タスク一覧ページを実装する方法を学ぶ
- Eloquent ORMを使ってデータを取得する方法を理解する
- Bladeテンプレートでデータを表示する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜCRUDの中で『一覧表示』を最初に作るのか？」

データベースとモデルができたら、次は画面を作ります。では、なぜCreate（作成）ではなくRead（一覧）から始めるのでしょうか？

---

### 理由1: データが正しく保存されているか確認できる

前のセクションでマイグレーションとモデルを作成しました。でも、本当に正しく動作しているのでしょうか？

一覧画面を作れば、Tinkerで追加したテストデータが表示されるかどうかで、**データベース連携が正しく動作しているか確認できます**。

---

### 理由2: 作成画面よりシンプル

一覧表示は、**データを取得して表示するだけ**です。

```
一覧表示: データ取得 → 表示
作成画面: フォーム表示 → 入力受付 → バリデーション → 保存 → リダイレクト
```

作成画面は複数の処理が必要ですが、一覧表示はシンプルなので、**まずは簡単なものから始めます**。

---

### 理由3: 作成後の確認に使える

一覧画面があれば、「作成」機能を実装した後に、**新しいデータが一覧に表示されるか確認できます**。

つまり、一覧画面は「作成」「編集」「削除」の**動作確認にも使える**のです。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | 実装の流れを理解する | 全体像を把握する |
| Step 2 | ルーティングの設定 | URLとコントローラーを紐付ける |
| Step 3 | コントローラーの作成と実装 | データを取得するロジックを書く |
| Step 4 | ビューの作成 | データを表示する画面を作る |
| Step 5 | 動作確認 | 正しく動作するか確認する |

この順番は、**リクエストの流れ**に沿っています：

```
ユーザーがURLにアクセス → ルーティング → コントローラー → ビュー
```

---

## Step 1: 実装の流れを理解する

タスク一覧ページを実装するには、以下の3つの要素が必要です。

1. **ルーティング**: URLとコントローラーのメソッドを紐付ける
2. **コントローラー**: データベースからデータを取得する
3. **ビュー**: データを表示する

```
[ブラウザ] → [ルーティング] → [コントローラー] → [ビュー] → [ブラウザ]
              /tasks         TaskController     tasks/index
                              →index()          .blade.php
```

---

## Step 2: ルーティングの設定

### 2-1. ルートを定義する

`routes/web.php`を開き、以下のルートを追加します。

**ファイル**: `routes/web.php`

```php
<?php

use App\Http\Controllers\TaskController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/tasks', [TaskController::class, 'index'])->name('tasks.index');
```

---

### 2-2. コードリーディング

#### `Route::get('/tasks', [TaskController::class, 'index'])->name('tasks.index')`

- `GET /tasks`というURLにアクセスしたら、`TaskController`の`index`メソッドを実行します
- `name('tasks.index')`は、このルートに`tasks.index`という名前を付けます
- 名前を付けることで、ビューやコントローラーから`route('tasks.index')`でURLを生成できるようになります

---

## Step 3: コントローラーの作成と実装

### 3-1. コントローラーを生成する

以下のコマンドを実行して、`TaskController`を作成します。

```bash
php artisan make:controller TaskController
```

**実行結果**:

```
Controller created successfully.
```

`app/Http/Controllers/`ディレクトリに、`TaskController.php`ファイルが作成されます。

---

### 3-2. indexアクションを実装する

作成されたコントローラーファイルを開き、以下のように編集します。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $tasks = Task::all();
        
        return view('tasks.index', compact('tasks'));
    }
}
```

---

### 3-3. コードリーディング

#### `use App\Models\Task;`

- `Task`モデルを使用するために、`use`文でインポートします

---

#### `$tasks = Task::all()`

- `Task`モデルを使って、`tasks`テーブルの全てのデータを取得します
- `all()`メソッドは、全てのレコードを取得します
- 取得したデータは、`$tasks`変数に格納されます

---

#### `return view('tasks.index', compact('tasks'))`

- `resources/views/tasks/index.blade.php`ファイルを表示します
- `compact('tasks')`は、`$tasks`変数をビューに渡します
- ビューでは、`$tasks`変数を使ってデータを表示できます

---

### 💡 TIP: compact()とは

**compact()**は、変数を配列に変換する関数です。

```php
compact('tasks')
```

これは、以下のコードと同じ意味です。

```php
['tasks' => $tasks]
```

---

## Step 4: ビューの作成

### 4-1. ビューファイルを作成する

`resources/views/tasks/`ディレクトリを作成し、`index.blade.php`ファイルを作成します。

```bash
mkdir -p resources/views/tasks
touch resources/views/tasks/index.blade.php
```

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>タスク一覧</title>
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
    <h1>タスク一覧</h1>
    
    @if($tasks->isEmpty())
        <p>タスクがありません。</p>
    @else
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>タイトル</th>
                    <th>ステータス</th>
                    <th>期限</th>
                    <th>作成日時</th>
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
                        <td>{{ $task->created_at->format('Y年m月d日 H:i') }}</td>
                    </tr>
                @endforeach
            </tbody>
        </table>
    @endif
</body>
</html>
```

---

### 4-2. コードリーディング

#### `@if($tasks->isEmpty())`

- `$tasks`が空（タスクが1件もない）場合、「タスクがありません。」と表示します
- `isEmpty()`メソッドは、コレクションが空かどうかを判定します

---

#### `@foreach($tasks as $task)`

- `$tasks`をループ処理し、1件ずつ`$task`変数に格納します
- ループ内では、`$task`変数を使ってデータを表示します

---

#### `{{ $task->id }}`

- `$task`の`id`を表示します
- `{{ }}`は、Bladeのエスケープ構文です。XSS攻撃を防ぐため、HTMLタグを無効化します

---

#### `{{ $task->due_date ? $task->due_date->format('Y年m月d日') : '未設定' }}`

- `$task->due_date`が存在する場合、`Y年m月d日`の形式で表示します
- `$task->due_date`が存在しない（NULL）場合、「未設定」と表示します
- `format()`メソッドは、Carbonオブジェクトの日付を指定した形式で表示します

---

## Step 5: 動作確認

### 5-1. テストデータを作成する

タスク一覧を表示するには、まずテストデータが必要です。

phpMyAdminを開き、`tasks`テーブルに手動でデータを追加します。

**例**:

| id | user_id | category_id | title | description | status | due_date | created_at | updated_at |
|----|---------|-------------|-------|-------------|--------|----------|------------|------------|
| 1 | 1 | NULL | 買い物 | 牛乳を買う | pending | 2024-01-20 | 2024-01-15 12:00:00 | 2024-01-15 12:00:00 |
| 2 | 1 | NULL | 掃除 | 部屋を掃除する | in_progress | 2024-01-18 | 2024-01-15 12:00:00 | 2024-01-15 12:00:00 |
| 3 | 1 | NULL | 勉強 | 英語を勉強する | completed | 2024-01-15 | 2024-01-15 12:00:00 | 2024-01-15 12:00:00 |

---

### 5-2. ブラウザでアクセスする

ブラウザで`http://localhost/tasks`にアクセスします。

**実行結果**:

タスク一覧が表示されます。

```
タスク一覧

ID | タイトル | ステータス | 期限 | 作成日時
---|----------|------------|------|----------
1  | 買い物   | 未着手     | 2024年01月20日 | 2024年01月15日 12:00
2  | 掃除     | 進行中     | 2024年01月18日 | 2024年01月15日 12:00
3  | 勉強     | 完了       | 2024年01月15日 | 2024年01月15日 12:00
```

---

## 🚨 よくある間違い

### 間違い1: ビューファイルのパスが間違っている

**エラー**:

```
View [tasks.index] not found.
```

**対処法**: `resources/views/tasks/index.blade.php`ファイルが存在するか確認します。

---

### 間違い2: compact()の変数名が間違っている

**エラー**:

```
Undefined variable $tasks
```

**対処法**: `compact('tasks')`の変数名が、コントローラーで定義した変数名と一致しているか確認します。

---

### 間違い3: テーブルにデータがない

**対処法**: phpMyAdminでテストデータを追加します。

---

## 💡 TIP: dd()でデバッグする

**dd()**は、変数の内容を表示して、処理を停止する関数です。

```php
public function index()
{
    $tasks = Task::all();
    dd($tasks); // ここで処理が停止し、$tasksの内容が表示される
    
    return view('tasks.index', compact('tasks'));
}
```

`dd()`を使うことで、データが正しく取得できているか確認できます。

---

## 💡 TIP: Eloquentのメソッド

Eloquentには、データを取得するための様々なメソッドがあります。

- **all()**: 全てのレコードを取得
- **find($id)**: 指定したIDのレコードを取得
- **where('status', 'pending')**: 条件に合うレコードを取得
- **orderBy('created_at', 'desc')**: 並び替え
- **paginate(10)**: ページネーション

---

## ✨ まとめ

このセクションでは、タスク一覧ページの実装について学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | 実装の流れ（ルーティング→コントローラー→ビュー） |
| Step 2 | `Route::get()`でルートを定義する方法 |
| Step 3 | コントローラーで`Task::all()`を使ってデータを取得する方法 |
| Step 4 | Bladeで`@foreach`を使ってデータを表示する方法 |
| Step 5 | 動作確認の方法 |

次のセクションでは、タスク作成の実装について学びます。

---
