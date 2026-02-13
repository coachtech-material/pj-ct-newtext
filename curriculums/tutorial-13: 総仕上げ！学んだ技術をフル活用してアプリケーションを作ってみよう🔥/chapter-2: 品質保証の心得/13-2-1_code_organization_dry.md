# Tutorial 13-2-1: コードの整理とDRY原則

## 🎯 このセクションで学ぶこと

- コードの整理方法を学ぶ
- DRY（Don't Repeat Yourself）原則を理解する
- 重複コードを共通化する方法を知る

> ⚠️ **注意**: このChapterでは**実際のコードは書きません**。品質の高いコードを書くための「心得」を学びます。実装はChapter 3以降で行います。

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ要件定義の次に品質保証を学ぶのか？」

要件定義が終わったら、すぐに実装を始めたくなりますよね。しかし、先輩エンジニアは**実装前に「良いコードとは何か」を意識します**。

### 理由1: 最初から意識することで手戻りを防ぐ

```
❌ 後から品質を意識する
→ 動くコードを書く → 問題に気づく → 大幅な書き直し

✅ 最初から品質を意識する
→ 良いコードの書き方を知る → 意識しながら実装 → 手戻りが少ない
```

### 理由2: 実務では「動くだけ」では不十分

実務では、コードは**チームで共有**され、**長期間メンテナンス**されます。読みやすく、変更しやすいコードを書くことが求められます。

### 理由3: 品質は後付けが難しい

品質の低いコードを後から改善するのは、最初から品質を意識して書くよりも**何倍も大変**です。

---

## DRY原則とは

### DRY = Don't Repeat Yourself

**DRY原則**とは、**同じコードを繰り返し書かない**という原則です。

日本語では「繰り返しを避けよ」と訳されます。

---

### なぜ重複コードが問題なのか

同じコードが複数箇所にあると、以下の問題が発生します。

| 問題 | 説明 | 具体例 |
|:---|:---|:---|
| **メンテナンスが大変** | 1箇所を修正すると、他の箇所も修正する必要がある | バリデーションルールを変更するとき、5箇所を修正する必要がある |
| **バグが発生しやすい** | 修正漏れが発生する | 3箇所修正したが、1箇所修正を忘れてバグになる |
| **コードが長くなる** | 可読性が低下する | 同じ処理が何度も出てきて、本質が見えにくくなる |

---

### 重複コードの例（悪い例）

タスク管理アプリで、所有者チェックが重複している例を見てみましょう。

```php
// タスク詳細
public function show(Task $task)
{
    // 所有者チェック（重複1）
    if ($task->user_id !== Auth::id()) {
        abort(403);
    }
    return view('tasks.show', compact('task'));
}

// タスク編集画面
public function edit(Task $task)
{
    // 所有者チェック（重複2）
    if ($task->user_id !== Auth::id()) {
        abort(403);
    }
    return view('tasks.edit', compact('task'));
}

// タスク更新
public function update(Request $request, Task $task)
{
    // 所有者チェック（重複3）
    if ($task->user_id !== Auth::id()) {
        abort(403);
    }
    $task->update($request->validated());
    return redirect()->route('tasks.show', $task);
}

// タスク削除
public function destroy(Task $task)
{
    // 所有者チェック（重複4）
    if ($task->user_id !== Auth::id()) {
        abort(403);
    }
    $task->delete();
    return redirect()->route('tasks.index');
}
```

**問題点**: `$task->user_id !== Auth::id()` のチェックが**4箇所**で重複しています。

もし所有者チェックのロジックを変更する場合（例: 管理者も編集可能にする）、4箇所すべてを修正する必要があります。

---

### Policyで共通化（良い例）

Laravelの**Policy**を使うと、認可ロジックを1箇所にまとめられます。

```php
// app/Policies/TaskPolicy.php
class TaskPolicy
{
    /**
     * タスクの詳細表示・編集・削除の認可
     */
    public function view(User $user, Task $task): bool
    {
        return $user->id === $task->user_id;
    }

    public function update(User $user, Task $task): bool
    {
        return $user->id === $task->user_id;
    }

    public function delete(User $user, Task $task): bool
    {
        return $user->id === $task->user_id;
    }
}
```

```php
// app/Http/Controllers/TaskController.php
public function show(Task $task)
{
    $this->authorize('view', $task);  // 1行で済む
    return view('tasks.show', compact('task'));
}

public function edit(Task $task)
{
    $this->authorize('update', $task);  // 1行で済む
    return view('tasks.edit', compact('task'));
}

public function update(Request $request, Task $task)
{
    $this->authorize('update', $task);  // 1行で済む
    $task->update($request->validated());
    return redirect()->route('tasks.show', $task);
}

public function destroy(Task $task)
{
    $this->authorize('delete', $task);  // 1行で済む
    $task->delete();
    return redirect()->route('tasks.index');
}
```

**改善点**:
- 所有者チェックのロジックが**Policyに集約**された
- コントローラーは`$this->authorize()`を呼ぶだけ
- ロジックを変更するときは**Policyの1箇所だけ**修正すればよい

---

## バリデーションの共通化

### 重複したバリデーション（悪い例）

```php
// タスク登録
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'priority' => 'required|integer|in:1,2,3',
        'category_id' => 'required|exists:categories,id',
    ]);
    // ...
}

// タスク更新（同じルールが重複）
public function update(Request $request, Task $task)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'priority' => 'required|integer|in:1,2,3',
        'category_id' => 'required|exists:categories,id',
    ]);
    // ...
}
```

### FormRequestで共通化（良い例）

```php
// app/Http/Requests/StoreTaskRequest.php
class StoreTaskRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'title' => 'required|max:255',
            'description' => 'nullable',
            'priority' => 'required|integer|in:1,2,3',
            'category_id' => 'required|exists:categories,id',
        ];
    }

    public function messages(): array
    {
        return [
            'title.required' => 'タイトルは必須です。',
            'priority.required' => '優先度は必須です。',
            'priority.in' => '優先度は1〜3の値を選択してください。',
            'category_id.required' => 'カテゴリーは必須です。',
            'category_id.exists' => '選択されたカテゴリーは存在しません。',
        ];
    }
}
```

```php
// コントローラー
public function store(StoreTaskRequest $request)
{
    auth()->user()->tasks()->create($request->validated());
    return redirect()->route('tasks.index');
}

public function update(StoreTaskRequest $request, Task $task)
{
    $this->authorize('update', $task);
    $task->update($request->validated());
    return redirect()->route('tasks.show', $task);
}
```

---

## Bladeコンポーネントで共通化

### 重複したフォーム（悪い例）

登録画面と編集画面で、同じフォームフィールドが重複しています。

```blade
{{-- 登録画面: resources/views/tasks/create.blade.php --}}
<form action="{{ route('tasks.store') }}" method="POST">
    @csrf
    <div class="mb-4">
        <label for="title">タイトル</label>
        <input type="text" name="title" value="{{ old('title') }}">
    </div>
    <div class="mb-4">
        <label for="priority">優先度</label>
        <select name="priority">
            <option value="1">低</option>
            <option value="2">中</option>
            <option value="3">高</option>
        </select>
    </div>
    <button type="submit">登録</button>
</form>

{{-- 編集画面: resources/views/tasks/edit.blade.php --}}
<form action="{{ route('tasks.update', $task) }}" method="POST">
    @csrf
    @method('PUT')
    <div class="mb-4">
        <label for="title">タイトル</label>
        <input type="text" name="title" value="{{ old('title', $task->title) }}">
    </div>
    <div class="mb-4">
        <label for="priority">優先度</label>
        <select name="priority">
            <option value="1" {{ $task->priority == 1 ? 'selected' : '' }}>低</option>
            <option value="2" {{ $task->priority == 2 ? 'selected' : '' }}>中</option>
            <option value="3" {{ $task->priority == 3 ? 'selected' : '' }}>高</option>
        </select>
    </div>
    <button type="submit">更新</button>
</form>
```

タイトル、優先度などのフォームフィールドが両方の画面でほぼ同じ内容になっています。フィールドを追加・変更するたびに、両方のファイルを修正する必要があります。

### コンポーネントで共通化（良い例）

```blade
{{-- resources/views/components/task-form.blade.php --}}
@props(['task' => null, 'categories'])

{{-- タイトル --}}
<div class="mb-4">
    <label for="title" class="block text-gray-700 font-medium mb-2">タイトル</label>
    <input type="text" name="title" id="title" 
        value="{{ old('title', $task?->title) }}"
        class="w-full border border-gray-300 rounded px-3 py-2">
    @error('title')
        <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
    @enderror
</div>

{{-- 優先度 --}}
<div class="mb-4">
    <label for="priority" class="block text-gray-700 font-medium mb-2">優先度</label>
    <select name="priority" id="priority" class="w-full border border-gray-300 rounded px-3 py-2">
        <option value="1" {{ old('priority', $task?->priority) == 1 ? 'selected' : '' }}>低</option>
        <option value="2" {{ old('priority', $task?->priority) == 2 ? 'selected' : '' }}>中</option>
        <option value="3" {{ old('priority', $task?->priority) == 3 ? 'selected' : '' }}>高</option>
    </select>
</div>

{{-- カテゴリー --}}
<div class="mb-4">
    <label for="category_id" class="block text-gray-700 font-medium mb-2">カテゴリー</label>
    <select name="category_id" id="category_id" class="w-full border border-gray-300 rounded px-3 py-2">
        <option value="">選択してください</option>
        @foreach ($categories as $category)
            <option value="{{ $category->id }}" 
                {{ old('category_id', $task?->category_id) == $category->id ? 'selected' : '' }}>
                {{ $category->name }}
            </option>
        @endforeach
    </select>
</div>

{{-- 説明 --}}
<div class="mb-6">
    <label for="description" class="block text-gray-700 font-medium mb-2">説明</label>
    <textarea name="description" id="description" rows="5"
        class="w-full border border-gray-300 rounded px-3 py-2">{{ old('description', $task?->description) }}</textarea>
</div>
```

```blade
{{-- 登録画面 --}}
<form action="{{ route('tasks.store') }}" method="POST">
    @csrf
    <x-task-form :categories="$categories" />
    <button type="submit">登録</button>
</form>

{{-- 編集画面 --}}
<form action="{{ route('tasks.update', $task) }}" method="POST">
    @csrf
    @method('PUT')
    <x-task-form :task="$task" :categories="$categories" />
    <button type="submit">更新</button>
</form>
```

---

## DRY原則の適用箇所まとめ

| 重複の種類 | 解決方法 | Laravelの機能 |
|:---|:---|:---|
| 認可チェックの重複 | 認可ロジックを集約 | **Policy** |
| バリデーションの重複 | バリデーションルールを集約 | **FormRequest** |
| ビューの重複 | UIパーツを共通化 | **Bladeコンポーネント** |
| クエリの重複 | クエリロジックを集約 | **スコープ** |

---

## 🚨 よくある間違い

### 間違い1: 過度な共通化

**問題**: 何でも共通化しようとして、かえって複雑になる

```php
// ❌ 過度な共通化
// 1箇所でしか使わないのに共通化している
class CommonHelper
{
    public static function formatTaskTitle($title)
    {
        return strtoupper($title);
    }
}
```

**対処法**: **2回以上使う**場合に共通化を検討する。1回しか使わないコードは共通化しない。

---

### 間違い2: 共通化のタイミングが早すぎる

**問題**: 最初から完璧な共通化を目指して、なかなか進まない

**対処法**: まずは動くコードを書き、**重複が見えてきたら**共通化する。

---

## ✨ まとめ

このセクションでは、コードの整理とDRY原則について学びました。

- **DRY原則**は「同じコードを繰り返し書かない」という原則
- 重複コードは**メンテナンス性の低下**と**バグの原因**になる
- Laravelでは**Policy**、**FormRequest**、**Bladeコンポーネント**で共通化できる
- **2回以上使う**場合に共通化を検討する

次のセクションでは、**命名規則**について学びます。

---
