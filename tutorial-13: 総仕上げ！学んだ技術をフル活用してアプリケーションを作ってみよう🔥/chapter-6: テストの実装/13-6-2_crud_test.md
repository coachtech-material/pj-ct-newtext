# Tutorial 13-6-2: CRUDテスト

## 🎯 このセクションで学ぶこと

- 書籍のCRUD機能をテストする方法を学ぶ
- HTTPテストの書き方を理解する
- アサーションメソッドの使い方を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜセットアップの次にCRUDテストなのか？」

Factoryができたら、まず**CRUDのテスト**を書きます。

### 理由1: 基本機能からテスト

```
CRUDテスト → 基本機能が動くか確認
認証テスト → セキュリティが動くか確認
```

### 理由2: AAAパターン

テストは**AAAパターン**で書きます。

| フェーズ | 英語 | 内容 |
|:---|:---|:---|
| 準備 | Arrange | テストデータを作成 |
| 実行 | Act | テスト対象の処理を実行 |
| 検証 | Assert | 結果を確認 |

---

## Step 1: テストファイルの作成

### 1-1. BookControllerTestを作成

```bash
sail artisan make:test BookControllerTest
```

### 1-2. テストファイルの基本構造

**ファイル**: `tests/Feature/BookControllerTest.php`

```php
<?php

namespace Tests\Feature;

use App\Models\Book;
use App\Models\Category;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class BookControllerTest extends TestCase
{
    use RefreshDatabase;

    // テストメソッドをここに追加
}
```

---

## Step 2: 一覧表示のテスト

### 2-1. 書籍一覧が表示されることをテスト

```php
public function test_書籍一覧が表示される(): void
{
    // 準備
    $user = User::factory()->create();
    $book = Book::factory()->create(['user_id' => $user->id]);

    // 実行
    $response = $this->actingAs($user)->get('/books');

    // 検証
    $response->assertStatus(200);
    $response->assertSee($book->title);
}
```

### 2-2. コードリーディング

#### `$this->actingAs($user)->get('/books')`の分解

| 部分 | 説明 | 戻り値 |
|:---|:---|:---|
| `$this` | TestCaseインスタンス | - |
| `->actingAs($user)` | 指定ユーザーとしてログイン | TestCase |
| `->get('/books')` | GETリクエストを送信 | TestResponse |

> 💡 **メソッドチェーンの流れ**: `actingAs()` → `get()` と順番に処理が連鎖します。

#### アサーションメソッド

| コード | 説明 |
|:---|:---|
| `assertStatus(200)` | HTTPステータスが200であることを検証 |
| `assertSee($book->title)` | レスポンスに書籍タイトルが含まれることを検証 |

---

## Step 3: 登録のテスト

### 3-1. 書籍を登録できることをテスト

```php
public function test_書籍を登録できる(): void
{
    // 準備
    $user = User::factory()->create();
    $category = Category::factory()->create();

    // 実行
    $response = $this->actingAs($user)->post('/books', [
        'title' => 'テスト書籍',
        'author' => 'テスト著者',
        'category_id' => $category->id,
        'rating' => 5,
        'review' => 'テストレビュー',
    ]);

    // 検証
    $response->assertRedirect('/books');
    $this->assertDatabaseHas('books', [
        'title' => 'テスト書籍',
        'user_id' => $user->id,
    ]);
}
```

### 3-2. バリデーションエラーのテスト

```php
public function test_タイトルなしで登録するとエラー(): void
{
    // 準備
    $user = User::factory()->create();

    // 実行
    $response = $this->actingAs($user)->post('/books', [
        'title' => '',  // 空
        'author' => 'テスト著者',
        'rating' => 5,
    ]);

    // 検証
    $response->assertSessionHasErrors('title');
}
```

---

## Step 4: 更新のテスト

### 4-1. 書籍を更新できることをテスト

```php
public function test_書籍を更新できる(): void
{
    // 準備
    $user = User::factory()->create();
    $book = Book::factory()->create(['user_id' => $user->id]);

    // 実行
    $response = $this->actingAs($user)->put("/books/{$book->id}", [
        'title' => '更新後のタイトル',
        'author' => $book->author,
        'rating' => $book->rating,
    ]);

    // 検証
    $response->assertRedirect("/books/{$book->id}");
    $this->assertDatabaseHas('books', [
        'id' => $book->id,
        'title' => '更新後のタイトル',
    ]);
}
```

---

## Step 5: 削除のテスト

### 5-1. 書籍を削除できることをテスト

```php
public function test_書籍を削除できる(): void
{
    // 準備
    $user = User::factory()->create();
    $book = Book::factory()->create(['user_id' => $user->id]);

    // 実行
    $response = $this->actingAs($user)->delete("/books/{$book->id}");

    // 検証
    $response->assertRedirect('/books');
    $this->assertDatabaseMissing('books', [
        'id' => $book->id,
    ]);
}
```

---

## Step 6: よく使うアサーションメソッド

| メソッド | 説明 |
|:---|:---|
| `assertStatus(200)` | HTTPステータスを検証 |
| `assertRedirect('/path')` | リダイレクト先を検証 |
| `assertSee('text')` | レスポンスにテキストが含まれることを検証 |
| `assertDatabaseHas('table', [...])` | DBにデータが存在することを検証 |
| `assertDatabaseMissing('table', [...])` | DBにデータが存在しないことを検証 |
| `assertSessionHasErrors('field')` | セッションにエラーがあることを検証 |

---

## ✨ まとめ

このセクションでは、CRUDテストについて学びました。

| テスト対象 | テスト内容 |
|:---|:---|
| 一覧表示 | 書籍一覧が表示されること |
| 登録 | 書籍を登録できること、バリデーションエラー |
| 更新 | 書籍を更新できること |
| 削除 | 書籍を削除できること |

次のセクションでは、認証・認可のテストを書いていきます。

---
