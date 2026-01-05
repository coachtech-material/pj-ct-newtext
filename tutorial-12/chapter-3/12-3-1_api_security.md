# Tutorial 12-3-1: APIのセキュリティ対策

## 🎯 このセクションで学ぶこと

- APIのセキュリティリスクを理解する
- レート制限（Rate Limiting）の実装方法を学ぶ
- 入力値の検証の重要性を理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜAPIセキュリティを学ぶのか？」

API開発では、セキュリティ対策が重要です。

---

### 理由1: APIは外部に公開される

WebアプリケーションのAPIは、**外部からアクセス可能**です。

悪意のあるユーザーが攻撃を試みる可能性があります。

| リスク | 説明 |
|--------|------|
| 大量リクエスト | サーバーがダウンする |
| 不正なデータ | データベースが破壊される |
| 情報漏洩 | 機密情報が盗まれる |

---

### 理由2: 攻撃パターンを知る

APIに対する**一般的な攻撃パターン**を知っておくことが重要です。

| 攻撃 | 説明 |
|------|------|
| DoS攻撃 | 大量のリクエストでサーバーをダウンさせる |
| SQLインジェクション | データベースを不正に操作する |
| XSS | 悪意のあるスクリプトを実行する |

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
| Step 3 | セキュリティのベストプラクティス | 安全なAPI開発 |

> 💡 **ポイント**: セキュリティは「後から追加」ではなく、最初から考慮すべきです。

---

## Step 1: レート制限の設定

### 1-1. レート制限（Rate Limiting）とは

**レート制限**とは、**一定時間内にAPIにアクセスできる回数を制限する仕組み**です。

| メリット | 説明 |
|----------|------|
| DoS攻撃を防ぐ | 大量のリクエストを防ぐ |
| サーバーの負荷を軽減 | 過度なアクセスを防ぐ |
| 公平性を保つ | 特定のユーザーがAPIを独占することを防ぐ |

---

### 1-2. Laravelのレート制限

Laravelでは、デフォルトでAPIにレート制限が適用されています。

**ファイル**: `bootstrap/app.php`

```php
->withMiddleware(function (Middleware $middleware) {
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
            return Limit::perMinute(60)->by($request->ip());
        });
    }
}
```

---

### 1-4. コードリーディング

#### `Limit::perMinute(60)`

```php
Limit::perMinute(60)
```

| 部分 | 説明 |
|------|------|
| `Limit::perMinute()` | 1分間あたりの制限を設定 |
| `60` | 60回までのリクエストを許可 |

---

#### `->by($request->ip())`

```php
->by($request->ip())
```

| 部分 | 説明 |
|------|------|
| `->by()` | 制限の基準を設定 |
| `$request->ip()` | IPアドレスごとに制限 |

---

### 1-5. レート制限のカスタマイズ

特定のエンドポイントに対して、異なるレート制限を適用することもできます。

```php
// 厳しい制限: 1分間に10回
RateLimiter::for('strict', function (Request $request) {
    return Limit::perMinute(10)->by($request->ip());
});
```

**ルーティング**:

```php
Route::middleware('throttle:strict')->group(function () {
    Route::post('/api/tasks', [TaskController::class, 'store']);
});
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
| データ破壊 | 不正なデータが保存される |

```php
$validated = $request->validate([
    'title' => 'required|string|max:255',
    'description' => 'nullable|string',
    'due_date' => 'nullable|date',
]);
```

---

### 2-2. SQLインジェクション対策

Laravelの**Eloquent ORM**を使うことで、SQLインジェクションを防ぐことができます。

```php
// ❌ 危険（生のSQLを使用）
$tasks = DB::select("SELECT * FROM tasks WHERE user_id = {$userId}");

// ✅ 安全（Eloquentを使用）
$tasks = Task::where('user_id', $userId)->get();
```

---

### 2-3. コードリーディング

#### なぜEloquentが安全なのか

```php
Task::where('user_id', $userId)->get();
```

| 部分 | 説明 |
|------|------|
| `where('user_id', $userId)` | 値が自動的にエスケープされる |
| プリペアドステートメント | SQLインジェクションを防ぐ |

---

### 2-4. XSS（Cross-Site Scripting）対策

APIでJSONを返す場合、XSSのリスクは低いですが、HTMLを返す場合は注意が必要です。

```php
// ❌ 危険（HTMLタグがそのまま出力される）
{!! $task->title !!}

// ✅ 安全（HTMLタグがエスケープされる）
{{ $task->title }}
```

---

## Step 3: セキュリティのベストプラクティス

### 3-1. HTTPSの使用

APIは、**必ずHTTPSを使用**してください。

| メリット | 説明 |
|----------|------|
| 通信内容が暗号化される | 第三者に盗聴されない |
| 中間者攻撃を防ぐ | 通信内容が改ざんされない |

---

### 3-2. 機密情報の管理

APIキーやシークレットキーは、**絶対にコードに直接書かない**でください。

```php
// ❌ 危険
$apiKey = 'sk_live_abcdefghijklmnopqrstuvwxyz';

// ✅ 安全
$apiKey = env('API_KEY');
```

---

### 3-3. ログの記録

APIでは、**ログを記録する**ことが重要です。

```php
use Illuminate\Support\Facades\Log;

Log::info('Task created', ['task_id' => $task->id]);
```

| メリット | 説明 |
|----------|------|
| 不正アクセスを検知できる | 異常なアクセスパターンを発見 |
| デバッグがしやすい | エラーの原因を特定 |

---

### 3-4. エラーメッセージの制限

本番環境では、詳細なエラーメッセージを返さないでください。

```php
// ❌ 危険（本番環境）
{
  "message": "SQLSTATE[42S02]: Base table or view not found"
}

// ✅ 安全（本番環境）
{
  "message": "サーバーエラーが発生しました"
}
```

---

## 🚨 よくある間違い

### 間違い1: HTTPSを使わない

**問題**: 通信内容が盗聴される

**対処法**: 本番環境では、必ずHTTPSを使用します。

---

### 間違い2: バリデーションを行わない

**問題**: SQLインジェクションやXSSの危険性

**対処法**: 全ての入力値に対して、バリデーションを行います。

```php
// ❌ 間違い
$task = Task::create($request->all());

// ✅ 正しい
$validated = $request->validate([...]);
$task = Task::create($validated);
```

---

### 間違い3: 生のSQLを使う

**問題**: SQLインジェクションの危険性

**対処法**: Eloquent ORMを使用します。

```php
// ❌ 間違い
DB::select("SELECT * FROM tasks WHERE id = {$id}");

// ✅ 正しい
Task::find($id);
```

---

## 💡 TIP: CSRF対策

APIでは、通常**CSRFトークンは使用しません**。

APIは`routes/api.php`に定義することで、CSRF保護が自動的に無効になります。

これは、APIがステートレス（セッションを使わない）であるためです。

---

## ✨ まとめ

このセクションでは、APIのセキュリティ対策について学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | レート制限の設定とカスタマイズ |
| Step 2 | 入力値の検証とインジェクション対策 |
| Step 3 | セキュリティのベストプラクティス |

**セキュリティのポイント**:

1. **レート制限**でDoS攻撃を防ぐ
2. **バリデーション**で不正なデータを防ぐ
3. **Eloquent ORM**でSQLインジェクションを防ぐ
4. **HTTPS**で通信を暗号化する

---
