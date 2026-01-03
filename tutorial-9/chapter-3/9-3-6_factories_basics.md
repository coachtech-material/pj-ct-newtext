# Tutorial 9-3-6: ファクトリーの基礎

## 🎯 このセクションで学ぶこと

*   ファクトリー（Factory）を使って、テストデータを効率的に生成できるようになる。
*   Fakerライブラリを使って、リアルなダミーデータを生成できるようになる。
*   リレーションシップを持つデータをファクトリーで生成できるようになる。

---

## 導入：テストデータを「量産」する

前のセクションで、シーダーを使って初期データを投入する方法を学びました。しかし、シーダーで手動でデータを作成するのは、大量のデータが必要な場合に非効率です。

例えば、以下のような状況を考えてみましょう。

*   **100人のユーザーを作成したい**
*   **各ユーザーに10件の投稿を作成したい**
*   **各投稿に5件のコメントを作成したい**

これを手動で書くのは大変です。そこで、Laravelでは、**ファクトリー（Factory）**という仕組みを使って、テストデータを効率的に生成できます。

---

## 詳細解説

### 🏭 ファクトリーとは？

ファクトリーとは、**モデルのインスタンスを簡単に生成するための設計図**です。ファクトリーを使うことで、以下のようにシンプルにテストデータを作成できます。

```php
$user = User::factory()->create();
```

これだけで、ランダムな名前、メールアドレス、パスワードを持つユーザーが作成されます。

---

### 📝 ファクトリーの作成

#### ステップ1: ファクトリーを生成する

```bash
docker compose exec php php artisan make:factory PostFactory --model=Post
```

これにより、`database/factories/PostFactory.php`が生成されます。

**`database/factories/PostFactory.php`**

```php
<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Post>
 */
class PostFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'title' => fake()->sentence(),
            'content' => fake()->paragraphs(3, true),
            'is_published' => fake()->boolean(80), // 80%の確率でtrue
            'published_at' => fake()->optional()->dateTimeBetween('-1 year', 'now'),
        ];
    }
}
```

**コードリーディング**

*   `definition()`: ファクトリーのデフォルトの状態を定義します
*   `fake()`: Fakerライブラリのインスタンスを取得します
*   `fake()->sentence()`: ランダムな文章を生成します
*   `fake()->paragraphs(3, true)`: 3段落のランダムなテキストを生成します
*   `fake()->boolean(80)`: 80%の確率で`true`を返します
*   `fake()->optional()`: 50%の確率で`null`を返します
*   `User::factory()`: ユーザーファクトリーを使って、自動的にユーザーを作成します

---

### 🚀 ファクトリーの使い方

#### 1つのインスタンスを作成する

```php
$post = Post::factory()->create();
```

これにより、データベースに1件の投稿が作成されます。

#### 複数のインスタンスを作成する

```php
$posts = Post::factory()->count(10)->create();
```

これにより、10件の投稿が作成されます。

#### データベースに保存せずにインスタンスを作成する

```php
$post = Post::factory()->make();
```

`make()`を使うと、データベースに保存せずに、メモリ上にインスタンスを作成します。テストで使うことが多いです。

#### 特定の属性を上書きする

```php
$post = Post::factory()->create([
    'title' => 'カスタムタイトル',
    'is_published' => true,
]);
```

---

### 🎨 Fakerライブラリ

Fakerは、リアルなダミーデータを生成するためのライブラリです。Laravelに標準で組み込まれています。

#### Fakerで生成できるデータの例

| メソッド | 生成されるデータ |
|:---|:---|
| `fake()->name()` | 山田太郎 |
| `fake()->email()` | taro@example.com |
| `fake()->phoneNumber()` | 090-1234-5678 |
| `fake()->address()` | 東京都渋谷区... |
| `fake()->company()` | 株式会社〇〇 |
| `fake()->sentence()` | This is a random sentence. |
| `fake()->paragraph()` | This is a random paragraph... |
| `fake()->text(200)` | 200文字のランダムなテキスト |
| `fake()->numberBetween(1, 100)` | 1〜100のランダムな整数 |
| `fake()->randomElement(['A', 'B', 'C'])` | A、B、Cのいずれか |
| `fake()->boolean()` | true または false |
| `fake()->date()` | 2024-12-11 |
| `fake()->dateTimeBetween('-1 year', 'now')` | 過去1年間のランダムな日時 |
| `fake()->imageUrl()` | https://via.placeholder.com/640x480 |

#### 日本語のダミーデータを生成する

Fakerは、ロケールを設定することで、日本語のダミーデータを生成できます。

**`config/app.php`**

```php
'faker_locale' => 'ja_JP',
```

これにより、`fake()->name()`で「山田太郎」のような日本語の名前が生成されます。

---

### 🔗 リレーションシップを持つデータの生成

#### 方法1: 自動的に関連データを作成する

```php
$post = Post::factory()->create();
```

`PostFactory`で`'user_id' => User::factory()`と定義しているため、自動的にユーザーも作成されます。

#### 方法2: 既存のユーザーに紐付ける

```php
$user = User::factory()->create();
$post = Post::factory()->create(['user_id' => $user->id]);
```

#### 方法3: 1人のユーザーに複数の投稿を作成する

```php
$user = User::factory()
    ->has(Post::factory()->count(10))
    ->create();
```

これにより、1人のユーザーと、そのユーザーに紐付いた10件の投稿が作成されます。

#### 方法4: 逆方向のリレーション

```php
$post = Post::factory()
    ->for(User::factory())
    ->create();
```

これにより、ユーザーを作成してから、そのユーザーに紐付いた投稿を作成します。

---

### 🎯 ファクトリーの状態（State）

ファクトリーには、**状態（State）**を定義することで、特定の条件を持つデータを簡単に生成できます。

**`database/factories/PostFactory.php`**

```php
/**
 * 公開済みの投稿
 */
public function published(): static
{
    return $this->state(fn (array $attributes) => [
        'is_published' => true,
        'published_at' => now(),
    ]);
}

/**
 * 下書きの投稿
 */
public function draft(): static
{
    return $this->state(fn (array $attributes) => [
        'is_published' => false,
        'published_at' => null,
    ]);
}
```

**使用例**

```php
// 公開済みの投稿を10件作成
$publishedPosts = Post::factory()->count(10)->published()->create();

// 下書きの投稿を5件作成
$draftPosts = Post::factory()->count(5)->draft()->create();
```

---

### 💡 TIP: シーダーでファクトリーを使う

シーダーとファクトリーを組み合わせることで、効率的にダミーデータを生成できます。

**`database/seeders/DatabaseSeeder.php`**

```php
public function run(): void
{
    // 管理者ユーザーを作成
    $admin = User::factory()->create([
        'name' => '管理者',
        'email' => 'admin@example.com',
        'is_admin' => true,
    ]);

    // 一般ユーザーを10人作成し、各ユーザーに5件の投稿を作成
    User::factory()
        ->count(10)
        ->has(Post::factory()->count(5))
        ->create();
}
```

---

### 🚨 ファクトリーのベストプラクティス

#### 1. リアルなデータを生成する

```php
'email' => fake()->unique()->safeEmail(),
```

`unique()`を使うことで、重複しないメールアドレスを生成できます。

#### 2. 外部キーは`factory()`を使う

```php
'user_id' => User::factory(),
```

これにより、関連するデータも自動的に作成されます。

#### 3. 状態（State）を活用する

```php
Post::factory()->published()->create();
Post::factory()->draft()->create();
```

---

## ✨ まとめ

このセクションでは、ファクトリーを使ってテストデータを効率的に生成する方法を学びました。

*   ファクトリーは、モデルのインスタンスを簡単に生成するための設計図である。
*   `php artisan make:factory`でファクトリーを作成できる。
*   `Post::factory()->create()`でテストデータを簡単に作成できる。
*   Fakerライブラリを使うと、リアルなダミーデータを生成できる。
*   `has()`や`for()`を使って、リレーションシップを持つデータを生成できる。
*   状態（State）を定義することで、特定の条件を持つデータを簡単に生成できる。

次のセクションでは、トランザクション処理について学びます。

---
