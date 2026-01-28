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

**コードリーディング（コントローラー）**：

| コード | 説明 |
|:---|:---|
| `$request->user()` | 現在ログインしているユーザーの情報を取得します |
| `view('profile.show', ...)` | 表示するビュー（resources/views/profile/show.blade.php）を指定します |
| `['user' => $user]` | ビュー側で `$user` 変数として使えるようにデータを渡します |


#### ルート

```php
Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'show'])->name('profile.show');
});
```

**コードリーディング（ルート）**：

| コード | 説明 |
|:---|:---|
| `middleware('auth')` | ログインしていないユーザーを制限し、ログイン画面へ誘導します |
| `group(function () { ... })` | グループ内のルートすべてに特定の条件（今回は認証）を一括適用します |
| `[ProfileController::class, 'show']` | アクセス時に ProfileController の show メソッドを呼び出します |
| `name('profile.show')` | ルートに名前を付けます。ビューなどで `route('profile.show')` として呼び出せます |

#### ビュー（profile/show.blade.php）

```blade
<h1>プロフィール</h1>
<p>名前: {{ $user->name }}</p>
<p>メールアドレス: {{ $user->email }}</p>
<p>登録日: {{ $user->created_at->format('Y年m月d日') }}</p>
```

**コードリーディング（ビュー）**：

| コード | 説明 |
|:---|:---|
| `{{ $user->name }}` | 変数の内容を安全に表示（エスケープ処理）します |
| `$user->created_at` | 登録日時データです。Laravelでは自動的にCarbonインスタンスとして扱われます |
| `format('Y年m月d日')` | 日付データを「2024年01月01日」のような形式に整えて表示します |

---

### 🚀 実践例2: 投稿の作成

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

**コードリーディング（コントローラー）**：

| コード | 説明 |
|:---|:---|
| `$request->validate([...])` | 入力データのバリデーション（検証）を行い、不備があれば自動で元の画面へ戻します |
| `$validated` | バリデーションを通過した「安全なデータ」のみが配列として代入されます |
| `$request->user()->posts()` | ログイン中のユーザーに紐づく「投稿（posts）」のリレーションを取得します |
| `create($validated)` | リレーションを介して、ユーザーIDを自動で紐付けた状態で新しいレコードを保存します |
| `redirect()->route('...', $post)` | 処理完了後、指定したルート（詳細画面など）へ移動させます。`$post` を渡すことでIDが自動で補完されます |
| `with('success', '...')` | セッションに一度だけ表示する「フラッシュメッセージ」を保存します |

> **💡 ポイント**: このメソッドチェーンでは、`user_id`が自動的に設定されます。`$request->user()`で取得したユーザーの投稿として作成されるため、手動で`user_id`を指定する必要はありません。

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

### 🚀 実践例3: ダッシュボード

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

**コードリーディング（コントローラー）**：

| コード | 説明 |
|:---|:---|
| `$user->posts()->count()` | リレーションを活用し、そのユーザーが作成した投稿の総数を取得します |
| `where('is_published', true)` | カラムの値を指定して、公開済みのレコードのみに絞り込みます |
| `latest()` | `created_at`（作成日時）の降順（新しい順）で並べ替えます |
| `take(5)->get()` | 指定した件数（今回は5件）だけデータを取得します |
| `compact('user', 'stats', 'latestPosts')` | 引数に渡した文字列と同じ名前の変数（$userなど）をまとめて配列にしてビューに渡します |

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

**コードリーディング（ビュー）**：

| コード | 説明 |
|:---|:---|
| `$stats['total_posts']` | コントローラーから渡された連想配列 `stats` の各キーの値を表示します |
| `@forelse ($latestPosts as $post)` | ループ処理を行います。データが存在しない場合の処理（@empty）も一緒に書ける便利な構文です |
| `$post->title` | ループ中の各投稿（Postモデルのインスタンス）のタイトルを表示します |
| `format('Y/m/d')` | 日付を「2024/01/01」のようなスラッシュ区切りの形式に変換します |
| `@empty` | 繰り返し対象のデータ（今回は $latestPosts）が空だった場合に実行されるブロックです |
| `@endforelse` | `@forelse` の範囲がここで終了することを示します |

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
