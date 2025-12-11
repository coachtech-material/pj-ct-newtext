# Tutorial 12-3-3: ログインAPIとトークン発行

## 🎯 このセクションで学ぶこと

*   ログインAPIを実装する方法を学ぶ。
*   トークンを発行する方法を学ぶ。
*   トークンを使った認証の流れを理解する。
*   ログアウトAPIを実装する方法を学ぶ。

---

## 導入：なぜトークンが必要なのか

APIでは、**セッションを使わない**ため、**トークン**を使って認証を行います。

**トークンベース認証の流れ**:

1.  ユーザーがログインする
2.  サーバーがトークンを発行する
3.  クライアントがトークンを保存する
4.  クライアントがリクエストにトークンを含める
5.  サーバーがトークンを検証する

---

## 詳細解説

### 🔍 ログインAPIの実装

ログインAPIを実装します。

**エンドポイント**: `POST /api/login`

**リクエストボディ**:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

**レスポンス例（成功時）**:

```json
{
  "token": "1|abcdefghijklmnopqrstuvwxyz",
  "user": {
    "id": 1,
    "name": "田中太郎",
    "email": "user@example.com"
  }
}
```

---

### 🔍 コントローラーの作成

```bash
php artisan make:controller Api/AuthController
```

**ファイル**: `app/Http/Controllers/Api/AuthController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

class AuthController extends Controller
{
    public function login(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);
        
        $user = User::where('email', $request->email)->first();
        
        if (!$user || !Hash::check($request->password, $user->password)) {
            throw ValidationException::withMessages([
                'email' => ['The provided credentials are incorrect.'],
            ]);
        }
        
        $token = $user->createToken('api-token')->plainTextToken;
        
        return response()->json([
            'token' => $token,
            'user' => $user,
        ], 200);
    }
}
```

**ポイント**:
*   `User::where('email', $request->email)->first()`で、ユーザーを取得する
*   `Hash::check()`で、パスワードを検証する
*   `$user->createToken()`で、トークンを発行する
*   `plainTextToken`で、トークンの文字列を取得する

---

### 🔍 ルートの定義

**ファイル**: `routes/api.php`

```php
use App\Http\Controllers\Api\AuthController;

Route::post('/login', [AuthController::class, 'login']);
```

---

### 🔍 実践演習: ログインAPIをテストしてください

Thunder Clientで、以下のリクエストを送信してください。

**1. 成功する場合**

*   メソッド: `POST`
*   URL: `http://localhost:8000/api/login`
*   Body（JSON）:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

**期待されるレスポンス**:

*   ステータスコード: `200 OK`
*   ボディ: トークンとユーザー情報

---

**2. 失敗する場合**

*   メソッド: `POST`
*   URL: `http://localhost:8000/api/login`
*   Body（JSON）:

```json
{
  "email": "user@example.com",
  "password": "wrong-password"
}
```

**期待されるレスポンス**:

*   ステータスコード: `422 Unprocessable Entity`
*   ボディ: エラーメッセージ

---

### 🔍 トークンの保存（クライアント側）

クライアント側では、トークンを保存します。

**JavaScript（ローカルストレージ）**:

```javascript
fetch('http://localhost:8000/api/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'password',
  }),
})
  .then(response => response.json())
  .then(data => {
    // トークンを保存
    localStorage.setItem('token', data.token);
    console.log('ログイン成功:', data.user);
  })
  .catch(error => {
    console.error('エラー:', error);
  });
```

---

### 🔍 トークンを使ったリクエスト

トークンを使って、認証が必要なAPIにリクエストを送信します。

**Thunder Client**:

1.  メソッド: `GET`
2.  URL: `http://localhost:8000/api/tasks`
3.  「Headers」タブをクリック
4.  キー: `Authorization`
5.  値: `Bearer トークン`

**JavaScript**:

```javascript
const token = localStorage.getItem('token');

fetch('http://localhost:8000/api/tasks', {
  method: 'GET',
  headers: {
    'Authorization': `Bearer ${token}`,
  },
})
  .then(response => response.json())
  .then(data => {
    console.log('タスク一覧:', data);
  })
  .catch(error => {
    console.error('エラー:', error);
  });
```

---

### 🔍 ログアウトAPIの実装

ログアウトAPIを実装します。

**エンドポイント**: `POST /api/logout`

**ファイル**: `app/Http/Controllers/Api/AuthController.php`

```php
public function logout(Request $request)
{
    $request->user()->currentAccessToken()->delete();
    
    return response()->json([
        'message' => 'Logged out successfully'
    ], 200);
}
```

**ポイント**:
*   `$request->user()`で、認証済みユーザーを取得する
*   `currentAccessToken()->delete()`で、現在のトークンを削除する

---

### 🔍 ルートの定義（ログアウト）

**ファイル**: `routes/api.php`

```php
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
});
```

**ポイント**:
*   `auth:sanctum`ミドルウェアを適用する
*   認証が必要なAPIは、このグループ内に定義する

---

### 🔍 実践演習: ログアウトAPIをテストしてください

Thunder Clientで、以下のリクエストを送信してください。

*   メソッド: `POST`
*   URL: `http://localhost:8000/api/logout`
*   Headers:
    *   キー: `Authorization`
    *   値: `Bearer トークン`

**期待されるレスポンス**:

*   ステータスコード: `200 OK`
*   ボディ: `{"message": "Logged out successfully"}`

---

### 🔍 すべてのトークンを削除する

すべてのトークンを削除する場合は、以下のようにします。

```php
public function logout(Request $request)
{
    $request->user()->tokens()->delete();
    
    return response()->json([
        'message' => 'Logged out from all devices'
    ], 200);
}
```

---

### 🔍 トークンの有効期限を設定する

トークンの有効期限を設定できます。

**ファイル**: `config/sanctum.php`

```php
'expiration' => 60, // 60分
```

**ポイント**:
*   `expiration`を設定すると、トークンの有効期限が設定される
*   `null`の場合は、有効期限なし

---

### 💡 TIP: トークンの名前を変える

トークンに名前を付けることができます。

```php
$token = $user->createToken('mobile-app')->plainTextToken;
$token = $user->createToken('web-app')->plainTextToken;
```

---

### 🚨 よくある間違い

#### 間違い1: パスワードをそのまま比較する

パスワードは、`Hash::check()`で検証します。

```php
// ❌ 間違い
if ($user->password !== $request->password) {
    // ...
}

// ✅ 正しい
if (!Hash::check($request->password, $user->password)) {
    // ...
}
```

---

#### 間違い2: トークンをそのまま返す

トークンは、`plainTextToken`で取得します。

```php
// ❌ 間違い
$token = $user->createToken('api-token');

// ✅ 正しい
$token = $user->createToken('api-token')->plainTextToken;
```

---

#### 間違い3: Bearerを忘れる

Authorizationヘッダーには、`Bearer`を付けます。

```
// ❌ 間違い
Authorization: トークン

// ✅ 正しい
Authorization: Bearer トークン
```

---

## ✨ まとめ

このセクションでは、ログインAPIとトークン発行を学びました。

*   ログインAPIを実装した。
*   トークンを発行した。
*   トークンを使った認証の流れを理解した。
*   ログアウトAPIを実装した。

次のセクションでは、認証が必要なAPIの実装について学びます。

---

## 📝 学習のポイント

- [ ] ログインAPIを実装した。
- [ ] トークンを発行した。
- [ ] トークンを使ったリクエストを送信した。
- [ ] ログアウトAPIを実装した。
- [ ] トークンの有効期限を設定した。
