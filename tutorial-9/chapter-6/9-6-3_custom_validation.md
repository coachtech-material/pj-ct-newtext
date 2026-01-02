# Tutorial 9-6-3: カスタムバリデーション

## 🎯 このセクションで学ぶこと

*   独自のバリデーションルールを作成できるようになる。
*   クロージャを使った簡易的なカスタムバリデーションを実装できるようになる。
*   `Rule`クラスを使った再利用可能なカスタムバリデーションを実装できるようになる。

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

#### 基本的な使い方

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

---

### 🚀 実践例2: 営業時間チェック

```php
$request->validate([
    'reservation_time' => [
        'required',
        'date',
        function ($attribute, $value, $fail) {
            $hour = (int) date('H', strtotime($value));
            
            if ($hour < 9 || $hour >= 18) {
                $fail('Reservations are only available between 9:00 and 18:00.');
            }
        },
    ],
]);
```

---

### 🔧 方法2: カスタムルールクラスを作成

再利用可能なカスタムバリデーションルールを作成するには、**Ruleクラス**を使います。

#### ステップ1: Ruleクラスを生成

```bash
php artisan make:rule Uppercase
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

#### ステップ2: Ruleクラスを使う

```php
use App\Rules\Uppercase;

$request->validate([
    'code' => ['required', 'string', new Uppercase],
]);
```

---

### 🚀 実践例3: 禁止ワードルール

#### ステップ1: Ruleクラスを生成

```bash
php artisan make:rule NoForbiddenWords
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

#### ステップ2: Ruleクラスを使う

```php
use App\Rules\NoForbiddenWords;

$request->validate([
    'comment' => ['required', 'string', new NoForbiddenWords],
]);
```

---

### 🚀 実践例4: パラメータを受け取るルール

#### ステップ1: Ruleクラスを生成

```bash
php artisan make:rule MinWords
```

**`app/Rules/MinWords.php`**

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\Rule;

class MinWords implements Rule
{
    protected $minWords;

    public function __construct($minWords)
    {
        $this->minWords = $minWords;
    }

    public function passes($attribute, $value)
    {
        $wordCount = str_word_count($value);
        return $wordCount >= $this->minWords;
    }

    public function message()
    {
        return 'The :attribute must contain at least ' . $this->minWords . ' words.';
    }
}
```

#### ステップ2: Ruleクラスを使う

```php
use App\Rules\MinWords;

$request->validate([
    'description' => ['required', 'string', new MinWords(10)],
]);
```

---

### 🚀 実践例5: データベースを使ったルール

#### ステップ1: Ruleクラスを生成

```bash
php artisan make:rule UniqueSlug
```

**`app/Rules/UniqueSlug.php`**

```php
<?php

namespace App\Rules;

use App\Models\Post;
use Illuminate\Contracts\Validation\Rule;

class UniqueSlug implements Rule
{
    protected $postId;

    public function __construct($postId = null)
    {
        $this->postId = $postId;
    }

    public function passes($attribute, $value)
    {
        $query = Post::where('slug', $value);
        
        if ($this->postId) {
            $query->where('id', '!=', $this->postId);
        }
        
        return $query->doesntExist();
    }

    public function message()
    {
        return 'The :attribute has already been taken.';
    }
}
```

#### ステップ2: Ruleクラスを使う

```php
use App\Rules\UniqueSlug;

// 新規作成時
$request->validate([
    'slug' => ['required', 'string', new UniqueSlug],
]);

// 更新時
$request->validate([
    'slug' => ['required', 'string', new UniqueSlug($post->id)],
]);
```

---

### 🚀 実践例6: 複数のフィールドを使ったルール

#### ステップ1: Ruleクラスを生成

```bash
php artisan make:rule ValidDateRange
```

**`app/Rules/ValidDateRange.php`**

```php
<?php

namespace App\Rules;

use Illuminate\Contracts\Validation\Rule;

class ValidDateRange implements Rule
{
    protected $startDate;

    public function __construct($startDate)
    {
        $this->startDate = $startDate;
    }

    public function passes($attribute, $value)
    {
        return strtotime($value) >= strtotime($this->startDate);
    }

    public function message()
    {
        return 'The :attribute must be after the start date.';
    }
}
```

#### ステップ2: Ruleクラスを使う

```php
use App\Rules\ValidDateRange;

$request->validate([
    'start_date' => 'required|date',
    'end_date' => ['required', 'date', new ValidDateRange($request->start_date)],
]);
```

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

#### 間違い1: `passes()`で例外を投げる

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

#### 間違い2: `message()`で動的なメッセージを返そうとする

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
*   パラメータを受け取るカスタムルールを作成できる。
*   データベースを使ったカスタムルールを作成できる。
*   複数のフィールドを使ったカスタムルールを作成できる。

次のセクションでは、フォームリクエストを使って、バリデーションロジックを分離する方法を学びます。

---
