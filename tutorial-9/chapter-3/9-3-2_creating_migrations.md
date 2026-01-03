# Tutorial 9-3-2: マイグレーションファイルの作成

## 🎯 このセクションで学ぶこと

*   `php artisan make:migration`コマンドを使って、マイグレーションファイルを生成できるようになる。
*   `Blueprint`クラスを使って、様々なカラム型を定義できるようになる。
*   外部キー制約、インデックス、ユニーク制約などを設定できるようになる。

---

## 導入：実際にテーブルを作成してみよう

前のセクションで、マイグレーションの概念と、既存のマイグレーションファイルの構造を学びました。このセクションでは、実際に新しいマイグレーションファイルを作成し、カスタムテーブルを作成する方法を学びます。

例として、ブログアプリケーションの`posts`テーブルを作成してみましょう。

---

## 詳細解説

### 🛠️ マイグレーションファイルの生成

マイグレーションファイルは、`php artisan make:migration`コマンドで生成します。

```bash
sail artisan make:migration create_posts_table
```

**コマンドの構成**

*   `make:migration`: マイグレーションファイルを生成するコマンド
*   `create_posts_table`: マイグレーションの名前（任意）。慣例として、`create_テーブル名_table`という形式にします。

このコマンドを実行すると、`database/migrations/`ディレクトリに、タイムスタンプ付きのファイルが生成されます。

```
database/migrations/
└── 2024_12_11_123456_create_posts_table.php
```

**生成されたファイルの内容**

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
        Schema::create('posts', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
};
```

Laravelは、マイグレーション名から「`posts`テーブルを作成する」ことを推測し、`Schema::create('posts', ...)`というコードを自動生成してくれます。

---

### 📝 カラムの定義

`up()`メソッドの中で、`Blueprint`クラスを使ってカラムを定義します。

#### 基本的なカラム型

| メソッド | 説明 | SQLの型 |
|:---|:---|:---|
| `$table->id()` | 主キー（自動増分） | `BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY` |
| `$table->string('name')` | 文字列（最大255文字） | `VARCHAR(255)` |
| `$table->string('name', 100)` | 文字列（最大100文字） | `VARCHAR(100)` |
| `$table->text('content')` | 長い文字列 | `TEXT` |
| `$table->integer('age')` | 整数 | `INT` |
| `$table->bigInteger('views')` | 大きな整数 | `BIGINT` |
| `$table->boolean('is_published')` | 真偽値 | `TINYINT(1)` |
| `$table->date('published_at')` | 日付 | `DATE` |
| `$table->datetime('published_at')` | 日時 | `DATETIME` |
| `$table->timestamp('published_at')` | タイムスタンプ | `TIMESTAMP` |
| `$table->timestamps()` | `created_at`と`updated_at` | `TIMESTAMP` |

#### 例：`posts`テーブルのカラムを定義する

```php
public function up(): void
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->string('title');
        $table->text('content');
        $table->boolean('is_published')->default(false);
        $table->integer('views')->default(0);
        $table->timestamp('published_at')->nullable();
        $table->timestamps();
    });
}
```

**コードリーディング**

*   `$table->id()`: 主キー（`id`カラム）を作成します。
*   `$table->string('title')`: `title`カラムを作成します（最大255文字）。
*   `$table->text('content')`: `content`カラムを作成します（長い文字列）。
*   `$table->boolean('is_published')->default(false)`: `is_published`カラムを作成し、デフォルト値を`false`に設定します。
*   `$table->integer('views')->default(0)`: `views`カラムを作成し、デフォルト値を`0`に設定します。
*   `$table->timestamp('published_at')->nullable()`: `published_at`カラムを作成し、`NULL`を許可します。
*   `$table->timestamps()`: `created_at`と`updated_at`カラムを作成します。

---

### 🔗 外部キー制約の定義

Tutorial 8で学んだように、外部キー制約を使うことで、データの整合性を保つことができます。例えば、`posts`テーブルに`user_id`カラムを追加し、`users`テーブルの`id`と紐付けてみましょう。

```php
public function up(): void
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->string('title');
        $table->text('content');
        $table->boolean('is_published')->default(false);
        $table->integer('views')->default(0);
        $table->timestamp('published_at')->nullable();
        $table->timestamps();
    });
}
```

**コードリーディング**

*   `$table->foreignId('user_id')`: `user_id`カラムを作成します。これは、`BIGINT UNSIGNED`型です。
*   `->constrained()`: 外部キー制約を自動的に設定します。Laravelは、カラム名から「`users`テーブルの`id`カラムを参照する」ことを推測します。
*   `->onDelete('cascade')`: 参照先のユーザーが削除されたときに、この投稿も一緒に削除されるように設定します。

もし、参照先のテーブル名やカラム名が異なる場合は、以下のように明示的に指定します。

```php
$table->foreignId('author_id')->constrained('users', 'id')->onDelete('cascade');
```

---

### 🔍 インデックスとユニーク制約

検索を高速化するために、インデックスを追加することができます。

```php
$table->string('email')->unique(); // ユニーク制約（重複を許さない）
$table->string('slug')->index();   // インデックス（検索を高速化）
```

複数のカラムに対して、複合インデックスを作成することもできます。

```php
$table->index(['user_id', 'created_at']);
```

---

### ✏️ カラムの修飾子

カラムには、様々な修飾子を付けることができます。

| 修飾子 | 説明 |
|:---|:---|
| `->nullable()` | `NULL`を許可する |
| `->default($value)` | デフォルト値を設定する |
| `->unsigned()` | 符号なし整数にする |
| `->unique()` | ユニーク制約を付ける |
| `->index()` | インデックスを付ける |
| `->comment('コメント')` | カラムにコメントを付ける |

**例**

```php
$table->integer('age')->unsigned()->nullable()->default(0)->comment('ユーザーの年齢');
```

---

### 🚀 マイグレーションの実行

マイグレーションファイルを作成したら、以下のコマンドで実行します。

```bash
sail artisan migrate
```

**実行結果のイメージ**

```
INFO  Running migrations.

2024_12_11_123456_create_posts_table .................. 15ms DONE
```

phpMyAdminで確認すると、`posts`テーブルが作成されていることが確認できます。

**[ここに、phpMyAdminで`posts`テーブルを確認したスクリーンショットを挿入]**

---

### 🔄 既存のテーブルにカラムを追加する

既に存在するテーブルに、新しいカラムを追加したい場合は、新しいマイグレーションファイルを作成します。

```bash
sail artisan make:migration add_subtitle_to_posts_table
```

**生成されたファイル**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('posts', function (Blueprint $table) {
            $table->string('subtitle')->nullable()->after('title');
        });
    }

    public function down(): void
    {
        Schema::table('posts', function (Blueprint $table) {
            $table->dropColumn('subtitle');
        });
    }
};
```

**コードリーディング**

*   `Schema::table('posts', ...)`: 既存の`posts`テーブルを変更します（`Schema::create`ではなく`Schema::table`を使います）。
*   `$table->string('subtitle')->nullable()->after('title')`: `subtitle`カラムを追加し、`title`カラムの後に配置します。
*   `$table->dropColumn('subtitle')`: `down()`メソッドで、`subtitle`カラムを削除します。

マイグレーションを実行します。

```bash
sail artisan migrate
```

これで、`posts`テーブルに`subtitle`カラムが追加されます。

---

## 💡 TIP: マイグレーションファイルの命名規則

マイグレーションファイルの名前は、以下のような規則に従うと、Laravelが自動的にコードを生成してくれます。

| パターン | 例 | 自動生成されるコード |
|:---|:---|:---|
| `create_テーブル名_table` | `create_posts_table` | `Schema::create('posts', ...)` |
| `add_カラム名_to_テーブル名_table` | `add_subtitle_to_posts_table` | `Schema::table('posts', ...)` |
| `drop_テーブル名_table` | `drop_posts_table` | `Schema::dropIfExists('posts')` |

この規則に従うことで、コードを書く手間が省けます。

---

## ✨ まとめ

このセクションでは、マイグレーションファイルの作成方法を学びました。

*   `php artisan make:migration`コマンドで、マイグレーションファイルを生成できる。
*   `Blueprint`クラスを使って、様々なカラム型（`string`, `text`, `integer`, `boolean`, `timestamp`など）を定義できる。
*   `->nullable()`, `->default()`, `->unique()`などの修飾子を使って、カラムの制約を設定できる。
*   `foreignId()->constrained()`を使って、外部キー制約を設定できる。
*   既存のテーブルにカラムを追加する場合は、`Schema::table()`を使う。

次のセクションでは、Eloquent ORMを使って、マイグレーションで作成したテーブルのデータを操作する方法を学びます。

---
