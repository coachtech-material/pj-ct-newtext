# Tutorial 12-5-9: コードの可読性を高める

## 🎯 このセクションで学ぶこと

- 可読性の高いコードとは何かを理解する
- コメント、空行、メソッドの分割を使って、コードの可読性を高める方法を学ぶ
- 命名規則を守ることの重要性を理解する
- マジックナンバーを避ける方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜForm Requestの後に『可読性の向上』を行うのか？」

構造的なリファクタリングが終わったら、次は「可読性」です。

---

### 理由1: コードは人が読むもの

コンピュータはどんなコードでも実行できますが、**人が読んで理解する**必要があります。

可読性の高いコードは、バグが少なく、保守しやすいです。

---

### 理由2: 早期リターンの活用

ネストが深いコードは読みにくいです。**早期リターン**を使うとフラットになります。

```php
// ネストが深い
if ($task) {
    if ($task->user_id === auth()->id()) {
        // 処理
    }
}

// 早期リターン
if (!$task) {
    return;
}
if ($task->user_id !== auth()->id()) {
    return;
}
// 処理
```

---

### 理由3: コメントの適切な使用

良いコードは**コメントがなくても理解できる**ことが理想です。

ただし、「なぜ」を説明するコメントは有用です。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | 可読性の低いコードを理解 | 問題点を把握 |
| Step 2 | 命名とコメントを改善 | 意図を明確に |
| Step 3 | 早期リターンを活用 | ネストを減らす |
| Step 4 | メソッドを分割 | 責任を分離 |

> 💡 **ポイント**: 「このコードは何をしているか」ではなく「なぜこうしているか」をコメントしましょう。

---

## Step 1: 可読性の低いコードを理解する

### 1-1. 可読性の低いコードの例

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

---

### 1-2. 問題点

| 問題 | 説明 |
|------|------|
| 変数名が短すぎる | `$t`、`$d`、`$s`、`$u`では何か分からない |
| 空行がない | 処理の区切りが分からない |
| コメントがない | 何をしているか分かりにくい |

---

## Step 2: 命名とコメントを改善する

### 2-1. 変数名を改善する

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

---

### 2-2. 改善点

| 改善 | 説明 |
|------|------|
| 変数名が分かりやすい | `$task`、`$title`、`$description` |
| コメントがある | 処理の意図が分かる |
| 空行で区切られている | 処理のまとまりが分かる |

---

### 2-3. コメントの書き方

コメントは、**何をしているか**ではなく、**なぜそうしているか**を書きます。

```php
// ❌ 悪い例（何をしているか）
// タスクを保存する
$task->save();

// ✅ 良い例（なぜそうしているか）
// タスクを保存してから、メールを送信する（順序が重要）
$task->save();
Mail::to(auth()->user()->email)->send(new TaskCreated($task));
```

---

### 2-4. マジックナンバーを避ける

**マジックナンバー**は、**意味が分からない数字**のことです。

```php
// ❌ 悪い例
if ($task->priority >= 3) {
    // 何かをする
}

// ✅ 良い例
const HIGH_PRIORITY = 3;

if ($task->priority >= self::HIGH_PRIORITY) {
    // 何かをする
}
```

---

## Step 3: 早期リターンを活用する

### 3-1. ネストが深いコードの問題

```php
// ❌ ネストが深い
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

---

### 3-2. 早期リターンで改善

```php
// ✅ 早期リターン
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

**改善点**:

- ネストが浅くなった
- 異常系を先に処理している
- メインの処理が読みやすくなった

---

### 3-3. 複数の条件がある場合

```php
// ❌ ネストが深い
public function show(Task $task)
{
    if ($task) {
        if ($task->user_id === auth()->id()) {
            if ($task->status !== 'deleted') {
                return view('tasks.show', compact('task'));
            }
        }
    }
    abort(404);
}

// ✅ 早期リターン
public function show(Task $task)
{
    if (!$task) {
        abort(404);
    }
    
    if ($task->user_id !== auth()->id()) {
        abort(403);
    }
    
    if ($task->status === 'deleted') {
        abort(404);
    }
    
    return view('tasks.show', compact('task'));
}
```

---

## Step 4: メソッドを分割する

### 4-1. 長いメソッドの問題

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

---

### 4-2. メソッドを分割する

```php
public function store(Request $request)
{
    $task = $this->createTask($request);
    $this->sendNotification($task);
    $this->logTaskCreation($task);
    
    return redirect()->route('tasks.index');
}

private function createTask(Request $request): Task
{
    $task = new Task();
    $task->title = $request->title;
    $task->description = $request->description;
    $task->status = $request->status;
    $task->user_id = auth()->id();
    $task->save();
    
    return $task;
}

private function sendNotification(Task $task): void
{
    Mail::to(auth()->user()->email)->send(new TaskCreated($task));
}

private function logTaskCreation(Task $task): void
{
    Log::info('Task created', ['task_id' => $task->id]);
}
```

---

### 4-3. 改善点

| 改善 | 説明 |
|------|------|
| 責任の分離 | 各メソッドが1つのことだけを行う |
| 再利用性 | 各メソッドを他の場所でも使える |
| テスト容易性 | 各メソッドを個別にテストできる |

---

### 4-4. 三項演算子を使いすぎない

```php
// ❌ 悪い例（読みにくい）
$status = $task->status === 'completed' ? 'Completed' : ($task->status === 'in_progress' ? 'In Progress' : 'Pending');

// ✅ 良い例（読みやすい）
if ($task->status === 'completed') {
    $status = 'Completed';
} elseif ($task->status === 'in_progress') {
    $status = 'In Progress';
} else {
    $status = 'Pending';
}

// ✅ さらに良い例（match式を使う）
$status = match($task->status) {
    'completed' => 'Completed',
    'in_progress' => 'In Progress',
    default => 'Pending',
};
```

---

### 4-5. 実践演習

以下のコードの可読性を高めてください。

```php
public function index()
{
    $t = Task::where('u', auth()->id())->where('s', 'p')->orderBy('c', 'desc')->get();
    return view('tasks.index', compact('t'));
}
```

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

## 🚨 よくある間違い

### 間違い1: コメントを書きすぎる

**問題**: 自明なことにコメントを書くと、ノイズになる

```php
// ❌ 悪い例
// タスクを取得する
$task = Task::find(1);

// タスクのタイトルを取得する
$title = $task->title;

// ✅ 良い例（コメント不要）
$task = Task::find(1);
$title = $task->title;
```

---

### 間違い2: 変数名を短くしすぎる

**問題**: 意味が分からない変数名は、コードを読む人を混乱させる

```php
// ❌ 悪い例
$t = Task::find(1);

// ✅ 良い例
$task = Task::find(1);
```

---

### 間違い3: メソッドを分割しすぎる

**問題**: 過度な分割は、コードの流れを追いにくくする

**対処法**: 適度な長さを保ちます。目安は1メソッド20〜30行程度です。

---

## 💡 TIP: PHP CS Fixerを使う

**PHP CS Fixer**を使うと、自動的にコーディングスタイルを修正できます。

```bash
composer require --dev friendsofphp/php-cs-fixer
./vendor/bin/php-cs-fixer fix app
```

---

## 💡 TIP: PSR-12に従う

PHPには、**PSR-12**というコーディング規約があります。

Laravelは、PSR-12に従っています。

**参考**: [PSR-12: Extended Coding Style](https://www.php-fig.org/psr/psr-12/)

---

## ✨ まとめ

このセクションでは、コードの可読性を高める方法を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | 可読性の低いコードの問題点 |
| Step 2 | 命名とコメントの改善 |
| Step 3 | 早期リターンでネストを減らす |
| Step 4 | メソッドの分割で責任を分離 |

次のセクションでは、リファクタリング演習を行います。

---
