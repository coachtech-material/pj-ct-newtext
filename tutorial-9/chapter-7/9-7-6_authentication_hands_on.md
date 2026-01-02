# Tutorial 9-7-6: 認証機能 - ハンズオン演習

## 📝 このセクションの目的

Chapter 7で学んだ認証機能を実際に手を動かして確認します。ログイン・ログアウト機能を実装し、認証が必要なページを作成しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 🎯 演習課題：マイページ機能の実装

### 📋 要件

1. ログイン・ログアウト機能を実装
2. `/mypage`にマイページを作成（認証必須）
3. 未ログイン時はログインページにリダイレクト
4. マイページにユーザー情報を表示

---

## 💡 ヒント

```bash
php artisan make:controller AuthController
```

```php
// ログイン
if (Auth::attempt(['email' => $email, 'password' => $password])) {
    return redirect('/mypage');
}

// ログアウト
Auth::logout();

// 認証済みユーザー取得
$user = Auth::user();

// ミドルウェア
Route::get('/mypage', [MypageController::class, 'index'])->middleware('auth');
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？認証機能はWebアプリケーションの核心機能です。一緒に手を動かしながら、マイページ機能を実装していきましょう。

### 💭 実装の思考プロセス

認証機能を実装する際、以下の順番で考えると効率的です：

1. **認証コントローラーを作成**：ログイン、ログアウトのロジックを実装
2. **ログインフォームを作成**：メールとパスワードでログイン
3. **マイページコントローラーを作成**：認証済みユーザー情報を表示
4. **ミドルウェアで認証を制御**：未ログイン時はリダイレクト
5. **ルートを定義**：ログイン、ログアウト、マイページのルート

認証のポイントは「Authファサードとミドルウェアで安全に認証を管理する」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: 認証コントローラーを作成する

**何を考えているか**：
- 「ログインとログアウトの処理をまとめよう」
- 「AuthControllerで認証関連のロジックを管理しよう」

ターミナルで以下のコマンドを実行します：

```bash
php artisan make:controller AuthController
```

`app/Http/Controllers/AuthController.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class AuthController extends Controller
{
    public function showLoginForm()
    {
        return view('auth.login');
    }

    public function login(Request $request)
    {
        $credentials = $request->only('email', 'password');

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();
            return redirect()->intended('/mypage');
        }

        return back()->withErrors([
            'email' => 'メールアドレスまたはパスワードが正しくありません',
        ]);
    }

    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        return redirect('/');
    }
}
```

**コードリーディング**：

```php
use Illuminate\Support\Facades\Auth;
```
→ `Auth`ファサードをインポートします。認証機能を使用するために必要です。

```php
public function showLoginForm()
{
    return view('auth.login');
}
```
→ ログインフォームを表示します。

```php
$credentials = $request->only('email', 'password');
```
→ リクエストからメールとパスワードだけを取得します。`only()`で必要なフィールドだけを抽出します。

```php
if (Auth::attempt($credentials)) {
    $request->session()->regenerate();
    return redirect()->intended('/mypage');
}
```
→ `Auth::attempt()`で認証を試みます。成功したらセッションを再生成し、マイページにリダイレクトします。`intended()`で元々アクセスしようとしたページに戻ります。

```php
return back()->withErrors([
    'email' => 'メールアドレスまたはパスワードが正しくありません',
]);
```
→ 認証失敗時はエラーメッセージを持って前のページに戻ります。

```php
public function logout(Request $request)
{
    Auth::logout();
    $request->session()->invalidate();
    $request->session()->regenerateToken();
    return redirect('/');
}
```
→ `Auth::logout()`でログアウトし、セッションを無効化し、CSRFトークンを再生成します。セキュリティ対策として重要です。

---

#### ステップ2: マイページコントローラーを作成する

**何を考えているか**：
- 「認証済みユーザーの情報を表示したい」
- 「Auth::user()でログイン中のユーザーを取得しよう」

ターミナルで以下のコマンドを実行します：

```bash
php artisan make:controller MypageController
```

`app/Http/Controllers/MypageController.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class MypageController extends Controller
{
    public function index()
    {
        $user = Auth::user();
        return view('mypage', compact('user'));
    }
}
```

**コードリーディング**：

```php
$user = Auth::user();
```
→ `Auth::user()`で現在ログイン中のユーザーを取得します。ユーザーモデルのインスタンスが返されます。

```php
return view('mypage', compact('user'));
```
→ ユーザー情報をビューに渡します。

---

#### ステップ3: ルートを定義する

**何を考えているか**：
- 「ログイン、ログアウト、マイページのルートを設定しよう」
- 「マイページにはauthミドルウェアを適用しよう」

`routes/web.php`を開いて、以下を追加します：

```php
use App\Http\Controllers\AuthController;
use App\Http\Controllers\MypageController;

// ログインフォーム表示
Route::get('/login', [AuthController::class, 'showLoginForm'])->name('login');
// ログイン処理
Route::post('/login', [AuthController::class, 'login']);
// ログアウト
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

// マイページ（認証必須）
Route::get('/mypage', [MypageController::class, 'index'])->middleware('auth');
```

**コードリーディング**：

```php
Route::get('/login', [AuthController::class, 'showLoginForm'])->name('login');
```
→ ログインフォームのルートを定義します。`name('login')`で名前付きルートとして登録します。

```php
Route::post('/login', [AuthController::class, 'login']);
```
→ ログイン処理のルートを定義します。POSTメソッドでフォームデータを受け取ります。

```php
Route::get('/mypage', [MypageController::class, 'index'])->middleware('auth');
```
→ マイページのルートを定義し、`middleware('auth')`で認証を必須にします。未ログイン時は自動的にログインページにリダイレクトされます。

---

#### ステップ4: ビューを作成する

**何を考えているか**：
- 「ログインフォームとマイページを作ろう」
- 「ログインフォームには@csrfを必ず追加しよう」

`resources/views/auth/login.blade.php`を作成します：

```blade
<h1>ログイン</h1>
<form action="{{ route('login') }}" method="POST">
    @csrf
    <div>
        <label>メールアドレス</label>
        <input type="email" name="email" value="{{ old('email') }}">
        @error('email')
            <p class="error">{{ $message }}</p>
        @enderror
    </div>
    <div>
        <label>パスワード</label>
        <input type="password" name="password">
    </div>
    <button type="submit">ログイン</button>
</form>
```

`resources/views/mypage.blade.php`を作成します：

```blade
<h1>マイページ</h1>
<p>ようこそ、{{ $user->name }}さん</p>
<p>メール: {{ $user->email }}</p>

<form action="{{ route('logout') }}" method="POST">
    @csrf
    <button type="submit">ログアウト</button>
</form>
```

**コードリーディング**：

```blade
<form action="{{ route('login') }}" method="POST">
    @csrf
```
→ フォームには必ず`@csrf`トークンを追加します。CSRF攻撃を防ぐために必須です。

```blade
<p>ようこそ、{{ $user->name }}さん</p>
```
→ ログイン中のユーザー名を表示します。`Auth::user()`で取得したユーザー情報を使用します。

---

### ✨ 完成！

これで認証機能が実装できました！ログイン、ログアウト、認証必須ページを作成できましたね。

---

## 📖 模範解答

### AuthController.php

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class AuthController extends Controller
{
    public function showLoginForm()
    {
        return view('auth.login');
    }

    public function login(Request $request)
    {
        $credentials = $request->only('email', 'password');

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();
            return redirect()->intended('/mypage');
        }

        return back()->withErrors([
            'email' => 'メールアドレスまたはパスワードが正しくありません',
        ]);
    }

    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        return redirect('/');
    }
}
```

### MypageController.php

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class MypageController extends Controller
{
    public function index()
    {
        $user = Auth::user();
        return view('mypage.index', ['user' => $user]);
    }
}
```

### routes/web.php

```php
use App\Http\Controllers\AuthController;
use App\Http\Controllers\MypageController;

Route::get('/login', [AuthController::class, 'showLoginForm'])->name('login');
Route::post('/login', [AuthController::class, 'login']);
Route::post('/logout', [AuthController::class, 'logout']);

Route::get('/mypage', [MypageController::class, 'index'])->middleware('auth');
```

### auth/login.blade.php

```blade
@extends('layouts.app')

@section('content')
<div class="container">
    <h1>ログイン</h1>
    
    <form action="{{ route('login') }}" method="POST">
        @csrf
        <div class="mb-3">
            <label>メールアドレス</label>
            <input type="email" name="email" class="form-control" value="{{ old('email') }}" required>
            @error('email')
                <p class="text-danger">{{ $message }}</p>
            @enderror
        </div>
        <div class="mb-3">
            <label>パスワード</label>
            <input type="password" name="password" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary">ログイン</button>
    </form>
</div>
@endsection
```

### mypage/index.blade.php

```blade
@extends('layouts.app')

@section('content')
<div class="container">
    <h1>マイページ</h1>
    
    <div class="card">
        <div class="card-body">
            <h2>ユーザー情報</h2>
            <p>名前: {{ $user->name }}</p>
            <p>メールアドレス: {{ $user->email }}</p>
        </div>
    </div>
    
    <form action="/logout" method="POST" class="mt-3">
        @csrf
        <button type="submit" class="btn btn-secondary">ログアウト</button>
    </form>
</div>
@endsection
```

---

## 💪 自己評価チェックリスト

- [ ] ログイン機能を実装できた
- [ ] ログアウト機能を実装できた
- [ ] authミドルウェアを使えた
- [ ] Auth::user()でユーザー情報を取得できた
- [ ] 未ログイン時にリダイレクトできた

すべてチェックできたら、Chapter 8に進みましょう！
