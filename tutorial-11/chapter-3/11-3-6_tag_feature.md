# Tutorial 11-3-6: タグ機能の実装（多対多）

## 🎯 このセクションで学ぶこと

*   タグテーブルと中間テーブルを作成し、タスクとの多対多のリレーションシップを実装する方法を学ぶ。
*   belongsToMany()を使って、多対多のリレーションシップを定義する方法を学ぶ。
*   attach()とdetach()を使って、リレーションシップを管理する方法を学ぶ。

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜカテゴリーの後に『タグ機能』を実装するのか？」

カテゴリー機能ができたら、次は「タグ機能」です。

---

### 理由1: 多対多リレーションシップを学ぶ

カテゴリーは「1対多」でしたが、タグは「多対多」です。

```
1つのタスク → 複数のタグ
1つのタグ → 複数のタスク
```

新しいリレーションシップのパターンを学びます。

---

### 理由2: 中間テーブルを学ぶ

多対多リレーションシップでは、**中間テーブル**が必要です。

```
tasks ← task_tag → tags
```

この中間テーブルの設計と使い方を学びます。

---

### 理由3: attach/detach/syncを学ぶ

多対多リレーションシップでは、特別なメソッドを使います。

- `attach()`: 関連を追加
- `detach()`: 関連を削除
- `sync()`: 関連を同期

これらの使い方を学びます。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| 1 | タグと中間テーブルのマイグレーション | データベースを準備 |
| 2 | 多対多リレーションシップ定義 | `belongsToMany`を使用 |
| 3 | タスクフォームにタグ選択追加 | 複数選択のUI |
| 4 | タグで絞り込み | 検索機能を拡張 |

> 💡 **ポイント**: 多対多では、両方のモデルに`belongsToMany`を定義します。

---

## 導入：なぜタグ機能が重要なのか

**タグ機能**は、タスクに複数のタグを付ける機能です。

タグ機能を実装することで、タスクをより柔軟に分類できるようになります。

---

## 詳細解説

### 🔍 多対多のリレーションシップ

**多対多のリレーションシップ**は、**1つのタスクが複数のタグを持ち、1つのタグが複数のタスクに属する**関係です。

例:
*   タスク「Laravelの勉強」→ タグ「プログラミング」「勉強」
*   タスク「買い物」→ タグ「プライベート」「買い物」

---

### 🔍 テーブル構造

多対多のリレーションシップには、**中間テーブル**が必要です。

*   `tasks`テーブル
*   `tags`テーブル
*   `task_tag`テーブル（中間テーブル）

---

### 🔍 tagsテーブルの作成

```bash
php artisan make:model Tag -m
```

**ファイル**: `database/migrations/xxxx_xx_xx_create_tags_table.php`

```php
public function up()
{
    Schema::create('tags', function (Blueprint $table) {
        $table->id();
        $table->string('name')->unique();
        $table->timestamps();
    });
}
```

---

### 🔍 中間テーブルの作成

```bash
php artisan make:migration create_task_tag_table
```

**ファイル**: `database/migrations/xxxx_xx_xx_create_task_tag_table.php`

```php
public function up()
{
    Schema::create('task_tag', function (Blueprint $table) {
        $table->id();
        $table->foreignId('task_id')->constrained()->onDelete('cascade');
        $table->foreignId('tag_id')->constrained()->onDelete('cascade');
        $table->timestamps();
    });
}
```

---

### 🔍 マイグレーションの実行

```bash
php artisan migrate
```

---

### 🔍 Tagモデル

**ファイル**: `app/Models/Tag.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Tag extends Model
{
    protected $fillable = [
        'name',
    ];

    /**
     * このタグが付いているタスク
     */
    public function tasks()
    {
        return $this->belongsToMany(Task::class);
    }
}
```

---

### 🔍 Taskモデルにリレーションシップを追加

**ファイル**: `app/Models/Task.php`

```php
/**
 * このタスクに付いているタグ
 */
public function tags()
{
    return $this->belongsToMany(Tag::class);
}
```

---

### 🔍 シーダーでタグを作成

**ファイル**: `database/seeders/TagSeeder.php`

```php
<?php

namespace Database\Seeders;

use App\Models\Tag;
use Illuminate\Database\Seeder;

class TagSeeder extends Seeder
{
    public function run()
    {
        $tags = [
            'プログラミング',
            '勉強',
            '買い物',
            'プライベート',
            '仕事',
            '緊急',
            '重要',
        ];

        foreach ($tags as $tag) {
            Tag::create(['name' => $tag]);
        }
    }
}
```

```bash
php artisan db:seed --class=TagSeeder
```

---

### 🔍 タスク作成フォームにタグを追加

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
use App\Models\Tag;

public function create()
{
    $categories = Category::all();
    $tags = Tag::all();
    return view('tasks.create', compact('categories', 'tags'));
}

public function edit(Task $task)
{
    $this->authorize('update', $task);
    $categories = Category::all();
    $tags = Tag::all();
    return view('tasks.edit', compact('task', 'categories', 'tags'));
}
```

---

### 🔍 ビューにタグのチェックボックスを追加

**ファイル**: `resources/views/tasks/create.blade.php`

```blade
<div>
    <label>タグ</label>
    @foreach ($tags as $tag)
        <label>
            <input type="checkbox" name="tags[]" value="{{ $tag->id }}" {{ in_array($tag->id, old('tags', [])) ? 'checked' : '' }}>
            {{ $tag->name }}
        </label>
    @endforeach
    @error('tags')
        <div style="color: red;">{{ $message }}</div>
    @enderror
</div>
```

**ファイル**: `resources/views/tasks/edit.blade.php`

```blade
<div>
    <label>タグ</label>
    @foreach ($tags as $tag)
        <label>
            <input type="checkbox" name="tags[]" value="{{ $tag->id }}" {{ in_array($tag->id, old('tags', $task->tags->pluck('id')->toArray())) ? 'checked' : '' }}>
            {{ $tag->name }}
        </label>
    @endforeach
    @error('tags')
        <div style="color: red;">{{ $message }}</div>
    @enderror
</div>
```

---

### 🔍 コントローラーでタグを保存

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'category_id' => 'nullable|exists:categories,id',
        'description' => 'nullable',
        'due_date' => 'nullable|date',
        'status' => 'required|in:未完了,完了',
        'tags' => 'nullable|array',
        'tags.*' => 'exists:tags,id',
    ]);

    $validated['user_id'] = auth()->id();

    $task = Task::create($validated);

    // タグを関連付ける
    if ($request->has('tags')) {
        $task->tags()->attach($request->tags);
    }

    return redirect()->route('tasks.index')->with('success', 'タスクを作成しました。');
}

public function update(Request $request, Task $task)
{
    $this->authorize('update', $task);

    $validated = $request->validate([
        'title' => 'required|max:255',
        'category_id' => 'nullable|exists:categories,id',
        'description' => 'nullable',
        'due_date' => 'nullable|date',
        'status' => 'required|in:未完了,完了',
        'tags' => 'nullable|array',
        'tags.*' => 'exists:tags,id',
    ]);

    $task->update($validated);

    // タグを同期する
    $task->tags()->sync($request->tags ?? []);

    return redirect()->route('tasks.show', $task)->with('success', 'タスクを更新しました。');
}
```

---

### 🔍 attach()とdetach()とsync()

*   `attach()`: リレーションシップを追加する
*   `detach()`: リレーションシップを削除する
*   `sync()`: リレーションシップを同期する（既存のリレーションシップを削除し、新しいリレーションシップを追加する）

```php
// タグを追加
$task->tags()->attach([1, 2, 3]);

// タグを削除
$task->tags()->detach([1, 2]);

// タグを同期（既存のタグを削除し、新しいタグを追加）
$task->tags()->sync([3, 4, 5]);
```

---

### 🔍 タスク詳細にタグを表示

**ファイル**: `resources/views/tasks/show.blade.php`

```blade
<table border="1">
    <tr>
        <th>ID</th>
        <td>{{ $task->id }}</td>
    </tr>
    <tr>
        <th>タイトル</th>
        <td>{{ $task->title }}</td>
    </tr>
    <tr>
        <th>カテゴリー</th>
        <td>{{ $task->category?->name ?? '未分類' }}</td>
    </tr>
    <tr>
        <th>タグ</th>
        <td>
            @foreach ($task->tags as $tag)
                <span style="background-color: #eee; padding: 2px 5px; margin-right: 5px;">{{ $tag->name }}</span>
            @endforeach
        </td>
    </tr>
    <!-- ... -->
</table>
```

---

### 🔍 タスク一覧にタグを表示

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<table border="1">
    <thead>
        <tr>
            <th>ID</th>
            <th>タイトル</th>
            <th>カテゴリー</th>
            <th>タグ</th>
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
                <td>
                    @foreach ($task->tags as $tag)
                        <span style="background-color: #eee; padding: 2px 5px; margin-right: 5px;">{{ $tag->name }}</span>
                    @endforeach
                </td>
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

### 💡 TIP: 中間テーブルに追加情報を保存

中間テーブルに追加情報を保存できます。

```php
$task->tags()->attach($tagId, ['created_by' => auth()->id()]);
```

---

### 🚨 よくある間違い

#### 間違い1: 中間テーブルの命名規則を間違える

**対処法**: 中間テーブルの名前は、アルファベット順で`task_tag`のようにします。

---

#### 間違い2: sync()を使わずにattach()を使う

**対処法**: 更新時は`sync()`を使います。`attach()`を使うと、既存のタグが残ります。

---

#### 間違い3: Eager Loadingを忘れる

**対処法**: 次のセクションで学ぶEager Loadingを使います。

---

## ✨ まとめ

このセクションでは、タグ機能を実装しました。

*   タグテーブルと中間テーブルを作成し、タスクとの多対多のリレーションシップを実装した。
*   belongsToMany()を使って、多対多のリレーションシップを定義した。
*   attach()、detach()、sync()を使って、リレーションシップを管理した。

次のセクションでは、Eager Loadingによるパフォーマンス改善について学びます。

---

## 📝 学習のポイント

- [ ] 多対多のリレーションシップを実装した。
- [ ] 中間テーブルを作成した。
- [ ] attach()、detach()、sync()を使った。
- [ ] チェックボックスでタグを選択できるようにした。
