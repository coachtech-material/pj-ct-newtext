# Tutorial 9-4-4: データの作成（create、save）

## 🎯 このセクションで学ぶこと

*   Eloquentを使って、データを作成できるようになる。
*   `create()`と`save()`の違いを理解し、使い分けられるようになる。
*   マスアサインメントの基本を理解する。

---

## 導入：データを「作る」2つの方法

Eloquentでは、データを作成する方法が主に2つあります。

1. **`create()`メソッド**: 配列を渡して、一度にレコードを作成する
2. **`save()`メソッド**: モデルのインスタンスを作成してから、保存する

どちらも同じ結果になりますが、使い分けることで、コードがより読みやすくなります。

このセクションでは、Eloquentを使ってデータを作成する方法を学びます。

---

## 詳細解説

### 📝 `create()`メソッド

`create()`メソッドは、配列を渡して、一度にレコードを作成します。

#### 基本的な使い方

```php
$user = User::create([
    'name' => '山田太郎',
    'email' => 'taro@example.com',
    'password' => Hash::make('password'),
]);
```

これは、以下のSQLと同じです。

```sql
INSERT INTO users (name, email, password) VALUES ('山田太郎', 'taro@example.com', 'ハッシュ化されたパスワード');
```

**重要なポイント**

*   `create()`は、作成されたモデルのインスタンスを返します。
*   `create()`を使うには、モデルに`$fillable`または`$guarded`を定義する必要があります（後述）。

---

### 📝 `save()`メソッド

`save()`メソッドは、モデルのインスタンスを作成してから、保存します。

#### 基本的な使い方

```php
$user = new User();
$user->name = '山田太郎';
$user->email = 'taro@example.com';
$user->password = Hash::make('password');
$user->save();
```

これも、以下のSQLと同じです。

```sql
INSERT INTO users (name, email, password) VALUES ('山田太郎', 'taro@example.com', 'ハッシュ化されたパスワード');
```

---

### 🔍 `create()`と`save()`の違い

| メソッド | 特徴 | 使い所 |
|:---|:---|:---|
| `create()` | 配列を渡して、一度に作成 | フォームから送信されたデータを保存する場合 |
| `save()` | インスタンスを作成してから保存 | 複雑なロジックがある場合、または段階的にデータを設定する場合 |

#### `create()`が適している例

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'name' => 'required',
        'email' => 'required|email',
        'password' => 'required|min:8',
    ]);

    $user = User::create([
        'name' => $validated['name'],
        'email' => $validated['email'],
        'password' => Hash::make($validated['password']),
    ]);

    return redirect('/users');
}
```

#### `save()`が適している例

```php
public function store(Request $request)
{
    $user = new User();
    $user->name = $request->name;
    $user->email = $request->email;
    $user->password = Hash::make($request->password);
    
    // 複雑なロジック
    if ($request->has('is_admin')) {
        $user->is_admin = true;
        $user->admin_approved_at = now();
    }
    
    $user->save();

    return redirect('/users');
}
```

---

### 🔒 マスアサインメントとは？

マスアサインメントとは、**配列を使って、一度に複数のカラムに値を代入すること**です。

```php
$user = User::create([
    'name' => '山田太郎',
    'email' => 'taro@example.com',
    'password' => Hash::make('password'),
]);
```

しかし、マスアサインメントには、セキュリティリスクがあります。

#### セキュリティリスクの例

悪意のあるユーザーが、以下のようなリクエストを送信したとします。

```
POST /users
name=山田太郎&email=taro@example.com&password=password&is_admin=true
```

もし、`is_admin`カラムがマスアサインメントで代入可能な場合、悪意のあるユーザーが管理者権限を取得できてしまいます。

---

### 🔐 `$fillable`と`$guarded`

Laravelでは、マスアサインメントを保護するために、`$fillable`または`$guarded`を定義します。

#### `$fillable`: ホワイトリスト方式

`$fillable`は、**マスアサインメントで代入可能なカラムを明示的に指定**します。

**`app/Models/User.php`**

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable
{
    protected $fillable = [
        'name',
        'email',
        'password',
    ];
}
```

これにより、`name`、`email`、`password`のみがマスアサインメントで代入可能になります。

#### `$guarded`: ブラックリスト方式

`$guarded`は、**マスアサインメントで代入不可能なカラムを明示的に指定**します。

**`app/Models/User.php`**

```php
protected $guarded = [
    'is_admin',
    'admin_approved_at',
];
```

これにより、`is_admin`と`admin_approved_at`以外のカラムがマスアサインメントで代入可能になります。

#### 全てのカラムを許可する（非推奨）

```php
protected $guarded = [];
```

これにより、全てのカラムがマスアサインメントで代入可能になります。ただし、セキュリティリスクがあるため、本番環境では推奨されません。

---

### 🚀 実践例：ユーザー登録

#### `create()`を使った例

```php
public function register(Request $request)
{
    $validated = $request->validate([
        'name' => 'required',
        'email' => 'required|email|unique:users',
        'password' => 'required|min:8|confirmed',
    ]);

    $user = User::create([
        'name' => $validated['name'],
        'email' => $validated['email'],
        'password' => Hash::make($validated['password']),
    ]);

    Auth::login($user);

    return redirect('/dashboard');
}
```

#### `save()`を使った例

```php
public function register(Request $request)
{
    $validated = $request->validate([
        'name' => 'required',
        'email' => 'required|email|unique:users',
        'password' => 'required|min:8|confirmed',
    ]);

    $user = new User();
    $user->name = $validated['name'];
    $user->email = $validated['email'];
    $user->password = Hash::make($validated['password']);
    $user->save();

    Auth::login($user);

    return redirect('/dashboard');
}
```

---

### 💡 TIP: `firstOrCreate()`と`updateOrCreate()`

#### `firstOrCreate()`: 存在しない場合のみ作成

```php
$user = User::firstOrCreate(
    ['email' => 'taro@example.com'],
    ['name' => '山田太郎', 'password' => Hash::make('password')]
);
```

これは、以下のロジックと同じです。

1. `email`が`taro@example.com`のユーザーを検索
2. 見つからない場合は、新しいユーザーを作成
3. 見つかった場合は、そのユーザーを返す

#### `updateOrCreate()`: 存在する場合は更新、存在しない場合は作成

```php
$user = User::updateOrCreate(
    ['email' => 'taro@example.com'],
    ['name' => '山田太郎', 'password' => Hash::make('password')]
);
```

これは、以下のロジックと同じです。

1. `email`が`taro@example.com`のユーザーを検索
2. 見つかった場合は、`name`と`password`を更新
3. 見つからない場合は、新しいユーザーを作成

---

### 🔍 タイムスタンプの自動設定

Eloquentは、デフォルトで`created_at`と`updated_at`を自動的に設定します。

```php
$user = User::create([...]);
echo $user->created_at; // 2024-12-11 10:00:00
echo $user->updated_at; // 2024-12-11 10:00:00
```

#### タイムスタンプを無効にする

```php
class User extends Model
{
    public $timestamps = false;
}
```

---

### 🚨 よくある間違い

#### 間違い1: `$fillable`を定義せずに`create()`を使う

```php
$user = User::create([
    'name' => '山田太郎',
    'email' => 'taro@example.com',
]);
```

**エラー**

```
Illuminate\Database\Eloquent\MassAssignmentException: Add [name] to fillable property to allow mass assignment on [App\Models\User].
```

**対処法**: モデルに`$fillable`を定義します。

```php
protected $fillable = ['name', 'email', 'password'];
```

#### 間違い2: `save()`を忘れる

```php
$user = new User();
$user->name = '山田太郎';
$user->email = 'taro@example.com';
// $user->save(); を忘れる
```

これでは、データベースに保存されません。必ず`save()`を呼び出します。

---

## ✨ まとめ

このセクションでは、Eloquentを使ってデータを作成する方法を学びました。

*   `create()`は、配列を渡して、一度にレコードを作成する。
*   `save()`は、モデルのインスタンスを作成してから、保存する。
*   マスアサインメントを保護するために、`$fillable`または`$guarded`を定義する必要がある。
*   `firstOrCreate()`、`updateOrCreate()`を使うと、存在チェックと作成/更新を一度に行える。
*   Eloquentは、デフォルトで`created_at`と`updated_at`を自動的に設定する。

次のセクションでは、Eloquentを使ってデータを更新・削除する方法を学びます。

---
