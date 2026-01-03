# Tutorial 12-2-1: マイグレーションとモデルの作成

## 🎯 このセクションで学ぶこと

- tasksテーブルのマイグレーションファイルを作成する方法を学ぶ
- Taskモデルを作成し、データベースとの連携を理解する
- マイグレーションとモデルの関係を理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜマイグレーションとモデルから始めるのか？」

実装を始める前に、**なぜこの順番で進めるのか**を考えてみましょう。

多くの初学者は「画面を早く作りたい！」と思うかもしれません。しかし、経験豊富なエンジニアは**必ずデータベースから始めます**。その理由を説明します。

---

### 理由1: データがなければ何も表示できない

一覧画面を作っても、表示するデータがなければ意味がありません。

```
画面を作る → データがない → 何も表示されない → 動作確認できない
```

まずはデータを保存する「箱」（テーブル）を用意する必要があります。

---

### 理由2: データベース設計が全ての基盤になる

コントローラーやビューは、**データの形に依存**します。

例えば、タスクに「優先度」カラムを後から追加すると：
- マイグレーションの追加
- モデルの`$fillable`の修正
- コントローラーの修正
- ビューの修正
- バリデーションの修正

**全てのコードを修正する必要があります**。だから最初にしっかりとデータベースを設計します。

---

### 理由3: モデルがあれば動作確認できる

モデルを作成すれば、`php artisan tinker`でデータの作成・取得をテストできます。

```bash
# Tinkerでデータ操作をテスト
$ php artisan tinker
>>> Task::create(['title' => 'テスト', 'user_id' => 1]);
>>> Task::all();
```

画面を作る前に、**データ操作が正しく動くか確認できる**のです。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | tasksテーブルのマイグレーション作成 | テーブル構造を定義する |
| Step 2 | Taskモデルの作成 | データ操作の準備をする |
| Step 3 | categoriesテーブルの作成 | 関連テーブルも用意する |
| Step 4 | 動作確認 | Tinkerでデータ操作をテストする |

> 💡 **ポイント**: 「データファースト」の考え方で、まずはデータ層から構築します。

---

## Step 1: tasksテーブルのマイグレーション作成

### 1-1. マイグレーションファイルを生成する

以下のコマンドを実行します。

```bash
php artisan make:migration create_tasks_table
```

**実行結果**:

```
Created Migration: 2024_01_15_123456_create_tasks_table
```

`database/migrations/`ディレクトリに、マイグレーションファイルが作成されます。

---

### 1-2. マイグレーションファイルを編集する

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

### 1-3. コードリーディング

#### `Schema::create('tasks', function (Blueprint $table) { ... })`

- `tasks`という名前のテーブルを作成します

---

#### `$table->id()`

- `id`カラムを作成します
- データ型は`BIGINT UNSIGNED`で、主キー（PRIMARY KEY）、自動増分（AUTO_INCREMENT）が設定されます

---

#### `$table->foreignId('user_id')->constrained()->onDelete('cascade')`

- `user_id`カラムを作成します
- `constrained()`は、外部キー制約を設定します（デフォルトで`users`テーブルの`id`を参照）
- `onDelete('cascade')`は、ユーザーが削除されたら、そのユーザーのタスクも削除されることを意味します

---

#### `$table->foreignId('category_id')->nullable()->constrained()->onDelete('set null')`

- `category_id`カラムを作成します
- `nullable()`は、NULLを許可することを意味します
- `onDelete('set null')`は、カテゴリーが削除されたら、`category_id`をNULLに設定することを意味します

---

#### `$table->enum('status', ['pending', 'in_progress', 'completed'])->default('pending')`

- `status`カラムを作成します
- データ型は`ENUM`で、指定した値のみを取ります
- `default('pending')`は、デフォルト値を`pending`に設定します

---

#### `$table->timestamps()`

- `created_at`と`updated_at`カラムを作成します
- Laravelが自動的に値を管理します

---

### 1-4. マイグレーションを実行する

マイグレーションファイルを作成したら、以下のコマンドを実行して、データベースにテーブルを作成します。

```bash
php artisan migrate
```

**実行結果**:

```
Migrating: 2024_01_15_123456_create_tasks_table
Migrated:  2024_01_15_123456_create_tasks_table (50.23ms)
```

これで、`tasks`テーブルがデータベースに作成されました。

---

## Step 2: Taskモデルの作成

### 2-1. モデルを生成する

以下のコマンドを実行します。

```bash
php artisan make:model Task
```

**実行結果**:

```
Model created successfully.
```

`app/Models/`ディレクトリに、`Task.php`ファイルが作成されます。

---

### 2-2. モデルを編集する

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

### 2-3. コードリーディング

#### `class Task extends Model`

- `Task`クラスは、`Model`クラスを継承しています
- これにより、Eloquent ORMの機能を使えるようになります

---

#### `protected $fillable`

- **マスアサインメント（Mass Assignment）** を許可するカラムを指定します
- マスアサインメントとは、`create()`や`update()`メソッドで、配列を使ってデータを一括で登録・更新することです
- `$fillable`に指定されていないカラムは、マスアサインメントできません

---

#### `protected $casts`

- カラムのデータ型を指定します
- `due_date`カラムを`date`型にキャストすることで、Carbonオブジェクトとして扱えるようになります

---

## Step 3: categoriesテーブルの作成

### 3-1. categoriesテーブルのマイグレーションを作成する

```bash
php artisan make:migration create_categories_table
```

---

### 3-2. マイグレーションファイルを編集する

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

### 3-3. マイグレーションを実行する

```bash
php artisan migrate
```

---

### 3-4. Categoryモデルを作成する

```bash
php artisan make:model Category
```

---

### 3-5. モデルを編集する

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

## Step 4: 動作確認

### 4-1. phpMyAdminで確認する

phpMyAdminを開き、テーブルが作成されているか確認しましょう。

1. ブラウザで`http://localhost:8080`を開く
2. データベースを選択
3. `tasks`テーブルと`categories`テーブルが存在することを確認
4. テーブルの構造を確認

---

### 4-2. Tinkerでデータ操作をテストする

```bash
php artisan tinker
```

```php
// カテゴリーを作成
>>> App\Models\Category::create(['name' => '仕事']);
>>> App\Models\Category::create(['name' => 'プライベート']);

// タスクを作成
>>> App\Models\Task::create(['user_id' => 1, 'title' => 'テストタスク']);

// タスクを取得
>>> App\Models\Task::all();
```

---

## 🚨 よくある間違い

### 間違い1: $fillableを設定し忘れる

**エラー**:

```
Illuminate\Database\Eloquent\MassAssignmentException
Add [title] to fillable property to allow mass assignment on [App\Models\Task].
```

**対処法**: `$fillable`に、マスアサインメントを許可するカラムを追加します。

---

### 間違い2: 外部キー制約を設定し忘れる

**問題**: 関連するテーブルのデータが削除されても、参照しているデータが残ってしまう

**対処法**: `foreignId()`と`constrained()`を使って、外部キー制約を設定します。

---

### 間違い3: マイグレーションを実行し忘れる

**問題**: テーブルが作成されず、エラーになる

**対処法**: `php artisan migrate`を実行して、テーブルを作成します。

---

## 💡 TIP: マイグレーションとモデルを同時に作成する

以下のコマンドを使うと、マイグレーションとモデルを同時に作成できます。

```bash
php artisan make:model Task -m
```

`-m`オプションを付けると、モデルと一緒にマイグレーションファイルも作成されます。

---

## 💡 TIP: $fillableと$guarded

**$fillable**と**$guarded**は、マスアサインメントを制御するためのプロパティです。

- **$fillable**: マスアサインメントを許可するカラムを指定する（ホワイトリスト方式）
- **$guarded**: マスアサインメントを禁止するカラムを指定する（ブラックリスト方式）

実務では、**$fillable**を使うことが推奨されます。

---

## ✨ まとめ

このセクションでは、マイグレーションとモデルの作成について学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | `php artisan make:migration`でテーブル構造を定義 |
| Step 2 | `php artisan make:model`でデータ操作クラスを作成 |
| Step 3 | 関連テーブル（categories）も同様に作成 |
| Step 4 | phpMyAdminとTinkerで動作確認 |

次のセクションでは、タスク一覧の実装について学びます。

---
