# Tutorial 9-4-2: Eloquentでデータを取得する

## 🎯 このセクションで学ぶこと

- Eloquentを使って、データベースからデータを取得する様々な方法を学ぶ
- `all()`, `find()`, `where()`, `first()`, `get()`などのメソッドを使いこなせるようになる
- クエリビルダーを使って、複雑な検索条件を組み立てられるようになる
- 集計関数や便利なメソッドを活用できるようになる

---

## 導入：Eloquentでデータを取得する

前のセクションで、Eloquent ORMの概念と、モデルとテーブルの対応関係を学びました。このセクションでは、実際にEloquentを使って、データベースからデータを取得する方法を学びます。

Eloquentには、データを取得するための様々なメソッドが用意されており、シンプルな取得から複雑な検索まで、直感的に記述できます。

### データ取得の全体像

Eloquentでのデータ取得は、大きく分けて以下の3つのパターンがあります。

| パターン | メソッド | 用途 |
|---------|---------|------|
| 全件取得 | `all()` | テーブルの全レコードを取得 |
| ID指定 | `find()` | 主キーでレコードを取得 |
| 条件指定 | `where()->get()` | 条件に一致するレコードを取得 |

それぞれの使い方を詳しく見ていきましょう。

---

## 詳細解説

### 📚 全てのレコードを取得する（`all()`）

最もシンプルな取得方法は、`all()`メソッドを使って、全てのレコードを取得することです。

```php
use App\Models\User;

$users = User::all();
```

これは、SQLの`SELECT * FROM users`に相当します。`$users`には、`User`モデルの**コレクション**（配列のようなもの）が格納されます。

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

> **💡 ポイント**: `all()`は全てのレコードを取得するため、データ量が多い場合はメモリを大量に消費します。大量のデータを扱う場合は、後述する`paginate()`や`chunk()`を使いましょう。

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

これにより、レコードが見つからない場合、自動的に404エラーページが表示されます。コントローラーでは、こちらを使うことが多いです。

#### 複数のIDを指定する

```php
$users = User::find([1, 2, 3]);
```

これは、SQLの`SELECT * FROM users WHERE id IN (1, 2, 3)`に相当します。

---

### 🔎 条件を指定してレコードを取得する（`where()`）

特定の条件に一致するレコードを取得するには、`where()`メソッドを使います。

```php
$users = User::where('email', 'taro@example.com')->get();
```

これは、SQLの`SELECT * FROM users WHERE email = 'taro@example.com'`に相当します。

> **🚨 重要**: `where()`は、クエリビルダーを返すため、最後に`get()`を呼び出してレコードを取得します。`get()`を忘れると、データではなくクエリビルダーのインスタンスが返されます。

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

---

### 🎯 比較演算子を使った条件

`where()`の第2引数に、比較演算子を指定できます。

```php
// 年齢が18歳以上
$users = User::where('age', '>=', 18)->get();

// 名前が「山田」で始まる（LIKE検索）
$users = User::where('name', 'LIKE', '山田%')->get();

// IDが1, 2, 3のいずれか
$users = User::whereIn('id', [1, 2, 3])->get();

// メールアドレスがNULLではない
$users = User::whereNotNull('email')->get();

// 作成日が2024年1月1日から12月31日の間
$posts = Post::whereBetween('created_at', ['2024-01-01', '2024-12-31'])->get();
```

---

### 📊 並び替え（`orderBy()`）

レコードを並び替えるには、`orderBy()`を使います。

```php
// 作成日時の新しい順（降順）
$users = User::orderBy('created_at', 'desc')->get();

// 名前の昇順
$users = User::orderBy('name', 'asc')->get();
```

`asc`は昇順（小さい順）、`desc`は降順（大きい順）を意味します。

#### 便利なショートカット

```php
$posts = Post::latest()->get(); // created_at DESC
$posts = Post::oldest()->get(); // created_at ASC
```

`latest()`は`orderBy('created_at', 'desc')`と同じ意味です。

#### 複数のカラムで並び替え

```php
$posts = Post::orderBy('is_pinned', 'desc')
             ->orderBy('created_at', 'desc')
             ->get();
```

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

### 🎯 特定のカラムだけを取得する（`select()`）

全てのカラムではなく、特定のカラムだけを取得するには、`select()`を使います。

```php
$users = User::select('id', 'name', 'email')->get();
```

これは、SQLの`SELECT id, name, email FROM users`に相当します。

---

### 📈 集計関数

#### レコード数を取得（`count()`）

```php
$count = User::where('is_admin', true)->count();
```

これは、SQLの`SELECT COUNT(*) FROM users WHERE is_admin = 1`に相当します。

#### 最大値・最小値・平均値・合計

```php
$maxViews = Post::max('views');    // 最大値
$minViews = Post::min('views');    // 最小値
$avgViews = Post::avg('views');    // 平均値
$totalViews = Post::sum('views');  // 合計
```

---

### 💡 便利なメソッド

#### `pluck()` - 特定のカラムの値のみを取得

```php
$emails = User::pluck('email');
// 結果: ["taro@example.com", "hanako@example.com", ...]
```

キーと値のペアで取得することもできます。

```php
$users = User::pluck('name', 'id');
// 結果: [1 => "山田太郎", 2 => "佐藤花子", ...]
```

これは、セレクトボックスの選択肢を作るときに便利です。

#### `chunk()` - 大量のデータを分割処理

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

### 💡 TIP: クエリビルダーの「遅延実行」

Eloquentのクエリビルダーは、**遅延実行（Lazy Evaluation）**という仕組みを採用しています。これは、「`get()`, `first()`, `count()`などのメソッドを呼び出すまで、実際にはSQLが実行されない」という意味です。

```php
$query = User::where('is_admin', true); // まだSQLは実行されない
$query = $query->where('created_at', '>', '2024-01-01'); // まだSQLは実行されない
$users = $query->get(); // ここで初めてSQLが実行される
```

これにより、条件を動的に組み立てることができます。

---

### 🚨 よくある間違い

#### 間違い1: `get()`を忘れる

```php
// NG: クエリビルダーのインスタンスが返される
$users = User::where('is_admin', true);

// OK: レコードのコレクションが返される
$users = User::where('is_admin', true)->get();
```

#### 間違い2: `all()`の後に`where()`を付ける

```php
// NG: all()はCollectionを返すため、where()は使えない
$users = User::all()->where('is_admin', true);

// OK: where()を先に使う
$users = User::where('is_admin', true)->get();
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
             ->latest()
             ->get();
```

#### 例3: タイトルに「Laravel」を含む公開済みの投稿を取得

```php
$posts = Post::where('is_published', true)
             ->where('title', 'like', '%Laravel%')
             ->get();
```

---

## ✨ まとめ

このセクションでは、Eloquentを使ってデータを取得する様々な方法を学びました。

| メソッド | 用途 |
|---------|------|
| `all()` | 全てのレコードを取得 |
| `find($id)` | 主キーでレコードを取得 |
| `where()->get()` | 条件に一致するレコードを取得 |
| `first()` | 条件に一致する最初の1件を取得 |
| `orderBy()` | 並び替え |
| `limit()` / `take()` | 件数制限 |
| `count()` | レコード数を取得 |
| `pluck()` | 特定のカラムの値のみを取得 |

次のセクションでは、ページネーションを使って、大量のデータを効率的に表示する方法を学びます。

---

## 📝 学習のポイント

- [ ] `User::all()`で全てのユーザーを取得できる
- [ ] `User::find($id)`で主キーを指定してユーザーを取得できる
- [ ] `User::where('email', $email)->first()`で条件に一致するユーザーを取得できる
- [ ] `where()`の後には、必ず`get()`または`first()`を付ける必要がある
- [ ] `orderBy()`, `limit()`, `take()`を使って、並び替えや件数制限ができる
- [ ] `count()`, `max()`, `min()`, `avg()`, `sum()`で集計ができる
- [ ] `pluck()`で特定のカラムの値のみを取得できる
- [ ] クエリビルダーは、`get()`や`first()`を呼び出すまでSQLが実行されないことを理解した
