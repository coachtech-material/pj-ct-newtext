# Tutorial 9-11-8: テスト - ハンズオン演習

## 📝 このセクションの目的

Chapter 11で学んだテストを実際に手を動かして確認します。フィーチャーテストを作成して、アプリケーションの動作を検証しましょう。

---

## 🎯 演習課題：タスク作成機能のテスト

### 📋 要件

1. `TaskTest`を作成
2. タスク作成のテストを実装
3. バリデーションのテストを実装

---

## 💡 ヒント

```bash
php artisan make:test TaskTest
```

```php
public function test_task_can_be_created()
{
    $response = $this->post('/tasks', [
        'title' => 'テストタスク',
        'description' => 'テスト説明',
    ]);
    
    $response->assertStatus(302);
    $this->assertDatabaseHas('tasks', [
        'title' => 'テストタスク',
    ]);
}
```

---

## 📖 模範解答

### TaskTest.php

```php
<?php

namespace Tests\Feature;

use App\Models\Task;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class TaskTest extends TestCase
{
    use RefreshDatabase;

    public function test_task_can_be_created()
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)->post('/tasks', [
            'title' => 'テストタスク',
            'description' => 'テスト説明',
            'status' => 'pending',
        ]);
        
        $response->assertStatus(302);
        $response->assertRedirect('/tasks');
        
        $this->assertDatabaseHas('tasks', [
            'title' => 'テストタスク',
            'description' => 'テスト説明',
        ]);
    }

    public function test_task_title_is_required()
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)->post('/tasks', [
            'description' => 'テスト説明',
        ]);
        
        $response->assertSessionHasErrors('title');
    }

    public function test_task_can_be_updated()
    {
        $user = User::factory()->create();
        $task = Task::factory()->create();
        
        $response = $this->actingAs($user)->put("/tasks/{$task->id}", [
            'title' => '更新されたタスク',
            'description' => '更新された説明',
            'status' => 'completed',
        ]);
        
        $response->assertStatus(302);
        
        $this->assertDatabaseHas('tasks', [
            'id' => $task->id,
            'title' => '更新されたタスク',
        ]);
    }

    public function test_task_can_be_deleted()
    {
        $user = User::factory()->create();
        $task = Task::factory()->create();
        
        $response = $this->actingAs($user)->delete("/tasks/{$task->id}");
        
        $response->assertStatus(302);
        
        $this->assertDatabaseMissing('tasks', [
            'id' => $task->id,
        ]);
    }
}
```

### テスト実行

```bash
php artisan test
php artisan test --filter TaskTest
```

---

## 💪 自己評価チェックリスト

- [ ] フィーチャーテストを作成できた
- [ ] RefreshDatabaseを使えた
- [ ] assertDatabaseHas()を使えた
- [ ] assertStatus()を使えた
- [ ] actingAs()で認証ユーザーをシミュレートできた

すべてチェックできたら、Tutorial 10に進みましょう！
