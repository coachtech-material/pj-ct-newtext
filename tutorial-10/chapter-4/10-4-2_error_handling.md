# Tutorial 10-4-2: エラーハンドリング

## 🎯 このセクションで学ぶこと

*   Laravelのエラーハンドリングの仕組みを理解する。
*   カスタムエラーレスポンスを返せるようになる。
*   例外（Exception）を適切に処理できるようになる。

---

## 導入：エラーは「隠す」のではなく「適切に処理する」

開発中は、詳細なエラーメッセージが表示されることで、問題を素早く特定できます。しかし、本番環境では、エラーメッセージをそのままユーザーに表示してはいけません。なぜなら、以下のようなリスクがあるからです。

*   **セキュリティリスク**: データベースの構造やファイルパスが漏洩する
*   **ユーザー体験の悪化**: 技術的なエラーメッセージは、一般ユーザーには理解できない

そのため、本番環境では、エラーを適切に処理し、ユーザーにはわかりやすいメッセージを表示する必要があります。

---

## 詳細解説

### 🛡️ Laravelのエラーハンドリングの仕組み

Laravelでは、全ての例外（Exception）は、`app/Exceptions/Handler.php`で処理されます。このファイルをカスタマイズすることで、エラーレスポンスを制御できます。

#### デフォルトの動作

*   **開発環境（`APP_DEBUG=true`）**: 詳細なエラーページを表示
*   **本番環境（`APP_DEBUG=false`）**: シンプルなエラーページを表示

---

### 🔍 HTTPステータスコードとエラーレスポンス

REST APIでは、エラーが発生した際に、適切なHTTPステータスコードを返すことが重要です。

| ステータスコード | 意味 | 用途 |
|:---|:---|:---|
| `400 Bad Request` | リクエストが不正 | バリデーションエラー |
| `401 Unauthorized` | 認証が必要 | トークンが無効 |
| `403 Forbidden` | アクセス権限がない | 認可エラー |
| `404 Not Found` | リソースが見つからない | 存在しないIDを指定 |
| `422 Unprocessable Entity` | バリデーションエラー | Laravelのデフォルト |
| `500 Internal Server Error` | サーバー内部エラー | 予期しないエラー |

---

### 📝 カスタムエラーレスポンスの返し方

#### 方法1: `abort()`ヘルパー

```php
if (!$user) {
    abort(404, 'ユーザーが見つかりません');
}
```

これにより、404エラーが返されます。

#### 方法2: `response()->json()`

```php
if (!$user) {
    return response()->json([
        'message' => 'ユーザーが見つかりません'
    ], 404);
}
```

これにより、JSON形式で404エラーが返されます。

#### 方法3: カスタム例外をスロー

```php
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;

if (!$user) {
    throw new NotFoundHttpException('ユーザーが見つかりません');
}
```

---

### 🎨 API用のエラーレスポンスをカスタマイズする

`app/Exceptions/Handler.php`の`register`メソッドで、例外ごとのレスポンスをカスタマイズできます。

**`app/Exceptions/Handler.php`**

```php
<?php

namespace App\Exceptions;

use Illuminate\Foundation\Exceptions\Handler as ExceptionHandler;
use Illuminate\Database\Eloquent\ModelNotFoundException;
use Symfony\Component\HttpKernel\Exception\NotFoundHttpException;
use Throwable;

class Handler extends ExceptionHandler
{
    public function register(): void
    {
        // ModelNotFoundExceptionをカスタマイズ
        $this->renderable(function (ModelNotFoundException $e, $request) {
            if ($request->is('api/*')) {
                return response()->json([
                    'message' => '指定されたリソースが見つかりません'
                ], 404);
            }
        });

        // NotFoundHttpExceptionをカスタマイズ
        $this->renderable(function (NotFoundHttpException $e, $request) {
            if ($request->is('api/*')) {
                return response()->json([
                    'message' => 'エンドポイントが見つかりません'
                ], 404);
            }
        });
    }
}
```

**コードリーディング**

*   `$this->renderable()`: 特定の例外に対するレスポンスをカスタマイズします。
*   `ModelNotFoundException`: Eloquentで`findOrFail()`を使った際に、レコードが見つからない場合にスローされる例外。
*   `$request->is('api/*')`: APIルート（`/api/`で始まるURL）の場合のみ、カスタムレスポンスを返します。

---

### 🚨 バリデーションエラーのカスタマイズ

Laravelのバリデーションエラーは、デフォルトで以下の形式で返されます。

```json
{
  "message": "The given data was invalid.",
  "errors": {
    "email": [
      "The email field is required."
    ],
    "password": [
      "The password field is required."
    ]
  }
}
```

このメッセージを日本語化したり、形式を変更したりすることができます。

#### 日本語化

前のセクションで学んだように、`config/app.php`の`locale`を`ja`に設定し、日本語の言語ファイルをインストールすることで、バリデーションエラーメッセージが日本語になります。

---

### 🔒 本番環境でのエラー表示

本番環境では、`.env`ファイルの`APP_DEBUG`を`false`に設定します。

```
APP_DEBUG=false
```

これにより、詳細なエラーメッセージは表示されず、シンプルなエラーページが表示されます。

---

### 📧 エラー通知

本番環境で重大なエラーが発生した場合、開発者に通知を送ることができます。

#### Slackに通知を送る

`config/logging.php`で、Slackチャンネルを設定します。

```php
'channels' => [
    'slack' => [
        'driver' => 'slack',
        'url' => env('LOG_SLACK_WEBHOOK_URL'),
        'username' => 'Laravel Log',
        'emoji' => ':boom:',
        'level' => 'critical',
    ],
],
```

`.env`ファイルに、Slack Webhook URLを追加します。

```
LOG_SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

これにより、`critical`レベル以上のエラーがSlackに通知されます。

---

## 💡 TIP: カスタム例外を作成する

独自の例外クラスを作成することで、エラーハンドリングをより柔軟にできます。

```bash
docker compose exec php php artisan make:exception InsufficientBalanceException
```

**`app/Exceptions/InsufficientBalanceException.php`**

```php
<?php

namespace App\Exceptions;

use Exception;

class InsufficientBalanceException extends Exception
{
    public function render($request)
    {
        return response()->json([
            'message' => '残高が不足しています'
        ], 400);
    }
}
```

**使用例**

```php
if ($user->balance < $amount) {
    throw new InsufficientBalanceException();
}
```

---

## ✨ まとめ

このセクションでは、Laravelのエラーハンドリングの仕組みと、カスタムエラーレスポンスの返し方を学びました。

*   Laravelの全ての例外は、`app/Exceptions/Handler.php`で処理される。
*   `abort()`や`response()->json()`を使って、カスタムエラーレスポンスを返せる。
*   `Handler.php`の`renderable()`メソッドで、例外ごとのレスポンスをカスタマイズできる。
*   本番環境では、`APP_DEBUG=false`に設定し、詳細なエラーメッセージを隠す。
*   重大なエラーは、Slackなどに通知を送ることができる。

次のセクションでは、Laravelのテスト機能について学びます。

---
