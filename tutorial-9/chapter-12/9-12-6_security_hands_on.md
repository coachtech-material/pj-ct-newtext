# Tutorial 9-12-6: Webセキュリティハンズオン

## 🎯 このハンズオンで実践すること

*   CSRF保護を実装したフォームを作成する。
*   SQLインジェクション対策を意識した検索機能を実装する。
*   XSS対策を意識したコメント機能を実装する。
*   安全な認証機能を実装する。
*   パスワードハッシュ化を実装する。

---

## 📝 課題：セキュアなブログシステムを構築しよう

このハンズオンでは、**セキュリティを意識したブログシステム**を構築します。以下の機能を実装してください。

### 実装する機能

1. **ユーザー登録・ログイン機能**
   - パスワードは安全にハッシュ化して保存
   - ログイン時にセッションIDを再生成
   - ログアウト時にセッションを無効化

2. **記事投稿機能**
   - CSRF保護を実装
   - XSS対策を実装（ユーザー入力を安全に表示）

3. **記事検索機能**
   - SQLインジェクション対策を実装
   - Eloquent ORMを使った安全なクエリ

4. **コメント機能**
   - XSS対策を実装
   - 認証済みユーザーのみコメント可能

---

## 🔧 環境準備

### 1. Laravelプロジェクトを作成

```bash
composer create-project laravel/laravel secure-blog
cd secure-blog
```

### 2. データベース設定

**.env**

```env
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=secure_blog
DB_USERNAME=root
DB_PASSWORD=
```

### 3. データベースを作成

```bash
mysql -u root -e "CREATE DATABASE secure_blog"
```

---

## 💡 ヒント

### ヒント1：マイグレーションの作成

以下のテーブルが必要です：

- **users**：ユーザー情報（name, email, password）
- **posts**：記事情報（title, content, user_id）
- **comments**：コメント情報（content, user_id, post_id）

```bash
php artisan make:migration create_posts_table
php artisan make:migration create_comments_table
```

### ヒント2：モデルの作成

```bash
php artisan make:model Post
php artisan make:model Comment
```

### ヒント3：コントローラーの作成

```bash
php artisan make:controller AuthController
php artisan make:controller PostController
php artisan make:controller CommentController
```

### ヒント4：CSRF保護

フォームには必ず`@csrf`ディレクティブを追加してください。

```blade
<form method="POST" action="/posts">
    @csrf
    <!-- フォームの内容 -->
</form>
```

### ヒント5：XSS対策

ユーザー入力を表示する際は、`{{ }}`構文を使ってください。

```blade
<p>{{ $post->content }}</p>
```

`{!! !!}`は使わないでください。

### ヒント6：SQLインジェクション対策

Eloquent ORMを使ってください。生SQLは使わないでください。

```php
// ✅ 安全
$posts = Post::where('title', 'like', '%' . $keyword . '%')->get();

// 🚨 危険
$posts = DB::select("SELECT * FROM posts WHERE title LIKE '%$keyword%'");
```

### ヒント7：パスワードハッシュ化

```php
use Illuminate\Support\Facades\Hash;

User::create([
    'password' => Hash::make($request->password),
]);
```

### ヒント8：認証

```php
use Illuminate\Support\Facades\Auth;

// ログイン
if (Auth::attempt($credentials)) {
    $request->session()->regenerate();
    return redirect('/dashboard');
}

// ログアウト
Auth::logout();
$request->session()->invalidate();
$request->session()->regenerateToken();
```

---

## 📖 模範解答

### 1. マイグレーション

#### database/migrations/xxxx_create_posts_table.php

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('posts', function (Blueprint $table) {
            $table->id();
            $table->string('title');
            $table->text('content');
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('posts');
    }
};
```

#### database/migrations/xxxx_create_comments_table.php

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('comments', function (Blueprint $table) {
            $table->id();
            $table->text('content');
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            $table->foreignId('post_id')->constrained()->onDelete('cascade');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('comments');
    }
};
```

```bash
php artisan migrate
```

---

### 2. モデル

#### app/Models/Post.php

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Post extends Model
{
    protected $fillable = ['title', 'content', 'user_id'];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function comments(): HasMany
    {
        return $this->hasMany(Comment::class);
    }
}
```

#### app/Models/Comment.php

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Comment extends Model
{
    protected $fillable = ['content', 'user_id', 'post_id'];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function post(): BelongsTo
    {
        return $this->belongsTo(Post::class);
    }
}
```

---

### 3. コントローラー

#### app/Http/Controllers/AuthController.php

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;

class AuthController extends Controller
{
    // 登録フォームを表示
    public function showRegisterForm()
    {
        return view('auth.register');
    }

    // ユーザー登録処理
    public function register(Request $request)
    {
        $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users',
            'password' => 'required|string|min:8|confirmed',
        ]);

        User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password), // パスワードをハッシュ化
        ]);

        return redirect('/login')->with('success', 'アカウントを作成しました');
    }

    // ログインフォームを表示
    public function showLoginForm()
    {
        return view('auth.login');
    }

    // ログイン処理
    public function login(Request $request)
    {
        $credentials = $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate(); // セッションIDを再生成（セキュリティ対策）
            return redirect()->intended('/posts');
        }

        return back()->withErrors([
            'email' => 'メールアドレスまたはパスワードが正しくありません。',
        ]);
    }

    // ログアウト処理
    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate(); // セッションを無効化
        $request->session()->regenerateToken(); // CSRFトークンを再生成
        return redirect('/');
    }
}
```

---

#### app/Http/Controllers/PostController.php

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    // 記事一覧を表示
    public function index(Request $request)
    {
        $query = Post::with('user');

        // 検索機能（SQLインジェクション対策）
        if ($request->has('keyword')) {
            $keyword = $request->keyword;
            // Eloquent ORMを使うことで、自動的にエスケープされる
            $query->where('title', 'like', '%' . $keyword . '%');
        }

        $posts = $query->latest()->paginate(10);

        return view('posts.index', compact('posts'));
    }

    // 記事詳細を表示
    public function show($id)
    {
        $post = Post::with(['user', 'comments.user'])->findOrFail($id);
        return view('posts.show', compact('post'));
    }

    // 記事作成フォームを表示
    public function create()
    {
        return view('posts.create');
    }

    // 記事を保存
    public function store(Request $request)
    {
        $request->validate([
            'title' => 'required|string|max:255',
            'content' => 'required|string',
        ]);

        Post::create([
            'title' => $request->title,
            'content' => $request->content,
            'user_id' => auth()->id(),
        ]);

        return redirect('/posts')->with('success', '記事を投稿しました');
    }

    // 記事を削除
    public function destroy($id)
    {
        $post = Post::findOrFail($id);

        // 自分の記事のみ削除可能
        if ($post->user_id !== auth()->id()) {
            abort(403, '権限がありません');
        }

        $post->delete();

        return redirect('/posts')->with('success', '記事を削除しました');
    }
}
```

---

#### app/Http/Controllers/CommentController.php

```php
<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use Illuminate\Http\Request;

class CommentController extends Controller
{
    // コメントを保存
    public function store(Request $request, $postId)
    {
        $request->validate([
            'content' => 'required|string|max:500',
        ]);

        Comment::create([
            'content' => $request->content,
            'user_id' => auth()->id(),
            'post_id' => $postId,
        ]);

        return redirect()->back()->with('success', 'コメントを投稿しました');
    }
}
```

---

### 4. ルート

#### routes/web.php

```php
<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\PostController;
use App\Http\Controllers\CommentController;
use Illuminate\Support\Facades\Route;

// トップページ
Route::get('/', function () {
    return redirect('/posts');
});

// 認証
Route::get('/register', [AuthController::class, 'showRegisterForm'])->name('register');
Route::post('/register', [AuthController::class, 'register']);
Route::get('/login', [AuthController::class, 'showLoginForm'])->name('login');
Route::post('/login', [AuthController::class, 'login']);
Route::post('/logout', [AuthController::class, 'logout'])->middleware('auth');

// 記事
Route::get('/posts', [PostController::class, 'index']);
Route::get('/posts/{id}', [PostController::class, 'show']);

// 認証が必要なルート
Route::middleware('auth')->group(function () {
    Route::get('/posts/create', [PostController::class, 'create']);
    Route::post('/posts', [PostController::class, 'store']);
    Route::delete('/posts/{id}', [PostController::class, 'destroy']);
    
    // コメント
    Route::post('/posts/{postId}/comments', [CommentController::class, 'store']);
});
```

---

### 5. ビュー

#### resources/views/auth/register.blade.php

```blade
<!DOCTYPE html>
<html>
<head>
    <title>ユーザー登録</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>ユーザー登録</h1>

        @if ($errors->any())
            <div class="alert alert-danger">
                <ul>
                    @foreach ($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </ul>
            </div>
        @endif

        <form method="POST" action="/register">
            @csrf <!-- CSRF保護 -->
            
            <div class="mb-3">
                <label class="form-label">名前</label>
                <input type="text" name="name" class="form-control" value="{{ old('name') }}" required>
            </div>

            <div class="mb-3">
                <label class="form-label">メールアドレス</label>
                <input type="email" name="email" class="form-control" value="{{ old('email') }}" required>
            </div>

            <div class="mb-3">
                <label class="form-label">パスワード</label>
                <input type="password" name="password" class="form-control" required>
            </div>

            <div class="mb-3">
                <label class="form-label">パスワード（確認）</label>
                <input type="password" name="password_confirmation" class="form-control" required>
            </div>

            <button type="submit" class="btn btn-primary">登録</button>
        </form>

        <p class="mt-3">すでにアカウントをお持ちですか？ <a href="/login">ログイン</a></p>
    </div>
</body>
</html>
```

---

#### resources/views/auth/login.blade.php

```blade
<!DOCTYPE html>
<html>
<head>
    <title>ログイン</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>ログイン</h1>

        @if (session('success'))
            <div class="alert alert-success">{{ session('success') }}</div>
        @endif

        @if ($errors->any())
            <div class="alert alert-danger">
                <ul>
                    @foreach ($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </ul>
            </div>
        @endif

        <form method="POST" action="/login">
            @csrf <!-- CSRF保護 -->
            
            <div class="mb-3">
                <label class="form-label">メールアドレス</label>
                <input type="email" name="email" class="form-control" value="{{ old('email') }}" required>
            </div>

            <div class="mb-3">
                <label class="form-label">パスワード</label>
                <input type="password" name="password" class="form-control" required>
            </div>

            <button type="submit" class="btn btn-primary">ログイン</button>
        </form>

        <p class="mt-3">アカウントをお持ちでないですか？ <a href="/register">新規登録</a></p>
    </div>
</body>
</html>
```

---

#### resources/views/posts/index.blade.php

```blade
<!DOCTYPE html>
<html>
<head>
    <title>記事一覧</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h1>記事一覧</h1>
            <div>
                @auth
                    <a href="/posts/create" class="btn btn-primary">新規投稿</a>
                    <form method="POST" action="/logout" class="d-inline">
                        @csrf
                        <button type="submit" class="btn btn-secondary">ログアウト</button>
                    </form>
                @else
                    <a href="/login" class="btn btn-primary">ログイン</a>
                    <a href="/register" class="btn btn-secondary">新規登録</a>
                @endauth
            </div>
        </div>

        @if (session('success'))
            <div class="alert alert-success">{{ session('success') }}</div>
        @endif

        <!-- 検索フォーム -->
        <form method="GET" action="/posts" class="mb-4">
            <div class="input-group">
                <input type="text" name="keyword" class="form-control" placeholder="キーワード検索" value="{{ request('keyword') }}">
                <button type="submit" class="btn btn-outline-secondary">検索</button>
            </div>
        </form>

        <!-- 記事一覧 -->
        @foreach ($posts as $post)
            <div class="card mb-3">
                <div class="card-body">
                    <h5 class="card-title">
                        <a href="/posts/{{ $post->id }}">{{ $post->title }}</a>
                    </h5>
                    <!-- XSS対策：{{ }}構文で自動エスケープ -->
                    <p class="card-text">{{ Str::limit($post->content, 100) }}</p>
                    <small class="text-muted">投稿者: {{ $post->user->name }} | {{ $post->created_at->diffForHumans() }}</small>
                </div>
            </div>
        @endforeach

        <!-- ページネーション -->
        {{ $posts->appends(request()->query())->links() }}
    </div>
</body>
</html>
```

---

#### resources/views/posts/show.blade.php

```blade
<!DOCTYPE html>
<html>
<head>
    <title>{{ $post->title }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <a href="/posts" class="btn btn-secondary mb-3">← 戻る</a>

        @if (session('success'))
            <div class="alert alert-success">{{ session('success') }}</div>
        @endif

        <div class="card mb-4">
            <div class="card-body">
                <!-- XSS対策：{{ }}構文で自動エスケープ -->
                <h1 class="card-title">{{ $post->title }}</h1>
                <p class="card-text">{{ $post->content }}</p>
                <small class="text-muted">投稿者: {{ $post->user->name }} | {{ $post->created_at->format('Y年m月d日') }}</small>

                @if (auth()->check() && auth()->id() === $post->user_id)
                    <form method="POST" action="/posts/{{ $post->id }}" class="mt-3" onsubmit="return confirm('本当に削除しますか？')">
                        @csrf
                        @method('DELETE')
                        <button type="submit" class="btn btn-danger">削除</button>
                    </form>
                @endif
            </div>
        </div>

        <!-- コメント一覧 -->
        <h3>コメント</h3>
        @foreach ($post->comments as $comment)
            <div class="card mb-2">
                <div class="card-body">
                    <!-- XSS対策：{{ }}構文で自動エスケープ -->
                    <p>{{ $comment->content }}</p>
                    <small class="text-muted">{{ $comment->user->name }} | {{ $comment->created_at->diffForHumans() }}</small>
                </div>
            </div>
        @endforeach

        <!-- コメント投稿フォーム -->
        @auth
            <form method="POST" action="/posts/{{ $post->id }}/comments" class="mt-4">
                @csrf <!-- CSRF保護 -->
                <div class="mb-3">
                    <label class="form-label">コメントを投稿</label>
                    <textarea name="content" class="form-control" rows="3" required></textarea>
                </div>
                <button type="submit" class="btn btn-primary">投稿</button>
            </form>
        @else
            <p class="mt-4">コメントを投稿するには、<a href="/login">ログイン</a>してください。</p>
        @endauth
    </div>
</body>
</html>
```

---

#### resources/views/posts/create.blade.php

```blade
<!DOCTYPE html>
<html>
<head>
    <title>記事を投稿</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>記事を投稿</h1>

        @if ($errors->any())
            <div class="alert alert-danger">
                <ul>
                    @foreach ($errors->all() as $error)
                        <li>{{ $error }}</li>
                    @endforeach
                </ul>
            </div>
        @endif

        <form method="POST" action="/posts">
            @csrf <!-- CSRF保護 -->
            
            <div class="mb-3">
                <label class="form-label">タイトル</label>
                <input type="text" name="title" class="form-control" value="{{ old('title') }}" required>
            </div>

            <div class="mb-3">
                <label class="form-label">本文</label>
                <textarea name="content" class="form-control" rows="10" required>{{ old('content') }}</textarea>
            </div>

            <button type="submit" class="btn btn-primary">投稿</button>
            <a href="/posts" class="btn btn-secondary">キャンセル</a>
        </form>
    </div>
</body>
</html>
```

---

## 🧪 動作確認

### 1. サーバーを起動

```bash
php artisan serve
```

### 2. ブラウザでアクセス

```
http://localhost:8000
```

### 3. 確認項目

- [ ] ユーザー登録ができる
- [ ] パスワードがハッシュ化されてデータベースに保存される
- [ ] ログインができる
- [ ] ログイン後、記事を投稿できる
- [ ] 記事にコメントを投稿できる
- [ ] 記事を検索できる（SQLインジェクション対策が効いている）
- [ ] ユーザー入力が安全に表示される（XSS対策が効いている）
- [ ] CSRF保護が効いている（`@csrf`を削除すると419エラーになる）
- [ ] ログアウトができる

---

## ✨ 完成！

お疲れさまでした！これで、**セキュリティを意識したブログシステム**が完成しました。

このハンズオンで学んだセキュリティ対策は、すべてのWebアプリケーション開発で必須の知識です。今後のプロジェクトでも、必ず実践してください。

---
