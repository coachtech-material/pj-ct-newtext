# Tutorial 10-5-3: 単体テストの基礎

## 🎯 このセクションで学ぶこと

*   単体テストを書き、関数やメソッドの動作を検証できるようになる。
*   PHPUnitの基本的な使い方を理解する。
*   アサーションメソッドを使い分けられるようになる。

---

## 導入：「単体テスト」とは何か？

**単体テスト（Unit Test）**とは、**個々の関数やメソッドが正しく動作するかを検証するテスト**です。

例えば、以下のような関数があるとします。

```php
function add($a, $b)
{
    return $a + $b;
}
```

この関数が正しく動作するかを確認するために、単体テストを書きます。

```php
public function test_add_function()
{
    $result = add(2, 3);
    $this->assertEquals(5, $result);
}
```

**単体テストの特徴**

| 特徴 | 説明 |
|:---|:---|
| テスト対象 | 1つの関数やメソッド |
| 実行速度 | 非常に高速（データベースやHTTPを使わない） |
| 目的 | ロジックが正しいかを検証 |
| 依存関係 | 他のクラスやデータベースに依存しない |

このセクションでは、単体テストの基礎を学びます。

---

## 詳細解説

### 🔍 単体テストの基本的な使い方

単体テストは、以下の3つのステップで構成されます。

1. **準備（Arrange）**: テストに必要なオブジェクトやデータを用意する
2. **実行（Act）**: テスト対象のメソッドを呼び出す
3. **検証（Assert）**: 結果が期待通りかを確認する

この3ステップは「**AAAパターン**」と呼ばれ、テストを書く際の基本的な構造です。

---

### 🔧 ステップ1: テストファイルを作成

```bash
sail artisan make:test CalculatorTest --unit
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `sail artisan make:test` | テストファイルを生成するArtisanコマンドです |
| `CalculatorTest` | 作成するテストクラスの名前です。慣習として`〇〇Test`という名前にします |
| `--unit` | 単体テストとして作成するオプションです。`tests/Unit/`ディレクトリに作成されます |

> **💡 ポイント**: `--unit`オプションを付けないと、`tests/Feature/`ディレクトリに作成されます（機能テスト用）。

**生成されるファイル: `tests/Unit/CalculatorTest.php`**

```php
<?php

namespace Tests\Unit;

use PHPUnit\Framework\TestCase;

class CalculatorTest extends TestCase
{
    public function test_add_function()
    {
        $result = 2 + 3;
        $this->assertEquals(5, $result);
    }
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `namespace Tests\Unit;` | このクラスが`Tests\Unit`名前空間に属することを宣言します |
| `use PHPUnit\Framework\TestCase;` | PHPUnitのテストケースクラスをインポートします |
| `class CalculatorTest extends TestCase` | `TestCase`を継承することで、アサーションメソッドが使えるようになります |
| `public function test_add_function()` | テストメソッドです。メソッド名は必ず`test_`で始めます |
| `$this->assertEquals(5, $result)` | 期待値`5`と実際の値`$result`が等しいかを検証します |

**構文解説: テストメソッドの命名規則**

```
test_テスト内容を説明する名前
```

*   メソッド名は必ず`test_`で始める（PHPUnitのルール）
*   スネークケース（`_`区切り）で、テスト内容を説明する名前にする
*   例: `test_add_returns_sum_of_two_numbers`

---

### 🔧 ステップ2: テストを実行

```bash
sail artisan test
```

**実行結果**

```
PASS  Tests\Unit\CalculatorTest
✓ add function

Tests:  1 passed
Time:   0.10s
```

**コードリーディング（実行結果）**

| 出力 | 説明 |
|:---|:---|
| `PASS` | テストが成功したことを示します |
| `Tests\Unit\CalculatorTest` | 実行されたテストクラスの名前です |
| `✓ add function` | 成功したテストメソッドの名前です（`test_`が省略されて表示されます） |
| `Tests: 1 passed` | 1件のテストが成功したことを示します |
| `Time: 0.10s` | テストの実行時間です |

**テスト実行コマンドのオプション**

| コマンド | 説明 |
|:---|:---|
| `sail artisan test` | 全てのテストを実行 |
| `sail artisan test --filter=CalculatorTest` | 特定のテストクラスのみ実行 |
| `sail artisan test --filter=test_add_function` | 特定のテストメソッドのみ実行 |
| `sail artisan test --testsuite=Unit` | 単体テストのみ実行 |

---

### 🚀 実践例1: ユニットテストの基本

モデルに定義した「文字を変換するメソッド」が正しく動くかをテストする、最もシンプルな例です。

**app/Models/User.php**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    /**
     * 名前の先頭に「様」をつけて返す
     */
    public function formatName($name)
    {
        return $name . '様';
    }
}
```

**コードリーディング（User.php）**

| コード | 説明 |
|:---|:---|
| `public function formatName($name)` | 文字列を受け取って加工する、テスト対象となるメソッドです |
| `return $name . '様';` | 受け取った名前の末尾に「様」を連結して返します。`.`は文字列連結演算子です |

**tests/Unit/UserTest.php**

```php
<?php

namespace Tests\Unit;

use App\Models\User;
use PHPUnit\Framework\TestCase;

class UserTest extends TestCase
{
    /**
     * 名前のフォーマットが正しいかテスト
     */
    public function test_format_name_adds_honorific()
    {
        // 1. 準備（Arrange）：モデルのインスタンスを作る
        $user = new User();

        // 2. 実行（Act）：メソッドを呼び出す
        $result = $user->formatName('田中');

        // 3. 検証（Assert）：結果が「田中様」になっているか確認
        $this->assertEquals('田中様', $result);
    }
}
```

**コードリーディング（UserTest.php）**

| コード | 説明 |
|:---|:---|
| `use App\Models\User;` | テスト対象のUserモデルをインポートします |
| `use PHPUnit\Framework\TestCase;` | 単体テストの基本機能を備えたクラスを読み込みます |
| `class UserTest extends TestCase` | テスト用クラスです。TestCaseを継承することで、検証用のメソッドが使えます |
| `test_format_name_adds_honorific` | テストメソッド名。「formatNameメソッドが敬称を追加する」ことをテストしていることが分かります |
| `$user = new User();` | テストしたい機能を持つオブジェクトを新しく用意します（準備） |
| `$user->formatName('田中')` | 実際にテストしたい処理を実行し、結果を`$result`に入れます（実行） |
| `$this->assertEquals('田中様', $result)` | 「田中様」という期待通りの結果が返ってきたかを厳密にチェックします（検証） |

**構文解説: assertEquals()**

```php
$this->assertEquals(期待値, 実際の値);
```

*   **第1引数**: 期待する値（テストが成功するべき値）
*   **第2引数**: 実際にメソッドから返された値
*   2つの値が等しければテスト成功、異なればテスト失敗

---

### 💡 TIP: `setUp()`と`tearDown()`

テストの前後に共通の処理を行いたい場合、`setUp()`と`tearDown()`メソッドを使います。

```php
class UserTest extends TestCase
{
    private $user;

    protected function setUp(): void
    {
        parent::setUp();
        // 各テストの前に実行される
        $this->user = new User();
    }

    protected function tearDown(): void
    {
        // 各テストの後に実行される
        $this->user = null;
        parent::tearDown();
    }

    public function test_format_name()
    {
        // $this->userが使える
        $result = $this->user->formatName('田中');
        $this->assertEquals('田中様', $result);
    }
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `protected function setUp(): void` | 各テストメソッドの**前**に自動的に実行されるメソッドです |
| `parent::setUp();` | 親クラスの`setUp()`を呼び出します。必ず最初に呼び出します |
| `$this->user = new User();` | テストで使うオブジェクトをプロパティに保存します |
| `protected function tearDown(): void` | 各テストメソッドの**後**に自動的に実行されるメソッドです |
| `parent::tearDown();` | 親クラスの`tearDown()`を呼び出します。必ず最後に呼び出します |

**使い分け**

| メソッド | 実行タイミング | 用途 |
|:---|:---|:---|
| `setUp()` | 各テストの前 | テストに必要なオブジェクトの準備 |
| `tearDown()` | 各テストの後 | リソースの解放、後片付け |

---

### 💡 TIP: よく使うアサーションメソッド

| メソッド | 説明 | 使用例 |
|:---|:---|:---|
| `assertTrue($condition)` | `$condition`が`true`であることを検証 | `$this->assertTrue($user->isActive())` |
| `assertFalse($condition)` | `$condition`が`false`であることを検証 | `$this->assertFalse($user->isDeleted())` |
| `assertEquals($expected, $actual)` | 2つの値が等しいことを検証 | `$this->assertEquals(5, $result)` |
| `assertNotEquals($expected, $actual)` | 2つの値が等しくないことを検証 | `$this->assertNotEquals(0, $count)` |
| `assertNull($value)` | 値が`null`であることを検証 | `$this->assertNull($user->deletedAt)` |
| `assertNotNull($value)` | 値が`null`でないことを検証 | `$this->assertNotNull($user->id)` |
| `assertCount($count, $array)` | 配列の要素数を検証 | `$this->assertCount(3, $items)` |
| `assertContains($needle, $haystack)` | 配列に要素が含まれることを検証 | `$this->assertContains('apple', $fruits)` |
| `assertSame($expected, $actual)` | 型も含めて完全に等しいことを検証 | `$this->assertSame(5, $result)` |
| `assertInstanceOf($class, $object)` | オブジェクトが特定のクラスのインスタンスであることを検証 | `$this->assertInstanceOf(User::class, $user)` |

**`assertEquals`と`assertSame`の違い**

```php
$this->assertEquals('5', 5);  // OK（値が等しい）
$this->assertSame('5', 5);    // NG（型が異なる: stringとint）
```

---

### 🚨 よくある間違い

**間違い1: テストメソッド名が`test`で始まっていない**

```php
// NG: テストとして認識されない
public function addition_test()
{
    // ...
}

// OK: test_で始める
public function test_addition()
{
    // ...
}
```

**対処法**: メソッド名は必ず`test_`で始めます。

---

**間違い2: アサーションがない**

```php
// NG: アサーションがないため、何も検証されない
public function test_add()
{
    $result = $this->calculator->add(2, 3);
    // アサーションがない
}

// OK: アサーションを追加
public function test_add()
{
    $result = $this->calculator->add(2, 3);
    $this->assertEquals(5, $result);
}
```

**対処法**: 必ず1つ以上のアサーションを含めます。

---

**間違い3: 期待値と実際の値の順序を間違える**

```php
// NG: 順序が逆
$this->assertEquals($result, 5);

// OK: 期待値が第1引数、実際の値が第2引数
$this->assertEquals(5, $result);
```

**対処法**: `assertEquals(期待値, 実際の値)`の順序を守ります。テスト失敗時のエラーメッセージが正しく表示されます。

---

## ✨ まとめ

このセクションでは、単体テストの基礎を学びました。

*   単体テストは、個々の関数やメソッドが正しく動作するかを検証する。
*   テストは「準備（Arrange）→ 実行（Act）→ 検証（Assert）」の3ステップで構成される。
*   `sail artisan make:test クラス名 --unit`でテストファイルを作成できる。
*   `sail artisan test`でテストを実行できる。
*   アサーションメソッドを使って、期待値と実際の値を比較する。
*   `setUp()`メソッドを使って、テストの前準備を行う。

次のセクションでは、機能テストの基礎を学びます。

---
