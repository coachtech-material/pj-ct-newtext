# Tutorial 11-5-7: リクエストクラスの活用

## 🎯 このセクションで学ぶこと

*   コントローラーにバリデーションを書く問題点を理解する。
*   フォームリクエストを使って、バリデーションロジックを分離する方法を学ぶ。
*   カスタムエラーメッセージの設定方法を学ぶ。
*   認可処理をリクエストクラスに書く方法を学ぶ。

---

## 導入：なぜリクエストクラスを使うのか

**バリデーション**をコントローラーに書くと、**コントローラーが肥大化**します。

**フォームリクエスト**を使うと、**バリデーションロジックを分離**でき、**コントローラーをスリムに**保てます。

---

## 詳細解説

### 🔍 コントローラーにバリデーションを書く問題点

以下のコードは、コントローラーにバリデーションが書かれています。

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
        'priority' => 'required|integer|min:1|max:5',
    ]);
    
    $this->taskService->createTask($validated, auth()->id());
    
    return redirect()->route('tasks.index');
}

public function update(Request $request, Task $task)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
        'priority' => 'required|integer|min:1|max:5',
    ]);
    
    $this->taskService->updateTask($task, $validated);
    
    return redirect()->route('tasks.index');
}
```

**問題点**:
*   バリデーションルールが重複している
*   コントローラーが肥大化している

---

### 🔍 フォームリクエストを作成する

フォームリクエストを作成して、バリデーションロジックを分離します。

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
            'priority' => 'required|integer|min:1|max:5',
        ];
    }
}
```

---

### 🔍 コントローラーでフォームリクエストを使う

コントローラーで、フォームリクエストを使います。

```php
use App\Http\Requests\TaskRequest;

public function store(TaskRequest $request)
{
    $validated = $request->validated();
    $this->taskService->createTask($validated, auth()->id());
    return redirect()->route('tasks.index');
}

public function update(TaskRequest $request, Task $task)
{
    $validated = $request->validated();
    $this->taskService->updateTask($task, $validated);
    return redirect()->route('tasks.index');
}
```

**改善点**:
*   バリデーションルールが1箇所にまとまった
*   コントローラーがスリムになった

---

### 🔍 カスタムエラーメッセージを設定する

フォームリクエストで、カスタムエラーメッセージを設定できます。

```php
public function messages()
{
    return [
        'title.required' => 'タイトルは必須です。',
        'title.max' => 'タイトルは255文字以内で入力してください。',
        'status.required' => 'ステータスは必須です。',
        'status.in' => 'ステータスは「未着手」「進行中」「完了」のいずれかを選択してください。',
        'priority.required' => '優先度は必須です。',
        'priority.integer' => '優先度は整数で入力してください。',
        'priority.min' => '優先度は1以上で入力してください。',
        'priority.max' => '優先度は5以下で入力してください。',
    ];
}
```

---

### 🔍 属性名をカスタマイズする

フォームリクエストで、属性名をカスタマイズできます。

```php
public function attributes()
{
    return [
        'title' => 'タイトル',
        'description' => '説明',
        'status' => 'ステータス',
        'priority' => '優先度',
    ];
}
```

これにより、エラーメッセージが「titleは必須です。」ではなく、「タイトルは必須です。」になります。

---

### 🔍 認可処理をリクエストクラスに書く

フォームリクエストで、認可処理を書けます。

```php
public function authorize()
{
    $task = $this->route('task');
    
    // タスクの所有者かどうかをチェック
    return $task && $task->user_id === auth()->id();
}
```

**ポイント**:
*   `authorize()`が`false`を返すと、403エラーが返される
*   認可処理をコントローラーに書く必要がなくなる

---

### 🔍 更新時と作成時でルールを変える

更新時と作成時でルールを変えたい場合は、以下のようにします。

```php
public function rules()
{
    $rules = [
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
        'priority' => 'required|integer|min:1|max:5',
    ];
    
    // 更新時は、タイトルの一意性をチェック（自分自身を除く）
    if ($this->isMethod('put') || $this->isMethod('patch')) {
        $rules['title'] = 'required|max:255|unique:tasks,title,' . $this->route('task')->id;
    }
    
    return $rules;
}
```

---

### 🔍 実践演習: フォームリクエストを作成してください

以下のコントローラーを、フォームリクエストを使ってリファクタリングしてください。

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'name' => 'required|max:255',
        'email' => 'required|email|unique:users',
        'password' => 'required|min:8|confirmed',
    ]);
    
    $this->userService->createUser($validated);
    
    return redirect()->route('users.index');
}
```

---

**解答例**:

```bash
php artisan make:request UserRequest
```

**ファイル**: `app/Http/Requests/UserRequest.php`

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UserRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'name' => 'required|max:255',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:8|confirmed',
        ];
    }

    public function messages()
    {
        return [
            'name.required' => '名前は必須です。',
            'email.required' => 'メールアドレスは必須です。',
            'email.email' => 'メールアドレスの形式が正しくありません。',
            'email.unique' => 'このメールアドレスは既に使用されています。',
            'password.required' => 'パスワードは必須です。',
            'password.min' => 'パスワードは8文字以上で入力してください。',
            'password.confirmed' => 'パスワードが一致しません。',
        ];
    }
}
```

**ファイル**: `app/Http/Controllers/UserController.php`

```php
use App\Http\Requests\UserRequest;

public function store(UserRequest $request)
{
    $validated = $request->validated();
    $this->userService->createUser($validated);
    return redirect()->route('users.index');
}
```

---

### 🔍 バリデーション後の処理を追加する

フォームリクエストで、バリデーション後の処理を追加できます。

```php
protected function passedValidation()
{
    // バリデーション成功後の処理
    $this->merge([
        'slug' => Str::slug($this->title),
    ]);
}
```

---

### 🔍 バリデーション前の処理を追加する

フォームリクエストで、バリデーション前の処理を追加できます。

```php
protected function prepareForValidation()
{
    // バリデーション前の処理
    $this->merge([
        'slug' => Str::slug($this->title),
    ]);
}
```

---

### 💡 TIP: 複数のフォームリクエストを使い分ける

作成用と更新用で、別々のフォームリクエストを作成することもできます。

*   `TaskStoreRequest`: 作成用
*   `TaskUpdateRequest`: 更新用

```bash
php artisan make:request TaskStoreRequest
php artisan make:request TaskUpdateRequest
```

---

### 🚨 よくある間違い

#### 間違い1: authorize()をfalseのままにする

`authorize()`が`false`のままだと、常に403エラーが返されます。

```php
public function authorize()
{
    return true;  // trueに変更する
}
```

---

#### 間違い2: validated()を使わない

`$request->all()`を使うと、バリデーションされていないデータも含まれます。

```php
// ❌ 間違い
$data = $request->all();

// ✅ 正しい
$data = $request->validated();
```

---

#### 間違い3: messages()を書きすぎる

すべてのエラーメッセージをカスタマイズする必要はありません。

必要なものだけをカスタマイズします。

---

## ✨ まとめ

このセクションでは、リクエストクラスの活用を学びました。

*   フォームリクエストを使って、バリデーションロジックを分離した。
*   カスタムエラーメッセージを設定した。
*   認可処理をリクエストクラスに書いた。

次のセクションでは、Eloquentスコープの活用について学びます。

---

## 📝 学習のポイント

- [ ] フォームリクエストを作成した。
- [ ] カスタムエラーメッセージを設定した。
- [ ] 認可処理をリクエストクラスに書いた。
- [ ] validated()を使った。
