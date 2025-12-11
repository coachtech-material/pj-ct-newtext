# Tutorial 9-2-4: フォームの作成

## 🎯 このセクションで学ぶこと

*   Bladeでフォームを作成できるようになる。
*   CSRFトークンの役割を理解し、`@csrf`ディレクティブを使えるようになる。
*   フォームからデータを送信し、コントローラーで受け取れるようになる。

---

## 導入:フォームとセキュリティ

Webアプリケーションでは、ユーザーからデータを受け取るために、フォームを使います。例えば、ユーザー登録、ログイン、投稿の作成などです。

しかし、フォームには**CSRF（Cross-Site Request Forgery）攻撃**というセキュリティリスクがあります。Laravelは、このリスクを防ぐために、**CSRFトークン**という仕組みを標準で提供しています。

このセクションでは、Bladeでフォームを作成し、CSRFトークンを使ってセキュリティを確保する方法を学びます。

---

## 詳細解説

### 🔐 CSRF攻撃とは？

CSRF攻撃とは、**ユーザーが意図しない操作を、悪意のあるサイトから実行させる攻撃**です。

#### 攻撃の流れ

1. ユーザーがWebアプリケーション（例：銀行サイト）にログインしている
2. ユーザーが悪意のあるサイト（例：罠サイト）にアクセスする
3. 罠サイトが、銀行サイトに対して「送金」のリクエストを送信する
4. ユーザーは気づかないうちに、送金が実行されてしまう

#### CSRFトークンによる防御

Laravelは、フォームに**CSRFトークン**という秘密の文字列を埋め込みます。このトークンは、サーバー側で生成され、セッションに保存されます。

フォームが送信されると、Laravelは以下をチェックします。

*   フォームに含まれるCSRFトークン
*   セッションに保存されているCSRFトークン

この2つが一致しない場合、リクエストは拒否されます。これにより、悪意のあるサイトからのリクエストを防ぐことができます。

---

### 📝 基本的なフォームの作成

#### ステップ1: ルートを定義する

**`routes/web.php`**

```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\PostController;

Route::get('/posts/create', [PostController::class, 'create']);
Route::post('/posts', [PostController::class, 'store']);
```

**コードリーディング**

*   `GET /posts/create`: フォームを表示するエンドポイント
*   `POST /posts`: フォームから送信されたデータを処理するエンドポイント

#### ステップ2: コントローラーを作成する

```bash
docker compose exec php php artisan make:controller PostController
```

**`app/Http/Controllers/PostController.php`**

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Post;

class PostController extends Controller
{
    /**
     * フォームを表示
     */
    public function create()
    {
        return view('posts.create');
    }

    /**
     * フォームから送信されたデータを処理
     */
    public function store(Request $request)
    {
        // バリデーション
        $validated = $request->validate([
            'title' => 'required|max:255',
            'content' => 'required',
        ]);

        // 投稿を作成
        $post = Post::create($validated);

        // リダイレクト
        return redirect('/posts')->with('success', '投稿を作成しました');
    }
}
```

**コードリーディング**

*   `create()`: フォームを表示するメソッド
*   `store()`: フォームから送信されたデータを処理するメソッド
*   `$request->validate([...])`: バリデーションを実行します（次のセクションで詳しく学びます）
*   `redirect('/posts')->with('success', '...')`: `/posts`にリダイレクトし、成功メッセージを渡します

#### ステップ3: Bladeビューを作成する

```bash
docker compose exec php mkdir -p resources/views/posts
docker compose exec php touch resources/views/posts/create.blade.php
```

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
        <input type="text" id="title" name="title" value="{{ old('title') }}">

        <label for="content">内容</label>
        <textarea id="content" name="content" rows="5">{{ old('content') }}</textarea>

        <button type="submit">投稿する</button>
    </form>
</body>
</html>
```

**コードリーディング**

*   `<form method="POST" action="/posts">`: POSTメソッドで`/posts`にデータを送信します。
*   `@csrf`: CSRFトークンを自動的に埋め込みます。**これを忘れると、419エラーが発生します。**
*   `value="{{ old('title') }}"`: バリデーションエラーが発生した際に、入力値を保持します。
*   `{{ old('content') }}`: テキストエリアの場合、タグの間に`old()`を配置します。

---

### 🔍 `@csrf`の仕組み

`@csrf`ディレクティブは、以下のHTMLを生成します。

```html
<input type="hidden" name="_token" value="ランダムな文字列">
```

このトークンは、Laravelが自動的に検証します。トークンが一致しない場合、`419 Page Expired`エラーが返されます。

---

### 🎨 フォームの種類

HTMLのフォームは、`GET`と`POST`の2つのメソッドしかサポートしていません。しかし、REST APIでは、`PUT`、`PATCH`、`DELETE`なども使います。

Laravelでは、`@method`ディレクティブを使って、これらのメソッドをシミュレートできます。

#### 例: 投稿の更新（PUT）

**`routes/web.php`**

```php
Route::put('/posts/{id}', [PostController::class, 'update']);
```

**Bladeビュー**

```blade
<form method="POST" action="/posts/{{ $post->id }}">
    @csrf
    @method('PUT')

    <label for="title">タイトル</label>
    <input type="text" id="title" name="title" value="{{ old('title', $post->title) }}">

    <label for="content">内容</label>
    <textarea id="content" name="content" rows="5">{{ old('content', $post->content) }}</textarea>

    <button type="submit">更新する</button>
</form>
```

**コードリーディング**

*   `@method('PUT')`: フォームのメソッドを`PUT`にシミュレートします。
*   `old('title', $post->title)`: バリデーションエラーがない場合は、`$post->title`を表示します。

#### 例: 投稿の削除（DELETE）

```blade
<form method="POST" action="/posts/{{ $post->id }}">
    @csrf
    @method('DELETE')

    <button type="submit">削除する</button>
</form>
```

---

### 🚀 フォームのベストプラクティス

#### 1. 常に`@csrf`を付ける

POSTリクエストを送信するフォームには、**必ず`@csrf`を付ける**必要があります。

#### 2. `old()`で入力値を保持する

バリデーションエラーが発生した際に、ユーザーが入力した値を保持することで、ユーザー体験が向上します。

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

#### 3. `action`属性には絶対パスを使う

```blade
<form method="POST" action="/posts">
```

または、`route()`ヘルパーを使います。

```blade
<form method="POST" action="{{ route('posts.store') }}">
```

---

### 💡 TIP: フォームリクエストを使う

複雑なバリデーションは、**フォームリクエスト（Form Request）**というクラスに分離することができます。

```bash
docker compose exec php php artisan make:request StorePostRequest
```

**`app/Http/Requests/StorePostRequest.php`**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StorePostRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'title' => 'required|max:255',
            'content' => 'required',
        ];
    }
}
```

**コントローラーで使用**

```php
public function store(StorePostRequest $request)
{
    $validated = $request->validated();
    $post = Post::create($validated);
    return redirect('/posts')->with('success', '投稿を作成しました');
}
```

---

## ✨ まとめ

このセクションでは、Bladeでフォームを作成し、CSRFトークンを使ってセキュリティを確保する方法を学びました。

*   フォームには、CSRF攻撃というセキュリティリスクがある。
*   Laravelは、`@csrf`ディレクティブでCSRFトークンを自動的に埋め込む。
*   `@method`ディレクティブで、`PUT`、`PATCH`、`DELETE`メソッドをシミュレートできる。
*   `old()`ヘルパーで、バリデーションエラー時に入力値を保持できる。
*   フォームリクエストを使うことで、バリデーションロジックを分離できる。

次のセクションでは、バリデーションエラーをBladeで表示する方法を学びます。

---

## 📝 学習のポイント

- [ ] CSRF攻撃とCSRFトークンの役割を理解した。
- [ ] `@csrf`ディレクティブを使って、フォームにCSRFトークンを埋め込める。
- [ ] `@method`ディレクティブで、`PUT`、`DELETE`メソッドをシミュレートできる。
- [ ] `old()`ヘルパーで、バリデーションエラー時に入力値を保持できる。
