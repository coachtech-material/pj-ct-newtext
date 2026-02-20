# 13-6-3: タスクPolicy実装

## 🎯 このセクションで学ぶこと

このセクションでは、Laravel Policyを使ってタスクの認可処理をリファクタリングします。

- Policyの作成と登録
- Policyメソッドの実装
- コントローラでのPolicy適用
- Bladeテンプレートでの認可チェック

> **📌 対応Issue**: #6 タスクPolicy実装

---

## 🧠 先輩エンジニアの思考プロセス

認可処理をリファクタリングする際、先輩エンジニアは以下のように考えます。

> 「前のセクションでは各メソッドに所有者チェックのコードを書いたが、同じコードが何度も出てきて冗長だ。LaravelにはPolicyという認可専用の仕組みがあるから、これを使ってコードを整理しよう。Policyを使えば、認可ロジックを1箇所にまとめられるし、Bladeテンプレートでも簡単に認可チェックができる。」

### Policyを使うメリット

| メリット | 説明 |
|:---|:---|
| コードの集約 | 認可ロジックを1箇所にまとめられる |
| 再利用性 | 同じ認可ロジックを複数の場所で使える |
| テスト容易性 | 認可ロジックを単独でテストできる |
| Blade連携 | `@can` ディレクティブで簡単に認可チェック |

---

## 🔀 ブランチの作成

Issue駆動開発のワークフローに従い、まずはIssue #6に対応するブランチを作成します。

```bash
# 現在のブランチを確認（mainにいることを確認）
git branch

# mainブランチの最新状態を取得
git pull origin main

# Issue #6 に対応するブランチを作成して切り替え
git switch -c feature/issue-6-task-policy
```

---

## 🏃 実践

### ステップ1: TaskPolicyの作成

Artisanコマンドでポリシーを作成します。

```bash
# ポリシーの作成
sail artisan make:policy TaskPolicy --model=Task
```

#### コマンドのコードリーディング

| オプション | 説明 |
|:---|:---|
| `--model=Task` | Taskモデルに対応するポリシーを作成（CRUDメソッドが自動生成される） |

---

### ステップ2: TaskPolicyの実装

`app/Policies/TaskPolicy.php` を以下のように編集します。

```php
<?php

namespace App\Policies;

use App\Models\Task;
use App\Models\User;

class TaskPolicy
{
    /**
     * タスク詳細を表示できるか
     */
    public function view(User $user, Task $task): bool
    {
        return $user->id === $task->user_id;
    }

    /**
     * タスクを更新できるか
     */
    public function update(User $user, Task $task): bool
    {
        return $user->id === $task->user_id;
    }

    /**
     * タスクを削除できるか
     */
    public function delete(User $user, Task $task): bool
    {
        return $user->id === $task->user_id;
    }
}
```

> **💡 補足**: `--model=Task` オプションで生成されるPolicyには `viewAny`, `create`, `restore`, `forceDelete` メソッドも含まれますが、今回のアプリケーションでは使用しないため削除しています。

#### コードリーディング

| メソッド | 引数 | 説明 |
|:---|:---|:---|
| `view` | `User $user, Task $task` | 詳細表示の認可 |
| `update` | `User $user, Task $task` | 更新の認可 |
| `delete` | `User $user, Task $task` | 削除の認可 |

#### 認可ロジックの解説

```php
public function view(User $user, Task $task): bool
{
    return $user->id === $task->user_id;
}
```

このコードは「ログインユーザーのIDとタスクの所有者IDが一致すれば`true`（許可）、そうでなければ`false`（拒否）」を返します。

---

### ステップ3: Policyの登録

Laravel 10では、Policyは `app/Providers/AuthServiceProvider.php` で登録します。ただし、命名規則（モデル名 + Policy）に従っていれば自動的に検出されるため、明示的な登録は省略可能です。

| モデル | ポリシー | 命名規則 |
|:---|:---|:---|
| `App\Models\Task` | `App\Policies\TaskPolicy` | モデル名 + Policy |

今回は命名規則に従っているため、`AuthServiceProvider` での登録は不要です。

> **💡 補足**: 命名規則に従わない場合は、`app/Providers/AuthServiceProvider.php` の `$policies` プロパティで手動登録が必要です。

---

### ステップ4: コントローラの修正

`app/Http/Controllers/TaskController.php` を修正し、Policyを使った認可に変更します。

```php
<?php

namespace App\Http\Controllers;

use App\Http\Requests\TaskRequest;
use App\Models\Category;
use App\Models\Task;

class TaskController extends Controller
{
    /**
     * タスク一覧を表示
     */
    public function index()
    {
        $tasks = auth()->user()->tasks()
            ->with('category')
            ->orderBy('priority', 'desc')
            ->orderBy('created_at', 'desc')
            ->get();

        return view('tasks.index', compact('tasks'));
    }

    /**
     * タスク作成フォームを表示
     */
    public function create()
    {
        $categories = Category::orderBy('name')->get();

        return view('tasks.create', compact('categories'));
    }

    /**
     * タスクを新規作成
     */
    public function store(TaskRequest $request)
    {
        $validated = $request->validated();
        $validated['user_id'] = auth()->id();

        Task::create($validated);

        return redirect()->route('tasks.index')
            ->with('success', 'タスクを作成しました。');
    }

    /**
     * タスク詳細を表示
     */
    public function show(Task $task)
    {
        // Policyによる認可チェック
        $this->authorize('view', $task);

        $task->load('category');

        return view('tasks.show', compact('task'));
    }

    /**
     * タスク編集フォームを表示
     */
    public function edit(Task $task)
    {
        // Policyによる認可チェック
        $this->authorize('update', $task);

        $categories = Category::orderBy('name')->get();

        return view('tasks.edit', compact('task', 'categories'));
    }

    /**
     * タスクを更新
     */
    public function update(TaskRequest $request, Task $task)
    {
        // Policyによる認可チェック
        $this->authorize('update', $task);

        $task->update($request->validated());

        return redirect()->route('tasks.index')
            ->with('success', 'タスクを更新しました。');
    }

    /**
     * タスクを削除
     */
    public function destroy(Task $task)
    {
        // Policyによる認可チェック
        $this->authorize('delete', $task);

        $task->delete();

        return redirect()->route('tasks.index')
            ->with('success', 'タスクを削除しました。');
    }
}
```

#### コードリーディング（変更点）

| 変更前 | 変更後 | 説明 |
|:---|:---|:---|
| `if ($task->user_id !== auth()->id()) { abort(403); }` | `$this->authorize('view', $task);` | Policyを使った認可チェック |

#### authorizeメソッドの動作

```php
$this->authorize('view', $task);
```

このコードは以下の処理を行います：

1. `TaskPolicy` の `view` メソッドを呼び出す
2. `view` メソッドが `true` を返せば処理を続行
3. `view` メソッドが `false` を返せば403エラーを自動的に返す

<img alt="13-6-3_c1.png" src="https://s3.ap-northeast-1.amazonaws.com/coachtech-lms-bucket-dev/curriculums/images/13-6-3_c1.png">

---

### ステップ5: Bladeテンプレートでの認可チェック

Bladeテンプレートでも `@can` ディレクティブを使って認可チェックができます。

`resources/views/tasks/show.blade.php` のアクションボタン部分に `@can` を追加してみましょう。

**変更前**（Chapter 3-2で配置したコード）:

```blade
{{-- アクションボタン --}}
<div class="flex space-x-4 mt-8 pt-6 border-t border-gray-200">
    <a href="{{ route('tasks.edit', $task) }}" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
        編集
    </a>
    <form action="{{ route('tasks.destroy', $task) }}" method="POST" onsubmit="return confirm('本当に削除しますか？');">
        @csrf
        @method('DELETE')
        <button type="submit" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded">
            削除
        </button>
    </form>
</div>
```

**変更後**（`@can` を追加）:

```blade
{{-- アクションボタン --}}
<div class="flex space-x-4 mt-8 pt-6 border-t border-gray-200">
    @can('update', $task)
        <a href="{{ route('tasks.edit', $task) }}" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
            編集
        </a>
    @endcan
    @can('delete', $task)
        <form action="{{ route('tasks.destroy', $task) }}" method="POST" onsubmit="return confirm('本当に削除しますか？');">
            @csrf
            @method('DELETE')
            <button type="submit" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded">
                削除
            </button>
        </form>
    @endcan
</div>
```

#### コードリーディング

| ディレクティブ | 説明 |
|:---|:---|
| `@can('update', $task)` | TaskPolicyのupdateメソッドがtrueを返す場合のみ表示 |
| `@endcan` | @canの終了 |
| `@cannot('update', $task)` | updateがfalseの場合のみ表示（逆パターン） |

> **💡 補足**: 今回のケースでは、詳細画面には自分のタスクしか表示されないため（コントローラで認可チェック済み）、`@can` の効果は見えにくいです。しかし、将来的に他のユーザーのタスクも閲覧できるような機能を追加した場合に役立ちます。

---

### ステップ6: 動作確認

以下の手順で動作を確認してください。

1. ユーザーAでログインし、タスクを作成
2. ログアウトして、ユーザーBでログイン
3. ユーザーAのタスクのURLに直接アクセス（例: `/tasks/1`）
4. 403エラーが表示されることを確認

---

## 💡 TIP: Policyの便利な使い方

### 1. Responseオブジェクトでカスタムメッセージ

```php
use Illuminate\Auth\Access\Response;

public function update(User $user, Task $task): Response
{
    return $user->id === $task->user_id
        ? Response::allow()
        : Response::deny('このタスクを編集する権限がありません。');
}
```

### 2. before メソッドで管理者を許可

```php
public function before(User $user, string $ability): ?bool
{
    // 管理者は全ての操作を許可
    if ($user->is_admin) {
        return true;
    }

    return null; // 通常の認可チェックを続行
}
```

---

## ❌ よくある間違い

### 1. authorizeの第2引数を忘れる

```php
// ❌ NG: モデルインスタンスを渡し忘れ
$this->authorize('view');
// エラー: Too few arguments
```

**対処法**: `$this->authorize('view', $task)` のようにモデルインスタンスを渡す。

### 2. Policyの命名規則を間違える

```php
// ❌ NG: 命名規則に従っていない
// app/Policies/TasksPolicy.php（複数形）
// app/Policies/Task.php（Policyがない）
```

**対処法**: `{モデル名}Policy` の命名規則に従う（例: `TaskPolicy`）。

### 3. Policyメソッドの引数順序を間違える

```php
// ❌ NG: 引数の順序が逆
public function view(Task $task, User $user): bool
{
    return $user->id === $task->user_id;
}
```

**対処法**: 第1引数は必ず `User $user`、第2引数がモデルインスタンス。

---

## ✅ 完了条件

以下の条件を満たしていることを確認してください。

- [ ] TaskPolicyが作成されている
- [ ] コントローラで `$this->authorize()` を使用している
- [ ] 自分のタスクは編集・削除できる
- [ ] 他人のタスクにアクセスすると403エラーになる

---

## ✨ まとめ

このセクションでは、Laravel Policyを使ってタスクの認可処理をリファクタリングしました。

| 学んだこと | 内容 |
|:---|:---|
| Policyの作成 | `sail artisan make:policy --model=` |
| 認可チェック | `$this->authorize('ability', $model)` |
| Blade連携 | `@can('ability', $model)` ディレクティブ |
| 認可ロジックの集約 | 1箇所にまとめて再利用性を向上 |

次のChapterでは、公開APIを実装します。

---

## 🔄 Git操作とプルリクエスト

作業が完了したら、変更をコミットしてプッシュし、プルリクエストを作成して変更内容を確認しましょう。

### ステップ1: コミットとプッシュ

```bash
# 変更をステージング
git add .

# コミット（Issue番号を含める）
git commit -m "feat: タスクPolicy実装 #6"

# リモートにプッシュ
git push origin feature/issue-6-task-policy
```

### ステップ2: プルリクエストの作成と確認

GitHubでプルリクエストを作成し、変更内容を確認してみましょう。

1. GitHubのリポジトリページを開く
2. 「Pull requests」タブをクリックする
3. 「New pull request」ボタンをクリックする
4. `base: main` ← `compare: feature/issue-6-task-policy` を選択する
5. 「Create pull request」ボタンをクリックする
6. 以下の内容を入力する

**タイトル**:
```
feat: タスクPolicy実装
```

**説明欄**:
```markdown
## 概要
タスクの認可処理をPolicyを使ってリファクタリングしました。

## 変更内容
- TaskPolicyの作成
- TaskControllerの認可処理をPolicyに置き換え
- Bladeテンプレートで@canディレクティブを使用

## 動作確認
- [ ] 自分のタスクは編集・削除できる
- [ ] 他人のタスクにアクセスすると403エラーになる

## 対応Issue
close #6
```

7. 「Create pull request」ボタンをクリックする

> **💡 確認ポイント**: PRを作成したら、「Files changed」タブでコントローラの変更を確認してみましょう。`if ($task->user_id !== auth()->id()) { abort(403); }` が `$this->authorize('view', $task);` に置き換わっていることで、コードがシンプルになっていることがわかります。

### ステップ3: プルリクエストのマージ

変更内容を確認したら、PRをマージします。

1. PRのページで「Merge pull request」ボタンをクリックする
2. 「Confirm merge」ボタンをクリックする
3. マージが完了すると、Issue #6が自動的にクローズされる

### ステップ4: ローカルのmainブランチを更新し、ブランチを削除

```bash
# mainブランチに切り替え
git switch main

# リモートの変更を取り込む
git pull origin main

# マージ済みのブランチを削除
git branch -d feature/issue-6-task-policy
```

> **📌 Issue対応**: PRをマージすると、説明欄の `close #6` によりIssue #6が自動的にクローズされます。
