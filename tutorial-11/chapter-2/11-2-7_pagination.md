# Tutorial 11-2-7: ページネーションの実装

## 🎯 このセクションで学ぶこと

*   ページネーションを実装し、大量のデータを扱えるようにする方法を学ぶ。
*   Laravelの組み込みページネーション機能を使う方法を学ぶ。
*   ページネーションのカスタマイズ方法を学ぶ。

---

## 導入：なぜページネーションが重要なのか

**ページネーション**は、大量のデータを複数のページに分割して表示する機能です。

ページネーションを実装することで、以下のようなメリットがあります。

*   **パフォーマンスの向上**: 一度に表示するデータ量を減らすことで、ページの読み込み速度が向上する
*   **ユーザビリティの向上**: データが見やすくなり、ユーザーが目的のデータを見つけやすくなる

---

## 詳細解説

### 🔍 コントローラーのindexメソッドを修正

`index`メソッドで、`paginate()`メソッドを使います。

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function index()
{
    $tasks = Task::where('user_id', auth()->id())
        ->orderBy('created_at', 'desc')
        ->paginate(10);  // 1ページあたり10件

    return view('tasks.index', compact('tasks'));
}
```

---

### 🔍 paginate()メソッド

`paginate()`メソッドは、**ページネーションを実装するメソッド**です。

```php
$tasks = Task::paginate(10);  // 1ページあたり10件
```

*   `paginate(10)`: 1ページあたり10件表示する
*   `paginate(20)`: 1ページあたり20件表示する

---

### 🔍 ビューでページネーションリンクを表示

ビューで、`links()`メソッドを使ってページネーションリンクを表示します。

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<h1>タスク一覧</h1>

@if (session('success'))
    <div style="color: green;">
        {{ session('success') }}
    </div>
@endif

<a href="{{ route('tasks.create') }}">新規作成</a>

<table border="1">
    <thead>
        <tr>
            <th>ID</th>
            <th>タイトル</th>
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

{{ $tasks->links() }}
```

---

### 🔍 動作確認

ブラウザでタスク一覧ページにアクセスし、ページネーションリンクが表示されることを確認します。

1. タスクを20件作成する
2. タスク一覧ページにアクセスする
3. 1ページ目に10件のタスクが表示される
4. 「次へ」リンクをクリックすると、2ページ目に移動する

---

### 🔍 ページネーションのスタイル

デフォルトのページネーションは、Tailwind CSSのスタイルが適用されています。

Bootstrapのスタイルを使いたい場合は、`AppServiceProvider`で設定します。

**ファイル**: `app/Providers/AppServiceProvider.php`

```php
use Illuminate\Pagination\Paginator;

public function boot()
{
    Paginator::useBootstrap();
}
```

---

### 🔍 simplePaginate()メソッド

`simplePaginate()`メソッドは、**シンプルなページネーション**を実装するメソッドです。

```php
$tasks = Task::simplePaginate(10);
```

`simplePaginate()`を使うと、「前へ」「次へ」のリンクのみが表示されます。

---

### 🔍 ページネーションの情報を表示

ページネーションの情報を表示できます。

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<p>
    全{{ $tasks->total() }}件中、{{ $tasks->firstItem() }}〜{{ $tasks->lastItem() }}件を表示
</p>

{{ $tasks->links() }}
```

---

### 🔍 クエリパラメータの保持

検索機能と組み合わせる場合、クエリパラメータを保持する必要があります。

```blade
{{ $tasks->appends(request()->query())->links() }}
```

---

### 💡 TIP: カスタムページネーションビュー

ページネーションのビューをカスタマイズできます。

**ビューの公開**:

```bash
php artisan vendor:publish --tag=laravel-pagination
```

これにより、`resources/views/vendor/pagination`にページネーションのビューが公開されます。

---

### 🚨 よくある間違い

#### 間違い1: all()を使ってしまう

**対処法**: `all()`の代わりに`paginate()`を使います。

---

#### 間違い2: links()を忘れる

**対処法**: ビューに`{{ $tasks->links() }}`を追加します。

---

#### 間違い3: ページネーションが表示されない

**対処法**: データが10件以下の場合、ページネーションは表示されません。データを11件以上作成してください。

---

## ✨ まとめ

このセクションでは、ページネーションを実装しました。

*   ページネーションを実装し、大量のデータを扱えるようにした。
*   Laravelの組み込みページネーション機能を使った。
*   ページネーションのカスタマイズ方法を学んだ。

次のセクションでは、検索機能の実装について学びます。

---

## 📝 学習のポイント

- [ ] paginate()メソッドを使った。
- [ ] links()メソッドでページネーションリンクを表示した。
- [ ] simplePaginate()メソッドを学んだ。
- [ ] ページネーションの情報を表示した。
