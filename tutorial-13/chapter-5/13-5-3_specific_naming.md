# Tutorial 13-5-3: 具体的な命名への変更

## 🎯 このセクションで学ぶこと

- 抽象的な変数名・メソッド名が、なぜコードを読みにくくするのかを理解する
- 具体的な命名に変更することで、コードの可読性を高める方法を学ぶ
- 命名力を高めるための実践演習を行う

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
| Step 1 | 抽象的な命名の問題を理解 | なぜ悪いのかを把握 |
| Step 2 | 変数名を具体的に変更 | 何を表しているかを明確に |
| Step 3 | メソッド名を具体的に変更 | 何をするかを明確に |
| Step 4 | 命名規則を学ぶ | Boolean、配列、メソッドの規則 |

> 💡 **ポイント**: 良い名前は、コメントがなくても意図が伝わります。

---

## Step 1: 抽象的な命名の問題を理解する

### 1-1. 抽象的な命名とは

以下のコードは、抽象的な命名を使っています。

```php
public function index()
{
    $data = Task::all();
    return view('tasks.index', compact('data'));
}
```

**問題点**:

- `$data`が何を表しているのか分からない
- コードを読む人が、コードを追って確認する必要がある

---

### 1-2. よくある抽象的な命名

| 抽象的な命名 | 問題点 |
|------------|--------|
| `$data` | 何のデータか分からない |
| `$result` | 何の結果か分からない |
| `$temp` | 一時的な何か？ |
| `$flag` | 何のフラグか分からない |
| `$i`、`$j` | ループ変数以外では避ける |

---

## Step 2: 変数名を具体的に変更する

### 2-1. 基本的な変更

```php
// Before（抽象的）
public function index()
{
    $data = Task::all();
    return view('tasks.index', compact('data'));
}

// After（具体的）
public function index()
{
    $tasks = Task::all();
    return view('tasks.index', compact('tasks'));
}
```

**改善点**:

- `$tasks`が「タスクの一覧」を表していることが一目で分かる

---

### 2-2. 複雑な例の変更

```php
// Before（抽象的）
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

// After（具体的）
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

---

### 2-3. さらに改善（Eloquentを活用）

```php
public function index()
{
    $activeUsers = User::where('status', 'active')->get();
    return view('users.index', compact('activeUsers'));
}
```

具体的な命名 + Eloquentの活用で、コードがさらに簡潔になりました。

---

## Step 3: メソッド名を具体的に変更する

### 3-1. 抽象的なメソッド名の問題

```php
public function check()
{
    $tasks = Task::where('status', 'pending')->get();
    return $tasks;
}
```

**問題点**:

- `check()`が何をチェックしているのか分からない

---

### 3-2. 具体的なメソッド名への変更

```php
public function fetchPendingTasks()
{
    $tasks = Task::where('status', 'pending')->get();
    return $tasks;
}
```

**改善点**:

- `fetchPendingTasks()`が「保留中のタスクを取得する」ことが一目で分かる

---

### 3-3. よくある抽象的なメソッド名と改善例

| 抽象的 | 具体的な例 |
|--------|-----------|
| `get()` | `fetchLatestTasks()`、`getUserById()` |
| `check()` | `validateInput()`、`isUserActive()` |
| `process()` | `sendEmail()`、`calculateTotal()` |
| `handle()` | `handleTaskCreation()`、`handleUserLogin()` |
| `do()` | `executePayment()`、`performSearch()` |

---

## Step 4: 命名規則を学ぶ

### 4-1. Boolean変数の命名

Boolean変数は、`is`、`has`、`can`などの接頭辞を使います。

```php
// ❌ 抽象的
$flag = true;
$check = false;

// ✅ 具体的
$isActive = true;
$hasPermission = false;
$canEdit = true;
$shouldNotify = false;
```

| 接頭辞 | 用途 | 例 |
|--------|------|-----|
| `is` | 状態を表す | `$isActive`、`$isCompleted` |
| `has` | 所有を表す | `$hasPermission`、`$hasTasks` |
| `can` | 能力を表す | `$canEdit`、`$canDelete` |
| `should` | 条件を表す | `$shouldNotify`、`$shouldRedirect` |

---

### 4-2. 配列・コレクションの命名

配列やコレクションは、**複数形**を使います。

```php
// ❌ 抽象的
$data = Task::all();
$list = User::all();

// ✅ 具体的
$tasks = Task::all();
$users = User::all();
$completedTasks = Task::where('status', 'completed')->get();
```

---

### 4-3. メソッド名の動詞

メソッド名は、**動詞で始める**のが基本です。

```php
// ❌ 名詞で始まる
public function tasks()
{
    return Task::all();
}

// ✅ 動詞で始まる
public function fetchAllTasks()
{
    return Task::all();
}
```

| 動詞 | 用途 | 例 |
|------|------|-----|
| `fetch` / `get` | 取得 | `fetchTasks()`、`getUserById()` |
| `create` / `store` | 作成 | `createTask()`、`storeUser()` |
| `update` | 更新 | `updateTask()`、`updateStatus()` |
| `delete` / `destroy` | 削除 | `deleteTask()`、`destroyUser()` |
| `validate` | 検証 | `validateInput()`、`validateEmail()` |
| `calculate` | 計算 | `calculateTotal()`、`calculateTax()` |

---

### 4-4. 実践演習

以下のコードを具体的な命名に書き換えてください。

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

## 🚨 よくある間違い

### 間違い1: 省略しすぎる

```php
// ❌ 省略しすぎ
$u = User::find(1);
$t = Task::all();

// ✅ 適切
$user = User::find(1);
$tasks = Task::all();
```

---

### 間違い2: 長すぎる命名

```php
// ❌ 長すぎる
$allActiveUsersWhoHaveCompletedTasksInTheLastWeek = User::where('status', 'active')->get();

// ✅ 適切
$activeUsersWithCompletedTasks = User::where('status', 'active')->get();
```

---

### 間違い3: 日本語のローマ字表記

```php
// ❌ ローマ字
$tasuku = Task::all();
$yuza = User::all();

// ✅ 英語
$tasks = Task::all();
$users = User::all();
```

---

## 💡 TIP: 命名の一貫性

プロジェクト全体で、命名の一貫性を保ちます。

- `fetch`、`get`、`retrieve`を混在させない
- `is`、`has`、`can`を統一する
- 同じ概念には同じ名前を使う

---

## ✨ まとめ

このセクションでは、具体的な命名への変更を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | 抽象的な命名の問題点を理解 |
| Step 2 | 変数名を具体的に変更 |
| Step 3 | メソッド名を具体的に変更 |
| Step 4 | Boolean、配列、メソッドの命名規則 |

次のセクションでは、foreachからCollectionメソッドへの書き換えを学びます。

---
