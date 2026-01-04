# Tutorial 9-1-7: Laravel基礎ハンズオン

## 📝 このセクションの目的

Chapter 1で学んだLaravelの基礎を実際に手を動かして確認します。**ルーティング → コントローラー → ビュー**の連携を実践しましょう。

> 💡 **このハンズオンのポイント**: データベースは使用しません。コントローラー内で準備した固定データをビューに渡して表示する、**Controller → View の連携を理解すること**が目的です。

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのプロジェクトを作成します。

```
~/laravel-practice/
├── 9-1-7_hands-on/                       ← このハンズオン用のディレクトリ
│   ├── profile-app-practice/             ← 要件を見て自分で作成するプロジェクト
│   │   ├── app/
│   │   ├── resources/
│   │   ├── routes/
│   │   └── ...
│   └── profile-app-sample/               ← 実践で一緒に作成するプロジェクト
│       ├── app/
│       ├── resources/
│       ├── routes/
│       └── ...
└── ...
```

| ディレクトリ | 用途 | URL |
|:---|:---|:---|
| `profile-app-practice/` | 📋 要件を見て、自分の力で作成する | `http://localhost/profile` |
| `profile-app-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する | `http://localhost/profile` |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

> ⚠️ **注意**: 2つのプロジェクトを同時に起動することはできません（ポートが競合するため）。一方のプロジェクトで作業する際は、もう一方を停止してください。

---

## 🎯 演習課題：自己紹介ページを作成しよう

### 📋 要件

1. `/profile`にアクセスすると、自己紹介ページが表示される
2. `ProfileController`を作成する
3. `profile.blade.php`ビューを作成する
4. 以下のデータを表示する（コントローラー内で固定値として準備）

| 項目 | 値 |
|------|-----|
| 名前 | 山田太郎 |
| 年齢 | 25 |
| 趣味 | プログラミング、読書、旅行 |

---

### 📁 Step 0: 環境を準備する（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

```bash
# laravel-practiceディレクトリに移動
cd ~/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 9-1-7_hands-on
cd 9-1-7_hands-on

# Laravel 10.xプロジェクトを作成（自分で作成する用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 profile-app-practice
```

```bash
# プロジェクトディレクトリに移動
cd profile-app-practice

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
└── 9-1-7_hands-on/
    └── profile-app-practice/     ← 自分で作成する用（今ここ）
        ├── app/
        ├── resources/
        ├── routes/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

**ここから先は、自分の力で実装してみましょう！**

---

### 🖼️ 完成イメージ

以下のような画面が表示されれば成功です。

<!-- 完成画面のスクリーンショットをここに配置 -->
![完成イメージ](images/9-1-7_profile_complete.png)

---

### 📌 ルーティング方式について

前のセクションで「ルートとメソッドを1つずつ書く方法」と「`Route::resource()`で省略する方法」の2つを学びました。

**このハンズオンでは「ルートとメソッドを1つずつ書く方法」を使います。**

```php
// このハンズオンで使う方法（ルートを1つずつ定義）
Route::get('/profile', [ProfileController::class, 'index']);
```

> 💡 **なぜこの方法を使うのか？**: `Route::resource()`は、CRUD操作（一覧・詳細・作成・更新・削除）を一括で定義する便利な方法ですが、今回は「1つのページを表示するだけ」なので、シンプルに1つずつ定義する方法が適切です。

---

## 💡 ヒント

まずは自分で考えて実装してみましょう。分からない場合は、以下のヒントを参考にしてください。

```bash
# コントローラーの作成
sail artisan make:controller ProfileController
```

```php
// ルーティングの定義
Route::get('/profile', [ProfileController::class, 'index']);
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？Laravelの基本はルーティング、コントローラー、ビューの連携です。一緒に手を動かしながら、自己紹介ページを作成していきましょう。

> 📌 **注意**: ここからは`profile-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### 💭 実装の思考プロセス

Laravelでページを作成する際、以下の順番で考えると効率的です：

| 順番 | 作業 | 説明 |
|------|------|------|
| Step 0 | 環境を準備 | Laravel Sailでコンテナを起動 |
| Step 1 | コントローラーを作成 | Artisanコマンドでコントローラーを生成 |
| Step 2 | ルーティングを定義 | URLとコントローラーを結びつける |
| Step 3 | コントローラーにロジックを追加 | データを準備してビューに渡す |
| Step 4 | ビューを作成 | BladeテンプレートでHTMLを記述 |
| Step 5 | ブラウザで確認 | 実際にアクセスして表示を確認 |

Laravel開発のポイントは「ルーティング → コントローラー → ビューの流れを理解する」ことです。

---

### 📝 ステップバイステップで実装

#### Step 0: 環境を準備する（実践用プロジェクト）

**何を考えているか**：
- 「実践用の新しいプロジェクトを作成しよう」
- 「自分で作成したプロジェクトとは別のディレクトリで進めよう」

まず、**自分で作成する用のプロジェクトを停止**します：

```bash
# profile-app-practiceディレクトリに移動
cd ~/laravel-practice/9-1-7_hands-on/profile-app-practice

# Sailを停止
./vendor/bin/sail down
```

次に、**実践用のプロジェクトを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/laravel-practice/9-1-7_hands-on

# Laravel 10.xプロジェクトを作成（実践用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 profile-app-sample
```

```bash
# プロジェクトディレクトリに移動
cd profile-app-sample

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
└── 9-1-7_hands-on/
    ├── profile-app-practice/     ← 自分で作成した用（停止中）
    └── profile-app-sample/       ← 実践用（今ここ、起動中）
        ├── app/
        ├── resources/
        ├── routes/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

**コマンド解説**：

| コマンド | 説明 |
|----------|------|
| `./vendor/bin/sail down` | Dockerコンテナを停止します。 |
| `./vendor/bin/sail up -d` | Dockerコンテナをバックグラウンドで起動します。`-d`オプションでターミナルを占有せずに実行できます。 |

> 💡 **TIP**: `sail`コマンドを短く使うために、エイリアスを設定しておくと便利です。
> ```bash
> alias sail='./vendor/bin/sail'
> ```
> これで`sail up -d`のように短く書けます。

---

#### Step 1: コントローラーを作成する

**何を考えているか**：
- 「プロフィールページを表示するコントローラーが必要だ」
- 「Artisanコマンドで簡単に生成できる」
- 「ProfileControllerという名前にしよう」

**ターミナルでプロジェクトのルートディレクトリにいることを確認**してから、以下のコマンドを実行します：

> **📌 コマンドの実行場所**
> 
> `sail artisan`コマンドは、**Laravelプロジェクトのルートディレクトリ**（`docker-compose.yml`があるディレクトリ）で実行する必要があります。
> Step 0で移動したプロジェクトディレクトリにいることを確認してください。

```bash
sail artisan make:controller ProfileController
```

**コマンド解説**：

| コマンド | 説明 |
|----------|------|
| `sail artisan make:controller ProfileController` | Artisanコマンドで`ProfileController`を生成します。`app/Http/Controllers/ProfileController.php`が作成されます。 |

> 💡 **ポイント**: `sail`を付けることで、Dockerコンテナ内でコマンドが実行されます。

---

#### Step 2: ルーティングを定義する

**何を考えているか**：
- 「`/profile`にアクセスしたらProfileControllerの処理を実行したい」
- 「`routes/web.php`にルートを追加しよう」
- 「コントローラーの`index`メソッドを呼び出そう」

`routes/web.php`を開いて、以下を追加します：

```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ProfileController;

Route::get('/', function () {
    return view('welcome');
});

// 追加：プロフィールページのルート
Route::get('/profile', [ProfileController::class, 'index']);
```

**コードリーディング**：

| コード | 説明 |
|--------|------|
| `use App\Http\Controllers\ProfileController;` | ProfileControllerクラスをインポートします。名前空間を使用するために必要です。 |
| `Route::get('/profile', ...)` | `/profile`へのGETリクエストを処理するルートを定義します。 |
| `[ProfileController::class, 'index']` | 配列形式のルート定義。ProfileControllerの`index`メソッドを呼び出します。 |

---

#### Step 3: コントローラーにロジックを追加する

**何を考えているか**：
- 「プロフィール情報（名前、年齢、趣味）を準備しよう」
- 「データを配列でまとめて、ビューに渡そう」
- 「`view()`ヘルパーでビューを返そう」

`app/Http/Controllers/ProfileController.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Http\Controllers;

class ProfileController extends Controller
{
    /**
     * プロフィールページを表示する
     * 
     * 高級レストランの比喩で言えば、厨房リーダー（コントローラー）が
     * 料理の材料（データ）を準備して、盛り付け担当（ビュー）に渡す役割です。
     */
    public function index()
    {
        // 表示するデータを準備（今回はDBを使わず固定値）
        $data = [
            'name' => '山田太郎',
            'age' => 25,
            'hobbies' => ['プログラミング', '読書', '旅行'],
        ];
        
        // ビューにデータを渡して表示
        return view('profile', $data);
    }
}
```

**コードリーディング**：

| コード | 説明 |
|--------|------|
| `namespace App\Http\Controllers;` | コントローラーの名前空間を定義します。Laravelのコントローラーはこの名前空間に配置されます。 |
| `class ProfileController extends Controller` | `Controller`クラスを継承します。Laravelのコントローラーの基本機能を利用できます。 |
| `public function index()` | `index`メソッドを定義します。ルートから呼び出されるメソッドです。 |
| `$data = [...]` | プロフィール情報を配列で準備します。今回はDBを使わず、固定値として定義しています。 |
| `return view('profile', $data);` | `view()`ヘルパーで`profile`ビューを返します。第2引数に`$data`を渡すことで、ビュー側でデータを利用できます。 |

---

#### Step 4: ビューを作成する

**何を考えているか**：
- 「`resources/views/profile.blade.php`を作成しよう」
- 「BladeテンプレートでHTMLを記述しよう」
- 「コントローラーから渡されたデータを表示しよう」

`resources/views/profile.blade.php`を新規作成します。

> **📌 ファイルの作成方法**
> 
> **方法1: ターミナルで作成**
> ```bash
> touch resources/views/profile.blade.php
> ```
> 
> **方法2: エディタ（VSCodeなど）で作成**
> `resources/views/`フォルダを右クリックして「新しいファイル」を選択し、`profile.blade.php`と入力します。

> **💡 Bladeテンプレートについて**
> 
> 以下のコードには`{{ }}`や`@foreach`などの**Blade構文**が含まれています。
> Bladeの詳細は**次のChapter（Chapter 2: ビューとBlade）**で学びます。
> 今は「こういう書き方をするんだな」と思いながら、**コピペでOK**です。

以下の内容を記述します：

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>プロフィール</title>
    <style>
        body {
            font-family: sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        .profile-item {
            margin: 15px 0;
        }
        .label {
            font-weight: bold;
            color: #555;
        }
        ul {
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <h1>プロフィール</h1>
    
    <div class="profile-item">
        <span class="label">名前:</span> {{ $name }}
    </div>
    
    <div class="profile-item">
        <span class="label">年齢:</span> {{ $age }}歳
    </div>
    
    <div class="profile-item">
        <span class="label">趣味:</span>
        <ul>
            @foreach ($hobbies as $hobby)
                <li>{{ $hobby }}</li>
            @endforeach
        </ul>
    </div>
</body>
</html>
```

**コードリーディング**：

| コード | 説明 |
|--------|------|
| `{{ $name }}` | Bladeの変数出力構文。コントローラーから渡された`$name`を表示します。自動的にHTMLエスケープされるので安全です。 |
| `{{ $age }}` | 同様に、年齢を表示します。 |
| `@foreach ($hobbies as $hobby)` | Bladeの`@foreach`ディレクティブ。配列をループ処理します。 |
| `{{ $hobby }}` | ループ内で各趣味を表示します。 |
| `@endforeach` | foreachループの終了を示します。 |

---

#### Step 5: ブラウザで確認する

**何を考えているか**：
- 「Sailでコンテナは起動済みだから、ブラウザでアクセスしよう」
- 「`/profile`にアクセスして表示を確認しよう」
- 「データが正しく表示されているかチェックしよう」

ブラウザで以下のURLにアクセスします：

```
http://localhost/profile
```

> 💡 **ポイント**: Laravel Sailを使用している場合、デフォルトでポート80が使用されるため、`http://localhost/profile`でアクセスできます。

---

### ✨ 完成！

これでLaravelの基本的なページ作成が完成しました！

**自分で作成したコードと比較してみましょう**：
- `profile-app-practice/`: 自分で作成したプロジェクト
- `profile-app-sample/`: 一緒に作成したプロジェクト

両方のプロジェクトを見比べて、違いがあれば確認してみてください。

**今回学んだ流れ**：

```
ブラウザ → ルーティング → コントローラー → ビュー → ブラウザに表示
         (web.php)    (ProfileController)  (profile.blade.php)
```

高級レストランの比喩で言えば：
- **ルーティング（ホールスタッフ）**: お客様（リクエスト）を適切な担当に案内
- **コントローラー（厨房リーダー）**: データを準備してビューに渡す
- **ビュー（盛り付け担当）**: データを美しく表示する

---

## 📖 補足：Route::resource()で書いた場合

今回は`Route::get()`で1つずつルートを定義しましたが、`Route::resource()`を使うと複数のルートを一括で定義できます。

参考として、同じ画面を`Route::resource()`で書いた場合のコード例を紹介します：

```php
// Route::resource()を使う場合
Route::resource('profiles', ProfileController::class)->only(['index']);
```

この場合、URLは`/profiles`になります（複数形）。

| 方法 | URL | 用途 |
|------|-----|------|
| `Route::get('/profile', ...)` | `/profile` | 単一のルートを定義したい場合 |
| `Route::resource('profiles', ...)->only(['index'])` | `/profiles` | CRUD操作の一部を使いたい場合 |

> 💡 **どちらを使うべき？**: 今回のように「1つのページを表示するだけ」なら`Route::get()`がシンプルです。CRUD操作（一覧・作成・編集・削除など）を実装する場合は`Route::resource()`が便利です。

---

## 📖 模範解答

### ProfileController.php

```php
<?php

namespace App\Http\Controllers;

class ProfileController extends Controller
{
    public function index()
    {
        $data = [
            'name' => '山田太郎',
            'age' => 25,
            'hobbies' => ['プログラミング', '読書', '旅行'],
        ];
        
        return view('profile', $data);
    }
}
```

### routes/web.php

```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\ProfileController;

Route::get('/', function () {
    return view('welcome');
});

Route::get('/profile', [ProfileController::class, 'index']);
```

### profile.blade.php

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>プロフィール</title>
    <style>
        body {
            font-family: sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
        }
        h1 {
            color: #333;
            border-bottom: 2px solid #007bff;
            padding-bottom: 10px;
        }
        .profile-item {
            margin: 15px 0;
        }
        .label {
            font-weight: bold;
            color: #555;
        }
        ul {
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <h1>プロフィール</h1>
    
    <div class="profile-item">
        <span class="label">名前:</span> {{ $name }}
    </div>
    
    <div class="profile-item">
        <span class="label">年齢:</span> {{ $age }}歳
    </div>
    
    <div class="profile-item">
        <span class="label">趣味:</span>
        <ul>
            @foreach ($hobbies as $hobby)
                <li>{{ $hobby }}</li>
            @endforeach
        </ul>
    </div>
</body>
</html>
```

---

## 🧪 動作確認の方法

### プロジェクトの切り替え

2つのプロジェクトを切り替えて動作確認する方法：

```bash
# profile-app-practiceで確認したい場合
cd ~/laravel-practice/9-1-7_hands-on/profile-app-sample
./vendor/bin/sail down

cd ~/laravel-practice/9-1-7_hands-on/profile-app-practice
./vendor/bin/sail up -d
# ブラウザで http://localhost/profile にアクセス

# profile-app-sampleで確認したい場合
cd ~/laravel-practice/9-1-7_hands-on/profile-app-practice
./vendor/bin/sail down

cd ~/laravel-practice/9-1-7_hands-on/profile-app-sample
./vendor/bin/sail up -d
# ブラウザで http://localhost/profile にアクセス
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

| 学んだこと | 説明 |
|------------|------|
| Laravel Sailの起動 | `sail up -d`でDockerコンテナを起動 |
| コントローラーの作成 | `sail artisan make:controller`でコントローラーを生成 |
| ルーティングの定義 | `Route::get()`でURLとコントローラーを結びつける |
| ビューへのデータ渡し | `view('profile', $data)`でデータを渡す |
| Bladeでのデータ表示 | `{{ $変数 }}`や`@foreach`でデータを表示 |

これで、Tutorial 9のChapter 1「Laravelの基礎」が完了しました。次のChapter 2では、ビューとテンプレートエンジンであるBladeについて学んでいきます。引き続き頑張りましょう！

---
