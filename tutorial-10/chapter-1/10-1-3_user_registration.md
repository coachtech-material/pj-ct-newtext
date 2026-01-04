# Tutorial 10-1-3: ユーザー登録機能の実装

## 🎯 このセクションで学ぶこと

*   Laravel Fortifyを使って、ユーザー登録機能を実装できるようになる。
*   パスワードのハッシュ化を理解する。
*   登録後の自動ログインの仕組みを理解する。

---

## 導入：「認証」の第一歩

認証機能の中で、最も基本的なのが**ユーザー登録機能**です。ユーザー登録機能を実装することで、ユーザーはアプリケーションにアカウントを作成できるようになります。

このセクションでは、前のセクションでインストールしたLaravel Fortifyを使って、ユーザー登録機能を実装します。

---

## 詳細解説

### 📝 ユーザー登録の流れ

Fortifyを使ったユーザー登録は、以下の流れで行われます：

```
1. ユーザーが /register にアクセス
   ↓
2. FortifyServiceProviderで指定したビューが表示される
   ↓
3. ユーザーが登録フォームに情報を入力してPOST
   ↓
4. Fortifyが CreateNewUser アクションクラスを呼び出す
   ↓
5. バリデーション → パスワードハッシュ化 → データベース保存
   ↓
6. 自動的にログイン状態になり、リダイレクト
```

**重要なポイント**：

*   **コントローラーを自作する必要がない**：Fortifyが内部で処理を行う
*   **処理のカスタマイズはアクションクラスで行う**：`app/Actions/Fortify/CreateNewUser.php`

---

### 🎨 ステップ1: 登録フォームのビューを作成する

まず、ユーザー登録フォームのBladeファイルを作成します。

#### ディレクトリの作成

```bash
mkdir -p resources/views/auth
```

#### 登録フォームの作成

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
<form method="POST" action="{{ route('register') }}">
```
→ Fortifyが自動的に登録した`register`ルートにPOSTします。

```blade
@csrf
```
→ CSRF対策のトークンを埋め込みます。これがないとリクエストが拒否されます。

```blade
value="{{ old('name') }}"
```
→ バリデーションエラー時に、入力した値を保持します。

```blade
@error('name')
    <p class="error">{{ $message }}</p>
@enderror
```
→ バリデーションエラーがあれば、エラーメッセージを表示します。

---

### 🔧 ステップ2: FortifyServiceProviderでビューを指定する

`app/Providers/FortifyServiceProvider.php`を開いて、`boot`メソッドに登録ビューを指定します：

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
        // ユーザー登録フォームのビューを指定
        Fortify::registerView(function () {
            return view('auth.register');
        });

        // ログインフォームのビューを指定（次のセクションで使用）
        Fortify::loginView(function () {
            return view('auth.login');
        });
    }
}
```

**コードリーディング**：

```php
Fortify::registerView(function () {
    return view('auth.register');
});
```
→ `/register`にGETリクエストが来たときに、`resources/views/auth/register.blade.php`を表示するよう指定します。

---

### 📝 ステップ3: CreateNewUserアクションクラスを確認する

Fortifyは、ユーザー登録時の処理を**アクションクラス**で管理します。

`app/Actions/Fortify/CreateNewUser.php`を開いて、内容を確認しましょう：

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
*   Fortifyが自動的にこのアクションクラスを呼び出します

---

### 🔐 パスワードのハッシュ化

**なぜハッシュ化が必要なのか？**

パスワードを平文（そのまま）でデータベースに保存すると、データベースが漏洩した際に、全てのユーザーのパスワードが盗まれてしまいます。

**ハッシュ化とは？**

ハッシュ化とは、**元に戻せない形式**にパスワードを変換することです。

```php
$password = 'password123';
$hashed = Hash::make($password);

echo $hashed;
// $2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi
```

**検証**

ログイン時には、`Hash::check()`を使って、入力されたパスワードとハッシュ化されたパスワードを比較します。

```php
if (Hash::check('password123', $hashed)) {
    echo 'パスワードが一致しました';
}
```

---

### 🚀 ステップ4: 動作確認

#### ルートの確認

Fortifyが登録したルートを確認します：

```bash
sail artisan route:list --path=register
```

**出力例**：

```
GET|HEAD  register .......... Laravel\Fortify\Http\Controllers\RegisteredUserController@create
POST      register .......... Laravel\Fortify\Http\Controllers\RegisteredUserController@store
```

**重要なポイント**：

*   `routes/web.php`に何も書いていないのに、ルートが登録されている
*   Fortifyが内部でルートを定義している
*   これがFortifyの「バックエンドの認証ロジックを提供する」という意味

#### ブラウザで確認

1. ブラウザで`http://localhost/register`にアクセス
2. 登録フォームが表示されることを確認
3. 情報を入力して「登録」ボタンをクリック
4. 登録が成功し、ダッシュボード（または設定したリダイレクト先）に遷移することを確認

---

### ⚙️ 登録後のリダイレクト先を設定する

登録後のリダイレクト先は、`config/fortify.php`で設定します：

```php
'home' => '/dashboard',
```

または、`app/Providers/RouteServiceProvider.php`の`HOME`定数を変更します：

```php
public const HOME = '/dashboard';
```

---

### 💡 TIP: バリデーションルールのカスタマイズ

`CreateNewUser.php`のバリデーションルールをカスタマイズできます。

#### 例: 名前の最大文字数を50文字に変更

```php
Validator::make($input, [
    'name' => ['required', 'string', 'max:50'],
    'email' => ['required', 'string', 'email', 'max:255', 'unique:users'],
    'password' => $this->passwordRules(),
])->validate();
```

#### 例: パスワードの要件を強化

`app/Actions/Fortify/PasswordValidationRules.php`を編集します：

```php
use Illuminate\Validation\Rules\Password;

protected function passwordRules(): array
{
    return [
        'required',
        'string',
        Password::min(8)
            ->letters()      // 英字を含む
            ->numbers()      // 数字を含む
            ->mixedCase()    // 大文字と小文字を含む
            ->symbols(),     // 記号を含む
        'confirmed',
    ];
}
```

---

### 🚨 よくある間違い

#### 間違い1: パスワードをハッシュ化しない

```php
return User::create([
    'password' => $input['password'], // NG: 平文で保存される
]);
```

**対処法**: `Hash::make()`を使います。

```php
return User::create([
    'password' => Hash::make($input['password']), // OK
]);
```

---

#### 間違い2: FortifyServiceProviderでビューを指定しない

ビューを指定しないと、`/register`にアクセスしても何も表示されません。

**対処法**: `FortifyServiceProvider`の`boot`メソッドで`Fortify::registerView()`を設定します。

---

## ✨ まとめ

このセクションでは、Laravel Fortifyを使って、ユーザー登録機能を実装しました。

*   **Bladeファイル**を作成し、`FortifyServiceProvider`で指定した
*   **CreateNewUser**アクションクラスで、バリデーションとパスワードのハッシュ化を行う
*   **コントローラーを自作する必要がない**：Fortifyが内部で処理を行う
*   **ルートはFortifyが自動的に登録する**：`sail artisan route:list`で確認できる

次のセクションでは、ログイン・ログアウト機能を実装します。

---
