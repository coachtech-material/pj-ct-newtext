# Tutorial 11-2-1: マイグレーションとモデルの作成

## 🎯 このセクションで学ぶこと

*   tasksテーブルのマイグレーションファイルを作成する方法を学ぶ。
*   Taskモデルを作成し、データベースとの連携を理解する。
*   マイグレーションとモデルの関係を理解する。

---

## 導入：マイグレーションとモデルの役割

**マイグレーション（Migration）**は、**データベースのテーブル構造を管理するファイル**です。

**モデル（Model）**は、**データベースのテーブルとやり取りするためのクラス**です。

この2つを作成することで、**データベースとLaravelアプリケーションを連携**させることができます。

---

## 詳細解説

### 🔍 マイグレーションファイルの作成

まず、tasksテーブルのマイグレーションファイルを作成します。

---

#### ステップ1: マイグレーションファイルを生成する

以下のコマンドを実行します。

```bash
php artisan make:migration create_tasks_table
```

---

#### 実行結果

```
Created Migration: 2024_01_15_123456_create_tasks_table
```

`database/migrations/`ディレクトリに、マイグレーションファイルが作成されます。

---

#### ステップ2: マイグレーションファイルを編集する

作成されたマイグレーションファイルを開き、以下のように編集します。

**ファイル**: `database/migrations/2024_01_15_123456_create_tasks_table.php`

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
        Schema::create('tasks', function (Blueprint $table) {
            $table->id();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->foreignId('category_id')->nullable()->constrained()->onDelete('set null');
            $table->string('title');
            $table->text('description')->nullable();
            $table->enum('status', ['pending', 'in_progress', 'completed'])->default('pending');
            $table->date('due_date')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('tasks');
    }
};
```

---

### 🔍 コードリーディング

#### `Schema::create('tasks', function (Blueprint $table) { ... })`

*   `tasks`という名前のテーブルを作成します。

---

#### `$table->id()`

*   `id`カラムを作成します。
*   データ型は`BIGINT UNSIGNED`で、主キー（PRIMARY KEY）、自動増分（AUTO_INCREMENT）が設定されます。

---

#### `$table->foreignId('user_id')->constrained()->onDelete('cascade')`

*   `user_id`カラムを作成します。
*   データ型は`BIGINT UNSIGNED`です。
*   `constrained()`は、外部キー制約を設定します。デフォルトでは、`users`テーブルの`id`カラムを参照します。
*   `onDelete('cascade')`は、ユーザーが削除されたら、そのユーザーのタスクも削除されることを意味します。

---

#### `$table->foreignId('category_id')->nullable()->constrained()->onDelete('set null')`

*   `category_id`カラムを作成します。
*   `nullable()`は、NULLを許可することを意味します。
*   `onDelete('set null')`は、カテゴリーが削除されたら、そのカテゴリーに属するタスクの`category_id`をNULLに設定することを意味します。

---

#### `$table->string('title')`

*   `title`カラムを作成します。
*   データ型は`VARCHAR(255)`です。

---

#### `$table->text('description')->nullable()`

*   `description`カラムを作成します。
*   データ型は`TEXT`です。
*   `nullable()`は、NULLを許可することを意味します。

---

#### `$table->enum('status', ['pending', 'in_progress', 'completed'])->default('pending')`

*   `status`カラムを作成します。
*   データ型は`ENUM`で、`pending`、`in_progress`、`completed`のいずれかの値を取ります。
*   `default('pending')`は、デフォルト値を`pending`に設定します。

---

#### `$table->date('due_date')->nullable()`

*   `due_date`カラムを作成します。
*   データ型は`DATE`です。
*   `nullable()`は、NULLを許可することを意味します。

---

#### `$table->timestamps()`

*   `created_at`と`updated_at`カラムを作成します。
*   データ型は`TIMESTAMP`です。

---

#### `Schema::dropIfExists('tasks')`

*   `tasks`テーブルが存在する場合、削除します。
*   マイグレーションをロールバックする際に使用されます。

---

### 🔍 マイグレーションの実行

マイグレーションファイルを作成したら、以下のコマンドを実行して、データベースにテーブルを作成します。

```bash
php artisan migrate
```

---

#### 実行結果

```
Migrating: 2024_01_15_123456_create_tasks_table
Migrated:  2024_01_15_123456_create_tasks_table (50.23ms)
```

これで、`tasks`テーブルがデータベースに作成されました。

---

### 💡 TIP: phpMyAdminで確認する

phpMyAdminを開き、`tasks`テーブルが作成されているか確認しましょう。

1. ブラウザで`http://localhost:8080`を開く
2. データベースを選択
3. `tasks`テーブルをクリック
4. テーブルの構造を確認

---

### 🔍 モデルの作成

次に、Taskモデルを作成します。

---

#### ステップ1: モデルを生成する

以下のコマンドを実行します。

```bash
php artisan make:model Task
```

---

#### 実行結果

```
Model created successfully.
```

`app/Models/`ディレクトリに、`Task.php`ファイルが作成されます。

---

#### ステップ2: モデルを編集する

作成されたモデルファイルを開き、以下のように編集します。

**ファイル**: `app/Models/Task.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Task extends Model
{
    use HasFactory;

    /**
     * The attributes that are mass assignable.
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'user_id',
        'category_id',
        'title',
        'description',
        'status',
        'due_date',
    ];

    /**
     * The attributes that should be cast.
     *
     * @var array<string, string>
     */
    protected $casts = [
        'due_date' => 'date',
    ];
}
```

---

### 🔍 コードリーディング

#### `class Task extends Model`

*   `Task`クラスは、`Model`クラスを継承しています。
*   これにより、`Task`クラスは、Eloquent ORMの機能を使えるようになります。

---

#### `use HasFactory`

*   `HasFactory`トレイトを使用しています。
*   これにより、ファクトリーを使ってテストデータを作成できるようになります。

---

#### `protected $fillable`

*   **マスアサインメント（Mass Assignment）**を許可するカラムを指定します。
*   マスアサインメントとは、`create()`や`update()`メソッドで、配列を使ってデータを一括で登録・更新することです。
*   `$fillable`に指定されていないカラムは、マスアサインメントできません。

---

#### `protected $casts`

*   カラムのデータ型を指定します。
*   `due_date`カラムを`date`型にキャストすることで、Carbonオブジェクトとして扱えるようになります。

---

### 💡 TIP: $fillableと$guarded

**$fillable**と**$guarded**は、マスアサインメントを制御するためのプロパティです。

*   **$fillable**: マスアサインメントを許可するカラムを指定する（ホワイトリスト方式）
*   **$guarded**: マスアサインメントを禁止するカラムを指定する（ブラックリスト方式）

実務では、**$fillable**を使うことが推奨されます。

---

### 🚀 実践: マイグレーションとモデルを作成しよう

#### ステップ1: categoriesテーブルのマイグレーションを作成する

```bash
php artisan make:migration create_categories_table
```

---

#### ステップ2: マイグレーションファイルを編集する

**ファイル**: `database/migrations/2024_01_15_123457_create_categories_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('categories', function (Blueprint $table) {
            $table->id();
            $table->string('name')->unique();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('categories');
    }
};
```

---

#### ステップ3: マイグレーションを実行する

```bash
php artisan migrate
```

---

#### ステップ4: Categoryモデルを作成する

```bash
php artisan make:model Category
```

---

#### ステップ5: モデルを編集する

**ファイル**: `app/Models/Category.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Category extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
    ];
}
```

---

### 🚨 よくある間違い

#### 間違い1: $fillableを設定し忘れる

**エラー**:

```
Illuminate\Database\Eloquent\MassAssignmentException
Add [title] to fillable property to allow mass assignment on [App\Models\Task].
```

**対処法**: `$fillable`に、マスアサインメントを許可するカラムを追加します。

---

#### 間違い2: 外部キー制約を設定し忘れる

**対処法**: `foreignId()`と`constrained()`を使って、外部キー制約を設定します。

---

#### 間違い3: マイグレーションを実行し忘れる

**対処法**: `php artisan migrate`を実行して、テーブルを作成します。

---

### 💡 TIP: マイグレーションとモデルを同時に作成する

以下のコマンドを使うと、マイグレーションとモデルを同時に作成できます。

```bash
php artisan make:model Task -m
```

*   `-m`オプションは、マイグレーションファイルも同時に作成することを意味します。

---

## ✨ まとめ

このセクションでは、tasksテーブルのマイグレーションとTaskモデルの作成について学びました。

*   マイグレーションファイルを作成し、テーブルの構造を定義する。
*   `php artisan migrate`を実行して、データベースにテーブルを作成する。
*   モデルを作成し、`$fillable`でマスアサインメントを許可するカラムを指定する。
*   外部キー制約を設定することで、データの整合性を保つ。

次のセクションでは、タスク一覧の実装について学びます。

---

## 📝 学習のポイント

- [ ] tasksテーブルのマイグレーションファイルを作成する方法を学んだ。
- [ ] Taskモデルを作成し、データベースとの連携を理解した。
- [ ] マイグレーションとモデルの関係を理解した。
