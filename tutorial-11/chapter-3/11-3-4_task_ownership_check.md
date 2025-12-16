# Tutorial 11-3-4: タスクの所有者チェック

## 🎯 このセクションで学ぶこと

- ポリシーを使って、タスクの所有者のみが編集・削除できるようにする方法を学ぶ
- `authorize()`メソッドを使って、認可チェックを行う方法を学ぶ
- `@can`ディレクティブを使って、ビューで認可チェックを行う方法を学ぶ

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

### 理由3: Policyの活用

Laravelには「Policy」という認可の仕組みがあります。

Policyを使うことで、認可ロジックを**一箇所にまとめて管理**できます。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | ポリシーの作成 | 認可ロジックをまとめる |
| Step 2 | コントローラーで認可チェック | 権限がない場合は403エラー |
| Step 3 | ビューで認可チェック | 権限がない場合はボタン非表示 |
| Step 4 | 動作確認 | 他のユーザーのタスクにアクセスできないことを確認 |

> 💡 **ポイント**: 所有者チェックは、セキュリティ上非常に重要です。必ず実装しましょう。

---

## Step 1: ポリシーの作成

### 1-1. ポリシーを生成する

**ポリシー**は、**認可ロジックをまとめたクラス**です。

```bash
php artisan make:policy TaskPolicy --model=Task
```

**実行結果**:

```
Policy created successfully.
```

`app/Policies/TaskPolicy.php`ファイルが作成されます。

---

### 1-2. ポリシーを編集する

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
    public function view(User $user, Task $task): bool
    {
        return $task->user_id === $user->id;
    }

    /**
     * タスクを更新できるか
     */
    public function update(User $user, Task $task): bool
    {
        return $task->user_id === $user->id;
    }

    /**
     * タスクを削除できるか
     */
    public function delete(User $user, Task $task): bool
    {
        return $task->user_id === $user->id;
    }
}
```

---

### 1-3. コードリーディング

#### `public function view(User $user, Task $task): bool`

- 第1引数`$user`: 現在ログインしているユーザー
- 第2引数`$task`: チェック対象のタスク
- 戻り値: 権限がある場合は`true`、ない場合は`false`

---

#### `return $task->user_id === $user->id`

- タスクの所有者とログインユーザーが同じかどうかをチェックします
- 同じ場合は`true`（権限あり）、違う場合は`false`（権限なし）

---

### 1-4. ポリシーの登録

Laravel 11では、ポリシーは**自動的に検出**されます。

Laravel 10以前では、`AuthServiceProvider`で登録する必要があります。

**ファイル**: `app/Providers/AuthServiceProvider.php`

```php
use App\Models\Task;
use App\Policies\TaskPolicy;

protected $policies = [
    Task::class => TaskPolicy::class,
];
```

---

## Step 2: コントローラーで認可チェック

### 2-1. authorize()メソッドを使う

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
        'status' => 'required|in:pending,in_progress,completed',
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

### 2-2. コードリーディング

#### `$this->authorize('view', $task)`

- 第1引数: ポリシーのメソッド名
- 第2引数: モデルインスタンス
- 権限がない場合は、**自動的に403エラー**が返されます

---

#### authorize()の動作

| 権限 | 動作 |
|------|------|
| あり | 処理を続行 |
| なし | 403 Forbiddenエラーを返す |

---

## Step 3: ビューで認可チェック

### 3-1. @canディレクティブを使う

`@can`ディレクティブを使って、ビューで認可チェックを行います。

**ファイル**: `resources/views/tasks/show.blade.php`

```blade
<h1>タスク詳細</h1>

@if (session('success'))
    <div style="color: green; margin-bottom: 15px;">
        {{ session('success') }}
    </div>
@endif

<table border="1" style="border-collapse: collapse; width: 100%;">
    <tr>
        <th style="padding: 10px; background-color: #f5f5f5;">タイトル</th>
        <td style="padding: 10px;">{{ $task->title }}</td>
    </tr>
    <tr>
        <th style="padding: 10px; background-color: #f5f5f5;">説明</th>
        <td style="padding: 10px;">{{ $task->description ?? '未設定' }}</td>
    </tr>
    <tr>
        <th style="padding: 10px; background-color: #f5f5f5;">ステータス</th>
        <td style="padding: 10px;">{{ $task->status }}</td>
    </tr>
    <tr>
        <th style="padding: 10px; background-color: #f5f5f5;">期限</th>
        <td style="padding: 10px;">{{ $task->due_date?->format('Y-m-d') ?? '未設定' }}</td>
    </tr>
</table>

<div style="margin-top: 20px;">
    @can('update', $task)
        <a href="{{ route('tasks.edit', $task) }}" style="display: inline-block; padding: 10px 20px; background-color: #2196f3; color: white; text-decoration: none; border-radius: 4px;">編集</a>
    @endcan

    @can('delete', $task)
        <form method="POST" action="{{ route('tasks.destroy', $task) }}" style="display: inline;" onsubmit="return confirm('本当に削除しますか？');">
            @csrf
            @method('DELETE')
            <button type="submit" style="padding: 10px 20px; background-color: #f44336; color: white; border: none; border-radius: 4px; cursor: pointer;">削除</button>
        </form>
    @endcan

    <a href="{{ route('tasks.index') }}" style="margin-left: 10px; color: #666;">← 一覧に戻る</a>
</div>
```

---

### 3-2. コードリーディング

#### `@can('update', $task)`

- 第1引数: ポリシーのメソッド名
- 第2引数: モデルインスタンス
- 権限がある場合のみ、`@can`と`@endcan`の間のコンテンツが表示されます

---

#### `@cannot`ディレクティブ

権限がない場合に表示したい場合は、`@cannot`を使います。

```blade
@cannot('update', $task)
    <p>このタスクを編集する権限がありません。</p>
@endcannot
```

---

## Step 4: 動作確認

### 4-1. 他のユーザーのタスクにアクセスする

1. ユーザーAでログインし、タスクを作成する（例: ID = 1）
2. ログアウトする
3. ユーザーBでログインする
4. ブラウザで`http://localhost/tasks/1`にアクセスする
5. 403 Forbiddenエラーが表示される

---

### 4-2. 編集・削除ボタンの表示を確認する

1. ユーザーAでログインする
2. 自分のタスクの詳細ページにアクセスする
3. 編集ボタンと削除ボタンが表示される
4. ログアウトする
5. ユーザーBでログインする
6. ユーザーAのタスクにはアクセスできない（403エラー）

---

### 4-3. Tinkerで確認する

```bash
php artisan tinker
```

```php
// ユーザーとタスクを取得
>>> $user = App\Models\User::find(1);
>>> $task = App\Models\Task::find(1);

// 認可チェック
>>> $user->can('view', $task);  // true or false
>>> $user->can('update', $task);  // true or false
```

---

## 🚨 よくある間違い

### 間違い1: ポリシーを作成し忘れる

**エラー**:

```
This action is unauthorized.
```

**対処法**: `php artisan make:policy TaskPolicy --model=Task`を実行します。

---

### 間違い2: authorize()を忘れる

**問題**: 他のユーザーのタスクを編集・削除できてしまう

**対処法**: コントローラーのメソッドで`$this->authorize()`を呼び出します。

---

### 間違い3: ビューで@canを使わない

**問題**: 権限がないのに編集・削除ボタンが表示される

**対処法**: ビューで`@can`ディレクティブを使って、権限がない場合はボタンを非表示にします。

---

## 💡 TIP: Gate::allows()

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

## 💡 TIP: before()メソッド

`before()`メソッドを使うと、**すべての認可チェックの前に実行される処理**を定義できます。

**ファイル**: `app/Policies/TaskPolicy.php`

```php
public function before(User $user, string $ability): bool|null
{
    // 管理者はすべてのアクションを実行できる
    if ($user->is_admin) {
        return true;
    }

    return null;  // 通常の認可チェックを続行
}
```

---

## 💡 TIP: authorizeResource()

リソースコントローラーでは、`authorizeResource()`メソッドを使って、自動的に認可チェックを行えます。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function __construct()
{
    $this->authorizeResource(Task::class, 'task');
}
```

これにより、各メソッドで自動的に認可チェックが行われます。

| メソッド | ポリシーメソッド |
|----------|------------------|
| index | viewAny |
| show | view |
| create | create |
| store | create |
| edit | update |
| update | update |
| destroy | delete |

---

## ✨ まとめ

このセクションでは、タスクの所有者チェックを実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | ポリシーを作成して認可ロジックをまとめる |
| Step 2 | `authorize()`でコントローラーで認可チェック |
| Step 3 | `@can`でビューで認可チェック |
| Step 4 | 動作確認 |

次のセクションでは、カテゴリー機能の実装について学びます。

---

## 📝 学習のポイント

- [ ] ポリシーを作成した
- [ ] `authorize()`メソッドを使った
- [ ] `@can`ディレクティブを使った
- [ ] `Gate::allows()`を学んだ
- [ ] `before()`メソッドを学んだ
