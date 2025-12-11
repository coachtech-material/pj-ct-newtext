# Tutorial 9-4-1: Eloquent ORMとは

## 🎯 このセクションで学ぶこと

*   ORM（Object-Relational Mapping）が何であるか、その役割を理解する。
*   Eloquent ORMを使うことで、SQLを書かずにデータベース操作ができることを理解する。
*   モデルとテーブルの対応関係を理解し、Eloquentの「規約」を説明できるようになる。

---

## 導入：「オブジェクト」でデータベースを操作する

Tutorial 8で、SQLを使ってデータベースのデータを操作する方法を学びました。例えば、全てのユーザーを取得するには、以下のようなSQLを実行しました。

```sql
SELECT * FROM users;
```

しかし、PHPのコードの中でSQLを直接書くと、以下のような問題があります。

*   **SQLの文法を覚える必要がある**: `SELECT`, `WHERE`, `JOIN`などの文法を正確に書く必要がある。
*   **SQLインジェクションのリスク**: ユーザー入力をそのままSQLに埋め込むと、攻撃を受ける可能性がある。
*   **コードが読みにくい**: SQLとPHPが混在し、コードが複雑になる。
*   **データベースの種類に依存する**: MySQL、PostgreSQL、SQLiteなど、データベースによってSQLの方言が異なる。

これらの問題を解決するのが、**ORM（Object-Relational Mapping）**です。

---

## 詳細解説

### 🏗️ ORMとは？

ORM（Object-Relational Mapping）とは、**データベースのテーブルを「オブジェクト」として扱う仕組み**です。SQLを書かずに、PHPのオブジェクト指向の構文で、データベースを操作できます。

Laravelには、**Eloquent ORM**という強力なORMが標準で組み込まれています。Eloquentを使うことで、以下のようなメリットがあります。

*   **SQLを書かなくて良い**: PHPのメソッドを呼び出すだけで、データベース操作ができる。
*   **SQLインジェクションを自動的に防ぐ**: Eloquentは、内部的にプリペアドステートメントを使うため、安全。
*   **コードが読みやすい**: オブジェクト指向の構文で、直感的にデータベース操作ができる。
*   **データベースの種類に依存しない**: MySQL、PostgreSQL、SQLiteなど、どのデータベースでも同じコードで動作する。

### 🔍 SQLとEloquentの比較

同じ操作を、SQLとEloquentで比較してみましょう。

#### 例1: 全てのユーザーを取得する

**SQL**
```sql
SELECT * FROM users;
```

**Eloquent**
```php
$users = User::all();
```

#### 例2: IDが1のユーザーを取得する

**SQL**
```sql
SELECT * FROM users WHERE id = 1;
```

**Eloquent**
```php
$user = User::find(1);
```

#### 例3: メールアドレスが一致するユーザーを取得する

**SQL**
```sql
SELECT * FROM users WHERE email = 'taro@example.com';
```

**Eloquent**
```php
$user = User::where('email', 'taro@example.com')->first();
```

#### 例4: 新しいユーザーを作成する

**SQL**
```sql
INSERT INTO users (name, email, password) VALUES ('山田太郎', 'taro@example.com', 'hashed_password');
```

**Eloquent**
```php
$user = User::create([
    'name' => '山田太郎',
    'email' => 'taro@example.com',
    'password' => bcrypt('password'),
]);
```

#### 例5: ユーザーを更新する

**SQL**
```sql
UPDATE users SET name = '山田花子' WHERE id = 1;
```

**Eloquent**
```php
$user = User::find(1);
$user->name = '山田花子';
$user->save();
```

#### 例6: ユーザーを削除する

**SQL**
```sql
DELETE FROM users WHERE id = 1;
```

**Eloquent**
```php
$user = User::find(1);
$user->delete();
```

このように、Eloquentを使うことで、SQLを書かずに、直感的にデータベース操作ができます。

---

### 🧩 モデルとテーブルの対応関係

Eloquent ORMでは、**1つのモデルクラスが、1つのデータベーステーブルに対応**します。

| モデルクラス | テーブル名 |
|:---|:---|
| `User` | `users` |
| `Post` | `posts` |
| `Comment` | `comments` |
| `Category` | `categories` |

Laravelは、「規約より設定（Convention over Configuration）」の哲学に基づいており、以下のような規約があります。

*   **モデル名は単数形、テーブル名は複数形**: `User`モデルは`users`テーブルに対応します。
*   **主キーは`id`**: デフォルトでは、主キーのカラム名は`id`と推測されます。
*   **タイムスタンプは`created_at`と`updated_at`**: デフォルトでは、これらのカラムが自動的に更新されます。

もし、これらの規約に従わない場合は、モデルクラスでプロパティを明示的に指定することもできます。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    // テーブル名を明示的に指定
    protected $table = 'blog_posts';

    // 主キーのカラム名を明示的に指定
    protected $primaryKey = 'post_id';

    // タイムスタンプを使わない場合
    public $timestamps = false;
}
```

しかし、基本的には規約に従うことで、コードがシンプルになります。

---

### 📝 モデルの作成

モデルは、`php artisan make:model`コマンドで生成します。

```bash
docker compose exec php php artisan make:model Post
```

このコマンドを実行すると、`app/Models/Post.php`というファイルが生成されます。

**生成されたファイルの内容**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    use HasFactory;
}
```

**コードリーディング**

*   `namespace App\Models;`: このクラスが`App\Models`という名前空間に属することを示します。
*   `use HasFactory;`: ファクトリー機能（テストデータ生成）を使えるようにします。
*   `class Post extends Model`: `Post`クラスを定義し、`Model`クラスを継承します。

この状態で、既に`posts`テーブルとの対応関係が自動的に設定されています。

#### モデルとマイグレーションを同時に生成する

モデルを作成する際に、`-m`オプションを付けると、マイグレーションファイルも同時に生成されます。

```bash
docker compose exec php php artisan make:model Post -m
```

これにより、`app/Models/Post.php`と`database/migrations/xxxx_create_posts_table.php`が同時に生成されます。

---

## 💡 TIP: Eloquentは「Active Record」パターン

Eloquentは、「Active Record」というデザインパターンを採用しています。これは、**1つのオブジェクトが、1つのデータベースレコードに対応する**という考え方です。

```php
// 1つのオブジェクト = 1つのレコード
$user = User::find(1);
$user->name = '山田花子';
$user->save(); // データベースに保存
```

このパターンにより、オブジェクト指向の考え方で、直感的にデータベース操作ができます。

---

## ✨ まとめ

このセクションでは、Eloquent ORMの概念と、その役割を学びました。

*   ORM（Object-Relational Mapping）とは、データベースのテーブルを「オブジェクト」として扱う仕組みである。
*   Eloquent ORMを使うことで、SQLを書かずに、PHPのメソッドでデータベース操作ができる。
*   1つのモデルクラスが、1つのデータベーステーブルに対応する。
*   Laravelの規約に従うことで、モデル名からテーブル名が自動的に推測される。
*   `php artisan make:model`コマンドで、モデルを生成できる。

次のセクションでは、Eloquentを使って、実際にデータの取得・作成・更新・削除（CRUD操作）を行う方法を学びます。

---

## 📝 学習のポイント

- [ ] ORMが、データベースのテーブルを「オブジェクト」として扱う仕組みであることを理解した。
- [ ] Eloquent ORMを使うことで、SQLを書かずにデータベース操作ができることを理解した。
- [ ] 1つのモデルクラスが、1つのデータベーステーブルに対応することを理解した。
- [ ] モデル名は単数形、テーブル名は複数形という規約を理解した。
- [ ] `php artisan make:model`コマンドで、モデルを生成できる。
