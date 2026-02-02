# 13-6-2 タスクCRUD実装

## 🎯 このセクションで学ぶこと

このセクションでは、タスクのCRUD（Create, Read, Update, Delete）機能を実装します。

- ログインユーザーに紐づくタスクの管理
- リレーションを活用したデータ取得
- セレクトボックスでのカテゴリー選択
- 優先度の表示と選択

> **📌 対応Issue**: #5 タスクCRUD実装

---

## 🧠 先輩エンジニアの思考プロセス

タスクCRUDを実装する際、先輩エンジニアは以下のように考えます。

> 「タスクはユーザーに紐づくデータだから、ログインユーザーのタスクだけを表示するようにしよう。また、カテゴリーとのリレーションがあるから、タスク作成時にカテゴリーを選択できるようにする必要がある。」

### タスクCRUDの特徴

| 特徴 | 説明 |
|:---|:---|
| ユーザー紐づき | ログインユーザーのタスクのみ表示・操作 |
| カテゴリー選択 | セレクトボックスでカテゴリーを選択 |
| 優先度 | 低・中・高の3段階で管理 |

---

## 🔀 ブランチの作成

Issue駆動開発のワークフローに従い、まずはIssue #5に対応するブランチを作成します。

```bash
# 現在のブランチを確認（mainにいることを確認）
git branch

# mainブランチの最新状態を取得
git pull origin main

# Issue #5 に対応するブランチを作成して切り替え
git switch -c feature/issue-5-task-crud
```

---

## 🏃 実践

### ステップ1: タスクコントローラの作成

リソースコントローラを作成します。

```bash
# リソースコントローラの作成
sail artisan make:controller TaskController --resource
```

---

### ステップ2: コントローラの実装

`app/Http/Controllers/TaskController.php` を以下のように編集します。

```php
<?php

namespace App\Http\Controllers;

use App\Models\Category;
use App\Models\Task;
use Illuminate\Http\Request;

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
    public function store(Request $request)
    {
        $validated = $request->validate([
            'category_id' => 'required|exists:categories,id',
            'title' => 'required|string|max:255',
            'description' => 'nullable|string|max:1000',
            'priority' => 'required|integer|in:1,2,3',
        ], [
            'category_id.required' => 'カテゴリーを選択してください。',
            'category_id.exists' => '選択されたカテゴリーは存在しません。',
            'title.required' => 'タイトルは必須です。',
            'title.max' => 'タイトルは255文字以内で入力してください。',
            'description.max' => '説明は1000文字以内で入力してください。',
            'priority.required' => '優先度を選択してください。',
            'priority.in' => '優先度は1〜3の値を選択してください。',
        ]);

        // ログインユーザーのIDを追加
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
        // 他のユーザーのタスクにはアクセスできない
        if ($task->user_id !== auth()->id()) {
            abort(403);
        }

        $task->load('category');

        return view('tasks.show', compact('task'));
    }

    /**
     * タスク編集フォームを表示
     */
    public function edit(Task $task)
    {
        // 他のユーザーのタスクにはアクセスできない
        if ($task->user_id !== auth()->id()) {
            abort(403);
        }

        $categories = Category::orderBy('name')->get();

        return view('tasks.edit', compact('task', 'categories'));
    }

    /**
     * タスクを更新
     */
    public function update(Request $request, Task $task)
    {
        // 他のユーザーのタスクにはアクセスできない
        if ($task->user_id !== auth()->id()) {
            abort(403);
        }

        $validated = $request->validate([
            'category_id' => 'required|exists:categories,id',
            'title' => 'required|string|max:255',
            'description' => 'nullable|string|max:1000',
            'priority' => 'required|integer|in:1,2,3',
        ], [
            'category_id.required' => 'カテゴリーを選択してください。',
            'category_id.exists' => '選択されたカテゴリーは存在しません。',
            'title.required' => 'タイトルは必須です。',
            'title.max' => 'タイトルは255文字以内で入力してください。',
            'description.max' => '説明は1000文字以内で入力してください。',
            'priority.required' => '優先度を選択してください。',
            'priority.in' => '優先度は1〜3の値を選択してください。',
        ]);

        $task->update($validated);

        return redirect()->route('tasks.index')
            ->with('success', 'タスクを更新しました。');
    }

    /**
     * タスクを削除
     */
    public function destroy(Task $task)
    {
        // 他のユーザーのタスクにはアクセスできない
        if ($task->user_id !== auth()->id()) {
            abort(403);
        }

        $task->delete();

        return redirect()->route('tasks.index')
            ->with('success', 'タスクを削除しました。');
    }
}
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `auth()->user()->tasks()` | ログインユーザーのタスクを取得 |
| `->with('category')` | カテゴリー情報をEager Loadingで取得（N+1問題を回避） |
| `->orderBy('priority', 'desc')` | 優先度の高い順にソート |
| `'exists:categories,id'` | categoriesテーブルに存在するIDかを検証 |
| `'in:1,2,3'` | 1, 2, 3のいずれかの値かを検証 |
| `$task->user_id !== auth()->id()` | タスクの所有者チェック |
| `abort(403)` | 403 Forbiddenエラーを返す |

---

### ステップ3: ルーティングの設定

`routes/web.php` にタスクのルーティングを追加します。

```php
<?php

use App\Http\Controllers\CategoryController;
use App\Http\Controllers\TaskController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return redirect()->route('login');
});

// 認証が必要なルート
Route::middleware('auth')->group(function () {
    // カテゴリーのCRUDルート
    Route::resource('categories', CategoryController::class);

    // タスクのCRUDルート
    Route::resource('tasks', TaskController::class);
});
```

---

### ステップ4: ビューの確認

タスク用のビューファイルは、Chapter 3-2で配置済みです。

| ファイル | 説明 |
|:---|:---|
| `resources/views/tasks/index.blade.php` | 一覧画面 |
| `resources/views/tasks/create.blade.php` | 作成画面 |
| `resources/views/tasks/show.blade.php` | 詳細画面 |
| `resources/views/tasks/edit.blade.php` | 編集画面 |

> **📌 補足**: ビューの詳細な内容については、Chapter 3-2「提供アセット」を参照してください。

---

### ステップ5: 動作確認

以下のURLにアクセスして動作を確認してください。

| URL | 機能 |
|:---|:---|
| `http://localhost/tasks` | タスク一覧 |
| `http://localhost/tasks/create` | タスク作成 |
| `http://localhost/tasks/1` | タスク詳細 |
| `http://localhost/tasks/1/edit` | タスク編集 |

#### 確認手順

1. ログインする
2. カテゴリーを作成する（タスク作成に必要）
3. タスク一覧画面にアクセス
4. 「新規作成」からタスクを作成
5. 作成したタスクの詳細を確認
6. タスクを編集
7. タスクを削除

---

## 💡 TIP: Eager Loadingの重要性

リレーションを持つデータを取得する際、Eager Loadingを使わないとN+1問題が発生します。

```php
// ❌ NG: N+1問題が発生
$tasks = Task::all();
foreach ($tasks as $task) {
    echo $task->category->name; // 毎回クエリが発行される
}
// クエリ数: 1（タスク取得）+ N（カテゴリー取得）

// ✅ OK: Eager Loadingで解決
$tasks = Task::with('category')->get();
foreach ($tasks as $task) {
    echo $task->category->name; // 追加クエリなし
}
// クエリ数: 2（タスク取得 + カテゴリー取得）
```

---

## ❌ よくある間違い

### 1. 所有者チェックを忘れる

```php
// ❌ NG: 所有者チェックがない
public function show(Task $task)
{
    return view('tasks.show', compact('task'));
}
// 結果: 他のユーザーのタスクも見れてしまう
```

**対処法**: 必ず所有者チェックを行う（次のセクションでPolicyを使った方法を学びます）。

### 2. user_idを手動で設定し忘れる

```php
// ❌ NG: user_idを設定し忘れ
Task::create($validated);
// エラー: user_id cannot be null
```

**対処法**: `$validated['user_id'] = auth()->id();` を追加する。

---

## ✅ 完了条件

以下の条件を満たしていることを確認してください。

- [ ] TaskControllerが作成されている
- [ ] ルーティングが設定されている
- [ ] タスク一覧が表示される（ログインユーザーのタスクのみ）
- [ ] タスクの作成・編集・削除ができる
- [ ] カテゴリーと優先度が選択できる
- [ ] 他のユーザーのタスクにアクセスすると403エラーになる

---

## ✨ まとめ

このセクションでは、タスクのCRUD機能を実装しました。

| 学んだこと | 内容 |
|:---|:---|
| ユーザー紐づきデータ | `auth()->user()->tasks()` でログインユーザーのデータを取得 |
| Eager Loading | `->with('category')` でN+1問題を回避 |
| 所有者チェック | `$task->user_id !== auth()->id()` で認可チェック |
| セレクトボックス | `<select>` タグでリレーション先を選択 |

次のセクションでは、Policyを使ってより洗練された認可処理を実装します。

---

## 🔄 Git操作とプルリクエスト

作業が完了したら、変更をコミットしてプッシュし、プルリクエストを作成して変更内容を確認しましょう。

### ステップ1: コミットとプッシュ

```bash
# 変更をステージング
git add .

# コミット（Issue番号を含める）
git commit -m "feat: タスクCRUD実装 #5"

# リモートにプッシュ
git push origin feature/issue-5-task-crud
```

### ステップ2: プルリクエストの作成と確認

GitHubでプルリクエストを作成し、変更内容を確認してみましょう。

1. GitHubのリポジトリページを開く
2. 「Pull requests」タブをクリックする
3. 「New pull request」ボタンをクリックする
4. `base: main` ← `compare: feature/issue-5-task-crud` を選択する
5. 「Create pull request」ボタンをクリックする
6. 以下の内容を入力する

**タイトル**:
```
feat: タスクCRUD実装
```

**説明欄**:
```markdown
## 概要
タスクのCRUD機能を実装しました。

## 変更内容
- TaskControllerの作成
- タスク用ビューの作成（index, create, show, edit）
- ルーティングの設定
- 所有者チェックの実装

## 動作確認
- [ ] タスク一覧が表示される
- [ ] タスクの作成ができる
- [ ] タスクの編集ができる
- [ ] タスクの削除ができる
- [ ] 他のユーザーのタスクにアクセスすると403エラーになる

## 対応Issue
close #5
```

7. 「Create pull request」ボタンをクリックする

> **💡 確認ポイント**: PRを作成したら、「Files changed」タブで所有者チェックのコードを確認してみましょう。各メソッドで `$task->user_id !== auth()->id()` のチェックが行われていることを確認できます。

### ステップ3: プルリクエストのマージ

変更内容を確認したら、PRをマージします。

1. PRのページで「Merge pull request」ボタンをクリックする
2. 「Confirm merge」ボタンをクリックする
3. マージが完了すると、Issue #5が自動的にクローズされる

### ステップ4: ローカルのmainブランチを更新し、ブランチを削除

```bash
# mainブランチに切り替え
git switch main

# リモートの変更を取り込む
git pull origin main

# マージ済みのブランチを削除
git branch -d feature/issue-5-task-crud
```

> **📌 Issue対応**: PRをマージすると、説明欄の `close #5` によりIssue #5が自動的にクローズされます。
