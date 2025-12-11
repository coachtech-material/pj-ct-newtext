# Tutorial 11-4-5: パスワードのハッシュ化

## 🎯 このセクションで学ぶこと

*   パスワードのハッシュ化とは何かを理解し、その重要性を学ぶ。
*   Laravelのパスワードハッシュ化の仕組みを学ぶ。
*   安全なパスワード管理の方法を学ぶ。

---

## 導入：なぜパスワードのハッシュ化が重要なのか

**パスワードのハッシュ化**は、**パスワードを暗号化して保存する仕組み**です。

パスワードをそのまま保存すると、データベースが漏洩した場合に、すべてのユーザーのパスワードが盗まれてしまいます。

---

## 詳細解説

### 🔍 ハッシュ化とは

**ハッシュ化**は、**元のデータから一方向の変換を行い、元に戻せないようにする処理**です。

例:
*   パスワード: `password123`
*   ハッシュ値: `$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi`

---

### 🔍 Laravelのパスワードハッシュ化

Laravelは、**bcrypt**アルゴリズムを使ってパスワードをハッシュ化します。

**ファイル**: `app/Models/User.php`

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use Notifiable;

    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected $casts = [
        'email_verified_at' => 'datetime',
        'password' => 'hashed',  // Laravel 11以降
    ];
}
```

---

### 🔍 パスワードのハッシュ化

`Hash::make()`を使って、パスワードをハッシュ化します。

```php
use Illuminate\Support\Facades\Hash;

$hashedPassword = Hash::make('password123');
```

---

### 🔍 パスワードの検証

`Hash::check()`を使って、パスワードを検証します。

```php
if (Hash::check('password123', $hashedPassword)) {
    // パスワードが一致
}
```

---

### 🔍 ユーザー登録時のパスワードハッシュ化

**ファイル**: `app/Http/Controllers/Auth/RegisterController.php`（Laravel Fortifyを使う場合は自動）

```php
use Illuminate\Support\Facades\Hash;

public function store(Request $request)
{
    $validated = $request->validate([
        'name' => 'required|max:255',
        'email' => 'required|email|unique:users',
        'password' => 'required|min:8|confirmed',
    ]);

    $user = User::create([
        'name' => $validated['name'],
        'email' => $validated['email'],
        'password' => Hash::make($validated['password']),
    ]);

    Auth::login($user);

    return redirect('/');
}
```

---

### 🔍 Laravel 11のpassword cast

Laravel 11では、`password`カラムに`hashed`キャストを設定すると、自動的にハッシュ化されます。

**ファイル**: `app/Models/User.php`

```php
protected $casts = [
    'password' => 'hashed',
];
```

```php
// 自動的にハッシュ化される
$user = User::create([
    'name' => 'John Doe',
    'email' => 'john@example.com',
    'password' => 'password123',
]);
```

---

### 🔍 パスワードのリセット

パスワードリセット機能を実装する場合は、Laravel Fortifyを使います。

```bash
composer require laravel/fortify
php artisan fortify:install
php artisan migrate
```

---

### 🔍 パスワードの強度チェック

パスワードの強度をチェックするバリデーションルールを使います。

```php
$validated = $request->validate([
    'password' => [
        'required',
        'min:8',
        'confirmed',
        'regex:/[a-z]/',      // 小文字を含む
        'regex:/[A-Z]/',      // 大文字を含む
        'regex:/[0-9]/',      // 数字を含む
        'regex:/[@$!%*#?&]/', // 記号を含む
    ],
]);
```

---

### 🔍 パスワードの変更

パスワード変更機能を実装します。

**ファイル**: `app/Http/Controllers/PasswordController.php`

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class PasswordController extends Controller
{
    public function update(Request $request)
    {
        $validated = $request->validate([
            'current_password' => 'required',
            'password' => 'required|min:8|confirmed',
        ]);

        $user = $request->user();

        if (!Hash::check($validated['current_password'], $user->password)) {
            return back()->withErrors(['current_password' => '現在のパスワードが正しくありません。']);
        }

        $user->update([
            'password' => Hash::make($validated['password']),
        ]);

        return back()->with('success', 'パスワードを変更しました。');
    }
}
```

---

### 💡 TIP: パスワードのリハッシュ化

bcryptのコストファクターを変更した場合、既存のパスワードをリハッシュ化できます。

```php
if (Hash::needsRehash($user->password)) {
    $user->update([
        'password' => Hash::make($plainPassword),
    ]);
}
```

---

### 🚨 よくある間違い

#### 間違い1: パスワードをそのまま保存する

**対処法**: 必ず`Hash::make()`を使います。

---

#### 間違い2: MD5やSHA1を使う

**対処法**: bcryptまたはArgon2を使います。

---

#### 間違い3: パスワードの強度チェックをしない

**対処法**: バリデーションルールで強度チェックを行います。

---

## ✨ まとめ

このセクションでは、パスワードのハッシュ化について学びました。

*   パスワードのハッシュ化の重要性を理解した。
*   Hash::make()とHash::check()を使った。
*   パスワードの強度チェックを実装した。

次のChapterでは、リファクタリングについて学びます。

---

## 📝 学習のポイント

- [ ] パスワードのハッシュ化の重要性を理解した。
- [ ] Hash::make()を使った。
- [ ] Hash::check()を使った。
- [ ] パスワードの強度チェックを実装した。
