# Tutorial 11-3-2: 1対多リレーションシップの実装

## 🎯 このセクションで学ぶこと

*   ユーザーとタスクの1対多リレーションシップを実装する方法を学ぶ。
*   Eloquentのリレーションシップメソッドを使ってデータを取得する。
*   ログインユーザーのタスクのみを表示するように実装する。

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
| 1 | Userモデルにリレーション定義 | `hasMany`でタスクを取得 |
| 2 | Taskモデルにリレーション定義 | `belongsTo`でユーザーを取得 |
| 3 | タスク作成時にuser_idを設定 | ログインユーザーと紐付け |

> 💡 **ポイント**: 1対多のリレーションシップでは、「1」側に`hasMany`、「多」側に`belongsTo`を定義します。

---

## 導入：リレーションシップとは

**リレーションシップ（Relationship）**とは、**テーブル間の関係**です。

タスク管理システムでは、以下のようなリレーションシップがあります。

*   **ユーザーとタスク**: 1対多（1人のユーザーは複数のタスクを持つ）
*   **タスクとカテゴリー**: 多対1（複数のタスクは1つのカテゴリーに属する）

このセクションでは、**ユーザーとタスクの1対多リレーションシップ**を実装します。

---

## 詳細解説

### 🔍 1対多リレーションシップとは

**1対多リレーションシップ**とは、**1つのレコードが複数のレコードと関連する関係**です。

**例**:

*   1人のユーザーは、複数のタスクを持つ
*   1つのカテゴリーは、複数のタスクを持つ

---

### 🔍 Userモデルにリレーションシップを定義する

まず、`User`モデルに、タスクとのリレーションシップを定義します。

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

### 🔍 コードリーディング

#### `public function tasks()`

*   `tasks()`メソッドは、ユーザーが持つタスクを取得するためのリレーションシップメソッドです。
*   メソッド名は、**複数形**にします（1人のユーザーは複数のタスクを持つため）。

---

#### `return $this->hasMany(Task::class)`

*   `hasMany()`は、**1対多リレーションシップ**を定義するメソッドです。
*   `Task::class`は、関連するモデルを指定します。
*   Eloquentは、自動的に`tasks`テーブルの`user_id`カラムを外部キーとして使用します。

---

### 🔍 Taskモデルにリレーションシップを定義する

次に、`Task`モデルに、ユーザーとのリレーションシップを定義します。

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

### 🔍 コードリーディング

#### `public function user()`

*   `user()`メソッドは、タスクが属するユーザーを取得するためのリレーションシップメソッドです。
*   メソッド名は、**単数形**にします（1つのタスクは1人のユーザーに属するため）。

---

#### `return $this->belongsTo(User::class)`

*   `belongsTo()`は、**多対1リレーションシップ**を定義するメソッドです。
*   `User::class`は、関連するモデルを指定します。
*   Eloquentは、自動的に`tasks`テーブルの`user_id`カラムを外部キーとして使用します。

---

### 🔍 ログインユーザーのタスクのみを表示する

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
        $tasks = Auth::user()->tasks;
        
        return view('tasks.index', compact('tasks'));
    }
}
```

---

### 🔍 コードリーディング

#### `Auth::user()->tasks`

*   `Auth::user()`は、ログインユーザーを取得します。
*   `->tasks`は、ユーザーが持つタスクを取得します。
*   これは、`User`モデルで定義した`tasks()`メソッドを使用しています。

---

### 🚀 実践: リレーションシップを試そう

#### ステップ1: 複数のユーザーを登録する

1. ユーザー1を登録（例: user1@example.com）
2. タスクを2件作成
3. ログアウト
4. ユーザー2を登録（例: user2@example.com）
5. タスクを1件作成

---

#### ステップ2: タスク一覧を確認する

1. ユーザー2でログインしている状態で、タスク一覧を確認
2. ユーザー2のタスクのみが表示される（1件）
3. ログアウト
4. ユーザー1でログイン
5. タスク一覧を確認
6. ユーザー1のタスクのみが表示される（2件）

---

### 💡 TIP: リレーションシップの他の使い方

#### タスクからユーザー名を取得する

```blade
<!-- ビュー -->
@foreach($tasks as $task)
    <p>タスク: {{ $task->title }}</p>
    <p>作成者: {{ $task->user->name }}</p>
@endforeach
```

---

#### ユーザーのタスク数を取得する

```php
// コントローラー
$user = Auth::user();
$taskCount = $user->tasks()->count();
echo "タスク数: {$taskCount}";
```

---

#### 条件付きでタスクを取得する

```php
// コントローラー
$tasks = Auth::user()->tasks()->where('status', 'pending')->get();
```

これは、ログインユーザーの「未着手」のタスクのみを取得します。

---

### 🔍 Eager Loadingでパフォーマンスを改善する

リレーションシップを使ってデータを取得する際、**N+1問題**が発生することがあります。

**N+1問題**とは、**データを取得する際に、大量のSQLクエリが実行される問題**です。

---

#### N+1問題の例

```php
$tasks = Task::all();

foreach ($tasks as $task) {
    echo $task->user->name; // ここで毎回SQLクエリが実行される
}
```

この場合、以下のようなSQLクエリが実行されます。

```sql
SELECT * FROM tasks; -- 1回
SELECT * FROM users WHERE id = 1; -- タスクの数だけ実行される
SELECT * FROM users WHERE id = 2;
SELECT * FROM users WHERE id = 3;
...
```

---

#### Eager Loadingで解決する

**Eager Loading**を使うと、N+1問題を解決できます。

```php
$tasks = Task::with('user')->get();

foreach ($tasks as $task) {
    echo $task->user->name; // SQLクエリは実行されない
}
```

この場合、以下のようなSQLクエリが実行されます。

```sql
SELECT * FROM tasks; -- 1回
SELECT * FROM users WHERE id IN (1, 2, 3, ...); -- 1回
```

SQLクエリの実行回数が大幅に減り、パフォーマンスが向上します。

---

### 🔍 TaskControllerでEager Loadingを使う

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function index()
{
    // Eager Loadingを使ってユーザー情報も一緒に取得
    $tasks = Auth::user()->tasks()->with('category')->get();
    
    return view('tasks.index', compact('tasks'));
}
```

---

### 🚨 よくある間違い

#### 間違い1: リレーションシップメソッド名が間違っている

**エラー**:

```
Call to undefined method App\Models\User::task()
```

**対処法**: メソッド名を確認します。1対多の場合は**複数形**、多対1の場合は**単数形**にします。

---

#### 間違い2: 外部キーが設定されていない

**エラー**:

```
SQLSTATE[23000]: Integrity constraint violation: 1452 Cannot add or update a child row: a foreign key constraint fails
```

**対処法**: マイグレーションファイルで、外部キー制約を設定します。

---

#### 間違い3: N+1問題を無視する

**対処法**: `with()`を使って、Eager Loadingを行います。

---

## ✨ まとめ

このセクションでは、ユーザーとタスクの1対多リレーションシップの実装について学びました。

*   `hasMany()`を使って、1対多リレーションシップを定義する。
*   `belongsTo()`を使って、多対1リレーションシップを定義する。
*   `Auth::user()->tasks`を使って、ログインユーザーのタスクを取得する。
*   Eager Loadingを使って、N+1問題を解決する。

次のセクションでは、セキュリティについて学びます。

---

## 📝 学習のポイント

- [ ] ユーザーとタスクの1対多リレーションシップを実装する方法を学んだ。
- [ ] Eloquentのリレーションシップメソッドを使ってデータを取得した。
- [ ] ログインユーザーのタスクのみを表示するように実装した。
