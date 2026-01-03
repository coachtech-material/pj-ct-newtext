# Tutorial 9-5-5: 実践: リレーションシップを使ったブログシステム

## 🎯 このセクションで学ぶこと

*   ユーザー、投稿、コメント、タグのリレーションシップを実装できるようになる。
*   実践的なデータ取得を学ぶ。
*   複雑なクエリを書けるようになる。

---

## 導入：「全てを組み合わせる」

これまで、様々なリレーションシップを学んできました。このセクションでは、それらを組み合わせて、**実践的なブログシステム**を実装します。

**実装する機能**

*   ユーザーは、複数の投稿を持つ（1対多）
*   投稿は、複数のコメントを持つ（1対多）
*   投稿は、複数のタグを持つ（多対多）
*   コメントは、ユーザーに属する（多対1）

---

## 詳細解説

### 📝 テーブル設計

**テーブル構成**

```
users テーブル
+----+----------+-------+
| id | name     | email |
+----+----------+-------+

posts テーブル
+----+---------+-----------+---------+
| id | user_id | title     | content |
+----+---------+-----------+---------+

comments テーブル
+----+---------+---------+---------+
| id | post_id | user_id | content |
+----+---------+---------+---------+

tags テーブル
+----+--------+
| id | name   |
+----+--------+

post_tag テーブル（中間テーブル）
+----+---------+---------+
| id | post_id | tag_id  |
+----+---------+---------+
```

---

### 🔧 マイグレーションの作成

#### postsテーブル

```bash
php artisan make:migration create_posts_table
```

```php
public function up()
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->string('title');
        $table->text('content');
        $table->boolean('is_published')->default(false);
        $table->timestamps();
    });
}
```

#### commentsテーブル

```bash
php artisan make:migration create_comments_table
```

```php
public function up()
{
    Schema::create('comments', function (Blueprint $table) {
        $table->id();
        $table->foreignId('post_id')->constrained()->onDelete('cascade');
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->text('content');
        $table->timestamps();
    });
}
```

#### tagsテーブル

```bash
php artisan make:migration create_tags_table
```

```php
public function up()
{
    Schema::create('tags', function (Blueprint $table) {
        $table->id();
        $table->string('name')->unique();
        $table->timestamps();
    });
}
```

#### post_tagテーブル

```bash
php artisan make:migration create_post_tag_table
```

```php
public function up()
{
    Schema::create('post_tag', function (Blueprint $table) {
        $table->id();
        $table->foreignId('post_id')->constrained()->onDelete('cascade');
        $table->foreignId('tag_id')->constrained()->onDelete('cascade');
        $table->timestamps();
    });
}
```

---

### 🔗 モデルの定義

#### User.php

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable
{
    protected $fillable = ['name', 'email', 'password'];

    public function posts()
    {
        return $this->hasMany(Post::class);
    }

    public function comments()
    {
        return $this->hasMany(Comment::class);
    }
}
```

#### Post.php

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    protected $fillable = ['user_id', 'title', 'content', 'is_published'];

    public function user()
    {
        return $this->belongsTo(User::class);
    }

    public function comments()
    {
        return $this->hasMany(Comment::class);
    }

    public function tags()
    {
        return $this->belongsToMany(Tag::class);
    }
}
```

#### Comment.php

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Comment extends Model
{
    protected $fillable = ['post_id', 'user_id', 'content'];

    public function post()
    {
        return $this->belongsTo(Post::class);
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

#### Tag.php

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Tag extends Model
{
    protected $fillable = ['name'];

    public function posts()
    {
        return $this->belongsToMany(Post::class);
    }
}
```

---

### 🔍 Tinkerでデータ構造を確認する

コントローラーを書く前に、Tinkerを起動してリレーションシップが正しく動作するか確認しましょう。

```bash
sail artisan tinker
```

```php
>>> use App\Models\User;
>>> use App\Models\Post;
>>> use App\Models\Comment;
>>> use App\Models\Tag;

// ユーザーの投稿を取得
>>> $user = User::first();
>>> $user->posts;

// 投稿のコメントを取得
>>> $post = Post::first();
>>> $post->comments;

// 投稿のタグを取得
>>> $post->tags;

// コメントの投稿者を取得
>>> $comment = Comment::first();
>>> $comment->user;

// Eager Loadingの確認
>>> Post::with(['user', 'comments', 'tags'])->first();
```

**確認ポイント**：
- `$user->posts`でユーザーの投稿が取得できるか？
- `$post->comments`で投稿のコメントが取得できるか？
- `$post->tags`で投稿のタグが取得できるか？

> 💡 **重要**: 「データが取れていないのに画面を作っても動かない」ことを理解しましょう。Tinkerでリレーションメソッドを実行し、意図したデータ（SQL）が返ってきているか確認してから、コントローラーとビューを実装します。

---

### 🚀 実践例1: 投稿の作成

#### コントローラー

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'content' => 'required',
        'tags' => 'array',
    ]);

    $post = Auth::user()->posts()->create([
        'title' => $validated['title'],
        'content' => $validated['content'],
        'is_published' => false,
    ]);

    // タグを追加
    if (isset($validated['tags'])) {
        $post->tags()->attach($validated['tags']);
    }

    return redirect('/posts/' . $post->id);
}
```

---

### 🚀 実践例2: 投稿一覧の表示

#### コントローラー

```php
public function index()
{
    $posts = Post::with(['user', 'tags'])
                 ->withCount('comments')
                 ->where('is_published', true)
                 ->latest()
                 ->paginate(10);

    return view('posts.index', compact('posts'));
}
```

#### Bladeテンプレート

```blade
@foreach($posts as $post)
    <div class="post">
        <h2><a href="/posts/{{ $post->id }}">{{ $post->title }}</a></h2>
        <p>投稿者: {{ $post->user->name }}</p>
        <p>コメント数: {{ $post->comments_count }}</p>
        
        <div class="tags">
            @foreach($post->tags as $tag)
                <span class="tag">{{ $tag->name }}</span>
            @endforeach
        </div>
    </div>
@endforeach

{{ $posts->links() }}
```

---

### 🚀 実践例3: 投稿詳細の表示

#### コントローラー

```php
public function show($id)
{
    $post = Post::with(['user', 'comments.user', 'tags'])
                ->findOrFail($id);

    return view('posts.show', compact('post'));
}
```

#### Bladeテンプレート

```blade
<h1>{{ $post->title }}</h1>
<p>投稿者: {{ $post->user->name }}</p>
<p>投稿日: {{ $post->created_at->format('Y年m月d日') }}</p>

<div class="tags">
    @foreach($post->tags as $tag)
        <span class="tag">{{ $tag->name }}</span>
    @endforeach
</div>

<div class="content">
    {!! nl2br(e($post->content)) !!}
</div>

<h2>コメント</h2>
@foreach($post->comments as $comment)
    <div class="comment">
        <p><strong>{{ $comment->user->name }}</strong></p>
        <p>{{ $comment->content }}</p>
        <p><small>{{ $comment->created_at->diffForHumans() }}</small></p>
    </div>
@endforeach
```

---

### 🚀 実践例4: コメントの投稿

#### コントローラー

```php
public function storeComment(Request $request, $postId)
{
    $validated = $request->validate([
        'content' => 'required',
    ]);

    $post = Post::findOrFail($postId);

    $post->comments()->create([
        'user_id' => Auth::id(),
        'content' => $validated['content'],
    ]);

    return redirect('/posts/' . $postId);
}
```

---

### 🚀 実践例5: タグで投稿を検索

#### コントローラー

```php
public function byTag($tagName)
{
    $tag = Tag::where('name', $tagName)->firstOrFail();

    $posts = $tag->posts()
                 ->with(['user', 'tags'])
                 ->withCount('comments')
                 ->where('is_published', true)
                 ->latest()
                 ->paginate(10);

    return view('posts.by-tag', compact('tag', 'posts'));
}
```

---

### 🚀 実践例6: ユーザーのダッシュボード

#### コントローラー

```php
public function dashboard()
{
    $user = Auth::user();

    $stats = [
        'total_posts' => $user->posts()->count(),
        'published_posts' => $user->posts()->where('is_published', true)->count(),
        'draft_posts' => $user->posts()->where('is_published', false)->count(),
        'total_comments' => $user->comments()->count(),
    ];

    $latestPosts = $user->posts()
                        ->withCount('comments')
                        ->latest()
                        ->take(5)
                        ->get();

    $latestComments = $user->comments()
                           ->with('post')
                           ->latest()
                           ->take(5)
                           ->get();

    return view('dashboard', compact('stats', 'latestPosts', 'latestComments'));
}
```

---

### 🚀 実践例7: 人気の投稿を取得

#### コントローラー

```php
public function popular()
{
    $posts = Post::with(['user', 'tags'])
                 ->withCount('comments')
                 ->where('is_published', true)
                 ->orderBy('comments_count', 'desc')
                 ->take(10)
                 ->get();

    return view('posts.popular', compact('posts'));
}
```

---

### 🚀 実践例8: 検索機能

#### コントローラー

```php
public function search(Request $request)
{
    $query = Post::query();

    // タイトルまたは内容で検索
    if ($request->filled('keyword')) {
        $keyword = $request->keyword;
        $query->where(function ($q) use ($keyword) {
            $q->where('title', 'like', '%' . $keyword . '%')
              ->orWhere('content', 'like', '%' . $keyword . '%');
        });
    }

    // タグで絞り込み
    if ($request->filled('tag')) {
        $query->whereHas('tags', function ($q) use ($request) {
            $q->where('name', $request->tag);
        });
    }

    // 投稿者で絞り込み
    if ($request->filled('author')) {
        $query->whereHas('user', function ($q) use ($request) {
            $q->where('name', 'like', '%' . $request->author . '%');
        });
    }

    $posts = $query->with(['user', 'tags'])
                   ->withCount('comments')
                   ->where('is_published', true)
                   ->latest()
                   ->paginate(10);

    return view('posts.search', compact('posts'));
}
```

---

### 💡 TIP: スコープの活用

モデルにスコープを定義することで、クエリを再利用できます。

**`app/Models/Post.php`**

```php
public function scopePublished($query)
{
    return $query->where('is_published', true);
}

public function scopeWithRelations($query)
{
    return $query->with(['user', 'tags'])->withCount('comments');
}
```

**使用例**

```php
$posts = Post::published()
             ->withRelations()
             ->latest()
             ->paginate(10);
```

---

### 🚨 パフォーマンスの最適化

#### N+1問題を避ける

```php
// NG: N+1問題が発生
$posts = Post::all();
foreach ($posts as $post) {
    echo $post->user->name;
    echo $post->comments->count();
}

// OK: Eager Loadingを使う
$posts = Post::with('user')->withCount('comments')->get();
foreach ($posts as $post) {
    echo $post->user->name;
    echo $post->comments_count;
}
```

---

## ✨ まとめ

このセクションでは、リレーションシップを使った実践的なブログシステムを実装しました。

*   ユーザー、投稿、コメント、タグのリレーションシップを実装した。
*   Eager Loadingを使って、N+1問題を避けた。
*   `withCount()`を使って、効率的にカウントを取得した。
*   スコープを使って、クエリを再利用可能にした。
*   複雑な検索機能を実装した。

これで、Chapter 5「Eloquent ORMとリレーションシップ」の全9セクションが完了しました。次は、Chapter 6「バリデーション」の残りのセクションに進みます。

---
