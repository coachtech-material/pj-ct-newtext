# Tutorial 11-5-9: コードの可読性を高める

## 🎯 このセクションで学ぶこと

*   可読性の高いコードとは何かを理解する。
*   コメント、空行、メソッドの分割を使って、コードの可読性を高める方法を学ぶ。
*   命名規則を守ることの重要性を理解する。
*   マジックナンバーを避ける方法を学ぶ。

---

## 導入：なぜ可読性が重要なのか

**可読性の高いコード**は、**他の人が読みやすく、理解しやすい**コードです。

**可読性が低いコード**は、**バグが発生しやすく、メンテナンスが大変**です。

---

## 詳細解説

### 🔍 可読性の低いコードの例

以下のコードは、可読性が低いです。

```php
public function store(Request $request)
{
    $t = new Task();
    $t->t = $request->title;
    $t->d = $request->description;
    $t->s = $request->status;
    $t->u = auth()->id();
    $t->save();
    Mail::to(auth()->user()->email)->send(new TaskCreated($t));
    Log::info('Task created', ['task_id' => $t->id]);
    return redirect()->route('tasks.index');
}
```

**問題点**:
*   変数名が短すぎる（`$t`、`$d`、`$s`、`$u`）
*   何をしているか分かりにくい
*   空行がない

---

### 🔍 可読性を高める

以下のように改善します。

```php
public function store(Request $request)
{
    // タスクを作成
    $task = new Task();
    $task->title = $request->title;
    $task->description = $request->description;
    $task->status = $request->status;
    $task->user_id = auth()->id();
    $task->save();
    
    // メール送信
    Mail::to(auth()->user()->email)->send(new TaskCreated($task));
    
    // ログ記録
    Log::info('Task created', ['task_id' => $task->id]);
    
    return redirect()->route('tasks.index');
}
```

**改善点**:
*   変数名が分かりやすい（`$task`、`$title`、`$description`）
*   コメントがある
*   空行で区切られている

---

### 🔍 コメントの書き方

コメントは、**何をしているか**ではなく、**なぜそうしているか**を書きます。

```php
// ❌ 悪い例
// タスクを保存する
$task->save();

// ✅ 良い例
// タスクを保存してから、メールを送信する
$task->save();
Mail::to(auth()->user()->email)->send(new TaskCreated($task));
```

---

### 🔍 空行の使い方

空行を使って、コードを区切ります。

```php
// タスクを作成
$task = new Task();
$task->title = $request->title;
$task->description = $request->description;
$task->status = $request->status;
$task->user_id = auth()->id();
$task->save();

// メール送信
Mail::to(auth()->user()->email)->send(new TaskCreated($task));

// ログ記録
Log::info('Task created', ['task_id' => $task->id]);
```

---

### 🔍 メソッドの分割

長いメソッドは、小さなメソッドに分割します。

**分割前**:

```php
public function store(Request $request)
{
    $task = new Task();
    $task->title = $request->title;
    $task->description = $request->description;
    $task->status = $request->status;
    $task->user_id = auth()->id();
    $task->save();
    
    Mail::to(auth()->user()->email)->send(new TaskCreated($task));
    Log::info('Task created', ['task_id' => $task->id]);
    
    return redirect()->route('tasks.index');
}
```

**分割後**:

```php
public function store(Request $request)
{
    $task = $this->createTask($request);
    $this->sendNotification($task);
    $this->logTaskCreation($task);
    
    return redirect()->route('tasks.index');
}

private function createTask(Request $request)
{
    $task = new Task();
    $task->title = $request->title;
    $task->description = $request->description;
    $task->status = $request->status;
    $task->user_id = auth()->id();
    $task->save();
    
    return $task;
}

private function sendNotification(Task $task)
{
    Mail::to(auth()->user()->email)->send(new TaskCreated($task));
}

private function logTaskCreation(Task $task)
{
    Log::info('Task created', ['task_id' => $task->id]);
}
```

---

### 🔍 命名規則を守る

**変数名**、**メソッド名**、**クラス名**は、**意味が分かる名前**にします。

**悪い例**:

```php
$t = Task::find(1);
$u = User::find(1);
$d = '2024-01-01';
```

**良い例**:

```php
$task = Task::find(1);
$user = User::find(1);
$date = '2024-01-01';
```

---

### 🔍 マジックナンバーを避ける

**マジックナンバー**は、**意味が分からない数字**のことです。

**悪い例**:

```php
if ($task->priority >= 3) {
    // 何かをする
}
```

**良い例**:

```php
const HIGH_PRIORITY = 3;

if ($task->priority >= self::HIGH_PRIORITY) {
    // 何かをする
}
```

---

### 🔍 早期リターンを使う

**早期リターン**を使うと、ネストが浅くなります。

**悪い例**:

```php
public function update(Request $request, Task $task)
{
    if ($task->user_id === auth()->id()) {
        $task->title = $request->title;
        $task->description = $request->description;
        $task->status = $request->status;
        $task->save();
        
        return redirect()->route('tasks.index');
    } else {
        abort(403);
    }
}
```

**良い例**:

```php
public function update(Request $request, Task $task)
{
    if ($task->user_id !== auth()->id()) {
        abort(403);
    }
    
    $task->title = $request->title;
    $task->description = $request->description;
    $task->status = $request->status;
    $task->save();
    
    return redirect()->route('tasks.index');
}
```

---

### 🔍 三項演算子を使いすぎない

**三項演算子**は、短く書けますが、読みにくくなることがあります。

**悪い例**:

```php
$status = $task->status === 'completed' ? 'Completed' : ($task->status === 'in_progress' ? 'In Progress' : 'Pending');
```

**良い例**:

```php
if ($task->status === 'completed') {
    $status = 'Completed';
} elseif ($task->status === 'in_progress') {
    $status = 'In Progress';
} else {
    $status = 'Pending';
}
```

---

### 🔍 実践演習: 以下のコードの可読性を高めてください

```php
public function index()
{
    $t = Task::where('u', auth()->id())->where('s', 'p')->orderBy('c', 'desc')->get();
    return view('tasks.index', compact('t'));
}
```

---

**解答例**:

```php
public function index()
{
    // ログインユーザーの未着手タスクを取得
    $tasks = Task::where('user_id', auth()->id())
        ->where('status', 'pending')
        ->orderBy('created_at', 'desc')
        ->get();
    
    return view('tasks.index', compact('tasks'));
}
```

---

### 🔍 一貫性を保つ

**コーディングスタイル**は、プロジェクト全体で一貫性を保ちます。

*   インデントは、スペース4つ
*   波括弧は、同じ行に書く
*   変数名は、キャメルケース

---

### 🔍 PSR-12に従う

PHPには、**PSR-12**というコーディング規約があります。

Laravelは、PSR-12に従っています。

**参考**: [PSR-12: Extended Coding Style](https://www.php-fig.org/psr/psr-12/)

---

### 💡 TIP: PHP CS Fixerを使う

**PHP CS Fixer**を使うと、自動的にコーディングスタイルを修正できます。

```bash
composer require --dev friendsofphp/php-cs-fixer
./vendor/bin/php-cs-fixer fix app
```

---

### 🚨 よくある間違い

#### 間違い1: コメントを書きすぎる

コメントは、必要最小限にします。

```php
// ❌ 悪い例
// タスクを取得する
$task = Task::find(1);

// タスクのタイトルを取得する
$title = $task->title;

// タイトルを表示する
echo $title;
```

---

#### 間違い2: 変数名を短くしすぎる

変数名は、意味が分かる長さにします。

```php
// ❌ 悪い例
$t = Task::find(1);

// ✅ 良い例
$task = Task::find(1);
```

---

#### 間違い3: メソッドを分割しすぎる

メソッドを分割しすぎると、逆に分かりにくくなります。

**対処法**: 適度な長さを保ちます。

---

## ✨ まとめ

このセクションでは、コードの可読性を高める方法を学びました。

*   コメント、空行、メソッドの分割を使った。
*   命名規則を守った。
*   マジックナンバーを避けた。
*   早期リターンを使った。

次のセクションでは、リファクタリング演習を行います。

---

## 📝 学習のポイント

- [ ] コメントを適切に書いた。
- [ ] 空行を使った。
- [ ] メソッドを分割した。
- [ ] 命名規則を守った。
- [ ] マジックナンバーを避けた。
