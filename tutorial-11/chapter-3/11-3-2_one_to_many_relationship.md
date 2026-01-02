# Tutorial 11-3-2: 1対多リレーションシップの実装

## 🎯 このセクションで学ぶこと

- ユーザーとタスクの1対多リレーションシップを実装する方法を学ぶ
- Eloquentのリレーションシップメソッドを使ってデータを取得する
- ログインユーザーのタスクのみを表示するように実装する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ認証の後に『リレーションシップ』を実装するのか？」

認証ができたら、次は「ユーザーとタスクのリレーションシップ」です。なぜこのタイミングなのでしょうか？

---

### 理由1: 「誰のタスク？」を明確にする

認証を追加したことで、**複数のユーザー**がシステムを使うようになります。

「このタスクは誰のもの？」を明確にするために、**ユーザーとタスクを紐付ける**必要があります。

---

### 理由2: データベース設計の段階で準備済み

実は、マイグレーションの段階で`user_id`カラムを追加していました。

```php
$table->foreignId('user_id')->constrained()->onDelete('cascade');
```

この外部キーを活用して、リレーションシップを定義します。

---

### 理由3: 次のセクションの準備

リレーションシップを定義すると、以下のことができるようになります：

- ログインユーザーのタスクのみ表示
- タスクの所有者チェック
- ユーザーごとのタスク数カウント

これらは次のセクションで実装します。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | Userモデルにリレーション定義 | `hasMany`でタスクを取得 |
| Step 2 | Taskモデルにリレーション定義 | `belongsTo`でユーザーを取得 |
| Step 3 | コントローラーの修正 | ログインユーザーのタスクのみ表示 |
| Step 4 | 動作確認 | リレーションシップをテスト |

> 💡 **ポイント**: 1対多のリレーションシップでは、「1」側に`hasMany`、「多」側に`belongsTo`を定義します。

---

## Step 1: Userモデルにリレーションシップを定義する

### 1-1. tasksメソッドを追加する

`User`モデルに、タスクとのリレーションシップを定義します。

**ファイル**: `app/Models/User.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;

class User extends Authenticatable
{
    use HasFactory, Notifiable;

    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    protected $hidden = [
        'password',
        'remember_token',
    ];

    protected function casts(): array
    {
        return [
            'email_verified_at' => 'datetime',
            'password' => 'hashed',
        ];
    }

    /**
     * ユーザーが持つタスク（1対多）
     */
    public function tasks()
    {
        return $this->hasMany(Task::class);
    }
}
```

---

### 1-2. コードリーディング

#### `public function tasks()`

- `tasks()`メソッドは、ユーザーが持つタスクを取得するためのリレーションシップメソッドです
- メソッド名は、**複数形**にします（1人のユーザーは複数のタスクを持つため）

---

#### `return $this->hasMany(Task::class)`

- `hasMany()`は、**1対多リレーションシップ**を定義するメソッドです
- `Task::class`は、関連するモデルを指定します
- Eloquentは、自動的に`tasks`テーブルの`user_id`カラムを外部キーとして使用します

---

## Step 2: Taskモデルにリレーションシップを定義する

### 2-1. userメソッドを追加する

`Task`モデルに、ユーザーとのリレーションシップを定義します。

**ファイル**: `app/Models/Task.php`

```php
<?php

namespace App\Models;

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
     * タスクが属するユーザー（多対1）
     */
    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

---

### 2-2. コードリーディング

#### `public function user()`

- `user()`メソッドは、タスクが属するユーザーを取得するためのリレーションシップメソッドです
- メソッド名は、**単数形**にします（1つのタスクは1人のユーザーに属するため）

---

#### `return $this->belongsTo(User::class)`

- `belongsTo()`は、**多対1リレーションシップ**を定義するメソッドです
- `User::class`は、関連するモデルを指定します
- Eloquentは、自動的に`tasks`テーブルの`user_id`カラムを外部キーとして使用します

---

#### 1対多リレーションシップの全体像

| モデル | メソッド | 戻り値 |
|--------|----------|--------|
| User | `tasks()` | 複数のTaskモデル |
| Task | `user()` | 1つのUserモデル |

---

## Step 3: コントローラーの修正

### 3-1. ログインユーザーのタスクのみを表示する

現在、タスク一覧ページでは、全てのタスクが表示されています。

これを、**ログインユーザーのタスクのみを表示する**ように変更します。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Models\Task;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class TaskController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        // ログインユーザーのタスクのみを取得
        $tasks = Auth::user()->tasks()->orderBy('created_at', 'desc')->paginate(10);
        
        return view('tasks.index', compact('tasks'));
    }
}
```

---

### 3-2. コードリーディング

#### `Auth::user()->tasks()`

- `Auth::user()`は、ログインユーザーを取得します
- `->tasks()`は、ユーザーが持つタスクのクエリビルダーを取得します
- これは、`User`モデルで定義した`tasks()`メソッドを使用しています

---

#### `Auth::user()->tasks` と `Auth::user()->tasks()` の違い

| 書き方 | 戻り値 | 用途 |
|--------|--------|------|
| `->tasks` | Collection | 全てのタスクを取得 |
| `->tasks()` | クエリビルダー | 条件を追加して取得 |

```php
// 全てのタスクを取得
$tasks = Auth::user()->tasks;

// 条件を追加して取得
$tasks = Auth::user()->tasks()->where('status', 'pending')->get();
```

---

### 3-3. タスク作成時にuser_idを設定する

タスク作成時に、ログインユーザーのIDを設定します。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
        'due_date' => 'nullable|date',
    ]);

    // ログインユーザーのIDを追加
    $validated['user_id'] = Auth::id();

    Task::create($validated);

    return redirect()->route('tasks.index')->with('success', 'タスクを作成しました。');
}
```

---

### 3-4. コードリーディング

#### `Auth::id()`

- `Auth::id()`は、ログインユーザーのIDを取得します
- `Auth::user()->id`と同じ結果ですが、より簡潔に書けます

---

## Step 4: 動作確認

### 4-1. 複数のユーザーを登録する

1. ユーザー1を登録（例: user1@example.com）
2. タスクを2件作成
3. ログアウト
4. ユーザー2を登録（例: user2@example.com）
5. タスクを1件作成

---

### 4-2. タスク一覧を確認する

1. ユーザー2でログインしている状態で、タスク一覧を確認
2. ユーザー2のタスクのみが表示される（1件）
3. ログアウト
4. ユーザー1でログイン
5. タスク一覧を確認
6. ユーザー1のタスクのみが表示される（2件）

---

### 4-3. Tinkerで確認する

```bash
php artisan tinker
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
>>> $task->user->name;
```

---

## 🚨 よくある間違い

### 間違い1: リレーションシップメソッド名が間違っている

**エラー**:

```
Call to undefined method App\Models\User::task()
```

**対処法**: メソッド名を確認します。1対多の場合は**複数形**、多対1の場合は**単数形**にします。

---

### 間違い2: 外部キーが設定されていない

**エラー**:

```
SQLSTATE[23000]: Integrity constraint violation: 1452 Cannot add or update a child row
```

**対処法**: マイグレーションファイルで、外部キー制約を設定します。

---

### 間違い3: user_idを設定し忘れる

**問題**: タスクを作成しても、誰のタスクかわからない

**対処法**: `store`メソッドで、`$validated['user_id'] = Auth::id();`を追加します。

---

## 💡 TIP: リレーションシップの活用例

### タスクからユーザー名を取得する

```blade
<!-- ビュー -->
@foreach($tasks as $task)
    <p>タスク: {{ $task->title }}</p>
    <p>作成者: {{ $task->user->name }}</p>
@endforeach
```

---

### 条件付きでタスクを取得する

```php
// コントローラー
$tasks = Auth::user()->tasks()->where('status', 'pending')->get();
```

これは、ログインユーザーの「未着手」のタスクのみを取得します。

---

### ユーザーのタスク数を取得する

```php
// コントローラー
$user = Auth::user();
$taskCount = $user->tasks()->count();
echo "タスク数: {$taskCount}";
```

---

## ✨ まとめ

このセクションでは、ユーザーとタスクの1対多リレーションシップの実装について学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | `hasMany()`で1対多リレーションシップを定義 |
| Step 2 | `belongsTo()`で多対1リレーションシップを定義 |
| Step 3 | `Auth::user()->tasks()`でログインユーザーのタスクを取得 |
| Step 4 | 複数ユーザーでの動作確認 |

次のセクションでは、ログインユーザーのタスクのみを表示する実装について詳しく学びます。

---
