# Tutorial 9-6-3: カスタムバリデーション

## 🎯 このセクションで学ぶこと

*   独自のバリデーションルールを作成する方法を理解する。
*   クロージャを使った簡易的なカスタムバリデーションの実装方法を理解する。
*   `Rule`クラスを使った再利用可能なカスタムバリデーションの実装方法を理解する。

---

## 導入：「標準ルール」では足りない時

Laravelには、多くのバリデーションルールが用意されていますが、**アプリケーション固有のルール**が必要になることがあります。

例えば、以下のような状況を考えてみましょう。

*   **禁止ワードを含まないかチェックしたい**
*   **特定の曜日のみ予約を受け付けたい**
*   **複数のフィールドの組み合わせをチェックしたい**

このセクションでは、独自のバリデーションルールを作成する方法を学びます。

---

## 詳細解説

### 🔧 方法1: クロージャを使ったカスタムバリデーション

最も簡単な方法は、**クロージャ**を使う方法です。

**基本的な使い方**

```php
use Illuminate\Validation\Rule;

$request->validate([
    'username' => [
        'required',
        'string',
        function ($attribute, $value, $fail) {
            if (strtolower($value) === 'admin') {
                $fail('The ' . $attribute . ' cannot be "admin".');
            }
        },
    ],
]);
```

**パラメータ**

*   `$attribute`: フィールド名（`username`）
*   `$value`: 入力値
*   `$fail`: エラーメッセージを設定するクロージャ

---

### 🚀 実践例1: 禁止ワードチェック

コメント投稿時に禁止ワードが含まれていないかをチェックする実装例です。

```php
$request->validate([
    'comment' => [
        'required',
        'string',
        function ($attribute, $value, $fail) {
            $forbiddenWords = ['spam', 'abuse', 'badword'];
            
            foreach ($forbiddenWords as $word) {
                if (stripos($value, $word) !== false) {
                    $fail('The ' . $attribute . ' contains forbidden words.');
                    return;
                }
            }
        },
    ],
]);
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `'comment' => [...]` | 配列形式でルールを指定します。クロージャを含める場合は配列形式が必須です |
| `'required', 'string'` | 必須かつ文字列型であることをチェックします |
| `function ($attribute, $value, $fail)` | カスタムバリデーションのクロージャを定義します |
| `$forbiddenWords = [...]` | 禁止ワードの配列を定義します |
| `stripos($value, $word)` | 大文字小文字を区別せずに、`$value`内に`$word`が含まれるかをチェックします |
| `$fail('...')` | バリデーションを失敗させ、エラーメッセージを設定します |
| `return;` | 最初の禁止ワードが見つかった時点で処理を終了します |

**構文解説**：

```php
function ($attribute, $value, $fail) {
    // バリデーションロジック
}
```
→ クロージャ（無名関数）を使ったカスタムバリデーションです。3つのパラメータを受け取ります。

```php
if (stripos($value, $word) !== false) {
```
→ `stripos()`は文字列内で別の文字列が最初に現れる位置を返します。見つからない場合は`false`を返すため、`!== false`で「見つかった」ことを判定します。`!= false`ではなく`!== false`を使うのは、位置が0の場合（先頭で見つかった場合）を正しく判定するためです。

**処理の流れ**：

```
1. 禁止ワードの配列を定義
    ↓
2. 各禁止ワードについてループ
    ↓
3. stripos()で入力値に禁止ワードが含まれるかチェック
   - 含まれる場合: $fail()でエラーメッセージを設定し、returnで終了
   - 含まれない場合: 次の禁止ワードをチェック
    ↓
4. すべての禁止ワードをチェックしても見つからなければ、バリデーション成功
```

---

### 🔧 方法2: カスタムルールクラスを作成

再利用可能なカスタムバリデーションルールを作成するには、**Ruleクラス**を使います。

**Ruleクラスの生成**

```bash
sail artisan make:rule Uppercase
```

**`app/Rules/Uppercase.php`**

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\Rule;

class Uppercase implements Rule
{
    public function passes($attribute, $value)
    {
        return strtoupper($value) === $value;
    }

    public function message()
    {
        return 'The :attribute must be uppercase.';
    }
}
```

**メソッド**

*   `passes()`: バリデーションが成功する条件を返す
*   `message()`: エラーメッセージを返す

---

**Ruleクラスの使用**

```php
use App\Rules\Uppercase;

$request->validate([
    'code' => ['required', 'string', new Uppercase],
]);
```

---

### 🚀 実践例3: 禁止ワードルール

クロージャで実装した禁止ワードチェックを、再利用可能なRuleクラスとして実装する例です。

**Ruleクラスの生成**

```bash
sail artisan make:rule NoForbiddenWords
```

**`app/Rules/NoForbiddenWords.php`**

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\Rule;

class NoForbiddenWords implements Rule
{
    protected $forbiddenWords = ['spam', 'abuse', 'badword'];

    public function passes($attribute, $value)
    {
        foreach ($this->forbiddenWords as $word) {
            if (stripos($value, $word) !== false) {
                return false;
            }
        }
        
        return true;
    }

    public function message()
    {
        return 'The :attribute contains forbidden words.';
    }
}
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `class NoForbiddenWords implements Rule` | `Rule`インターフェースを実装したカスタムルールクラスです |
| `protected $forbiddenWords = [...]` | クラスプロパティとして禁止ワードを定義します |
| `public function passes($attribute, $value)` | バリデーションロジックを実装します。`true`で成功、`false`で失敗 |
| `$this->forbiddenWords` | クラスプロパティにアクセスします |
| `return false;` | 禁止ワードが見つかった場合、バリデーション失敗を返します |
| `return true;` | すべてのチェックを通過した場合、バリデーション成功を返します |
| `public function message()` | エラーメッセージを返します。`:attribute`はフィールド名に置換されます |

**構文解説**：

```php
class NoForbiddenWords implements Rule
```
→ `implements Rule`で`Illuminate\Contracts\Validation\Rule`インターフェースを実装します。このインターフェースは`passes()`と`message()`メソッドの実装を要求します。

```php
protected $forbiddenWords = ['spam', 'abuse', 'badword'];
```
→ クラスプロパティとして禁止ワードを定義することで、コンストラクタで外部から渡すこともできるように拡張可能です。

```php
return 'The :attribute contains forbidden words.';
```
→ `:attribute`はLaravelが自動的にフィールド名に置換するプレースホルダーです。

**Ruleクラスの使用**

```php
use App\Rules\NoForbiddenWords;

$request->validate([
    'comment' => ['required', 'string', new NoForbiddenWords],
]);
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `use App\Rules\NoForbiddenWords;` | カスタムルールクラスをインポートします |
| `new NoForbiddenWords` | ルールクラスのインスタンスを作成し、バリデーションルールとして使用します |

**クロージャとRuleクラスの使い分け**：

| 方法 | メリット | デメリット | 使用場面 |
|:---|:---|:---|:---|
| クロージャ | 手軽に実装できる | 再利用しにくい | 1箇所でのみ使用する場合 |
| Ruleクラス | 再利用可能、テストしやすい | ファイルを作成する手間がある | 複数箇所で使用する場合 |

---

### 💡 TIP: `Validator::extend()`を使った登録

カスタムルールを**グローバルに登録**することもできます。

**`app/Providers/AppServiceProvider.php`**

```php
use Illuminate\Support\Facades\Validator;

public function boot()
{
    Validator::extend('uppercase', function ($attribute, $value, $parameters, $validator) {
        return strtoupper($value) === $value;
    });

    Validator::replacer('uppercase', function ($message, $attribute, $rule, $parameters) {
        return str_replace(':attribute', $attribute, 'The :attribute must be uppercase.');
    });
}
```

**使用例**

```php
$request->validate([
    'code' => 'required|string|uppercase',
]);
```

---

### 🚨 よくある間違い

**間違い1: `passes()`で例外を投げる**

```php
public function passes($attribute, $value)
{
    if (strtoupper($value) !== $value) {
        throw new \Exception('Invalid value'); // NG
    }
    
    return true;
}
```

**対処法**: `passes()`は、`true`または`false`を返します。

```php
public function passes($attribute, $value)
{
    return strtoupper($value) === $value; // OK
}
```

---

**間違い2: `message()`で動的なメッセージを返そうとする**

```php
public function message()
{
    return 'The value is ' . $this->value; // $this->valueは存在しない
}
```

**対処法**: コンストラクタで値を保存します。

```php
protected $value;

public function __construct($value)
{
    $this->value = $value;
}

public function message()
{
    return 'The value is ' . $this->value;
}
```

---

## ✨ まとめ

このセクションでは、独自のバリデーションルールを作成する方法を学びました。

*   クロージャを使って、簡易的なカスタムバリデーションを実装できる。
*   `Rule`クラスを使って、再利用可能なカスタムバリデーションを実装できる。
*   クロージャは1箇所でのみ使用する場合、Ruleクラスは複数箇所で再利用する場合に適している。

---
