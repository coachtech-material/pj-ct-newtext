# Tutorial 11-3-6: タグ機能の実装（多対多）

## 🎯 このセクションで学ぶこと

- タグテーブルと中間テーブルを作成し、タスクとの多対多のリレーションシップを実装する方法を学ぶ
- `belongsToMany()`を使って、多対多のリレーションシップを定義する方法を学ぶ
- `attach()`と`detach()`と`sync()`を使って、リレーションシップを管理する方法を学ぶ

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
| Step 1 | タグと中間テーブルのマイグレーション | データベースを準備 |
| Step 2 | 多対多リレーションシップ定義 | `belongsToMany`を使用 |
| Step 3 | タスクフォームにタグ選択追加 | 複数選択のUI |
| Step 4 | タグの保存と表示 | attach/syncを使用 |

> 💡 **ポイント**: 多対多では、両方のモデルに`belongsToMany`を定義します。

---

## Step 1: タグと中間テーブルのマイグレーション

### 1-1. tagsテーブルを作成する

```bash
php artisan make:model Tag -m
```

**ファイル**: `database/migrations/xxxx_xx_xx_create_tags_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('tags', function (Blueprint $table) {
            $table->id();
            $table->string('name')->unique();
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('tags');
    }
};
```

---

### 1-2. 中間テーブルを作成する

多対多リレーションシップには、**中間テーブル**が必要です。

```bash
php artisan make:migration create_task_tag_table
```

**ファイル**: `database/migrations/xxxx_xx_xx_create_task_tag_table.php`

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create('task_tag', function (Blueprint $table) {
            $table->id();
            $table->foreignId('task_id')->constrained()->onDelete('cascade');
            $table->foreignId('tag_id')->constrained()->onDelete('cascade');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('task_tag');
    }
};
```

---

### 1-3. コードリーディング

#### 中間テーブルの命名規則

中間テーブルの名前は、**アルファベット順**で`task_tag`のようにします。

| テーブルA | テーブルB | 中間テーブル |
|-----------|-----------|--------------|
| tasks | tags | task_tag |
| posts | users | post_user |
| roles | users | role_user |

---

#### `onDelete('cascade')`

- タスクが削除されたら、中間テーブルのレコードも削除されます
- タグが削除されたら、中間テーブルのレコードも削除されます

---

### 1-4. マイグレーションを実行する

```bash
php artisan migrate
```

---

### 1-5. シーダーでタグを作成する

**ファイル**: `database/seeders/TagSeeder.php`

```php
<?php

namespace Database\Seeders;

use App\Models\Tag;
use Illuminate\Database\Seeder;

class TagSeeder extends Seeder
{
    public function run(): void
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

シーダーを実行します。

```bash
php artisan db:seed --class=TagSeeder
```

---

## Step 2: 多対多リレーションシップ定義

### 2-1. Tagモデルを編集する

**ファイル**: `app/Models/Tag.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Tag extends Model
{
    use HasFactory;

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

### 2-2. Taskモデルにリレーションシップを追加する

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

### 2-3. コードリーディング

#### `$this->belongsToMany(Tag::class)`

- 多対多リレーションシップを定義します
- Eloquentは自動的に`task_tag`中間テーブルを使用します
- 両方のモデルに`belongsToMany`を定義します

---

#### リレーションシップの全体像

| モデル | メソッド | 関係 |
|--------|----------|------|
| Task | `tags()` | 1つのタスクは複数のタグを持つ |
| Tag | `tasks()` | 1つのタグは複数のタスクに属する |

---

## Step 3: タスクフォームにタグ選択追加

### 3-1. コントローラーを修正する

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

### 3-2. 作成フォームにタグのチェックボックスを追加する

**ファイル**: `resources/views/tasks/create.blade.php`

```blade
<div class="form-group" style="margin-bottom: 15px;">
    <label style="display: block; margin-bottom: 5px; font-weight: bold;">タグ</label>
    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
        @foreach ($tags as $tag)
            <label style="display: flex; align-items: center; gap: 5px;">
                <input type="checkbox" name="tags[]" value="{{ $tag->id }}" {{ in_array($tag->id, old('tags', [])) ? 'checked' : '' }}>
                {{ $tag->name }}
            </label>
        @endforeach
    </div>
    @error('tags')
        <div style="color: red; margin-top: 5px;">{{ $message }}</div>
    @enderror
</div>
```

---

### 3-3. 編集フォームにタグのチェックボックスを追加する

**ファイル**: `resources/views/tasks/edit.blade.php`

```blade
<div class="form-group" style="margin-bottom: 15px;">
    <label style="display: block; margin-bottom: 5px; font-weight: bold;">タグ</label>
    <div style="display: flex; flex-wrap: wrap; gap: 10px;">
        @foreach ($tags as $tag)
            <label style="display: flex; align-items: center; gap: 5px;">
                <input type="checkbox" name="tags[]" value="{{ $tag->id }}" {{ in_array($tag->id, old('tags', $task->tags->pluck('id')->toArray())) ? 'checked' : '' }}>
                {{ $tag->name }}
            </label>
        @endforeach
    </div>
    @error('tags')
        <div style="color: red; margin-top: 5px;">{{ $message }}</div>
    @enderror
</div>
```

---

### 3-4. コードリーディング

#### `name="tags[]"`

- 配列形式でデータを送信します
- PHPでは`$request->tags`で配列として受け取れます

---

#### `$task->tags->pluck('id')->toArray()`

- `$task->tags`: タスクに関連付けられたタグのコレクション
- `pluck('id')`: IDだけを抽出
- `toArray()`: 配列に変換

これにより、編集時に既存のタグがチェックされた状態で表示されます。

---

## Step 4: タグの保存と表示

### 4-1. storeメソッドを修正する

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'category_id' => 'nullable|exists:categories,id',
        'description' => 'nullable',
        'due_date' => 'nullable|date',
        'status' => 'required|in:pending,in_progress,completed',
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
```

---

### 4-2. updateメソッドを修正する

```php
public function update(Request $request, Task $task)
{
    $this->authorize('update', $task);

    $validated = $request->validate([
        'title' => 'required|max:255',
        'category_id' => 'nullable|exists:categories,id',
        'description' => 'nullable',
        'due_date' => 'nullable|date',
        'status' => 'required|in:pending,in_progress,completed',
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

### 4-3. コードリーディング

#### `attach()`、`detach()`、`sync()`の違い

| メソッド | 動作 | 使用場面 |
|----------|------|----------|
| `attach()` | 関連を追加 | 新規作成時 |
| `detach()` | 関連を削除 | 特定のタグを外す |
| `sync()` | 関連を同期 | 更新時（既存を削除して新しいものを追加） |

```php
// タグを追加
$task->tags()->attach([1, 2, 3]);

// タグを削除
$task->tags()->detach([1, 2]);

// タグを同期（既存のタグを削除し、新しいタグを追加）
$task->tags()->sync([3, 4, 5]);
```

---

### 4-4. タスク詳細にタグを表示する

**ファイル**: `resources/views/tasks/show.blade.php`

```blade
<tr>
    <th style="padding: 10px; background-color: #f5f5f5;">タグ</th>
    <td style="padding: 10px;">
        @forelse ($task->tags as $tag)
            <span style="display: inline-block; background-color: #e0e0e0; padding: 4px 8px; margin: 2px; border-radius: 4px; font-size: 0.9em;">{{ $tag->name }}</span>
        @empty
            <span style="color: #999;">タグなし</span>
        @endforelse
    </td>
</tr>
```

---

### 4-5. タスク一覧にタグを表示する

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<td style="padding: 10px;">
    @foreach ($task->tags as $tag)
        <span style="display: inline-block; background-color: #e0e0e0; padding: 2px 6px; margin: 1px; border-radius: 3px; font-size: 0.85em;">{{ $tag->name }}</span>
    @endforeach
</td>
```

---

### 4-6. 動作確認

1. タスク作成ページにアクセスする
2. タグを複数選択してタスクを作成する
3. タスク詳細ページでタグが表示されることを確認する
4. タスク編集ページでタグを変更して保存する
5. 変更が反映されていることを確認する

---

## 🚨 よくある間違い

### 間違い1: 中間テーブルの命名規則を間違える

**エラー**:

```
SQLSTATE[42S02]: Base table or view not found: 1146 Table 'task_tag' doesn't exist
```

**対処法**: 中間テーブルの名前は、アルファベット順で`task_tag`のようにします。

---

### 間違い2: sync()を使わずにattach()を使う

**問題**: 更新時に既存のタグが残ってしまう

**対処法**: 更新時は`sync()`を使います。`attach()`を使うと、既存のタグが残ります。

---

### 間違い3: Eager Loadingを忘れる

**問題**: N+1問題が発生してパフォーマンスが低下する

**対処法**: 次のセクションで学ぶEager Loadingを使います。

---

## 💡 TIP: 中間テーブルに追加情報を保存

中間テーブルに追加情報を保存できます。

```php
// 追加情報を付けてattach
$task->tags()->attach($tagId, ['created_by' => auth()->id()]);

// 追加情報を取得
foreach ($task->tags as $tag) {
    echo $tag->pivot->created_by;
}
```

---

## ✨ まとめ

このセクションでは、タグ機能を実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | タグテーブルと中間テーブルの作成 |
| Step 2 | `belongsToMany`で多対多リレーションシップを定義 |
| Step 3 | チェックボックスでタグを選択 |
| Step 4 | `attach()`と`sync()`でリレーションシップを管理 |

次のセクションでは、Eager Loadingによるパフォーマンス改善について学びます。

---

## 📝 学習のポイント

- [ ] 多対多のリレーションシップを実装した
- [ ] 中間テーブルを作成した
- [ ] `attach()`、`detach()`、`sync()`を使った
- [ ] チェックボックスでタグを選択できるようにした
