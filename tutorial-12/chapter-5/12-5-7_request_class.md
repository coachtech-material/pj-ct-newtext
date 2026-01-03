# Tutorial 12-5-7: リクエストクラスの活用

## 🎯 このセクションで学ぶこと

- コントローラーにバリデーションを書く問題点を理解する
- フォームリクエストを使って、バリデーションロジックを分離する方法を学ぶ
- カスタムエラーメッセージの設定方法を学ぶ
- 認可処理をリクエストクラスに書く方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜDRYの後に『Form Request』を実装するのか？」

DRY原則を学んだら、次は「Form Request」です。

---

### 理由1: コントローラーのバリデーションを分離

コントローラーのバリデーションは、**最も簡単にリファクタリングできる**部分です。

```php
// リファクタリング前（コントローラー内）
$validated = $request->validate([
    'title' => 'required|max:255',
    'description' => 'nullable',
]);

// リファクタリング後（Form Request）
public function store(TaskRequest $request)
{
    $validated = $request->validated();
}
```

---

### 理由2: 再利用性の向上

同じバリデーションルールを複数のアクションで使う場合、**Form Requestで共通化**できます。

---

### 理由3: 単一責任の原則

コントローラーは「リクエストを受けてレスポンスを返す」ことに集中すべきです。

バリデーションは**Form Requestの責任**として分離します。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | 問題点を理解 | なぜ分離が必要か |
| Step 2 | Form Request作成 | バリデーションを分離 |
| Step 3 | カスタムメッセージ設定 | ユーザーフレンドリーに |
| Step 4 | 認可処理を追加 | セキュリティ強化 |

> 💡 **ポイント**: Form Requestでは`authorize()`メソッドで認可チェックも行えます。

---

## Step 1: コントローラーにバリデーションを書く問題点

### 1-1. 問題のあるコード

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

---

### 1-2. 問題点

| 問題 | 説明 |
|------|------|
| 重複 | バリデーションルールが重複している |
| 肥大化 | コントローラーが肥大化している |
| 保守性 | ルール変更時に複数箇所を修正する必要がある |

---

## Step 2: フォームリクエストを作成する

### 2-1. フォームリクエストを生成する

```bash
php artisan make:request TaskRequest
```

---

### 2-2. バリデーションルールを移動する

**ファイル**: `app/Http/Requests/TaskRequest.php`

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class TaskRequest extends FormRequest
{
    /**
     * リクエストの認可を判定する
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * バリデーションルールを定義する
     */
    public function rules(): array
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

### 2-3. コントローラーでフォームリクエストを使う

**ファイル**: `app/Http/Controllers/TaskController.php`

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

---

### 2-4. 改善点

| 改善 | 説明 |
|------|------|
| 重複解消 | バリデーションルールが1箇所にまとまった |
| スリム化 | コントローラーがスリムになった |
| 保守性向上 | ルール変更が1箇所で済む |

---

## Step 3: カスタムエラーメッセージを設定する

### 3-1. messages()メソッドを追加する

```php
/**
 * カスタムエラーメッセージを定義する
 */
public function messages(): array
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

### 3-2. attributes()メソッドで属性名をカスタマイズする

```php
/**
 * 属性名をカスタマイズする
 */
public function attributes(): array
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

## Step 4: 認可処理をリクエストクラスに書く

### 4-1. authorize()メソッドで認可チェック

```php
/**
 * リクエストの認可を判定する
 */
public function authorize(): bool
{
    // 更新時のみ所有者チェック
    if ($this->route('task')) {
        $task = $this->route('task');
        return $task->user_id === auth()->id();
    }
    
    // 作成時は常に許可
    return true;
}
```

**ポイント**:

- `authorize()`が`false`を返すと、403エラーが返される
- 認可処理をコントローラーに書く必要がなくなる

---

### 4-2. 更新時と作成時でルールを変える

```php
public function rules(): array
{
    $rules = [
        'title' => 'required|max:255',
        'description' => 'nullable',
        'status' => 'required|in:pending,in_progress,completed',
        'priority' => 'required|integer|min:1|max:5',
    ];
    
    // 更新時は、タイトルの一意性をチェック（自分自身を除く）
    if ($this->isMethod('put') || $this->isMethod('patch')) {
        $taskId = $this->route('task')->id;
        $rules['title'] = 'required|max:255|unique:tasks,title,' . $taskId;
    }
    
    return $rules;
}
```

---

### 4-3. バリデーション前後の処理

```php
/**
 * バリデーション前の処理
 */
protected function prepareForValidation(): void
{
    // 入力値を整形
    $this->merge([
        'title' => trim($this->title),
    ]);
}

/**
 * バリデーション成功後の処理
 */
protected function passedValidation(): void
{
    // スラッグを自動生成
    $this->merge([
        'slug' => Str::slug($this->title),
    ]);
}
```

---

### 4-4. 実践演習

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
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'name' => 'required|max:255',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:8|confirmed',
        ];
    }

    public function messages(): array
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

---

## 🚨 よくある間違い

### 間違い1: authorize()をfalseのままにする

**問題**: `authorize()`が`false`のままだと、常に403エラーが返される

```php
// ❌ 間違い
public function authorize(): bool
{
    return false;
}

// ✅ 正しい
public function authorize(): bool
{
    return true;
}
```

---

### 間違い2: validated()を使わない

**問題**: `$request->all()`を使うと、バリデーションされていないデータも含まれる

```php
// ❌ 間違い
$data = $request->all();

// ✅ 正しい
$data = $request->validated();
```

---

### 間違い3: messages()を書きすぎる

**問題**: すべてのエラーメッセージをカスタマイズすると、保守が大変

**対処法**: 必要なものだけをカスタマイズします。`attributes()`を使えば、多くのメッセージは自動的に日本語化されます。

---

## 💡 TIP: 複数のフォームリクエストを使い分ける

作成用と更新用で、別々のフォームリクエストを作成することもできます。

```bash
php artisan make:request TaskStoreRequest
php artisan make:request TaskUpdateRequest
```

- `TaskStoreRequest`: 作成用（パスワード必須など）
- `TaskUpdateRequest`: 更新用（パスワードは任意など）

---

## ✨ まとめ

このセクションでは、リクエストクラスの活用を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | コントローラーにバリデーションを書く問題点 |
| Step 2 | フォームリクエストの作成と使用 |
| Step 3 | カスタムエラーメッセージの設定 |
| Step 4 | 認可処理とルールの動的変更 |

次のセクションでは、コードの可読性について学びます。

---
