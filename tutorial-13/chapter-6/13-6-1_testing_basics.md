# Tutorial 13-6-1: テストの基礎

## 🎯 このセクションで学ぶこと

- PHPUnitを使ったテストの基本を理解する
- 書籍CRUD機能のテストを作成する
- テストを実行して動作を確認する

---

## テストとは

**テスト**とは、**コードが期待通りに動作するかを自動的に確認する仕組み**です。

### なぜテストが必要か

| 問題 | テストがあれば |
|:---|:---|
| 修正後に別の機能が壊れた | テストで検出できる |
| 動作確認を毎回手動で行う | 自動化で時間短縮 |
| 仕様が不明確 | テストが仕様書になる |

---

## Step 1: テストファイルの作成

### 1-1. BookControllerTestを作成

```bash
sail artisan make:test BookControllerTest
```

### 1-2. テストファイルを編集

**ファイル**: `tests/Feature/BookControllerTest.php`

```php
<?php

namespace Tests\Feature;

use App\Models\Book;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class BookControllerTest extends TestCase
{
    use RefreshDatabase;

    /**
     * 書籍一覧が表示されることをテスト
     */
    public function test_書籍一覧が表示される(): void
    {
        $user = User::factory()->create();
        $book = Book::factory()->create(['user_id' => $user->id]);

        $response = $this->actingAs($user)->get('/books');

        $response->assertStatus(200);
        $response->assertSee($book->title);
    }

    /**
     * 書籍を登録できることをテスト
     */
    public function test_書籍を登録できる(): void
    {
        $user = User::factory()->create();

        $response = $this->actingAs($user)->post('/books', [
            'title' => 'テスト書籍',
            'author' => 'テスト著者',
            'rating' => 5,
            'review' => 'テストレビュー',
        ]);

        $response->assertRedirect('/books');
        $this->assertDatabaseHas('books', [
            'title' => 'テスト書籍',
            'user_id' => $user->id,
        ]);
    }

    /**
     * 他のユーザーの書籍にアクセスできないことをテスト
     */
    public function test_他のユーザーの書籍にアクセスできない(): void
    {
        $user1 = User::factory()->create();
        $user2 = User::factory()->create();
        $book = Book::factory()->create(['user_id' => $user1->id]);

        $response = $this->actingAs($user2)->get("/books/{$book->id}");

        $response->assertStatus(403);
    }
}
```

---

## Step 2: Factoryの作成

### 2-1. BookFactoryを作成

```bash
sail artisan make:factory BookFactory
```

### 2-2. BookFactoryを編集

**ファイル**: `database/factories/BookFactory.php`

```php
<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class BookFactory extends Factory
{
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'title' => fake()->sentence(3),
            'author' => fake()->name(),
            'rating' => fake()->numberBetween(1, 5),
            'review' => fake()->paragraph(),
        ];
    }
}
```

---

## Step 3: テストの実行

### 3-1. テストを実行

```bash
sail artisan test
```

**出力例**:

```
   PASS  Tests\Feature\BookControllerTest
  ✓ 書籍一覧が表示される
  ✓ 書籍を登録できる
  ✓ 他のユーザーの書籍にアクセスできない

  Tests:    3 passed (6 assertions)
  Duration: 0.50s
```

### 3-2. 特定のテストのみ実行

```bash
sail artisan test --filter=書籍一覧が表示される
```

---

## Step 4: コードリーディング

| コード | 説明 |
|:---|:---|
| `use RefreshDatabase` | テストごとにDBをリセット |
| `User::factory()->create()` | テスト用ユーザーを作成 |
| `$this->actingAs($user)` | 指定ユーザーとしてログイン |
| `$response->assertStatus(200)` | HTTPステータスを検証 |
| `$this->assertDatabaseHas(...)` | DBにデータが存在するか検証 |

---

## ✨ まとめ

このセクションでは、テストの基礎について学びました。

- PHPUnitを使ったテストの作成方法
- Factoryでテストデータを生成
- `sail artisan test`でテストを実行

テストを書くことで、コードの品質を保ちながら開発を進められます。

---
