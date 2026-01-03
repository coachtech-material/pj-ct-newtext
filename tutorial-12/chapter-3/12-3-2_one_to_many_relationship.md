# Tutorial 12-3-2: 1対多リレーションシップの実装

## 🎯 このセクションで学ぶこと

- ユーザーとタスクの1対多リレーションシップを実装する方法を学ぶ
- Tinkerでリレーションシップの動作を確認する方法を学ぶ
- ログインユーザーのタスクのみを表示するように実装する

---

## 🧠 先輩エンジニアの思考プロセス

### リレーションシップの実装タイミング

認証ができたら、次は「ユーザーとタスクのリレーションシップ」です。

| 理由 | 説明 |
|:---|:---|
| 「誰のタスク？」を明確にする | 複数のユーザーがシステムを使うようになった |
| データベース設計で準備済み | マイグレーションで`user_id`カラムを追加済み |
| 次の機能の準備 | タスクの所有者チェック、ユーザーごとの表示 |

### 提供コードありきのフロー

今回も「提供コードありき」のフローで進めます：

```
1. 画面アクセス＆エラー確認（現状の問題を確認）
2. Tinker検証（リレーションシップの動作を確認）
3. バックエンド実装（モデルとコントローラーの修正）
4. 動作確認
```

---

## Step 1: 画面アクセス＆エラー確認

### 1-1. 現状の問題を確認する

現在、タスク一覧ページでは**全てのタスクが表示**されています。

```
http://localhost/tasks
```

| 問題 | 説明 |
|:---|:---|
| 全ユーザーのタスクが見える | セキュリティ上の問題 |
| 誰のタスクかわからない | user_idが設定されていない |

### 1-2. データベースを確認する

Tinkerでタスクのuser_idを確認します：

```bash
sail artisan tinker
```

```php
>>> App\Models\Task::all(['id', 'title', 'user_id']);
```

**期待する結果**：`user_id`がnullまたは設定されていないタスクがある

---

## Step 2: Tinker検証

### 2-1. リレーションシップの動作を確認する（実装前）

まず、リレーションシップが定義されていない状態を確認します：

```php
>>> $user = App\Models\User::first();
>>> $user->tasks;
```

**エラー**：
```
BadMethodCallException: Call to undefined method App\Models\User::tasks()
```

**読み解き**：`tasks()`メソッドがUserモデルに定義されていないため、エラーになります。

### 2-2. リレーションシップの概念を理解する

1対多リレーションシップでは、以下のように定義します：

| モデル | メソッド | 意味 |
|:---|:---|:---|
| User | `hasMany(Task::class)` | 1人のユーザーは複数のタスクを持つ |
| Task | `belongsTo(User::class)` | 1つのタスクは1人のユーザーに属する |

---

## Step 3: バックエンド実装

### 3-1. Userモデルにリレーションシップを定義する

**ファイル**: `app/Models/User.php`

```php
/**
 * ユーザーが持つタスク（1対多）
 */
public function tasks()
{
    return $this->hasMany(Task::class);
}
```

**コードリーディング**：

```php
return $this->hasMany(Task::class);
```
→ `hasMany()`は、1対多リレーションシップを定義するメソッドです。Eloquentは、自動的に`tasks`テーブルの`user_id`カラムを外部キーとして使用します。

### 3-2. Taskモデルにリレーションシップを定義する

**ファイル**: `app/Models/Task.php`

```php
/**
 * タスクが属するユーザー（多対1）
 */
public function user()
{
    return $this->belongsTo(User::class);
}
```

**コードリーディング**：

```php
return $this->belongsTo(User::class);
```
→ `belongsTo()`は、多対1リレーションシップを定義するメソッドです。タスクが「どのユーザーに属するか」を取得できます。

### 3-3. Tinkerでリレーションシップを確認する

```bash
sail artisan tinker
```

```php
// ユーザーを取得
>>> $user = App\Models\User::first();

// ユーザーのタスクを取得
>>> $user->tasks;

// タスク数を取得
>>> $user->tasks()->count();

// タスクからユーザーを取得
>>> $task = App\Models\Task::first();
>>> $task->user;
>>> $task->user->name;
```

> **💡 ポイント**: `->tasks`と`->tasks()`の違い

| 書き方 | 戻り値 | 用途 |
|:---|:---|:---|
| `->tasks` | Collection | 全てのタスクを取得 |
| `->tasks()` | クエリビルダー | 条件を追加して取得 |

```php
// 全てのタスクを取得
>>> $user->tasks;

// 条件を追加して取得
>>> $user->tasks()->where('status', 'pending')->get();
```

### 3-4. コントローラーを修正する

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
use Illuminate\Support\Facades\Auth;

/**
 * Display a listing of the resource.
 */
public function index(Request $request)
{
    // ログインユーザーのタスクのみを取得
    $query = Auth::user()->tasks()->with('category');
    
    // 検索条件（既存のコード）
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
$query = Auth::user()->tasks()->with('category');
```
→ `Auth::user()`でログインユーザーを取得し、`->tasks()`でそのユーザーのタスクのクエリビルダーを取得します。

### 3-5. タスク作成時にuser_idを設定する

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
/**
 * Store a newly created resource in storage.
 */
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
        'due_date' => 'nullable|date',
        'category_id' => 'nullable|exists:categories,id',
    ]);

    // ログインユーザーのIDを追加
    $validated['user_id'] = Auth::id();

    Task::create($validated);

    return redirect()->route('tasks.index')->with('success', 'タスクを作成しました。');
}
```

**コードリーディング**：

```php
$validated['user_id'] = Auth::id();
```
→ `Auth::id()`でログインユーザーのIDを取得し、タスクに紐付けます。

---

## Step 4: 動作確認

### 4-1. 複数のユーザーでテストする

1. ユーザー1でログイン
2. タスクを2件作成
3. ログアウト
4. ユーザー2で登録・ログイン
5. タスクを1件作成

### 4-2. タスク一覧を確認する

| ユーザー | 期待する結果 |
|:---|:---|
| ユーザー1 | 自分のタスク2件のみ表示 |
| ユーザー2 | 自分のタスク1件のみ表示 |

### 4-3. Tinkerで確認する

```bash
sail artisan tinker
```

```php
// ユーザー1のタスク数
>>> App\Models\User::find(1)->tasks()->count();
=> 2

// ユーザー2のタスク数
>>> App\Models\User::find(2)->tasks()->count();
=> 1

// タスクの所有者を確認
>>> App\Models\Task::first()->user->name;
```

---

## 💡 TIP: リレーションシップの活用例

### タスクからユーザー名を取得する

```blade
@foreach($tasks as $task)
    <p>タスク: {{ $task->title }}</p>
    <p>作成者: {{ $task->user->name }}</p>
@endforeach
```

### 条件付きでタスクを取得する

```php
// ログインユーザーの「未着手」のタスクのみ取得
$tasks = Auth::user()->tasks()->where('status', 'pending')->get();
```

### ユーザーのタスク数を取得する

```php
$taskCount = Auth::user()->tasks()->count();
```

---

## ✨ まとめ

このセクションでは、「提供コードありき」の開発フローで1対多リレーションシップを実装しました。

| ステップ | 学んだこと |
|:---|:---|
| Step 1 | 現状の問題を確認（全ユーザーのタスクが見える） |
| Step 2 | Tinkerでリレーションシップの動作を確認 |
| Step 3 | `hasMany()`と`belongsTo()`でリレーションシップを定義 |
| Step 4 | 複数ユーザーでの動作確認 |

次のセクションでは、ログインユーザーのタスクのみを表示する実装について詳しく学びます。

---
