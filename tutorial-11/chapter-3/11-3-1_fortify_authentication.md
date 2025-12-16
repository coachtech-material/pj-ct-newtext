# Tutorial 11-3-1: 認証機能の実装（Laravel Fortify）

## 🎯 このセクションで学ぶこと

- Laravel Fortifyを使った認証機能を実装する方法を学ぶ
- ユーザー登録、ログイン、ログアウト機能を実装する
- 認証済みユーザーのみがタスクにアクセスできるようにする

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜCRUDの後に『認証』を実装するのか？」

CRUDが完成したら、次は「認証」機能です。なぜこのタイミングなのでしょうか？

---

### 理由1: まずは機能を動かすことが優先

最初から認証を入れると、**ログインしないとテストできない**状態になります。

まずはCRUDを完成させて動作確認し、その後で認証を追加する方が効率的です。

---

### 理由2: 認証がないとセキュリティ上問題

CRUDが動いたら、次は**セキュリティ**を考えます。

現状では誰でもタスクを見たり編集したりできてしまいます。認証を追加して、**ログインユーザーのみ**がアクセスできるようにします。

---

### 理由3: リレーションシップの準備

認証を追加すると、「このタスクは誰のもの？」という問題が出てきます。

次のセクションで実装する**ユーザーとタスクのリレーションシップ**の準備として、まず認証を実装します。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | Fortifyのインストールと設定 | 認証パッケージを導入 |
| Step 2 | 認証ビューの作成 | ログイン・登録画面を作成 |
| Step 3 | FortifyServiceProviderの設定 | ビューとリダイレクト先を指定 |
| Step 4 | ルートの保護 | ログイン必須にする |
| Step 5 | 動作確認 | 認証機能をテストする |

> 💡 **ポイント**: Laravel Fortifyは、認証のバックエンド処理を提供します。フロントエンドは自分で作成します。

---

## Step 1: Fortifyのインストールと設定

### 1-1. Fortifyをインストールする

Laravelプロジェクトに、Fortifyをインストールします。

```bash
composer require laravel/fortify
```

---

### 1-2. 設定ファイルを公開する

Fortifyをインストールしたら、設定ファイルを公開します。

```bash
php artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

このコマンドを実行すると、以下のファイルが作成されます。

- `config/fortify.php`: Fortifyの設定ファイル
- `app/Providers/FortifyServiceProvider.php`: Fortifyのサービスプロバイダー
- `app/Actions/Fortify/`: 認証アクションのディレクトリ

---

### 1-3. 機能を有効にする

`config/fortify.php`で、使用する機能を有効にします。

**ファイル**: `config/fortify.php`

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    // Features::emailVerification(),
    // Features::updateProfileInformation(),
    // Features::updatePasswords(),
    // Features::twoFactorAuthentication([
    //     'confirm' => true,
    //     'confirmPassword' => true,
    // ]),
],
```

このセクションでは、**ユーザー登録**と**パスワードリセット**を有効にします。

---

### 1-4. コードリーディング

#### Laravel Fortifyとは

**Laravel Fortify**は、**Laravelの公式認証パッケージ**です。

Fortifyは、以下の認証機能を提供します。

- **ユーザー登録**
- **ログイン・ログアウト**
- **パスワードリセット**
- **メール認証**
- **2要素認証**

Fortifyの特徴は、**フロントエンドに依存しない**ことです。Blade、Vue.js、Reactなど、どのようなフロントエンドでも使用できます。

---

## Step 2: 認証ビューの作成

### 2-1. ユーザー登録ページを作成する

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
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .error {
            color: red;
            margin-bottom: 15px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .link {
            text-align: center;
            margin-top: 15px;
        }
    </style>
</head>
<body>
    <h1>ユーザー登録</h1>

    @if ($errors->any())
        <div class="error">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form method="POST" action="{{ route('register') }}">
        @csrf

        <div class="form-group">
            <label for="name">名前</label>
            <input type="text" id="name" name="name" value="{{ old('name') }}" required>
        </div>

        <div class="form-group">
            <label for="email">メールアドレス</label>
            <input type="email" id="email" name="email" value="{{ old('email') }}" required>
        </div>

        <div class="form-group">
            <label for="password">パスワード</label>
            <input type="password" id="password" name="password" required>
        </div>

        <div class="form-group">
            <label for="password_confirmation">パスワード（確認）</label>
            <input type="password" id="password_confirmation" name="password_confirmation" required>
        </div>

        <button type="submit">登録</button>
    </form>

    <p class="link">既にアカウントをお持ちですか？ <a href="{{ route('login') }}">ログイン</a></p>
</body>
</html>
```

---

### 2-2. ログインページを作成する

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
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="email"],
        input[type="password"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .error {
            color: red;
            margin-bottom: 15px;
        }
        button {
            width: 100%;
            padding: 10px;
            background-color: #2196f3;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        .link {
            text-align: center;
            margin-top: 15px;
        }
        .remember {
            display: flex;
            align-items: center;
            gap: 5px;
        }
    </style>
</head>
<body>
    <h1>ログイン</h1>

    @if ($errors->any())
        <div class="error">
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form method="POST" action="{{ route('login') }}">
        @csrf

        <div class="form-group">
            <label for="email">メールアドレス</label>
            <input type="email" id="email" name="email" value="{{ old('email') }}" required>
        </div>

        <div class="form-group">
            <label for="password">パスワード</label>
            <input type="password" id="password" name="password" required>
        </div>

        <div class="form-group remember">
            <input type="checkbox" id="remember" name="remember">
            <label for="remember" style="margin-bottom: 0; font-weight: normal;">ログイン状態を保持する</label>
        </div>

        <button type="submit">ログイン</button>
    </form>

    <p class="link">アカウントをお持ちでないですか？ <a href="{{ route('register') }}">ユーザー登録</a></p>
</body>
</html>
```

---

### 2-3. コードリーディング

#### `route('register')` と `route('login')`

- Fortifyは、認証関連のルートを自動的に登録します
- `register`、`login`、`logout`などのルート名が使えます

---

#### `password_confirmation`

- パスワード確認フィールドは、`password_confirmation`という名前にする必要があります
- Laravelのバリデーションルール`confirmed`が、この名前を期待しています

---

## Step 3: FortifyServiceProviderの設定

### 3-1. ビューとリダイレクト先を指定する

`app/Providers/FortifyServiceProvider.php`の`boot()`メソッドで、ビューを指定します。

**ファイル**: `app/Providers/FortifyServiceProvider.php`

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
    public function register(): void
    {
        //
    }

    public function boot(): void
    {
        Fortify::createUsersUsing(CreateNewUser::class);
        Fortify::updateUserProfileInformationUsing(UpdateUserProfileInformation::class);
        Fortify::updateUserPasswordsUsing(UpdateUserPassword::class);
        Fortify::resetUserPasswordsUsing(ResetUserPassword::class);

        // ビューの指定
        Fortify::registerView(function () {
            return view('auth.register');
        });

        Fortify::loginView(function () {
            return view('auth.login');
        });

        RateLimiter::for('login', function (Request $request) {
            $throttleKey = Str::transliterate(Str::lower($request->input(Fortify::username())).'|'.$request->ip());

            return Limit::perMinute(5)->by($throttleKey);
        });

        RateLimiter::for('two-factor', function (Request $request) {
            return Limit::perMinute(5)->by($request->session()->get('login.id'));
        });
    }
}
```

---

### 3-2. コードリーディング

#### `Fortify::registerView()` と `Fortify::loginView()`

- 登録画面とログイン画面のビューを指定します
- Fortifyは、これらのビューを自動的に表示します

---

#### `RateLimiter::for('login', ...)`

- ログイン試行の回数制限を設定します
- 1分間に5回までログインを試行できます
- これにより、**ブルートフォース攻撃**を防ぎます

---

## Step 4: ルートの保護

### 4-1. 認証済みユーザーのみアクセスできるようにする

タスク関連のルートを、認証済みユーザーのみがアクセスできるようにします。

**ファイル**: `routes/web.php`

```php
use App\Http\Controllers\TaskController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

// 認証済みユーザーのみアクセス可能
Route::middleware(['auth'])->group(function () {
    Route::get('/tasks', [TaskController::class, 'index'])->name('tasks.index');
    Route::get('/tasks/create', [TaskController::class, 'create'])->name('tasks.create');
    Route::post('/tasks', [TaskController::class, 'store'])->name('tasks.store');
    Route::get('/tasks/{task}', [TaskController::class, 'show'])->name('tasks.show');
    Route::get('/tasks/{task}/edit', [TaskController::class, 'edit'])->name('tasks.edit');
    Route::put('/tasks/{task}', [TaskController::class, 'update'])->name('tasks.update');
    Route::delete('/tasks/{task}', [TaskController::class, 'destroy'])->name('tasks.destroy');
});
```

---

### 4-2. ログアウト機能を追加する

タスク一覧ページにログアウトボタンを追加します。

**ファイル**: `resources/views/tasks/index.blade.php`

ヘッダー部分に以下を追加します。

```blade
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
    <h1>タスク一覧</h1>
    <div>
        <span>{{ auth()->user()->name }}さん</span>
        <form method="POST" action="{{ route('logout') }}" style="display: inline;">
            @csrf
            <button type="submit" style="background: none; border: none; color: #f44336; cursor: pointer;">ログアウト</button>
        </form>
    </div>
</div>
```

---

### 4-3. コードリーディング

#### `Route::middleware(['auth'])->group(function () { ... })`

- `auth`ミドルウェアを適用したルートグループを作成します
- このグループ内のルートは、**ログインしていないとアクセスできません**
- 未ログインでアクセスすると、自動的にログインページにリダイレクトされます

---

#### `auth()->user()->name`

- `auth()`ヘルパーで、現在ログインしているユーザーを取得できます
- `auth()->user()`でユーザーモデルを取得し、`name`プロパティで名前を取得します

---

## Step 5: 動作確認

### 5-1. ユーザー登録をテストする

1. ブラウザで`http://localhost/register`にアクセスする
2. 名前、メールアドレス、パスワードを入力する
3. 「登録」ボタンをクリックする
4. ユーザーが作成され、自動的にログインされる

---

### 5-2. ログインをテストする

1. ログアウトする
2. ブラウザで`http://localhost/login`にアクセスする
3. メールアドレス、パスワードを入力する
4. 「ログイン」ボタンをクリックする
5. ログインが成功し、タスク一覧ページにリダイレクトされる

---

### 5-3. ルート保護を確認する

1. ログアウトする
2. ブラウザで`http://localhost/tasks`にアクセスする
3. 自動的にログインページにリダイレクトされる

---

### 5-4. Fortifyが登録するルートを確認する

```bash
php artisan route:list | grep -E "(register|login|logout)"
```

**実行結果**:

```
GET|HEAD  login .................... login › Laravel\Fortify
POST      login ..................... Laravel\Fortify
POST      logout .................... logout › Laravel\Fortify
GET|HEAD  register .................. register › Laravel\Fortify
POST      register .................. Laravel\Fortify
```

---

## 🚨 よくある間違い

### 間違い1: ビューを作成していない

**エラー**:

```
View [auth.login] not found.
```

**対処法**: `resources/views/auth/login.blade.php`と`resources/views/auth/register.blade.php`を作成します。

---

### 間違い2: FortifyServiceProviderでビューを指定していない

**問題**: ログインページにアクセスしても何も表示されない

**対処法**: `app/Providers/FortifyServiceProvider.php`の`boot()`メソッドで、ビューを指定します。

---

### 間違い3: マイグレーションを実行していない

**エラー**:

```
SQLSTATE[42S02]: Base table or view not found: 1146 Table 'database.users' doesn't exist
```

**対処法**: `php artisan migrate`を実行します。

---

## 💡 TIP: シーダーでテストユーザーを作成

毎回ユーザー登録するのは手間なので、シーダーでテストユーザーを作成しておきます。

**ファイル**: `database/seeders/DatabaseSeeder.php`

```php
public function run(): void
{
    \App\Models\User::factory()->create([
        'name' => 'Test User',
        'email' => 'test@example.com',
        'password' => bcrypt('password'),
    ]);
}
```

シーダーを実行します。

```bash
php artisan db:seed
```

これで、`test@example.com` / `password`でログインできます。

---

## ✨ まとめ

このセクションでは、Laravel Fortifyを使った認証機能の実装について学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | Fortifyのインストールと設定 |
| Step 2 | 登録・ログインビューの作成 |
| Step 3 | FortifyServiceProviderでビューを指定 |
| Step 4 | `auth`ミドルウェアでルートを保護 |
| Step 5 | 認証機能の動作確認 |

次のセクションでは、ユーザーとタスクのリレーションシップを実装します。

---

## 📝 学習のポイント

- [ ] Laravel Fortifyを使った認証機能を実装した
- [ ] ユーザー登録、ログイン、ログアウト機能を実装した
- [ ] 認証済みユーザーのみがアクセスできるようにした
- [ ] `auth`ミドルウェアの役割を理解した
