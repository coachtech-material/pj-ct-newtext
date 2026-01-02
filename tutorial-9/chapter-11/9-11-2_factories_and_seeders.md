# Tutorial 9-11-2: ファクトリーとシーダー

## 🎯 このセクションで学ぶこと

*   ファクトリー（Factory）を使って、テストデータを効率的に生成できるようになる。
*   シーダー（Seeder）を使って、開発用のダミーデータを一括生成できるようになる。
*   Fakerライブラリを使って、リアルなダミーデータを生成できるようになる。

---

## 導入：テストデータを手動で作るのは大変

前のセクションで、テストの基礎を学びました。しかし、テストを書く際に、毎回手動でテストデータを作成するのは非効率です。

```php
$user = User::create([
    'name' => '山田太郎',
    'email' => 'taro@example.com',
    'password' => bcrypt('password123'),
]);
```

このようなコードを、テストごとに書くのは面倒です。また、複雑なリレーションシップを持つデータ（例：ユーザーと投稿とコメント）を作成するのは、さらに大変です。

Laravelには、**ファクトリー（Factory）**という仕組みがあり、テストデータを簡単に生成できます。

---

## 詳細解説

### 🏭 ファクトリーとは？

ファクトリーとは、**モデルのインスタンスを簡単に生成するための設計図**です。ファクトリーを使うことで、以下のようにシンプルにテストデータを作成できます。

```php
$user = User::factory()->create();
```

これだけで、ランダムな名前、メールアドレス、パスワードを持つユーザーが作成されます。

---

### 📝 ファクトリーの定義

Laravelをインストールすると、`database/factories/UserFactory.php`が自動生成されています。

**`database/factories/UserFactory.php`**

```php
<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

class UserFactory extends Factory
{
    protected static ?string $password;

    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => static::$password ??= Hash::make('password'),
            'remember_token' => Str::random(10),
        ];
    }
}
```

**コードリーディング**

*   `fake()->name()`: Fakerライブラリを使って、ランダムな名前を生成します。
*   `fake()->unique()->safeEmail()`: 重複しない、安全なメールアドレスを生成します。
*   `Hash::make('password')`: パスワードをハッシュ化します。

---

### 🚀 ファクトリーの使い方

#### 1つのインスタンスを作成する

```php
$user = User::factory()->create();
```

これにより、データベースに1件のユーザーが作成されます。

#### 複数のインスタンスを作成する

```php
$users = User::factory()->count(10)->create();
```

これにより、10件のユーザーが作成されます。

#### データベースに保存せずにインスタンスを作成する

```php
$user = User::factory()->make();
```

`make()`を使うと、データベースに保存せずに、メモリ上にインスタンスを作成します。

#### 特定の属性を上書きする

```php
$user = User::factory()->create([
    'name' => '山田太郎',
    'email' => 'taro@example.com',
]);
```

これにより、名前とメールアドレスを指定して、ユーザーを作成できます。

---

### 🔗 リレーションシップを持つデータの生成

ファクトリーを使うと、リレーションシップを持つデータも簡単に生成できます。

#### 例：ユーザーと投稿を一緒に作成する

まず、`Post`モデルのファクトリーを作成します。

```bash
docker compose exec php php artisan make:factory PostFactory --model=Post
```

**`database/factories/PostFactory.php`**

```php
<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class PostFactory extends Factory
{
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'title' => fake()->sentence(),
            'content' => fake()->paragraph(),
            'is_published' => fake()->boolean(),
        ];
    }
}
```

**コードリーディング**

*   `'user_id' => User::factory()`: `user_id`には、自動的に新しいユーザーを作成して関連付けます。
*   `fake()->sentence()`: ランダムな文章を生成します。
*   `fake()->paragraph()`: ランダムな段落を生成します。
*   `fake()->boolean()`: ランダムな真偽値を生成します。

#### 使用例

```php
// ユーザーと投稿を一緒に作成
$post = Post::factory()->create();

// 既存のユーザーに紐付いた投稿を作成
$user = User::factory()->create();
$post = Post::factory()->create(['user_id' => $user->id]);

// 1人のユーザーに10件の投稿を作成
$user = User::factory()
            ->has(Post::factory()->count(10))
            ->create();
```

---

### 🌱 シーダーとは？

シーダー（Seeder）とは、**開発用のダミーデータを一括生成するための仕組み**です。テストではなく、開発環境でアプリケーションを動かす際に、ダミーデータを用意するために使います。

#### シーダーの作成

```bash
docker compose exec php php artisan make:seeder UserSeeder
```

**`database/seeders/UserSeeder.php`**

```php
<?php

namespace Database\Seeders;

use App\Models\User;
use Illuminate\Database\Seeder;

class UserSeeder extends Seeder
{
    public function run(): void
    {
        // 管理者ユーザーを作成
        User::factory()->create([
            'name' => '管理者',
            'email' => 'admin@example.com',
            'is_admin' => true,
        ]);

        // 一般ユーザーを10人作成
        User::factory()->count(10)->create();
    }
}
```

#### シーダーの実行

```bash
docker compose exec php php artisan db:seed --class=UserSeeder
```

または、`DatabaseSeeder.php`に登録して、一括実行することもできます。

**`database/seeders/DatabaseSeeder.php`**

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        $this->call([
            UserSeeder::class,
            PostSeeder::class,
        ]);
    }
}
```

```bash
docker compose exec php php artisan db:seed
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
| `fake()->numberBetween(1, 100)` | 1〜100のランダムな整数 |
| `fake()->boolean()` | true または false |
| `fake()->date()` | 2024-12-11 |
| `fake()->imageUrl()` | https://via.placeholder.com/640x480 |

#### 日本語のダミーデータを生成する

Fakerは、ロケールを設定することで、日本語のダミーデータを生成できます。

**`config/app.php`**

```php
'faker_locale' => 'ja_JP',
```

これにより、`fake()->name()`で「山田太郎」のような日本語の名前が生成されます。

---

## 💡 TIP: マイグレーションとシーダーを一度に実行する

開発環境をリセットして、ダミーデータを再生成したい場合は、以下のコマンドを使います。

```bash
docker compose exec php php artisan migrate:fresh --seed
```

これにより、全てのテーブルを削除し、マイグレーションを実行し、シーダーを実行します。

---

## ✨ まとめ

このセクションでは、ファクトリーとシーダーを使って、テストデータと開発用ダミーデータを効率的に生成する方法を学びました。

*   ファクトリーは、モデルのインスタンスを簡単に生成するための設計図である。
*   `User::factory()->create()`で、テストデータを簡単に作成できる。
*   シーダーは、開発用のダミーデータを一括生成するための仕組みである。
*   Fakerライブラリを使うと、リアルなダミーデータを生成できる。
*   `migrate:fresh --seed`で、データベースをリセットして、ダミーデータを再生成できる。


---
