# Tutorial 12-3-3: ログインAPIとトークン発行

## 🎯 このセクションで学ぶこと

- ログインAPIを実装する方法を学ぶ
- トークンを発行する方法を学ぶ
- トークンを使った認証の流れを理解する
- ログアウトAPIを実装する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜセキュリティの後に『ログインAPI』を実装するのか？」

セキュリティの基礎を学んだら、次は「ログインAPI」です。

---

### 理由1: トークンの発行

ユーザーがログインしたら、**APIトークンを発行**します。

このトークンを使って、以降のAPIリクエストを認証します。

---

### 理由2: 認証フロー

| 順番 | 処理 |
|------|------|
| 1 | ユーザーがメールアドレスとパスワードを送信 |
| 2 | サーバーが認証情報を検証 |
| 3 | 正しければトークンを発行 |
| 4 | クライアントはトークンを保存 |
| 5 | 以降のリクエストでトークンを送信 |

---

### 理由3: Sanctumのトークン機能

Sanctumでは、`createToken()`メソッドで**簡単にトークンを発行**できます。

```php
$token = $user->createToken('api-token')->plainTextToken;
```

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | ログインAPIの実装 | メールとパスワードで認証 |
| Step 2 | トークンを使ったリクエスト | 認証済みAPIへのアクセス |
| Step 3 | ログアウトAPIの実装 | トークンの削除 |

> 💡 **ポイント**: トークンは「パスワードの代わり」として使われます。

---

## Step 1: ログインAPIの実装

### 1-1. ログインAPIの仕様

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

### 1-2. コントローラーの作成

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
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Hash;
use Illuminate\Validation\ValidationException;

class AuthController extends Controller
{
    public function login(Request $request): JsonResponse
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

---

### 1-3. コードリーディング

| コード | 説明 |
|--------|------|
| `User::where('email', $request->email)->first()` | ユーザーを取得 |
| `Hash::check($request->password, $user->password)` | パスワードを検証 |
| `$user->createToken('api-token')->plainTextToken` | トークンを発行 |

---

### 1-4. ルートの定義

**ファイル**: `routes/api.php`

```php
use App\Http\Controllers\Api\AuthController;

Route::post('/login', [AuthController::class, 'login']);
```

---

### 1-5. Thunder Clientでテスト

**1. 成功する場合**

- メソッド: `POST`
- URL: `http://localhost:8000/api/login`
- Body（JSON）:

```json
{
  "email": "user@example.com",
  "password": "password"
}
```

- 期待: ステータスコード `200 OK`

**2. 失敗する場合**

- メソッド: `POST`
- URL: `http://localhost:8000/api/login`
- Body（JSON）:

```json
{
  "email": "user@example.com",
  "password": "wrong-password"
}
```

- 期待: ステータスコード `422 Unprocessable Entity`

---

## Step 2: トークンを使ったリクエスト

### 2-1. トークンの保存（クライアント側）

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

### 2-2. トークンを使ったリクエスト

トークンを使って、認証が必要なAPIにリクエストを送信します。

**Thunder Client**:

1. メソッド: `GET`
2. URL: `http://localhost:8000/api/tasks`
3. 「Headers」タブをクリック
4. キー: `Authorization`
5. 値: `Bearer トークン`

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

## Step 3: ログアウトAPIの実装

### 3-1. ログアウトAPIの仕様

**エンドポイント**: `POST /api/logout`

**ファイル**: `app/Http/Controllers/Api/AuthController.php`

```php
public function logout(Request $request): JsonResponse
{
    $request->user()->currentAccessToken()->delete();
    
    return response()->json([
        'message' => 'Logged out successfully'
    ], 200);
}
```

---

### 3-2. コードリーディング

| コード | 説明 |
|--------|------|
| `$request->user()` | 認証済みユーザーを取得 |
| `currentAccessToken()->delete()` | 現在のトークンを削除 |

---

### 3-3. ルートの定義（ログアウト）

**ファイル**: `routes/api.php`

```php
Route::middleware('auth:sanctum')->group(function () {
    Route::post('/logout', [AuthController::class, 'logout']);
});
```

> 💡 **ポイント**: `auth:sanctum`ミドルウェアを適用し、認証が必要なAPIはこのグループ内に定義します。

---

### 3-4. すべてのトークンを削除する

すべてのトークンを削除する場合は、以下のようにします。

```php
public function logout(Request $request): JsonResponse
{
    $request->user()->tokens()->delete();
    
    return response()->json([
        'message' => 'Logged out from all devices'
    ], 200);
}
```

---

### 3-5. トークンの有効期限を設定する

**ファイル**: `config/sanctum.php`

```php
'expiration' => 60, // 60分
```

| 設定 | 説明 |
|------|------|
| 数値 | 有効期限（分） |
| null | 有効期限なし |

---

## 🚨 よくある間違い

### 間違い1: パスワードをそのまま比較する

**問題**: パスワードはハッシュ化されている

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

### 間違い2: トークンをそのまま返す

**問題**: オブジェクトではなく文字列を返す

```php
// ❌ 間違い
$token = $user->createToken('api-token');

// ✅ 正しい
$token = $user->createToken('api-token')->plainTextToken;
```

---

### 間違い3: Bearerを忘れる

**問題**: Authorizationヘッダーの形式が間違い

```
// ❌ 間違い
Authorization: トークン

// ✅ 正しい
Authorization: Bearer トークン
```

---

## 💡 TIP: トークンの名前を変える

トークンに名前を付けることができます。

```php
$token = $user->createToken('mobile-app')->plainTextToken;
$token = $user->createToken('web-app')->plainTextToken;
```

---

## ✨ まとめ

このセクションでは、ログインAPIとトークン発行を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | ログインAPIの実装とトークン発行 |
| Step 2 | トークンを使ったリクエストの送信 |
| Step 3 | ログアウトAPIの実装とトークン削除 |

次のセクションでは、認証が必要なAPIの実装について学びます。

---

## 📝 学習のポイント

- [ ] ログインAPIを実装した
- [ ] トークンを発行した
- [ ] トークンを使ったリクエストを送信した
- [ ] ログアウトAPIを実装した
- [ ] トークンの有効期限を設定した
