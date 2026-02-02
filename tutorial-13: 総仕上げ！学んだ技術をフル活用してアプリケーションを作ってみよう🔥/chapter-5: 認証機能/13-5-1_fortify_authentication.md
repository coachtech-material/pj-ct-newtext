# 13-5-1 認証機能の実装（Fortify）

## 🎯 このセクションで学ぶこと

このセクションでは、Laravel Fortifyを使用してタスク管理アプリに認証機能を実装します。

- Laravel Fortifyのインストールと設定
- ユーザー登録機能の実装
- ログイン・ログアウト機能の実装
- 認証ビューの作成

> **📌 対応Issue**: #3 認証機能の実装（Fortify）

---

## 🧠 先輩エンジニアの思考プロセス

認証機能を実装する際、先輩エンジニアは以下のように考えます。

> 「認証機能は自分で実装すると複雑でセキュリティリスクも高い。Laravelには認証用のパッケージがいくつかあるが、今回はFortifyを使おう。FortifyはUIを持たないヘッドレスな認証パッケージなので、自分でビューを作成する必要があるが、その分カスタマイズしやすい。」

### Laravel認証パッケージの比較

| パッケージ | 特徴 | 向いている用途 |
|:---|:---|:---|
| **Fortify** | UIなし（ヘッドレス）、カスタマイズ自由 | 独自デザインの認証画面を作りたい場合 |
| Breeze | シンプルなUI付き、Tailwind CSS | 素早く認証機能を導入したい場合 |
| Jetstream | 高機能（チーム管理、2FA等）、Livewire/Inertia | 本格的なアプリケーション |

---

## 🔀 ブランチの作成

Issue駆動開発のワークフローに従い、まずはIssue #3に対応するブランチを作成します。

```bash
# 現在のブランチを確認（mainにいることを確認）
git branch

# mainブランチの最新状態を取得
git pull origin main

# Issue #3 に対応するブランチを作成して切り替え
git switch -c feature/issue-3-authentication
```

### コマンドのコードリーディング

| コマンド | 説明 |
|:---|:---|
| `git branch` | 現在のブランチ一覧を表示（`*`が付いているのが現在のブランチ） |
| `git pull origin main` | リモートのmainブランチの最新状態をローカルに取り込む |
| `git switch -c feature/issue-3-authentication` | 新しいブランチを作成して切り替え |

> **💡 ポイント**: 新しいブランチを作成する前に、必ず `git pull` でmainブランチを最新状態にしておきましょう。

---

## 🏃 実践

### ステップ1: Laravel Fortifyのインストール

Composerを使ってFortifyをインストールします。

```bash
# Fortifyのインストール
sail composer require laravel/fortify
```

#### コマンドのコードリーディング

| コマンド | 説明 |
|:---|:---|
| `sail composer` | Laravel Sailを使ってComposerコマンドを実行 |
| `require laravel/fortify` | Fortifyパッケージをインストール |

---

### ステップ2: Fortifyの設定ファイルを公開

Fortifyの設定ファイルとサービスプロバイダを公開します。

```bash
# 設定ファイルの公開
sail artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

このコマンドを実行すると、以下のファイルが作成されます。

| ファイル | 説明 |
|:---|:---|
| `config/fortify.php` | Fortifyの設定ファイル |
| `app/Providers/FortifyServiceProvider.php` | Fortifyのサービスプロバイダ |
| `app/Actions/Fortify/` | 認証アクション（登録、パスワードリセット等） |

---

### ステップ3: サービスプロバイダの登録

`bootstrap/providers.php` にFortifyServiceProviderを追加します。

```php
<?php

return [
    App\Providers\AppServiceProvider::class,
    App\Providers\FortifyServiceProvider::class,
];
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `App\Providers\FortifyServiceProvider::class` | Fortifyのサービスプロバイダを登録 |

---

### ステップ4: Fortifyの設定

`config/fortify.php` を確認し、必要な機能を有効にします。

```php
<?php

use Laravel\Fortify\Features;

return [
    'guard' => 'web',

    'passwords' => 'users',

    'username' => 'email',

    'email' => 'email',

    'home' => '/tasks',

    'prefix' => '',

    'domain' => null,

    'middleware' => ['web'],

    'limiters' => [
        'login' => 'login',
        'two-factor' => 'two-factor',
    ],

    'views' => true,

    'features' => [
        Features::registration(),
        Features::resetPasswords(),
        // Features::emailVerification(),
        Features::updateProfileInformation(),
        Features::updatePasswords(),
        // Features::twoFactorAuthentication([
        //     'confirm' => true,
        //     'confirmPassword' => true,
        // ]),
    ],
];
```

#### コードリーディング

| 設定 | 説明 |
|:---|:---|
| `'guard' => 'web'` | 使用する認証ガード |
| `'username' => 'email'` | ログインに使用するカラム |
| `'home' => '/tasks'` | ログイン後のリダイレクト先 |
| `'views' => true` | Fortifyのビュールートを有効化 |
| `Features::registration()` | ユーザー登録機能を有効化 |
| `Features::resetPasswords()` | パスワードリセット機能を有効化 |

---

### ステップ5: FortifyServiceProviderの設定

`app/Providers/FortifyServiceProvider.php` を編集し、認証ビューを設定します。

```php
<?php

namespace App\Providers;

use App\Actions\Fortify\CreateNewUser;
use App\Actions\Fortify\ResetUserPassword;
use App\Actions\Fortify\UpdateUserPassword;
use App\Actions\Fortify\UpdateUserProfileInformation;
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Support\ServiceProvider;
use Illuminate\Support\Str;
use Laravel\Fortify\Fortify;

class FortifyServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Fortify::createUsersUsing(CreateNewUser::class);
        Fortify::updateUserProfileInformationUsing(UpdateUserProfileInformation::class);
        Fortify::updateUserPasswordsUsing(UpdateUserPassword::class);
        Fortify::resetUserPasswordsUsing(ResetUserPassword::class);

        RateLimiter::for('login', function (Request $request) {
            $throttleKey = Str::transliterate(Str::lower($request->input(Fortify::username())).'|'.$request->ip());

            return Limit::perMinute(5)->by($throttleKey);
        });

        RateLimiter::for('two-factor', function (Request $request) {
            return Limit::perMinute(5)->by($request->session()->get('login.id'));
        });

        // 認証ビューの設定
        Fortify::loginView(function () {
            return view('auth.login');
        });

        Fortify::registerView(function () {
            return view('auth.register');
        });
    }
}
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `Fortify::createUsersUsing(CreateNewUser::class)` | ユーザー登録時のアクションを指定 |
| `RateLimiter::for('login', ...)` | ログイン試行回数の制限（1分間に5回まで） |
| `Fortify::loginView(...)` | ログインビューを指定 |
| `Fortify::registerView(...)` | 登録ビューを指定 |

---

### ステップ6: 認証ビューの作成

認証用のビューファイルを作成します。

#### レイアウトファイルの作成

`resources/views/layouts/app.blade.php` を作成します。

```php
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>@yield('title', 'タスク管理アプリ')</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', Meiryo, sans-serif;
            background-color: #f5f5f5;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .header {
            background-color: #333;
            color: white;
            padding: 15px 0;
            margin-bottom: 30px;
        }
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            font-size: 1.5rem;
        }
        .header nav a {
            color: white;
            text-decoration: none;
            margin-left: 20px;
        }
        .header nav a:hover {
            text-decoration: underline;
        }
        .card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            padding: 30px;
            margin-bottom: 20px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 1rem;
        }
        .form-group input:focus,
        .form-group select:focus,
        .form-group textarea:focus {
            outline: none;
            border-color: #007bff;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            font-size: 1rem;
            cursor: pointer;
            text-decoration: none;
        }
        .btn-primary {
            background-color: #007bff;
            color: white;
        }
        .btn-primary:hover {
            background-color: #0056b3;
        }
        .btn-danger {
            background-color: #dc3545;
            color: white;
        }
        .btn-danger:hover {
            background-color: #c82333;
        }
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        .btn-secondary:hover {
            background-color: #545b62;
        }
        .alert {
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .error-message {
            color: #dc3545;
            font-size: 0.875rem;
            margin-top: 5px;
        }
        .text-center {
            text-align: center;
        }
        .mt-3 {
            margin-top: 1rem;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-content">
            <h1>タスク管理アプリ</h1>
            <nav>
                @auth
                    <a href="{{ route('tasks.index') }}">タスク一覧</a>
                    <a href="{{ route('categories.index') }}">カテゴリー</a>
                    <span>{{ auth()->user()->name }}さん</span>
                    <form action="{{ route('logout') }}" method="POST" style="display: inline;">
                        @csrf
                        <button type="submit" style="background: none; border: none; color: white; cursor: pointer; margin-left: 20px;">ログアウト</button>
                    </form>
                @else
                    <a href="{{ route('login') }}">ログイン</a>
                    <a href="{{ route('register') }}">新規登録</a>
                @endauth
            </nav>
        </div>
    </header>

    <div class="container">
        @if (session('success'))
            <div class="alert alert-success">
                {{ session('success') }}
            </div>
        @endif

        @if (session('error'))
            <div class="alert alert-danger">
                {{ session('error') }}
            </div>
        @endif

        @yield('content')
    </div>
</body>
</html>
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `@yield('title', 'タスク管理アプリ')` | 子ビューからタイトルを受け取る（デフォルト値あり） |
| `@auth ... @else ... @endauth` | 認証状態による表示の切り替え |
| `{{ csrf_token() }}` | CSRFトークンをmetaタグに埋め込む |
| `{{ route('logout') }}` | 名前付きルートからURLを生成 |
| `@yield('content')` | 子ビューのコンテンツを表示する場所 |

---

#### ログインビューの作成

`resources/views/auth/login.blade.php` を作成します。

```php
@extends('layouts.app')

@section('title', 'ログイン')

@section('content')
<div style="max-width: 400px; margin: 0 auto;">
    <div class="card">
        <h2 class="text-center" style="margin-bottom: 20px;">ログイン</h2>

        <form method="POST" action="{{ route('login') }}">
            @csrf

            <div class="form-group">
                <label for="email">メールアドレス</label>
                <input type="email" id="email" name="email" value="{{ old('email') }}" required autofocus>
                @error('email')
                    <p class="error-message">{{ $message }}</p>
                @enderror
            </div>

            <div class="form-group">
                <label for="password">パスワード</label>
                <input type="password" id="password" name="password" required>
                @error('password')
                    <p class="error-message">{{ $message }}</p>
                @enderror
            </div>

            <div class="form-group">
                <label>
                    <input type="checkbox" name="remember"> ログイン状態を保持する
                </label>
            </div>

            <button type="submit" class="btn btn-primary" style="width: 100%;">ログイン</button>
        </form>

        <p class="text-center mt-3">
            アカウントをお持ちでない方は<a href="{{ route('register') }}">新規登録</a>
        </p>
    </div>
</div>
@endsection
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `@extends('layouts.app')` | レイアウトファイルを継承 |
| `@section('title', 'ログイン')` | タイトルを設定 |
| `@csrf` | CSRFトークンを埋め込む（必須） |
| `{{ old('email') }}` | バリデーションエラー時に入力値を復元 |
| `@error('email') ... @enderror` | エラーメッセージを表示 |
| `name="remember"` | 「ログイン状態を保持」のチェックボックス |

---

#### 登録ビューの作成

`resources/views/auth/register.blade.php` を作成します。

```php
@extends('layouts.app')

@section('title', '新規登録')

@section('content')
<div style="max-width: 400px; margin: 0 auto;">
    <div class="card">
        <h2 class="text-center" style="margin-bottom: 20px;">新規登録</h2>

        <form method="POST" action="{{ route('register') }}">
            @csrf

            <div class="form-group">
                <label for="name">名前</label>
                <input type="text" id="name" name="name" value="{{ old('name') }}" required autofocus>
                @error('name')
                    <p class="error-message">{{ $message }}</p>
                @enderror
            </div>

            <div class="form-group">
                <label for="email">メールアドレス</label>
                <input type="email" id="email" name="email" value="{{ old('email') }}" required>
                @error('email')
                    <p class="error-message">{{ $message }}</p>
                @enderror
            </div>

            <div class="form-group">
                <label for="password">パスワード</label>
                <input type="password" id="password" name="password" required>
                @error('password')
                    <p class="error-message">{{ $message }}</p>
                @enderror
            </div>

            <div class="form-group">
                <label for="password_confirmation">パスワード（確認）</label>
                <input type="password" id="password_confirmation" name="password_confirmation" required>
            </div>

            <button type="submit" class="btn btn-primary" style="width: 100%;">登録</button>
        </form>

        <p class="text-center mt-3">
            すでにアカウントをお持ちの方は<a href="{{ route('login') }}">ログイン</a>
        </p>
    </div>
</div>
@endsection
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `name="password_confirmation"` | パスワード確認用フィールド（Laravelの`confirmed`ルールで使用） |
| `{{ old('name') }}` | バリデーションエラー時に入力値を復元 |

---

### ステップ7: ユーザー登録アクションの確認

`app/Actions/Fortify/CreateNewUser.php` を確認します。このファイルはFortifyが自動生成したもので、ユーザー登録時のバリデーションとユーザー作成を行います。

```php
<?php

namespace App\Actions\Fortify;

use App\Models\User;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;
use Laravel\Fortify\Contracts\CreatesNewUsers;

class CreateNewUser implements CreatesNewUsers
{
    use PasswordValidationRules;

    /**
     * Validate and create a newly registered user.
     *
     * @param  array<string, string>  $input
     */
    public function create(array $input): User
    {
        Validator::make($input, [
            'name' => ['required', 'string', 'max:255'],
            'email' => [
                'required',
                'string',
                'email',
                'max:255',
                Rule::unique(User::class),
            ],
            'password' => $this->passwordRules(),
        ])->validate();

        return User::create([
            'name' => $input['name'],
            'email' => $input['email'],
            'password' => Hash::make($input['password']),
        ]);
    }
}
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `implements CreatesNewUsers` | Fortifyの契約インターフェースを実装 |
| `use PasswordValidationRules` | パスワードのバリデーションルールを提供するトレイト |
| `Validator::make(...)->validate()` | バリデーションを実行し、失敗時は例外をスロー |
| `Rule::unique(User::class)` | usersテーブルでユニークであることを検証 |
| `Hash::make($input['password'])` | パスワードをハッシュ化して保存 |

---

### ステップ8: 動作確認

開発サーバーを起動して、認証機能が正しく動作するか確認します。

```bash
# 開発サーバーの起動（すでに起動している場合は不要）
sail up -d
```

以下のURLにアクセスして動作を確認してください。

| URL | 機能 |
|:---|:---|
| `http://localhost/register` | ユーザー登録画面 |
| `http://localhost/login` | ログイン画面 |

#### 確認手順

1. **ユーザー登録**: `/register` にアクセスし、名前・メールアドレス・パスワードを入力して登録
2. **ログイン**: `/login` にアクセスし、登録したメールアドレスとパスワードでログイン
3. **ログアウト**: ヘッダーの「ログアウト」ボタンをクリック

---

## 💡 TIP: 認証関連のヘルパー関数

Laravelには認証に関する便利なヘルパー関数が用意されています。

```php
// ログイン中のユーザーを取得
$user = auth()->user();

// ログイン中かどうかを確認
if (auth()->check()) {
    // ログイン中の処理
}

// ログイン中のユーザーのID
$userId = auth()->id();

// ゲスト（未ログイン）かどうかを確認
if (auth()->guest()) {
    // 未ログインの処理
}
```

---

## ❌ よくある間違い

### 1. FortifyServiceProviderを登録し忘れる

```php
// ❌ NG: bootstrap/providers.php に追加し忘れ
return [
    App\Providers\AppServiceProvider::class,
    // FortifyServiceProviderがない
];
```

**対処法**: `bootstrap/providers.php` に `App\Providers\FortifyServiceProvider::class` を追加する。

### 2. CSRFトークンを忘れる

```php
// ❌ NG: @csrf がない
<form method="POST" action="{{ route('login') }}">
    <!-- @csrf がない -->
    <input type="email" name="email">
    ...
</form>
// エラー: 419 Page Expired
```

**対処法**: POSTフォームには必ず `@csrf` を追加する。

### 3. ビューファイルのパスを間違える

```php
// ❌ NG: ビューのパスが間違っている
Fortify::loginView(function () {
    return view('login'); // auth.login ではない
});
```

**対処法**: ビューファイルのパスを正しく指定する（`auth.login` は `resources/views/auth/login.blade.php`）。

---

## ✅ 完了条件

以下の条件を満たしていることを確認してください。

- [ ] Laravel Fortifyがインストールされている
- [ ] FortifyServiceProviderが登録されている
- [ ] ログイン画面（`/login`）が表示される
- [ ] 登録画面（`/register`）が表示される
- [ ] ユーザー登録ができる
- [ ] ログイン・ログアウトができる

---

## ✨ まとめ

このセクションでは、Laravel Fortifyを使用して認証機能を実装しました。

| 学んだこと | 内容 |
|:---|:---|
| Fortifyのインストール | `sail composer require laravel/fortify` |
| 設定ファイルの公開 | `sail artisan vendor:publish` |
| 認証ビューの設定 | `Fortify::loginView()`, `Fortify::registerView()` |
| 認証ヘルパー | `auth()->user()`, `auth()->check()` |

次のChapterでは、カテゴリーとタスクのCRUD機能を実装します。

---

## 🔄 Git操作とプルリクエスト

作業が完了したら、変更をコミットしてプッシュし、プルリクエストを作成して変更内容を確認しましょう。

### ステップ1: コミットとプッシュ

```bash
# 変更をステージング
git add .

# コミット（Issue番号を含める）
git commit -m "feat: 認証機能の実装（Fortify） #3"

# リモートにプッシュ
git push origin feature/issue-3-authentication
```

### ステップ2: プルリクエストの作成と確認

GitHubでプルリクエストを作成し、変更内容を確認してみましょう。

1. GitHubのリポジトリページを開く
2. 「Pull requests」タブをクリックする
3. 「New pull request」ボタンをクリックする
4. `base: main` ← `compare: feature/issue-3-authentication` を選択する
5. 「Create pull request」ボタンをクリックする
6. 以下の内容を入力する

**タイトル**:
```
feat: 認証機能の実装（Fortify）
```

**説明欄**:
```markdown
## 概要
Laravel Fortifyを使用して認証機能を実装しました。

## 変更内容
- Fortifyのインストールと設定
- ログイン・登録ビューの作成
- レイアウトファイルの作成

## 動作確認
- [ ] ユーザー登録ができる
- [ ] ログインができる
- [ ] ログアウトができる

## 対応Issue
close #3
```

7. 「Create pull request」ボタンをクリックする

> **💡 確認ポイント**: PRを作成したら、「Files changed」タブで変更内容を確認してみましょう。どのファイルがどのように変更されたかを確認することで、コードレビューの練習になります。

### ステップ3: プルリクエストのマージ

変更内容を確認したら、PRをマージします。

1. PRのページで「Merge pull request」ボタンをクリックする
2. 「Confirm merge」ボタンをクリックする
3. マージが完了すると、Issue #3が自動的にクローズされる

### ステップ4: ローカルのmainブランチを更新し、ブランチを削除

```bash
# mainブランチに切り替え
git switch main

# リモートの変更を取り込む
git pull origin main

# マージ済みのブランチを削除
git branch -d feature/issue-3-authentication
```

#### コマンドのコードリーディング

| コマンド | 説明 |
|:---|:---|
| `git switch main` | mainブランチに切り替え |
| `git pull origin main` | リモートの最新状態をローカルに反映 |
| `git branch -d feature/issue-3-authentication` | マージ済みのブランチを削除（`-d`は安全な削除） |

> **💡 ブランチ削除の理由**: マージが完了したブランチは不要になるため、削除してリポジトリを整理します。`-d`オプションは、マージされていないブランチは削除しないため安全です。

> **📌 Issue対応**: PRをマージすると、説明欄の `close #3` によりIssue #3が自動的にクローズされます。
