# Tutorial 13-2-2: タスク一覧の実装

## 🎯 このセクションで学ぶこと

- 提供されたBladeファイルを読み解き、必要なデータを特定する方法を学ぶ
- Tinkerでデータ取得を確認してから、コントローラーを実装する方法を学ぶ
- 「提供コードありき」の開発フローを実践する

---

## 🧠 先輩エンジニアの思考プロセス

### 「提供コードありき」の開発フロー

このTutorialでは、**フロントエンドエンジニアから納品されたBladeファイルがある**という想定で開発を進めます。

実務では、以下のような流れで開発を進めます：

```
1. 画面アクセス＆エラー確認 → 何が足りないかを把握
2. Bladeの解読 → 必要な変数・リレーションを特定
3. Tinker検証 → データ構造を確認
4. バックエンド実装 → モデル・コントローラーを実装
```

**「データが取れていないのに画面を作っても動かない」** という問題を防ぐため、必ずTinkerで確認してから実装します。

---

## Step 1: 画面アクセス＆エラー確認

### 1-1. ブラウザでアクセスする

前のセクションでBladeファイルを配置しました。まずは画面にアクセスして、エラーを確認します。

```
http://localhost/tasks
```

### 1-2. エラーを確認する

以下のようなエラーが表示されるはずです：

```
Target class [App\Http\Controllers\TaskController] does not exist.
```

**読み解き**：`TaskController`が存在しないため、エラーになっています。

---

## Step 2: Bladeの解読

エラーを修正する前に、**Bladeファイルを読み解いて、何が必要かを把握**します。

### 2-1. tasks/index.blade.phpを読む

`resources/views/tasks/index.blade.php`を開いて、必要な変数を特定します。

```blade
{{-- 検索フォームのカテゴリー選択 --}}
@foreach($categories as $category)
    <option value="{{ $category->id }}">{{ $category->name }}</option>
@endforeach

{{-- タスク一覧 --}}
@forelse($tasks as $task)
    <h3>{{ $task->title }}</h3>
    <span class="status-{{ $task->status }}">...</span>
    @if($task->category)
        | カテゴリー: {{ $task->category->name }}
    @endif
    @if($task->due_date)
        | 期限: {{ $task->due_date->format('Y/m/d') }}
    @endif
@empty
    <p>タスクがありません。</p>
@endforelse

{{-- ページネーション --}}
{{ $tasks->links() }}
```

### 2-2. 必要なデータを整理する

| 変数 | 型 | 説明 |
|:---|:---|:---|
| `$categories` | Collection | カテゴリーの一覧 |
| `$tasks` | Paginator | タスクの一覧（ページネーション付き） |
| `$task->category` | Category | タスクに紐づくカテゴリー（リレーション） |

### 2-3. 必要なリレーションを特定する

`$task->category->name`という記述から、**TaskモデルにCategoryへのリレーションが必要**だとわかります。

```php
// Taskモデルに必要
public function category()
{
    return $this->belongsTo(Category::class);
}
```

---

## Step 3: Tinker検証

コントローラーを実装する前に、**Tinkerでデータ取得を確認**します。

### 3-1. Tinkerを起動する

```bash
sail artisan tinker
```

### 3-2. カテゴリーを取得する

```php
>>> App\Models\Category::all();
```

**期待する結果**：

```
=> Illuminate\Database\Eloquent\Collection {#1234
     all: [
       App\Models\Category {#5678
         id: 1,
         name: "仕事",
         ...
       },
       App\Models\Category {#9012
         id: 2,
         name: "プライベート",
         ...
       },
     ],
   }
```

> **💡 ポイント**: データが空の場合は、先にテストデータを作成します。

### 3-3. タスクを取得する

```php
>>> App\Models\Task::paginate(10);
```

**期待する結果**：

```
=> Illuminate\Pagination\LengthAwarePaginator {#1234
     ...
   }
```

### 3-4. リレーションを確認する

```php
>>> $task = App\Models\Task::first();
>>> $task->category;
```

**期待する結果**：

```
=> App\Models\Category {#5678
     id: 1,
     name: "仕事",
     ...
   }
```

> **🚨 エラーが出た場合**：`Call to undefined relationship [category]`というエラーが出たら、Taskモデルにリレーションを追加する必要があります。

---

## Step 4: バックエンド実装

Tinkerで確認できたら、コントローラーを実装します。

### 4-1. ルートを定義する

`routes/web.php`を開き、以下を追加します。

**ファイル**: `routes/web.php`

```php
<?php

use App\Http\Controllers\TaskController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

// タスク管理のルート（リソースコントローラー）
Route::resource('tasks', TaskController::class);
```

**コードリーディング**：

```php
Route::resource('tasks', TaskController::class);
```
→ リソースコントローラーを使うと、CRUD操作に必要な7つのルートを一括で定義できます。

### 4-2. コントローラーを作成する

```bash
sail artisan make:controller TaskController --resource
```

### 4-3. indexアクションを実装する

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Models\Category;
use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        // Bladeで必要な変数を確認
        // $categories → カテゴリー一覧
        // $tasks → タスク一覧（ページネーション付き）
        
        $categories = Category::all();
        $tasks = Task::with('category')->paginate(10);
        
        return view('tasks.index', compact('categories', 'tasks'));
    }
    
    // 他のメソッドは後で実装
}
```

**コードリーディング**：

```php
$categories = Category::all();
```
→ Bladeの`@foreach($categories as $category)`で使用するため、カテゴリー一覧を取得します。

```php
$tasks = Task::with('category')->paginate(10);
```
→ `with('category')`で**Eager Loading**を使い、N+1問題を防ぎます。`paginate(10)`でページネーションを適用します。

```php
return view('tasks.index', compact('categories', 'tasks'));
```
→ Bladeで必要な変数を渡します。

### 4-4. Taskモデルにリレーションを追加する

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
     * タスクが属するカテゴリーを取得
     */
    public function category()
    {
        return $this->belongsTo(Category::class);
    }
}
```

---

## Step 5: 動作確認

### 5-1. ブラウザでアクセスする

```
http://localhost/tasks
```

### 5-2. 確認ポイント

| 確認項目 | 期待する結果 |
|:---|:---|
| タスク一覧が表示される | テストデータが表示される |
| カテゴリー名が表示される | `$task->category->name`が正しく表示される |
| ページネーションが動作する | ページ切り替えができる |
| 検索フォームにカテゴリーが表示される | `$categories`が正しく渡されている |

### 5-3. エラーが出た場合のデバッグ

**エラー**: `Undefined variable $tasks`

→ コントローラーで`compact('tasks')`を忘れていないか確認

**エラー**: `Call to undefined relationship [category]`

→ Taskモデルに`category()`リレーションを追加したか確認

**エラー**: `Method links does not exist`

→ `Task::all()`ではなく`Task::paginate(10)`を使っているか確認

---

## 💡 TIP: @ddでデバッグする

画面が真っ白になったり、データが表示されない場合は、Bladeに`@dd()`を追加してデバッグします。

```blade
{{-- コントローラーから渡された変数を確認 --}}
@dd($tasks)

{{-- リレーションを確認 --}}
@dd($tasks->first()->category)
```

---

## 💡 TIP: Eager Loadingの重要性

`with('category')`を使わないと、**N+1問題**が発生します。

```php
// 悪い例：N+1問題が発生
$tasks = Task::paginate(10);
// タスクが10件あると、11回のSQLが実行される

// 良い例：Eager Loading
$tasks = Task::with('category')->paginate(10);
// タスクが10件あっても、2回のSQLで済む
```

---

## ✨ まとめ

このセクションでは、「提供コードありき」の開発フローでタスク一覧を実装しました。

| ステップ | 学んだこと |
|:---|:---|
| Step 1 | 画面アクセスでエラーを確認し、何が足りないかを把握 |
| Step 2 | Bladeを読み解いて、必要な変数・リレーションを特定 |
| Step 3 | Tinkerでデータ取得を確認 |
| Step 4 | コントローラーを実装し、Bladeに変数を渡す |
| Step 5 | 動作確認とデバッグ |

次のセクションでは、タスク作成の実装について学びます。

---
