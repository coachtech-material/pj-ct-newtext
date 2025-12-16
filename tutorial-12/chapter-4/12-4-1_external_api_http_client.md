# Tutorial 12-4-1: 外部APIの利用（HTTP Client）

## 🎯 このセクションで学ぶこと

*   外部APIを利用する方法を学ぶ。
*   Laravel HTTP Clientの使い方を理解する。
*   エラーハンドリングの実装方法を学ぶ。

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜAPI認証の後に『外部API連携』を学ぶのか？」

自分でAPIを作れるようになったら、次は「外部API連携」です。

---

### 理由1: 実務では外部APIを使う

実際の開発では、**外部のAPIを利用する**ことが多いです。

- 決済API（Stripe、PayPal）
- 地図API（Google Maps）
- SNS API（Twitter、LINE）
- 天気API、翻訳API など

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

- ネットワークエラー
- タイムアウト
- APIの仕様変更

適切なエラーハンドリングが必要です。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| 1 | HTTPクライアントの基本 | `Http::get()`、`Http::post()`の使い方 |
| 2 | レスポンスの処理 | JSONの解析、エラーチェック |
| 3 | 実践: 外部APIの呼び出し | 実際のAPIを使って練習 |

> 💡 **ポイント**: 外部APIを使うときは、APIドキュメントをよく読むことが重要です。

---

## 導入：外部APIとは

**外部API**とは、**他のサービスが提供するAPI**のことです。

外部APIを利用することで、以下のようなことが可能になります。

*   **天気情報を取得する**: OpenWeatherMap APIなど
*   **決済機能を実装する**: Stripe APIなど
*   **地図を表示する**: Google Maps APIなど
*   **翻訳機能を実装する**: Google Translate APIなど

このセクションでは、**Laravel HTTP Client**を使って、外部APIを利用する方法を学びます。

---

## 詳細解説

### 🔍 Laravel HTTP Clientとは

**Laravel HTTP Client**とは、**HTTPリクエストを簡単に送信するための機能**です。

Laravel HTTP Clientを使うことで、以下のようなメリットがあります。

*   **シンプル**: 簡単にHTTPリクエストを送信できる
*   **テストしやすい**: モックを使ってテストできる
*   **エラーハンドリングが簡単**: エラー処理を簡単に実装できる

---

### 🔍 基本的な使い方

**ファイル**: `app/Http/Controllers/Api/WeatherController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class WeatherController extends Controller
{
    /**
     * 天気情報を取得する
     */
    public function index(Request $request)
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
            'humidity' => $data['main']['humidity'],
        ], 200);
    }
}
```

---

### 🔍 コードリーディング

#### `Http::get('https://api.openweathermap.org/data/2.5/weather', [...])`

*   `Http::get()`メソッドで、GETリクエストを送信します。
*   第1引数にURL、第2引数にクエリパラメータを指定します。

---

#### `$response->failed()`

*   `failed()`メソッドで、リクエストが失敗したかどうかを確認します。
*   HTTPステータスコードが400以上の場合、`true`を返します。

---

#### `$response->json()`

*   `json()`メソッドで、レスポンスをJSON形式で取得します。

---

### 🔍 POSTリクエストの送信

```php
$response = Http::post('https://api.example.com/tasks', [
    'title' => 'New Task',
    'description' => 'This is a new task',
]);
```

---

### 🔍 ヘッダーの設定

```php
$response = Http::withHeaders([
    'Authorization' => 'Bearer ' . env('API_TOKEN'),
    'Accept' => 'application/json',
])->get('https://api.example.com/tasks');
```

---

### 🔍 タイムアウトの設定

```php
$response = Http::timeout(10)->get('https://api.example.com/tasks');
```

---

### 🔍 リトライの設定

```php
$response = Http::retry(3, 100)->get('https://api.example.com/tasks');
```

*   第1引数: リトライ回数
*   第2引数: リトライ間隔（ミリ秒）

---

### 🔍 エラーハンドリング

```php
try {
    $response = Http::get('https://api.example.com/tasks');

    if ($response->successful()) {
        // 成功時の処理
        $data = $response->json();
    } elseif ($response->clientError()) {
        // クライアントエラー（4xx）の処理
        return response()->json([
            'message' => 'リクエストが不正です'
        ], 400);
    } elseif ($response->serverError()) {
        // サーバーエラー（5xx）の処理
        return response()->json([
            'message' => 'サーバーエラーが発生しました'
        ], 500);
    }
} catch (\Exception $e) {
    // 例外処理
    return response()->json([
        'message' => 'エラーが発生しました'
    ], 500);
}
```

---

### 🔍 レスポンスのステータスコードを確認する

```php
$response = Http::get('https://api.example.com/tasks');

if ($response->status() === 200) {
    // 成功
}

if ($response->ok()) {
    // 200番台
}

if ($response->successful()) {
    // 200番台
}

if ($response->failed()) {
    // 400番台または500番台
}

if ($response->clientError()) {
    // 400番台
}

if ($response->serverError()) {
    // 500番台
}
```

---

### 🔍 実践例: GitHub APIを使ったリポジトリ情報の取得

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Http;

class GitHubController extends Controller
{
    /**
     * GitHubリポジトリ情報を取得する
     */
    public function show(string $owner, string $repo)
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

**ファイル**: `routes/api.php`

```php
Route::get('/github/{owner}/{repo}', [GitHubController::class, 'show']);
```

---

**テスト**:

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

### 💡 TIP: テストでのモック

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

### 💡 TIP: APIキーの管理

APIキーは、**必ず環境変数に保存**してください。

**ファイル**: `.env`

```
OPENWEATHER_API_KEY=your_api_key_here
GITHUB_TOKEN=your_github_token_here
```

**使用例**:

```php
$apiKey = env('OPENWEATHER_API_KEY');
```

---

### 🚨 よくある間違い

#### 間違い1: エラーハンドリングを行わない

**対処法**: 必ず`failed()`や`successful()`でエラーチェックを行います。

---

#### 間違い2: タイムアウトを設定しない

**対処法**: `timeout()`メソッドでタイムアウトを設定します。

---

#### 間違い3: APIキーをコードに直接書く

**対処法**: APIキーは、環境変数（`.env`ファイル）に保存します。

---

## ✨ まとめ

このセクションでは、外部APIの利用（HTTP Client）について学びました。

*   Laravel HTTP Clientを使うことで、簡単にHTTPリクエストを送信できる。
*   `Http::get()`でGETリクエスト、`Http::post()`でPOSTリクエストを送信する。
*   `failed()`や`successful()`でエラーチェックを行う。
*   タイムアウトやリトライを設定することで、安定したAPIを実装できる。

これで、Tutorial 12「API開発基礎」の主要なセクションが完了しました。

---

## 📝 学習のポイント

- [ ] 外部APIを利用する方法を学んだ。
- [ ] Laravel HTTP Clientの使い方を理解した。
- [ ] エラーハンドリングの実装方法を学んだ。
