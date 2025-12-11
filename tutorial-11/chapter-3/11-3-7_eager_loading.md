# Tutorial 11-3-7: Eager Loadingによるパフォーマンス改善

## 🎯 このセクションで学ぶこと

*   Eager Loadingを使って、N+1問題を解決し、パフォーマンスを改善する方法を学ぶ。
*   with()メソッドを使って、リレーションシップを事前に読み込む方法を学ぶ。
*   Laravel Debugbarを使って、実行されたクエリを確認する方法を学ぶ。

---

## 導入：なぜEager Loadingが重要なのか

**N+1問題**は、**リレーションシップを持つデータを取得する際に、大量のクエリが実行される問題**です。

Eager Loadingを使うことで、N+1問題を解決し、パフォーマンスを改善できます。

---

## 詳細解説

### 🔍 N+1問題とは

タスク一覧で、各タスクのカテゴリー名を表示する場合を考えます。

```php
$tasks = Task::all();

foreach ($tasks as $task) {
    echo $task->category->name;
}
```

この場合、以下のクエリが実行されます。

1. `SELECT * FROM tasks` （1回）
2. `SELECT * FROM categories WHERE id = 1` （タスクの数だけ実行）
3. `SELECT * FROM categories WHERE id = 2`
4. ...

タスクが100件ある場合、**101回のクエリ**が実行されます。

---

### 🔍 Eager Loadingの実装

`with()`メソッドを使うと、リレーションシップを事前に読み込めます。

```php
$tasks = Task::with('category')->get();

foreach ($tasks as $task) {
    echo $task->category->name;
}
```

この場合、以下のクエリが実行されます。

1. `SELECT * FROM tasks` （1回）
2. `SELECT * FROM categories WHERE id IN (1, 2, 3, ...)` （1回）

**合計2回のクエリ**で済みます。

---

### 🔍 コントローラーでEager Loadingを使う

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function index(Request $request)
{
    $query = Task::with(['category', 'tags']);

    // 検索条件
    if ($request->filled('keyword')) {
        $query->where('title', 'like', '%' . $request->keyword . '%');
    }

    if ($request->filled('category_id')) {
        $query->where('category_id', $request->category_id);
    }

    if ($request->filled('status')) {
        $query->where('status', $request->status);
    }

    $tasks = $query->orderBy('created_at', 'desc')->paginate(10);

    $categories = Category::all();

    return view('tasks.index', compact('tasks', 'categories'));
}
```

---

### 🔍 複数のリレーションシップを読み込む

```php
$tasks = Task::with(['category', 'tags', 'user'])->get();
```

---

### 🔍 ネストしたリレーションシップを読み込む

```php
$tasks = Task::with(['category.parent', 'tags'])->get();
```

---

### 🔍 Laravel Debugbarのインストール

**Laravel Debugbar**は、実行されたクエリを確認できるツールです。

```bash
composer require barryvdh/laravel-debugbar --dev
```

インストール後、ブラウザでページを開くと、画面下部にデバッグバーが表示されます。

---

### 🔍 クエリの確認

デバッグバーの「Queries」タブをクリックすると、実行されたクエリが表示されます。

Eager Loadingを使う前と後で、クエリの数を比較してみましょう。

---

### 🔍 load()メソッド

既に取得したモデルに対して、リレーションシップを読み込めます。

```php
$task = Task::find(1);
$task->load('category', 'tags');
```

---

### 🔍 loadMissing()メソッド

まだ読み込まれていないリレーションシップのみを読み込めます。

```php
$task = Task::with('category')->find(1);
$task->loadMissing('tags');  // categoryは既に読み込まれているので、tagsのみ読み込む
```

---

### 🔍 条件付きEager Loading

リレーションシップに条件を付けて読み込めます。

```php
$tasks = Task::with(['tags' => function ($query) {
    $query->where('name', 'like', '%重要%');
}])->get();
```

---

### 💡 TIP: Lazy Eager Loading

`load()`メソッドを使うと、**Lazy Eager Loading**ができます。

```php
$tasks = Task::all();

if ($someCondition) {
    $tasks->load('category', 'tags');
}
```

---

### 🚨 よくある間違い

#### 間違い1: with()を忘れる

**対処法**: リレーションシップを使う場合は、必ず`with()`を使います。

---

#### 間違い2: ページネーションでEager Loadingを忘れる

**対処法**: `paginate()`の前に`with()`を使います。

```php
$tasks = Task::with(['category', 'tags'])->paginate(10);
```

---

#### 間違い3: N+1問題に気づかない

**対処法**: Laravel Debugbarを使って、クエリの数を確認します。

---

## ✨ まとめ

このセクションでは、Eager Loadingによるパフォーマンス改善を学びました。

*   N+1問題を理解し、Eager Loadingで解決した。
*   with()メソッドを使って、リレーションシップを事前に読み込んだ。
*   Laravel Debugbarを使って、実行されたクエリを確認した。

次のセクションでは、リレーションシップを使った検索機能について学びます。

---

## 📝 学習のポイント

- [ ] N+1問題を理解した。
- [ ] with()メソッドを使った。
- [ ] Laravel Debugbarをインストールした。
- [ ] クエリの数を確認した。
