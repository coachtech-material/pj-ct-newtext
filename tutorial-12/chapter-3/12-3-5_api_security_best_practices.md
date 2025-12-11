# Tutorial 12-3-5: APIセキュリティのベストプラクティス

## 🎯 このセクションで学ぶこと

*   レート制限の設定方法を学ぶ。
*   HTTPSの重要性を理解する。
*   APIキー管理のベストプラクティスを学ぶ。
*   その他のセキュリティ対策を理解する。

---

## 導入：なぜAPIセキュリティが重要なのか

APIは、**外部からアクセスできる**ため、セキュリティ対策が重要です。

*   **レート制限**: 過度なリクエストを防ぐ
*   **HTTPS**: 通信を暗号化する
*   **APIキー管理**: 機密情報を保護する

**適切なセキュリティ対策**を行うことで、APIを安全に運用できます。

---

## 詳細解説

### 🔍 レート制限とは

**レート制限**は、**一定時間内のリクエスト数を制限する**仕組みです。

**目的**:
*   **DoS攻撃を防ぐ**: 過度なリクエストを防ぐ
*   **サーバーの負荷を軽減する**: リソースを保護する
*   **不正な利用を防ぐ**: APIの悪用を防ぐ

---

### 🔍 Laravelでのレート制限

Laravelでは、**throttleミドルウェア**を使って、レート制限を設定できます。

**ファイル**: `routes/api.php`

```php
Route::middleware(['auth:sanctum', 'throttle:60,1'])->group(function () {
    Route::apiResource('tasks', TaskController::class);
});
```

**ポイント**:
*   `throttle:60,1`: 1分間に60リクエストまで
*   制限を超えると、**429 Too Many Requests**が返される

---

### 🔍 HTTPステータスコード: 429 Too Many Requests

**429 Too Many Requests**は、**リクエスト数が多すぎる**ことを示します。

**レスポンス例**:

```json
{
  "message": "Too Many Requests"
}
```

**ヘッダー**:

*   `X-RateLimit-Limit`: 制限数
*   `X-RateLimit-Remaining`: 残りのリクエスト数
*   `Retry-After`: 再試行までの秒数

---

### 🔍 実践演習: レート制限をテストしてください

Thunder Clientで、以下のリクエストを60回以上連続で送信してください。

*   メソッド: `GET`
*   URL: `http://localhost:8000/api/tasks`
*   Headers:
    *   キー: `Authorization`
    *   値: `Bearer トークン`

**期待されるレスポンス（61回目）**:

*   ステータスコード: `429 Too Many Requests`
*   ボディ: `{"message": "Too Many Requests"}`

---

### 🔍 レート制限をカスタマイズする

レート制限をカスタマイズできます。

**ファイル**: `app/Providers/RouteServiceProvider.php`

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

protected function configureRateLimiting()
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
}
```

**ポイント**:
*   `perMinute(60)`: 1分間に60リクエストまで
*   `by($request->user()?->id ?: $request->ip())`: ユーザーIDまたはIPアドレスで制限

---

### 🔍 HTTPSとは

**HTTPS**は、**HTTP over SSL/TLS**の略で、**通信を暗号化する**プロトコルです。

**なぜHTTPSが必要なのか**:
*   **盗聴を防ぐ**: 通信内容を暗号化する
*   **改ざんを防ぐ**: 通信内容の改ざんを検知する
*   **なりすましを防ぐ**: サーバーの正当性を確認する

**本番環境では、必ずHTTPSを使う**

---

### 🔍 HTTPSを強制する

Laravelでは、HTTPSを強制できます。

**ファイル**: `app/Providers/AppServiceProvider.php`

```php
use Illuminate\Support\Facades\URL;

public function boot()
{
    if ($this->app->environment('production')) {
        URL::forceScheme('https');
    }
}
```

---

### 🔍 APIキー管理のベストプラクティス

**APIキー**は、**外部APIにアクセスするための認証情報**です。

**ベストプラクティス**:

1.  **環境変数に保存する**: `.env`ファイルに保存する
2.  **コードに書かない**: ハードコーディングしない
3.  **Gitにコミットしない**: `.gitignore`に追加する
4.  **本番環境と開発環境で分ける**: 異なるAPIキーを使う

---

### 🔍 環境変数の使い方

**ファイル**: `.env`

```
STRIPE_KEY=sk_test_abcdefghijklmnopqrstuvwxyz
STRIPE_SECRET=sk_live_abcdefghijklmnopqrstuvwxyz
```

**ファイル**: `config/services.php`

```php
'stripe' => [
    'key' => env('STRIPE_KEY'),
    'secret' => env('STRIPE_SECRET'),
],
```

**使い方**:

```php
$stripeKey = config('services.stripe.key');
```

---

### 🔍 その他のセキュリティ対策

**1. CORS設定を適切に行う**

本番環境では、特定のオリジンだけを許可します。

```php
'allowed_origins' => [
    'https://example.com',
],
```

---

**2. バリデーションを徹底する**

すべてのリクエストでバリデーションを行います。

```php
$validated = $request->validate([
    'title' => 'required|max:255',
    'priority' => 'required|integer|min:1|max:5',
]);
```

---

**3. SQLインジェクションを防ぐ**

Eloquent ORMを使うと、SQLインジェクションを防げます。

```php
// ✅ 正しい（Eloquent ORM）
$tasks = Task::where('user_id', $userId)->get();

// ❌ 間違い（生のSQL）
$tasks = DB::select("SELECT * FROM tasks WHERE user_id = $userId");
```

---

**4. XSS攻撃を防ぐ**

Bladeテンプレートでは、`{{ }}`を使うと、自動的にエスケープされます。

```blade
{{-- ✅ 正しい --}}
{{ $task->title }}

{{-- ❌ 間違い --}}
{!! $task->title !!}
```

---

**5. CSRF攻撃を防ぐ**

APIでは、CSRFトークンは不要ですが、Webページでは必要です。

```blade
<form method="POST" action="/tasks">
    @csrf
    ...
</form>
```

---

**6. ログを記録する**

重要な操作は、ログに記録します。

```php
use Illuminate\Support\Facades\Log;

Log::info('Task created', ['task_id' => $task->id, 'user_id' => $user->id]);
```

---

**7. エラーメッセージを適切に返す**

本番環境では、詳細なエラーメッセージを隠します。

```php
if ($this->app->environment('production')) {
    return response()->json([
        'message' => 'An error occurred'
    ], 500);
}
```

---

### 💡 TIP: セキュリティヘッダーを追加する

セキュリティヘッダーを追加すると、セキュリティが向上します。

**ファイル**: `app/Http/Middleware/SecurityHeaders.php`

```php
<?php

namespace App\Http\Middleware;

use Closure;

class SecurityHeaders
{
    public function handle($request, Closure $next)
    {
        $response = $next($request);
        
        $response->headers->set('X-Content-Type-Options', 'nosniff');
        $response->headers->set('X-Frame-Options', 'DENY');
        $response->headers->set('X-XSS-Protection', '1; mode=block');
        
        return $response;
    }
}
```

**ファイル**: `app/Http/Kernel.php`

```php
protected $middleware = [
    // ...
    \App\Http\Middleware\SecurityHeaders::class,
];
```

---

### 🚨 よくある間違い

#### 間違い1: HTTPSを使わない

本番環境では、必ずHTTPSを使います。

```
// ❌ 間違い（本番環境）
http://example.com/api/tasks

// ✅ 正しい（本番環境）
https://example.com/api/tasks
```

---

#### 間違い2: APIキーをコードに書く

APIキーは、環境変数に保存します。

```php
// ❌ 間違い
$stripeKey = 'sk_test_abcdefghijklmnopqrstuvwxyz';

// ✅ 正しい
$stripeKey = config('services.stripe.key');
```

---

#### 間違い3: レート制限を設定しない

レート制限を設定しないと、DoS攻撃を受ける可能性があります。

```php
// ❌ 間違い
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('tasks', TaskController::class);
});

// ✅ 正しい
Route::middleware(['auth:sanctum', 'throttle:60,1'])->group(function () {
    Route::apiResource('tasks', TaskController::class);
});
```

---

## ✨ まとめ

このセクションでは、APIセキュリティのベストプラクティスを学びました。

*   レート制限を設定した。
*   HTTPSの重要性を理解した。
*   APIキー管理のベストプラクティスを学んだ。
*   その他のセキュリティ対策を理解した。

これで、Chapter 3（API認証とセキュリティ）は完了です。Tutorial 12（API開発基礎）の全19セクションが完成しました！

---

## 📝 学習のポイント

- [ ] レート制限を設定した。
- [ ] 429 Too Many Requestsを理解した。
- [ ] HTTPSの重要性を理解した。
- [ ] APIキーを環境変数に保存した。
- [ ] セキュリティヘッダーを追加した。

---

## 🎉 Tutorial 12の完了

Tutorial 12（API開発基礎）を完了しました！

このチュートリアルでは、以下のことを学びました。

*   **Chapter 1**: API開発の基礎（6セクション）
*   **Chapter 2**: RESTful APIの実装（7セクション）
*   **Chapter 3**: API認証とセキュリティ（5セクション）
*   **Chapter 4**: 外部API利用の実装（1セクション）

次のTutorial 13では、より高度なLaravelの機能について学びます。
