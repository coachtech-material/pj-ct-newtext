# Tutorial 9-11-5: データベーステスト

## 🎯 このセクションで学ぶこと

*   データベースのテストを書き、データの整合性を検証できるようになる。
*   `assertDatabaseHas()`、`assertDatabaseMissing()`を使えるようになる。
*   ファクトリーとシーダーを使って、テストデータを準備できるようになる。

---

## 導入：「データベーステスト」とは何か？

**データベーステスト**とは、**データベースに正しくデータが保存されているかを検証するテスト**です。

例えば、以下のようなテストを書きます。

*   投稿を作成した後、データベースに投稿が保存されているか
*   投稿を削除した後、データベースから投稿が削除されているか
*   投稿を更新した後、データベースの投稿が更新されているか

このセクションでは、データベーステストの基礎を学びます。

---

## 詳細解説

### 🔧 基本的なデータベースアサーション

#### `assertDatabaseHas()`

```php
use Illuminate\Foundation\Testing\RefreshDatabase;

class PostTest extends TestCase
{
    use RefreshDatabase;

    public function test_can_create_post()
    {
        $user = User::factory()->create();

        $data = [
            'title' => 'Test Post',
            'content' => 'Test Content',
        ];

        $response = $this->actingAs($user, 'sanctum')
            ->post('/api/posts', $data);

        $response->assertStatus(201);

        // データベースに投稿が保存されていることを検証
        $this->assertDatabaseHas('posts', [
            'title' => 'Test Post',
            'content' => 'Test Content',
            'user_id' => $user->id,
        ]);
    }
}
```

---

#### `assertDatabaseMissing()`

```php
public function test_can_delete_post()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $response = $this->actingAs($user, 'sanctum')
        ->delete("/api/posts/{$post->id}");

    $response->assertStatus(200);

    // データベースから投稿が削除されていることを検証
    $this->assertDatabaseMissing('posts', [
        'id' => $post->id,
    ]);
}
```

---

### 🚀 実践例1: 投稿の作成

```php
public function test_create_post_saves_to_database()
{
    $user = User::factory()->create();

    $data = [
        'title' => 'New Post',
        'content' => 'Post Content',
    ];

    $this->actingAs($user, 'sanctum')
        ->post('/api/posts', $data);

    $this->assertDatabaseHas('posts', [
        'title' => 'New Post',
        'content' => 'Post Content',
        'user_id' => $user->id,
    ]);
}
```

---

### 🚀 実践例2: 投稿の更新

```php
public function test_update_post_updates_database()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $data = [
        'title' => 'Updated Title',
        'content' => 'Updated Content',
    ];

    $this->actingAs($user, 'sanctum')
        ->put("/api/posts/{$post->id}", $data);

    $this->assertDatabaseHas('posts', [
        'id' => $post->id,
        'title' => 'Updated Title',
        'content' => 'Updated Content',
    ]);
}
```

---

### 🚀 実践例3: 投稿の削除

```php
public function test_delete_post_removes_from_database()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $this->actingAs($user, 'sanctum')
        ->delete("/api/posts/{$post->id}");

    $this->assertDatabaseMissing('posts', [
        'id' => $post->id,
    ]);
}
```

---

### 💡 TIP: `assertDatabaseCount()`

```php
public function test_posts_count()
{
    Post::factory()->count(5)->create();

    $this->assertDatabaseCount('posts', 5);
}
```

---

### 🚀 実践例4: リレーションシップのテスト

```php
public function test_post_belongs_to_user()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $this->assertDatabaseHas('posts', [
        'id' => $post->id,
        'user_id' => $user->id,
    ]);

    $this->assertEquals($user->id, $post->user_id);
}
```

---

### 🚀 実践例5: 外部キー制約のテスト

```php
public function test_cannot_create_post_with_invalid_user_id()
{
    $this->expectException(\Illuminate\Database\QueryException::class);

    Post::create([
        'title' => 'Test Post',
        'content' => 'Test Content',
        'user_id' => 999, // 存在しないユーザーID
    ]);
}
```

---

### 🚀 実践例6: ソフトデリートのテスト

**`app/Models/Post.php`**

```php
use Illuminate\Database\Eloquent\SoftDeletes;

class Post extends Model
{
    use SoftDeletes;
}
```

**テスト**

```php
public function test_soft_delete_post()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $this->actingAs($user, 'sanctum')
        ->delete("/api/posts/{$post->id}");

    // データベースに投稿が残っているが、deleted_atが設定されている
    $this->assertDatabaseHas('posts', [
        'id' => $post->id,
    ]);

    $this->assertNotNull($post->fresh()->deleted_at);
}
```

---

### 💡 TIP: `assertSoftDeleted()`

```php
public function test_soft_delete_post()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $this->actingAs($user, 'sanctum')
        ->delete("/api/posts/{$post->id}");

    $this->assertSoftDeleted('posts', [
        'id' => $post->id,
    ]);
}
```

---

### 🚀 実践例7: トランザクションのテスト

```php
public function test_transaction_rollback_on_error()
{
    $user = User::factory()->create();

    try {
        \DB::transaction(function () use ($user) {
            Post::create([
                'title' => 'Test Post',
                'content' => 'Test Content',
                'user_id' => $user->id,
            ]);

            // エラーを発生させる
            throw new \Exception('Test error');
        });
    } catch (\Exception $e) {
        // エラーが発生したので、ロールバックされる
    }

    // データベースに投稿が保存されていないことを検証
    $this->assertDatabaseMissing('posts', [
        'title' => 'Test Post',
    ]);
}
```

---

### 🚀 実践例8: ファクトリーを使ったテストデータの準備

```php
public function test_user_has_many_posts()
{
    $user = User::factory()
        ->has(Post::factory()->count(3))
        ->create();

    $this->assertDatabaseCount('posts', 3);
    $this->assertEquals(3, $user->posts->count());
}
```

---

### 🚨 よくある間違い

#### 間違い1: `RefreshDatabase`を使っていない

```php
// NG
class PostTest extends TestCase
{
    public function test_can_create_post()
    {
        // 前のテストのデータが残っている
    }
}

// OK
use Illuminate\Foundation\Testing\RefreshDatabase;

class PostTest extends TestCase
{
    use RefreshDatabase;
}
```

---

#### 間違い2: テストデータを手動で作成

```php
// NG
$user = User::create([
    'name' => 'Test User',
    'email' => 'test@example.com',
    'password' => bcrypt('password'),
]);

// OK
$user = User::factory()->create();
```

---

## ✨ まとめ

このセクションでは、データベーステストの基礎を学びました。

*   `assertDatabaseHas()`を使って、データベースにデータが保存されていることを検証できる。
*   `assertDatabaseMissing()`を使って、データベースからデータが削除されていることを検証できる。
*   `RefreshDatabase`トレイトを使って、テストごとにデータベースをリセットできる。
*   ファクトリーを使って、テストデータを簡単に準備できる。

次のセクションでは、認証機能のテストについて学びます。

---
