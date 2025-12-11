# Tutorial 11-3-8: リレーションシップを使った検索

## 🎯 このセクションで学ぶこと

*   whereHas()を使って、リレーションシップを使った検索を実装する方法を学ぶ。
*   タグで検索できるようにする方法を学ぶ。
*   複数の条件を組み合わせた検索を実装する方法を学ぶ。

---

## 導入：なぜリレーションシップを使った検索が重要なのか

**リレーションシップを使った検索**は、**関連するモデルの条件で検索する機能**です。

例えば、「プログラミング」タグが付いているタスクを検索したい場合に使います。

---

## 詳細解説

### 🔍 whereHas()メソッド

`whereHas()`メソッドを使うと、リレーションシップを使った検索ができます。

```php
$tasks = Task::whereHas('tags', function ($query) {
    $query->where('name', 'プログラミング');
})->get();
```

---

### 🔍 タグで検索

タグで検索できるようにします。

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
    <select name="tag_id">
        <option value="">すべてのタグ</option>
        @foreach ($tags as $tag)
            <option value="{{ $tag->id }}" {{ request('tag_id') == $tag->id ? 'selected' : '' }}>
                {{ $tag->name }}
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
    $query = Task::with(['category', 'tags']);

    // キーワード検索
    if ($request->filled('keyword')) {
        $query->where('title', 'like', '%' . $request->keyword . '%');
    }

    // カテゴリー検索
    if ($request->filled('category_id')) {
        $query->where('category_id', $request->category_id);
    }

    // タグ検索
    if ($request->filled('tag_id')) {
        $query->whereHas('tags', function ($q) use ($request) {
            $q->where('tags.id', $request->tag_id);
        });
    }

    // ステータス検索
    if ($request->filled('status')) {
        $query->where('status', $request->status);
    }

    $tasks = $query->orderBy('created_at', 'desc')->paginate(10);

    $categories = Category::all();
    $tags = Tag::all();

    return view('tasks.index', compact('tasks', 'categories', 'tags'));
}
```

---

### 🔍 複数のタグで検索

複数のタグで検索する場合は、チェックボックスを使います。

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
    <div>
        <label>タグ</label>
        @foreach ($tags as $tag)
            <label>
                <input type="checkbox" name="tag_ids[]" value="{{ $tag->id }}" {{ in_array($tag->id, request('tag_ids', [])) ? 'checked' : '' }}>
                {{ $tag->name }}
            </label>
        @endforeach
    </div>
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
// タグ検索（複数）
if ($request->filled('tag_ids')) {
    $query->whereHas('tags', function ($q) use ($request) {
        $q->whereIn('tags.id', $request->tag_ids);
    });
}
```

---

### 🔍 すべてのタグを含むタスクを検索

すべてのタグを含むタスクを検索する場合は、`whereHas()`を複数回使います。

```php
if ($request->filled('tag_ids')) {
    foreach ($request->tag_ids as $tagId) {
        $query->whereHas('tags', function ($q) use ($tagId) {
            $q->where('tags.id', $tagId);
        });
    }
}
```

---

### 🔍 has()メソッド

`has()`メソッドを使うと、リレーションシップが存在するかどうかで検索できます。

```php
// タグが1つ以上付いているタスク
$tasks = Task::has('tags')->get();

// タグが3つ以上付いているタスク
$tasks = Task::has('tags', '>=', 3)->get();
```

---

### 🔍 doesntHave()メソッド

`doesntHave()`メソッドを使うと、リレーションシップが存在しないタスクを検索できます。

```php
// タグが付いていないタスク
$tasks = Task::doesntHave('tags')->get();
```

---

### 💡 TIP: orWhereHas()

`orWhereHas()`を使うと、OR条件で検索できます。

```php
$tasks = Task::whereHas('tags', function ($query) {
    $query->where('name', 'プログラミング');
})->orWhereHas('tags', function ($query) {
    $query->where('name', '勉強');
})->get();
```

---

### 🚨 よくある間違い

#### 間違い1: whereHas()の中でテーブル名を指定しない

**対処法**: `tags.id`のように、テーブル名を指定します。

---

#### 間違い2: Eager Loadingを忘れる

**対処法**: `with()`を使って、Eager Loadingを行います。

---

#### 間違い3: has()とwhereHas()を混同する

**対処法**: `has()`は存在チェック、`whereHas()`は条件付き検索です。

---

## ✨ まとめ

このセクションでは、リレーションシップを使った検索を実装しました。

*   whereHas()を使って、リレーションシップを使った検索を実装した。
*   タグで検索できるようにした。
*   has()とdoesntHave()を学んだ。

次のChapterでは、セキュリティについて学びます。

---

## 📝 学習のポイント

- [ ] whereHas()を使った。
- [ ] タグで検索できるようにした。
- [ ] has()とdoesntHave()を学んだ。
- [ ] 複数の条件を組み合わせた検索を実装した。
