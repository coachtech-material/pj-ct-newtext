# Tutorial 9-1-4: ルーティングの基礎

## 🎯 このセクションで学ぶこと

- ルーティングの基本的な書き方を理解する
- HTTPメソッド（GET / POST）の違いを理解する
- ルートパラメータの使い方を理解する

> **📌 前提知識**
> 
> 前のセクションで学んだ「ルーティング = 受付係」というイメージを思い出してください。
> このセクションでは、その受付係（ルーティング）の具体的な書き方を学びます。

---

## 📍 ルーティングとは

ルーティングとは、**「どのURLにアクセスされたら、どの処理を実行するか」を定義する仕組み**です。

前のセクションのレストランの比喩で言えば、**受付係がメニュー表を見て、どのウェイターに注文を渡すか決める**のがルーティングです。

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
Route::get('/users', [UserController::class, 'index']);

// ユーザー詳細を表示
Route::get('/users/{id}', [UserController::class, 'show']);
```

**POST**は、データを送信するときに使います。

```php
// 新しいユーザーを作成
Route::post('/users', [UserController::class, 'store']);
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
Route::get('/users/{id}', [UserController::class, 'show']);
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

## 📋 よく使うルーティングパターン

Webアプリケーションでよく使うルーティングのパターンをまとめます。

```php
use App\Http\Controllers\TaskController;

// 一覧表示
Route::get('/tasks', [TaskController::class, 'index']);

// 作成フォーム表示
Route::get('/tasks/create', [TaskController::class, 'create']);

// 新規作成（フォーム送信）
Route::post('/tasks', [TaskController::class, 'store']);

// 詳細表示
Route::get('/tasks/{id}', [TaskController::class, 'show']);

// 編集フォーム表示
Route::get('/tasks/{id}/edit', [TaskController::class, 'edit']);

// 更新（フォーム送信）
Route::put('/tasks/{id}', [TaskController::class, 'update']);

// 削除
Route::delete('/tasks/{id}', [TaskController::class, 'destroy']);
```

| URL | メソッド | 処理 |
|:---|:---|:---|
| `/tasks` | GET | 一覧表示 |
| `/tasks/create` | GET | 作成フォーム表示 |
| `/tasks` | POST | 新規作成 |
| `/tasks/{id}` | GET | 詳細表示 |
| `/tasks/{id}/edit` | GET | 編集フォーム表示 |
| `/tasks/{id}` | PUT | 更新 |
| `/tasks/{id}` | DELETE | 削除 |

> **📌 補足**
> 
> このパターンは**CRUD（クラッド）**と呼ばれ、Webアプリケーションの基本的な操作パターンです。
> CRUDについては、後のセクションで詳しく学びます。

---

## 🔍 ルーティングの確認方法

定義したルーティングは、以下のコマンドで一覧表示できます。

```bash
sail artisan route:list
```

このコマンドを実行すると、現在定義されている全てのルーティングが表示されます。

```
GET|HEAD   / ..................................... 
GET|HEAD   users .............. UserController@index
GET|HEAD   users/{id} ......... UserController@show
POST       users .............. UserController@store
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

このセクションでは、ルーティングの基本的な書き方を学びました。

| 項目 | 内容 |
|:---|:---|
| **ルーティングの場所** | `routes/web.php` |
| **基本構文** | `Route::get('/url', [Controller::class, 'method']);` |
| **HTTPメソッド** | GET（取得）、POST（送信）、PUT（更新）、DELETE（削除） |
| **ルートパラメータ** | `{id}`で変数を受け取る |
| **確認コマンド** | `sail artisan route:list` |

> **📌 ポイント**
> 
> ルーティングは、Laravelアプリケーションの**入り口**です。
> ユーザーがアクセスするURLは、全てルーティングで定義されています。
> 
> 「このURLにアクセスしたら、どのコントローラーが動くのか？」を意識しながら開発を進めましょう。

次のセクションでは、リクエストとレスポンスについて学びます。

---
