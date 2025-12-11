# Tutorial 11-6-4: 認可機能のテスト

## 🎯 このセクションで学ぶこと

*   ポリシーを使った認可機能のテストを書く方法を学ぶ。
*   所有権チェックのテストを書く方法を学ぶ。
*   ミドルウェアのテストを書く方法を学ぶ。

---

## 導入：なぜ認可機能をテストするのか

**認可機能**は、**誰が何をできるか**を制御する仕組みです。

認可機能をテストすることで、**不正な操作を防ぎ、データの安全性を保つ**ことができます。

---

## 詳細解説

### 🔍 ポリシーの作成

まず、ポリシーを作成します。

```bash
php artisan make:policy TaskPolicy --model=Task
```

**ファイル**: `app/Policies/TaskPolicy.php`

```php
<?php

namespace App\Policies;

use App\Models\Task;
use App\Models\User;

class TaskPolicy
{
    public function view(User $user, Task $task)
    {
        return $user->id === $task->user_id;
    }

    public function update(User $user, Task $task)
    {
        return $user->id === $task->user_id;
    }

    public function delete(User $user, Task $task)
    {
        return $user->id === $task->user_id;
    }
}
```

---

### 🔍 コントローラーでポリシーを使う

コントローラーで、ポリシーを使います。

```php
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

### 🔍 所有権チェックのテスト（正常系）

自分のタスクを更新できることをテストします。

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

### 🔍 所有権チェックのテスト（異常系）

他人のタスクを更新できないことをテストします。

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

### 🔍 削除の認可テスト

自分のタスクを削除できることをテストします。

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

### 🔍 削除の認可テスト（異常系）

他人のタスクを削除できないことをテストします。

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

### 🔍 閲覧の認可テスト

自分のタスクを閲覧できることをテストします。

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

### 🔍 閲覧の認可テスト（異常系）

他人のタスクを閲覧できないことをテストします。

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

### 🔍 ポリシーのユニットテスト

ポリシー自体をユニットテストすることもできます。

```bash
php artisan make:test TaskPolicyTest --unit
```

**ファイル**: `tests/Unit/TaskPolicyTest.php`

```php
<?php

namespace Tests\Unit;

use App\Models\Task;
use App\Models\User;
use App\Policies\TaskPolicy;
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

### 🔍 実践演習: テストを作成してください

以下のテストを作成してください。

**テスト内容**:
*   管理者は、すべてのタスクを削除できることを確認する

---

**解答例**:

まず、ポリシーを修正します。

**ファイル**: `app/Policies/TaskPolicy.php`

```php
public function delete(User $user, Task $task)
{
    return $user->id === $task->user_id || $user->is_admin;
}
```

次に、テストを作成します。

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

### 🔍 ミドルウェアのテスト

ミドルウェアをテストすることもできます。

```php
public function test_未ログインユーザーはタスク一覧にアクセスできない()
{
    // 実行
    $response = $this->get('/tasks');
    
    // 検証
    $response->assertStatus(302);
    $response->assertRedirect('/login');
}

public function test_ログインユーザーはタスク一覧にアクセスできる()
{
    // 準備
    $user = User::factory()->create();
    
    // 実行
    $response = $this->actingAs($user)->get('/tasks');
    
    // 検証
    $response->assertStatus(200);
}
```

---

### 💡 TIP: Gate::allowを使う

`Gate::allow()`を使って、認可をテストすることもできます。

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

### 🚨 よくある間違い

#### 間違い1: authorize()を忘れる

コントローラーで`authorize()`を忘れると、認可チェックがスキップされます。

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

#### 間違い2: ポリシーを登録し忘れる

ポリシーを作成したら、`AuthServiceProvider`に登録します。

**ファイル**: `app/Providers/AuthServiceProvider.php`

```php
protected $policies = [
    Task::class => TaskPolicy::class,
];
```

---

#### 間違い3: 403エラーをテストしない

認可エラー（403）のテストを忘れないようにします。

```php
$response->assertStatus(403);
```

---

## ✨ まとめ

このセクションでは、認可機能のテストを学びました。

*   ポリシーを使った認可機能のテストを書いた。
*   所有権チェックのテストを書いた。
*   ポリシーのユニットテストを書いた。

次のセクションでは、テストカバレッジの確認について学びます。

---

## 📝 学習のポイント

- [ ] ポリシーを作成した。
- [ ] 所有権チェックのテストを書いた。
- [ ] 認可エラーのテストを書いた。
- [ ] ポリシーのユニットテストを書いた。
