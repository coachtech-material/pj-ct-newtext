# Tutorial 11-5-1: コードの整理とDRY原則

## 🎯 このセクションで学ぶこと

*   コードの整理方法を学ぶ。
*   DRY（Don't Repeat Yourself）原則を理解する。
*   リファクタリングの重要性と実践方法を学ぶ。

---

## 導入：なぜリファクタリングが必要なのか

**リファクタリング（Refactoring）**とは、**コードの動作を変えずに、コードの構造を改善すること**です。

リファクタリングを行うことで、以下のようなメリットがあります。

*   **コードの可読性が向上する**: 他の開発者がコードを理解しやすくなる
*   **メンテナンスが容易になる**: バグ修正や機能追加がしやすくなる
*   **コードの重複が減る**: 同じコードを何度も書く必要がなくなる

このセクションでは、**DRY原則**を学び、コードの整理方法を理解します。

---

## 詳細解説

### 🔍 DRY原則とは

**DRY（Don't Repeat Yourself）原則**とは、**同じコードを繰り返し書かない**という原則です。

同じコードを繰り返し書くと、以下のような問題が発生します。

*   **メンテナンスが大変**: 1箇所を修正すると、他の箇所も修正する必要がある
*   **バグが発生しやすい**: 修正漏れが発生する
*   **コードが長くなる**: 可読性が低下する

---

### 🔍 DRY原則の例

#### 悪い例（コードの重複）

```php
// タスク一覧
public function index()
{
    $tasks = Task::where('user_id', Auth::id())->get();
    return view('tasks.index', compact('tasks'));
}

// 完了したタスク一覧
public function completed()
{
    $tasks = Task::where('user_id', Auth::id())->where('status', 'completed')->get();
    return view('tasks.completed', compact('tasks'));
}

// 未完了のタスク一覧
public function pending()
{
    $tasks = Task::where('user_id', Auth::id())->where('status', 'pending')->get();
    return view('tasks.pending', compact('tasks'));
}
```

この例では、`Task::where('user_id', Auth::id())`が3回繰り返されています。

---

#### 良い例（DRY原則を適用）

```php
// タスク一覧
public function index()
{
    $tasks = $this->getUserTasks();
    return view('tasks.index', compact('tasks'));
}

// 完了したタスク一覧
public function completed()
{
    $tasks = $this->getUserTasks()->where('status', 'completed')->get();
    return view('tasks.completed', compact('tasks'));
}

// 未完了のタスク一覧
public function pending()
{
    $tasks = $this->getUserTasks()->where('status', 'pending')->get();
    return view('tasks.pending', compact('tasks'));
}

// ログインユーザーのタスクを取得する（共通処理）
private function getUserTasks()
{
    return Task::where('user_id', Auth::id());
}
```

`getUserTasks()`メソッドを作成することで、コードの重複を排除しました。

---

### 🔍 Eloquentのスコープを使う

Eloquentの**スコープ（Scope）**を使うと、より簡潔にコードを書くことができます。

**スコープ**とは、**クエリの条件を再利用可能にする機能**です。

---

#### Taskモデルにスコープを追加する

**ファイル**: `app/Models/Task.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\Auth;

class Task extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'category_id',
        'title',
        'description',
        'status',
        'due_date',
    ];

    protected $casts = [
        'due_date' => 'date',
    ];

    /**
     * タスクが属するユーザー（多対1）
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }

    /**
     * ログインユーザーのタスクのみを取得するスコープ
     */
    public function scopeForCurrentUser($query)
    {
        return $query->where('user_id', Auth::id());
    }

    /**
     * 完了したタスクのみを取得するスコープ
     */
    public function scopeCompleted($query)
    {
        return $query->where('status', 'completed');
    }

    /**
     * 未完了のタスクのみを取得するスコープ
     */
    public function scopePending($query)
    {
        return $query->where('status', 'pending');
    }
}
```

---

### 🔍 コードリーディング

#### `public function scopeForCurrentUser($query)`

*   `scope`で始まるメソッドは、スコープとして認識されます。
*   メソッド名は、`scope`の後に続く部分（`ForCurrentUser`）がスコープ名になります。
*   使用する際は、`Task::forCurrentUser()`のように呼び出します。

---

#### スコープを使ったコントローラー

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    /**
     * タスク一覧
     */
    public function index()
    {
        $tasks = Task::forCurrentUser()->get();
        return view('tasks.index', compact('tasks'));
    }

    /**
     * 完了したタスク一覧
     */
    public function completed()
    {
        $tasks = Task::forCurrentUser()->completed()->get();
        return view('tasks.completed', compact('tasks'));
    }

    /**
     * 未完了のタスク一覧
     */
    public function pending()
    {
        $tasks = Task::forCurrentUser()->pending()->get();
        return view('tasks.pending', compact('tasks'));
    }
}
```

スコープを使うことで、コードが簡潔になり、可読性が向上しました。

---

### 💡 TIP: スコープのチェーン

スコープは、チェーンして使うことができます。

```php
$tasks = Task::forCurrentUser()->pending()->get();
```

これは、「ログインユーザーの未完了のタスク」を取得します。

---

### 🔍 Bladeコンポーネントを使う

Bladeの**コンポーネント（Component）**を使うと、ビューのコードの重複を排除できます。

---

#### 悪い例（コードの重複）

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<div class="alert alert-success">
    {{ session('success') }}
</div>
```

**ファイル**: `resources/views/tasks/create.blade.php`

```blade
<div class="alert alert-success">
    {{ session('success') }}
</div>
```

同じコードが複数のビューに存在しています。

---

#### 良い例（Bladeコンポーネントを使う）

**ファイル**: `resources/views/components/alert.blade.php`

```blade
@if(session($type))
    <div class="alert alert-{{ $type }}">
        {{ session($type) }}
    </div>
@endif
```

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<x-alert type="success" />
```

**ファイル**: `resources/views/tasks/create.blade.php`

```blade
<x-alert type="success" />
```

コンポーネントを使うことで、コードの重複を排除しました。

---

### 🔍 サービスクラスを使う

**サービスクラス（Service Class）**を使うと、コントローラーのコードを整理できます。

サービスクラスは、**ビジネスロジックを切り出すためのクラス**です。

---

#### 悪い例（コントローラーにビジネスロジックが混在）

```php
public function store(Request $request)
{
    $request->validate([
        'title' => 'required|string|max:255',
        'description' => 'nullable|string',
        'due_date' => 'nullable|date',
    ]);

    $task = Task::create([
        'user_id' => Auth::id(),
        'title' => $request->title,
        'description' => $request->description,
        'status' => 'pending',
        'due_date' => $request->due_date,
    ]);

    // メール送信
    Mail::to(Auth::user())->send(new TaskCreated($task));

    // ログ記録
    Log::info('Task created', ['task_id' => $task->id]);

    return redirect()->route('tasks.index')->with('success', 'タスクを作成しました。');
}
```

このコントローラーは、バリデーション、データ作成、メール送信、ログ記録など、多くの処理を行っています。

---

#### 良い例（サービスクラスを使う）

**ファイル**: `app/Services/TaskService.php`

```php
<?php

namespace App\Services;

use App\Models\Task;
use App\Mail\TaskCreated;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Mail;

class TaskService
{
    /**
     * タスクを作成する
     */
    public function createTask(array $data)
    {
        $task = Task::create([
            'user_id' => Auth::id(),
            'title' => $data['title'],
            'description' => $data['description'] ?? null,
            'status' => 'pending',
            'due_date' => $data['due_date'] ?? null,
        ]);

        // メール送信
        Mail::to(Auth::user())->send(new TaskCreated($task));

        // ログ記録
        Log::info('Task created', ['task_id' => $task->id]);

        return $task;
    }
}
```

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Models\Task;
use App\Services\TaskService;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    protected $taskService;

    public function __construct(TaskService $taskService)
    {
        $this->taskService = $taskService;
    }

    public function store(Request $request)
    {
        $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'due_date' => 'nullable|date',
        ]);

        $this->taskService->createTask($request->all());

        return redirect()->route('tasks.index')->with('success', 'タスクを作成しました。');
    }
}
```

サービスクラスを使うことで、コントローラーがシンプルになり、ビジネスロジックが整理されました。

---

### 💡 TIP: 依存性注入（Dependency Injection）

```php
public function __construct(TaskService $taskService)
{
    $this->taskService = $taskService;
}
```

これは、**依存性注入（Dependency Injection）**と呼ばれる手法です。

Laravelは、自動的に`TaskService`のインスタンスを生成し、コントローラーに渡します。

---

### 🚨 よくある間違い

#### 間違い1: コードの重複を放置する

**対処法**: DRY原則を意識し、共通処理をメソッドやクラスに切り出します。

---

#### 間違い2: コントローラーにビジネスロジックを書きすぎる

**対処法**: サービスクラスを作成し、ビジネスロジックを切り出します。

---

#### 間違い3: リファクタリングを後回しにする

**対処法**: 機能を実装したら、すぐにリファクタリングを行います。

---

## ✨ まとめ

このセクションでは、コードの整理とDRY原則について学びました。

*   DRY原則は、同じコードを繰り返し書かないという原則である。
*   Eloquentのスコープを使うことで、クエリの条件を再利用できる。
*   Bladeコンポーネントを使うことで、ビューのコードの重複を排除できる。
*   サービスクラスを使うことで、コントローラーのコードを整理できる。

次のセクションでは、テストについて学びます。

---

## 📝 学習のポイント

- [ ] コードの整理方法を学んだ。
- [ ] DRY（Don't Repeat Yourself）原則を理解した。
- [ ] リファクタリングの重要性と実践方法を学んだ。
