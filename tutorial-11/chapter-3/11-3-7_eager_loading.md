# Tutorial 11-3-7: Eager Loadingによるパフォーマンス改善

## 🎯 このセクションで学ぶこと

- Eager Loadingを使って、N+1問題を解決し、パフォーマンスを改善する方法を学ぶ
- `with()`メソッドを使って、リレーションシップを事前に読み込む方法を学ぶ
- Laravel Debugbarを使って、実行されたクエリを確認する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜタグ機能の後に『Eager Loading』を実装するのか？」

リレーションシップが増えたら、次は「パフォーマンス改善」です。

---

### 理由1: N+1問題が発生している

リレーションシップを使うと、**N+1問題**が発生しやすくなります。

```php
// N+1問題の例
$tasks = Task::all();
foreach ($tasks as $task) {
    echo $task->user->name;  // タスクごとにクエリが発行される
}
```

---

### 理由2: 機能追加後にパフォーマンスを確認

機能を追加したら、**パフォーマンスを確認**するのが良い習慣です。

Laravel Debugbarを使って、発行されているクエリ数を確認します。

---

### 理由3: 実務で必須の知識

N+1問題は、**実務で最もよく遭遇するパフォーマンス問題**の一つです。

Eager Loadingを使って解決する方法を、ここでしっかり学びます。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | N+1問題の確認 | 問題を理解する |
| Step 2 | Laravel Debugbarのインストール | クエリ数を確認 |
| Step 3 | Eager Loadingの適用 | `with()`を使って解決 |
| Step 4 | パフォーマンス改善の確認 | クエリ数が減ったことを確認 |

> 💡 **ポイント**: `with()`を使うと、関連データを事前に取得できます。

---

## Step 1: N+1問題の確認

### 1-1. N+1問題とは

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

### 1-2. なぜN+1問題が起こるのか

Eloquentは**遅延読み込み（Lazy Loading）**がデフォルトです。

```php
$task->category  // このタイミングでクエリが発行される
```

リレーションシップにアクセスするたびに、クエリが発行されます。

---

### 1-3. N+1問題の影響

| タスク数 | クエリ数 | 影響 |
|----------|----------|------|
| 10件 | 11回 | 軽微 |
| 100件 | 101回 | 遅い |
| 1000件 | 1001回 | 非常に遅い |

---

## Step 2: Laravel Debugbarのインストール

### 2-1. Debugbarをインストールする

**Laravel Debugbar**は、実行されたクエリを確認できるツールです。

```bash
composer require barryvdh/laravel-debugbar --dev
```

---

### 2-2. インストールの確認

インストール後、ブラウザでページを開くと、画面下部にデバッグバーが表示されます。

---

### 2-3. クエリの確認

デバッグバーの「Queries」タブをクリックすると、実行されたクエリが表示されます。

- クエリの数
- 各クエリの実行時間
- クエリの内容

---

## Step 3: Eager Loadingの適用

### 3-1. with()メソッドを使う

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

### 3-2. コントローラーでEager Loadingを使う

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function index(Request $request)
{
    // Eager Loadingでカテゴリーとタグを事前に読み込む
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

### 3-3. コードリーディング

#### `Task::with(['category', 'tags'])`

- 複数のリレーションシップを配列で指定できます
- クエリビルダーを返すので、後から条件を追加できます

---

#### ページネーションとEager Loading

```php
$tasks = Task::with(['category', 'tags'])->paginate(10);
```

`paginate()`の前に`with()`を使うことで、ページネーションされたデータにもEager Loadingが適用されます。

---

### 3-4. 複数のリレーションシップを読み込む

```php
// 複数のリレーションシップを読み込む
$tasks = Task::with(['category', 'tags', 'user'])->get();
```

---

### 3-5. ネストしたリレーションシップを読み込む

```php
// カテゴリーの親カテゴリーも読み込む
$tasks = Task::with(['category.parent', 'tags'])->get();
```

ドット記法で、ネストしたリレーションシップを指定できます。

---

## Step 4: パフォーマンス改善の確認

### 4-1. Debugbarでクエリ数を比較する

**Eager Loading前**:

- タスク10件の場合: 21回のクエリ（1 + 10 + 10）
- タスク100件の場合: 201回のクエリ

**Eager Loading後**:

- タスク10件の場合: 3回のクエリ
- タスク100件の場合: 3回のクエリ

---

### 4-2. 動作確認

1. ブラウザでタスク一覧ページにアクセスする
2. Debugbarの「Queries」タブを確認する
3. クエリ数が少ないことを確認する

---

### 4-3. load()メソッド

既に取得したモデルに対して、リレーションシップを読み込めます。

```php
$task = Task::find(1);
$task->load('category', 'tags');
```

---

### 4-4. loadMissing()メソッド

まだ読み込まれていないリレーションシップのみを読み込めます。

```php
$task = Task::with('category')->find(1);
$task->loadMissing('tags');  // categoryは既に読み込まれているので、tagsのみ読み込む
```

---

### 4-5. 条件付きEager Loading

リレーションシップに条件を付けて読み込めます。

```php
$tasks = Task::with(['tags' => function ($query) {
    $query->where('name', 'like', '%重要%');
}])->get();
```

---

## 🚨 よくある間違い

### 間違い1: with()を忘れる

**問題**: N+1問題が発生してパフォーマンスが低下する

**対処法**: リレーションシップを使う場合は、必ず`with()`を使います。

---

### 間違い2: ページネーションでEager Loadingを忘れる

**問題**: ページネーションされたデータでN+1問題が発生する

**対処法**: `paginate()`の前に`with()`を使います。

```php
// 正しい
$tasks = Task::with(['category', 'tags'])->paginate(10);

// 間違い
$tasks = Task::paginate(10);
$tasks->load('category', 'tags');  // これでも動くが、with()の方が効率的
```

---

### 間違い3: N+1問題に気づかない

**問題**: 開発環境では気づかないが、本番環境で遅くなる

**対処法**: Laravel Debugbarを使って、クエリの数を確認します。

---

## 💡 TIP: Lazy Eager Loading

`load()`メソッドを使うと、**Lazy Eager Loading**ができます。

```php
$tasks = Task::all();

if ($someCondition) {
    $tasks->load('category', 'tags');
}
```

条件によってリレーションシップを読み込むかどうかを決められます。

---

## 💡 TIP: N+1問題の自動検出

開発環境でN+1問題を自動検出するパッケージがあります。

```bash
composer require beyondcode/laravel-query-detector --dev
```

N+1問題が発生すると、警告が表示されます。

---

## ✨ まとめ

このセクションでは、Eager Loadingによるパフォーマンス改善を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | N+1問題の原因と影響 |
| Step 2 | Laravel Debugbarでクエリを確認 |
| Step 3 | `with()`でEager Loadingを適用 |
| Step 4 | パフォーマンス改善の確認 |

次のセクションでは、リレーションシップを使った検索機能について学びます。

---
