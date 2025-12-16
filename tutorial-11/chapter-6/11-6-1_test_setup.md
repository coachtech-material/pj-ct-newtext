# Tutorial 11-6-1: テスト環境のセットアップ

## 🎯 このセクションで学ぶこと

*   テストの重要性を理解する。
*   テスト用のデータベースを準備する方法を学ぶ。
*   PHPUnitの基本的な使い方を学ぶ。
*   Laravelのテスト機能を理解する。

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
| 1 | テスト環境の確認 | PHPUnitが動作することを確認 |
| 2 | テスト用データベースの設定 | `.env.testing`を作成 |
| 3 | 最初のテストを実行 | `php artisan test`で動作確認 |

> 💡 **ポイント**: テストは「期待する結果」と「実際の結果」を比較します。

---

## 導入:なぜテストが重要なのか

**テスト**は、**コードが正しく動作することを確認する**ための仕組みです。

テストを書くことで、**バグを早期に発見**でき、**リファクタリングも安心して行える**ようになります。

---

## 詳細解説

### 🔍 テストの種類

Laravelでは、主に以下の2種類のテストを書きます。

*   **ユニットテスト**: 個々のメソッドやクラスをテストする
*   **フィーチャーテスト**: アプリケーション全体の動作をテストする

---

### 🔍 PHPUnitとは

**PHPUnit**は、PHPのテストフレームワークです。

Laravelには、PHPUnitが標準で組み込まれています。

---

### 🔍 テスト環境のセットアップ

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

**ポイント**:
*   `DB_CONNECTION`が`sqlite`になっている
*   `DB_DATABASE`が`:memory:`になっている（メモリ上にデータベースを作成）

---

### 🔍 テスト用のデータベースを準備する

テスト用のデータベースは、**メモリ上に作成**されます。

これにより、**テストが高速に実行**され、**本番データに影響を与えない**ようになります。

---

### 🔍 テストを実行する

テストを実行するには、以下のコマンドを実行します。

```bash
php artisan test
```

または、PHPUnitを直接実行します。

```bash
./vendor/bin/phpunit
```

---

### 🔍 テストの作成

テストを作成するには、以下のコマンドを実行します。

```bash
# フィーチャーテストを作成
php artisan make:test TaskTest

# ユニットテストを作成
php artisan make:test TaskTest --unit
```

**ファイル**: `tests/Feature/TaskTest.php`

```php
<?php

namespace Tests\Feature;

use Tests\TestCase;

class TaskTest extends TestCase
{
    public function test_example()
    {
        $response = $this->get('/');
        $response->assertStatus(200);
    }
}
```

---

### 🔍 テストの基本構造

テストは、以下の構造で書きます。

```php
public function test_タスクを作成できる()
{
    // 準備（Arrange）
    $user = User::factory()->create();
    
    // 実行（Act）
    $response = $this->actingAs($user)->post('/tasks', [
        'title' => 'テストタスク',
        'description' => 'テスト説明',
        'status' => 'pending',
    ]);
    
    // 検証（Assert）
    $response->assertStatus(302);
    $this->assertDatabaseHas('tasks', [
        'title' => 'テストタスク',
    ]);
}
```

**ポイント**:
*   **準備（Arrange）**: テストに必要なデータを準備する
*   **実行（Act）**: テスト対象の処理を実行する
*   **検証（Assert）**: 結果が期待通りかを検証する

---

### 🔍 ファクトリーを使ってテストデータを作成する

**ファクトリー**を使うと、テストデータを簡単に作成できます。

```bash
php artisan make:factory TaskFactory --model=Task
```

**ファイル**: `database/factories/TaskFactory.php`

```php
<?php

namespace Database\Factories;

use App\Models\User;
use Illuminate\Database\Eloquent\Factories\Factory;

class TaskFactory extends Factory
{
    public function definition()
    {
        return [
            'title' => $this->faker->sentence,
            'description' => $this->faker->paragraph,
            'status' => 'pending',
            'priority' => $this->faker->numberBetween(1, 5),
            'user_id' => User::factory(),
        ];
    }
}
```

**使い方**:

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

### 🔍 テストデータベースのマイグレーション

テストを実行する前に、データベースのマイグレーションを実行します。

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

**ポイント**:
*   `RefreshDatabase`トレイトを使うと、テストごとにデータベースがリセットされる

---

### 🔍 実践演習: テストを作成してください

以下のテストを作成してください。

**テスト内容**:
*   ログインしたユーザーが、タスク一覧ページにアクセスできることを確認する

---

**解答例**:

```bash
php artisan make:test TaskTest
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

### 🔍 アサーションメソッド

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

### 🔍 テストの実行を高速化する

テストの実行を高速化するには、並列実行を使います。

```bash
php artisan test --parallel
```

---

### 💡 TIP: テストカバレッジを確認する

テストカバレッジを確認するには、以下のコマンドを実行します。

```bash
./vendor/bin/phpunit --coverage-html coverage
```

`coverage/index.html`をブラウザで開くと、テストカバレッジが表示されます。

---

### 🚨 よくある間違い

#### 間違い1: RefreshDatabaseを使わない

`RefreshDatabase`を使わないと、テストデータが残ってしまいます。

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

#### 間違い2: テストメソッド名がtestで始まっていない

テストメソッド名は、`test`で始める必要があります。

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

#### 間違い3: 本番データベースでテストを実行する

本番データベースでテストを実行すると、データが削除されます。

**対処法**: `phpunit.xml`で、テスト用のデータベースを設定します。

---

## ✨ まとめ

このセクションでは、テスト環境のセットアップを学びました。

*   テストの重要性を理解した。
*   テスト用のデータベースを準備した。
*   PHPUnitの基本的な使い方を学んだ。
*   ファクトリーを使ってテストデータを作成した。

次のセクションでは、CRUD機能のテストを書きます。

---

## 📝 学習のポイント

- [ ] テストの重要性を理解した。
- [ ] テスト用のデータベースを準備した。
- [ ] PHPUnitを使った。
- [ ] ファクトリーを使った。
- [ ] RefreshDatabaseを使った。
