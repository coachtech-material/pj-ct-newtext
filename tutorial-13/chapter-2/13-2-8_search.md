# Tutorial 13-2-8: 検索機能の実装

## 🎯 このセクションで学ぶこと

- 提供された検索フォームを読み解き、検索処理の流れを理解する方法を学ぶ
- WHERE句を使って条件に合うデータを絞り込む方法を学ぶ
- Tinkerで検索クエリを確認してから、コントローラーを実装する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 検索機能の特徴

検索機能は、**一覧表示の拡張**として実装します。

```php
// 検索なし
$tasks = Task::all();

// 検索あり
$tasks = Task::where('title', 'like', "%{$keyword}%")->get();
```

一覧表示のコードを少し修正するだけで実装できます。

今回も「提供コードありき」のフローで進めます：

```
1. 画面アクセス＆エラー確認（検索フォームの確認）
2. Bladeの解読（検索フォームの構造を確認）
3. Tinker検証（検索クエリを確認）
4. バックエンド実装
```

---

## Step 1: 画面アクセス＆エラー確認

### 1-1. 一覧画面で検索フォームを確認する

```
http://localhost/tasks
```

一覧画面に検索フォームが表示されていることを確認します。

### 1-2. 検索を実行する

キーワードを入力して「検索」ボタンをクリックすると、URLが変わります：

```
http://localhost/tasks?keyword=テスト&status=pending
```

**読み解き**：検索条件がURLのクエリパラメータとして送信されています。現時点では、検索条件が無視されて全件表示されます。

---

## Step 2: Bladeの解読

### 2-1. 検索フォームを読む

`resources/views/tasks/index.blade.php`の検索フォーム部分を確認します。

```blade
<form action="{{ route('tasks.index') }}" method="GET">
    <div class="search-form">
        <input type="text" name="keyword" placeholder="タイトルで検索" 
               value="{{ request('keyword') }}">
        
        <select name="status">
            <option value="">すべてのステータス</option>
            <option value="pending" {{ request('status') === 'pending' ? 'selected' : '' }}>未着手</option>
            <option value="in_progress" {{ request('status') === 'in_progress' ? 'selected' : '' }}>進行中</option>
            <option value="completed" {{ request('status') === 'completed' ? 'selected' : '' }}>完了</option>
        </select>
        
        <label>
            期限:
            <input type="date" name="due_date_from" value="{{ request('due_date_from') }}">
            〜
            <input type="date" name="due_date_to" value="{{ request('due_date_to') }}">
        </label>
        
        <button type="submit">検索</button>
        <a href="{{ route('tasks.index') }}">クリア</a>
    </div>
</form>
```

### 2-2. 検索フォームの構造を理解する

| 要素 | 説明 |
|:---|:---|
| `method="GET"` | 検索はGETリクエスト（URLに条件が含まれる） |
| `name="keyword"` | タイトルでの部分一致検索 |
| `name="status"` | ステータスでの絞り込み |
| `name="due_date_from"` / `name="due_date_to"` | 期限の範囲検索 |
| `value="{{ request('keyword') }}"` | 検索後も入力値を保持 |

### 2-3. request()ヘルパーを理解する

```blade
value="{{ request('keyword') }}"
```

`request('keyword')`は、URLのクエリパラメータ`?keyword=xxx`の値を取得します。

これにより、検索後も**入力した値が保持**されます。

---

## Step 3: Tinker検証

コントローラーを実装する前に、**Tinkerで検索クエリを確認**します。

### 3-1. Tinkerを起動する

```bash
sail artisan tinker
```

### 3-2. 全件取得を確認する

```php
>>> App\Models\Task::all();
```

### 3-3. キーワード検索を確認する

```php
>>> App\Models\Task::where('title', 'like', '%テスト%')->get();
```

**期待する結果**：タイトルに「テスト」を含むタスクのみが取得される

### 3-4. ステータス検索を確認する

```php
>>> App\Models\Task::where('status', 'pending')->get();
```

**期待する結果**：ステータスが「pending」のタスクのみが取得される

### 3-5. 複数条件を組み合わせる

```php
>>> App\Models\Task::where('title', 'like', '%テスト%')
...     ->where('status', 'pending')
...     ->get();
```

**期待する結果**：タイトルに「テスト」を含み、かつステータスが「pending」のタスクのみが取得される

### 3-6. 日付範囲検索を確認する

```php
>>> App\Models\Task::where('due_date', '>=', '2024-01-01')
...     ->where('due_date', '<=', '2024-12-31')
...     ->get();
```

**期待する結果**：期限が2024年内のタスクのみが取得される

> **💡 ポイント**: Tinkerで検索クエリを確認してから、コントローラーに実装します。

---

## Step 4: バックエンド実装

### 4-1. indexアクションを修正する

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
/**
 * Display a listing of the resource.
 */
public function index(Request $request)
{
    // Bladeで必要な変数を確認
    // $tasks → タスク一覧（検索条件でフィルタリング）
    
    // 基本クエリ（ログインユーザーのタスクのみ）
    $query = Task::with('category');
    
    // キーワード検索
    if ($request->filled('keyword')) {
        $query->where('title', 'like', '%' . $request->keyword . '%');
    }
    
    // ステータス検索
    if ($request->filled('status')) {
        $query->where('status', $request->status);
    }
    
    // 期限（開始）
    if ($request->filled('due_date_from')) {
        $query->where('due_date', '>=', $request->due_date_from);
    }
    
    // 期限（終了）
    if ($request->filled('due_date_to')) {
        $query->where('due_date', '<=', $request->due_date_to);
    }
    
    // 並び替えとページネーション
    $tasks = $query->orderBy('created_at', 'desc')->paginate(10);
    
    return view('tasks.index', compact('tasks'));
}
```

**コードリーディング**：

```php
$query = Task::with('category');
```
→ クエリビルダーを変数に格納します。この時点ではまだSQLは実行されません。

```php
if ($request->filled('keyword')) {
```
→ `filled()`メソッドは、**リクエストに値が存在し、かつ空でない場合にtrue**を返します。

```php
$query->where('title', 'like', '%' . $request->keyword . '%');
```
→ `LIKE`句で**部分一致検索**を行います。`%keyword%`は「keywordを含む」という意味です。

```php
$tasks = $query->orderBy('created_at', 'desc')->paginate(10);
```
→ 最後に`paginate()`を呼び出すと、SQLが実行されます。

### 4-2. クエリビルダーの連鎖

```php
$query = Task::with('category');        // 基本クエリ
$query->where('title', 'like', '...');  // 条件を追加
$query->where('status', '...');         // さらに条件を追加
$tasks = $query->paginate(10);          // 最後に実行
```

条件を**段階的に追加**できるのがクエリビルダーの利点です。

---

## Step 5: 動作確認

### 5-1. キーワード検索を確認する

```
http://localhost/tasks?keyword=テスト
```

| 確認項目 | 期待する結果 |
|:---|:---|
| タイトルに「テスト」を含むタスクのみ表示 | 検索条件が適用されている |
| 検索フォームに「テスト」が入力されている | 入力値が保持されている |

### 5-2. 複数条件の検索を確認する

```
http://localhost/tasks?keyword=テスト&status=pending
```

| 確認項目 | 期待する結果 |
|:---|:---|
| 両方の条件を満たすタスクのみ表示 | AND条件で検索されている |

### 5-3. クリアボタンを確認する

1. 検索条件を入力して検索
2. 「クリア」リンクをクリック

| 確認項目 | 期待する結果 |
|:---|:---|
| 検索条件がリセットされる | 全てのタスクが表示される |
| URLからクエリパラメータが消える | `/tasks`に遷移 |

### 5-4. ページネーションを確認する

1. 検索条件を入力して検索
2. 2ページ目のリンクをクリック

| 確認項目 | 期待する結果 |
|:---|:---|
| 検索条件が保持される | URLに`?keyword=xxx&page=2`が含まれる |

---

## 💡 TIP: ページネーションでクエリパラメータを保持する

ページネーションリンクに検索条件を引き継ぐには、`appends()`を使います。

```blade
{{ $tasks->appends(request()->query())->links() }}
```

これがないと、2ページ目に移動したときに検索条件が消えてしまいます。

---

## 💡 TIP: 検索結果の件数表示

検索結果の件数を表示するには、`total()`を使います。

```blade
<p>検索結果: {{ $tasks->total() }}件</p>
```

`total()`はページネーションの**全件数**を取得します（現在のページの件数ではありません）。

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

**コントローラーで使用**：

```php
$tasks = Task::with('category')
    ->search($request->keyword)
    ->status($request->status)
    ->orderBy('created_at', 'desc')
    ->paginate(10);
```

スコープを使うと、**検索ロジックを再利用**できます。

---

## ✨ まとめ

このセクションでは、「提供コードありき」の開発フローで検索機能を実装しました。

| ステップ | 学んだこと |
|:---|:---|
| Step 1 | 検索フォームの確認とURLクエリパラメータの理解 |
| Step 2 | Bladeを読み解いて、request()ヘルパーと入力値の保持を理解 |
| Step 3 | Tinkerで検索クエリを確認（LIKE句、複数条件、日付範囲） |
| Step 4 | indexアクションにfilled()とクエリビルダーで検索を実装 |
| Step 5 | 動作確認とページネーションの確認 |

次のChapterでは、認証とリレーションシップについて学びます。

---
