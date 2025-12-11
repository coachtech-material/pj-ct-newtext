# Tutorial 9-5-4: リレーションシップを使ったデータ取得（1対多）

## 🎯 このセクションで学ぶこと

*   SQLで`JOIN`を使って取得していたデータを、Eloquentのリレーションシップメソッドで簡単に取得できるようになる。
*   `with()`を使って、Eager Loadingを実装できるようになる。
*   N+1問題を理解し、解決できるようになる。

---

## 導入：「JOIN」から「リレーションシップ」へ

Tutorial 8では、複数のテーブルからデータを取得するために、`JOIN`を使いました。

```sql
SELECT posts.*, users.name 
FROM posts 
INNER JOIN users ON posts.user_id = users.id;
```

しかし、Laravelでは、リレーションシップメソッドを使うことで、**もっと直感的にデータを取得できます**。

```php
$posts = Post::with('user')->get();

foreach ($posts as $post) {
    echo $post->title . ' by ' . $post->user->name;
}
```

このセクションでは、リレーションシップを使ったデータ取得の方法を学びます。

---

## 詳細解説

### 🔍 基本的なデータ取得

#### ユーザーの全ての投稿を取得

```php
$user = User::find(1);
$posts = $user->posts;

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

---

### 🚨 N+1問題とは？

N+1問題とは、**リレーションシップを持つデータを取得する際に、大量のSQLクエリが実行される問題**です。

#### 問題のあるコード

```php
$posts = Post::all();

foreach ($posts as $post) {
    echo $post->user->name; // ここで毎回SQLが実行される
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

もし、投稿が100件あれば、**101回のSQLクエリが実行されます**（1回目で投稿を取得、残り100回で各投稿のユーザーを取得）。

---

### ✅ Eager Loadingで解決

Eager Loadingとは、**リレーションシップを持つデータを事前に読み込む仕組み**です。

#### `with()`を使った解決

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
$posts = Post::with(['user', 'comments'])->get();

foreach ($posts as $post) {
    echo $post->user->name;
    echo $post->comments->count() . '件のコメント';
}
```

**実行されるSQL**

```sql
SELECT * FROM posts;
SELECT * FROM users WHERE id IN (1, 2, 3, ...);
SELECT * FROM comments WHERE post_id IN (1, 2, 3, ...);
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

### 🔍 Lazy Eager Loading

すでに取得したモデルに対して、後からリレーションシップを読み込むこともできます。

```php
$posts = Post::all();

// 後からユーザーを読み込む
$posts->load('user');

foreach ($posts as $post) {
    echo $post->user->name;
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

### 🔍 リレーションシップのカウント

#### ユーザーごとの投稿数を表示

```php
$users = User::withCount('posts')->get();

foreach ($users as $user) {
    echo $user->name . ': ' . $user->posts_count . '件';
}
```

**実行されるSQL**

```sql
SELECT users.*, (SELECT COUNT(*) FROM posts WHERE users.id = posts.user_id) AS posts_count FROM users;
```

---

### 🚀 実践例：投稿の詳細ページ

#### コントローラー

```php
public function show($id)
{
    $post = Post::with(['user', 'comments.user'])
                ->findOrFail($id);

    return view('posts.show', compact('post'));
}
```

#### Bladeテンプレート

```blade
<h1>{{ $post->title }}</h1>
<p>投稿者: {{ $post->user->name }}</p>
<p>{{ $post->content }}</p>

<h2>コメント</h2>
@foreach($post->comments as $comment)
    <div class="comment">
        <p><strong>{{ $comment->user->name }}</strong></p>
        <p>{{ $comment->content }}</p>
    </div>
@endforeach
```

---

### 💡 TIP: `exists`と`doesntExist`

#### リレーションシップが存在するかチェック

```php
$user = User::find(1);

if ($user->posts()->exists()) {
    echo 'このユーザーは投稿を持っています';
}

if ($user->posts()->doesntExist()) {
    echo 'このユーザーは投稿を持っていません';
}
```

---

### 🔍 リレーションシップのフィルタリング

#### 公開済みの投稿のみを取得

```php
$user = User::find(1);
$publishedPosts = $user->posts()->where('is_published', true)->get();
```

#### 最新の5件の投稿を取得

```php
$user = User::find(1);
$latestPosts = $user->posts()->latest()->take(5)->get();
```

---

### 🚀 実践例：ユーザーのダッシュボード

#### コントローラー

```php
public function dashboard()
{
    $user = Auth::user();
    
    $stats = [
        'total_posts' => $user->posts()->count(),
        'published_posts' => $user->posts()->where('is_published', true)->count(),
        'draft_posts' => $user->posts()->where('is_published', false)->count(),
        'total_comments' => $user->posts()->withCount('comments')->get()->sum('comments_count'),
    ];

    $latestPosts = $user->posts()->latest()->take(5)->get();

    return view('dashboard', compact('stats', 'latestPosts'));
}
```

---

### 🚨 よくある間違い

#### 間違い1: `with()`を使わずにループ内でリレーションシップにアクセス

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

#### 間違い2: 存在しないリレーションシップを読み込もうとする

```php
$posts = Post::with('author')->get(); // エラー
```

**エラー**

```
Call to undefined relationship [author] on model [App\Models\Post].
```

**対処法**: モデルに`author()`メソッドを定義するか、正しいリレーションシップ名を使います。

---

## ✨ まとめ

このセクションでは、リレーションシップを使ったデータ取得の方法を学びました。

*   SQLで`JOIN`を使って取得していたデータを、Eloquentのリレーションシップメソッドで簡単に取得できる。
*   N+1問題とは、リレーションシップを持つデータを取得する際に、大量のSQLクエリが実行される問題である。
*   `with()`を使って、Eager Loadingを実装することで、N+1問題を解決できる。
*   `withCount()`を使って、リレーションシップのカウントを取得できる。
*   `exists()`や`doesntExist()`を使って、リレーションシップの存在チェックができる。

次のセクションでは、多対多のリレーションシップについて学びます。

---

## 📝 学習のポイント

- [ ] N+1問題を理解し、`with()`を使って解決できる。
- [ ] Eager Loadingを使って、パフォーマンスを改善できる。
- [ ] `withCount()`を使って、リレーションシップのカウントを取得できる。
- [ ] 条件付きEager Loadingを使って、必要なデータのみを読み込める。
