# Tutorial 9-5-10: CRUD機能 - ハンズオン演習

## 📝 このセクションの目的

Chapter 5で学んだCRUD機能を実際に手を動かして確認します。タスク管理アプリを作成して、Create、Read、Update、Deleteの全機能を実装しましょう。

**学習のポイント**：
- リソースコントローラーを使えるか
- フォームからデータを送信できるか
- CRUD操作を実装できるか

---

## 🎯 演習課題：タスク管理アプリを作成しよう

### 📋 要件

#### 1. Taskモデルとマイグレーションの作成

**カラム構成**：
- id, title (VARCHAR 200), description (TEXT nullable), status (VARCHAR 20, default 'pending'), due_date (DATE nullable), timestamps

#### 2. リソースコントローラーの作成

`TaskController`をリソースコントローラーとして作成してください。

#### 3. ビューの作成

以下のビューを作成してください：

- `tasks/index.blade.php`: タスク一覧
- `tasks/create.blade.php`: タスク作成フォーム
- `tasks/edit.blade.php`: タスク編集フォーム

#### 4. ルートの定義

リソースルートを定義してください。

---

## 💡 ヒント

```bash
php artisan make:model Task -mcr
```

```php
// routes/web.php
Route::resource('tasks', TaskController::class);
```

```blade
<!-- フォーム -->
<form action="{{ route('tasks.store') }}" method="POST">
    @csrf
    <input type="text" name="title">
    <button type="submit">作成</button>
</form>
```

---

## 📖 模範解答

### マイグレーションファイル

```php
public function up(): void
{
    Schema::create('tasks', function (Blueprint $table) {
        $table->id();
        $table->string('title', 200);
        $table->text('description')->nullable();
        $table->string('status', 20)->default('pending');
        $table->date('due_date')->nullable();
        $table->timestamps();
    });
}
```

### Task.php

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Task extends Model
{
    protected $fillable = [
        'title',
        'description',
        'status',
        'due_date',
    ];

    protected $casts = [
        'due_date' => 'date',
    ];
}
```

### TaskController.php

```php
<?php

namespace App\Http\Controllers;

use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    public function index()
    {
        $tasks = Task::latest()->get();
        return view('tasks.index', ['tasks' => $tasks]);
    }

    public function create()
    {
        return view('tasks.create');
    }

    public function store(Request $request)
    {
        Task::create($request->all());
        return redirect()->route('tasks.index');
    }

    public function edit($id)
    {
        $task = Task::findOrFail($id);
        return view('tasks.edit', ['task' => $task]);
    }

    public function update(Request $request, $id)
    {
        $task = Task::findOrFail($id);
        $task->update($request->all());
        return redirect()->route('tasks.index');
    }

    public function destroy($id)
    {
        Task::findOrFail($id)->delete();
        return redirect()->route('tasks.index');
    }
}
```

### routes/web.php

```php
use App\Http\Controllers\TaskController;

Route::resource('tasks', TaskController::class);
```

### tasks/index.blade.php

```blade
@extends('layouts.app')

@section('content')
<div class="container">
    <h1>タスク一覧</h1>
    <a href="{{ route('tasks.create') }}" class="btn btn-primary">新規作成</a>
    
    <table class="table mt-3">
        <thead>
            <tr>
                <th>タイトル</th>
                <th>ステータス</th>
                <th>期限</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            @foreach ($tasks as $task)
            <tr>
                <td>{{ $task->title }}</td>
                <td>{{ $task->status }}</td>
                <td>{{ $task->due_date }}</td>
                <td>
                    <a href="{{ route('tasks.edit', $task->id) }}">編集</a>
                    <form action="{{ route('tasks.destroy', $task->id) }}" method="POST" style="display:inline;">
                        @csrf
                        @method('DELETE')
                        <button type="submit">削除</button>
                    </form>
                </td>
            </tr>
            @endforeach
        </tbody>
    </table>
</div>
@endsection
```

### tasks/create.blade.php

```blade
@extends('layouts.app')

@section('content')
<div class="container">
    <h1>タスク作成</h1>
    
    <form action="{{ route('tasks.store') }}" method="POST">
        @csrf
        <div class="mb-3">
            <label>タイトル</label>
            <input type="text" name="title" class="form-control" required>
        </div>
        <div class="mb-3">
            <label>説明</label>
            <textarea name="description" class="form-control"></textarea>
        </div>
        <div class="mb-3">
            <label>期限</label>
            <input type="date" name="due_date" class="form-control">
        </div>
        <button type="submit" class="btn btn-primary">作成</button>
    </form>
</div>
@endsection
```

---

## 💪 自己評価チェックリスト

- [ ] リソースコントローラーを作成できた
- [ ] リソースルートを定義できた
- [ ] CRUD操作を実装できた
- [ ] フォームからデータを送信できた
- [ ] @csrfトークンを使えた
- [ ] @method('DELETE')を使えた

すべてチェックできたら、Chapter 6に進みましょう！
