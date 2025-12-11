# Tutorial 11-4-1: CSRF保護

## 🎯 このセクションで学ぶこと

*   CSRF（Cross-Site Request Forgery）攻撃とその対策を学ぶ。
*   LaravelのCSRF保護機能を理解する。
*   フォームにCSRFトークンを追加する方法を学ぶ。

---

## 導入：なぜCSRF保護が重要なのか

**CSRF（Cross-Site Request Forgery）攻撃**とは、**ユーザーの意図しないリクエストを送信させる攻撃**です。

CSRF攻撃を受けると、以下のような被害が発生する可能性があります。

*   **データの改ざん**: タスクやユーザー情報が不正に変更される
*   **不正な操作**: ユーザーの意図しない操作（削除、購入など）が実行される

このセクションでは、**CSRF攻撃**について学び、Laravelが提供するCSRF保護機能を理解します。

---

## 詳細解説

### 🔍 CSRF攻撃とは

**CSRF（Cross-Site Request Forgery）攻撃**とは、**ユーザーの意図しないリクエストを送信させる攻撃**です。

---

#### CSRF攻撃の例

1. ユーザーがタスク管理システムにログインしている
2. 攻撃者が作成した悪意のあるWebサイトにアクセスする
3. そのWebサイトには、以下のようなHTMLが埋め込まれている

```html
<form action="http://task-app.com/tasks/1" method="POST">
    <input type="hidden" name="_method" value="DELETE">
</form>
<script>
    document.forms[0].submit();
</script>
```

4. ユーザーが気づかないうちに、タスクが削除される

---

### 🔍 CSRF攻撃が成功する理由

CSRF攻撃が成功する理由は、**ブラウザが自動的にCookieを送信する**からです。

1. ユーザーがタスク管理システムにログインすると、ブラウザにセッションCookieが保存される
2. 攻撃者のWebサイトから `http://task-app.com/tasks/1` にリクエストを送信すると、ブラウザは自動的にセッションCookieを送信する
3. サーバーは、セッションCookieを確認して、ユーザーが認証済みだと判断する
4. タスクが削除される

---

### 🔍 LaravelのCSRF保護

Laravelは、**CSRFトークン**を使ってCSRF攻撃を防ぎます。

**CSRFトークン**とは、**フォームごとに生成されるランダムな文字列**です。

---

#### CSRFトークンの仕組み

1. フォームを表示するとき、サーバーはCSRFトークンを生成し、フォームに埋め込む
2. フォームを送信するとき、CSRFトークンも一緒に送信される
3. サーバーは、送信されたCSRFトークンが正しいかを確認する
4. CSRFトークンが正しければ、リクエストを処理する
5. CSRFトークンが間違っていれば、リクエストを拒否する

攻撃者のWebサイトからリクエストを送信する場合、CSRFトークンを取得できないため、リクエストは拒否されます。

---

### 🔍 Bladeテンプレートで@csrfを使う

Bladeテンプレートでは、`@csrf`ディレクティブを使ってCSRFトークンを追加します。

**ファイル**: `resources/views/tasks/create.blade.php`

```blade
<form method="POST" action="{{ route('tasks.store') }}">
    @csrf

    <div>
        <label for="title">タイトル</label>
        <input type="text" id="title" name="title" required>
    </div>

    <button type="submit">作成</button>
</form>
```

`@csrf`は、以下のHTMLに展開されます。

```html
<input type="hidden" name="_token" value="ランダムな文字列">
```

---

### 🔍 CSRFトークンの確認

ブラウザの開発者ツールで、CSRFトークンを確認できます。

1. ブラウザでフォームを表示する
2. 開発者ツールを開く（F12キー）
3. 「Elements」タブで、`<input type="hidden" name="_token">` を探す
4. `value`属性に、CSRFトークンが表示される

---

### 🔍 CSRFトークンがない場合のエラー

CSRFトークンがない場合、Laravelは `419 Page Expired` エラーを返します。

**エラーメッセージ**:

```
419 | Page Expired
```

このエラーが表示された場合、フォームに `@csrf` を追加します。

---

### 🔍 AjaxリクエストでCSRFトークンを送信する

Ajaxリクエストでも、CSRFトークンを送信する必要があります。

**方法1**: metaタグにCSRFトークンを埋め込む

**ファイル**: `resources/views/layouts/app.blade.php`

```blade
<head>
    <meta name="csrf-token" content="{{ csrf_token() }}">
</head>
```

**JavaScriptでCSRFトークンを取得**:

```javascript
const token = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

fetch('/tasks', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRF-TOKEN': token
    },
    body: JSON.stringify({ title: 'New Task' })
});
```

---

**方法2**: Axiosを使う

Axiosは、自動的にCSRFトークンを送信します。

```javascript
axios.post('/tasks', { title: 'New Task' });
```

Axiosは、`<meta name="csrf-token">`からCSRFトークンを取得し、`X-CSRF-TOKEN`ヘッダーに追加します。

---

### 🔍 CSRF保護を無効にする（非推奨）

特定のルートでCSRF保護を無効にすることもできますが、**セキュリティ上のリスクがあるため、推奨されません**。

**ファイル**: `app/Http/Middleware/VerifyCsrfToken.php`

```php
protected $except = [
    'api/*',  // APIルートはCSRF保護を無効にする
];
```

---

### 💡 TIP: セッションの有効期限

CSRFトークンは、セッションに保存されます。セッションの有効期限が切れると、CSRFトークンも無効になります。

セッションの有効期限は、`config/session.php`で設定できます。

```php
'lifetime' => 120,  // 120分
```

---

### 🚨 よくある間違い

#### 間違い1: @csrfを忘れる

**対処法**: すべてのPOST、PUT、DELETE、PATCHリクエストのフォームに `@csrf` を追加します。

---

#### 間違い2: Ajaxリクエストでヘッダーを設定していない

**対処法**: `X-CSRF-TOKEN`ヘッダーにCSRFトークンを設定します。

---

#### 間違い3: セッションの有効期限が切れている

**対処法**: ページをリロードして、新しいCSRFトークンを取得します。

---

## ✨ まとめ

このセクションでは、CSRF保護について学びました。

*   CSRF攻撃は、ユーザーの意図しないリクエストを送信させる攻撃。
*   LaravelはCSRFトークンを使ってCSRF攻撃を防ぐ。
*   Bladeテンプレートでは、`@csrf`ディレクティブを使ってCSRFトークンを追加する。
*   AjaxリクエストでもCSRFトークンを送信する必要がある。

次のセクションでは、SQLインジェクション対策について学びます。

---

## 📝 学習のポイント

- [ ] CSRF攻撃とその対策を理解した。
- [ ] LaravelのCSRF保護機能を理解した。
- [ ] フォームに`@csrf`を追加した。
- [ ] AjaxリクエストでCSRFトークンを送信する方法を学んだ。
