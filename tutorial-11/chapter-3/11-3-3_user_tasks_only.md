# Tutorial 11-3-3: ログインユーザーのタスクのみ表示

## 🎯 このセクションで学ぶこと

- ログインユーザーのタスクのみを表示する方法を学ぶ
- グローバルスコープを使って、自動的にフィルタリングする方法を学ぶ
- 認証ミドルウェアを使って、未ログインユーザーをリダイレクトする方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜリレーションシップの後に『自分のタスクのみ表示』を実装するのか？」

リレーションシップを定義したら、次は「ログインユーザーのタスクのみ表示」です。

---

### 理由1: リレーションシップを活用する

前のセクションで定義したリレーションシップを、**実際に使う**段階です。

```php
// 全タスク取得（これまで）
$tasks = Task::all();

// ログインユーザーのタスクのみ（これから）
$tasks = auth()->user()->tasks;
```

---

### 理由2: セキュリティの第一歩

他のユーザーのタスクが見えてしまうのは、**セキュリティ上の問題**です。

まずは一覧表示で自分のタスクのみ表示するようにします。

---

### 理由3: 次のセクションの準備

一覧表示を修正したら、次は「詳細」「編集」「削除」でも**所有者チェック**が必要です。

このセクションで基本的な考え方を学び、次のセクションで応用します。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | 現在の実装を確認 | whereでフィルタリング |
| Step 2 | グローバルスコープの実装 | 自動的にフィルタリング |
| Step 3 | コントローラーの簡素化 | コードを簡潔に |
| Step 4 | 動作確認 | 他のユーザーのタスクが見えないことを確認 |

> 💡 **ポイント**: `auth()->user()->tasks`で、ログインユーザーのタスクのみを取得できます。

---

## Step 1: 現在の実装を確認する

### 1-1. indexメソッドの確認

現在の`index`メソッドでは、`where('user_id', auth()->id())`を使って、ログインユーザーのタスクのみを取得しています。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function index(Request $request)
{
    $query = Task::where('user_id', auth()->id());

    // 検索条件
    if ($request->filled('keyword')) {
        $query->where('title', 'like', '%' . $request->keyword . '%');
    }

    if ($request->filled('status')) {
        $query->where('status', $request->status);
    }

    $tasks = $query->orderBy('created_at', 'desc')->paginate(10);

    return view('tasks.index', compact('tasks'));
}
```

---

### 1-2. 問題点

現在の実装には、以下の問題があります。

- **毎回`where('user_id', auth()->id())`を書く必要がある**
- **書き忘れると、他のユーザーのタスクが見えてしまう**
- **コードが冗長になる**

---

## Step 2: グローバルスコープの実装

### 2-1. グローバルスコープとは

**グローバルスコープ**を使うと、**すべてのクエリに自動的に条件を追加**できます。

これにより、`where('user_id', auth()->id())`を毎回書く必要がなくなります。

---

### 2-2. スコープクラスを作成する

**ファイル**: `app/Models/Scopes/UserScope.php`

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class UserScope implements Scope
{
    /**
     * Apply the scope to a given Eloquent query builder.
     */
    public function apply(Builder $builder, Model $model): void
    {
        if (auth()->check()) {
            $builder->where('user_id', auth()->id());
        }
    }
}
```

---

### 2-3. コードリーディング

#### `implements Scope`

- `Scope`インターフェースを実装することで、グローバルスコープとして使えるようになります

---

#### `auth()->check()`

- ユーザーがログインしているかどうかを確認します
- ログインしていない場合は、条件を追加しません（エラー防止）

---

#### `$builder->where('user_id', auth()->id())`

- すべてのクエリに、`user_id = ログインユーザーのID`という条件を追加します

---

### 2-4. モデルにグローバルスコープを追加する

**ファイル**: `app/Models/Task.php`

```php
<?php

namespace App\Models;

use App\Models\Scopes\UserScope;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Task extends Model
{
    use HasFactory;

    protected $fillable = [
        'user_id',
        'category_id',
        'title',
        'description',
        'status',
        'due_date',
    ];

    protected $casts = [
        'due_date' => 'date',
    ];

    /**
     * The "booted" method of the model.
     */
    protected static function booted(): void
    {
        static::addGlobalScope(new UserScope());
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

---

### 2-5. コードリーディング

#### `protected static function booted()`

- モデルが起動されたときに実行されるメソッドです
- グローバルスコープの追加など、初期化処理を行います

---

#### `static::addGlobalScope(new UserScope())`

- `UserScope`をグローバルスコープとして追加します
- これにより、すべてのクエリに自動的に条件が追加されます

---

## Step 3: コントローラーの簡素化

### 3-1. indexメソッドを修正する

グローバルスコープを使うと、コントローラーから`where('user_id', auth()->id())`を削除できます。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function index(Request $request)
{
    // where('user_id', auth()->id())が自動的に追加される
    $query = Task::query();

    // 検索条件
    if ($request->filled('keyword')) {
        $query->where('title', 'like', '%' . $request->keyword . '%');
    }

    if ($request->filled('status')) {
        $query->where('status', $request->status);
    }

    $tasks = $query->orderBy('created_at', 'desc')->paginate(10);

    return view('tasks.index', compact('tasks'));
}
```

---

### 3-2. showメソッドを修正する

```php
public function show(Task $task)
{
    // グローバルスコープにより、自動的にログインユーザーのタスクかチェックされる
    // 他のユーザーのタスクにアクセスした場合、404エラーが返される
    return view('tasks.show', compact('task'));
}
```

---

### 3-3. コードリーディング

#### ルートモデルバインディングとグローバルスコープ

グローバルスコープが適用されている場合、ルートモデルバインディングでも自動的にフィルタリングされます。

```
GET /tasks/5
```

このリクエストでは、以下のSQLが実行されます。

```sql
SELECT * FROM tasks WHERE id = 5 AND user_id = 1;
```

他のユーザーのタスクにアクセスしようとすると、**404エラー**が返されます。

---

### 3-4. グローバルスコープを無効化する

管理者画面など、全ユーザーのデータを表示したい場合は、グローバルスコープを無効化できます。

```php
// 特定のスコープを無効化
$allTasks = Task::withoutGlobalScope(UserScope::class)->get();

// すべてのグローバルスコープを無効化
$allTasks = Task::withoutGlobalScopes()->get();
```

---

## Step 4: 動作確認

### 4-1. 認証ミドルウェアの確認

未ログインユーザーがタスクページにアクセスできないことを確認します。

1. ログアウトする
2. ブラウザで`http://localhost/tasks`にアクセスする
3. ログインページにリダイレクトされる

---

### 4-2. 他のユーザーのタスクにアクセスする

1. ユーザーAでログインし、タスクを作成する（例: ID = 1）
2. ログアウトする
3. ユーザーBでログインする
4. ブラウザで`http://localhost/tasks/1`にアクセスする
5. 404エラーが表示される（グローバルスコープにより、ユーザーBのタスクとして検索されるため）

---

### 4-3. Tinkerで確認する

```bash
php artisan tinker
```

```php
// ログインをシミュレート
>>> auth()->loginUsingId(1);

// グローバルスコープが適用される
>>> App\Models\Task::all();  // user_id = 1 のタスクのみ

// グローバルスコープを無効化
>>> App\Models\Task::withoutGlobalScopes()->get();  // 全タスク
```

---

## 🚨 よくある間違い

### 間違い1: グローバルスコープを適用し忘れる

**問題**: 他のユーザーのタスクが見えてしまう

**対処法**: モデルの`booted()`メソッドで、グローバルスコープを追加します。

---

### 間違い2: 管理者画面で全ユーザーのデータを表示できない

**問題**: グローバルスコープが適用されて、管理者でも自分のデータしか見えない

**対処法**: `withoutGlobalScope()`を使って、グローバルスコープを無効化します。

---

### 間違い3: auth()->check()を忘れる

**エラー**:

```
Attempt to read property "id" on null
```

**対処法**: `auth()->check()`でログイン状態を確認してから、`auth()->id()`を使います。

---

## 💡 TIP: ローカルスコープとの違い

**ローカルスコープ**は、必要なときだけ適用されるスコープです。

**グローバルスコープ**は、すべてのクエリに自動的に適用されるスコープです。

| スコープ | 適用タイミング | 使い分け |
|----------|---------------|----------|
| ローカル | 明示的に呼び出したとき | 特定の条件でフィルタリング |
| グローバル | 常に自動的に | セキュリティ、マルチテナント |

**ローカルスコープの例**:

```php
// モデルに定義
public function scopeCompleted($query)
{
    return $query->where('status', 'completed');
}

// 使用例
$completedTasks = Task::completed()->get();
```

---

## ✨ まとめ

このセクションでは、ログインユーザーのタスクのみを表示する方法を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | 現在の実装の問題点を確認 |
| Step 2 | グローバルスコープで自動フィルタリング |
| Step 3 | コントローラーのコードを簡潔に |
| Step 4 | 動作確認と認証ミドルウェア |

次のセクションでは、タスクの所有者チェックについて学びます。

---
