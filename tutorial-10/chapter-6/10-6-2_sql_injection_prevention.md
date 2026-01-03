# Tutorial 10-6-2: SQLインジェクション対策

## 🎯 このセクションで学ぶこと

*   SQLインジェクション攻撃の仕組みを理解する。
*   LaravelのEloquent ORMとクエリビルダーが、どのようにSQLインジェクションを防ぐかを学ぶ。
*   生SQLを使う際の注意点を理解する。

---

## 導入：データベースへの攻撃を防ぐ

前のセクションで、CSRF攻撃について学びました。このセクションでは、**SQLインジェクション**という、さらに危険な攻撃について学びます。

SQLインジェクションは、**データベースを直接操作される**攻撃であり、最悪の場合、**全てのデータが盗まれる**可能性があります。

---

## 詳細解説

### 💉 SQLインジェクション攻撃とは

**SQLインジェクション**とは、**悪意のあるSQL文を注入して、データベースを不正に操作する攻撃**です。

#### 脆弱なコードの例

以下のような、**ユーザー入力を直接SQL文に埋め込む**コードは、非常に危険です。

```php
// 🚨 危険なコード（絶対に使わないでください）
$username = $_GET['username'];
$password = $_GET['password'];

$sql = "SELECT * FROM users WHERE username = '$username' AND password = '$password'";
$result = DB::select($sql);
```

#### 攻撃のシナリオ

攻撃者が、以下のような入力をした場合：

```
username: admin' OR '1'='1
password: （空）
```

実行されるSQL文：

```sql
SELECT * FROM users WHERE username = 'admin' OR '1'='1' AND password = ''
```

**何が起きるか**：

*   `'1'='1'`は常に真なので、**すべてのユーザー**が取得される
*   攻撃者は、パスワードを知らなくても、管理者としてログインできる

---

### 🛡️ LaravelのSQLインジェクション対策

Laravelは、**プリペアドステートメント**（Prepared Statements）を使って、SQLインジェクションを防ぎます。

#### プリペアドステートメントとは

プリペアドステートメントは、**SQLとデータを分離**する仕組みです。

```php
// 安全なコード
$username = $request->input('username');
$password = $request->input('password');

$user = DB::select('SELECT * FROM users WHERE username = ? AND password = ?', [$username, $password]);
```

**仕組み**：

1. SQLの構造（`SELECT * FROM users WHERE username = ? AND password = ?`）を先に送信
2. データ（`$username`、`$password`）を後から送信
3. データベースは、データを「SQL文の一部」ではなく、「ただの文字列」として扱う

**攻撃者が`admin' OR '1'='1`と入力しても**：

```sql
SELECT * FROM users WHERE username = 'admin\' OR \'1\'=\'1' AND password = ''
```

シングルクォートがエスケープされ、攻撃が無効化されます。

---

### ✅ Eloquent ORMは自動的に保護する

Laravelの**Eloquent ORM**は、自動的にプリペアドステートメントを使います。

```php
// 安全なコード
$user = User::where('username', $request->input('username'))
            ->where('password', $request->input('password'))
            ->first();
```

**実行されるSQL**：

```sql
SELECT * FROM users WHERE username = ? AND password = ?
```

Eloquentが自動的に、ユーザー入力をエスケープします。

---

### ✅ クエリビルダーも自動的に保護する

Laravelの**クエリビルダー**も、自動的にプリペアドステートメントを使います。

```php
// 安全なコード
$users = DB::table('users')
           ->where('username', $request->input('username'))
           ->get();
```

---

### ⚠️ 生SQLを使う際の注意点

生SQLを使う場合は、**必ずプレースホルダー（`?`）を使う**必要があります。

#### 危険な例

```php
// 🚨 危険なコード
$username = $request->input('username');
$users = DB::select("SELECT * FROM users WHERE username = '$username'");
```

#### 安全な例

```php
// ✅ 安全なコード
$username = $request->input('username');
$users = DB::select('SELECT * FROM users WHERE username = ?', [$username]);
```

または、名前付きプレースホルダーを使う：

```php
// ✅ 安全なコード
$username = $request->input('username');
$users = DB::select('SELECT * FROM users WHERE username = :username', ['username' => $username]);
```

---

### 🚫 LIKE句での注意点

LIKE句を使う場合も、プレースホルダーを使います。

#### 危険な例

```php
// 🚨 危険なコード
$keyword = $request->input('keyword');
$posts = DB::select("SELECT * FROM posts WHERE title LIKE '%$keyword%'");
```

#### 安全な例

```php
// ✅ 安全なコード
$keyword = $request->input('keyword');
$posts = DB::select('SELECT * FROM posts WHERE title LIKE ?', ['%' . $keyword . '%']);
```

または、Eloquentを使う：

```php
// ✅ 安全なコード
$keyword = $request->input('keyword');
$posts = Post::where('title', 'like', '%' . $keyword . '%')->get();
```

---

### 🔍 ORDER BY句での注意点

ORDER BY句は、プレースホルダーが使えません。ユーザー入力をそのまま使うのは危険です。

#### 危険な例

```php
// 🚨 危険なコード
$sort = $request->input('sort'); // 'title' または 'created_at'
$posts = DB::select("SELECT * FROM posts ORDER BY $sort");
```

攻撃者が`sort=id; DROP TABLE posts;`と入力すると、テーブルが削除される可能性があります。

#### 安全な例

```php
// ✅ 安全なコード
$sort = $request->input('sort');

// ホワイトリストで検証
$allowedSorts = ['title', 'created_at'];
if (!in_array($sort, $allowedSorts)) {
    $sort = 'created_at'; // デフォルト値
}

$posts = Post::orderBy($sort)->get();
```

**重要なポイント**：

*   ユーザー入力を**ホワイトリスト**で検証する
*   許可された値以外は、デフォルト値を使う

---

### 💡 実践例：検索機能

#### コントローラー

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function search(Request $request)
    {
        $keyword = $request->input('keyword');
        $sort = $request->input('sort', 'created_at'); // デフォルトは'created_at'
        
        // ソートカラムのホワイトリスト
        $allowedSorts = ['title', 'created_at', 'views'];
        if (!in_array($sort, $allowedSorts)) {
            $sort = 'created_at';
        }
        
        // Eloquentを使った安全な検索
        $posts = Post::where('title', 'like', '%' . $keyword . '%')
                     ->orderBy($sort, 'desc')
                     ->paginate(20);
        
        return view('posts.search', ['posts' => $posts]);
    }
}
```

**コードリーディング**：

*   `where('title', 'like', '%' . $keyword . '%')`：Eloquentが自動的にエスケープ
*   `in_array($sort, $allowedSorts)`：ホワイトリストで検証

---

## 💡 TIP

### バリデーションと組み合わせる

ユーザー入力は、必ずバリデーションを行いましょう。

```php
$request->validate([
    'keyword' => 'required|string|max:100',
    'sort' => 'in:title,created_at,views',
]);
```

**コードリーディング**：

*   `in:title,created_at,views`：許可された値のみを受け付ける

### ログに記録する

不正な入力を検知したら、ログに記録しましょう。

```php
if (!in_array($sort, $allowedSorts)) {
    Log::warning('Invalid sort parameter', ['sort' => $sort, 'ip' => $request->ip()]);
    $sort = 'created_at';
}
```

---

## ✨ まとめ

*   **SQLインジェクション**は、悪意のあるSQL文を注入して、データベースを不正に操作する攻撃
*   Laravelの**Eloquent ORM**と**クエリビルダー**は、自動的にプリペアドステートメントを使い、SQLインジェクションを防ぐ
*   生SQLを使う場合は、**必ずプレースホルダー（`?`）を使う**
*   ORDER BY句など、プレースホルダーが使えない場合は、**ホワイトリスト**で検証する
*   ユーザー入力は、必ず**バリデーション**を行う

---
