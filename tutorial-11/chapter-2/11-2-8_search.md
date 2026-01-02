# Tutorial 11-2-8: 検索機能の実装

## 🎯 このセクションで学ぶこと

- タスクの検索機能を実装する方法を学ぶ
- WHERE句を使って条件に合うデータを絞り込む方法を学ぶ
- 検索フォームを実装し、ユーザーが検索できるようにする方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜCRUDの後に『検索』を実装するのか？」

CRUDが完成したら、次は「検索」機能です。なぜこのタイミングなのでしょうか？

---

### 理由1: CRUDが基本、検索は応用

検索機能は**応用機能**です。

まずはCRUDという基本機能を完成させてから、応用機能を追加するのが一般的です。

---

### 理由2: 一覧表示の拡張として実装

検索機能は、**一覧表示の拡張**として実装します。

```php
// 検索なし
$tasks = Task::all();

// 検索あり
$tasks = Task::where('title', 'like', "%{$keyword}%")->get();
```

一覧表示のコードを少し修正するだけで実装できます。

---

### 理由3: クエリビルダーを深く学ぶ

検索機能では、**複雑なクエリ**を書く必要があります。

- キーワード検索（LIKE）
- ステータスで絞り込み
- 日付で絞り込み
- 複数条件の組み合わせ

これらを通じて、Eloquentのクエリビルダーを深く理解できます。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | 検索フォームの作成 | ユーザーが検索条件を入力 |
| Step 2 | indexメソッドの修正 | 検索条件でフィルタリング |
| Step 3 | 期限での検索を追加 | より詳細な検索を可能に |
| Step 4 | 検索結果の件数表示 | ユーザーに結果を伝える |
| Step 5 | 動作確認 | 正しく動作するか確認する |

> 💡 **ポイント**: 検索はGETリクエストで実装します。URLに検索条件が含まれるので、ブックマークや共有ができます。

---

## Step 1: 検索フォームの作成

### 1-1. 一覧ページに検索フォームを追加する

タスク一覧ページに、検索フォームを追加します。

**ファイル**: `resources/views/tasks/index.blade.php`

`<h1>`タグの下、テーブルの上に以下のコードを追加します。

```blade
<form method="GET" action="{{ route('tasks.index') }}" style="margin-bottom: 20px; padding: 15px; background-color: #f5f5f5; border-radius: 4px;">
    <div style="display: flex; gap: 10px; flex-wrap: wrap; align-items: center;">
        <input type="text" name="keyword" placeholder="タイトルで検索" value="{{ request('keyword') }}" style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
        
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

### 1-2. コードリーディング

#### `method="GET"`

- 検索はGETリクエストで実装します
- URLに検索条件が含まれるので、**ブックマークや共有が可能**です
- 例: `/tasks?keyword=買い物&status=pending`

---

#### `value="{{ request('keyword') }}"`

- `request('keyword')`で、URLのクエリパラメータを取得します
- これにより、検索後も**入力した値が保持**されます

---

#### `{{ request('status') == 'pending' ? 'selected' : '' }}`

- 現在の検索条件と一致する場合、`selected`属性を追加します
- これにより、検索後も**選択した値が保持**されます

---

## Step 2: indexメソッドの修正

### 2-1. 検索条件を追加する

コントローラーのindexメソッドを修正します。

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

### 2-2. コードリーディング

#### `$query = Task::where('user_id', auth()->id())`

- まず、ログインユーザーのタスクのみを対象にします
- `$query`変数に**クエリビルダー**を格納します

---

#### `$request->filled('keyword')`

- `filled()`メソッドは、**リクエストに値が存在し、かつ空でない場合にtrue**を返します
- `has()`との違い: `has()`は空文字でもtrueを返しますが、`filled()`は空文字ではfalseを返します

---

#### `$query->where('title', 'like', '%' . $request->keyword . '%')`

- `LIKE`句で**部分一致検索**を行います
- `%keyword%`: keywordを含む
- `keyword%`: keywordで始まる
- `%keyword`: keywordで終わる

---

#### クエリビルダーの連鎖

```php
$query = Task::where('user_id', auth()->id());  // 基本条件
$query->where('title', 'like', '...');           // 条件を追加
$query->where('status', '...');                   // さらに条件を追加
$tasks = $query->paginate(10);                    // 最後に実行
```

条件を**段階的に追加**できるのがクエリビルダーの利点です。

---

## Step 3: 期限での検索を追加

### 3-1. 検索フォームに期限を追加する

期限での検索も追加します。

**ファイル**: `resources/views/tasks/index.blade.php`

検索フォームに以下を追加します。

```blade
<label style="display: flex; align-items: center; gap: 5px;">
    期限:
    <input type="date" name="due_date_from" value="{{ request('due_date_from') }}" style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
    〜
    <input type="date" name="due_date_to" value="{{ request('due_date_to') }}" style="padding: 8px; border: 1px solid #ddd; border-radius: 4px;">
</label>
```

---

### 3-2. コントローラーに期限検索を追加する

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

### 3-3. コードリーディング

#### `$query->where('due_date', '>=', $request->due_date_from)`

- `>=`は「以上」を意味します
- 指定した日付以降のタスクを検索します

---

#### 日付範囲検索

| 条件 | 意味 |
|------|------|
| `due_date >= 2024-01-01` | 2024年1月1日以降 |
| `due_date <= 2024-12-31` | 2024年12月31日以前 |
| 両方指定 | 2024年1月1日〜12月31日 |

---

## Step 4: 検索結果の件数表示

### 4-1. 件数を表示する

検索結果の件数を表示します。

**ファイル**: `resources/views/tasks/index.blade.php`

テーブルの上に以下を追加します。

```blade
<p style="margin-bottom: 10px;">検索結果: {{ $tasks->total() }}件</p>
```

---

### 4-2. ページネーションでクエリパラメータを保持する

ページネーションリンクに検索条件を引き継ぎます。

**ファイル**: `resources/views/tasks/index.blade.php`

テーブルの下に以下を追加します。

```blade
{{ $tasks->appends(request()->query())->links() }}
```

---

### 4-3. コードリーディング

#### `$tasks->total()`

- ページネーションの**全件数**を取得します
- 現在のページの件数ではなく、検索結果の総件数です

---

#### `$tasks->appends(request()->query())->links()`

- `appends(request()->query())`で、**現在のクエリパラメータをページネーションリンクに追加**します
- これがないと、2ページ目に移動したときに検索条件が消えてしまいます

---

## Step 5: 動作確認

### 5-1. キーワード検索を確認する

1. ブラウザでタスク一覧ページにアクセスする
2. キーワードに「買い物」と入力する
3. 「検索」ボタンをクリックする
4. タイトルに「買い物」を含むタスクのみが表示される

---

### 5-2. 複数条件の検索を確認する

1. キーワードに「タスク」と入力する
2. ステータスに「未着手」を選択する
3. 「検索」ボタンをクリックする
4. タイトルに「タスク」を含み、かつステータスが「未着手」のタスクのみが表示される

---

### 5-3. クリアボタンを確認する

1. 検索条件を入力して検索する
2. 「クリア」リンクをクリックする
3. 検索条件がリセットされ、全てのタスクが表示される

---

### 5-4. ページネーションを確認する

1. 検索条件を入力して検索する
2. 2ページ目のリンクをクリックする
3. 検索条件が保持されたまま、2ページ目が表示される

---

## 🚨 よくある間違い

### 間違い1: SQLインジェクション

**問題**: 生のSQLを使うと、悪意のある入力でデータベースが攻撃される

**対処法**: Laravelのクエリビルダーを使うと、自動的にエスケープされます。

```php
// 安全（クエリビルダー）
$query->where('title', 'like', '%' . $request->keyword . '%');

// 危険（生のSQL）
DB::select("SELECT * FROM tasks WHERE title LIKE '%{$request->keyword}%'");
```

---

### 間違い2: ページネーションでクエリパラメータが消える

**問題**: 2ページ目に移動すると検索条件がリセットされる

**対処法**: `appends(request()->query())`を使います。

```blade
{{ $tasks->appends(request()->query())->links() }}
```

---

### 間違い3: 検索フォームの値が保持されない

**問題**: 検索後、フォームが空になる

**対処法**: `value="{{ request('keyword') }}"`を使います。

---

## 💡 TIP: スコープを使った検索

検索ロジックをモデルに移動すると、コントローラーがスッキリします。

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

スコープを使うと、**検索ロジックを再利用**できます。

---

## ✨ まとめ

このセクションでは、検索機能を実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | GETメソッドで検索フォームを作成 |
| Step 2 | `filled()`とLIKE句で検索条件を追加 |
| Step 3 | 日付範囲検索の実装 |
| Step 4 | `total()`と`appends()`でUXを向上 |
| Step 5 | 動作確認の方法 |

次のChapterでは、認証とリレーションシップについて学びます。

---
