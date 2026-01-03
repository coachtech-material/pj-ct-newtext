# Tutorial 12-3-3: ログインユーザーのタスクのみ表示

## 🎯 このセクションで学ぶこと

- ログインユーザーのタスクのみを表示する方法を学ぶ
- グローバルスコープを使って、自動的にフィルタリングする方法を学ぶ
- Tinkerでグローバルスコープの動作を確認する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 現在の問題点

前のセクションで、コントローラーに`Auth::user()->tasks()`を書いてログインユーザーのタスクのみを取得しました。

しかし、この方法には問題があります：

| 問題 | 説明 |
|:---|:---|
| 毎回書く必要がある | すべてのメソッドで`Auth::user()->tasks()`を書く必要がある |
| 書き忘れリスク | 書き忘れると、他のユーザーのタスクが見えてしまう |
| コードが冗長 | 同じコードを何度も書くことになる |

### 解決策：グローバルスコープ

**グローバルスコープ**を使うと、**すべてのクエリに自動的に条件を追加**できます。

```php
// グローバルスコープなし（毎回書く必要がある）
$tasks = Task::where('user_id', auth()->id())->get();

// グローバルスコープあり（自動的にフィルタリング）
$tasks = Task::all();  // 内部で自動的にwhere('user_id', auth()->id())が追加される
```

---

## Step 1: 現在の実装を確認する

### 1-1. Tinkerで現在の動作を確認する

```bash
sail artisan tinker
```

```php
// ログインをシミュレート
>>> auth()->loginUsingId(1);

// 現在の取得方法
>>> auth()->user()->tasks()->get();
```

### 1-2. 問題を再現する

```php
// Task::all()を使うと全ユーザーのタスクが取得される
>>> App\Models\Task::all();
```

**読み解き**：`Task::all()`では、ログインユーザーに関係なく全てのタスクが取得されてしまいます。

---

## Step 2: グローバルスコープの実装

### 2-1. スコープクラスを作成する

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

**コードリーディング**：

```php
implements Scope
```
→ `Scope`インターフェースを実装することで、グローバルスコープとして使えるようになります。

```php
if (auth()->check()) {
```
→ ユーザーがログインしているかどうかを確認します。ログインしていない場合は、条件を追加しません（エラー防止）。

```php
$builder->where('user_id', auth()->id());
```
→ すべてのクエリに、`user_id = ログインユーザーのID`という条件を追加します。

### 2-2. モデルにグローバルスコープを追加する

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
    
    public function category()
    {
        return $this->belongsTo(Category::class);
    }
}
```

**コードリーディング**：

```php
protected static function booted(): void
```
→ モデルが起動されたときに実行されるメソッドです。グローバルスコープの追加など、初期化処理を行います。

```php
static::addGlobalScope(new UserScope());
```
→ `UserScope`をグローバルスコープとして追加します。これにより、すべてのクエリに自動的に条件が追加されます。

---

## Step 3: Tinkerで動作を確認する

### 3-1. グローバルスコープの動作を確認する

```bash
sail artisan tinker
```

```php
// ログインをシミュレート
>>> auth()->loginUsingId(1);

// グローバルスコープが適用される
>>> App\Models\Task::all();
```

**期待する結果**：user_id = 1 のタスクのみが取得される

### 3-2. SQLを確認する

```php
>>> App\Models\Task::toSql();
=> "select * from `tasks` where `user_id` = ?"
```

**読み解き**：`where user_id = ?`が自動的に追加されています。

### 3-3. グローバルスコープを無効化する

```php
// 特定のスコープを無効化
>>> App\Models\Task::withoutGlobalScope(App\Models\Scopes\UserScope::class)->get();

// すべてのグローバルスコープを無効化
>>> App\Models\Task::withoutGlobalScopes()->get();
```

**期待する結果**：全ユーザーのタスクが取得される

> **💡 ポイント**: 管理者画面など、全ユーザーのデータを表示したい場合は、`withoutGlobalScope()`を使います。

---

## Step 4: コントローラーの簡素化

### 4-1. indexメソッドを修正する

グローバルスコープを使うと、コントローラーから`Auth::user()->tasks()`を削除できます。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
/**
 * Display a listing of the resource.
 */
public function index(Request $request)
{
    // where('user_id', auth()->id())が自動的に追加される
    $query = Task::with('category');

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

**コードリーディング**：

```php
$query = Task::with('category');
```
→ `Task::with()`を使っても、グローバルスコープが自動的に適用されます。`Auth::user()->tasks()`を書く必要がなくなりました。

### 4-2. ルートモデルバインディングとグローバルスコープ

グローバルスコープが適用されている場合、ルートモデルバインディングでも自動的にフィルタリングされます。

```php
public function show(Task $task)
{
    // グローバルスコープにより、自動的にログインユーザーのタスクかチェックされる
    // 他のユーザーのタスクにアクセスした場合、404エラーが返される
    return view('tasks.show', compact('task'));
}
```

**実行されるSQL**：
```sql
SELECT * FROM tasks WHERE id = 5 AND user_id = 1;
```

---

## Step 5: 動作確認

### 5-1. 他のユーザーのタスクにアクセスする

1. ユーザーAでログインし、タスクを作成する（例: ID = 1）
2. ログアウトする
3. ユーザーBでログインする
4. ブラウザで`http://localhost/tasks/1`にアクセスする

| 確認項目 | 期待する結果 |
|:---|:---|
| 404エラーが表示される | グローバルスコープにより、ユーザーBのタスクとして検索されるため |

### 5-2. 認証ミドルウェアの確認

1. ログアウトする
2. ブラウザで`http://localhost/tasks`にアクセスする

| 確認項目 | 期待する結果 |
|:---|:---|
| ログインページにリダイレクトされる | 未認証ユーザーはアクセスできない |

---

## 💡 TIP: ローカルスコープとの違い

| スコープ | 適用タイミング | 使い分け |
|:---|:---|:---|
| グローバル | 常に自動的に | セキュリティ、マルチテナント |
| ローカル | 明示的に呼び出したとき | 特定の条件でフィルタリング |

**ローカルスコープの例**：

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

このセクションでは、「提供コードありき」の開発フローでグローバルスコープを実装しました。

| ステップ | 学んだこと |
|:---|:---|
| Step 1 | 現在の実装の問題点をTinkerで確認 |
| Step 2 | グローバルスコープを作成してモデルに追加 |
| Step 3 | Tinkerでグローバルスコープの動作を確認 |
| Step 4 | コントローラーのコードを簡潔に |
| Step 5 | 他のユーザーのタスクにアクセスできないことを確認 |

次のセクションでは、タスクの所有者チェックについて学びます。

---
