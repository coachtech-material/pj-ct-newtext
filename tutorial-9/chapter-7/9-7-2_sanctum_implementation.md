# Tutorial 9-7-2: Sanctumで認証APIを実装する

## 🎯 このセクションで学ぶこと

*   Sanctumを使って、ユーザー登録APIを実装できるようになる。
*   ログインAPIとログアウトAPIを実装できるようになる。
*   認証が必要なAPIエンドポイントを保護できるようになる。

---

## 導入：実際に認証APIを作ってみよう

前のセクションで、Laravel Sanctumの概念とトークンベース認証の仕組みを学びました。このセクションでは、実際にSanctumを使って、以下の4つのAPIエンドポイントを実装します。

*   **POST /api/register**: ユーザー登録
*   **POST /api/login**: ログイン
*   **POST /api/logout**: ログアウト
*   **GET /api/user**: 認証済みユーザー情報の取得

---

## 詳細解説

### 🛠️ 準備：Sanctumの設定

#### ステップ1: `User`モデルに`HasApiTokens`トレイトを追加する

`app/Models/User.php`を開き、`HasApiTokens`トレイトを追加します。

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens; // この行を追加

    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];
}
```

`HasApiTokens`トレイトにより、`User`モデルでトークンを発行・管理できるようになります。

#### ステップ2: APIルートを設定する

`routes/api.php`を開き、以下のルートを追加します。

```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AuthController;

// 認証不要のルート
Route::post('/register', [AuthController::class, 'register']);
Route::post('/login', [AuthController::class, 'login']);

// 認証が必要なルート
Route::middleware('auth:sanctum')->group(function () {
    Route::get('/user', [AuthController::class, 'user']);
    Route::post('/logout', [AuthController::class, 'logout']);
});
```

**コードリーディング**

*   `Route::post('/register', ...)`: ユーザー登録のエンドポイント（認証不要）
*   `Route::post('/login', ...)`: ログインのエンドポイント（認証不要）
*   `Route::middleware('auth:sanctum')->group(...)`: 認証が必要なエンドポイントをグループ化
*   `auth:sanctum`ミドルウェアは、リクエストヘッダーの`Authorization: Bearer {トークン}`を検証します

---

### 📝 ユーザー登録APIの実装

`app/Http/Controllers/AuthController.php`を作成します。

```bash
docker compose exec php php artisan make:controller AuthController
```

**`app/Http/Controllers/AuthController.php`**

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;
use Illuminate\Support\Facades\Hash;

class AuthController extends Controller
{
    /**
     * ユーザー登録
     */
    public function register(Request $request)
    {
        // バリデーション
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|string|email|max:255|unique:users',
            'password' => 'required|string|min:8',
        ]);

        // ユーザーを作成
        $user = User::create([
            'name' => $validated['name'],
            'email' => $validated['email'],
            'password' => Hash::make($validated['password']),
        ]);

        // トークンを発行
        $token = $user->createToken('auth_token')->plainTextToken;

        // レスポンスを返す
        return response()->json([
            'user' => $user,
            'token' => $token,
        ], 201);
    }
}
```

**コードリーディング**

*   `$request->validate([...])`: バリデーションを実行します。
*   `Hash::make($validated['password'])`: パスワードをハッシュ化します。平文のパスワードをデータベースに保存してはいけません。
*   `$user->createToken('auth_token')`: トークンを発行します。`auth_token`は、トークンの名前です（任意）。
*   `->plainTextToken`: 発行されたトークンの平文を取得します。これをクライアントに返します。
*   `response()->json([...], 201)`: JSON形式でレスポンスを返します。`201`は「Created（作成成功）」のステータスコードです。

#### テスト：Postmanでユーザー登録を試す

Postmanで以下のリクエストを送信してみましょう。

```
POST http://localhost/api/register
Content-Type: application/json

{
  "name": "山田太郎",
  "email": "taro@example.com",
  "password": "password123"
}
```

**レスポンス**

```json
{
  "user": {
    "id": 1,
    "name": "山田太郎",
    "email": "taro@example.com",
    "created_at": "2024-12-11T12:00:00.000000Z",
    "updated_at": "2024-12-11T12:00:00.000000Z"
  },
  "token": "1|abcdefghijklmnopqrstuvwxyz"
}
```

---

### 🔑 ログインAPIの実装

`AuthController.php`に、`login`メソッドを追加します。

```php
/**
 * ログイン
 */
public function login(Request $request)
{
    // バリデーション
    $request->validate([
        'email' => 'required|email',
        'password' => 'required',
    ]);

    // ユーザーを検索
    $user = User::where('email', $request->email)->first();

    // ユーザーが存在しない、またはパスワードが一致しない場合
    if (!$user || !Hash::check($request->password, $user->password)) {
        return response()->json([
            'message' => 'メールアドレスまたはパスワードが正しくありません'
        ], 401);
    }

    // トークンを発行
    $token = $user->createToken('auth_token')->plainTextToken;

    // レスポンスを返す
    return response()->json([
        'user' => $user,
        'token' => $token,
    ]);
}
```

**コードリーディング**

*   `User::where('email', $request->email)->first()`: メールアドレスでユーザーを検索します。
*   `Hash::check($request->password, $user->password)`: 入力されたパスワードと、データベースに保存されているハッシュ化されたパスワードを比較します。
*   `401`は「Unauthorized（認証失敗）」のステータスコードです。

#### テスト：Postmanでログインを試す

```
POST http://localhost/api/login
Content-Type: application/json

{
  "email": "taro@example.com",
  "password": "password123"
}
```

**レスポンス**

```json
{
  "user": {
    "id": 1,
    "name": "山田太郎",
    "email": "taro@example.com"
  },
  "token": "2|zyxwvutsrqponmlkjihgfedcba"
}
```

---

### 👤 認証済みユーザー情報の取得

`AuthController.php`に、`user`メソッドを追加します。

```php
/**
 * 認証済みユーザー情報を取得
 */
public function user(Request $request)
{
    return response()->json($request->user());
}
```

**コードリーディング**

*   `$request->user()`: 現在認証されているユーザーを取得します。`auth:sanctum`ミドルウェアが、トークンを検証し、ユーザーを特定します。

#### テスト：Postmanで認証済みユーザー情報を取得する

```
GET http://localhost/api/user
Headers:
  Authorization: Bearer 2|zyxwvutsrqponmlkjihgfedcba
```

**レスポンス**

```json
{
  "id": 1,
  "name": "山田太郎",
  "email": "taro@example.com"
}
```

**重要なポイント**

*   `Authorization: Bearer {トークン}`ヘッダーを付けないと、`401 Unauthorized`エラーが返されます。

---

### 🚪 ログアウトAPIの実装

`AuthController.php`に、`logout`メソッドを追加します。

```php
/**
 * ログアウト
 */
public function logout(Request $request)
{
    // 現在のトークンを削除
    $request->user()->currentAccessToken()->delete();

    return response()->json([
        'message' => 'ログアウトしました'
    ]);
}
```

**コードリーディング**

*   `$request->user()->currentAccessToken()->delete()`: 現在使用されているトークンをデータベースから削除します。これにより、そのトークンは無効になります。

#### テスト：Postmanでログアウトを試す

```
POST http://localhost/api/logout
Headers:
  Authorization: Bearer 2|zyxwvutsrqponmlkjihgfedcba
```

**レスポンス**

```json
{
  "message": "ログアウトしました"
}
```

ログアウト後、同じトークンで`/api/user`にアクセスすると、`401 Unauthorized`エラーが返されます。

---

## 💡 TIP: 全てのトークンを削除する

ユーザーが複数のデバイスでログインしている場合、全てのトークンを削除したい場合があります。

```php
// 全てのトークンを削除
$request->user()->tokens()->delete();
```

---

## ✨ まとめ

このセクションでは、Laravel Sanctumを使って、認証APIを実装しました。

*   `User`モデルに`HasApiTokens`トレイトを追加することで、トークンを発行・管理できる。
*   `$user->createToken('auth_token')->plainTextToken`で、トークンを発行できる。
*   `auth:sanctum`ミドルウェアを使うことで、認証が必要なエンドポイントを保護できる。
*   `$request->user()`で、現在認証されているユーザーを取得できる。
*   `$request->user()->currentAccessToken()->delete()`で、トークンを削除（ログアウト）できる。


---

## 📝 学習のポイント

- [ ] `HasApiTokens`トレイトを使って、トークンを発行・管理できる。
- [ ] `$user->createToken()->plainTextToken`で、トークンを発行できる。
- [ ] `auth:sanctum`ミドルウェアで、認証が必要なエンドポイントを保護できる。
- [ ] `$request->user()`で、現在認証されているユーザーを取得できる。
- [ ] `currentAccessToken()->delete()`で、トークンを削除（ログアウト）できる。
