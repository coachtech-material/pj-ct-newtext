# Tutorial 11-3-3: ログインユーザーのタスクのみ表示

## 🎯 このセクションで学ぶこと

*   ログインユーザーのタスクのみを表示する方法を学ぶ。
*   グローバルスコープを使って、自動的にフィルタリングする方法を学ぶ。
*   認証ミドルウェアを使って、未ログインユーザーをリダイレクトする方法を学ぶ。

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
| 1 | 一覧表示の修正 | リレーションシップを使って取得 |
| 2 | タスク作成の修正 | ログインユーザーのIDを自動設定 |
| 3 | 動作確認 | 他のユーザーのタスクが見えないことを確認 |

> 💡 **ポイント**: `auth()->user()->tasks`で、ログインユーザーのタスクのみを取得できます。

---

## 導入：なぜログインユーザーのタスクのみ表示するのか

**マルチテナント**なアプリケーションでは、**ログインユーザーのデータのみを表示**する必要があります。

ログインユーザーのタスクのみを表示することで、セキュリティとプライバシーを保護できます。

---

## 詳細解説

### 🔍 現在の実装の確認

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

### 🔍 すべてのメソッドに適用

`show`、`edit`、`update`、`destroy`メソッドでも、ログインユーザーのタスクかどうかをチェックしています。

```php
public function show(Task $task)
{
    if ($task->user_id !== auth()->id()) {
        abort(403, 'このタスクにアクセスする権限がありません。');
    }

    return view('tasks.show', compact('task'));
}
```

---

### 🔍 グローバルスコープの実装

**グローバルスコープ**を使うと、**すべてのクエリに自動的に条件を追加**できます。

**ファイル**: `app/Models/Scopes/UserScope.php`

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class UserScope implements Scope
{
    public function apply(Builder $builder, Model $model)
    {
        $builder->where('user_id', auth()->id());
    }
}
```

---

### 🔍 モデルにグローバルスコープを追加

**ファイル**: `app/Models/Task.php`

```php
use App\Models\Scopes\UserScope;

protected static function booted()
{
    static::addGlobalScope(new UserScope());
}
```

---

### 🔍 コントローラーを簡潔にする

グローバルスコープを使うと、コントローラーから`where('user_id', auth()->id())`を削除できます。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function index(Request $request)
{
    $query = Task::query();  // where('user_id', auth()->id())が自動的に追加される

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

public function show(Task $task)
{
    // グローバルスコープにより、自動的にログインユーザーのタスクかチェックされる
    // 他のユーザーのタスクにアクセスした場合、404エラーが返される
    return view('tasks.show', compact('task'));
}
```

---

### 🔍 グローバルスコープの無効化

グローバルスコープを一時的に無効化できます。

```php
$allTasks = Task::withoutGlobalScope(UserScope::class)->get();
```

---

### 🔍 認証ミドルウェア

`auth`ミドルウェアを使うと、未ログインユーザーをログインページにリダイレクトできます。

**ファイル**: `routes/web.php`

```php
Route::middleware(['auth'])->group(function () {
    Route::get('/tasks', [TaskController::class, 'index'])->name('tasks.index');
    Route::get('/tasks/create', [TaskController::class, 'create'])->name('tasks.create');
    Route::post('/tasks', [TaskController::class, 'store'])->name('tasks.store');
    Route::get('/tasks/{task}', [TaskController::class, 'show'])->name('tasks.show');
    Route::get('/tasks/{task}/edit', [TaskController::class, 'edit'])->name('tasks.edit');
    Route::put('/tasks/{task}', [TaskController::class, 'update'])->name('tasks.update');
    Route::delete('/tasks/{task}', [TaskController::class, 'destroy'])->name('tasks.destroy');
});
```

---

### 🔍 動作確認

1. ログアウトする
2. ブラウザで `http://localhost/tasks` にアクセスする
3. ログインページにリダイレクトされる

---

### 💡 TIP: ローカルスコープとの違い

**ローカルスコープ**は、必要なときだけ適用されるスコープです。

**グローバルスコープ**は、すべてのクエリに自動的に適用されるスコープです。

**ローカルスコープの例**:

```php
public function scopeCompleted($query)
{
    return $query->where('status', '完了');
}

// 使用例
$completedTasks = Task::completed()->get();
```

---

### 🚨 よくある間違い

#### 間違い1: グローバルスコープを適用し忘れる

**対処法**: モデルの`booted()`メソッドで、グローバルスコープを追加します。

---

#### 間違い2: 管理者画面で全ユーザーのデータを表示できない

**対処法**: `withoutGlobalScope()`を使って、グローバルスコープを無効化します。

---

#### 間違い3: 認証ミドルウェアを適用し忘れる

**対処法**: ルーティングに`middleware(['auth'])`を追加します。

---

## ✨ まとめ

このセクションでは、ログインユーザーのタスクのみを表示する方法を学びました。

*   グローバルスコープを使って、自動的にフィルタリングできるようにした。
*   認証ミドルウェアを使って、未ログインユーザーをリダイレクトした。
*   コントローラーのコードを簡潔にした。

次のセクションでは、タスクの所有者チェックについて学びます。

---

## 📝 学習のポイント

- [ ] グローバルスコープを実装した。
- [ ] 認証ミドルウェアを適用した。
- [ ] withoutGlobalScope()を学んだ。
- [ ] ローカルスコープとの違いを理解した。
