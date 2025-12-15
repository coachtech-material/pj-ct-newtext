# Tutorial 9-6-5: バリデーション - ハンズオン演習

## 📝 このセクションの目的

Chapter 6で学んだバリデーションを実際に手を動かして確認します。フォームリクエストを使って、入力値の検証を実装しましょう。

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
