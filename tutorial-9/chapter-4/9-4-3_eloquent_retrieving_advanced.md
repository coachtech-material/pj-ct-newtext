# Tutorial 9-4-3: データの取得（find、all、where）

## 🎯 このセクションで学ぶこと

*   Eloquentを使って、様々な方法でデータを取得できるようになる。
*   `find()`、`all()`、`where()`などのメソッドを使い分けられるようになる。
*   クエリビルダーを使って、複雑な条件でデータを取得できるようになる。

---

## 導入：データを「取得する」方法は無限にある

前のセクションで、Eloquentの基本的なデータ取得方法を学びました。しかし、実際のアプリケーション開発では、もっと複雑な条件でデータを取得する必要があります。

例えば、以下のような状況を考えてみましょう。

*   **特定のIDのユーザーを取得したい**
*   **公開済みの投稿のみを取得したい**
*   **作成日が新しい順に投稿を取得したい**
*   **特定のカテゴリーに属する投稿を取得したい**

このセクションでは、Eloquentを使って、様々な方法でデータを取得する方法を学びます。

---

## 詳細解説

### 🔍 基本的なデータ取得メソッド

#### 全てのレコードを取得する

```php
$users = User::all();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM users;
```

#### 特定のIDのレコードを取得する

```php
$user = User::find(1);
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM users WHERE id = 1;
```

**重要なポイント**

*   `find()`は、レコードが見つからない場合、`null`を返します。
*   レコードが見つからない場合に404エラーを返したい場合は、`findOrFail()`を使います。

```php
$user = User::findOrFail(1);
```

#### 複数のIDのレコードを取得する

```php
$users = User::find([1, 2, 3]);
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM users WHERE id IN (1, 2, 3);
```

---

### 🎯 `where()`を使った条件付き取得

#### 基本的な`where()`

```php
$users = User::where('is_admin', true)->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM users WHERE is_admin = 1;
```

**重要なポイント**

*   `where()`の後には、必ず`get()`を付けます。
*   `get()`を付けないと、クエリビルダーのインスタンスが返されます。

#### 複数の条件を指定する

```php
$users = User::where('is_admin', true)
             ->where('status', 'active')
             ->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM users WHERE is_admin = 1 AND status = 'active';
```

#### OR条件を指定する

```php
$users = User::where('is_admin', true)
             ->orWhere('is_moderator', true)
             ->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM users WHERE is_admin = 1 OR is_moderator = 1;
```

---

### 🔍 比較演算子を使った条件

#### 大なり・小なり

```php
$posts = Post::where('views', '>', 1000)->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM posts WHERE views > 1000;
```

#### LIKE検索

```php
$users = User::where('name', 'like', '%山田%')->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM users WHERE name LIKE '%山田%';
```

#### BETWEEN

```php
$posts = Post::whereBetween('created_at', ['2024-01-01', '2024-12-31'])->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM posts WHERE created_at BETWEEN '2024-01-01' AND '2024-12-31';
```

#### IN

```php
$users = User::whereIn('id', [1, 2, 3])->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM users WHERE id IN (1, 2, 3);
```

#### NULL チェック

```php
$posts = Post::whereNull('published_at')->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM posts WHERE published_at IS NULL;
```

---

### 📊 並び替え（ORDER BY）

#### 昇順（ASC）

```php
$posts = Post::orderBy('created_at', 'asc')->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM posts ORDER BY created_at ASC;
```

#### 降順（DESC）

```php
$posts = Post::orderBy('created_at', 'desc')->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM posts ORDER BY created_at DESC;
```

#### 複数のカラムで並び替え

```php
$posts = Post::orderBy('is_pinned', 'desc')
             ->orderBy('created_at', 'desc')
             ->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM posts ORDER BY is_pinned DESC, created_at DESC;
```

#### ショートカット

```php
$posts = Post::latest()->get(); // created_at DESC
$posts = Post::oldest()->get(); // created_at ASC
```

---

### 🎯 件数制限（LIMIT）

#### 最初のN件を取得

```php
$posts = Post::take(10)->get();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM posts LIMIT 10;
```

#### 最初の1件を取得

```php
$post = Post::first();
```

これは、以下のSQLと同じです。

```sql
SELECT * FROM posts LIMIT 1;
```

**重要なポイント**

*   `first()`は、レコードが見つからない場合、`null`を返します。
*   レコードが見つからない場合に404エラーを返したい場合は、`firstOrFail()`を使います。

---

### 🔍 特定のカラムのみを取得

```php
$users = User::select('id', 'name', 'email')->get();
```

これは、以下のSQLと同じです。

```sql
SELECT id, name, email FROM users;
```

---

### 📈 集計関数

#### レコード数を取得

```php
$count = User::count();
```

これは、以下のSQLと同じです。

```sql
SELECT COUNT(*) FROM users;
```

#### 最大値・最小値・平均値・合計

```php
$maxViews = Post::max('views');
$minViews = Post::min('views');
$avgViews = Post::avg('views');
$totalViews = Post::sum('views');
```

---

### 🚀 実践例：複雑な条件でデータを取得する

#### 例1: 公開済みの投稿を、閲覧数が多い順に10件取得

```php
$posts = Post::where('is_published', true)
             ->orderBy('views', 'desc')
             ->take(10)
             ->get();
```

#### 例2: 特定のユーザーの投稿を、作成日が新しい順に取得

```php
$posts = Post::where('user_id', 1)
             ->orderBy('created_at', 'desc')
             ->get();
```

#### 例3: タイトルに「Laravel」を含む公開済みの投稿を取得

```php
$posts = Post::where('is_published', true)
             ->where('title', 'like', '%Laravel%')
             ->get();
```

---

### 💡 TIP: `pluck()`で特定のカラムの値のみを取得

```php
$emails = User::pluck('email');
```

これにより、メールアドレスの配列が取得されます。

```php
["taro@example.com", "hanako@example.com", ...]
```

#### キーと値のペアで取得

```php
$users = User::pluck('name', 'id');
```

これにより、以下のような配列が取得されます。

```php
[
    1 => "山田太郎",
    2 => "佐藤花子",
    ...
]
```

---

### 🔍 `chunk()`で大量のデータを分割処理

大量のデータを一度に取得すると、メモリ不足になる可能性があります。`chunk()`を使うことで、データを分割して処理できます。

```php
User::chunk(100, function ($users) {
    foreach ($users as $user) {
        // ユーザーごとの処理
    }
});
```

これにより、100件ずつデータを取得して処理します。

---

### 🚨 よくある間違い

#### 間違い1: `get()`を忘れる

```php
$users = User::where('is_admin', true); // NG
```

これは、クエリビルダーのインスタンスが返されるため、レコードを取得できません。

**正しい書き方**

```php
$users = User::where('is_admin', true)->get(); // OK
```

#### 間違い2: `all()`の後に`where()`を付ける

```php
$users = User::all()->where('is_admin', true); // NG
```

`all()`は、Collectionを返すため、`where()`は使えません。

**正しい書き方**

```php
$users = User::where('is_admin', true)->get(); // OK
```

---

## ✨ まとめ

このセクションでは、Eloquentを使って、様々な方法でデータを取得する方法を学びました。

*   `find()`で特定のIDのレコードを取得できる。
*   `where()`で条件を指定してレコードを取得できる。
*   `orderBy()`で並び替えができる。
*   `take()`、`first()`で件数を制限できる。
*   `count()`、`max()`、`min()`、`avg()`、`sum()`で集計ができる。
*   `pluck()`で特定のカラムの値のみを取得できる。
*   `chunk()`で大量のデータを分割処理できる。

次のセクションでは、Eloquentを使ってデータを作成する方法を学びます。

---

## 📝 学習のポイント

- [ ] `find()`、`all()`、`where()`を使い分けられる。
- [ ] `where()`の後には、必ず`get()`を付ける必要がある。
- [ ] `orderBy()`、`take()`、`first()`を使って、データを絞り込める。
- [ ] `count()`、`max()`、`min()`などの集計関数を使える。
- [ ] `pluck()`で特定のカラムの値のみを取得できる。
