# Tutorial 9-11-6: 認証機能のテスト

## 🎯 このセクションで学ぶこと

*   認証機能のテストを書き、ログイン・ログアウトの動作を検証できるようになる。
*   `actingAs()`を使って、認証済みユーザーとしてテストを実行できるようになる。
*   認証が必要なエンドポイントのテストを書けるようになる。

---

## 導入：「認証機能のテスト」とは何か？

**認証機能のテスト**とは、**ログイン・ログアウト・ユーザー登録などの認証機能が正しく動作するかを検証するテスト**です。

例えば、以下のようなテストを書きます。

*   ユーザー登録が正しく動作するか
*   ログインが正しく動作するか
*   ログアウトが正しく動作するか
*   認証が必要なエンドポイントにアクセスできるか

このセクションでは、認証機能のテストの基礎を学びます。

---

## 詳細解説

### 🚀 実践例1: ユーザー登録のテスト

```php
use Illuminate\Foundation\Testing\RefreshDatabase;

class AuthTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_register()
    {
        $data = [
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => 'password',
            'password_confirmation' => 'password',
        ];

        $response = $this->post('/api/register', $data);

        $response->assertStatus(201);
        $response->assertJsonStructure([
            'user' => ['id', 'name', 'email'],
            'token',
        ]);

        $this->assertDatabaseHas('users', [
            'name' => 'Test User',
            'email' => 'test@example.com',
        ]);
    }
}
```

---

### 🚀 実践例2: ログインのテスト

```php
public function test_user_can_login()
{
    $user = User::factory()->create([
        'email' => 'test@example.com',
        'password' => bcrypt('password'),
    ]);

    $data = [
        'email' => 'test@example.com',
        'password' => 'password',
    ];

    $response = $this->post('/api/login', $data);

    $response->assertStatus(200);
    $response->assertJsonStructure([
        'user' => ['id', 'name', 'email'],
        'token',
    ]);
}
```

---

### 🚀 実践例3: ログインに失敗するテスト

```php
public function test_user_cannot_login_with_invalid_credentials()
{
    $user = User::factory()->create([
        'email' => 'test@example.com',
        'password' => bcrypt('password'),
    ]);

    $data = [
        'email' => 'test@example.com',
        'password' => 'wrong-password',
    ];

    $response = $this->post('/api/login', $data);

    $response->assertStatus(401);
    $response->assertJson([
        'message' => 'Invalid credentials',
    ]);
}
```

---

### 🚀 実践例4: ログアウトのテスト

```php
public function test_user_can_logout()
{
    $user = User::factory()->create();

    $response = $this->actingAs($user, 'sanctum')
        ->post('/api/logout');

    $response->assertStatus(200);
    $response->assertJson([
        'message' => 'Logged out successfully',
    ]);
}
```

---

### 🚀 実践例5: 認証済みユーザーのプロフィール取得

```php
public function test_authenticated_user_can_get_profile()
{
    $user = User::factory()->create();

    $response = $this->actingAs($user, 'sanctum')
        ->get('/api/profile');

    $response->assertStatus(200);
    $response->assertJson([
        'user' => [
            'id' => $user->id,
            'name' => $user->name,
            'email' => $user->email,
        ]
    ]);
}
```

---

### 🚀 実践例6: 未認証ユーザーはアクセスできない

```php
public function test_unauthenticated_user_cannot_access_profile()
{
    $response = $this->get('/api/profile');

    $response->assertStatus(401);
    $response->assertJson([
        'message' => 'Unauthenticated.',
    ]);
}
```

---

### 🚀 実践例7: バリデーションエラー

```php
public function test_register_requires_name()
{
    $data = [
        'email' => 'test@example.com',
        'password' => 'password',
        'password_confirmation' => 'password',
        // nameが不足
    ];

    $response = $this->post('/api/register', $data);

    $response->assertStatus(422);
    $response->assertJsonValidationErrors(['name']);
}

public function test_register_requires_valid_email()
{
    $data = [
        'name' => 'Test User',
        'email' => 'invalid-email', // 無効なメールアドレス
        'password' => 'password',
        'password_confirmation' => 'password',
    ];

    $response = $this->post('/api/register', $data);

    $response->assertStatus(422);
    $response->assertJsonValidationErrors(['email']);
}
```

---

### 🚀 実践例8: パスワード確認のテスト

```php
public function test_register_requires_password_confirmation()
{
    $data = [
        'name' => 'Test User',
        'email' => 'test@example.com',
        'password' => 'password',
        'password_confirmation' => 'different-password', // 一致しない
    ];

    $response = $this->post('/api/register', $data);

    $response->assertStatus(422);
    $response->assertJsonValidationErrors(['password']);
}
```

---

### 🚀 実践例9: 認証が必要なエンドポイント

```php
public function test_authenticated_user_can_create_post()
{
    $user = User::factory()->create();

    $data = [
        'title' => 'Test Post',
        'content' => 'Test Content',
    ];

    $response = $this->actingAs($user, 'sanctum')
        ->post('/api/posts', $data);

    $response->assertStatus(201);

    $this->assertDatabaseHas('posts', [
        'title' => 'Test Post',
        'content' => 'Test Content',
        'user_id' => $user->id,
    ]);
}

public function test_unauthenticated_user_cannot_create_post()
{
    $data = [
        'title' => 'Test Post',
        'content' => 'Test Content',
    ];

    $response = $this->post('/api/posts', $data);

    $response->assertStatus(401);
}
```

---

### 💡 TIP: `actingAs()`

`actingAs()`を使うと、認証済みユーザーとしてテストを実行できます。

```php
$user = User::factory()->create();

$response = $this->actingAs($user, 'sanctum')
    ->get('/api/profile');
```

---

### 🚀 実践例10: トークンの検証

```php
public function test_login_returns_valid_token()
{
    $user = User::factory()->create([
        'email' => 'test@example.com',
        'password' => bcrypt('password'),
    ]);

    $data = [
        'email' => 'test@example.com',
        'password' => 'password',
    ];

    $response = $this->post('/api/login', $data);

    $response->assertStatus(200);
    $token = $response->json('token');

    // トークンを使ってプロフィールにアクセス
    $response = $this->withHeaders([
        'Authorization' => 'Bearer ' . $token,
    ])->get('/api/profile');

    $response->assertStatus(200);
}
```

---

### 🚨 よくある間違い

#### 間違い1: `actingAs()`のガード名を忘れる

```php
// NG
$response = $this->actingAs($user)
    ->get('/api/profile');

// OK
$response = $this->actingAs($user, 'sanctum')
    ->get('/api/profile');
```

---

#### 間違い2: パスワードをハッシュ化していない

```php
// NG
$user = User::factory()->create([
    'password' => 'password', // ハッシュ化されていない
]);

// OK
$user = User::factory()->create([
    'password' => bcrypt('password'), // ハッシュ化
]);
```

---

## ✨ まとめ

このセクションでは、認証機能のテストの基礎を学びました。

*   ユーザー登録、ログイン、ログアウトのテストを書ける。
*   `actingAs()`を使って、認証済みユーザーとしてテストを実行できる。
*   認証が必要なエンドポイントのテストを書ける。
*   バリデーションエラーのテストを書ける。

次のセクションでは、CRUD+認証+DBアサートの連続演習を行います。

---
