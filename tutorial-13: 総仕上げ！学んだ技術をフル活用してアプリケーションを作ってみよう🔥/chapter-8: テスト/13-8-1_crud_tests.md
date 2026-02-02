# 13-8-1 CRUDテスト実装

## 🎯 このセクションで学ぶこと

このセクションでは、タスクCRUD機能のFeatureテストを実装します。

- Featureテストの基本
- テスト用データベースの設定
- ファクトリを使ったテストデータの作成
- 認証が必要なテストの書き方
- アサーションメソッドの使い方

> **📌 対応Issue**: #8 CRUDテスト実装

---

## 🧠 先輩エンジニアの思考プロセス

テストを実装する際、先輩エンジニアは以下のように考えます。

> 「テストは品質を担保するために欠かせない。特にCRUD機能のテストは、アプリケーションの基本動作を確認するために重要だ。LaravelにはPHPUnitが組み込まれていて、Featureテストでは実際にHTTPリクエストを送信してレスポンスを検証できる。テスト用のデータはファクトリを使って効率的に作成しよう。」

### テストの種類

| 種類 | 説明 | 配置場所 |
|:---|:---|:---|
| **Featureテスト** | HTTPリクエストを送信してアプリケーション全体の動作を検証 | `tests/Feature/` |
| Unitテスト | 個々のクラスやメソッドを単独で検証 | `tests/Unit/` |

---

## 🔀 ブランチの作成

Issue駆動開発のワークフローに従い、まずはIssue #8に対応するブランチを作成します。

```bash
# 現在のブランチを確認（mainにいることを確認）
git branch

# mainブランチの最新状態を取得
git pull origin main

# Issue #8 に対応するブランチを作成して切り替え
git switch -c feature/issue-8-crud-tests
```

---

## 🏃 実践

### ステップ1: テスト用データベースの設定

テスト実行時に本番データベースを使わないよう、テスト用のデータベース設定を行います。

`phpunit.xml` を確認し、以下の設定があることを確認します。

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         colors="true"
>
    <testsuites>
        <testsuite name="Unit">
            <directory>tests/Unit</directory>
        </testsuite>
        <testsuite name="Feature">
            <directory>tests/Feature</directory>
        </testsuite>
    </testsuites>
    <source>
        <include>
            <directory>app</directory>
        </include>
    </source>
    <php>
        <env name="APP_ENV" value="testing"/>
        <env name="APP_MAINTENANCE_DRIVER" value="file"/>
        <env name="BCRYPT_ROUNDS" value="4"/>
        <env name="CACHE_STORE" value="array"/>
        <env name="DB_CONNECTION" value="sqlite"/>
        <env name="DB_DATABASE" value=":memory:"/>
        <env name="MAIL_MAILER" value="array"/>
        <env name="PULSE_ENABLED" value="false"/>
        <env name="QUEUE_CONNECTION" value="sync"/>
        <env name="SESSION_DRIVER" value="array"/>
        <env name="TELESCOPE_ENABLED" value="false"/>
    </php>
</phpunit>
```

#### 設定のコードリーディング

| 設定 | 説明 |
|:---|:---|
| `APP_ENV=testing` | テスト環境として実行 |
| `DB_CONNECTION=sqlite` | テスト用にSQLiteを使用 |
| `DB_DATABASE=:memory:` | インメモリデータベースを使用（高速） |
| `BCRYPT_ROUNDS=4` | パスワードハッシュの計算回数を減らして高速化 |

---

### ステップ2: ファクトリの確認

テストデータを効率的に作成するため、ファクトリを確認します。

#### UserFactoryの確認

`database/factories/UserFactory.php` を確認します。

```php
<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\User>
 */
class UserFactory extends Factory
{
    /**
     * The current password being used by the factory.
     */
    protected static ?string $password;

    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->unique()->safeEmail(),
            'email_verified_at' => now(),
            'password' => static::$password ??= Hash::make('password'),
            'remember_token' => Str::random(10),
        ];
    }

    /**
     * Indicate that the model's email address should be unverified.
     */
    public function unverified(): static
    {
        return $this->state(fn (array $attributes) => [
            'email_verified_at' => null,
        ]);
    }
}
```

#### CategoryFactoryの作成

`database/factories/CategoryFactory.php` を作成します。

```bash
# ファクトリの作成
sail artisan make:factory CategoryFactory --model=Category
```

```php
<?php

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Category>
 */
class CategoryFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => fake()->unique()->word(),
        ];
    }
}
```

#### TaskFactoryの作成

`database/factories/TaskFactory.php` を作成します。

```bash
# ファクトリの作成
sail artisan make:factory TaskFactory --model=Task
```

```php
<?php

namespace Database\Factories;

use App\Models\Category;
use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends \Illuminate\Database\Eloquent\Factories\Factory<\App\Models\Task>
 */
class TaskFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'user_id' => User::factory(),
            'category_id' => Category::factory(),
            'title' => fake()->sentence(3),
            'description' => fake()->paragraph(),
            'priority' => fake()->numberBetween(1, 3),
        ];
    }

    /**
     * 高優先度のタスクを作成
     */
    public function highPriority(): static
    {
        return $this->state(fn (array $attributes) => [
            'priority' => 3,
        ]);
    }

    /**
     * 低優先度のタスクを作成
     */
    public function lowPriority(): static
    {
        return $this->state(fn (array $attributes) => [
            'priority' => 1,
        ]);
    }
}
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `fake()->sentence(3)` | 3単語のランダムな文を生成 |
| `fake()->paragraph()` | ランダムな段落を生成 |
| `User::factory()` | リレーション先のモデルも自動生成 |
| `->state(fn (...) => [...])` | 特定の状態を持つファクトリを定義 |

---

### ステップ3: テストクラスの作成

タスクCRUDのFeatureテストを作成します。

```bash
# テストクラスの作成
sail artisan make:test TaskControllerTest
```

---

### ステップ4: テストの実装

`tests/Feature/TaskControllerTest.php` を以下のように編集します。

```php
<?php

namespace Tests\Feature;

use App\Models\Category;
use App\Models\Task;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class TaskControllerTest extends TestCase
{
    use RefreshDatabase;

    /**
     * テスト用のユーザーとカテゴリーを作成
     */
    private function createUserAndCategory(): array
    {
        $user = User::factory()->create();
        $category = Category::factory()->create();

        return [$user, $category];
    }

    /**
     * タスク一覧が表示されることをテスト
     */
    public function test_task_index_displays_tasks(): void
    {
        // Arrange（準備）
        $user = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $user->id]);

        // Act（実行）
        $response = $this->actingAs($user)->get(route('tasks.index'));

        // Assert（検証）
        $response->assertStatus(200);
        $response->assertSee($task->title);
    }

    /**
     * 他のユーザーのタスクが表示されないことをテスト
     */
    public function test_task_index_does_not_display_other_users_tasks(): void
    {
        // Arrange
        $user = User::factory()->create();
        $otherUser = User::factory()->create();
        $otherTask = Task::factory()->create(['user_id' => $otherUser->id]);

        // Act
        $response = $this->actingAs($user)->get(route('tasks.index'));

        // Assert
        $response->assertStatus(200);
        $response->assertDontSee($otherTask->title);
    }

    /**
     * タスク作成フォームが表示されることをテスト
     */
    public function test_task_create_form_is_displayed(): void
    {
        // Arrange
        $user = User::factory()->create();

        // Act
        $response = $this->actingAs($user)->get(route('tasks.create'));

        // Assert
        $response->assertStatus(200);
        $response->assertSee('タスク作成');
    }

    /**
     * タスクが正常に作成されることをテスト
     */
    public function test_task_can_be_created(): void
    {
        // Arrange
        [$user, $category] = $this->createUserAndCategory();

        $taskData = [
            'category_id' => $category->id,
            'title' => 'テストタスク',
            'description' => 'テストの説明',
            'priority' => 2,
        ];

        // Act
        $response = $this->actingAs($user)->post(route('tasks.store'), $taskData);

        // Assert
        $response->assertRedirect(route('tasks.index'));
        $response->assertSessionHas('success');

        $this->assertDatabaseHas('tasks', [
            'user_id' => $user->id,
            'title' => 'テストタスク',
        ]);
    }

    /**
     * バリデーションエラーでタスクが作成されないことをテスト
     */
    public function test_task_cannot_be_created_with_invalid_data(): void
    {
        // Arrange
        [$user, $category] = $this->createUserAndCategory();

        $taskData = [
            'category_id' => $category->id,
            'title' => '', // 空のタイトル（バリデーションエラー）
            'description' => 'テストの説明',
            'priority' => 2,
        ];

        // Act
        $response = $this->actingAs($user)->post(route('tasks.store'), $taskData);

        // Assert
        $response->assertSessionHasErrors('title');
        $this->assertDatabaseCount('tasks', 0);
    }

    /**
     * タスク詳細が表示されることをテスト
     */
    public function test_task_show_displays_task_details(): void
    {
        // Arrange
        $user = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->get(route('tasks.show', $task));

        // Assert
        $response->assertStatus(200);
        $response->assertSee($task->title);
        $response->assertSee($task->description);
    }

    /**
     * 他のユーザーのタスク詳細にアクセスできないことをテスト
     */
    public function test_cannot_view_other_users_task(): void
    {
        // Arrange
        $user = User::factory()->create();
        $otherUser = User::factory()->create();
        $otherTask = Task::factory()->create(['user_id' => $otherUser->id]);

        // Act
        $response = $this->actingAs($user)->get(route('tasks.show', $otherTask));

        // Assert
        $response->assertStatus(403);
    }

    /**
     * タスク編集フォームが表示されることをテスト
     */
    public function test_task_edit_form_is_displayed(): void
    {
        // Arrange
        $user = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->get(route('tasks.edit', $task));

        // Assert
        $response->assertStatus(200);
        $response->assertSee('タスク編集');
        $response->assertSee($task->title);
    }

    /**
     * タスクが正常に更新されることをテスト
     */
    public function test_task_can_be_updated(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create();
        $task = Task::factory()->create([
            'user_id' => $user->id,
            'category_id' => $category->id,
        ]);

        $updatedData = [
            'category_id' => $category->id,
            'title' => '更新後のタイトル',
            'description' => '更新後の説明',
            'priority' => 3,
        ];

        // Act
        $response = $this->actingAs($user)->put(route('tasks.update', $task), $updatedData);

        // Assert
        $response->assertRedirect(route('tasks.index'));
        $response->assertSessionHas('success');

        $this->assertDatabaseHas('tasks', [
            'id' => $task->id,
            'title' => '更新後のタイトル',
        ]);
    }

    /**
     * 他のユーザーのタスクを更新できないことをテスト
     */
    public function test_cannot_update_other_users_task(): void
    {
        // Arrange
        $user = User::factory()->create();
        $otherUser = User::factory()->create();
        $category = Category::factory()->create();
        $otherTask = Task::factory()->create([
            'user_id' => $otherUser->id,
            'category_id' => $category->id,
        ]);

        $updatedData = [
            'category_id' => $category->id,
            'title' => '更新後のタイトル',
            'description' => '更新後の説明',
            'priority' => 3,
        ];

        // Act
        $response = $this->actingAs($user)->put(route('tasks.update', $otherTask), $updatedData);

        // Assert
        $response->assertStatus(403);
    }

    /**
     * タスクが正常に削除されることをテスト
     */
    public function test_task_can_be_deleted(): void
    {
        // Arrange
        $user = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->delete(route('tasks.destroy', $task));

        // Assert
        $response->assertRedirect(route('tasks.index'));
        $response->assertSessionHas('success');

        $this->assertDatabaseMissing('tasks', [
            'id' => $task->id,
        ]);
    }

    /**
     * 他のユーザーのタスクを削除できないことをテスト
     */
    public function test_cannot_delete_other_users_task(): void
    {
        // Arrange
        $user = User::factory()->create();
        $otherUser = User::factory()->create();
        $otherTask = Task::factory()->create(['user_id' => $otherUser->id]);

        // Act
        $response = $this->actingAs($user)->delete(route('tasks.destroy', $otherTask));

        // Assert
        $response->assertStatus(403);

        $this->assertDatabaseHas('tasks', [
            'id' => $otherTask->id,
        ]);
    }

    /**
     * 未認証ユーザーがタスク一覧にアクセスできないことをテスト
     */
    public function test_unauthenticated_user_cannot_access_tasks(): void
    {
        // Act
        $response = $this->get(route('tasks.index'));

        // Assert
        $response->assertRedirect(route('login'));
    }
}
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `use RefreshDatabase` | 各テスト後にデータベースをリセット |
| `$this->actingAs($user)` | 指定したユーザーとしてログインした状態でリクエスト |
| `->get(route('tasks.index'))` | GETリクエストを送信 |
| `->post(route('tasks.store'), $data)` | POSTリクエストを送信 |
| `->put(route('tasks.update', $task), $data)` | PUTリクエストを送信 |
| `->delete(route('tasks.destroy', $task))` | DELETEリクエストを送信 |
| `->assertStatus(200)` | HTTPステータスコードを検証 |
| `->assertSee($text)` | レスポンスに指定したテキストが含まれることを検証 |
| `->assertDontSee($text)` | レスポンスに指定したテキストが含まれないことを検証 |
| `->assertRedirect($url)` | リダイレクト先を検証 |
| `->assertSessionHas('success')` | セッションにキーが存在することを検証 |
| `->assertSessionHasErrors('title')` | バリデーションエラーを検証 |
| `$this->assertDatabaseHas('tasks', [...])` | データベースにレコードが存在することを検証 |
| `$this->assertDatabaseMissing('tasks', [...])` | データベースにレコードが存在しないことを検証 |
| `$this->assertDatabaseCount('tasks', 0)` | テーブルのレコード数を検証 |

---

### ステップ5: テストの実行

テストを実行して、全てのテストが成功することを確認します。

```bash
# 全てのテストを実行
sail artisan test

# 特定のテストクラスのみ実行
sail artisan test --filter=TaskControllerTest

# 詳細な出力で実行
sail artisan test --filter=TaskControllerTest -v
```

#### 出力例

```
   PASS  Tests\Feature\TaskControllerTest
  ✓ task index displays tasks                                    0.15s
  ✓ task index does not display other users tasks                0.08s
  ✓ task create form is displayed                                0.05s
  ✓ task can be created                                          0.09s
  ✓ task cannot be created with invalid data                     0.06s
  ✓ task show displays task details                              0.07s
  ✓ cannot view other users task                                 0.06s
  ✓ task edit form is displayed                                  0.06s
  ✓ task can be updated                                          0.08s
  ✓ cannot update other users task                               0.06s
  ✓ task can be deleted                                          0.07s
  ✓ cannot delete other users task                               0.06s
  ✓ unauthenticated user cannot access tasks                     0.04s

  Tests:    13 passed (35 assertions)
  Duration: 1.02s
```

---

## 💡 TIP: テストの命名規則

テストメソッドの命名には、何をテストしているかが明確にわかる名前を付けましょう。

```php
// ✅ 良い例: 何をテストしているかが明確
public function test_task_can_be_created(): void
public function test_cannot_delete_other_users_task(): void

// ❌ 悪い例: 何をテストしているかが不明確
public function test_1(): void
public function test_task(): void
```

---

## 💡 TIP: AAAパターン

テストは **AAA（Arrange-Act-Assert）パターン** で書くと読みやすくなります。

```php
public function test_task_can_be_created(): void
{
    // Arrange（準備）: テストに必要なデータを準備
    [$user, $category] = $this->createUserAndCategory();
    $taskData = [...];

    // Act（実行）: テスト対象の処理を実行
    $response = $this->actingAs($user)->post(route('tasks.store'), $taskData);

    // Assert（検証）: 結果を検証
    $response->assertRedirect(route('tasks.index'));
    $this->assertDatabaseHas('tasks', [...]);
}
```

---

## ❌ よくある間違い

### 1. RefreshDatabaseを忘れる

```php
// ❌ NG: RefreshDatabaseがない
class TaskControllerTest extends TestCase
{
    // use RefreshDatabase がない
    
    public function test_task_can_be_created(): void
    {
        // 前のテストのデータが残っていて失敗する可能性がある
    }
}
```

**対処法**: `use RefreshDatabase;` を追加する。

### 2. actingAsを忘れる

```php
// ❌ NG: 認証なしでアクセス
public function test_task_can_be_created(): void
{
    $response = $this->post(route('tasks.store'), $taskData);
    // 結果: ログイン画面にリダイレクトされる
}
```

**対処法**: `$this->actingAs($user)` で認証状態を設定する。

### 3. ファクトリでリレーションを設定し忘れる

```php
// ❌ NG: user_idを設定していない
$task = Task::factory()->create();
// 結果: ランダムなユーザーのタスクが作成される

// ✅ OK: user_idを明示的に設定
$task = Task::factory()->create(['user_id' => $user->id]);
```

---

## ✅ 完了条件

以下の条件を満たしていることを確認してください。

- [ ] TaskControllerTestが作成されている
- [ ] CategoryFactoryとTaskFactoryが作成されている
- [ ] 全てのテストが成功する
- [ ] 認可のテスト（他のユーザーのタスクにアクセスできない）が含まれている

---

## ✨ まとめ

このセクションでは、タスクCRUD機能のFeatureテストを実装しました。

| 学んだこと | 内容 |
|:---|:---|
| Featureテスト | `sail artisan make:test` で作成 |
| ファクトリ | `sail artisan make:factory` でテストデータを効率的に作成 |
| 認証テスト | `$this->actingAs($user)` でログイン状態をシミュレート |
| データベースアサーション | `assertDatabaseHas`, `assertDatabaseMissing` |
| AAAパターン | Arrange-Act-Assert でテストを構造化 |

これでTutorial 13の全ての実装が完了しました。おめでとうございます！

---

## 🔄 Git操作とプルリクエスト

作業が完了したら、変更をコミットしてプッシュし、プルリクエストを作成して変更内容を確認しましょう。

### ステップ1: コミットとプッシュ

```bash
# 変更をステージング
git add .

# コミット（Issue番号を含める）
git commit -m "feat: CRUDテスト実装 #8"

# リモートにプッシュ
git push origin feature/issue-8-crud-tests
```

### ステップ2: プルリクエストの作成と確認

GitHubでプルリクエストを作成し、変更内容を確認してみましょう。

1. GitHubのリポジトリページを開く
2. 「Pull requests」タブをクリックする
3. 「New pull request」ボタンをクリックする
4. `base: main` ← `compare: feature/issue-8-crud-tests` を選択する
5. 「Create pull request」ボタンをクリックする
6. 以下の内容を入力する

**タイトル**:
```
feat: CRUDテスト実装
```

**説明欄**:
```markdown
## 概要
タスクCRUD機能のFeatureテストを実装しました。

## 変更内容
- TaskControllerTestの作成
- CategoryFactory, TaskFactoryの作成
- 認可テストの実装

## テスト内容
- タスク一覧表示テスト
- タスク作成テスト
- タスク編集テスト
- タスク削除テスト
- 認可テスト（他ユーザーのタスクにアクセス不可）

## 動作確認
- [ ] 全てのテストが成功する

## 対応Issue
close #8
```

7. 「Create pull request」ボタンをクリックする

> **💡 確認ポイント**: PRを作成したら、「Files changed」タブでテストコードを確認してみましょう。各テストメソッドがAAAパターンで書かれていること、認可のテストが含まれていることを確認できます。

### ステップ3: プルリクエストのマージ

変更内容を確認したら、PRをマージします。

1. PRのページで「Merge pull request」ボタンをクリックする
2. 「Confirm merge」ボタンをクリックする
3. マージが完了すると、Issue #8が自動的にクローズされる

### ステップ4: ローカルのmainブランチを更新し、ブランチを削除

```bash
# mainブランチに切り替え
git switch main

# リモートの変更を取り込む
git pull origin main

# マージ済みのブランチを削除
git branch -d feature/issue-8-crud-tests
```

> **📌 Issue対応**: PRをマージすると、説明欄の `close #8` によりIssue #8が自動的にクローズされます。

---

## 🎉 Tutorial 13 完了！

お疲れ様でした！Tutorial 13「総仕上げ！学んだ技術をフル活用してアプリケーションを作ってみよう」が完了しました。

このチュートリアルで学んだことを振り返りましょう。

| Chapter | 内容 |
|:---|:---|
| Chapter 1 | 要件定義と設計 |
| Chapter 2 | 品質保証の心得 |
| Chapter 3 | 環境構築とGit/GitHub設定 |
| Chapter 4 | マイグレーションとモデル |
| Chapter 5 | 認証機能（Fortify） |
| Chapter 6 | CRUD機能とPolicy |
| Chapter 7 | 公開API |
| Chapter 8 | テスト |

これらの知識を活かして、今後も素晴らしいアプリケーションを作成してください！
