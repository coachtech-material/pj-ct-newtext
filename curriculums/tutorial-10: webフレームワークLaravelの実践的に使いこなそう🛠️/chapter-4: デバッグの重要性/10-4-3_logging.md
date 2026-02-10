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

### 🤔 なぜこのタイミングでログを学ぶのか？

ここまでのチュートリアルで、コントローラー、モデル、バリデーション、認証・認可など、Laravelの主要な機能を学んできました。実際のアプリケーション開発では、これらの機能が**正しく動作しているかを確認する**必要があります。

| 学習済みの内容 | ログが役立つ場面 |
|:---|:---|
| コントローラー | リクエストの処理開始・完了を記録 |
| モデル（Eloquent） | データベース操作の成功・失敗を記録 |
| バリデーション | バリデーションエラーの詳細を記録 |
| 認証・認可 | ログイン試行、アクセス拒否を記録 |

`dd()`や`dump()`は開発中に便利ですが、**本番環境では使用できません**。ログを使えば、本番環境でも問題の原因を追跡できます。

**ログを学ぶメリット**

*   **本番環境でのデバッグ**: `dd()`が使えない環境でも問題を追跡できる
*   **履歴の保存**: 過去に何が起きたかを後から確認できる
*   **チーム開発**: 他の開発者と問題の情報を共有できる
*   **セキュリティ監査**: 不正アクセスの試行を記録・検知できる

---

## 詳細解説

### 🔍 ログの基本

Laravelでは、`Log`ファサードを使って、ログを記録します。

```php
use Illuminate\Support\Facades\Log;

Log::info('This is an info message');
Log::error('This is an error message');
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `use Illuminate\Support\Facades\Log;` | Logファサードをインポートします。ファサードを使うことで、シンプルな構文でログを記録できます |
| `Log::info('...')` | `info`レベルでログを記録します。静的メソッドとして呼び出します |
| `Log::error('...')` | `error`レベルでログを記録します |

**構文解説**

```
Log::ログレベル('メッセージ');
Log::ログレベル('メッセージ', ['キー' => '値', ...]);
```

*   **第1引数**: ログメッセージ（文字列）
*   **第2引数**: コンテキスト情報（連想配列、省略可能）

**ログファイルの場所**

*   `storage/logs/laravel.log`

ログは上記のファイルに追記されていきます。ターミナルで以下のコマンドを実行すると、リアルタイムでログを確認できます。

```bash
tail -f storage/logs/laravel.log
```

---

### 🔍 ログレベル

Laravelでは、以下のログレベルが用意されています。**重要度の高い順**に並んでいます。

| ログレベル | 説明 | 使用例 |
|:---|:---|:---|
| `emergency` | システムが使用不可能 | データベースが完全にダウン |
| `alert` | 即座に対応が必要 | Webサイト全体がダウン |
| `critical` | 重大なエラー | アプリケーションコンポーネントが利用不可 |
| `error` | エラー | 例外が発生 |
| `warning` | 警告 | 非推奨のAPIを使用 |
| `notice` | 通常だが重要な情報 | ユーザーがログイン |
| `info` | 情報 | ユーザーが投稿を作成 |
| `debug` | デバッグ情報 | 変数の値を確認 |

**使い分けの目安**

*   **開発中のデバッグ**: `debug`
*   **通常の処理記録**: `info`
*   **注意が必要な状況**: `warning`
*   **エラー発生時**: `error`
*   **重大な問題**: `critical`、`alert`、`emergency`

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
| `auth()->id()` | 現在ログインしているユーザーのIDを取得するヘルパー関数です |
| `Log::info('Post created successfully', ['post_id' => $post->id])` | 投稿作成成功時に、作成された投稿のIDを記録します |

**処理の流れ**

1. 処理開始時に`Log::info()`でログを記録（誰が処理を開始したかを記録）
2. バリデーションとデータ作成を実行
3. 処理完了時に`Log::info()`でログを記録（作成された投稿のIDを記録）

**ログファイルの出力例**

```
[2024-01-01 12:00:00] local.INFO: Post creation started {"user_id":1}
[2024-01-01 12:00:01] local.INFO: Post created successfully {"post_id":42}
```

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
| `try { ... } catch (\Exception $e) { ... }` | try-catch構文で例外をキャッチします。`try`ブロック内でエラーが発生すると、`catch`ブロックが実行されます |
| `Post::findOrFail($id)` | 投稿が見つからない場合、`ModelNotFoundException`例外をスローします |
| `\Exception $e` | キャッチした例外オブジェクトを`$e`変数に格納します。`\`はグローバル名前空間を示します |
| `Log::error('Failed to retrieve post', [...])` | errorレベルでログを記録します。エラー発生時に使用します |
| `'post_id' => $id` | どの投稿IDでエラーが発生したかを記録します |
| `$e->getMessage()` | 例外のエラーメッセージを取得します |
| `$e->getTraceAsString()` | スタックトレース（エラーが発生するまでの呼び出し履歴）を文字列として取得します |

**構文解説: try-catch**

```php
try {
    // エラーが発生する可能性のある処理
} catch (例外クラス $変数) {
    // エラー発生時の処理
}
```

*   `try`ブロック内でエラーが発生すると、即座に`catch`ブロックに移動します
*   `catch`の引数で、キャッチする例外の種類を指定できます
*   `\Exception`は全ての例外の親クラスなので、全ての例外をキャッチできます

**ログファイルの出力例**

```
[2024-01-01 12:00:00] local.ERROR: Failed to retrieve post {"post_id":999,"error":"No query results for model [App\\Models\\Post] 999","trace":"#0 /var/www/html/vendor/laravel/framework/src/..."}
```

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
| `'ip' => request()->ip()` | リクエスト元のIPアドレスを記録します。不正アクセスの追跡に役立ちます |
| `'user_agent' => request()->userAgent()` | ブラウザやデバイスの情報（User-Agent）を記録します |
| `'timestamp' => now()` | ログイン時刻を記録します。`now()`は現在日時を返すヘルパー関数です |
| `request()` | 現在のHTTPリクエストオブジェクトを取得するヘルパー関数です |

**構文解説: ヘルパー関数**

| ヘルパー関数 | 説明 |
|:---|:---|
| `auth()` | 認証関連の機能にアクセスします |
| `auth()->id()` | ログインユーザーのIDを取得します |
| `request()` | 現在のリクエストオブジェクトを取得します |
| `request()->ip()` | クライアントのIPアドレスを取得します |
| `now()` | 現在の日時（Carbonオブジェクト）を取得します |

**ログファイルの出力例**

```
[2024-01-01 12:00:00] local.INFO: User logged in {"user_id":1,"ip":"192.168.1.1","user_agent":"Mozilla/5.0...","timestamp":"2024-01-01T12:00:00.000000Z"}
```

**コンテキスト情報を含めるメリット**

*   **問題の特定が容易**: どのユーザーが、どのIPから、いつアクセスしたかが分かる
*   **セキュリティ監査**: 不正アクセスの試行を追跡できる
*   **パフォーマンス分析**: 特定の条件下での問題を特定できる

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

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `'stack'` | 複数のチャンネルを組み合わせるドライバーです |
| `'single'` | 1つのファイルにログを記録します |
| `'daily'` | 日ごとにファイルを分けてログを記録します |
| `'slack'` | Slackにログを送信します |
| `storage_path('logs/laravel.log')` | `storage/logs/laravel.log`のパスを返すヘルパー関数です |
| `'level' => 'debug'` | このレベル以上のログを記録します |
| `'days' => 14` | 14日分のログファイルを保持します |

**使用例**

```php
// デフォルトチャンネルに記録
Log::info('Normal log');

// 特定のチャンネルに記録
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

**生成されるファイル例**

```
storage/logs/laravel-2024-01-01.log
storage/logs/laravel-2024-01-02.log
storage/logs/laravel-2024-01-03.log
```

**ローテーションのメリット**

*   ログファイルが肥大化しない
*   古いログが自動的に削除される
*   日付ごとに問題を追跡しやすい

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

> **⚠️ 注意**: パスワード、クレジットカード番号、APIキーなどの機密情報は絶対にログに記録しないでください。ログファイルは開発者がアクセスできるため、セキュリティリスクになります。

---

**間違い2: ログレベルを間違える**

```php
Log::info('Database connection failed'); // NG: errorを使うべき
```

**対処法**: 適切なログレベルを使います。

```php
Log::error('Database connection failed'); // OK
```

**ログレベルの選び方**

| 状況 | 適切なレベル |
|:---|:---|
| 処理の開始・完了 | `info` |
| 変数の値を確認 | `debug` |
| 例外が発生 | `error` |
| 非推奨機能の使用 | `warning` |
| システム停止レベルの問題 | `critical` |

---

## ✨ まとめ

このセクションでは、ログの活用方法を学びました。

*   `Log::info()`、`Log::error()`を使って、ログを記録できる。
*   ログレベルを理解し、適切に使い分けられる。
*   コンテキスト情報を含めることで、デバッグが容易になる。
*   ログチャンネルを使い分けることで、用途に応じたログ記録ができる。
*   機密情報はログに記録しないように注意する。

次のセクションでは、エラー画面の読み方とスタックトレースについて学びます。

---
