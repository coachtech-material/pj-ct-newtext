# Tutorial 11-5-3: 具体的な命名への変更

## 🎯 このセクションで学ぶこと

*   抽象的な変数名・メソッド名が、なぜコードを読みにくくするのかを理解する。
*   具体的な命名に変更することで、コードの可読性を高める方法を学ぶ。
*   命名力を高めるための実践演習を行う。

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜDRYの後に『命名』を改善するのか？」

コードの重複を解消したら、次は「命名」です。

---

### 理由1: 読みやすさの基本

コードは**書く時間より読む時間の方が長い**です。

わかりやすい名前をつけることで、将来の自分や他の開発者が理解しやすくなります。

---

### 理由2: 意図を伝える

`$data`より`$taskData`、`$x`より`$taskCount`の方が、**何を表しているかが明確**です。

```php
// 悪い例
$d = Task::all();

// 良い例
$tasks = Task::all();
```

---

### 理由3: リファクタリングの土台

良い命名ができていると、**次のリファクタリングがしやすく**なります。

コードの意図が明確なので、どこを改善すべきかがわかりやすくなります。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| 1 | 曖昧な名前を特定 | `$data`、`$temp`などを探す |
| 2 | 具体的な名前に変更 | 何を表しているかが明確な名前に |
| 3 | 一貫性を確保 | 同じ概念には同じ名前を使う |

> 💡 **ポイント**: 良い名前は、コメントがなくても意図が伝わります。

---

## 導入：なぜ具体的な命名が重要なのか

**抽象的な命名**（例：`$data`、`check()`）は、**コードを読む人に「これは何？」と考えさせてしまいます**。

**具体的な命名**（例：`$activeUsers`、`fetchLatestTasks()`）は、**コードを読むだけで意図が伝わります**。

---

## 詳細解説

### 🔍 抽象的な命名の問題点

以下のコードは、抽象的な命名を使っています。

```php
public function index()
{
    $data = Task::all();
    return view('tasks.index', compact('data'));
}
```

**問題点**:
*   `$data`が何を表しているのか分からない
*   コードを読む人が、コードを追って確認する必要がある

---

### 🔍 具体的な命名への変更

```php
public function index()
{
    $tasks = Task::all();
    return view('tasks.index', compact('tasks'));
}
```

**改善点**:
*   `$tasks`が「タスクの一覧」を表していることが一目で分かる

---

### 🔍 メソッド名の改善

以下のコードは、抽象的なメソッド名を使っています。

```php
public function check()
{
    $tasks = Task::where('status', 'pending')->get();
    return $tasks;
}
```

**問題点**:
*   `check()`が何をチェックしているのか分からない

---

### 🔍 具体的なメソッド名への変更

```php
public function fetchPendingTasks()
{
    $tasks = Task::where('status', 'pending')->get();
    return $tasks;
}
```

**改善点**:
*   `fetchPendingTasks()`が「保留中のタスクを取得する」ことが一目で分かる

---

### 🔍 よくある抽象的な命名

| 抽象的な命名 | 具体的な命名の例 |
|------------|---------------|
| `$data` | `$users`、`$tasks`、`$products` |
| `$result` | `$searchResults`、`$filteredTasks` |
| `$temp` | `$sortedUsers`、`$formattedDate` |
| `$flag` | `$isActive`、`$hasPermission` |
| `$i`、`$j` | `$userIndex`、`$taskIndex` |
| `get()` | `fetchLatestTasks()`、`getUserById()` |
| `check()` | `validateInput()`、`isUserActive()` |
| `process()` | `sendEmail()`、`calculateTotal()` |

---

### 🔍 実践: 抽象的なコードを具体的に書き換える

**Before（抽象的な命名）**:

```php
public function index()
{
    $data = User::all();
    $result = [];
    
    foreach ($data as $item) {
        if ($item->status == 'active') {
            $result[] = $item;
        }
    }
    
    return view('users.index', compact('result'));
}
```

**After（具体的な命名）**:

```php
public function index()
{
    $allUsers = User::all();
    $activeUsers = [];
    
    foreach ($allUsers as $user) {
        if ($user->status == 'active') {
            $activeUsers[] = $user;
        }
    }
    
    return view('users.index', compact('activeUsers'));
}
```

さらに改善（Collectionメソッドを使う）:

```php
public function index()
{
    $activeUsers = User::where('status', 'active')->get();
    return view('users.index', compact('activeUsers'));
}
```

---

### 🔍 Boolean変数の命名

Boolean変数は、`is`、`has`、`can`などの接頭辞を使います。

```php
// ❌ 抽象的
$flag = true;
$check = false;

// ✅ 具体的
$isActive = true;
$hasPermission = false;
$canEdit = true;
```

---

### 🔍 配列・コレクションの命名

配列やコレクションは、複数形を使います。

```php
// ❌ 抽象的
$data = Task::all();
$list = User::all();

// ✅ 具体的
$tasks = Task::all();
$users = User::all();
```

---

### 🔍 メソッド名の動詞

メソッド名は、動詞で始めます。

```php
// ❌ 抽象的
public function tasks()
{
    return Task::all();
}

// ✅ 具体的
public function fetchAllTasks()
{
    return Task::all();
}
```

---

### 🔍 実践演習: 以下のコードを具体的な命名に書き換えてください

```php
public function show($id)
{
    $data = Task::find($id);
    
    if (!$data) {
        return redirect()->route('tasks.index');
    }
    
    $list = $data->user->tasks;
    
    return view('tasks.show', compact('data', 'list'));
}
```

**解答例**:

```php
public function show($id)
{
    $task = Task::find($id);
    
    if (!$task) {
        return redirect()->route('tasks.index');
    }
    
    $userTasks = $task->user->tasks;
    
    return view('tasks.show', compact('task', 'userTasks'));
}
```

---

### 💡 TIP: 命名の一貫性

プロジェクト全体で、命名の一貫性を保ちます。

*   `fetch`、`get`、`retrieve`を混在させない
*   `is`、`has`、`can`を統一する

---

### 🚨 よくある間違い

#### 間違い1: 省略しすぎる

```php
// ❌ 省略しすぎ
$u = User::find(1);
$t = Task::all();

// ✅ 適切
$user = User::find(1);
$tasks = Task::all();
```

---

#### 間違い2: 長すぎる命名

```php
// ❌ 長すぎる
$allActiveUsersWhoHaveCompletedTasksInTheLastWeek = User::where('status', 'active')->get();

// ✅ 適切
$activeUsersWithCompletedTasks = User::where('status', 'active')->get();
```

---

#### 間違い3: 日本語のローマ字表記

```php
// ❌ ローマ字
$tasuku = Task::all();
$yuza = User::all();

// ✅ 英語
$tasks = Task::all();
$users = User::all();
```

---

## ✨ まとめ

このセクションでは、具体的な命名への変更を学びました。

*   抽象的な命名が、コードを読みにくくすることを理解した。
*   `$data`を`$activeUsers`に、`check()`を`fetchLatestTasks()`に変更した。
*   Boolean変数、配列、メソッド名の命名規則を学んだ。

次のセクションでは、foreachからCollectionメソッドへの書き換えを学びます。

---

## 📝 学習のポイント

- [ ] 抽象的な命名の問題点を理解した。
- [ ] 具体的な命名に変更した。
- [ ] Boolean変数の命名規則を学んだ。
- [ ] 命名の一貫性を保つことを学んだ。
