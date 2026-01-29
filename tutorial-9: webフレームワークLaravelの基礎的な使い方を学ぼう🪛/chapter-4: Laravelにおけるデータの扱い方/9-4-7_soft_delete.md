# Tutorial 9-4-7: ソフトデリート（論理削除）の実装

## 🎯 このセクションで学ぶこと

*   ソフトデリート（論理削除）と物理削除の違いを理解する。
*   Eloquentの`SoftDeletes`トレイトを使った、ソフトデリートの実装方法を理解する。
*   削除済みデータの取得、復元、完全削除の方法を理解する。

---

## 導入：データを「本当に」消していいのか？

前のセクションで、`delete()`メソッドを使ってデータを削除する方法を学びました。しかし、実務では「データを完全に消す」ことは意外と少ないです。

例えば、以下のような場面を考えてみてください。

*   **ユーザーが退会した**: 退会したユーザーのデータを完全に消すと、過去の注文履歴や投稿が参照できなくなる。
*   **投稿を削除した**: 誤って削除した場合、復元できなくなる。
*   **商品を販売終了した**: 過去の注文履歴で商品情報が参照できなくなる。

これらの問題を解決するのが、**ソフトデリート（論理削除）**です。

---

## 詳細解説

### 🗑️ 物理削除とソフトデリートの違い

| 項目 | 物理削除 | ソフトデリート（論理削除） |
|:---|:---|:---|
| **動作** | データベースからレコードを完全に削除 | `deleted_at`カラムに削除日時を記録 |
| **復元** | 不可能 | 可能 |
| **データ容量** | 削除後は容量が減る | 削除後も容量は変わらない |
| **参照整合性** | 外部キー制約に注意が必要 | 関連データを保持できる |
| **実装の複雑さ** | シンプル | やや複雑（クエリに条件が追加される） |

**ソフトデリートの仕組み**

ソフトデリートでは、レコードを削除する代わりに、`deleted_at`カラムに削除日時を記録します。通常のクエリでは、`deleted_at`がNULLのレコードのみが取得されます。

```
-- 物理削除
DELETE FROM users WHERE id = 1;

-- ソフトデリート（実際の動作）
UPDATE users SET deleted_at = '2024-01-15 10:30:00' WHERE id = 1;
```

---

### 🛠️ ソフトデリートの実装

#### 1. マイグレーションに`deleted_at`カラムを追加

まず、テーブルに`deleted_at`カラムを追加するマイグレーションを作成します。

```bash
sail artisan make:migration add_soft_deletes_to_posts_table
```

**マイグレーションファイル**

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
            $table->softDeletes(); // deleted_at カラムを追加
        });
    }

    public function down(): void
    {
        Schema::table('posts', function (Blueprint $table) {
            $table->dropSoftDeletes(); // deleted_at カラムを削除
        });
    }
};
```

**コードリーディング**

*   `$table->softDeletes()`: `deleted_at`という名前の`TIMESTAMP`型カラムを追加します。デフォルトはNULLです。
*   `$table->dropSoftDeletes()`: `deleted_at`カラムを削除します。

マイグレーションを実行します。

```bash
sail artisan migrate
```

#### 2. モデルに`SoftDeletes`トレイトを追加

次に、モデルに`SoftDeletes`トレイトを追加します。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Post extends Model
{
    use SoftDeletes;
    
    protected $fillable = ['title', 'content', 'user_id'];
}
```

**コードリーディング**

*   `use SoftDeletes;`: このトレイトを追加することで、ソフトデリート機能が有効になります。

これだけで、ソフトデリートの実装は完了です。

---

### 📝 ソフトデリートの基本操作

#### データを削除する（ソフトデリート）

```php
$post = Post::find(1);
$post->delete();
```

このコードを実行すると、レコードは削除されず、`deleted_at`カラムに現在の日時が記録されます。

#### 削除済みかどうかを確認する

```php
$post = Post::withTrashed()->find(1);

if ($post->trashed()) {
    echo 'この投稿は削除済みです';
}
```

**コードリーディング**

*   `withTrashed()`: 削除済みのレコードも含めて取得します。
*   `trashed()`: レコードがソフトデリートされているかどうかを確認します。

---

### 🔍 削除済みデータの取得

#### 削除済みのレコードも含めて取得

```php
// 削除済みも含めて全件取得
$posts = Post::withTrashed()->get();

// 削除済みも含めて条件検索
$posts = Post::withTrashed()->where('user_id', 1)->get();
```

#### 削除済みのレコードのみを取得

```php
// 削除済みのみ取得
$deletedPosts = Post::onlyTrashed()->get();

// 削除済みの件数を取得
$deletedCount = Post::onlyTrashed()->count();
```

#### 通常のクエリ（削除済みを除外）

```php
// 通常のクエリは、削除済みを自動的に除外
$posts = Post::all(); // deleted_at が NULL のレコードのみ
```

---

### 🔄 削除済みデータの復元

ソフトデリートの大きなメリットは、削除したデータを復元できることです。

```php
// 削除済みのレコードを取得
$post = Post::withTrashed()->find(1);

// 復元する
$post->restore();
```

**復元後**、`deleted_at`カラムはNULLに戻り、通常のクエリで取得できるようになります。

#### 条件を指定して一括復元

```php
// 特定のユーザーの削除済み投稿を全て復元
Post::onlyTrashed()->where('user_id', 1)->restore();
```

---

### 💀 完全削除（物理削除）

ソフトデリートを使っていても、データを完全に削除したい場合があります。

```php
// 削除済みのレコードを取得
$post = Post::withTrashed()->find(1);

// 完全に削除（物理削除）
$post->forceDelete();
```

**コードリーディング**

*   `forceDelete()`: ソフトデリートを無視して、レコードを完全に削除します。

> ⚠️ **注意**: `forceDelete()`を実行すると、データは復元できなくなります。

---

### 🧩 リレーションシップとソフトデリート

ソフトデリートを使う場合、リレーションシップにも注意が必要です。

#### 削除済みの関連データを含める

```php
// ユーザーの投稿を取得（削除済みも含む）
$user = User::find(1);
$posts = $user->posts()->withTrashed()->get();
```

#### カスケード削除の代わりにソフトデリート

親レコードを削除したときに、子レコードもソフトデリートしたい場合は、モデルのイベントを使います。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class User extends Model
{
    use SoftDeletes;

    protected static function booted(): void
    {
        // ユーザーが削除されたとき、投稿もソフトデリート
        static::deleted(function (User $user) {
            $user->posts()->delete();
        });

        // ユーザーが復元されたとき、投稿も復元
        static::restored(function (User $user) {
            $user->posts()->onlyTrashed()->restore();
        });
    }

    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}
```

---

### 📊 実務でのソフトデリートの使い分け

| テーブル | 推奨 | 理由 |
|:---|:---|:---|
| **users** | ソフトデリート | 退会後も注文履歴等で参照される可能性がある |
| **posts** | ソフトデリート | 誤削除の復元、管理者による確認が必要 |
| **orders** | ソフトデリート | 会計・監査のためにデータを保持する必要がある |
| **comments** | ケースバイケース | 重要度による |
| **sessions** | 物理削除 | 一時的なデータなので保持する必要がない |
| **password_resets** | 物理削除 | セキュリティ上、使用後は削除すべき |

---

## 💡 TIP: ソフトデリートのインデックス

ソフトデリートを使う場合、`deleted_at`カラムにインデックスを追加すると、クエリのパフォーマンスが向上します。

```php
Schema::table('posts', function (Blueprint $table) {
    $table->index('deleted_at');
});
```

---

## ✨ まとめ

このセクションでは、ソフトデリート（論理削除）の実装方法を学びました。

*   **ソフトデリート**は、データを完全に削除せず、`deleted_at`カラムに削除日時を記録する仕組みである。
*   マイグレーションで`$table->softDeletes()`を追加し、モデルで`use SoftDeletes;`を宣言する。
*   `delete()`でソフトデリート、`restore()`で復元、`forceDelete()`で完全削除ができる。
*   `withTrashed()`で削除済みも含めて取得、`onlyTrashed()`で削除済みのみを取得できる。
*   実務では、ユーザーや注文など、復元や監査が必要なデータにはソフトデリートを使うことが多い。

ソフトデリートは、実務で非常に頻繁に使われる機能です。物理削除との使い分けを意識して、適切に実装することが重要です。

---
