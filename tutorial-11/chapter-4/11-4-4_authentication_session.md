# Tutorial 11-4-4: 認証とセッション管理

## 🎯 このセクションで学ぶこと

*   セッションハイジャックとは何かを理解し、その危険性を学ぶ。
*   セッション固定攻撃を防ぐ方法を学ぶ。
*   安全なセッション管理の方法を学ぶ。

---

## 導入：なぜ認証とセッション管理が重要なのか

**セッションハイジャック**は、**他人のセッションIDを盗んで、なりすます攻撃**です。

安全なセッション管理を行わないと、ユーザーのアカウントが乗っ取られる可能性があります。

---

## 詳細解説

### 🔍 セッションとは

**セッション**は、**ユーザーの状態を保持する仕組み**です。

Laravelでは、セッションIDをCookieに保存し、サーバー側でセッションデータを管理します。

---

### 🔍 セッションハイジャック

**セッションハイジャック**は、**他人のセッションIDを盗んで、なりすます攻撃**です。

例:
1. ユーザーAがログインする
2. 攻撃者がユーザーAのセッションIDを盗む
3. 攻撃者がユーザーAのセッションIDを使って、ユーザーAになりすます

---

### 🔍 セッション固定攻撃

**セッション固定攻撃**は、**攻撃者が用意したセッションIDを使わせる攻撃**です。

例:
1. 攻撃者がセッションIDを用意する
2. ユーザーAに、攻撃者が用意したセッションIDを使わせる
3. ユーザーAがログインする
4. 攻撃者が同じセッションIDを使って、ユーザーAになりすます

---

### 🔍 Laravelのセッション固定攻撃対策

Laravelは、ログイン時に自動的にセッションIDを再生成します。

**ファイル**: `app/Http/Controllers/Auth/LoginController.php`（Laravel Fortifyを使う場合は自動）

```php
use Illuminate\Support\Facades\Auth;

public function login(Request $request)
{
    $credentials = $request->validate([
        'email' => 'required|email',
        'password' => 'required',
    ]);

    if (Auth::attempt($credentials)) {
        $request->session()->regenerate();  // セッションIDを再生成

        return redirect()->intended('/');
    }

    return back()->withErrors([
        'email' => 'メールアドレスまたはパスワードが正しくありません。',
    ]);
}
```

---

### 🔍 セッションの有効期限

セッションの有効期限を設定することで、セッションハイジャックのリスクを減らせます。

**ファイル**: `config/session.php`

```php
'lifetime' => 120,  // 120分（2時間）
'expire_on_close' => false,  // ブラウザを閉じてもセッションを保持
```

---

### 🔍 セッションの無効化

ログアウト時は、セッションを無効化します。

```php
public function logout(Request $request)
{
    Auth::logout();

    $request->session()->invalidate();  // セッションを無効化
    $request->session()->regenerateToken();  // CSRFトークンを再生成

    return redirect('/');
}
```

---

### 🔍 セッションドライバー

Laravelは、複数のセッションドライバーをサポートしています。

*   `file`: ファイルにセッションを保存（デフォルト）
*   `cookie`: Cookieにセッションを保存
*   `database`: データベースにセッションを保存
*   `redis`: Redisにセッションを保存

**ファイル**: `config/session.php`

```php
'driver' => env('SESSION_DRIVER', 'file'),
```

---

### 🔍 databaseドライバーの設定

```bash
php artisan session:table
php artisan migrate
```

**ファイル**: `.env`

```
SESSION_DRIVER=database
```

---

### 🔍 HTTPSの使用

**HTTPS**を使うことで、セッションIDの盗聴を防げます。

**ファイル**: `config/session.php`

```php
'secure' => env('SESSION_SECURE_COOKIE', true),  // HTTPSのみでCookieを送信
'http_only' => true,  // JavaScriptからCookieにアクセスできないようにする
'same_site' => 'lax',  // CSRF攻撃を防ぐ
```

---

### 🔍 Remember Meトークン

「ログイン状態を保持する」機能を実装する場合は、Remember Meトークンを使います。

```php
if (Auth::attempt($credentials, $request->filled('remember'))) {
    $request->session()->regenerate();
    return redirect()->intended('/');
}
```

---

### 💡 TIP: セッションのタイムアウト

一定時間操作がない場合、自動的にログアウトさせることができます。

**ファイル**: `app/Http/Middleware/CheckSessionTimeout.php`

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Support\Facades\Auth;

class CheckSessionTimeout
{
    public function handle($request, Closure $next)
    {
        $timeout = 1800; // 30分

        if (session('last_activity') && (time() - session('last_activity') > $timeout)) {
            Auth::logout();
            $request->session()->invalidate();
            return redirect('/login')->with('message', 'セッションがタイムアウトしました。');
        }

        session(['last_activity' => time()]);

        return $next($request);
    }
}
```

---

### 🚨 よくある間違い

#### 間違い1: ログイン時にセッションIDを再生成しない

**対処法**: `$request->session()->regenerate()`を呼び出します。

---

#### 間違い2: ログアウト時にセッションを無効化しない

**対処法**: `$request->session()->invalidate()`を呼び出します。

---

#### 間違い3: HTTPSを使わない

**対処法**: 本番環境では必ずHTTPSを使います。

---

## ✨ まとめ

このセクションでは、認証とセッション管理について学びました。

*   セッションハイジャックとセッション固定攻撃の危険性を理解した。
*   ログイン時にセッションIDを再生成した。
*   ログアウト時にセッションを無効化した。

次のセクションでは、パスワードのハッシュ化について学びます。

---

## 📝 学習のポイント

- [ ] セッションハイジャックの危険性を理解した。
- [ ] セッション固定攻撃を防ぐ方法を学んだ。
- [ ] セッションIDを再生成した。
- [ ] HTTPSの重要性を理解した。
