# Tutorial 10-1-5: 認証済みユーザーの取得とミドルウェア

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

認証済みユーザーを取得する方法は主に3つあります。どれも同じ結果を返しますが、書き方が異なります。

#### 方法1: `auth()`ヘルパー

```php
$user = auth()->user();

if ($user) {
    echo 'ログイン済み: ' . $user->name;
} else {
    echo '未ログイン';
}
```

**コードリーディング（1行ずつ分解）**

| コード | 演算子 | 意味 |
|:---|:---:|:---|
| `auth()` | - | 認証ヘルパー関数を呼び出し、AuthManagerインスタンスを取得 |
| `->user()` | `->` | インスタンスの`user()`メソッドを呼び出し、認証済みユーザーを取得 |
| `$user->name` | `->` | Userインスタンスのnameプロパティにアクセス |

> **💡 Tutorial 7の復習**: `auth()->user()`は、`auth()`が返すインスタンスに対して`->`で`user()`メソッドを呼び出しています。これはTutorial 7で学んだ「オブジェクトのメソッドを呼び出す」構文と同じです。

---

#### 方法2: `Auth`ファサード

```php
use Illuminate\Support\Facades\Auth;

$user = Auth::user();
```

**コードリーディング**

| コード | 演算子 | 意味 |
|:---|:---:|:---|
| `Auth::user()` | `::` | Authファサードの静的メソッドを呼び出し |

> **💡 `auth()->user()`と`Auth::user()`の違い**
> - `auth()->user()`: ヘルパー関数を使用（`->`を使う）
> - `Auth::user()`: ファサードを使用（`::`を使う）
> 
> どちらも同じ結果を返しますが、`auth()`ヘルパーの方が短く書けます。

---

#### 方法3: `$request->user()`

```php
public function show(Request $request)
{
    $user = $request->user();
    
    return view('profile', ['user' => $user]);
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
Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'show']);
    Route::put('/profile', [ProfileController::class, 'update']);
    Route::delete('/profile', [ProfileController::class, 'destroy']);
});
```

**コードリーディング**

*   `auth`: 認証ミドルウェア（セッションベース認証）
*   このルートグループ内のルートは、認証済みユーザーのみがアクセスできる
*   ログインしていない場合、自動的に`/login`にリダイレクトされる

---

#### 個別のルートに適用

```php
Route::get('/dashboard', [DashboardController::class, 'index'])
    ->middleware('auth');
```

---

### 🚀 実践例1: プロフィール取得

#### コントローラー

```php
public function show(Request $request)
{
    $user = $request->user();
    
    return view('profile.show', ['user' => $user]);
}
```

#### ルート

```php
Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'show'])->name('profile.show');
});
```

#### ビュー（profile/show.blade.php）

```blade
<h1>プロフィール</h1>
<p>名前: {{ $user->name }}</p>
<p>メールアドレス: {{ $user->email }}</p>
<p>登録日: {{ $user->created_at->format('Y年m月d日') }}</p>
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

    return redirect()->route('profile.show')
        ->with('success', 'プロフィールを更新しました');
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

    return redirect()->route('posts.show', $post)
        ->with('success', '投稿を作成しました');
}
```

**コードリーディング（メソッドチェーンの分解）**

`$request->user()->posts()->create($validated)` を分解してみましょう。

| ステップ | コード | 演算子 | 戻り値 | 意味 |
|:---:|:---|:---:|:---|:---|
| 1 | `$request->user()` | `->` | Userインスタンス | 認証済みユーザーを取得 |
| 2 | `->posts()` | `->` | クエリビルダ | ユーザーの投稿リレーションを取得 |
| 3 | `->create($validated)` | `->` | Postインスタンス | 新しい投稿を作成してDBに保存 |

> **💡 ポイント**: このメソッドチェーンでは、`user_id`が自動的に設定されます。`$request->user()`で取得したユーザーの投稿として作成されるため、手動で`user_id`を指定する必要はありません。

---

### 🚀 実践例4: 自分の投稿のみ更新を許可

#### コントローラー

```php
public function update(Request $request, $id)
{
    $post = Post::findOrFail($id);

    // 自分の投稿かチェック
    if ($post->user_id !== $request->user()->id) {
        abort(403, '権限がありません');
    }

    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'content' => 'required|string',
    ]);

    $post->update($validated);

    return redirect()->route('posts.show', $post)
        ->with('success', '投稿を更新しました');
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

### 🔍 Bladeテンプレートでの認証チェック

#### `@auth`ディレクティブ

```blade
@auth
    <p>ようこそ、{{ auth()->user()->name }}さん</p>
    <form method="POST" action="{{ route('logout') }}">
        @csrf
        <button type="submit">ログアウト</button>
    </form>
@endauth

@guest
    <a href="{{ route('login') }}">ログイン</a>
    <a href="{{ route('register') }}">新規登録</a>
@endguest
```

**コードリーディング**

*   `@auth ... @endauth`: ログインしている場合のみ表示
*   `@guest ... @endguest`: ログインしていない場合のみ表示
*   `auth()->user()`: ログインしているユーザーを取得

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

    return view('dashboard', compact('user', 'stats', 'latestPosts'));
}
```

**コードリーディング（メソッドチェーンの分解）**

`$user->posts()->latest()->take(5)->get()` を分解してみましょう。

| ステップ | コード | 演算子 | 戻り値 | 意味 |
|:---:|:---|:---:|:---|:---|
| 1 | `$user->posts()` | `->` | クエリビルダ | ユーザーの投稿リレーションを取得 |
| 2 | `->latest()` | `->` | クエリビルダ | 新しい順に並び替え |
| 3 | `->take(5)` | `->` | クエリビルダ | 5件に制限 |
| 4 | `->get()` | `->` | Collection | 結果を取得 |

> **💡 ポイント**: `posts()`はメソッド呼び出し（`()`あり）なのでクエリビルダが返り、その後に追加の条件を付けられます。もし`$user->posts`（`()`なし）と書くと、全ての投稿が取得されてしまいます。

#### ビュー（dashboard.blade.php）

```blade
<h1>ダッシュボード</h1>

<div class="stats">
    <p>総投稿数: {{ $stats['total_posts'] }}</p>
    <p>公開済み: {{ $stats['published_posts'] }}</p>
    <p>下書き: {{ $stats['draft_posts'] }}</p>
</div>

<h2>最新の投稿</h2>
@forelse ($latestPosts as $post)
    <div class="post">
        <h3>{{ $post->title }}</h3>
        <p>{{ $post->created_at->format('Y/m/d') }}</p>
    </div>
@empty
    <p>投稿がありません</p>
@endforelse
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

    'admin' => [
        'driver' => 'session',
        'provider' => 'admins',
    ],
],
```

**使用例**

```php
$admin = auth('admin')->user();

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

**対処法**: 認証チェックをするか、`auth`ミドルウェアを使います。

```php
// 方法1: 認証チェック
if (auth()->check()) {
    $user = auth()->user();
    echo $user->name;
}

// 方法2: authミドルウェアを使う（推奨）
Route::middleware('auth')->group(function () {
    // このルート内では auth()->user() は必ず存在する
});
```

---

#### 間違い2: `auth`ミドルウェアを使わずに手動でチェック

```php
public function show(Request $request)
{
    if (!auth()->check()) {
        return redirect('/login');
    }
    
    // 処理
}
```

**対処法**: `auth`ミドルウェアを使います。

```php
Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'show']);
});
```

---

## ✨ まとめ

このセクションでは、認証済みユーザーの取得とミドルウェアについて学びました。

*   `auth()->user()`を使って、認証済みユーザーを取得できる
*   `auth()->check()`を使って、ログイン状態を確認できる
*   `auth`ミドルウェアを使って、認証済みユーザーのみがアクセスできるルートを作成できる
*   `$request->user()`を使って、コントローラー内で認証済みユーザーを取得できる
*   `@auth` / `@guest`ディレクティブで、ログイン状態に応じた表示ができる

これで、Chapter 1「認証機能」の全5セクションが完了しました。次のセクションでは、ハンズオンで実際に認証機能を実装します。

---
