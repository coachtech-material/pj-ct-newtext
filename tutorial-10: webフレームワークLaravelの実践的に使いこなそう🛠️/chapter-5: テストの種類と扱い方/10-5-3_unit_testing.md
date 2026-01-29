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

**コードリーディング（User.php）**：

| コード | 説明 |
|:---|:---|
| `public function formatName($name)` | 文字列を受け取って加工する、テスト対象となるメソッドです |
| `return $name . '様';` | 受け取った名前の末尾に「様」を連結して返します |

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
        // 1. 準備：モデルのインスタンスを作る
        $user = new User();

        // 2. 実行：メソッドを呼び出す
        $result = $user->formatName('田中');

        // 3. 検証：結果が「田中様」になっているか確認
        $this->assertEquals('田中様', $result);
    }
}
```

**コードリーディング（UserTest.php）**：

| コード | 説明 |
|:---|:---|
| `use PHPUnit\Framework\TestCase;` | 単体テスト（Unitテスト）の基本機能を備えたクラスを読み込みます |
| `class UserTest extends TestCase` | テスト用クラスです。TestCaseを継承することで、検証用のメソッドが使えます |
| `test_...`（メソッド名） | PHPUnitのルールで、メソッド名の先頭は必ず `test_` にします |
| `$user = new User();` | テストしたい機能を持つオブジェクトを新しく用意します |
| `$user->formatName('田中')` | 実際にテストしたい処理を実行し、結果を `$result` に入れます |
| `$this->assertEquals('田中様', $result)` | 「田中様」という期待通りの結果が返ってきたかを厳密にチェックします |

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
