# Tutorial 11-3-1: Sanctumによる認証実装

## 🎯 このセクションで学ぶこと

*   Laravel Sanctumを使った認証機能を実装する方法を学ぶ。
*   ユーザー登録、ログイン、ログアウト機能を実装する。
*   認証済みユーザーのみがタスクにアクセスできるようにする。

---

## 導入：なぜ認証が必要なのか

**認証（Authentication）**とは、**ユーザーが本人であることを確認する仕組み**です。

認証機能を実装することで、以下のようなことが可能になります。

*   **ユーザーごとにデータを管理**: 各ユーザーが自分のタスクのみを閲覧・編集できる
*   **セキュリティの向上**: 不正アクセスを防ぐ
*   **ユーザー体験の向上**: ログイン状態を保持し、毎回ログインする手間を省く

---

## 詳細解説

### 🔍 Laravel Sanctumとは

**Laravel Sanctum**は、**Laravelの公式認証パッケージ**です。

Sanctumは、以下の2つの認証方式をサポートしています。

1. **APIトークン認証**: モバイルアプリやSPAで使用
2. **セッション認証**: 従来のWebアプリケーションで使用

このセクションでは、**セッション認証**を使って認証機能を実装します。

---

### 🔍 Sanctumのインストール

Laravelプロジェクトを作成すると、Sanctumは既にインストールされています。

もしインストールされていない場合は、以下のコマンドを実行します。

```bash
composer require laravel/sanctum
```

---

### 🔍 Sanctumの設定

Sanctumの設定ファイルを公開します。

```bash
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
```

---

#### 実行結果

```
Copied File [/vendor/laravel/sanctum/config/sanctum.php] To [/config/sanctum.php]
Copied File [/vendor/laravel/sanctum/database/migrations/2019_12_14_000001_create_personal_access_tokens_table.php] To [/database/migrations/2019_12_14_000001_create_personal_access_tokens_table.php]
Publishing complete.
```

---

### 🔍 マイグレーションの実行

Sanctumのマイグレーションを実行します。

```bash
php artisan migrate
```

これで、`personal_access_tokens`テーブルが作成されます。

---

### 🔍 ユーザー登録機能の実装

#### ステップ1: ルーティングの設定

**ファイル**: `routes/web.php`

```php
<?php

use App\Http\Controllers\AuthController;
use App\Http\Controllers\TaskController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

// 認証関連
Route::get('/register', [AuthController::class, 'showRegisterForm'])->name('register');
Route::post('/register', [AuthController::class, 'register']);
Route::get('/login', [AuthController::class, 'showLoginForm'])->name('login');
Route::post('/login', [AuthController::class, 'login']);
Route::post('/logout', [AuthController::class, 'logout'])->name('logout');

// タスク関連（認証が必要）
Route::middleware('auth')->group(function () {
    Route::get('/tasks', [TaskController::class, 'index'])->name('tasks.index');
});
```

---

### 🔍 コードリーディング

#### `Route::middleware('auth')->group(function () { ... })`

*   `auth`ミドルウェアを適用したルートグループを作成します。
*   このグループ内のルートは、**認証済みユーザーのみがアクセスできる**ようになります。
*   未認証ユーザーがアクセスしようとすると、ログインページにリダイレクトされます。

---

#### ステップ2: AuthControllerの作成

```bash
php artisan make:controller AuthController
```

---

#### ステップ3: AuthControllerの実装

**ファイル**: `app/Http/Controllers/AuthController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;

class AuthController extends Controller
{
    /**
     * 登録フォームを表示
     */
    public function showRegisterForm()
    {
        return view('auth.register');
    }

    /**
     * ユーザー登録処理
     */
    public function register(Request $request)
    {
        $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|string|email|max:255|unique:users',
            'password' => 'required|string|min:8|confirmed',
        ]);

        $user = User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password),
        ]);

        Auth::login($user);

        return redirect()->route('tasks.index')->with('success', 'ユーザー登録が完了しました。');
    }

    /**
     * ログインフォームを表示
     */
    public function showLoginForm()
    {
        return view('auth.login');
    }

    /**
     * ログイン処理
     */
    public function login(Request $request)
    {
        $credentials = $request->validate([
            'email' => 'required|string|email',
            'password' => 'required|string',
        ]);

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();

            return redirect()->intended(route('tasks.index'))->with('success', 'ログインしました。');
        }

        return back()->withErrors([
            'email' => 'メールアドレスまたはパスワードが正しくありません。',
        ])->onlyInput('email');
    }

    /**
     * ログアウト処理
     */
    public function logout(Request $request)
    {
        Auth::logout();

        $request->session()->invalidate();
        $request->session()->regenerateToken();

        return redirect()->route('login')->with('success', 'ログアウトしました。');
    }
}
```

---

### 🔍 コードリーディング

#### `Hash::make($request->password)`

*   パスワードをハッシュ化します。
*   ハッシュ化することで、データベースに平文のパスワードを保存せず、セキュリティを向上させます。

---

#### `Auth::login($user)`

*   ユーザーをログイン状態にします。
*   セッションにユーザー情報が保存されます。

---

#### `Auth::attempt($credentials)`

*   メールアドレスとパスワードで認証を試みます。
*   認証に成功すると`true`を返し、ユーザーがログイン状態になります。
*   認証に失敗すると`false`を返します。

---

#### `$request->session()->regenerate()`

*   セッションIDを再生成します。
*   セッション固定攻撃（Session Fixation Attack）を防ぐためのセキュリティ対策です。

---

#### `redirect()->intended(route('tasks.index'))`

*   ユーザーが元々アクセスしようとしていたページにリダイレクトします。
*   元々アクセスしようとしていたページがない場合は、`tasks.index`にリダイレクトします。

---

#### `Auth::logout()`

*   ユーザーをログアウト状態にします。
*   セッションからユーザー情報が削除されます。

---

#### `$request->session()->invalidate()`

*   セッションを無効化します。

---

#### `$request->session()->regenerateToken()`

*   CSRFトークンを再生成します。

---

### 🔍 ビューの作成

#### 登録フォーム

**ファイル**: `resources/views/auth/register.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ユーザー登録</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        form {
            margin-top: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
        button {
            background-color: #4caf50;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
        .error {
            color: red;
            font-size: 14px;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <h1>ユーザー登録</h1>
    
    <form method="POST" action="{{ route('register') }}">
        @csrf
        
        <div class="form-group">
            <label for="name">名前</label>
            <input type="text" id="name" name="name" value="{{ old('name') }}" required>
            @error('name')
                <div class="error">{{ $message }}</div>
            @enderror
        </div>
        
        <div class="form-group">
            <label for="email">メールアドレス</label>
            <input type="email" id="email" name="email" value="{{ old('email') }}" required>
            @error('email')
                <div class="error">{{ $message }}</div>
            @enderror
        </div>
        
        <div class="form-group">
            <label for="password">パスワード</label>
            <input type="password" id="password" name="password" required>
            @error('password')
                <div class="error">{{ $message }}</div>
            @enderror
        </div>
        
        <div class="form-group">
            <label for="password_confirmation">パスワード（確認）</label>
            <input type="password" id="password_confirmation" name="password_confirmation" required>
        </div>
        
        <button type="submit">登録</button>
    </form>
    
    <p>既にアカウントをお持ちの方は<a href="{{ route('login') }}">こちら</a></p>
</body>
</html>
```

---

#### ログインフォーム

**ファイル**: `resources/views/auth/login.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ログイン</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        form {
            margin-top: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 8px;
            box-sizing: border-box;
        }
        button {
            background-color: #2196f3;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #0b7dda;
        }
        .error {
            color: red;
            font-size: 14px;
            margin-top: 5px;
        }
        .success {
            color: green;
            font-size: 14px;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <h1>ログイン</h1>
    
    @if(session('success'))
        <div class="success">{{ session('success') }}</div>
    @endif
    
    <form method="POST" action="{{ route('login') }}">
        @csrf
        
        <div class="form-group">
            <label for="email">メールアドレス</label>
            <input type="email" id="email" name="email" value="{{ old('email') }}" required>
            @error('email')
                <div class="error">{{ $message }}</div>
            @enderror
        </div>
        
        <div class="form-group">
            <label for="password">パスワード</label>
            <input type="password" id="password" name="password" required>
            @error('password')
                <div class="error">{{ $message }}</div>
            @enderror
        </div>
        
        <button type="submit">ログイン</button>
    </form>
    
    <p>アカウントをお持ちでない方は<a href="{{ route('register') }}">こちら</a></p>
</body>
</html>
```

---

### 🚀 実践: 認証機能を試そう

#### ステップ1: ユーザー登録

1. ブラウザで`http://localhost/register`にアクセス
2. 名前、メールアドレス、パスワードを入力
3. 「登録」ボタンをクリック
4. タスク一覧ページにリダイレクトされる

---

#### ステップ2: ログアウト

タスク一覧ページにログアウトボタンを追加します。

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<body>
    <h1>タスク一覧</h1>
    
    <form method="POST" action="{{ route('logout') }}" style="margin-bottom: 20px;">
        @csrf
        <button type="submit">ログアウト</button>
    </form>
    
    <!-- 以下、既存のコード -->
```

---

#### ステップ3: ログイン

1. ログアウトボタンをクリック
2. ログインページにリダイレクトされる
3. メールアドレスとパスワードを入力
4. 「ログイン」ボタンをクリック
5. タスク一覧ページにリダイレクトされる

---

### 💡 TIP: 認証済みユーザーの取得

認証済みユーザーの情報は、以下の方法で取得できます。

```php
// コントローラー
$user = Auth::user();
echo $user->name; // ユーザー名
echo $user->email; // メールアドレス
```

```blade
<!-- ビュー -->
{{ Auth::user()->name }}
{{ Auth::user()->email }}
```

---

### 🚨 よくある間違い

#### 間違い1: CSRFトークンを忘れる

**エラー**:

```
419 | Page Expired
```

**対処法**: フォームに`@csrf`を追加します。

---

#### 間違い2: パスワードをハッシュ化し忘れる

**対処法**: `Hash::make()`を使ってパスワードをハッシュ化します。

---

#### 間違い3: ミドルウェアを設定し忘れる

**対処法**: `Route::middleware('auth')`を使って、認証が必要なルートを保護します。

---

## ✨ まとめ

このセクションでは、Laravel Sanctumを使った認証機能の実装について学びました。

*   Laravel Sanctumを使って、ユーザー登録、ログイン、ログアウト機能を実装する。
*   `Hash::make()`を使って、パスワードをハッシュ化する。
*   `Auth::attempt()`を使って、認証を試みる。
*   `Route::middleware('auth')`を使って、認証が必要なルートを保護する。

次のセクションでは、リレーションシップの実装について学びます。

---

## 📝 学習のポイント

- [ ] Laravel Sanctumを使った認証機能を実装する方法を学んだ。
- [ ] ユーザー登録、ログイン、ログアウト機能を実装した。
- [ ] 認証済みユーザーのみがタスクにアクセスできるようにした。
