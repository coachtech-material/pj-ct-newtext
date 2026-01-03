# Tutorial 13-3-1: SanctumによるAPI認証

## 🎯 このセクションで学ぶこと

- Laravel SanctumによるAPI認証の仕組みを理解する
- ログイン・ログアウトAPIの実装方法を学ぶ
- トークンベース認証の実装方法を理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜCRUD APIの後に『API認証』を実装するのか？」

CRUD APIが完成したら、次は「API認証」です。

---

### 理由1: セキュリティの確保

現状のAPIは、**誰でもアクセスできる**状態です。

本番環境では、認証されたユーザーだけがアクセスできるようにする必要があります。

---

### 理由2: APIはセッションを使わない

Webアプリケーションでは「セッション」で認証状態を管理しました。

しかし、APIでは**トークンベースの認証**を使います。

| 特徴 | 説明 |
|------|------|
| ステートレス | サーバーに状態を持たない |
| スケーラブル | 複数サーバーで動作可能 |
| モバイル対応 | モバイルアプリでも使える |

---

### 理由3: Laravel Sanctum

Laravelには**Sanctum**というAPI認証パッケージがあります。

シンプルで使いやすく、SPAやモバイルアプリの認証に最適です。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | Sanctumのセットアップ | パッケージの設定 |
| Step 2 | 認証APIの実装 | ログイン・ログアウト |
| Step 3 | APIのテスト | 動作確認 |

> 💡 **ポイント**: Sanctumは、APIトークン認証とSPA認証の両方をサポートしています。

---

## Step 1: Sanctumのセットアップ

### 1-1. Laravel Sanctumとは

**Laravel Sanctum**とは、**LaravelでAPI認証を簡単に実装するためのパッケージ**です。

| 特徴 | 説明 |
|------|------|
| シンプル | 簡単に実装できる |
| トークンベース | トークンを使って認証する |
| SPA対応 | シングルページアプリケーションにも対応 |

---

### 1-2. Sanctumのインストール

Laravel 11では、Sanctumがデフォルトでインストールされています。

もしインストールされていない場合は、以下のコマンドでインストールします。

```bash
composer require laravel/sanctum
php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
php artisan migrate
```

---

### 1-3. Userモデルの設定

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

> 💡 **ポイント**: `HasApiTokens`トレイトを使うことで、ユーザーがAPIトークンを持てるようになります。

---

## Step 2: 認証APIの実装

### 2-1. 認証APIコントローラーの作成

```bash
php artisan make:controller Api/AuthController
```

---

### 2-2. コントローラーの実装

**ファイル**: `app/Http/Controllers/Api/AuthController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

class AuthController extends Controller
{
    /**
     * ユーザー登録
     */
    public function register(Request $request): JsonResponse
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
    public function login(Request $request): JsonResponse
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
    public function logout(Request $request): JsonResponse
    {
        $request->user()->currentAccessToken()->delete();

        return response()->json([
            'message' => 'ログアウトしました'
        ], 200);
    }

    /**
     * 認証済みユーザー情報を取得
     */
    public function user(Request $request): JsonResponse
    {
        return response()->json([
            'user' => $request->user()
        ], 200);
    }
}
```

---

### 2-3. コードリーディング

| コード | 説明 |
|--------|------|
| `$user->createToken('auth_token')->plainTextToken` | APIトークンを作成 |
| `Auth::attempt($request->only('email', 'password'))` | 認証を試みる |
| `$request->user()->currentAccessToken()->delete()` | 現在のトークンを削除 |

---

### 2-4. ルーティングの設定

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

## Step 3: APIのテスト

### 3-1. ユーザー登録

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

### 3-2. ログイン

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

### 3-3. 認証済みユーザー情報を取得

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

### 3-4. ログアウト

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

### 3-5. 未認証時のエラーレスポンス

認証が必要なAPIに、トークンなしでアクセスすると、以下のようなエラーが返されます。

```json
{
  "message": "Unauthenticated."
}
```

HTTPステータスコード: `401 Unauthorized`

---

## 🚨 よくある間違い

### 間違い1: HasApiTokensトレイトを忘れる

**問題**: トークンが作成できない

**対処法**: Userモデルに`use HasApiTokens;`を追加します。

---

### 間違い2: auth:sanctumミドルウェアを忘れる

**問題**: 認証なしでAPIにアクセスできてしまう

**対処法**: 認証が必要なルートには、`auth:sanctum`ミドルウェアを適用します。

---

### 間違い3: トークンを平文で保存する

**問題**: セキュリティリスク

**対処法**: トークンは、データベースにハッシュ化されて保存されます。クライアントには、`plainTextToken`を返します。

---

## 💡 TIP: トークンの有効期限

デフォルトでは、Sanctumのトークンに有効期限はありません。

有効期限を設定する場合は、`config/sanctum.php`で設定します。

```php
'expiration' => 60, // 60分
```

---

## ✨ まとめ

このセクションでは、SanctumによるAPI認証について学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | Sanctumのセットアップと設定 |
| Step 2 | 認証APIの実装（ログイン・ログアウト） |
| Step 3 | APIのテストと動作確認 |

次のセクションでは、APIのセキュリティについて学びます。

---
