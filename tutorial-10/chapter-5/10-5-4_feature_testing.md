# Tutorial 10-5-4: 機能テストの基礎

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
sail artisan make:test PostTest
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
        $response = $this->get('/posts');

        $response->assertStatus(200);
    }
}
```

---

### 🔧 ステップ2: テストを実行

```bash
sail artisan test
```

---

### 🚀 実践例1: GETリクエスト

```php
public function test_can_get_posts()
{
    $response = $this->get('/posts');

    $response->assertStatus(200);
    $response->assertViewIs('posts.index');
    $response->assertViewHas('posts');
}
```

---

### 🚀 実践例2: POSTリクエスト

```php
use App\Models\User;
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
        $this->assertDatabaseHas('posts', ['title' => 'Test Post']);
    }
}
```

**コードリーディング（メソッドチェーンの分解）**

`$this->actingAs($user)->post('/posts', $data)` を分解してみましょう。

| ステップ | コード | 演算子 | 戻り値 | 意味 |
|:---:|:---|:---:|:---|:---|
| 1 | `$this->actingAs($user)` | `->` | TestCaseインスタンス | 指定ユーザーとして認証状態を設定 |
| 2 | `->post('/posts', $data)` | `->` | TestResponse | POSTリクエストを送信してレスポンスを取得 |

> **💡 Tutorial 7の復習**: `$this`は現在のテストクラスのインスタンスを指します。`actingAs()`はテストクラス自身を返すので、続けて`->post()`を呼び出せます。

---

### 🚀 実践例3: PUTリクエスト

```php
use App\Models\Post;
use App\Models\User;

public function test_can_update_post()
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
    $this->assertDatabaseHas('posts', ['title' => 'Updated Title']);
}
```

---

### 🚀 実践例4: DELETEリクエスト

```php
use App\Models\Post;
use App\Models\User;

public function test_can_delete_post()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $response = $this->actingAs($user)
        ->delete("/posts/{$post->id}");

    $response->assertRedirect();
    $this->assertDatabaseMissing('posts', ['id' => $post->id]);
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

### 🚀 実践例5: 認証が必要なページ

```php
use App\Models\User;

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
    $this->assertDatabaseHas('posts', ['title' => 'Test Post']);
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

    $response = $this->actingAs($user)
        ->post('/posts', $data);

    $response->assertSessionHasErrors(['title']);
}
```

---

### 🚀 実践例7: JSONの詳細な検証

```php
use App\Models\Post;

public function test_can_get_post_details()
{
    $post = Post::factory()->create([
        'title' => 'Test Post',
        'content' => 'Test Content',
    ]);

    $response = $this->get("/posts/{$post->id}");

    $response->assertStatus(200);
    $response->assertViewIs('posts.show');
    $response->assertViewHas('post');
    $response->assertSee('Test Post');
}
```

---

### 🚀 実践例8: JSON配列の要素数を検証

```php
use App\Models\Post;

public function test_posts_list_has_correct_count()
{
    Post::factory()->count(10)->create();

    $response = $this->get('/posts');

    $response->assertStatus(200);
    $response->assertViewHas('posts', function ($posts) {
        return $posts->count() === 10;
    });
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

    $response = $this->actingAs($user)
        ->withHeaders([
            'X-Custom-Header' => 'value',
        ])
        ->post('/posts', $data);

    $response->assertRedirect();
}
```

**コードリーディング（複数のメソッドチェーン）**

| ステップ | コード | 演算子 | 戻り値 | 意味 |
|:---:|:---|:---:|:---|:---|
| 1 | `$this->actingAs($user)` | `->` | TestCase | 認証状態を設定 |
| 2 | `->withHeaders([...])` | `->` | TestCase | カスタムヘッダーを設定 |
| 3 | `->post('/posts', $data)` | `->` | TestResponse | POSTリクエストを送信 |

> **💡 ポイント**: このように複数のメソッドをチェーンすることで、認証、ヘッダー設定、リクエスト送信を一連の流れで記述できます。

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

#### 間違い2: 認証を忘れる

```php
// NG
$response = $this->post('/posts', $data); // 認証が必要なのに、ログインしていない

// OK
$user = User::factory()->create();
$response = $this->actingAs($user)
    ->post('/posts', $data);
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
