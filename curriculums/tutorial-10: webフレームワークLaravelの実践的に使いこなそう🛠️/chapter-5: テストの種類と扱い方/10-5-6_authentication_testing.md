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

**認証機能のテストが重要な理由**

| 理由 | 説明 |
|:---|:---|
| セキュリティ | 認証機能はセキュリティの要であり、バグがあると重大な問題になる |
| ユーザー体験 | ログインできない、ログアウトできないなどの問題はユーザー離脱につながる |
| 回帰テスト | 認証機能を変更した際に、既存の動作が壊れていないことを確認できる |

このセクションでは、認証機能のテストの基礎を学びます。

---

## 詳細解説

### 🔍 認証テストの基本的な使い方

認証テストでは、以下の流れでテストを行います。

1. **準備**: テスト用ユーザーをファクトリで作成する
2. **実行**: ログイン、ログアウト、登録などのリクエストを送信する
3. **検証**: 認証状態、リダイレクト先、データベースの状態を検証する

**認証テストでよく使うメソッド**

| メソッド | 説明 |
|:---|:---|
| `actingAs($user)` | 指定したユーザーとして認証状態を設定する |
| `assertAuthenticated()` | ユーザーが認証済みであることを検証する |
| `assertAuthenticatedAs($user)` | 指定したユーザーとして認証されていることを検証する |
| `assertGuest()` | ユーザーが未認証（ゲスト）であることを検証する |

---

### 🚀 実践例1: ユーザー登録のテスト

ユーザー登録が正しく動作することを検証する例です。

```php
use Illuminate\Foundation\Testing\RefreshDatabase;

class AuthTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_register()
    {
        // 1. 送信するデータを用意
        $data = [
            'name' => 'Test User',
            'email' => 'test@example.com',
            'password' => 'password',
            'password_confirmation' => 'password',
        ];

        // 2. POSTリクエストを送信
        $response = $this->post('/register', $data);

        // 3. リダイレクト先を検証
        $response->assertRedirect('/dashboard');

        // 4. データベースにユーザーが保存されていることを検証
        $this->assertDatabaseHas('users', [
            'name' => 'Test User',
            'email' => 'test@example.com',
        ]);

        // 5. ユーザーが認証済みであることを検証
        $this->assertAuthenticated();
    }
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `use RefreshDatabase;` | テストごとにデータベースをリセットするトレイトです |
| `$data = [...]` | 登録フォームに送信するデータを用意します。`password_confirmation`はパスワード確認用です |
| `$this->post('/register', $data);` | `/register`にPOSTリクエストを送信します |
| `$response->assertRedirect('/dashboard');` | 登録後に`/dashboard`にリダイレクトされることを検証します |
| `$this->assertDatabaseHas('users', [...])` | `users`テーブルにユーザーが保存されていることを検証します |
| `$this->assertAuthenticated();` | ユーザーが認証済み（ログイン状態）であることを検証します |

**構文解説: assertAuthenticated()**

```php
$this->assertAuthenticated();
```

*   現在のリクエストでユーザーが認証済みであることを検証します
*   認証されていなければテスト失敗

---

### 🚀 実践例2: ログインのテスト

ログインが正しく動作することを検証する例です。

```php
public function test_user_can_login()
{
    // 1. テスト用ユーザーを作成
    $user = User::factory()->create([
        'email' => 'test@example.com',
        'password' => bcrypt('password'),
    ]);

    // 2. ログインデータを用意
    $data = [
        'email' => 'test@example.com',
        'password' => 'password',
    ];

    // 3. POSTリクエストを送信
    $response = $this->post('/login', $data);

    // 4. リダイレクト先を検証
    $response->assertRedirect('/dashboard');

    // 5. 指定したユーザーとして認証されていることを検証
    $this->assertAuthenticatedAs($user);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `User::factory()->create([...])` | ファクトリを使ってテスト用ユーザーを作成します。属性を指定して上書きできます |
| `'password' => bcrypt('password')` | パスワードをハッシュ化して保存します。ログイン時は平文で送信します |
| `$this->post('/login', $data);` | `/login`にPOSTリクエストを送信します |
| `$this->assertAuthenticatedAs($user);` | 指定したユーザーとして認証されていることを検証します |

**構文解説: assertAuthenticatedAs()**

```php
$this->assertAuthenticatedAs($user);
```

*   **引数**: 期待するユーザーモデル
*   指定したユーザーとして認証されていることを検証します
*   別のユーザーとして認証されている場合はテスト失敗

---

### 🚀 実践例3: ログインに失敗するテスト

間違ったパスワードでログインに失敗することを検証する例です。

```php
public function test_user_cannot_login_with_invalid_credentials()
{
    // 1. テスト用ユーザーを作成
    $user = User::factory()->create([
        'email' => 'test@example.com',
        'password' => bcrypt('password'),
    ]);

    // 2. 間違ったパスワードでログインを試みる
    $data = [
        'email' => 'test@example.com',
        'password' => 'wrong-password',
    ];

    // 3. POSTリクエストを送信
    $response = $this->post('/login', $data);

    // 4. セッションにエラーがあることを検証
    $response->assertSessionHasErrors();

    // 5. ユーザーが未認証であることを検証
    $this->assertGuest();
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `'password' => 'wrong-password'` | 意図的に間違ったパスワードを送信します |
| `$response->assertSessionHasErrors();` | セッションにバリデーションエラーがあることを検証します |
| `$this->assertGuest();` | ユーザーが未認証（ゲスト）であることを検証します |

**構文解説: assertGuest()**

```php
$this->assertGuest();
```

*   現在のリクエストでユーザーが未認証であることを検証します
*   認証されていればテスト失敗

---

### 🚀 実践例4: ログアウトのテスト

ログアウトが正しく動作することを検証する例です。

```php
public function test_user_can_logout()
{
    // 1. テスト用ユーザーを作成
    $user = User::factory()->create();

    // 2. 認証済みユーザーとしてログアウトリクエストを送信
    $response = $this->actingAs($user)
        ->post('/logout');

    // 3. リダイレクト先を検証
    $response->assertRedirect('/');

    // 4. ユーザーが未認証であることを検証
    $this->assertGuest();
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$this->actingAs($user)` | 指定したユーザーとして認証状態を設定します |
| `->post('/logout');` | `/logout`にPOSTリクエストを送信します |
| `$response->assertRedirect('/');` | ログアウト後にトップページにリダイレクトされることを検証します |
| `$this->assertGuest();` | ログアウト後にユーザーが未認証であることを検証します |

**構文解説: actingAs()**

```php
$this->actingAs($user)->post('/logout');
```

*   **引数**: 認証するユーザーモデル
*   指定したユーザーとして認証状態を設定します
*   メソッドチェーンで`get()`、`post()`などと組み合わせて使います

---

### 🚀 実践例5: 認証済みユーザーのダッシュボードアクセス

認証済みユーザーがダッシュボードにアクセスできることを検証する例です。

```php
public function test_authenticated_user_can_access_dashboard()
{
    // 1. テスト用ユーザーを作成
    $user = User::factory()->create();

    // 2. 認証済みユーザーとしてダッシュボードにアクセス
    $response = $this->actingAs($user)
        ->get('/dashboard');

    // 3. ステータスコードとビューを検証
    $response->assertStatus(200);
    $response->assertViewIs('dashboard');
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$this->actingAs($user)->get('/dashboard');` | 認証済みユーザーとして`/dashboard`にGETリクエストを送信します |
| `$response->assertStatus(200);` | ステータスコードが200（成功）であることを検証します |
| `$response->assertViewIs('dashboard');` | 返されたビューが`dashboard`であることを検証します |

---

### 🚀 実践例6: 未認証ユーザーはアクセスできない

未認証ユーザーがダッシュボードにアクセスするとログインページにリダイレクトされることを検証する例です。

```php
public function test_unauthenticated_user_cannot_access_dashboard()
{
    // 1. 未認証状態でダッシュボードにアクセス
    $response = $this->get('/dashboard');

    // 2. ログインページにリダイレクトされることを検証
    $response->assertRedirect('/login');
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$this->get('/dashboard');` | 未認証状態で`/dashboard`にGETリクエストを送信します（`actingAs()`を使わない） |
| `$response->assertRedirect('/login');` | ログインページにリダイレクトされることを検証します |

**処理の流れ**

1. 未認証ユーザーが認証が必要なページにアクセス
2. Laravelの`auth`ミドルウェアがリクエストをブロック
3. ログインページにリダイレクト

---

### 🚀 実践例7: バリデーションエラー

ユーザー登録時のバリデーションエラーを検証する例です。

```php
public function test_register_requires_name()
{
    // nameを意図的に省略
    $data = [
        'email' => 'test@example.com',
        'password' => 'password',
        'password_confirmation' => 'password',
    ];

    $response = $this->post('/register', $data);

    // nameフィールドにエラーがあることを検証
    $response->assertSessionHasErrors(['name']);
}

public function test_register_requires_valid_email()
{
    // 無効なメールアドレスを送信
    $data = [
        'name' => 'Test User',
        'email' => 'invalid-email',
        'password' => 'password',
        'password_confirmation' => 'password',
    ];

    $response = $this->post('/register', $data);

    // emailフィールドにエラーがあることを検証
    $response->assertSessionHasErrors(['email']);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `'email' => 'invalid-email'` | 意図的に無効なメールアドレスを送信します |
| `$response->assertSessionHasErrors(['name']);` | セッションに`name`フィールドのエラーがあることを検証します |
| `$response->assertSessionHasErrors(['email']);` | セッションに`email`フィールドのエラーがあることを検証します |

**構文解説: assertSessionHasErrors()**

```php
$response->assertSessionHasErrors(['フィールド名']);
$response->assertSessionHasErrors(['フィールド名' => 'エラーメッセージ']);
```

*   セッションにバリデーションエラーが含まれていることを検証します
*   配列で複数のフィールドを指定できます
*   エラーメッセージも検証する場合は、連想配列で指定します

---

### 🚀 実践例8: パスワード確認のテスト

パスワードと確認用パスワードが一致しない場合のエラーを検証する例です。

```php
public function test_register_requires_password_confirmation()
{
    // パスワードと確認用パスワードが一致しない
    $data = [
        'name' => 'Test User',
        'email' => 'test@example.com',
        'password' => 'password',
        'password_confirmation' => 'different-password',
    ];

    $response = $this->post('/register', $data);

    // passwordフィールドにエラーがあることを検証
    $response->assertSessionHasErrors(['password']);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `'password_confirmation' => 'different-password'` | 意図的にパスワードと異なる値を送信します |
| `$response->assertSessionHasErrors(['password']);` | `password`フィールドにエラーがあることを検証します（`confirmed`ルールのエラー） |

---

### 🚀 実践例9: 認証が必要なページ

認証済みユーザーのみが投稿を作成できることを検証する例です。

```php
public function test_authenticated_user_can_create_post()
{
    // 1. テスト用ユーザーを作成
    $user = User::factory()->create();

    // 2. 投稿データを用意
    $data = [
        'title' => 'Test Post',
        'content' => 'Test Content',
    ];

    // 3. 認証済みユーザーとして投稿を作成
    $response = $this->actingAs($user)
        ->post('/posts', $data);

    // 4. リダイレクトを検証
    $response->assertRedirect();

    // 5. データベースに投稿が保存されていることを検証
    $this->assertDatabaseHas('posts', [
        'title' => 'Test Post',
        'content' => 'Test Content',
        'user_id' => $user->id,
    ]);
}

public function test_unauthenticated_user_cannot_create_post()
{
    // 1. 投稿データを用意
    $data = [
        'title' => 'Test Post',
        'content' => 'Test Content',
    ];

    // 2. 未認証状態で投稿を作成しようとする
    $response = $this->post('/posts', $data);

    // 3. ログインページにリダイレクトされることを検証
    $response->assertRedirect('/login');
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$this->actingAs($user)->post('/posts', $data);` | 認証済みユーザーとして投稿を作成します |
| `'user_id' => $user->id` | 投稿が正しいユーザーに紐づいていることを検証します |
| `$this->post('/posts', $data);` | 未認証状態で投稿を作成しようとします（`actingAs()`を使わない） |
| `$response->assertRedirect('/login');` | 未認証の場合はログインページにリダイレクトされることを検証します |

---

### 💡 TIP: `actingAs()`の使い方

`actingAs()`を使うと、認証済みユーザーとしてテストを実行できます。

```php
$user = User::factory()->create();

// 認証済みユーザーとしてリクエストを送信
$response = $this->actingAs($user)
    ->get('/dashboard');
```

**`actingAs()`のオプション**

```php
// 特定のガードを指定する場合
$this->actingAs($user, 'admin')
    ->get('/admin/dashboard');
```

*   第2引数でガード名を指定できます
*   複数の認証ガードを使用している場合に便利です

---

### 💡 TIP: 認証関連のアサーションメソッド

| メソッド | 説明 | 使用例 |
|:---|:---|:---|
| `assertAuthenticated()` | ユーザーが認証済みであることを確認 | `$this->assertAuthenticated()` |
| `assertAuthenticatedAs($user)` | 指定したユーザーとして認証されていることを確認 | `$this->assertAuthenticatedAs($user)` |
| `assertGuest()` | ユーザーが未認証（ゲスト）であることを確認 | `$this->assertGuest()` |
| `assertCredentials($credentials)` | 指定した認証情報が有効であることを確認 | `$this->assertCredentials(['email' => '...', 'password' => '...'])` |
| `assertInvalidCredentials($credentials)` | 指定した認証情報が無効であることを確認 | `$this->assertInvalidCredentials(['email' => '...', 'password' => '...'])` |

---

### 🚨 よくある間違い

**間違い1: パスワードをハッシュ化していない**

```php
// NG: パスワードがハッシュ化されていない
$user = User::factory()->create([
    'password' => 'password',
]);

// OK: パスワードをハッシュ化
$user = User::factory()->create([
    'password' => bcrypt('password'),
]);
```

**対処法**: ファクトリでパスワードを明示的に指定する場合は、`bcrypt()`でハッシュ化します。

> **💡 補足**: Laravelのデフォルトの`UserFactory`では、パスワードは自動的にハッシュ化されます。明示的に指定する場合のみ`bcrypt()`が必要です。

---

**間違い2: リダイレクト先を確認していない**

```php
// NG: リダイレクトされることだけを確認
$response = $this->post('/login', $data);
$response->assertRedirect();

// OK: リダイレクト先も確認
$response = $this->post('/login', $data);
$response->assertRedirect('/dashboard');
```

**対処法**: `assertRedirect()`には引数でリダイレクト先を指定して、正しいページにリダイレクトされることを検証します。

---

**間違い3: 認証状態を確認していない**

```php
// NG: ログイン後の認証状態を確認していない
$response = $this->post('/login', $data);
$response->assertRedirect('/dashboard');

// OK: 認証状態も確認
$response = $this->post('/login', $data);
$response->assertRedirect('/dashboard');
$this->assertAuthenticatedAs($user);
```

**対処法**: ログイン後は`assertAuthenticated()`または`assertAuthenticatedAs()`で認証状態を確認します。

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
