# Tutorial 9-4-2: Eloquentでデータを取得する

## 🎯 このセクションで学ぶこと

*   Eloquentを使って、データベースからデータを取得する様々な方法を学ぶ。
*   `all()`, `find()`, `where()`, `first()`, `get()`などのメソッドを使いこなせるようになる。
*   クエリビルダーを使って、複雑な検索条件を組み立てられるようになる。

---

## 導入：Eloquentでデータを取得する

前のセクションで、Eloquent ORMの概念と、モデルとテーブルの対応関係を学びました。このセクションでは、実際にEloquentを使って、データベースからデータを取得する方法を学びます。

Eloquentには、データを取得するための様々なメソッドが用意されており、シンプルな取得から複雑な検索まで、直感的に記述できます。

---

## 詳細解説

### 📚 全てのレコードを取得する（`all()`）

最もシンプルな取得方法は、`all()`メソッドを使って、全てのレコードを取得することです。

```php
use App\Models\User;

$users = User::all();
```

これは、SQLの`SELECT * FROM users`に相当します。`$users`には、`User`モデルのコレクション（配列のようなもの）が格納されます。

**コントローラーでの使用例**

```php
public function index()
{
    $users = User::all();
    return view('users.index', compact('users'));
}
```

**Bladeでの表示**

```blade
@foreach ($users as $user)
    <li>{{ $user->name }} ({{ $user->email }})</li>
@endforeach
```

---

### 🔍 主キーでレコードを取得する（`find()`）

主キー（`id`）を指定して、1件のレコードを取得するには、`find()`メソッドを使います。

```php
$user = User::find(1);
```

これは、SQLの`SELECT * FROM users WHERE id = 1`に相当します。

**レコードが見つからない場合**

`find()`は、レコードが見つからない場合、`null`を返します。

```php
$user = User::find(999);

if ($user) {
    echo $user->name;
} else {
    echo 'ユーザーが見つかりません';
}
```

#### `findOrFail()` - 見つからない場合は404エラー

レコードが見つからない場合に、404エラーを返したい場合は、`findOrFail()`を使います。

```php
$user = User::findOrFail(1);
```

これにより、レコードが見つからない場合、自動的に404エラーページが表示されます。

---

### 🔎 条件を指定してレコードを取得する（`where()`）

特定の条件に一致するレコードを取得するには、`where()`メソッドを使います。

```php
$users = User::where('email', 'taro@example.com')->get();
```

これは、SQLの`SELECT * FROM users WHERE email = 'taro@example.com'`に相当します。

**重要なポイント**

*   `where()`は、クエリビルダーを返すため、最後に`get()`を呼び出してレコードを取得します。
*   `get()`は、条件に一致する全てのレコードをコレクションとして返します。

#### 1件だけ取得する（`first()`）

条件に一致する最初の1件だけを取得するには、`first()`を使います。

```php
$user = User::where('email', 'taro@example.com')->first();
```

これは、SQLの`SELECT * FROM users WHERE email = 'taro@example.com' LIMIT 1`に相当します。

`first()`は、レコードが見つからない場合、`null`を返します。

#### `firstOrFail()` - 見つからない場合は404エラー

```php
$user = User::where('email', 'taro@example.com')->firstOrFail();
```

---

### 🔢 複数の条件を組み合わせる

`where()`は、複数回呼び出すことで、AND条件を組み立てることができます。

```php
$users = User::where('is_admin', true)
             ->where('created_at', '>', '2024-01-01')
             ->get();
```

これは、SQLの`SELECT * FROM users WHERE is_admin = 1 AND created_at > '2024-01-01'`に相当します。

#### OR条件（`orWhere()`）

OR条件を使う場合は、`orWhere()`を使います。

```php
$users = User::where('is_admin', true)
             ->orWhere('is_moderator', true)
             ->get();
```

これは、SQLの`SELECT * FROM users WHERE is_admin = 1 OR is_moderator = 1`に相当します。

#### 比較演算子を使う

`where()`の第2引数に、比較演算子を指定できます。

```php
// 年齢が18歳以上
$users = User::where('age', '>=', 18)->get();

// 名前が「山田」で始まる
$users = User::where('name', 'LIKE', '山田%')->get();

// IDが1, 2, 3のいずれか
$users = User::whereIn('id', [1, 2, 3])->get();

// メールアドレスがNULLではない
$users = User::whereNotNull('email')->get();
```

---

### 📊 並び替え（`orderBy()`）

レコードを並び替えるには、`orderBy()`を使います。

```php
// 作成日時の新しい順
$users = User::orderBy('created_at', 'desc')->get();

// 名前の昇順
$users = User::orderBy('name', 'asc')->get();
```

`asc`は昇順（小さい順）、`desc`は降順（大きい順）を意味します。

#### 最新のレコードを取得する（`latest()`）

`created_at`カラムで降順に並び替える場合は、`latest()`を使うと簡潔です。

```php
$users = User::latest()->get();
```

これは、`orderBy('created_at', 'desc')`と同じ意味です。

---

### 🔢 件数を制限する（`limit()`, `take()`）

取得するレコードの件数を制限するには、`limit()`または`take()`を使います。

```php
// 最初の10件を取得
$users = User::limit(10)->get();

// または
$users = User::take(10)->get();
```

#### スキップする（`skip()`, `offset()`）

最初の数件をスキップするには、`skip()`または`offset()`を使います。

```php
// 最初の5件をスキップして、次の10件を取得
$users = User::skip(5)->take(10)->get();
```

これは、ページネーション（ページ分割）で使われます。

---

### 📄 ページネーション（`paginate()`）

大量のレコードを扱う場合、全てを一度に表示するのではなく、ページごとに分割して表示することが一般的です。Eloquentには、ページネーション機能が組み込まれています。

```php
$users = User::paginate(15);
```

これにより、1ページあたり15件のレコードが取得され、ページネーションリンク（「前へ」「次へ」ボタン）も自動生成されます。

**Bladeでの表示**

```blade
@foreach ($users as $user)
    <li>{{ $user->name }}</li>
@endforeach

{{ $users->links() }}
```

`$users->links()`は、ページネーションリンクを自動生成します。

---

### 🔢 レコード数を取得する（`count()`）

条件に一致するレコードの件数を取得するには、`count()`を使います。

```php
$count = User::where('is_admin', true)->count();
```

これは、SQLの`SELECT COUNT(*) FROM users WHERE is_admin = 1`に相当します。

---

### 🎯 特定のカラムだけを取得する（`select()`）

全てのカラムではなく、特定のカラムだけを取得するには、`select()`を使います。

```php
$users = User::select('id', 'name', 'email')->get();
```

これは、SQLの`SELECT id, name, email FROM users`に相当します。

---

## 💡 TIP: クエリビルダーの「遅延実行」

Eloquentのクエリビルダーは、**遅延実行（Lazy Evaluation）**という仕組みを採用しています。これは、「`get()`, `first()`, `count()`などのメソッドを呼び出すまで、実際にはSQLが実行されない」という意味です。

```php
$query = User::where('is_admin', true); // まだSQLは実行されない
$query = $query->where('created_at', '>', '2024-01-01'); // まだSQLは実行されない
$users = $query->get(); // ここで初めてSQLが実行される
```

これにより、条件を動的に組み立てることができます。

---

## ✨ まとめ

このセクションでは、Eloquentを使ってデータを取得する様々な方法を学びました。

*   `all()`で全てのレコードを取得できる。
*   `find()`で主キーを指定してレコードを取得できる。
*   `where()`で条件を指定してレコードを取得できる。
*   `first()`で条件に一致する最初の1件を取得できる。
*   `orderBy()`で並び替え、`limit()`で件数制限ができる。
*   `paginate()`でページネーション機能を簡単に実装できる。
*   `count()`でレコード数を取得できる。

次のセクションでは、Eloquentを使って、データの作成・更新・削除を行う方法を学びます。

---

## 📝 学習のポイント

- [ ] `User::all()`で全てのユーザーを取得できる。
- [ ] `User::find($id)`で主キーを指定してユーザーを取得できる。
- [ ] `User::where('email', $email)->first()`で条件に一致するユーザーを取得できる。
- [ ] `orderBy()`, `limit()`, `paginate()`を使って、並び替えや件数制限ができる。
- [ ] クエリビルダーは、`get()`や`first()`を呼び出すまでSQLが実行されないことを理解した。
