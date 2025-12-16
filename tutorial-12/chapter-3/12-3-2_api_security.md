# Tutorial 12-3-2: APIのセキュリティ対策

## 🎯 このセクションで学ぶこと

*   APIのセキュリティリスクを理解する。
*   レート制限（Rate Limiting）の実装方法を学ぶ。
*   APIのセキュリティベストプラクティスを理解する。

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜSanctum導入の後に『APIセキュリティ』を学ぶのか？」

Sanctumを導入したら、次は「APIセキュリティ」です。

---

### 理由1: 認証だけでは不十分

認証は「誰がアクセスしているか」を確認するだけです。

APIのセキュリティには、**他にも考慮すべき点**があります。

- レート制限（DoS攻撃対策）
- 入力値の検証
- HTTPSの使用
- 機密情報の保護

---

### 理由2: 攻撃パターンを知る

APIに対する**一般的な攻撃パターン**を知っておくことが重要です。

- インジェクション攻撃
- 認証の突破
- 過剰なデータ露出

---

### 理由3: 防御策を実装

攻撃パターンを知ったら、**防御策を実装**します。

Laravelには、多くのセキュリティ機能が組み込まれています。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| 1 | APIセキュリティの脅威を理解 | 何から守るべきかを知る |
| 2 | レート制限の設定 | DoS攻撃対策 |
| 3 | 入力値の検証 | インジェクション対策 |

> 💡 **ポイント**: セキュリティは「後から追加」ではなく、最初から考慮すべきです。

---

## 導入：APIのセキュリティ

APIは、外部からアクセスできるため、**セキュリティ対策が非常に重要**です。

適切なセキュリティ対策を行わないと、以下のようなリスクがあります。

*   **不正アクセス**: 認証されていないユーザーがデータにアクセスする
*   **DDoS攻撃**: 大量のリクエストでサーバーをダウンさせる
*   **データ漏洩**: 機密情報が外部に漏れる

このセクションでは、APIのセキュリティ対策について学びます。

---

## 詳細解説

### 🔍 レート制限（Rate Limiting）とは

**レート制限（Rate Limiting）**とは、**一定時間内にAPIにアクセスできる回数を制限する仕組み**です。

レート制限を実装することで、以下のようなメリットがあります。

*   **DDoS攻撃を防ぐ**: 大量のリクエストを防ぐことができる
*   **サーバーの負荷を軽減する**: 過度なアクセスを防ぐことができる
*   **公平性を保つ**: 特定のユーザーがAPIを独占することを防ぐ

---

### 🔍 Laravelのレート制限

Laravelでは、デフォルトでAPIにレート制限が適用されています。

**ファイル**: `bootstrap/app.php`

```php
->withMiddleware(function (Middleware $middleware) {
    $middleware->api(prepend: [
        \Laravel\Sanctum\Http\Middleware\EnsureFrontendRequestsAreStateful::class,
    ]);

    $middleware->alias([
        'verified' => \App\Http\Middleware\EnsureEmailIsVerified::class,
    ]);

    // レート制限の設定
    $middleware->throttleApi();
})
```

---

### 🔍 レート制限の設定

デフォルトでは、**1分間に60回**までのリクエストが許可されています。

この設定を変更する場合は、`app/Providers/AppServiceProvider.php`で設定します。

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

### 🔍 コードリーディング

#### `Limit::perMinute(60)`

*   1分間に60回までのリクエストを許可します。

---

#### `->by($request->user()?->id ?: $request->ip())`

*   認証済みユーザーの場合は、ユーザーIDでレート制限を適用します。
*   未認証ユーザーの場合は、IPアドレスでレート制限を適用します。

---

### 🔍 レート制限のカスタマイズ

特定のエンドポイントに対して、異なるレート制限を適用することもできます。

**ファイル**: `app/Providers/AppServiceProvider.php`

```php
public function boot(): void
{
    // 通常のAPIエンドポイント: 1分間に60回
    RateLimiter::for('api', function (Request $request) {
        return Limit::perMinute(60)->by($request->user()?->id ?: $request->ip());
    });

    // ログインエンドポイント: 1分間に5回
    RateLimiter::for('login', function (Request $request) {
        return Limit::perMinute(5)->by($request->ip());
    });
}
```

---

**ファイル**: `routes/api.php`

```php
Route::post('/login', [AuthController::class, 'login'])->middleware('throttle:login');
```

---

### 🔍 レート制限超過時のレスポンス

レート制限を超えた場合、以下のようなレスポンスが返されます。

```json
{
  "message": "Too Many Attempts."
}
```

HTTPステータスコード: `429 Too Many Requests`

---

### 🔍 HTTPS の使用

APIは、**必ずHTTPSを使用**してください。

HTTPSを使用することで、以下のようなメリットがあります。

*   **通信内容が暗号化される**: 第三者に盗聴されない
*   **中間者攻撃を防ぐ**: 通信内容が改ざんされない

---

### 🔍 入力値のバリデーション

APIでは、**必ず入力値のバリデーション**を行ってください。

バリデーションを行わないと、以下のようなリスクがあります。

*   **SQLインジェクション**: データベースが不正に操作される
*   **XSS（Cross-Site Scripting）**: 悪意のあるスクリプトが実行される

Laravelでは、`validate()`メソッドを使って、簡単にバリデーションを実装できます。

```php
$request->validate([
    'title' => 'required|string|max:255',
    'description' => 'nullable|string',
    'due_date' => 'nullable|date',
]);
```

---

### 🔍 SQLインジェクション対策

Laravelの**Eloquent ORM**を使うことで、SQLインジェクションを防ぐことができます。

**NG（危険）**:

```php
$tasks = DB::select("SELECT * FROM tasks WHERE user_id = {$userId}");
```

**OK（安全）**:

```php
$tasks = Task::where('user_id', $userId)->get();
```

---

### 🔍 XSS（Cross-Site Scripting）対策

Laravelでは、**Bladeテンプレート**を使うことで、XSSを防ぐことができます。

**NG（危険）**:

```php
{!! $task->title !!}
```

**OK（安全）**:

```php
{{ $task->title }}
```

`{{ }}`を使うことで、HTMLタグがエスケープされます。

---

### 🔍 CSRF（Cross-Site Request Forgery）対策

APIでは、通常**CSRFトークンは使用しません**。

代わりに、**トークンベース認証**を使います。

Sanctumを使うことで、CSRF対策が自動的に行われます。

---

### 🔍 認可（Authorization）の実装

APIでは、**認証（Authentication）**だけでなく、**認可（Authorization）**も重要です。

**認証**: ユーザーが誰であるかを確認する
**認可**: ユーザーが何をできるかを確認する

例えば、以下のような認可を実装します。

*   **自分のタスクのみを編集できる**: 他のユーザーのタスクは編集できない
*   **管理者のみが全てのタスクを閲覧できる**: 一般ユーザーは自分のタスクのみを閲覧できる

---

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
public function update(Request $request, string $id)
{
    $task = Task::findOrFail($id);

    // 認可チェック: 自分のタスクのみを更新できる
    if ($task->user_id !== Auth::id()) {
        return response()->json([
            'message' => 'このタスクを更新する権限がありません'
        ], 403);
    }

    $request->validate([
        'title' => 'required|string|max:255',
        'description' => 'nullable|string',
        'status' => 'required|in:pending,in_progress,completed',
        'due_date' => 'nullable|date',
    ]);

    $task->update($request->only(['title', 'description', 'status', 'due_date']));

    return new TaskResource($task);
}
```

---

### 💡 TIP: APIキーの管理

APIキーやシークレットキーは、**絶対にコードに直接書かない**でください。

環境変数（`.env`ファイル）に保存します。

**NG（危険）**:

```php
$apiKey = 'sk_live_abcdefghijklmnopqrstuvwxyz';
```

**OK（安全）**:

```php
$apiKey = env('STRIPE_API_KEY');
```

---

### 💡 TIP: ログの記録

APIでは、**ログを記録する**ことが重要です。

ログを記録することで、以下のようなメリットがあります。

*   **不正アクセスを検知できる**: 異常なアクセスパターンを発見できる
*   **デバッグがしやすい**: エラーの原因を特定できる

```php
use Illuminate\Support\Facades\Log;

Log::info('Task created', ['task_id' => $task->id, 'user_id' => Auth::id()]);
```

---

### 🚨 よくある間違い

#### 間違い1: HTTPSを使わない

**対処法**: 本番環境では、必ずHTTPSを使用します。

---

#### 間違い2: バリデーションを行わない

**対処法**: 全ての入力値に対して、バリデーションを行います。

---

#### 間違い3: エラーメッセージに詳細な情報を含める

**対処法**: エラーメッセージには、システムの内部情報を含めないようにします。

**NG（危険）**:

```json
{
  "message": "SQLSTATE[42S02]: Base table or view not found: 1146 Table 'database.tasks' doesn't exist"
}
```

**OK（安全）**:

```json
{
  "message": "サーバーエラーが発生しました"
}
```

---

## ✨ まとめ

このセクションでは、APIのセキュリティ対策について学びました。

*   レート制限を実装することで、DDoS攻撃を防ぐことができる。
*   HTTPSを使用することで、通信内容が暗号化される。
*   入力値のバリデーションを行うことで、SQLインジェクションやXSSを防ぐことができる。
*   認可を実装することで、ユーザーが適切な権限を持っているかを確認できる。

次のセクションでは、外部APIの利用について学びます。

---

## 📝 学習のポイント

- [ ] APIのセキュリティリスクを理解した。
- [ ] レート制限（Rate Limiting）の実装方法を学んだ。
- [ ] APIのセキュリティベストプラクティスを理解した。
