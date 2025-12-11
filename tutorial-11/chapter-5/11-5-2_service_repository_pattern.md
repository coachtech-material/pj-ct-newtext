# Tutorial 11-5-2: サービスクラスとリポジトリパターン

## 🎯 このセクションで学ぶこと

*   サービスクラスの役割と実装方法を学ぶ。
*   リポジトリパターンの概念と実装方法を学ぶ。
*   アーキテクチャパターンを使ったコード設計を理解する。

---

## 導入：なぜアーキテクチャパターンが必要なのか

**アーキテクチャパターン（Architecture Pattern）**とは、**アプリケーションの構造を整理するための設計パターン**です。

アーキテクチャパターンを使うことで、以下のようなメリットがあります。

*   **コードの責任が明確になる**: 各クラスの役割が明確になる
*   **テストがしやすくなる**: 各クラスを独立してテストできる
*   **変更に強くなる**: 一部の変更が他の部分に影響しにくくなる

このセクションでは、**サービスクラス**と**リポジトリパターン**について学びます。

---

## 詳細解説

### 🔍 サービスクラスとは

**サービスクラス（Service Class）**とは、**ビジネスロジックを切り出すためのクラス**です。

サービスクラスを使うことで、コントローラーがシンプルになり、ビジネスロジックが整理されます。

---

### 🔍 サービスクラスの役割

サービスクラスは、以下のような処理を担当します。

*   **ビジネスロジック**: タスクの作成、更新、削除などの処理
*   **外部サービスとの連携**: メール送信、API呼び出しなど
*   **複雑な計算**: 統計情報の計算など

---

### 🔍 サービスクラスの実装例

**ファイル**: `app/Services/TaskService.php`

```php
<?php

namespace App\Services;

use App\Models\Task;
use App\Mail\TaskCreated;
use App\Mail\TaskUpdated;
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
        Log::info('Task created', ['task_id' => $task->id, 'user_id' => Auth::id()]);

        return $task;
    }

    /**
     * タスクを更新する
     */
    public function updateTask(Task $task, array $data)
    {
        $task->update($data);

        // メール送信
        Mail::to(Auth::user())->send(new TaskUpdated($task));

        // ログ記録
        Log::info('Task updated', ['task_id' => $task->id, 'user_id' => Auth::id()]);

        return $task;
    }

    /**
     * タスクを削除する
     */
    public function deleteTask(Task $task)
    {
        $taskId = $task->id;
        $task->delete();

        // ログ記録
        Log::info('Task deleted', ['task_id' => $taskId, 'user_id' => Auth::id()]);

        return true;
    }

    /**
     * タスクのステータスを変更する
     */
    public function changeStatus(Task $task, string $status)
    {
        $task->update(['status' => $status]);

        // ログ記録
        Log::info('Task status changed', [
            'task_id' => $task->id,
            'status' => $status,
            'user_id' => Auth::id()
        ]);

        return $task;
    }
}
```

---

### 🔍 コントローラーからサービスクラスを使う

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

    /**
     * タスクを作成する
     */
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

    /**
     * タスクを更新する
     */
    public function update(Request $request, Task $task)
    {
        $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'due_date' => 'nullable|date',
            'status' => 'required|in:pending,in_progress,completed',
        ]);

        $this->taskService->updateTask($task, $request->all());

        return redirect()->route('tasks.index')->with('success', 'タスクを更新しました。');
    }

    /**
     * タスクを削除する
     */
    public function destroy(Task $task)
    {
        $this->taskService->deleteTask($task);

        return redirect()->route('tasks.index')->with('success', 'タスクを削除しました。');
    }
}
```

---

### 🔍 リポジトリパターンとは

**リポジトリパターン（Repository Pattern）**とは、**データアクセスロジックを切り出すためのパターン**です。

リポジトリパターンを使うことで、以下のようなメリットがあります。

*   **データアクセスロジックが一箇所にまとまる**: データベースへのアクセス方法が統一される
*   **テストがしやすくなる**: リポジトリをモックに置き換えることで、テストが容易になる
*   **データベースの変更に強くなる**: データベースを変更しても、リポジトリのみを修正すればよい

---

### 🔍 リポジトリパターンの実装例

**ファイル**: `app/Repositories/TaskRepository.php`

```php
<?php

namespace App\Repositories;

use App\Models\Task;
use Illuminate\Support\Facades\Auth;

class TaskRepository
{
    /**
     * ログインユーザーの全タスクを取得する
     */
    public function getAllForCurrentUser()
    {
        return Task::where('user_id', Auth::id())->get();
    }

    /**
     * ログインユーザーの完了したタスクを取得する
     */
    public function getCompletedForCurrentUser()
    {
        return Task::where('user_id', Auth::id())
            ->where('status', 'completed')
            ->get();
    }

    /**
     * ログインユーザーの未完了のタスクを取得する
     */
    public function getPendingForCurrentUser()
    {
        return Task::where('user_id', Auth::id())
            ->where('status', 'pending')
            ->get();
    }

    /**
     * タスクをIDで取得する
     */
    public function findById(int $id)
    {
        return Task::findOrFail($id);
    }

    /**
     * タスクを作成する
     */
    public function create(array $data)
    {
        return Task::create($data);
    }

    /**
     * タスクを更新する
     */
    public function update(Task $task, array $data)
    {
        $task->update($data);
        return $task;
    }

    /**
     * タスクを削除する
     */
    public function delete(Task $task)
    {
        return $task->delete();
    }
}
```

---

### 🔍 サービスクラスからリポジトリを使う

**ファイル**: `app/Services/TaskService.php`

```php
<?php

namespace App\Services;

use App\Models\Task;
use App\Mail\TaskCreated;
use App\Mail\TaskUpdated;
use App\Repositories\TaskRepository;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Mail;

class TaskService
{
    protected $taskRepository;

    public function __construct(TaskRepository $taskRepository)
    {
        $this->taskRepository = $taskRepository;
    }

    /**
     * タスクを作成する
     */
    public function createTask(array $data)
    {
        $data['user_id'] = Auth::id();
        $data['status'] = 'pending';

        $task = $this->taskRepository->create($data);

        // メール送信
        Mail::to(Auth::user())->send(new TaskCreated($task));

        // ログ記録
        Log::info('Task created', ['task_id' => $task->id, 'user_id' => Auth::id()]);

        return $task;
    }

    /**
     * タスクを更新する
     */
    public function updateTask(Task $task, array $data)
    {
        $task = $this->taskRepository->update($task, $data);

        // メール送信
        Mail::to(Auth::user())->send(new TaskUpdated($task));

        // ログ記録
        Log::info('Task updated', ['task_id' => $task->id, 'user_id' => Auth::id()]);

        return $task;
    }

    /**
     * タスクを削除する
     */
    public function deleteTask(Task $task)
    {
        $taskId = $task->id;
        $this->taskRepository->delete($task);

        // ログ記録
        Log::info('Task deleted', ['task_id' => $taskId, 'user_id' => Auth::id()]);

        return true;
    }
}
```

---

### 🔍 アーキテクチャの全体像

```
Controller (コントローラー)
    ↓
Service (サービスクラス) ← ビジネスロジック
    ↓
Repository (リポジトリ) ← データアクセスロジック
    ↓
Model (モデル) ← データベースとのやり取り
```

*   **Controller**: HTTPリクエストを受け取り、レスポンスを返す
*   **Service**: ビジネスロジックを実行する
*   **Repository**: データベースへのアクセスを担当する
*   **Model**: データベースのテーブルと対応する

---

### 💡 TIP: いつリポジトリパターンを使うべきか

リポジトリパターンは、以下のような場合に有効です。

*   **大規模なアプリケーション**: データアクセスロジックが複雑な場合
*   **テストが重要な場合**: リポジトリをモックに置き換えることで、テストが容易になる
*   **データベースの変更が予想される場合**: リポジトリのみを修正すればよい

小規模なアプリケーションでは、リポジトリパターンを使わず、サービスクラスから直接Eloquentを使う方がシンプルです。

---

### 🚨 よくある間違い

#### 間違い1: コントローラーにビジネスロジックを書く

**対処法**: サービスクラスを作成し、ビジネスロジックを切り出します。

---

#### 間違い2: サービスクラスにデータアクセスロジックを書く

**対処法**: リポジトリを作成し、データアクセスロジックを切り出します。

---

#### 間違い3: 過度に複雑な設計をする

**対処法**: アプリケーションの規模に応じて、適切な設計を選択します。

---

## ✨ まとめ

このセクションでは、サービスクラスとリポジトリパターンについて学びました。

*   サービスクラスは、ビジネスロジックを切り出すためのクラスである。
*   リポジトリパターンは、データアクセスロジックを切り出すためのパターンである。
*   アーキテクチャパターンを使うことで、コードの責任が明確になり、テストがしやすくなる。
*   アプリケーションの規模に応じて、適切な設計を選択することが重要である。

次のセクションでは、テストについて学びます。

---

## 📝 学習のポイント

- [ ] サービスクラスの役割と実装方法を学んだ。
- [ ] リポジトリパターンの概念と実装方法を学んだ。
- [ ] アーキテクチャパターンを使ったコード設計を理解した。
