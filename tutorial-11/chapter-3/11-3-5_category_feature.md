# Tutorial 11-3-5: カテゴリー機能の実装

## 🎯 このセクションで学ぶこと

*   カテゴリーテーブルを作成し、タスクとのリレーションシップを実装する方法を学ぶ。
*   1対多のリレーションシップを実装する方法を学ぶ。
*   プルダウンメニューでカテゴリーを選択できるようにする方法を学ぶ。

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
| 1 | カテゴリーのマイグレーション・モデル | データベースを準備 |
| 2 | リレーションシップ定義 | 1対多の関係を定義 |
| 3 | タスクフォームにカテゴリー選択追加 | UIを更新 |
| 4 | カテゴリーで絞り込み | 検索機能を拡張 |

> 💡 **ポイント**: カテゴリーは「1つのタスクに1つ」なので、`belongsTo`を使います。

---

## 導入：なぜカテゴリー機能が重要なのか

**カテゴリー機能**は、タスクを分類する機能です。

カテゴリー機能を実装することで、タスクを整理しやすくなり、検索もしやすくなります。

---

## 詳細解説

### 🔍 カテゴリーテーブルの作成

カテゴリーテーブルを作成します。

```bash
php artisan make:model Category -m
```

**ファイル**: `database/migrations/xxxx_xx_xx_create_categories_table.php`

```php
public function up()
{
    Schema::create('categories', function (Blueprint $table) {
        $table->id();
        $table->string('name');
        $table->timestamps();
    });
}
```

---

### 🔍 tasksテーブルにcategory_idを追加

```bash
php artisan make:migration add_category_id_to_tasks_table
```

**ファイル**: `database/migrations/xxxx_xx_xx_add_category_id_to_tasks_table.php`

```php
public function up()
{
    Schema::table('tasks', function (Blueprint $table) {
        $table->foreignId('category_id')->nullable()->constrained()->onDelete('set null');
    });
}

public function down()
{
    Schema::table('tasks', function (Blueprint $table) {
        $table->dropForeign(['category_id']);
        $table->dropColumn('category_id');
    });
}
```

---

### 🔍 マイグレーションの実行

```bash
php artisan migrate
```

---

### 🔍 Categoryモデル

**ファイル**: `app/Models/Category.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Category extends Model
{
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

### 🔍 Taskモデルにリレーションシップを追加

**ファイル**: `app/Models/Task.php`

```php
protected $fillable = [
    'user_id',
    'category_id',  // 追加
    'title',
    'description',
    'due_date',
    'status',
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

### 🔍 シーダーでカテゴリーを作成

**ファイル**: `database/seeders/CategorySeeder.php`

```php
<?php

namespace Database\Seeders;

use App\Models\Category;
use Illuminate\Database\Seeder;

class CategorySeeder extends Seeder
{
    public function run()
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

**ファイル**: `database/seeders/DatabaseSeeder.php`

```php
public function run()
{
    $this->call([
        CategorySeeder::class,
    ]);
}
```

```bash
php artisan db:seed --class=CategorySeeder
```

---

### 🔍 タスク作成フォームにカテゴリーを追加

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
```

---

### 🔍 ビューにカテゴリーのプルダウンを追加

**ファイル**: `resources/views/tasks/create.blade.php`

```blade
<form method="POST" action="{{ route('tasks.store') }}">
    @csrf

    <div>
        <label for="title">タイトル</label>
        <input type="text" id="title" name="title" value="{{ old('title') }}" required>
        @error('title')
            <div style="color: red;">{{ $message }}</div>
        @enderror
    </div>

    <div>
        <label for="category_id">カテゴリー</label>
        <select id="category_id" name="category_id">
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

    <!-- ... -->

    <button type="submit">作成</button>
</form>
```

---

### 🔍 バリデーションルールを追加

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'category_id' => 'nullable|exists:categories,id',  // 追加
        'description' => 'nullable',
        'due_date' => 'nullable|date',
        'status' => 'required|in:未完了,完了',
    ]);

    $validated['user_id'] = auth()->id();

    Task::create($validated);

    return redirect()->route('tasks.index')->with('success', 'タスクを作成しました。');
}
```

---

### 🔍 タスク一覧にカテゴリーを表示

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<table border="1">
    <thead>
        <tr>
            <th>ID</th>
            <th>タイトル</th>
            <th>カテゴリー</th>
            <th>期限</th>
            <th>ステータス</th>
            <th>操作</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($tasks as $task)
            <tr>
                <td>{{ $task->id }}</td>
                <td>{{ $task->title }}</td>
                <td>{{ $task->category?->name ?? '未分類' }}</td>
                <td>{{ $task->due_date }}</td>
                <td>{{ $task->status }}</td>
                <td>
                    <a href="{{ route('tasks.show', $task) }}">詳細</a>
                    <a href="{{ route('tasks.edit', $task) }}">編集</a>
                    <form method="POST" action="{{ route('tasks.destroy', $task) }}" style="display:inline;" onsubmit="return confirm('本当に削除しますか?');">
                        @csrf
                        @method('DELETE')
                        <button type="submit">削除</button>
                    </form>
                </td>
            </tr>
        @endforeach
    </tbody>
</table>
```

---

### 🔍 Null Safe演算子

`?->`は、**Null Safe演算子**です。

```blade
{{ $task->category?->name ?? '未分類' }}
```

*   `$task->category`がnullの場合、エラーにならずにnullを返す
*   `??`演算子で、nullの場合は「未分類」を表示する

---

### 🔍 カテゴリーで検索

カテゴリーで検索できるようにします。

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<form method="GET" action="{{ route('tasks.index') }}">
    <input type="text" name="keyword" placeholder="タイトルで検索" value="{{ request('keyword') }}">
    <select name="category_id">
        <option value="">すべてのカテゴリー</option>
        @foreach ($categories as $category)
            <option value="{{ $category->id }}" {{ request('category_id') == $category->id ? 'selected' : '' }}>
                {{ $category->name }}
            </option>
        @endforeach
    </select>
    <select name="status">
        <option value="">すべて</option>
        <option value="未完了" {{ request('status') == '未完了' ? 'selected' : '' }}>未完了</option>
        <option value="完了" {{ request('status') == '完了' ? 'selected' : '' }}>完了</option>
    </select>
    <button type="submit">検索</button>
    <a href="{{ route('tasks.index') }}">クリア</a>
</form>
```

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

    $categories = Category::all();

    return view('tasks.index', compact('tasks', 'categories'));
}
```

---

### 💡 TIP: カテゴリーの管理画面

カテゴリーの管理画面を作成すると、ユーザーが自由にカテゴリーを追加・編集・削除できるようになります。

---

### 🚨 よくある間違い

#### 間違い1: 外部キー制約を忘れる

**対処法**: マイグレーションで`constrained()`を使います。

---

#### 間違い2: Null Safe演算子を使わない

**対処法**: `$task->category?->name`のように、`?->`を使います。

---

#### 間違い3: カテゴリーをビューに渡し忘れる

**対処法**: コントローラーで`compact('categories')`を使います。

---

## ✨ まとめ

このセクションでは、カテゴリー機能を実装しました。

*   カテゴリーテーブルを作成し、タスクとのリレーションシップを実装した。
*   1対多のリレーションシップを実装した。
*   プルダウンメニューでカテゴリーを選択できるようにした。

次のセクションでは、タグ機能の実装について学びます。

---

## 📝 学習のポイント

- [ ] カテゴリーテーブルを作成した。
- [ ] 1対多のリレーションシップを実装した。
- [ ] Null Safe演算子を使った。
- [ ] カテゴリーで検索できるようにした。
