# Tutorial 10-2-5: HTTPライフサイクル実践ハンズオン

## 🎯 このセクションで学ぶこと

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

*   実際に手を動かして、HTTPライフサイクル全体を体験する。
*   ミドルウェア、ルーティング、コントローラーの連携を実装する。
*   ログを使って、リクエストの流れを可視化する。

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのプロジェクトを作成します。

```
~/coachtech/laravel-practice/
├── 10-2-5_hands-on/                      ← このハンズオン用のディレクトリ
│   ├── lifecycle-app-practice/           ← 要件を見て自分で作成するプロジェクト
│   │   ├── app/
│   │   │   ├── Http/Middleware/
│   │   │   └── Models/
│   │   └── ...
│   └── lifecycle-app-sample/             ← 実践で一緒に作成するプロジェクト
│       ├── app/
│       │   ├── Http/Middleware/
│       │   └── Models/
│       └── ...
└── ...
```

| ディレクトリ | 用途 | URL |
|:---|:---|:---|
| `lifecycle-app-practice/` | 📋 要件を見て、自分の力で作成する | `http://localhost/posts` |
| `lifecycle-app-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する | `http://localhost/posts` |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

> ⚠️ **注意**: 2つのプロジェクトを同時に起動することはできません（ポートが競合するため）。一方のプロジェクトで作業する際は、もう一方を停止してください。

---

## 導入：理論を実践で確認する

前のセクションで、HTTPライフサイクルの理論を学びました。このセクションでは、**実際にコードを書いて**、リクエストがどのように処理されるかを体験します。

**このハンズオンで作るもの**：
ブログ記事の閲覧数カウンター機能を実装し、HTTPライフサイクルの各段階でログを記録します。

---

## 🎯 演習課題：ブログ記事の閲覧数カウンター

### 🖼️ 完成イメージ

<!-- ブログ記事とログ出力のスクリーンショットをここに配置 -->
![10-2-5 完成イメージ](images/10-2-5_http_lifecycle_complete.png)

**この演習で作るもの**：
ミドルウェアで閲覧数をカウントし、HTTPライフサイクルをログで可視化する「ブログ記事表示機能」を作成します。

---

### 📋 要件

*   ブログ記事を表示する機能を作成する
*   ミドルウェアを使って、閲覧数をカウントする
*   ログを記録して、HTTPライフサイクルを可視化する

---

### ✅ 完成品の確認方法

**🌐 ブラウザでの確認（推奨）**

- **動作確認URL**: `http://localhost/posts`
- **確認手順**:
  1. Sailを起動する（`./vendor/bin/sail up -d`）
  2. マイグレーションを実行（`./vendor/bin/sail artisan migrate`）
  3. シーダーを実行（`./vendor/bin/sail artisan db:seed --class=PostSeeder`）
  4. ブラウザで `http://localhost/posts` にアクセス
  5. ページを何度かリロードして閲覧数が増えることを確認

**正しく実装できていれば**:
- [ ] ブログ記事一覧が表示される
- [ ] 記事詳細ページをリロードすると閲覧数が増える
- [ ] ログファイルにHTTPライフサイクルのログが記録される

**🔧 ログの確認方法**:

```bash
# リアルタイムでログを確認
./vendor/bin/sail exec laravel.test tail -f storage/logs/laravel.log
```

> 📌 **Bladeファイルについて**: バックエンド実装に集中するため、動作確認用のシンプルなBladeファイルを以下に用意しています。

<details>
<summary>📄 確認用Bladeファイル（クリックで展開）</summary>

`resources/views/posts/index.blade.php`:

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ブログ記事一覧</title>
</head>
<body>
    <h1>ブログ記事一覧</h1>
    <ul>
        @foreach ($posts as $post)
            <li>
                <a href="/posts/{{ $post->id }}">{{ $post->title }}</a>
                （閲覧数: {{ $post->views }}）
            </li>
        @endforeach
    </ul>
</body>
</html>
```

`resources/views/posts/show.blade.php`:

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{{ $post->title }}</title>
</head>
<body>
    <h1>{{ $post->title }}</h1>
    <p>閲覧数: {{ $post->views }}</p>
    <div>{{ $post->content }}</div>
    <p><a href="/posts">一覧に戻る</a></p>
</body>
</html>
```

</details>

---

### 📁 Step 0: 環境を準備する（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

> **📌 前のハンズオンのプロジェクトを停止**
> 
> 前のハンズオン（10-2-4）のプロジェクトが起動している場合は、先に停止してください。
> ```bash
> cd ~/coachtech/laravel-practice/10-2-4_hands-on/middleware-app-sample
> ./vendor/bin/sail down
> ```

```bash
# laravel-practiceディレクトリに移動
cd ~/coachtech/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 10-2-5_hands-on
cd 10-2-5_hands-on

# Laravel 10.xプロジェクトを作成（自分で作成する用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 lifecycle-app-practice
```

```bash
# プロジェクトディレクトリに移動
cd lifecycle-app-practice

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
~/coachtech/laravel-practice/
└── 10-2-5_hands-on/
    └── lifecycle-app-practice/     ← 自分で作成する用（今ここ）
        ├── app/
        │   ├── Http/Middleware/
        │   └── Models/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

```bash
# マイグレーションとモデルの作成
sail artisan make:migration create_posts_table
sail artisan make:model Post

# ミドルウェアの作成
sail artisan make:middleware LogHttpLifecycle
sail artisan make:middleware CountPostViews
```

```php
// ミドルウェアでログを記録
Log::info('=== HTTP Lifecycle Start ===');
$response = $next($request);
Log::info('=== HTTP Lifecycle End ===');
return $response;
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？HTTPライフサイクルを理解するには、実際にログを記録して流れを確認するのが一番です。一緒に手を動かしながら、ブログ記事の閲覧数カウンター機能を実装していきましょう。

> 📌 **注意**: ここからは`lifecycle-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### 💻 環境準備（実践用プロジェクト）

まず、**自分で作成する用のプロジェクトを停止**します：

```bash
# lifecycle-app-practiceディレクトリに移動
cd ~/coachtech/laravel-practice/10-2-5_hands-on/lifecycle-app-practice

# Sailを停止
./vendor/bin/sail down
```

次に、**実践用のプロジェクトを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/coachtech/laravel-practice/10-2-5_hands-on

# Laravel 10.xプロジェクトを作成（実践用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 lifecycle-app-sample
```

```bash
# プロジェクトディレクトリに移動
cd lifecycle-app-sample

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
~/coachtech/laravel-practice/
└── 10-2-5_hands-on/
    ├── lifecycle-app-practice/     ← 自分で作成した用（停止中）
    └── lifecycle-app-sample/       ← 実践用（今ここ、起動中）
        ├── app/
        │   ├── Http/Middleware/
        │   └── Models/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

---

### 🔧 ステップ1: マイグレーションとモデルの作成

#### 何を考えているか
まず、ブログ記事を保存するためのデータベーステーブルを作成します。閲覧数を記録するために、`views`カラムを追加します。

#### コマンド

```bash
sail artisan make:migration create_posts_table
```

**コマンド解説**：
- `make:migration`：新しいマイグレーションファイルを作成
- `create_posts_table`：テーブル名を示す命名規則

#### マイグレーションファイルを編集

**`database/migrations/xxxx_create_posts_table.php`**

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up()
    {
        Schema::create('posts', function (Blueprint $table) {
            $table->id();                          // → 主キー（自動増分）
            $table->string('title');               // → 記事のタイトル
            $table->text('content');               // → 記事の本文
            $table->integer('views')->default(0);  // → 閲覧数（デフォルト0）
            $table->timestamps();                  // → created_at, updated_at
        });
    }

    public function down()
    {
        Schema::dropIfExists('posts');
    }
};
```

**コードリーディング**：
- `$table->id()`：主キー（自動増分のID）
- `$table->string('title')`：VARCHAR型のカラム
- `$table->text('content')`：TEXT型のカラム（長文用）
- `$table->integer('views')->default(0)`：INT型のカラム、デフォルト値は0
- `$table->timestamps()`：created_atとupdated_atを自動追加

#### マイグレーションを実行

```bash
sail artisan migrate
```

---

#### モデルを作成

```bash
sail artisan make:model Post
```

**`app/Models/Post.php`**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    protected $fillable = ['title', 'content', 'views'];

    // 閲覧数を1増やすメソッド
    public function incrementViews()
    {
        $this->increment('views');
    }
}
```

**コードリーディング**：
- `protected $fillable`：一括代入可能なカラムを指定
- `incrementViews()`：閲覧数を1増やすカスタムメソッド
- `$this->increment('views')`：Eloquentの便利メソッド（`UPDATE posts SET views = views + 1`を実行）

---

### 🔧 ステップ2: シーダーでテストデータを作成

#### 何を考えているか
動作確認のために、サンプルデータを作成します。

#### コマンド

```bash
sail artisan make:seeder PostSeeder
```

**`database/seeders/PostSeeder.php`**

```php
<?php

namespace Database\Seeders;

use App\Models\Post;
use Illuminate\Database\Seeder;

class PostSeeder extends Seeder
{
    public function run()
    {
        Post::create([
            'title' => 'Laravelの基礎',
            'content' => 'Laravelは、PHPのWebアプリケーションフレームワークです。',
        ]);

        Post::create([
            'title' => 'Eloquent ORMの使い方',
            'content' => 'Eloquent ORMは、Laravelのデータベース操作ツールです。',
        ]);

        Post::create([
            'title' => 'ミドルウェアとは',
            'content' => 'ミドルウェアは、リクエストとレスポンスの間に入る処理です。',
        ]);
    }
}
```

#### シーダーを実行

```bash
sail artisan db:seed --class=PostSeeder
```

**コマンド解説**：
- `db:seed`：シーダーを実行
- `--class=PostSeeder`：実行するシーダークラスを指定

---

### 🔧 ステップ3: HTTPライフサイクルログ記録ミドルウェアの作成

#### 何を考えているか
リクエストの流れを可視化するために、各段階でログを記録するミドルウェアを作成します。

#### コマンド

```bash
sail artisan make:middleware LogHttpLifecycle
```

**`app/Http/Middleware/LogHttpLifecycle.php`**

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class LogHttpLifecycle
{
    public function handle(Request $request, Closure $next)
    {
        // リクエストの前処理
        Log::info('=== HTTP Lifecycle Start ===');
        Log::info('1. Request received', [
            'url' => $request->url(),
            'method' => $request->method(),
        ]);

        Log::info('2. Middleware processing (before controller)');

        // 次のミドルウェアまたはコントローラーを実行
        $response = $next($request);

        // レスポンスの後処理
        Log::info('3. Middleware processing (after controller)');
        Log::info('4. Response ready', [
            'status' => $response->status(),
        ]);
        Log::info('=== HTTP Lifecycle End ===');

        return $response;
    }
}
```

**コードリーディング**：
- `handle(Request $request, Closure $next)`：ミドルウェアのメインメソッド
- `Log::info()`：ログを記録（`storage/logs/laravel.log`に保存）
- `$next($request)`：次のミドルウェアまたはコントローラーを実行
- `$response = $next($request)`：コントローラーの実行結果を取得
- `$response->status()`：HTTPステータスコード（200、404など）

---

### 🔧 ステップ4: 閲覧数カウントミドルウェアの作成

#### 何を考えているか
記事が表示された後に、閲覧数を自動的に増やすミドルウェアを作成します。

#### コマンド

```bash
sail artisan make:middleware CountPostViews
```

**`app/Http/Middleware/CountPostViews.php`**

```php
<?php

namespace App\Http\Middleware;

use App\Models\Post;
use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class CountPostViews
{
    public function handle(Request $request, Closure $next)
    {
        // コントローラーを実行
        $response = $next($request);

        // レスポンスの後処理（閲覧数をカウント）
        $postId = $request->route('id');
        
        if ($postId) {
            $post = Post::find($postId);
            
            if ($post) {
                $post->incrementViews();
                Log::info('Post views incremented', [
                    'post_id' => $postId,
                    'views' => $post->views
                ]);
            }
        }

        return $response;
    }
}
```

**コードリーディング**：
- `$request->route('id')`：ルートパラメータ`{id}`の値を取得
- `Post::find($postId)`：IDで記事を検索（見つからない場合はnull）
- `$post->incrementViews()`：閲覧数を1増やす

---

### 🔧 ステップ5: ミドルウェアを登録

#### 何を考えているか
作成したミドルウェアを、Laravelに登録します。

**`app/Http/Kernel.php`**

```php
protected $middlewareAliases = [
    // 既存のミドルウェア...
    'log.lifecycle' => \App\Http\Middleware\LogHttpLifecycle::class,
    'count.views' => \App\Http\Middleware\CountPostViews::class,
];
```

**コードリーディング**：
- `$middlewareAliases`：ルートで使えるミドルウェアのエイリアスを定義
- `'log.lifecycle'`：ルートで`->middleware('log.lifecycle')`と指定できる

---

### 🔧 ステップ6: コントローラーの作成

#### 何を考えているか
記事の一覧表示と詳細表示を行うコントローラーを作成します。

#### コマンド

```bash
sail artisan make:controller PostController
```

**`app/Http/Controllers/PostController.php`**

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class PostController extends Controller
{
    public function index()
    {
        Log::info('PostController@index called');
        
        $posts = Post::all();
        
        return view('posts.index', compact('posts'));
    }

    public function show($id)
    {
        Log::info('PostController@show called', ['post_id' => $id]);
        
        $post = Post::findOrFail($id);
        
        return view('posts.show', compact('post'));
    }
}
```

**コードリーディング**：
- `Post::all()`：全ての記事を取得
- `Post::findOrFail($id)`：IDで記事を検索（見つからない場合は404エラー）
- `view()`：Bladeテンプレートを返す

---

### 🔧 ステップ7: ルートの定義

#### 何を考えているか
Webルートを定義し、ミドルウェアを適用します。

**`routes/web.php`**

```php
<?php

use App\Http\Controllers\PostController;
use Illuminate\Support\Facades\Route;

// HTTPライフサイクルログを記録するミドルウェアを適用
Route::middleware(['log.lifecycle'])->group(function () {
    // 記事一覧
    Route::get('/posts', [PostController::class, 'index'])->name('posts.index');
    
    // 記事詳細（閲覧数カウントミドルウェアも適用）
    Route::middleware(['count.views'])->group(function () {
        Route::get('/posts/{id}', [PostController::class, 'show'])->name('posts.show');
    });
});
```

**コードリーディング**：
- `Route::middleware(['log.lifecycle'])->group()`：グループ内の全ルートにミドルウェアを適用
- ネストしたグループ：`log.lifecycle`と`count.views`の両方が適用される

---

### 🔧 ステップ8: ビューファイルの作成

#### 記事一覧ビュー

ターミナルで以下のコマンドを実行して、ディレクトリを作成します：

```bash
mkdir -p resources/views/posts
```

**`resources/views/posts/index.blade.php`**

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>記事一覧</title>
</head>
<body>
    <h1>記事一覧</h1>
    <ul>
        @foreach ($posts as $post)
            <li>
                <a href="{{ route('posts.show', $post->id) }}">{{ $post->title }}</a>
                (閲覧数: {{ $post->views }})
            </li>
        @endforeach
    </ul>
</body>
</html>
```

#### 記事詳細ビュー

**`resources/views/posts/show.blade.php`**

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{{ $post->title }}</title>
</head>
<body>
    <h1>{{ $post->title }}</h1>
    <p>{{ $post->content }}</p>
    <p>閲覧数: {{ $post->views }}</p>
    <a href="{{ route('posts.index') }}">一覧に戻る</a>
</body>
</html>
```

---

### 🚀 ステップ9: 動作確認

#### 記事一覧を表示

ブラウザで `http://localhost/posts` にアクセスします。

**期待される表示**：
- 記事のタイトル一覧が表示される
- 各記事の閲覧数が0と表示される

---

#### 記事詳細を表示

記事のタイトルをクリックして、`http://localhost/posts/1` にアクセスします。

**期待される表示**：
- 記事のタイトル、内容が表示される
- 閲覧数が1に増えている

**注目ポイント**：
`views`が1に増えています！

---

### 🔍 ログを確認

**`storage/logs/laravel.log`**

```
[2024-01-01 00:00:00] local.INFO: === HTTP Lifecycle Start ===
[2024-01-01 00:00:00] local.INFO: 1. Request received {"url":"http://localhost/posts/1","method":"GET"}
[2024-01-01 00:00:00] local.INFO: 2. Middleware processing (before controller)
[2024-01-01 00:00:00] local.INFO: PostController@show called {"post_id":"1"}
[2024-01-01 00:00:00] local.INFO: 3. Middleware processing (after controller)
[2024-01-01 00:00:00] local.INFO: Post views incremented {"post_id":"1","views":1}
[2024-01-01 00:00:00] local.INFO: 4. Response ready {"status":200}
[2024-01-01 00:00:00] local.INFO: === HTTP Lifecycle End ===
```

**ログから読み取れる流れ**：

1. リクエスト受信
2. ミドルウェア（前処理）
3. コントローラー実行
4. ミドルウェア（後処理）← ここで閲覧数をカウント
5. レスポンス送信

---

### 📊 HTTPライフサイクルの可視化

```
1. ユーザーがGET /posts/1にアクセス
   ↓
2. public/index.php（エントリーポイント）
   ↓
3. HTTPカーネル
   ↓
4. LogHttpLifecycle ミドルウェア（前処理）← ログ記録
   ↓
5. CountPostViews ミドルウェア（前処理）
   ↓
6. ルーター（routes/web.php）
   ↓
7. PostController@show 実行 ← ログ記録
   ↓
8. レスポンス生成（JSON）
   ↓
9. CountPostViews ミドルウェア（後処理）← 閲覧数カウント
   ↓
10. LogHttpLifecycle ミドルウェア（後処理）← ログ記録
   ↓
11. レスポンス送信
```

---

### ✨ 完成！

おめでとうございます！HTTPライフサイクル全体を体験できました。

**自分で作成したコードと比較してみましょう**：
- `lifecycle-app-practice/`: 自分で作成したプロジェクト
- `lifecycle-app-sample/`: 一緒に作成したプロジェクト

両方のプロジェクトを見比べて、違いがあれば確認してみてください。

---

### 💡 発展演習: レスポンスタイムを計測

#### ミドルウェアを改良

```php
public function handle(Request $request, Closure $next)
{
    $startTime = microtime(true);

    Log::info('=== HTTP Lifecycle Start ===');

    $response = $next($request);

    $endTime = microtime(true);
    $duration = ($endTime - $startTime) * 1000; // ミリ秒

    Log::info('Response time', ['duration' => round($duration, 2) . 'ms']);
    Log::info('=== HTTP Lifecycle End ===');

    return $response;
}
```

**コードリーディング**：
- `microtime(true)`：現在時刻を秒単位で取得（マイクロ秒精度）
- `($endTime - $startTime) * 1000`：経過時間をミリ秒に変換
- `round($duration, 2)`：小数点第2位まで丸める

---

## 🧪 動作確認の方法

### プロジェクトの切り替え

2つのプロジェクトを切り替えて動作確認する方法：

```bash
# lifecycle-app-practiceで確認したい場合
cd ~/coachtech/laravel-practice/10-2-5_hands-on/lifecycle-app-sample
./vendor/bin/sail down

cd ~/coachtech/laravel-practice/10-2-5_hands-on/lifecycle-app-practice
./vendor/bin/sail up -d

# lifecycle-app-sampleで確認したい場合
cd ~/coachtech/laravel-practice/10-2-5_hands-on/lifecycle-app-practice
./vendor/bin/sail down

cd ~/coachtech/laravel-practice/10-2-5_hands-on/lifecycle-app-sample
./vendor/bin/sail up -d
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ ミドルウェアを使って、リクエストの前後処理を実装した
- ✅ ログを記録して、HTTPライフサイクルを可視化した
- ✅ 閲覧数カウンターを実装して、ミドルウェアの後処理を体験した
- ✅ リクエストがどのように処理されるかを、実際のコードで確認した

引き続き、次のセクションも頑張りましょう！

### 🛑 Sailの停止

次のセクションに進む前に、Sailを停止しておきましょう。

```bash
./vendor/bin/sail down
```

> 💡 **なぜ停止するの？**: Sailを起動したままだと、次のセクションで別のプロジェクトを起動する際にポートが競合してエラーになることがあります。セクションの終わりには必ずSailを停止する習慣をつけましょう。

---
