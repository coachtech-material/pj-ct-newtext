# Tutorial 13-6-1: テスト環境のセットアップ

## 🎯 このセクションで学ぶこと

- テストの重要性を理解する
- テスト用のデータベースを準備する方法を学ぶ
- PHPUnitの基本的な使い方を学ぶ
- Laravelのテスト機能を理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜリファクタリングの後に『テスト』を書くのか？」

リファクタリングが終わったら、次は「テスト」です。なぜこのタイミングなのでしょうか？

---

### 理由1: リファクタリングの安全網

テストがあれば、**リファクタリングしても壊れていないことを確認**できます。

今後のリファクタリングに備えて、テストを書いておきます。

---

### 理由2: 機能が安定してから

頻繁に仕様が変わる段階でテストを書くと、**テストの修正が大変**です。

機能が安定してからテストを書く方が効率的です。

---

### 理由3: まずは環境構築から

テストを書く前に、**テスト環境を整える**必要があります。

このセクションでは、PHPUnitの設定とテスト用データベースの準備を行います。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | テストの種類を理解 | ユニットテストとフィーチャーテスト |
| Step 2 | テスト環境を確認 | PHPUnitの設定を確認 |
| Step 3 | テストを作成・実行 | 基本的なテストを書く |
| Step 4 | ファクトリーを使う | テストデータを効率的に作成 |

> 💡 **ポイント**: テストは「期待する結果」と「実際の結果」を比較します。

---

## Step 1: テストの種類を理解する

### 1-1. Laravelのテストの種類

Laravelでは、主に以下の2種類のテストを書きます。

| 種類 | 説明 | 場所 |
|------|------|------|
| ユニットテスト | 個々のメソッドやクラスをテスト | `tests/Unit/` |
| フィーチャーテスト | アプリケーション全体の動作をテスト | `tests/Feature/` |

---

### 1-2. PHPUnitとは

**PHPUnit**は、PHPのテストフレームワークです。

Laravelには、PHPUnitが標準で組み込まれています。

---

## Step 2: テスト環境を確認する

### 2-1. phpunit.xmlの設定

Laravelプロジェクトには、すでにテスト環境が用意されています。

**ファイル**: `phpunit.xml`

```xml
<?xml version="1.0" encoding="UTF-8"?>
<phpunit xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="./vendor/phpunit/phpunit/phpunit.xsd"
         bootstrap="vendor/autoload.php"
         colors="true">
    <testsuites>
        <testsuite name="Unit">
            <directory suffix="Test.php">./tests/Unit</directory>
        </testsuite>
        <testsuite name="Feature">
            <directory suffix="Test.php">./tests/Feature</directory>
        </testsuite>
    </testsuites>
    <php>
        <env name="APP_ENV" value="testing"/>
        <env name="BCRYPT_ROUNDS" value="4"/>
        <env name="CACHE_DRIVER" value="array"/>
        <env name="DB_CONNECTION" value="sqlite"/>
        <env name="DB_DATABASE" value=":memory:"/>
        <env name="MAIL_MAILER" value="array"/>
        <env name="QUEUE_CONNECTION" value="sync"/>
        <env name="SESSION_DRIVER" value="array"/>
    </php>
</phpunit>
```

---

### 2-2. 設定のポイント

| 設定 | 説明 |
|------|------|
| `DB_CONNECTION` | `sqlite`を使用（軽量） |
| `DB_DATABASE` | `:memory:`でメモリ上にDB作成 |
| `BCRYPT_ROUNDS` | `4`で高速化 |

---

### 2-3. RefreshDatabaseトレイトを使う

**ファイル**: `tests/TestCase.php`

```php
<?php

namespace Tests;

use Illuminate\Foundation\Testing\TestCase as BaseTestCase;
use Illuminate\Foundation\Testing\RefreshDatabase;

abstract class TestCase extends BaseTestCase
{
    use CreatesApplication, RefreshDatabase;
}
```

**ポイント**: `RefreshDatabase`トレイトを使うと、テストごとにデータベースがリセットされます。

---

## Step 3: テストを作成・実行する

### 3-1. テストを作成する

```bash
# フィーチャーテストを作成
sail artisan make:test TaskTest

# ユニットテストを作成
sail artisan make:test TaskTest --unit
```

---

### 3-2. テストの基本構造

**ファイル**: `tests/Feature/TaskTest.php`

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Tests\TestCase;

class TaskTest extends TestCase
{
    public function test_ログインしたユーザーがタスク一覧ページにアクセスできる()
    {
        // 準備（Arrange）
        $user = User::factory()->create();
        
        // 実行（Act）
        $response = $this->actingAs($user)->get('/tasks');
        
        // 検証（Assert）
        $response->assertStatus(200);
    }
}
```

---

### 3-3. AAAパターン

テストは、**AAAパターン**で書きます。

| パターン | 説明 |
|----------|------|
| Arrange（準備） | テストに必要なデータを準備する |
| Act（実行） | テスト対象の処理を実行する |
| Assert（検証） | 結果が期待通りかを検証する |

---

### 3-4. テストを実行する

```bash
# Laravelのテストコマンド
sail artisan test

# PHPUnitを直接実行
./vendor/bin/phpunit

# 並列実行で高速化
sail artisan test --parallel
```

---

## Step 4: ファクトリーを使ってテストデータを作成する

### 4-1. ファクトリーを作成する

```bash
sail artisan make:factory TaskFactory --model=Task
```

---

### 4-2. ファクトリーを定義する

**ファイル**: `database/factories/TaskFactory.php`

```php
<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class TaskFactory extends Factory
{
    public function definition(): array
    {
        return [
            'title' => fake()->sentence,
            'description' => fake()->paragraph,
            'status' => 'pending',
            'priority' => fake()->numberBetween(1, 5),
            'user_id' => User::factory(),
        ];
    }
}
```

---

### 4-3. ファクトリーを使う

```php
// 1つのタスクを作成
$task = Task::factory()->create();

// 10個のタスクを作成
$tasks = Task::factory()->count(10)->create();

// 特定の値を指定してタスクを作成
$task = Task::factory()->create([
    'title' => 'テストタスク',
]);
```

---

### 4-4. アサーションメソッド

Laravelには、便利なアサーションメソッドが用意されています。

```php
// ステータスコードを検証
$response->assertStatus(200);

// リダイレクトを検証
$response->assertRedirect('/tasks');

// データベースにデータがあることを検証
$this->assertDatabaseHas('tasks', ['title' => 'テストタスク']);

// データベースにデータがないことを検証
$this->assertDatabaseMissing('tasks', ['title' => '削除されたタスク']);

// ビューに変数が渡されていることを検証
$response->assertViewHas('tasks');

// ビューが表示されていることを検証
$response->assertViewIs('tasks.index');
```

---

### 4-5. 実践演習

以下のテストを作成してください。

**テスト内容**: ログインしたユーザーが、タスク一覧ページにアクセスできることを確認する

**解答例**:

```bash
sail artisan make:test TaskTest
```

**ファイル**: `tests/Feature/TaskTest.php`

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Tests\TestCase;

class TaskTest extends TestCase
{
    public function test_ログインしたユーザーがタスク一覧ページにアクセスできる()
    {
        // 準備
        $user = User::factory()->create();
        
        // 実行
        $response = $this->actingAs($user)->get('/tasks');
        
        // 検証
        $response->assertStatus(200);
    }
}
```

---

## 🚨 よくある間違い

### 間違い1: RefreshDatabaseを使わない

**問題**: テストデータが残ってしまい、テストが不安定になる

```php
// ❌ 間違い
class TaskTest extends TestCase
{
    // RefreshDatabaseを使っていない
}

// ✅ 正しい
class TaskTest extends TestCase
{
    use RefreshDatabase;
}
```

---

### 間違い2: テストメソッド名がtestで始まっていない

**問題**: テストが実行されない

```php
// ❌ 間違い
public function タスクを作成できる()
{
    // ...
}

// ✅ 正しい
public function test_タスクを作成できる()
{
    // ...
}
```

---

### 間違い3: 本番データベースでテストを実行する

**問題**: 本番データが削除される

**対処法**: `phpunit.xml`で、テスト用のデータベースを設定します。

---

## 💡 TIP: テストカバレッジを確認する

テストカバレッジを確認するには、以下のコマンドを実行します。

```bash
./vendor/bin/phpunit --coverage-html coverage
```

`coverage/index.html`をブラウザで開くと、テストカバレッジが表示されます。

---

## ✨ まとめ

このセクションでは、テスト環境のセットアップを学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | テストの種類（ユニット・フィーチャー） |
| Step 2 | テスト環境の確認（phpunit.xml） |
| Step 3 | テストの作成と実行（AAAパターン） |
| Step 4 | ファクトリーとアサーション |

次のセクションでは、CRUD機能のテストを書きます。

---
