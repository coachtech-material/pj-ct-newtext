# Tutorial 9-5-4: リレーションシップのクエリ

## 🎯 このセクションで学ぶこと

*   `whereHas()`を使って、リレーションシップを条件にデータを取得する方法を理解する。
*   `doesntHave()`を使って、リレーションシップを持たないデータを取得する方法を理解する。
*   `withWhereHas()`を使って、Eager Loadingと条件を組み合わせる方法を理解する。

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

**例：投稿を持つユーザーのみを取得**

```php
$users = User::has('posts')->get();
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `User::` | Userモデルに対してクエリを開始します |
| `has('posts')` | `posts`リレーションシップを持つレコードのみに絞り込みます |
| `->get()` | 結果をコレクションとして取得します |

**実行されるSQL**

```sql
SELECT * FROM users WHERE EXISTS (
    SELECT * FROM posts WHERE users.id = posts.user_id
);
```

`EXISTS`サブクエリを使って、関連するレコードが存在するかどうかをチェックしています。

---

### 🔍 `doesntHave()`: リレーションシップを持たないレコードを取得

`doesntHave()`を使うことで、**リレーションシップを持たないレコードのみを取得**できます。

**例：投稿を持たないユーザーのみを取得**

```php
$users = User::doesntHave('posts')->get();
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `doesntHave('posts')` | `posts`リレーションシップを**持たない**レコードのみに絞り込みます |

**実行されるSQL**

```sql
SELECT * FROM users WHERE NOT EXISTS (
    SELECT * FROM posts WHERE users.id = posts.user_id
);
```

`NOT EXISTS`を使って、関連するレコードが存在しないことをチェックしています。

---

### 🔍 `has()` with カウント

`has()`の第2、第3引数を使うことで、**リレーションシップの数を条件にできます**。

**例：投稿が3件以上のユーザーのみを取得**

```php
$users = User::has('posts', '>=', 3)->get();
```

**構文**：

```php
has('リレーション名', '比較演算子', 数値)
```

| 引数 | 説明 | 例 |
|:---|:---|:---|
| 第1引数 | リレーション名 | `'posts'` |
| 第2引数 | 比較演算子 | `'>'`, `'>='`, `'<'`, `'<='`, `'='` |
| 第3引数 | 比較する数値 | `3` |

**実行されるSQL**

```sql
SELECT * FROM users WHERE (
    SELECT COUNT(*) FROM posts WHERE users.id = posts.user_id
) >= 3;
```

---

### 🔍 `whereHas()`: リレーションシップの内容を条件にする

`whereHas()`を使うことで、**リレーションシップの内容を条件にできます**。

**例：公開済みの投稿を持つユーザーのみを取得**

```php
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true);
})->get();
```

**構文**：

```php
whereHas('リレーション名', function ($query) {
    $query->where('カラム名', 値);
})
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `whereHas('posts', ...)` | `posts`リレーションシップに対して条件を指定します |
| `function ($query)` | クロージャ（無名関数）でクエリビルダーを受け取ります |
| `$query->where('is_published', true)` | 関連テーブルの`is_published`カラムが`true`のレコードに絞り込みます |

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

**例：公開済みの投稿を持たないユーザーのみを取得**

```php
$users = User::whereDoesntHave('posts', function ($query) {
    $query->where('is_published', true);
})->get();
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `whereDoesntHave('posts', ...)` | 条件に一致する`posts`リレーションシップを**持たない**レコードに絞り込みます |

これは「公開済みの投稿を1件も持たないユーザー」を取得します。下書きのみのユーザーや、投稿が0件のユーザーが該当します。

---

### 🚀 実践例：ブログの投稿検索

ブログアプリケーションでよく使われる検索パターンを見ていきましょう。

**例1: 特定のタグを持つ投稿を取得**

```php
$posts = Post::whereHas('tags', function ($query) {
    $query->where('name', 'Laravel');
})->get();
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `Post::whereHas('tags', ...)` | `tags`リレーションシップに対して条件を指定します |
| `$query->where('name', 'Laravel')` | タグ名が「Laravel」のタグを持つ投稿に絞り込みます |

**例2: 複数のタグを持つ投稿を取得**

```php
$posts = Post::whereHas('tags', function ($query) {
    $query->whereIn('name', ['Laravel', 'PHP']);
})->get();
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `whereIn('name', ['Laravel', 'PHP'])` | タグ名が「Laravel」または「PHP」のいずれかを持つ投稿に絞り込みます |

**例3: コメントが10件以上の投稿を取得**

```php
$posts = Post::has('comments', '>=', 10)->get();
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `has('comments', '>=', 10)` | コメント数が10件以上の投稿に絞り込みます |

---

### 🔍 `withWhereHas()`: Eager Loadingと条件を組み合わせる

`withWhereHas()`を使うことで、**Eager Loadingと条件を組み合わせられます**。

**例：公開済みの投稿を持つユーザーを取得し、その投稿も読み込む**

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

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `withWhereHas('posts', ...)` | `whereHas()`と`with()`を同時に実行します |
| `$query->where('is_published', true)` | 公開済みの投稿のみを条件にします |
| `$user->posts` | 公開済みの投稿のみがロードされています |

**`whereHas()`と`with()`を別々に使う場合との違い**：

```php
// 別々に使う場合（非推奨）
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true);
})->with('posts')->get();
// → $user->postsには全ての投稿（下書きも含む）がロードされる

// withWhereHasを使う場合（推奨）
$users = User::withWhereHas('posts', function ($query) {
    $query->where('is_published', true);
})->get();
// → $user->postsには公開済みの投稿のみがロードされる
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

ユーザーのダッシュボードで、投稿を状態別に表示する実装例です。

**コントローラー**

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

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `Auth::user()` | 現在ログイン中のユーザーを取得します |
| `$user->posts()` | ユーザーの投稿に対するクエリビルダーを取得します（`()`を付けることでクエリビルダーとして扱えます） |
| `->where('is_published', true)` | 公開済みの投稿に絞り込みます |
| `->latest()` | 作成日時の降順（新しい順）でソートします |
| `->has('comments')` | コメントを持つ投稿に絞り込みます |
| `->withCount('comments')` | コメント数を`comments_count`属性として追加します |
| `compact(...)` | 変数をビューに渡します |

**処理の流れ**：

```
1. ログインユーザーを取得
    ↓
2. 公開済み投稿を取得（$publishedPosts）
    ↓
3. 下書き投稿を取得（$draftPosts）
    ↓
4. コメント付き投稿を取得（$postsWithComments）
    ↓
5. ビューに渡して表示
```

---

### 🔍 ネストしたリレーションシップのクエリ

**例：コメントに「Laravel」という単語を含む投稿を持つユーザーを取得**

```php
$users = User::whereHas('posts.comments', function ($query) {
    $query->where('content', 'like', '%Laravel%');
})->get();
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `whereHas('posts.comments', ...)` | ネストしたリレーションシップ（投稿のコメント）に対して条件を指定します |
| `'posts.comments'` | ドット記法で「投稿のコメント」を表現します |
| `'like', '%Laravel%'` | 部分一致検索を行います |

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

**例：公開済みの投稿を持ち、かつコメントが10件以上のユーザーを取得**

```php
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true)
          ->has('comments', '>=', 10);
})->get();
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `->where('is_published', true)` | 公開済みの投稿に絞り込みます |
| `->has('comments', '>=', 10)` | さらにコメントが10件以上の投稿に絞り込みます |

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

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `whereHas('posts', ...)` | 公開済みの投稿を持つユーザー |
| `orWhereHas('comments', ...)` | **または**承認済みのコメントを持つユーザー |

このクエリは「公開済みの投稿を持つユーザー」または「承認済みのコメントを持つユーザー」を取得します。

---

### 🚀 実践例：投稿の検索機能

複数の条件を組み合わせた検索機能の実装例です。

**コントローラー**

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

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `Post::query()` | 空のクエリビルダーを作成します。条件を動的に追加するための起点です |
| `$request->filled('title')` | リクエストに`title`パラメータが存在し、空でないかをチェックします |
| `use ($request)` | クロージャ内で`$request`変数を使用するための宣言です |
| `->with(['user', 'tags'])` | Eager Loadingで投稿者とタグを事前に読み込みます |
| `->withCount('comments')` | コメント数を`comments_count`属性として追加します |
| `->paginate(10)` | 10件ずつページネーションします |

**処理の流れ**：

```
1. 空のクエリビルダーを作成
    ↓
2. リクエストパラメータに応じて条件を追加
   - title → タイトルで部分一致検索
   - tag → タグ名で絞り込み
   - author → 投稿者名で絞り込み
   - min_comments → コメント数で絞り込み
    ↓
3. Eager Loadingとページネーションを適用
    ↓
4. 結果をビューに渡す
```

---

### 🚨 よくある間違い

**間違い1: `whereHas()`の中で`get()`を使う**

```php
// NG: whereHas()の中でget()を使っている
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true)->get(); // NG
})->get();
```

**対処法**: `whereHas()`の中では、`get()`は不要です。クロージャ内のクエリは条件の定義のみを行います。

```php
// OK: get()を削除
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true); // OK
})->get();
```

**間違い2: `has()`と`whereHas()`を混同する**

```php
// has()は、リレーションシップの存在のみをチェック
$users = User::has('posts')->get();
// → 投稿を1件以上持つユーザーを取得

// whereHas()は、リレーションシップの内容を条件にする
$users = User::whereHas('posts', function ($query) {
    $query->where('is_published', true);
})->get();
// → 公開済みの投稿を持つユーザーを取得
```

**使い分けのポイント**：

| メソッド | 用途 | 例 |
|:---|:---|:---|
| `has()` | 関連データの**存在**をチェック | 「投稿を持つユーザー」 |
| `whereHas()` | 関連データの**内容**を条件にする | 「公開済みの投稿を持つユーザー」 |

---

## ✨ まとめ

このセクションでは、リレーションシップを条件にしたクエリの書き方を学びました。

*   `has()`を使って、リレーションシップを持つレコードのみを取得できる。
*   `doesntHave()`を使って、リレーションシップを持たないレコードのみを取得できる。
*   `whereHas()`を使って、リレーションシップの内容を条件にできる。
*   `whereDoesntHave()`を使って、リレーションシップの内容を否定条件にできる。
*   `withWhereHas()`を使って、Eager Loadingと条件を組み合わせられる。

---
