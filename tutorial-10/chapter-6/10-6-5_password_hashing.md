# Tutorial 10-6-5: パスワードのハッシュ化

## 🎯 このセクションで学ぶこと

*   パスワードを平文で保存する危険性を理解する。
*   ハッシュ化と暗号化の違いを理解する。
*   Laravelのパスワードハッシュ化機能を使って、安全にパスワードを保存する方法を学ぶ。
*   ソルトとストレッチングの役割を理解する。

---

## 導入：パスワードは最も重要な秘密情報

前のセクションで、認証とセッション管理について学びました。このセクションでは、認証の根幹である**パスワードの保存方法**について学びます。

**重要な質問**：
あなたのWebアプリケーションのデータベースが、攻撃者に盗まれたとします。ユーザーのパスワードは安全でしょうか？

この質問に「はい」と答えられるようになることが、このセクションの目標です。

---

## 詳細解説

### 🚨 平文でパスワードを保存してはいけない

**平文**（Plain Text）とは、**暗号化されていない、そのままの文字列**です。

#### 危険なコード例

```php
// 🚨 絶対にやってはいけない
User::create([
    'email' => $request->email,
    'password' => $request->password, // 平文で保存
]);
```

**データベースの内容**：

| id | email | password |
|----|-------|----------|
| 1 | user@example.com | password123 |
| 2 | admin@example.com | admin2024 |

**何が問題か**：

1. **データベースが漏洩すると、全てのパスワードが盗まれる**
2. **管理者がユーザーのパスワードを見ることができる**（プライバシー侵害）
3. **ユーザーが他のサイトで同じパスワードを使っている場合、そのサイトも危険にさらされる**

---

### 🔐 ハッシュ化とは

**ハッシュ化**とは、**元のデータから、固定長の文字列（ハッシュ値）を生成する処理**です。

#### ハッシュ化の特徴

1. **一方向性**：ハッシュ値から元のデータを復元できない
2. **固定長**：どんなに長いデータでも、同じ長さのハッシュ値になる
3. **決定性**：同じデータからは、常に同じハッシュ値が生成される
4. **衝突耐性**：異なるデータから、同じハッシュ値が生成される確率が極めて低い

**例**：

```
元のデータ: password123
ハッシュ値: $2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi
```

---

### 🔓 暗号化との違い

| | ハッシュ化 | 暗号化 |
|---|-----------|--------|
| **復号** | 不可能 | 可能 |
| **用途** | パスワード保存 | データの秘匿 |
| **鍵** | 不要 | 必要 |

**重要なポイント**：
パスワードは**ハッシュ化**して保存します。暗号化は使いません。なぜなら、パスワードを復号する必要がないからです。

---

### 🔧 Laravelのパスワードハッシュ化

Laravelは、**bcrypt**アルゴリズムを使って、パスワードをハッシュ化します。

#### パスワードをハッシュ化する

```php
use Illuminate\Support\Facades\Hash;

$hashedPassword = Hash::make('password123');
```

**生成されるハッシュ値**：

```
$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi
```

**コードリーディング**：

*   `Hash::make()`：パスワードをハッシュ化
*   `$2y$`：bcryptアルゴリズムを使用
*   `10`：コストファクター（後述）

---

#### パスワードを検証する

```php
if (Hash::check('password123', $hashedPassword)) {
    // パスワードが一致
} else {
    // パスワードが一致しない
}
```

**コードリーディング**：

*   `Hash::check()`：平文のパスワードとハッシュ値を比較
*   ハッシュ値から元のパスワードを復元するのではなく、入力されたパスワードをハッシュ化して比較します

---

### 🧂 ソルトとは

**ソルト**（Salt）とは、**ハッシュ化する前に、パスワードに追加するランダムな文字列**です。

#### ソルトの役割

ソルトがないと、同じパスワードは常に同じハッシュ値になります。

**ソルトなし**：

| ユーザー | パスワード | ハッシュ値 |
|---------|-----------|-----------|
| user1 | password123 | abc... |
| user2 | password123 | abc... |

攻撃者は、「ハッシュ値が同じユーザーは、同じパスワードを使っている」とわかります。

**ソルトあり**：

| ユーザー | パスワード | ソルト | ハッシュ値 |
|---------|-----------|--------|-----------|
| user1 | password123 | xyz | def... |
| user2 | password123 | uvw | ghi... |

同じパスワードでも、異なるハッシュ値になります。

**重要なポイント**：
Laravelの`Hash::make()`は、自動的にソルトを生成します。開発者が意識する必要はありません。

---

### 🏋️ ストレッチングとは

**ストレッチング**（Key Stretching）とは、**ハッシュ化を複数回繰り返すことで、計算時間を増やす手法**です。

#### ストレッチングの役割

攻撃者は、**総当たり攻撃**（Brute Force Attack）で、パスワードを推測しようとします。

**例**：
1秒間に10億回のハッシュ化ができる場合、8文字のパスワード（英数字）を総当たりで破るには、約2時間かかります。

ストレッチングを使って、ハッシュ化を1000回繰り返すと、2000時間（約83日）かかります。

**重要なポイント**：
Laravelの`Hash::make()`は、自動的にストレッチングを行います。**コストファクター**で、繰り返し回数を調整できます。

---

### ⚙️ コストファクター

**コストファクター**とは、**ハッシュ化の計算コスト**を指定する値です。

**config/hashing.php**

```php
'bcrypt' => [
    'rounds' => env('BCRYPT_ROUNDS', 10),
],
```

**コストファクターと計算時間の関係**：

| コストファクター | 計算時間（目安） |
|----------------|----------------|
| 10 | 0.1秒 |
| 12 | 0.4秒 |
| 14 | 1.6秒 |

**推奨値**：
10〜12が一般的です。高すぎると、ログインが遅くなります。

---

### 💡 実践例：ユーザー登録

#### コントローラー

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class RegisterController extends Controller
{
    public function register(Request $request)
    {
        // バリデーション
        $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users',
            'password' => 'required|string|min:8|confirmed',
        ]);
        
        // ユーザーを作成
        User::create([
            'name' => $request->name,
            'email' => $request->email,
            'password' => Hash::make($request->password), // ハッシュ化
        ]);
        
        return redirect('/login')->with('success', 'アカウントを作成しました');
    }
}
```

**コードリーディング**：

*   `Hash::make($request->password)`：パスワードをハッシュ化
*   `confirmed`：`password_confirmation`フィールドと一致するか検証

---

#### モデルでの自動ハッシュ化

Laravelの`User`モデルは、デフォルトで**ミューテータ**を使って、パスワードを自動的にハッシュ化します。

**app/Models/User.php**

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Support\Facades\Hash;

class User extends Authenticatable
{
    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    // パスワードを自動的にハッシュ化
    protected function password(): Attribute
    {
        return Attribute::make(
            set: fn ($value) => Hash::make($value),
        );
    }
}
```

**コードリーディング**：

*   `Attribute::make(set: ...)`：セット時に自動的にハッシュ化
*   これにより、`User::create(['password' => 'password123'])`と書くだけで、自動的にハッシュ化されます

---

### 🔍 パスワードの強度チェック

パスワードの強度をチェックすることも重要です。

#### バリデーションルール

```php
$request->validate([
    'password' => [
        'required',
        'string',
        'min:8',              // 最低8文字
        'regex:/[a-z]/',      // 小文字を含む
        'regex:/[A-Z]/',      // 大文字を含む
        'regex:/[0-9]/',      // 数字を含む
        'regex:/[@$!%*?&]/',  // 特殊文字を含む
    ],
]);
```

---

#### カスタムバリデーションルール

```php
use Illuminate\Validation\Rules\Password;

$request->validate([
    'password' => ['required', Password::min(8)
        ->letters()
        ->mixedCase()
        ->numbers()
        ->symbols()
        ->uncompromised()], // 漏洩したパスワードをチェック
]);
```

**コードリーディング**：

*   `Password::min(8)`：最低8文字
*   `letters()`：文字を含む
*   `mixedCase()`：大文字と小文字を含む
*   `numbers()`：数字を含む
*   `symbols()`：特殊文字を含む
*   `uncompromised()`：Have I Been Pwned APIで、漏洩したパスワードをチェック

---

### 🔄 パスワードの変更

#### コントローラー

```php
public function changePassword(Request $request)
{
    $request->validate([
        'current_password' => 'required',
        'new_password' => 'required|string|min:8|confirmed',
    ]);
    
    // 現在のパスワードを検証
    if (!Hash::check($request->current_password, auth()->user()->password)) {
        return back()->withErrors(['current_password' => '現在のパスワードが正しくありません']);
    }
    
    // 新しいパスワードを保存
    auth()->user()->update([
        'password' => Hash::make($request->new_password),
    ]);
    
    return redirect('/dashboard')->with('success', 'パスワードを変更しました');
}
```

**コードリーディング**：

*   `Hash::check()`：現在のパスワードを検証
*   `Hash::make()`：新しいパスワードをハッシュ化

---

### 🛡️ レインボーテーブル攻撃

**レインボーテーブル**とは、**よく使われるパスワードとそのハッシュ値を事前に計算したテーブル**です。

**攻撃のシナリオ**：

1. 攻撃者がデータベースを盗む
2. ハッシュ値をレインボーテーブルで検索
3. 一致するハッシュ値があれば、元のパスワードがわかる

**対策**：

*   **ソルト**を使うことで、レインボーテーブル攻撃を防げます
*   Laravelの`Hash::make()`は、自動的にソルトを使います

---

### 🔒 パスワードリセット

パスワードを忘れた場合、**パスワードリセット**機能を提供します。

#### 仕組み

1. ユーザーがメールアドレスを入力
2. サーバーが**ランダムなトークン**を生成し、メールで送信
3. ユーザーがトークンを使って、新しいパスワードを設定

**重要なポイント**：

*   トークンは**一度だけ使える**
*   トークンには**有効期限**がある（通常60分）

Laravelは、パスワードリセット機能を標準で提供しています。

```bash
php artisan make:migration create_password_resets_table
```

---

## 💡 TIP

### パスワードのハッシュ化アルゴリズム

Laravelは、デフォルトで**bcrypt**を使いますが、**argon2**も選択できます。

**config/hashing.php**

```php
'driver' => 'argon2',
```

**argon2の特徴**：

*   bcryptよりも安全
*   メモリを大量に使うため、総当たり攻撃に強い

---

### パスワードの定期的な変更は不要

以前は「パスワードを定期的に変更すべき」とされていましたが、現在は**推奨されていません**。

**理由**：

*   ユーザーが覚えやすい弱いパスワードを選ぶようになる
*   パスワードをメモに書いて保存するようになる

**推奨される対策**：

*   **強力なパスワード**を使う
*   **二要素認証**を有効にする
*   **パスワードマネージャー**を使う

---

## ✨ まとめ

*   パスワードは**絶対に平文で保存してはいけない**
*   **ハッシュ化**は一方向性で、元のデータを復元できない
*   **暗号化**は復号可能だが、パスワード保存には使わない
*   Laravelの`Hash::make()`は、**bcrypt**アルゴリズムを使って、自動的にソルトとストレッチングを行う
*   **ソルト**は、同じパスワードでも異なるハッシュ値を生成する
*   **ストレッチング**は、計算時間を増やすことで、総当たり攻撃を困難にする
*   **コストファクター**で、ハッシュ化の計算コストを調整できる
*   パスワードの強度チェックには、`Password`ルールを使う
*   パスワードリセット機能を提供することで、ユーザーがパスワードを忘れても安全に再設定できる

---
