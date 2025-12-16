# Tutorial 11-3-4: タスクの所有者チェック

## 🎯 このセクションで学ぶこと

*   ポリシーを使って、タスクの所有者のみが編集・削除できるようにする方法を学ぶ。
*   Gate::allows()を使って、認可チェックを行う方法を学ぶ。
*   @canディレクティブを使って、ビューで認可チェックを行う方法を学ぶ。

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ『自分のタスクのみ表示』の後に『所有者チェック』を実装するのか？」

一覧表示を修正したら、次は「詳細」「編集」「削除」の所有者チェックです。

---

### 理由1: URLを直接入力されると危険

一覧表示では自分のタスクのみ表示されますが、**URLを直接入力**されると他のユーザーのタスクにアクセスできてしまいます。

```
/tasks/1  ← 他のユーザーのタスクかもしれない
```

---

### 理由2: 認可（Authorization）の基本

「認証」は「誰か」を確認すること。「認可」は「何ができるか」を確認することです。

このセクションでは、**認可の基本**を学びます。

---

### 理由3: Policyの準備

Laravelには「Policy」という認可の仕組みがあります。

このセクションでは簡単な方法で実装し、後のセクションでPolicyを使った方法を学びます。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| 1 | 詳細表示の所有者チェック | 自分のタスクのみ表示 |
| 2 | 編集の所有者チェック | 自分のタスクのみ編集 |
| 3 | 削除の所有者チェック | 自分のタスクのみ削除 |

> 💡 **ポイント**: 所有者チェックは、セキュリティ上非常に重要です。必ず実装しましょう。

---

## 導入：なぜタスクの所有者チェックが重要なのか

**認可（Authorization）**は、**ユーザーが特定のアクションを実行する権限があるかどうかをチェック**する機能です。

タスクの所有者チェックを実装することで、他のユーザーのタスクを編集・削除できないようにできます。

---

## 詳細解説

### 🔍 ポリシーの作成

**ポリシー**は、**認可ロジックをまとめたクラス**です。

```bash
php artisan make:policy TaskPolicy --model=Task
```

**ファイル**: `app/Policies/TaskPolicy.php`

```php
<?php

namespace App\Policies;

use App\Models\Task;
use App\Models\User;

class TaskPolicy
{
    /**
     * タスクを表示できるか
     */
    public function view(User $user, Task $task)
    {
        return $task->user_id === $user->id;
    }

    /**
     * タスクを更新できるか
     */
    public function update(User $user, Task $task)
    {
        return $task->user_id === $user->id;
    }

    /**
     * タスクを削除できるか
     */
    public function delete(User $user, Task $task)
    {
        return $task->user_id === $user->id;
    }
}
```

---

### 🔍 ポリシーの登録

Laravel 11では、ポリシーは自動的に検出されます。

Laravel 10以前では、`AuthServiceProvider`で登録する必要があります。

**ファイル**: `app/Providers/AuthServiceProvider.php`

```php
protected $policies = [
    Task::class => TaskPolicy::class,
];
```

---

### 🔍 コントローラーで認可チェック

`authorize()`メソッドを使って、認可チェックを行います。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function show(Task $task)
{
    $this->authorize('view', $task);

    return view('tasks.show', compact('task'));
}

public function edit(Task $task)
{
    $this->authorize('update', $task);

    return view('tasks.edit', compact('task'));
}

public function update(Request $request, Task $task)
{
    $this->authorize('update', $task);

    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'due_date' => 'nullable|date',
        'status' => 'required|in:未完了,完了',
    ]);

    $task->update($validated);

    return redirect()->route('tasks.show', $task)->with('success', 'タスクを更新しました。');
}

public function destroy(Task $task)
{
    $this->authorize('delete', $task);

    $task->delete();

    return redirect()->route('tasks.index')->with('success', 'タスクを削除しました。');
}
```

---

### 🔍 authorize()メソッド

`authorize()`メソッドは、**認可チェックを行い、権限がない場合は403エラーを返す**メソッドです。

```php
$this->authorize('update', $task);
```

*   第1引数: ポリシーのメソッド名
*   第2引数: モデルインスタンス

---

### 🔍 動作確認

1. ユーザーAでログインし、タスクを作成する
2. ログアウトする
3. ユーザーBでログインする
4. ユーザーAのタスクのURLに直接アクセスする（例: `http://localhost/tasks/1`）
5. 403エラーが表示される

---

### 🔍 ビューで認可チェック

`@can`ディレクティブを使って、ビューで認可チェックを行います。

**ファイル**: `resources/views/tasks/show.blade.php`

```blade
<h1>タスク詳細</h1>

@if (session('success'))
    <div style="color: green;">
        {{ session('success') }}
    </div>
@endif

<table border="1">
    <!-- ... -->
</table>

@can('update', $task)
    <a href="{{ route('tasks.edit', $task) }}">編集</a>
@endcan

@can('delete', $task)
    <form method="POST" action="{{ route('tasks.destroy', $task) }}" style="display:inline;" onsubmit="return confirm('本当に削除しますか?');">
        @csrf
        @method('DELETE')
        <button type="submit">削除</button>
    </form>
@endcan

<a href="{{ route('tasks.index') }}">一覧に戻る</a>
```

---

### 🔍 Gate::allows()

`Gate::allows()`を使って、コントローラーやビューで認可チェックを行えます。

```php
use Illuminate\Support\Facades\Gate;

if (Gate::allows('update', $task)) {
    // 更新できる
}

if (Gate::denies('update', $task)) {
    // 更新できない
}
```

---

### 🔍 before()メソッド

`before()`メソッドを使うと、**すべての認可チェックの前に実行される処理**を定義できます。

**ファイル**: `app/Policies/TaskPolicy.php`

```php
public function before(User $user, $ability)
{
    // 管理者はすべてのアクションを実行できる
    if ($user->is_admin) {
        return true;
    }
}
```

---

### 💡 TIP: リソースコントローラーの認可

リソースコントローラーでは、`authorizeResource()`メソッドを使って、自動的に認可チェックを行えます。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function __construct()
{
    $this->authorizeResource(Task::class, 'task');
}
```

これにより、各メソッドで自動的に認可チェックが行われます。

---

### 🚨 よくある間違い

#### 間違い1: ポリシーを作成し忘れる

**対処法**: `php artisan make:policy TaskPolicy --model=Task`を実行します。

---

#### 間違い2: authorize()を忘れる

**対処法**: コントローラーのメソッドで`$this->authorize()`を呼び出します。

---

#### 間違い3: ビューで@canを使わない

**対処法**: ビューで`@can`ディレクティブを使って、権限がない場合はボタンを非表示にします。

---

## ✨ まとめ

このセクションでは、タスクの所有者チェックを実装しました。

*   ポリシーを使って、認可ロジックをまとめた。
*   authorize()メソッドを使って、コントローラーで認可チェックを行った。
*   @canディレクティブを使って、ビューで認可チェックを行った。

次のセクションでは、カテゴリー機能の実装について学びます。

---

## 📝 学習のポイント

- [ ] ポリシーを作成した。
- [ ] authorize()メソッドを使った。
- [ ] @canディレクティブを使った。
- [ ] Gate::allows()を学んだ。
