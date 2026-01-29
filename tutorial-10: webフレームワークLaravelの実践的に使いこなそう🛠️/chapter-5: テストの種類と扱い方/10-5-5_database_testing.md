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

**データベーステストの重要性**

| 検証項目 | 説明 |
|:---|:---|
| データの保存 | フォームから送信されたデータが正しく保存されているか |
| データの更新 | 更新処理で正しいカラムが変更されているか |
| データの削除 | 削除処理でレコードが正しく削除されているか |
| リレーションシップ | 外部キーが正しく設定されているか |

このセクションでは、データベーステストの基礎を学びます。

---

## 詳細解説

### 🔍 データベーステストの基本的な使い方

データベーステストでは、以下の流れでテストを行います。

1. **準備**: テストに必要なデータをファクトリで作成する
2. **実行**: HTTPリクエストを送信する、またはモデルを直接操作する
3. **検証**: データベースの状態をアサーションメソッドで検証する

---

### 🔧 基本的なデータベースアサーション

**`assertDatabaseHas()` - データが存在することを検証**

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `use RefreshDatabase;` | テストごとにデータベースをリセットするトレイトです |
| `$user = User::factory()->create();` | ファクトリを使ってテスト用ユーザーを作成し、データベースに保存します |
| `$this->actingAs($user)` | 指定したユーザーとして認証状態を設定します |
| `->post('/posts', $data);` | `/posts`にPOSTリクエストを送信します |
| `$this->assertDatabaseHas('posts', [...])` | `posts`テーブルに指定した条件に一致するレコードが存在することを検証します |

**構文解説: assertDatabaseHas()**

```php
$this->assertDatabaseHas('テーブル名', [
    'カラム名1' => '値1',
    'カラム名2' => '値2',
]);
```

*   **第1引数**: テーブル名（文字列）
*   **第2引数**: 検索条件（連想配列）
*   指定した全ての条件に一致するレコードが1件以上存在すればテスト成功

---

**`assertDatabaseMissing()` - データが存在しないことを検証**

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$post = Post::factory()->create(['user_id' => $user->id]);` | ファクトリを使ってテスト用投稿を作成します。`user_id`を指定して所有者を設定します |
| `->delete("/posts/{$post->id}");` | 指定したIDの投稿にDELETEリクエストを送信します |
| `$this->assertDatabaseMissing('posts', [...])` | `posts`テーブルに指定した条件に一致するレコードが存在しないことを検証します |

**構文解説: assertDatabaseMissing()**

```php
$this->assertDatabaseMissing('テーブル名', [
    'カラム名' => '値',
]);
```

*   `assertDatabaseHas()`の逆で、レコードが存在しないことを検証します
*   削除処理のテストで使用します

---

### 🚀 実践例1: 投稿の作成

投稿を作成し、データベースに保存されていることを検証する例です。

```php
public function test_create_post_saves_to_database()
{
    // 1. 準備：テスト用ユーザーを作成
    $user = User::factory()->create();

    // 2. 送信するデータを用意
    $data = [
        'title' => 'New Post',
        'content' => 'Post Content',
    ];

    // 3. POSTリクエストを送信
    $this->actingAs($user)
        ->post('/posts', $data);

    // 4. データベースを検証
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

**処理の流れ**

1. ファクトリでテスト用ユーザーを作成
2. 投稿データを用意
3. 認証済みユーザーとしてPOSTリクエストを送信
4. データベースに投稿が保存されていることを検証

---

### 🚀 実践例2: 投稿の更新

投稿を更新し、データベースが更新されていることを検証する例です。

```php
public function test_update_post_updates_database()
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
    $this->actingAs($user)
        ->put("/posts/{$post->id}", $data);

    // 4. データベースを検証
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

**構文解説: ファクトリでの属性指定**

```php
Post::factory()->create(['user_id' => $user->id]);
```

*   `create()`の引数に連想配列を渡すと、ファクトリのデフォルト値を上書きできます
*   リレーションシップを設定する際に便利です

---

### 🚀 実践例3: 投稿の削除

投稿を削除し、データベースから削除されていることを検証する例です。

```php
public function test_delete_post_removes_from_database()
{
    // 1. 準備：ユーザーと投稿を作成
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    // 2. DELETEリクエストを送信
    $this->actingAs($user)
        ->delete("/posts/{$post->id}");

    // 3. データベースを検証
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

レコードの件数を検証する場合は、`assertDatabaseCount()`を使います。

```php
public function test_posts_count()
{
    // 5件の投稿を作成
    Post::factory()->count(5)->create();

    // postsテーブルに5件のレコードがあることを検証
    $this->assertDatabaseCount('posts', 5);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `Post::factory()->count(5)->create();` | ファクトリを使って5件の投稿を一度に作成します |
| `$this->assertDatabaseCount('posts', 5);` | `posts`テーブルのレコード数が5件であることを検証します |

**構文解説: assertDatabaseCount()**

```php
$this->assertDatabaseCount('テーブル名', 件数);
```

*   **第1引数**: テーブル名
*   **第2引数**: 期待するレコード件数

---

### 🚀 実践例4: リレーションシップのテスト

投稿がユーザーに正しく紐づいていることを検証する例です。

```php
public function test_post_belongs_to_user()
{
    // 1. 準備：ユーザーと投稿を作成
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    // 2. データベースレベルで検証
    $this->assertDatabaseHas('posts', [
        'id' => $post->id,
        'user_id' => $user->id,
    ]);

    // 3. モデルレベルで検証
    $this->assertEquals($user->id, $post->user_id);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$this->assertDatabaseHas('posts', [...])` | データベースレベルでリレーションシップを検証します |
| `$this->assertEquals($user->id, $post->user_id);` | モデルレベルでリレーションシップを検証します |

**2つの検証方法の違い**

| 検証方法 | 説明 | 用途 |
|:---|:---|:---|
| `assertDatabaseHas()` | データベースを直接確認 | データが正しく保存されているか |
| `assertEquals()` | モデルのプロパティを確認 | モデルの状態が正しいか |

---

### 🚀 実践例5: 外部キー制約のテスト

存在しないユーザーIDで投稿を作成しようとした場合に例外が発生することを検証する例です。

```php
public function test_cannot_create_post_with_invalid_user_id()
{
    // 例外が発生することを期待
    $this->expectException(\Illuminate\Database\QueryException::class);

    // 存在しないユーザーIDで投稿を作成
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

**構文解説: expectException()**

```php
$this->expectException(例外クラス::class);
```

*   テスト内で指定した例外がスローされることを期待します
*   例外がスローされなければテスト失敗
*   `expectException()`は例外が発生する処理の**前**に呼び出します

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

**コードリーディング（モデル）**

| コード | 説明 |
|:---|:---|
| `use SoftDeletes;` | ソフトデリート機能を有効にするトレイトです。`deleted_at`カラムを使って論理削除を行います |

**テスト**

```php
public function test_soft_delete_post()
{
    // 1. 準備：ユーザーと投稿を作成
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    // 2. DELETEリクエストを送信
    $this->actingAs($user)
        ->delete("/posts/{$post->id}");

    // 3. データベースに投稿が残っていることを検証（ソフトデリート）
    $this->assertDatabaseHas('posts', [
        'id' => $post->id,
    ]);

    // 4. deleted_atが設定されていることを検証
    $this->assertNotNull($post->fresh()->deleted_at);
}
```

**コードリーディング（テスト）**

| コード | 説明 |
|:---|:---|
| `$this->assertDatabaseHas('posts', ['id' => $post->id]);` | ソフトデリート後もレコードはデータベースに残っていることを検証します |
| `$post->fresh()` | データベースから最新のモデルを取得します。削除後の状態を確認するために使用します |
| `$this->assertNotNull($post->fresh()->deleted_at);` | `deleted_at`カラムに値が設定されていることを検証します |

**構文解説: fresh()**

```php
$model->fresh();
```

*   データベースから最新のモデルを再取得します
*   モデルの状態がデータベースと同期していない場合に使用します
*   削除や更新後に最新の状態を確認する際に便利です

---

### 💡 TIP: `assertSoftDeleted()`

ソフトデリートを検証する専用のメソッドもあります。

```php
public function test_soft_delete_post()
{
    $user = User::factory()->create();
    $post = Post::factory()->create(['user_id' => $user->id]);

    $this->actingAs($user)
        ->delete("/posts/{$post->id}");

    // ソフトデリートされていることを検証
    $this->assertSoftDeleted('posts', [
        'id' => $post->id,
    ]);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$this->assertSoftDeleted('posts', [...])` | 指定したレコードがソフトデリートされている（`deleted_at`が設定されている）ことを検証します |

---

### 💡 TIP: よく使うデータベースアサーションメソッド

| メソッド | 説明 | 使用例 |
|:---|:---|:---|
| `assertDatabaseHas($table, $data)` | データが存在することを検証 | `$this->assertDatabaseHas('posts', ['title' => 'Test'])` |
| `assertDatabaseMissing($table, $data)` | データが存在しないことを検証 | `$this->assertDatabaseMissing('posts', ['id' => 1])` |
| `assertDatabaseCount($table, $count)` | レコード数を検証 | `$this->assertDatabaseCount('posts', 5)` |
| `assertSoftDeleted($table, $data)` | ソフトデリートされていることを検証 | `$this->assertSoftDeleted('posts', ['id' => 1])` |
| `assertNotSoftDeleted($table, $data)` | ソフトデリートされていないことを検証 | `$this->assertNotSoftDeleted('posts', ['id' => 1])` |

---

### 🚨 よくある間違い

**間違い1: `RefreshDatabase`を使っていない**

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
}
```

**対処法**: データベースを使うテストでは、必ず`RefreshDatabase`トレイトを使います。

---

**間違い2: テストデータを手動で作成**

```php
// NG: 手動でデータを作成（冗長で保守性が低い）
$user = User::create([
    'name' => 'Test User',
    'email' => 'test@example.com',
    'password' => bcrypt('password'),
]);

// OK: ファクトリを使う（簡潔で保守性が高い）
$user = User::factory()->create();
```

**対処法**: テストデータはファクトリを使って作成します。

---

**間違い3: 検証条件が不十分**

```php
// NG: titleだけで検証（他の投稿と重複する可能性がある）
$this->assertDatabaseHas('posts', [
    'title' => 'Test Post',
]);

// OK: 複数の条件で検証（特定のレコードを正確に検証）
$this->assertDatabaseHas('posts', [
    'title' => 'Test Post',
    'user_id' => $user->id,
]);
```

**対処法**: 複数の条件を指定して、特定のレコードを正確に検証します。

---

## ✨ まとめ

このセクションでは、データベーステストの基礎を学びました。

*   `assertDatabaseHas()`を使って、データベースにデータが保存されていることを検証できる。
*   `assertDatabaseMissing()`を使って、データベースからデータが削除されていることを検証できる。
*   `assertDatabaseCount()`を使って、レコード数を検証できる。
*   `RefreshDatabase`トレイトを使って、テストごとにデータベースをリセットできる。
*   ファクトリーを使って、テストデータを簡単に準備できる。
*   `assertSoftDeleted()`を使って、ソフトデリートを検証できる。

次のセクションでは、認証機能のテストについて学びます。

---
