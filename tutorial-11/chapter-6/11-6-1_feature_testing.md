# Tutorial 11-6-1: 機能テストの実装

## 🎯 このセクションで学ぶこと

*   機能テスト（Feature Test）の概念と重要性を理解する。
*   Laravelの機能テストの書き方を学ぶ。
*   タスク管理システムの機能テストを実装する。

---

## 導入：なぜテストが必要なのか

**テスト（Testing）**とは、**アプリケーションが正しく動作することを確認する作業**です。

テストを書くことで、以下のようなメリットがあります。

*   **バグを早期に発見できる**: コードを変更した際に、既存の機能が壊れていないか確認できる
*   **リファクタリングが安全にできる**: テストがあれば、コードを変更しても安心
*   **仕様書としての役割**: テストコードを読むことで、アプリケーションの動作を理解できる

このセクションでは、**機能テスト（Feature Test）**の実装方法を学びます。

---

## 詳細解説

### 🔍 機能テストとは

**機能テスト（Feature Test）**とは、**アプリケーション全体の動作を確認するテスト**です。

機能テストでは、以下のようなことを確認します。

*   **HTTPリクエストとレスポンス**: 正しいステータスコードが返されるか
*   **データベースの状態**: データが正しく保存されているか
*   **ビューの表示**: 正しいビューが表示されるか

---

### 🔍 テストの作成

Laravelでは、`artisan`コマンドを使ってテストを作成します。

```bash
php artisan make:test TaskTest
```

これにより、`tests/Feature/TaskTest.php`が作成されます。

---

### 🔍 テストの基本構造

**ファイル**: `tests/Feature/TaskTest.php`

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;

class TaskTest extends TestCase
{
    use RefreshDatabase;

    /**
     * タスク一覧ページが表示されることを確認する
     */
    public function test_task_index_page_is_displayed()
    {
        $response = $this->get('/tasks');

        $response->assertStatus(200);
    }
}
```

---

### 🔍 コードリーディング

#### `use RefreshDatabase;`

*   `RefreshDatabase`トレイトを使うことで、テスト実行後にデータベースがリセットされます。
*   これにより、テスト間でデータが干渉しなくなります。

---

#### `public function test_task_index_page_is_displayed()`

*   テストメソッドは、`test_`で始まるか、`@test`アノテーションを付けます。
*   メソッド名は、テストの内容を説明するものにします。

---

#### `$this->get('/tasks')`

*   `/tasks`にGETリクエストを送信します。
*   `$response`には、レスポンスが格納されます。

---

#### `$response->assertStatus(200)`

*   レスポンスのステータスコードが200（OK）であることを確認します。

---

### 🔍 テストの実行

テストを実行するには、以下のコマンドを使います。

```bash
php artisan test
```

---

#### 実行結果

```
   PASS  Tests\Feature\TaskTest
  ✓ task index page is displayed

  Tests:  1 passed
  Time:   0.12s
```

---

### 🔍 認証が必要なページのテスト

タスク一覧ページは、認証が必要です。

認証なしでアクセスすると、ログインページにリダイレクトされます。

---

#### テストの実装

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Tests\TestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;

class TaskTest extends TestCase
{
    use RefreshDatabase;

    /**
     * 未認証ユーザーはタスク一覧ページにアクセスできない
     */
    public function test_unauthenticated_user_cannot_access_task_index()
    {
        $response = $this->get('/tasks');

        $response->assertRedirect('/login');
    }

    /**
     * 認証済みユーザーはタスク一覧ページにアクセスできる
     */
    public function test_authenticated_user_can_access_task_index()
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->get('/tasks');

        $response->assertStatus(200);
    }
}
```

---

### 🔍 コードリーディング

#### `User::factory()->create()`

*   ユーザーファクトリーを使って、テスト用のユーザーを作成します。
*   ファクトリーについては、次のセクションで詳しく学びます。

---

#### `$this->actingAs($user)`

*   指定したユーザーでログインした状態でリクエストを送信します。

---

#### `$response->assertRedirect('/login')`

*   レスポンスが`/login`にリダイレクトされることを確認します。

---

### 🔍 タスク作成のテスト

タスクを作成する機能のテストを実装します。

```php
/**
 * タスクを作成できる
 */
public function test_user_can_create_task()
{
    $user = User::factory()->create();

    $response = $this->actingAs($user)->post('/tasks', [
        'title' => 'テストタスク',
        'description' => 'これはテストです',
        'due_date' => '2024-12-31',
    ]);

    $response->assertRedirect('/tasks');
    $response->assertSessionHas('success', 'タスクを作成しました。');

    $this->assertDatabaseHas('tasks', [
        'title' => 'テストタスク',
        'description' => 'これはテストです',
        'user_id' => $user->id,
    ]);
}
```

---

### 🔍 コードリーディング

#### `$this->actingAs($user)->post('/tasks', [...])`

*   ログインした状態で、`/tasks`にPOSTリクエストを送信します。
*   第2引数には、送信するデータを配列で指定します。

---

#### `$response->assertSessionHas('success', 'タスクを作成しました。')`

*   セッションに`success`キーが存在し、値が`'タスクを作成しました。'`であることを確認します。

---

#### `$this->assertDatabaseHas('tasks', [...])`

*   データベースの`tasks`テーブルに、指定した条件のレコードが存在することを確認します。

---

### 🔍 バリデーションのテスト

バリデーションが正しく動作するかをテストします。

```php
/**
 * タイトルが必須であることを確認する
 */
public function test_task_title_is_required()
{
    $user = User::factory()->create();

    $response = $this->actingAs($user)->post('/tasks', [
        'title' => '',
        'description' => 'これはテストです',
    ]);

    $response->assertSessionHasErrors('title');
}

/**
 * タイトルが255文字以内であることを確認する
 */
public function test_task_title_must_not_exceed_255_characters()
{
    $user = User::factory()->create();

    $response = $this->actingAs($user)->post('/tasks', [
        'title' => str_repeat('あ', 256),
        'description' => 'これはテストです',
    ]);

    $response->assertSessionHasErrors('title');
}
```

---

### 🔍 コードリーディング

#### `$response->assertSessionHasErrors('title')`

*   セッションに`title`フィールドのバリデーションエラーが存在することを確認します。

---

#### `str_repeat('あ', 256)`

*   `'あ'`を256回繰り返した文字列を生成します。

---

### 🔍 タスク更新のテスト

タスクを更新する機能のテストを実装します。

```php
/**
 * タスクを更新できる
 */
public function test_user_can_update_task()
{
    $user = User::factory()->create();
    $task = Task::factory()->create(['user_id' => $user->id]);

    $response = $this->actingAs($user)->put("/tasks/{$task->id}", [
        'title' => '更新されたタスク',
        'description' => '更新されました',
        'status' => 'completed',
        'due_date' => '2024-12-31',
    ]);

    $response->assertRedirect('/tasks');
    $response->assertSessionHas('success', 'タスクを更新しました。');

    $this->assertDatabaseHas('tasks', [
        'id' => $task->id,
        'title' => '更新されたタスク',
        'description' => '更新されました',
        'status' => 'completed',
    ]);
}
```

---

### 🔍 タスク削除のテスト

タスクを削除する機能のテストを実装します。

```php
/**
 * タスクを削除できる
 */
public function test_user_can_delete_task()
{
    $user = User::factory()->create();
    $task = Task::factory()->create(['user_id' => $user->id]);

    $response = $this->actingAs($user)->delete("/tasks/{$task->id}");

    $response->assertRedirect('/tasks');
    $response->assertSessionHas('success', 'タスクを削除しました。');

    $this->assertDatabaseMissing('tasks', [
        'id' => $task->id,
    ]);
}
```

---

### 🔍 コードリーディング

#### `$this->assertDatabaseMissing('tasks', [...])`

*   データベースの`tasks`テーブルに、指定した条件のレコードが存在しないことを確認します。

---

### 🔍 他のユーザーのタスクにアクセスできないことを確認する

```php
/**
 * 他のユーザーのタスクを更新できない
 */
public function test_user_cannot_update_other_users_task()
{
    $user1 = User::factory()->create();
    $user2 = User::factory()->create();
    $task = Task::factory()->create(['user_id' => $user1->id]);

    $response = $this->actingAs($user2)->put("/tasks/{$task->id}", [
        'title' => '更新されたタスク',
        'description' => '更新されました',
        'status' => 'completed',
        'due_date' => '2024-12-31',
    ]);

    $response->assertStatus(403); // Forbidden
}
```

---

### 💡 TIP: テストの命名規則

テストメソッドの命名は、以下のような形式が推奨されます。

```
test_{誰が}_{何を}_{どうする}
```

**例**:

*   `test_user_can_create_task`
*   `test_unauthenticated_user_cannot_access_task_index`
*   `test_task_title_is_required`

---

### 🚨 よくある間違い

#### 間違い1: `RefreshDatabase`を忘れる

**対処法**: `use RefreshDatabase;`を追加します。

---

#### 間違い2: テストが他のテストに依存する

**対処法**: 各テストは独立して実行できるようにします。

---

#### 間違い3: テストが多すぎる

**対処法**: 重要な機能に絞ってテストを書きます。

---

## ✨ まとめ

このセクションでは、機能テストの実装について学びました。

*   機能テストは、アプリケーション全体の動作を確認するテストである。
*   `RefreshDatabase`トレイトを使うことで、テスト実行後にデータベースがリセットされる。
*   `actingAs()`を使うことで、ログインした状態でリクエストを送信できる。
*   `assertDatabaseHas()`を使うことで、データベースの状態を確認できる。

次のセクションでは、ファクトリーとシーダーについて学びます。

---

## 📝 学習のポイント

- [ ] 機能テスト（Feature Test）の概念と重要性を理解した。
- [ ] Laravelの機能テストの書き方を学んだ。
- [ ] タスク管理システムの機能テストを実装した。
