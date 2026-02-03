# 認証機能のテスト

## 🎯 このセクションで学ぶこと

このセクションでは、認証機能に対するテストを実装します。

- ログイン機能のテスト
- ユーザー登録機能のテスト
- 未認証ユーザーのリダイレクトテスト

認証機能はセキュリティに直結する重要な機能です。テストを書いて、正しく動作することを保証しましょう。

---

## 🌿 ブランチの作成

Issue #9 に対応するブランチを作成します。

```bash
# 現在のブランチを確認（mainにいることを確認）
git branch

# mainブランチの最新状態を取得
git pull origin main

# Issue #9 に対応するブランチを作成して切り替え
git switch -c feature/issue-9-auth-tests
```

---

## 📝 ステップ1: AuthenticationTest の作成

ログイン機能のテストを作成します。

```bash
sail artisan make:test AuthenticationTest
```

**ファイル**: `tests/Feature/AuthenticationTest.php`

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class AuthenticationTest extends TestCase
{
    use RefreshDatabase;

    /** @test */
    public function ログイン画面を表示できる(): void
    {
        // Act
        $response = $this->get(route('login'));

        // Assert
        $response->assertStatus(200);
    }

    /** @test */
    public function 正しい認証情報でログインできる(): void
    {
        // Arrange
        $user = User::factory()->create([
            'password' => bcrypt('password123'),
        ]);

        // Act
        $response = $this->post(route('login'), [
            'email' => $user->email,
            'password' => 'password123',
        ]);

        // Assert
        $response->assertRedirect(route('tasks.index'));
        $this->assertAuthenticatedAs($user);
    }

    /** @test */
    public function 間違ったパスワードではログインできない(): void
    {
        // Arrange
        $user = User::factory()->create([
            'password' => bcrypt('password123'),
        ]);

        // Act
        $response = $this->post(route('login'), [
            'email' => $user->email,
            'password' => 'wrong-password',
        ]);

        // Assert
        $response->assertSessionHasErrors('email');
        $this->assertGuest();
    }

    /** @test */
    public function 存在しないメールアドレスではログインできない(): void
    {
        // Act
        $response = $this->post(route('login'), [
            'email' => 'nonexistent@example.com',
            'password' => 'password123',
        ]);

        // Assert
        $response->assertSessionHasErrors('email');
        $this->assertGuest();
    }

    /** @test */
    public function メールアドレスが空だとバリデーションエラーになる(): void
    {
        // Act
        $response = $this->post(route('login'), [
            'email' => '',
            'password' => 'password123',
        ]);

        // Assert
        $response->assertSessionHasErrors('email');
    }

    /** @test */
    public function パスワードが空だとバリデーションエラーになる(): void
    {
        // Arrange
        $user = User::factory()->create();

        // Act
        $response = $this->post(route('login'), [
            'email' => $user->email,
            'password' => '',
        ]);

        // Assert
        $response->assertSessionHasErrors('password');
    }

    /** @test */
    public function ログアウトできる(): void
    {
        // Arrange
        $user = User::factory()->create();

        // Act
        $response = $this->actingAs($user)->post(route('logout'));

        // Assert
        $response->assertRedirect('/');
        $this->assertGuest();
    }
}
```

### コードリーディング

| コード | 説明 |
|:---|:---|
| `bcrypt('password123')` | パスワードをハッシュ化して保存 |
| `$this->post(route('login'), [...])` | ログインフォームにPOSTリクエストを送信 |
| `assertAuthenticatedAs($user)` | 指定したユーザーとして認証されていることを確認 |
| `assertGuest()` | 認証されていない（ゲスト）状態であることを確認 |
| `assertSessionHasErrors('email')` | セッションに `email` のバリデーションエラーがあることを確認 |

---

## 📝 ステップ2: RegistrationTest の作成

ユーザー登録機能のテストを作成します。

```bash
sail artisan make:test RegistrationTest
```

**ファイル**: `tests/Feature/RegistrationTest.php`

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class RegistrationTest extends TestCase
{
    use RefreshDatabase;

    /** @test */
    public function 登録画面を表示できる(): void
    {
        // Act
        $response = $this->get(route('register'));

        // Assert
        $response->assertStatus(200);
    }

    /** @test */
    public function 新規ユーザーを登録できる(): void
    {
        // Act
        $response = $this->post(route('register'), [
            'name' => 'テストユーザー',
            'email' => 'test@example.com',
            'password' => 'password123',
            'password_confirmation' => 'password123',
        ]);

        // Assert
        $response->assertRedirect(route('tasks.index'));
        $this->assertDatabaseHas('users', [
            'name' => 'テストユーザー',
            'email' => 'test@example.com',
        ]);
        $this->assertAuthenticated();
    }

    /** @test */
    public function 名前が空だとバリデーションエラーになる(): void
    {
        // Act
        $response = $this->post(route('register'), [
            'name' => '',
            'email' => 'test@example.com',
            'password' => 'password123',
            'password_confirmation' => 'password123',
        ]);

        // Assert
        $response->assertSessionHasErrors('name');
    }

    /** @test */
    public function メールアドレスが空だとバリデーションエラーになる(): void
    {
        // Act
        $response = $this->post(route('register'), [
            'name' => 'テストユーザー',
            'email' => '',
            'password' => 'password123',
            'password_confirmation' => 'password123',
        ]);

        // Assert
        $response->assertSessionHasErrors('email');
    }

    /** @test */
    public function 無効なメールアドレス形式だとバリデーションエラーになる(): void
    {
        // Act
        $response = $this->post(route('register'), [
            'name' => 'テストユーザー',
            'email' => 'invalid-email',
            'password' => 'password123',
            'password_confirmation' => 'password123',
        ]);

        // Assert
        $response->assertSessionHasErrors('email');
    }

    /** @test */
    public function 既に登録済みのメールアドレスだとバリデーションエラーになる(): void
    {
        // Arrange
        User::factory()->create(['email' => 'existing@example.com']);

        // Act
        $response = $this->post(route('register'), [
            'name' => 'テストユーザー',
            'email' => 'existing@example.com',
            'password' => 'password123',
            'password_confirmation' => 'password123',
        ]);

        // Assert
        $response->assertSessionHasErrors('email');
    }

    /** @test */
    public function パスワードが8文字未満だとバリデーションエラーになる(): void
    {
        // Act
        $response = $this->post(route('register'), [
            'name' => 'テストユーザー',
            'email' => 'test@example.com',
            'password' => 'short',
            'password_confirmation' => 'short',
        ]);

        // Assert
        $response->assertSessionHasErrors('password');
    }

    /** @test */
    public function パスワード確認が一致しないとバリデーションエラーになる(): void
    {
        // Act
        $response = $this->post(route('register'), [
            'name' => 'テストユーザー',
            'email' => 'test@example.com',
            'password' => 'password123',
            'password_confirmation' => 'different-password',
        ]);

        // Assert
        $response->assertSessionHasErrors('password');
    }
}
```

### コードリーディング

| コード | 説明 |
|:---|:---|
| `$this->post(route('register'), [...])` | 登録フォームにPOSTリクエストを送信 |
| `assertAuthenticated()` | 認証されている状態であることを確認（ユーザーは問わない） |
| `assertDatabaseHas('users', [...])` | usersテーブルに指定したレコードが存在することを確認 |
| `password_confirmation` | Laravelの `confirmed` ルールで使用される確認用フィールド |

---

## 📝 ステップ3: 未認証リダイレクトテスト の作成

未認証ユーザーが保護されたページにアクセスした際のリダイレクトをテストします。

```bash
sail artisan make:test UnauthenticatedRedirectTest
```

**ファイル**: `tests/Feature/UnauthenticatedRedirectTest.php`

```php
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class UnauthenticatedRedirectTest extends TestCase
{
    use RefreshDatabase;

    /** @test */
    public function 未認証ユーザーはタスク一覧にアクセスするとログインページにリダイレクトされる(): void
    {
        // Act
        $response = $this->get(route('tasks.index'));

        // Assert
        $response->assertRedirect(route('login'));
    }

    /** @test */
    public function 未認証ユーザーはタスク作成画面にアクセスするとログインページにリダイレクトされる(): void
    {
        // Act
        $response = $this->get(route('tasks.create'));

        // Assert
        $response->assertRedirect(route('login'));
    }

    /** @test */
    public function 未認証ユーザーはカテゴリー一覧にアクセスするとログインページにリダイレクトされる(): void
    {
        // Act
        $response = $this->get(route('categories.index'));

        // Assert
        $response->assertRedirect(route('login'));
    }

    /** @test */
    public function 未認証ユーザーはカテゴリー作成画面にアクセスするとログインページにリダイレクトされる(): void
    {
        // Act
        $response = $this->get(route('categories.create'));

        // Assert
        $response->assertRedirect(route('login'));
    }
}
```

### コードリーディング

| コード | 説明 |
|:---|:---|
| `$this->get(route('tasks.index'))` | 認証なしでタスク一覧にアクセス |
| `assertRedirect(route('login'))` | ログインページにリダイレクトされることを確認 |

> **💡 ポイント**: 未認証リダイレクトのテストは、`auth` ミドルウェアが正しく機能していることを確認するためのものです。セキュリティ上、保護されたページに未認証でアクセスできないことを保証します。

---

## 🧪 ステップ4: テストの実行

作成したテストを実行して、全てパスすることを確認します。

```bash
# AuthenticationTestを実行
sail test tests/Feature/AuthenticationTest.php

# RegistrationTestを実行
sail test tests/Feature/RegistrationTest.php

# UnauthenticatedRedirectTestを実行
sail test tests/Feature/UnauthenticatedRedirectTest.php

# 認証関連のテストをまとめて実行
sail test --filter=Authentication
sail test --filter=Registration
sail test --filter=Unauthenticated
```

**期待される出力**:

```
   PASS  Tests\Feature\AuthenticationTest
  ✓ ログイン画面を表示できる
  ✓ 正しい認証情報でログインできる
  ✓ 間違ったパスワードではログインできない
  ✓ 存在しないメールアドレスではログインできない
  ✓ メールアドレスが空だとバリデーションエラーになる
  ✓ パスワードが空だとバリデーションエラーになる
  ✓ ログアウトできる

   PASS  Tests\Feature\RegistrationTest
  ✓ 登録画面を表示できる
  ✓ 新規ユーザーを登録できる
  ✓ 名前が空だとバリデーションエラーになる
  ...

   PASS  Tests\Feature\UnauthenticatedRedirectTest
  ✓ 未認証ユーザーはタスク一覧にアクセスするとログインページにリダイレクトされる
  ...

  Tests:    19 passed
  Duration: 1.85s
```

---

## ❌ よくある間違い

### 1. パスワードをハッシュ化し忘れる

```php
// ❌ NG: パスワードが平文のまま
$user = User::factory()->create([
    'password' => 'password123', // ハッシュ化されていない
]);
```

**対処法**: `bcrypt()` でハッシュ化する。

```php
// ✅ OK
$user = User::factory()->create([
    'password' => bcrypt('password123'),
]);
```

### 2. assertAuthenticatedとassertAuthenticatedAsの違いを理解していない

```php
// assertAuthenticated(): 誰かしらが認証されていればOK
$this->assertAuthenticated();

// assertAuthenticatedAs($user): 特定のユーザーとして認証されていることを確認
$this->assertAuthenticatedAs($user);
```

### 3. password_confirmationを忘れる

```php
// ❌ NG: password_confirmationがない
$response = $this->post(route('register'), [
    'name' => 'テストユーザー',
    'email' => 'test@example.com',
    'password' => 'password123',
    // 'password_confirmation' が抜けている
]);
```

**対処法**: `password_confirmation` を追加する。

---

## ✅ 完了条件

以下の条件を満たしていることを確認してください。

- [ ] AuthenticationTestが作成されている（7テスト）
- [ ] RegistrationTestが作成されている（8テスト）
- [ ] UnauthenticatedRedirectTestが作成されている（4テスト）
- [ ] 全てのテストがパスする

---

## ✨ まとめ

このセクションでは、認証機能のテストを実装しました。

| 学んだこと | 内容 |
|:---|:---|
| ログインテスト | 正常系・異常系のログイン動作を検証 |
| 登録テスト | ユーザー登録とバリデーションを検証 |
| リダイレクトテスト | 未認証ユーザーのアクセス制御を検証 |
| assertAuthenticatedAs | 特定ユーザーとして認証されていることを確認 |
| assertGuest | 未認証状態であることを確認 |

次のセクションでは、APIのテストを実装します。

---

## 🔄 Git操作とプルリクエスト

作業が完了したら、変更をコミットしてプッシュし、プルリクエストを作成して変更内容を確認しましょう。

### ステップ1: コミットとプッシュ

```bash
# 変更をステージング
git add .

# コミット（Issue番号を含める）
git commit -m "feat: 認証機能のテスト実装 #9"

# リモートにプッシュ
git push origin feature/issue-9-auth-tests
```

### ステップ2: プルリクエストの作成と確認

GitHubでプルリクエストを作成し、変更内容を確認してみましょう。

1. GitHubのリポジトリページを開く
2. 「Pull requests」タブをクリックする
3. 「New pull request」ボタンをクリックする
4. `base: main` ← `compare: feature/issue-9-auth-tests` を選択する
5. 「Create pull request」ボタンをクリックする
6. 以下の内容を入力する

**タイトル**:
```
feat: 認証機能のテスト実装
```

**説明欄**:
```markdown
## 概要
認証機能（ログイン・登録・リダイレクト）に対するテストを実装しました。

## 変更内容
- AuthenticationTestの作成（ログイン機能）
- RegistrationTestの作成（ユーザー登録機能）
- UnauthenticatedRedirectTestの作成（未認証リダイレクト）

## テスト項目
- [ ] ログインテスト（7テスト）
- [ ] 登録テスト（8テスト）
- [ ] 未認証リダイレクトテスト（4テスト）

## 対応Issue
close #9
```

7. 「Create pull request」ボタンをクリックする

> **💡 確認ポイント**: PRを作成したら、「Files changed」タブでテストコードを確認してみましょう。認証に関するテストは、正常系だけでなく異常系（間違ったパスワード、存在しないメールアドレス等）もカバーしているか確認することが重要です。

### ステップ3: プルリクエストのマージ

変更内容を確認したら、PRをマージします。

1. PRのページで「Merge pull request」ボタンをクリックする
2. 「Confirm merge」ボタンをクリックする
3. マージが完了すると、Issue #9が自動的にクローズされる

### ステップ4: ローカルのmainブランチを更新し、ブランチを削除

```bash
# mainブランチに切り替え
git switch main

# リモートの変更を取り込む
git pull origin main

# マージ済みのブランチを削除
git branch -d feature/issue-9-auth-tests
```

> **📌 Issue対応**: PRをマージすると、説明欄の `close #9` によりIssue #9が自動的にクローズされます。
