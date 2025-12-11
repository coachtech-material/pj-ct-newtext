# Tutorial 9-5-1: 1対多のリレーションシップ

## 🎯 このセクションで学ぶこと

*   Eloquentで1対多のリレーションシップを定義できるようになる。
*   `hasMany()`と`belongsTo()`メソッドを使って、関連データを取得できるようになる。
*   リレーションシップを使った効率的なデータ取得（Eager Loading）を理解する。

---

## 導入：Tutorial 8で学んだリレーションシップをEloquentで実装する

Tutorial 8で、SQLを使って1対多のリレーションシップを学びました。例えば、「1人のユーザーは複数の投稿を持つ」という関係を、外部キー（`user_id`）を使って表現しました。

```sql
-- ユーザーテーブル
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255)
);

-- 投稿テーブル（user_idで外部キー制約）
CREATE TABLE posts (
    id BIGINT PRIMARY KEY,
    user_id BIGINT,
    title VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

そして、JOINを使って、ユーザーとその投稿を一緒に取得しました。

```sql
SELECT users.name, posts.title
FROM users
INNER JOIN posts ON users.id = posts.user_id;
```

Eloquent ORMでは、このような「リレーションシップ」をPHPのメソッドとして定義することで、**SQLを書かずに関連データを取得できる**ようになります。

---

## 詳細解説

### 🏗️ 1対多のリレーションシップの定義

1対多のリレーションシップは、以下の2つのメソッドで定義します。

*   **`hasMany()`**: 「1」側のモデル（User）に定義する。「このユーザーは複数の投稿を持つ」という意味。
*   **`belongsTo()`**: 「多」側のモデル（Post）に定義する。「この投稿は1人のユーザーに属する」という意味。

#### ステップ1: マイグレーションで外部キーを定義する

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

*   `foreignId('user_id')`: `user_id`カラムを作成します。
*   `->constrained()`: 外部キー制約を自動的に設定します（`users`テーブルの`id`を参照）。
*   `->onDelete('cascade')`: ユーザーが削除されたら、その投稿も一緒に削除されます。

マイグレーションを実行します。

```bash
docker compose exec php php artisan migrate
```

#### ステップ2: `User`モデルに`hasMany()`を定義する

`app/Models/User.php`に、以下のメソッドを追加します。

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

*   `public function posts()`: メソッド名は、通常「複数形」にします（`posts`）。
*   `return $this->hasMany(Post::class)`: 「このユーザーは複数の`Post`を持つ」という関係を定義します。
*   Laravelは、`Post`モデルの`user_id`カラムを自動的に推測します。

#### ステップ3: `Post`モデルに`belongsTo()`を定義する

`app/Models/Post.php`に、以下のメソッドを追加します。

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

*   `public function user()`: メソッド名は、通常「単数形」にします（`user`）。
*   `return $this->belongsTo(User::class)`: 「この投稿は1人の`User`に属する」という関係を定義します。

---

### 🔍 リレーションシップを使ったデータ取得

リレーションシップを定義すると、以下のように関連データを取得できます。

#### 1. ユーザーの投稿を取得する

```php
$user = User::find(1);
$posts = $user->posts; // このユーザーの全ての投稿を取得
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

#### 2. 投稿の作成者を取得する

```php
$post = Post::find(1);
$user = $post->user; // この投稿の作成者を取得
```

**Bladeでの表示**

```blade
<h2>{{ $post->title }}</h2>
<p>作成者: {{ $post->user->name }}</p>
```

---

### ⚡ N+1問題とEager Loading

リレーションシップを使う際に、**N+1問題**という重大なパフォーマンス問題が発生することがあります。

#### N+1問題とは？

以下のコードを見てください。

```php
$posts = Post::all(); // 1回のクエリで全ての投稿を取得

foreach ($posts as $post) {
    echo $post->user->name; // 投稿ごとにユーザーを取得（N回のクエリ）
}
```

このコードは、以下のようなSQLを実行します。

```sql
-- 1回目: 全ての投稿を取得
SELECT * FROM posts;

-- 2回目以降: 投稿ごとにユーザーを取得（投稿が100件なら100回実行される）
SELECT * FROM users WHERE id = 1;
SELECT * FROM users WHERE id = 2;
SELECT * FROM users WHERE id = 3;
...
```

投稿が100件あれば、合計101回のクエリが実行されます。これが**N+1問題**です。

#### Eager Loadingで解決する

Eager Loading（事前読み込み）を使うことで、N+1問題を解決できます。

```php
$posts = Post::with('user')->get(); // 2回のクエリで全てのデータを取得

foreach ($posts as $post) {
    echo $post->user->name; // 追加のクエリは発生しない
}
```

このコードは、以下のようなSQLを実行します。

```sql
-- 1回目: 全ての投稿を取得
SELECT * FROM posts;

-- 2回目: 全てのユーザーを一度に取得
SELECT * FROM users WHERE id IN (1, 2, 3, ...);
```

投稿が100件あっても、合計2回のクエリで済みます。

**重要なポイント**

*   `with('user')`は、リレーションシップのメソッド名（`user()`）を文字列で指定します。
*   複数のリレーションシップを読み込む場合は、`with(['user', 'comments'])`のように配列で指定します。

---

### 🔢 リレーションシップの条件付き取得

リレーションシップに条件を付けることもできます。

#### 例：公開済みの投稿だけを取得する

```php
public function publishedPosts()
{
    return $this->hasMany(Post::class)->where('is_published', true);
}
```

```php
$user = User::find(1);
$publishedPosts = $user->publishedPosts; // 公開済みの投稿だけを取得
```

---

### 📝 リレーションシップを使ったデータ作成

リレーションシップを使って、関連データを作成することもできます。

#### 例：ユーザーに紐付いた投稿を作成する

```php
$user = User::find(1);

$post = $user->posts()->create([
    'title' => '新しい投稿',
    'content' => '投稿の内容',
]);
```

`posts()->create()`は、自動的に`user_id`を設定してくれます。

---

## 💡 TIP: リレーションシップのメソッド名の慣例

リレーションシップのメソッド名は、以下の慣例に従うと分かりやすいです。

*   **`hasMany()`**: 複数形（`posts`, `comments`）
*   **`belongsTo()`**: 単数形（`user`, `category`）

この慣例に従うことで、コードが読みやすくなります。

---

## ✨ まとめ

このセクションでは、Eloquentで1対多のリレーションシップを定義し、関連データを取得する方法を学びました。

*   1対多のリレーションシップは、`hasMany()`（1側）と`belongsTo()`（多側）で定義する。
*   `$user->posts`のように、プロパティとしてアクセスすることで、関連データを取得できる。
*   N+1問題を避けるために、`with()`を使ってEager Loadingを行う。
*   リレーションシップを使って、関連データを作成することもできる。

次のセクションでは、多対多のリレーションシップを学び、中間テーブル（ピボットテーブル）の扱い方を理解します。

---

## 📝 学習のポイント

- [ ] `hasMany()`と`belongsTo()`を使って、1対多のリレーションシップを定義できる。
- [ ] `$user->posts`のように、関連データをプロパティとしてアクセスできる。
- [ ] N+1問題を理解し、`with()`を使ってEager Loadingを行える。
- [ ] リレーションシップを使って、関連データを作成できる。
