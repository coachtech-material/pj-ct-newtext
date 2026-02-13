# Tutorial 10-6-1: CSRF保護

## 📖 このチャプターの進め方

このチャプターでは、CSRF、SQLインジェクション、XSSなどの脆弱性と、Laravelの保護機能について学びます。コードが出てきますが、まずは「どんな攻撃があり、どう防ぐのか」を理解しながら読み進めてください。実際に手を動かすのは、チャプターの最後にあるハンズオン（10-6-6）で行います。

---

## 🎯 このセクションで学ぶこと

*   CSRF（クロスサイトリクエストフォージェリ）攻撃の仕組みを理解する。
*   LaravelのCSRF保護機能を使って、攻撃を防ぐ方法を学ぶ。
*   `@csrf`ディレクティブの役割を理解する。

---

## 導入：Webアプリケーションの脆弱性を理解する

これまで、Laravelの様々な機能を学んできました。しかし、Webアプリケーションを開発する上で、**セキュリティ**は非常に重要です。

このChapterでは、Webアプリケーションの代表的な脆弱性と、Laravelがどのように保護しているかを学びます。

最初に学ぶのは、CSRF（Cross-Site Request Forgery）攻撃です。

---

## 詳細解説

### 🔓 CSRF攻撃とは

CSRF（クロスサイトリクエストフォージェリ）とは、**ユーザーの意図しないリクエストを、攻撃者が強制的に送信させる攻撃**です。

#### 攻撃のシナリオ

1. ユーザーがSNSサイト（`example.com`）にログインしている
2. ユーザーが悪意のあるサイト（`evil.com`）にアクセスする
3. `evil.com`に、以下のような罠が仕掛けられている

```html
<!-- evil.comのページ -->
<form action="https://example.com/posts/delete/123" method="POST">
    <input type="submit" value="無料プレゼントをもらう">
</form>
```

4. ユーザーがボタンをクリックすると、**ユーザーの知らないうちに**、`example.com`に削除リクエストが送信される
5. ユーザーはログイン済みなので、リクエストが成功し、投稿が削除されてしまう

**身近な例で理解する**：
これは、あなたの銀行口座にログインしている状態で、悪意のあるサイトが「あなたの名義で送金リクエストを送信する」ようなものです。

---

### 🛡️ LaravelのCSRF保護

Laravelは、**CSRFトークン**を使って、CSRF攻撃を防ぎます。

#### CSRFトークンの仕組み

1. Laravelがセッション（サーバー側）に**ランダムなトークン**を生成・保存する
2. フォームを表示する際に、トークンを**隠しフィールド**として埋め込む
3. ユーザーがフォームを送信すると、隠しフィールドのトークンがサーバーに送られる
4. Laravelは、セッションに保存されたトークンと、送信されたトークンが一致するかを検証する
5. 一致すれば、リクエストを受け付ける
6. 一致しなければ、リクエストを拒否する（419エラー）

**重要なポイント**：
攻撃者のサイト（`evil.com`）からは、ユーザーのセッションに保存されたCSRFトークンを知ることができません。そのため、正しいトークンを含むリクエストを送信できず、攻撃は失敗します。

---

### 🔧 @csrfディレクティブの使い方

Laravelでは、フォームに`@csrf`ディレクティブを追加するだけで、CSRF保護が有効になります。

#### フォームの例

```blade
<form action="/posts" method="POST">
    @csrf
    
    <input type="text" name="title" placeholder="タイトル">
    <textarea name="content" placeholder="本文"></textarea>
    
    <button type="submit">投稿する</button>
</form>
```

**生成されるHTML**：

```html
<form action="/posts" method="POST">
    <input type="hidden" name="_token" value="ランダムな文字列">
    
    <input type="text" name="title" placeholder="タイトル">
    <textarea name="content" placeholder="本文"></textarea>
    
    <button type="submit">投稿する</button>
</form>
```

**コードリーディング**：

*   `@csrf`：CSRFトークンを含む隠しフィールドを自動生成
*   `<input type="hidden" name="_token" value="...">`：Laravelが自動的に検証するトークン

---

### ❌ @csrfを忘れるとどうなるか

`@csrf`を忘れると、フォームを送信した際に**419エラー**（Page Expired）が表示されます。

```
419 | Page Expired
```

これは、Laravelが「CSRFトークンがない、または間違っている」と判断したためです。

---

### 🔍 CSRFトークンの検証

Laravelは、**ミドルウェア**を使って、CSRFトークンを自動的に検証します。

#### app/Http/Kernel.php

```php
protected $middlewareGroups = [
    'web' => [
        // ...
        \App\Http\Middleware\VerifyCsrfToken::class,
        // ...
    ],
];
```

**コードリーディング**：

*   `VerifyCsrfToken`ミドルウェアが、すべてのPOST/PUT/PATCH/DELETEリクエストでCSRFトークンを検証します
*   GETリクエストは検証されません（GETは「読み取り専用」であるべきため）

---

### 🚫 特定のURLをCSRF保護から除外する

API エンドポイントなど、CSRF保護が不要な場合は、除外することができます。

#### app/Http/Middleware/VerifyCsrfToken.php

```php
<?php

namespace App\Http\Middleware;

use Illuminate\Foundation\Http\Middleware\VerifyCsrfToken as Middleware;

class VerifyCsrfToken extends Middleware
{
    protected $except = [
        'api/*',  // /api/で始まるURLを除外
        'webhook/payment',  // 特定のURLを除外
    ];
}
```

**注意**：
除外する場合は、**他のセキュリティ対策**（APIトークン認証など）を必ず実装してください。

---

### 🌐 AjaxリクエストでのCSRF保護

> 💡 **補足**: 以下の内容はJavaScript（Ajax）を使用する際のテクニックです。JavaScriptについては別途学習が必要ですが、今は「こういうことができる」程度の理解でOKです。

Ajaxリクエストでも、CSRFトークンを送信する必要があります。

#### JavaScriptでCSRFトークンを取得

```blade
<meta name="csrf-token" content="{{ csrf_token() }}">
```

#### Axiosの設定

```javascript
// resources/js/bootstrap.js
import axios from 'axios';

axios.defaults.headers.common['X-CSRF-TOKEN'] = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
```

#### Ajaxリクエストの例

```javascript
axios.post('/posts', {
    title: '新しい投稿',
    content: 'これはテストです'
})
.then(response => {
    console.log('投稿成功');
})
.catch(error => {
    console.error('エラー', error);
});
```

**コードリーディング**：

*   `X-CSRF-TOKEN`ヘッダーにトークンを含めることで、Laravelが自動的に検証します

---

### 🚀 実践例：投稿削除フォーム

CSRF保護を使って、投稿を安全に削除するフォームの例です。

#### ビュー

```blade
<form action="/posts/{{ $post->id }}" method="POST" onsubmit="return confirm('本当に削除しますか？')">
    @csrf
    @method('DELETE')
    
    <button type="submit" class="btn btn-danger">削除</button>
</form>
```

**コードリーディング**：

*   `@csrf`：CSRF保護
*   `@method('DELETE')`：HTMLフォームはGETとPOSTしかサポートしないため、DELETEメソッドを指定
*   `onsubmit="return confirm(...)"`：削除前に確認ダイアログを表示

#### ルート

```php
Route::delete('/posts/{id}', [PostController::class, 'destroy']);
```

#### コントローラー

```php
public function destroy($id)
{
    $post = Post::findOrFail($id);
    $post->delete();
    
    return redirect('/posts')->with('success', '投稿を削除しました');
}
```

---

## 💡 TIP

### CSRFトークンの有効期限

CSRFトークンは、**セッション**に保存されます。セッションが切れると、トークンも無効になります。

**対策**：
長時間フォームを開いたままにすると、トークンが期限切れになることがあります。この場合、ユーザーに「ページを再読み込みしてください」と案内しましょう。

### CSRF保護が不要なケース

以下の場合は、CSRF保護が不要です：

*   **GETリクエスト**：読み取り専用の操作
*   **APIエンドポイント**：トークン認証を使用する場合
*   **Webhook**：外部サービスからのコールバック

---

## ✨ まとめ

*   **CSRF攻撃**は、ユーザーの意図しないリクエストを強制的に送信させる攻撃
*   Laravelは、**CSRFトークン**を使って、CSRF攻撃を防ぐ
*   フォームに`@csrf`ディレクティブを追加するだけで、CSRF保護が有効になる
*   CSRFトークンがない、または間違っている場合は、419エラーが表示される
*   Ajaxリクエストでは、`X-CSRF-TOKEN`ヘッダーにトークンを含める
*   APIエンドポイントなど、CSRF保護が不要な場合は、`VerifyCsrfToken`ミドルウェアで除外できる

---
