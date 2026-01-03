# Tutorial 12-2-4: タスク詳細の実装

## 🎯 このセクションで学ぶこと

- 提供された詳細画面を読み解き、必要なデータを特定する方法を学ぶ
- ルートモデルバインディングを使って、コードを簡潔にする方法を学ぶ
- Tinkerで1件取得を確認してから、コントローラーを実装する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 詳細表示の特徴

一覧表示では`Task::all()`で全件取得しました。詳細表示では`Task::find($id)`で**1件だけ取得**します。

この「IDで1件取得」というパターンは、「編集」「削除」でも使うので、**先に詳細表示で学んでおくと効率的**です。

今回も「提供コードありき」のフローで進めます：

```
1. 画面アクセス＆エラー確認
2. Bladeの解読（必要なデータを確認）
3. Tinker検証（1件取得を確認）
4. バックエンド実装
```

---

## Step 1: 画面アクセス＆エラー確認

### 1-1. ブラウザでアクセスする

```
http://localhost/tasks/1
```

### 1-2. エラーを確認する

```
Undefined variable $task
```

**読み解き**：`show`アクションで`$task`を渡していないため、エラーになっています。

---

## Step 2: Bladeの解読

### 2-1. tasks/show.blade.phpを読む

`resources/views/tasks/show.blade.php`を開いて、必要なデータを確認します。

```blade
<h1>{{ $task->title }}</h1>

<table>
    <tr>
        <th>ステータス</th>
        <td>
            <span class="status-{{ $task->status }}">
                @if($task->status === 'pending') 未着手
                @elseif($task->status === 'in_progress') 進行中
                @else 完了
                @endif
            </span>
        </td>
    </tr>
    <tr>
        <th>カテゴリー</th>
        <td>{{ $task->category->name ?? '未設定' }}</td>
    </tr>
    <tr>
        <th>期限</th>
        <td>{{ $task->due_date ? $task->due_date->format('Y年m月d日') : '未設定' }}</td>
    </tr>
    <tr>
        <th>説明</th>
        <td>{!! nl2br(e($task->description)) ?: '説明なし' !!}</td>
    </tr>
    <tr>
        <th>作成日時</th>
        <td>{{ $task->created_at->format('Y年m月d日 H:i') }}</td>
    </tr>
</table>

<a href="{{ route('tasks.edit', $task) }}">編集</a>
<form action="{{ route('tasks.destroy', $task) }}" method="POST">
    @csrf
    @method('DELETE')
    <button type="submit">削除</button>
</form>
```

### 2-2. 必要なデータを整理する

| 変数 | 型 | 説明 |
|:---|:---|:---|
| `$task` | Task | タスクのモデルインスタンス |
| `$task->category` | Category | タスクに紐づくカテゴリー（リレーション） |

### 2-3. 必要なリレーションを特定する

```blade
{{ $task->category->name ?? '未設定' }}
```

→ `$task->category`（Categoryへのリレーション）が必要です。

---

## Step 3: Tinker検証

コントローラーを実装する前に、**Tinkerで1件取得を確認**します。

### 3-1. Tinkerを起動する

```bash
sail artisan tinker
```

### 3-2. タスクを1件取得する

```php
>>> $task = App\Models\Task::find(1);
>>> $task;
```

**期待する結果**：

```
=> App\Models\Task {#1234
     id: 1,
     user_id: 1,
     category_id: 1,
     title: "テストタスク",
     ...
   }
```

### 3-3. リレーションを確認する

```php
>>> $task->category;
```

**期待する結果**：

```
=> App\Models\Category {#5678
     id: 1,
     name: "仕事",
     ...
   }
```

### 3-4. 存在しないIDを取得する

```php
>>> App\Models\Task::find(9999);
```

**期待する結果**：

```
=> null
```

> **💡 ポイント**: `find()`はNULLを返しますが、`findOrFail()`は404エラーを返します。

```php
>>> App\Models\Task::findOrFail(9999);
```

**期待する結果**：

```
Illuminate\Database\Eloquent\ModelNotFoundException
```

---

## Step 4: バックエンド実装

### 4-1. showアクションを実装する

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
/**
 * Display the specified resource.
 */
public function show(Task $task)
{
    // Bladeで必要な変数を確認
    // $task → タスクのモデルインスタンス
    // $task->category → カテゴリーへのリレーション
    
    return view('tasks.show', compact('task'));
}
```

**コードリーディング**：

```php
public function show(Task $task)
```
→ **ルートモデルバインディング**を使っています。URLの`/tasks/1`から自動的に`Task::findOrFail(1)`が実行され、`$task`に代入されます。

### 4-2. ルートモデルバインディングとは

**従来の方法**：

```php
public function show($id)
{
    $task = Task::findOrFail($id);
    return view('tasks.show', compact('task'));
}
```

**ルートモデルバインディングを使った方法**：

```php
public function show(Task $task)
{
    return view('tasks.show', compact('task'));
}
```

引数に`Task $task`と型ヒントを書くだけで、**URLのIDから自動的にモデルを取得**してくれます。

**メリット**：
- コードが簡潔になる
- 存在しないIDの場合、自動的に404エラーを返す
- コントローラーの責務が明確になる

---

## Step 5: 動作確認

### 5-1. ブラウザでアクセスする

```
http://localhost/tasks/1
```

### 5-2. 確認ポイント

| 確認項目 | 期待する結果 |
|:---|:---|
| タスク詳細が表示される | タイトル、説明、ステータスなどが表示される |
| カテゴリー名が表示される | `$task->category->name`が正しく表示される |
| 編集・削除ボタンが表示される | リンクが正しく生成されている |

### 5-3. 存在しないタスクにアクセスする

```
http://localhost/tasks/9999
```

| 確認項目 | 期待する結果 |
|:---|:---|
| 404エラーが表示される | ルートモデルバインディングが自動で404を返す |

---

## 💡 TIP: Eager Loadingで最適化

詳細画面でもN+1問題を防ぐため、Eager Loadingを使うことができます。

```php
public function show(Task $task)
{
    // リレーションを事前に読み込む
    $task->load('category');
    
    return view('tasks.show', compact('task'));
}
```

ただし、詳細画面は1件しか表示しないので、N+1問題の影響は小さいです。一覧画面ほど重要ではありません。

---

## 💡 TIP: @ddでデバッグする

データが正しく取得できているか確認するには、Bladeに`@dd()`を追加します。

```blade
{{-- タスクの内容を確認 --}}
@dd($task)

{{-- リレーションを確認 --}}
@dd($task->category)
```

---

## 💡 TIP: Null合体演算子

```blade
{{ $task->category->name ?? '未設定' }}
```

`??`は**Null合体演算子**です。`$task->category`がNULLの場合、「未設定」を表示します。

これにより、カテゴリーが設定されていないタスクでもエラーにならずに表示できます。

---

## ✨ まとめ

このセクションでは、「提供コードありき」の開発フローでタスク詳細を実装しました。

| ステップ | 学んだこと |
|:---|:---|
| Step 1 | 画面アクセスでエラーを確認 |
| Step 2 | Bladeを読み解いて、必要なデータとリレーションを特定 |
| Step 3 | Tinkerで1件取得とリレーションを確認 |
| Step 4 | ルートモデルバインディングでshowアクションを実装 |
| Step 5 | 動作確認と404エラーの確認 |

次のセクションでは、タスク編集の実装について学びます。

---
