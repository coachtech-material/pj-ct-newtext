# Tutorial 11-5-4: foreachからCollectionメソッドへの書き換え

## 🎯 このセクションで学ぶこと

*   foreachを使ったコードの問題点を理解する。
*   Collectionメソッド（`pluck()`、`map()`、`filter()`）を使って、コードを簡潔にする方法を学ぶ。
*   「foreachおじさん」から脱却する実践演習を行う。

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
| 1 | foreachを特定 | Collectionメソッドで置き換えられるか確認 |
| 2 | 適切なメソッドを選択 | filter、map、pluckなど |
| 3 | リファクタリング | より簡潔なコードに |

> 💡 **ポイント**: 全てのforeachを置き換える必要はありません。可読性が上がる場合に使いましょう。

---

## 導入：なぜCollectionメソッドを使うのか

**foreach**は、配列を処理する基本的な方法ですが、**コードが冗長になりがち**です。

**Collectionメソッド**を使うと、**コードを簡潔に、読みやすく**書けます。

---

## 詳細解説

### 🔍 foreachの問題点

以下のコードは、foreachを使って、ユーザーの名前だけを取得しています。

```php
$users = User::all();
$names = [];

foreach ($users as $user) {
    $names[] = $user->name;
}
```

**問題点**:
*   3行かかっている
*   `$names = [];`の初期化が必要
*   コードが冗長

---

### 🔍 pluck()を使った書き換え

```php
$names = User::all()->pluck('name');
```

**改善点**:
*   1行で書ける
*   初期化が不要
*   コードが簡潔

---

### 🔍 pluck()の使い方

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

### 🔍 pluck()でキーを指定する

`pluck()`の第2引数で、キーを指定できます。

```php
// IDをキーにして、名前を取得
$names = User::all()->pluck('name', 'id');
// 結果: [1 => 'John', 2 => 'Jane', 3 => 'Bob']
```

---

### 🔍 map()を使った書き換え

以下のコードは、foreachを使って、ユーザーの名前を大文字に変換しています。

```php
$users = User::all();
$upperNames = [];

foreach ($users as $user) {
    $upperNames[] = strtoupper($user->name);
}
```

**map()を使った書き換え**:

```php
$upperNames = User::all()->map(function ($user) {
    return strtoupper($user->name);
});
```

---

### 🔍 map()の使い方

`map()`は、**配列の中身を加工する**メソッドです。

```php
// ユーザーの名前を大文字に変換
$upperNames = User::all()->map(function ($user) {
    return strtoupper($user->name);
});

// ユーザーの名前とメールアドレスを結合
$combined = User::all()->map(function ($user) {
    return $user->name . ' (' . $user->email . ')';
});
```

---

### 🔍 アロー関数を使った簡潔な書き方

PHP 7.4以降では、アロー関数を使って、さらに簡潔に書けます。

```php
$upperNames = User::all()->map(fn($user) => strtoupper($user->name));
```

---

### 🔍 filter()を使った書き換え

以下のコードは、foreachを使って、アクティブなユーザーだけを抽出しています。

```php
$users = User::all();
$activeUsers = [];

foreach ($users as $user) {
    if ($user->status == 'active') {
        $activeUsers[] = $user;
    }
}
```

**filter()を使った書き換え**:

```php
$activeUsers = User::all()->filter(function ($user) {
    return $user->status == 'active';
});
```

---

### 🔍 filter()の使い方

`filter()`は、**条件に合うものだけを残す**メソッドです。

```php
// アクティブなユーザーだけを抽出
$activeUsers = User::all()->filter(function ($user) {
    return $user->status == 'active';
});

// タスクが10個以上あるユーザーだけを抽出
$busyUsers = User::all()->filter(function ($user) {
    return $user->tasks->count() >= 10;
});
```

---

### 🔍 メソッドチェーン

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

### 🔍 first()の使い方

`first()`は、**最初の1つを取得**するメソッドです。

```php
// 最初のユーザーを取得
$firstUser = User::all()->first();

// アクティブなユーザーの最初の1人を取得
$firstActiveUser = User::all()
    ->filter(fn($user) => $user->status == 'active')
    ->first();
```

---

### 🔍 count()の使い方

`count()`は、**数を数える**メソッドです。

```php
// ユーザーの数を数える
$userCount = User::all()->count();

// アクティブなユーザーの数を数える
$activeUserCount = User::all()
    ->filter(fn($user) => $user->status == 'active')
    ->count();
```

---

### 🔍 実践演習: 以下のforeachをCollectionメソッドに書き換えてください

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

### 💡 TIP: sum()、avg()、max()、min()

Collectionメソッドには、他にも便利なメソッドがあります。

```php
// タスクの優先度の合計
$totalPriority = Task::all()->sum('priority');

// タスクの優先度の平均
$averagePriority = Task::all()->avg('priority');

// タスクの優先度の最大値
$maxPriority = Task::all()->max('priority');

// タスクの優先度の最小値
$minPriority = Task::all()->min('priority');
```

---

### 🚨 よくある間違い

#### 間違い1: filter()の後にvalues()を忘れる

`filter()`は、キーを保持します。キーをリセットするには、`values()`を使います。

```php
$activeUsers = User::all()
    ->filter(fn($user) => $user->status == 'active')
    ->values();  // キーをリセット
```

---

#### 間違い2: pluck()とmap()を混同する

*   `pluck()`: 特定のカラムだけを抜き出す
*   `map()`: 配列の中身を加工する

---

#### 間違い3: foreachを完全に避ける

Collectionメソッドで表現できない複雑な処理は、foreachを使っても問題ありません。

---

## ✨ まとめ

このセクションでは、foreachからCollectionメソッドへの書き換えを学びました。

*   `pluck()`を使って、特定のカラムだけを抜き出した。
*   `map()`を使って、配列の中身を加工した。
*   `filter()`を使って、条件に合うものだけを残した。

次のセクションでは、重複コードの削除について学びます。

---

## 📝 学習のポイント

- [ ] foreachの問題点を理解した。
- [ ] pluck()を使った。
- [ ] map()を使った。
- [ ] filter()を使った。
- [ ] メソッドチェーンを使った。
