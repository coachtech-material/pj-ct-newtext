# Tutorial 9-5-8: ポリモーフィックリレーションシップ

## 🎯 このセクションで学ぶこと

*   ポリモーフィックリレーションシップの概念を理解する。
*   `morphTo()`と`morphMany()`を使って、柔軟なリレーションシップを定義できるようになる。
*   実践的なユースケースを理解する。

---

## 導入：「複数のテーブル」に対するリレーションシップ

これまで学んだリレーションシップは、**特定のテーブル**に対するものでした。例えば、投稿は必ずユーザーに属し、コメントは必ず投稿に属します。

しかし、実際のアプリケーション開発では、**複数のテーブルに対してリレーションシップを持ちたい**ことがあります。

**例：コメント機能**

*   投稿に対するコメント
*   動画に対するコメント
*   写真に対するコメント

このような場合、ポリモーフィックリレーションシップを使うことで、**1つのcommentsテーブルで全てのコメントを管理**できます。

---

## 詳細解説

### 🔗 ポリモーフィックリレーションシップとは？

ポリモーフィックリレーションシップとは、**1つのモデルが、複数の異なるモデルに属することができるリレーションシップ**です。

**例**

*   コメントは、投稿、動画、写真のいずれかに属する
*   画像は、ユーザー、投稿、商品のいずれかに属する
*   タグは、投稿、動画、写真のいずれかに属する

---

### 📝 テーブル設計

#### 例：コメント機能

**テーブル構成**

```
posts テーブル
+----+----------+
| id | title    |
+----+----------+
| 1  | 記事1    |
| 2  | 記事2    |
+----+----------+

videos テーブル
+----+----------+
| id | title    |
+----+----------+
| 1  | 動画1    |
| 2  | 動画2    |
+----+----------+

comments テーブル
+----+----------------+------------------+---------+
| id | commentable_id | commentable_type | content |
+----+----------------+------------------+---------+
| 1  | 1              | App\Models\Post  | コメント1 |
| 2  | 1              | App\Models\Post  | コメント2 |
| 3  | 1              | App\Models\Video | コメント3 |
+----+----------------+------------------+---------+
```

**重要なポイント**

*   `commentable_id`: 親レコードのID
*   `commentable_type`: 親モデルのクラス名（`App\Models\Post`、`App\Models\Video`など）

---

### 🔧 マイグレーションの作成

```bash
php artisan make:migration create_comments_table
```

**マイグレーションファイル**

```php
public function up()
{
    Schema::create('comments', function (Blueprint $table) {
        $table->id();
        $table->morphs('commentable'); // commentable_id と commentable_type を自動生成
        $table->text('content');
        $table->timestamps();
    });
}
```

**`morphs()`の展開**

```php
$table->unsignedBigInteger('commentable_id');
$table->string('commentable_type');
$table->index(['commentable_id', 'commentable_type']);
```

---

### 🔗 Laravelでのリレーションシップ定義

#### `morphTo()`: 親モデルを取得

**`app/Models/Comment.php`**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    protected $fillable = ['content'];

    public function commentable()
    {
        return $this->morphTo();
    }
}
```

#### `morphMany()`: 子モデルを取得

**`app/Models/Post.php`**

```php
public function comments()
{
    return $this->morphMany(Comment::class, 'commentable');
}
```

**`app/Models/Video.php`**

```php
public function comments()
{
    return $this->morphMany(Comment::class, 'commentable');
}
```

---

### 🚀 実践例：データの取得

#### 投稿のコメントを取得

```php
$post = Post::find(1);
$comments = $post->comments;

foreach ($comments as $comment) {
    echo $comment->content;
}
```

#### コメントの親モデルを取得

```php
$comment = Comment::find(1);
$commentable = $comment->commentable;

if ($commentable instanceof Post) {
    echo '投稿: ' . $commentable->title;
} elseif ($commentable instanceof Video) {
    echo '動画: ' . $commentable->title;
}
```

---

### 🚀 実践例：データの作成

#### 投稿にコメントを追加

```php
$post = Post::find(1);

$comment = $post->comments()->create([
    'content' => '素晴らしい記事ですね！',
]);
```

**実行されるSQL**

```sql
INSERT INTO comments (commentable_id, commentable_type, content) 
VALUES (1, 'App\Models\Post', '素晴らしい記事ですね！');
```

---

### 🔍 Eager Loading

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->content;
    }
}
```

---

### 🔍 ポリモーフィックリレーションシップのクエリ

#### コメントを持つ投稿のみを取得

```php
$posts = Post::has('comments')->get();
```

#### 特定の内容を含むコメントを持つ投稿を取得

```php
$posts = Post::whereHas('comments', function ($query) {
    $query->where('content', 'like', '%素晴らしい%');
})->get();
```

---

### 🚀 実践例：画像機能

#### テーブル設計

```
users テーブル
+----+----------+
| id | name     |
+----+----------+

posts テーブル
+----+----------+
| id | title    |
+----+----------+

images テーブル
+----+--------------+----------------+------+
| id | imageable_id | imageable_type | url  |
+----+--------------+----------------+------+
| 1  | 1            | App\Models\User| a.jpg|
| 2  | 1            | App\Models\Post| b.jpg|
+----+--------------+----------------+------+
```

#### マイグレーション

```php
Schema::create('images', function (Blueprint $table) {
    $table->id();
    $table->morphs('imageable');
    $table->string('url');
    $table->timestamps();
});
```

#### モデル

**`app/Models/Image.php`**

```php
public function imageable()
{
    return $this->morphTo();
}
```

**`app/Models/User.php`**

```php
public function images()
{
    return $this->morphMany(Image::class, 'imageable');
}
```

**`app/Models/Post.php`**

```php
public function images()
{
    return $this->morphMany(Image::class, 'imageable');
}
```

#### 使用例

```php
$user = User::find(1);
$user->images()->create(['url' => 'avatar.jpg']);

$post = Post::find(1);
$post->images()->create(['url' => 'thumbnail.jpg']);
```

---

### 🔍 ポリモーフィック多対多リレーションシップ

ポリモーフィックリレーションシップは、多対多にも対応しています。

#### 例：タグ機能

**テーブル構成**

```
posts テーブル
+----+----------+
| id | title    |
+----+----------+

videos テーブル
+----+----------+
| id | title    |
+----+----------+

tags テーブル
+----+--------+
| id | name   |
+----+--------+
| 1  | Laravel|
| 2  | PHP    |
+----+--------+

taggables テーブル（中間テーブル）
+----+---------+--------------+--------------+
| id | tag_id  | taggable_id  | taggable_type|
+----+---------+--------------+--------------+
| 1  | 1       | 1            | App\Models\Post |
| 2  | 2       | 1            | App\Models\Post |
| 3  | 1       | 1            | App\Models\Video|
+----+---------+--------------+--------------+
```

#### マイグレーション

```php
Schema::create('taggables', function (Blueprint $table) {
    $table->id();
    $table->foreignId('tag_id')->constrained()->onDelete('cascade');
    $table->morphs('taggable');
    $table->timestamps();
});
```

#### モデル

**`app/Models/Tag.php`**

```php
public function posts()
{
    return $this->morphedByMany(Post::class, 'taggable');
}

public function videos()
{
    return $this->morphedByMany(Video::class, 'taggable');
}
```

**`app/Models/Post.php`**

```php
public function tags()
{
    return $this->morphToMany(Tag::class, 'taggable');
}
```

**`app/Models/Video.php`**

```php
public function tags()
{
    return $this->morphToMany(Tag::class, 'taggable');
}
```

#### 使用例

```php
$post = Post::find(1);
$post->tags()->attach([1, 2]);

$tag = Tag::find(1);
$posts = $tag->posts;
$videos = $tag->videos;
```

---

### 💡 TIP: カスタムポリモーフィックタイプ

デフォルトでは、`commentable_type`には完全なクラス名（`App\Models\Post`）が保存されます。これを短い名前に変更できます。

**`app/Providers/AppServiceProvider.php`**

```php
use Illuminate\Database\Eloquent\Relations\Relation;

public function boot()
{
    Relation::morphMap([
        'post' => 'App\Models\Post',
        'video' => 'App\Models\Video',
    ]);
}
```

これにより、`commentable_type`には`post`や`video`が保存されます。

---

### 🚨 よくある間違い

#### 間違い1: `morphs()`を使わずに手動でカラムを定義

```php
$table->unsignedBigInteger('commentable_id');
$table->string('commentable_type');
// インデックスを忘れる
```

**対処法**: `morphs()`を使います。

```php
$table->morphs('commentable'); // OK
```

---

## ✨ まとめ

このセクションでは、ポリモーフィックリレーションシップについて学びました。

*   ポリモーフィックリレーションシップは、1つのモデルが複数の異なるモデルに属することができるリレーションシップである。
*   `morphTo()`を使って、親モデルを取得できる。
*   `morphMany()`を使って、子モデルを取得できる。
*   `morphToMany()`と`morphedByMany()`を使って、ポリモーフィック多対多リレーションシップを実装できる。

次のセクションでは、リレーションシップを使ったブログシステムの実践例を学びます。

---

## 📝 学習のポイント

- [ ] ポリモーフィックリレーションシップの概念を理解した。
- [ ] `morphTo()`と`morphMany()`を使い分けられる。
- [ ] `morphs()`を使って、マイグレーションを作成できる。
- [ ] ポリモーフィック多対多リレーションシップを実装できる。
