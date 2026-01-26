# Tutorial 9-5-5: CRUD機能 - ハンズオン演習

## 📝 このセクションの目的

Chapter 5で学んだCRUD機能を実際に手を動かして確認します。タスク管理アプリを作成して、Create、Read、Update、Deleteの全機能を実装しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

**学習のポイント**：
- リソースコントローラーを使えるか
- フォームからデータを送信できるか
- CRUD操作を実装できるか

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのプロジェクトを作成します。

```
~/laravel-practice/
├── 9-5-5_hands-on/                       ← このハンズオン用のディレクトリ
│   ├── task-app-practice/                ← 要件を見て自分で作成するプロジェクト
│   │   ├── app/
│   │   ├── database/
│   │   ├── resources/views/
│   │   ├── routes/
│   │   └── ...
│   └── task-app-sample/                  ← 実践で一緒に作成するプロジェクト
│       ├── app/
│       ├── database/
│       ├── resources/views/
│       ├── routes/
│       └── ...
└── ...
```

| ディレクトリ | 用途 | URL |
|:---|:---|:---|
| `task-app-practice/` | 📋 要件を見て、自分の力で作成する | `http://localhost/tasks` |
| `task-app-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する | `http://localhost/tasks` |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

> ⚠️ **注意**: 2つのプロジェクトを同時に起動することはできません（ポートが競合するため）。一方のプロジェクトで作業する際は、もう一方を停止してください。

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

### 📁 Step 0: 環境を準備する（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

> **📌 前のハンズオンのプロジェクトを停止**
> 
> 前のハンズオン（9-4-9）のプロジェクトが起動している場合は、先に停止してください。
> ```bash
> cd ~/laravel-practice/9-4-9_hands-on/eloquent-app-sample
> ./vendor/bin/sail down
> ```

```bash
# laravel-practiceディレクトリに移動
cd ~/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 9-5-5_hands-on
cd 9-5-5_hands-on

# Laravel 10.xプロジェクトを作成（自分で作成する用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 task-app-practice
```

```bash
# プロジェクトディレクトリに移動
cd task-app-practice

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql

# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate

# データベースのマイグレーション
./vendor/bin/sail artisan migrate
```

**✅ ディレクトリ構造の確認**

```
~/laravel-practice/
└── 9-5-5_hands-on/
    └── task-app-practice/     ← 自分で作成する用（今ここ）
        ├── app/
        ├── database/
        ├── resources/views/
        ├── routes/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

> 💡 **ポイント**: タスクのデータは、モデルとマイグレーションを作成した後、tinkerで作成します。実践セクションの「ステップ4: Tinkerでデータ構造を確認する」を参考にしてください。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

```bash
sail artisan make:model Task -mcr
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

> 📌 **注意**: ここからは`task-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### 💻 環境準備（実践用プロジェクト）

まず、**自分で作成する用のプロジェクトを停止**します：

```bash
# task-app-practiceディレクトリに移動
cd ~/laravel-practice/9-5-5_hands-on/task-app-practice

# Sailを停止
./vendor/bin/sail down
```

次に、**実践用のプロジェクトを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/laravel-practice/9-5-5_hands-on

# Laravel 10.xプロジェクトを作成（実践用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 task-app-sample
```

```bash
# プロジェクトディレクトリに移動
cd task-app-sample

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql

# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate

# データベースのマイグレーション
./vendor/bin/sail artisan migrate
```

**✅ ディレクトリ構造の確認**

```
~/laravel-practice/
└── 9-5-5_hands-on/
    ├── task-app-practice/     ← 自分で作成した用（停止中）
    └── task-app-sample/       ← 実践用（今ここ、起動中）
        ├── app/
        ├── database/
        ├── resources/views/
        ├── routes/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

> 💡 **ポイント**: タスクのデータは、モデルとマイグレーションを作成した後、ステップ4のtinkerで作成します。

---

### 💭 実装の思考プロセス

CRUDアプリを構築する際、以下の順番で考えると効率的です：

1. **モデル、マイグレーション、コントローラーを一度に作成**：`-mcr`オプションで効率化
2. **マイグレーションでテーブル構造を定義**：タスクに必要なカラムを設定
3. **Tinkerでデータ構造を確認**：コントローラーを書く前にデータが取れるか確認
4. **リソースルートを定義**：7つのルートを一度に設定
5. **コントローラーにCRUDロジックを実装**：index, create, store, edit, update, destroy
6. **ビューを作成**：一覧、作成、編集フォーム

> 💡 **重要**: 「画面を作ってから動かす」のではなく、**「Tinkerでデータ取得を確認してから画面に繋ぐ」**という堅実なバックエンド開発フローを身につけましょう。

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
sail artisan make:model Task -mcr
```

**コマンド解説**：

```bash
sail artisan make:model Task -mcr
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
sail artisan migrate
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

#### ステップ4: Tinkerでデータ構造を確認する

**何を考えているか**：
- 「コントローラーを書く前に、データが正しく取れるか確認しよう」
- 「データが取れていないのに画面を作っても動かない」

Tinkerを起動して、データの作成と取得を確認します：

```bash
sail artisan tinker
```

```php
>>> use App\Models\Task;

// テストデータを作成
>>> Task::create(['title' => 'テストタスク', 'status' => 'pending']);

// データが取得できるか確認
>>> Task::all();

// 特定のタスクを取得
>>> Task::find(1);

// 最新順で取得
>>> Task::latest()->get();
```

**確認ポイント**：
- `Task::all()`でデータが取得できるか？
- `Task::find(1)`で特定のタスクが取得できるか？
- `Task::latest()->get()`で最新順に並ぶか？

> 💡 **ポイント**: Tinkerでデータが取れることを確認してから、コントローラーとビューを実装します。これが「データが取れていないのに画面を作っても動かない」問題を防ぐ堅実な開発フローです。

---

#### ステップ5: リソースルートを定義する

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

#### ステップ6: コントローラーにCRUDロジックを実装する

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

#### ステップ7: ビューを作成する

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

**自分で作成したコードと比較してみましょう**：
- `task-app-practice/`: 自分で作成したプロジェクト
- `task-app-sample/`: 一緒に作成したプロジェクト

両方のプロジェクトを見比べて、違いがあれば確認してみてください。

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

## 🧪 動作確認の方法

### プロジェクトの切り替え

2つのプロジェクトを切り替えて動作確認する方法：

```bash
# task-app-practiceで確認したい場合
cd ~/laravel-practice/9-5-5_hands-on/task-app-sample
./vendor/bin/sail down

cd ~/laravel-practice/9-5-5_hands-on/task-app-practice
./vendor/bin/sail up -d

# task-app-sampleで確認したい場合
cd ~/laravel-practice/9-5-5_hands-on/task-app-practice
./vendor/bin/sail down

cd ~/laravel-practice/9-5-5_hands-on/task-app-sample
./vendor/bin/sail up -d
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ リソースコントローラーを使える
- ✅ フォームからデータを送信できる
- ✅ CRUD操作を実装できる

引き続き、次のセクションも頑張りましょう！

### 🛑 Sailの停止

次のセクションに進む前に、Sailを停止しておきましょう。

```bash
./vendor/bin/sail down
```

> 💡 **なぜ停止するの？**: Sailを起動したままだと、次のセクションで別のプロジェクトを起動する際にポートが競合してエラーになることがあります。セクションの終わりには必ずSailを停止する習慣をつけましょう。

---
