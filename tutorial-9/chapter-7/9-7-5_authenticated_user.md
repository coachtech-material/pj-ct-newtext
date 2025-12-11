# Tutorial 9-7-5: 認証済みユーザーの取得とミドルウェア

## 🎯 このセクションで学ぶこと

*   `auth()`ヘルパーを使って、認証済みユーザーを取得できるようになる。
*   `auth`ミドルウェアを使って、ルートを保護できるようになる。
*   認証済みユーザーのみがアクセスできる機能を実装できるようになる。

---

## 導入：「ログイン済みかどうか」を判定する

前のセクションで、ログイン・ログアウト機能を実装しました。次は、**認証済みユーザーを取得**し、**認証済みユーザーのみがアクセスできるルート**を作成します。

このセクションでは、`auth()`ヘルパーと`auth`ミドルウェアを使って、これらの機能を実装します。

---

## 詳細解説

### 🔍 認証済みユーザーの取得

#### 方法1: `auth()`ヘルパー

```php
$user = auth()->user();

if ($user) {
    echo 'ログイン済み: ' . $user->name;
} else {
    echo '未ログイン';
}
```

---

#### 方法2: `Auth`ファサード

```php
use Illuminate\Support\Facades\Auth;

$user = Auth::user();
```

---

#### 方法3: `$request->user()`

```php
public function show(Request $request)
{
    $user = $request->user();
    
    return response()->json(['user' => $user]);
}
```

---

### 🔍 ログイン状態の確認

#### `auth()->check()`

```php
if (auth()->check()) {
    echo 'ログイン済み';
} else {
    echo '未ログイン';
}
```

---

#### `auth()->guest()`

```php
if (auth()->guest()) {
    echo '未ログイン';
} else {
    echo 'ログイン済み';
}
```

---

### 🔐 `auth`ミドルウェア

`auth`ミドルウェアを使うことで、**認証済みユーザーのみがアクセスできるルート**を作成できます。

#### ルートに適用

```php
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/profile', [ProfileController::class, 'show']);
    Route::put('/profile', [ProfileController::class, 'update']);
    Route::delete('/profile', [ProfileController::class, 'destroy']);
});
```

**コードリーディング**

*   `auth:sanctum`: Sanctumの認証ミドルウェア
*   このルートグループ内のルートは、認証済みユーザーのみがアクセスできる

---

#### 個別のルートに適用

```php
Route::get('/dashboard', [DashboardController::class, 'index'])
    ->middleware('auth:sanctum');
```

---

### 🚀 実践例1: プロフィール取得

#### コントローラー

```php
public function show(Request $request)
{
    $user = $request->user();
    
    return response()->json(['user' => $user]);
}
```

#### ルート

```php
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/profile', [ProfileController::class, 'show']);
});
```

#### Postmanでテスト

```
GET http://localhost/api/profile
Authorization: Bearer 2|xyz789...
```

#### レスポンス

```json
{
    "user": {
        "id": 1,
        "name": "山田太郎",
        "email": "yamada@example.com",
        "created_at": "2024-01-01T00:00:00.000000Z",
        "updated_at": "2024-01-01T00:00:00.000000Z"
    }
}
```

---

### 🚀 実践例2: プロフィール更新

#### コントローラー

```php
public function update(Request $request)
{
    $validated = $request->validate([
        'name' => 'required|string|max:255',
        'email' => 'required|email|unique:users,email,' . $request->user()->id,
    ]);

    $user = $request->user();
    $user->update($validated);

    return response()->json([
        'message' => 'Profile updated successfully',
        'user' => $user,
    ]);
}
```

---

### 🚀 実践例3: 投稿の作成

#### コントローラー

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'content' => 'required|string',
    ]);

    $post = $request->user()->posts()->create($validated);

    return response()->json([
        'message' => 'Post created successfully',
        'post' => $post,
    ], 201);
}
```

**コードリーディング**

*   `$request->user()->posts()->create()`: 認証済みユーザーの投稿として作成

---

### 🚀 実践例4: 自分の投稿のみ更新を許可

#### コントローラー

```php
public function update(Request $request, $id)
{
    $post = Post::findOrFail($id);

    // 自分の投稿かチェック
    if ($post->user_id !== $request->user()->id) {
        return response()->json([
            'message' => 'Unauthorized',
        ], 403);
    }

    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'content' => 'required|string',
    ]);

    $post->update($validated);

    return response()->json([
        'message' => 'Post updated successfully',
        'post' => $post,
    ]);
}
```

---

### 💡 TIP: `auth()->id()`

認証済みユーザーのIDのみを取得する場合は、`auth()->id()`を使います。

```php
$userId = auth()->id();

$posts = Post::where('user_id', $userId)->get();
```

---

### 🔍 Web版の認証

#### ルート

```php
Route::middleware('auth')->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
    Route::get('/profile', [ProfileController::class, 'show']);
});
```

#### コントローラー

```php
public function index()
{
    $user = auth()->user();
    
    $posts = $user->posts()->latest()->take(5)->get();
    
    return view('dashboard', compact('user', 'posts'));
}
```

---

### 🔍 Bladeテンプレートでの認証チェック

#### `@auth`ディレクティブ

```blade
@auth
    <p>ようこそ、{{ auth()->user()->name }}さん</p>
    <a href="/logout">ログアウト</a>
@endauth

@guest
    <a href="/login">ログイン</a>
    <a href="/register">新規登録</a>
@endguest
```

---

### 🚀 実践例5: ダッシュボード

#### コントローラー

```php
public function dashboard(Request $request)
{
    $user = $request->user();
    
    $stats = [
        'total_posts' => $user->posts()->count(),
        'published_posts' => $user->posts()->where('is_published', true)->count(),
        'draft_posts' => $user->posts()->where('is_published', false)->count(),
        'total_comments' => $user->comments()->count(),
    ];

    $latestPosts = $user->posts()->latest()->take(5)->get();

    return response()->json([
        'user' => $user,
        'stats' => $stats,
        'latest_posts' => $latestPosts,
    ]);
}
```

---

### 💡 TIP: カスタムガード

複数の認証方法を使う場合、カスタムガードを定義できます。

**`config/auth.php`**

```php
'guards' => [
    'web' => [
        'driver' => 'session',
        'provider' => 'users',
    ],

    'api' => [
        'driver' => 'sanctum',
        'provider' => 'users',
    ],

    'admin' => [
        'driver' => 'session',
        'provider' => 'admins',
    ],
],
```

**使用例**

```php
$user = auth('admin')->user();

Route::middleware('auth:admin')->group(function () {
    // 管理者のみがアクセスできるルート
});
```

---

### 🚨 よくある間違い

#### 間違い1: 認証チェックをせずに`auth()->user()`を使う

```php
$user = auth()->user();
echo $user->name; // ログインしていない場合、エラーになる
```

**対処法**: 認証チェックをします。

```php
if (auth()->check()) {
    $user = auth()->user();
    echo $user->name;
}
```

---

#### 間違い2: `auth`ミドルウェアを使わずに手動でチェック

```php
public function show(Request $request)
{
    if (!auth()->check()) {
        return response()->json(['message' => 'Unauthenticated'], 401);
    }
    
    // 処理
}
```

**対処法**: `auth`ミドルウェアを使います。

```php
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/profile', [ProfileController::class, 'show']);
});
```

---

## ✨ まとめ

このセクションでは、認証済みユーザーの取得とミドルウェアについて学びました。

*   `auth()->user()`を使って、認証済みユーザーを取得できる。
*   `auth()->check()`を使って、ログイン状態を確認できる。
*   `auth`ミドルウェアを使って、認証済みユーザーのみがアクセスできるルートを作成できる。
*   `$request->user()`を使って、コントローラー内で認証済みユーザーを取得できる。

これで、Chapter 7「認証機能」の全5セクションが完了しました。次は、Chapter 8「HTTPライフサイクルとミドルウェア」の残りのセクションを執筆します。

---

## 📝 学習のポイント

- [ ] `auth()->user()`を使って、認証済みユーザーを取得できる。
- [ ] `auth()->check()`を使って、ログイン状態を確認できる。
- [ ] `auth`ミドルウェアを使って、ルートを保護できる。
- [ ] `$request->user()`を使って、コントローラー内で認証済みユーザーを取得できる。
