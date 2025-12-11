# Tutorial 11-5-5: 重複コードの削除

## 🎯 このセクションで学ぶこと

*   DRY原則（Don't Repeat Yourself）とは何かを理解する。
*   重複コードが、なぜ問題なのかを学ぶ。
*   重複コードを関数やメソッドに抽出する方法を学ぶ。

---

## 導入：なぜ重複コードを削除するのか

**DRY原則（Don't Repeat Yourself）**は、**同じコードを繰り返し書かない**という原則です。

重複コードがあると、**修正が大変**になり、**バグが発生しやすく**なります。

---

## 詳細解説

### 🔍 重複コードの問題点

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

**問題点**:
*   `where('user_id', auth()->id())`が重複している
*   `orderBy('created_at', 'desc')`が重複している
*   修正する場合、2箇所を修正する必要がある

---

### 🔍 メソッドに抽出する

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
*   重複コードが削除された
*   修正する場合、1箇所を修正すればよい

---

### 🔍 Eloquentスコープを使う

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

    public function scopeLatest($query)
    {
        return $query->orderBy('created_at', 'desc');
    }
}
```

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
public function index()
{
    $tasks = Task::forUser(auth()->id())
        ->withStatus('pending')
        ->latest()
        ->get();
    
    return view('tasks.index', compact('tasks'));
}

public function completed()
{
    $tasks = Task::forUser(auth()->id())
        ->withStatus('completed')
        ->latest()
        ->get();
    
    return view('tasks.completed', compact('tasks'));
}
```

---

### 🔍 重複するバリデーションルール

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

### 🔍 フォームリクエストに抽出する

重複するバリデーションルールを、フォームリクエストに抽出します。

```bash
php artisan make:request TaskRequest
```

**ファイル**: `app/Http/Requests/TaskRequest.php`

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class TaskRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'title' => 'required|max:255',
            'description' => 'nullable',
            'status' => 'required|in:pending,in_progress,completed',
        ];
    }
}
```

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

---

### 🔍 重複するビューのコード

以下のコードは、重複するビューのコードがあります。

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

### 🔍 パーシャルに抽出する

重複するビューのコードを、パーシャルに抽出します。

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

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
@include('tasks._table')
```

**ファイル**: `resources/views/tasks/completed.blade.php`

```blade
@include('tasks._table')
```

---

### 🔍 実践演習: 以下のコードから重複を削除してください

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

### 💡 TIP: 3回ルール

**3回ルール**は、**同じコードが3回出てきたら、抽出を検討する**というルールです。

---

### 🚨 よくある間違い

#### 間違い1: 過度な抽象化

重複コードを削除しすぎると、コードが読みにくくなります。

**対処法**: 適度な抽象化を心がけます。

---

#### 間違い2: 似ているが異なるコードを無理に統合する

似ているが異なるコードを無理に統合すると、複雑になります。

**対処法**: 本当に同じコードだけを抽出します。

---

## ✨ まとめ

このセクションでは、重複コードの削除を学びました。

*   DRY原則を理解した。
*   重複コードをメソッドに抽出した。
*   Eloquentスコープを使った。
*   フォームリクエストを使った。

次のセクションでは、サービスクラスの導入とDIについて学びます。

---

## 📝 学習のポイント

- [ ] DRY原則を理解した。
- [ ] 重複コードの問題点を理解した。
- [ ] メソッドに抽出した。
- [ ] Eloquentスコープを使った。
