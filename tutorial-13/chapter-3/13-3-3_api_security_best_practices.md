# Tutorial 13-3-3: APIセキュリティのベストプラクティス

## 🎯 このセクションで学ぶこと

- レート制限の設定方法を学ぶ
- HTTPSの重要性を理解する
- APIキー管理のベストプラクティスを学ぶ
- その他のセキュリティ対策を理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ最後に『セキュリティベストプラクティス』を学ぶのか？」

API認証を実装したら、最後は「ベストプラクティス」です。

---

### 理由1: 実践的な知識の整理

これまで学んだセキュリティの知識を、**実践的なベストプラクティス**として整理します。

---

### 理由2: 本番環境への準備

開発環境と本番環境では、**セキュリティの要件が異なります**。

| 項目 | 開発環境 | 本番環境 |
|------|----------|----------|
| HTTPS | 任意 | 必須 |
| デバッグ | 有効 | 無効 |
| エラーメッセージ | 詳細 | 簡潔 |

---

### 理由3: 継続的なセキュリティ

セキュリティは**一度設定して終わり**ではありません。

| 対策 | 説明 |
|------|------|
| 定期的なアップデート | 脆弱性の修正 |
| 脆弱性のチェック | セキュリティ監査 |
| ログの監視 | 不正アクセスの検知 |

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | レート制限の設定 | DoS攻撃対策 |
| Step 2 | HTTPSの強制 | 通信の暗号化 |
| Step 3 | その他のセキュリティ対策 | 総合的な防御 |

> 💡 **ポイント**: セキュリティは「完璧」を目指すのではなく、「継続的な改善」が重要です。

---

## Step 1: レート制限の設定

### 1-1. レート制限とは

**レート制限**は、**一定時間内のリクエスト数を制限する**仕組みです。

| 目的 | 説明 |
|------|------|
| DoS攻撃を防ぐ | 過度なリクエストを防ぐ |
| サーバーの負荷を軽減 | リソースを保護する |
| 不正な利用を防ぐ | APIの悪用を防ぐ |

---

### 1-2. Laravelでのレート制限

**ファイル**: `routes/api.php`

```php
Route::middleware(['auth:sanctum', 'throttle:60,1'])->group(function () {
    Route::apiResource('tasks', TaskController::class);
});
```

| 設定 | 説明 |
|------|------|
| `throttle:60,1` | 1分間に60リクエストまで |
| 制限超過時 | 429 Too Many Requests |

---

### 1-3. レート制限のカスタマイズ

**ファイル**: `app/Providers/AppServiceProvider.php`

```php
use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Support\Facades\RateLimiter;

public function boot(): void
{
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });
}
```

---

### 1-4. 429 Too Many Requests

レート制限を超えた場合のレスポンス:

```json
{
  "message": "Too Many Requests"
}
```

**ヘッダー**:

| ヘッダー | 説明 |
|----------|------|
| X-RateLimit-Limit | 制限数 |
| X-RateLimit-Remaining | 残りのリクエスト数 |
| Retry-After | 再試行までの秒数 |

---

## Step 2: HTTPSの強制

### 2-1. HTTPSとは

**HTTPS**は、**HTTP over SSL/TLS**の略で、**通信を暗号化する**プロトコルです。

| メリット | 説明 |
|----------|------|
| 盗聴を防ぐ | 通信内容を暗号化 |
| 改ざんを防ぐ | 通信内容の改ざんを検知 |
| なりすましを防ぐ | サーバーの正当性を確認 |

**本番環境では、必ずHTTPSを使う**

---

### 2-2. HTTPSを強制する

**ファイル**: `app/Providers/AppServiceProvider.php`

```php
use Illuminate\Support\Facades\URL;

public function boot(): void
{
    if ($this->app->environment('production')) {
        URL::forceScheme('https');
    }
}
```

---

### 2-3. APIキー管理のベストプラクティス

| ルール | 説明 |
|--------|------|
| 環境変数に保存する | `.env`ファイルに保存 |
| コードに書かない | ハードコーディングしない |
| Gitにコミットしない | `.gitignore`に追加 |
| 環境ごとに分ける | 本番と開発で異なるキー |

**ファイル**: `.env`

```
STRIPE_KEY=sk_test_abcdefghijklmnopqrstuvwxyz
```

**使い方**:

```php
$stripeKey = config('services.stripe.key');
```

---

## Step 3: その他のセキュリティ対策

### 3-1. CORS設定を適切に行う

本番環境では、特定のオリジンだけを許可します。

```php
'allowed_origins' => [
    'https://example.com',
],
```

---

### 3-2. バリデーションを徹底する

すべてのリクエストでバリデーションを行います。

```php
$validated = $request->validate([
    'title' => 'required|max:255',
    'status' => 'required|in:pending,in_progress,completed',
]);
```

---

### 3-3. SQLインジェクションを防ぐ

Eloquent ORMを使うと、SQLインジェクションを防げます。

```php
// ✅ 正しい（Eloquent ORM）
$tasks = Task::where('user_id', $userId)->get();

// ❌ 間違い（生のSQL）
$tasks = DB::select("SELECT * FROM tasks WHERE user_id = $userId");
```

---

### 3-4. ログを記録する

重要な操作は、ログに記録します。

```php
use Illuminate\Support\Facades\Log;

Log::info('Task created', ['task_id' => $task->id, 'user_id' => $user->id]);
```

---

### 3-5. セキュリティヘッダーを追加する

**ファイル**: `app/Http/Middleware/SecurityHeaders.php`

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class SecurityHeaders
{
    public function handle(Request $request, Closure $next)
    {
        $response = $next($request);
        
        $response->headers->set('X-Content-Type-Options', 'nosniff');
        $response->headers->set('X-Frame-Options', 'DENY');
        $response->headers->set('X-XSS-Protection', '1; mode=block');
        
        return $response;
    }
}
```

---

### 3-6. エラーメッセージを適切に返す

本番環境では、詳細なエラーメッセージを隠します。

```php
// ❌ 危険（本番環境）
{
  "message": "SQLSTATE[42S02]: Base table or view not found"
}

// ✅ 安全（本番環境）
{
  "message": "An error occurred"
}
```

---

## 🚨 よくある間違い

### 間違い1: HTTPSを使わない

**問題**: 通信内容が盗聴される

```
// ❌ 間違い（本番環境）
http://example.com/api/tasks

// ✅ 正しい（本番環境）
https://example.com/api/tasks
```

---

### 間違い2: APIキーをコードに書く

**問題**: APIキーが漏洩する

```php
// ❌ 間違い
$stripeKey = 'sk_test_abcdefghijklmnopqrstuvwxyz';

// ✅ 正しい
$stripeKey = config('services.stripe.key');
```

---

### 間違い3: レート制限を設定しない

**問題**: DoS攻撃を受ける可能性

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

## 💡 TIP: セキュリティチェックリスト

| 項目 | 確認 |
|------|------|
| HTTPSを使用している | [ ] |
| レート制限を設定している | [ ] |
| APIキーを環境変数に保存している | [ ] |
| バリデーションを行っている | [ ] |
| Eloquent ORMを使用している | [ ] |
| ログを記録している | [ ] |
| 本番環境でデバッグを無効にしている | [ ] |

---

## ✨ まとめ

このセクションでは、APIセキュリティのベストプラクティスを学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | レート制限の設定とカスタマイズ |
| Step 2 | HTTPSの強制とAPIキー管理 |
| Step 3 | その他のセキュリティ対策 |

これで、Chapter 3（API認証とセキュリティ）は完了です。

---
## 🎉 Tutorial 13 Chapter 3の完了

Chapter 3（API認証とセキュリティ）を完了しました！

このチャプターでは、以下のことを学びました。

| セクション | 内容 |
|:---|:---|
| 13-3-1 | API認証の仕組み（概念理解） |
| 13-3-2 | APIのセキュリティ対策 |
| 13-3-3 | APIセキュリティのベストプラクティス |

> **📌 重要なポイント**
> 
> このカリキュラムでは、API認証（Sanctum）の**実装**は扱いません。
> 概念を理解した上で、必要に応じて公式ドキュメントを参照してください。

次のChapter 4では、外部APIの利用について学びます。
