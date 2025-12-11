# Tutorial 9-10-3: ログの活用

## 🎯 このセクションで学ぶこと

*   `Log::info()`、`Log::error()`を使って、ログを記録できるようになる。
*   ログレベルを理解し、適切に使い分けられるようになる。
*   ログファイルを確認し、デバッグに活用できるようになる。

---

## 導入：「ログ」とは何か？

アプリケーションを開発していると、**何が起きているのかを記録したい**場面があります。例えば、以下のような状況です。

*   エラーが発生した時に、詳細な情報を記録したい
*   ユーザーがどのような操作を行ったかを記録したい
*   APIのリクエストとレスポンスを記録したい

Laravelでは、**ログ**を使って、これらの情報を記録できます。

---

## 詳細解説

### 🔍 ログの基本

Laravelでは、`Log`ファサードを使って、ログを記録します。

```php
use Illuminate\Support\Facades\Log;

Log::info('This is an info message');
Log::error('This is an error message');
```

**ログファイル**

*   `storage/logs/laravel.log`

---

### 🔍 ログレベル

Laravelでは、以下のログレベルが用意されています。

| ログレベル | 説明 | 使用例 |
|------------|------|--------|
| `emergency` | システムが使用不可能 | データベースが完全にダウン |
| `alert` | 即座に対応が必要 | Webサイト全体がダウン |
| `critical` | 重大なエラー | アプリケーションコンポーネントが利用不可 |
| `error` | エラー | 例外が発生 |
| `warning` | 警告 | 非推奨のAPIを使用 |
| `notice` | 通常だが重要な情報 | ユーザーがログイン |
| `info` | 情報 | ユーザーが投稿を作成 |
| `debug` | デバッグ情報 | 変数の値を確認 |

---

### 🚀 実践例1: 基本的なログ記録

```php
use Illuminate\Support\Facades\Log;

public function store(Request $request)
{
    Log::info('Post creation started', ['user_id' => auth()->id()]);

    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'content' => 'required|string',
    ]);

    $post = $request->user()->posts()->create($validated);

    Log::info('Post created successfully', ['post_id' => $post->id]);

    return response()->json(['message' => 'Post created successfully', 'post' => $post], 201);
}
```

---

### 🚀 実践例2: エラーログ

```php
public function show($id)
{
    try {
        $post = Post::findOrFail($id);

        return response()->json(['post' => $post]);
    } catch (\Exception $e) {
        Log::error('Failed to retrieve post', [
            'post_id' => $id,
            'error' => $e->getMessage(),
            'trace' => $e->getTraceAsString(),
        ]);

        return response()->json(['message' => 'Post not found'], 404);
    }
}
```

---

### 🚀 実践例3: コンテキスト情報を含める

```php
Log::info('User logged in', [
    'user_id' => auth()->id(),
    'ip' => request()->ip(),
    'user_agent' => request()->userAgent(),
    'timestamp' => now(),
]);
```

---

### 🚀 実践例4: 条件付きログ

```php
if (config('app.debug')) {
    Log::debug('Debug information', [
        'request' => $request->all(),
        'user' => auth()->user(),
    ]);
}
```

---

### 💡 TIP: ログチャンネル

Laravelでは、複数のログチャンネルを使い分けることができます。

**`config/logging.php`**

```php
'channels' => [
    'stack' => [
        'driver' => 'stack',
        'channels' => ['single'],
    ],

    'single' => [
        'driver' => 'single',
        'path' => storage_path('logs/laravel.log'),
        'level' => 'debug',
    ],

    'daily' => [
        'driver' => 'daily',
        'path' => storage_path('logs/laravel.log'),
        'level' => 'debug',
        'days' => 14,
    ],

    'slack' => [
        'driver' => 'slack',
        'url' => env('LOG_SLACK_WEBHOOK_URL'),
        'username' => 'Laravel Log',
        'emoji' => ':boom:',
        'level' => 'critical',
    ],
];
```

**使用例**

```php
Log::channel('slack')->critical('Something went wrong!');
```

---

### 🚀 実践例5: カスタムログファイル

```php
Log::build([
    'driver' => 'single',
    'path' => storage_path('logs/custom.log'),
])->info('This is a custom log');
```

---

### 🚀 実践例6: ログのフォーマット

```php
Log::info('User action', [
    'action' => 'create_post',
    'user_id' => auth()->id(),
    'post_id' => $post->id,
    'timestamp' => now()->toDateTimeString(),
]);
```

**ログファイル**

```
[2024-01-01 12:00:00] local.INFO: User action {"action":"create_post","user_id":1,"post_id":10,"timestamp":"2024-01-01 12:00:00"}
```

---

### 🚀 実践例7: ミドルウェアでログ記録

**`app/Http/Middleware/LogRequests.php`**

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;

class LogRequests
{
    public function handle(Request $request, Closure $next)
    {
        Log::info('Request received', [
            'url' => $request->url(),
            'method' => $request->method(),
            'ip' => $request->ip(),
        ]);

        $response = $next($request);

        Log::info('Response sent', [
            'status' => $response->status(),
        ]);

        return $response;
    }
}
```

---

### 💡 TIP: ログのローテーション

`daily`ドライバーを使うと、ログファイルが日ごとに作成されます。

**`config/logging.php`**

```php
'daily' => [
    'driver' => 'daily',
    'path' => storage_path('logs/laravel.log'),
    'level' => 'debug',
    'days' => 14, // 14日間保存
],
```

---

### 🚀 実践例8: 例外をログに記録

**`app/Exceptions/Handler.php`**

```php
public function report(Throwable $exception)
{
    if ($this->shouldReport($exception)) {
        Log::error('Exception occurred', [
            'message' => $exception->getMessage(),
            'file' => $exception->getFile(),
            'line' => $exception->getLine(),
            'trace' => $exception->getTraceAsString(),
        ]);
    }

    parent::report($exception);
}
```

---

### 🚨 よくある間違い

#### 間違い1: 機密情報をログに記録

```php
Log::info('User logged in', [
    'password' => $request->password, // NG: パスワードをログに記録しない
]);
```

**対処法**: 機密情報は記録しません。

```php
Log::info('User logged in', [
    'user_id' => auth()->id(),
    'ip' => request()->ip(),
]);
```

---

#### 間違い2: ログレベルを間違える

```php
Log::info('Database connection failed'); // NG: errorを使うべき
```

**対処法**: 適切なログレベルを使います。

```php
Log::error('Database connection failed'); // OK
```

---

## ✨ まとめ

このセクションでは、ログの活用方法を学びました。

*   `Log::info()`、`Log::error()`を使って、ログを記録できる。
*   ログレベルを理解し、適切に使い分けられる。
*   コンテキスト情報を含めることで、デバッグが容易になる。
*   ログチャンネルを使い分けることで、用途に応じたログ記録ができる。

次のセクションでは、エラー画面の読み方とスタックトレースについて学びます。

---

## 📝 学習のポイント

- [ ] `Log::info()`、`Log::error()`を使って、ログを記録できる。
- [ ] ログレベルを理解し、適切に使い分けられる。
- [ ] コンテキスト情報を含めることで、デバッグが容易になる。
- [ ] ログファイルを確認し、デバッグに活用できる。
