# Tutorial 11-4-2: SQLインジェクション対策

## 🎯 このセクションで学ぶこと

*   SQLインジェクションとは何かを理解し、その危険性を学ぶ。
*   Eloquent ORMとクエリビルダーを使って、SQLインジェクションを防ぐ方法を学ぶ。
*   生のSQLを使う場合の安全な方法を学ぶ。

---

## 導入：なぜSQLインジェクション対策が重要なのか

**SQLインジェクション**は、**悪意のあるSQL文を注入して、データベースを不正に操作する攻撃**です。

SQLインジェクション対策を行わないと、データベースの情報が漏洩したり、データが改ざんされたりする可能性があります。

---

## 詳細解説

### 🔍 SQLインジェクションの例

以下のコードは、**SQLインジェクションの脆弱性**があります。

```php
// ❌ 危険なコード
$keyword = request('keyword');
$tasks = DB::select("SELECT * FROM tasks WHERE title LIKE '%{$keyword}%'");
```

ユーザーが`keyword`に`'; DROP TABLE tasks; --`を入力すると、以下のSQL文が実行されます。

```sql
SELECT * FROM tasks WHERE title LIKE '%'; DROP TABLE tasks; --%'
```

これにより、**tasksテーブルが削除**されてしまいます。

---

### 🔍 Eloquent ORMを使った安全な実装

Eloquent ORMを使うと、自動的にSQLインジェクション対策が行われます。

```php
// ✅ 安全なコード
$keyword = request('keyword');
$tasks = Task::where('title', 'like', '%' . $keyword . '%')->get();
```

Eloquent ORMは、内部で**プリペアドステートメント**を使っているため、SQLインジェクションが防げます。

---

### 🔍 クエリビルダーを使った安全な実装

クエリビルダーも、プリペアドステートメントを使います。

```php
// ✅ 安全なコード
$keyword = request('keyword');
$tasks = DB::table('tasks')
    ->where('title', 'like', '%' . $keyword . '%')
    ->get();
```

---

### 🔍 プリペアドステートメントとは

**プリペアドステートメント**は、**SQL文とデータを分離して実行する仕組み**です。

```php
// プリペアドステートメントのイメージ
$sql = "SELECT * FROM tasks WHERE title LIKE ?";
$bindings = ['%Laravel%'];
```

これにより、ユーザーの入力がSQL文として解釈されることを防げます。

---

### 🔍 生のSQLを使う場合

生のSQLを使う場合は、**バインディング**を使います。

```php
// ✅ 安全なコード
$keyword = request('keyword');
$tasks = DB::select("SELECT * FROM tasks WHERE title LIKE ?", ['%' . $keyword . '%']);
```

---

### 🔍 名前付きバインディング

名前付きバインディングも使えます。

```php
// ✅ 安全なコード
$keyword = request('keyword');
$tasks = DB::select("SELECT * FROM tasks WHERE title LIKE :keyword", ['keyword' => '%' . $keyword . '%']);
```

---

### 🔍 whereRaw()を使う場合

`whereRaw()`を使う場合も、バインディングを使います。

```php
// ✅ 安全なコード
$keyword = request('keyword');
$tasks = Task::whereRaw('title LIKE ?', ['%' . $keyword . '%'])->get();
```

---

### 🔍 危険な例

以下のコードは、**SQLインジェクションの脆弱性**があります。

```php
// ❌ 危険なコード
$keyword = request('keyword');
$tasks = Task::whereRaw("title LIKE '%{$keyword}%'")->get();
```

---

### 💡 TIP: DB::raw()

`DB::raw()`を使う場合も、バインディングを使います。

```php
// ❌ 危険なコード
$keyword = request('keyword');
$tasks = Task::select(DB::raw("*, CONCAT(title, '{$keyword}') as search_title"))->get();

// ✅ 安全なコード（ただし、DB::raw()は避けるべき）
$tasks = Task::selectRaw("*, CONCAT(title, ?) as search_title", [$keyword])->get();
```

---

### 🚨 よくある間違い

#### 間違い1: 文字列連結でSQL文を作る

**対処法**: Eloquent ORMまたはクエリビルダーを使います。

---

#### 間違い2: whereRaw()で文字列連結を使う

**対処法**: バインディングを使います。

---

#### 間違い3: ユーザー入力をそのままSQL文に埋め込む

**対処法**: 必ずプリペアドステートメントを使います。

---

## ✨ まとめ

このセクションでは、SQLインジェクション対策を学びました。

*   SQLインジェクションの危険性を理解した。
*   Eloquent ORMとクエリビルダーを使って、SQLインジェクションを防いだ。
*   生のSQLを使う場合は、バインディングを使った。

次のセクションでは、XSS対策について学びます。

---

## 📝 学習のポイント

- [ ] SQLインジェクションの危険性を理解した。
- [ ] Eloquent ORMを使った安全な実装を学んだ。
- [ ] プリペアドステートメントを理解した。
- [ ] 生のSQLを使う場合は、バインディングを使った。
