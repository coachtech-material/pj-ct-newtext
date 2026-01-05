# Tutorial 13-6-1: テスト環境のセットアップ

## 🎯 このセクションで学ぶこと

- PHPUnitを使ったテストの基本を理解する
- テスト用データベースの設定方法を学ぶ
- Factoryでテストデータを生成する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜテストを書くのか？」

テストを書くことで、以下のメリットがあります。

| メリット | 説明 |
|:---|:---|
| バグの早期発見 | 修正後に他の機能が壊れていないか確認できる |
| リファクタリングの安心感 | テストがあれば安心してコードを改善できる |
| 仕様書としての役割 | テストコードが仕様を説明する |

---

## Step 1: テスト用データベースの設定

### 1-1. phpunit.xmlの確認

**ファイル**: `phpunit.xml`

```xml
<php>
    <env name="APP_ENV" value="testing"/>
    <env name="DB_CONNECTION" value="sqlite"/>
    <env name="DB_DATABASE" value=":memory:"/>
</php>
```

> 💡 **ポイント**: テスト時はSQLiteのインメモリデータベースを使用します。本番のデータベースに影響を与えません。

### 1-2. RefreshDatabaseトレイト

テストクラスで`RefreshDatabase`トレイトを使うと、テストごとにデータベースがリセットされます。

```php
use Illuminate\Foundation\Testing\RefreshDatabase;

class BookControllerTest extends TestCase
{
    use RefreshDatabase;
    
    // ...
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

use App\Models\Category;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class BookFactory extends Factory
{
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'category_id' => Category::factory(),
            'title' => fake()->sentence(3),
            'author' => fake()->name(),
            'rating' => fake()->numberBetween(1, 5),
            'review' => fake()->paragraph(),
        ];
    }
}
```

### 2-3. CategoryFactoryを作成

```bash
sail artisan make:factory CategoryFactory
```

**ファイル**: `database/factories/CategoryFactory.php`

```php
<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

class CategoryFactory extends Factory
{
    public function definition(): array
    {
        return [
            'name' => fake()->randomElement(['プログラミング', 'ビジネス', '小説', '自己啓発', 'その他']),
        ];
    }
}
```

---

## Step 3: Factoryの使い方

### 3-1. 基本的な使い方

```php
use App\Models\Book;
use App\Models\User;

// 1件作成（DBに保存）
$book = Book::factory()->create();

// 1件作成（DBに保存しない）
$book = Book::factory()->make();

// 複数件作成
$books = Book::factory()->count(5)->create();
```

### 3-2. 属性を指定して作成

```php
// 特定のユーザーの書籍を作成
$user = User::factory()->create();
$book = Book::factory()->create(['user_id' => $user->id]);

// 評価を指定
$book = Book::factory()->create(['rating' => 5]);
```

### 3-3. リレーションを含めて作成

```php
// ユーザーと書籍を同時に作成
$user = User::factory()
    ->has(Book::factory()->count(3))
    ->create();

// $user->books で3件の書籍が取得できる
```

---

## Step 4: テストの実行

### 4-1. 全テストを実行

```bash
sail artisan test
```

### 4-2. 特定のテストファイルを実行

```bash
sail artisan test tests/Feature/BookControllerTest.php
```

### 4-3. 特定のテストメソッドを実行

```bash
sail artisan test --filter=test_書籍一覧が表示される
```

---

## ✨ まとめ

このセクションでは、テスト環境のセットアップについて学びました。

| Step | 学んだこと |
|:---|:---|
| Step 1 | テスト用データベースの設定 |
| Step 2 | Factoryの作成 |
| Step 3 | Factoryの使い方 |
| Step 4 | テストの実行方法 |

次のセクションでは、CRUDのテストを書いていきます。

---
