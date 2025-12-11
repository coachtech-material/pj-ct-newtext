# Tutorial 12-3-1: SanctumによるAPI認証

## 🎯 このセクションで学ぶこと

*   Laravel SanctumによるAPI認証の仕組みを理解する。
*   ログイン・ログアウトAPIの実装方法を学ぶ。
*   トークンベース認証の実装方法を理解する。

---

## 導入：API認証とは

**API認証（API Authentication）**とは、**APIにアクセスするユーザーを識別する仕組み**です。

API認証を実装することで、以下のようなことが可能になります。

*   **ログインユーザーのみがAPIにアクセスできる**: 未認証ユーザーはアクセスできない
*   **ユーザーごとにデータを管理できる**: 各ユーザーのタスクを管理できる
*   **セキュリティが向上する**: 不正なアクセスを防ぐことができる

このセクションでは、**Laravel Sanctum**を使ったAPI認証の実装方法を学びます。

---

## 詳細解説

### 🔍 Laravel Sanctumとは

**Laravel Sanctum**とは、**LaravelでAPI認証を簡単に実装するためのパッケージ**です。

Sanctumは、以下のような特徴があります。

*   **シンプル**: 簡単に実装できる
*   **トークンベース**: トークンを使って認証する
*   **SPA対応**: シングルページアプリケーション（SPA）にも対応

---

### 🔍 Sanctumのインストール

Laravel 11では、Sanctumがデフォルトでインストールされています。

もしインストールされていない場合は、以下のコマンドでインストールします。

```bash
composer require laravel/sanctum
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
php artisan migrate
```

---

### 🔍 Userモデルの設定

**ファイル**: `app/Models/User.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasFactory, Notifiable, HasApiTokens;

    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected function casts(): array
    {
        return [
            'email_verified_at' => 'datetime',
            'password' => 'hashed',
        ];
    }
}
```

---

### 🔍 コードリーディング

#### `use HasApiTokens;`

*   `HasApiTokens`トレイトを使うことで、ユーザーがAPIトークンを持てるようになります。

---

### 🔍 認証APIコントローラーの作成

```bash
php artisan make:controller Api/AuthController
```

---

**ファイル**: `app/Http/Controllers/Api/AuthController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

class AuthController extends Controller
{
    /**
     * ユーザー登録
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

        $token = $user->createToken('auth_token')->plainTextToken;

        return response()->json([
            'message' => 'ユーザー登録が完了しました',
            'user' => $user,
            'token' => $token,
        ], 201);
    }

    /**
     * ログイン
     */
    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);

        if (!Auth::attempt($request->only('email', 'password'))) {
            throw ValidationException::withMessages([
                'email' => ['メールアドレスまたはパスワードが正しくありません'],
            ]);
        }

        $user = Auth::user();
        $token = $user->createToken('auth_token')->plainTextToken;

        return response()->json([
            'message' => 'ログインしました',
            'user' => $user,
            'token' => $token,
        ], 200);
    }

    /**
     * ログアウト
     */
    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete();

        return response()->json([
            'message' => 'ログアウトしました'
        ], 200);
    }

    /**
     * 認証済みユーザー情報を取得
     */
    public function user(Request $request)
    {
        return response()->json([
            'user' => $request->user()
        ], 200);
    }
}
```

---

### 🔍 コードリーディング

#### `$user->createToken('auth_token')->plainTextToken`

*   `createToken()`メソッドで、ユーザーのAPIトークンを作成します。
*   `plainTextToken`プロパティで、トークンの文字列を取得します。
*   このトークンは、APIリクエストの`Authorization`ヘッダーに含めます。

---

#### `Auth::attempt($request->only('email', 'password'))`

*   `attempt()`メソッドで、メールアドレスとパスワードで認証を試みます。
*   認証に成功すると`true`、失敗すると`false`を返します。

---

#### `$request->user()->currentAccessToken()->delete()`

*   `currentAccessToken()`メソッドで、現在のリクエストで使用されているトークンを取得します。
*   `delete()`メソッドで、トークンを削除します。

---

### 🔍 ルーティングの設定

**ファイル**: `routes/api.php`

```php
<?php

use App\Http\Controllers\Api\AuthController;
use App\Http\Controllers\Api\TaskController;
use Illuminate\Support\Facades\Route;

// 認証不要のルート
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);

// 認証が必要なルート
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
    Route::get('/user', [AuthController::class, 'user']);
    Route::apiResource('tasks', TaskController::class);
});
```

---

### 🔍 APIのテスト

#### 1. ユーザー登録

```bash
curl -X POST http://localhost/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Taro Yamada",
    "email": "taro@example.com",
    "password": "password123",
    "password_confirmation": "password123"
  }'
```

**レスポンス**:

```json
{
  "message": "ユーザー登録が完了しました",
  "user": {
    "id": 1,
    "name": "Taro Yamada",
    "email": "taro@example.com"
  },
  "token": "1|abcdefghijklmnopqrstuvwxyz"
}
```

---

#### 2. ログイン

```bash
curl -X POST http://localhost/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "taro@example.com",
    "password": "password123"
  }'
```

**レスポンス**:

```json
{
  "message": "ログインしました",
  "user": {
    "id": 1,
    "name": "Taro Yamada",
    "email": "taro@example.com"
  },
  "token": "2|abcdefghijklmnopqrstuvwxyz"
}
```

---

#### 3. 認証済みユーザー情報を取得

```bash
curl -X GET http://localhost/api/user \
  -H "Authorization: Bearer 2|abcdefghijklmnopqrstuvwxyz"
```

**レスポンス**:

```json
{
  "user": {
    "id": 1,
    "name": "Taro Yamada",
    "email": "taro@example.com"
  }
}
```

---

#### 4. ログアウト

```bash
curl -X POST http://localhost/api/logout \
  -H "Authorization: Bearer 2|abcdefghijklmnopqrstuvwxyz"
```

**レスポンス**:

```json
{
  "message": "ログアウトしました"
}
```

---

### 🔍 未認証時のエラーレスポンス

認証が必要なAPIに、トークンなしでアクセスすると、以下のようなエラーが返されます。

```json
{
  "message": "Unauthenticated."
}
```

HTTPステータスコード: `401 Unauthorized`

---

### 💡 TIP: トークンの有効期限

デフォルトでは、Sanctumのトークンに有効期限はありません。

有効期限を設定する場合は、`config/sanctum.php`で設定します。

**ファイル**: `config/sanctum.php`

```php
'expiration' => 60, // 60分
```

---

### 💡 TIP: 複数のトークンを管理する

Sanctumでは、ユーザーが複数のトークンを持つことができます。

例えば、Webアプリ用とモバイルアプリ用で異なるトークンを発行することができます。

```php
$webToken = $user->createToken('web-token')->plainTextToken;
$mobileToken = $user->createToken('mobile-token')->plainTextToken;
```

---

### 🚨 よくある間違い

#### 間違い1: `HasApiTokens`トレイトを忘れる

**対処法**: Userモデルに`use HasApiTokens;`を追加します。

---

#### 間違い2: `auth:sanctum`ミドルウェアを忘れる

**対処法**: 認証が必要なルートには、`auth:sanctum`ミドルウェアを適用します。

---

#### 間違い3: トークンを平文で保存する

**対処法**: トークンは、データベースにハッシュ化されて保存されます。クライアントには、`plainTextToken`を返します。

---

## ✨ まとめ

このセクションでは、SanctumによるAPI認証について学びました。

*   Laravel Sanctumは、API認証を簡単に実装するためのパッケージである。
*   `HasApiTokens`トレイトを使うことで、ユーザーがAPIトークンを持てるようになる。
*   `createToken()`メソッドで、APIトークンを作成する。
*   `auth:sanctum`ミドルウェアで、認証が必要なルートを保護する。

次のセクションでは、APIのセキュリティについて学びます。

---

## 📝 学習のポイント

- [ ] Laravel SanctumによるAPI認証の仕組みを理解した。
- [ ] ログイン・ログアウトAPIの実装方法を学んだ。
- [ ] トークンベース認証の実装方法を理解した。
