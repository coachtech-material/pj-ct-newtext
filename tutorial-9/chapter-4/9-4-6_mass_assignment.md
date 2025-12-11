# Tutorial 9-4-6: マスアサインメントと$fillable

## 🎯 このセクションで学ぶこと

*   マスアサインメントの仕組みを深く理解する。
*   `$fillable`と`$guarded`の使い分けを理解する。
*   マスアサインメントのセキュリティリスクを理解し、適切に保護できるようになる。

---

## 導入：「便利」と「危険」は紙一重

前のセクションで、`create()`や`update()`を使って、配列を渡してデータを作成・更新する方法を学びました。これは非常に便利ですが、**セキュリティリスク**があります。

このセクションでは、マスアサインメントの仕組みを深く理解し、適切に保護する方法を学びます。

---

## 詳細解説

### 🔒 マスアサインメントとは？

マスアサインメントとは、**配列を使って、一度に複数のカラムに値を代入すること**です。

```php
$user = User::create([
    'name' => '山田太郎',
    'email' => 'taro@example.com',
    'password' => Hash::make('password'),
]);
```

これは、以下のコードと同じです。

```php
$user = new User();
$user->name = '山田太郎';
$user->email = 'taro@example.com';
$user->password = Hash::make('password');
$user->save();
```

マスアサインメントを使うことで、コードがシンプルになります。

---

### 🚨 マスアサインメントのセキュリティリスク

マスアサインメントには、**セキュリティリスク**があります。

#### 攻撃シナリオ

以下のようなコントローラーがあるとします。

```php
public function store(Request $request)
{
    $user = User::create($request->all());
    return redirect('/users');
}
```

悪意のあるユーザーが、以下のようなリクエストを送信したとします。

```
POST /users
name=山田太郎&email=taro@example.com&password=password&is_admin=true
```

もし、`is_admin`カラムがマスアサインメントで代入可能な場合、**悪意のあるユーザーが管理者権限を取得できてしまいます**。

---

### 🔐 `$fillable`: ホワイトリスト方式

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

#### 攻撃を防ぐ

```php
$user = User::create([
    'name' => '山田太郎',
    'email' => 'taro@example.com',
    'password' => Hash::make('password'),
    'is_admin' => true, // これは無視される
]);
```

`is_admin`は`$fillable`に含まれていないため、無視されます。

---

### 🔐 `$guarded`: ブラックリスト方式

`$guarded`は、**マスアサインメントで代入不可能なカラムを明示的に指定**します。

**`app/Models/User.php`**

```php
protected $guarded = [
    'is_admin',
    'admin_approved_at',
];
```

これにより、`is_admin`と`admin_approved_at`以外のカラムがマスアサインメントで代入可能になります。

---

### 🔍 `$fillable`と`$guarded`の使い分け

| 方式 | 特徴 | 使い所 |
|:---|:---|:---|
| `$fillable` | 代入可能なカラムを明示的に指定 | カラム数が少ない場合、またはセキュリティを重視する場合 |
| `$guarded` | 代入不可能なカラムを明示的に指定 | カラム数が多い場合 |

**推奨**: `$fillable`を使う方が、セキュリティ的に安全です。

---

### 🚀 実践例：ユーザー登録

#### 安全な実装

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'name' => 'required',
        'email' => 'required|email|unique:users',
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

**重要なポイント**

*   `$request->all()`を直接`create()`に渡さない
*   バリデーション済みのデータのみを使う

---

### 💡 TIP: `$request->only()`と`$request->except()`

#### `$request->only()`: 指定したキーのみを取得

```php
$data = $request->only(['name', 'email', 'password']);
$user = User::create($data);
```

#### `$request->except()`: 指定したキー以外を取得

```php
$data = $request->except(['_token', '_method']);
$user = User::create($data);
```

---

### 🔒 マスアサインメントを無効にする

特定の操作で、マスアサインメントの保護を一時的に無効にすることができます。

```php
$user = User::unguarded(function () {
    return User::create([
        'name' => '山田太郎',
        'email' => 'taro@example.com',
        'is_admin' => true, // 通常は保護されているが、ここでは許可される
    ]);
});
```

**注意**: これは、シーダーやテストでのみ使用してください。本番環境では使用しないでください。

---

### 🔍 `forceFill()`を使った強制代入

`forceFill()`を使うことで、`$fillable`や`$guarded`を無視して、強制的に値を代入できます。

```php
$user = User::find(1);
$user->forceFill([
    'is_admin' => true,
])->save();
```

**注意**: これは、管理者のみが実行できる操作で使用してください。

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

#### 間違い2: `$request->all()`を直接`create()`に渡す

```php
$user = User::create($request->all()); // 危険
```

これは、セキュリティリスクがあります。必ずバリデーション済みのデータを使います。

```php
$validated = $request->validate([...]);
$user = User::create($validated); // 安全
```

#### 間違い3: `$fillable`と`$guarded`を両方定義する

```php
protected $fillable = ['name', 'email'];
protected $guarded = ['is_admin']; // エラー
```

`$fillable`と`$guarded`は、どちらか一方のみを定義してください。

---

### 🔐 ベストプラクティス

#### 1. `$fillable`を使う

`$guarded`よりも`$fillable`を使う方が、セキュリティ的に安全です。

```php
protected $fillable = ['name', 'email', 'password'];
```

#### 2. バリデーション済みのデータのみを使う

```php
$validated = $request->validate([...]);
$user = User::create($validated);
```

#### 3. `$request->all()`を直接使わない

```php
$user = User::create($request->all()); // NG
$user = User::create($request->only(['name', 'email'])); // OK
```

#### 4. 管理者権限などの重要なカラムは、必ず`$fillable`から除外する

```php
protected $fillable = ['name', 'email', 'password'];
// is_admin は $fillable に含めない
```

---

## ✨ まとめ

このセクションでは、マスアサインメントの仕組みと、適切に保護する方法を学びました。

*   マスアサインメントは、配列を使って、一度に複数のカラムに値を代入する仕組みである。
*   マスアサインメントには、セキュリティリスクがある。
*   `$fillable`を使って、代入可能なカラムを明示的に指定することで、セキュリティリスクを防げる。
*   `$guarded`を使って、代入不可能なカラムを明示的に指定することもできる。
*   `$fillable`を使う方が、セキュリティ的に安全である。
*   バリデーション済みのデータのみを使うことが重要である。

これで、Chapter 4「Eloquent ORMの基礎」の全6セクションが完了しました。次は、Chapter 5「Eloquent ORMとリレーションシップ」の残りのセクションを執筆します。

---

## 📝 学習のポイント

- [ ] マスアサインメントの仕組みを理解した。
- [ ] マスアサインメントのセキュリティリスクを理解した。
- [ ] `$fillable`を使って、代入可能なカラムを明示的に指定できる。
- [ ] `$guarded`を使って、代入不可能なカラムを明示的に指定できる。
- [ ] バリデーション済みのデータのみを使うことが重要である。
