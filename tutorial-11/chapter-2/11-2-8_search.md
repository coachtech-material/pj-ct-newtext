# Tutorial 11-2-8: 検索機能の実装

## 🎯 このセクションで学ぶこと

*   タスクの検索機能を実装する方法を学ぶ。
*   WHERE句を使って条件に合うデータを絞り込む方法を学ぶ。
*   検索フォームを実装し、ユーザーが検索できるようにする方法を学ぶ。

---

## 導入：なぜ検索機能が重要なのか

**検索機能**は、大量のデータから目的のデータを見つける機能です。

検索機能を実装することで、ユーザーは効率的にデータを見つけられるようになります。

---

## 詳細解説

### 🔍 検索フォームの追加

タスク一覧ページに、検索フォームを追加します。

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<h1>タスク一覧</h1>

@if (session('success'))
    <div style="color: green;">
        {{ session('success') }}
    </div>
@endif

<a href="{{ route('tasks.create') }}">新規作成</a>

<form method="GET" action="{{ route('tasks.index') }}">
    <input type="text" name="keyword" placeholder="タイトルで検索" value="{{ request('keyword') }}">
    <select name="status">
        <option value="">すべて</option>
        <option value="未完了" {{ request('status') == '未完了' ? 'selected' : '' }}>未完了</option>
        <option value="完了" {{ request('status') == '完了' ? 'selected' : '' }}>完了</option>
    </select>
    <button type="submit">検索</button>
    <a href="{{ route('tasks.index') }}">クリア</a>
</form>

<table border="1">
    <!-- ... -->
</table>

{{ $tasks->appends(request()->query())->links() }}
```

---

### 🔍 コントローラーのindexメソッドを修正

検索条件を追加します。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function index(Request $request)
{
    $query = Task::where('user_id', auth()->id());

    // キーワード検索
    if ($request->filled('keyword')) {
        $query->where('title', 'like', '%' . $request->keyword . '%');
    }

    // ステータス検索
    if ($request->filled('status')) {
        $query->where('status', $request->status);
    }

    $tasks = $query->orderBy('created_at', 'desc')->paginate(10);

    return view('tasks.index', compact('tasks'));
}
```

---

### 🔍 filled()メソッド

`filled()`メソッドは、**リクエストに値が存在し、かつ空でない場合にtrueを返す**メソッドです。

```php
if ($request->filled('keyword')) {
    // keywordが存在し、かつ空でない場合
}
```

---

### 🔍 LIKE句

`LIKE`句は、**部分一致検索**を行うSQL構文です。

```php
$query->where('title', 'like', '%' . $request->keyword . '%');
```

*   `%keyword%`: keywordを含む
*   `keyword%`: keywordで始まる
*   `%keyword`: keywordで終わる

---

### 🔍 動作確認

ブラウザでタスク一覧ページにアクセスし、検索フォームが表示されることを確認します。

1. キーワードに「テスト」と入力
2. 「検索」ボタンをクリック
3. タイトルに「テスト」を含むタスクのみが表示される

---

### 🔍 複数条件の検索

複数の条件を組み合わせて検索できます。

1. キーワードに「テスト」と入力
2. ステータスに「未完了」を選択
3. 「検索」ボタンをクリック
4. タイトルに「テスト」を含み、かつステータスが「未完了」のタスクのみが表示される

---

### 🔍 期限での検索

期限での検索も追加できます。

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<form method="GET" action="{{ route('tasks.index') }}">
    <input type="text" name="keyword" placeholder="タイトルで検索" value="{{ request('keyword') }}">
    <select name="status">
        <option value="">すべて</option>
        <option value="未完了" {{ request('status') == '未完了' ? 'selected' : '' }}>未完了</option>
        <option value="完了" {{ request('status') == '完了' ? 'selected' : '' }}>完了</option>
    </select>
    <input type="date" name="due_date_from" value="{{ request('due_date_from') }}" placeholder="期限（開始）">
    <input type="date" name="due_date_to" value="{{ request('due_date_to') }}" placeholder="期限（終了）">
    <button type="submit">検索</button>
    <a href="{{ route('tasks.index') }}">クリア</a>
</form>
```

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
// 期限（開始）
if ($request->filled('due_date_from')) {
    $query->where('due_date', '>=', $request->due_date_from);
}

// 期限（終了）
if ($request->filled('due_date_to')) {
    $query->where('due_date', '<=', $request->due_date_to);
}
```

---

### 🔍 検索結果の件数表示

検索結果の件数を表示します。

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<p>検索結果: {{ $tasks->total() }}件</p>

<table border="1">
    <!-- ... -->
</table>
```

---

### 💡 TIP: スコープを使った検索

検索ロジックをモデルに移動できます。

**ファイル**: `app/Models/Task.php`

```php
public function scopeSearch($query, $keyword)
{
    if ($keyword) {
        $query->where('title', 'like', '%' . $keyword . '%');
    }
    return $query;
}

public function scopeStatus($query, $status)
{
    if ($status) {
        $query->where('status', $status);
    }
    return $query;
}
```

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
$tasks = Task::where('user_id', auth()->id())
    ->search($request->keyword)
    ->status($request->status)
    ->orderBy('created_at', 'desc')
    ->paginate(10);
```

---

### 🚨 よくある間違い

#### 間違い1: SQLインジェクション

**対処法**: Laravelのクエリビルダーを使うと、自動的にエスケープされます。生のSQLを使う場合は、必ずバインディングを使います。

---

#### 間違い2: ページネーションでクエリパラメータが消える

**対処法**: `appends(request()->query())`を使います。

```blade
{{ $tasks->appends(request()->query())->links() }}
```

---

#### 間違い3: 検索フォームの値が保持されない

**対処法**: `value="{{ request('keyword') }}"`を使います。

---

## ✨ まとめ

このセクションでは、検索機能を実装しました。

*   タスクの検索機能を実装し、条件に合うデータを絞り込めるようにした。
*   WHERE句を使って、複数の条件を組み合わせた検索を実装した。
*   検索フォームを実装し、ユーザーが検索できるようにした。

次のChapterでは、認証とリレーションシップについて学びます。

---

## 📝 学習のポイント

- [ ] 検索フォームを実装した。
- [ ] WHERE句とLIKE句を使った。
- [ ] filled()メソッドを使った。
- [ ] スコープを使った検索を学んだ。
