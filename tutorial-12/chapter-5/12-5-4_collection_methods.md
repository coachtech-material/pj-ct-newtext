# Tutorial 12-5-4: foreachからCollectionメソッドへの書き換え

## 🎯 このセクションで学ぶこと

- foreachを使ったコードの問題点を理解する
- Collectionメソッド（`pluck()`、`map()`、`filter()`）を使って、コードを簡潔にする方法を学ぶ
- 「foreachおじさん」から脱却する実践演習を行う

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ命名の後に『Collectionメソッド』を学ぶのか？」

命名を改善したら、次は「Collectionメソッド」です。

---

### 理由1: foreachを減らす

PHPでは`foreach`をよく使いますが、Laravelの**Collectionメソッド**を使うとより簡潔に書けます。

```php
// foreachを使う場合
$names = [];
foreach ($tasks as $task) {
    $names[] = $task->name;
}

// Collectionメソッドを使う場合
$names = $tasks->pluck('name');
```

---

### 理由2: 可読性の向上

Collectionメソッドは、**何をしているかが名前から明確**です。

- `filter()`: 条件に合うものだけ残す
- `map()`: 各要素を変換する
- `pluck()`: 特定のカラムだけ取り出す

---

### 理由3: メソッドチェーンで表現力アップ

複数の処理を**メソッドチェーン**で繋げることで、処理の流れが明確になります。

```php
$completedTaskNames = $tasks
    ->filter(fn($task) => $task->is_completed)
    ->pluck('name');
```

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | foreachの問題点を理解 | なぜ改善が必要か |
| Step 2 | pluck()を学ぶ | 特定のカラムを抜き出す |
| Step 3 | map()を学ぶ | 各要素を変換する |
| Step 4 | filter()を学ぶ | 条件でフィルタリング |

> 💡 **ポイント**: 全てのforeachを置き換える必要はありません。可読性が上がる場合に使いましょう。

---

## Step 1: foreachの問題点を理解する

### 1-1. foreachの冗長さ

以下のコードは、foreachを使って、ユーザーの名前だけを取得しています。

```php
$users = User::all();
$names = [];

foreach ($users as $user) {
    $names[] = $user->name;
}
```

**問題点**:

- 3行かかっている
- `$names = [];`の初期化が必要
- コードが冗長

---

### 1-2. Collectionメソッドで解決

```php
$names = User::all()->pluck('name');
```

**改善点**:

- 1行で書ける
- 初期化が不要
- コードが簡潔

---

## Step 2: pluck()を学ぶ

### 2-1. pluck()の基本

`pluck()`は、**特定のカラムだけを抜き出す**メソッドです。

```php
// ユーザーの名前だけを取得
$names = User::all()->pluck('name');
// 結果: ['John', 'Jane', 'Bob']

// ユーザーのメールアドレスだけを取得
$emails = User::all()->pluck('email');
// 結果: ['john@example.com', 'jane@example.com', 'bob@example.com']
```

---

### 2-2. pluck()でキーを指定する

`pluck()`の第2引数で、キーを指定できます。

```php
// IDをキーにして、名前を取得
$names = User::all()->pluck('name', 'id');
// 結果: [1 => 'John', 2 => 'Jane', 3 => 'Bob']
```

これは、フォームのセレクトボックスを作るときに便利です。

```blade
<select name="user_id">
    @foreach($users->pluck('name', 'id') as $id => $name)
        <option value="{{ $id }}">{{ $name }}</option>
    @endforeach
</select>
```

---

## Step 3: map()を学ぶ

### 3-1. map()の基本

`map()`は、**配列の中身を加工する**メソッドです。

**foreachを使った場合**:

```php
$users = User::all();
$upperNames = [];

foreach ($users as $user) {
    $upperNames[] = strtoupper($user->name);
}
```

**map()を使った場合**:

```php
$upperNames = User::all()->map(function ($user) {
    return strtoupper($user->name);
});
```

---

### 3-2. アロー関数を使った簡潔な書き方

PHP 7.4以降では、アロー関数を使って、さらに簡潔に書けます。

```php
$upperNames = User::all()->map(fn($user) => strtoupper($user->name));
```

---

### 3-3. map()の活用例

```php
// ユーザーの名前とメールアドレスを結合
$combined = User::all()->map(function ($user) {
    return $user->name . ' (' . $user->email . ')';
});
// 結果: ['John (john@example.com)', 'Jane (jane@example.com)', ...]

// タスクのタイトルに接頭辞を追加
$prefixedTitles = Task::all()->map(fn($task) => '[タスク] ' . $task->title);
```

---

## Step 4: filter()を学ぶ

### 4-1. filter()の基本

`filter()`は、**条件に合うものだけを残す**メソッドです。

**foreachを使った場合**:

```php
$users = User::all();
$activeUsers = [];

foreach ($users as $user) {
    if ($user->status == 'active') {
        $activeUsers[] = $user;
    }
}
```

**filter()を使った場合**:

```php
$activeUsers = User::all()->filter(function ($user) {
    return $user->status == 'active';
});
```

---

### 4-2. アロー関数を使った簡潔な書き方

```php
$activeUsers = User::all()->filter(fn($user) => $user->status == 'active');
```

---

### 4-3. filter()の活用例

```php
// 完了したタスクだけを抽出
$completedTasks = Task::all()->filter(fn($task) => $task->status == 'completed');

// タスクが10個以上あるユーザーだけを抽出
$busyUsers = User::all()->filter(fn($user) => $user->tasks->count() >= 10);

// 期限が過ぎたタスクだけを抽出
$overdueTasks = Task::all()->filter(fn($task) => $task->due_date < now());
```

---

### 4-4. メソッドチェーン

Collectionメソッドは、**メソッドチェーン**で繋げられます。

```php
// アクティブなユーザーの名前だけを取得
$names = User::all()
    ->filter(fn($user) => $user->status == 'active')
    ->pluck('name');

// アクティブなユーザーの名前を大文字に変換
$upperNames = User::all()
    ->filter(fn($user) => $user->status == 'active')
    ->map(fn($user) => strtoupper($user->name));
```

---

### 4-5. その他の便利なメソッド

| メソッド | 説明 | 例 |
|----------|------|-----|
| `first()` | 最初の1つを取得 | `$users->first()` |
| `count()` | 数を数える | `$users->count()` |
| `sum()` | 合計を計算 | `$tasks->sum('priority')` |
| `avg()` | 平均を計算 | `$tasks->avg('priority')` |
| `max()` | 最大値を取得 | `$tasks->max('priority')` |
| `min()` | 最小値を取得 | `$tasks->min('priority')` |

```php
// 最初のユーザーを取得
$firstUser = User::all()->first();

// アクティブなユーザーの数を数える
$activeUserCount = User::all()
    ->filter(fn($user) => $user->status == 'active')
    ->count();

// タスクの優先度の合計
$totalPriority = Task::all()->sum('priority');
```

---

### 4-6. 実践演習

以下のforeachをCollectionメソッドに書き換えてください。

**問題1**:

```php
$tasks = Task::all();
$titles = [];

foreach ($tasks as $task) {
    $titles[] = $task->title;
}
```

**解答**:

```php
$titles = Task::all()->pluck('title');
```

---

**問題2**:

```php
$tasks = Task::all();
$completedTasks = [];

foreach ($tasks as $task) {
    if ($task->status == 'completed') {
        $completedTasks[] = $task;
    }
}
```

**解答**:

```php
$completedTasks = Task::all()->filter(fn($task) => $task->status == 'completed');
```

---

**問題3**:

```php
$tasks = Task::all();
$uppercaseTitles = [];

foreach ($tasks as $task) {
    $uppercaseTitles[] = strtoupper($task->title);
}
```

**解答**:

```php
$uppercaseTitles = Task::all()->map(fn($task) => strtoupper($task->title));
```

---

## 🚨 よくある間違い

### 間違い1: filter()の後にvalues()を忘れる

`filter()`は、キーを保持します。キーをリセットするには、`values()`を使います。

```php
$activeUsers = User::all()
    ->filter(fn($user) => $user->status == 'active')
    ->values();  // キーをリセット
```

---

### 間違い2: pluck()とmap()を混同する

- `pluck()`: 特定のカラムだけを抜き出す
- `map()`: 配列の中身を加工する

```php
// pluck: カラムを抜き出すだけ
$names = $users->pluck('name');

// map: 加工が必要な場合
$upperNames = $users->map(fn($user) => strtoupper($user->name));
```

---

### 間違い3: foreachを完全に避ける

Collectionメソッドで表現できない複雑な処理は、foreachを使っても問題ありません。

可読性が上がる場合にCollectionメソッドを使いましょう。

---

## ✨ まとめ

このセクションでは、foreachからCollectionメソッドへの書き換えを学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | foreachの問題点を理解 |
| Step 2 | `pluck()`で特定のカラムを抜き出す |
| Step 3 | `map()`で各要素を変換する |
| Step 4 | `filter()`で条件でフィルタリング |

次のセクションでは、重複コードの削除について学びます。

---
