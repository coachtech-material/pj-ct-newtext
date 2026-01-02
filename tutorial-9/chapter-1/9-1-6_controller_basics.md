# Tutorial 9-1-6: コントローラーの基礎

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
docker compose exec php php artisan make:controller UserController
```

このコマンドを実行すると、`app/Http/Controllers/UserController.php`というファイルが生成されます。

**生成されたファイルの内容**

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
{
    //
}
```

**コードリーディング**

*   `namespace App\Http\Controllers;`: このクラスが`App\Http\Controllers`という名前空間に属することを示します。
*   `use Illuminate\Http\Request;`: `Request`クラスをインポートします。これは、HTTPリクエストの情報を扱うためのクラスです。
*   `class UserController extends Controller`: `UserController`クラスを定義し、`Controller`クラスを継承します。

現時点では、クラスの中身は空です。ここに、メソッドを追加していきます。

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
docker compose exec php php artisan make:controller UserController --resource
```

`--resource`オプションを付けることで、以下の7つのメソッドが自動生成されます。

| メソッド | 用途 | HTTPメソッド | URL |
|:---|:---|:---|:---|
| `index()` | 一覧表示 | GET | `/users` |
| `create()` | 作成フォーム表示 | GET | `/users/create` |
| `store()` | データ作成 | POST | `/users` |
| `show($id)` | 詳細表示 | GET | `/users/{id}` |
| `edit($id)` | 編集フォーム表示 | GET | `/users/{id}/edit` |
| `update($id)` | データ更新 | PUT/PATCH | `/users/{id}` |
| `destroy($id)` | データ削除 | DELETE | `/users/{id}` |

**生成されたコントローラー**

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class UserController extends Controller
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
Route::resource('users', UserController::class);
```

この1行で、上記の7つのルートが全て定義されます。`php artisan route:list`で確認すると、以下のようになります。

| Method | URI | Name | Action |
|:---|:---|:---|:---|
| GET | users | users.index | UserController@index |
| GET | users/create | users.create | UserController@create |
| POST | users | users.store | UserController@store |
| GET | users/{user} | users.show | UserController@show |
| GET | users/{user}/edit | users.edit | UserController@edit |
| PUT/PATCH | users/{user} | users.update | UserController@update |
| DELETE | users/{user} | users.destroy | UserController@destroy |

ルート名も自動的に生成されるため、`route('users.show', ['user' => $user->id])`のように使うことができます。

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

#### 3. JSONを返す（API用）

```php
return response()->json([
    'message' => 'Success',
    'data' => $users
]);
```

#### 4. リダイレクトする

```php
// 名前付きルートにリダイレクト
return redirect()->route('users.index');

// URLにリダイレクト
return redirect('/users');

// 前のページに戻る
return back();
```

#### 5. ダウンロードさせる

```php
return response()->download($pathToFile);
```

---

## 💡 TIP: コントローラーの責務を小さく保つ

コントローラーは、「リクエストを受け取り、処理を委譲し、レスポンスを返す」という役割に徹するべきです。複雑なビジネスロジックは、コントローラーに書かずに、サービスクラスやモデルに分離することが推奨されます。

**悪い例：コントローラーに複雑なロジックを書く**
```php
public function store(Request $request)
{
    // バリデーション
    $validated = $request->validate([...]);

    // ユーザー作成
    $user = User::create($validated);

    // プロフィール作成
    $user->profile()->create([...]);

    // メール送信
    Mail::to($user->email)->send(new WelcomeMail($user));

    // ログ記録
    Log::info('User created: ' . $user->id);

    return redirect()->route('users.show', $user);
}
```

**良い例：サービスクラスに処理を委譲する**
```php
public function store(Request $request, UserService $userService)
{
    $validated = $request->validate([...]);

    $user = $userService->createUser($validated);

    return redirect()->route('users.show', $user);
}
```

このように、コントローラーをシンプルに保つことで、テストがしやすく、保守しやすいコードになります。

---

## ✨ まとめ

このセクションでは、Laravelのコントローラーの基礎を学びました。

*   コントローラーは、MVCアーキテクチャにおいて「司令塔」の役割を果たし、リクエストを受け取り、モデルとビューを橋渡しする。
*   `php artisan make:controller`コマンドで、コントローラーを生成できる。
*   コントローラーのメソッドは、ルーティングで指定されたときに実行され、ビューやJSONなどのレスポンスを返す。
*   ルートパラメータは、メソッドの引数として受け取ることができ、ルートモデルバインディングを使うとさらに簡潔に書ける。
*   `--resource`オプションを使うと、CRUD操作の7つのメソッドを持つリソースコントローラーを一括生成できる。
*   `Route::resource()`を使うと、リソースコントローラーのルートを一括定義できる。

これで、Tutorial 9のChapter 1「Laravelの基礎」が完了しました。次のChapter 2では、ビューとテンプレートエンジンであるBladeについて学んでいきます。

---
