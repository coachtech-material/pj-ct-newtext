# Tutorial 12-1-2: LaravelでAPIを開発する準備

## 🎯 このセクションで学ぶこと

- API開発用のスターターキットをセットアップする方法を学ぶ
- APIルーティングの設定方法を理解する
- APIレスポンスの基本的な返し方を学ぶ
- APIのデバッグ方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ概念理解の後に『環境構築』を行うのか？」

APIの概念を理解したら、次は「環境構築」です。

---

### 理由1: 手を動かして理解を深める

概念だけでは理解が浅くなります。**実際に環境を作って動かす**ことで理解が深まります。

---

### 理由2: LaravelのAPI機能を有効化

Laravelには**API開発用の機能**が用意されています。

| 機能 | 説明 |
|------|------|
| `api.php`ルートファイル | API専用のルーティング |
| APIミドルウェア | レート制限など |
| JSON レスポンス | 自動的なJSON変換 |

これらを有効化して、API開発の準備を整えます。

---

### 理由3: すぐに動く環境から始める

このチュートリアルでは、**スターターキット**を使います。

| メリット | 説明 |
|----------|------|
| すぐに動作確認できる | 環境構築の手間を省く |
| サンプルデータがある | APIの動作を確認しやすい |
| API学習に集中できる | 認証などの複雑な設定が不要 |

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | スターターキットのセットアップ | 環境構築 |
| Step 2 | APIルーティングの確認 | `api.php`の使い方を学ぶ |
| Step 3 | APIレスポンスの返し方 | JSON形式のレスポンス |
| Step 4 | デバッグ方法 | ログを使ったデバッグ |

> 💡 **ポイント**: スターターキットを使うことで、API開発の本質に集中できます。

---

## Step 1: スターターキットのセットアップ

### 1-1. スターターキットとは

**スターターキット**は、API開発に必要な最低限の設定が済んだプロジェクトです。

| 含まれるもの | 説明 |
|--------------|------|
| マイグレーション | `users`テーブルと`tasks`テーブル |
| モデル | `User`モデルと`Task`モデル |
| シーダー | テスト用のユーザーとタスクデータ |

---

### 1-2. プロジェクトのクローン

```bash
git clone https://github.com/coachtech-material/laravel-api-starter-forTutorial13.git
cd laravel-api-starter-forTutorial13
```

---

### 1-3. 依存パッケージのインストール

```bash
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    laravelsail/php83-composer:latest \
    composer install --ignore-platform-reqs
```

---

### 1-4. 環境設定ファイルの作成

```bash
cp .env.example .env
```

---

### 1-5. Sailの起動

```bash
./vendor/bin/sail up -d
```

---

### 1-6. アプリケーションキーの生成

```bash
sail artisan key:generate
```

---

### 1-7. データベースのセットアップ

```bash
sail artisan migrate:fresh --seed
```

このコマンドで以下が実行されます。

| 処理 | 説明 |
|------|------|
| `migrate:fresh` | テーブルを作成 |
| `--seed` | テストデータを投入 |

---

### 1-8. 動作確認

ブラウザで `http://localhost` にアクセスして、Laravelの画面が表示されることを確認します。

---

## Step 2: APIルーティングの確認

### 2-1. APIルートファイル

Laravelでは、`routes/api.php`にAPIのルーティングを定義します。

**ファイル**: `routes/api.php`

```php
<?php

use Illuminate\Support\Facades\Route;

// ここにAPIルートを定義します
```

---

### 2-2. APIルーティングの特徴

| 特徴 | 説明 |
|------|------|
| `/api`プレフィックス | `/tasks`は`/api/tasks`になる |
| `api`ミドルウェア | レート制限などが適用される |
| ステートレス | セッションは使用しない |

---

### 2-3. 簡単なAPIの作成

**ファイル**: `routes/api.php`

```php
<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

// 簡単なHello World API
Route::get('/hello', function () {
    return response()->json([
        'message' => 'Hello, World!'
    ]);
});

// パラメータを受け取るAPI
Route::get('/hello/{name}', function (string $name) {
    return response()->json([
        'message' => "Hello, {$name}!"
    ]);
});

// POSTリクエストを受け取るAPI
Route::post('/echo', function (Request $request) {
    return response()->json([
        'received' => $request->input('message')
    ]);
});
```

---

### 2-4. コードリーディング

上記のコードを1行ずつ見ていきましょう。

---

#### `Route::get('/hello', function () { ... })`

```php
Route::get('/hello', function () {
```

| 部分 | 説明 |
|------|------|
| `Route` | Laravelのルーティングクラス |
| `::get` | GETリクエストを受け付ける |
| `'/hello'` | URLのパス（`/api/hello`になる） |
| `function () { ... }` | リクエストを処理する関数 |

---

#### `return response()->json([...])`

```php
return response()->json([
    'message' => 'Hello, World!'
]);
```

| 部分 | 説明 |
|------|------|
| `return` | レスポンスを返す |
| `response()` | レスポンスを作成するヘルパー関数 |
| `->json([...])` | 配列をJSON形式に変換 |
| `'message' => 'Hello, World!'` | JSONのキーと値 |

---

#### `Route::get('/hello/{name}', function (string $name) { ... })`

```php
Route::get('/hello/{name}', function (string $name) {
```

| 部分 | 説明 |
|------|------|
| `'/hello/{name}'` | `{name}`はURLパラメータ |
| `string $name` | パラメータを受け取る引数 |

例: `/api/hello/Taro`にアクセスすると、`$name`に`Taro`が入る

---

#### `$request->input('message')`

```php
$request->input('message')
```

| 部分 | 説明 |
|------|------|
| `$request` | リクエストオブジェクト |
| `->input('message')` | リクエストボディから`message`の値を取得 |

---

### 2-5. Thunder Clientでテスト

Thunder Clientを使って、作成したAPIをテストします。

**1. Hello World API**

- メソッド: `GET`
- URL: `http://localhost/api/hello`
- 期待するレスポンス:

```json
{
  "message": "Hello, World!"
}
```

**2. パラメータ付きAPI**

- メソッド: `GET`
- URL: `http://localhost/api/hello/Taro`
- 期待するレスポンス:

```json
{
  "message": "Hello, Taro!"
}
```

**3. POSTリクエスト**

- メソッド: `POST`
- URL: `http://localhost/api/echo`
- Headers: `Content-Type: application/json`
- Body（JSON）:

```json
{
  "message": "Hello from Thunder Client"
}
```

- 期待するレスポンス:

```json
{
  "received": "Hello from Thunder Client"
}
```

---

## Step 3: APIコントローラーの作成

### 3-1. APIコントローラーを生成する

```bash
sail artisan make:controller Api/TaskController --api
```

`--api`オプションを付けることで、API用のコントローラーが作成されます。

---

### 3-2. コントローラーの実装

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    public function index()
    {
        return response()->json([
            'data' => [
                ['id' => 1, 'title' => 'タスク1'],
                ['id' => 2, 'title' => 'タスク2'],
            ]
        ]);
    }

    public function store(Request $request)
    {
        return response()->json([
            'message' => 'タスクを作成しました',
            'data' => [
                'id' => 3,
                'title' => $request->input('title'),
            ]
        ], 201);
    }

    public function show(string $id)
    {
        return response()->json([
            'data' => [
                'id' => $id,
                'title' => "タスク{$id}",
            ]
        ]);
    }

    public function update(Request $request, string $id)
    {
        return response()->json([
            'message' => 'タスクを更新しました',
            'data' => [
                'id' => $id,
                'title' => $request->input('title'),
            ]
        ]);
    }

    public function destroy(string $id)
    {
        return response()->json(null, 204);
    }
}
```

---

### 3-3. コードリーディング

#### `namespace App\Http\Controllers\Api`

```php
namespace App\Http\Controllers\Api;
```

| 部分 | 説明 |
|------|------|
| `namespace` | このクラスが属する名前空間 |
| `App\Http\Controllers\Api` | `Api`ディレクトリ内のコントローラー |

---

#### `response()->json([...], 201)`

```php
return response()->json([
    'message' => 'タスクを作成しました',
    'data' => [...]
], 201);
```

| 部分 | 説明 |
|------|------|
| `response()->json([...])` | 配列をJSON形式に変換 |
| `, 201` | HTTPステータスコード（201 Created） |

---

#### `response()->json(null, 204)`

```php
return response()->json(null, 204);
```

| 部分 | 説明 |
|------|------|
| `null` | レスポンスボディなし |
| `204` | HTTPステータスコード（204 No Content） |

---

### 3-4. 各メソッドの役割

| メソッド | HTTPメソッド | 役割 | ステータスコード |
|--------|------|------|------|
| `index()` | GET | 一覧取得 | 200 |
| `store()` | POST | 新規作成 | 201 |
| `show()` | GET | 詳細取得 | 200 |
| `update()` | PUT/PATCH | 更新 | 200 |
| `destroy()` | DELETE | 削除 | 204 |

> 💡 **ポイント**: `--api`オプションで生成すると、`create()`と`edit()`メソッドが含まれません。これらはHTMLフォーム表示用なので、APIでは不要です。

---

### 3-5. APIルーティングの設定

**ファイル**: `routes/api.php`

```php
<?php

use App\Http\Controllers\Api\TaskController;
use Illuminate\Support\Facades\Route;

Route::apiResource('tasks', TaskController::class);
```

---

### 3-6. apiResourceで作成されるルーティング

| HTTPメソッド | URL | アクション |
|---|---|---|
| GET | `/api/tasks` | index |
| POST | `/api/tasks` | store |
| GET | `/api/tasks/{id}` | show |
| PUT | `/api/tasks/{id}` | update |
| PATCH | `/api/tasks/{id}` | update |
| DELETE | `/api/tasks/{id}` | destroy |

---

### 3-7. ルーティングの確認

```bash
sail artisan route:list --path=api
```

---

## Step 4: デバッグ方法

### 4-1. APIでのデバッグの注意点

Web開発では`dd()`を使ってデバッグしますが、APIでは注意が必要です。

| 問題 | 説明 |
|------|------|
| `dd()`の出力が崩れる | Thunder Clientの「Preview」タブを見ないと読めない |
| JSONレスポンスが壊れる | `dd()`がHTMLを出力するため |

---

### 4-2. ログを使ったデバッグ（推奨）

APIでは、**ログを使ったデバッグ**が安全です。

```php
use Illuminate\Support\Facades\Log;

public function store(Request $request)
{
    // リクエストの内容をログに出力
    Log::info('タスク作成リクエスト', [
        'title' => $request->input('title'),
        'description' => $request->input('description'),
    ]);
    
    // 処理を続ける...
}
```

---

### 4-3. ログの確認方法

ログは`storage/logs/laravel.log`に出力されます。

**方法1: ファイルを直接確認**

```bash
sail exec laravel.test cat storage/logs/laravel.log
```

**方法2: リアルタイムで確認**

```bash
sail exec laravel.test tail -f storage/logs/laravel.log
```

**方法3: Sailのログコマンド**

```bash
sail logs
```

---

### 4-4. ログのレベル

| レベル | メソッド | 用途 |
|--------|----------|------|
| debug | `Log::debug()` | 開発時の詳細情報 |
| info | `Log::info()` | 一般的な情報 |
| warning | `Log::warning()` | 警告 |
| error | `Log::error()` | エラー |

---

### 4-5. デバッグの例

```php
public function show(string $id)
{
    Log::info('タスク詳細取得', ['id' => $id]);
    
    $task = Task::find($id);
    
    if (!$task) {
        Log::warning('タスクが見つかりません', ['id' => $id]);
        return response()->json(['message' => 'Task not found'], 404);
    }
    
    Log::info('タスク取得成功', ['task' => $task->toArray()]);
    
    return response()->json(['data' => $task]);
}
```

---

## 🚨 よくある間違い

### 間違い1: routes/web.phpにAPIを定義する

**問題**: セッションやCSRF保護が適用されてしまう

**対処法**: APIは`routes/api.php`に定義します。

---

### 間違い2: dd()でデバッグしようとする

**問題**: JSONレスポンスが壊れる

**対処法**: `Log::info()`を使ってログに出力します。

---

### 間違い3: ステータスコードを省略する

**問題**: デフォルトで200が返される

```php
// ❌ 間違い
return response()->json($task);

// ✅ 正しい
return response()->json($task, 200);
```

---

## ✨ まとめ

このセクションでは、LaravelでAPI開発を行うための準備を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | スターターキットのセットアップ |
| Step 2 | APIルーティングの設定と特徴 |
| Step 3 | APIコントローラーの作成とapiResource |
| Step 4 | ログを使ったデバッグ方法 |

次のセクションでは、JSON形式について詳しく学びます。

---
