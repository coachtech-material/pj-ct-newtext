# Tutorial 13-2-1: マイグレーションとモデルの作成

## 🎯 このセクションで学ぶこと

- 書籍レビューアプリのマイグレーションを作成する
- Bookモデルを作成し、fillableを設定する
- イシュー駆動開発の流れを実践する

---

## Step 0: 開発の準備（チケット駆動）

### 0-1. GitHubでIssueを確認

GitHubで `#1 書籍一覧機能` のIssueを確認します。

このセクションでは、書籍一覧機能の土台となる**マイグレーションとモデル**を作成します。

### 0-2. mainブランチを最新化

```bash
git checkout main
git pull origin main
```

### 0-3. Issue番号付きブランチを作成

```bash
git switch -c feature/issue-1-book-list
```

> 💡 **ポイント**: ブランチ名にIssue番号を含めることで、どのIssueに対応しているかが明確になります。

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜマイグレーションとモデルから始めるのか？」

多くの初学者は「画面を早く作りたい！」と思うかもしれません。しかし、経験豊富なエンジニアは**必ずデータベースから始めます**。

### 理由1: データがなければ何も表示できない

```
❌ 先に画面を作る
→ 「データがないから表示できない...」
→ ダミーデータをハードコードしてしまう

✅ 先にテーブルとモデルを作る
→ Tinkerでテストデータを作成
→ 画面で実際のデータを表示できる
```

### 理由2: モデルがあれば動作確認できる

モデルを作成すれば、`php artisan tinker`でデータの作成・取得をテストできます。画面を作る前に、**データ操作が正しく動くか確認できる**のです。

---

### このセクションの実装順序

| 順番 | 作業 | 理由 |
|:---:|:---|:---|
| 1 | マイグレーション作成 | テーブルがないとデータを保存できない |
| 2 | マイグレーション実行 | テーブルを実際に作成 |
| 3 | モデル作成 | Eloquentでデータ操作するため |
| 4 | Tinkerで確認 | データ操作が動くかテスト |

---

## Step 1: マイグレーションの作成

### 1-1. マイグレーションファイルを生成する

```bash
sail artisan make:migration create_books_table
```

**出力例**:

```
Created Migration: 2024_01_01_000000_create_books_table
```

### 1-2. マイグレーションファイルを編集する

**ファイル**: `database/migrations/xxxx_xx_xx_xxxxxx_create_books_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('books', function (Blueprint $table) {
            $table->id();
            $table->string('title');           // 書籍タイトル
            $table->string('author');          // 著者名
            $table->tinyInteger('rating');     // 評価（1〜5）
            $table->text('review')->nullable(); // レビュー（任意）
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('books');
    }
};
```

> 💡 **ポイント**: `user_id`は後のChapter（認証機能）で追加します。まずはシンプルな構成で進めます。

---

### 1-3. コードリーディング

| コード | 説明 |
|:---|:---|
| `$table->id()` | 主キー（BIGINT, AUTO_INCREMENT） |
| `$table->string('title')` | VARCHAR(255)型のカラム |
| `$table->tinyInteger('rating')` | 小さな整数（1〜5の評価に最適） |
| `$table->text('review')->nullable()` | 長文テキスト、NULL許可 |
| `$table->timestamps()` | created_at, updated_atを自動作成 |

---

### 1-4. マイグレーションを実行する

```bash
sail artisan migrate
```

**出力例**:

```
Migrating: 2024_01_01_000000_create_books_table
Migrated:  2024_01_01_000000_create_books_table (25.67ms)
```

### 1-5. phpMyAdminで確認

`http://localhost:8080`にアクセスし、`books`テーブルが作成されていることを確認します。

---

## Step 2: モデルの作成

### 2-1. Bookモデルを生成する

```bash
sail artisan make:model Book
```

**出力例**:

```
Model created successfully.
```

### 2-2. モデルファイルを編集する

**ファイル**: `app/Models/Book.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Book extends Model
{
    use HasFactory;

    /**
     * 一括代入可能な属性
     */
    protected $fillable = [
        'title',
        'author',
        'rating',
        'review',
    ];
}
```

---

### 2-3. $fillableとは

`$fillable`に指定した属性のみ、`create()`や`update()`で一括代入できます。

```php
// $fillableに'title', 'author', 'rating', 'review'が指定されている場合
Book::create([
    'title' => 'リーダブルコード',
    'author' => 'Dustin Boswell',
    'rating' => 5,
    'review' => '必読書です。'
]); // ✅ 成功

// $fillableに指定されていない属性を含む場合
Book::create([
    'title' => 'リーダブルコード',
    'id' => 999,  // idは$fillableに含まれていない
]); // ❌ エラー（Mass Assignment Exception）
```

これにより、**意図しない属性の変更を防ぐ**ことができます。

---

## Step 3: Tinkerで動作確認

### 3-1. Tinkerを起動

```bash
sail artisan tinker
```

### 3-2. 書籍を作成

```php
use App\Models\Book;

Book::create([
    'title' => 'リーダブルコード',
    'author' => 'Dustin Boswell',
    'rating' => 5,
    'review' => '読みやすいコードを書くための必読書です。'
]);
```

### 3-3. 書籍を取得

```php
Book::all();
```

### Tinkerコマンドのコードリーディング

| コード | 説明 |
|:---|:---|
| `use App\Models\Book;` | Bookモデルを使用可能にする |
| `Book::create([...])` | 新しい書籍レコードを作成して保存 |
| `Book::all()` | 全ての書籍レコードを取得 |

#### `Book::create([...])`の分解

| 部分 | 説明 |
|:---|:---|
| `Book` | Bookモデルクラス |
| `::` | 静的メソッド呼び出し（インスタンス不要） |
| `create([...])` | 配列の内容でレコードを作成 |
| 戻り値 | 作成されたBookインスタンス |

**出力例**:

```
=> Illuminate\Database\Eloquent\Collection {#1234
     all: [
       App\Models\Book {#5678
         id: 1,
         title: "リーダブルコード",
         author: "Dustin Boswell",
         rating: 5,
         review: "読みやすいコードを書くための必読書です。",
         created_at: "2024-01-01 00:00:00",
         updated_at: "2024-01-01 00:00:00",
       },
     ],
   }
```

### 3-4. Tinkerを終了

```php
exit
```

---

## Step 4: コミットとプッシュ

### 4-1. 変更をステージング

```bash
git add .
```

### 4-2. コミット

```bash
git commit -m "feat: booksテーブルとBookモデルを作成"
```

> 💡 **ポイント**: まだIssueをクローズしないので、`Closes #1`は含めません。書籍一覧画面の実装が完了してからクローズします。

### 4-3. プッシュ

```bash
git push origin feature/issue-1-book-list
```

---

## 🚨 よくある間違い

### 間違い1: $fillableを設定し忘れる

**エラー例**:

```
Add [title] to fillable property to allow mass assignment on [App\Models\Book].
```

**対処法**: `$fillable`に属性を追加します。

---

### 間違い2: マイグレーションを実行し忘れる

**対処法**: `sail artisan migrate`を実行します。

---

### 間違い3: Tinkerでモデルをuseし忘れる

**対処法**: `use App\Models\Book;`を実行してからモデルを使用します。

---

## 💡 TIP: マイグレーションとモデルを同時に作成する

以下のコマンドを使うと、マイグレーションとモデルを同時に作成できます。

```bash
sail artisan make:model Book -m
```

`-m`オプションを付けると、モデルと一緒にマイグレーションファイルも作成されます。

---

## ✨ まとめ

このセクションでは、マイグレーションとモデルの作成について学びました。

| Step | 学んだこと |
|:---|:---|
| Step 0 | イシュー駆動開発の流れ（ブランチ作成） |
| Step 1 | `books`テーブルのマイグレーション作成 |
| Step 2 | `Book`モデルの作成と`$fillable`の設定 |
| Step 3 | Tinkerで動作確認 |
| Step 4 | コミットとプッシュ |

次のセクションでは、書籍一覧画面を実装します。

---
