# Tutorial 13-3-2: APIのセキュリティ対策

## 🎯 このセクションで学ぶこと

- APIのセキュリティリスクを理解する
- レート制限（Rate Limiting）の実装方法を学ぶ
- APIのセキュリティベストプラクティスを理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜSanctum導入の後に『APIセキュリティ』を学ぶのか？」

Sanctumを導入したら、次は「APIセキュリティ」です。

---

### 理由1: 認証だけでは不十分

認証は「誰がアクセスしているか」を確認するだけです。

APIのセキュリティには、**他にも考慮すべき点**があります。

| 対策 | 説明 |
|------|------|
| レート制限 | DoS攻撃対策 |
| 入力値の検証 | インジェクション対策 |
| HTTPSの使用 | 通信の暗号化 |
| 機密情報の保護 | APIキーの管理 |

---

### 理由2: 攻撃パターンを知る

APIに対する**一般的な攻撃パターン**を知っておくことが重要です。

| 攻撃 | 説明 |
|------|------|
| インジェクション攻撃 | SQLインジェクションなど |
| 認証の突破 | ブルートフォース攻撃 |
| 過剰なデータ露出 | 不要な情報を返す |

---

### 理由3: 防御策を実装

攻撃パターンを知ったら、**防御策を実装**します。

Laravelには、多くのセキュリティ機能が組み込まれています。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | レート制限の設定 | DoS攻撃対策 |
| Step 2 | 入力値の検証 | インジェクション対策 |
| Step 3 | 認可の実装 | 権限チェック |

> 💡 **ポイント**: セキュリティは「後から追加」ではなく、最初から考慮すべきです。

---

## Step 1: レート制限の設定

### 1-1. レート制限（Rate Limiting）とは

**レート制限**とは、**一定時間内にAPIにアクセスできる回数を制限する仕組み**です。

| メリット | 説明 |
|----------|------|
| DDoS攻撃を防ぐ | 大量のリクエストを防ぐ |
| サーバーの負荷を軽減 | 過度なアクセスを防ぐ |
| 公平性を保つ | 特定のユーザーがAPIを独占することを防ぐ |

---

### 1-2. Laravelのレート制限

Laravelでは、デフォルトでAPIにレート制限が適用されています。

**ファイル**: `bootstrap/app.php`

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->api(prepend: [
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    ]);

    // レート制限の設定
    $middleware->throttleApi();
})
```

---

### 1-3. レート制限の設定

デフォルトでは、**1分間に60回**までのリクエストが許可されています。

**ファイル**: `app/Providers/AppServiceProvider.php`

```php
<?php

namespace App\Providers;

use Illuminate\Cache\RateLimiting\Limit;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\RateLimiter;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    public function boot(): void
    {
        RateLimiter::for('api', function (Request $request) {
            return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
        });
    }
}
```

---

### 1-4. コードリーディング

| コード | 説明 |
|--------|------|
| `Limit::perMinute(60)` | 1分間に60回までのリクエストを許可 |
| `->by($request->user()?->id ?: $request->ip())` | ユーザーIDまたはIPアドレスで制限 |

---

### 1-5. レート制限のカスタマイズ

特定のエンドポイントに対して、異なるレート制限を適用することもできます。

```php
// ログインエンドポイント: 1分間に5回
RateLimiter::for('login', function (Request $request) {
    return Limit::perMinute(5)->by($request->ip());
});
```

**ルーティング**:

```php
Route::post('/login', [AuthController::class, 'login'])->middleware('throttle:login');
```

---

### 1-6. レート制限超過時のレスポンス

レート制限を超えた場合、以下のようなレスポンスが返されます。

```json
{
  "message": "Too Many Attempts."
}
```

HTTPステータスコード: `429 Too Many Requests`

---

## Step 2: 入力値の検証

### 2-1. バリデーションの重要性

APIでは、**必ず入力値のバリデーション**を行ってください。

| リスク | 説明 |
|--------|------|
| SQLインジェクション | データベースが不正に操作される |
| XSS | 悪意のあるスクリプトが実行される |

```php
$request->validate([
    'title' => 'required|string|max:255',
    'description' => 'nullable|string',
    'due_date' => 'nullable|date',
]);
```

---

### 2-2. SQLインジェクション対策

Laravelの**Eloquent ORM**を使うことで、SQLインジェクションを防ぐことができます。

```php
// ❌ 危険
$tasks = DB::select("SELECT * FROM tasks WHERE user_id = {$userId}");

// ✅ 安全
$tasks = Task::where('user_id', $userId)->get();
```

---

### 2-3. XSS（Cross-Site Scripting）対策

Laravelでは、**Bladeテンプレート**を使うことで、XSSを防ぐことができます。

```php
// ❌ 危険
{!! $task->title !!}

// ✅ 安全
{{ $task->title }}
```

`{{ }}`を使うことで、HTMLタグがエスケープされます。

---

### 2-4. HTTPSの使用

APIは、**必ずHTTPSを使用**してください。

| メリット | 説明 |
|----------|------|
| 通信内容が暗号化される | 第三者に盗聴されない |
| 中間者攻撃を防ぐ | 通信内容が改ざんされない |

---

## Step 3: 認可の実装

### 3-1. 認証と認可の違い

| 概念 | 説明 |
|------|------|
| 認証（Authentication） | ユーザーが誰であるかを確認する |
| 認可（Authorization） | ユーザーが何をできるかを確認する |

---

### 3-2. 認可の実装例

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function update(Request $request, string $id): JsonResponse
{
    $task = Task::findOrFail($id);

    // 認可チェック: 自分のタスクのみを更新できる
    if ($task->user_id !== Auth::id()) {
        return response()->json([
            'message' => 'このタスクを更新する権限がありません'
        ], 403);
    }

    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'description' => 'nullable|string',
        'status' => 'required|in:pending,in_progress,completed',
    ]);

    $task->update($validated);

    return response()->json(['data' => $task], 200);
}
```

---

### 3-3. APIキーの管理

APIキーやシークレットキーは、**絶対にコードに直接書かない**でください。

```php
// ❌ 危険
$apiKey = 'sk_live_abcdefghijklmnopqrstuvwxyz';

// ✅ 安全
$apiKey = env('STRIPE_API_KEY');
```

---

### 3-4. ログの記録

APIでは、**ログを記録する**ことが重要です。

```php
use Illuminate\Support\Facades\Log;

Log::info('Task created', ['task_id' => $task->id, 'user_id' => Auth::id()]);
```

| メリット | 説明 |
|----------|------|
| 不正アクセスを検知できる | 異常なアクセスパターンを発見 |
| デバッグがしやすい | エラーの原因を特定 |

---

## 🚨 よくある間違い

### 間違い1: HTTPSを使わない

**問題**: 通信内容が盗聴される

**対処法**: 本番環境では、必ずHTTPSを使用します。

---

### 間違い2: バリデーションを行わない

**問題**: SQLインジェクションやXSSの危険性

**対処法**: 全ての入力値に対して、バリデーションを行います。

---

### 間違い3: エラーメッセージに詳細な情報を含める

**問題**: システムの内部情報が漏洩する

```php
// ❌ 危険
{
  "message": "SQLSTATE[42S02]: Base table or view not found"
}

// ✅ 安全
{
  "message": "サーバーエラーが発生しました"
}
```

---

## 💡 TIP: CSRF対策

APIでは、通常**CSRFトークンは使用しません**。

代わりに、**トークンベース認証**を使います。

Sanctumを使うことで、CSRF対策が自動的に行われます。

---

## ✨ まとめ

このセクションでは、APIのセキュリティ対策について学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | レート制限の設定とカスタマイズ |
| Step 2 | 入力値の検証とインジェクション対策 |
| Step 3 | 認可の実装とAPIキーの管理 |

次のセクションでは、ログインAPIとトークンについて学びます。

---
