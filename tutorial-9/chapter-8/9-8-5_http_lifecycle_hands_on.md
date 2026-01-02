# Tutorial 9-8-5: HTTPライフサイクル実践ハンズオン

## 🎯 このセクションで学ぶこと

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

*   実際に手を動かして、HTTPライフサイクル全体を体験する。
*   ミドルウェア、ルーティング、コントローラーの連携を実装する。
*   ログを使って、リクエストの流れを可視化する。

---

## 導入：理論を実践で確認する

前のセクションで、HTTPライフサイクルの理論を学びました。このセクションでは、**実際にコードを書いて**、リクエストがどのように処理されるかを体験します。

**このハンズオンで作るもの**：
ブログ記事の閲覧数カウンター機能を実装し、HTTPライフサイクルの各段階でログを記録します。

---

## 🏃 実践演習

### 📝 演習の目標

*   ブログ記事を表示する機能を作成する
*   ミドルウェアを使って、閲覧数をカウントする
*   ログを記録して、HTTPライフサイクルを可視化する

---

### 🔧 ステップ1: マイグレーションとモデルの作成

#### 何を考えているか
まず、ブログ記事を保存するためのデータベーステーブルを作成します。閲覧数を記録するために、`views`カラムを追加します。

#### コマンド

```bash
docker compose exec php php artisan make:migration create_posts_table
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
docker compose exec php php artisan migrate
```

---

#### モデルを作成

```bash
docker compose exec php php artisan make:model Post
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
docker compose exec php php artisan make:seeder PostSeeder
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
docker compose exec php php artisan db:seed --class=PostSeeder
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
docker compose exec php php artisan make:middleware LogHttpLifecycle
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
docker compose exec php php artisan make:middleware CountPostViews
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
docker compose exec php php artisan make:controller PostController
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
        
        return response()->json(['posts' => $posts]);
    }

    public function show($id)
    {
        Log::info('PostController@show called', ['post_id' => $id]);
        
        $post = Post::findOrFail($id);
        
        return response()->json(['post' => $post]);
    }
}
```

**コードリーディング**：
- `Post::all()`：全ての記事を取得
- `Post::findOrFail($id)`：IDで記事を検索（見つからない場合は404エラー）
- `response()->json()`：JSON形式でレスポンスを返す

---

### 🔧 ステップ7: ルートの定義

#### 何を考えているか
APIルートを定義し、ミドルウェアを適用します。

**`routes/api.php`**

```php
<?php

use App\Http\Controllers\PostController;
use Illuminate\Support\Facades\Route;

// HTTPライフサイクルログを記録するミドルウェアを適用
Route::middleware(['log.lifecycle'])->group(function () {
    // 記事一覧
    Route::get('/posts', [PostController::class, 'index']);
    
    // 記事詳細（閲覧数カウントミドルウェアも適用）
    Route::middleware(['count.views'])->group(function () {
        Route::get('/posts/{id}', [PostController::class, 'show']);
    });
});
```

**コードリーディング**：
- `Route::middleware(['log.lifecycle'])->group()`：グループ内の全ルートにミドルウェアを適用
- ネストしたグループ：`log.lifecycle`と`count.views`の両方が適用される

---

### 🚀 ステップ8: 動作確認

#### 記事一覧を取得

```bash
curl http://localhost/api/posts
```

**期待されるレスポンス**：

```json
{
    "posts": [
        {
            "id": 1,
            "title": "Laravelの基礎",
            "content": "Laravelは、PHPのWebアプリケーションフレームワークです。",
            "views": 0,
            "created_at": "2024-01-01T00:00:00.000000Z",
            "updated_at": "2024-01-01T00:00:00.000000Z"
        },
        ...
    ]
}
```

---

#### 記事詳細を表示

```bash
curl http://localhost/api/posts/1
```

**期待されるレスポンス**：

```json
{
    "post": {
        "id": 1,
        "title": "Laravelの基礎",
        "content": "Laravelは、PHPのWebアプリケーションフレームワークです。",
        "views": 1,
        "created_at": "2024-01-01T00:00:00.000000Z",
        "updated_at": "2024-01-01T00:00:00.000000Z"
    }
}
```

**注目ポイント**：
`views`が1に増えています！

---

### 🔍 ログを確認

**`storage/logs/laravel.log`**

```
[2024-01-01 00:00:00] local.INFO: === HTTP Lifecycle Start ===
[2024-01-01 00:00:00] local.INFO: 1. Request received {"url":"http://localhost/api/posts/1","method":"GET"}
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
1. ユーザーがGET /api/posts/1にアクセス
   ↓
2. public/index.php（エントリーポイント）
   ↓
3. HTTPカーネル
   ↓
4. LogHttpLifecycle ミドルウェア（前処理）← ログ記録
   ↓
5. CountPostViews ミドルウェア（前処理）
   ↓
6. ルーター（routes/api.php）
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

## ✨ 完成！

おめでとうございます！HTTPライフサイクル全体を体験できました。

**このハンズオンで学んだこと**：

*   ミドルウェアを使って、リクエストの前後処理を実装した
*   ログを記録して、HTTPライフサイクルを可視化した
*   閲覧数カウンターを実装して、ミドルウェアの後処理を体験した
*   リクエストがどのように処理されるかを、実際のコードで確認した

---
