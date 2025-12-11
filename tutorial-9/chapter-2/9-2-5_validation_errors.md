# Tutorial 9-2-5: バリデーションエラーの表示

## 🎯 このセクションで学ぶこと

*   バリデーションエラーをBladeで表示できるようになる。
*   `$errors`変数を使って、エラーメッセージを取得できるようになる。
*   ユーザーフレンドリーなエラー表示を実装できるようになる。

---

## 導入：エラーメッセージはユーザーへの「道しるべ」

前のセクションで、フォームを作成し、CSRFトークンを使ってセキュリティを確保する方法を学びました。しかし、ユーザーが不正なデータを入力した場合、どのように伝えれば良いでしょうか？

例えば、以下のような状況です。

*   タイトルが空欄のまま送信された
*   メールアドレスの形式が間違っている
*   パスワードが短すぎる

これらのエラーを、**わかりやすく、親切に表示する**ことで、ユーザー体験が大きく向上します。

このセクションでは、Laravelのバリデーションエラーを、Bladeで表示する方法を学びます。

---

## 詳細解説

### 🔍 `$errors`変数

Laravelでは、バリデーションエラーが発生すると、自動的に`$errors`という変数がBladeに渡されます。この変数を使って、エラーメッセージを表示できます。

#### `$errors`の主なメソッド

| メソッド | 説明 |
|:---|:---|
| `$errors->any()` | エラーが1つでもあれば`true`を返す |
| `$errors->has('title')` | `title`フィールドにエラーがあれば`true`を返す |
| `$errors->first('title')` | `title`フィールドの最初のエラーメッセージを返す |
| `$errors->get('title')` | `title`フィールドの全てのエラーメッセージを配列で返す |
| `$errors->all()` | 全てのエラーメッセージを配列で返す |

---

### 📝 全てのエラーをまとめて表示する

最もシンプルな方法は、全てのエラーメッセージをまとめて表示することです。

**`resources/views/posts/create.blade.php`**

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>投稿作成</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .error-box {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 4px;
        }
        .error-box ul {
            margin: 0;
            padding-left: 20px;
        }
        label {
            display: block;
            margin-top: 10px;
        }
        input, textarea {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
        }
        button {
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>投稿作成</h1>

    @if ($errors->any())
        <div class="error-box">
            <strong>入力内容に誤りがあります</strong>
            <ul>
                @foreach ($errors->all() as $error)
                    <li>{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form method="POST" action="/posts">
        @csrf

        <label for="title">タイトル</label>
        <input type="text" id="title" name="title" value="{{ old('title') }}">

        <label for="content">内容</label>
        <textarea id="content" name="content" rows="5">{{ old('content') }}</textarea>

        <button type="submit">投稿する</button>
    </form>
</body>
</html>
```

**コードリーディング**

*   `@if ($errors->any())`: エラーが1つでもある場合、エラーボックスを表示します。
*   `@foreach ($errors->all() as $error)`: 全てのエラーメッセージをループで表示します。

---

### 🎨 フィールドごとにエラーを表示する

より親切なUIにするために、各フィールドの下にエラーメッセージを表示することもできます。

**`resources/views/posts/create.blade.php`**

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>投稿作成</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        label {
            display: block;
            margin-top: 10px;
        }
        input, textarea {
            width: 100%;
            padding: 8px;
            margin-top: 5px;
            border: 1px solid #ddd;
        }
        input.error, textarea.error {
            border-color: #dc3545;
        }
        .error-message {
            color: #dc3545;
            font-size: 14px;
            margin-top: 5px;
        }
        button {
            margin-top: 15px;
            padding: 10px 20px;
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>投稿作成</h1>

    <form method="POST" action="/posts">
        @csrf

        <label for="title">タイトル</label>
        <input 
            type="text" 
            id="title" 
            name="title" 
            value="{{ old('title') }}"
            class="{{ $errors->has('title') ? 'error' : '' }}"
        >
        @if ($errors->has('title'))
            <div class="error-message">{{ $errors->first('title') }}</div>
        @endif

        <label for="content">内容</label>
        <textarea 
            id="content" 
            name="content" 
            rows="5"
            class="{{ $errors->has('content') ? 'error' : '' }}"
        >{{ old('content') }}</textarea>
        @if ($errors->has('content'))
            <div class="error-message">{{ $errors->first('content') }}</div>
        @endif

        <button type="submit">投稿する</button>
    </form>
</body>
</html>
```

**コードリーディング**

*   `class="{{ $errors->has('title') ? 'error' : '' }}"`: エラーがある場合、`error`クラスを追加します。
*   `@if ($errors->has('title'))`: `title`フィールドにエラーがある場合、エラーメッセージを表示します。
*   `{{ $errors->first('title') }}`: `title`フィールドの最初のエラーメッセージを表示します。

---

### 🌐 エラーメッセージの日本語化

Laravelのバリデーションエラーメッセージは、デフォルトでは英語です。日本語化するには、言語ファイルをインストールします。

#### ステップ1: 言語ファイルをインストールする

```bash
docker compose exec php php artisan lang:publish
```

これにより、`lang/en`ディレクトリが作成されます。

#### ステップ2: 日本語の言語ファイルをダウンロードする

GitHubから日本語の言語ファイルをダウンロードします。

```bash
docker compose exec php git clone https://github.com/Laravel-Lang/lang.git temp_lang
docker compose exec php cp -r temp_lang/locales/ja lang/
docker compose exec php rm -rf temp_lang
```

#### ステップ3: デフォルトのロケールを日本語に設定する

**`config/app.php`**

```php
'locale' => 'ja',
```

これで、バリデーションエラーメッセージが日本語で表示されます。

---

### 🚀 カスタムエラーメッセージ

特定のフィールドに対して、カスタムエラーメッセージを設定することもできます。

**コントローラー**

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'content' => 'required',
    ], [
        'title.required' => 'タイトルは必須です',
        'title.max' => 'タイトルは255文字以内で入力してください',
        'content.required' => '内容は必須です',
    ]);

    $post = Post::create($validated);
    return redirect('/posts')->with('success', '投稿を作成しました');
}
```

**コードリーディング**

*   `validate()`の第2引数に、カスタムエラーメッセージを配列で渡します。
*   `'title.required'`: `title`フィールドの`required`ルールに対するメッセージ

---

### 💡 TIP: `@error`ディレクティブ

Laravel 5.8以降では、`@error`ディレクティブを使って、よりシンプルにエラーを表示できます。

```blade
<label for="title">タイトル</label>
<input type="text" id="title" name="title" value="{{ old('title') }}">
@error('title')
    <div class="error-message">{{ $message }}</div>
@enderror
```

**コードリーディング**

*   `@error('title')`: `title`フィールドにエラーがある場合、内部のコードを実行します。
*   `{{ $message }}`: エラーメッセージを表示します。

---

### 🎯 成功メッセージの表示

エラーだけでなく、成功メッセージも表示することで、ユーザー体験が向上します。

**コントローラー**

```php
return redirect('/posts')->with('success', '投稿を作成しました');
```

**Bladeビュー**

```blade
@if (session('success'))
    <div class="success-box">
        {{ session('success') }}
    </div>
@endif
```

**CSS**

```css
.success-box {
    background-color: #d4edda;
    border: 1px solid #c3e6cb;
    color: #155724;
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 4px;
}
```

---

## ✨ まとめ

このセクションでは、Laravelのバリデーションエラーを、Bladeで表示する方法を学びました。

*   `$errors`変数を使って、バリデーションエラーを取得できる。
*   `$errors->any()`で、エラーの有無をチェックできる。
*   `$errors->first('title')`で、特定のフィールドの最初のエラーメッセージを取得できる。
*   `@error`ディレクティブを使うと、よりシンプルにエラーを表示できる。
*   言語ファイルをインストールすることで、エラーメッセージを日本語化できる。
*   カスタムエラーメッセージを設定することで、よりわかりやすいメッセージを表示できる。

これで、Chapter 2「ビューとテンプレート」の全5セクションが完了しました。次は、Chapter 3「データベースとマイグレーション」の残りのセクションを執筆します。

---

## 📝 学習のポイント

- [ ] `$errors`変数を使って、バリデーションエラーを取得できる。
- [ ] `$errors->any()`、`$errors->has()`、`$errors->first()`を使い分けられる。
- [ ] `@error`ディレクティブを使って、シンプルにエラーを表示できる。
- [ ] 言語ファイルをインストールして、エラーメッセージを日本語化できる。
- [ ] カスタムエラーメッセージを設定できる。
