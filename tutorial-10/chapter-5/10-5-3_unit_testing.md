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

このセクションでは、単体テストの基礎を学びます。

---

## 詳細解説

### 🔧 ステップ1: テストファイルを作成

```bash
sail artisan make:test CalculatorTest --unit
```

**`tests/Unit/CalculatorTest.php`**

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

---

### 🚀 実践例1: クラスのメソッドをテスト

サービスクラスを作成し、そのメソッドをテストする例です。

**`app/Services/Calculator.php`**

```php
<?php

namespace App\Services;

class Calculator
{
    public function add($a, $b)
    {
        return $a + $b;
    }

    public function subtract($a, $b)
    {
        return $a - $b;
    }

    public function multiply($a, $b)
    {
        return $a * $b;
    }

    public function divide($a, $b)
    {
        if ($b === 0) {
            throw new \InvalidArgumentException('Division by zero');
        }

        return $a / $b;
    }
}
```

**コードリーディング（Calculator.php）**

| コード | 説明 |
|:---|:---|
| `namespace App\Services;` | サービスクラスを`App\Services`名前空間に配置します |
| `public function add($a, $b)` | 2つの引数を受け取り、加算結果を返すメソッドです |
| `public function divide($a, $b)` | 除算を行うメソッドです。ゼロ除算の場合は例外をスローします |
| `if ($b === 0)` | 除数が0かどうかをチェックします |
| `throw new \InvalidArgumentException('Division by zero');` | ゼロ除算の場合、`InvalidArgumentException`例外をスローします |

**`tests/Unit/CalculatorTest.php`**

```php
<?php

namespace Tests\Unit;

use App\Services\Calculator;
use PHPUnit\Framework\TestCase;

class CalculatorTest extends TestCase
{
    protected $calculator;

    protected function setUp(): void
    {
        parent::setUp();
        $this->calculator = new Calculator();
    }

    public function test_add()
    {
        $result = $this->calculator->add(2, 3);
        $this->assertEquals(5, $result);
    }

    public function test_subtract()
    {
        $result = $this->calculator->subtract(10, 3);
        $this->assertEquals(7, $result);
    }

    public function test_multiply()
    {
        $result = $this->calculator->multiply(4, 5);
        $this->assertEquals(20, $result);
    }

    public function test_divide()
    {
        $result = $this->calculator->divide(10, 2);
        $this->assertEquals(5, $result);
    }

    public function test_divide_by_zero_throws_exception()
    {
        $this->expectException(\InvalidArgumentException::class);
        $this->calculator->divide(10, 0);
    }
}
```

**コードリーディング（CalculatorTest.php）**

| コード | 説明 |
|:---|:---|
| `use App\Services\Calculator;` | テスト対象のCalculatorクラスをインポートします |
| `use PHPUnit\Framework\TestCase;` | PHPUnitのTestCaseクラスをインポートします。単体テストはこのクラスを継承します |
| `protected $calculator;` | テスト全体で使用するCalculatorインスタンスを保持するプロパティです |
| `protected function setUp(): void` | 各テストメソッドの実行前に呼び出されるセットアップメソッドです |
| `parent::setUp();` | 親クラスのsetUp()を呼び出します。必ず最初に実行します |
| `$this->calculator = new Calculator();` | Calculatorのインスタンスを作成し、プロパティに保存します |
| `public function test_add()` | テストメソッドです。メソッド名は`test_`で始める必要があります |
| `$this->assertEquals(5, $result);` | 期待値（5）と実際の値（$result）が等しいことを検証します |
| `$this->expectException(\InvalidArgumentException::class);` | 次の処理で指定した例外がスローされることを期待します |
| `$this->calculator->divide(10, 0);` | ゼロ除算を実行し、例外がスローされることを確認します |

---

### 💡 TIP: `setUp()`と`tearDown()`

*   `setUp()`: 各テストの前に実行される
*   `tearDown()`: 各テストの後に実行される

---

### 💡 TIP: よく使うアサーションメソッド

| メソッド | 説明 |
|----------|------|
| `assertTrue($condition)` | `$condition`が`true`であることを検証 |
| `assertFalse($condition)` | `$condition`が`false`であることを検証 |
| `assertEquals($expected, $actual)` | `$expected`と`$actual`が等しいことを検証 |
| `assertNotEquals($expected, $actual)` | `$expected`と`$actual`が等しくないことを検証 |
| `assertNull($value)` | `$value`が`null`であることを検証 |
| `assertNotNull($value)` | `$value`が`null`でないことを検証 |
| `assertCount($count, $array)` | 配列の要素数を検証 |
| `assertContains($needle, $haystack)` | 配列に要素が含まれることを検証 |

---

### 🚨 よくある間違い

**間違い1: テストメソッド名が`test`で始まっていない**

```php
// NG
public function addition_test()
{
    // ...
}

// OK
public function test_addition()
{
    // ...
}
```

---

**間違い2: アサーションがない**

```php
// NG
public function test_add()
{
    $result = $this->calculator->add(2, 3);
    // アサーションがない
}

// OK
public function test_add()
{
    $result = $this->calculator->add(2, 3);
    $this->assertEquals(5, $result); // アサーションを追加
}
```

---

## ✨ まとめ

このセクションでは、単体テストの基礎を学びました。

*   単体テストは、個々の関数やメソッドが正しく動作するかを検証する。
*   `sail artisan test`でテストを実行できる。
*   アサーションメソッドを使って、期待値と実際の値を比較する。
*   `setUp()`メソッドを使って、テストの前準備を行う。

次のセクションでは、機能テストの基礎を学びます。

---
