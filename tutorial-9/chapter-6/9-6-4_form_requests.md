# Tutorial 9-6-4: フォームリクエスト

## 🎯 このセクションで学ぶこと

*   フォームリクエストを使って、バリデーションロジックをコントローラーから分離できるようになる。
*   `authorize()`メソッドを使って、認可ロジックを実装できるようになる。
*   フォームリクエストのカスタマイズ方法を学ぶ。

---

## 導入：「コントローラー」が太りすぎている

これまで、コントローラーの中で`$request->validate()`を使ってバリデーションを実装してきました。しかし、バリデーションルールが複雑になると、**コントローラーが太りすぎてしまいます**。

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'content' => 'required|string',
        'category_id' => 'required|exists:categories,id',
        'tags' => 'nullable|array',
        'tags.*' => 'exists:tags,id',
        'is_published' => 'required|boolean',
        'published_at' => 'required_if:is_published,true|date|after:now',
        'thumbnail' => 'nullable|image|max:5120',
    ]); // コントローラーが長くなる

    // 実際の処理
    $post = Auth::user()->posts()->create($validated);
    
    return redirect('/posts/' . $post->id);
}
```

Laravelでは、**フォームリクエスト**を使うことで、バリデーションロジックをコントローラーから分離できます。

---

## 詳細解説

### 🔧 フォームリクエストの作成

#### ステップ1: フォームリクエストを生成

```bash
php artisan make:request StorePostRequest
```

**`app/Http/Requests/StorePostRequest.php`**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StorePostRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'title' => 'required|string|max:255',
            'content' => 'required|string',
            'category_id' => 'required|exists:categories,id',
            'tags' => 'nullable|array',
            'tags.*' => 'exists:tags,id',
            'is_published' => 'required|boolean',
            'published_at' => 'required_if:is_published,true|date|after:now',
            'thumbnail' => 'nullable|image|max:5120',
        ];
    }
}
```

**メソッド**

*   `authorize()`: このリクエストを実行する権限があるかを判定
*   `rules()`: バリデーションルールを定義

---

#### ステップ2: コントローラーで使用

```php
use App\Http\Requests\StorePostRequest;

public function store(StorePostRequest $request)
{
    $validated = $request->validated();

    $post = Auth::user()->posts()->create($validated);
    
    return redirect('/posts/' . $post->id);
}
```

**コードリーディング**

*   `StorePostRequest $request`: 型ヒントを使って、フォームリクエストを注入
*   `$request->validated()`: バリデーション済みのデータを取得
*   バリデーションが失敗すると、自動的にリダイレクトされる

---

### 🔐 `authorize()`メソッド

`authorize()`メソッドを使うことで、**認可ロジック**を実装できます。

#### 例1: ログインユーザーのみ許可

```php
public function authorize()
{
    return Auth::check();
}
```

#### 例2: 自分の投稿のみ更新を許可

```php
public function authorize()
{
    $post = Post::findOrFail($this->route('post'));
    return $post->user_id === Auth::id();
}
```

**`$this->route('post')`**: ルートパラメータを取得

---

### 📝 エラーメッセージのカスタマイズ

#### `messages()`メソッド

```php
public function messages()
{
    return [
        'title.required' => 'タイトルは必須です。',
        'title.max' => 'タイトルは255文字以内で入力してください。',
        'content.required' => '本文は必須です。',
    ];
}
```

---

#### `attributes()`メソッド

```php
public function attributes()
{
    return [
        'title' => 'タイトル',
        'content' => '本文',
        'category_id' => 'カテゴリー',
    ];
}
```

これにより、エラーメッセージが「The title field is required.」から「タイトルは必須です。」に変わります。

---

### 🚀 実践例1: ユーザー登録

#### フォームリクエスト

```bash
php artisan make:request RegisterRequest
```

**`app/Http/Requests/RegisterRequest.php`**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rules\Password;

class RegisterRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'name' => 'required|string|max:255',
            'email' => 'required|email|unique:users',
            'password' => ['required', 'confirmed', Password::min(8)
                ->letters()
                ->numbers()],
            'birth_date' => 'required|date|before:today',
            'phone' => 'nullable|regex:/^[0-9]{10,11}$/',
        ];
    }

    public function messages()
    {
        return [
            'name.required' => '名前は必須です。',
            'email.required' => 'メールアドレスは必須です。',
            'email.unique' => 'このメールアドレスは既に登録されています。',
            'password.required' => 'パスワードは必須です。',
        ];
    }
}
```

#### コントローラー

```php
use App\Http\Requests\RegisterRequest;

public function register(RegisterRequest $request)
{
    $validated = $request->validated();

    $user = User::create([
        'name' => $validated['name'],
        'email' => $validated['email'],
        'password' => Hash::make($validated['password']),
        'birth_date' => $validated['birth_date'],
        'phone' => $validated['phone'] ?? null,
    ]);

    Auth::login($user);

    return redirect('/dashboard');
}
```

---

### 🚀 実践例2: 投稿の更新

#### フォームリクエスト

```bash
php artisan make:request UpdatePostRequest
```

**`app/Http/Requests/UpdatePostRequest.php`**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UpdatePostRequest extends FormRequest
{
    public function authorize()
    {
        $post = Post::findOrFail($this->route('post'));
        return $post->user_id === Auth::id();
    }

    public function rules()
    {
        return [
            'title' => 'required|string|max:255',
            'content' => 'required|string',
            'category_id' => 'required|exists:categories,id',
            'tags' => 'nullable|array',
            'tags.*' => 'exists:tags,id',
            'is_published' => 'required|boolean',
        ];
    }
}
```

#### コントローラー

```php
use App\Http\Requests\UpdatePostRequest;

public function update(UpdatePostRequest $request, $id)
{
    $post = Post::findOrFail($id);
    
    $post->update($request->validated());
    
    if ($request->has('tags')) {
        $post->tags()->sync($request->tags);
    }

    return redirect('/posts/' . $post->id);
}
```

---

### 💡 TIP: `prepareForValidation()`

バリデーション前に、データを加工することができます。

```php
protected function prepareForValidation()
{
    $this->merge([
        'slug' => Str::slug($this->title),
    ]);
}
```

---

### 💡 TIP: `passedValidation()`

バリデーション後に、追加の処理を実行できます。

```php
protected function passedValidation()
{
    $this->merge([
        'user_id' => Auth::id(),
    ]);
}
```

---

### 💡 TIP: カスタムルールを使う

```php
use App\Rules\NoForbiddenWords;

public function rules()
{
    return [
        'comment' => ['required', 'string', new NoForbiddenWords],
    ];
}
```

---

### 🚀 実践例3: 条件付きバリデーション

#### フォームリクエスト

```php
public function rules()
{
    $rules = [
        'name' => 'required|string|max:255',
        'email' => 'required|email',
    ];

    if ($this->is_company) {
        $rules['company_name'] = 'required|string|max:255';
        $rules['company_address'] = 'required|string';
    }

    return $rules;
}
```

---

### 🚨 よくある間違い

#### 間違い1: `authorize()`で`false`を返すとエラーになる

```php
public function authorize()
{
    return false; // 403 Forbiddenエラーになる
}
```

**対処法**: 認可が不要な場合は、`true`を返します。

```php
public function authorize()
{
    return true;
}
```

---

#### 間違い2: `validated()`を使わずに`all()`を使う

```php
$data = $request->all(); // NG: バリデーションされていないデータも含まれる
```

**対処法**: `validated()`を使います。

```php
$data = $request->validated(); // OK: バリデーション済みのデータのみ
```

---

## ✨ まとめ

このセクションでは、フォームリクエストを使って、バリデーションロジックをコントローラーから分離する方法を学びました。

*   フォームリクエストを使うことで、コントローラーをシンプルに保てる。
*   `authorize()`メソッドを使って、認可ロジックを実装できる。
*   `messages()`や`attributes()`を使って、エラーメッセージをカスタマイズできる。
*   `prepareForValidation()`や`passedValidation()`を使って、バリデーション前後の処理を実装できる。

これで、Chapter 6「バリデーション」の全4セクションが完了しました。次は、Chapter 7「認証機能」の残りのセクションに進みます。

---

## 📝 学習のポイント

- [ ] フォームリクエストを作成し、コントローラーで使用できる。
- [ ] `authorize()`メソッドを使って、認可ロジックを実装できる。
- [ ] `messages()`や`attributes()`を使って、エラーメッセージをカスタマイズできる。
- [ ] `prepareForValidation()`や`passedValidation()`を使える。
