# Tutorial 10-4-5: よくあるエラー集と対処法

## 🎯 このセクションで学ぶこと

*   Laravelでよく遭遇するエラーと対処法を学ぶ。
*   エラーメッセージから素早く問題を特定できるようになる。
*   エラー対処のパターンを身につける。

---

## 導入：「あるあるエラー」を知る

Laravelで開発していると、**よく遭遇するエラー**があります。これらのエラーは、初心者が必ず通る道です。

このセクションでは、よくあるエラーと対処法をカタログ形式で紹介します。

---

## 詳細解説

### 1. `Target class [XXX] does not exist.`

#### エラーメッセージ

```
Target class [PostController] does not exist.
```

#### 原因

*   コントローラーのクラス名が間違っている
*   名前空間が間違っている
*   ファイルが存在しない

#### 対処法

**ケース1: クラス名のスペルミス**

```php
// NG
Route::get('/posts', [PostControler::class, 'index']); // 'l'が1つ

// OK
Route::get('/posts', [PostController::class, 'index']);
```

**ケース2: 名前空間の指定忘れ**

```php
// NG
Route::get('/posts', [PostController::class, 'index']);

// OK
use App\Http\Controllers\PostController;
Route::get('/posts', [PostController::class, 'index']);
```

**ケース3: ファイルが存在しない**

```bash
php artisan make:controller PostController
```

---

### 2. `MassAssignmentException`

#### エラーメッセージ

```
Add [title] to fillable property to allow mass assignment on [App\Models\Post].
```

#### 原因

*   `create()`や`update()`で指定したカラムが`$fillable`に含まれていない

#### 対処法

**`app/Models/Post.php`**

```php
protected $fillable = ['title', 'content', 'user_id'];
```

---

### 3. `Integrity constraint violation`

#### エラーメッセージ

```
SQLSTATE[23000]: Integrity constraint violation: 1452 Cannot add or update a child row: a foreign key constraint fails
```

#### 原因

*   外部キー制約違反（存在しない`user_id`を指定している）

#### 対処法

**ケース1: 存在しないIDを指定**

```php
// NG
Post::create([
    'title' => 'Test',
    'content' => 'Test content',
    'user_id' => 999, // 存在しないユーザーID
]);

// OK
Post::create([
    'title' => 'Test',
    'content' => 'Test content',
    'user_id' => auth()->id(), // 認証済みユーザーのID
]);
```

**ケース2: 外部キーカラムが`NULL`**

```php
// マイグレーションで外部キーを nullable にする
$table->foreignId('user_id')->nullable()->constrained();
```

---

### 4. `Call to undefined method`

#### エラーメッセージ

```
Call to undefined method App\Models\Post::user()
```

#### 原因

*   メソッドが定義されていない
*   メソッド名のスペルミス

#### 対処法

**`app/Models/Post.php`**

```php
public function user()
{
    return $this->belongsTo(User::class);
}
```

---

### 5. `Undefined variable`

#### エラーメッセージ

```
Undefined variable $post
```

#### 原因

*   Bladeテンプレートで変数が定義されていない
*   コントローラーから変数を渡していない

#### 対処法

**コントローラー**

```php
public function show($id)
{
    $post = Post::findOrFail($id);

    return view('posts.show', compact('post')); // $postを渡す
}
```

---

### 6. `Too few arguments to function`

#### エラーメッセージ

```
Too few arguments to function App\Http\Controllers\PostController::update(), 1 passed and exactly 2 expected
```

#### 原因

*   メソッドに渡される引数が不足している

#### 対処法

**ルート**

```php
Route::put('/posts/{id}', [PostController::class, 'update']);
```

**コントローラー**

```php
public function update(Request $request, $id) // 2つの引数
{
    // ...
}
```

---

### 7. `SQLSTATE[42S02]: Base table or view not found`

#### エラーメッセージ

```
SQLSTATE[42S02]: Base table or view not found: 1146 Table 'blog.posts' doesn't exist
```

#### 原因

*   テーブルが存在しない
*   マイグレーションを実行していない

#### 対処法

```bash
php artisan migrate
```

---

### 8. `Route [XXX] not defined.`

#### エラーメッセージ

```
Route [posts.show] not defined.
```

#### 原因

*   ルートに名前が付けられていない
*   ルート名が間違っている

#### 対処法

**ルート**

```php
Route::get('/posts/{id}', [PostController::class, 'show'])->name('posts.show');
```

---

### 9. `Class 'XXX' not found`

#### エラーメッセージ

```
Class 'App\Models\Post' not found
```

#### 原因

*   クラスが存在しない
*   名前空間が間違っている
*   `use`文が不足している

#### 対処法

**コントローラー**

```php
use App\Models\Post; // use文を追加

public function index()
{
    $posts = Post::all();
    // ...
}
```

---

### 10. `Unauthenticated.`

#### エラーメッセージ

```
{
    "message": "Unauthenticated."
}
```

#### 原因

*   認証が必要なルートにアクセスしているが、ログインしていない
*   認証トークンが不正

#### 対処法

**Postmanでテスト**

```
GET http://localhost/api/profile
Authorization: Bearer {your_token}
```

---

### 11. `CSRF token mismatch.`

#### エラーメッセージ

```
CSRF token mismatch.
```

#### 原因

*   CSRFトークンが不正
*   フォームに`@csrf`が含まれていない

#### 対処法

**Blade**

```blade
<form action="/posts" method="POST">
    @csrf
    <!-- フォームの内容 -->
</form>
```

---

### 12. `Trying to get property 'XXX' of non-object`

#### エラーメッセージ

```
Trying to get property 'title' of non-object
```

#### 原因

*   オブジェクトが`null`
*   データベースからレコードが取得できていない

#### 対処法

**コントローラー**

```php
$post = Post::find($id);

if (!$post) {
    return response()->json(['message' => 'Post not found'], 404);
}

echo $post->title;
```

---

### 13. `Syntax error, unexpected 'XXX'`

#### エラーメッセージ

```
Syntax error, unexpected '}', expecting end of file
```

#### 原因

*   構文エラー（括弧の閉じ忘れ、セミコロン忘れなど）

#### 対処法

*   エディタのシンタックスハイライトを確認
*   括弧の対応を確認

---

### 14. `Connection refused`

#### エラーメッセージ

```
SQLSTATE[HY000] [2002] Connection refused
```

#### 原因

*   データベースに接続できない
*   `.env`の設定が間違っている

#### 対処法

**`.env`**

```
DB_CONNECTION=mysql
DB_HOST=127.0.0.1
DB_PORT=3306
DB_DATABASE=blog
DB_USERNAME=root
DB_PASSWORD=
```

**Dockerの場合**

```
DB_HOST=mysql  # コンテナ名
```

---

### 15. `Method XXX does not exist.`

#### エラーメッセージ

```
Method Illuminate\Database\Eloquent\Collection::save does not exist.
```

#### 原因

*   コレクションに対して、モデルのメソッドを呼び出している

#### 対処法

```php
// NG
$posts = Post::all();
$posts->save(); // コレクションには save() メソッドがない

// OK
$post = Post::find(1);
$post->save(); // モデルには save() メソッドがある
```

---

### 💡 TIP: エラー解決の手順

1. **エラーメッセージを読む**: 何が起きているのかを理解する
2. **発生場所を確認**: ファイル名と行番号を確認
3. **スタックトレースを見る**: エラーに至るまでの流れを追う
4. **Google検索**: エラーメッセージで検索
5. **公式ドキュメント**: Laravelの公式ドキュメントを確認

---

## ✨ まとめ

このセクションでは、Laravelでよく遭遇するエラーと対処法を学びました。

*   `Target class not found`: クラス名や名前空間を確認
*   `MassAssignmentException`: `$fillable`に追加
*   `Integrity constraint violation`: 外部キー制約を確認
*   `Call to undefined method`: メソッドを定義
*   `Undefined variable`: コントローラーから変数を渡す

これで、Chapter 10「デバッグとエラーハンドリング」の全5セクションが完了しました。次は、Chapter 11「テスト」の残りのセクションに進みます。

---
