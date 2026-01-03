# Tutorial 12-5-10: 実践: リファクタリング演習

## 🎯 このセクションで学ぶこと

- これまで学んだリファクタリングの技術を、実際のコードに適用する
- リファクタリング前後のコードを比較して、改善点を理解する
- リファクタリングの手順を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ最後に『リファクタリング演習』を行うのか？」

リファクタリングの技法を学んだら、最後は「実践」です。

---

### 理由1: 学んだことを統合する

これまで学んだDRY、命名、Collectionメソッド、Form Request、可読性を**組み合わせて**実践します。

---

### 理由2: 実際のコードで練習

理論だけでなく、**実際のコードをリファクタリング**することで理解が深まります。

---

### 理由3: リファクタリングの判断力を養う

「どこをリファクタリングすべきか」「どの程度リファクタリングすべきか」という**判断力**を養います。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | コントローラーのリファクタリング | バリデーション分離、サービス導入 |
| Step 2 | モデルのリファクタリング | スコープで再利用性向上 |
| Step 3 | ビューのリファクタリング | パーシャルで重複排除 |
| Step 4 | リファクタリングの手順を学ぶ | 安全な進め方 |

> 💡 **ポイント**: 一度に全てを直そうとせず、少しずつ改善していきましょう。

---

## Step 1: コントローラーのリファクタリング

### 1-1. リファクタリング前のコード

以下のコントローラーをリファクタリングしてください。

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

### 1-2. 問題点を特定する

| 問題 | 説明 |
|------|------|
| バリデーション重複 | 同じルールが2箇所にある |
| 変数名が短い | `$t`では何か分からない |
| ビジネスロジック混在 | コントローラーが肥大化 |

---

### 1-3. フォームリクエストを作成する

**ファイル**: `app/Http/Requests/TaskRequest.php`

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class TaskRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'title' => 'required|max:255',
            'description' => 'nullable',
            'status' => 'required|in:pending,in_progress,completed',
            'priority' => 'required|integer|min:1|max:5',
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => 'タイトルは必須です。',
            'status.required' => 'ステータスは必須です。',
            'priority.required' => '優先度は必須です。',
        ];
    }
}
```

---

### 1-4. サービスクラスを作成する

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
    public function createTask(array $data, int $userId): Task
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
    
    public function updateTask(Task $task, array $data): Task
    {
        $task->update([
            'title' => $data['title'],
            'description' => $data['description'],
            'status' => $data['status'],
            'priority' => $data['priority'],
        ]);
        
        return $task;
    }
    
    private function sendNotification(Task $task): void
    {
        Mail::to(auth()->user()->email)->send(new TaskCreated($task));
    }
    
    private function logTaskCreation(Task $task): void
    {
        Log::info('Task created', ['task_id' => $task->id]);
    }
}
```

---

### 1-5. リファクタリング後のコントローラー

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Http\Requests\TaskRequest;
use App\Models\Task;
use App\Services\TaskService;

class TaskController extends Controller
{
    public function __construct(
        private TaskService $taskService
    ) {}
    
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

### 1-6. 改善点

| 改善 | 説明 |
|------|------|
| バリデーション分離 | フォームリクエストに移動 |
| ビジネスロジック分離 | サービスクラスに移動 |
| コントローラースリム化 | 各メソッドが2〜3行に |

---

## Step 2: モデルのリファクタリング

### 2-1. リファクタリング前のコード

以下のクエリをリファクタリングしてください。

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

### 2-2. Eloquentスコープを追加する

**ファイル**: `app/Models/Task.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Task extends Model
{
    protected $fillable = [
        'user_id', 'title', 'description', 'status', 'priority'
    ];

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

---

### 2-3. リファクタリング後のコントローラー

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

### 2-4. 改善点

| 改善 | 説明 |
|------|------|
| 再利用性向上 | スコープを組み合わせて使える |
| 可読性向上 | クエリの意図が明確 |
| 保守性向上 | 変更が1箇所で済む |

---

## Step 3: ビューのリファクタリング

### 3-1. リファクタリング前のコード

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

**ファイル**: `resources/views/tasks/completed.blade.php`（同じコード）

---

### 3-2. パーシャルを作成する

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

---

### 3-3. パーシャルを使用する

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<h1>タスク一覧</h1>
@include('tasks._table')
```

**ファイル**: `resources/views/tasks/completed.blade.php`

```blade
<h1>完了したタスク</h1>
@include('tasks._table')
```

---

### 3-4. 改善点

| 改善 | 説明 |
|------|------|
| 重複排除 | テーブルコードが1箇所に |
| 再利用性向上 | 他のビューでも使える |
| 保守性向上 | 変更が1箇所で済む |

---

## Step 4: リファクタリングの手順を学ぶ

### 4-1. 安全なリファクタリングの手順

| 順番 | 手順 | 説明 |
|------|------|------|
| 1 | テストを書く | リファクタリング前に動作を保証 |
| 2 | 小さく変更する | 一度に大きく変更しない |
| 3 | テストを実行する | 変更後に動作を確認 |
| 4 | 繰り返す | 1〜3を繰り返す |

---

### 4-2. リファクタリングのタイミング

| タイミング | 説明 |
|------------|------|
| 新機能追加前 | コードを整理してから追加 |
| バグ修正前 | コードを整理してから修正 |
| コードレビュー後 | 指摘された箇所を改善 |

---

## 🚨 よくある間違い

### 間違い1: テストを書かずにリファクタリングする

**問題**: バグが発生しても気づかない

**対処法**: リファクタリング前に、テストを書きます。

---

### 間違い2: 一度に大きく変更する

**問題**: 問題が発生したときに原因が特定しにくい

**対処法**: 小さく変更して、テストを実行します。

---

### 間違い3: リファクタリングしすぎる

**問題**: 時間がかかりすぎる

**対処法**: 必要な箇所だけをリファクタリングします。

---

## 💡 TIP: リファクタリングの本

リファクタリングについて、さらに学びたい場合は、以下の本がおすすめです。

**リファクタリング 既存のコードを安全に改善する（第2版）** by Martin Fowler

---

## ✨ まとめ

このセクションでは、リファクタリング演習を行いました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | コントローラーのリファクタリング（Form Request、Service） |
| Step 2 | モデルのリファクタリング（Eloquentスコープ） |
| Step 3 | ビューのリファクタリング（パーシャル） |
| Step 4 | リファクタリングの手順と注意点 |

次の章では、テストについて学びます。

---
