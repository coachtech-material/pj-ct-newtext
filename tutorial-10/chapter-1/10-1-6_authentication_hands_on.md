# Tutorial 10-1-6: 認証機能 - ハンズオン演習

## 📝 このセクションの目的

Chapter 1で学んだFortifyを使った認証機能を実際に手を動かして確認します。Fortifyの設定を行い、提供されたBladeファイルを読み解いて、認証が必要なページを作成しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 🎯 演習課題：Fortifyを使った認証機能の実装

### 📋 要件

1. Laravel Fortifyをインストールし、設定する
2. 提供されたBladeファイルを配置し、Fortifyで読み込む
3. `/dashboard`にダッシュボードを作成（認証必須）
4. 未ログイン時はログインページにリダイレクト
5. ダッシュボードにユーザー情報を表示

---

## 💡 ヒント

```bash
# Fortifyのインストール
sail composer require laravel/fortify
sail artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

```php
// FortifyServiceProvider.php
Fortify::loginView(function () {
    return view('auth.login');
});

Fortify::registerView(function () {
    return view('auth.register');
});

// ミドルウェア
Route::get('/dashboard', [DashboardController::class, 'index'])->middleware('auth');
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？Fortifyを使った認証機能はWebアプリケーションの核心機能です。一緒に手を動かしながら、認証機能を実装していきましょう。

### 💭 実装の思考プロセス

Fortifyを使った認証機能を実装する際、以下の順番で考えると効率的です：

1. **Fortifyをインストール**：Composerでインストールし、設定ファイルを公開
2. **Bladeファイルを配置**：提供されたログイン・登録フォームを配置
3. **FortifyServiceProviderを設定**：ビューを指定
4. **ダッシュボードを作成**：認証済みユーザー情報を表示
5. **ルートを定義**：認証ミドルウェアを適用

認証のポイントは「Fortifyがバックエンドの認証処理を担当し、フロントエンドは自由に設計できる」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: Fortifyをインストールする

**何を考えているか**：
- 「Fortifyをインストールして、認証のバックエンド処理を使えるようにしよう」
- 「設定ファイルとアクションクラスを公開しよう」

ターミナルで以下のコマンドを実行します：

```bash
# Fortifyをインストール
sail composer require laravel/fortify

# 設定ファイルとアクションクラスを公開
sail artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"

# マイグレーションを実行（まだの場合）
sail artisan migrate
```

**確認ポイント**：
- `config/fortify.php`が作成されていること
- `app/Actions/Fortify/`ディレクトリが作成されていること
- `app/Providers/FortifyServiceProvider.php`が作成されていること

---

#### ステップ2: Fortifyの設定を確認する

**何を考えているか**：
- 「どの機能を有効にするか確認しよう」
- 「ユーザー登録とログインを有効にしよう」

`config/fortify.php`を開いて、以下の設定を確認します：

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    // Features::emailVerification(),
],
```

**コードリーディング**：

```php
Features::registration()
```
→ ユーザー登録機能を有効化します。

```php
Features::resetPasswords()
```
→ パスワードリセット機能を有効化します。

---

#### ステップ3: Bladeファイルを配置する

**何を考えているか**：
- 「ログインフォームと登録フォームを作成しよう」
- 「Fortifyが自動的に登録したルートに対応するビューを作ろう」

ターミナルで以下のコマンドを実行して、ディレクトリを作成します：

```bash
mkdir -p resources/views/auth
```

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
        input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #3490dc; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2779bd; }
        .error { color: red; font-size: 12px; margin-top: 5px; }
        .link { text-align: center; margin-top: 15px; }
    </style>
</head>
<body>
    <h1>ログイン</h1>
    
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
        
        <button type="submit">ログイン</button>
    </form>
    
    <p class="link">
        <a href="{{ route('register') }}">アカウントをお持ちでない方はこちら</a>
    </p>
</body>
</html>
```

`resources/views/auth/register.blade.php`を作成します：

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ユーザー登録</title>
    <style>
        body { font-family: sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 10px; background: #3490dc; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2779bd; }
        .error { color: red; font-size: 12px; margin-top: 5px; }
        .link { text-align: center; margin-top: 15px; }
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
                <p class="error">{{ $message }}</p>
            @enderror
        </div>
        
        <div class="form-group">
            <label for="email">メールアドレス</label>
            <input type="email" id="email" name="email" value="{{ old('email') }}" required>
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
        
        <div class="form-group">
            <label for="password_confirmation">パスワード（確認）</label>
            <input type="password" id="password_confirmation" name="password_confirmation" required>
        </div>
        
        <button type="submit">登録</button>
    </form>
    
    <p class="link">
        <a href="{{ route('login') }}">すでにアカウントをお持ちの方はこちら</a>
    </p>
</body>
</html>
```

**コードリーディング**：

```blade
<form method="POST" action="{{ route('login') }}">
    @csrf
```
→ Fortifyが自動的に登録した`login`ルートにPOSTします。`@csrf`は必須です。

```blade
@error('email')
    <p class="error">{{ $message }}</p>
@enderror
```
→ バリデーションエラーがあれば、エラーメッセージを表示します。

---

#### ステップ4: FortifyServiceProviderを設定する

**何を考えているか**：
- 「Fortifyに、どのビューを使うか教えよう」
- 「loginViewとregisterViewを設定しよう」

`app/Providers/FortifyServiceProvider.php`を開いて、`boot`メソッドを以下のように編集します：

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Fortify\Fortify;

class FortifyServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        //
    }

    public function boot(): void
    {
        // ログインフォームのビューを指定
        Fortify::loginView(function () {
            return view('auth.login');
        });

        // ユーザー登録フォームのビューを指定
        Fortify::registerView(function () {
            return view('auth.register');
        });
    }
}
```

**コードリーディング**：

```php
Fortify::loginView(function () {
    return view('auth.login');
});
```
→ `/login`にGETリクエストが来たときに、`resources/views/auth/login.blade.php`を表示するよう指定します。

---

#### ステップ5: Fortifyが登録したルートを確認する

**何を考えているか**：
- 「Fortifyがどんなルートを自動的に登録したか確認しよう」
- 「routes/web.phpに何も書いていないのにルートが登録されているはず」

ターミナルで以下のコマンドを実行します：

```bash
sail artisan route:list
```

**出力例**：

```
GET|HEAD  login .......... Laravel\Fortify\Http\Controllers\AuthenticatedSessionController@create
POST      login .......... Laravel\Fortify\Http\Controllers\AuthenticatedSessionController@store
POST      logout .......... Laravel\Fortify\Http\Controllers\AuthenticatedSessionController@destroy
GET|HEAD  register .......... Laravel\Fortify\Http\Controllers\RegisteredUserController@create
POST      register .......... Laravel\Fortify\Http\Controllers\RegisteredUserController@store
```

**重要なポイント**：

*   `routes/web.php`に何も書いていないのに、ルートが登録されている
*   Fortifyが内部でルートを定義している
*   これがFortifyの「バックエンドの認証ロジックを提供する」という意味

---

#### ステップ6: ダッシュボードを作成する

**何を考えているか**：
- 「認証済みユーザーのみがアクセスできるページを作ろう」
- 「authミドルウェアを使って保護しよう」

ターミナルで以下のコマンドを実行します：

```bash
sail artisan make:controller DashboardController
```

`app/Http/Controllers/DashboardController.php`を開いて、以下のように編集します：

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

**コードリーディング**：

```php
$request->user()
```
→ 認証済みユーザーを取得します。`auth()->user()`と同じです。

---

#### ステップ7: ルートを定義する

**何を考えているか**：
- 「ダッシュボードのルートを定義しよう」
- 「authミドルウェアを適用しよう」

`routes/web.php`を開いて、以下を追加します：

```php
use App\Http\Controllers\DashboardController;

Route::middleware('auth')->group(function () {
    Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
});
```

**コードリーディング**：

```php
Route::middleware('auth')->group(function () {
```
→ このグループ内のルートは、認証済みユーザーのみがアクセスできます。

---

#### ステップ8: ダッシュボードのビューを作成する

**何を考えているか**：
- 「ユーザー情報を表示しよう」
- 「ログアウトボタンも追加しよう」

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

**コードリーディング**：

```blade
<form method="POST" action="{{ route('logout') }}">
    @csrf
    <button type="submit" class="logout-btn">ログアウト</button>
</form>
```
→ ログアウトはPOSTリクエストで行います。`@csrf`は必須です。

---

#### ステップ9: 動作確認

**何を考えているか**：
- 「実際に動作するか確認しよう」
- 「ユーザー登録 → ログイン → ダッシュボード → ログアウトの流れを確認しよう」

1. ブラウザで`http://localhost/register`にアクセス
2. ユーザー情報を入力して「登録」ボタンをクリック
3. 登録が成功し、ダッシュボードに遷移することを確認
4. ログアウトボタンをクリック
5. ログインページにリダイレクトされることを確認
6. 登録したメールアドレスとパスワードでログイン
7. ダッシュボードに遷移することを確認

---

### ✨ 完成！

これでFortifyを使った認証機能が実装できました！

**学んだこと**：

*   Fortifyはバックエンドの認証処理を提供する
*   フロントエンド（Bladeファイル）は自由に設計できる
*   ルートはFortifyが自動的に登録する
*   `sail artisan route:list`でルートを確認できる

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ Laravel Fortifyをインストールし、設定できた
- ✅ Bladeファイルを配置し、Fortifyで読み込めた
- ✅ 認証が必要なダッシュボードを作成できた
- ✅ Fortifyが自動的に登録するルートを確認できた

引き続き、次のChapterも頑張りましょう！

---
