# Tutorial 12-2-3: タスク作成の実装

## 🎯 このセクションで学ぶこと

- 提供されたフォーム画面を読み解き、必要なバリデーションを特定する方法を学ぶ
- Tinkerでデータ作成を確認してから、コントローラーを実装する方法を学ぶ
- フォーム送信とバリデーションの実装方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### フォーム実装の流れ

フォーム画面の実装は、以下の2つのアクションが必要です：

| アクション | HTTPメソッド | 役割 |
|:---|:---|:---|
| `create` | GET | フォーム画面を表示 |
| `store` | POST | フォームデータを受け取って保存 |

今回も「提供コードありき」のフローで進めます：

```
1. 画面アクセス＆エラー確認
2. Bladeの解読（フォームの項目を確認）
3. Tinker検証（データ作成を確認）
4. バックエンド実装
```

---

## Step 1: 画面アクセス＆エラー確認

### 1-1. ブラウザでアクセスする

```
http://localhost/tasks/create
```

### 1-2. エラーを確認する

```
Undefined variable $categories
```

**読み解き**：`create`アクションで`$categories`を渡していないため、エラーになっています。

---

## Step 2: Bladeの解読

### 2-1. tasks/create.blade.phpを読む

`resources/views/tasks/create.blade.php`を開いて、フォームの項目を確認します。

```blade
<form action="{{ route('tasks.store') }}" method="POST">
    @csrf
    
    <div class="form-group">
        <label for="title">タイトル <span style="color: red;">*</span></label>
        <input type="text" id="title" name="title" value="{{ old('title') }}" required>
        @error('title')
            <p class="error">{{ $message }}</p>
        @enderror
    </div>
    
    <div class="form-group">
        <label for="description">説明</label>
        <textarea id="description" name="description">{{ old('description') }}</textarea>
    </div>
    
    <div class="form-group">
        <label for="category_id">カテゴリー</label>
        <select id="category_id" name="category_id">
            <option value="">選択してください</option>
            @foreach($categories as $category)
                <option value="{{ $category->id }}">{{ $category->name }}</option>
            @endforeach
        </select>
    </div>
    
    <div class="form-group">
        <label for="status">ステータス</label>
        <select id="status" name="status">
            <option value="pending">未着手</option>
            <option value="in_progress">進行中</option>
            <option value="completed">完了</option>
        </select>
    </div>
    
    <div class="form-group">
        <label for="due_date">期限</label>
        <input type="date" id="due_date" name="due_date" value="{{ old('due_date') }}">
    </div>
    
    <button type="submit">作成</button>
</form>
```

### 2-2. フォーム項目を整理する

| フィールド名 | name属性 | 必須 | バリデーション |
|:---|:---|:---|:---|
| タイトル | `title` | ✅ | 必須、文字列、最大255文字 |
| 説明 | `description` | - | 文字列、NULL許可 |
| カテゴリー | `category_id` | - | 存在するカテゴリーID、NULL許可 |
| ステータス | `status` | - | pending/in_progress/completedのいずれか |
| 期限 | `due_date` | - | 日付形式、NULL許可 |

### 2-3. 必要な変数を特定する

```blade
@foreach($categories as $category)
```

→ `$categories`（カテゴリー一覧）が必要です。

---

## Step 3: Tinker検証

コントローラーを実装する前に、**Tinkerでデータ作成を確認**します。

### 3-1. Tinkerを起動する

```bash
sail artisan tinker
```

### 3-2. タスクを作成する

```php
>>> App\Models\Task::create([
...     'user_id' => 1,
...     'title' => 'テストタスク',
...     'description' => 'これはテストです',
...     'status' => 'pending',
... ]);
```

**期待する結果**：

```
=> App\Models\Task {#1234
     user_id: 1,
     title: "テストタスク",
     description: "これはテストです",
     status: "pending",
     updated_at: "2024-01-15 12:00:00",
     created_at: "2024-01-15 12:00:00",
     id: 1,
   }
```

### 3-3. カテゴリー付きで作成する

```php
>>> $category = App\Models\Category::first();
>>> App\Models\Task::create([
...     'user_id' => 1,
...     'category_id' => $category->id,
...     'title' => 'カテゴリー付きタスク',
...     'status' => 'pending',
... ]);
```

### 3-4. 作成したタスクを確認する

```php
>>> App\Models\Task::with('category')->get();
```

> **💡 ポイント**: Tinkerで作成できることを確認してから、コントローラーを実装します。

---

## Step 4: バックエンド実装

### 4-1. createアクションを実装する

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
/**
 * Show the form for creating a new resource.
 */
public function create()
{
    // Bladeで必要な変数を確認
    // $categories → カテゴリー一覧（セレクトボックス用）
    
    $categories = Category::all();
    
    return view('tasks.create', compact('categories'));
}
```

### 4-2. storeアクションを実装する

```php
/**
 * Store a newly created resource in storage.
 */
public function store(Request $request)
{
    // バリデーション
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'description' => 'nullable|string',
        'category_id' => 'nullable|exists:categories,id',
        'status' => 'in:pending,in_progress,completed',
        'due_date' => 'nullable|date',
    ]);
    
    // タスクを作成
    // ※認証実装後は auth()->id() を使用
    $task = Task::create([
        'user_id' => 1, // 仮のユーザーID（認証実装後に修正）
        'title' => $validated['title'],
        'description' => $validated['description'] ?? null,
        'category_id' => $validated['category_id'] ?? null,
        'status' => $validated['status'] ?? 'pending',
        'due_date' => $validated['due_date'] ?? null,
    ]);
    
    return redirect()->route('tasks.show', $task)
        ->with('success', 'タスクを作成しました');
}
```

**コードリーディング**：

```php
$validated = $request->validate([...]);
```
→ バリデーションを実行し、失敗した場合は自動的に前のページにリダイレクトされます。

```php
'category_id' => 'nullable|exists:categories,id',
```
→ `nullable`でNULLを許可し、`exists:categories,id`で存在するカテゴリーIDかチェックします。

```php
return redirect()->route('tasks.show', $task)->with('success', '...');
```
→ 作成後は詳細画面にリダイレクトし、フラッシュメッセージを表示します。

---

## Step 5: 動作確認

### 5-1. フォーム画面を確認する

```
http://localhost/tasks/create
```

| 確認項目 | 期待する結果 |
|:---|:---|
| フォームが表示される | エラーなく表示される |
| カテゴリーが選択できる | セレクトボックスにカテゴリーが表示される |

### 5-2. タスクを作成する

1. タイトルに「テストタスク」と入力
2. カテゴリーを選択
3. 「作成」ボタンをクリック

| 確認項目 | 期待する結果 |
|:---|:---|
| 詳細画面にリダイレクトされる | 作成したタスクの詳細が表示される |
| フラッシュメッセージが表示される | 「タスクを作成しました」と表示される |

### 5-3. バリデーションを確認する

1. タイトルを空にして「作成」ボタンをクリック

| 確認項目 | 期待する結果 |
|:---|:---|
| エラーメッセージが表示される | 「タイトルは必須です」と表示される |
| 入力値が保持される | 他のフィールドの値が消えない |

---

## 💡 TIP: old()とバリデーションエラー

バリデーションエラー時に入力値を保持するには、`old()`ヘルパーを使います。

```blade
<input type="text" name="title" value="{{ old('title') }}">
```

Bladeファイルには既に`old()`が実装されているので、バリデーションエラー時に自動的に入力値が保持されます。

---

## 💡 TIP: @errorディレクティブ

バリデーションエラーを表示するには、`@error`ディレクティブを使います。

```blade
@error('title')
    <p class="error">{{ $message }}</p>
@enderror
```

`$message`には、バリデーションエラーメッセージが自動的に入ります。

---

## 💡 TIP: バリデーションメッセージの日本語化

デフォルトでは英語のエラーメッセージが表示されます。日本語化するには：

```bash
# 言語ファイルを公開
sail artisan lang:publish

# 日本語ファイルを作成
mkdir -p lang/ja
```

`lang/ja/validation.php`を作成し、日本語のメッセージを定義します。

---

## ✨ まとめ

このセクションでは、「提供コードありき」の開発フローでタスク作成を実装しました。

| ステップ | 学んだこと |
|:---|:---|
| Step 1 | 画面アクセスでエラーを確認 |
| Step 2 | Bladeを読み解いて、フォーム項目とバリデーションを特定 |
| Step 3 | Tinkerでデータ作成を確認 |
| Step 4 | createとstoreアクションを実装 |
| Step 5 | 動作確認とバリデーションの確認 |

次のセクションでは、タスク詳細の実装について学びます。

---
