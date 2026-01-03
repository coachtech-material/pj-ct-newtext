# Tutorial 9-1-7: コントローラーの基礎

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

コントローラーは、`php artisan make:controller`コマンドで生成します。

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

*   `namespace App\Http\Controllers;`: このクラスが`App\Http\Controllers`という名前空間に属することを示します。
*   `use Illuminate\Http\Request;`: `Request`クラスをインポートします。これは、HTTPリクエストの情報を扱うためのクラスです。
*   `class SampleController extends Controller`: `SampleController`クラスを定義し、`Controller`クラスを継承します。

現時点では、クラスの中身は空です。ここに、メソッドを追加していきます。

> **💡 POINT**
> 
> 以降の例では、前のセクションで作成した`UserController`を引き続き使用します。新しいコントローラーを作成する必要はありません。

### 📝 メソッドの追加

コントローラーのメソッドは、ルーティングで指定されたときに実行されます。例えば、ユーザー一覧を表示する`index`メソッドを追加してみましょう。

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

```php
Route::resource('products', ProductController::class);
```

この1行で、上記の7つのルートが全て定義されます。`php artisan route:list`で確認すると、以下のようになります。

| Method | URI | Name | Action |
|:---|:---|:---|:---|
| GET | products | products.index | ProductController@index |
| GET | products/create | products.create | ProductController@create |
| POST | products | products.store | ProductController@store |
| GET | products/{product} | products.show | ProductController@show |
| GET | products/{product}/edit | products.edit | ProductController@edit |
| PUT/PATCH | products/{product} | products.update | ProductController@update |
| DELETE | products/{product} | products.destroy | ProductController@destroy |

ルート名も自動的に生成されるため、`route('products.show', ['product' => $product->id])`のように使うことができます。

### 🔄 レスポンスの返し方

コントローラーのメソッドは、様々な形式でレスポンスを返すことができます。

#### 1. ビューを返す

```php
return view('users.index', compact('users'));
```

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
*   `php artisan make:controller`コマンドで、コントローラーを生成できる。
*   コントローラーのメソッドは、ルーティングで指定されたときに実行され、ビューやリダイレクトなどのレスポンスを返す。
*   ルートパラメータは、メソッドの引数として受け取ることができ、ルートモデルバインディングを使うとさらに簡潔に書ける。
*   `--resource`オプションを使うと、CRUD操作の7つのメソッドを持つリソースコントローラーを一括生成できる。
*   `Route::resource()`を使うと、リソースコントローラーのルートを一括定義できる。

これで、Tutorial 9のChapter 1「Laravelの基礎」が完了しました。次のChapter 2では、ビューとテンプレートエンジンであるBladeについて学んでいきます。

---
