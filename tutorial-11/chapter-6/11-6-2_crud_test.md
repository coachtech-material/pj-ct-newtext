# Tutorial 11-6-2: CRUD機能のテスト

## 🎯 このセクションで学ぶこと

*   タスクのCRUD機能をテストする方法を学ぶ。
*   正常系と異常系のテストを書く方法を学ぶ。
*   HTTPテストの基本を理解する。

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ環境構築の後に『CRUDテスト』を書くのか？」

テスト環境が整ったら、次は「CRUDテスト」です。

---

### 理由1: 最も重要な機能から

CRUDは**アプリケーションの核となる機能**です。

まずはここが正しく動くことを保証します。

---

### 理由2: Featureテストで統合的に確認

CRUDテストでは、**実際にHTTPリクエストを送信**してテストします。

```php
$response = $this->post('/tasks', [
    'title' => 'テストタスク',
]);
$response->assertStatus(302);
$this->assertDatabaseHas('tasks', ['title' => 'テストタスク']);
```

---

### 理由3: データベースとの連携を確認

CRUDテストでは、**データベースに正しく保存されているか**も確認します。

`assertDatabaseHas()`を使って、期待するデータが存在することを検証します。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| 1 | 一覧表示のテスト | GETリクエストをテスト |
| 2 | 作成のテスト | POSTリクエストとデータベース確認 |
| 3 | 更新・削除のテスト | PUT/DELETEリクエストをテスト |

> 💡 **ポイント**: `RefreshDatabase`トレイトを使うと、テストごとにデータベースをリセットできます。

---

## 導入：なぜCRUD機能をテストするのか

**CRUD機能**は、アプリケーションの**基本的な機能**です。

CRUD機能をテストすることで、**アプリケーションが正しく動作することを確認**できます。

---

## 詳細解説

### 🔍 タスク作成のテスト（正常系）

タスクを作成できることをテストします。

```php
public function test_ログインしたユーザーがタスクを作成できる()
{
    // 準備
    $user = User::factory()->create();
    
    // 実行
    $response = $this->actingAs($user)->post('/tasks', [
        'title' => 'テストタスク',
        'description' => 'テスト説明',
        'status' => 'pending',
        'priority' => 3,
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertRedirect('/tasks');
    $this->assertDatabaseHas('tasks', [
        'title' => 'テストタスク',
        'description' => 'テスト説明',
        'status' => 'pending',
        'priority' => 3,
        'user_id' => $user->id,
    ]);
}
```

---

### 🔍 タスク作成のテスト（異常系）

タイトルが空の場合、エラーになることをテストします。

```php
public function test_タイトルが空の場合タスクを作成できない()
{
    // 準備
    $user = User::factory()->create();
    
    // 実行
    $response = $this->actingAs($user)->post('/tasks', [
        'title' => '',
        'description' => 'テスト説明',
        'status' => 'pending',
        'priority' => 3,
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertSessionHasErrors('title');
    $this->assertDatabaseMissing('tasks', [
        'description' => 'テスト説明',
    ]);
}
```

---

### 🔍 タスク一覧のテスト

タスク一覧が表示されることをテストします。

```php
public function test_ログインしたユーザーが自分のタスク一覧を表示できる()
{
    // 準備
    $user = User::factory()->create();
    $task1 = Task::factory()->create(['user_id' => $user->id, 'title' => 'タスク1']);
    $task2 = Task::factory()->create(['user_id' => $user->id, 'title' => 'タスク2']);
    $otherTask = Task::factory()->create(['title' => '他人のタスク']);
    
    // 実行
    $response = $this->actingAs($user)->get('/tasks');
    
    // 検証
    $response->assertStatus(200);
    $response->assertSee('タスク1');
    $response->assertSee('タスク2');
    $response->assertDontSee('他人のタスク');
}
```

---

### 🔍 タスク詳細のテスト

タスク詳細が表示されることをテストします。

```php
public function test_ログインしたユーザーが自分のタスク詳細を表示できる()
{
    // 準備
    $user = User::factory()->create();
    $task = Task::factory()->create([
        'user_id' => $user->id,
        'title' => 'テストタスク',
        'description' => 'テスト説明',
    ]);
    
    // 実行
    $response = $this->actingAs($user)->get("/tasks/{$task->id}");
    
    // 検証
    $response->assertStatus(200);
    $response->assertSee('テストタスク');
    $response->assertSee('テスト説明');
}
```

---

### 🔍 タスク更新のテスト（正常系）

タスクを更新できることをテストします。

```php
public function test_ログインしたユーザーが自分のタスクを更新できる()
{
    // 準備
    $user = User::factory()->create();
    $task = Task::factory()->create([
        'user_id' => $user->id,
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
    $response->assertStatus(302);
    $response->assertRedirect('/tasks');
    $this->assertDatabaseHas('tasks', [
        'id' => $task->id,
        'title' => '更新されたタイトル',
        'description' => '更新された説明',
        'status' => 'completed',
        'priority' => 5,
    ]);
}
```

---

### 🔍 タスク更新のテスト（異常系）

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

### 🔍 タスク削除のテスト（正常系）

タスクを削除できることをテストします。

```php
public function test_ログインしたユーザーが自分のタスクを削除できる()
{
    // 準備
    $user = User::factory()->create();
    $task = Task::factory()->create(['user_id' => $user->id]);
    
    // 実行
    $response = $this->actingAs($user)->delete("/tasks/{$task->id}");
    
    // 検証
    $response->assertStatus(302);
    $response->assertRedirect('/tasks');
    $this->assertDatabaseMissing('tasks', [
        'id' => $task->id,
    ]);
}
```

---

### 🔍 タスク削除のテスト（異常系）

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

### 🔍 未ログインユーザーのテスト

未ログインユーザーがアクセスできないことをテストします。

```php
public function test_未ログインユーザーはタスク一覧にアクセスできない()
{
    // 実行
    $response = $this->get('/tasks');
    
    // 検証
    $response->assertStatus(302);
    $response->assertRedirect('/login');
}

public function test_未ログインユーザーはタスクを作成できない()
{
    // 実行
    $response = $this->post('/tasks', [
        'title' => 'テストタスク',
        'description' => 'テスト説明',
        'status' => 'pending',
        'priority' => 3,
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertRedirect('/login');
    $this->assertDatabaseMissing('tasks', [
        'title' => 'テストタスク',
    ]);
}
```

---

### 🔍 実践演習: テストを作成してください

以下のテストを作成してください。

**テスト内容**:
*   優先度が1未満の場合、タスクを作成できないことを確認する

---

**解答例**:

```php
public function test_優先度が1未満の場合タスクを作成できない()
{
    // 準備
    $user = User::factory()->create();
    
    // 実行
    $response = $this->actingAs($user)->post('/tasks', [
        'title' => 'テストタスク',
        'description' => 'テスト説明',
        'status' => 'pending',
        'priority' => 0,
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertSessionHasErrors('priority');
    $this->assertDatabaseMissing('tasks', [
        'title' => 'テストタスク',
    ]);
}
```

---

### 🔍 テストの整理

テストが増えてきたら、`setUp()`メソッドで共通の処理をまとめます。

```php
class TaskTest extends TestCase
{
    use RefreshDatabase;
    
    private $user;
    
    protected function setUp(): void
    {
        parent::setUp();
        $this->user = User::factory()->create();
    }
    
    public function test_ログインしたユーザーがタスクを作成できる()
    {
        // $this->userを使う
        $response = $this->actingAs($this->user)->post('/tasks', [
            'title' => 'テストタスク',
            'description' => 'テスト説明',
            'status' => 'pending',
            'priority' => 3,
        ]);
        
        $response->assertStatus(302);
    }
}
```

---

### 💡 TIP: データプロバイダーを使う

複数のパターンをテストする場合は、データプロバイダーを使います。

```php
/**
 * @dataProvider invalidTitleProvider
 */
public function test_無効なタイトルの場合タスクを作成できない($title)
{
    $user = User::factory()->create();
    
    $response = $this->actingAs($user)->post('/tasks', [
        'title' => $title,
        'description' => 'テスト説明',
        'status' => 'pending',
        'priority' => 3,
    ]);
    
    $response->assertSessionHasErrors('title');
}

public function invalidTitleProvider()
{
    return [
        [''],
        [str_repeat('a', 256)],
    ];
}
```

---

### 🚨 よくある間違い

#### 間違い1: actingAs()を忘れる

`actingAs()`を忘れると、未ログイン状態でテストが実行されます。

```php
// ❌ 間違い
$response = $this->post('/tasks', [...]);

// ✅ 正しい
$response = $this->actingAs($user)->post('/tasks', [...]);
```

---

#### 間違い2: assertDatabaseHasで全てのカラムを検証しない

`assertDatabaseHas`では、必要なカラムだけを検証します。

```php
// ❌ 冗長
$this->assertDatabaseHas('tasks', [
    'id' => $task->id,
    'title' => 'テストタスク',
    'description' => 'テスト説明',
    'status' => 'pending',
    'priority' => 3,
    'user_id' => $user->id,
    'created_at' => $task->created_at,
    'updated_at' => $task->updated_at,
]);

// ✅ 良い
$this->assertDatabaseHas('tasks', [
    'title' => 'テストタスク',
    'user_id' => $user->id,
]);
```

---

#### 間違い3: 正常系のテストしか書かない

異常系のテストも書きます。

*   バリデーションエラー
*   権限エラー
*   未ログインエラー

---

## ✨ まとめ

このセクションでは、CRUD機能のテストを学びました。

*   タスクの作成、一覧、詳細、更新、削除のテストを書いた。
*   正常系と異常系のテストを書いた。
*   未ログインユーザーのテストを書いた。

次のセクションでは、認証機能のテストを書きます。

---

## 📝 学習のポイント

- [ ] タスク作成のテストを書いた。
- [ ] タスク更新のテストを書いた。
- [ ] タスク削除のテストを書いた。
- [ ] 正常系と異常系のテストを書いた。
- [ ] 未ログインユーザーのテストを書いた。
