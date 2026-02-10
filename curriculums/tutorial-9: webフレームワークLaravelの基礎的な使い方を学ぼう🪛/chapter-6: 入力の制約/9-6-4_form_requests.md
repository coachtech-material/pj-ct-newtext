# Tutorial 9-6-4: フォームリクエスト

## 🎯 このセクションで学ぶこと

*   フォームリクエストを使って、バリデーションロジックをコントローラーから分離する方法を理解する。
*   `authorize()`メソッドを使った認可ロジックの実装方法を理解する。
*   フォームリクエストのカスタマイズ方法を理解する。

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

**フォームリクエストの生成**

```bash
sail artisan make:request StorePostRequest
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

**コントローラーでの使用**

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

**例1: ログインユーザーのみ許可**

```php
public function authorize()
{
    return Auth::check();
}
```

**例2: 自分の投稿のみ更新を許可**

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

**`messages()`メソッド**

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

**`attributes()`メソッド**

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

ユーザー登録フォームのバリデーションをフォームリクエストで実装する例です。

**フォームリクエストの生成**

```bash
sail artisan make:request RegisterRequest
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

**コードリーディング（フォームリクエスト）**：

| コード | 説明 |
|:---|:---|
| `class RegisterRequest extends FormRequest` | `FormRequest`を継承したカスタムリクエストクラスです |
| `public function authorize()` | リクエストの認可を判定します。`true`で許可、`false`で403エラー |
| `return true;` | ユーザー登録は誰でも可能なので、常に`true`を返します |
| `public function rules()` | バリデーションルールを配列で返します |
| `Password::min(8)->letters()->numbers()` | パスワードルールオブジェクト。8文字以上、英字と数字を含む |
| `public function messages()` | カスタムエラーメッセージを定義します |
| `'email.unique' => '...'` | `フィールド名.ルール名`の形式でメッセージを指定します |

**構文解説**：

```php
'password' => ['required', 'confirmed', Password::min(8)
    ->letters()
    ->numbers()],
```
→ 配列形式でルールを指定しています。`Password::min(8)`はパスワードルールオブジェクトで、メソッドチェーンで条件を追加できます。`letters()`は英字を含むこと、`numbers()`は数字を含むことを要求します。

```php
'email.unique' => 'このメールアドレスは既に登録されています。',
```
→ `messages()`メソッドでは、`フィールド名.ルール名`の形式でカスタムメッセージを指定します。この場合、`email`フィールドの`unique`ルールに対するメッセージです。

**コントローラー**

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

**コードリーディング（コントローラー）**：

| コード | 説明 |
|:---|:---|
| `RegisterRequest $request` | 型ヒントでフォームリクエストを注入。自動的にバリデーションが実行されます |
| `$request->validated()` | バリデーション済みのデータのみを取得します |
| `Hash::make($validated['password'])` | パスワードをハッシュ化してから保存します |
| `$validated['phone'] ?? null` | null合体演算子。phoneがnullの場合はnullを使用します |
| `Auth::login($user)` | 作成したユーザーでログイン状態にします |

**処理の流れ**：

```
1. RegisterRequestがコントローラーに注入される
    ↓
2. Laravelが自動的にauthorize()を実行
   - falseの場合: 403 Forbiddenエラー
   - trueの場合: 次へ進む
    ↓
3. Laravelが自動的にrules()のバリデーションを実行
   - 失敗の場合: 自動的にリダイレクトし、エラーメッセージを表示
   - 成功の場合: コントローラーのメソッドが実行される
    ↓
4. $request->validated()でバリデーション済みデータを取得
    ↓
5. ユーザーを作成し、ログイン状態にする
    ↓
6. ダッシュボードにリダイレクト
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

### 🚀 実践例2: 条件付きバリデーション

フォームの入力内容に応じて、バリデーションルールを動的に変更する例です。

**フォームリクエスト**

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class ContactRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        $rules = [
            'name' => 'required|string|max:255',
            'email' => 'required|email',
            'is_company' => 'required|boolean',
        ];

        if ($this->is_company) {
            $rules['company_name'] = 'required|string|max:255';
            $rules['company_address'] = 'required|string';
        }

        return $rules;
    }

    public function messages()
    {
        return [
            'company_name.required' => '法人の場合、会社名は必須です。',
            'company_address.required' => '法人の場合、会社住所は必須です。',
        ];
    }
}
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `$rules = [...]` | 基本のバリデーションルールを配列で定義します |
| `if ($this->is_company)` | リクエストの`is_company`フィールドの値をチェックします |
| `$this->is_company` | フォームリクエスト内では`$this`でリクエストデータにアクセスできます |
| `$rules['company_name'] = '...'` | 条件に応じてルールを動的に追加します |
| `return $rules;` | 最終的なルール配列を返します |

**構文解説**：

```php
if ($this->is_company) {
    $rules['company_name'] = 'required|string|max:255';
    $rules['company_address'] = 'required|string';
}
```
→ `$this->is_company`でリクエストデータにアクセスしています。フォームリクエストクラス内では、`$this`を使ってリクエストのフィールド値を直接参照できます。`is_company`が`true`の場合のみ、`company_name`と`company_address`のルールが追加されます。

**処理の流れ**：

```
1. 基本ルール（name, email, is_company）を定義
    ↓
2. is_companyの値をチェック
   - trueの場合: company_nameとcompany_addressのルールを追加
   - falseの場合: 追加なし
    ↓
3. 最終的なルール配列を返す
    ↓
4. Laravelがルールに基づいてバリデーションを実行
```

**条件付きバリデーションの使用場面**：

| 場面 | 例 |
|:---|:---|
| 法人/個人の切り替え | 法人の場合のみ会社情報を必須にする |
| 配送方法の選択 | 配送の場合のみ住所を必須にする |
| 支払い方法の選択 | クレジットカードの場合のみカード情報を必須にする |

---

### 🚨 よくある間違い

**間違い1: `authorize()`で`false`を返すとエラーになる**

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

**間違い2: `validated()`を使わずに`all()`を使う**

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
*   条件付きバリデーションを使って、動的にルールを変更できる。

---
