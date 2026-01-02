# Tutorial 9-5-3: Eager Loadingとレイジーローディング

## 🎯 このセクションで学ぶこと

*   Eager LoadingとLazy Loadingの違いを理解する。
*   N+1問題を深く理解し、解決できるようになる。
*   `with()`、`load()`、`loadMissing()`を使い分けられるようになる。

---

## 導入：「遅延読み込み」vs「事前読み込み」

Eloquentでは、リレーションシップを持つデータを取得する方法が2つあります。

1. **Lazy Loading（遅延読み込み）**: 必要になったときに、リレーションシップを読み込む
2. **Eager Loading（事前読み込み）**: 最初から、リレーションシップを読み込む

どちらも同じ結果になりますが、**パフォーマンスに大きな違い**があります。

このセクションでは、Eager LoadingとLazy Loadingの違いを理解し、N+1問題を解決する方法を学びます。

---

## 詳細解説

### 🐌 Lazy Loading（遅延読み込み）

Lazy Loadingとは、**リレーションシップに初めてアクセスしたときに、データを読み込む方法**です。

#### 例

```php
$posts = Post::all();

foreach ($posts as $post) {
    echo $post->user->name; // ここで初めてユーザーを読み込む
}
```

**実行されるSQL**

```sql
-- 投稿を全て取得
SELECT * FROM posts;

-- 各投稿のユーザーを取得（投稿の数だけSQLが実行される）
SELECT * FROM users WHERE id = 1;
SELECT * FROM users WHERE id = 1;
SELECT * FROM users WHERE id = 2;
...
```

もし、投稿が100件あれば、**101回のSQLクエリが実行されます**。

---

### 🚨 N+1問題とは？

N+1問題とは、**Lazy Loadingによって、大量のSQLクエリが実行される問題**です。

*   **1回目**: 親レコード（投稿）を取得
*   **N回**: 各親レコードの子レコード（ユーザー）を取得

この問題は、**パフォーマンスを大幅に低下させます**。

---

### ⚡ Eager Loading（事前読み込み）

Eager Loadingとは、**最初から、リレーションシップを読み込む方法**です。

#### 例

```php
$posts = Post::with('user')->get();

foreach ($posts as $post) {
    echo $post->user->name; // SQLは実行されない
}
```

**実行されるSQL**

```sql
-- 投稿を全て取得
SELECT * FROM posts;

-- 全てのユーザーを一度に取得
SELECT * FROM users WHERE id IN (1, 2, 3, ...);
```

これにより、**2回のSQLクエリで全てのデータを取得できます**。

---

### 🔍 複数のリレーションシップを読み込む

```php
$posts = Post::with(['user', 'comments', 'tags'])->get();
```

**実行されるSQL**

```sql
SELECT * FROM posts;
SELECT * FROM users WHERE id IN (1, 2, 3, ...);
SELECT * FROM comments WHERE post_id IN (1, 2, 3, ...);
SELECT * FROM tags INNER JOIN post_tag ON tags.id = post_tag.tag_id WHERE post_tag.post_id IN (1, 2, 3, ...);
```

---

### 🔍 ネストしたリレーションシップを読み込む

```php
$posts = Post::with('comments.user')->get();

foreach ($posts as $post) {
    foreach ($post->comments as $comment) {
        echo $comment->user->name;
    }
}
```

**実行されるSQL**

```sql
SELECT * FROM posts;
SELECT * FROM comments WHERE post_id IN (1, 2, 3, ...);
SELECT * FROM users WHERE id IN (1, 2, 3, ...);
```

---

### 🎯 条件付きEager Loading

#### 公開済みのコメントのみを読み込む

```php
$posts = Post::with(['comments' => function ($query) {
    $query->where('is_approved', true);
}])->get();
```

#### 最新の5件のコメントのみを読み込む

```php
$posts = Post::with(['comments' => function ($query) {
    $query->latest()->take(5);
}])->get();
```

---

### 🔄 Lazy Eager Loading

すでに取得したモデルに対して、後からリレーションシップを読み込むこともできます。

#### `load()`を使った読み込み

```php
$posts = Post::all();

// 後からユーザーを読み込む
$posts->load('user');

foreach ($posts as $post) {
    echo $post->user->name;
}
```

---

### 💡 TIP: `loadMissing()`

`loadMissing()`を使うと、まだ読み込まれていないリレーションシップのみを読み込みます。

```php
$posts = Post::with('user')->get();

// userは既に読み込まれているため、再度読み込まれない
// commentsのみが読み込まれる
$posts->loadMissing(['user', 'comments']);
```

---

### 🔍 リレーションシップのカウント

#### `withCount()`を使ったカウント

```php
$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->title . ': ' . $post->comments_count . '件のコメント';
}
```

**実行されるSQL**

```sql
SELECT posts.*, (SELECT COUNT(*) FROM comments WHERE posts.id = comments.post_id) AS comments_count FROM posts;
```

---

### 🚀 実践例：ブログの投稿一覧

#### パフォーマンスの悪い例（Lazy Loading）

```php
public function index()
{
    $posts = Post::all(); // NG

    return view('posts.index', compact('posts'));
}
```

**Bladeテンプレート**

```blade
@foreach($posts as $post)
    <div class="post">
        <h2>{{ $post->title }}</h2>
        <p>投稿者: {{ $post->user->name }}</p> <!-- ここでN+1問題が発生 -->
        <p>コメント数: {{ $post->comments->count() }}</p> <!-- ここでもN+1問題が発生 -->
    </div>
@endforeach
```

#### パフォーマンスの良い例（Eager Loading）

```php
public function index()
{
    $posts = Post::with('user')
                 ->withCount('comments')
                 ->get(); // OK

    return view('posts.index', compact('posts'));
}
```

**Bladeテンプレート**

```blade
@foreach($posts as $post)
    <div class="post">
        <h2>{{ $post->title }}</h2>
        <p>投稿者: {{ $post->user->name }}</p> <!-- SQLは実行されない -->
        <p>コメント数: {{ $post->comments_count }}</p> <!-- SQLは実行されない -->
    </div>
@endforeach
```

---

### 🔍 デフォルトでEager Loadingを設定

モデルで、デフォルトで読み込むリレーションシップを設定できます。

**`app/Models/Post.php`**

```php
class Post extends Model
{
    protected $with = ['user'];
}
```

これにより、`Post::all()`を実行すると、自動的に`user`が読み込まれます。

#### デフォルトのEager Loadingを無効にする

```php
$posts = Post::without('user')->get();
```

---

### 💡 TIP: `loadCount()`

すでに取得したモデルに対して、後からリレーションシップのカウントを読み込むこともできます。

```php
$posts = Post::all();

// 後からコメント数を読み込む
$posts->loadCount('comments');

foreach ($posts as $post) {
    echo $post->comments_count;
}
```

---

### 🔍 N+1問題を検出する

Laravel Debugbarを使うことで、N+1問題を検出できます。

#### インストール

```bash
composer require barryvdh/laravel-debugbar --dev
```

#### 使い方

ブラウザで画面を開くと、画面下部にデバッグバーが表示されます。「Queries」タブをクリックすると、実行されたSQLクエリの数が表示されます。

---

### 🚨 よくある間違い

#### 間違い1: Eager Loadingを使わずにループ内でリレーションシップにアクセス

```php
$posts = Post::all(); // NG

foreach ($posts as $post) {
    echo $post->user->name; // N+1問題が発生
}
```

**対処法**: `with()`を使います。

```php
$posts = Post::with('user')->get(); // OK
```

#### 間違い2: `with()`と`withCount()`を混同する

```php
$posts = Post::with('comments')->get();

foreach ($posts as $post) {
    echo $post->comments->count(); // これはコレクションのcount()
}
```

**対処法**: `withCount()`を使います。

```php
$posts = Post::withCount('comments')->get();

foreach ($posts as $post) {
    echo $post->comments_count; // これはSQLのCOUNT()
}
```

---

## ✨ まとめ

このセクションでは、Eager LoadingとLazy Loadingの違いを学びました。

*   Lazy Loadingは、必要になったときに、リレーションシップを読み込む方法である。
*   Eager Loadingは、最初から、リレーションシップを読み込む方法である。
*   N+1問題とは、Lazy Loadingによって、大量のSQLクエリが実行される問題である。
*   `with()`を使って、Eager Loadingを実装することで、N+1問題を解決できる。
*   `load()`や`loadMissing()`を使って、後からリレーションシップを読み込むこともできる。
*   `withCount()`を使って、リレーションシップのカウントを効率的に取得できる。

次のセクションでは、リレーションシップのクエリについて学びます。

---
