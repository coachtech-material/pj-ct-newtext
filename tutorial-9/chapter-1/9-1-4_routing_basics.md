# Tutorial 9-1-4: ルーティングの基礎

## 🎯 このセクションで学ぶこと

- ルーティングが「道案内」として果たす役割を理解する
- 基本的なルーティングの書き方を理解する
- **名前付きルート**と`route()`ヘルパーの使い方を学ぶ
- HTTPメソッド（GET / POST）の違いを理解する

> **📌 前提知識**
> 
> 前のセクションで学んだ「ルーティング = 受付係」というイメージを思い出してください。
> このセクションでは、その受付係（ルーティング）の具体的な書き方を学びます。

---

## 📍 ルーティングとは：リクエストの「道案内」

ルーティングとは、**「どのURLにアクセスされたら、どの処理を実行するか」を定義する仕組み**です。

前のセクションのレストランの比喩で言えば、**受付係がメニュー表を見て、どのウェイターに注文を渡すか決める**のがルーティングです。

### ルーティングの役割

```
ユーザー → ブラウザでURLにアクセス
              ↓
         【ルーティング】← 「この道を通ってください」と案内
              ↓
         コントローラー → 処理を実行
              ↓
         ビュー → 画面を表示
```

ルーティングは、ユーザーのリクエストを**正しいコントローラーに届ける「道案内」**の役割を担っています。

Laravelでは、`routes/web.php`ファイルにルーティングを定義します。

---

## 📝 基本的なルーティングの書き方

### 最もシンプルなルーティング

```php
Route::get('/hello', function () {
    return 'Hello, World!';
});
```

このコードは、「`/hello`にアクセスされたら、`Hello, World!`という文字列を返す」という意味です。

| 部分 | 意味 |
|:---|:---|
| `Route::get` | GETリクエストを受け付ける |
| `'/hello'` | URLのパス（`http://localhost/hello`） |
| `function () { ... }` | 実行する処理 |

---

### コントローラーを呼び出すルーティング

実際の開発では、処理を直接書くのではなく、**コントローラーを呼び出す**のが一般的です。

```php
use App\Http\Controllers\UserController;

Route::get('/users', [UserController::class, 'index']);
```

このコードは、「`/users`にアクセスされたら、`UserController`の`index`メソッドを実行する」という意味です。

| 部分 | 意味 |
|:---|:---|
| `Route::get` | GETリクエストを受け付ける |
| `'/users'` | URLのパス |
| `UserController::class` | 呼び出すコントローラー |
| `'index'` | 呼び出すメソッド名 |

---

## 🏷️ 名前付きルート：URLに「名札」を付ける

### なぜ名前付きルートが必要なのか

URLを直接書くと、URLを変更したときに**全ての箇所を修正**する必要があります。

```php
// URLを直接書いた場合
<a href="/users">ユーザー一覧</a>
<a href="/users/create">新規作成</a>

// もしURLを /members に変更したら...
// 全ての箇所を修正しなければならない！
```

名前付きルートを使えば、**URLに「名札」を付けて管理**できます。URLを変更しても、名前を使っている箇所は自動的に新しいURLを参照します。

---

### 名前付きルートの定義

ルーティングに`->name()`を付けて名前を定義します。

```php
use App\Http\Controllers\UserController;

// 名前付きルートの定義
Route::get('/users', [UserController::class, 'index'])->name('users.index');
Route::get('/users/create', [UserController::class, 'create'])->name('users.create');
Route::get('/users/{id}', [UserController::class, 'show'])->name('users.show');
```

| URL | 名前 | 説明 |
|:---|:---|:---|
| `/users` | `users.index` | ユーザー一覧 |
| `/users/create` | `users.create` | 作成フォーム |
| `/users/{id}` | `users.show` | 詳細表示 |

> **💡 命名規則**
> 
> 名前は「`リソース名.アクション名`」の形式で付けるのが一般的です。
> 例：`users.index`、`users.create`、`users.show`

---

### route()ヘルパー：名前からURLを生成

Bladeテンプレートやコントローラーで、`route()`ヘルパーを使って名前からURLを生成できます。

**Bladeテンプレートでの使用例**

```blade
{{-- 名前付きルートを使ったリンク --}}
<a href="{{ route('users.index') }}">ユーザー一覧</a>

{{-- パラメータ付きの場合 --}}
<a href="{{ route('users.show', ['id' => 1]) }}">ユーザー詳細</a>
```

**コントローラーでの使用例（リダイレクト）**

```php
// 名前付きルートにリダイレクト
return redirect()->route('users.index');

// パラメータ付きでリダイレクト
return redirect()->route('users.show', ['id' => $user->id]);
```

---

### 名前付きルートのメリット

| 方法 | URLを変更したとき |
|:---|:---|
| URLを直接書く | 全ての箇所を手動で修正 |
| 名前付きルート | ルーティングの定義だけ修正すればOK |

```php
// URLを /members に変更しても...
Route::get('/members', [UserController::class, 'index'])->name('users.index');

// Bladeテンプレートは変更不要！
<a href="{{ route('users.index') }}">ユーザー一覧</a>
// → 自動的に /members を参照
```

---

## 🔀 HTTPメソッド

Webアプリケーションでは、**HTTPメソッド**によってリクエストの種類を区別します。

### 主なHTTPメソッド

| メソッド | 用途 | 例 |
|:---|:---|:---|
| **GET** | データの取得・表示 | ページの表示、一覧の取得 |
| **POST** | データの送信・作成 | フォームの送信、新規登録 |
| **PUT / PATCH** | データの更新 | 情報の編集 |
| **DELETE** | データの削除 | 情報の削除 |

---

### GETとPOSTの使い分け

**GET**は、データを取得するときに使います。

```php
// ユーザー一覧を表示
Route::get('/users', [UserController::class, 'index'])->name('users.index');

// ユーザー詳細を表示
Route::get('/users/{id}', [UserController::class, 'show'])->name('users.show');
```

**POST**は、データを送信するときに使います。

```php
// 新しいユーザーを作成
Route::post('/users', [UserController::class, 'store'])->name('users.store');
```

> **💡 覚え方**
> 
> - **GET** = 「見せて」（データを取得）
> - **POST** = 「受け取って」（データを送信）

---

## 🔢 ルートパラメータ

URLの一部を**変数**として受け取ることができます。これを**ルートパラメータ**と呼びます。

### 基本的なルートパラメータ

```php
Route::get('/users/{id}', [UserController::class, 'show'])->name('users.show');
```

このルーティングは、以下のようなURLにマッチします：

- `/users/1` → `$id = 1`
- `/users/42` → `$id = 42`
- `/users/100` → `$id = 100`

`{id}`の部分が変数になり、コントローラーで受け取ることができます。

---

### コントローラーでパラメータを受け取る

```php
public function show($id)
{
    // $id には URLの {id} の値が入る
    // /users/1 にアクセスすると、$id = 1
}
```

---

## 🔗 ルーティングとビューの連携：実践例

ここまで学んだことを使って、**ルーティングとビューがどう繋がるか**を確認しましょう。

### Step 1: ルーティングを定義

**`routes/web.php`**

```php
use App\Http\Controllers\PageController;

Route::get('/', [PageController::class, 'home'])->name('home');
Route::get('/about', [PageController::class, 'about'])->name('about');
Route::get('/contact', [PageController::class, 'contact'])->name('contact');
```

### Step 2: コントローラーを作成

**`app/Http/Controllers/PageController.php`**

```php
<?php

namespace App\Http\Controllers;

class PageController extends Controller
{
    public function home()
    {
        return view('pages.home');
    }

    public function about()
    {
        return view('pages.about');
    }

    public function contact()
    {
        return view('pages.contact');
    }
}
```

### Step 3: ビューでリンクを作成

**`resources/views/pages/home.blade.php`**

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ホーム</title>
</head>
<body>
    <nav>
        {{-- route()ヘルパーで名前付きルートからURLを生成 --}}
        <a href="{{ route('home') }}">ホーム</a>
        <a href="{{ route('about') }}">会社概要</a>
        <a href="{{ route('contact') }}">お問い合わせ</a>
    </nav>
    
    <h1>ホームページへようこそ</h1>
</body>
</html>
```

### データの流れ

```
1. ユーザーが /about にアクセス
       ↓
2. ルーティングが「about という名前のルートだ」と判断
       ↓
3. PageController の about() メソッドを呼び出し
       ↓
4. about() が pages.about ビューを返す
       ↓
5. ブラウザに会社概要ページが表示される
```

> **📌 ポイント**
> 
> `route('about')`は、ルーティングで定義した名前`about`から、自動的にURL`/about`を生成します。
> これにより、**ルーティングとビューが名前で繋がる**ことを意識してください。

---

## 🔍 ルーティングの確認方法

定義したルーティングは、以下のコマンドで一覧表示できます。

```bash
sail artisan route:list
```

このコマンドを実行すると、現在定義されている全てのルーティングが表示されます。

```
GET|HEAD   / ........................ home › PageController@home
GET|HEAD   about .................... about › PageController@about
GET|HEAD   contact .................. contact › PageController@contact
GET|HEAD   users .................... users.index › UserController@index
```

> **💡 TIP**
> 
> 「ルーティングが動かない」「404エラーが出る」というときは、まず`route:list`で確認しましょう。
> 定義したはずのルーティングが表示されていなければ、`routes/web.php`の記述に問題があります。

---

## ⚠️ よくあるエラーと対処法

### 1. 404 Not Found

**原因**: URLが間違っている、またはルーティングが定義されていない

**対処法**: 
- `sail artisan route:list`でルーティングを確認
- URLのスペルミスをチェック

---

### 2. Target class does not exist

**原因**: コントローラーのクラス名が間違っている、または`use`文が不足している

**対処法**:
- コントローラーのファイル名とクラス名が一致しているか確認
- `routes/web.php`の先頭に`use`文があるか確認

```php
// この行が必要
use App\Http\Controllers\UserController;
```

---

## ✨ まとめ

このセクションでは、ルーティングの基本的な書き方と、名前付きルートの重要性を学びました。

| 項目 | 内容 |
|:---|:---|
| **ルーティングの場所** | `routes/web.php` |
| **基本構文** | `Route::get('/url', [Controller::class, 'method']);` |
| **名前付きルート** | `->name('route.name')`で名前を付ける |
| **route()ヘルパー** | `route('route.name')`で名前からURLを生成 |
| **HTTPメソッド** | GET（取得）、POST（送信）、PUT（更新）、DELETE（削除） |
| **ルートパラメータ** | `{id}`で変数を受け取る |
| **確認コマンド** | `sail artisan route:list` |

> **📌 ポイント**
> 
> ルーティングは、Laravelアプリケーションの**入り口**であり、**道案内**です。
> 
> - **名前付きルート**を使うことで、URLの変更に強いコードが書ける
> - **route()ヘルパー**を使うことで、ルーティングとビューが繋がる
> 
> 「このURLにアクセスしたら、どのコントローラーが動くのか？」を意識しながら開発を進めましょう。

次のセクションでは、リクエストとレスポンスについて学び、**ユーザーの入力を受け取って処理する流れ**を体験します。

---
