# Tutorial 9-5-3: 1対多のリレーションシップ（hasMany、belongsTo）

## 🎯 このセクションで学ぶこと

*   Tutorial 8で学んだ1対多のリレーションシップを、Laravelで実装できるようになる。
*   `hasMany()`と`belongsTo()`を使って、リレーションシップを定義できるようになる。
*   Eloquentを使って、リレーションシップを持つデータを簡単に取得できるようになる。

---

## 導入：「あの面倒なJOIN」が、こんなに簡単に

Tutorial 8では、SQLで1対多のリレーションシップを実装し、JOINを使ってデータを取得しました。

```sql
SELECT posts.*, users.name 
FROM posts 
INNER JOIN users ON posts.user_id = users.id;
```

しかし、Laravelでは、**もっと簡単にリレーションシップを実装できます**。

```php
$posts = Post::with('user')->get();

foreach ($posts as $post) {
    echo $post->user->name; // ユーザー名を取得
}
```

このセクションでは、Tutorial 8で学んだ1対多のリレーションシップを、Laravelで実装する方法を学びます。

---

## 詳細解説

### 🔗 1対多のリレーションシップとは？

1対多のリレーションシップとは、**1つのレコードが、複数のレコードと関連する関係**です。

**例**

*   1人のユーザーが、複数の投稿を持つ
*   1つのカテゴリーが、複数の商品を持つ
*   1つの会社が、複数の従業員を持つ

---

### 📝 テーブル設計の復習

Tutorial 8で学んだように、1対多のリレーションシップを実装するには、**外部キー**を使います。

**テーブル構成**

```
users テーブル
+----+----------+
| id | name     |
+----+----------+
| 1  | 山田太郎 |
| 2  | 佐藤花子 |
+----+----------+

posts テーブル
+----+-----------+---------+
| id | title     | user_id |
+----+-----------+---------+
| 1  | 記事1     | 1       |
| 2  | 記事2     | 1       |
| 3  | 記事3     | 2       |
+----+-----------+---------+
```

`posts`テーブルの`user_id`が、`users`テーブルの`id`を参照しています。

---

### 🔗 Laravelでのリレーションシップ定義

Laravelでは、モデルにリレーションシップメソッドを定義することで、リレーションシップを実装します。

#### `hasMany()`: 1つのレコードが複数のレコードを持つ

**`app/Models/User.php`**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}
```

**コードリーディング**

*   `hasMany(Post::class)`: このユーザーは、複数の投稿を持つ
*   メソッド名は、複数形（`posts`）にするのが慣例

#### `belongsTo()`: 1つのレコードが別のレコードに属する

**`app/Models/Post.php`**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

**コードリーディング**

*   `belongsTo(User::class)`: この投稿は、1人のユーザーに属する
*   メソッド名は、単数形（`user`）にするのが慣例

---

### 🚀 実践例：リレーションシップを使ったデータ取得

#### 例1: ユーザーの全ての投稿を取得

```php
$user = User::find(1);
$posts = $user->posts;

foreach ($posts as $post) {
    echo $post->title;
}
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM posts WHERE user_id = 1;
```

#### 例2: 投稿の作成者を取得

```php
$post = Post::find(1);
$user = $post->user;

echo $user->name;
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM users WHERE id = (SELECT user_id FROM posts WHERE id = 1);
```

---

### 💡 TIP: リレーションシップはプロパティとしてアクセスできる

```php
$user = User::find(1);

// メソッドとしてアクセス（クエリビルダーが返される）
$posts = $user->posts()->where('is_published', true)->get();

// プロパティとしてアクセス（コレクションが返される）
$posts = $user->posts;
```

**違い**

*   `$user->posts()`: クエリビルダーが返される（追加の条件を付けられる）
*   `$user->posts`: コレクションが返される（すぐに結果が取得される）

---

### 🔍 外部キーのカスタマイズ

Laravelは、デフォルトで以下の規則に従って外部キーを推測します。

*   `hasMany()`: `{モデル名の小文字}_id`（例: `user_id`）
*   `belongsTo()`: `{メソッド名}_id`（例: `user_id`）

もし、外部キーの名前が異なる場合は、第2引数で指定できます。

```php
public function posts()
{
    return $this->hasMany(Post::class, 'author_id');
}
```

```php
public function user()
{
    return $this->belongsTo(User::class, 'author_id');
}
```

---

### 🚀 実践例：投稿の作成

#### 例1: `save()`を使った作成

```php
$user = User::find(1);

$post = new Post();
$post->title = '新しい記事';
$post->content = '記事の内容';

$user->posts()->save($post);
```

これは、以下のSQLと同じです。

```sql
INSERT INTO posts (title, content, user_id) VALUES ('新しい記事', '記事の内容', 1);
```

#### 例2: `create()`を使った作成

```php
$user = User::find(1);

$post = $user->posts()->create([
    'title' => '新しい記事',
    'content' => '記事の内容',
]);
```

これも、以下のSQLと同じです。

```sql
INSERT INTO posts (title, content, user_id) VALUES ('新しい記事', '記事の内容', 1);
```

**重要なポイント**

*   `user_id`は自動的に設定されます。

---

### 🔍 リレーションシップの存在チェック

#### 投稿を持つユーザーのみを取得

```php
$users = User::has('posts')->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM users WHERE EXISTS (SELECT * FROM posts WHERE users.id = posts.user_id);
```

#### 投稿が3件以上のユーザーのみを取得

```php
$users = User::has('posts', '>=', 3)->get();
```

#### 公開済みの投稿を持つユーザーのみを取得

```php
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true);
})->get();
```

---

### 🚀 実践例：コントローラーでの使用

#### ユーザーの投稿一覧を表示

```php
public function show($id)
{
    $user = User::findOrFail($id);
    $posts = $user->posts;

    return view('users.show', compact('user', 'posts'));
}
```

**Bladeテンプレート**

```blade
<h1>{{ $user->name }}の投稿一覧</h1>

@foreach($posts as $post)
    <div>
        <h2>{{ $post->title }}</h2>
        <p>{{ $post->content }}</p>
    </div>
@endforeach
```

---

### 🔍 リレーションシップのカウント

#### ユーザーごとの投稿数を取得

```php
$users = User::withCount('posts')->get();

foreach ($users as $user) {
    echo $user->name . ': ' . $user->posts_count . '件';
}
```

これは、以下のSQLと同じです。

```sql
SELECT users.*, (SELECT COUNT(*) FROM posts WHERE users.id = posts.user_id) AS posts_count FROM users;
```

---

### 💡 TIP: リレーションシップの削除

#### ユーザーを削除する際に、関連する投稿も削除する

**`app/Models/User.php`**

```php
protected static function booted()
{
    static::deleting(function ($user) {
        $user->posts()->delete();
    });
}
```

または、マイグレーションで`onDelete('cascade')`を設定します。

```php
$table->foreignId('user_id')
      ->constrained()
      ->onDelete('cascade');
```

---

### 🚨 よくある間違い

#### 間違い1: リレーションシップメソッドを定義していない

```php
$user = User::find(1);
$posts = $user->posts; // エラー
```

**エラー**

```
Undefined property: App\Models\User::$posts
```

**対処法**: モデルに`posts()`メソッドを定義します。

#### 間違い2: 外部キーが間違っている

```php
public function posts()
{
    return $this->hasMany(Post::class);
}
```

もし、`posts`テーブルの外部キーが`author_id`の場合、以下のように修正します。

```php
public function posts()
{
    return $this->hasMany(Post::class, 'author_id');
}
```

---

## ✨ まとめ

このセクションでは、Tutorial 8で学んだ1対多のリレーションシップを、Laravelで実装する方法を学びました。

*   `hasMany()`を使って、1つのレコードが複数のレコードを持つリレーションシップを定義できる。
*   `belongsTo()`を使って、1つのレコードが別のレコードに属するリレーションシップを定義できる。
*   `$user->posts`のように、プロパティとしてアクセスすることで、関連するデータを取得できる。
*   `save()`や`create()`を使って、リレーションシップを持つデータを作成できる。
*   `has()`や`whereHas()`を使って、リレーションシップの存在チェックができる。

次のセクションでは、リレーションシップを使ったデータ取得について、さらに詳しく学びます。

---

## 📝 学習のポイント

- [ ] `hasMany()`と`belongsTo()`の違いを理解し、使い分けられる。
- [ ] リレーションシップメソッドを定義できる。
- [ ] `$user->posts`のように、プロパティとしてアクセスできる。
- [ ] `save()`や`create()`を使って、リレーションシップを持つデータを作成できる。
- [ ] `has()`や`whereHas()`を使って、リレーションシップの存在チェックができる。
