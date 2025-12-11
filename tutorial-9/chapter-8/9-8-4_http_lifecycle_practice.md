# Tutorial 9-8-4: 実践: HTTPライフサイクルを体験しよう

## 🎯 このセクションで学ぶこと

*   小さな実践演習を通じて、リクエストからレスポンスまでの流れを体験する。
*   ミドルウェア、ルーティング、コントローラー、レスポンスの連携を理解する。
*   実際に手を動かして、HTTPライフサイクルを体感する。

---

## 導入：「理論」から「実践」へ

これまで、HTTPライフサイクル、ミドルウェア、ルーティング、コントローラーについて学んできました。このセクションでは、**小さな実践演習**を通じて、これらの概念を統合し、リクエストからレスポンスまでの流れを体験します。

---

## 実践演習: ブログ記事の閲覧数カウンター

### 📝 演習の目標

*   ブログ記事を表示するAPIを作成する
*   ミドルウェアを使って、閲覧数をカウントする
*   ログを記録して、HTTPライフサイクルを可視化する

---

### 🔧 ステップ1: マイグレーションとモデルの作成

#### マイグレーション

```bash
php artisan make:migration create_posts_table
```

**`database/migrations/xxxx_create_posts_table.php`**

```php
public function up()
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->string('title');
        $table->text('content');
        $table->integer('views')->default(0);
        $table->timestamps();
    });
}
```

```bash
php artisan migrate
```

---

#### モデル

```bash
php artisan make:model Post
```

**`app/Models/Post.php`**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    protected $fillable = ['title', 'content', 'views'];

    public function incrementViews()
    {
        $this->increment('views');
    }
}
```

---

### 🔧 ステップ2: シーダーでテストデータを作成

```bash
php artisan make:seeder PostSeeder
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

```bash
php artisan db:seed --class=PostSeeder
```

---

### 🔧 ステップ3: ログ記録ミドルウェアの作成

```bash
php artisan make:middleware LogHttpLifecycle
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

        Log::info('2. Middleware processing');

        $response = $next($request);

        // レスポンスの後処理
        Log::info('3. Controller executed');
        Log::info('4. Response sent', [
            'status' => $response->status(),
        ]);
        Log::info('=== HTTP Lifecycle End ===');

        return $response;
    }
}
```

---

### 🔧 ステップ4: 閲覧数カウントミドルウェアの作成

```bash
php artisan make:middleware CountPostViews
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
        $response = $next($request);

        // レスポンスの後処理
        $postId = $request->route('id');
        
        if ($postId) {
            $post = Post::find($postId);
            
            if ($post) {
                $post->incrementViews();
                Log::info('Post views incremented', ['post_id' => $postId, 'views' => $post->views]);
            }
        }

        return $response;
    }
}
```

---

### 🔧 ステップ5: ミドルウェアを登録

**`app/Http/Kernel.php`**

```php
protected $middlewareAliases = [
    'log.lifecycle' => \App\Http\Middleware\LogHttpLifecycle::class,
    'count.views' => \App\Http\Middleware\CountPostViews::class,
];
```

---

### 🔧 ステップ6: コントローラーの作成

```bash
php artisan make:controller PostController
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

---

### 🔧 ステップ7: ルートの定義

**`routes/api.php`**

```php
use App\Http\Controllers\PostController;

Route::middleware(['log.lifecycle'])->group(function () {
    Route::get('/posts', [PostController::class, 'index']);
    
    Route::middleware(['count.views'])->group(function () {
        Route::get('/posts/{id}', [PostController::class, 'show']);
    });
});
```

---

### 🚀 ステップ8: 動作確認

#### リクエスト1: 記事一覧を取得

```
GET http://localhost/api/posts
```

#### レスポンス

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

#### リクエスト2: 記事を表示

```
GET http://localhost/api/posts/1
```

#### レスポンス

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

---

### 🔍 ログを確認

**`storage/logs/laravel.log`**

```
[2024-01-01 00:00:00] local.INFO: === HTTP Lifecycle Start ===
[2024-01-01 00:00:00] local.INFO: 1. Request received {"url":"http://localhost/api/posts/1","method":"GET"}
[2024-01-01 00:00:00] local.INFO: 2. Middleware processing
[2024-01-01 00:00:00] local.INFO: PostController@show called {"post_id":"1"}
[2024-01-01 00:00:00] local.INFO: 3. Controller executed
[2024-01-01 00:00:00] local.INFO: Post views incremented {"post_id":"1","views":1}
[2024-01-01 00:00:00] local.INFO: 4. Response sent {"status":200}
[2024-01-01 00:00:00] local.INFO: === HTTP Lifecycle End ===
```

---

### 📊 HTTPライフサイクルの流れ

```
1. リクエスト受信
   ↓
2. LogHttpLifecycle ミドルウェア（前処理）
   ↓
3. CountPostViews ミドルウェア（前処理）
   ↓
4. ルーティング
   ↓
5. PostController@show 実行
   ↓
6. レスポンス生成
   ↓
7. CountPostViews ミドルウェア（後処理）← 閲覧数をカウント
   ↓
8. LogHttpLifecycle ミドルウェア（後処理）
   ↓
9. レスポンス送信
```

---

### 💡 TIP: 閲覧数が増えることを確認

同じ記事に複数回アクセスすると、閲覧数が増えることを確認できます。

```
GET http://localhost/api/posts/1  → views: 1
GET http://localhost/api/posts/1  → views: 2
GET http://localhost/api/posts/1  → views: 3
```

---

### 🚀 発展演習: レスポンスタイムを計測

#### ミドルウェアの改良

```php
public function handle(Request $request, Closure $next)
{
    $startTime = microtime(true);

    Log::info('=== HTTP Lifecycle Start ===');

    $response = $next($request);

    $endTime = microtime(true);
    $duration = ($endTime - $startTime) * 1000; // ミリ秒

    Log::info('Response time', ['duration' => $duration . 'ms']);
    Log::info('=== HTTP Lifecycle End ===');

    return $response;
}
```

---

## ✨ まとめ

このセクションでは、小さな実践演習を通じて、HTTPライフサイクルを体験しました。

*   ミドルウェアを使って、リクエストの前後処理を実装した。
*   ログを記録して、HTTPライフサイクルを可視化した。
*   閲覧数カウンターを実装して、ミドルウェアの後処理を体験した。

これで、Chapter 8「HTTPライフサイクルとミドルウェア」の全4セクションが完了しました。次は、Chapter 9「認可とポリシー」の残りのセクションを執筆します。

---

## 📝 学習のポイント

- [ ] ミドルウェアを使って、リクエストの前後処理を実装できた。
- [ ] ログを記録して、HTTPライフサイクルを可視化できた。
- [ ] 閲覧数カウンターを実装して、ミドルウェアの後処理を体験できた。
- [ ] HTTPライフサイクルの流れを理解できた。
