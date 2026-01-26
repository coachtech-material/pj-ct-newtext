# Tutorial 9-6-5: バリデーション - ハンズオン演習

## 📝 このセクションの目的

Chapter 6で学んだバリデーションを実際に手を動かして確認します。フォームリクエストを使って、入力値の検証を実装しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのプロジェクトを作成します。

```
~/laravel-practice/
├── 9-6-5_hands-on/                       ← このハンズオン用のディレクトリ
│   ├── validation-app-practice/          ← 要件を見て自分で作成するプロジェクト
│   │   ├── app/
│   │   │   └── Http/Requests/
│   │   ├── resources/views/
│   │   └── ...
│   └── validation-app-sample/            ← 実践で一緒に作成するプロジェクト
│       ├── app/
│       │   └── Http/Requests/
│       ├── resources/views/
│       └── ...
└── ...
```

| ディレクトリ | 用途 | URL |
|:---|:---|:---|
| `validation-app-practice/` | 📋 要件を見て、自分の力で作成する | `http://localhost/register` |
| `validation-app-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する | `http://localhost/register` |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

> ⚠️ **注意**: 2つのプロジェクトを同時に起動することはできません（ポートが競合するため）。一方のプロジェクトで作業する際は、もう一方を停止してください。

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

### 📁 Step 0: 環境を準備する（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

> **📌 前のハンズオンのプロジェクトを停止**
> 
> 前のハンズオン（9-5-6）のプロジェクトが起動している場合は、先に停止してください。
> ```bash
> cd ~/laravel-practice/9-5-6_hands-on/task-app-sample
> ./vendor/bin/sail down
> ```

```bash
# laravel-practiceディレクトリに移動
cd ~/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 9-6-5_hands-on
cd 9-6-5_hands-on

# Laravel 10.xプロジェクトを作成（自分で作成する用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 validation-app-practice
```

```bash
# プロジェクトディレクトリに移動
cd validation-app-practice

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql

# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate

# データベースのマイグレーション
./vendor/bin/sail artisan migrate
```

**✅ ディレクトリ構造の確認**

```
~/laravel-practice/
└── 9-6-5_hands-on/
    └── validation-app-practice/     ← 自分で作成する用（今ここ）
        ├── app/
        │   └── Http/Requests/
        ├── resources/views/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

```bash
sail artisan make:request StoreUserRequest
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

> 📌 **注意**: ここからは`validation-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### 💻 環境準備（実践用プロジェクト）

まず、**自分で作成する用のプロジェクトを停止**します：

```bash
# validation-app-practiceディレクトリに移動
cd ~/laravel-practice/9-6-5_hands-on/validation-app-practice

# Sailを停止
./vendor/bin/sail down
```

次に、**実践用のプロジェクトを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/laravel-practice/9-6-5_hands-on

# Laravel 10.xプロジェクトを作成（実践用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 validation-app-sample
```

```bash
# プロジェクトディレクトリに移動
cd validation-app-sample

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql

# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate

# データベースのマイグレーション
./vendor/bin/sail artisan migrate
```

**✅ ディレクトリ構造の確認**

```
~/laravel-practice/
└── 9-6-5_hands-on/
    ├── validation-app-practice/     ← 自分で作成した用（停止中）
    └── validation-app-sample/       ← 実践用（今ここ、起動中）
        ├── app/
        │   └── Http/Requests/
        ├── resources/views/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

---

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
sail artisan make:request StoreUserRequest
```

**コマンド解説**：

```bash
sail artisan make:request StoreUserRequest
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

ターミナルで以下のコマンドを実行して、`register.blade.php`ファイルを作成します：

```bash
touch resources/views/register.blade.php
```

`resources/views/register.blade.php`をエディタで開き、以下の内容を記述します：

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

**自分で作成したコードと比較してみましょう**：
- `validation-app-practice/`: 自分で作成したプロジェクト
- `validation-app-sample/`: 一緒に作成したプロジェクト

両方のプロジェクトを見比べて、違いがあれば確認してみてください。

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

## 🧪 動作確認の方法

### プロジェクトの切り替え

2つのプロジェクトを切り替えて動作確認する方法：

```bash
# validation-app-practiceで確認したい場合
cd ~/laravel-practice/9-6-5_hands-on/validation-app-sample
./vendor/bin/sail down

cd ~/laravel-practice/9-6-5_hands-on/validation-app-practice
./vendor/bin/sail up -d

# validation-app-sampleで確認したい場合
cd ~/laravel-practice/9-6-5_hands-on/validation-app-practice
./vendor/bin/sail down

cd ~/laravel-practice/9-6-5_hands-on/validation-app-sample
./vendor/bin/sail up -d
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ フォームリクエストを作成できる
- ✅ バリデーションルールを定義できる
- ✅ カスタムエラーメッセージを設定できる

引き続き、次のセクションも頑張りましょう！

### 🛑 Sailの停止

次のセクションに進む前に、Sailを停止しておきましょう。

```bash
./vendor/bin/sail down
```

> 💡 **なぜ停止するの？**: Sailを起動したままだと、次のセクションで別のプロジェクトを起動する際にポートが競合してエラーになることがあります。セクションの終わりには必ずSailを停止する習慣をつけましょう。

---
