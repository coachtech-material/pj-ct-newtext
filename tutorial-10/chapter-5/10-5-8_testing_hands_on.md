# Tutorial 10-5-8: テスト - ハンズオン演習

## 📝 このセクションの目的

Chapter 11で学んだテストを実際に手を動かして確認します。フィーチャーテストを作成して、アプリケーションの動作を検証しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

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

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？テストはアプリケーションの品質を保つために不可欠です。一緒に手を動かしながら、タスク作成機能のテストを実装していきましょう。

### 💭 実装の思考プロセス

テストを実装する際、以下の順番で考えると効率的です：

1. **テストクラスを作成**：Artisanコマンドで生成
2. **RefreshDatabaseを使用**：テスト用データベースをリセット
3. **正常系テストを実装**：機能が正しく動作することを確認
4. **異常系テストを実装**：バリデーションエラーをテスト
5. **テストを実行**：全テストがパスすることを確認

テストのポイントは「正常系と異常系の両方をテストし、アプリケーションの品質を保つ」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: テストクラスを作成する

**何を考えているか**：
- 「タスク機能をテストするクラスが必要だ」
- 「TaskTestという名前にしよう」
- 「Artisanコマンドで簡単に生成できる」

ターミナルで以下のコマンドを実行します：

```bash
php artisan make:test TaskTest
```

**コマンド解説**：

```bash
php artisan make:test TaskTest
```
→ `TaskTest`フィーチャーテストを生成します。`tests/Feature/TaskTest.php`が作成されます。

---

#### ステップ2: RefreshDatabaseを使用する

**何を考えているか**：
- 「テストごとにデータベースをリセットしたい」
- 「RefreshDatabaseトレイトで簡単に実現できる」
- 「テスト間の干渉を防ぐ」

`tests/Feature/TaskTest.php`を開いて、以下のように編集します：

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
}
```

**コード解説**：

```php
use Illuminate\Foundation\Testing\RefreshDatabase;
```
→ `RefreshDatabase`トレイトをインポートします。

```php
use RefreshDatabase;
```
→ `RefreshDatabase`トレイトを使用します。各テストの前にデータベースがリセットされ、テスト間の干渉を防ぎます。

---

#### ステップ3: 正常系テストを実装する

**何を考えているか**：
- 「タスクが正しく作成されることをテストしよう」
- 「テストユーザーを作成して認証しよう」
- 「データベースにデータが保存されることを確認しよう」

テストメソッドを追加します：

```php
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
```

**コード解説**：

```php
$user = User::factory()->create();
```
→ `User::factory()->create()`でテスト用ユーザーを作成します。Factoryでダミーデータを簡単に生成できます。

```php
$response = $this->actingAs($user)->post('/tasks', [
    'title' => 'テストタスク',
    'description' => 'テスト説明',
    'status' => 'pending',
]);
```
→ `actingAs($user)`でユーザーとして認証し、`post()`でタスク作成リクエストを送信します。

```php
$response->assertStatus(302);
$response->assertRedirect('/tasks');
```
→ `assertStatus(302)`でリダイレクトステータスを確認し、`assertRedirect()`でリダイレクト先を確認します。

```php
$this->assertDatabaseHas('tasks', [
    'title' => 'テストタスク',
    'description' => 'テスト説明',
]);
```
→ `assertDatabaseHas()`でデータベースにデータが保存されていることを確認します。

---

#### ステップ4: 異常系テストを実装する

**何を考えているか**：
- 「バリデーションエラーが正しく発生することをテストしよう」
- 「必須項目が空の場合のテストを追加しよう」

テストメソッドを追加します：

```php
public function test_task_title_is_required()
{
    $user = User::factory()->create();
    
    $response = $this->actingAs($user)->post('/tasks', [
        'description' => 'テスト説明',
    ]);
    
    $response->assertSessionHasErrors('title');
}
```

**コード解説**：

```php
$response = $this->actingAs($user)->post('/tasks', [
    'description' => 'テスト説明',
]);
```
→ `title`を含まないデータでリクエストを送信します。

```php
$response->assertSessionHasErrors('title');
```
→ `assertSessionHasErrors()`で`title`フィールドにバリデーションエラーがあることを確認します。

---

#### ステップ5: テストを実行する

**何を考えているか**：
- 「全テストがパスすることを確認しよう」
- 「php artisan testで実行できる」

ターミナルで以下のコマンドを実行します：

```bash
php artisan test
```

**コマンド解説**：

```bash
php artisan test
```
→ 全テストを実行します。緑色のチェックマークが表示されればテスト成功です。

特定のテストファイルだけを実行する場合：

```bash
php artisan test --filter TaskTest
```

---

### ✨ 完成！

これでフィーチャーテストが実装できました！正常系と異常系の両方をテストし、アプリケーションの品質を保つことができましたね。

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

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ Chapter 11で学んだテストを実際に手を動かして確認します。フィーチャーテストを作成して、アプリケーションの動作を検証しましょう。

引き続き、次のセクションも頑張りましょう！

---
