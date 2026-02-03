# CRUD機能のテスト

## 🎯 このセクションで学ぶこと

このセクションでは、カテゴリーとタスクのCRUD機能に対するテストを実装します。

- CategoryControllerのテスト（一覧・詳細・作成・編集・削除）
- TaskControllerのテスト（一覧・詳細・作成・編集・削除）
- バリデーションエラーのテスト
- 認可（Policy）のテスト

テストを書くことで、機能が正しく動作することを保証し、将来の変更による不具合を防ぎます。

---

## 🌿 ブランチの作成

Issue #8 に対応するブランチを作成します。

```bash
# 現在のブランチを確認（mainにいることを確認）
git branch

# mainブランチの最新状態を取得
git pull origin main

# Issue #8 に対応するブランチを作成して切り替え
git switch -c feature/issue-8-crud-tests
```

---

## 📝 ステップ1: CategoryControllerTest の作成

カテゴリーのCRUD機能をテストします。

```bash
sail artisan make:test CategoryControllerTest
```

**ファイル**: `tests/Feature/CategoryControllerTest.php`

```php
<?php

namespace Tests\Feature;

use App\Models\Category;
use App\Models\Task;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class CategoryControllerTest extends TestCase
{
    use RefreshDatabase;

    /** @test */
    public function ユーザーはカテゴリー一覧を取得できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        Category::factory()->count(3)->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->get(route('categories.index'));

        // Assert
        $response->assertStatus(200);
        $response->assertViewHas('categories');
    }

    /** @test */
    public function ユーザーはカテゴリー詳細を取得できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->get(route('categories.show', $category));

        // Assert
        $response->assertStatus(200);
        $response->assertViewHas('category');
    }

    /** @test */
    public function ユーザーはカテゴリー作成画面を表示できる(): void
    {
        // Arrange
        $user = User::factory()->create();

        // Act
        $response = $this->actingAs($user)->get(route('categories.create'));

        // Assert
        $response->assertStatus(200);
    }

    /** @test */
    public function ユーザーはカテゴリーを作成できる(): void
    {
        // Arrange
        $user = User::factory()->create();

        // Act
        $response = $this->actingAs($user)->post(route('categories.store'), [
            'name' => 'テストカテゴリー',
        ]);

        // Assert
        $response->assertRedirect(route('categories.index'));
        $this->assertDatabaseHas('categories', [
            'name' => 'テストカテゴリー',
            'user_id' => $user->id,
        ]);
    }

    /** @test */
    public function カテゴリー名が空だとバリデーションエラーになる(): void
    {
        // Arrange
        $user = User::factory()->create();

        // Act
        $response = $this->actingAs($user)->post(route('categories.store'), [
            'name' => '',
        ]);

        // Assert
        $response->assertSessionHasErrors('name');
    }

    /** @test */
    public function カテゴリー名が256文字以上だとバリデーションエラーになる(): void
    {
        // Arrange
        $user = User::factory()->create();

        // Act
        $response = $this->actingAs($user)->post(route('categories.store'), [
            'name' => str_repeat('あ', 256),
        ]);

        // Assert
        $response->assertSessionHasErrors('name');
    }

    /** @test */
    public function ユーザーはカテゴリー編集画面を表示できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->get(route('categories.edit', $category));

        // Assert
        $response->assertStatus(200);
        $response->assertViewHas('category');
    }

    /** @test */
    public function ユーザーはカテゴリーを更新できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->put(route('categories.update', $category), [
            'name' => '更新後のカテゴリー名',
        ]);

        // Assert
        $response->assertRedirect(route('categories.index'));
        $this->assertDatabaseHas('categories', [
            'id' => $category->id,
            'name' => '更新後のカテゴリー名',
        ]);
    }

    /** @test */
    public function ユーザーはカテゴリーを削除できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->delete(route('categories.destroy', $category));

        // Assert
        $response->assertRedirect(route('categories.index'));
        $this->assertDatabaseMissing('categories', ['id' => $category->id]);
    }

    /** @test */
    public function タスクが紐づいているカテゴリーは削除できない(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create(['user_id' => $user->id]);
        // カテゴリーにタスクを紐づける
        Task::factory()->create([
            'user_id' => $user->id,
            'category_id' => $category->id,
        ]);

        // Act
        $response = $this->actingAs($user)->delete(route('categories.destroy', $category));

        // Assert
        $response->assertRedirect(route('categories.index'));
        $response->assertSessionHas('error'); // エラーメッセージがセッションに含まれる
        $this->assertDatabaseHas('categories', ['id' => $category->id]); // 削除されていない
    }
}
```

### コードリーディング

| コード | 説明 |
|:---|:---|
| `use RefreshDatabase` | 各テスト実行前にデータベースをリセット |
| `User::factory()->create()` | テスト用のユーザーを作成 |
| `$this->actingAs($user)` | 指定したユーザーとしてログインした状態でリクエスト |
| `assertStatus(200)` | HTTPステータスコードが200であることを確認 |
| `assertViewHas('categories')` | ビューに `categories` 変数が渡されていることを確認 |
| `assertRedirect()` | リダイレクトされることを確認 |
| `assertDatabaseHas()` | データベースに指定したレコードが存在することを確認 |
| `assertDatabaseMissing()` | データベースに指定したレコードが存在しないことを確認 |
| `assertSessionHasErrors()` | セッションにバリデーションエラーが含まれることを確認 |
| `assertSessionHas('error')` | セッションに指定したキーが含まれることを確認 |

---

## 📝 ステップ2: TaskControllerTest の作成

タスクのCRUD機能をテストします。

```bash
sail artisan make:test TaskControllerTest
```

**ファイル**: `tests/Feature/TaskControllerTest.php`

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

    /** @test */
    public function ユーザーはタスク一覧を取得できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        Task::factory()->count(3)->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->get(route('tasks.index'));

        // Assert
        $response->assertStatus(200);
        $response->assertViewHas('tasks');
    }

    /** @test */
    public function ユーザーはタスク詳細を取得できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->get(route('tasks.show', $task));

        // Assert
        $response->assertStatus(200);
        $response->assertViewHas('task');
    }

    /** @test */
    public function ユーザーはタスク作成画面を表示できる(): void
    {
        // Arrange
        $user = User::factory()->create();

        // Act
        $response = $this->actingAs($user)->get(route('tasks.create'));

        // Assert
        $response->assertStatus(200);
    }

    /** @test */
    public function ユーザーはタスクを作成できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->post(route('tasks.store'), [
            'title' => 'テストタスク',
            'description' => 'テストの説明',
            'status' => 'pending',
            'due_date' => '2025-12-31',
            'category_id' => $category->id,
        ]);

        // Assert
        $response->assertRedirect(route('tasks.index'));
        $this->assertDatabaseHas('tasks', [
            'title' => 'テストタスク',
            'user_id' => $user->id,
        ]);
    }

    /** @test */
    public function タスクタイトルが空だとバリデーションエラーになる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->post(route('tasks.store'), [
            'title' => '',
            'status' => 'pending',
            'category_id' => $category->id,
        ]);

        // Assert
        $response->assertSessionHasErrors('title');
    }

    /** @test */
    public function 無効なステータスだとバリデーションエラーになる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->post(route('tasks.store'), [
            'title' => 'テストタスク',
            'status' => 'invalid_status', // 無効なステータス
            'category_id' => $category->id,
        ]);

        // Assert
        $response->assertSessionHasErrors('status');
    }

    /** @test */
    public function ユーザーはタスク編集画面を表示できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->get(route('tasks.edit', $task));

        // Assert
        $response->assertStatus(200);
        $response->assertViewHas('task');
    }

    /** @test */
    public function ユーザーはタスクを更新できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $user->id]);
        $category = Category::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->put(route('tasks.update', $task), [
            'title' => '更新後のタスク名',
            'status' => 'completed',
            'category_id' => $category->id,
        ]);

        // Assert
        $response->assertRedirect(route('tasks.index'));
        $this->assertDatabaseHas('tasks', [
            'id' => $task->id,
            'title' => '更新後のタスク名',
            'status' => 'completed',
        ]);
    }

    /** @test */
    public function ユーザーはタスクを削除できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->delete(route('tasks.destroy', $task));

        // Assert
        $response->assertRedirect(route('tasks.index'));
        $this->assertDatabaseMissing('tasks', ['id' => $task->id]);
    }
}
```

---

## 📝 ステップ3: 認可テストの追加

TaskControllerTestに認可（Policy）のテストを追加します。他人のタスクにアクセスできないことを確認します。

**ファイル**: `tests/Feature/TaskControllerTest.php` に追記

```php
    // --- 認可テスト ---

    /** @test */
    public function 他人のタスク詳細にアクセスすると403エラーになる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $otherUser = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $otherUser->id]);

        // Act
        $response = $this->actingAs($user)->get(route('tasks.show', $task));

        // Assert
        $response->assertForbidden(); // 403
    }

    /** @test */
    public function 他人のタスク編集画面にアクセスすると403エラーになる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $otherUser = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $otherUser->id]);

        // Act
        $response = $this->actingAs($user)->get(route('tasks.edit', $task));

        // Assert
        $response->assertForbidden();
    }

    /** @test */
    public function 他人のタスクを更新しようとすると403エラーになる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $otherUser = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $otherUser->id]);
        $category = Category::factory()->create(['user_id' => $user->id]);

        // Act
        $response = $this->actingAs($user)->put(route('tasks.update', $task), [
            'title' => '不正な更新',
            'status' => 'pending',
            'category_id' => $category->id,
        ]);

        // Assert
        $response->assertForbidden();
    }

    /** @test */
    public function 他人のタスクを削除しようとすると403エラーになる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $otherUser = User::factory()->create();
        $task = Task::factory()->create(['user_id' => $otherUser->id]);

        // Act
        $response = $this->actingAs($user)->delete(route('tasks.destroy', $task));

        // Assert
        $response->assertForbidden();
    }
```

### コードリーディング

| コード | 説明 |
|:---|:---|
| `$otherUser = User::factory()->create()` | 別のユーザーを作成 |
| `['user_id' => $otherUser->id]` | タスクを別ユーザーの所有にする |
| `assertForbidden()` | 403ステータスコードを確認（`assertStatus(403)` と同等） |

---

## 🧪 ステップ4: テストの実行

作成したテストを実行して、全てパスすることを確認します。

```bash
# CategoryControllerTestを実行
sail test tests/Feature/CategoryControllerTest.php

# TaskControllerTestを実行
sail test tests/Feature/TaskControllerTest.php

# 両方のテストを実行
sail test --filter=ControllerTest
```

**期待される出力**:

```
   PASS  Tests\Feature\CategoryControllerTest
  ✓ ユーザーはカテゴリー一覧を取得できる
  ✓ ユーザーはカテゴリー詳細を取得できる
  ✓ ユーザーはカテゴリー作成画面を表示できる
  ✓ ユーザーはカテゴリーを作成できる
  ✓ カテゴリー名が空だとバリデーションエラーになる
  ✓ カテゴリー名が256文字以上だとバリデーションエラーになる
  ✓ ユーザーはカテゴリー編集画面を表示できる
  ✓ ユーザーはカテゴリーを更新できる
  ✓ ユーザーはカテゴリーを削除できる
  ✓ タスクが紐づいているカテゴリーは削除できない

   PASS  Tests\Feature\TaskControllerTest
  ✓ ユーザーはタスク一覧を取得できる
  ...
  ✓ 他人のタスクを削除しようとすると403エラーになる

  Tests:    24 passed
  Duration: 2.45s
```

---

## ❌ よくある間違い

### 1. RefreshDatabaseを忘れる

```php
// ❌ NG: データベースがリセットされない
class TaskControllerTest extends TestCase
{
    // use RefreshDatabase; が抜けている
}
```

**対処法**: テストクラスに `use RefreshDatabase;` を追加する。

### 2. actingAsを忘れる

```php
// ❌ NG: 未認証状態でリクエストしてしまう
$response = $this->get(route('tasks.index'));
// 結果: ログインページにリダイレクトされる
```

**対処法**: `$this->actingAs($user)` でログイン状態にする。

### 3. リレーションのuser_idを設定し忘れる

```php
// ❌ NG: タスクが別ユーザーの所有になる可能性がある
$task = Task::factory()->create();
// user_idがファクトリのデフォルト（新規ユーザー）になる
```

**対処法**: `['user_id' => $user->id]` を明示的に指定する。

---

## ✅ 完了条件

以下の条件を満たしていることを確認してください。

- [ ] CategoryControllerTestが作成されている
- [ ] TaskControllerTestが作成されている
- [ ] 全てのテストがパスする
- [ ] 認可テスト（4アクション分）が含まれている
- [ ] タスク紐づき時のカテゴリー削除不可テストが含まれている

---

## ✨ まとめ

このセクションでは、CRUD機能のテストを実装しました。

| 学んだこと | 内容 |
|:---|:---|
| Featureテスト | HTTPリクエストをシミュレートしてコントローラをテスト |
| actingAs | 特定のユーザーとしてログインした状態でテスト |
| assertDatabaseHas/Missing | データベースの状態を検証 |
| assertSessionHasErrors | バリデーションエラーを検証 |
| assertForbidden | 403エラー（認可エラー）を検証 |

次のセクションでは、認証機能のテストを実装します。

---

## 🔄 Git操作とプルリクエスト

作業が完了したら、変更をコミットしてプッシュし、プルリクエストを作成して変更内容を確認しましょう。

### ステップ1: コミットとプッシュ

```bash
# 変更をステージング
git add .

# コミット（Issue番号を含める）
git commit -m "feat: CRUD機能のテスト実装 #8"

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
feat: CRUD機能のテスト実装
```

**説明欄**:
```markdown
## 概要
カテゴリーとタスクのCRUD機能に対するテストを実装しました。

## 変更内容
- CategoryControllerTestの作成
- TaskControllerTestの作成
- バリデーションエラーのテスト
- 認可（Policy）のテスト

## テスト項目
- [ ] カテゴリーCRUD（10テスト）
- [ ] タスクCRUD（10テスト）
- [ ] 認可テスト（4テスト）

## 対応Issue
close #8
```

7. 「Create pull request」ボタンをクリックする

> **💡 確認ポイント**: PRを作成したら、「Files changed」タブでテストコードを確認してみましょう。AAAパターンに従っているか、テストケースが網羅的かを確認することで、テストの品質を担保できます。

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
