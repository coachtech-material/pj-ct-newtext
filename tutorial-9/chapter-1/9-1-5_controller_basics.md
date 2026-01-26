# Tutorial 9-1-5: コントローラーの基礎

## 🎯 このセクションで学ぶこと

*   コントローラーが何であるか、その役割を理解する。
*   Artisanコマンドを使って、コントローラーを生成できるようになる。
*   コントローラーのメソッドで、リクエストを処理し、レスポンスを返せるようになる。
*   リソースコントローラーを使って、CRUD操作の7つのメソッドを一括生成できるようになる。

---

## 導入：コントローラーは「司令塔」

前のセクションで、ルーティングを使ってURLとコントローラーを紐付ける方法を学びました。このセクションでは、その「コントローラー」について詳しく学んでいきます。

MVCアーキテクチャにおいて、コントローラーは**「司令塔」**の役割を果たします。ユーザーからのリクエストを受け取り、モデルにデータの取得を依頼し、その結果をビューに渡してHTMLを生成し、最終的にブラウザにレスポンスを返す、という一連の流れを制御します。

コントローラーは、`app/Http/Controllers/`ディレクトリに配置され、クラスとして定義されます。Laravelでは、Artisanコマンドを使って、コントローラーを簡単に生成することができます。

---

## 詳細解説

### 🛠️ コントローラーの生成

コントローラーは、`sail artisan make:controller`コマンド（`php artisan make:controller`）で生成します。

> **📌 コマンドの実行場所**
> 
> `sail artisan`コマンドは、**Laravelプロジェクトのルートディレクトリ**（`docker-compose.yml`があるディレクトリ）で実行する必要があります。
> ```bash
> # 例: プロジェクトディレクトリに移動
> cd ~/coachtech/laravel-practice
> ```

```bash
sail artisan make:controller SampleController
```

このコマンドを実行すると、`app/Http/Controllers/SampleController.php`というファイルが生成されます。

> **📌 補足**
> 
> 前のセクション（9-1-4）で、すでに`UserController`と`WelcomeController`を作成しました。同じ名前のコントローラーを再度作成しようとすると、「Controller already exists.」というエラーが表示されます。ここでは例として`SampleController`という別の名前を使用しています。

**生成されたファイルの内容**

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class SampleController extends Controller
{
    //
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `namespace App\Http\Controllers;` | このクラスが属する「住所」のようなもの。Laravelのコントローラーはこの名前空間に配置されます。 |
| `use Illuminate\Http\Request;` | `Request`クラスをインポート（使えるように準備）します。HTTPリクエストの情報を扱うためのクラスです。 |
| `class SampleController extends Controller` | `SampleController`クラスを定義し、`Controller`クラスを継承します。 |

> **📌 初学者向け用語解説**
> 
> | 用語 | 意味 | 例え |
> |:---|:---|:---|
> | **namespace（名前空間）** | クラスの「住所」。同じ名前のクラスがあっても、住所が違えば区別できる | 「東京都の田中さん」と「大阪府の田中さん」は別人 |
> | **use** | 他の場所にあるクラスを「使えるようにする」宣言 | 「このファイルでRequestクラスを使います」 |
> | **extends（継承）** | 親クラスの機能を引き継ぐこと | 「動物」クラスを継承した「犬」クラスは、動物の機能を持つ |
> | **class** | 設計図のようなもの。データと処理をまとめたもの | 「車」クラスには「走る」「止まる」などの機能がある |

現時点では、クラスの中身は空です。ここに、メソッドを追加していきます。

> **💡 POINT**
> 
> 以降の例では、前のセクションで作成した`UserController`を引き続き使用します。新しいコントローラーを作成する必要はありません。

### 📝 メソッドの追加

コントローラーのメソッドは、ルーティングで指定されたときに実行されます。例えば、ユーザー一覧を表示する`index`メソッドを追加してみましょう。

> **📌 publicとは？**
> 
> `public`はメソッドの「可視性」を表します。`public`は「外部から呼び出せる」という意味です。
> 
> | 可視性 | 意味 |
> |:---|:---|
> | `public` | どこからでも呼び出せる（ルーティングから呼ばれるメソッドはこれ） |
> | `private` | 同じクラス内からのみ呼び出せる |
> | `protected` | 同じクラスと子クラスから呼び出せる |
> 
> コントローラーのメソッドは、ルーティングから呼び出されるため、**必ず`public`にする必要があります**。

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;

class UserController extends Controller
{
    public function index()
    {
        // 全てのユーザーを取得
        $users = User::all();

        // ビューにデータを渡す
        return view('users.index', compact('users'));
    }
}
```

**コードリーディング**

*   `use App\Models\User;`: `User`モデルをインポートします。
*   `public function index()`: `index`メソッドを定義します。このメソッドは、ルーティングで`[UserController::class, 'index']`と指定されたときに実行されます。
*   `User::all()`: `User`モデルの`all()`メソッドを呼び出し、データベースから全てのユーザーを取得します。
*   `return view('users.index', compact('users'));`: `resources/views/users/index.blade.php`というビューを読み込み、`$users`変数をビューに渡します。

> **📌 compact()関数とは？**
> 
> `compact()`はPHPの組み込み関数で、**変数名をキー、変数の値を値とする配列**を作成します。
> 
> ```php
> $users = User::all();
> 
> // compact()を使う場合
> return view('users.index', compact('users'));
> // ↑ これは以下と同じ意味 ↓
> return view('users.index', ['users' => $users]);
> ```
> 
> 変数名とキー名が同じ場合は`compact()`を使うと短く書けます。

### 🔢 ルートパラメータの受け取り

ルーティングで定義したパラメータは、コントローラーのメソッドの引数として受け取ることができます。

**ルーティング（`routes/web.php`）**
```php
Route::get('/users/{id}', [UserController::class, 'show']);
```

**コントローラー（`UserController.php`）**
```php
public function show($id)
{
    // IDを使ってユーザーを取得
    $user = User::find($id);

    // ユーザーが見つからない場合は404エラー
    if (!$user) {
        abort(404, 'ユーザーが見つかりません');
    }

    // ビューにデータを渡す
    return view('users.show', compact('user'));
}
```

**コードリーディング**

*   `public function show($id)`: ルートパラメータ`{id}`を、引数`$id`として受け取ります。
*   `User::find($id)`: `find()`メソッドは、主キー（`id`）を指定してレコードを1件取得します。見つからない場合は`null`を返します。
*   `abort(404, 'ユーザーが見つかりません');`: HTTPステータスコード404を返し、エラーメッセージを表示します。

#### より簡潔な書き方：ルートモデルバインディング

Laravelには、ルートパラメータを自動的にモデルのインスタンスに変換する「ルートモデルバインディング」という機能があります。

**ルーティング**
```php
Route::get('/users/{user}', [UserController::class, 'show']);
```

**コントローラー**
```php
public function show(User $user)
{
    // $userには、自動的にUser::find($id)の結果が代入される
    return view('users.show', compact('user'));
}
```

パラメータ名（`{user}`）とメソッドの引数の型（`User $user`）を一致させることで、Laravelが自動的にデータベースからユーザーを取得し、見つからない場合は404エラーを返してくれます。これにより、コードが非常に簡潔になります。

### 🗂️ リソースコントローラー

CRUD操作（作成・読み取り・更新・削除）を行うコントローラーは、決まったパターンがあります。Laravelでは、このパターンを「リソースコントローラー」として、一括生成することができます。

> **📌 コマンドの実行場所**
> 
> `sail artisan`コマンドは、**Laravelプロジェクトのルートディレクトリ**で実行します。

```bash
sail artisan make:controller ProductController --resource
```

> **📌 補足**
> 
> ここでは例として`ProductController`を使用しています。すでに作成済みの`UserController`とは別のコントローラーです。

`--resource`オプションを付けることで、以下の7つのメソッドが自動生成されます。

| メソッド | 用途 | HTTPメソッド | URL |
|:---|:---|:---|:---|
| `index()` | 一覧表示 | GET | `/products` |
| `create()` | 作成フォーム表示 | GET | `/products/create` |
| `store()` | データ作成 | POST | `/products` |
| `show($id)` | 詳細表示 | GET | `/products/{id}` |
| `edit($id)` | 編集フォーム表示 | GET | `/products/{id}/edit` |
| `update($id)` | データ更新 | PUT/PATCH | `/products/{id}` |
| `destroy($id)` | データ削除 | DELETE | `/products/{id}` |

**生成されたコントローラー**

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ProductController extends Controller
{
    public function index()
    {
        //
    }

    public function create()
    {
        //
    }

    public function store(Request $request)
    {
        //
    }

    public function show(string $id)
    {
        //
    }

    public function edit(string $id)
    {
        //
    }

    public function update(Request $request, string $id)
    {
        //
    }

    public function destroy(string $id)
    {
        //
    }
}
```

これらのメソッドに、具体的な処理を書いていきます。

#### リソースルートの一括定義

リソースコントローラーを使う場合、ルーティングも一括で定義できます。

**従来の書き方（ルートを1つずつ定義）**

```php
// routes/web.php
use App\Http\Controllers\ProductController;

// 7つのルートを全て手書きする必要がある
Route::get('/products', [ProductController::class, 'index'])->name('products.index');
Route::get('/products/create', [ProductController::class, 'create'])->name('products.create');
Route::post('/products', [ProductController::class, 'store'])->name('products.store');
Route::get('/products/{product}', [ProductController::class, 'show'])->name('products.show');
Route::get('/products/{product}/edit', [ProductController::class, 'edit'])->name('products.edit');
Route::put('/products/{product}', [ProductController::class, 'update'])->name('products.update');
Route::delete('/products/{product}', [ProductController::class, 'destroy'])->name('products.destroy');
```

この書き方でも動作しますが、**7行も書く必要があり、タイプミスのリスクも高まります**。

**`Route::resource()`を使った書き方（推奨）**

```php
// routes/web.php
use App\Http\Controllers\ProductController;

// たった1行で同じルートが全て定義される！
Route::resource('products', ProductController::class);
```

この**たった1行**で、上記の7つのルートが全て定義されます。

**実際に登録されるルートを確認する**

`sail artisan route:list`コマンドを実行すると、登録されたルートの一覧を確認できます。（プロジェクトのルートディレクトリで実行）

```bash
sail artisan route:list
```

**出力結果**

| Method | URI | Name | Action |
|:---|:---|:---|:---|
| GET | products | products.index | ProductController@index |
| GET | products/create | products.create | ProductController@create |
| POST | products | products.store | ProductController@store |
| GET | products/{product} | products.show | ProductController@show |
| GET | products/{product}/edit | products.edit | ProductController@edit |
| PUT/PATCH | products/{product} | products.update | ProductController@update |
| DELETE | products/{product} | products.destroy | ProductController@destroy |

**各ルートの詳細解説**

| ルート名 | URL | HTTPメソッド | 用途 | 例 |
|:---|:---|:---|:---|:---|
| `products.index` | `/products` | GET | 商品一覧を表示 | 「商品一覧」ページ |
| `products.create` | `/products/create` | GET | 新規作成フォームを表示 | 「商品を追加」ページ |
| `products.store` | `/products` | POST | フォームから送信されたデータを保存 | 「登録」ボタン押下時 |
| `products.show` | `/products/{product}` | GET | 特定の商品の詳細を表示 | 「商品詳細」ページ |
| `products.edit` | `/products/{product}/edit` | GET | 編集フォームを表示 | 「商品を編集」ページ |
| `products.update` | `/products/{product}` | PUT/PATCH | フォームから送信されたデータで更新 | 「更新」ボタン押下時 |
| `products.destroy` | `/products/{product}` | DELETE | 特定の商品を削除 | 「削除」ボタン押下時 |

> **📌 {product}とは？**
> 
> `{product}`はルートパラメータです。実際には商品のIDが入ります。
> 例：`/products/5`はIDが5の商品を指します。

**Bladeテンプレートでの使用例**

ルート名が自動的に生成されるため、`route()`ヘルパーで簡単にURLを生成できます。

```blade
{{-- 商品一覧へのリンク --}}
<a href="{{ route('products.index') }}">商品一覧</a>

{{-- 新規作成フォームへのリンク --}}
<a href="{{ route('products.create') }}">商品を追加</a>

{{-- 特定の商品の詳細へのリンク（IDを渡す） --}}
<a href="{{ route('products.show', ['product' => $product->id]) }}">{{ $product->name }}</a>

{{-- 編集フォームへのリンク --}}
<a href="{{ route('products.edit', ['product' => $product->id]) }}">編集</a>

{{-- 削除フォーム（DELETEメソッドを使用） --}}
<form action="{{ route('products.destroy', ['product' => $product->id]) }}" method="POST">
    @csrf
    @method('DELETE')
    <button type="submit">削除</button>
</form>
```

> **💡 @method('DELETE')とは？**
> 
> HTMLのフォームはGETとPOSTしかサポートしていません。
> PUTやDELETEを使うために、Laravelでは`@method('DELETE')`を使って「これはDELETEリクエストだよ」と伝えます。

#### 一部のルートのみを使う場合

7つ全てのルートが必要ない場合は、`only`や`except`で絞り込めます。

```php
// index, showのみを使う（読み取り専用）
Route::resource('products', ProductController::class)->only(['index', 'show']);

// destroy以外を使う（削除機能なし）
Route::resource('products', ProductController::class)->except(['destroy']);
```

| メソッド | 説明 | 使いどころ |
|:---|:---|:---|
| `only()` | 指定したルートのみを登録 | 一部の機能だけ使う場合 |
| `except()` | 指定したルート以外を登録 | 特定の機能を除外する場合 |

#### まとめ：なぜ`Route::resource()`を使うのか？

| 従来の書き方 | `Route::resource()` |
|:---|:---|
| 7行必要 | 1行でOK |
| タイプミスのリスクが高い | 自動生成でミスなし |
| ルート名を手動で設定 | ルート名も自動生成 |
| チームでバラバラになりやすい | 統一された書き方 |

> **📌 実務でのポイント**
> 
> CRUD操作を行うコントローラーには、`Route::resource()`を使うのが一般的です。
> コードが簡潔になり、チーム開発でも統一された書き方ができます。

### 🔄 レスポンスの返し方

コントローラーのメソッドは、様々な形式でレスポンスを返すことができます。

#### 1. ビューを返す

`view()`ヘルパーの第2引数で、ビューにデータを渡すことができます。

```php
// 方法1: 配列で渡す
$users = User::all();
return view('users.index', ['users' => $users]);

// 方法2: compact()で渡す（変数名とキー名が同じ場合）
$users = User::all();
return view('users.index', compact('users'));

// 方法3: 複数の変数を渡す
$users = User::all();
$title = 'ユーザー一覧';
return view('users.index', compact('users', 'title'));
```

| 書き方 | 特徴 |
|:---|:---|
| `['users' => $users]` | キー名と変数名を自由に指定できる |
| `compact('users')` | 変数名とキー名が同じ場合に短く書ける |

#### 2. 文字列を返す

```php
return 'Hello, World!';
```

#### 3. リダイレクトする

```php
// 名前付きルートにリダイレクト
return redirect()->route('users.index');

// URLにリダイレクト
return redirect('/users');

// 前のページに戻る
return back();
```

#### 4. ダウンロードさせる

```php
return response()->download($pathToFile);
```

---

## ✨ まとめ

このセクションでは、Laravelのコントローラーの基礎を学びました。

*   コントローラーは、MVCアーキテクチャにおいて「司令塔」の役割を果たし、リクエストを受け取り、モデルとビューを橋渡しする。
*   `sail artisan make:controller`コマンドで、コントローラーを生成できる。
*   コントローラーのメソッドは、ルーティングで指定されたときに実行され、ビューやリダイレクトなどのレスポンスを返す。
*   ルートパラメータは、メソッドの引数として受け取ることができ、ルートモデルバインディングを使うとさらに簡潔に書ける。
*   `--resource`オプションを使うと、CRUD操作の7つのメソッドを持つリソースコントローラーを一括生成できる。
*   `Route::resource()`を使うと、リソースコントローラーのルートを一括定義できる。

次のセクションでは、リクエストとレスポンスについて学び、「ユーザーの入力を受け取って処理する流れ」を体験します。

---
