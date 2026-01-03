# Tutorial 9-5-1: 1対多のリレーションシップ（hasMany、belongsTo）

## 🎯 このセクションで学ぶこと

- Tutorial 8で学んだ1対多のリレーションシップを、Laravelで実装できるようになる
- `hasMany()`と`belongsTo()`を使って、リレーションシップを定義できるようになる
- Eloquentを使って、リレーションシップを持つデータを簡単に取得できるようになる
- N+1問題を理解し、Eager Loadingで解決できるようになる

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

- 1人のユーザーが、複数の投稿を持つ
- 1つのカテゴリーが、複数の商品を持つ
- 1つの会社が、複数の従業員を持つ

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

### 🏗️ マイグレーションで外部キーを定義する

まず、`posts`テーブルに`user_id`カラムを追加します。

**`database/migrations/xxxx_create_posts_table.php`**

```php
public function up(): void
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->string('title');
        $table->text('content');
        $table->timestamps();
    });
}
```

**コードリーディング**

- `foreignId('user_id')` → `user_id`カラムを作成します
- `->constrained()` → 外部キー制約を自動的に設定します（`users`テーブルの`id`を参照）
- `->onDelete('cascade')` → ユーザーが削除されたら、その投稿も一緒に削除されます

マイグレーションを実行します。

```bash
sail artisan migrate
```

---

### 🔗 Laravelでのリレーションシップ定義

Laravelでは、モデルにリレーションシップメソッドを定義することで、リレーションシップを実装します。

#### `hasMany()`: 1つのレコードが複数のレコードを持つ

**`app/Models/User.php`**

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable
{
    /**
     * このユーザーが持つ投稿
     */
    public function posts()
    {
        return $this->hasMany(Post::class);
    }
}
```

**コードリーディング**

- `public function posts()` → メソッド名は、複数形（`posts`）にするのが慣例
- `return $this->hasMany(Post::class)` → 「このユーザーは複数の`Post`を持つ」という関係を定義
- Laravelは、`Post`モデルの`user_id`カラムを自動的に推測します

#### `belongsTo()`: 1つのレコードが別のレコードに属する

**`app/Models/Post.php`**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    /**
     * この投稿が属するユーザー
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

**コードリーディング**

- `public function user()` → メソッド名は、単数形（`user`）にするのが慣例
- `return $this->belongsTo(User::class)` → 「この投稿は1人の`User`に属する」という関係を定義

---

### 🔍 リレーションシップを使ったデータ取得

リレーションシップを定義すると、以下のように関連データを取得できます。

#### 1. ユーザーの全ての投稿を取得

```php
$user = User::find(1);
$posts = $user->posts; // このユーザーの全ての投稿を取得

foreach ($posts as $post) {
    echo $post->title;
}
```

**実行されるSQL**

```sql
-- ユーザーを取得
SELECT * FROM users WHERE id = 1;

-- 投稿を取得
SELECT * FROM posts WHERE user_id = 1;
```

**Bladeでの表示**

```blade
<h2>{{ $user->name }}の投稿一覧</h2>
<ul>
    @foreach ($user->posts as $post)
        <li>{{ $post->title }}</li>
    @endforeach
</ul>
```

#### 2. 投稿の作成者を取得

```php
$post = Post::find(1);
$user = $post->user; // この投稿の作成者を取得

echo $user->name;
```

**Bladeでの表示**

```blade
<h2>{{ $post->title }}</h2>
<p>作成者: {{ $post->user->name }}</p>
```

---

### 💡 TIP: リレーションシップはプロパティとしてもメソッドとしてもアクセスできる

```php
$user = User::find(1);

// メソッドとしてアクセス（クエリビルダーが返される）
$posts = $user->posts()->where('is_published', true)->get();

// プロパティとしてアクセス（コレクションが返される）
$posts = $user->posts;
```

**違い**

| アクセス方法 | 戻り値 | 用途 |
|-------------|--------|------|
| `$user->posts()` | クエリビルダー | 追加の条件を付けたい場合 |
| `$user->posts` | コレクション | すぐに結果を取得したい場合 |

---

### 🚀 リレーションシップを使ったデータ作成

リレーションシップを使って、関連データを作成することもできます。

#### 例1: `save()`を使った作成

```php
$user = User::find(1);

$post = new Post();
$post->title = '新しい記事';
$post->content = '記事の内容';

$user->posts()->save($post);
```

#### 例2: `create()`を使った作成

```php
$user = User::find(1);

$post = $user->posts()->create([
    'title' => '新しい記事',
    'content' => '記事の内容',
]);
```

> **💡 ポイント**: `user_id`は自動的に設定されます。手動で設定する必要はありません。

---

### 🚨 N+1問題とは？

N+1問題とは、**リレーションシップを持つデータを取得する際に、大量のSQLクエリが実行される問題**です。これは、Laravelを使う上で最も注意すべきパフォーマンス問題の1つです。

#### 問題のあるコード

```php
$posts = Post::all();

foreach ($posts as $post) {
    echo $post->user->name; // ここで毎回SQLが実行される
}
```

**実行されるSQL**

```sql
-- 1回目: 投稿を全て取得
SELECT * FROM posts;

-- 2回目以降: 各投稿のユーザーを取得（投稿の数だけSQLが実行される）
SELECT * FROM users WHERE id = 1;
SELECT * FROM users WHERE id = 1;
SELECT * FROM users WHERE id = 2;
...
```

もし、投稿が100件あれば、**101回のSQLクエリが実行されます**（1回目で投稿を取得、残り100回で各投稿のユーザーを取得）。これが**N+1問題**です。

---

### ⚡ Eager Loadingで解決する

Eager Loading（事前読み込み）を使うことで、N+1問題を解決できます。

#### `with()`を使った解決

```php
$posts = Post::with('user')->get(); // 2回のクエリで全てのデータを取得

foreach ($posts as $post) {
    echo $post->user->name; // 追加のSQLは実行されない
}
```

**実行されるSQL**

```sql
-- 1回目: 投稿を全て取得
SELECT * FROM posts;

-- 2回目: 全てのユーザーを一度に取得
SELECT * FROM users WHERE id IN (1, 2, 3, ...);
```

投稿が100件あっても、**合計2回のSQLクエリで済みます**。

> **💡 ポイント**: `with('user')`は、リレーションシップのメソッド名（`user()`）を文字列で指定します。

#### 複数のリレーションシップを読み込む

```php
$posts = Post::with(['user', 'comments'])->get();

foreach ($posts as $post) {
    echo $post->user->name;
    echo $post->comments->count() . '件のコメント';
}
```

#### ネストしたリレーションシップを読み込む

```php
$posts = Post::with('comments.user')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->user->name;
    }
}
```

---

### 🎯 条件付きEager Loading

リレーションシップに条件を付けることもできます。

#### 公開済みの投稿のみを読み込む

```php
$users = User::with(['posts' => function ($query) {
    $query->where('is_published', true);
}])->get();

foreach ($users as $user) {
    foreach ($user->posts as $post) {
        echo $post->title;
    }
}
```

---

### 🔍 リレーションシップの存在チェック

#### 投稿を持つユーザーのみを取得

```php
$users = User::has('posts')->get();
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

### 🔢 リレーションシップのカウント

#### ユーザーごとの投稿数を取得

```php
$users = User::withCount('posts')->get();

foreach ($users as $user) {
    echo $user->name . ': ' . $user->posts_count . '件';
}
```

---

### 🚀 実践例：ブログの投稿一覧

#### コントローラー

```php
public function index()
{
    $posts = Post::with('user')
                 ->where('is_published', true)
                 ->orderBy('created_at', 'desc')
                 ->paginate(10);

    return view('posts.index', compact('posts'));
}
```

#### Bladeテンプレート

```blade
@foreach($posts as $post)
    <div class="post">
        <h2>{{ $post->title }}</h2>
        <p>投稿者: {{ $post->user->name }}</p>
        <p>{{ Str::limit($post->content, 100) }}</p>
    </div>
@endforeach

{{ $posts->links() }}
```

---

### 🔍 外部キーのカスタマイズ

Laravelは、デフォルトで以下の規則に従って外部キーを推測します。

- `hasMany()`: `{モデル名の小文字}_id`（例: `user_id`）
- `belongsTo()`: `{メソッド名}_id`（例: `user_id`）

もし、外部キーの名前が異なる場合は、第2引数で指定できます。

```php
// postsテーブルの外部キーがauthor_idの場合
public function posts()
{
    return $this->hasMany(Post::class, 'author_id');
}

public function user()
{
    return $this->belongsTo(User::class, 'author_id');
}
```

---

### 🚨 よくある間違い

#### 間違い1: `with()`を使わずにループ内でリレーションシップにアクセス

```php
// NG: N+1問題が発生
$posts = Post::all();

foreach ($posts as $post) {
    echo $post->user->name;
}
```

**対処法**: `with()`を使います。

```php
// OK: 2回のクエリで済む
$posts = Post::with('user')->get();
```

#### 間違い2: リレーションシップメソッドを定義していない

```php
$user = User::find(1);
$posts = $user->posts; // エラー: Undefined property
```

**対処法**: モデルに`posts()`メソッドを定義します。

---

## ✨ まとめ

このセクションでは、Tutorial 8で学んだ1対多のリレーションシップを、Laravelで実装する方法を学びました。

| 概念 | 説明 |
|------|------|
| `hasMany()` | 1つのレコードが複数のレコードを持つ（User → Posts） |
| `belongsTo()` | 1つのレコードが別のレコードに属する（Post → User） |
| Eager Loading | `with()`を使って、N+1問題を解決する |
| `has()` / `whereHas()` | リレーションシップの存在チェック |
| `withCount()` | リレーションシップのカウントを取得 |

次のセクションでは、多対多のリレーションシップについて学びます。

---
