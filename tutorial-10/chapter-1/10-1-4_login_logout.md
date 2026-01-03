# Tutorial 10-1-4: ログイン・ログアウト機能の実装

## 🎯 このセクションで学ぶこと

*   Laravel Sanctumを使って、ログイン機能を実装できるようになる。
*   ログアウト機能を実装できるようになる。
*   認証トークンの管理方法を理解する。

---

## 導入：「ログイン」と「ログアウト」

前のセクションで、ユーザー登録機能を実装しました。次は、**ログイン機能**と**ログアウト機能**を実装します。

*   **ログイン**: ユーザーがメールアドレスとパスワードを入力し、認証される
*   **ログアウト**: ユーザーが認証状態を解除する

このセクションでは、Laravel Sanctumを使って、これらの機能を実装します。

---

## 詳細解説

### 📝 ログインの流れ

1. ユーザーがメールアドレスとパスワードを入力
2. サーバーがバリデーションを実行
3. メールアドレスでユーザーを検索
4. パスワードが一致するか確認
5. 認証トークンを発行（API認証の場合）
6. ログイン状態にする

---

### 🔧 ステップ1: フォームリクエストの作成

```bash
php artisan make:request LoginRequest
```

**`app/Http/Requests/LoginRequest.php`**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class LoginRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'email' => 'required|email',
            'password' => 'required|string',
        ];
    }

    public function messages()
    {
        return [
            'email.required' => 'メールアドレスは必須です。',
            'password.required' => 'パスワードは必須です。',
        ];
    }
}
```

---

### 🔧 ステップ2: コントローラーの実装

**`app/Http/Controllers/AuthController.php`**

```php
use App\Http\Requests\LoginRequest;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use App\Models\User;

public function login(LoginRequest $request)
{
    $validated = $request->validated();

    // ユーザーを検索
    $user = User::where('email', $validated['email'])->first();

    // ユーザーが存在しない、またはパスワードが一致しない
    if (!$user || !Hash::check($validated['password'], $user->password)) {
        return response()->json([
            'message' => 'The provided credentials are incorrect.',
        ], 401);
    }

    // ログイン状態にする
    Auth::login($user);

    // 認証トークンを発行
    $token = $user->createToken('auth_token')->plainTextToken;

    return response()->json([
        'message' => 'Login successful',
        'user' => $user,
        'token' => $token,
    ]);
}
```

**コードリーディング**

*   `User::where('email', $validated['email'])->first()`: メールアドレスでユーザーを検索
*   `Hash::check()`: パスワードが一致するか確認
*   `Auth::login()`: ユーザーをログイン状態にする
*   `createToken()`: Sanctumの認証トークンを発行

---

### 🔧 ステップ3: ルートの定義

**`routes/api.php`**

```php
Route::post('/login', [AuthController::class, 'login']);
```

---

### 🚀 実践例1: Postmanでテスト

#### リクエスト

```
POST http://localhost/api/login
Content-Type: application/json

{
    "email": "yamada@example.com",
    "password": "password123"
}
```

#### レスポンス

```json
{
    "message": "Login successful",
    "user": {
        "id": 1,
        "name": "山田太郎",
        "email": "yamada@example.com",
        "created_at": "2024-01-01T00:00:00.000000Z",
        "updated_at": "2024-01-01T00:00:00.000000Z"
    },
    "token": "2|xyz789..."
}
```

---

### 🔧 ログアウト機能の実装

#### コントローラー

```php
public function logout(Request $request)
{
    // 現在のトークンを削除
    $request->user()->currentAccessToken()->delete();

    return response()->json([
        'message' => 'Logout successful',
    ]);
}
```

**コードリーディング**

*   `$request->user()`: 認証済みユーザーを取得
*   `currentAccessToken()`: 現在使用中のトークンを取得
*   `delete()`: トークンを削除

---

### 🔧 ルートの定義

**`routes/api.php`**

```php
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
});
```

**コードリーディング**

*   `auth:sanctum`: Sanctumの認証ミドルウェア
*   このルートは、認証済みユーザーのみがアクセスできる

---

### 🚀 実践例2: Postmanでテスト

#### リクエスト

```
POST http://localhost/api/logout
Authorization: Bearer 2|xyz789...
```

#### レスポンス

```json
{
    "message": "Logout successful"
}
```

---

### 💡 TIP: 全てのトークンを削除

```php
public function logoutAll(Request $request)
{
    // 全てのトークンを削除
    $request->user()->tokens()->delete();

    return response()->json([
        'message' => 'All tokens deleted',
    ]);
}
```

---

### 🚀 実践例3: Web版のログイン

#### コントローラー

```php
public function login(LoginRequest $request)
{
    $validated = $request->validated();

    if (Auth::attempt($validated)) {
        $request->session()->regenerate();

        return redirect()->intended('/dashboard');
    }

    return back()->withErrors([
        'email' => 'The provided credentials do not match our records.',
    ])->onlyInput('email');
}
```

**コードリーディング**

*   `Auth::attempt()`: メールアドレスとパスワードで認証を試みる
*   `$request->session()->regenerate()`: セッションIDを再生成（セッション固定攻撃を防ぐ）
*   `redirect()->intended()`: ログイン前にアクセスしようとしたページにリダイレクト

---

### 🚀 実践例4: Web版のログアウト

#### コントローラー

```php
public function logout(Request $request)
{
    Auth::logout();

    $request->session()->invalidate();
    $request->session()->regenerateToken();

    return redirect('/');
}
```

**コードリーディング**

*   `Auth::logout()`: ログアウト
*   `$request->session()->invalidate()`: セッションを無効化
*   `$request->session()->regenerateToken()`: CSRFトークンを再生成

---

### 💡 TIP: Remember Me機能

#### ログイン時

```php
$credentials = $request->only('email', 'password');
$remember = $request->filled('remember');

if (Auth::attempt($credentials, $remember)) {
    // ログイン成功
}
```

---

### 🔍 認証トークンの管理

#### トークンの一覧を取得

```php
$tokens = $request->user()->tokens;

foreach ($tokens as $token) {
    echo $token->name;
    echo $token->created_at;
}
```

#### 特定のトークンを削除

```php
$request->user()->tokens()->where('id', $tokenId)->delete();
```

---

### 🚀 実践例5: トークンに名前を付ける

```php
$token = $user->createToken('mobile_app')->plainTextToken;
$token = $user->createToken('web_app')->plainTextToken;
```

これにより、どのデバイスからログインしているかを管理できます。

---

### 🚨 よくある間違い

#### 間違い1: `Auth::attempt()`にハッシュ化されたパスワードを渡す

```php
Auth::attempt([
    'email' => $validated['email'],
    'password' => Hash::make($validated['password']), // NG
]);
```

**対処法**: `Auth::attempt()`は、自動的にパスワードをハッシュ化して比較します。

```php
Auth::attempt([
    'email' => $validated['email'],
    'password' => $validated['password'], // OK
]);
```

---

#### 間違い2: ログアウト時にトークンを削除しない

```php
public function logout(Request $request)
{
    Auth::logout(); // これだけではトークンは削除されない
    
    return response()->json(['message' => 'Logout successful']);
}
```

**対処法**: トークンを明示的に削除します。

```php
public function logout(Request $request)
{
    $request->user()->currentAccessToken()->delete(); // OK
    
    return response()->json(['message' => 'Logout successful']);
}
```

---

## ✨ まとめ

このセクションでは、Laravel Sanctumを使って、ログイン・ログアウト機能を実装しました。

*   `Auth::attempt()`または`Hash::check()`を使って、ログイン機能を実装した。
*   `createToken()`を使って、Sanctumの認証トークンを発行した。
*   `currentAccessToken()->delete()`を使って、ログアウト機能を実装した。
*   `tokens()->delete()`を使って、全てのトークンを削除できる。

次のセクションでは、認証済みユーザーの取得とミドルウェアについて学びます。

---
