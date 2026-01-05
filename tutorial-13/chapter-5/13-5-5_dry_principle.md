# Tutorial 13-5-5: 重複コードの削除

## 🎯 このセクションで学ぶこと

- DRY原則（Don't Repeat Yourself）とは何かを理解する
- 重複コードが、なぜ問題なのかを学ぶ
- 重複コードを関数やメソッドに抽出する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜCollectionメソッドの後に『DRY原則の深掘り』を行うのか？」

基本的なリファクタリングを学んだら、次は「DRY原則の深掘り」です。

---

### 理由1: より高度な重複の発見

最初のDRYでは明らかな重複を解消しました。

ここでは、**構造的な重複**や**概念的な重複**を見つけて解消します。

---

### 理由2: 抽象化のレベルを上げる

同じパターンのコードが複数箇所にある場合、**抽象化**して共通化できます。

```php
// 抽象化前
if ($task->status === 'completed') { ... }
if ($task->status === 'pending') { ... }

// 抽象化後
if ($task->isCompleted()) { ... }
if ($task->isPending()) { ... }
```

---

### 理由3: 保守性の向上

DRY原則を徹底すると、**変更が1箇所で済む**ようになります。

バグ修正や機能追加が楽になります。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | 重複コードの問題点を理解 | なぜ削除が必要か |
| Step 2 | メソッドに抽出 | 重複を1箇所にまとめる |
| Step 3 | バリデーションの重複を解消 | フォームリクエストを使う |
| Step 4 | ビューの重複を解消 | パーシャルを使う |

> 💡 **ポイント**: 過度な抽象化は逆効果です。2〜3回同じパターンが出てきたら抽象化を検討しましょう。

---

## Step 1: 重複コードの問題点を理解する

### 1-1. 重複コードの例

以下のコードは、重複コードがあります。

```php
public function index()
{
    $tasks = Task::where('user_id', auth()->id())
        ->where('status', 'pending')
        ->orderBy('created_at', 'desc')
        ->get();
    
    return view('tasks.index', compact('tasks'));
}

public function completed()
{
    $tasks = Task::where('user_id', auth()->id())
        ->where('status', 'completed')
        ->orderBy('created_at', 'desc')
        ->get();
    
    return view('tasks.completed', compact('tasks'));
}
```

---

### 1-2. 問題点

| 問題 | 説明 |
|------|------|
| 重複 | `where('user_id', auth()->id())`が重複している |
| 重複 | `orderBy('created_at', 'desc')`が重複している |
| 修正コスト | 修正する場合、2箇所を修正する必要がある |
| バグリスク | 修正漏れが発生しやすい |

---

## Step 2: メソッドに抽出する

### 2-1. プライベートメソッドに抽出

重複コードをメソッドに抽出します。

```php
public function index()
{
    $tasks = $this->getUserTasks('pending');
    return view('tasks.index', compact('tasks'));
}

public function completed()
{
    $tasks = $this->getUserTasks('completed');
    return view('tasks.completed', compact('tasks'));
}

private function getUserTasks($status)
{
    return Task::where('user_id', auth()->id())
        ->where('status', $status)
        ->orderBy('created_at', 'desc')
        ->get();
}
```

**改善点**:

- 重複コードが削除された
- 修正する場合、1箇所を修正すればよい

---

### 2-2. Eloquentスコープを使う

さらに改善するには、Eloquentスコープを使います。

**ファイル**: `app/Models/Task.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Task extends Model
{
    public function scopeForUser($query, $userId)
    {
        return $query->where('user_id', $userId);
    }

    public function scopeWithStatus($query, $status)
    {
        return $query->where('status', $status);
    }

    public function scopeLatestFirst($query)
    {
        return $query->orderBy('created_at', 'desc');
    }
}
```

---

### 2-3. スコープを使ったコントローラー

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function index()
{
    $tasks = Task::forUser(auth()->id())
        ->withStatus('pending')
        ->latestFirst()
        ->get();
    
    return view('tasks.index', compact('tasks'));
}

public function completed()
{
    $tasks = Task::forUser(auth()->id())
        ->withStatus('completed')
        ->latestFirst()
        ->get();
    
    return view('tasks.completed', compact('tasks'));
}
```

スコープを使うことで、コードが読みやすくなりました。

---

## Step 3: バリデーションの重複を解消する

### 3-1. 重複するバリデーションルール

以下のコードは、重複するバリデーションルールがあります。

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
    ]);
    
    // ...
}

public function update(Request $request, Task $task)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
    ]);
    
    // ...
}
```

---

### 3-2. フォームリクエストを作成する

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
            'title' => 'required|max:255',
            'description' => 'nullable',
            'status' => 'required|in:pending,in_progress,completed',
        ];
    }
}
```

---

### 3-3. フォームリクエストを使ったコントローラー

**ファイル**: `app/Http/Controllers/TaskController.php`

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

バリデーションルールが1箇所にまとまりました。

---

## Step 4: ビューの重複を解消する

### 4-1. 重複するビューのコード

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<table>
    <thead>
        <tr>
            <th>タイトル</th>
            <th>ステータス</th>
            <th>作成日</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($tasks as $task)
        <tr>
            <td>{{ $task->title }}</td>
            <td>{{ $task->status }}</td>
            <td>{{ $task->created_at->format('Y-m-d') }}</td>
        </tr>
        @endforeach
    </tbody>
</table>
```

**ファイル**: `resources/views/tasks/completed.blade.php`

```blade
<table>
    <thead>
        <tr>
            <th>タイトル</th>
            <th>ステータス</th>
            <th>作成日</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($tasks as $task)
        <tr>
            <td>{{ $task->title }}</td>
            <td>{{ $task->status }}</td>
            <td>{{ $task->created_at->format('Y-m-d') }}</td>
        </tr>
        @endforeach
    </tbody>
</table>
```

---

### 4-2. パーシャルに抽出する

**ファイル**: `resources/views/tasks/_table.blade.php`

```blade
<table>
    <thead>
        <tr>
            <th>タイトル</th>
            <th>ステータス</th>
            <th>作成日</th>
        </tr>
    </thead>
    <tbody>
        @foreach ($tasks as $task)
        <tr>
            <td>{{ $task->title }}</td>
            <td>{{ $task->status }}</td>
            <td>{{ $task->created_at->format('Y-m-d') }}</td>
        </tr>
        @endforeach
    </tbody>
</table>
```

---

### 4-3. パーシャルを使用する

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<h1>タスク一覧</h1>
@include('tasks._table')
```

**ファイル**: `resources/views/tasks/completed.blade.php`

```blade
<h1>完了したタスク</h1>
@include('tasks._table')
```

ビューの重複が解消されました。

---

### 4-4. 実践演習

以下のコードから重複を削除してください。

```php
public function sendWelcomeEmail($user)
{
    $subject = 'Welcome to our app!';
    $message = 'Thank you for registering.';
    Mail::to($user->email)->send(new WelcomeEmail($subject, $message));
}

public function sendPasswordResetEmail($user)
{
    $subject = 'Password Reset';
    $message = 'Click here to reset your password.';
    Mail::to($user->email)->send(new PasswordResetEmail($subject, $message));
}
```

**解答例**:

```php
public function sendWelcomeEmail($user)
{
    $this->sendEmail($user, 'Welcome to our app!', 'Thank you for registering.', WelcomeEmail::class);
}

public function sendPasswordResetEmail($user)
{
    $this->sendEmail($user, 'Password Reset', 'Click here to reset your password.', PasswordResetEmail::class);
}

private function sendEmail($user, $subject, $message, $mailClass)
{
    Mail::to($user->email)->send(new $mailClass($subject, $message));
}
```

---

## 🚨 よくある間違い

### 間違い1: 過度な抽象化

**問題**: 重複コードを削除しすぎると、コードが読みにくくなる

**対処法**: 適度な抽象化を心がけます。3回ルール（同じコードが3回出てきたら抽出）を参考にしましょう。

---

### 間違い2: 似ているが異なるコードを無理に統合する

**問題**: 似ているが異なるコードを無理に統合すると、複雑になる

**対処法**: 本当に同じコードだけを抽出します。

---

### 間違い3: 抽出したメソッドの名前が曖昧

**問題**: `process()`や`handle()`など、何をするか分からない名前

**対処法**: 具体的な名前をつけます（例：`getUserTasks()`、`sendNotificationEmail()`）

---

## 💡 TIP: 3回ルール

**3回ルール**は、**同じコードが3回出てきたら、抽出を検討する**というルールです。

- 1回目: そのまま書く
- 2回目: 少し気になるが、そのまま書く
- 3回目: 抽出を検討する

---

## ✨ まとめ

このセクションでは、重複コードの削除を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | 重複コードの問題点を理解 |
| Step 2 | メソッドに抽出、Eloquentスコープを使用 |
| Step 3 | フォームリクエストでバリデーションを共通化 |
| Step 4 | パーシャルでビューを共通化 |

次のセクションでは、フォームリクエストクラスについて詳しく学びます。

---
