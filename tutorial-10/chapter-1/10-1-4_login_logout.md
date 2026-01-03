# Tutorial 10-1-4: ログイン・ログアウト機能の実装

## 🎯 このセクションで学ぶこと

*   Laravel Fortifyを使って、ログイン機能を実装できるようになる。
*   ログアウト機能を実装できるようになる。
*   セッションベース認証の仕組みを理解する。

---

## 導入：「ログイン」と「ログアウト」

前のセクションで、ユーザー登録機能を実装しました。次は、**ログイン機能**と**ログアウト機能**を実装します。

*   **ログイン**: ユーザーがメールアドレスとパスワードを入力し、認証される
*   **ログアウト**: ユーザーが認証状態を解除する

このセクションでは、Laravel Fortifyを使って、これらの機能を実装します。

---

## 詳細解説

### 📝 ログインの流れ

Fortifyを使ったログインは、以下の流れで行われます：

```
1. ユーザーが /login にアクセス
   ↓
2. FortifyServiceProviderで指定したビューが表示される
   ↓
3. ユーザーがメールアドレスとパスワードを入力してPOST
   ↓
4. Fortifyが認証処理を実行
   ↓
5. 成功: セッションを作成し、リダイレクト
   失敗: エラーメッセージを表示
```

**重要なポイント**：

*   **コントローラーを自作する必要がない**：Fortifyが内部で処理を行う
*   **セッションベース認証**：ログイン状態はセッションで管理される

---

### 🎨 ステップ1: ログインフォームのビューを作成する

`resources/views/auth/login.blade.php`を作成します：

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ログイン</title>
    <style>
        body { font-family: sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="email"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        .checkbox-group { display: flex; align-items: center; gap: 8px; }
        button { width: 100%; padding: 10px; background: #3490dc; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2779bd; }
        .error { color: red; font-size: 12px; margin-top: 5px; }
        .alert { background: #f8d7da; color: #721c24; padding: 10px; border-radius: 4px; margin-bottom: 15px; }
        .link { text-align: center; margin-top: 15px; }
    </style>
</head>
<body>
    <h1>ログイン</h1>
    
    @if (session('status'))
        <div class="alert">
            {{ session('status') }}
        </div>
    @endif
    
    <form method="POST" action="{{ route('login') }}">
        @csrf
        
        <div class="form-group">
            <label for="email">メールアドレス</label>
            <input type="email" id="email" name="email" value="{{ old('email') }}" required autofocus>
            @error('email')
                <p class="error">{{ $message }}</p>
            @enderror
        </div>
        
        <div class="form-group">
            <label for="password">パスワード</label>
            <input type="password" id="password" name="password" required>
            @error('password')
                <p class="error">{{ $message }}</p>
            @enderror
        </div>
        
        <div class="form-group checkbox-group">
            <input type="checkbox" id="remember" name="remember">
            <label for="remember">ログイン状態を保持する</label>
        </div>
        
        <button type="submit">ログイン</button>
    </form>
    
    <p class="link">
        <a href="{{ route('register') }}">アカウントをお持ちでない方はこちら</a>
    </p>
</body>
</html>
```

**コードリーディング**：

```blade
<form method="POST" action="{{ route('login') }}">
```
→ Fortifyが自動的に登録した`login`ルートにPOSTします。

```blade
<input type="checkbox" id="remember" name="remember">
```
→ 「ログイン状態を保持する」機能（Remember Me）。チェックすると、ブラウザを閉じてもログイン状態が維持されます。

```blade
@if (session('status'))
    <div class="alert">
        {{ session('status') }}
    </div>
@endif
```
→ パスワードリセット後などに表示されるステータスメッセージ。

---

### 🔧 ステップ2: FortifyServiceProviderでビューを指定する

前のセクションで設定済みですが、`boot`メソッドに`loginView`が設定されていることを確認します：

```php
public function boot(): void
{
    // ユーザー登録フォームのビューを指定
    Fortify::registerView(function () {
        return view('auth.register');
    });

    // ログインフォームのビューを指定
    Fortify::loginView(function () {
        return view('auth.login');
    });
}
```

---

### 🚀 ステップ3: 動作確認

#### ルートの確認

Fortifyが登録したルートを確認します：

```bash
sail artisan route:list --path=login
```

**出力例**：

```
GET|HEAD  login .......... Laravel\Fortify\Http\Controllers\AuthenticatedSessionController@create
POST      login .......... Laravel\Fortify\Http\Controllers\AuthenticatedSessionController@store
```

**重要なポイント**：

*   `routes/web.php`に何も書いていないのに、ルートが登録されている
*   Fortifyが内部でルートを定義している

#### ブラウザで確認

1. ブラウザで`http://localhost/login`にアクセス
2. ログインフォームが表示されることを確認
3. 登録済みのメールアドレスとパスワードを入力して「ログイン」ボタンをクリック
4. ログインが成功し、ダッシュボードに遷移することを確認

---

### 🔓 ログアウト機能の実装

#### ログアウトボタンの追加

ダッシュボードなどのビューに、ログアウトボタンを追加します：

```blade
<form method="POST" action="{{ route('logout') }}">
    @csrf
    <button type="submit">ログアウト</button>
</form>
```

**コードリーディング**：

```blade
<form method="POST" action="{{ route('logout') }}">
```
→ Fortifyが自動的に登録した`logout`ルートにPOSTします。

```blade
@csrf
```
→ CSRF対策のトークン。ログアウトもPOSTリクエストなので必要です。

#### ルートの確認

```bash
sail artisan route:list --path=logout
```

**出力例**：

```
POST      logout .......... Laravel\Fortify\Http\Controllers\AuthenticatedSessionController@destroy
```

---

### 🔐 セッションベース認証の仕組み

Fortifyが採用している**セッションベース認証**の仕組みを詳しく見てみましょう。

#### ログイン時の処理

```
1. ユーザーがメールアドレスとパスワードを送信
   ↓
2. Fortifyがデータベースでユーザーを検索
   ↓
3. パスワードをHash::check()で検証
   ↓
4. 認証成功: セッションにユーザーIDを保存
   ↓
5. セッションIDをCookieに保存してブラウザに返す
```

#### 認証済みリクエストの処理

```
1. ブラウザがCookieに含まれるセッションIDを送信
   ↓
2. Laravelがセッションからユーザー情報を復元
   ↓
3. Auth::user()でユーザー情報を取得できる
```

#### ログアウト時の処理

```
1. ユーザーがログアウトをリクエスト
   ↓
2. セッションを無効化
   ↓
3. CSRFトークンを再生成
   ↓
4. ログインページにリダイレクト
```

---

### 💡 TIP: Remember Me機能

「ログイン状態を保持する」にチェックを入れると、**Remember Me**機能が有効になります。

#### 仕組み

*   通常のセッション: ブラウザを閉じると終了
*   Remember Me: 長期間有効なトークンをCookieに保存

#### 設定

`config/auth.php`で、Remember Meの有効期限を設定できます：

```php
'providers' => [
    'users' => [
        'driver' => 'eloquent',
        'model' => App\Models\User::class,
    ],
],
```

---

### 🛡️ 認証ミドルウェア

ログインしていないユーザーを自動的にログインページにリダイレクトするには、**認証ミドルウェア**を使います。

#### ルートに認証ミドルウェアを適用

```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\DashboardController;

// 認証が必要なルート
Route::middleware('auth')->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index']);
});
```

**コードリーディング**：

*   `middleware('auth')`: このルートにアクセスするには、ログインが必要
*   ログインしていない場合、自動的に`/login`にリダイレクト

---

### 🔍 ログイン状態の確認

#### コントローラーで確認

```php
public function index(Request $request)
{
    // ログインしているユーザーを取得
    $user = $request->user();
    // または
    $user = Auth::user();

    return view('dashboard', ['user' => $user]);
}
```

#### Bladeで確認

```blade
@auth
    <p>ようこそ、{{ auth()->user()->name }}さん！</p>
    <form method="POST" action="{{ route('logout') }}">
        @csrf
        <button type="submit">ログアウト</button>
    </form>
@else
    <p><a href="{{ route('login') }}">ログイン</a>してください。</p>
@endauth
```

**コードリーディング**：

*   `@auth ... @endauth`: ログインしている場合のみ表示
*   `@else`: ログインしていない場合に表示
*   `auth()->user()`: ログインしているユーザーを取得

---

### 🚨 よくある間違い

#### 間違い1: ログアウトをGETリクエストで実装する

```blade
<a href="{{ route('logout') }}">ログアウト</a>  <!-- NG -->
```

**問題点**: GETリクエストでログアウトすると、CSRF攻撃のリスクがあります。

**対処法**: POSTリクエストを使います。

```blade
<form method="POST" action="{{ route('logout') }}">
    @csrf
    <button type="submit">ログアウト</button>
</form>
```

---

#### 間違い2: @csrfを忘れる

```blade
<form method="POST" action="{{ route('login') }}">
    <!-- @csrfがない -->
    <input type="email" name="email">
    <input type="password" name="password">
    <button type="submit">ログイン</button>
</form>
```

**問題点**: 419エラー（Page Expired）が発生します。

**対処法**: `@csrf`を必ず追加します。

---

### 🚀 実践例: ダッシュボードの作成

ログイン後に表示するダッシュボードを作成しましょう。

#### コントローラーの作成

```bash
sail artisan make:controller DashboardController
```

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class DashboardController extends Controller
{
    public function index(Request $request)
    {
        return view('dashboard', [
            'user' => $request->user(),
        ]);
    }
}
```

#### ルートの定義

```php
use App\Http\Controllers\DashboardController;

Route::middleware('auth')->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
});
```

#### ビューの作成

`resources/views/dashboard.blade.php`を作成します：

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ダッシュボード</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        .card { background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
        .logout-btn { background: #dc3545; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <h1>ダッシュボード</h1>
    
    <div class="card">
        <h2>ようこそ、{{ $user->name }}さん！</h2>
        <p>メールアドレス: {{ $user->email }}</p>
        <p>登録日: {{ $user->created_at->format('Y年m月d日') }}</p>
    </div>
    
    <form method="POST" action="{{ route('logout') }}">
        @csrf
        <button type="submit" class="logout-btn">ログアウト</button>
    </form>
</body>
</html>
```

---

## ✨ まとめ

このセクションでは、Laravel Fortifyを使って、ログイン・ログアウト機能を実装しました。

*   **Bladeファイル**を作成し、`FortifyServiceProvider`で指定した
*   **コントローラーを自作する必要がない**：Fortifyが内部で処理を行う
*   **セッションベース認証**：ログイン状態はセッションで管理される
*   **認証ミドルウェア**を使うと、ログインしていないユーザーを自動的にリダイレクトできる
*   **@auth / @endauth**ディレクティブで、ログイン状態に応じた表示ができる

次のセクションでは、認証済みユーザーの取得とミドルウェアについて詳しく学びます。

---
