# Tutorial 11-6-3: 認証機能のテスト

## 🎯 このセクションで学ぶこと

*   ユーザー登録のテストを書く方法を学ぶ。
*   ログイン・ログアウトのテストを書く方法を学ぶ。
*   パスワードリセットのテストを書く方法を学ぶ。

---

## 導入：なぜ認証機能をテストするのか

**認証機能**は、アプリケーションの**セキュリティの要**です。

認証機能をテストすることで、**不正アクセスを防ぎ、ユーザーの安全を守る**ことができます。

---

## 詳細解説

### 🔍 ユーザー登録のテスト（正常系）

ユーザーを登録できることをテストします。

```php
public function test_ユーザーを登録できる()
{
    // 実行
    $response = $this->post('/register', [
        'name' => 'テストユーザー',
        'email' => 'test@example.com',
        'password' => 'password123',
        'password_confirmation' => 'password123',
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertRedirect('/dashboard');
    $this->assertDatabaseHas('users', [
        'name' => 'テストユーザー',
        'email' => 'test@example.com',
    ]);
    $this->assertAuthenticated();
}
```

**ポイント**:
*   `assertAuthenticated()`で、ログイン状態を確認する

---

### 🔍 ユーザー登録のテスト（異常系）

メールアドレスが重複している場合、エラーになることをテストします。

```php
public function test_重複したメールアドレスで登録できない()
{
    // 準備
    User::factory()->create(['email' => 'test@example.com']);
    
    // 実行
    $response = $this->post('/register', [
        'name' => 'テストユーザー',
        'email' => 'test@example.com',
        'password' => 'password123',
        'password_confirmation' => 'password123',
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertSessionHasErrors('email');
    $this->assertDatabaseCount('users', 1);
}
```

---

### 🔍 パスワードが短い場合のテスト

パスワードが短い場合、エラーになることをテストします。

```php
public function test_パスワードが短い場合登録できない()
{
    // 実行
    $response = $this->post('/register', [
        'name' => 'テストユーザー',
        'email' => 'test@example.com',
        'password' => 'pass',
        'password_confirmation' => 'pass',
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertSessionHasErrors('password');
    $this->assertDatabaseMissing('users', [
        'email' => 'test@example.com',
    ]);
}
```

---

### 🔍 パスワード確認が一致しない場合のテスト

パスワード確認が一致しない場合、エラーになることをテストします。

```php
public function test_パスワード確認が一致しない場合登録できない()
{
    // 実行
    $response = $this->post('/register', [
        'name' => 'テストユーザー',
        'email' => 'test@example.com',
        'password' => 'password123',
        'password_confirmation' => 'different',
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertSessionHasErrors('password');
    $this->assertDatabaseMissing('users', [
        'email' => 'test@example.com',
    ]);
}
```

---

### 🔍 ログインのテスト（正常系）

ログインできることをテストします。

```php
public function test_ログインできる()
{
    // 準備
    $user = User::factory()->create([
        'email' => 'test@example.com',
        'password' => Hash::make('password123'),
    ]);
    
    // 実行
    $response = $this->post('/login', [
        'email' => 'test@example.com',
        'password' => 'password123',
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertRedirect('/dashboard');
    $this->assertAuthenticatedAs($user);
}
```

**ポイント**:
*   `assertAuthenticatedAs($user)`で、特定のユーザーでログインしていることを確認する

---

### 🔍 ログインのテスト（異常系）

パスワードが間違っている場合、ログインできないことをテストします。

```php
public function test_パスワードが間違っている場合ログインできない()
{
    // 準備
    $user = User::factory()->create([
        'email' => 'test@example.com',
        'password' => Hash::make('password123'),
    ]);
    
    // 実行
    $response = $this->post('/login', [
        'email' => 'test@example.com',
        'password' => 'wrongpassword',
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertSessionHasErrors('email');
    $this->assertGuest();
}
```

**ポイント**:
*   `assertGuest()`で、未ログイン状態を確認する

---

### 🔍 存在しないユーザーでログインできないテスト

存在しないユーザーでログインできないことをテストします。

```php
public function test_存在しないユーザーでログインできない()
{
    // 実行
    $response = $this->post('/login', [
        'email' => 'notexist@example.com',
        'password' => 'password123',
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertSessionHasErrors('email');
    $this->assertGuest();
}
```

---

### 🔍 ログアウトのテスト

ログアウトできることをテストします。

```php
public function test_ログアウトできる()
{
    // 準備
    $user = User::factory()->create();
    
    // 実行
    $response = $this->actingAs($user)->post('/logout');
    
    // 検証
    $response->assertStatus(302);
    $response->assertRedirect('/');
    $this->assertGuest();
}
```

---

### 🔍 パスワードリセットリンクの送信テスト

パスワードリセットリンクを送信できることをテストします。

```php
public function test_パスワードリセットリンクを送信できる()
{
    // 準備
    $user = User::factory()->create(['email' => 'test@example.com']);
    
    // 実行
    $response = $this->post('/forgot-password', [
        'email' => 'test@example.com',
    ]);
    
    // 検証
    $response->assertStatus(302);
    $this->assertDatabaseHas('password_reset_tokens', [
        'email' => 'test@example.com',
    ]);
}
```

---

### 🔍 パスワードリセットのテスト

パスワードをリセットできることをテストします。

```php
public function test_パスワードをリセットできる()
{
    // 準備
    $user = User::factory()->create(['email' => 'test@example.com']);
    $token = Password::createToken($user);
    
    // 実行
    $response = $this->post('/reset-password', [
        'token' => $token,
        'email' => 'test@example.com',
        'password' => 'newpassword123',
        'password_confirmation' => 'newpassword123',
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertRedirect('/login');
    
    // 新しいパスワードでログインできることを確認
    $this->assertTrue(Hash::check('newpassword123', $user->fresh()->password));
}
```

---

### 🔍 実践演習: テストを作成してください

以下のテストを作成してください。

**テスト内容**:
*   メールアドレスが無効な形式の場合、登録できないことを確認する

---

**解答例**:

```php
public function test_メールアドレスが無効な形式の場合登録できない()
{
    // 実行
    $response = $this->post('/register', [
        'name' => 'テストユーザー',
        'email' => 'invalid-email',
        'password' => 'password123',
        'password_confirmation' => 'password123',
    ]);
    
    // 検証
    $response->assertStatus(302);
    $response->assertSessionHasErrors('email');
    $this->assertDatabaseMissing('users', [
        'name' => 'テストユーザー',
    ]);
}
```

---

### 🔍 メール送信のテスト

メールが送信されることをテストします。

```php
use Illuminate\Support\Facades\Mail;
use App\Mail\WelcomeEmail;

public function test_登録時にウェルカムメールが送信される()
{
    // 準備
    Mail::fake();
    
    // 実行
    $response = $this->post('/register', [
        'name' => 'テストユーザー',
        'email' => 'test@example.com',
        'password' => 'password123',
        'password_confirmation' => 'password123',
    ]);
    
    // 検証
    Mail::assertSent(WelcomeEmail::class, function ($mail) {
        return $mail->hasTo('test@example.com');
    });
}
```

**ポイント**:
*   `Mail::fake()`で、メール送信をモックする
*   `Mail::assertSent()`で、メールが送信されたことを確認する

---

### 💡 TIP: Notification::fake()を使う

通知をテストする場合は、`Notification::fake()`を使います。

```php
use Illuminate\Support\Facades\Notification;
use App\Notifications\WelcomeNotification;

public function test_登録時に通知が送信される()
{
    Notification::fake();
    
    $response = $this->post('/register', [...]);
    
    Notification::assertSentTo(
        [$user], WelcomeNotification::class
    );
}
```

---

### 🚨 よくある間違い

#### 間違い1: パスワードをハッシュ化し忘れる

テストデータを作成する際、パスワードをハッシュ化します。

```php
// ❌ 間違い
$user = User::factory()->create([
    'password' => 'password123',
]);

// ✅ 正しい
$user = User::factory()->create([
    'password' => Hash::make('password123'),
]);
```

---

#### 間違い2: assertAuthenticatedとassertAuthenticatedAsを混同する

*   `assertAuthenticated()`: ログイン状態を確認する
*   `assertAuthenticatedAs($user)`: 特定のユーザーでログインしていることを確認する

---

#### 間違い3: Mail::fake()を忘れる

`Mail::fake()`を忘れると、実際にメールが送信されます。

```php
// ❌ 間違い
public function test_メールが送信される()
{
    // Mail::fake()を忘れている
    $response = $this->post('/register', [...]);
}

// ✅ 正しい
public function test_メールが送信される()
{
    Mail::fake();
    $response = $this->post('/register', [...]);
}
```

---

## ✨ まとめ

このセクションでは、認証機能のテストを学びました。

*   ユーザー登録のテストを書いた。
*   ログイン・ログアウトのテストを書いた。
*   パスワードリセットのテストを書いた。
*   メール送信のテストを書いた。

次のセクションでは、認可機能のテストを書きます。

---

## 📝 学習のポイント

- [ ] ユーザー登録のテストを書いた。
- [ ] ログインのテストを書いた。
- [ ] ログアウトのテストを書いた。
- [ ] パスワードリセットのテストを書いた。
- [ ] メール送信のテストを書いた。
