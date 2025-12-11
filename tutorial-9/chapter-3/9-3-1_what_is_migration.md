# Tutorial 9-3-1: マイグレーションとは

## 🎯 このセクションで学ぶこと

*   マイグレーションが何であるか、その役割を理解する。
*   なぜマイグレーションを使うのか、「直接SQLを実行する」方法との違いを説明できるようになる。
*   マイグレーションファイルの構造を理解し、`up()`と`down()`メソッドの役割を説明できるようになる。

---

## 導入：データベースのテーブル構造を「コード」で管理する

Tutorial 8で、SQLを使ってデータベースのテーブルを作成する方法を学びました。例えば、`users`テーブルを作成するには、以下のようなSQLを実行しました。

```sql
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NULL,
    updated_at TIMESTAMP NULL
);
```

しかし、この方法には以下のような問題があります。

*   **チーム開発で同期が取れない**: 他の開発者が同じテーブル構造を再現するには、SQLファイルを共有し、手動で実行する必要がある。
*   **変更履歴が残らない**: テーブル構造を変更した際、「いつ、誰が、何を変更したか」の履歴が残らない。
*   **ロールバックが難しい**: テーブル構造を元に戻したい場合、手動でSQLを書いて実行する必要がある。
*   **環境ごとの差異**: 開発環境、テスト環境、本番環境で、テーブル構造が微妙に異なってしまうことがある。

これらの問題を解決するのが、**マイグレーション（Migration）**です。

---

## 詳細解説

### 🏗️ マイグレーションとは？

マイグレーションとは、**データベースのテーブル構造を「コード」で管理する仕組み**です。テーブルの作成、カラムの追加、インデックスの追加などを、PHPのコードとして記述し、バージョン管理（Git）で管理します。

Laravelでは、マイグレーションファイルを`database/migrations/`ディレクトリに配置し、`php artisan migrate`コマンドで実行します。

### 🔑 マイグレーションのメリット

マイグレーションを使うことで、以下のようなメリットがあります。

#### 1. **チーム全員が同じテーブル構造を共有できる**

マイグレーションファイルをGitで管理することで、他の開発者は`git pull`でファイルを取得し、`php artisan migrate`を実行するだけで、同じテーブル構造を再現できます。

#### 2. **変更履歴が残る**

マイグレーションファイルは、タイムスタンプ付きのファイル名で保存されるため、「いつ、どのような変更が行われたか」が一目で分かります。

```
database/migrations/
├── 2024_01_01_000000_create_users_table.php
├── 2024_01_15_120000_add_phone_to_users_table.php
└── 2024_02_10_090000_create_posts_table.php
```

#### 3. **ロールバックが簡単**

マイグレーションには、テーブルを作成する`up()`メソッドと、テーブルを削除する`down()`メソッドの両方が定義されています。これにより、`php artisan migrate:rollback`コマンドで、変更を元に戻すことができます。

#### 4. **環境ごとの差異をなくせる**

開発環境、テスト環境、本番環境で、全て同じマイグレーションファイルを実行することで、環境ごとの差異をなくすことができます。

---

### 📝 マイグレーションファイルの構造

Laravelをインストールすると、いくつかのマイグレーションファイルが自動生成されています。`database/migrations/`ディレクトリを見てみましょう。

```
database/migrations/
├── 2014_10_12_000000_create_users_table.php
├── 2014_10_12_100000_create_password_reset_tokens_table.php
└── 2019_08_19_000000_create_failed_jobs_table.php
```

これらのファイルは、Laravelの認証機能やジョブキュー機能で使うテーブルを作成するためのものです。

`2014_10_12_000000_create_users_table.php`を開いてみましょう。

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::create('users', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->string('email')->unique();
            $table->timestamp('email_verified_at')->nullable();
            $table->string('password');
            $table->rememberToken();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('users');
    }
};
```

**コードリーディング**

*   `return new class extends Migration`: 無名クラスを使って、`Migration`クラスを継承しています。これは、PHP 8以降の新しい書き方です。
*   `public function up()`: マイグレーションを実行したときに呼ばれるメソッドです。ここに、テーブルを作成する処理を書きます。
*   `Schema::create('users', ...)`: `users`という名前のテーブルを作成します。
*   `function (Blueprint $table)`: `Blueprint`クラスを使って、カラムを定義します。
*   `$table->id()`: 主キー（`id`カラム）を作成します。これは、`BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY`に相当します。
*   `$table->string('name')`: `VARCHAR(255)`型の`name`カラムを作成します。
*   `$table->string('email')->unique()`: `email`カラムを作成し、`UNIQUE`制約を付けます。
*   `$table->timestamps()`: `created_at`と`updated_at`カラムを作成します。これらは、Eloquent ORMが自動的に更新します。
*   `public function down()`: マイグレーションをロールバックしたときに呼ばれるメソッドです。ここに、テーブルを削除する処理を書きます。
*   `Schema::dropIfExists('users')`: `users`テーブルが存在する場合、削除します。

---

### 🔄 マイグレーションの実行とロールバック

マイグレーションを実行するには、以下のコマンドを使います。

```bash
docker compose exec php php artisan migrate
```

このコマンドを実行すると、`database/migrations/`ディレクトリ内の全てのマイグレーションファイルが順番に実行され、テーブルが作成されます。

**実行結果のイメージ**

```
INFO  Running migrations.

2014_10_12_000000_create_users_table .................. 10ms DONE
2014_10_12_100000_create_password_reset_tokens_table .. 5ms DONE
2019_08_19_000000_create_failed_jobs_table ............ 8ms DONE
```

#### マイグレーションの状態を確認する

どのマイグレーションが実行済みかを確認するには、以下のコマンドを使います。

```bash
docker compose exec php php artisan migrate:status
```

**実行結果のイメージ**

```
Migration name ......................................... Batch / Status
2014_10_12_000000_create_users_table ................... [1] Ran
2014_10_12_100000_create_password_reset_tokens_table ... [1] Ran
2019_08_19_000000_create_failed_jobs_table ............. [1] Ran
```

#### ロールバックする

最後に実行したマイグレーションを元に戻すには、以下のコマンドを使います。

```bash
docker compose exec php php artisan migrate:rollback
```

これにより、`down()`メソッドが実行され、テーブルが削除されます。

#### 全てのマイグレーションをロールバックする

全てのマイグレーションを元に戻すには、以下のコマンドを使います。

```bash
docker compose exec php php artisan migrate:reset
```

#### 全てのマイグレーションをロールバックして再実行する

開発中は、テーブル構造を何度も変更することがあります。その場合、以下のコマンドで、全てのマイグレーションをロールバックして再実行できます。

```bash
docker compose exec php php artisan migrate:refresh
```

これは、`migrate:reset`と`migrate`を連続で実行するのと同じです。

---

## 💡 TIP: マイグレーションの実行履歴は`migrations`テーブルに保存される

Laravelは、どのマイグレーションが実行済みかを、`migrations`という特別なテーブルに記録しています。phpMyAdminで`migrations`テーブルを見てみると、以下のようなデータが保存されています。

| id | migration | batch |
|:---|:---|:---|
| 1 | 2014_10_12_000000_create_users_table | 1 |
| 2 | 2014_10_12_100000_create_password_reset_tokens_table | 1 |
| 3 | 2019_08_19_000000_create_failed_jobs_table | 1 |

`batch`は、マイグレーションを実行した「バッチ番号」です。`migrate:rollback`を実行すると、最後のバッチ番号のマイグレーションだけがロールバックされます。

---

## ✨ まとめ

このセクションでは、マイグレーションの概念と、その役割を学びました。

*   マイグレーションとは、データベースのテーブル構造を「コード」で管理する仕組みである。
*   マイグレーションを使うことで、チーム全員が同じテーブル構造を共有でき、変更履歴が残り、ロールバックが簡単になる。
*   マイグレーションファイルには、`up()`メソッド（テーブル作成）と`down()`メソッド（テーブル削除）が定義されている。
*   `php artisan migrate`でマイグレーションを実行し、`php artisan migrate:rollback`でロールバックできる。
*   マイグレーションの実行履歴は、`migrations`テーブルに保存される。

次のセクションでは、実際にマイグレーションファイルを作成し、カスタムテーブルを作成する方法を学びます。

---

## 📝 学習のポイント

- [ ] マイグレーションが、データベースのテーブル構造を「コード」で管理する仕組みであることを理解した。
- [ ] マイグレーションを使うメリット（チーム開発、変更履歴、ロールバック）を説明できる。
- [ ] `up()`メソッドと`down()`メソッドの役割を理解した。
- [ ] `php artisan migrate`でマイグレーションを実行できる。
- [ ] `php artisan migrate:rollback`でマイグレーションをロールバックできる。
