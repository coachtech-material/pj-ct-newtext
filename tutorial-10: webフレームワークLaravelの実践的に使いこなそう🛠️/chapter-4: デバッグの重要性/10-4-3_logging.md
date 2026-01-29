# Tutorial 10-4-3: ログの活用

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

投稿作成時に、処理の開始と完了をログに記録する例です。

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `use Illuminate\Support\Facades\Log;` | Logファサードをインポートします |
| `Log::info('Post creation started', [...])` | infoレベルでログを記録します。第1引数はメッセージ、第2引数はコンテキスト情報（配列） |
| `['user_id' => auth()->id()]` | コンテキスト情報として、ログインユーザーのIDを記録します |
| `Log::info('Post created successfully', ['post_id' => $post->id])` | 投稿作成成功時に、作成された投稿のIDを記録します |

---

### 🚀 実践例2: エラーログ

例外が発生した時に、エラー情報をログに記録する例です。

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `try { ... } catch (\Exception $e) { ... }` | try-catch構文で例外をキャッチします |
| `Post::findOrFail($id)` | 投稿が見つからない場合、`ModelNotFoundException`例外をスローします |
| `Log::error('Failed to retrieve post', [...])` | errorレベルでログを記録します。エラー発生時に使用します |
| `'post_id' => $id` | どの投稿IDでエラーが発生したかを記録します |
| `'error' => $e->getMessage()` | 例外のエラーメッセージを記録します |
| `'trace' => $e->getTraceAsString()` | スタックトレース（エラーが発生するまでの呼び出し履歴）を記録します |

---

### 🚀 実践例3: コンテキスト情報を含める

ユーザーのログイン時に、詳細なコンテキスト情報を記録する例です。

```php
Log::info('User logged in', [
    'user_id' => auth()->id(),
    'ip' => request()->ip(),
    'user_agent' => request()->userAgent(),
    'timestamp' => now(),
]);
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `'user_id' => auth()->id()` | ログインしたユーザーのIDを記録します |
| `'ip' => request()->ip()` | リクエスト元のIPアドレスを記録します |
| `'user_agent' => request()->userAgent()` | ブラウザやデバイスの情報（User-Agent）を記録します |
| `'timestamp' => now()` | ログイン時刻を記録します。`now()`は現在日時を返すヘルパー関数です |

**ログファイルの出力例**

```
[2024-01-01 12:00:00] local.INFO: User logged in {"user_id":1,"ip":"192.168.1.1","user_agent":"Mozilla/5.0...","timestamp":"2024-01-01T12:00:00.000000Z"}
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

### 🚨 よくある間違い

**間違い1: 機密情報をログに記録**

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

**間違い2: ログレベルを間違える**

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
