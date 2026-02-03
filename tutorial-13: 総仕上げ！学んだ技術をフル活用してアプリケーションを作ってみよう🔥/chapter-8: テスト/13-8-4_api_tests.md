# APIのテスト

## 🎯 このセクションで学ぶこと

このセクションでは、公開APIに対するテストを実装します。

- GET /api/tasks（タスク一覧取得）のテスト
- GET /api/tasks/{id}（タスク詳細取得）のテスト
- 404エラー（存在しないリソース）のテスト

APIテストでは、JSONレスポンスの構造や内容を検証します。

---

## 🌿 ブランチの作成

Issue #10 に対応するブランチを作成します。

```bash
# 現在のブランチを確認（mainにいることを確認）
git branch

# mainブランチの最新状態を取得
git pull origin main

# Issue #10 に対応するブランチを作成して切り替え
git switch -c feature/issue-10-api-tests
```

---

## 📝 ステップ1: ApiTaskTest の作成

公開APIのテストを作成します。

### 🧠 先輩エンジニアの視点：テスト項目を考える

APIテストでは、**レスポンスの構造と内容の両方**を検証することが重要です。また、エッジケース（データが0件の場合など）も忘れずにテストします。

| 観点 | 考えること | 具体例 |
|:---|:---|:---|
| **正常系** | APIが正しいレスポンスを返すか | 一覧取得、詳細取得 |
| **異常系** | 存在しないリソースで適切なエラーを返すか | 404エラー |
| **境界値** | データが0件の場合に正しく動作するか | 空配列を返す |

### テスト項目一覧

| # | テスト名 | 観点 |
|:--|:---|:---|
| 1 | タスク一覧をJSON形式で取得できる | 正常系 |
| 2 | タスク一覧のJSONレスポンス構造が正しい | 正常系 |
| 3 | タスク一覧のJSONレスポンス内容が正しい | 正常系 |
| 4 | タスクが0件の場合は空の配列を返す | 境界値 |
| 5 | 特定のタスクをJSON形式で取得できる | 正常系 |
| 6 | 特定のタスクのJSONレスポンス内容が正しい | 正常系 |
| 7 | 存在しないタスクIDで404エラーを返す | 異常系 |
| 8 | 無効なタスクIDで404エラーを返す | 異常系 |

### テストファイルの作成

```bash
sail artisan make:test ApiTaskTest
```

**ファイル**: `tests/Feature/ApiTaskTest.php`

```php
<?php

namespace Tests\Feature;

use App\Models\Category;
use App\Models\Task;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class ApiTaskTest extends TestCase
{
    use RefreshDatabase;

    /** @test */
    public function タスク一覧をJSON形式で取得できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create();
        Task::factory()->count(3)->create([
            'user_id' => $user->id,
            'category_id' => $category->id,
        ]);

        // Act
        $response = $this->getJson('/api/tasks');

        // Assert
        $response->assertStatus(200);
        $response->assertJsonCount(3, 'data');
    }

    /** @test */
    public function タスク一覧のJSONレスポンス構造が正しい(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create(['name' => 'テストカテゴリー']);
        Task::factory()->create([
            'user_id' => $user->id,
            'category_id' => $category->id,
            'title' => 'テストタスク',
            'priority' => 2,
        ]);

        // Act
        $response = $this->getJson('/api/tasks');

        // Assert
        $response->assertStatus(200);
        $response->assertJsonStructure([
            'data' => [
                '*' => [
                    'id',
                    'title',
                    'priority',
                    'priority_label',
                    'category' => [
                        'id',
                        'name',
                    ],
                ],
            ],
        ]);
    }

    /** @test */
    public function タスク一覧のJSONレスポンス内容が正しい(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create(['name' => 'テストカテゴリー']);
        $task = Task::factory()->create([
            'user_id' => $user->id,
            'category_id' => $category->id,
            'title' => 'テストタスク',
            'priority' => 2,
        ]);

        // Act
        $response = $this->getJson('/api/tasks');

        // Assert
        $response->assertStatus(200);
        $response->assertJsonFragment([
            'id' => $task->id,
            'title' => 'テストタスク',
            'priority' => 2,
            'priority_label' => '中',
        ]);
        $response->assertJsonFragment([
            'name' => 'テストカテゴリー',
        ]);
    }

    /** @test */
    public function タスクが0件の場合は空の配列を返す(): void
    {
        // Act
        $response = $this->getJson('/api/tasks');

        // Assert
        $response->assertStatus(200);
        $response->assertJsonCount(0, 'data');
        $response->assertJson(['data' => []]);
    }

    /** @test */
    public function 特定のタスクをJSON形式で取得できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create(['name' => 'テストカテゴリー']);
        $task = Task::factory()->create([
            'user_id' => $user->id,
            'category_id' => $category->id,
            'title' => 'テストタスク',
            'description' => 'テストの説明',
            'priority' => 3,
        ]);

        // Act
        $response = $this->getJson("/api/tasks/{$task->id}");

        // Assert
        $response->assertStatus(200);
        $response->assertJsonStructure([
            'data' => [
                'id',
                'title',
                'description',
                'priority',
                'priority_label',
                'category' => [
                    'id',
                    'name',
                ],
            ],
        ]);
    }

    /** @test */
    public function 特定のタスクのJSONレスポンス内容が正しい(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create(['name' => '仕事']);
        $task = Task::factory()->create([
            'user_id' => $user->id,
            'category_id' => $category->id,
            'title' => '重要なタスク',
            'description' => 'これは重要なタスクです',
            'priority' => 3,
        ]);

        // Act
        $response = $this->getJson("/api/tasks/{$task->id}");

        // Assert
        $response->assertStatus(200);
        $response->assertJson([
            'data' => [
                'id' => $task->id,
                'title' => '重要なタスク',
                'description' => 'これは重要なタスクです',
                'priority' => 3,
                'priority_label' => '高',
                'category' => [
                    'id' => $category->id,
                    'name' => '仕事',
                ],
            ],
        ]);
    }

    /** @test */
    public function 存在しないタスクIDで404エラーを返す(): void
    {
        // Act
        $response = $this->getJson('/api/tasks/99999');

        // Assert
        $response->assertNotFound(); // 404
    }

    /** @test */
    public function 無効なタスクIDで404エラーを返す(): void
    {
        // Act
        $response = $this->getJson('/api/tasks/invalid');

        // Assert
        $response->assertStatus(404);
    }
}
```

### コードリーディング（AAA形式で解説）

#### `タスク一覧をJSON形式で取得できる`（正常系）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | `Task::factory()->count(3)->create([...])` | テスト用タスクを3件作成 |
| **Act** | `$this->getJson('/api/tasks')` | JSON形式でGETリクエストを送信 |
| **Assert** | `assertStatus(200)` | ステータスコード200を確認 |
| **Assert** | `assertJsonCount(3, 'data')` | データが3件あることを確認 |

#### `タスクが0件の場合は空の配列を返す`（境界値）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | （なし） | データを作成しない |
| **Act** | `$this->getJson('/api/tasks')` | 空のデータベースに対してリクエスト |
| **Assert** | `assertJsonCount(0, 'data')` | データが0件であることを確認 |
| **Assert** | `assertJson(['data' => []])` | 空配列が返ることを確認 |

#### `存在しないタスクIDで404エラーを返す`（異常系）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | （なし） | 存在しないIDにアクセスするので準備不要 |
| **Act** | `$this->getJson('/api/tasks/99999')` | 存在しないIDでリクエスト |
| **Assert** | `assertNotFound()` | 404エラーが返ることを確認 |

#### 補足：使用するアサーション

| コード | 説明 |
|:---|:---|
| `assertJsonStructure([...])` | JSONレスポンスの構造を検証 |
| `assertJsonFragment([...])` | JSONレスポンスに指定した内容が含まれることを確認 |
| `assertJson([...])` | JSONレスポンスが指定した内容と一致することを確認 |
| `'*' => [...]` | 配列内の全要素が指定した構造を持つことを確認 |

---

## 📚 APIテストのポイント

### getJson vs get

```php
// getJson(): JSON形式でリクエスト（Acceptヘッダーが自動設定される）
$response = $this->getJson('/api/tasks');

// get(): 通常のHTTPリクエスト
$response = $this->get('/api/tasks');
```

APIテストでは `getJson()` を使用することで、`Accept: application/json` ヘッダーが自動的に設定され、APIらしいレスポンスを受け取れます。

### assertJsonStructure の使い方

```php
// 単純な構造
$response->assertJsonStructure([
    'id',
    'title',
    'priority',
]);

// ネストした構造
$response->assertJsonStructure([
    'data' => [
        'id',
        'title',
        'category' => [
            'id',
            'name',
        ],
    ],
]);

// 配列内の全要素を検証（* を使用）
$response->assertJsonStructure([
    'data' => [
        '*' => [
            'id',
            'title',
        ],
    ],
]);
```

### assertJson vs assertJsonFragment

```php
// assertJson(): 完全一致（指定した内容が全て含まれる必要がある）
$response->assertJson([
    'data' => [
        'id' => 1,
        'title' => 'テスト',
    ],
]);

// assertJsonFragment(): 部分一致（指定した内容が含まれていればOK）
$response->assertJsonFragment([
    'title' => 'テスト',
]);
```

---

## 🧪 ステップ2: テストの実行

作成したテストを実行して、全てパスすることを確認します。

```bash
# ApiTaskTestを実行
sail test tests/Feature/ApiTaskTest.php
```

**期待される出力**:

```
   PASS  Tests\Feature\ApiTaskTest
  ✓ タスク一覧をJSON形式で取得できる
  ✓ タスク一覧のJSONレスポンス構造が正しい
  ✓ タスク一覧のJSONレスポンス内容が正しい
  ✓ タスクが0件の場合は空の配列を返す
  ✓ 特定のタスクをJSON形式で取得できる
  ✓ 特定のタスクのJSONレスポンス内容が正しい
  ✓ 存在しないタスクIDで404エラーを返す
  ✓ 無効なタスクIDで404エラーを返す

  Tests:    8 passed
  Duration: 0.95s
```

---

## 🧪 ステップ3: 全テストの実行

Chapter 8で作成した全てのテストを実行して、全てパスすることを確認します。

```bash
# 全てのテストを実行
sail test

# カバレッジレポートを生成（オプション）
sail test --coverage
```

**期待される出力**:

```
   PASS  Tests\Feature\ApiTaskTest
  ✓ タスク一覧をJSON形式で取得できる                                    0.12s
  ...

   PASS  Tests\Feature\AuthenticationTest
  ✓ ログイン画面を表示できる                                            0.08s
  ...

   PASS  Tests\Feature\CategoryControllerTest
  ✓ ユーザーはカテゴリー一覧を取得できる                                0.10s
  ...

   PASS  Tests\Feature\RegistrationTest
  ✓ 登録画面を表示できる                                                0.07s
  ...

   PASS  Tests\Feature\TaskControllerTest
  ✓ ユーザーはタスク一覧を取得できる                                    0.09s
  ...

   PASS  Tests\Feature\UnauthenticatedRedirectTest
  ✓ 未認証ユーザーはタスク一覧にアクセスするとログインページにリダイレクトされる
  ...

  Tests:    54 passed
  Duration: 5.00s
```

---

## ❌ よくある間違い

### 1. getJsonを使わずにgetを使う

```php
// ❌ NG: Acceptヘッダーが設定されない
$response = $this->get('/api/tasks');

// ✅ OK: JSON形式でリクエスト
$response = $this->getJson('/api/tasks');
```

### 2. assertJsonStructureで配列を検証する際に * を忘れる

```php
// ❌ NG: 配列の最初の要素しか検証されない
$response->assertJsonStructure([
    'data' => [
        'id',
        'title',
    ],
]);

// ✅ OK: 配列内の全要素を検証
$response->assertJsonStructure([
    'data' => [
        '*' => [
            'id',
            'title',
        ],
    ],
]);
```

### 3. APIリソースのラッパーを忘れる

```php
// ❌ NG: dataキーを忘れている
$response->assertJsonCount(3); // 失敗する

// ✅ OK: dataキーを指定
$response->assertJsonCount(3, 'data');
```

---

## ✅ 完了条件

以下の条件を満たしていることを確認してください。

- [ ] ApiTaskTestが作成されている（8テスト）
- [ ] タスク一覧取得のテストがパスする
- [ ] タスク詳細取得のテストがパスする
- [ ] 404エラーのテストがパスする
- [ ] 正常系・異常系・境界値の3観点でテストが書かれている
- [ ] Chapter 8の全テスト（53テスト）がパスする

---

## ✨ まとめ

このセクションでは、APIのテストを実装しました。

| 学んだこと | 内容 |
|:---|:---|
| APIテストの3観点 | 正常系（レスポンス検証）・異常系（404エラー）・境界値（0件の場合） |
| getJson | JSON形式でGETリクエストを送信 |
| assertJsonStructure | JSONレスポンスの構造を検証 |
| assertJsonFragment | JSONレスポンスに指定した内容が含まれることを確認 |
| assertJsonCount | JSON配列の要素数を検証 |
| 404テスト | 存在しないリソースへのアクセスを検証（異常系） |

---

## 🔄 Git操作とプルリクエスト

作業が完了したら、変更をコミットしてプッシュし、プルリクエストを作成して変更内容を確認しましょう。

### ステップ1: コミットとプッシュ

```bash
# 変更をステージング
git add .

# コミット（Issue番号を含める）
git commit -m "feat: APIテスト実装 #10"

# リモートにプッシュ
git push origin feature/issue-10-api-tests
```

### ステップ2: プルリクエストの作成と確認

GitHubでプルリクエストを作成し、変更内容を確認してみましょう。

1. GitHubのリポジトリページを開く
2. 「Pull requests」タブをクリックする
3. 「New pull request」ボタンをクリックする
4. `base: main` ← `compare: feature/issue-10-api-tests` を選択する
5. 「Create pull request」ボタンをクリックする
6. 以下の内容を入力する

**タイトル**:
```
feat: APIテスト実装
```

**説明欄**:
```markdown
## 概要
公開API（タスク一覧・詳細取得）に対するテストを実装しました。

## 変更内容
- ApiTaskTestの作成
- タスク一覧取得のテスト
- タスク詳細取得のテスト
- 404エラーのテスト

## テスト項目
- [ ] タスク一覧取得（4テスト：正常系3 + 境界値1）
- [ ] タスク詳細取得（2テスト：正常系2）
- [ ] 404エラー（2テスト：異常系2）

## 対応Issue
close #10
```

7. 「Create pull request」ボタンをクリックする

> **💡 確認ポイント**: PRを作成したら、「Files changed」タブでテストコードを確認してみましょう。APIテストでは、レスポンスの構造だけでなく、内容も正しく検証しているか確認することが重要です。

### ステップ3: プルリクエストのマージ

変更内容を確認したら、PRをマージします。

1. PRのページで「Merge pull request」ボタンをクリックする
2. 「Confirm merge」ボタンをクリックする
3. マージが完了すると、Issue #10が自動的にクローズされる

### ステップ4: ローカルのmainブランチを更新し、ブランチを削除

```bash
# mainブランチに切り替え
git switch main

# リモートの変更を取り込む
git pull origin main

# マージ済みのブランチを削除
git branch -d feature/issue-10-api-tests
```

> **📌 Issue対応**: PRをマージすると、説明欄の `close #10` によりIssue #10が自動的にクローズされます。

---

## 🎉 Tutorial 13 完了！

おめでとうございます！Tutorial 13「総仕上げ！学んだ技術をフル活用してアプリケーションを作ってみよう」を完了しました。

### 学習内容の振り返り

| Chapter | 学んだこと |
|:---|:---|
| Chapter 1 | 要件定義とデータベース設計 |
| Chapter 2 | プロジェクト概要の把握 |
| Chapter 3 | 環境構築とGit/GitHubワークフロー |
| Chapter 4 | マイグレーションとモデル（リレーション） |
| Chapter 5 | 認証機能（Laravel Fortify） |
| Chapter 6 | CRUD機能とPolicy（認可） |
| Chapter 7 | 公開API（APIリソース） |
| Chapter 8 | テスト（PHPUnit） |

### 身についたスキル

- **設計力**: 要件定義からデータベース設計まで一貫して行える
- **実装力**: Laravel の主要機能（認証・CRUD・API・Policy）を使いこなせる
- **テスト力**: PHPUnit でテストを書いて品質を保証できる
- **Git/GitHub運用**: Issue駆動開発、ブランチ戦略、PRベースのワークフローを実践できる

### 次のステップ

このチュートリアルで学んだ知識を活かして、以下のことに挑戦してみましょう。

1. **機能追加**: タスクの検索機能、ソート機能、フィルター機能を追加する
2. **UI改善**: Tailwind CSS を使ってデザインを改善する
3. **テスト拡充**: カバレッジを上げて、より堅牢なアプリケーションにする
4. **デプロイ**: 本番環境にデプロイして公開する

---

**お疲れ様でした！** これで、Laravel を使った実践的なアプリケーション開発の基礎が身につきました。この経験を活かして、さらに高度なアプリケーション開発に挑戦してください。
