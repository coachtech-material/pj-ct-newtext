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

投稿一覧ページにGETリクエストを送信し、レスポンスを検証する例です。

```php
public function test_can_get_posts()
{
    $response = $this->get('/posts');

    $response->assertStatus(200);
    $response->assertViewIs('posts.index');
    $response->assertViewHas('posts');
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$response = $this->get('/posts');` | `/posts`にGETリクエストを送信し、レスポンスを取得します |
| `$response->assertStatus(200);` | HTTPステータスコードが200（成功）であることを検証します |
| `$response->assertViewIs('posts.index');` | 返されたビューが`posts.index`であることを検証します |
| `$response->assertViewHas('posts');` | ビューに`posts`変数が渡されていることを検証します |

---

### 🚀 実践例2: POSTリクエスト

投稿を作成するPOSTリクエストを送信し、データベースに保存されることを検証する例です。

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `use RefreshDatabase;` | テストごとにデータベースをリセットするトレイトです |
| `$user = User::factory()->create();` | ファクトリを使ってテスト用ユーザーを作成します |
| `$this->actingAs($user)` | 指定したユーザーとして認証状態を設定します |
| `->post('/posts', $data);` | `/posts`にPOSTリクエストを送信します |
| `$response->assertRedirect();` | レスポンスがリダイレクトであることを検証します |
| `$this->assertDatabaseHas('posts', ['title' => 'Test Post']);` | データベースに指定したデータが存在することを検証します |

---

### 🚀 実践例3: PUTリクエスト

投稿を更新するPUTリクエストを送信し、データベースが更新されることを検証する例です。

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$post = Post::factory()->create(['user_id' => $user->id]);` | ファクトリを使ってテスト用投稿を作成します。`user_id`を指定して所有者を設定します |
| `->put("/posts/{$post->id}", $data);` | 指定したIDの投稿にPUTリクエストを送信します |
| `$this->assertDatabaseHas('posts', ['title' => 'Updated Title']);` | データベースの投稿が更新されていることを検証します |

---

### 🚀 実践例4: DELETEリクエスト

投稿を削除するDELETEリクエストを送信し、データベースから削除されることを検証する例です。

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `->delete("/posts/{$post->id}");` | 指定したIDの投稿にDELETEリクエストを送信します |
| `$this->assertDatabaseMissing('posts', ['id' => $post->id]);` | データベースに指定したデータが存在しないことを検証します |

---

### 🚀 実践例5: バリデーションエラー

必須フィールドが不足している場合のバリデーションエラーを検証する例です。

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$data = ['content' => 'Test Content'];` | `title`フィールドを意図的に省略したデータを作成します |
| `$response->assertSessionHasErrors(['title']);` | セッションに`title`フィールドのバリデーションエラーが含まれていることを検証します |

---

### 💡 TIP: よく使うアサーションメソッド

| メソッド | 説明 |
|----------|------|
| `assertStatus($status)` | ステータスコードを検証 |
| `assertRedirect()` | リダイレクトレスポンスであることを検証 |
| `assertViewIs($view)` | 返されたビュー名を検証 |
| `assertViewHas($key)` | ビューに変数が渡されていることを検証 |
| `assertSessionHasErrors($keys)` | セッションにバリデーションエラーがあることを検証 |
| `assertDatabaseHas($table, $data)` | データベースにデータが存在することを検証 |
| `assertDatabaseMissing($table, $data)` | データベースにデータが存在しないことを検証 |

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

### 🚨 よくある間違い

**間違い1: データベースがリセットされない**

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

**間違い2: 認証を忘れる**

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
*   `assertStatus()`、`assertRedirect()`などのメソッドを使って、レスポンスを検証できる。
*   `actingAs()`を使って、認証済みユーザーとしてリクエストを送信できる。

次のセクションでは、データベーステストについて学びます。

---
