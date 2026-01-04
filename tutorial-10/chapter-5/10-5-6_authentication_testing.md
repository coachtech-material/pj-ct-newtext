# Tutorial 10-5-6: 認証機能のテスト

## 🎯 このセクションで学ぶこと

*   認証機能のテストを書き、ログイン・ログアウトの動作を検証できるようになる。
*   `actingAs()`を使って、認証済みユーザーとしてテストを実行できるようになる。
*   認証が必要なページのテストを書けるようになる。

---

## 導入：「認証機能のテスト」とは何か？

**認証機能のテスト**とは、**ログイン・ログアウト・ユーザー登録などの認証機能が正しく動作するかを検証するテスト**です。

例えば、以下のようなテストを書きます。

*   ユーザー登録が正しく動作するか
*   ログインが正しく動作するか
*   ログアウトが正しく動作するか
*   認証が必要なページにアクセスできるか

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

        $response = $this->post('/register', $data);

        $response->assertRedirect('/dashboard');

        $this->assertDatabaseHas('users', [
            'name' => 'Test User',
            'email' => 'test@example.com',
        ]);

        $this->assertAuthenticated();
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

    $response = $this->post('/login', $data);

    $response->assertRedirect('/dashboard');
    $this->assertAuthenticatedAs($user);
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

    $response = $this->post('/login', $data);

    $response->assertSessionHasErrors();
    $this->assertGuest();
}
```

---

### 🚀 実践例4: ログアウトのテスト

```php
public function test_user_can_logout()
{
    $user = User::factory()->create();

    $response = $this->actingAs($user)
        ->post('/logout');

    $response->assertRedirect('/');
    $this->assertGuest();
}
```

---

### 🚀 実践例5: 認証済みユーザーのダッシュボードアクセス

```php
public function test_authenticated_user_can_access_dashboard()
{
    $user = User::factory()->create();

    $response = $this->actingAs($user)
        ->get('/dashboard');

    $response->assertStatus(200);
    $response->assertViewIs('dashboard');
}
```

---

### 🚀 実践例6: 未認証ユーザーはアクセスできない

```php
public function test_unauthenticated_user_cannot_access_dashboard()
{
    $response = $this->get('/dashboard');

    $response->assertRedirect('/login');
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

    $response = $this->post('/register', $data);

    $response->assertSessionHasErrors(['name']);
}

public function test_register_requires_valid_email()
{
    $data = [
        'name' => 'Test User',
        'email' => 'invalid-email', // 無効なメールアドレス
        'password' => 'password',
        'password_confirmation' => 'password',
    ];

    $response = $this->post('/register', $data);

    $response->assertSessionHasErrors(['email']);
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

    $response = $this->post('/register', $data);

    $response->assertSessionHasErrors(['password']);
}
```

---

### 🚀 実践例9: 認証が必要なページ

```php
public function test_authenticated_user_can_create_post()
{
    $user = User::factory()->create();

    $data = [
        'title' => 'Test Post',
        'content' => 'Test Content',
    ];

    $response = $this->actingAs($user)
        ->post('/posts', $data);

    $response->assertRedirect();

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

    $response = $this->post('/posts', $data);

    $response->assertRedirect('/login');
}
```

---

### 💡 TIP: `actingAs()`

`actingAs()`を使うと、認証済みユーザーとしてテストを実行できます。

```php
$user = User::factory()->create();

$response = $this->actingAs($user)
    ->get('/dashboard');
```

---

### 💡 TIP: 認証関連のアサーションメソッド

| メソッド | 説明 |
|:---|:---|
| `assertAuthenticated()` | ユーザーが認証済みであることを確認 |
| `assertAuthenticatedAs($user)` | 指定したユーザーとして認証されていることを確認 |
| `assertGuest()` | ユーザーが未認証（ゲスト）であることを確認 |

---

### 🚨 よくある間違い

#### 間違い1: パスワードをハッシュ化していない

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

> **💡 補足**: Laravelのデフォルトの`UserFactory`では、パスワードは自動的にハッシュ化されます。明示的に指定する場合のみ`bcrypt()`が必要です。

---

#### 間違い2: リダイレクト先を確認していない

```php
// NG: リダイレクトされることだけを確認
$response = $this->post('/login', $data);
$response->assertRedirect();

// OK: リダイレクト先も確認
$response = $this->post('/login', $data);
$response->assertRedirect('/dashboard');
```

---

## ✨ まとめ

このセクションでは、認証機能のテストの基礎を学びました。

*   ユーザー登録、ログイン、ログアウトのテストを書ける。
*   `actingAs()`を使って、認証済みユーザーとしてテストを実行できる。
*   認証が必要なページのテストを書ける。
*   バリデーションエラーのテストを書ける。
*   `assertAuthenticated()`、`assertGuest()`などの認証関連アサーションを使える。

次のセクションでは、CRUD+認証+DBアサートの連続演習を行います。

---
