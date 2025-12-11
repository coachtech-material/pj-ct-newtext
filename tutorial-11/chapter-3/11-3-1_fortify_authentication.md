# Tutorial 11-3-1: 認証機能の実装（Laravel Fortify）

## 🎯 このセクションで学ぶこと

*   Laravel Fortifyを使った認証機能を実装する方法を学ぶ。
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

### 🔍 Laravel Fortifyとは

**Laravel Fortify**は、**Laravelの公式認証パッケージ**です。

Fortifyは、以下の認証機能を提供します。

*   **ユーザー登録**
*   **ログイン・ログアウト**
*   **パスワードリセット**
*   **メール認証**
*   **2要素認証**

Fortifyの特徴は、**フロントエンドに依存しない**ことです。つまり、Blade、Vue.js、Reactなど、どのようなフロントエンドでも使用できます。

---

### 🔍 Fortifyのインストール

Laravelプロジェクトに、Fortifyをインストールします。

```bash
composer require laravel/fortify
```

---

### 🔍 Fortifyの設定

Fortifyをインストールしたら、設定ファイルを公開します。

```bash
php artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

このコマンドを実行すると、以下のファイルが作成されます。

*   `config/fortify.php`: Fortifyの設定ファイル
*   `app/Providers/FortifyServiceProvider.php`: Fortifyのサービスプロバイダー
*   `app/Actions/Fortify/`: 認証アクションのディレクトリ

---

### 🔍 FortifyServiceProviderの登録

`config/app.php`の`providers`配列に、`FortifyServiceProvider`を追加します。

**ファイル**: `config/app.php`

```php
'providers' => [
    // ...
    App\Providers\FortifyServiceProvider::class,
],
```

Laravel 11以降では、自動的に登録されるため、この手順は不要です。

---

### 🔍 マイグレーションの実行

Fortifyは、`users`テーブルを使用します。Laravelプロジェクトを作成すると、`users`テーブルのマイグレーションファイルが既に存在しています。

マイグレーションを実行します。

```bash
php artisan migrate
```

---

### 🔍 Fortifyの機能を有効にする

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

### 🔍 ビューの作成

Fortifyは、フロントエンドに依存しないため、ビューは自分で作成する必要があります。

以下のビューを作成します。

*   `resources/views/auth/register.blade.php`: ユーザー登録ページ
*   `resources/views/auth/login.blade.php`: ログインページ

---

#### ユーザー登録ページ

**ファイル**: `resources/views/auth/register.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ユーザー登録</title>
</head>
<body>
    <h1>ユーザー登録</h1>

    @if ($errors->any())
        <div>
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form method="POST" action="{{ route('register') }}">
        @csrf

        <div>
            <label for="name">名前</label>
            <input type="text" id="name" name="name" value="{{ old('name') }}" required>
        </div>

        <div>
            <label for="email">メールアドレス</label>
            <input type="email" id="email" name="email" value="{{ old('email') }}" required>
        </div>

        <div>
            <label for="password">パスワード</label>
            <input type="password" id="password" name="password" required>
        </div>

        <div>
            <label for="password_confirmation">パスワード（確認）</label>
            <input type="password" id="password_confirmation" name="password_confirmation" required>
        </div>

        <button type="submit">登録</button>
    </form>

    <p>既にアカウントをお持ちですか？ <a href="{{ route('login') }}">ログイン</a></p>
</body>
</html>
```

---

#### ログインページ

**ファイル**: `resources/views/auth/login.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ログイン</title>
</head>
<body>
    <h1>ログイン</h1>

    @if ($errors->any())
        <div>
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form method="POST" action="{{ route('login') }}">
        @csrf

        <div>
            <label for="email">メールアドレス</label>
            <input type="email" id="email" name="email" value="{{ old('email') }}" required>
        </div>

        <div>
            <label for="password">パスワード</label>
            <input type="password" id="password" name="password" required>
        </div>

        <div>
            <label>
                <input type="checkbox" name="remember"> ログイン状態を保持する
            </label>
        </div>

        <button type="submit">ログイン</button>
    </form>

    <p>アカウントをお持ちでないですか？ <a href="{{ route('register') }}">ユーザー登録</a></p>
</body>
</html>
```

---

### 🔍 FortifyServiceProviderでビューを指定

`app/Providers/FortifyServiceProvider.php`の`boot()`メソッドで、ビューを指定します。

**ファイル**: `app/Providers/FortifyServiceProvider.php`

```php
public function boot(): void
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    Fortify::loginView(function () {
        return view('auth.login');
    });
}
```

---

### 🔍 ルーティングの確認

Fortifyは、以下のルートを自動的に登録します。

```
GET  /register       - ユーザー登録ページ
POST /register       - ユーザー登録処理
GET  /login          - ログインページ
POST /login          - ログイン処理
POST /logout         - ログアウト処理
```

ルートを確認します。

```bash
php artisan route:list | grep -E "(register|login|logout)"
```

---

### 🔍 ユーザー登録のテスト

ブラウザで `http://localhost/register` にアクセスし、ユーザー登録を試します。

1. 名前、メールアドレス、パスワードを入力
2. 「登録」ボタンをクリック
3. ユーザーが作成され、自動的にログインされる

---

### 🔍 ログインのテスト

ブラウザで `http://localhost/login` にアクセスし、ログインを試します。

1. メールアドレス、パスワードを入力
2. 「ログイン」ボタンをクリック
3. ログインが成功する

---

### 🔍 ログアウト機能の実装

ログアウトは、POSTリクエストで `/logout` にアクセスします。

**ファイル**: `resources/views/tasks/index.blade.php`（例）

```blade
<form method="POST" action="{{ route('logout') }}">
    @csrf
    <button type="submit">ログアウト</button>
</form>
```

---

### 🔍 認証済みユーザーのみアクセスできるようにする

タスク一覧ページなど、認証済みユーザーのみがアクセスできるようにします。

**ファイル**: `routes/web.php`

```php
Route::middleware(['auth'])->group(function () {
    Route::get('/tasks', [TaskController::class, 'index'])->name('tasks.index');
    Route::get('/tasks/create', [TaskController::class, 'create'])->name('tasks.create');
    Route::post('/tasks', [TaskController::class, 'store'])->name('tasks.store');
    // ...
});
```

---

### 🔍 リダイレクト先の設定

ログイン後のリダイレクト先を設定します。

**ファイル**: `app/Providers/FortifyServiceProvider.php`

```php
use Laravel\Fortify\Fortify;

public function boot(): void
{
    Fortify::registerView(function () {
        return view('auth.register');
    });

    Fortify::loginView(function () {
        return view('auth.login');
    });

    // ログイン後のリダイレクト先
    Fortify::redirects('login', '/tasks');
}
```

---

### 💡 TIP: シーダーでテストユーザーを作成

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

これで、`test@example.com` / `password` でログインできます。

---

### 🚨 よくある間違い

#### 間違い1: ビューを作成していない

**対処法**: `resources/views/auth/register.blade.php` と `resources/views/auth/login.blade.php` を作成します。

---

#### 間違い2: FortifyServiceProviderでビューを指定していない

**対処法**: `app/Providers/FortifyServiceProvider.php` の `boot()` メソッドで、ビューを指定します。

---

#### 間違い3: マイグレーションを実行していない

**対処法**: `php artisan migrate` を実行します。

---

## ✨ まとめ

このセクションでは、Laravel Fortifyを使った認証機能の実装について学びました。

*   Fortifyは、Laravelの公式認証パッケージで、フロントエンドに依存しない。
*   ユーザー登録、ログイン、ログアウト機能を実装できる。
*   `auth`ミドルウェアを使って、認証済みユーザーのみがアクセスできるようにする。
*   シーダーでテストユーザーを作成しておくと、開発が楽になる。

次のセクションでは、ユーザーとタスクのリレーションシップを実装します。

---

## 📝 学習のポイント

- [ ] Laravel Fortifyを使った認証機能を実装した。
- [ ] ユーザー登録、ログイン、ログアウト機能を実装した。
- [ ] 認証済みユーザーのみがアクセスできるようにした。
