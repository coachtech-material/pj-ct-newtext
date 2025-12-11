# Tutorial 9-7-3: ユーザー登録機能の実装

## 🎯 このセクションで学ぶこと

*   Laravel Sanctumを使って、ユーザー登録機能を実装できるようになる。
*   パスワードのハッシュ化を理解する。
*   登録後の自動ログインを実装できるようになる。

---

## 導入：「認証」の第一歩

認証機能の中で、最も基本的なのが**ユーザー登録機能**です。ユーザー登録機能を実装することで、ユーザーはアプリケーションにアカウントを作成できるようになります。

このセクションでは、Laravel Sanctumを使って、ユーザー登録機能を実装します。

---

## 詳細解説

### 📝 ユーザー登録の流れ

1. ユーザーが登録フォームに情報を入力
2. サーバーがバリデーションを実行
3. パスワードをハッシュ化
4. データベースにユーザー情報を保存
5. ユーザーに認証トークンを発行（API認証の場合）
6. ログイン状態にする

---

### 🔧 ステップ1: ユーザーモデルの準備

Laravelでは、デフォルトで`User`モデルが用意されています。

**`app/Models/User.php`**

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens;

    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected $casts = [
        'email_verified_at' => 'datetime',
    ];
}
```

**コードリーディング**

*   `HasApiTokens`: Sanctumの機能を使うために必要
*   `$fillable`: マスアサインメントを許可するカラム
*   `$hidden`: JSONに変換する際に隠すカラム

---

### 🔧 ステップ2: フォームリクエストの作成

```bash
php artisan make:request RegisterRequest
```

**`app/Http/Requests/RegisterRequest.php`**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class RegisterRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users',
            'password' => ['required', 'confirmed', Password::min(8)
                ->letters()
                ->numbers()],
        ];
    }

    public function messages()
    {
        return [
            'name.required' => '名前は必須です。',
            'email.required' => 'メールアドレスは必須です。',
            'email.unique' => 'このメールアドレスは既に登録されています。',
            'password.required' => 'パスワードは必須です。',
            'password.confirmed' => 'パスワードが一致しません。',
        ];
    }
}
```

---

### 🔧 ステップ3: コントローラーの作成

```bash
php artisan make:controller AuthController
```

**`app/Http/Controllers/AuthController.php`**

```php
<?php

namespace App\Http\Controllers;

use App\Http\Requests\RegisterRequest;
use App\Models\User;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Auth;

class AuthController extends Controller
{
    public function register(RegisterRequest $request)
    {
        $validated = $request->validated();

        // ユーザーを作成
        $user = User::create([
            'name' => $validated['name'],
            'email' => $validated['email'],
            'password' => Hash::make($validated['password']),
        ]);

        // 自動ログイン
        Auth::login($user);

        // APIトークンを発行（API認証の場合）
        $token = $user->createToken('auth_token')->plainTextToken;

        return response()->json([
            'message' => 'User registered successfully',
            'user' => $user,
            'token' => $token,
        ], 201);
    }
}
```

**コードリーディング**

*   `Hash::make()`: パスワードをハッシュ化
*   `Auth::login()`: ユーザーをログイン状態にする
*   `createToken()`: Sanctumの認証トークンを発行

---

### 🔧 ステップ4: ルートの定義

**`routes/api.php`**

```php
use App\Http\Controllers\AuthController;

Route::post('/register', [AuthController::class, 'register']);
```

---

### 🚀 実践例1: Postmanでテスト

#### リクエスト

```
POST http://localhost/api/register
Content-Type: application/json

{
    "name": "山田太郎",
    "email": "yamada@example.com",
    "password": "password123",
    "password_confirmation": "password123"
}
```

#### レスポンス

```json
{
    "message": "User registered successfully",
    "user": {
        "id": 1,
        "name": "山田太郎",
        "email": "yamada@example.com",
        "created_at": "2024-01-01T00:00:00.000000Z",
        "updated_at": "2024-01-01T00:00:00.000000Z"
    },
    "token": "1|abc123..."
}
```

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

```php
if (Hash::check('password123', $hashed)) {
    echo 'パスワードが一致しました';
}
```

---

### 💡 TIP: メール確認機能

実際のアプリケーションでは、登録後にメール確認を行うことが一般的です。

#### ステップ1: `User`モデルに`MustVerifyEmail`を追加

```php
use Illuminate\Contracts\Auth\MustVerifyEmail;

class User extends Authenticatable implements MustVerifyEmail
{
    // ...
}
```

#### ステップ2: メール確認のルートを追加

```php
Route::get('/email/verify/{id}/{hash}', [AuthController::class, 'verifyEmail'])
    ->middleware(['signed'])
    ->name('verification.verify');
```

---

### 🚀 実践例2: 登録後にプロフィールページにリダイレクト

#### Web版のコントローラー

```php
public function register(RegisterRequest $request)
{
    $validated = $request->validated();

    $user = User::create([
        'name' => $validated['name'],
        'email' => $validated['email'],
        'password' => Hash::make($validated['password']),
    ]);

    Auth::login($user);

    return redirect('/profile')->with('success', '登録が完了しました');
}
```

---

### 🚀 実践例3: 追加情報を登録

#### フォームリクエスト

```php
public function rules()
{
    return [
        'name' => 'required|string|max:255',
        'email' => 'required|email|unique:users',
        'password' => ['required', 'confirmed', Password::min(8)
            ->letters()
            ->numbers()],
        'birth_date' => 'required|date|before:today',
        'phone' => 'nullable|regex:/^[0-9]{10,11}$/',
    ];
}
```

#### コントローラー

```php
public function register(RegisterRequest $request)
{
    $validated = $request->validated();

    $user = User::create([
        'name' => $validated['name'],
        'email' => $validated['email'],
        'password' => Hash::make($validated['password']),
        'birth_date' => $validated['birth_date'],
        'phone' => $validated['phone'] ?? null,
    ]);

    Auth::login($user);

    $token = $user->createToken('auth_token')->plainTextToken;

    return response()->json([
        'message' => 'User registered successfully',
        'user' => $user,
        'token' => $token,
    ], 201);
}
```

---

### 🚨 よくある間違い

#### 間違い1: パスワードをハッシュ化しない

```php
$user = User::create([
    'password' => $validated['password'], // NG: 平文で保存される
]);
```

**対処法**: `Hash::make()`を使います。

```php
$user = User::create([
    'password' => Hash::make($validated['password']), // OK
]);
```

---

#### 間違い2: `password_confirmation`をデータベースに保存しようとする

```php
$user = User::create([
    'name' => $validated['name'],
    'email' => $validated['email'],
    'password' => Hash::make($validated['password']),
    'password_confirmation' => $validated['password_confirmation'], // NG
]);
```

**対処法**: `password_confirmation`は、バリデーションのみに使います。

---

## ✨ まとめ

このセクションでは、Laravel Sanctumを使って、ユーザー登録機能を実装しました。

*   フォームリクエストを使って、バリデーションを実装した。
*   `Hash::make()`を使って、パスワードをハッシュ化した。
*   `Auth::login()`を使って、登録後に自動ログインを実装した。
*   `createToken()`を使って、Sanctumの認証トークンを発行した。

次のセクションでは、ログイン・ログアウト機能を実装します。

---

## 📝 学習のポイント

- [ ] フォームリクエストを使って、ユーザー登録のバリデーションを実装できる。
- [ ] `Hash::make()`を使って、パスワードをハッシュ化できる。
- [ ] `Auth::login()`を使って、登録後に自動ログインを実装できる。
- [ ] `createToken()`を使って、Sanctumの認証トークンを発行できる。
