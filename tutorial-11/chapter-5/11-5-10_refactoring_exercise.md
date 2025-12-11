# Tutorial 11-5-10: 実践: リファクタリング演習

## 🎯 このセクションで学ぶこと

*   これまで学んだリファクタリングの技術を、実際のコードに適用する。
*   リファクタリング前後のコードを比較して、改善点を理解する。
*   リファクタリングの手順を学ぶ。

---

## 導入：リファクタリング演習の目的

このセクションでは、**実際のコード**をリファクタリングします。

これまで学んだ技術を、**実践的に使う**ことで、リファクタリングのスキルを身につけます。

---

## 詳細解説

### 🔍 演習1: コントローラーのリファクタリング

以下のコントローラーをリファクタリングしてください。

**リファクタリング前**:

```php
<?php

namespace App\Http\Controllers;

use App\Models\Task;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Facades\Log;
use App\Mail\TaskCreated;

class TaskController extends Controller
{
    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'description' => 'nullable',
            'status' => 'required|in:pending,in_progress,completed',
            'priority' => 'required|integer|min:1|max:5',
        ]);
        
        $t = new Task();
        $t->title = $validated['title'];
        $t->description = $validated['description'];
        $t->status = $validated['status'];
        $t->priority = $validated['priority'];
        $t->user_id = auth()->id();
        $t->save();
        
        Mail::to(auth()->user()->email)->send(new TaskCreated($t));
        Log::info('Task created', ['task_id' => $t->id]);
        
        return redirect()->route('tasks.index');
    }
    
    public function update(Request $request, Task $task)
    {
        $validated = $request->validate([
            'title' => 'required|max:255',
            'description' => 'nullable',
            'status' => 'required|in:pending,in_progress,completed',
            'priority' => 'required|integer|min:1|max:5',
        ]);
        
        $task->title = $validated['title'];
        $task->description = $validated['description'];
        $task->status = $validated['status'];
        $task->priority = $validated['priority'];
        $task->save();
        
        return redirect()->route('tasks.index');
    }
}
```

---

**問題点**:
*   バリデーションルールが重複している
*   変数名が短すぎる（`$t`）
*   ビジネスロジックがコントローラーに書かれている

---

**リファクタリング後**:

**ファイル**: `app/Http/Requests/TaskRequest.php`

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class TaskRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'title' => 'required|max:255',
            'description' => 'nullable',
            'status' => 'required|in:pending,in_progress,completed',
            'priority' => 'required|integer|min:1|max:5',
        ];
    }

    public function messages()
    {
        return [
            'title.required' => 'タイトルは必須です。',
            'status.required' => 'ステータスは必須です。',
            'priority.required' => '優先度は必須です。',
        ];
    }
}
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
        $task = Task::create([
            'title' => $data['title'],
            'description' => $data['description'],
            'status' => $data['status'],
            'priority' => $data['priority'],
            'user_id' => $userId,
        ]);
        
        $this->sendNotification($task);
        $this->logTaskCreation($task);
        
        return $task;
    }
    
    public function updateTask(Task $task, array $data)
    {
        $task->update([
            'title' => $data['title'],
            'description' => $data['description'],
            'status' => $data['status'],
            'priority' => $data['priority'],
        ]);
        
        return $task;
    }
    
    private function sendNotification(Task $task)
    {
        Mail::to(auth()->user()->email)->send(new TaskCreated($task));
    }
    
    private function logTaskCreation(Task $task)
    {
        Log::info('Task created', ['task_id' => $task->id]);
    }
}
```

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Http\Requests\TaskRequest;
use App\Models\Task;
use App\Services\TaskService;

class TaskController extends Controller
{
    private $taskService;
    
    public function __construct(TaskService $taskService)
    {
        $this->taskService = $taskService;
    }
    
    public function store(TaskRequest $request)
    {
        $this->taskService->createTask($request->validated(), auth()->id());
        return redirect()->route('tasks.index');
    }
    
    public function update(TaskRequest $request, Task $task)
    {
        $this->taskService->updateTask($task, $request->validated());
        return redirect()->route('tasks.index');
    }
}
```

---

**改善点**:
*   バリデーションルールがフォームリクエストに分離された
*   ビジネスロジックがサービスクラスに分離された
*   変数名が分かりやすくなった
*   コントローラーがスリムになった

---

### 🔍 演習2: モデルのリファクタリング

以下のクエリをリファクタリングしてください。

**リファクタリング前**:

```php
// コントローラー1
$tasks = Task::where('user_id', auth()->id())
    ->where('status', 'pending')
    ->orderBy('created_at', 'desc')
    ->get();

// コントローラー2
$tasks = Task::where('user_id', auth()->id())
    ->where('status', 'completed')
    ->orderBy('created_at', 'desc')
    ->get();

// コントローラー3
$tasks = Task::where('user_id', auth()->id())
    ->where('priority', '>=', 3)
    ->orderBy('created_at', 'desc')
    ->get();
```

---

**リファクタリング後**:

**ファイル**: `app/Models/Task.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Task extends Model
{
    public function scopeForUser($query, $userId)
    {
        return $query->where('user_id', $userId);
    }

    public function scopeWithStatus($query, $status)
    {
        return $query->where('status', $status);
    }

    public function scopeHighPriority($query)
    {
        return $query->where('priority', '>=', 3);
    }

    public function scopeLatestFirst($query)
    {
        return $query->orderBy('created_at', 'desc');
    }
}
```

**コントローラー**:

```php
// コントローラー1
$tasks = Task::forUser(auth()->id())
    ->withStatus('pending')
    ->latestFirst()
    ->get();

// コントローラー2
$tasks = Task::forUser(auth()->id())
    ->withStatus('completed')
    ->latestFirst()
    ->get();

// コントローラー3
$tasks = Task::forUser(auth()->id())
    ->highPriority()
    ->latestFirst()
    ->get();
```

---

**改善点**:
*   クエリが再利用可能になった
*   クエリの意図が分かりやすくなった

---

### 🔍 演習3: ビューのリファクタリング

以下のビューをリファクタリングしてください。

**リファクタリング前**:

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<table>
    <thead>
        <tr>
            <th>タイトル</th>
            <th>ステータス</th>
            <th>優先度</th>
            <th>作成日</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($tasks as $task)
        <tr>
            <td>{{ $task->title }}</td>
            <td>{{ $task->status }}</td>
            <td>{{ $task->priority }}</td>
            <td>{{ $task->created_at->format('Y-m-d') }}</td>
        </tr>
        @endforeach
    </tbody>
</table>
```

**ファイル**: `resources/views/tasks/completed.blade.php`

```blade
<table>
    <thead>
        <tr>
            <th>タイトル</th>
            <th>ステータス</th>
            <th>優先度</th>
            <th>作成日</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($tasks as $task)
        <tr>
            <td>{{ $task->title }}</td>
            <td>{{ $task->status }}</td>
            <td>{{ $task->priority }}</td>
            <td>{{ $task->created_at->format('Y-m-d') }}</td>
        </tr>
        @endforeach
    </tbody>
</table>
```

---

**リファクタリング後**:

**ファイル**: `resources/views/tasks/_table.blade.php`

```blade
<table>
    <thead>
        <tr>
            <th>タイトル</th>
            <th>ステータス</th>
            <th>優先度</th>
            <th>作成日</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($tasks as $task)
        <tr>
            <td>{{ $task->title }}</td>
            <td>{{ $task->status }}</td>
            <td>{{ $task->priority }}</td>
            <td>{{ $task->created_at->format('Y-m-d') }}</td>
        </tr>
        @endforeach
    </tbody>
</table>
```

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
@include('tasks._table')
```

**ファイル**: `resources/views/tasks/completed.blade.php`

```blade
@include('tasks._table')
```

---

**改善点**:
*   重複コードが削除された
*   パーシャルが再利用可能になった

---

### 🔍 リファクタリングの手順

リファクタリングは、以下の手順で行います。

1.  **テストを書く**: リファクタリング前に、テストを書きます。
2.  **小さく変更する**: 一度に大きく変更せず、小さく変更します。
3.  **テストを実行する**: 変更後、テストを実行して、動作を確認します。
4.  **繰り返す**: 1〜3を繰り返します。

---

### 🔍 リファクタリングのタイミング

リファクタリングは、以下のタイミングで行います。

*   **新機能を追加する前**: コードを整理してから、新機能を追加します。
*   **バグを修正する前**: コードを整理してから、バグを修正します。
*   **コードレビューで指摘された時**: 指摘された箇所をリファクタリングします。

---

### 💡 TIP: リファクタリングの本

リファクタリングについて、さらに学びたい場合は、以下の本がおすすめです。

*   **リファクタリング 既存のコードを安全に改善する（第2版）** by Martin Fowler

---

### 🚨 よくある間違い

#### 間違い1: テストを書かずにリファクタリングする

テストを書かずにリファクタリングすると、バグが発生しやすくなります。

**対処法**: リファクタリング前に、テストを書きます。

---

#### 間違い2: 一度に大きく変更する

一度に大きく変更すると、バグが発生しやすくなります。

**対処法**: 小さく変更して、テストを実行します。

---

#### 間違い3: リファクタリングしすぎる

リファクタリングしすぎると、時間がかかります。

**対処法**: 必要な箇所だけをリファクタリングします。

---

## ✨ まとめ

このセクションでは、リファクタリング演習を行いました。

*   コントローラーをリファクタリングした。
*   モデルをリファクタリングした。
*   ビューをリファクタリングした。
*   リファクタリングの手順を学んだ。

次の章では、テストについて学びます。

---

## 📝 学習のポイント

- [ ] コントローラーをリファクタリングした。
- [ ] モデルをリファクタリングした。
- [ ] ビューをリファクタリングした。
- [ ] リファクタリングの手順を理解した。
