# Tutorial 9-5-6: CRUD機能 - ハンズオン演習

## 📝 このセクションの目的

Chapter 5で学んだCRUD機能を実際に手を動かして確認します。タスク管理アプリを作成して、Create、Read、Update、Deleteの全機能を実装しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

**学習のポイント**：
- リソースコントローラーを使えるか
- フォームからデータを送信できるか
- CRUD操作を実装できるか

---

## 🎯 演習課題：タスク管理アプリを作成しよう

### 📋 要件

#### 1. Taskモデルとマイグレーションの作成

**カラム構成**：
- id, title (VARCHAR 200), description (TEXT nullable), status (VARCHAR 20, default 'pending'), due_date (DATE nullable), timestamps

#### 2. リソースコントローラーの作成

`TaskController`をリソースコントローラーとして作成してください。

#### 3. ビューの作成

以下のビューを作成してください：

- `tasks/index.blade.php`: タスク一覧
- `tasks/create.blade.php`: タスク作成フォーム
- `tasks/edit.blade.php`: タスク編集フォーム

#### 4. ルートの定義

リソースルートを定義してください。

---

## 💡 ヒント

```bash
php artisan make:model Task -mcr
```

```php
// routes/web.php
Route::resource('tasks', TaskController::class);
```

```blade
<!-- フォーム -->
<form action="{{ route('tasks.store') }}" method="POST">
    @csrf
    <input type="text" name="title">
    <button type="submit">作成</button>
</form>
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？CRUD機能はWebアプリケーションの基本中の基本です。一緒に手を動かしながら、タスク管理アプリを作成していきましょう。

### 💭 実装の思考プロセス

CRUDアプリを構築する際、以下の順番で考えると効率的です：

1. **モデル、マイグレーション、コントローラーを一度に作成**：`-mcr`オプションで効率化
2. **マイグレーションでテーブル構造を定義**：タスクに必要なカラムを設定
3. **リソースルートを定義**：7つのルートを一度に設定
4. **コントローラーにCRUDロジックを実装**：index, create, store, edit, update, destroy
5. **ビューを作成**：一覧、作成、編集フォーム

CRUDのポイントは「リソースコントローラーとリソースルートで規約に沿った開発をする」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: モデル、マイグレーション、コントローラーを一度に作成する

**何を考えているか**：
- 「タスク管理に必要なファイルを一度に生成しよう」
- 「`-mcr`オプションでモデル、マイグレーション、リソースコントローラーを作ろう」
- 「効率的に開発を始めよう」

ターミナルで以下のコマンドを実行します：

```bash
php artisan make:model Task -mcr
```

**コマンド解説**：

```bash
php artisan make:model Task -mcr
```
→ `-m`でマイグレーション、`-c`でコントローラー、`-r`でリソースコントローラーを同時に生成します。一度に必要なファイルが作成されます。

---

#### ステップ2: マイグレーションでテーブル構造を定義する

**何を考えているか**：
- 「タスクにはタイトル、説明、ステータス、期限が必要だ」
- 「説明と期限はnullableにしよう」
- 「ステータスのデフォルト値を'pending'にしよう」

生成されたマイグレーションファイルを開いて、`up`メソッドを以下のように編集します：

```php
public function up(): void
{
    Schema::create('tasks', function (Blueprint $table) {
        $table->id();
        $table->string('title', 200);
        $table->text('description')->nullable();
        $table->string('status', 20)->default('pending');
        $table->date('due_date')->nullable();
        $table->timestamps();
    });
}
```

**コードリーディング**：

```php
$table->string('title', 200);
```
→ タイトルを`VARCHAR(200)`で定義します。必須項目です。

```php
$table->text('description')->nullable();
```
→ 説明を`TEXT`型で定義し、`nullable()`でNULLを許可します。簡単なタスクでは説明が不要な場合があります。

```php
$table->string('status', 20)->default('pending');
```
→ ステータスを`VARCHAR(20)`で定義し、デフォルト値を`'pending'`に設定します。新規タスクは自動的に「保留中」になります。

```php
$table->date('due_date')->nullable();
```
→ 期限を`DATE`型で定義し、`nullable()`でNULLを許可します。期限がないタスクもあります。

マイグレーションを実行します：

```bash
php artisan migrate
```

---

#### ステップ3: モデルで属性を設定する

**何を考えているか**：
- 「$fillableで一括代入可能な属性を指定しよう」
- 「$castsで日付型を設定しよう」

`app/Models/Task.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Task extends Model
{
    protected $fillable = [
        'title',
        'description',
        'status',
        'due_date',
    ];

    protected $casts = [
        'due_date' => 'date',
    ];
}
```

**コードリーディング**：

```php
protected $fillable = [
    'title',
    'description',
    'status',
    'due_date',
];
```
→ `$fillable`で一括代入可能な属性を指定します。セキュリティ対策として重要です。

```php
protected $casts = [
    'due_date' => 'date',
];
```
→ `$casts`で`due_date`を`date`型にキャストします。Carbonインスタンスとして扱えるようになります。

---

#### ステップ4: リソースルートを定義する

**何を考えているか**：
- 「CRUDに必要な7つのルートを一度に設定しよう」
- 「`Route::resource`で簡単に定義できる」

`routes/web.php`を開いて、以下を追加します：

```php
use App\Http\Controllers\TaskController;

Route::resource('tasks', TaskController::class);
```

**コードリーディング**：

```php
Route::resource('tasks', TaskController::class);
```
→ リソースルートで以下の7つのルートが一度に定義されます：
- GET `/tasks` → index()
- GET `/tasks/create` → create()
- POST `/tasks` → store()
- GET `/tasks/{id}` → show()
- GET `/tasks/{id}/edit` → edit()
- PUT/PATCH `/tasks/{id}` → update()
- DELETE `/tasks/{id}` → destroy()

---

#### ステップ5: コントローラーにCRUDロジックを実装する

**何を考えているか**：
- 「一覧表示、作成、編集、削除のロジックを実装しよう」
- 「リソースコントローラーの規約に沿って実装しよう」

`app/Http/Controllers/TaskController.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Http\Controllers;

use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    public function index()
    {
        $tasks = Task::latest()->get();
        return view('tasks.index', compact('tasks'));
    }

    public function create()
    {
        return view('tasks.create');
    }

    public function store(Request $request)
    {
        Task::create($request->all());
        return redirect()->route('tasks.index');
    }

    public function edit($id)
    {
        $task = Task::findOrFail($id);
        return view('tasks.edit', compact('task'));
    }

    public function update(Request $request, $id)
    {
        $task = Task::findOrFail($id);
        $task->update($request->all());
        return redirect()->route('tasks.index');
    }

    public function destroy($id)
    {
        Task::findOrFail($id)->delete();
        return redirect()->route('tasks.index');
    }
}
```

**コードリーディング**：

```php
public function index()
{
    $tasks = Task::latest()->get();
    return view('tasks.index', compact('tasks'));
}
```
→ `index`メソッドで全タスクを最新順で取得し、一覧ページに渡します。`compact('tasks')`は`['tasks' => $tasks]`の省略記法です。

```php
public function create()
{
    return view('tasks.create');
}
```
→ `create`メソッドで作成フォームを表示します。

```php
public function store(Request $request)
{
    Task::create($request->all());
    return redirect()->route('tasks.index');
}
```
→ `store`メソッドでタスクを作成し、一覧ページにリダイレクトします。`route('tasks.index')`で名前付きルートを使用します。

```php
public function edit($id)
{
    $task = Task::findOrFail($id);
    return view('tasks.edit', compact('task'));
}
```
→ `edit`メソッドで編集フォームを表示します。既存のタスクデータを渡します。

```php
public function update(Request $request, $id)
{
    $task = Task::findOrFail($id);
    $task->update($request->all());
    return redirect()->route('tasks.index');
}
```
→ `update`メソッドでタスクを更新します。

```php
public function destroy($id)
{
    Task::findOrFail($id)->delete();
    return redirect()->route('tasks.index');
}
```
→ `destroy`メソッドでタスクを削除します。

---

#### ステップ6: ビューを作成する

**何を考えているか**：
- 「一覧ページ、作成フォーム、編集フォームを作ろう」
- 「フォームには@csrfトークンを必ず追加しよう」
- 「名前付きルートでURLを生成しよう」

`resources/views/tasks/index.blade.php`を作成します：

```blade
<h1>タスク一覧</h1>
<a href="{{ route('tasks.create') }}">新規作成</a>

@foreach ($tasks as $task)
    <div>
        <h3>{{ $task->title }}</h3>
        <p>{{ $task->description }}</p>
        <a href="{{ route('tasks.edit', $task->id) }}">編集</a>
        <form action="{{ route('tasks.destroy', $task->id) }}" method="POST">
            @csrf
            @method('DELETE')
            <button type="submit">削除</button>
        </form>
    </div>
@endforeach
```

`resources/views/tasks/create.blade.php`を作成します：

```blade
<h1>タスク作成</h1>
<form action="{{ route('tasks.store') }}" method="POST">
    @csrf
    <input type="text" name="title" placeholder="タイトル">
    <textarea name="description" placeholder="説明"></textarea>
    <input type="date" name="due_date">
    <button type="submit">作成</button>
</form>
```

---

### ✨ 完成！

これでCRUD機能を持つタスク管理アプリが完成しました！リソースコントローラーとリソースルートを使って、効率的にCRUDを実装できましたね。

---

## 📖 模範解答

### マイグレーションファイル

```php
public function up(): void
{
    Schema::create('tasks', function (Blueprint $table) {
        $table->id();
        $table->string('title', 200);
        $table->text('description')->nullable();
        $table->string('status', 20)->default('pending');
        $table->date('due_date')->nullable();
        $table->timestamps();
    });
}
```

### Task.php

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Task extends Model
{
    protected $fillable = [
        'title',
        'description',
        'status',
        'due_date',
    ];

    protected $casts = [
        'due_date' => 'date',
    ];
}
```

### TaskController.php

```php
<?php

namespace App\Http\Controllers;

use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    public function index()
    {
        $tasks = Task::latest()->get();
        return view('tasks.index', ['tasks' => $tasks]);
    }

    public function create()
    {
        return view('tasks.create');
    }

    public function store(Request $request)
    {
        Task::create($request->all());
        return redirect()->route('tasks.index');
    }

    public function edit($id)
    {
        $task = Task::findOrFail($id);
        return view('tasks.edit', ['task' => $task]);
    }

    public function update(Request $request, $id)
    {
        $task = Task::findOrFail($id);
        $task->update($request->all());
        return redirect()->route('tasks.index');
    }

    public function destroy($id)
    {
        Task::findOrFail($id)->delete();
        return redirect()->route('tasks.index');
    }
}
```

### routes/web.php

```php
use App\Http\Controllers\TaskController;

Route::resource('tasks', TaskController::class);
```

### tasks/index.blade.php

```blade
@extends('layouts.app')

@section('content')
<div class="container">
    <h1>タスク一覧</h1>
    <a href="{{ route('tasks.create') }}" class="btn btn-primary">新規作成</a>
    
    <table class="table mt-3">
        <thead>
            <tr>
                <th>タイトル</th>
                <th>ステータス</th>
                <th>期限</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            @foreach ($tasks as $task)
            <tr>
                <td>{{ $task->title }}</td>
                <td>{{ $task->status }}</td>
                <td>{{ $task->due_date }}</td>
                <td>
                    <a href="{{ route('tasks.edit', $task->id) }}">編集</a>
                    <form action="{{ route('tasks.destroy', $task->id) }}" method="POST" style="display:inline;">
                        @csrf
                        @method('DELETE')
                        <button type="submit">削除</button>
                    </form>
                </td>
            </tr>
            @endforeach
        </tbody>
    </table>
</div>
@endsection
```

### tasks/create.blade.php

```blade
@extends('layouts.app')

@section('content')
<div class="container">
    <h1>タスク作成</h1>
    
    <form action="{{ route('tasks.store') }}" method="POST">
        @csrf
        <div class="mb-3">
            <label>タイトル</label>
            <input type="text" name="title" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>説明</label>
            <textarea name="description" class="form-control"></textarea>
        </div>
        <div class="mb-3">
            <label>期限</label>
            <input type="date" name="due_date" class="form-control">
        </div>
        <button type="submit" class="btn btn-primary">作成</button>
    </form>
</div>
@endsection
```
---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ リソースコントローラーを使える
- ✅ フォームからデータを送信できる
- ✅ CRUD操作を実装できる

引き続き、次のセクションも頑張りましょう！

---
