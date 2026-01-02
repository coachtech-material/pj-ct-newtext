# Tutorial 9-5-4: リレーションシップのクエリ

## 🎯 このセクションで学ぶこと

*   `whereHas()`を使って、リレーションシップを条件にデータを取得できるようになる。
*   `doesntHave()`を使って、リレーションシップを持たないデータを取得できるようになる。
*   `withWhereHas()`を使って、Eager Loadingと条件を組み合わせられるようになる。

---

## 導入：「関連するデータ」を条件にする

これまで、リレーションシップを使ってデータを取得する方法を学びました。しかし、実際のアプリケーション開発では、**関連するデータを条件にして、データを取得する**ことがよくあります。

例えば、以下のような状況を考えてみましょう。

*   **公開済みの投稿を持つユーザーのみを取得したい**
*   **コメントがない投稿のみを取得したい**
*   **特定のタグを持つ投稿のみを取得したい**

このセクションでは、リレーションシップを条件にしたクエリの書き方を学びます。

---

## 詳細解説

### 🔍 `has()`: リレーションシップを持つレコードを取得

`has()`を使うことで、**リレーションシップを持つレコードのみを取得**できます。

#### 例：投稿を持つユーザーのみを取得

```php
$users = User::has('posts')->get();
```

**実行されるSQL**

```sql
SELECT * FROM users WHERE EXISTS (
    SELECT * FROM posts WHERE users.id = posts.user_id
);
```

---

### 🔍 `doesntHave()`: リレーションシップを持たないレコードを取得

`doesntHave()`を使うことで、**リレーションシップを持たないレコードのみを取得**できます。

#### 例：投稿を持たないユーザーのみを取得

```php
$users = User::doesntHave('posts')->get();
```

**実行されるSQL**

```sql
SELECT * FROM users WHERE NOT EXISTS (
    SELECT * FROM posts WHERE users.id = posts.user_id
);
```

---

### 🔍 `has()` with カウント

`has()`の第2、第3引数を使うことで、**リレーションシップの数を条件にできます**。

#### 例：投稿が3件以上のユーザーのみを取得

```php
$users = User::has('posts', '>=', 3)->get();
```

**実行されるSQL**

```sql
SELECT * FROM users WHERE (
    SELECT COUNT(*) FROM posts WHERE users.id = posts.user_id
) >= 3;
```

---

### 🔍 `whereHas()`: リレーションシップの内容を条件にする

`whereHas()`を使うことで、**リレーションシップの内容を条件にできます**。

#### 例：公開済みの投稿を持つユーザーのみを取得

```php
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true);
})->get();
```

**実行されるSQL**

```sql
SELECT * FROM users WHERE EXISTS (
    SELECT * FROM posts 
    WHERE users.id = posts.user_id 
    AND is_published = 1
);
```

---

### 🔍 `whereDoesntHave()`: リレーションシップの内容を否定条件にする

`whereDoesntHave()`を使うことで、**リレーションシップの内容を否定条件にできます**。

#### 例：公開済みの投稿を持たないユーザーのみを取得

```php
$users = User::whereDoesntHave('posts', function ($query) {
    $query->where('is_published', true);
})->get();
```

---

### 🚀 実践例：ブログの投稿検索

#### 例1: 特定のタグを持つ投稿を取得

```php
$posts = Post::whereHas('tags', function ($query) {
    $query->where('name', 'Laravel');
})->get();
```

#### 例2: 複数のタグを持つ投稿を取得

```php
$posts = Post::whereHas('tags', function ($query) {
    $query->whereIn('name', ['Laravel', 'PHP']);
})->get();
```

#### 例3: コメントが10件以上の投稿を取得

```php
$posts = Post::has('comments', '>=', 10)->get();
```

---

### 🔍 `withWhereHas()`: Eager Loadingと条件を組み合わせる

`withWhereHas()`を使うことで、**Eager Loadingと条件を組み合わせられます**。

#### 例：公開済みの投稿を持つユーザーを取得し、その投稿も読み込む

```php
$users = User::withWhereHas('posts', function ($query) {
    $query->where('is_published', true);
})->get();

foreach ($users as $user) {
    foreach ($user->posts as $post) {
        echo $post->title; // 公開済みの投稿のみ
    }
}
```

**実行されるSQL**

```sql
-- ユーザーを取得
SELECT * FROM users WHERE EXISTS (
    SELECT * FROM posts 
    WHERE users.id = posts.user_id 
    AND is_published = 1
);

-- 公開済みの投稿を取得
SELECT * FROM posts 
WHERE user_id IN (1, 2, 3, ...) 
AND is_published = 1;
```

---

### 🚀 実践例：ダッシュボード

#### コントローラー

```php
public function dashboard()
{
    $user = Auth::user();
    
    // 公開済みの投稿のみを取得
    $publishedPosts = $user->posts()
                           ->where('is_published', true)
                           ->latest()
                           ->get();
    
    // 下書きの投稿のみを取得
    $draftPosts = $user->posts()
                       ->where('is_published', false)
                       ->latest()
                       ->get();
    
    // コメントがある投稿のみを取得
    $postsWithComments = $user->posts()
                              ->has('comments')
                              ->withCount('comments')
                              ->latest()
                              ->get();

    return view('dashboard', compact('publishedPosts', 'draftPosts', 'postsWithComments'));
}
```

---

### 🔍 ネストしたリレーションシップのクエリ

#### 例：コメントに「Laravel」という単語を含む投稿を持つユーザーを取得

```php
$users = User::whereHas('posts.comments', function ($query) {
    $query->where('content', 'like', '%Laravel%');
})->get();
```

**実行されるSQL**

```sql
SELECT * FROM users WHERE EXISTS (
    SELECT * FROM posts 
    WHERE users.id = posts.user_id 
    AND EXISTS (
        SELECT * FROM comments 
        WHERE posts.id = comments.post_id 
        AND content LIKE '%Laravel%'
    )
);
```

---

### 🔍 複数の条件を組み合わせる

#### 例：公開済みの投稿を持ち、かつコメントが10件以上のユーザーを取得

```php
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true)
          ->has('comments', '>=', 10);
})->get();
```

---

### 💡 TIP: `orWhereHas()`

`orWhereHas()`を使うことで、OR条件を追加できます。

```php
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true);
})->orWhereHas('comments', function ($query) {
    $query->where('is_approved', true);
})->get();
```

---

### 🚀 実践例：投稿の検索機能

#### コントローラー

```php
public function search(Request $request)
{
    $query = Post::query();

    // タイトルで検索
    if ($request->filled('title')) {
        $query->where('title', 'like', '%' . $request->title . '%');
    }

    // タグで検索
    if ($request->filled('tag')) {
        $query->whereHas('tags', function ($q) use ($request) {
            $q->where('name', $request->tag);
        });
    }

    // 投稿者で検索
    if ($request->filled('author')) {
        $query->whereHas('user', function ($q) use ($request) {
            $q->where('name', 'like', '%' . $request->author . '%');
        });
    }

    // コメント数で絞り込み
    if ($request->filled('min_comments')) {
        $query->has('comments', '>=', $request->min_comments);
    }

    $posts = $query->with(['user', 'tags'])
                   ->withCount('comments')
                   ->latest()
                   ->paginate(10);

    return view('posts.search', compact('posts'));
}
```

---

### 🚨 よくある間違い

#### 間違い1: `whereHas()`の中で`get()`を使う

```php
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true)->get(); // NG
})->get();
```

**対処法**: `whereHas()`の中では、`get()`は不要です。

```php
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true); // OK
})->get();
```

#### 間違い2: `has()`と`whereHas()`を混同する

```php
// has()は、リレーションシップの存在のみをチェック
$users = User::has('posts')->get();

// whereHas()は、リレーションシップの内容を条件にする
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true);
})->get();
```

---

## ✨ まとめ

このセクションでは、リレーションシップを条件にしたクエリの書き方を学びました。

*   `has()`を使って、リレーションシップを持つレコードのみを取得できる。
*   `doesntHave()`を使って、リレーションシップを持たないレコードのみを取得できる。
*   `whereHas()`を使って、リレーションシップの内容を条件にできる。
*   `whereDoesntHave()`を使って、リレーションシップの内容を否定条件にできる。
*   `withWhereHas()`を使って、Eager Loadingと条件を組み合わせられる。

次のセクションでは、ポリモーフィックリレーションシップについて学びます。

---
