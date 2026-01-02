# Tutorial 9-12-4: 認証とセッション管理

## 🎯 このセクションで学ぶこと

*   Webアプリケーションにおける認証の仕組みを理解する。
*   セッションとCookieの役割と違いを理解する。
*   Laravelのセッション管理機能を使って、安全な認証を実装する方法を学ぶ。
*   セッションハイジャック攻撃とその対策を理解する。

---

## 導入：「ログイン状態」を維持する仕組み

これまで、CSRF、SQLインジェクション、XSSという3つの代表的な攻撃について学びました。このセクションでは、Webアプリケーションの根幹である**認証とセッション管理**について学びます。

**疑問**：
ブラウザでログインすると、ページを移動しても「ログイン状態」が維持されます。これはどのような仕組みで実現されているのでしょうか？

この仕組みを理解することは、セキュリティを考える上で非常に重要です。

---

## 詳細解説

### 🔑 認証とは

**認証**（Authentication）とは、**ユーザーが本人であることを確認するプロセス**です。

#### 認証の3つの要素

| 要素 | 説明 | 例 |
|------|------|-----|
| **知識** | ユーザーが知っている情報 | パスワード、秘密の質問 |
| **所有** | ユーザーが持っているもの | スマートフォン、ICカード |
| **生体** | ユーザー自身の特徴 | 指紋、顔認証 |

一般的なWebアプリケーションでは、**知識（パスワード）**を使った認証が主流です。

---

### 🍪 HTTPはステートレス

**HTTP**プロトコルは、**ステートレス**（状態を持たない）です。つまり、各リクエストは独立しており、前のリクエストの情報を覚えていません。

**例**：
1. ユーザーがログインする（`POST /login`）
2. 次のページにアクセスする（`GET /dashboard`）
3. サーバーは、「このユーザーがログインしたこと」を覚えていない

この問題を解決するのが、**セッション**と**Cookie**です。

---

### 🎫 セッションとCookieの仕組み

#### Cookieとは

**Cookie**とは、**ブラウザに保存される小さなデータ**です。サーバーがCookieを発行すると、ブラウザは次回以降のリクエストで、自動的にCookieを送信します。

**Cookieの例**：

```
Set-Cookie: session_id=abc123; Path=/; HttpOnly; Secure
```

**コードリーディング**：

*   `session_id=abc123`：Cookieの名前と値
*   `Path=/`：すべてのパスで有効
*   `HttpOnly`：JavaScriptからアクセス不可（XSS対策）
*   `Secure`：HTTPS通信のみで送信（盗聴対策）

---

#### セッションとは

**セッション**とは、**サーバー側に保存されるユーザーの状態**です。セッションIDをCookieに保存し、ブラウザとサーバーを紐付けます。

**セッションの流れ**：

```
1. ユーザーがログイン
   ↓
2. サーバーがセッションを作成し、セッションIDを発行
   ↓
3. セッションIDをCookieに保存
   ↓
4. ブラウザが次回以降のリクエストで、セッションIDを送信
   ↓
5. サーバーがセッションIDからユーザーを特定
```

**身近な例で理解する**：
セッションは、映画館のチケットのようなものです。チケット（セッションID）を持っていれば、映画館（サーバー）に入場できます。チケットを失くすと、入場できなくなります。

---

### 🔧 Laravelのセッション管理

Laravelは、セッション管理を**自動的に**行います。

#### セッションドライバー

Laravelは、複数のセッションドライバーをサポートしています。

| ドライバー | 説明 | 用途 |
|-----------|------|------|
| **file** | ファイルシステムに保存 | 開発環境 |
| **cookie** | Cookieに保存（暗号化） | 小規模アプリ |
| **database** | データベースに保存 | 本番環境 |
| **redis** | Redisに保存 | 高速化が必要な場合 |

**config/session.php**

```php
'driver' => env('SESSION_DRIVER', 'file'),
```

---

#### セッションの使い方

セッションにデータを保存・取得する方法は非常にシンプルです。

```php
// セッションにデータを保存
session(['user_id' => 123]);

// セッションからデータを取得
$userId = session('user_id');

// セッションからデータを削除
session()->forget('user_id');

// セッションを全て削除
session()->flush();
```

---

### 🔐 Laravelの認証機能

Laravelは、認証機能を標準で提供しています。Chapter 7で学んだ**Laravel Fortify**を使うと、簡単に認証を実装できます。

#### ログイン処理の流れ

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class LoginController extends Controller
{
    public function login(Request $request)
    {
        // バリデーション
        $credentials = $request->validate([
            'email' => 'required|email',
            'password' => 'required',
        ]);
        
        // 認証を試みる
        if (Auth::attempt($credentials)) {
            // 認証成功
            $request->session()->regenerate(); // セッションIDを再生成（セッションハイジャック対策）
            
            return redirect()->intended('/dashboard');
        }
        
        // 認証失敗
        return back()->withErrors([
            'email' => 'メールアドレスまたはパスワードが正しくありません。',
        ]);
    }
}
```

**コードリーディング**：

*   `Auth::attempt($credentials)`：メールアドレスとパスワードで認証を試みる
*   `$request->session()->regenerate()`：セッションIDを再生成（重要！）
*   `redirect()->intended()`：ログイン前にアクセスしようとしたページにリダイレクト

---

#### ログアウト処理

```php
public function logout(Request $request)
{
    Auth::logout();
    
    $request->session()->invalidate(); // セッションを無効化
    $request->session()->regenerateToken(); // CSRFトークンを再生成
    
    return redirect('/');
}
```

**コードリーディング**：

*   `Auth::logout()`：ログアウト
*   `$request->session()->invalidate()`：セッションを無効化
*   `$request->session()->regenerateToken()`：CSRFトークンを再生成（CSRF対策）

---

### 🛡️ セッションハイジャック攻撃

**セッションハイジャック**とは、**攻撃者がユーザーのセッションIDを盗み、なりすましログインする攻撃**です。

#### 攻撃のシナリオ

1. ユーザーがログインし、セッションIDが発行される
2. 攻撃者が、何らかの方法でセッションIDを盗む（XSS攻撃、盗聴など）
3. 攻撃者が盗んだセッションIDを使って、ユーザーになりすます

---

### 🔒 セッションハイジャック対策

Laravelは、複数の対策を提供しています。

#### 1. セッションIDの再生成

ログイン時に、セッションIDを再生成します。

```php
$request->session()->regenerate();
```

これにより、古いセッションIDが無効になります。

---

#### 2. HttpOnlyフラグ

CookieにHttpOnlyフラグを設定することで、JavaScriptからのアクセスを防ぎます。

**config/session.php**

```php
'http_only' => true,
```

これにより、XSS攻撃でセッションIDが盗まれるリスクを軽減できます。

---

#### 3. Secureフラグ

CookieにSecureフラグを設定することで、HTTPS通信のみでCookieを送信します。

**config/session.php**

```php
'secure' => env('SESSION_SECURE_COOKIE', true),
```

これにより、盗聴でセッションIDが盗まれるリスクを軽減できます。

---

#### 4. SameSite属性

CookieにSameSite属性を設定することで、CSRF攻撃を防ぎます。

**config/session.php**

```php
'same_site' => 'lax',
```

**SameSite属性の値**：

| 値 | 説明 |
|----|------|
| **strict** | 同じサイトからのリクエストのみでCookieを送信 |
| **lax** | 同じサイトからのリクエスト、または安全なメソッド（GET）でCookieを送信 |
| **none** | すべてのリクエストでCookieを送信（Secureフラグが必要） |

---

#### 5. セッションの有効期限

セッションに有効期限を設定することで、長時間放置されたセッションを無効化します。

**config/session.php**

```php
'lifetime' => 120, // 120分（2時間）
```

---

### 💡 実践例：Remember Me機能

「ログイン状態を保持する」機能を実装する場合、**Remember Me**トークンを使います。

#### ログイン時にRemember Meを有効化

```php
if (Auth::attempt($credentials, $request->filled('remember'))) {
    $request->session()->regenerate();
    return redirect()->intended('/dashboard');
}
```

**コードリーディング**：

*   `Auth::attempt($credentials, $request->filled('remember'))`：第2引数に`true`を渡すと、Remember Meが有効になる

---

#### ビュー

```blade
<form method="POST" action="/login">
    @csrf
    
    <input type="email" name="email" required>
    <input type="password" name="password" required>
    
    <label>
        <input type="checkbox" name="remember">
        ログイン状態を保持する
    </label>
    
    <button type="submit">ログイン</button>
</form>
```

**仕組み**：

*   Remember Meが有効な場合、Laravelは**長期間有効なトークン**をCookieに保存します
*   ブラウザを閉じても、トークンが有効な限り、ログイン状態が維持されます

---

### 🔍 セッションのデバッグ

セッションの内容を確認する方法です。

```php
// セッションの全データを取得
$allData = session()->all();
dd($allData);

// 特定のキーの存在を確認
if (session()->has('user_id')) {
    // ...
}

// セッションIDを取得
$sessionId = session()->getId();
```

---

### 📊 セッションのライフサイクル

```
1. ユーザーが初めてサイトにアクセス
   ↓
2. Laravelがセッションを作成し、セッションIDを発行
   ↓
3. セッションIDをCookieに保存
   ↓
4. ユーザーがログイン
   ↓
5. セッションにユーザーIDを保存
   ↓
6. ユーザーがページを移動
   ↓
7. ブラウザがセッションIDを送信
   ↓
8. Laravelがセッションからユーザーを特定
   ↓
9. ユーザーがログアウト
   ↓
10. セッションを無効化
```

---

## 💡 TIP

### セッションのストレージを変更する

本番環境では、**database**または**redis**ドライバーを使うことを推奨します。

#### databaseドライバーの設定

```bash
php artisan session:table
php artisan migrate
```

**config/session.php**

```php
'driver' => 'database',
```

これにより、セッションがデータベースに保存されます。

---

### セッションのガベージコレクション

古いセッションは、自動的に削除されます。

**config/session.php**

```php
'lottery' => [2, 100], // 2%の確率でガベージコレクションを実行
```

---

### 複数デバイスでのログイン制限

同じユーザーが複数のデバイスでログインすることを制限できます。

```php
Auth::logoutOtherDevices($currentPassword);
```

これにより、他のデバイスのセッションが無効化されます。

---

## ✨ まとめ

*   **認証**は、ユーザーが本人であることを確認するプロセス
*   **HTTP**はステートレスなので、**セッション**と**Cookie**を使ってログイン状態を維持する
*   **Cookie**はブラウザに保存され、**セッション**はサーバーに保存される
*   Laravelは、セッション管理を自動的に行い、複数のドライバーをサポートする
*   **セッションハイジャック**攻撃を防ぐために、セッションIDの再生成、HttpOnlyフラグ、Secureフラグ、SameSite属性を使う
*   ログイン時は`$request->session()->regenerate()`、ログアウト時は`$request->session()->invalidate()`を必ず実行する
*   **Remember Me**機能を使うと、ブラウザを閉じてもログイン状態を維持できる

---
