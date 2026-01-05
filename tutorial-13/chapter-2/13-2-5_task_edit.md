# Tutorial 13-2-5: タスク編集の実装

## 🎯 このセクションで学ぶこと

- 提供された編集画面を読み解き、必要なデータを特定する方法を学ぶ
- 編集フォームで既存データを表示する方法を学ぶ
- PUTメソッドを使った更新処理の実装方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 編集機能の特徴

編集機能は「作成」と「詳細表示」の組み合わせです：

| 機能 | 共通点 |
|:---|:---|
| 作成 | フォームの表示、バリデーション、保存 |
| 詳細表示 | 1件取得、ルートモデルバインディング |

**違い**：
- フォームに**既存データを表示**する
- HTTPメソッドが**PUT**（更新）

今回も「提供コードありき」のフローで進めます：

```
1. 画面アクセス＆エラー確認
2. Bladeの解読（既存データの表示方法を確認）
3. Tinker検証（更新処理を確認）
4. バックエンド実装
```

---

## Step 1: 画面アクセス＆エラー確認

### 1-1. ブラウザでアクセスする

```
http://localhost/tasks/1/edit
```

### 1-2. エラーを確認する

```
Undefined variable $task
```

**読み解き**：`edit`アクションで`$task`と`$categories`を渡していないため、エラーになっています。

---

## Step 2: Bladeの解読

### 2-1. tasks/edit.blade.phpを読む

`resources/views/tasks/edit.blade.php`を開いて、フォームの構造を確認します。

```blade
<form action="{{ route('tasks.update', $task) }}" method="POST">
    @csrf
    @method('PUT')
    
    <div class="form-group">
        <label for="title">タイトル</label>
        <input type="text" id="title" name="title" 
               value="{{ old('title', $task->title) }}" required>
        @error('title')
            <p class="error">{{ $message }}</p>
        @enderror
    </div>
    
    <div class="form-group">
        <label for="description">説明</label>
        <textarea id="description" name="description">{{ old('description', $task->description) }}</textarea>
    </div>
    
    <div class="form-group">
        <label for="category_id">カテゴリー</label>
        <select id="category_id" name="category_id">
            <option value="">選択してください</option>
            @foreach($categories as $category)
                <option value="{{ $category->id }}" 
                        {{ old('category_id', $task->category_id) == $category->id ? 'selected' : '' }}>
                    {{ $category->name }}
                </option>
            @endforeach
        </select>
    </div>
    
    <div class="form-group">
        <label for="status">ステータス</label>
        <select id="status" name="status">
            <option value="pending" {{ old('status', $task->status) === 'pending' ? 'selected' : '' }}>未着手</option>
            <option value="in_progress" {{ old('status', $task->status) === 'in_progress' ? 'selected' : '' }}>進行中</option>
            <option value="completed" {{ old('status', $task->status) === 'completed' ? 'selected' : '' }}>完了</option>
        </select>
    </div>
    
    <div class="form-group">
        <label for="due_date">期限</label>
        <input type="date" id="due_date" name="due_date" 
               value="{{ old('due_date', $task->due_date?->format('Y-m-d')) }}">
    </div>
    
    <button type="submit">更新</button>
</form>
```

### 2-2. 作成フォームとの違いを確認する

| 項目 | 作成フォーム | 編集フォーム |
|:---|:---|:---|
| action | `route('tasks.store')` | `route('tasks.update', $task)` |
| method | POST | POST + `@method('PUT')` |
| value | `old('title')` | `old('title', $task->title)` |

### 2-3. 必要な変数を特定する

| 変数 | 型 | 説明 |
|:---|:---|:---|
| `$task` | Task | 編集対象のタスク |
| `$categories` | Collection | カテゴリー一覧（セレクトボックス用） |

### 2-4. old()の第2引数を理解する

```blade
value="{{ old('title', $task->title) }}"
```

- **第1引数**: バリデーションエラー時の入力値
- **第2引数**: デフォルト値（既存データ）

**動作**：
1. バリデーションエラーがある場合 → `old('title')`（入力した値）を表示
2. バリデーションエラーがない場合 → `$task->title`（既存データ）を表示

---

## Step 3: Tinker検証

コントローラーを実装する前に、**Tinkerで更新処理を確認**します。

### 3-1. Tinkerを起動する

```bash
sail artisan tinker
```

### 3-2. タスクを取得する

```php
>>> $task = App\Models\Task::find(1);
>>> $task->title;
```

### 3-3. タスクを更新する

```php
>>> $task->update(['title' => '更新後のタイトル']);
>>> $task->fresh()->title;
```

**期待する結果**：

```
=> "更新後のタイトル"
```

### 3-4. 複数フィールドを更新する

```php
>>> $task->update([
...     'title' => 'さらに更新',
...     'status' => 'completed',
...     'due_date' => '2024-12-31',
... ]);
>>> $task->fresh();
```

> **💡 ポイント**: `update()`メソッドは`$fillable`に定義されたカラムのみ更新できます。

---

## Step 4: バックエンド実装

### 4-1. editアクションを実装する

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
/**
 * Show the form for editing the specified resource.
 */
public function edit(Task $task)
{
    // Bladeで必要な変数を確認
    // $task → 編集対象のタスク
    // $categories → カテゴリー一覧（セレクトボックス用）
    
    $categories = Category::all();
    
    return view('tasks.edit', compact('task', 'categories'));
}
```

### 4-2. updateアクションを実装する

```php
/**
 * Update the specified resource in storage.
 */
public function update(Request $request, Task $task)
{
    // バリデーション（作成と同じルール）
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'description' => 'nullable|string',
        'category_id' => 'nullable|exists:categories,id',
        'status' => 'in:pending,in_progress,completed',
        'due_date' => 'nullable|date',
    ]);
    
    // タスクを更新
    $task->update($validated);
    
    return redirect()->route('tasks.show', $task)
        ->with('success', 'タスクを更新しました');
}
```

**コードリーディング**：

```php
public function update(Request $request, Task $task)
```
→ ルートモデルバインディングで`$task`を取得し、`$request`でフォームデータを受け取ります。

```php
$task->update($validated);
```
→ バリデーション済みのデータでタスクを更新します。`$fillable`に定義されたカラムのみ更新されます。

### 4-3. @method('PUT')の仕組み

HTMLフォームは`GET`と`POST`しかサポートしていません。`PUT`や`DELETE`を使うには、`@method`ディレクティブを使います。

```blade
<form action="{{ route('tasks.update', $task) }}" method="POST">
    @csrf
    @method('PUT')
```

これにより、フォームに隠しフィールドが追加されます：

```html
<input type="hidden" name="_method" value="PUT">
```

Laravelはこの隠しフィールドを見て、`PUT`リクエストとして処理します。

---

## Step 5: 動作確認

### 5-1. 編集画面を確認する

```
http://localhost/tasks/1/edit
```

| 確認項目 | 期待する結果 |
|:---|:---|
| フォームが表示される | エラーなく表示される |
| 既存データが表示される | タイトル、説明などが入力済み |
| カテゴリーが選択されている | 既存のカテゴリーが選択状態 |

### 5-2. タスクを更新する

1. タイトルを「更新後のタスク」に変更
2. 「更新」ボタンをクリック

| 確認項目 | 期待する結果 |
|:---|:---|
| 詳細画面にリダイレクトされる | 更新後のタスクが表示される |
| フラッシュメッセージが表示される | 「タスクを更新しました」と表示される |

### 5-3. バリデーションを確認する

1. タイトルを空にして「更新」ボタンをクリック

| 確認項目 | 期待する結果 |
|:---|:---|
| エラーメッセージが表示される | 「タイトルは必須です」と表示される |
| 他の入力値が保持される | 変更した値が消えない |

---

## 💡 TIP: 作成と編集のバリデーションを共通化する

作成と編集で同じバリデーションルールを使う場合、**フォームリクエスト**を使って共通化できます。

```bash
sail artisan make:request TaskRequest
```

**ファイル**: `app/Http/Requests/TaskRequest.php`

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class TaskRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'category_id' => 'nullable|exists:categories,id',
            'status' => 'in:pending,in_progress,completed',
            'due_date' => 'nullable|date',
        ];
    }
}
```

**コントローラーで使用**：

```php
use App\Http\Requests\TaskRequest;

public function store(TaskRequest $request)
{
    $validated = $request->validated();
    // ...
}

public function update(TaskRequest $request, Task $task)
{
    $validated = $request->validated();
    // ...
}
```

---

## 💡 TIP: Null安全演算子

```blade
value="{{ old('due_date', $task->due_date?->format('Y-m-d')) }}"
```

`?->`は**Null安全演算子**です。`$task->due_date`がNULLの場合、`format()`を呼び出さずにNULLを返します。

これにより、期限が設定されていないタスクでもエラーにならずに表示できます。

---

## ✨ まとめ

このセクションでは、「提供コードありき」の開発フローでタスク編集を実装しました。

| ステップ | 学んだこと |
|:---|:---|
| Step 1 | 画面アクセスでエラーを確認 |
| Step 2 | Bladeを読み解いて、old()の第2引数と@method('PUT')を理解 |
| Step 3 | Tinkerで更新処理を確認 |
| Step 4 | editとupdateアクションを実装 |
| Step 5 | 動作確認とバリデーションの確認 |

次のセクションでは、タスク削除の実装について学びます。

---
