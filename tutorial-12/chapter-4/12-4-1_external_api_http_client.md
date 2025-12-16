# Tutorial 12-4-1: 外部APIの利用（HTTP Client）

## 🎯 このセクションで学ぶこと

- 外部APIを利用する方法を学ぶ
- Laravel HTTP Clientの使い方を理解する
- エラーハンドリングの実装方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜAPI認証の後に『外部API連携』を学ぶのか？」

自分でAPIを作れるようになったら、次は「外部API連携」です。

---

### 理由1: 実務では外部APIを使う

実際の開発では、**外部のAPIを利用する**ことが多いです。

| 種類 | 例 |
|------|-----|
| 決済API | Stripe、PayPal |
| 地図API | Google Maps |
| SNS API | Twitter、LINE |
| その他 | 天気API、翻訳API |

---

### 理由2: HTTPクライアントの使い方

Laravelには**HTTPクライアント**が組み込まれています。

```php
$response = Http::get('https://api.example.com/data');
$data = $response->json();
```

---

### 理由3: エラーハンドリング

外部APIは**常に成功するとは限りません**。

| 問題 | 対策 |
|------|------|
| ネットワークエラー | リトライ設定 |
| タイムアウト | タイムアウト設定 |
| APIの仕様変更 | エラーハンドリング |

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | HTTPクライアントの基本 | GET、POSTの使い方 |
| Step 2 | エラーハンドリング | 安定したAPI呼び出し |
| Step 3 | 実践: 外部APIの呼び出し | 実際のAPIを使って練習 |

> 💡 **ポイント**: 外部APIを使うときは、APIドキュメントをよく読むことが重要です。

---

## Step 1: HTTPクライアントの基本

### 1-1. Laravel HTTP Clientとは

**Laravel HTTP Client**とは、**HTTPリクエストを簡単に送信するための機能**です。

| メリット | 説明 |
|----------|------|
| シンプル | 簡単にHTTPリクエストを送信できる |
| テストしやすい | モックを使ってテストできる |
| エラーハンドリングが簡単 | エラー処理を簡単に実装できる |

---

### 1-2. GETリクエストの送信

**ファイル**: `app/Http/Controllers/Api/WeatherController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Http;

class WeatherController extends Controller
{
    public function index(Request $request): JsonResponse
    {
        $city = $request->query('city', 'Tokyo');

        $response = Http::get('https://api.openweathermap.org/data/2.5/weather', [
            'q' => $city,
            'appid' => env('OPENWEATHER_API_KEY'),
            'units' => 'metric',
            'lang' => 'ja',
        ]);

        if ($response->failed()) {
            return response()->json([
                'message' => '天気情報の取得に失敗しました'
            ], 500);
        }

        $data = $response->json();

        return response()->json([
            'city' => $data['name'],
            'temperature' => $data['main']['temp'],
            'description' => $data['weather'][0]['description'],
        ], 200);
    }
}
```

---

### 1-3. コードリーディング

| コード | 説明 |
|--------|------|
| `Http::get(url, params)` | GETリクエストを送信 |
| `$response->failed()` | リクエストが失敗したか確認 |
| `$response->json()` | レスポンスをJSON形式で取得 |

---

### 1-4. POSTリクエストの送信

```php
$response = Http::post('https://api.example.com/tasks', [
    'title' => 'New Task',
    'description' => 'This is a new task',
]);
```

---

### 1-5. ヘッダーの設定

```php
$response = Http::withHeaders([
    'Authorization' => 'Bearer ' . env('API_TOKEN'),
    'Accept' => 'application/json',
])->get('https://api.example.com/tasks');
```

---

## Step 2: エラーハンドリング

### 2-1. タイムアウトの設定

```php
$response = Http::timeout(10)->get('https://api.example.com/tasks');
```

---

### 2-2. リトライの設定

```php
$response = Http::retry(3, 100)->get('https://api.example.com/tasks');
```

| 引数 | 説明 |
|------|------|
| 第1引数 | リトライ回数 |
| 第2引数 | リトライ間隔（ミリ秒） |

---

### 2-3. エラーハンドリングの実装

```php
try {
    $response = Http::get('https://api.example.com/tasks');

    if ($response->successful()) {
        $data = $response->json();
    } elseif ($response->clientError()) {
        return response()->json([
            'message' => 'リクエストが不正です'
        ], 400);
    } elseif ($response->serverError()) {
        return response()->json([
            'message' => 'サーバーエラーが発生しました'
        ], 500);
    }
} catch (\Exception $e) {
    return response()->json([
        'message' => 'エラーが発生しました'
    ], 500);
}
```

---

### 2-4. レスポンスのステータスコードを確認する

| メソッド | 説明 |
|----------|------|
| `$response->status()` | ステータスコードを取得 |
| `$response->ok()` | 200番台か確認 |
| `$response->successful()` | 200番台か確認 |
| `$response->failed()` | 400番台または500番台か確認 |
| `$response->clientError()` | 400番台か確認 |
| `$response->serverError()` | 500番台か確認 |

---

## Step 3: 実践: 外部APIの呼び出し

### 3-1. GitHub APIを使ったリポジトリ情報の取得

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Http;

class GitHubController extends Controller
{
    public function show(string $owner, string $repo): JsonResponse
    {
        $response = Http::withHeaders([
            'Accept' => 'application/vnd.github.v3+json',
        ])->get("https://api.github.com/repos/{$owner}/{$repo}");

        if ($response->failed()) {
            return response()->json([
                'message' => 'リポジトリ情報の取得に失敗しました'
            ], 404);
        }

        $data = $response->json();

        return response()->json([
            'name' => $data['name'],
            'description' => $data['description'],
            'stars' => $data['stargazers_count'],
            'forks' => $data['forks_count'],
            'language' => $data['language'],
            'url' => $data['html_url'],
        ], 200);
    }
}
```

---

### 3-2. ルートの定義

**ファイル**: `routes/api.php`

```php
Route::get('/github/{owner}/{repo}', [GitHubController::class, 'show']);
```

---

### 3-3. テスト

```bash
curl -X GET http://localhost/api/github/laravel/laravel
```

**レスポンス**:

```json
{
  "name": "laravel",
  "description": "Laravel is a web application framework with expressive, elegant syntax.",
  "stars": 75000,
  "forks": 24000,
  "language": "PHP",
  "url": "https://github.com/laravel/laravel"
}
```

---

## 🚨 よくある間違い

### 間違い1: エラーハンドリングを行わない

**問題**: APIが失敗したときにエラーになる

**対処法**: 必ず`failed()`や`successful()`でエラーチェックを行います。

---

### 間違い2: タイムアウトを設定しない

**問題**: APIが応答しないときに無限に待つ

**対処法**: `timeout()`メソッドでタイムアウトを設定します。

---

### 間違い3: APIキーをコードに直接書く

**問題**: APIキーが漏洩する

**対処法**: APIキーは、環境変数（`.env`ファイル）に保存します。

```php
// ❌ 間違い
$apiKey = 'your_api_key_here';

// ✅ 正しい
$apiKey = env('OPENWEATHER_API_KEY');
```

---

## 💡 TIP: テストでのモック

テストでは、実際のAPIにリクエストを送信せず、モックを使います。

```php
use Illuminate\Support\Facades\Http;

Http::fake([
    'https://api.github.com/*' => Http::response([
        'name' => 'laravel',
        'description' => 'Laravel is a web application framework',
        'stargazers_count' => 75000,
        'forks_count' => 24000,
        'language' => 'PHP',
        'html_url' => 'https://github.com/laravel/laravel',
    ], 200),
]);

$response = $this->get('/api/github/laravel/laravel');

$response->assertStatus(200);
```

---

## 💡 TIP: APIキーの管理

APIキーは、**必ず環境変数に保存**してください。

**ファイル**: `.env`

```
OPENWEATHER_API_KEY=your_api_key_here
GITHUB_TOKEN=your_github_token_here
```

---

## ✨ まとめ

このセクションでは、外部APIの利用（HTTP Client）について学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | HTTPクライアントの基本（GET、POST、ヘッダー設定） |
| Step 2 | エラーハンドリング（タイムアウト、リトライ） |
| Step 3 | 実践: GitHub APIを使ったリポジトリ情報の取得 |

これで、Tutorial 12「API開発基礎」の主要なセクションが完了しました。

---

## 📝 学習のポイント

- [ ] 外部APIを利用する方法を学んだ
- [ ] Laravel HTTP Clientの使い方を理解した
- [ ] エラーハンドリングの実装方法を学んだ
