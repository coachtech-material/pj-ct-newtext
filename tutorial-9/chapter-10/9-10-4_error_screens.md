# Tutorial 9-10-4: エラー画面の読み方とスタックトレース

## 🎯 このセクションで学ぶこと

*   Laravelの赤いエラー画面（Ignition）の読み方を理解する。
*   スタックトレースの見方を学ぶ。
*   エラーメッセージから問題を特定できるようになる。

---

## 導入：「赤い画面」を恐れない

Laravelで開発していると、**赤いエラー画面**に遭遇することがあります。この画面は、**Ignition**と呼ばれるエラーページで、エラーの詳細情報を表示します。

最初は怖く感じるかもしれませんが、**エラー画面は味方**です。エラーの原因を特定するための重要な情報が詰まっています。

このセクションでは、エラー画面の読み方とスタックトレースの見方を学びます。

---

## 詳細解説

### 🔍 Ignitionエラー画面の構成

Ignitionエラー画面は、以下の要素で構成されています。

1. **エラーメッセージ**: 何が起きたのかを示す
2. **エラーの種類**: 例外のクラス名
3. **発生場所**: ファイル名と行番号
4. **スタックトレース**: エラーに至るまでの処理の流れ
5. **コンテキスト**: リクエスト情報、ルート情報など

---

### 🚀 実践例1: `Class not found`エラー

#### エラー画面

```
Error

Class "App\Http\Controllers\PostControler" not found

app/Http/Controllers/PostControler.php:10
```

#### 読み方

*   **エラーメッセージ**: `Class "App\Http\Controllers\PostControler" not found`
*   **原因**: クラス名のスペルミス（`PostControler` → `PostController`）
*   **対処法**: クラス名を修正する

---

### 🚀 実践例2: `MassAssignmentException`

#### エラー画面

```
Illuminate\Database\Eloquent\MassAssignmentException

Add [title] to fillable property to allow mass assignment on [App\Models\Post].

app/Http/Controllers/PostController.php:25
```

#### 読み方

*   **エラーメッセージ**: `Add [title] to fillable property to allow mass assignment on [App\Models\Post].`
*   **原因**: `title`が`$fillable`に含まれていない
*   **対処法**: `Post`モデルの`$fillable`に`title`を追加する

```php
protected $fillable = ['title', 'content'];
```

---

### 🚀 実践例3: `Integrity constraint violation`

#### エラー画面

```
SQLSTATE[23000]: Integrity constraint violation: 1452 Cannot add or update a child row: a foreign key constraint fails (`blog`.`posts`, CONSTRAINT `posts_user_id_foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE)

app/Http/Controllers/PostController.php:30
```

#### 読み方

*   **エラーメッセージ**: `Integrity constraint violation: 1452 Cannot add or update a child row`
*   **原因**: 外部キー制約違反（存在しない`user_id`を指定している）
*   **対処法**: 正しい`user_id`を指定する

---

### 🔍 スタックトレースの読み方

スタックトレースは、**エラーに至るまでの処理の流れ**を示します。

#### スタックトレースの例

```
1. app/Http/Controllers/PostController.php:30
   App\Http\Controllers\PostController->store()

2. vendor/laravel/framework/src/Illuminate/Routing/Controller.php:54
   Illuminate\Routing\Controller->callAction()

3. vendor/laravel/framework/src/Illuminate/Routing/ControllerDispatcher.php:45
   Illuminate\Routing\ControllerDispatcher->dispatch()

4. vendor/laravel/framework/src/Illuminate/Routing/Route.php:219
   Illuminate\Routing\Route->runController()
```

#### 読み方

*   **上から下へ**: 処理の流れを追う
*   **最初の行**: エラーが発生した場所
*   **自分のコード**: `app/`で始まる行に注目
*   **フレームワークのコード**: `vendor/`で始まる行は、通常は無視してOK

---

### 🚀 実践例4: `Call to undefined method`

#### エラー画面

```
Error

Call to undefined method App\Models\Post::user()

app/Http/Controllers/PostController.php:15
```

#### 読み方

*   **エラーメッセージ**: `Call to undefined method App\Models\Post::user()`
*   **原因**: `Post`モデルに`user()`メソッドが定義されていない
*   **対処法**: `Post`モデルに`user()`メソッドを追加する

```php
public function user()
{
    return $this->belongsTo(User::class);
}
```

---

### 🚀 実践例5: `Undefined variable`

#### エラー画面

```
ErrorException

Undefined variable $post

resources/views/posts/show.blade.php:10
```

#### 読み方

*   **エラーメッセージ**: `Undefined variable $post`
*   **原因**: Bladeテンプレートで`$post`変数が定義されていない
*   **対処法**: コントローラーから`$post`変数を渡す

```php
return view('posts.show', compact('post'));
```

---

### 💡 TIP: エラーメッセージをGoogle検索

エラーメッセージをそのままGoogle検索すると、同じ問題に遭遇した人の解決策が見つかることがあります。

**検索例**

```
laravel MassAssignmentException
laravel Integrity constraint violation
```

---

### 🚀 実践例6: `Too few arguments`

#### エラー画面

```
ArgumentCountError

Too few arguments to function App\Http\Controllers\PostController::update(), 1 passed and exactly 2 expected

app/Http/Controllers/PostController.php:40
```

#### 読み方

*   **エラーメッセージ**: `Too few arguments to function App\Http\Controllers\PostController::update(), 1 passed and exactly 2 expected`
*   **原因**: `update()`メソッドに渡される引数が不足している
*   **対処法**: ルート定義を確認し、正しいパラメータを渡す

```php
// ルート
Route::put('/posts/{id}', [PostController::class, 'update']);

// コントローラー
public function update(Request $request, $id)
{
    // ...
}
```

---

### 🔍 コンテキスト情報

Ignitionエラー画面には、以下のコンテキスト情報も表示されます。

*   **Request**: リクエストの詳細（URL、メソッド、パラメータ）
*   **Route**: ルート情報（名前、アクション、ミドルウェア）
*   **User**: 認証済みユーザー情報
*   **Environment**: 環境変数

---

### 💡 TIP: `dd()`と`dump()`

デバッグ時には、`dd()`（Dump and Die）や`dump()`を使って、変数の内容を確認できます。

```php
public function show($id)
{
    $post = Post::findOrFail($id);

    dd($post); // ここで処理が止まり、$postの内容が表示される

    return response()->json(['post' => $post]);
}
```

---

### 🚀 実践例7: `Route not found`

#### エラー画面

```
Symfony\Component\HttpKernel\Exception\NotFoundHttpException

app/Http/Controllers/PostController.php:10
```

#### 読み方

*   **エラーメッセージ**: `NotFoundHttpException`
*   **原因**: ルートが定義されていない、またはURLが間違っている
*   **対処法**: `routes/api.php`または`routes/web.php`を確認

---

### 🚨 よくある間違い

#### 間違い1: エラーメッセージを読まずに推測する

エラーメッセージには、問題の原因が明確に書かれていることが多いです。まずはエラーメッセージをしっかり読みましょう。

---

#### 間違い2: スタックトレースを無視する

スタックトレースは、エラーに至るまでの処理の流れを示します。特に、自分のコード（`app/`で始まる行）に注目しましょう。

---

## ✨ まとめ

このセクションでは、エラー画面の読み方とスタックトレースについて学びました。

*   Ignitionエラー画面は、エラーの詳細情報を表示する。
*   エラーメッセージから、問題の原因を特定できる。
*   スタックトレースは、エラーに至るまでの処理の流れを示す。
*   自分のコード（`app/`で始まる行）に注目する。

次のセクションでは、よくあるエラー集と対処法を学びます。

---
