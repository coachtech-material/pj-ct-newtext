# Tutorial 11-5-1: コードの整理とDRY原則

## 🎯 このセクションで学ぶこと

- コードの整理方法を学ぶ
- DRY（Don't Repeat Yourself）原則を理解する
- リファクタリングの重要性と実践方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ機能実装の後に『リファクタリング』を行うのか？」

機能が完成したら、次は「リファクタリング」です。なぜこのタイミングなのでしょうか？

---

### 理由1: 動くコードを先に書く

最初から完璧なコードを書こうとすると、**なかなか進まない**ことがあります。

まずは動くコードを書いて、その後で**きれいにする**のが効率的です。

---

### 理由2: 問題点が見えてくる

コードを書いていると、「ここ、同じこと書いてるな」「このメソッド長すぎるな」と気づきます。

機能が完成した後なら、**全体を見渡して問題点を把握**できます。

---

### 理由3: DRY原則から始める理由

DRY（Don't Repeat Yourself）は、**最も基本的なリファクタリング原則**です。

重複コードを見つけて共通化することで、コードの品質が大幅に向上します。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | DRY原則を理解 | 重複コードの問題を把握 |
| Step 2 | Eloquentスコープで共通化 | クエリの重複を排除 |
| Step 3 | Bladeコンポーネントで共通化 | ビューの重複を排除 |
| Step 4 | サービスクラスで整理 | ビジネスロジックを分離 |

> 💡 **ポイント**: リファクタリングは「動作を変えずにコードを改善する」ことです。

---

## Step 1: DRY原則を理解する

### 1-1. DRY原則とは

**DRY（Don't Repeat Yourself）原則**とは、**同じコードを繰り返し書かない**という原則です。

同じコードを繰り返し書くと、以下のような問題が発生します。

| 問題 | 説明 |
|------|------|
| メンテナンスが大変 | 1箇所を修正すると、他の箇所も修正する必要がある |
| バグが発生しやすい | 修正漏れが発生する |
| コードが長くなる | 可読性が低下する |

---

### 1-2. 悪い例（コードの重複）

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

### 1-3. 良い例（DRY原則を適用）

```php
// タスク一覧
public function index()
{
    $tasks = $this->getUserTasks()->get();
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

## Step 2: Eloquentスコープで共通化

### 2-1. スコープとは

Eloquentの**スコープ（Scope）**を使うと、より簡潔にコードを書くことができます。

**スコープ**とは、**クエリの条件を再利用可能にする機能**です。

---

### 2-2. Taskモデルにスコープを追加する

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

### 2-3. コードリーディング

#### `public function scopeForCurrentUser($query)`

- `scope`で始まるメソッドは、スコープとして認識されます
- メソッド名は、`scope`の後に続く部分（`ForCurrentUser`）がスコープ名になります
- 使用する際は、`Task::forCurrentUser()`のように呼び出します

---

### 2-4. スコープを使ったコントローラー

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

### 2-5. スコープのチェーン

スコープは、チェーンして使うことができます。

```php
$tasks = Task::forCurrentUser()->pending()->get();
```

これは、「ログインユーザーの未完了のタスク」を取得します。

---

## Step 3: Bladeコンポーネントで共通化

### 3-1. 悪い例（コードの重複）

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
@if(session('success'))
    <div class="alert alert-success">
        {{ session('success') }}
    </div>
@endif
```

**ファイル**: `resources/views/tasks/create.blade.php`

```blade
@if(session('success'))
    <div class="alert alert-success">
        {{ session('success') }}
    </div>
@endif
```

同じコードが複数のビューに存在しています。

---

### 3-2. Bladeコンポーネントを作成する

**ファイル**: `resources/views/components/alert.blade.php`

```blade
@props(['type' => 'success'])

@if(session($type))
    <div class="alert alert-{{ $type }}" style="padding: 15px; margin-bottom: 15px; border-radius: 4px; {{ $type === 'success' ? 'background-color: #d4edda; color: #155724;' : 'background-color: #f8d7da; color: #721c24;' }}">
        {{ session($type) }}
    </div>
@endif
```

---

### 3-3. コンポーネントを使用する

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

## Step 4: サービスクラスで整理

### 4-1. サービスクラスとは

**サービスクラス（Service Class）**を使うと、コントローラーのコードを整理できます。

サービスクラスは、**ビジネスロジックを切り出すためのクラス**です。

---

### 4-2. 悪い例（コントローラーにビジネスロジックが混在）

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

### 4-3. サービスクラスを作成する

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
    public function createTask(array $data): Task
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

---

### 4-4. サービスクラスを使ったコントローラー

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Models\Task;
use App\Services\TaskService;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    public function __construct(
        protected TaskService $taskService
    ) {}

    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'due_date' => 'nullable|date',
        ]);

        $this->taskService->createTask($validated);

        return redirect()->route('tasks.index')->with('success', 'タスクを作成しました。');
    }
}
```

サービスクラスを使うことで、コントローラーがシンプルになり、ビジネスロジックが整理されました。

---

### 4-5. コードリーディング

#### 依存性注入（Dependency Injection）

```php
public function __construct(
    protected TaskService $taskService
) {}
```

これは、**依存性注入（Dependency Injection）**と呼ばれる手法です。

Laravelは、自動的に`TaskService`のインスタンスを生成し、コントローラーに渡します。

---

## 🚨 よくある間違い

### 間違い1: コードの重複を放置する

**問題**: 同じコードが複数箇所に存在し、修正漏れが発生する

**対処法**: DRY原則を意識し、共通処理をメソッドやクラスに切り出します。

---

### 間違い2: コントローラーにビジネスロジックを書きすぎる

**問題**: コントローラーが肥大化し、テストが難しくなる

**対処法**: サービスクラスを作成し、ビジネスロジックを切り出します。

---

### 間違い3: リファクタリングを後回しにする

**問題**: 技術的負債が蓄積し、後で修正が困難になる

**対処法**: 機能を実装したら、すぐにリファクタリングを行います。

---

## ✨ まとめ

このセクションでは、コードの整理とDRY原則について学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | DRY原則の理解と重複コードの問題 |
| Step 2 | Eloquentスコープでクエリの重複を排除 |
| Step 3 | Bladeコンポーネントでビューの重複を排除 |
| Step 4 | サービスクラスでビジネスロジックを分離 |

次のセクションでは、具体的な命名規則について学びます。

---
