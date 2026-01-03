# Tutorial 9-2-3: フォームとデータ送信

## 🎯 このセクションで学ぶこと

*   セキュリティ：**`@csrf`**の必須性を理解し、正しく使えるようになる。
*   RESTful対応：**`@method('PUT')` / `@method('DELETE')`**の必要性を理解する。
*   UXへの配慮：**`old('name')`**による入力値保持、**`@error('name')`**によるエラー表示を実装できるようになる。

---

## 導入：フォームは「データの入り口」

Webアプリケーションでは、ユーザーからデータを受け取るために、フォームを使います。例えば、ユーザー登録、ログイン、投稿の作成などです。

フォームは「データの入り口」であり、**セキュリティ**と**ユーザー体験（UX）**の両方を考慮する必要があります。

*   **セキュリティ**: CSRF攻撃を防ぐ
*   **UX**: 入力エラー時に値を保持し、エラーメッセージを表示する

このセクションでは、これらを実現するBladeの機能を学びます。

---

## 詳細解説

### 🔐 セキュリティ：`@csrf`の必須性

#### CSRF攻撃とは？

**CSRF（Cross-Site Request Forgery）攻撃**とは、ユーザーが意図しない操作を、悪意のあるサイトから実行させる攻撃です。

**攻撃の流れ**

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

#### `@csrf`の使い方

```blade
<form method="POST" action="/posts">
    @csrf
    
    <input type="text" name="title">
    <button type="submit">送信</button>
</form>
```

`@csrf`ディレクティブは、以下のHTMLを生成します。

```html
<input type="hidden" name="_token" value="ランダムな文字列">
```

> ⚠️ **重要**: POSTリクエストを送信するフォームには、**必ず`@csrf`を付ける**必要があります。これを忘れると、**419 Page Expired**エラーが発生します。

---

### 🎨 RESTful対応：`@method`

HTMLのフォームは、`GET`と`POST`の2つのメソッドしかサポートしていません。しかし、RESTful設計では、`PUT`、`PATCH`、`DELETE`なども使います。

| HTTPメソッド | 用途 |
|:---|:---|
| GET | データの取得（一覧、詳細） |
| POST | データの作成 |
| PUT / PATCH | データの更新 |
| DELETE | データの削除 |

Laravelでは、`@method`ディレクティブを使って、これらのメソッドをシミュレートできます。

#### 例：投稿の更新（PUT）

```blade
<form method="POST" action="/posts/{{ $post->id }}">
    @csrf
    @method('PUT')
    
    <input type="text" name="title" value="{{ $post->title }}">
    <button type="submit">更新する</button>
</form>
```

**コードリーディング**

*   `method="POST"`: HTMLフォームはPOSTで送信します。
*   `@method('PUT')`: Laravelに「これはPUTリクエストだ」と伝えます。

`@method('PUT')`は、以下のHTMLを生成します。

```html
<input type="hidden" name="_method" value="PUT">
```

#### 例：投稿の削除（DELETE）

```blade
<form method="POST" action="/posts/{{ $post->id }}">
    @csrf
    @method('DELETE')
    
    <button type="submit">削除する</button>
</form>
```

---

### 📝 UXへの配慮：`old()`による入力値保持

バリデーションエラーが発生した際に、ユーザーが入力した値を保持することで、ユーザー体験が向上します。

#### 基本的な使い方

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

`old('title')`は、前回のリクエストで送信された`title`の値を返します。バリデーションエラーがなければ、空文字を返します。

#### デフォルト値を指定する

編集フォームでは、既存のデータをデフォルト値として表示したい場合があります。

```blade
<input type="text" name="title" value="{{ old('title', $post->title) }}">
```

**動作の流れ**

1. 初回表示時: `old('title')`は空なので、`$post->title`が表示される
2. バリデーションエラー時: `old('title')`に前回の入力値が入っているので、それが表示される

#### テキストエリアの場合

```blade
<textarea name="content">{{ old('content', $post->content) }}</textarea>
```

テキストエリアは`value`属性がないため、タグの間に値を配置します。

---

### 🚨 UXへの配慮：`@error`によるエラー表示

バリデーションエラーが発生した際に、エラーメッセージを表示することで、ユーザーは何を修正すべきかわかります。

#### 基本的な使い方

```blade
<input type="text" name="title" value="{{ old('title') }}">

@error('title')
    <p style="color: red;">{{ $message }}</p>
@enderror
```

**コードリーディング**

*   `@error('title')`: `title`フィールドにエラーがある場合に実行されます。
*   `{{ $message }}`: エラーメッセージを表示します。
*   `@enderror`: エラーブロックの終了を示します。

#### エラー時にスタイルを変更する

```blade
<input 
    type="text" 
    name="title" 
    value="{{ old('title') }}"
    style="@error('title') border-color: red; @enderror"
>

@error('title')
    <p style="color: red;">{{ $message }}</p>
@enderror
```

#### 全てのエラーを一覧表示する

```blade
@if ($errors->any())
    <div style="background-color: #fee; padding: 10px; margin-bottom: 20px;">
        <ul>
            @foreach ($errors->all() as $error)
                <li style="color: red;">{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif
```

---

### 🏃 実践例：投稿作成フォーム

これまで学んだ機能を組み合わせた、完全なフォームの例を見てみましょう。

#### ルーティング（`routes/web.php`）

```php
use App\Http\Controllers\PostController;

Route::get('/posts/create', [PostController::class, 'create']);
Route::post('/posts', [PostController::class, 'store']);
```

#### コントローラー（`PostController.php`）

```php
public function create()
{
    return view('posts.create');
}

public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'content' => 'required',
    ]);

    Post::create($validated);

    return redirect('/posts')->with('success', '投稿を作成しました');
}
```

#### Blade（`resources/views/posts/create.blade.php`）

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>投稿作成</title>
    <style>
        .error { color: red; font-size: 0.9em; }
        .error-input { border-color: red; }
    </style>
</head>
<body>
    <h1>投稿作成</h1>

    {{-- 全エラーの一覧表示 --}}
    @if ($errors->any())
        <div style="background-color: #fee; padding: 10px; margin-bottom: 20px;">
            <p>入力内容に問題があります。</p>
            <ul>
                @foreach ($errors->all() as $error)
                    <li class="error">{{ $error }}</li>
                @endforeach
            </ul>
        </div>
    @endif

    <form method="POST" action="/posts">
        @csrf

        <div>
            <label for="title">タイトル</label>
            <input 
                type="text" 
                id="title" 
                name="title" 
                value="{{ old('title') }}"
                class="@error('title') error-input @enderror"
            >
            @error('title')
                <p class="error">{{ $message }}</p>
            @enderror
        </div>

        <div>
            <label for="content">内容</label>
            <textarea 
                id="content" 
                name="content" 
                rows="5"
                class="@error('content') error-input @enderror"
            >{{ old('content') }}</textarea>
            @error('content')
                <p class="error">{{ $message }}</p>
            @enderror
        </div>

        <button type="submit">投稿する</button>
    </form>
</body>
</html>
```

**コードリーディング**

*   `@csrf`: CSRF対策のトークンを埋め込む。
*   `old('title')`: バリデーションエラー時に入力値を保持。
*   `@error('title')`: タイトルにエラーがあればメッセージを表示。
*   `$errors->any()`: エラーが1つでもあれば、全エラーを一覧表示。

---

### 📋 フォームのチェックリスト

フォームを作成する際は、以下のチェックリストを確認しましょう。

| チェック項目 | 対応 |
|:---|:---|
| CSRF対策 | `@csrf`を付ける |
| PUT/DELETE対応 | `@method('PUT')`などを付ける |
| 入力値保持 | `old('name')`を使う |
| エラー表示 | `@error('name')`を使う |
| 編集フォームのデフォルト値 | `old('name', $model->name)`を使う |

---

## ✨ まとめ

このセクションでは、Bladeでフォームを作成し、セキュリティとUXを確保する方法を学びました。

*   **`@csrf`**: CSRF攻撃を防ぐために、POSTフォームには必ず付ける。忘れると419エラー。
*   **`@method('PUT')` / `@method('DELETE')`**: HTMLフォームでPUT/DELETEをシミュレートする。
*   **`old('name')`**: バリデーションエラー時に入力値を保持し、ユーザーの再入力の手間を省く。
*   **`@error('name')`**: フィールドごとにエラーメッセージを表示し、ユーザーに修正箇所を伝える。

次のセクションでは、Bladeファイルの読み解き方（レイアウトとコンポーネント）を学びます。

---
