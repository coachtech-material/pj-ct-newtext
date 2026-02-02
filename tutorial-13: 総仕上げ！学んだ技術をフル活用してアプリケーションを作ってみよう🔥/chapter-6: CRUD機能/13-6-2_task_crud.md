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

### ステップ4: ビューの作成

タスク用のビューファイルを作成します。

#### 一覧ビュー（index）

`resources/views/tasks/index.blade.php` を作成します。

```php
@extends('layouts.app')

@section('title', 'タスク一覧')

@section('content')
<div class="card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h2>タスク一覧</h2>
        <a href="{{ route('tasks.create') }}" class="btn btn-primary">新規作成</a>
    </div>

    @if ($tasks->isEmpty())
        <p>タスクがありません。</p>
    @else
        <table style="width: 100%; border-collapse: collapse;">
            <thead>
                <tr style="background-color: #f5f5f5;">
                    <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">タイトル</th>
                    <th style="padding: 10px; text-align: center; border-bottom: 2px solid #ddd;">カテゴリー</th>
                    <th style="padding: 10px; text-align: center; border-bottom: 2px solid #ddd;">優先度</th>
                    <th style="padding: 10px; text-align: center; border-bottom: 2px solid #ddd;">操作</th>
                </tr>
            </thead>
            <tbody>
                @foreach ($tasks as $task)
                    <tr>
                        <td style="padding: 10px; border-bottom: 1px solid #ddd;">
                            <a href="{{ route('tasks.show', $task) }}">{{ $task->title }}</a>
                        </td>
                        <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">
                            {{ $task->category->name }}
                        </td>
                        <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">
                            @php
                                $priorityColors = [
                                    1 => '#28a745', // 低: 緑
                                    2 => '#ffc107', // 中: 黄
                                    3 => '#dc3545', // 高: 赤
                                ];
                            @endphp
                            <span style="display: inline-block; padding: 3px 10px; border-radius: 4px; background-color: {{ $priorityColors[$task->priority] }}; color: {{ $task->priority == 2 ? '#333' : 'white' }}; font-size: 0.875rem;">
                                {{ $task->priority_label }}
                            </span>
                        </td>
                        <td style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">
                            <a href="{{ route('tasks.edit', $task) }}" class="btn btn-secondary" style="padding: 5px 10px; font-size: 0.875rem;">編集</a>
                            <form action="{{ route('tasks.destroy', $task) }}" method="POST" style="display: inline;" onsubmit="return confirm('本当に削除しますか？');">
                                @csrf
                                @method('DELETE')
                                <button type="submit" class="btn btn-danger" style="padding: 5px 10px; font-size: 0.875rem;">削除</button>
                            </form>
                        </td>
                    </tr>
                @endforeach
            </tbody>
        </table>
    @endif
</div>
@endsection
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `$task->category->name` | リレーションを通じてカテゴリー名を取得 |
| `$task->priority_label` | アクセサで優先度のラベルを取得 |
| `@php ... @endphp` | Bladeテンプレート内でPHPコードを実行 |

---

#### 作成フォーム（create）

`resources/views/tasks/create.blade.php` を作成します。

```php
@extends('layouts.app')

@section('title', 'タスク作成')

@section('content')
<div class="card" style="max-width: 600px; margin: 0 auto;">
    <h2 style="margin-bottom: 20px;">タスク作成</h2>

    <form method="POST" action="{{ route('tasks.store') }}">
        @csrf

        <div class="form-group">
            <label for="category_id">カテゴリー</label>
            <select id="category_id" name="category_id" required>
                <option value="">選択してください</option>
                @foreach ($categories as $category)
                    <option value="{{ $category->id }}" {{ old('category_id') == $category->id ? 'selected' : '' }}>
                        {{ $category->name }}
                    </option>
                @endforeach
            </select>
            @error('category_id')
                <p class="error-message">{{ $message }}</p>
            @enderror
        </div>

        <div class="form-group">
            <label for="title">タイトル</label>
            <input type="text" id="title" name="title" value="{{ old('title') }}" required>
            @error('title')
                <p class="error-message">{{ $message }}</p>
            @enderror
        </div>

        <div class="form-group">
            <label for="description">説明</label>
            <textarea id="description" name="description" rows="4">{{ old('description') }}</textarea>
            @error('description')
                <p class="error-message">{{ $message }}</p>
            @enderror
        </div>

        <div class="form-group">
            <label for="priority">優先度</label>
            <select id="priority" name="priority" required>
                <option value="">選択してください</option>
                <option value="1" {{ old('priority') == 1 ? 'selected' : '' }}>低</option>
                <option value="2" {{ old('priority', 2) == 2 ? 'selected' : '' }}>中</option>
                <option value="3" {{ old('priority') == 3 ? 'selected' : '' }}>高</option>
            </select>
            @error('priority')
                <p class="error-message">{{ $message }}</p>
            @enderror
        </div>

        <div style="display: flex; gap: 10px;">
            <button type="submit" class="btn btn-primary">作成</button>
            <a href="{{ route('tasks.index') }}" class="btn btn-secondary">キャンセル</a>
        </div>
    </form>
</div>
@endsection
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `old('category_id') == $category->id ? 'selected' : ''` | バリデーションエラー時に選択状態を復元 |
| `old('priority', 2)` | デフォルト値として2（中）を設定 |

---

#### 詳細ビュー（show）

`resources/views/tasks/show.blade.php` を作成します。

```php
@extends('layouts.app')

@section('title', $task->title)

@section('content')
<div class="card" style="max-width: 800px; margin: 0 auto;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <h2>{{ $task->title }}</h2>
        <a href="{{ route('tasks.index') }}" class="btn btn-secondary">一覧に戻る</a>
    </div>

    <table style="width: 100%; margin-bottom: 20px;">
        <tr>
            <th style="padding: 10px; text-align: left; background-color: #f5f5f5; width: 150px;">カテゴリー</th>
            <td style="padding: 10px;">{{ $task->category->name }}</td>
        </tr>
        <tr>
            <th style="padding: 10px; text-align: left; background-color: #f5f5f5;">優先度</th>
            <td style="padding: 10px;">
                @php
                    $priorityColors = [
                        1 => '#28a745',
                        2 => '#ffc107',
                        3 => '#dc3545',
                    ];
                @endphp
                <span style="display: inline-block; padding: 3px 10px; border-radius: 4px; background-color: {{ $priorityColors[$task->priority] }}; color: {{ $task->priority == 2 ? '#333' : 'white' }};">
                    {{ $task->priority_label }}
                </span>
            </td>
        </tr>
        <tr>
            <th style="padding: 10px; text-align: left; background-color: #f5f5f5;">説明</th>
            <td style="padding: 10px;">{!! nl2br(e($task->description)) ?: '<span style="color: #999;">説明なし</span>' !!}</td>
        </tr>
        <tr>
            <th style="padding: 10px; text-align: left; background-color: #f5f5f5;">作成日時</th>
            <td style="padding: 10px;">{{ $task->created_at->format('Y年m月d日 H:i') }}</td>
        </tr>
        <tr>
            <th style="padding: 10px; text-align: left; background-color: #f5f5f5;">更新日時</th>
            <td style="padding: 10px;">{{ $task->updated_at->format('Y年m月d日 H:i') }}</td>
        </tr>
    </table>

    <div style="display: flex; gap: 10px;">
        <a href="{{ route('tasks.edit', $task) }}" class="btn btn-primary">編集</a>
        <form action="{{ route('tasks.destroy', $task) }}" method="POST" onsubmit="return confirm('本当に削除しますか？');">
            @csrf
            @method('DELETE')
            <button type="submit" class="btn btn-danger">削除</button>
        </form>
    </div>
</div>
@endsection
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `nl2br(e($task->description))` | 改行を`<br>`に変換し、HTMLエスケープ |
| `$task->created_at->format('Y年m月d日 H:i')` | Carbonインスタンスを日本語形式でフォーマット |

---

#### 編集フォーム（edit）

`resources/views/tasks/edit.blade.php` を作成します。

```php
@extends('layouts.app')

@section('title', 'タスク編集')

@section('content')
<div class="card" style="max-width: 600px; margin: 0 auto;">
    <h2 style="margin-bottom: 20px;">タスク編集</h2>

    <form method="POST" action="{{ route('tasks.update', $task) }}">
        @csrf
        @method('PUT')

        <div class="form-group">
            <label for="category_id">カテゴリー</label>
            <select id="category_id" name="category_id" required>
                <option value="">選択してください</option>
                @foreach ($categories as $category)
                    <option value="{{ $category->id }}" {{ old('category_id', $task->category_id) == $category->id ? 'selected' : '' }}>
                        {{ $category->name }}
                    </option>
                @endforeach
            </select>
            @error('category_id')
                <p class="error-message">{{ $message }}</p>
            @enderror
        </div>

        <div class="form-group">
            <label for="title">タイトル</label>
            <input type="text" id="title" name="title" value="{{ old('title', $task->title) }}" required>
            @error('title')
                <p class="error-message">{{ $message }}</p>
            @enderror
        </div>

        <div class="form-group">
            <label for="description">説明</label>
            <textarea id="description" name="description" rows="4">{{ old('description', $task->description) }}</textarea>
            @error('description')
                <p class="error-message">{{ $message }}</p>
            @enderror
        </div>

        <div class="form-group">
            <label for="priority">優先度</label>
            <select id="priority" name="priority" required>
                <option value="">選択してください</option>
                <option value="1" {{ old('priority', $task->priority) == 1 ? 'selected' : '' }}>低</option>
                <option value="2" {{ old('priority', $task->priority) == 2 ? 'selected' : '' }}>中</option>
                <option value="3" {{ old('priority', $task->priority) == 3 ? 'selected' : '' }}>高</option>
            </select>
            @error('priority')
                <p class="error-message">{{ $message }}</p>
            @enderror
        </div>

        <div style="display: flex; gap: 10px;">
            <button type="submit" class="btn btn-primary">更新</button>
            <a href="{{ route('tasks.index') }}" class="btn btn-secondary">キャンセル</a>
        </div>
    </form>
</div>
@endsection
```

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
