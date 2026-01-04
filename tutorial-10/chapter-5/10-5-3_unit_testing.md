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

### 🚀 実践例1: 基本的なアサーション

```php
public function test_basic_assertions()
{
    $this->assertTrue(true);
    $this->assertFalse(false);
    $this->assertEquals(5, 5);
    $this->assertNotEquals(5, 10);
    $this->assertNull(null);
    $this->assertNotNull('value');
    $this->assertEmpty([]);
    $this->assertNotEmpty([1, 2, 3]);
}
```

---

### 🚀 実践例2: 配列のアサーション

```php
public function test_array_assertions()
{
    $array = [1, 2, 3, 4, 5];

    $this->assertCount(5, $array);
    $this->assertContains(3, $array);
    $this->assertNotContains(10, $array);
}
```

---

### 🚀 実践例3: 文字列のアサーション

```php
public function test_string_assertions()
{
    $string = 'Hello, Laravel!';

    $this->assertStringContainsString('Laravel', $string);
    $this->assertStringStartsWith('Hello', $string);
    $this->assertStringEndsWith('!', $string);
}
```

---

### 🚀 実践例4: クラスのメソッドをテスト

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

---

### 💡 TIP: `setUp()`と`tearDown()`

*   `setUp()`: 各テストの前に実行される
*   `tearDown()`: 各テストの後に実行される

---

### 🚀 実践例5: データプロバイダー

```php
/**
 * @dataProvider additionProvider
 */
public function test_add_with_data_provider($a, $b, $expected)
{
    $result = $this->calculator->add($a, $b);
    $this->assertEquals($expected, $result);
}

public function additionProvider()
{
    return [
        [2, 3, 5],
        [10, 5, 15],
        [-5, 5, 0],
        [0, 0, 0],
    ];
}
```

---

### 🚀 実践例6: 例外のテスト

```php
public function test_divide_by_zero_throws_exception()
{
    $this->expectException(\InvalidArgumentException::class);
    $this->expectExceptionMessage('Division by zero');

    $this->calculator->divide(10, 0);
}
```

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

#### 間違い1: テストメソッド名が`test`で始まっていない

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

#### 間違い2: アサーションがない

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
*   データプロバイダーを使って、複数のテストケースを効率的に実行できる。

次のセクションでは、機能テストの基礎を学びます。

---
