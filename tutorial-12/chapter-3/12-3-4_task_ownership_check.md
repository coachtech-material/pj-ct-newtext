# Tutorial 12-3-4: タスクの所有者チェック（認可）

## 🎯 このセクションで学ぶこと

- ポリシーを使って、タスクの所有者のみが編集・削除できるようにする方法を学ぶ
- 提供されたBladeの`@can`ディレクティブを読み解く方法を学ぶ
- Tinkerで認可チェックの動作を確認する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 認証と認可の違い

| 概念 | 説明 | 例 |
|:---|:---|:---|
| 認証（Authentication） | 「誰か」を確認する | ログイン |
| 認可（Authorization） | 「何ができるか」を確認する | タスクの編集権限 |

### 現在の問題点

グローバルスコープで一覧表示は制限できましたが、**URLを直接入力**されると他のユーザーのタスクにアクセスできてしまう可能性があります。

```
/tasks/1/edit  ← 他のユーザーのタスクかもしれない
```

### 提供コードありきのフロー

今回も「提供コードありき」のフローで進めます：

```
1. 画面アクセス＆エラー確認（認可エラーを確認）
2. Bladeの解読（@canディレクティブを確認）
3. Tinker検証（認可チェックの動作を確認）
4. バックエンド実装（ポリシーの作成）
5. 動作確認
```

---

## Step 1: 画面アクセス＆エラー確認

### 1-1. 提供されたBladeを確認する

`resources/views/tasks/show.blade.php`を開いて、編集・削除ボタンの部分を確認します。

```blade
@can('update', $task)
    <a href="{{ route('tasks.edit', $task) }}" class="btn btn-primary">編集</a>
@endcan

@can('delete', $task)
    <form action="{{ route('tasks.destroy', $task) }}" method="POST" style="display: inline;">
        @csrf
        @method('DELETE')
        <button type="submit" class="btn btn-danger" onclick="return confirm('本当に削除しますか？')">削除</button>
    </form>
@endcan
```

### 1-2. @canディレクティブを読み解く

```blade
@can('update', $task)
```

**読み解き**：
- `@can`は認可チェックを行うBladeディレクティブ
- 第1引数`'update'`：ポリシーのメソッド名
- 第2引数`$task`：チェック対象のモデル
- 権限がある場合のみ、`@can`と`@endcan`の間のコンテンツが表示される

### 1-3. ブラウザで確認する

```
http://localhost/tasks/1
```

現時点では、ポリシーが定義されていないため、`@can`の中身が表示されない可能性があります。

---

## Step 2: Tinker検証

### 2-1. 認可チェックの動作を確認する（実装前）

```bash
sail artisan tinker
```

```php
>>> $user = App\Models\User::find(1);
>>> $task = App\Models\Task::withoutGlobalScopes()->find(1);
>>> $user->can('update', $task);
```

**期待する結果**：ポリシーが定義されていないため、`false`が返される

### 2-2. ポリシーの概念を理解する

ポリシーは、**認可ロジックをまとめたクラス**です。

| メソッド | 用途 |
|:---|:---|
| `view` | タスクを表示できるか |
| `update` | タスクを更新できるか |
| `delete` | タスクを削除できるか |

---

## Step 3: バックエンド実装

### 3-1. ポリシーを生成する

```bash
sail artisan make:policy TaskPolicy --model=Task
```

**実行結果**：
```
Policy created successfully.
```

`app/Policies/TaskPolicy.php`ファイルが作成されます。

### 3-2. ポリシーを編集する

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

**コードリーディング**：

```php
public function view(User $user, Task $task): bool
```
→ 第1引数`$user`は現在ログインしているユーザー、第2引数`$task`はチェック対象のタスク。

```php
return $task->user_id === $user->id;
```
→ タスクの所有者とログインユーザーが同じかどうかをチェックします。同じ場合は`true`（権限あり）、違う場合は`false`（権限なし）。

### 3-3. Tinkerで認可チェックを確認する

```bash
sail artisan tinker
```

```php
// ユーザーとタスクを取得
>>> $user = App\Models\User::find(1);
>>> $task = App\Models\Task::withoutGlobalScopes()->find(1);

// 認可チェック
>>> $user->can('view', $task);
>>> $user->can('update', $task);
>>> $user->can('delete', $task);
```

**期待する結果**：
- タスクの所有者の場合：`true`
- 他のユーザーの場合：`false`

### 3-4. コントローラーで認可チェックを追加する

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

    $categories = Category::all();
    return view('tasks.edit', compact('task', 'categories'));
}

public function update(Request $request, Task $task)
{
    $this->authorize('update', $task);

    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'due_date' => 'nullable|date',
        'status' => 'required|in:pending,in_progress,completed',
        'category_id' => 'nullable|exists:categories,id',
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

**コードリーディング**：

```php
$this->authorize('view', $task);
```
→ 第1引数はポリシーのメソッド名、第2引数はモデルインスタンス。権限がない場合は、**自動的に403エラー**が返されます。

---

## Step 4: 動作確認

### 4-1. 自分のタスクにアクセスする

1. ユーザーAでログイン
2. 自分のタスクの詳細ページにアクセス

| 確認項目 | 期待する結果 |
|:---|:---|
| 詳細ページが表示される | 正常にアクセスできる |
| 編集ボタンが表示される | `@can('update', $task)`が`true` |
| 削除ボタンが表示される | `@can('delete', $task)`が`true` |

### 4-2. 他のユーザーのタスクにアクセスする

1. ユーザーAでログインし、タスクを作成する（例: ID = 1）
2. ログアウトする
3. ユーザーBでログインする
4. ブラウザで`http://localhost/tasks/1`にアクセスする

| 確認項目 | 期待する結果 |
|:---|:---|
| 403 Forbiddenエラーが表示される | 認可チェックが機能している |

### 4-3. 編集ページに直接アクセスする

```
http://localhost/tasks/1/edit
```

| 確認項目 | 期待する結果 |
|:---|:---|
| 403 Forbiddenエラーが表示される | URLを直接入力しても編集できない |

---

## 💡 TIP: @cannotディレクティブ

権限がない場合に表示したい場合は、`@cannot`を使います。

```blade
@cannot('update', $task)
    <p>このタスクを編集する権限がありません。</p>
@endcannot
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
|:---|:---|
| index | viewAny |
| show | view |
| create | create |
| store | create |
| edit | update |
| update | update |
| destroy | delete |

---

## ✨ まとめ

このセクションでは、「提供コードありき」の開発フローでタスクの所有者チェック（認可）を実装しました。

| ステップ | 学んだこと |
|:---|:---|
| Step 1 | 提供されたBladeの`@can`ディレクティブを読み解く |
| Step 2 | Tinkerで認可チェックの動作を確認 |
| Step 3 | ポリシーを作成して`authorize()`でチェック |
| Step 4 | 自分のタスクと他のユーザーのタスクでの動作確認 |

次のセクションでは、カテゴリー機能の実装について学びます。

---
