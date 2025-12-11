# Tutorial 9-6-1: バリデーションの基礎

## 🎯 このセクションで学ぶこと

*   バリデーションが何であるか、その重要性を理解する。
*   Laravelの`validate()`メソッドを使って、フォーム入力を検証できるようになる。
*   バリデーションルールの書き方と、エラーメッセージの表示方法を学ぶ。

---

## 導入：ユーザー入力は「信用してはいけない」

Webアプリケーションでは、ユーザーからの入力を受け取ることが頻繁にあります。例えば、ユーザー登録フォーム、投稿作成フォーム、コメント投稿フォームなどです。

しかし、ユーザーが入力するデータは、**必ずしも正しいとは限りません**。以下のような問題が起こり得ます。

*   **必須項目が空**: メールアドレスや名前が入力されていない
*   **形式が不正**: メールアドレスの形式が間違っている（例：`abc@`）
*   **文字数制限を超えている**: 名前が255文字を超えている
*   **悪意のある入力**: SQLインジェクションやXSS攻撃を試みる

これらの問題を防ぐために、**バリデーション（検証）**が必要です。バリデーションとは、ユーザーの入力が正しい形式であるかをチェックし、不正な入力を拒否する仕組みです。

---

## 詳細解説

### 🛡️ Laravelのバリデーション機能

Laravelには、強力なバリデーション機能が標準で組み込まれています。コントローラーで`validate()`メソッドを呼び出すだけで、簡単にバリデーションを実行できます。

#### 基本的な使い方

**例：ユーザー登録フォームのバリデーション**

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;

class UserController extends Controller
{
    public function store(Request $request)
    {
        // バリデーションを実行
        $validated = $request->validate([
            'name' => 'required|max:255',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:8',
        ]);

        // バリデーションが成功したら、ユーザーを作成
        $user = User::create([
            'name' => $validated['name'],
            'email' => $validated['email'],
            'password' => bcrypt($validated['password']),
        ]);

        return redirect()->route('users.show', $user);
    }
}
```

**コードリーディング**

*   `$request->validate([...])`: バリデーションルールを配列で指定します。
*   `'name' => 'required|max:255'`: `name`フィールドは必須で、最大255文字まで。
*   `'email' => 'required|email|unique:users'`: `email`フィールドは必須で、メールアドレス形式で、`users`テーブルで一意（重複不可）。
*   `'password' => 'required|min:8'`: `password`フィールドは必須で、最小8文字。
*   バリデーションが失敗すると、自動的に前のページにリダイレクトされ、エラーメッセージが表示されます。
*   バリデーションが成功すると、検証済みのデータが`$validated`に格納されます。

---

### 📝 主なバリデーションルール

Laravelには、様々なバリデーションルールが用意されています。

| ルール | 説明 | 例 |
|:---|:---|:---|
| `required` | 必須項目 | `'name' => 'required'` |
| `email` | メールアドレス形式 | `'email' => 'email'` |
| `min:n` | 最小文字数（文字列）または最小値（数値） | `'password' => 'min:8'` |
| `max:n` | 最大文字数（文字列）または最大値（数値） | `'name' => 'max:255'` |
| `unique:テーブル名,カラム名` | データベースで一意 | `'email' => 'unique:users,email'` |
| `confirmed` | 確認フィールドと一致（`password_confirmation`） | `'password' => 'confirmed'` |
| `numeric` | 数値 | `'age' => 'numeric'` |
| `integer` | 整数 | `'age' => 'integer'` |
| `between:min,max` | 範囲内 | `'age' => 'between:18,100'` |
| `in:値1,値2,...` | 指定した値のいずれか | `'role' => 'in:admin,user'` |
| `date` | 日付形式 | `'birthday' => 'date'` |
| `after:日付` | 指定した日付より後 | `'start_date' => 'after:today'` |
| `before:日付` | 指定した日付より前 | `'end_date' => 'before:2025-12-31'` |

#### 複数のルールを組み合わせる

ルールは、パイプ（`|`）で区切って複数指定できます。

```php
'email' => 'required|email|unique:users|max:255'
```

配列形式で指定することもできます。

```php
'email' => ['required', 'email', 'unique:users', 'max:255']
```

---

### 🚨 バリデーションエラーの表示

バリデーションが失敗すると、Laravelは自動的に前のページにリダイレクトし、エラーメッセージを`$errors`変数に格納します。

**Bladeでエラーメッセージを表示する**

```blade
<form method="POST" action="{{ route('users.store') }}">
    @csrf

    <div>
        <label for="name">名前</label>
        <input type="text" name="name" id="name" value="{{ old('name') }}">
        @error('name')
            <p style="color: red;">{{ $message }}</p>
        @enderror
    </div>

    <div>
        <label for="email">メールアドレス</label>
        <input type="email" name="email" id="email" value="{{ old('email') }}">
        @error('email')
            <p style="color: red;">{{ $message }}</p>
        @enderror
    </div>

    <div>
        <label for="password">パスワード</label>
        <input type="password" name="password" id="password">
        @error('password')
            <p style="color: red;">{{ $message }}</p>
        @enderror
    </div>

    <button type="submit">登録</button>
</form>
```

**コードリーディング**

*   `@csrf`: CSRF保護のためのトークンを生成します（必須）。
*   `value="{{ old('name') }}"`: バリデーションエラー時に、入力した値を保持します。
*   `@error('name')`: `name`フィールドにエラーがある場合、エラーメッセージを表示します。
*   `{{ $message }}`: エラーメッセージの内容を表示します。

#### 全てのエラーメッセージを一括表示する

```blade
@if ($errors->any())
    <div style="color: red;">
        <ul>
            @foreach ($errors->all() as $error)
                <li>{{ $error }}</li>
            @endforeach
        </ul>
    </div>
@endif
```

---

### 🌐 エラーメッセージの日本語化

デフォルトでは、エラーメッセージは英語で表示されます。日本語化するには、以下の手順を実行します。

#### ステップ1: 言語ファイルをインストールする

Laravelの公式日本語化リポジトリから、言語ファイルをダウンロードします。

```bash
docker compose exec php composer require laravel-lang/lang --dev
docker compose exec php php artisan lang:publish ja
```

#### ステップ2: デフォルトの言語を日本語に設定する

`config/app.php`の`locale`を`ja`に変更します。

```php
'locale' => 'ja',
```

これで、エラーメッセージが日本語で表示されるようになります。

---

### 🎨 カスタムエラーメッセージ

エラーメッセージをカスタマイズしたい場合は、`validate()`の第2引数で指定します。

```php
$request->validate([
    'name' => 'required|max:255',
    'email' => 'required|email|unique:users',
], [
    'name.required' => '名前は必須です。',
    'name.max' => '名前は255文字以内で入力してください。',
    'email.required' => 'メールアドレスは必須です。',
    'email.email' => 'メールアドレスの形式が正しくありません。',
    'email.unique' => 'このメールアドレスは既に登録されています。',
]);
```

---

## 💡 TIP: フォームリクエストで複雑なバリデーションを分離する

バリデーションルールが複雑になると、コントローラーが肥大化します。その場合、**フォームリクエスト**という専用のクラスにバリデーションロジックを分離することができます。

```bash
docker compose exec php php artisan make:request StoreUserRequest
```

これにより、`app/Http/Requests/StoreUserRequest.php`が生成されます。詳細は、後のセクションで学びます。

---

## ✨ まとめ

このセクションでは、Laravelのバリデーション機能の基礎を学びました。

*   バリデーションとは、ユーザーの入力が正しい形式であるかをチェックする仕組みである。
*   `$request->validate()`を使って、バリデーションルールを配列で指定できる。
*   `required`, `email`, `min`, `max`, `unique`などの様々なルールがある。
*   バリデーションエラーは、`@error`ディレクティブを使ってBladeで表示できる。
*   `old()`ヘルパーを使って、エラー時に入力値を保持できる。

次のセクションでは、より高度なバリデーション（カスタムルール、フォームリクエスト）を学びます。

---

## 📝 学習のポイント

- [ ] バリデーションが、ユーザー入力を検証する重要な仕組みであることを理解した。
- [ ] `$request->validate()`を使って、バリデーションルールを指定できる。
- [ ] `required`, `email`, `min`, `max`, `unique`などの主要なルールを使える。
- [ ] `@error`ディレクティブを使って、エラーメッセージを表示できる。
- [ ] `old()`ヘルパーを使って、エラー時に入力値を保持できる。
