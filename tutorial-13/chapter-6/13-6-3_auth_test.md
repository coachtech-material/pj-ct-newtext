# Tutorial 13-6-3: 認証・認可テスト

## 🎯 このセクションで学ぶこと

- 認証が必要なルートのテスト方法を学ぶ
- 認可（Policy）のテスト方法を学ぶ
- 403エラーのテスト方法を学ぶ

---

## Step 1: 認証テスト

### 1-1. 未認証ユーザーがリダイレクトされることをテスト

```php
public function test_未認証ユーザーは一覧画面にアクセスできない(): void
{
    // 実行（ログインせずにアクセス）
    $response = $this->get('/books');

    // 検証（ログイン画面にリダイレクト）
    $response->assertRedirect('/login');
}
```

### 1-2. 認証済みユーザーがアクセスできることをテスト

```php
public function test_認証済みユーザーは一覧画面にアクセスできる(): void
{
    // 準備
    $user = User::factory()->create();

    // 実行
    $response = $this->actingAs($user)->get('/books');

    // 検証
    $response->assertStatus(200);
}
```

---

## Step 2: 認可テスト（他のユーザーの書籍）

### 2-1. 他のユーザーの書籍にアクセスできないことをテスト

```php
public function test_他のユーザーの書籍詳細にアクセスできない(): void
{
    // 準備
    $user1 = User::factory()->create();
    $user2 = User::factory()->create();
    $book = Book::factory()->create(['user_id' => $user1->id]);

    // 実行（user2がuser1の書籍にアクセス）
    $response = $this->actingAs($user2)->get("/books/{$book->id}");

    // 検証（403 Forbidden）
    $response->assertStatus(403);
}
```

### 2-2. 他のユーザーの書籍を編集できないことをテスト

```php
public function test_他のユーザーの書籍を編集できない(): void
{
    // 準備
    $user1 = User::factory()->create();
    $user2 = User::factory()->create();
    $book = Book::factory()->create(['user_id' => $user1->id]);

    // 実行
    $response = $this->actingAs($user2)->put("/books/{$book->id}", [
        'title' => '不正な更新',
        'author' => 'テスト',
        'rating' => 5,
    ]);

    // 検証
    $response->assertStatus(403);
    $this->assertDatabaseMissing('books', [
        'id' => $book->id,
        'title' => '不正な更新',
    ]);
}
```

### 2-3. 他のユーザーの書籍を削除できないことをテスト

```php
public function test_他のユーザーの書籍を削除できない(): void
{
    // 準備
    $user1 = User::factory()->create();
    $user2 = User::factory()->create();
    $book = Book::factory()->create(['user_id' => $user1->id]);

    // 実行
    $response = $this->actingAs($user2)->delete("/books/{$book->id}");

    // 検証
    $response->assertStatus(403);
    $this->assertDatabaseHas('books', [
        'id' => $book->id,
    ]);
}
```

---

## Step 3: 自分の書籍へのアクセス

### 3-1. 自分の書籍にはアクセスできることをテスト

```php
public function test_自分の書籍詳細にアクセスできる(): void
{
    // 準備
    $user = User::factory()->create();
    $book = Book::factory()->create(['user_id' => $user->id]);

    // 実行
    $response = $this->actingAs($user)->get("/books/{$book->id}");

    // 検証
    $response->assertStatus(200);
    $response->assertSee($book->title);
}
```

---

## Step 4: テストの整理

### 4-1. データプロバイダを使う

同じようなテストを複数書く場合、データプロバイダを使うと効率的です。

```php
/**
 * @dataProvider unauthorizedRoutesProvider
 */
public function test_他のユーザーの書籍にアクセスできない(string $method, string $route): void
{
    $user1 = User::factory()->create();
    $user2 = User::factory()->create();
    $book = Book::factory()->create(['user_id' => $user1->id]);

    $response = $this->actingAs($user2)->{$method}(str_replace('{id}', $book->id, $route));

    $response->assertStatus(403);
}

public static function unauthorizedRoutesProvider(): array
{
    return [
        '詳細画面' => ['get', '/books/{id}'],
        '編集画面' => ['get', '/books/{id}/edit'],
        '更新処理' => ['put', '/books/{id}'],
        '削除処理' => ['delete', '/books/{id}'],
    ];
}
```

---

## Step 5: テストの実行と確認

### 5-1. 全テストを実行

```bash
sail artisan test
```

**出力例**:

```
   PASS  Tests\Feature\BookControllerTest
  ✓ 書籍一覧が表示される
  ✓ 書籍を登録できる
  ✓ タイトルなしで登録するとエラー
  ✓ 書籍を更新できる
  ✓ 書籍を削除できる
  ✓ 未認証ユーザーは一覧画面にアクセスできない
  ✓ 認証済みユーザーは一覧画面にアクセスできる
  ✓ 他のユーザーの書籍詳細にアクセスできない
  ✓ 他のユーザーの書籍を編集できない
  ✓ 他のユーザーの書籍を削除できない
  ✓ 自分の書籍詳細にアクセスできる

  Tests:    11 passed (22 assertions)
  Duration: 1.50s
```

---

## ✨ まとめ

このセクションでは、認証・認可テストについて学びました。

| テスト対象 | テスト内容 |
|:---|:---|
| 認証 | 未認証ユーザーがリダイレクトされること |
| 認可 | 他のユーザーの書籍にアクセスできないこと |
| 正常系 | 自分の書籍にはアクセスできること |

テストを書くことで、セキュリティの問題を早期に発見できます。

---
