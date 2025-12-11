# Tutorial 9-1-5: ルーティングの基礎

## 🎯 このセクションで学ぶこと

*   ルーティングが何であるか、その役割を理解する。
*   `routes/web.php`でルートを定義し、URLとコントローラーを紐付けられるようになる。
*   HTTPメソッド（GET、POST、PUT、DELETE）に応じたルートを定義できるようになる。
*   ルートパラメータを使って、動的なURLを扱えるようになる。

---

## 導入：ルーティングとは「道案内」

前のセクションで、MVCアーキテクチャにおけるデータの流れを学びました。その最初のステップが「ルーティング」です。

ルーティングとは、**「どのURLにアクセスしたら、どの処理を実行するか」を定義する仕組み**です。これは、Webアプリケーションにおける「道案内」のようなものです。

例えば、以下のようなURLがあったとします。

*   `http://localhost:8080/` → トップページを表示
*   `http://localhost:8080/users` → ユーザー一覧を表示
*   `http://localhost:8080/users/123` → ID=123のユーザー詳細を表示
*   `http://localhost:8080/posts/create` → 投稿作成フォームを表示

これらのURLに対して、「どのコントローラーのどのメソッドを実行するか」を決めるのが、ルーティングの役割です。Laravelでは、`routes/web.php`というファイルにルートを定義します。

---

## 詳細解説

### 📝 基本的なルート定義

最もシンプルなルート定義は、以下のような形です。

```php
<?php
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return 'Hello, Laravel!';
});
```

**コードリーディング**

*   `Route::get('/', ...)`: GETメソッドで`/`（ルートURL）にアクセスしたときの処理を定義します。
*   `function () { return 'Hello, Laravel!'; }`: クロージャ（無名関数）を使って、直接レスポンスを返しています。この場合、ブラウザには「Hello, Laravel!」という文字列が表示されます。

ブラウザで`http://localhost:8080/`にアクセスすると、「Hello, Laravel!」と表示されます。

**[ここに、ブラウザで「Hello, Laravel!」が表示されたスクリーンショットを挿入]**

### 🎯 コントローラーを使ったルート定義

実際の開発では、クロージャではなく、コントローラーを使ってルートを定義します。

```php
<?php
use App\Http\Controllers\UserController;

Route::get('/users', [UserController::class, 'index']);
```

**コードリーディング**

*   `[UserController::class, 'index']`: 配列の形式で、コントローラーのクラスとメソッドを指定します。
*   `UserController::class`: `App\Http\Controllers\UserController`という完全修飾名（FQCN）を取得します。
*   `'index'`: `UserController`クラスの`index`メソッドを実行します。

この定義により、`/users`にアクセスすると、`UserController`の`index`メソッドが実行されます。

### 🔀 HTTPメソッドに応じたルート定義

Webアプリケーションでは、同じURLでも、HTTPメソッド（GET、POST、PUT、DELETE）によって異なる処理を行います。

| HTTPメソッド | 用途 | Laravelのルート定義 |
|:---|:---|:---|
| **GET** | データの取得（一覧表示、詳細表示） | `Route::get()` |
| **POST** | データの作成（フォーム送信） | `Route::post()` |
| **PUT/PATCH** | データの更新 | `Route::put()` / `Route::patch()` |
| **DELETE** | データの削除 | `Route::delete()` |

**例：ユーザーのCRUD操作のルート定義**

```php
<?php
use App\Http\Controllers\UserController;

// ユーザー一覧を表示（GET）
Route::get('/users', [UserController::class, 'index']);

// ユーザー作成フォームを表示（GET）
Route::get('/users/create', [UserController::class, 'create']);

// ユーザーを作成（POST）
Route::post('/users', [UserController::class, 'store']);

// ユーザー詳細を表示（GET）
Route::get('/users/{id}', [UserController::class, 'show']);

// ユーザー編集フォームを表示（GET）
Route::get('/users/{id}/edit', [UserController::class, 'edit']);

// ユーザーを更新（PUT）
Route::put('/users/{id}', [UserController::class, 'update']);

// ユーザーを削除（DELETE）
Route::delete('/users/{id}', [UserController::class, 'destroy']);
```

この7つのルートは、RESTful APIの標準的なパターンです。Laravelでは、これを`Route::resource()`という便利なメソッドで一括定義することもできます（後のセクションで学びます）。

### 🔢 ルートパラメータ

URLの一部を変数として受け取ることができます。これを**ルートパラメータ**と呼びます。

```php
Route::get('/users/{id}', [UserController::class, 'show']);
```

`{id}`の部分がルートパラメータです。例えば、`/users/123`にアクセスすると、`id`に`123`が代入され、コントローラーに渡されます。

**コントローラー側での受け取り方**

```php
<?php
namespace App\Http\Controllers;

class UserController extends Controller
{
    public function show($id)
    {
        return "ユーザーID: {$id} の詳細を表示します";
    }
}
```

ブラウザで`http://localhost:8080/users/123`にアクセスすると、「ユーザーID: 123 の詳細を表示します」と表示されます。

#### 複数のパラメータ

複数のパラメータを受け取ることもできます。

```php
Route::get('/posts/{postId}/comments/{commentId}', function ($postId, $commentId) {
    return "投稿ID: {$postId}, コメントID: {$commentId}";
});
```

`/posts/5/comments/10`にアクセスすると、「投稿ID: 5, コメントID: 10」と表示されます。

#### オプションパラメータ

パラメータを省略可能にすることもできます。パラメータ名の後に`?`を付けます。

```php
Route::get('/users/{id?}', function ($id = null) {
    if ($id) {
        return "ユーザーID: {$id}";
    } else {
        return "全ユーザーを表示";
    }
});
```

*   `/users/123` → 「ユーザーID: 123」
*   `/users` → 「全ユーザーを表示」

### 🏷️ ルートに名前を付ける

ルートに名前を付けることで、URLが変更されても、コード内での参照を変更する必要がなくなります。

```php
Route::get('/users/{id}', [UserController::class, 'show'])->name('users.show');
```

ビューやコントローラーから、この名前を使ってURLを生成できます。

```php
// URLを生成
$url = route('users.show', ['id' => 123]);
// 結果: http://localhost:8080/users/123
```

Bladeテンプレートでは、以下のように使います。

```blade
<a href="{{ route('users.show', ['id' => $user->id]) }}">
    {{ $user->name }}
</a>
```

これにより、URLが`/users/{id}`から`/members/{id}`に変更されても、ルート定義の1箇所を変更するだけで、全ての参照が自動的に更新されます。

### 📂 ルートのグループ化

複数のルートに共通の設定（プレフィックス、ミドルウェアなど）を適用したい場合、ルートをグループ化できます。

```php
Route::prefix('admin')->group(function () {
    Route::get('/users', [AdminUserController::class, 'index']);
    Route::get('/posts', [AdminPostController::class, 'index']);
});
```

この定義により、以下のURLが生成されます。

*   `/admin/users` → `AdminUserController@index`
*   `/admin/posts` → `AdminPostController@index`

---

## 💡 TIP: ルートの確認方法

定義したルートの一覧を確認するには、以下のコマンドを実行します。

```bash
docker compose exec php php artisan route:list
```

このコマンドを実行すると、全てのルートが表形式で表示されます。

**[ここに、`php artisan route:list`の実行結果のスクリーンショットを挿入]**

| Method | URI | Name | Action |
|:---|:---|:---|:---|
| GET | / | - | Closure |
| GET | users | - | App\Http\Controllers\UserController@index |
| GET | users/{id} | users.show | App\Http\Controllers\UserController@show |

この一覧を見ることで、「どのURLがどのコントローラーに紐付いているか」を確認できます。

---

## ✨ まとめ

このセクションでは、Laravelのルーティングの基礎を学びました。

*   ルーティングとは、URLとコントローラーを紐付ける「道案内」の役割を持つ。
*   `routes/web.php`で、`Route::get()`, `Route::post()`, `Route::put()`, `Route::delete()`を使ってルートを定義する。
*   ルートパラメータ（`{id}`）を使うことで、動的なURLを扱うことができる。
*   ルートに名前を付けることで、URL変更時の影響を最小限に抑えられる。
*   `php artisan route:list`コマンドで、定義したルートの一覧を確認できる。

次のセクションでは、ルーティングで呼び出される「コントローラー」について、より詳しく学んでいきます。

---

## 📝 学習のポイント

- [ ] ルーティングが、URLとコントローラーを紐付ける役割を持つことを理解した。
- [ ] `Route::get()`, `Route::post()`などを使って、HTTPメソッドに応じたルートを定義できる。
- [ ] ルートパラメータ（`{id}`）を使って、URLから値を受け取ることができる。
- [ ] `->name()`を使って、ルートに名前を付けることができる。
- [ ] `php artisan route:list`で、ルートの一覧を確認できる。
