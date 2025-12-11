# Tutorial 11-5-6: サービスクラスの導入とDI（依存性注入）

## 🎯 このセクションで学ぶこと

*   コントローラーが肥大化する問題を理解する。
*   サービスクラスを使って、ビジネスロジックを分離する方法を学ぶ。
*   DI（依存性注入）の基本的な使い方を学ぶ。
*   「コンストラクタに書けば使える」という作法を身につける。

---

## 導入：なぜサービスクラスを使うのか

**コントローラー**は、リクエストを受け取り、レスポンスを返す役割を持ちます。

しかし、**ビジネスロジック**をコントローラーに書くと、**コントローラーが肥大化**します。

**サービスクラス**を使うと、**ビジネスロジックを分離**でき、**コントローラーをスリムに**保てます。

---

## 詳細解説

### 🔍 コントローラーが肥大化する例

以下のコードは、コントローラーにビジネスロジックが書かれています。

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
    ]);
    
    $task = new Task();
    $task->title = $validated['title'];
    $task->description = $validated['description'];
    $task->status = $validated['status'];
    $task->user_id = auth()->id();
    $task->save();
    
    // メール送信
    Mail::to(auth()->user()->email)->send(new TaskCreated($task));
    
    // ログ記録
    Log::info('Task created', ['task_id' => $task->id]);
    
    return redirect()->route('tasks.index');
}
```

**問題点**:
*   コントローラーにビジネスロジックが書かれている
*   テストしにくい
*   再利用しにくい

---

### 🔍 サービスクラスを作成する

サービスクラスを作成して、ビジネスロジックを分離します。

```bash
mkdir -p app/Services
touch app/Services/TaskService.php
```

**ファイル**: `app/Services/TaskService.php`

```php
<?php

namespace App\Services;

use App\Models\Task;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Log;
use App\Mail\TaskCreated;

class TaskService
{
    public function createTask(array $data, int $userId)
    {
        $task = new Task();
        $task->title = $data['title'];
        $task->description = $data['description'];
        $task->status = $data['status'];
        $task->user_id = $userId;
        $task->save();
        
        // メール送信
        Mail::to(auth()->user()->email)->send(new TaskCreated($task));
        
        // ログ記録
        Log::info('Task created', ['task_id' => $task->id]);
        
        return $task;
    }
}
```

---

### 🔍 コントローラーをスリムにする

コントローラーから、サービスクラスを使います。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Services\TaskService;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    private $taskService;
    
    public function __construct(TaskService $taskService)
    {
        $this->taskService = $taskService;
    }
    
    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'description' => 'nullable',
            'status' => 'required|in:pending,in_progress,completed',
        ]);
        
        $this->taskService->createTask($validated, auth()->id());
        
        return redirect()->route('tasks.index');
    }
}
```

**改善点**:
*   コントローラーがスリムになった
*   ビジネスロジックがサービスクラスに分離された
*   テストしやすくなった

---

### 🔍 DI（依存性注入）とは

**DI（Dependency Injection）**は、**依存するオブジェクトを外部から注入する**仕組みです。

Laravelでは、**コンストラクタに書けば、自動的に注入される**ので、特別な設定は不要です。

```php
public function __construct(TaskService $taskService)
{
    $this->taskService = $taskService;
}
```

**ポイント**:
*   コンストラクタに`TaskService`を書くだけで、自動的に注入される
*   `new TaskService()`と書く必要はない

---

### 🔍 DIのメリット

**1. テストしやすい**

DIを使うと、テスト時にモックを注入できます。

```php
public function test_task_creation()
{
    $mockService = Mockery::mock(TaskService::class);
    $mockService->shouldReceive('createTask')->once();
    
    $this->app->instance(TaskService::class, $mockService);
    
    // テスト実行
}
```

---

**2. 依存関係が明確**

コンストラクタを見れば、何に依存しているかが分かります。

```php
public function __construct(TaskService $taskService, UserService $userService)
{
    $this->taskService = $taskService;
    $this->userService = $userService;
}
```

---

### 🔍 サービスクラスの命名規則

サービスクラスは、`〇〇Service`という名前にします。

*   `TaskService`
*   `UserService`
*   `OrderService`

---

### 🔍 サービスクラスのメソッド名

サービスクラスのメソッド名は、**動詞で始める**のが一般的です。

*   `createTask()`
*   `updateTask()`
*   `deleteTask()`
*   `sendEmail()`

---

### 🔍 実践演習: サービスクラスを作成してください

以下のコントローラーを、サービスクラスを使ってリファクタリングしてください。

```php
public function update(Request $request, Task $task)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
    ]);
    
    $task->title = $validated['title'];
    $task->description = $validated['description'];
    $task->status = $validated['status'];
    $task->save();
    
    // メール送信
    Mail::to(auth()->user()->email)->send(new TaskUpdated($task));
    
    // ログ記録
    Log::info('Task updated', ['task_id' => $task->id]);
    
    return redirect()->route('tasks.index');
}
```

---

**解答例**:

**ファイル**: `app/Services/TaskService.php`

```php
public function updateTask(Task $task, array $data)
{
    $task->title = $data['title'];
    $task->description = $data['description'];
    $task->status = $data['status'];
    $task->save();
    
    // メール送信
    Mail::to(auth()->user()->email)->send(new TaskUpdated($task));
    
    // ログ記録
    Log::info('Task updated', ['task_id' => $task->id]);
    
    return $task;
}
```

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function update(Request $request, Task $task)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
    ]);
    
    $this->taskService->updateTask($task, $validated);
    
    return redirect()->route('tasks.index');
}
```

---

### 🔍 サービスクラスをメソッドで注入する

コンストラクタだけでなく、**メソッドでも注入できます**。

```php
public function store(Request $request, TaskService $taskService)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
    ]);
    
    $taskService->createTask($validated, auth()->id());
    
    return redirect()->route('tasks.index');
}
```

**ポイント**:
*   メソッドの引数に書くだけで、自動的に注入される
*   1つのメソッドだけで使う場合は、メソッド注入が便利

---

### 🔍 複数のサービスクラスを注入する

複数のサービスクラスを注入することもできます。

```php
public function __construct(TaskService $taskService, UserService $userService)
{
    $this->taskService = $taskService;
    $this->userService = $userService;
}
```

---

### 💡 TIP: サービスクラスとリポジトリパターン

さらに高度なパターンとして、**リポジトリパターン**があります。

*   **サービスクラス**: ビジネスロジックを担当
*   **リポジトリクラス**: データベース操作を担当

```php
class TaskRepository
{
    public function create(array $data)
    {
        return Task::create($data);
    }
}

class TaskService
{
    private $taskRepository;
    
    public function __construct(TaskRepository $taskRepository)
    {
        $this->taskRepository = $taskRepository;
    }
    
    public function createTask(array $data, int $userId)
    {
        $data['user_id'] = $userId;
        $task = $this->taskRepository->create($data);
        
        // メール送信
        Mail::to(auth()->user()->email)->send(new TaskCreated($task));
        
        return $task;
    }
}
```

---

### 🚨 よくある間違い

#### 間違い1: サービスクラスをnewする

```php
// ❌ 間違い
$taskService = new TaskService();
$taskService->createTask($validated, auth()->id());
```

```php
// ✅ 正しい
public function __construct(TaskService $taskService)
{
    $this->taskService = $taskService;
}
```

---

#### 間違い2: サービスクラスに何でも詰め込む

サービスクラスは、**単一責任の原則**に従います。

*   `TaskService`: タスク関連のビジネスロジック
*   `UserService`: ユーザー関連のビジネスロジック

---

#### 間違い3: コントローラーに何も書かない

コントローラーには、**リクエストの受け取りとレスポンスの返却**を書きます。

```php
public function store(Request $request)
{
    $validated = $request->validate([...]);
    $this->taskService->createTask($validated, auth()->id());
    return redirect()->route('tasks.index');
}
```

---

## ✨ まとめ

このセクションでは、サービスクラスの導入とDIを学びました。

*   サービスクラスを使って、ビジネスロジックを分離した。
*   DIを使って、コンストラクタに書けば自動的に注入されることを学んだ。
*   コントローラーをスリムに保つ方法を学んだ。

次のセクションでは、リクエストクラスの活用について学びます。

---

## 📝 学習のポイント

- [ ] サービスクラスを作成した。
- [ ] DIを使った。
- [ ] コンストラクタに書けば使えることを理解した。
- [ ] コントローラーをスリムにした。
