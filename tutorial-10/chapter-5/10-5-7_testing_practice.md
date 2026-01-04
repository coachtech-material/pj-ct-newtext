# Tutorial 10-5-7: 実践: CRUD+認証+DBアサートの連続演習

## 🎯 このセクションで学ぶこと

*   小さな実践演習を通じて、CRUD操作、認証、データベースアサートを連続して学ぶ。
*   実際に手を動かして、テストを体感する。
*   テスト駆動開発（TDD）の流れを理解する。

---

## 導入：「理論」から「実践」へ

これまで、単体テスト、機能テスト、データベーステスト、認証テストについて学んできました。このセクションでは、**小さな実践演習**を通じて、これらのテストを組み合わせて学びます。

---

## 実践演習: ブログ記事のCRUD+認証

### 📝 演習の目標

*   ユーザー登録、ログイン、ログアウトのテストを書く
*   投稿のCRUD操作（作成、取得、更新、削除）のテストを書く
*   データベースアサートを使って、データの整合性を検証する

---

### 🔧 ステップ1: テストファイルを作成

```bash
sail artisan make:test PostCrudTest
```

---

### 🔧 ステップ2: ユーザー登録のテスト

**`tests/Feature/PostCrudTest.php`**

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use App\Models\Post;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class PostCrudTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_register()
    {
        $data = [
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => 'password',
            'password_confirmation' => 'password',
        ];

        $response = $this->post('/register', $data);

        $response->assertRedirect('/dashboard');

        $this->assertDatabaseHas('users', [
            'name' => 'Test User',
            'email' => 'test@example.com',
        ]);

        $this->assertAuthenticated();
    }
}
```

---

### 🔧 ステップ3: ログインのテスト

```php
public function test_user_can_login()
{
    $user = User::factory()->create([
        'email' => 'test@example.com',
        'password' => bcrypt('password'),
    ]);

    $data = [
        'email' => 'test@example.com',
        'password' => 'password',
    ];

    $response = $this->post('/login', $data);

    $response->assertRedirect('/dashboard');
    $this->assertAuthenticatedAs($user);
}
```

---

### 🔧 ステップ4: 投稿の作成（CREATE）

```php
public function test_authenticated_user_can_create_post()
{
    $user = User::factory()->create();

    $data = [
        'title' => 'Test Post',
        'content' => 'Test Content',
    ];

    $response = $this->actingAs($user)
        ->post('/posts', $data);

    $response->assertRedirect();

    $this->assertDatabaseHas('posts', [
        'title' => 'Test Post',
        'content' => 'Test Content',
        'user_id' => $user->id,
    ]);
}

public function test_unauthenticated_user_cannot_create_post()
{
    $data = [
        'title' => 'Test Post',
        'content' => 'Test Content',
    ];

    $response = $this->post('/posts', $data);

    $response->assertRedirect('/login');
}
```

---

### 🔧 ステップ5: 投稿の取得（READ）

```php
public function test_can_get_posts_list()
{
    Post::factory()->count(5)->create();

    $response = $this->get('/posts');

    $response->assertStatus(200);
    $response->assertViewIs('posts.index');
    $response->assertViewHas('posts', function ($posts) {
        return $posts->count() === 5;
    });
}

public function test_can_get_single_post()
{
    $post = Post::factory()->create([
        'title' => 'Test Post',
        'content' => 'Test Content',
    ]);

    $response = $this->get("/posts/{$post->id}");

    $response->assertStatus(200);
    $response->assertViewIs('posts.show');
    $response->assertSee('Test Post');
    $response->assertSee('Test Content');
}
```

---

### 🔧 ステップ6: 投稿の更新（UPDATE）

```php
public function test_authenticated_user_can_update_own_post()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $data = [
        'title' => 'Updated Title',
        'content' => 'Updated Content',
    ];

    $response = $this->actingAs($user)
        ->put("/posts/{$post->id}", $data);

    $response->assertRedirect();

    $this->assertDatabaseHas('posts', [
        'id' => $post->id,
        'title' => 'Updated Title',
        'content' => 'Updated Content',
    ]);
}

public function test_user_cannot_update_other_users_post()
{
    $user1 = User::factory()->create();
    $user2 = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user1->id]);

    $data = [
        'title' => 'Updated Title',
        'content' => 'Updated Content',
    ];

    $response = $this->actingAs($user2)
        ->put("/posts/{$post->id}", $data);

    $response->assertStatus(403);
}
```

---

### 🔧 ステップ7: 投稿の削除（DELETE）

```php
public function test_authenticated_user_can_delete_own_post()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $response = $this->actingAs($user)
        ->delete("/posts/{$post->id}");

    $response->assertRedirect();

    $this->assertDatabaseMissing('posts', [
        'id' => $post->id,
    ]);
}

public function test_user_cannot_delete_other_users_post()
{
    $user1 = User::factory()->create();
    $user2 = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user1->id]);

    $response = $this->actingAs($user2)
        ->delete("/posts/{$post->id}");

    $response->assertStatus(403);
}
```

---

### 🔧 ステップ8: バリデーションのテスト

```php
public function test_create_post_requires_title()
{
    $user = User::factory()->create();

    $data = [
        'content' => 'Test Content',
        // titleが不足
    ];

    $response = $this->actingAs($user)
        ->post('/posts', $data);

    $response->assertSessionHasErrors(['title']);
}

public function test_create_post_requires_content()
{
    $user = User::factory()->create();

    $data = [
        'title' => 'Test Title',
        // contentが不足
    ];

    $response = $this->actingAs($user)
        ->post('/posts', $data);

    $response->assertSessionHasErrors(['content']);
}
```

---

### 🚀 ステップ9: テストを実行

```bash
sail artisan test
```

**実行結果**

```
PASS  Tests\Feature\PostCrudTest
✓ user can register
✓ user can login
✓ authenticated user can create post
✓ unauthenticated user cannot create post
✓ can get posts list
✓ can get single post
✓ authenticated user can update own post
✓ user cannot update other users post
✓ authenticated user can delete own post
✓ user cannot delete other users post
✓ create post requires title
✓ create post requires content

Tests:  12 passed
Time:   2.50s
```

---

### 💡 TIP: テスト駆動開発（TDD）

テスト駆動開発（TDD）では、以下の流れでコードを書きます。

1. **Red**: テストを書く（失敗する）
2. **Green**: テストが通るようにコードを書く
3. **Refactor**: コードをリファクタリングする

---

### 🚀 発展演習: コメント機能のテスト

#### 演習内容

*   投稿にコメントを追加できるか
*   コメントを更新できるか
*   コメントを削除できるか

#### テスト例

```php
public function test_authenticated_user_can_add_comment_to_post()
{
    $user = User::factory()->create();
    $post = Post::factory()->create();

    $data = [
        'content' => 'Test Comment',
    ];

    $response = $this->actingAs($user)
        ->post("/posts/{$post->id}/comments", $data);

    $response->assertRedirect();

    $this->assertDatabaseHas('comments', [
        'content' => 'Test Comment',
        'user_id' => $user->id,
        'post_id' => $post->id,
    ]);
}
```

---

## ✨ まとめ

このセクションでは、小さな実践演習を通じて、CRUD操作、認証、データベースアサートを連続して学びました。

*   ユーザー登録、ログイン、ログアウトのテストを書いた。
*   投稿のCRUD操作のテストを書いた。
*   データベースアサートを使って、データの整合性を検証した。
*   バリデーションのテストを書いた。

次のセクションでは、ハンズオン形式でテストを実践します。

---
