# Tutorial 10-6-6: Webセキュリティハンズオン

## 🎯 このハンズオンで実践すること

Chapter 6で学んだセキュリティ対策を実際に手を動かして確認します。このハンズオンでは、**CSRF保護**と**XSS対策**に焦点を当てて実装します。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのプロジェクトを作成します。

```
~/laravel-practice/
├── 10-6-6_hands-on/                      ← このハンズオン用のディレクトリ
│   ├── security-app-practice/            ← 要件を見て自分で作成するプロジェクト
│   │   ├── app/
│   │   │   └── Http/Controllers/
│   │   │       └── ContactController.php
│   │   └── resources/views/
│   │       └── contact/
│   │           ├── form.blade.php
│   │           └── thanks.blade.php
│   └── security-app-sample/              ← 実践で一緒に作成するプロジェクト
│       ├── app/
│       │   └── Http/Controllers/
│       └── resources/views/
└── ...
```

| ディレクトリ | 用途 |
|:---|:---|
| `security-app-practice/` | 📋 要件を見て、自分の力で作成する |
| `security-app-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

> ⚠️ **注意**: 2つのプロジェクトを同時に起動することはできません（ポートが競合するため）。一方のプロジェクトで作業する際は、もう一方を停止してください。

---

## 📝 課題：CSRF保護付きお問い合わせフォームを作成しよう

このハンズオンでは、**セキュリティを意識したお問い合わせフォーム**を作成します。

### 📋 要件

1. **お問い合わせフォームを作成**
   - 名前、メールアドレス、メッセージを入力
   - CSRF保護を実装（`@csrf`ディレクティブ）

2. **送信完了画面を作成**
   - 入力内容を表示
   - XSS対策を実装（`{{ }}`構文でエスケープ）

3. **ルーティングを設定**
   - `GET /contact` → フォーム表示
   - `POST /contact` → 送信処理

> 💡 **ポイント**: このハンズオンでは、データベースへの保存は行いません。フォームの送信とセキュリティ対策に集中しましょう。

---

## 🔧 環境準備（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

> **📌 前のハンズオンのプロジェクトを停止**
> 
> 前のハンズオン（10-5-8）のプロジェクトが起動している場合は、先に停止してください。
> ```bash
> cd ~/laravel-practice/10-5-8_hands-on/testing-app-sample
> ./vendor/bin/sail down
> ```

```bash
# laravel-practiceディレクトリに移動
cd ~/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 10-6-6_hands-on
cd 10-6-6_hands-on

# Laravel 10.xプロジェクトを作成（自分で作成する用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 security-app-practice
```

```bash
# プロジェクトディレクトリに移動
cd security-app-practice

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
```

**✅ ディレクトリ構造の確認**

```
~/laravel-practice/
└── 10-6-6_hands-on/
    └── security-app-practice/     ← 自分で作成する用（今ここ）
        ├── app/
        │   └── Http/Controllers/
        └── resources/views/
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

### ヒント1: コントローラーの作成

```bash
sail artisan make:controller ContactController
```

### ヒント2: CSRF保護

フォームには必ず`@csrf`ディレクティブを追加してください。

```blade
<form method="POST" action="/contact">
    @csrf
    <!-- フォームの内容 -->
</form>
```

### ヒント3: XSS対策

ユーザー入力を表示する際は、`{{ }}`構文を使ってください。

```blade
<p>{{ $name }}</p>
```

`{!! !!}`は使わないでください（HTMLがそのまま出力されてしまいます）。

### ヒント4: ルーティング

```php
Route::get('/contact', [ContactController::class, 'showForm']);
Route::post('/contact', [ContactController::class, 'submit']);
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？セキュリティを意識したWebアプリケーション開発は重要です。一緒に手を動かしながら、CSRF保護付きお問い合わせフォームを作成していきましょう。

> 📌 **注意**: ここからは`security-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### 💻 環境準備（実践用プロジェクト）

まず、**自分で作成する用のプロジェクトを停止**します：

```bash
# security-app-practiceディレクトリに移動
cd ~/laravel-practice/10-6-6_hands-on/security-app-practice

# Sailを停止
./vendor/bin/sail down
```

次に、**実践用のプロジェクトを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/laravel-practice/10-6-6_hands-on

# Laravel 10.xプロジェクトを作成（実践用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 security-app-sample
```

```bash
# プロジェクトディレクトリに移動
cd security-app-sample

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
```

**✅ ディレクトリ構造の確認**

```
~/laravel-practice/
└── 10-6-6_hands-on/
    ├── security-app-practice/     ← 自分で作成した用（停止中）
    └── security-app-sample/       ← 実践用（今ここ、起動中）
        ├── app/
        │   └── Http/Controllers/
        └── resources/views/
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

---

### 💭 実装の思考プロセス

セキュリティを意識したフォームを実装する際、以下の順番で考えると効率的です：

1. **コントローラーを作成**：フォーム表示と送信処理
2. **ビューを作成**：フォームと完了画面
3. **CSRF保護を追加**：`@csrf`ディレクティブ
4. **XSS対策を確認**：`{{ }}`構文でエスケープ
5. **ルーティングを設定**：GETとPOST

---

### 📝 ステップバイステップで実装

#### ステップ1: コントローラーを作成する

**何を考えているか**：
- 「お問い合わせフォームを表示するメソッドが必要だ」
- 「フォーム送信を処理するメソッドも必要だ」

ターミナルで以下のコマンドを実行します：

```bash
sail artisan make:controller ContactController
```

**コマンド解説**：

| 部分 | 説明 |
|------|------|
| `make:controller` | コントローラーを作成 |
| `ContactController` | コントローラー名 |

→ `app/Http/Controllers/ContactController.php`が作成されます。

---

#### ステップ2: コントローラーにメソッドを追加する

**何を考えているか**：
- 「フォームを表示するメソッドを作ろう」
- 「送信処理を行うメソッドを作ろう」

`app/Http/Controllers/ContactController.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ContactController extends Controller
{
    /**
     * お問い合わせフォームを表示
     */
    public function showForm()
    {
        return view('contact.form');
    }

    /**
     * お問い合わせを送信
     */
    public function submit(Request $request)
    {
        // バリデーション
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email',
            'message' => 'required|string',
        ]);

        // 完了画面にデータを渡す
        return view('contact.thanks', [
            'name' => $validated['name'],
            'email' => $validated['email'],
            'message' => $validated['message'],
        ]);
    }
}
```

**コード解説**：

| 行 | コード | 説明 |
|:---|:---|:---|
| 1 | `public function showForm()` | フォーム表示用メソッド |
| 2 | `return view('contact.form')` | `contact/form.blade.php`を表示 |
| 3 | `public function submit(Request $request)` | 送信処理用メソッド |
| 4 | `$request->validate([...])` | 入力値のバリデーション |
| 5 | `return view('contact.thanks', [...])` | 完了画面にデータを渡す |

---

#### ステップ3: フォームのビューを作成する

**何を考えているか**：
- 「お問い合わせフォームのビューを作ろう」
- 「CSRF保護を忘れずに追加しよう」

まず、ビュー用のディレクトリを作成します：

```bash
mkdir -p resources/views/contact
```

`resources/views/contact/form.blade.php`を作成します：

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>お問い合わせ</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        label { display: block; margin-top: 15px; font-weight: bold; }
        input, textarea { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; }
        textarea { height: 150px; }
        button { margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .error { color: red; font-size: 14px; }
    </style>
</head>
<body>
    <h1>お問い合わせ</h1>

    <form method="POST" action="/contact">
        @csrf

        <label for="name">お名前</label>
        <input type="text" id="name" name="name" value="{{ old('name') }}">
        @error('name')
            <p class="error">{{ $message }}</p>
        @enderror

        <label for="email">メールアドレス</label>
        <input type="email" id="email" name="email" value="{{ old('email') }}">
        @error('email')
            <p class="error">{{ $message }}</p>
        @enderror

        <label for="message">メッセージ</label>
        <textarea id="message" name="message">{{ old('message') }}</textarea>
        @error('message')
            <p class="error">{{ $message }}</p>
        @enderror

        <button type="submit">送信</button>
    </form>
</body>
</html>
```

**コード解説**：

| 行 | コード | 説明 |
|:---|:---|:---|
| 1 | `<form method="POST" action="/contact">` | POSTメソッドで`/contact`に送信 |
| 2 | `@csrf` | **CSRF保護トークンを埋め込む**（重要！） |
| 3 | `value="{{ old('name') }}"` | バリデーションエラー時に入力値を保持 |
| 4 | `@error('name')` | バリデーションエラーを表示 |

> 💡 **CSRF保護のポイント**: `@csrf`を忘れると、フォーム送信時に「419 Page Expired」エラーが発生します。

---

#### ステップ4: 完了画面のビューを作成する

**何を考えているか**：
- 「送信完了画面を作ろう」
- 「ユーザー入力を表示するときはXSS対策を忘れずに」

`resources/views/contact/thanks.blade.php`を作成します：

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>送信完了</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        h1 { color: #28a745; }
        .info { background: #f8f9fa; padding: 20px; border-radius: 4px; margin-top: 20px; }
        .info p { margin: 10px 0; }
        .label { font-weight: bold; color: #666; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>送信完了</h1>
    <p>お問い合わせありがとうございます。</p>

    <div class="info">
        <p><span class="label">お名前：</span>{{ $name }}</p>
        <p><span class="label">メールアドレス：</span>{{ $email }}</p>
        <p><span class="label">メッセージ：</span></p>
        <p>{{ $message }}</p>
    </div>

    <p style="margin-top: 20px;"><a href="/contact">戻る</a></p>
</body>
</html>
```

**コード解説**：

| 行 | コード | 説明 |
|:---|:---|:---|
| 1 | `{{ $name }}` | **XSS対策済み**（HTMLエスケープされる） |
| 2 | `{{ $email }}` | **XSS対策済み** |
| 3 | `{{ $message }}` | **XSS対策済み** |

> 💡 **XSS対策のポイント**: `{{ }}`構文を使うと、`<script>`タグなどの危険な文字が自動的にエスケープされます。

---

#### ステップ5: ルーティングを設定する

**何を考えているか**：
- 「フォーム表示用のGETルートが必要だ」
- 「送信処理用のPOSTルートも必要だ」

`routes/web.php`を開いて、以下を追加します：

```php
use App\Http\Controllers\ContactController;

Route::get('/contact', [ContactController::class, 'showForm']);
Route::post('/contact', [ContactController::class, 'submit']);
```

**コード解説**：

| 行 | コード | 説明 |
|:---|:---|:---|
| 1 | `Route::get('/contact', ...)` | GETリクエストでフォームを表示 |
| 2 | `Route::post('/contact', ...)` | POSTリクエストで送信処理 |

---

#### ステップ6: 動作確認

ブラウザで `http://localhost/contact` にアクセスして、以下を確認します：

1. **フォームが表示される**
2. **必須項目を空にして送信** → バリデーションエラーが表示される
3. **正しく入力して送信** → 完了画面が表示される
4. **完了画面に入力内容が表示される**

---

### 🔍 CSRF保護の確認

CSRF保護が正しく機能しているか確認してみましょう。

#### 確認方法1: HTMLソースを確認

ブラウザで `http://localhost/contact` を開き、HTMLソースを確認します（右クリック → 「ページのソースを表示」）。

以下のような隠しフィールドが含まれていれば、CSRF保護が有効です：

```html
<input type="hidden" name="_token" value="ランダムな文字列">
```

#### 確認方法2: @csrfを削除してテスト

試しに`@csrf`を削除してフォームを送信すると、「419 Page Expired」エラーが発生します。これはCSRF保護が正しく機能している証拠です。

> ⚠️ **注意**: 確認後は必ず`@csrf`を元に戻してください。

---

### 🔍 XSS対策の確認

XSS対策が正しく機能しているか確認してみましょう。

#### 確認方法: スクリプトタグを入力

フォームのメッセージ欄に以下を入力して送信します：

```
<script>alert('XSS攻撃')</script>
```

**期待される結果**:
- 完了画面で、スクリプトが**実行されず**、文字列としてそのまま表示される
- HTMLソースを確認すると、`<script>`が`&lt;script&gt;`にエスケープされている

これはXSS対策が正しく機能している証拠です。

---

### ✨ 完成！

これでCSRF保護とXSS対策を実装したお問い合わせフォームが完成しました！

**自分で作成したコードと比較してみましょう**：
- `security-app-practice/`: 自分で作成したプロジェクト
- `security-app-sample/`: 一緒に作成したプロジェクト

両方のプロジェクトを見比べて、違いがあれば確認してみてください。

---

## 📖 模範解答

### app/Http/Controllers/ContactController.php

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class ContactController extends Controller
{
    /**
     * お問い合わせフォームを表示
     */
    public function showForm()
    {
        return view('contact.form');
    }

    /**
     * お問い合わせを送信
     */
    public function submit(Request $request)
    {
        // バリデーション
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email',
            'message' => 'required|string',
        ]);

        // 完了画面にデータを渡す
        return view('contact.thanks', [
            'name' => $validated['name'],
            'email' => $validated['email'],
            'message' => $validated['message'],
        ]);
    }
}
```

### routes/web.php

```php
<?php

use App\Http\Controllers\ContactController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/contact', [ContactController::class, 'showForm']);
Route::post('/contact', [ContactController::class, 'submit']);
```

### resources/views/contact/form.blade.php

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>お問い合わせ</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        h1 { color: #333; }
        label { display: block; margin-top: 15px; font-weight: bold; }
        input, textarea { width: 100%; padding: 10px; margin-top: 5px; border: 1px solid #ccc; border-radius: 4px; }
        textarea { height: 150px; }
        button { margin-top: 20px; padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .error { color: red; font-size: 14px; }
    </style>
</head>
<body>
    <h1>お問い合わせ</h1>

    <form method="POST" action="/contact">
        @csrf

        <label for="name">お名前</label>
        <input type="text" id="name" name="name" value="{{ old('name') }}">
        @error('name')
            <p class="error">{{ $message }}</p>
        @enderror

        <label for="email">メールアドレス</label>
        <input type="email" id="email" name="email" value="{{ old('email') }}">
        @error('email')
            <p class="error">{{ $message }}</p>
        @enderror

        <label for="message">メッセージ</label>
        <textarea id="message" name="message">{{ old('message') }}</textarea>
        @error('message')
            <p class="error">{{ $message }}</p>
        @enderror

        <button type="submit">送信</button>
    </form>
</body>
</html>
```

### resources/views/contact/thanks.blade.php

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>送信完了</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        h1 { color: #28a745; }
        .info { background: #f8f9fa; padding: 20px; border-radius: 4px; margin-top: 20px; }
        .info p { margin: 10px 0; }
        .label { font-weight: bold; color: #666; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>送信完了</h1>
    <p>お問い合わせありがとうございます。</p>

    <div class="info">
        <p><span class="label">お名前：</span>{{ $name }}</p>
        <p><span class="label">メールアドレス：</span>{{ $email }}</p>
        <p><span class="label">メッセージ：</span></p>
        <p>{{ $message }}</p>
    </div>

    <p style="margin-top: 20px;"><a href="/contact">戻る</a></p>
</body>
</html>
```

---

## 🚨 うまくいかない場合

### エラー1: 419 Page Expired

**原因**: CSRF保護が機能している（`@csrf`が不足している）

**対処法**: フォームに`@csrf`を追加してください。

```blade
<form method="POST" action="/contact">
    @csrf
    <!-- フォームの内容 -->
</form>
```

---

### エラー2: ルートが見つからない

**原因**: ルーティングが設定されていない

**対処法**: `routes/web.php`にルートを追加してください。

```php
use App\Http\Controllers\ContactController;

Route::get('/contact', [ContactController::class, 'showForm']);
Route::post('/contact', [ContactController::class, 'submit']);
```

---

### エラー3: ビューが見つからない

**原因**: ビューファイルが正しい場所にない

**対処法**: 以下のディレクトリ構造を確認してください。

```
resources/views/
└── contact/
    ├── form.blade.php
    └── thanks.blade.php
```

---

## ✨ まとめ

このハンズオンでは、セキュリティを意識したお問い合わせフォームを作成しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | コントローラーの作成 |
| Step 2 | フォーム表示と送信処理の実装 |
| Step 3 | `@csrf`によるCSRF保護 |
| Step 4 | `{{ }}`構文によるXSS対策 |
| Step 5 | ルーティングの設定 |

**セキュリティの重要なポイント**:

| 対策 | 実装方法 | 効果 |
|------|----------|------|
| CSRF保護 | `@csrf`ディレクティブ | 不正なフォーム送信を防ぐ |
| XSS対策 | `{{ }}`構文 | 悪意のあるスクリプト実行を防ぐ |

これでTutorial 10のハンズオンは全て完了です。お疲れ様でした！

---
