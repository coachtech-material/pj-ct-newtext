# Tutorial 9-11-4: 機能テストの基礎

## 🎯 このセクションで学ぶこと

*   機能テストを書き、HTTPリクエストとレスポンスを検証できるようになる。
*   `get()`、`post()`、`put()`、`delete()`メソッドを使えるようになる。
*   レスポンスのステータスコードやJSONを検証できるようになる。

---

## 導入：「機能テスト」とは何か？

**機能テスト（Feature Test）**とは、**アプリケーション全体の動作を検証するテスト**です。HTTPリクエストを送信し、レスポンスを検証します。

例えば、以下のようなテストを書きます。

*   投稿一覧を取得できるか
*   投稿を作成できるか
*   投稿を更新できるか
*   投稿を削除できるか

このセクションでは、機能テストの基礎を学びます。

---

## 詳細解説

### 🔧 ステップ1: テストファイルを作成

```bash
php artisan make:test PostTest
```

**`tests/Feature/PostTest.php`**

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class PostTest extends TestCase
{
    public function test_can_get_posts()
    {
        $response = $this->get('/api/posts');

        $response->assertStatus(200);
    }
}
```

---

### 🔧 ステップ2: テストを実行

```bash
php artisan test
```

---

### 🚀 実践例1: GETリクエスト

```php
public function test_can_get_posts()
{
    $response = $this->get('/api/posts');

    $response->assertStatus(200);
    $response->assertJsonStructure([
        'posts' => [
            '*' => ['id', 'title', 'content', 'created_at', 'updated_at']
        ]
    ]);
}
```

---

### 🚀 実践例2: POSTリクエスト

```php
public function test_can_create_post()
{
    $data = [
        'title' => 'Test Post',
        'content' => 'Test Content',
    ];

    $response = $this->post('/api/posts', $data);

    $response->assertStatus(201);
    $response->assertJson([
        'message' => 'Post created successfully',
    ]);
}
```

---

### 🚀 実践例3: PUTリクエスト

```php
public function test_can_update_post()
{
    $data = [
        'title' => 'Updated Title',
        'content' => 'Updated Content',
    ];

    $response = $this->put('/api/posts/1', $data);

    $response->assertStatus(200);
    $response->assertJson([
        'message' => 'Post updated successfully',
    ]);
}
```

---

### 🚀 実践例4: DELETEリクエスト

```php
public function test_can_delete_post()
{
    $response = $this->delete('/api/posts/1');

    $response->assertStatus(200);
    $response->assertJson([
        'message' => 'Post deleted successfully',
    ]);
}
```

---

### 💡 TIP: よく使うアサーションメソッド

| メソッド | 説明 |
|----------|------|
| `assertStatus($status)` | ステータスコードを検証 |
| `assertJson($data)` | JSONレスポンスを検証 |
| `assertJsonStructure($structure)` | JSON構造を検証 |
| `assertJsonCount($count, $key)` | JSON配列の要素数を検証 |
| `assertJsonFragment($fragment)` | JSON内に特定のデータが含まれることを検証 |

---

### 🚀 実践例5: 認証が必要なエンドポイント

```php
use App\Models\User;

public function test_authenticated_user_can_create_post()
{
    $user = User::factory()->create();

    $data = [
        'title' => 'Test Post',
        'content' => 'Test Content',
    ];

    $response = $this->actingAs($user, 'sanctum')
        ->post('/api/posts', $data);

    $response->assertStatus(201);
}
```

---

### 🚀 実践例6: バリデーションエラー

```php
public function test_create_post_requires_title()
{
    $user = User::factory()->create();

    $data = [
        'content' => 'Test Content',
        // titleが不足
    ];

    $response = $this->actingAs($user, 'sanctum')
        ->post('/api/posts', $data);

    $response->assertStatus(422);
    $response->assertJsonValidationErrors(['title']);
}
```

---

### 🚀 実践例7: JSONの詳細な検証

```php
public function test_can_get_post_details()
{
    $response = $this->get('/api/posts/1');

    $response->assertStatus(200);
    $response->assertJson([
        'post' => [
            'id' => 1,
            'title' => 'Test Post',
            'content' => 'Test Content',
        ]
    ]);
    $response->assertJsonFragment(['title' => 'Test Post']);
}
```

---

### 🚀 実践例8: JSON配列の要素数を検証

```php
public function test_posts_list_has_correct_count()
{
    $response = $this->get('/api/posts');

    $response->assertStatus(200);
    $response->assertJsonCount(10, 'posts'); // 10件の投稿があることを検証
}
```

---

### 💡 TIP: `RefreshDatabase`トレイト

テストごとにデータベースをリセットするには、`RefreshDatabase`トレイトを使います。

```php
use Illuminate\Foundation\Testing\RefreshDatabase;

class PostTest extends TestCase
{
    use RefreshDatabase;

    public function test_can_create_post()
    {
        // テストごとにデータベースがリセットされる
    }
}
```

---

### 🚀 実践例9: ヘッダーを含むリクエスト

```php
public function test_can_create_post_with_custom_header()
{
    $user = User::factory()->create();

    $data = [
        'title' => 'Test Post',
        'content' => 'Test Content',
    ];

    $response = $this->actingAs($user, 'sanctum')
        ->withHeaders([
            'Accept' => 'application/json',
            'X-Custom-Header' => 'value',
        ])
        ->post('/api/posts', $data);

    $response->assertStatus(201);
}
```

---

### 🚨 よくある間違い

#### 間違い1: データベースがリセットされない

```php
// NG: RefreshDatabaseを使っていない
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

    public function test_can_create_post()
    {
        // テストごとにデータベースがリセットされる
    }
}
```

---

#### 間違い2: 認証トークンを忘れる

```php
// NG
$response = $this->post('/api/posts', $data); // 認証が必要なのに、トークンがない

// OK
$user = User::factory()->create();
$response = $this->actingAs($user, 'sanctum')
    ->post('/api/posts', $data);
```

---

## ✨ まとめ

このセクションでは、機能テストの基礎を学びました。

*   機能テストは、HTTPリクエストとレスポンスを検証する。
*   `get()`、`post()`、`put()`、`delete()`メソッドを使って、リクエストを送信できる。
*   `assertStatus()`、`assertJson()`などのメソッドを使って、レスポンスを検証できる。
*   `actingAs()`を使って、認証済みユーザーとしてリクエストを送信できる。

次のセクションでは、データベーステストについて学びます。

---

## 📝 学習のポイント

- [ ] 機能テストを書き、HTTPリクエストとレスポンスを検証できる。
- [ ] `get()`、`post()`、`put()`、`delete()`メソッドを使える。
- [ ] レスポンスのステータスコードやJSONを検証できる。
- [ ] `actingAs()`を使って、認証済みユーザーとしてリクエストを送信できる。
