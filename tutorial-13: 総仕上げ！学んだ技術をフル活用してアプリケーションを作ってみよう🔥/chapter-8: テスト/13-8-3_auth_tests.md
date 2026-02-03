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

### 🧠 先輩エンジニアの視点：テスト項目を考える

認証機能は**セキュリティに直結する重要機能**です。正常系だけでなく、異常系を手厚くテストすることが重要です。

| 観点 | 考えること | 具体例 |
|:---|:---|:---|
| **正常系** | 認証フローが正しく動作するか | ログイン成功、ログアウト成功 |
| **異常系** | 不正な認証情報で適切に拒否されるか | 間違ったパスワード、存在しないユーザー、空入力 |

> **💡 境界値テストについて**: ログイン機能では、入力値の長さ制限（メール255文字、パスワード8文字以上など）は**登録時に検証済み**のため、境界値テストは省略しています。認証の正確性を確認することがログインテストの主目的です。

### テスト項目一覧

| # | テスト名 | 観点 |
|:--|:---|:---|
| 1 | ログイン画面を表示できる | 正常系 |
| 2 | 正しい認証情報でログインできる | 正常系 |
| 3 | 間違ったパスワードではログインできない | 異常系 |
| 4 | 存在しないメールアドレスではログインできない | 異常系 |
| 5 | メールアドレスが空だとバリデーションエラーになる | 異常系 |
| 6 | パスワードが空だとバリデーションエラーになる | 異常系 |
| 7 | ログアウトできる | 正常系 |

### テストファイルの作成

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

### コードリーディング（AAA形式で解説）

#### 共通パターン

| コード | 説明 |
|:---|:---|
| `bcrypt('password123')` | パスワードをハッシュ化して保存 |
| `assertAuthenticatedAs($user)` | 指定したユーザーとして認証されていることを確認 |
| `assertGuest()` | 認証されていない（ゲスト）状態であることを確認 |

#### `正しい認証情報でログインできる`（正常系）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | `User::factory()->create(['password' => bcrypt('password123')])` | ハッシュ化したパスワードでユーザーを作成 |
| **Act** | `$this->post(route('login'), ['email' => ..., 'password' => ...])` | ログインリクエストを送信 |
| **Assert** | `assertRedirect(route('tasks.index'))` | タスク一覧にリダイレクトされることを確認 |
| **Assert** | `assertAuthenticatedAs($user)` | 正しいユーザーとして認証されていることを確認 |

#### `間違ったパスワードではログインできない`（異常系）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | `User::factory()->create(['password' => bcrypt('password123')])` | 正しいパスワードでユーザーを作成 |
| **Act** | `$this->post(route('login'), ['password' => 'wrong-password'])` | **間違った**パスワードでリクエスト |
| **Assert** | `assertSessionHasErrors('email')` | エラーメッセージがあることを確認 |
| **Assert** | `assertGuest()` | 認証されていないことを確認 |

---

## 📝 ステップ2: RegistrationTest の作成

ユーザー登録機能のテストを作成します。

### 🧠 先輩エンジニアの視点：テスト項目を考える

ユーザー登録は**不正なデータの混入を防ぐ**必要があるため、バリデーションのテストを充実させます。

| 観点 | 考えること | 具体例 |
|:---|:---|:---|
| **正常系** | 正しいデータで登録できるか | 全項目入力で登録成功 |
| **異常系** | 不正なデータで適切にエラーになるか | 空入力、重複メール、形式不正 |
| **境界値** | 入力値の境界で正しく動作するか | パスワード8文字未満 |

### テスト項目一覧

| # | テスト名 | 観点 |
|:--|:---|:---|
| 1 | 登録画面を表示できる | 正常系 |
| 2 | 新規ユーザーを登録できる | 正常系 |
| 3 | 名前が空だとバリデーションエラーになる | 異常系 |
| 4 | メールアドレスが空だとバリデーションエラーになる | 異常系 |
| 5 | 無効なメールアドレス形式だとバリデーションエラーになる | 異常系 |
| 6 | 既に登録済みのメールアドレスだとバリデーションエラーになる | 異常系 |
| 7 | パスワードが8文字未満だとバリデーションエラーになる | 境界値 |
| 8 | パスワード確認が一致しないとバリデーションエラーになる | 異常系 |

### テストファイルの作成

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

### コードリーディング（AAA形式で解説）

#### `新規ユーザーを登録できる`（正常系）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | （なし） | 事前準備は不要 |
| **Act** | `$this->post(route('register'), ['name' => ..., 'email' => ..., ...])` | 登録リクエストを送信 |
| **Assert** | `assertRedirect(route('tasks.index'))` | タスク一覧にリダイレクトされることを確認 |
| **Assert** | `assertDatabaseHas('users', [...])` | ユーザーがDBに保存されていることを確認 |
| **Assert** | `assertAuthenticated()` | 認証されていることを確認 |

#### `パスワードが8文字未満だとバリデーションエラーになる`（境界値）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | （なし） | 事前準備は不要 |
| **Act** | `$this->post(route('register'), ['password' => 'short', ...])` | 7文字以下のパスワードでリクエスト |
| **Assert** | `assertSessionHasErrors('password')` | パスワードにバリデーションエラーがあることを確認 |

> **💡 境界値のポイント**: パスワードの最小長が8文字の場合、7文字（失敗）と8文字（成功）の両方をテストするのが理想的です。

#### 補足：使用するアサーション

| コード | 説明 |
|:---|:---|
| `assertAuthenticated()` | 認証されている状態であることを確認（ユーザーは問わない） |
| `password_confirmation` | Laravelの `confirmed` ルールで使用される確認用フィールド |

---

## 📝 ステップ3: 未認証リダイレクトテスト の作成

未認証ユーザーが保護されたページにアクセスした際のリダイレクトをテストします。

### 🧠 先輩エンジニアの視点：テスト項目を考える

このテストは**authミドルウェアが正しく機能しているか**を確認します。全て異常系（未認証でのアクセス）のテストです。

| 観点 | 考えること | 具体例 |
|:---|:---|:---|
| **異常系** | 未認証で保護されたページにアクセスできないか | ログインページへリダイレクト |

### テスト項目一覧

| # | テスト名 | 観点 |
|:--|:---|:---|
| 1 | 未認証ユーザーはタスク一覧にアクセスするとログインページにリダイレクトされる | 異常系 |
| 2 | 未認証ユーザーはタスク作成画面にアクセスするとログインページにリダイレクトされる | 異常系 |
| 3 | 未認証ユーザーはカテゴリー一覧にアクセスするとログインページにリダイレクトされる | 異常系 |
| 4 | 未認証ユーザーはカテゴリー作成画面にアクセスするとログインページにリダイレクトされる | 異常系 |

### テストファイルの作成

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

### コードリーディング（AAA形式で解説）

#### `未認証ユーザーはタスク一覧にアクセスするとログインページにリダイレクトされる`（異常系）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | （なし） | 未認証状態なので事前準備は不要 |
| **Act** | `$this->get(route('tasks.index'))` | **認証なしで**タスク一覧にアクセス |
| **Assert** | `assertRedirect(route('login'))` | ログインページにリダイレクトされることを確認 |

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
- [ ] 全てのテストがパスする（合計19テスト）
- [ ] 正常系・異常系の観点でテストが書かれている（境界値は登録側でカバー）

---

## ✨ まとめ

このセクションでは、認証機能のテストを実装しました。

| 学んだこと | 内容 |
|:---|:---|
| 認証テストの観点 | 正常系（認証成功）・異常系（認証失敗）が中心。境界値は登録側で検証 |
| ログインテスト | 正しい/間違った認証情報でのログイン動作を検証 |
| 登録テスト | ユーザー登録とバリデーション（重複チェック含む）を検証 |
| リダイレクトテスト | authミドルウェアによるアクセス制御を検証（異常系） |
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
- [ ] ログインテスト（7テスト：正常系3 + 異常系4）
- [ ] 登録テスト（8テスト：正常系2 + 異常系5 + 境界値1）
- [ ] 未認証リダイレクトテスト（4テスト：異常系4）

※ ログインテストは境界値を省略（登録時に検証済みのため）

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
