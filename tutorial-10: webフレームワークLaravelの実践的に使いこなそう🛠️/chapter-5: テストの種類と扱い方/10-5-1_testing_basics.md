# Tutorial 10-5-1: テストの基礎

## 🎯 このセクションで学ぶこと

*   テストが何であるか、なぜ重要なのかを理解する。
*   Laravelのテスト機能（PHPUnit）を使えるようになる。
*   フィーチャーテストとユニットテストの違いを理解する。

---

## 導入：「動いている」ことを証明する

これまでのセクションで、ルーティング、コントローラー、認証、バリデーションなど、様々な機能を実装してきました。しかし、「コードを書いた」だけでは、「正しく動いている」ことを保証できません。

例えば、以下のような状況を考えてみましょう。

*   新しい機能を追加したら、既存の機能が壊れてしまった
*   バグを修正したら、別の場所で新しいバグが発生した
*   リファクタリング（コードの整理）をしたら、動作が変わってしまった

これらの問題を防ぐために、**テスト（Test）**を書きます。テストとは、「コードが期待通りに動作するか」を自動的に確認するプログラムです。

---

## 詳細解説

### 🧪 テストの種類

Laravelでは、主に2種類のテストを書きます。

| テストの種類 | 説明 | 例 |
|:---|:---|:---|
| **ユニットテスト** | 個別の関数やメソッドが正しく動作するかをテスト | 「`calculateTotal()`メソッドが正しい合計を返すか」 |
| **フィーチャーテスト** | アプリケーション全体の機能が正しく動作するかをテスト | 「ユーザー登録画面が正しくユーザーを作成するか」 |

このセクションでは、**フィーチャーテスト**に焦点を当てます。

---

### 🛠️ テストの準備

Laravelには、**PHPUnit**というテストフレームワークが標準で組み込まれています。

#### テスト用データベースの設定

テストを実行する際は、本番データベースとは別の**テスト用データベース**を使います。これにより、テストが本番データに影響を与えることを防ぎます。

**`.env.testing`ファイルを作成**

```bash
docker compose exec php cp .env .env.testing
```

**`.env.testing`を編集**

```
DB_CONNECTION=sqlite
DB_DATABASE=:memory:
```

これにより、テスト時にはメモリ上のSQLiteデータベースが使われます。

---

### 📝 最初のテストを書く

#### テストファイルの生成

```bash
sail artisan make:test UserRegistrationTest
```

これにより、`tests/Feature/UserRegistrationTest.php`が生成されます。

**`tests/Feature/UserRegistrationTest.php`**

```php
<?php

namespace Tests\Feature;

use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class UserRegistrationTest extends TestCase
{
    use RefreshDatabase;

    /**
     * ユーザー登録が成功するかテスト
     */
    public function test_user_can_register(): void
    {
        $response = $this->post('/register', [
            'name' => '山田太郎',
            'email' => 'taro@example.com',
            'password' => 'password123',
            'password_confirmation' => 'password123',
        ]);

        $response->assertRedirect('/dashboard');

        $this->assertDatabaseHas('users', [
            'email' => 'taro@example.com'
        ]);

        $this->assertAuthenticated();
    }
}
```

**コードリーディング**

*   `use RefreshDatabase;`: テストごとにデータベースをリセットします。これにより、テスト間でデータが干渉しません。
*   `public function test_user_can_register()`: テストメソッドは、`test_`で始める必要があります。
*   `$this->post('/register', [...])`: `/register`エンドポイントにPOSTリクエストを送信します。
*   `$response->assertRedirect('/dashboard')`: ダッシュボードにリダイレクトされることを確認します。
*   `$this->assertDatabaseHas('users', [...])`: データベースに指定したデータが存在することを確認します。
*   `$this->assertAuthenticated()`: ユーザーが認証済みであることを確認します。

---

### 🚀 テストの実行

```bash
sail artisan test
```

**実行結果のイメージ**

```
PASS  Tests\Feature\UserRegistrationTest
✓ user can register

Tests:  1 passed
Time:   0.5s
```

テストが成功すると、緑色のチェックマークが表示されます。

---

### 🔍 テストのアサーション（検証）

Laravelには、様々なアサーションメソッドが用意されています。

#### HTTPレスポンスのアサーション

| メソッド | 説明 |
|:---|:---|
| `assertStatus(200)` | ステータスコードが200であることを確認 |
| `assertOk()` | ステータスコードが200であることを確認（`assertStatus(200)`と同じ） |
| `assertCreated()` | ステータスコードが201であることを確認 |
| `assertNotFound()` | ステータスコードが404であることを確認 |
| `assertUnauthorized()` | ステータスコードが401であることを確認 |
| `assertForbidden()` | ステータスコードが403であることを確認 |

#### JSONレスポンスのアサーション

| メソッド | 説明 |
|:---|:---|
| `assertJson(['key' => 'value'])` | JSONに指定したキーと値が含まれることを確認 |
| `assertJsonStructure(['key1', 'key2'])` | JSONの構造が期待通りであることを確認 |
| `assertJsonPath('user.name', '山田太郎')` | JSONの特定のパスの値を確認 |

#### データベースのアサーション

| メソッド | 説明 |
|:---|:---|
| `assertDatabaseHas('users', [...])` | データベースに指定したデータが存在することを確認 |
| `assertDatabaseMissing('users', [...])` | データベースに指定したデータが存在しないことを確認 |
| `assertDatabaseCount('users', 5)` | データベースのレコード数を確認 |

---

### 🔑 認証が必要なページのテスト

認証が必要なページをテストする場合は、`actingAs()`メソッドを使います。

```php
use App\Models\User;

public function test_authenticated_user_can_access_dashboard(): void
{
    $user = User::factory()->create();

    $response = $this->actingAs($user)
                     ->get('/dashboard');

    $response->assertOk();
}
```

**コードリーディング**

*   `User::factory()->create()`: ファクトリーを使って、テスト用のユーザーを作成します（次のセクションで詳しく学びます）。
*   `$this->actingAs($user)`: 指定したユーザーとして認証された状態でリクエストを送信します。

---

### 📊 テストカバレッジ

テストカバレッジとは、「コードのどの部分がテストされているか」を示す指標です。理想的には、全てのコードがテストされている状態（100%カバレッジ）が望ましいですが、現実的には70〜80%を目指すのが一般的です。

---

## 💡 TIP: テスト駆動開発（TDD）

テスト駆動開発（Test-Driven Development, TDD）とは、「先にテストを書いてから、コードを書く」という開発手法です。

**TDDの流れ**

1. **Red**: まず、失敗するテストを書く
2. **Green**: テストが通る最小限のコードを書く
3. **Refactor**: コードをリファクタリング（整理）する

TDDを実践することで、バグの少ない、保守しやすいコードを書くことができます。

---

## ✨ まとめ

このセクションでは、Laravelのテスト機能の基礎を学びました。

*   テストとは、コードが期待通りに動作するかを自動的に確認するプログラムである。
*   Laravelには、PHPUnitというテストフレームワークが標準で組み込まれている。
*   フィーチャーテストは、アプリケーション全体の機能をテストする。
*   `assertStatus()`, `assertJson()`, `assertDatabaseHas()`などのアサーションメソッドを使って、期待通りの動作を確認できる。
*   `actingAs()`を使って、認証が必要なページをテストできる。

次のセクションでは、ファクトリーとシーダーを使って、テストデータを効率的に生成する方法を学びます。

---
