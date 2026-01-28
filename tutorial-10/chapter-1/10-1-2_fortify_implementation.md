# Tutorial 10-1-2: Fortifyの認証機能を理解する

## 🎯 このセクションで学ぶこと

*   Laravel Fortifyのインストールと設定の流れを理解する。
*   Fortifyが提供するルートとコントローラーの仕組みを理解する。
*   認証機能の有効化と動作確認の方法を理解する。

---

## 導入：Fortifyのセットアップ

前のセクションで、Laravel Fortifyが何であるかを学びました。このセクションでは、Fortifyのインストールから認証機能の実装までの流れを見ていきます。

Fortifyは、**バックエンドの認証処理**を提供するパッケージです。フロントエンド（ログインフォームなど）は、別途自分で作成する必要があります。

---

## 詳細解説

### 📦 Fortifyのインストール

Fortifyをインストールする流れを見ていきます。

**1. Composerでインストール**

```bash
sail composer require laravel/fortify
```

このコマンドで、Fortifyパッケージがプロジェクトに追加されます。

**2. Fortifyの設定ファイルを公開**

```bash
sail artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

このコマンドを実行すると、以下のファイルが作成されます：

*   `config/fortify.php`：Fortifyの設定ファイル
*   `app/Actions/Fortify/`：ユーザー登録・パスワードリセットなどのアクションクラス
*   `app/Providers/FortifyServiceProvider.php`：Fortifyのサービスプロバイダー

**3. マイグレーションを実行**

Fortifyは、Laravelのデフォルトの`users`テーブルを使用します。すでにマイグレーションを実行している場合は、このステップは不要です。

```bash
sail artisan migrate
```

---

### ⚙️ Fortifyの設定

`config/fortify.php`ファイルには、Fortifyの動作を制御する設定が含まれています。

**主要な設定項目**

```php
<?php

return [
    // 認証ガードの設定（デフォルトは'web'）
    'guard' => 'web',

    // パスワードブローカーの設定
    'passwords' => 'users',

    // ユーザー登録を有効化
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
];
```

**設定の意味**：

*   `guard`：認証に使用するガード（セッションベース認証では`web`を使用）
*   `passwords`：パスワードリセットに使用するブローカー
*   `features`：有効化する機能（登録、パスワードリセットなど）

**有効化できる機能**

このチュートリアルでは、以下の機能を有効化します：

*   `Features::registration()`：ユーザー登録
*   `Features::resetPasswords()`：パスワードリセット

---

### 🛤️ Fortifyが提供するルート

Fortifyをインストールすると、以下のルートが自動的に登録されます。

**ルート一覧の確認方法**

```bash
sail artisan route:list --path=login
sail artisan route:list --path=register
sail artisan route:list --path=logout
```

**主要なルート**：

| メソッド | URI | 説明 |
|---------|-----|------|
| GET | `/login` | ログインフォームを表示（ビューは自分で作成） |
| POST | `/login` | ログイン処理 |
| POST | `/logout` | ログアウト処理 |
| GET | `/register` | ユーザー登録フォームを表示（ビューは自分で作成） |
| POST | `/register` | ユーザー登録処理 |

**重要なポイント**：

*   Fortifyは、**POSTリクエストの処理**のみを提供します
*   **GETリクエスト（フォームの表示）**は、自分でビューを作成する必要があります

---

### 🎨 ビューのカスタマイズ

Fortifyは、フロントエンドを提供しないため、ログインフォームやユーザー登録フォームを自分で作成する必要があります。

**FortifyServiceProviderでビューを指定**

`app/Providers/FortifyServiceProvider.php`の`boot`メソッドで、表示するビューを指定します：

```php
<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use Laravel\Fortify\Fortify;

class FortifyServiceProvider extends ServiceProvider
{
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

*   `Fortify::loginView()`：ログインフォームのビューを指定
*   `Fortify::registerView()`：ユーザー登録フォームのビューを指定
*   `view('auth.login')`：`resources/views/auth/login.blade.php`を表示

---

### 📝 ユーザー登録のアクションクラス

Fortifyは、ユーザー登録時の処理を**アクションクラス**で管理します。

**CreateNewUser.php**

`app/Actions/Fortify/CreateNewUser.php`の内容を見ていきます：

```php
<?php

namespace App\Actions\Fortify;

use App\Models\User;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Validator;
use Laravel\Fortify\Contracts\CreatesNewUsers;

class CreateNewUser implements CreatesNewUsers
{
    use PasswordValidationRules;

    public function create(array $input): User
    {
        Validator::make($input, [
            'name' => ['required', 'string', 'max:255'],
            'email' => ['required', 'string', 'email', 'max:255', 'unique:users'],
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

**コードリーディング**：

1. **バリデーション**：名前、メールアドレス、パスワードをバリデーション
2. **パスワードのハッシュ化**：`Hash::make()`でパスワードを暗号化
3. **ユーザーの作成**：`User::create()`でデータベースに保存

**重要なポイント**：

*   パスワードは**絶対に平文で保存してはいけません**
*   `Hash::make()`を使って、必ずハッシュ化します

---

### 🔐 認証の確認方法

Fortifyをインストールした後、認証が正しく動作しているかを確認する方法を見ていきます。

**コントローラーでの確認**

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class DashboardController extends Controller
{
    public function index(Request $request)
    {
        // ログインしているか確認
        if ($request->user()) {
            return view('dashboard', ['user' => $request->user()]);
        }

        return redirect('/login');
    }
}
```

**Bladeでの確認**

```blade
@auth
    <p>ようこそ、{{ auth()->user()->name }}さん！</p>
@else
    <p>ログインしてください。</p>
@endauth
```

---

### 🛡️ 認証ミドルウェア

Laravelには、**認証ミドルウェア**が用意されています。これを使うと、ログインしていないユーザーを自動的にログインページにリダイレクトできます。

**ルートに認証ミドルウェアを適用**

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

*   `middleware('auth')`：このルートにアクセスするには、ログインが必要
*   ログインしていない場合、自動的に`/login`にリダイレクト

---

## 💡 TIP

### FortifyServiceProviderの登録

Fortifyをインストールすると、`FortifyServiceProvider`が自動的に`config/app.php`の`providers`配列に追加されます。もし追加されていない場合は、手動で追加する必要があります。

```php
'providers' => [
    // ...
    App\Providers\FortifyServiceProvider::class,
],
```

### パスワードのバリデーションルール

`CreateNewUser.php`で使われている`$this->passwordRules()`は、`PasswordValidationRules`トレイトで定義されています。デフォルトでは、以下のルールが適用されます：

*   最低8文字
*   確認用パスワードと一致

カスタマイズしたい場合は、`PasswordValidationRules`トレイトを編集します。

---

## ✨ まとめ

このセクションでは、Laravel Fortifyの認証機能について学びました。

*   **Fortifyのインストール**は、Composerで`laravel/fortify`をインストールし、設定ファイルを公開する
*   Fortifyは、**POSTリクエストの処理**のみを提供し、**GETリクエスト（フォーム表示）**は自分で作成する
*   **FortifyServiceProvider**で、ログインフォームとユーザー登録フォームのビューを指定する
*   **CreateNewUser**アクションクラスで、ユーザー登録時のバリデーションとパスワードのハッシュ化が行われる
*   **認証ミドルウェア**を使うと、ログインしていないユーザーを自動的にリダイレクトできる

---
