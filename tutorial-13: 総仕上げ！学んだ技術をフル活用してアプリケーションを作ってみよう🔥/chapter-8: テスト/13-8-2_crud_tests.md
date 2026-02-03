# Tutorial 13-8-3: CRUD機能のテスト

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

## 🗑️ デフォルトのテストファイルを削除

Laravelには、デフォルトでサンプルのテストファイル（ExampleTest）が含まれています。これらは今回のアプリケーションでは動作しないため、削除します。

```bash
# デフォルトのExampleTestを削除
rm tests/Feature/ExampleTest.php
rm tests/Unit/ExampleTest.php

# tests/Unitディレクトリを維持するため、.gitkeepを作成
touch tests/Unit/.gitkeep
```

> **💡 なぜ削除するのか？**: デフォルトのExampleTestは、Laravelの初期状態（`/` にアクセスするとウェルカムページが表示される）を前提としたテストです。今回のアプリケーションでは `/` はログインページにリダイレクトするため、そのままではエラーになります。
>
> **📌 .gitkeepについて**: `tests/Unit/`ディレクトリが空になると、PHPUnitが「Test directory not found」という警告を出します。`.gitkeep`は空のファイルで、Gitで空ディレクトリを維持するための慣習的なファイルです。

---

## 📝 ステップ1: CategoryControllerTest の作成

カテゴリーのCRUD機能をテストします。

### 🧠 先輩エンジニアの視点：テスト項目を考える

CRUDコントローラのテストを書く際、13-8-1で学んだ**3つの観点**でテスト項目を洗い出します。

| 観点 | 考えること | 具体例 |
|:---|:---|:---|
| **正常系** | 期待通りの入力で正しく動作するか | CRUD各アクションが成功する |
| **異常系** | エラー時に適切にハンドリングされるか | 空入力、ビジネスルール違反 |
| **境界値** | 上限・下限ギリギリで正しく動作するか | 255文字OK、256文字NG |

### テスト項目一覧

| # | テスト名 | 観点 |
|:--|:---|:---|
| 1 | ユーザーはカテゴリー一覧を取得できる | 正常系 |
| 2 | ユーザーはカテゴリー詳細を取得できる | 正常系 |
| 3 | ユーザーはカテゴリー作成画面を表示できる | 正常系 |
| 4 | ユーザーはカテゴリーを作成できる | 正常系 |
| 5 | カテゴリー名が空だとバリデーションエラーになる | 異常系 |
| 6 | カテゴリー名は255文字まで入力できる | 境界値 |
| 7 | カテゴリー名が256文字以上だとバリデーションエラーになる | 境界値 |
| 8 | ユーザーはカテゴリー編集画面を表示できる | 正常系 |
| 9 | ユーザーはカテゴリーを更新できる | 正常系 |
| 10 | ユーザーはカテゴリーを削除できる | 正常系 |
| 11 | タスクが紐づいているカテゴリーは削除できない | 異常系 |

### テストファイルの作成

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
        Category::factory()->count(3)->create();

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
        $category = Category::factory()->create();

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
    public function カテゴリー名は255文字まで入力できる(): void
    {
        // Arrange
        $user = User::factory()->create();

        // Act
        $response = $this->actingAs($user)->post(route('categories.store'), [
            'name' => str_repeat('あ', 255),
        ]);

        // Assert
        $response->assertRedirect(route('categories.index'));
        $this->assertDatabaseHas('categories', [
            'name' => str_repeat('あ', 255),
        ]);
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
        $category = Category::factory()->create();

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
        $category = Category::factory()->create();

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
        $category = Category::factory()->create();

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
        $category = Category::factory()->create();
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

### コードリーディング（AAA形式で解説）

#### 共通パターン

| コード | 説明 |
|:---|:---|
| `use RefreshDatabase` | 各テスト実行前にデータベースをリセット |
| `$this->actingAs($user)` | 指定したユーザーとしてログインした状態でリクエスト |

#### `ユーザーはカテゴリーを作成できる`（正常系）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | `$user = User::factory()->create()` | テスト用ユーザーを作成 |
| **Act** | `$this->actingAs($user)->post(route('categories.store'), [...])` | ログイン状態でPOSTリクエストを送信 |
| **Assert** | `assertRedirect(route('categories.index'))` | 一覧ページにリダイレクトされることを確認 |
| **Assert** | `assertDatabaseHas('categories', [...])` | カテゴリーがDBに保存されていることを確認 |

#### `カテゴリー名が空だとバリデーションエラーになる`（異常系）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | `$user = User::factory()->create()` | テスト用ユーザーを作成 |
| **Act** | `post(route('categories.store'), ['name' => ''])` | 空のnameでPOSTリクエスト |
| **Assert** | `assertSessionHasErrors('name')` | nameフィールドにバリデーションエラーがあることを確認 |

#### `カテゴリー名は255文字まで入力できる` / `256文字以上だとエラー`（境界値）

| フェーズ | 255文字（成功） | 256文字（失敗） |
|:---|:---|:---|
| **Arrange** | ユーザーを作成 | ユーザーを作成 |
| **Act** | `str_repeat('あ', 255)` でPOST | `str_repeat('あ', 256)` でPOST |
| **Assert** | `assertRedirect` + `assertDatabaseHas` | `assertSessionHasErrors('name')` |

> **💡 境界値テストのポイント**: 上限ギリギリ（255文字）で**成功**することと、上限を超えた（256文字）で**失敗**することの両方をテストします。

#### `タスクが紐づいているカテゴリーは削除できない`（異常系：ビジネスルール）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | `$category = Category::factory()->create()` | カテゴリーを作成 |
| **Arrange** | `Task::factory()->create(['category_id' => $category->id])` | そのカテゴリーにタスクを紐づけ |
| **Act** | `delete(route('categories.destroy', $category))` | 削除リクエストを送信 |
| **Assert** | `assertSessionHas('error')` | エラーメッセージがセッションにあることを確認 |
| **Assert** | `assertDatabaseHas('categories', [...])` | カテゴリーが削除されていないことを確認 |

> **💡 異常系の種類**: 異常系には「バリデーションエラー」「認可エラー」「ビジネスルール違反」などがあります。どれも「期待通りでない操作」に対して適切にエラーハンドリングされることを確認します。

---

## 📝 ステップ2: TaskControllerTest の作成

タスクのCRUD機能をテストします。

### 🧠 先輩エンジニアの視点：テスト項目を考える

タスクはカテゴリーと異なり、**ユーザーに紐づくリソース**です。そのため、異常系の中でも特に**認可**（他人のタスクにアクセスできないこと）のテストが重要になります。

| 観点 | 考えること | 具体例 |
|:---|:---|:---|
| **正常系** | 期待通りの入力で正しく動作するか | CRUD各アクションが成功する |
| **異常系** | エラー時に適切にハンドリングされるか | 空入力、無効値、**認可エラー** |
| **境界値** | 上限・下限ギリギリで正しく動作するか | タイトル255文字OK、256文字NG |

> **💡 ポイント**: 「誰のデータか」を意識するリソースでは、認可テスト（異常系）が特に重要です。セキュリティに直結するため、必ずテストを書きましょう。

### テスト項目一覧

| # | テスト名 | 観点 |
|:--|:---|:---|
| 1 | ユーザーはタスク一覧を取得できる | 正常系 |
| 2 | ユーザーはタスク詳細を取得できる | 正常系 |
| 3 | ユーザーはタスク作成画面を表示できる | 正常系 |
| 4 | ユーザーはタスクを作成できる | 正常系 |
| 5 | タスクタイトルが空だとバリデーションエラーになる | 異常系 |
| 6 | 無効な優先度だとバリデーションエラーになる | 異常系 |
| 7 | タイトルは255文字まで入力できる | 境界値 |
| 8 | タイトルが256文字以上だとバリデーションエラーになる | 境界値 |
| 9 | ユーザーはタスク編集画面を表示できる | 正常系 |
| 10 | ユーザーはタスクを更新できる | 正常系 |
| 11 | ユーザーはタスクを削除できる | 正常系 |

※ 認可テスト（異常系）はステップ3で追加します。

### テストファイルの作成

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
        $category = Category::factory()->create();

        // Act
        $response = $this->actingAs($user)->post(route('tasks.store'), [
            'title' => 'テストタスク',
            'description' => 'テストの説明',
            'priority' => 2,
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
        $category = Category::factory()->create();

        // Act
        $response = $this->actingAs($user)->post(route('tasks.store'), [
            'title' => '',
            'priority' => 2,
            'category_id' => $category->id,
        ]);

        // Assert
        $response->assertSessionHasErrors('title');
    }

    /** @test */
    public function 無効な優先度だとバリデーションエラーになる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create();

        // Act
        $response = $this->actingAs($user)->post(route('tasks.store'), [
            'title' => 'テストタスク',
            'priority' => 99, // 無効な優先度（1, 2, 3以外）
            'category_id' => $category->id,
        ]);

        // Assert
        $response->assertSessionHasErrors('priority');
    }

    /** @test */
    public function タイトルは255文字まで入力できる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create();

        // Act
        $response = $this->actingAs($user)->post(route('tasks.store'), [
            'title' => str_repeat('あ', 255),
            'priority' => 2,
            'category_id' => $category->id,
        ]);

        // Assert
        $response->assertRedirect(route('tasks.index'));
        $this->assertDatabaseHas('tasks', [
            'title' => str_repeat('あ', 255),
            'user_id' => $user->id,
        ]);
    }

    /** @test */
    public function タイトルが256文字以上だとバリデーションエラーになる(): void
    {
        // Arrange
        $user = User::factory()->create();
        $category = Category::factory()->create();

        // Act
        $response = $this->actingAs($user)->post(route('tasks.store'), [
            'title' => str_repeat('あ', 256),
            'priority' => 2,
            'category_id' => $category->id,
        ]);

        // Assert
        $response->assertSessionHasErrors('title');
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
        $category = Category::factory()->create();

        // Act
        $response = $this->actingAs($user)->put(route('tasks.update', $task), [
            'title' => '更新後のタスク名',
            'priority' => 3,
            'category_id' => $category->id,
        ]);

        // Assert
        $response->assertRedirect(route('tasks.index'));
        $this->assertDatabaseHas('tasks', [
            'id' => $task->id,
            'title' => '更新後のタスク名',
            'priority' => 3,
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

### コードリーディング（AAA形式で解説）

#### `ユーザーはタスク一覧を取得できる`（正常系）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | `$user = User::factory()->create()` | テスト用ユーザーを作成 |
| **Arrange** | `Task::factory()->count(3)->create(['user_id' => $user->id])` | そのユーザーのタスクを3件作成 |
| **Act** | `$this->actingAs($user)->get(route('tasks.index'))` | ログイン状態で一覧ページにアクセス |
| **Assert** | `assertStatus(200)` | 正常にページが表示されることを確認 |
| **Assert** | `assertViewHas('tasks')` | ビューにtasks変数が渡されていることを確認 |

#### `ユーザーはタスクを作成できる`（正常系）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | `$user = User::factory()->create()` | テスト用ユーザーを作成 |
| **Arrange** | `$category = Category::factory()->create()` | タスクに紐づけるカテゴリーを作成 |
| **Act** | `post(route('tasks.store'), ['title' => ..., 'priority' => ..., ...])` | タスク作成リクエストを送信 |
| **Assert** | `assertRedirect(route('tasks.index'))` | 一覧ページにリダイレクトされることを確認 |
| **Assert** | `assertDatabaseHas('tasks', ['title' => ..., 'user_id' => $user->id])` | タスクがDBに保存され、ログインユーザーに紐づいていることを確認 |

#### `無効な優先度だとバリデーションエラーになる`（異常系）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | ユーザーとカテゴリーを作成 | テストの前提条件を準備 |
| **Act** | `post(route('tasks.store'), ['priority' => 99, ...])` | 無効な優先度（1,2,3以外）でリクエスト |
| **Assert** | `assertSessionHasErrors('priority')` | priorityフィールドにバリデーションエラーがあることを確認 |

#### `タイトルは255文字まで入力できる` / `256文字以上だとエラー`（境界値）

| フェーズ | 255文字（成功） | 256文字（失敗） |
|:---|:---|:---|
| **Arrange** | ユーザーとカテゴリーを作成 | ユーザーとカテゴリーを作成 |
| **Act** | `str_repeat('あ', 255)` でPOST | `str_repeat('あ', 256)` でPOST |
| **Assert** | `assertRedirect` + `assertDatabaseHas` | `assertSessionHasErrors('title')` |

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
        $category = Category::factory()->create();

        // Act
        $response = $this->actingAs($user)->put(route('tasks.update', $task), [
            'title' => '不正な更新',
            'priority' => 2,
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

### 認可テスト項目一覧（異常系）

| # | テスト名 | 観点 |
|:--|:---|:---|
| 12 | 他人のタスク詳細にアクセスすると403エラーになる | 異常系（認可） |
| 13 | 他人のタスク編集画面にアクセスすると403エラーになる | 異常系（認可） |
| 14 | 他人のタスクを更新しようとすると403エラーになる | 異常系（認可） |
| 15 | 他人のタスクを削除しようとすると403エラーになる | 異常系（認可） |

### コードリーディング（AAA形式で解説）

#### `他人のタスク詳細にアクセスすると403エラーになる`（異常系：認可）

| フェーズ | コード | 説明 |
|:---|:---|:---|
| **Arrange** | `$user = User::factory()->create()` | ログインするユーザーを作成 |
| **Arrange** | `$otherUser = User::factory()->create()` | 別のユーザーを作成 |
| **Arrange** | `Task::factory()->create(['user_id' => $otherUser->id])` | **別ユーザーの**タスクを作成 |
| **Act** | `$this->actingAs($user)->get(route('tasks.show', $task))` | ログインユーザーが他人のタスクにアクセス |
| **Assert** | `assertForbidden()` | 403エラーになることを確認 |

> **💡 ポイント**: `assertForbidden()` は `assertStatus(403)` と同等です。認可エラー（異常系）を検証する際によく使います。

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
  ✓ カテゴリー名は255文字まで入力できる
  ✓ カテゴリー名が256文字以上だとバリデーションエラーになる
  ✓ ユーザーはカテゴリー編集画面を表示できる
  ✓ ユーザーはカテゴリーを更新できる
  ✓ ユーザーはカテゴリーを削除できる
  ✓ タスクが紐づいているカテゴリーは削除できない

   PASS  Tests\Feature\TaskControllerTest
  ✓ ユーザーはタスク一覧を取得できる
  ...
  ✓ 他人のタスクを削除しようとすると403エラーになる

  Tests:    26 passed
  Duration: 2.50s
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

- [ ] CategoryControllerTestが作成されている（11テスト）
- [ ] TaskControllerTestが作成されている（15テスト）
- [ ] 全てのテストがパスする（合計26テスト）
- [ ] 正常系・異常系・境界値の3観点でテストが書かれている
- [ ] 認可テスト（4アクション分）が含まれている

---

## ✨ まとめ

このセクションでは、CRUD機能のテストを実装しました。

| 学んだこと | 内容 |
|:---|:---|
| テストの3観点 | 正常系・異常系・境界値でテスト項目を洗い出す |
| Featureテスト | HTTPリクエストをシミュレートしてコントローラをテスト |
| actingAs | 特定のユーザーとしてログインした状態でテスト |
| assertDatabaseHas/Missing | データベースの状態を検証 |
| assertSessionHasErrors | バリデーションエラーを検証（異常系） |
| assertForbidden | 403エラーを検証（異常系：認可） |
| 境界値テスト | 上限ギリギリ（成功）と上限超え（失敗）の両方をテスト |

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
- [ ] カテゴリーCRUD（11テスト：正常系7 + 異常系2 + 境界値2）
- [ ] タスクCRUD（11テスト：正常系7 + 異常系2 + 境界値2）
- [ ] 認可テスト（4テスト：異常系）

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
