# Tutorial 12-6-4: 認可機能のテスト

## 🎯 このセクションで学ぶこと

- ポリシーを使った認可機能のテストを書く方法を学ぶ
- 所有権チェックのテストを書く方法を学ぶ
- ミドルウェアのテストを書く方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ認証テストの後に『認可テスト』を書くのか？」

認証テストができたら、次は「認可テスト」です。

---

### 理由1: 認証と認可は別物

| 概念 | 説明 |
|------|------|
| 認証（Authentication） | 「誰か」を確認する |
| 認可（Authorization） | 「何ができるか」を確認する |

認証が通っても、**権限がなければアクセスできない**ことを確認します。

---

### 理由2: 他人のデータにアクセスできないことを確認

ログインしていても、**他のユーザーのタスクにはアクセスできない**ことを確認します。

```php
$user = User::factory()->create();
$otherTask = Task::factory()->create(); // 別のユーザーのタスク

$response = $this->actingAs($user)->get("/tasks/{$otherTask->id}");
$response->assertStatus(403);
```

---

### 理由3: Policyのテスト

Policyで定義した認可ロジックが**正しく動作する**ことを確認します。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | ポリシーの作成 | 認可ロジックを定義 |
| Step 2 | 閲覧の認可テスト | 正常系・異常系を確認 |
| Step 3 | 更新・削除の認可テスト | 所有権チェックを確認 |
| Step 4 | ポリシーのユニットテスト | 認可ロジックを直接テスト |

> 💡 **ポイント**: 認可テストは、セキュリティ上非常に重要です。

---

## Step 1: ポリシーの作成

### 1-1. ポリシーを生成する

```bash
php artisan make:policy TaskPolicy --model=Task
```

---

### 1-2. ポリシーを定義する

**ファイル**: `app/Policies/TaskPolicy.php`

```php
<?php

namespace App\Policies;

use App\Models\Task;
use App\Models\User;

class TaskPolicy
{
    public function view(User $user, Task $task): bool
    {
        return $user->id === $task->user_id;
    }

    public function update(User $user, Task $task): bool
    {
        return $user->id === $task->user_id;
    }

    public function delete(User $user, Task $task): bool
    {
        return $user->id === $task->user_id;
    }
}
```

---

### 1-3. コントローラーでポリシーを使う

```php
public function show(Task $task)
{
    $this->authorize('view', $task);
    return view('tasks.show', compact('task'));
}

public function update(TaskRequest $request, Task $task)
{
    $this->authorize('update', $task);
    $this->taskService->updateTask($task, $request->validated());
    return redirect()->route('tasks.index');
}

public function destroy(Task $task)
{
    $this->authorize('delete', $task);
    $task->delete();
    return redirect()->route('tasks.index');
}
```

---

## Step 2: 閲覧の認可テスト

### 2-1. 正常系: 自分のタスクを閲覧できる

```php
public function test_自分のタスクを閲覧できる()
{
    // 準備
    $user = User::factory()->create();
    $task = Task::factory()->create([
        'user_id' => $user->id,
        'title' => 'テストタスク',
    ]);
    
    // 実行
    $response = $this->actingAs($user)->get("/tasks/{$task->id}");
    
    // 検証
    $response->assertStatus(200);
    $response->assertSee('テストタスク');
}
```

---

### 2-2. 異常系: 他人のタスクを閲覧できない

```php
public function test_他人のタスクを閲覧できない()
{
    // 準備
    $user = User::factory()->create();
    $otherUser = User::factory()->create();
    $task = Task::factory()->create([
        'user_id' => $otherUser->id,
        'title' => 'テストタスク',
    ]);
    
    // 実行
    $response = $this->actingAs($user)->get("/tasks/{$task->id}");
    
    // 検証
    $response->assertStatus(403);
}
```

---

## Step 3: 更新・削除の認可テスト

### 3-1. 正常系: 自分のタスクを更新できる

```php
public function test_自分のタスクを更新できる()
{
    // 準備
    $user = User::factory()->create();
    $task = Task::factory()->create(['user_id' => $user->id]);
    
    // 実行
    $response = $this->actingAs($user)->put("/tasks/{$task->id}", [
        'title' => '更新されたタイトル',
        'description' => '更新された説明',
        'status' => 'completed',
        'priority' => 5,
    ]);
    
    // 検証
    $response->assertStatus(302);
    $this->assertDatabaseHas('tasks', [
        'id' => $task->id,
        'title' => '更新されたタイトル',
    ]);
}
```

---

### 3-2. 異常系: 他人のタスクを更新できない

```php
public function test_他人のタスクを更新できない()
{
    // 準備
    $user = User::factory()->create();
    $otherUser = User::factory()->create();
    $task = Task::factory()->create([
        'user_id' => $otherUser->id,
        'title' => '元のタイトル',
    ]);
    
    // 実行
    $response = $this->actingAs($user)->put("/tasks/{$task->id}", [
        'title' => '更新されたタイトル',
        'description' => '更新された説明',
        'status' => 'completed',
        'priority' => 5,
    ]);
    
    // 検証
    $response->assertStatus(403);
    $this->assertDatabaseHas('tasks', [
        'id' => $task->id,
        'title' => '元のタイトル',
    ]);
}
```

---

### 3-3. 正常系: 自分のタスクを削除できる

```php
public function test_自分のタスクを削除できる()
{
    // 準備
    $user = User::factory()->create();
    $task = Task::factory()->create(['user_id' => $user->id]);
    
    // 実行
    $response = $this->actingAs($user)->delete("/tasks/{$task->id}");
    
    // 検証
    $response->assertStatus(302);
    $this->assertDatabaseMissing('tasks', [
        'id' => $task->id,
    ]);
}
```

---

### 3-4. 異常系: 他人のタスクを削除できない

```php
public function test_他人のタスクを削除できない()
{
    // 準備
    $user = User::factory()->create();
    $otherUser = User::factory()->create();
    $task = Task::factory()->create(['user_id' => $otherUser->id]);
    
    // 実行
    $response = $this->actingAs($user)->delete("/tasks/{$task->id}");
    
    // 検証
    $response->assertStatus(403);
    $this->assertDatabaseHas('tasks', [
        'id' => $task->id,
    ]);
}
```

---

## Step 4: ポリシーのユニットテスト

### 4-1. ユニットテストを作成する

```bash
php artisan make:test TaskPolicyTest --unit
```

---

### 4-2. ポリシーを直接テストする

**ファイル**: `tests/Unit/TaskPolicyTest.php`

```php
<?php

namespace Tests\Unit;

use App\Models\Task;
use App\Models\User;
use App\Policies\TaskPolicy;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class TaskPolicyTest extends TestCase
{
    use RefreshDatabase;
    
    public function test_所有者はタスクを更新できる()
    {
        // 準備
        $user = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $user->id]);
        $policy = new TaskPolicy();
        
        // 実行
        $result = $policy->update($user, $task);
        
        // 検証
        $this->assertTrue($result);
    }
    
    public function test_所有者以外はタスクを更新できない()
    {
        // 準備
        $user = User::factory()->create();
        $otherUser = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $otherUser->id]);
        $policy = new TaskPolicy();
        
        // 実行
        $result = $policy->update($user, $task);
        
        // 検証
        $this->assertFalse($result);
    }
}
```

---

### 4-3. 実践演習: 管理者のテスト

以下のテストを作成してください。

**テスト内容**: 管理者は、すべてのタスクを削除できることを確認する

**ポリシーの修正**:

```php
public function delete(User $user, Task $task): bool
{
    return $user->id === $task->user_id || $user->is_admin;
}
```

**テスト**:

```php
public function test_管理者はすべてのタスクを削除できる()
{
    // 準備
    $admin = User::factory()->create(['is_admin' => true]);
    $otherUser = User::factory()->create();
    $task = Task::factory()->create(['user_id' => $otherUser->id]);
    
    // 実行
    $response = $this->actingAs($admin)->delete("/tasks/{$task->id}");
    
    // 検証
    $response->assertStatus(302);
    $this->assertDatabaseMissing('tasks', [
        'id' => $task->id,
    ]);
}
```

---

## 🚨 よくある間違い

### 間違い1: authorize()を忘れる

**問題**: 認可チェックがスキップされる

```php
// ❌ 間違い
public function update(TaskRequest $request, Task $task)
{
    // authorize()を忘れている
    $this->taskService->updateTask($task, $request->validated());
    return redirect()->route('tasks.index');
}

// ✅ 正しい
public function update(TaskRequest $request, Task $task)
{
    $this->authorize('update', $task);
    $this->taskService->updateTask($task, $request->validated());
    return redirect()->route('tasks.index');
}
```

---

### 間違い2: ポリシーを登録し忘れる

**問題**: ポリシーが適用されない

**ファイル**: `app/Providers/AuthServiceProvider.php`

```php
protected $policies = [
    Task::class => TaskPolicy::class,
];
```

---

### 間違い3: 403エラーをテストしない

**問題**: 認可の異常系を見逃す

**対処法**: 必ず403エラーのテストを書きます。

```php
$response->assertStatus(403);
```

---

## 💡 TIP: Gate::allowsを使う

`Gate::allows()`を使って、認可をテストすることもできます。

```php
use Illuminate\Support\Facades\Gate;

public function test_所有者はタスクを更新できる()
{
    $user = User::factory()->create();
    $task = Task::factory()->create(['user_id' => $user->id]);
    
    $this->assertTrue(Gate::forUser($user)->allows('update', $task));
}

public function test_所有者以外はタスクを更新できない()
{
    $user = User::factory()->create();
    $otherUser = User::factory()->create();
    $task = Task::factory()->create(['user_id' => $otherUser->id]);
    
    $this->assertFalse(Gate::forUser($user)->allows('update', $task));
}
```

---

## ✨ まとめ

このセクションでは、認可機能のテストを学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | ポリシーの作成と使用 |
| Step 2 | 閲覧の認可テスト（正常系・異常系） |
| Step 3 | 更新・削除の認可テスト（正常系・異常系） |
| Step 4 | ポリシーのユニットテスト |

次のセクションでは、テストカバレッジの確認について学びます。

---
