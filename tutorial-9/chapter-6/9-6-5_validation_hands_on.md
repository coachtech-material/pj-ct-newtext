# Tutorial 9-6-5: バリデーション - ハンズオン演習

## 📝 このセクションの目的

Chapter 6で学んだバリデーションを実際に手を動かして確認します。フォームリクエストを使って、入力値の検証を実装しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 🎯 演習課題：ユーザー登録フォームのバリデーション

### 📋 要件

1. `StoreUserRequest`フォームリクエストを作成
2. 以下のバリデーションルールを設定：
   - name: 必須、最大50文字
   - email: 必須、メール形式、ユニーク
   - password: 必須、最小8文字、確認用と一致
3. エラーメッセージを日本語化

---

## 💡 ヒント

```bash
php artisan make:request StoreUserRequest
```

```php
public function rules()
{
    return [
        'name' => 'required|max:50',
        'email' => 'required|email|unique:users',
        'password' => 'required|min:8|confirmed',
    ];
}
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？バリデーションはデータの品質を保つために不可欠です。一緒に手を動かしながら、ユーザー登録フォームのバリデーションを実装していきましょう。

### 💭 実装の思考プロセス

バリデーションを実装する際、以下の順番で考えると効率的です：

1. **フォームリクエストを作成**：バリデーションロジックを分離
2. **バリデーションルールを定義**：必須、形式、ユニークなどのルールを設定
3. **エラーメッセージをカスタマイズ**：日本語でわかりやすく表示
4. **コントローラーで使用**：フォームリクエストをタイプヒントで指定
5. **ビューでエラー表示**：@errorディレクティブでエラーを表示

バリデーションのポイントは「フォームリクエストでバリデーションロジックを分離し、再利用性を高める」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: フォームリクエストを作成する

**何を考えているか**：
- 「バリデーションロジックをコントローラーから分離したい」
- 「フォームリクエストで再利用可能にしよう」
- 「Artisanコマンドで簡単に生成できる」

ターミナルで以下のコマンドを実行します：

```bash
php artisan make:request StoreUserRequest
```

**コマンド解説**：

```bash
php artisan make:request StoreUserRequest
```
→ `StoreUserRequest`フォームリクエストを生成します。`app/Http/Requests/StoreUserRequest.php`が作成されます。

---

#### ステップ2: バリデーションルールを定義する

**何を考えているか**：
- 「名前は必須で、50文字以内にしよう」
- 「メールは必須、メール形式、ユニークにしよう」
- 「パスワードは必須、8文字以上、確認用と一致させよう」

`app/Http/Requests/StoreUserRequest.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreUserRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'name' => 'required|max:50',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:8|confirmed',
        ];
    }
}
```

**コードリーディング**：

```php
public function authorize()
{
    return true;
}
```
→ `authorize`メソッドでリクエストの許可を制御します。`true`を返すと、すべてのユーザーがアクセスできます。

```php
public function rules()
{
    return [
        'name' => 'required|max:50',
        'email' => 'required|email|unique:users',
        'password' => 'required|min:8|confirmed',
    ];
}
```
→ `rules`メソッドでバリデーションルールを定義します。

```php
'name' => 'required|max:50',
```
→ 名前は必須で、最大50文字です。`|`で複数のルールを連結します。

```php
'email' => 'required|email|unique:users',
```
→ メールは必須、メール形式、`users`テーブルでユニークです。重複登録を防ぎます。

```php
'password' => 'required|min:8|confirmed',
```
→ パスワードは必須、最小8文字、確認用と一致します。`confirmed`は`password_confirmation`フィールドとの一致をチェックします。

---

#### ステップ3: エラーメッセージをカスタマイズする

**何を考えているか**：
- 「エラーメッセージを日本語で表示したい」
- 「ユーザーにわかりやすいメッセージを表示しよう」
- 「`messages`メソッドでカスタマイズできる」

`StoreUserRequest`に`messages`メソッドを追加します：

```php
public function messages()
{
    return [
        'name.required' => '名前は必須です',
        'name.max' => '名前は50文字以内で入力してください',
        'email.required' => 'メールアドレスは必須です',
        'email.email' => 'メールアドレスの形式が正しくありません',
        'email.unique' => 'このメールアドレスは既に使用されています',
        'password.required' => 'パスワードは必須です',
        'password.min' => 'パスワードは8文字以上で入力してください',
        'password.confirmed' => 'パスワードが一致しません',
    ];
}
```

**コードリーディング**：

```php
public function messages()
```
→ `messages`メソッドでカスタムエラーメッセージを定義します。

```php
'name.required' => '名前は必須です',
```
→ `フィールド名.ルール名`の形式でメッセージを指定します。各フィールドとルールの組み合わせごとにメッセージをカスタマイズできます。

---

#### ステップ4: コントローラーで使用する

**何を考えているか**：
- 「コントローラーでフォームリクエストを使いたい」
- 「タイプヒントで指定するだけで自動的にバリデーションされる」
- 「`validated()`で検証済みデータだけを取得しよう」

`UserController`に`store`メソッドを実装します：

```php
use App\Http\Requests\StoreUserRequest;
use App\Models\User;

public function store(StoreUserRequest $request)
{
    User::create($request->validated());
    return redirect('/users');
}
```

**コードリーディング**：

```php
public function store(StoreUserRequest $request)
```
→ タイプヒントで`StoreUserRequest`を指定します。Laravelが自動的にバリデーションを実行し、失敗するとエラーを返します。

```php
User::create($request->validated());
```
→ `validated()`で検証済みのデータだけを取得します。不正なデータが混入するのを防ぎます。

---

#### ステップ5: ビューでエラー表示する

**何を考えているか**：
- 「バリデーションエラーをユーザーに表示したい」
- 「@errorディレクティブで簡単に表示できる」
- 「old()ヘルパーで入力値を保持しよう」

`resources/views/register.blade.php`を作成します：

```blade
<form action="{{ route('users.store') }}" method="POST">
    @csrf
    <div>
        <label>名前</label>
        <input type="text" name="name" value="{{ old('name') }}">
        @error('name')
            <p class="error">{{ $message }}</p>
        @enderror
    </div>
    <div>
        <label>メールアドレス</label>
        <input type="email" name="email" value="{{ old('email') }}">
        @error('email')
            <p class="error">{{ $message }}</p>
        @enderror
    </div>
    <div>
        <label>パスワード</label>
        <input type="password" name="password">
        @error('password')
            <p class="error">{{ $message }}</p>
        @enderror
    </div>
    <div>
        <label>パスワード（確認）</label>
        <input type="password" name="password_confirmation">
    </div>
    <button type="submit">登録</button>
</form>
```

**コードリーディング**：

```blade
value="{{ old('name') }}"
```
→ `old()`ヘルパーで前回の入力値を取得します。バリデーションエラー時に入力値が保持されます。

```blade
@error('name')
    <p class="error">{{ $message }}</p>
@enderror
```
→ `@error`ディレクティブでエラーメッセージを表示します。`$message`変数にエラーメッセージが格納されます。

---

### ✨ 完成！

これでバリデーション機能が実装できました！フォームリクエストでバリデーションロジックを分離し、カスタムエラーメッセージを表示できましたね。

---

## 📖 模範解答

### StoreUserRequest.php

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class StoreUserRequest extends FormRequest
{
    public function authorize()
    {
        return true;
    }

    public function rules()
    {
        return [
            'name' => 'required|max:50',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:8|confirmed',
        ];
    }

    public function messages()
    {
        return [
            'name.required' => '名前は必須です',
            'name.max' => '名前は50文字以内で入力してください',
            'email.required' => 'メールアドレスは必須です',
            'email.email' => 'メールアドレスの形式が正しくありません',
            'email.unique' => 'このメールアドレスは既に使用されています',
            'password.required' => 'パスワードは必須です',
            'password.min' => 'パスワードは8文字以上で入力してください',
            'password.confirmed' => 'パスワードが一致しません',
        ];
    }
}
```

### UserController.php

```php
public function store(StoreUserRequest $request)
{
    User::create($request->validated());
    return redirect('/users');
}
```

### register.blade.php

```blade
<form action="{{ route('users.store') }}" method="POST">
    @csrf
    <div>
        <label>名前</label>
        <input type="text" name="name" value="{{ old('name') }}">
        @error('name')
            <p class="error">{{ $message }}</p>
        @enderror
    </div>
    <div>
        <label>メールアドレス</label>
        <input type="email" name="email" value="{{ old('email') }}">
        @error('email')
            <p class="error">{{ $message }}</p>
        @enderror
    </div>
    <div>
        <label>パスワード</label>
        <input type="password" name="password">
        @error('password')
            <p class="error">{{ $message }}</p>
        @enderror
    </div>
    <div>
        <label>パスワード（確認）</label>
        <input type="password" name="password_confirmation">
    </div>
    <button type="submit">登録</button>
</form>
```

---

## 💪 自己評価チェックリスト

- [ ] フォームリクエストを作成できた
- [ ] バリデーションルールを設定できた
- [ ] エラーメッセージをカスタマイズできた
- [ ] @errorでエラーを表示できた
- [ ] old()で入力値を保持できた

すべてチェックできたら、Chapter 7に進みましょう！
