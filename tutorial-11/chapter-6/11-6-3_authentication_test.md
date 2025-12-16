# Tutorial 11-6-3: 認証機能のテスト

## 🎯 このセクションで学ぶこと

- ユーザー登録のテストを書く方法を学ぶ
- ログイン・ログアウトのテストを書く方法を学ぶ
- パスワードリセットのテストを書く方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜCRUDテストの後に『認証テスト』を書くのか？」

CRUDテストができたら、次は「認証テスト」です。

---

### 理由1: セキュリティの確認

認証が必要なページに、**未ログインでアクセスできないこと**を確認します。

```php
$response = $this->get('/tasks');
$response->assertRedirect('/login');
```

---

### 理由2: ログイン状態のシミュレート

テストでは、`actingAs()`を使って**ログイン状態をシミュレート**できます。

```php
$user = User::factory()->create();
$response = $this->actingAs($user)->get('/tasks');
$response->assertStatus(200);
```

---

### 理由3: 認証フローの確認

ログイン、ログアウト、ユーザー登録などの**認証フロー**が正しく動くことを確認します。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | ユーザー登録のテスト | 正常系・異常系を確認 |
| Step 2 | ログインのテスト | 認証フローを確認 |
| Step 3 | ログアウトのテスト | セッション破棄を確認 |
| Step 4 | パスワードリセットのテスト | リセットフローを確認 |

> 💡 **ポイント**: `actingAs()`を使うと、ログイン状態をシミュレートできます。

---

## Step 1: ユーザー登録のテスト

### 1-1. 正常系: ユーザーを登録できる

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

**ポイント**: `assertAuthenticated()`で、ログイン状態を確認します。

---

### 1-2. 異常系: メールアドレスが重複

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

### 1-3. 異常系: パスワードが短い

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

### 1-4. 異常系: パスワード確認が一致しない

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

## Step 2: ログインのテスト

### 2-1. 正常系: ログインできる

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

**ポイント**: `assertAuthenticatedAs($user)`で、特定のユーザーでログインしていることを確認します。

---

### 2-2. 異常系: パスワードが間違っている

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

**ポイント**: `assertGuest()`で、未ログイン状態を確認します。

---

### 2-3. 異常系: 存在しないユーザー

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

## Step 3: ログアウトのテスト

### 3-1. ログアウトできる

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

## Step 4: パスワードリセットのテスト

### 4-1. パスワードリセットリンクを送信できる

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

### 4-2. パスワードをリセットできる

```php
use Illuminate\Support\Facades\Password;

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

### 4-3. メール送信のテスト

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

- `Mail::fake()`で、メール送信をモックする
- `Mail::assertSent()`で、メールが送信されたことを確認する

---

### 4-4. 実践演習

以下のテストを作成してください。

**テスト内容**: メールアドレスが無効な形式の場合、登録できないことを確認する

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

## 🚨 よくある間違い

### 間違い1: パスワードをハッシュ化し忘れる

**問題**: テストデータのパスワードがハッシュ化されていない

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

### 間違い2: assertAuthenticatedとassertAuthenticatedAsを混同する

| メソッド | 説明 |
|----------|------|
| `assertAuthenticated()` | ログイン状態を確認 |
| `assertAuthenticatedAs($user)` | 特定のユーザーでログインしていることを確認 |

---

### 間違い3: Mail::fake()を忘れる

**問題**: 実際にメールが送信されてしまう

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

## 💡 TIP: Notification::fake()を使う

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

## ✨ まとめ

このセクションでは、認証機能のテストを学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | ユーザー登録のテスト（正常系・異常系） |
| Step 2 | ログインのテスト（正常系・異常系） |
| Step 3 | ログアウトのテスト |
| Step 4 | パスワードリセットとメール送信のテスト |

次のセクションでは、認可機能のテストを書きます。

---

## 📝 学習のポイント

- [ ] ユーザー登録のテストを書いた
- [ ] ログインのテストを書いた
- [ ] ログアウトのテストを書いた
- [ ] パスワードリセットのテストを書いた
- [ ] メール送信のテストを書いた
