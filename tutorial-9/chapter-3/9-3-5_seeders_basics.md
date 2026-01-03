# Tutorial 9-3-5: シーダーの基礎

## 🎯 このセクションで学ぶこと

*   シーダー（Seeder）を使って、初期データを投入できるようになる。
*   開発環境で、ダミーデータを効率的に生成できるようになる。
*   シーダーとファクトリーの違いを理解する。

---

## 導入：開発には「データ」が必要

マイグレーションを実行すると、データベースにテーブルが作成されます。しかし、テーブルが空のままでは、アプリケーションの動作を確認できません。

例えば、以下のような状況を考えてみましょう。

*   **ユーザー一覧ページを作りたい** → ユーザーデータが必要
*   **投稿の詳細ページを作りたい** → 投稿データが必要
*   **コメント機能をテストしたい** → ユーザーと投稿とコメントのデータが必要

手動でデータを入力するのは非効率です。そこで、Laravelでは、**シーダー（Seeder）**という仕組みを使って、初期データを自動的に投入できます。

---

## 詳細解説

### 🌱 シーダーとは？

シーダーとは、**データベースに初期データを投入するためのクラス**です。シーダーを使うことで、以下のようなデータを簡単に作成できます。

*   **マスターデータ**: カテゴリー、タグ、設定値など
*   **開発用ダミーデータ**: テスト用のユーザー、投稿、コメントなど
*   **管理者アカウント**: 本番環境で使う管理者ユーザー

---

### 📝 シーダーの作成

#### ステップ1: シーダーを生成する

```bash
sail artisan make:seeder UserSeeder
```

これにより、`database/seeders/UserSeeder.php`が生成されます。

**`database/seeders/UserSeeder.php`**

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class UserSeeder extends Seeder
{
    /**
     * Run the database seeds.
     */
    public function run(): void
    {
        // 管理者ユーザーを作成
        User::create([
            'name' => '管理者',
            'email' => 'admin@example.com',
            'password' => Hash::make('password'),
            'is_admin' => true,
        ]);

        // 一般ユーザーを作成
        User::create([
            'name' => '山田太郎',
            'email' => 'taro@example.com',
            'password' => Hash::make('password'),
            'is_admin' => false,
        ]);

        User::create([
            'name' => '佐藤花子',
            'email' => 'hanako@example.com',
            'password' => Hash::make('password'),
            'is_admin' => false,
        ]);
    }
}
```

**コードリーディング**

*   `run()`: シーダーが実行される際に呼ばれるメソッド
*   `User::create([...])`: ユーザーを作成します
*   `Hash::make('password')`: パスワードをハッシュ化します

---

### 🚀 シーダーの実行

#### 特定のシーダーを実行する

```bash
sail artisan db:seed --class=UserSeeder
```

#### 全てのシーダーを実行する

まず、`DatabaseSeeder.php`に、実行したいシーダーを登録します。

**`database/seeders/DatabaseSeeder.php`**

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Seed the application's database.
     */
    public function run(): void
    {
        $this->call([
            UserSeeder::class,
            PostSeeder::class,
            CommentSeeder::class,
        ]);
    }
}
```

**コードリーディング**

*   `$this->call([...])`: 指定したシーダーを順番に実行します

**実行**

```bash
sail artisan db:seed
```

---

### 🔗 シーダーとファクトリーの組み合わせ

シーダーでファクトリーを使うことで、大量のダミーデータを簡単に生成できます。

**`database/seeders/UserSeeder.php`**

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

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

**コードリーディング**

*   `User::factory()->create([...])`: ファクトリーを使って、特定の属性を持つユーザーを作成します
*   `User::factory()->count(10)->create()`: ファクトリーを使って、10人のランダムなユーザーを作成します

---

### 🎨 リレーションシップを持つデータの投入

ユーザーと投稿のように、リレーションシップを持つデータを投入する場合は、以下のようにします。

**`database/seeders/PostSeeder.php`**

```php
<?php

namespace Database\Seeders;

use Illuminate\Database\Seeder;
use App\Models\User;
use App\Models\Post;

class PostSeeder extends Seeder
{
    public function run(): void
    {
        // 全てのユーザーを取得
        $users = User::all();

        // 各ユーザーに3件の投稿を作成
        foreach ($users as $user) {
            Post::factory()->count(3)->create([
                'user_id' => $user->id,
            ]);
        }
    }
}
```

**より簡潔な書き方**

```php
public function run(): void
{
    User::all()->each(function ($user) {
        Post::factory()->count(3)->create(['user_id' => $user->id]);
    });
}
```

---

### 🔄 マイグレーションとシーダーを一度に実行する

開発中は、以下のコマンドを頻繁に使います。

```bash
sail artisan migrate:fresh --seed
```

これにより、以下の処理が実行されます。

1. 全てのテーブルを削除
2. マイグレーションを実行
3. シーダーを実行

---

### 💡 TIP: 環境ごとにシーダーを分ける

本番環境と開発環境で、異なるシーダーを実行したい場合は、環境変数を使います。

**`database/seeders/DatabaseSeeder.php`**

```php
public function run(): void
{
    if (app()->environment('local')) {
        // 開発環境でのみ実行
        $this->call([
            UserSeeder::class,
            PostSeeder::class,
        ]);
    }

    if (app()->environment('production')) {
        // 本番環境でのみ実行
        $this->call([
            AdminUserSeeder::class,
            CategorySeeder::class,
        ]);
    }
}
```

---

### 🚨 本番環境でのシーダー実行の注意点

本番環境では、シーダーを実行する際に注意が必要です。

#### 注意点1: 既存データが削除される可能性

`migrate:fresh --seed`を本番環境で実行すると、**全てのデータが削除**されます。絶対に実行してはいけません。

#### 注意点2: 重複データの防止

シーダーを複数回実行すると、データが重複する可能性があります。以下のように、重複を防ぐロジックを追加します。

```php
public function run(): void
{
    // 既に管理者ユーザーが存在する場合はスキップ
    if (User::where('email', 'admin@example.com')->exists()) {
        return;
    }

    User::create([
        'name' => '管理者',
        'email' => 'admin@example.com',
        'password' => Hash::make('password'),
        'is_admin' => true,
    ]);
}
```

または、`firstOrCreate()`を使います。

```php
User::firstOrCreate(
    ['email' => 'admin@example.com'],
    [
        'name' => '管理者',
        'password' => Hash::make('password'),
        'is_admin' => true,
    ]
);
```

---

### 🔍 シーダーとファクトリーの違い

| 概念 | 用途 | 実行タイミング |
|:---|:---|:---|
| **シーダー** | 初期データ、マスターデータの投入 | 開発環境のセットアップ、本番環境のデプロイ |
| **ファクトリー** | テストデータの生成 | テスト実行時、シーダー内での使用 |

**使い分けの例**

*   **シーダー**: 管理者ユーザー、カテゴリーマスター、設定値
*   **ファクトリー**: テスト用のユーザー、投稿、コメント

---

## ✨ まとめ

このセクションでは、シーダーを使って初期データを投入する方法を学びました。

*   シーダーは、データベースに初期データを投入するためのクラスである。
*   `php artisan make:seeder`でシーダーを作成できる。
*   `php artisan db:seed`でシーダーを実行できる。
*   シーダーとファクトリーを組み合わせることで、大量のダミーデータを簡単に生成できる。
*   `migrate:fresh --seed`で、データベースをリセットして初期データを投入できる。
*   本番環境では、シーダーを慎重に実行する必要がある。

次のセクションでは、ファクトリーについてさらに詳しく学びます。

---
