# Tutorial 10-5-5: データベーステスト

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

**`assertDatabaseHas()`**

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

        $response = $this->actingAs($user)
            ->post('/posts', $data);

        $response->assertRedirect();

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

**`assertDatabaseMissing()`**

```php
public function test_can_delete_post()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $response = $this->actingAs($user)
        ->delete("/posts/{$post->id}");

    $response->assertRedirect();

    // データベースから投稿が削除されていることを検証
    $this->assertDatabaseMissing('posts', [
        'id' => $post->id,
    ]);
}
```

---

### 🚀 実践例1: 投稿の作成

投稿を作成し、データベースに保存されていることを検証する例です。

```php
public function test_create_post_saves_to_database()
{
    $user = User::factory()->create();

    $data = [
        'title' => 'New Post',
        'content' => 'Post Content',
    ];

    $this->actingAs($user)
        ->post('/posts', $data);

    $this->assertDatabaseHas('posts', [
        'title' => 'New Post',
        'content' => 'Post Content',
        'user_id' => $user->id,
    ]);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$user = User::factory()->create();` | ファクトリを使ってテスト用ユーザーを作成します |
| `$this->actingAs($user)` | 指定したユーザーとして認証状態を設定します |
| `->post('/posts', $data);` | `/posts`にPOSTリクエストを送信します |
| `$this->assertDatabaseHas('posts', [...])` | `posts`テーブルに指定したデータが存在することを検証します |
| `'user_id' => $user->id` | 作成した投稿が正しいユーザーに紐づいていることを検証します |

---

### 🚀 実践例2: 投稿の更新

投稿を更新し、データベースが更新されていることを検証する例です。

```php
public function test_update_post_updates_database()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $data = [
        'title' => 'Updated Title',
        'content' => 'Updated Content',
    ];

    $this->actingAs($user)
        ->put("/posts/{$post->id}", $data);

    $this->assertDatabaseHas('posts', [
        'id' => $post->id,
        'title' => 'Updated Title',
        'content' => 'Updated Content',
    ]);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$post = Post::factory()->create(['user_id' => $user->id]);` | ファクトリを使ってテスト用投稿を作成します。`user_id`を指定して所有者を設定します |
| `->put("/posts/{$post->id}", $data);` | 指定したIDの投稿にPUTリクエストを送信します |
| `'id' => $post->id` | 更新対象の投稿を特定するためにIDを指定します |

---

### 🚀 実践例3: 投稿の削除

投稿を削除し、データベースから削除されていることを検証する例です。

```php
public function test_delete_post_removes_from_database()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $this->actingAs($user)
        ->delete("/posts/{$post->id}");

    $this->assertDatabaseMissing('posts', [
        'id' => $post->id,
    ]);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `->delete("/posts/{$post->id}");` | 指定したIDの投稿にDELETEリクエストを送信します |
| `$this->assertDatabaseMissing('posts', [...])` | `posts`テーブルに指定したデータが存在しないことを検証します |

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

投稿がユーザーに正しく紐づいていることを検証する例です。

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$this->assertDatabaseHas('posts', [...])` | データベースレベルでリレーションシップを検証します |
| `$this->assertEquals($user->id, $post->user_id);` | モデルレベルでリレーションシップを検証します |

---

### 🚀 実践例5: 外部キー制約のテスト

存在しないユーザーIDで投稿を作成しようとした場合に例外が発生することを検証する例です。

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$this->expectException(\Illuminate\Database\QueryException::class);` | 次の処理で`QueryException`がスローされることを期待します |
| `'user_id' => 999` | 存在しないユーザーIDを指定して外部キー制約違反を発生させます |

---

### 🚀 実践例6: ソフトデリートのテスト

ソフトデリートを使用している場合のテスト例です。

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

    $this->actingAs($user)
        ->delete("/posts/{$post->id}");

    // データベースに投稿が残っているが、deleted_atが設定されている
    $this->assertDatabaseHas('posts', [
        'id' => $post->id,
    ]);

    $this->assertNotNull($post->fresh()->deleted_at);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `use SoftDeletes;` | ソフトデリート機能を有効にするトレイトです |
| `$this->assertDatabaseHas('posts', ['id' => $post->id]);` | ソフトデリート後もレコードはデータベースに残っていることを検証します |
| `$post->fresh()` | データベースから最新のモデルを取得します |
| `$this->assertNotNull($post->fresh()->deleted_at);` | `deleted_at`カラムに値が設定されていることを検証します |

---

### 💡 TIP: `assertSoftDeleted()`

```php
public function test_soft_delete_post()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $this->actingAs($user)
        ->delete("/posts/{$post->id}");

    $this->assertSoftDeleted('posts', [
        'id' => $post->id,
    ]);
}
```

---

### 🚨 よくある間違い

**間違い1: `RefreshDatabase`を使っていない**

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

**間違い2: テストデータを手動で作成**

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
