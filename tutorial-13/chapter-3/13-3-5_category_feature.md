# Tutorial 13-3-5: カテゴリー機能の実装

## 🎯 このセクションで学ぶこと

- カテゴリーテーブルを作成し、タスクとのリレーションシップを実装する方法を学ぶ
- 1対多のリレーションシップを実装する方法を学ぶ
- プルダウンメニューでカテゴリーを選択できるようにする方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ所有者チェックの後に『カテゴリー機能』を実装するのか？」

基本的なセキュリティが整ったら、次は「カテゴリー機能」です。

---

### 理由1: 1対多リレーションシップの復習

ユーザーとタスクの関係は「1対多」でした。カテゴリーとタスクも「1対多」です。

```
1人のユーザー → 複数のタスク
1つのカテゴリー → 複数のタスク
```

同じパターンを繰り返すことで、**リレーションシップの理解を深めます**。

---

### 理由2: 機能拡張の練習

実務では、基本機能ができた後に**機能を追加**していきます。

カテゴリー機能の追加を通じて、既存のコードに機能を追加する方法を学びます。

---

### 理由3: 次のセクションの準備

カテゴリーは「1対多」ですが、次のセクションで実装するタグは「多対多」です。

まずは簡単な「1対多」で練習し、次に複雑な「多対多」に挑戦します。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | カテゴリーのマイグレーション・モデル作成 | データベースを準備 |
| Step 2 | リレーションシップ定義 | 1対多の関係を定義 |
| Step 3 | タスクフォームにカテゴリー選択追加 | UIを更新 |
| Step 4 | カテゴリーで絞り込み | 検索機能を拡張 |

> 💡 **ポイント**: カテゴリーは「1つのタスクに1つ」なので、`belongsTo`を使います。

---

## Step 1: カテゴリーのマイグレーション・モデル作成

### 1-1. カテゴリーテーブルを作成する

カテゴリーテーブルを作成します。

```bash
sail artisan make:model Category -m
```

**ファイル**: `database/migrations/xxxx_xx_xx_create_categories_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('categories', function (Blueprint $table) {
            $table->id();
            $table->string('name');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('categories');
    }
};
```

---

### 1-2. tasksテーブルにcategory_idを追加する

すでに`category_id`カラムがある場合はスキップしてください。

```bash
sail artisan make:migration add_category_id_to_tasks_table
```

**ファイル**: `database/migrations/xxxx_xx_xx_add_category_id_to_tasks_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table('tasks', function (Blueprint $table) {
            $table->foreignId('category_id')->nullable()->constrained()->onDelete('set null');
        });
    }

    public function down(): void
    {
        Schema::table('tasks', function (Blueprint $table) {
            $table->dropForeign(['category_id']);
            $table->dropColumn('category_id');
        });
    }
};
```

---

### 1-3. マイグレーションを実行する

```bash
sail artisan migrate
```

---

### 1-4. Categoryモデルを編集する

**ファイル**: `app/Models/Category.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Category extends Model
{
    use HasFactory;

    protected $fillable = [
        'name',
    ];

    /**
     * このカテゴリーに属するタスク
     */
    public function tasks()
    {
        return $this->hasMany(Task::class);
    }
}
```

---

### 1-5. シーダーでカテゴリーを作成する

**ファイル**: `database/seeders/CategorySeeder.php`

```php
<?php

namespace Database\Seeders;

use App\Models\Category;
use Illuminate\Database\Seeder;

class CategorySeeder extends Seeder
{
    public function run(): void
    {
        $categories = [
            '仕事',
            'プライベート',
            '買い物',
            '勉強',
            'その他',
        ];

        foreach ($categories as $category) {
            Category::create(['name' => $category]);
        }
    }
}
```

シーダーを実行します。

```bash
sail artisan db:seed --class=CategorySeeder
```

---

## Step 2: リレーションシップ定義

### 2-1. Taskモデルにリレーションシップを追加する

**ファイル**: `app/Models/Task.php`

```php
protected $fillable = [
    'user_id',
    'category_id',  // 追加
    'title',
    'description',
    'status',
    'due_date',
];

/**
 * このタスクが属するカテゴリー
 */
public function category()
{
    return $this->belongsTo(Category::class);
}
```

---

### 2-2. コードリーディング

#### `$this->belongsTo(Category::class)`

- タスクは1つのカテゴリーに属するので、`belongsTo`を使います
- Eloquentは自動的に`category_id`カラムを外部キーとして使用します

---

#### リレーションシップの全体像

| モデル | メソッド | 関係 |
|--------|----------|------|
| Category | `tasks()` | 1つのカテゴリーは複数のタスクを持つ |
| Task | `category()` | 1つのタスクは1つのカテゴリーに属する |

---

## Step 3: タスクフォームにカテゴリー選択追加

### 3-1. コントローラーを修正する

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
use App\Models\Category;

public function create()
{
    $categories = Category::all();
    return view('tasks.create', compact('categories'));
}

public function edit(Task $task)
{
    $this->authorize('update', $task);
    $categories = Category::all();
    return view('tasks.edit', compact('task', 'categories'));
}

public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'category_id' => 'nullable|exists:categories,id',  // 追加
        'description' => 'nullable',
        'due_date' => 'nullable|date',
        'status' => 'required|in:pending,in_progress,completed',
    ]);

    $validated['user_id'] = auth()->id();

    Task::create($validated);

    return redirect()->route('tasks.index')->with('success', 'タスクを作成しました。');
}
```

---

### 3-2. ビューにカテゴリーのプルダウンを追加する

**ファイル**: `resources/views/tasks/create.blade.php`

```blade
<div class="form-group">
    <label for="category_id">カテゴリー</label>
    <select id="category_id" name="category_id" style="width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
        <option value="">選択してください</option>
        @foreach ($categories as $category)
            <option value="{{ $category->id }}" {{ old('category_id') == $category->id ? 'selected' : '' }}>
                {{ $category->name }}
            </option>
        @endforeach
    </select>
    @error('category_id')
        <div style="color: red;">{{ $message }}</div>
    @enderror
</div>
```

---

### 3-3. コードリーディング

#### `exists:categories,id`

- バリデーションルールで、`categories`テーブルの`id`カラムに存在する値かどうかをチェックします
- 存在しないIDが送信された場合、バリデーションエラーになります

---

#### `old('category_id') == $category->id ? 'selected' : ''`

- バリデーションエラー時に、選択していた値を保持します
- 三項演算子で、一致する場合は`selected`属性を追加します

---

### 3-4. タスク一覧にカテゴリーを表示する

**ファイル**: `resources/views/tasks/index.blade.php`

テーブルのヘッダーと行にカテゴリー列を追加します。

```blade
<table border="1" style="border-collapse: collapse; width: 100%;">
    <thead>
        <tr style="background-color: #f5f5f5;">
            <th style="padding: 10px;">ID</th>
            <th style="padding: 10px;">タイトル</th>
            <th style="padding: 10px;">カテゴリー</th>
            <th style="padding: 10px;">期限</th>
            <th style="padding: 10px;">ステータス</th>
            <th style="padding: 10px;">操作</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($tasks as $task)
            <tr>
                <td style="padding: 10px;">{{ $task->id }}</td>
                <td style="padding: 10px;">{{ $task->title }}</td>
                <td style="padding: 10px;">{{ $task->category?->name ?? '未分類' }}</td>
                <td style="padding: 10px;">{{ $task->due_date?->format('Y-m-d') ?? '未設定' }}</td>
                <td style="padding: 10px;">{{ $task->status }}</td>
                <td style="padding: 10px;">
                    <a href="{{ route('tasks.show', $task) }}">詳細</a>
                    <a href="{{ route('tasks.edit', $task) }}">編集</a>
                </td>
            </tr>
        @endforeach
    </tbody>
</table>
```

---

### 3-5. コードリーディング

#### `$task->category?->name ?? '未分類'`

- `?->`は**Null Safe演算子**です
- `$task->category`がnullの場合、エラーにならずにnullを返します
- `??`演算子で、nullの場合は「未分類」を表示します

---

## Step 4: カテゴリーで絞り込み

### 4-1. 検索フォームにカテゴリーを追加する

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<form method="GET" action="{{ route('tasks.index') }}" style="margin-bottom: 20px; padding: 15px; background-color: #f5f5f5; border-radius: 4px;">
    <div style="display: flex; gap: 10px; flex-wrap: wrap; align-items: center;">
        <input type="text" name="keyword" placeholder="タイトルで検索" value="{{ request('keyword') }}" style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
        
        <select name="category_id" style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
            <option value="">すべてのカテゴリー</option>
            @foreach ($categories as $category)
                <option value="{{ $category->id }}" {{ request('category_id') == $category->id ? 'selected' : '' }}>
                    {{ $category->name }}
                </option>
            @endforeach
        </select>
        
        <select name="status" style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
            <option value="">すべてのステータス</option>
            <option value="pending" {{ request('status') == 'pending' ? 'selected' : '' }}>未着手</option>
            <option value="in_progress" {{ request('status') == 'in_progress' ? 'selected' : '' }}>進行中</option>
            <option value="completed" {{ request('status') == 'completed' ? 'selected' : '' }}>完了</option>
        </select>
        
        <button type="submit" style="padding: 8px 16px; background-color: #2196f3; color: white; border: none; border-radius: 4px; cursor: pointer;">検索</button>
        <a href="{{ route('tasks.index') }}" style="padding: 8px 16px; color: #666; text-decoration: none;">クリア</a>
    </div>
</form>
```

---

### 4-2. コントローラーにカテゴリー検索を追加する

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function index(Request $request)
{
    $query = Task::query();

    // キーワード検索
    if ($request->filled('keyword')) {
        $query->where('title', 'like', '%' . $request->keyword . '%');
    }

    // カテゴリー検索
    if ($request->filled('category_id')) {
        $query->where('category_id', $request->category_id);
    }

    // ステータス検索
    if ($request->filled('status')) {
        $query->where('status', $request->status);
    }

    $tasks = $query->orderBy('created_at', 'desc')->paginate(10);

    // カテゴリー一覧を取得
    $categories = Category::all();

    return view('tasks.index', compact('tasks', 'categories'));
}
```

---

### 4-3. 動作確認

1. ブラウザでタスク一覧ページにアクセスする
2. カテゴリーを選択して「検索」ボタンをクリックする
3. 選択したカテゴリーのタスクのみが表示される

---

## 🚨 よくある間違い

### 間違い1: 外部キー制約を忘れる

**問題**: 存在しないカテゴリーIDを設定できてしまう

**対処法**: マイグレーションで`constrained()`を使います。

---

### 間違い2: Null Safe演算子を使わない

**エラー**:

```
Attempt to read property "name" on null
```

**対処法**: `$task->category?->name`のように、`?->`を使います。

---

### 間違い3: カテゴリーをビューに渡し忘れる

**エラー**:

```
Undefined variable: categories
```

**対処法**: コントローラーで`compact('categories')`を使います。

---

## 💡 TIP: カテゴリーの管理画面

カテゴリーの管理画面を作成すると、ユーザーが自由にカテゴリーを追加・編集・削除できるようになります。

```bash
sail artisan make:controller CategoryController --resource
```

タスクのCRUDと同じパターンで実装できます。

---

## ✨ まとめ

このセクションでは、カテゴリー機能を実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | カテゴリーテーブルとモデルの作成 |
| Step 2 | `belongsTo`で1対多リレーションシップを定義 |
| Step 3 | プルダウンメニューでカテゴリーを選択 |
| Step 4 | カテゴリーで検索機能を拡張 |

次のセクションでは、タグ機能の実装について学びます。

---
