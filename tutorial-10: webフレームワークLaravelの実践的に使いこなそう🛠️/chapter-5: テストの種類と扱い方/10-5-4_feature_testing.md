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

**単体テストと機能テストの違い**

| 項目 | 単体テスト | 機能テスト |
|:---|:---|:---|
| テスト対象 | 1つの関数やメソッド | アプリケーション全体の動作 |
| HTTPリクエスト | 使わない | 使う |
| データベース | 使わない | 使う |
| 実行速度 | 高速 | 比較的遅い |
| 目的 | ロジックの検証 | ユーザー操作の検証 |

このセクションでは、機能テストの基礎を学びます。

---

## 詳細解説

### 🔍 機能テストの基本的な使い方

機能テストでは、以下の流れでテストを行います。

1. **準備**: テストに必要なデータ（ユーザー、投稿など）を作成する
2. **リクエスト送信**: `get()`、`post()`などでHTTPリクエストを送信する
3. **レスポンス検証**: ステータスコード、ビュー、データベースの状態を検証する

---

### 🔧 ステップ1: テストファイルを作成

```bash
sail artisan make:test PostTest
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `sail artisan make:test` | テストファイルを生成するArtisanコマンドです |
| `PostTest` | 作成するテストクラスの名前です |
| （`--unit`なし） | `--unit`オプションを付けないと、`tests/Feature/`ディレクトリに作成されます（機能テスト用） |

**生成されるファイル: `tests/Feature/PostTest.php`**

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `namespace Tests\Feature;` | このクラスが`Tests\Feature`名前空間に属することを宣言します |
| `use Tests\TestCase;` | Laravelの機能テスト用基底クラスをインポートします |
| `class PostTest extends TestCase` | `TestCase`を継承することで、HTTPリクエストメソッドが使えるようになります |
| `$this->get('/posts')` | `/posts`にGETリクエストを送信します |
| `$response->assertStatus(200)` | レスポンスのステータスコードが200であることを検証します |

**構文解説: HTTPリクエストメソッド**

```php
$response = $this->get('/パス');      // GETリクエスト
$response = $this->post('/パス', $データ);  // POSTリクエスト
$response = $this->put('/パス', $データ);   // PUTリクエスト
$response = $this->delete('/パス');   // DELETEリクエスト
```

*   **第1引数**: リクエスト先のURL（パス）
*   **第2引数**: 送信するデータ（POST、PUTの場合）
*   **戻り値**: レスポンスオブジェクト（アサーションメソッドを呼び出せる）

---

### 🔧 ステップ2: テストを実行

```bash
sail artisan test
```

**実行結果の例**

```
PASS  Tests\Feature\PostTest
✓ can get posts

Tests:  1 passed
Time:   0.50s
```

**テスト実行コマンドのオプション**

| コマンド | 説明 |
|:---|:---|
| `sail artisan test` | 全てのテストを実行 |
| `sail artisan test --filter=PostTest` | 特定のテストクラスのみ実行 |
| `sail artisan test --testsuite=Feature` | 機能テストのみ実行 |

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
| `$response->assertViewIs('posts.index');` | 返されたビューが`posts.index`（`resources/views/posts/index.blade.php`）であることを検証します |
| `$response->assertViewHas('posts');` | ビューに`posts`変数が渡されていることを検証します |

**構文解説: assertViewIs()**

```php
$response->assertViewIs('ビュー名');
```

*   ビュー名はドット記法で指定します（`posts.index` = `resources/views/posts/index.blade.php`）
*   返されたビューが期待通りかを検証します

**構文解説: assertViewHas()**

```php
$response->assertViewHas('変数名');
$response->assertViewHas('変数名', $期待値);
```

*   ビューに特定の変数が渡されているかを検証します
*   第2引数を指定すると、変数の値も検証できます

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
        // 1. 準備：テスト用ユーザーを作成
        $user = User::factory()->create();

        // 2. 送信するデータを用意
        $data = [
            'title' => 'Test Post',
            'content' => 'Test Content',
        ];

        // 3. 認証済みユーザーとしてPOSTリクエストを送信
        $response = $this->actingAs($user)
            ->post('/posts', $data);

        // 4. レスポンスとデータベースを検証
        $response->assertRedirect();
        $this->assertDatabaseHas('posts', ['title' => 'Test Post']);
    }
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `use RefreshDatabase;` | テストごとにデータベースをリセットするトレイトです。クラス内で`use`します |
| `$user = User::factory()->create();` | ファクトリを使ってテスト用ユーザーを作成し、データベースに保存します |
| `$this->actingAs($user)` | 指定したユーザーとして認証状態を設定します。以降のリクエストはこのユーザーとして送信されます |
| `->post('/posts', $data);` | `/posts`にPOSTリクエストを送信します。`$data`がリクエストボディとして送信されます |
| `$response->assertRedirect();` | レスポンスがリダイレクト（302など）であることを検証します |
| `$this->assertDatabaseHas('posts', ['title' => 'Test Post']);` | `posts`テーブルに`title`が`Test Post`のレコードが存在することを検証します |

**構文解説: actingAs()**

```php
$this->actingAs($user)->post('/posts', $data);
```

*   `actingAs()`は認証済みユーザーとしてリクエストを送信するためのメソッドです
*   メソッドチェーンで`get()`、`post()`などと組み合わせて使います
*   認証が必要なルートをテストする際に必須です

**構文解説: assertDatabaseHas()**

```php
$this->assertDatabaseHas('テーブル名', ['カラム名' => '値']);
```

*   **第1引数**: テーブル名
*   **第2引数**: 検索条件（連想配列）
*   指定した条件に一致するレコードがデータベースに存在することを検証します

---

### 🚀 実践例3: PUTリクエスト

投稿を更新するPUTリクエストを送信し、データベースが更新されることを検証する例です。

```php
use App\Models\Post;
use App\Models\User;

public function test_can_update_post()
{
    // 1. 準備：ユーザーと投稿を作成
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    // 2. 更新するデータを用意
    $data = [
        'title' => 'Updated Title',
        'content' => 'Updated Content',
    ];

    // 3. PUTリクエストを送信
    $response = $this->actingAs($user)
        ->put("/posts/{$post->id}", $data);

    // 4. レスポンスとデータベースを検証
    $response->assertRedirect();
    $this->assertDatabaseHas('posts', ['title' => 'Updated Title']);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$post = Post::factory()->create(['user_id' => $user->id]);` | ファクトリを使ってテスト用投稿を作成します。`user_id`を指定して所有者を設定します |
| `"/posts/{$post->id}"` | 変数展開を使って、投稿のIDをURLに埋め込みます |
| `->put("/posts/{$post->id}", $data);` | 指定したIDの投稿にPUTリクエストを送信します |
| `$this->assertDatabaseHas('posts', ['title' => 'Updated Title']);` | データベースの投稿が更新されていることを検証します |

**構文解説: 変数展開（ダブルクォート内）**

```php
"/posts/{$post->id}"  // 結果: "/posts/1" など
```

*   ダブルクォート内では、`{$変数}`の形式で変数を展開できます
*   オブジェクトのプロパティにアクセスする場合は`{}`で囲みます

---

### 🚀 実践例4: DELETEリクエスト

投稿を削除するDELETEリクエストを送信し、データベースから削除されることを検証する例です。

```php
use App\Models\Post;
use App\Models\User;

public function test_can_delete_post()
{
    // 1. 準備：ユーザーと投稿を作成
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    // 2. DELETEリクエストを送信
    $response = $this->actingAs($user)
        ->delete("/posts/{$post->id}");

    // 3. レスポンスとデータベースを検証
    $response->assertRedirect();
    $this->assertDatabaseMissing('posts', ['id' => $post->id]);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `->delete("/posts/{$post->id}");` | 指定したIDの投稿にDELETEリクエストを送信します |
| `$this->assertDatabaseMissing('posts', ['id' => $post->id]);` | `posts`テーブルに指定したIDのレコードが存在しないことを検証します |

**構文解説: assertDatabaseMissing()**

```php
$this->assertDatabaseMissing('テーブル名', ['カラム名' => '値']);
```

*   `assertDatabaseHas()`の逆で、レコードが存在しないことを検証します
*   削除処理のテストで使用します

---

### 🚀 実践例5: バリデーションエラー

必須フィールドが不足している場合のバリデーションエラーを検証する例です。

```php
public function test_create_post_requires_title()
{
    $user = User::factory()->create();

    // titleを意図的に省略
    $data = [
        'content' => 'Test Content',
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

**構文解説: assertSessionHasErrors()**

```php
$response->assertSessionHasErrors(['フィールド名']);
$response->assertSessionHasErrors(['フィールド名' => 'エラーメッセージ']);
```

*   セッションにバリデーションエラーが含まれていることを検証します
*   配列で複数のフィールドを指定できます
*   エラーメッセージも検証する場合は、連想配列で指定します

---

### 💡 TIP: よく使うアサーションメソッド

**レスポンス検証**

| メソッド | 説明 | 使用例 |
|:---|:---|:---|
| `assertStatus($status)` | ステータスコードを検証 | `$response->assertStatus(200)` |
| `assertOk()` | ステータスコードが200であることを検証 | `$response->assertOk()` |
| `assertRedirect($uri)` | リダイレクト先を検証 | `$response->assertRedirect('/posts')` |
| `assertViewIs($view)` | 返されたビュー名を検証 | `$response->assertViewIs('posts.index')` |
| `assertViewHas($key)` | ビューに変数が渡されていることを検証 | `$response->assertViewHas('posts')` |
| `assertSessionHasErrors($keys)` | セッションにバリデーションエラーがあることを検証 | `$response->assertSessionHasErrors(['title'])` |

**データベース検証**

| メソッド | 説明 | 使用例 |
|:---|:---|:---|
| `assertDatabaseHas($table, $data)` | データが存在することを検証 | `$this->assertDatabaseHas('posts', ['title' => 'Test'])` |
| `assertDatabaseMissing($table, $data)` | データが存在しないことを検証 | `$this->assertDatabaseMissing('posts', ['id' => 1])` |
| `assertDatabaseCount($table, $count)` | レコード数を検証 | `$this->assertDatabaseCount('posts', 5)` |

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `use Illuminate\Foundation\Testing\RefreshDatabase;` | トレイトをインポートします |
| `use RefreshDatabase;` | クラス内でトレイトを使用します。これにより、各テストの前にデータベースがリセットされます |

**RefreshDatabaseの動作**

1. テスト開始前にマイグレーションを実行
2. 各テストをトランザクション内で実行
3. テスト終了後にロールバック（データが元に戻る）

---

### 🚨 よくある間違い

**間違い1: データベースがリセットされない**

```php
// NG: RefreshDatabaseを使っていない
class PostTest extends TestCase
{
    public function test_can_create_post()
    {
        // 前のテストのデータが残っている可能性がある
    }
}

// OK: RefreshDatabaseを使う
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

**対処法**: データベースを使うテストでは、必ず`RefreshDatabase`トレイトを使います。

---

**間違い2: 認証を忘れる**

```php
// NG: 認証が必要なのに、ログインしていない
$response = $this->post('/posts', $data);

// OK: actingAs()で認証済みユーザーとしてリクエスト
$user = User::factory()->create();
$response = $this->actingAs($user)
    ->post('/posts', $data);
```

**対処法**: 認証が必要なルートをテストする場合は、`actingAs()`を使います。

---

**間違い3: ファクトリでデータを作成していない**

```php
// NG: ファクトリを使わずに直接インスタンスを作成
$user = new User();
$response = $this->actingAs($user)->get('/posts');

// OK: ファクトリでデータベースに保存
$user = User::factory()->create();
$response = $this->actingAs($user)->get('/posts');
```

**対処法**: 機能テストでは、`factory()->create()`でデータベースにデータを保存します。

---

## ✨ まとめ

このセクションでは、機能テストの基礎を学びました。

*   機能テストは、HTTPリクエストとレスポンスを検証する。
*   `get()`、`post()`、`put()`、`delete()`メソッドを使って、リクエストを送信できる。
*   `assertStatus()`、`assertRedirect()`などのメソッドを使って、レスポンスを検証できる。
*   `actingAs()`を使って、認証済みユーザーとしてリクエストを送信できる。
*   `RefreshDatabase`トレイトを使って、テストごとにデータベースをリセットできる。

次のセクションでは、データベーステストについて学びます。

---
