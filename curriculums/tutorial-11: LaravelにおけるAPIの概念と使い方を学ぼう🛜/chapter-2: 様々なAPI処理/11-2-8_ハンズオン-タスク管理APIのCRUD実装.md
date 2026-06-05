# 11-2-8: ハンズオン - タスク管理APIのCRUD実装

## 📌 このハンズオンについて

Chapter 2で学んだCRUD操作を実際に手を動かして確認します。タスク管理APIを実装し、Postmanで各操作のステータスコードとレスポンスを確認しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

### 📁 ディレクトリ構成

このハンズオンでは、「自分で作成する用」と「解答を確認する用」の2つのプロジェクトを作成します。

```
~/api-practice/
├── 11-2-8_hands-on/                         ← このハンズオン用のディレクトリ
│   ├── task-crud-practice/                  ← 要件を見て自分で作成するプロジェクト
│   │   ├── app/Http/Controllers/
│   │   │   └── TaskController.php
│   │   └── routes/api.php
│   └── task-crud-sample/                    ← 実践で一緒に作成するプロジェクト
│       ├── app/Http/Controllers/
│       │   └── TaskController.php
│       └── routes/api.php
└── ...
```

| ディレクトリ | 用途 |
|:---|:---|
| `task-crud-practice/` | 📋 要件を見て、自分の力で作成する |
| `task-crud-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したプロジェクトと、解答を見ながら作成したプロジェクトを比較することで、理解が深まります。

---

## 🎯 演習課題：タスク管理APIのCRUD実装

### この演習で作るもの

タスク管理APIのCRUD操作を実装します。

このハンズオンでは、**Tutorial 11専用のスターターキット**を使用します。

> 💡 **ポイント**: Chapter 1のハンズオン（11-1-7）とは別のプロジェクトを作成します。

### スターターキットに含まれるもの

| 項目 | 内容 |
|------|------|
| Laravel | 10.x |
| データベース | `users`テーブル、`tasks`テーブル（マイグレーション済み） |
| 初期データ | テスト用ユーザー（ID: 1）、サンプルタスク5件がシーダーで作成済み |
| Taskモデル | `$fillable`設定済み |
| 認証 | なし（認証機能は含まれていません） |

### 📋 要件

- タスク一覧を取得できる
- 新しいタスクを作成できる
- タスクの詳細を取得できる
- タスクを更新できる
- タスクを削除できる
- バリデーションエラー時に適切なエラーレスポンスが返る
- 存在しないタスクにアクセスすると404エラーが返る

**実装するAPI**:

| HTTPメソッド | URL | 操作 | ステータスコード |
|-------------|-----|------|----------------|
| GET | /api/tasks | 一覧取得 | 200 |
| POST | /api/tasks | 作成 | 201 / 422 |
| GET | /api/tasks/{id} | 詳細取得 | 200 / 404 |
| PUT | /api/tasks/{id} | 更新 | 200 / 404 / 422 |
| DELETE | /api/tasks/{id} | 削除 | 204 / 404 |

### 📦 GitHubでのコード管理

完成した成果物を **GitHubのpublicリポジトリ** で管理します。

- `~/api-practice/11-2-8_hands-on/task-crud-practice/` ディレクトリの中身（Laravelプロジェクト一式）を **publicリポジトリ** で管理する
- リポジトリ名は **`task-crud-practice`** とする
- 下記の雛形をもとに、`README.md` を **自分の言葉で** 作成する
- コミットとpushを完了させる

> 💡 **`practice/` と `sample/` の使い分け**:
> - **`task-crud-practice/`** が **「提出物」** です。最終的にここにある成果物をGitHubに push します
> - **`task-crud-sample/`** は **「答え合わせ用」** で、ローカルでの比較確認のみに使います。GitHubには push しません

<details>
<summary>📄 README.md の雛形（クリックで展開）</summary>

`task-crud-practice/README.md` に、以下の雛形をベースに **自分の言葉で** 記載しましょう（Laravelデフォルトの README を置き換えてOK）。

````markdown
# task-crud-practice

## 概要
COACHTECH 教材 Tutorial 11-2「タスク管理APIのCRUD実装」で作成した成果物です。
（**ここに、何を作ったかを1〜2行で書きましょう**）

## 使用技術
- PHP 8.x
- Laravel 10.x
- REST API（CRUD）
- API Resources、FormRequest（バリデーション）
（**他に使ったものがあれば追記してください**）

## 学んだこと
- （**自分の言葉で2〜3項目書きましょう**）
- 
- 

## 動作確認
（**どうやって動かして確認するかを記載してください。例: Postman で各エンドポイントへリクエスト**）
````

> 💡 **「学んだこと」の書き方の例（参考）**:
> - REST API の CRUD 実装（GET / POST / PUT / DELETE）と HTTP ステータスコードの使い分け
> - `apiResource` ルートで5つのアクションを一括定義する方法
> - API Resources / FormRequest によるレスポンス整形とバリデーション

任意で以下も追加すると、より評価されやすくなります:
- 詰まったポイントと解決方法
- 開発の工夫
- Postman の動作確認スクショ

</details>

### ✅ 完成チェックリスト

- [ ] `GET /api/tasks`でタスク一覧が取得できる（200）
- [ ] `POST /api/tasks`でタスクを作成できる（201）
- [ ] `GET /api/tasks/{id}`でタスク詳細が取得できる（200）
- [ ] `PUT /api/tasks/{id}`でタスクを更新できる（200）
- [ ] `DELETE /api/tasks/{id}`でタスクを削除できる（204）
- [ ] バリデーションエラー時に422が返る
- [ ] 存在しないタスクにアクセスすると404が返る

> 💡 **動作確認**: Postmanで各エンドポイントにリクエストを送信

### ✏️ 実装タスク

1. TaskControllerを作成する
2. CRUDメソッドを実装する
3. ルーティングを設定する
4. Postmanで動作確認する

---

## ⚙️ 環境準備（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

### Step 1: ディレクトリを作成

```bash
# api-practiceディレクトリに移動（なければ作成）
mkdir -p ~/api-practice
cd ~/api-practice

# ハンズオン用ディレクトリを作成
mkdir -p 11-2-8_hands-on
cd 11-2-8_hands-on
```

### Step 2: スターターキットをクローン

```bash
# 自分で作成する用のプロジェクトをクローン
git clone https://github.com/coachtech-material/laravel-api-starter.git task-crud-practice
cd task-crud-practice
```

### Step 3: Composerパッケージをインストール

```bash
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer install
```

### Step 4: 環境変数ファイルを作成

```bash
cp .env.example .env
```

### Step 5: Docker環境を起動

<details>
<summary>⚠️ M1/M2/M3 Mac（Apple Silicon）をお使いの方</summary>

Apple Silicon搭載のMacでは、`sail up -d`実行時に以下のエラーが発生することがあります：

```
no matching manifest for linux/arm64/v8
```

**解決方法**: `compose.yaml`を開き、mysqlサービスに`platform: 'linux/amd64'`を追加してください。

```yaml
mysql:
    image: 'mysql/mysql-server:8.0'
    platform: 'linux/amd64'  # ← この行を追加
    ports:
        ...
```

編集後、保存してから`sail up -d`を実行してください。

</details>

```bash
./vendor/bin/sail up -d
```

### Step 6: アプリケーションキーを生成

```bash
./vendor/bin/sail artisan key:generate
```

### Step 7: データベースの準備

```bash
./vendor/bin/sail artisan migrate:fresh --seed
```

### Step 8: セットアップ完了の確認

ブラウザで `http://localhost` にアクセスし、Laravelのウェルカムページが表示されることを確認します。

**✅ ディレクトリ構造の確認**

```
~/api-practice/
└── 11-2-8_hands-on/
    └── task-crud-practice/     ← 自分で作成する用（今ここ）
        ├── app/Http/Controllers/
        ├── routes/api.php
        └── ...
```

> 💡 **環境構築が完了！**
> 
> `TaskController`を作成し、CRUD操作を実装してみましょう。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

### コントローラーの作成

```bash
sail artisan make:controller TaskController --api
```

### ルーティング

```php
// routes/api.php
Route::apiResource('tasks', TaskController::class);
```

### CRUDメソッドの実装ポイント

| メソッド | ポイント |
|----------|---------|
| `index()` | `Task::all()`で全件取得 |
| `store()` | `$request->validate()`でバリデーション、`Task::create()`で作成 |
| `show()` | `Task::find($id)`で検索、見つからなければ404 |
| `update()` | `$task->update()`で更新 |
| `destroy()` | `$task->delete()`で削除、204を返す |

---

## 🏃 実践セクション：一緒に作ってみましょう！

ちゃんとできましたか？タスク管理APIのCRUD実装は、API開発の基本です。一緒に手を動かしながら、各メソッドを実装していきましょう。

> 📌 **注意**: ここからは`task-crud-sample/`ディレクトリで作業します。自分で作成したプロジェクトと比較できるように、別のプロジェクトで進めましょう。

---

### ⚙️ 環境準備（実践用プロジェクト）

### Step 1: 自分で作成したプロジェクトを停止

まず、自分で作成したプロジェクトのDockerコンテナを停止します。

```bash
# task-crud-practiceディレクトリで実行
cd ~/api-practice/11-2-8_hands-on/task-crud-practice
sail down
```

### Step 2: 実践用のプロジェクトをクローン

```bash
# ハンズオンディレクトリに移動
cd ~/api-practice/11-2-8_hands-on

# 実践用のプロジェクトをクローン
git clone https://github.com/coachtech-material/laravel-api-starter.git task-crud-sample
cd task-crud-sample
```

### Step 3: Composerパッケージをインストール

```bash
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer install
```

### Step 4: 環境変数ファイルを作成

```bash
cp .env.example .env
```

### Step 5: Docker環境を起動

<details>
<summary>⚠️ M1/M2/M3 Mac（Apple Silicon）をお使いの方</summary>

Apple Silicon搭載のMacでは、`sail up -d`実行時に以下のエラーが発生することがあります：

```
no matching manifest for linux/arm64/v8
```

**解決方法**: `compose.yaml`を開き、mysqlサービスに`platform: 'linux/amd64'`を追加してください。

```yaml
mysql:
    image: 'mysql/mysql-server:8.0'
    platform: 'linux/amd64'  # ← この行を追加
    ports:
        ...
```

編集後、保存してから`sail up -d`を実行してください。

</details>

```bash
./vendor/bin/sail up -d
```

### Step 6: アプリケーションキーを生成

```bash
./vendor/bin/sail artisan key:generate
```

### Step 7: データベースの準備

```bash
./vendor/bin/sail artisan migrate:fresh --seed
```

### Step 8: セットアップ完了の確認

ブラウザで `http://localhost` にアクセスし、Laravelのウェルカムページが表示されることを確認します。

**✅ ディレクトリ構造の確認**

```
~/api-practice/
└── 11-2-8_hands-on/
    ├── task-crud-practice/     ← 自分で作成した用
    └── task-crud-sample/       ← 実践用（今ここ）
        ├── app/Http/Controllers/
        ├── routes/api.php
        └── ...
```

---

### 🧠 先輩エンジニアの思考プロセス

先輩エンジニアは要件を以下のように構造化し、実装タスクに落とし込みます：

| Step | やること | 説明 |
|:-----|:---------|:-----|
| 1 | TaskControllerを作成する | `make:controller`コマンドで雛形を生成 |
| 2 | CRUDメソッドを実装する | index → store → show → update → destroy |
| 3 | ルーティングを設定する | `apiResource`で一括登録 |
| 4 | Postmanで動作確認する | 各操作のステータスコードを確認 |

---

### 📝 ステップバイステップで実装

#### ステップ1: TaskControllerを作成する

**何を考えているか**：
- 「APIリソース用のコントローラーを作成しよう」
- 「`--api`オプションでCRUDメソッドの雛形を生成しよう」

ターミナルで以下のコマンドを実行します。

```bash
sail artisan make:controller TaskController --api
```

| 部分 | 説明 |
|------|------|
| `make:controller` | コントローラーを作成 |
| `TaskController` | コントローラー名 |
| `--api` | APIリソース用のメソッドを自動生成 |

**生成されるメソッド**:

| メソッド | HTTPメソッド | 用途 |
|----------|-------------|------|
| `index()` | GET | 一覧取得 |
| `store()` | POST | 新規作成 |
| `show()` | GET | 詳細取得 |
| `update()` | PUT/PATCH | 更新 |
| `destroy()` | DELETE | 削除 |

---

#### ステップ2: CRUDメソッドを実装する

**何を考えているか**：
- 「各メソッドでどんな処理をするか考えよう」
- 「エラーケースも考慮しよう」

**ファイル**: `app/Http/Controllers/TaskController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    /**
     * タスク一覧を取得
     */
    public function index()
    {
        $tasks = Task::all();

        return response()->json([
            'data' => $tasks
        ], 200);
    }

    /**
     * タスクを新規作成
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
        ]);

        $task = Task::create([
            'user_id' => 1,
            'title' => $validated['title'],
            'description' => $validated['description'] ?? null,
            'status' => 'pending',
        ]);

        return response()->json([
            'message' => 'タスクを作成しました',
            'data' => $task
        ], 201);
    }

    /**
     * タスク詳細を取得
     */
    public function show(string $id)
    {
        $task = Task::find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        return response()->json([
            'data' => $task
        ], 200);
    }

    /**
     * タスクを更新
     */
    public function update(Request $request, string $id)
    {
        $task = Task::find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'status' => 'required|in:pending,in_progress,completed',
        ]);

        $task->update($validated);

        return response()->json([
            'message' => 'タスクを更新しました',
            'data' => $task
        ], 200);
    }

    /**
     * タスクを削除
     */
    public function destroy(string $id)
    {
        $task = Task::find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        $task->delete();

        return response()->json(null, 204);
    }
}
```

---

**コードリーディング**

**indexメソッド**

```php
public function index()
{
    $tasks = Task::all();

    return response()->json([
        'data' => $tasks
    ], 200);
}
```

| 行 | コード | 説明 |
|:---|:---|:---|
| 1 | `$tasks = Task::all();` | 全てのタスクを取得 |
| 2 | `return response()->json([...], 200);` | JSON形式でレスポンスを返す |
| 3 | `'data' => $tasks` | レスポンスのキー名を`data`に統一 |
| 4 | `200` | ステータスコード（OK） |

---

**storeメソッド**

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'description' => 'nullable|string',
    ]);

    $task = Task::create([
        'user_id' => 1,
        'title' => $validated['title'],
        'description' => $validated['description'] ?? null,
        'status' => 'pending',
    ]);

    return response()->json([
        'message' => 'タスクを作成しました',
        'data' => $task
    ], 201);
}
```

| 行 | コード | 説明 |
|:---|:---|:---|
| 1 | `$validated = $request->validate([...]);` | バリデーションを実行 |
| 2 | `'title' => 'required\|string\|max:255'` | タイトルは必須、文字列、最大255文字 |
| 3 | `'user_id' => 1` | ユーザーIDを1に固定（認証なしのため） |
| 4 | `$validated['description'] ?? null` | descriptionがなければnull |
| 5 | `201` | ステータスコード（Created） |

---

**showメソッド**

```php
public function show(string $id)
{
    $task = Task::find($id);

    if (!$task) {
        return response()->json([
            'message' => 'タスクが見つかりません'
        ], 404);
    }

    return response()->json([
        'data' => $task
    ], 200);
}
```

| 行 | コード | 説明 |
|:---|:---|:---|
| 1 | `$task = Task::find($id);` | IDでタスクを検索（見つからなければnull） |
| 2 | `if (!$task)` | タスクが見つからない場合 |
| 3 | `404` | ステータスコード（Not Found） |

---

**updateメソッド**

```php
public function update(Request $request, string $id)
{
    $task = Task::find($id);

    if (!$task) {
        return response()->json([
            'message' => 'タスクが見つかりません'
        ], 404);
    }

    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'description' => 'nullable|string',
        'status' => 'required|in:pending,in_progress,completed',
    ]);

    $task->update($validated);

    return response()->json([
        'message' => 'タスクを更新しました',
        'data' => $task
    ], 200);
}
```

| 行 | コード | 説明 |
|:---|:---|:---|
| 1 | `$task = Task::find($id);` | IDでタスクを検索 |
| 2 | `if (!$task)` | タスクが見つからない場合は404 |
| 3 | `$request->validate([...])` | バリデーションを実行 |
| 4 | `$task->update($validated)` | タスクを更新 |
| 5 | `200` | ステータスコード（OK） |

---

**destroyメソッド**

```php
public function destroy(string $id)
{
    $task = Task::find($id);

    if (!$task) {
        return response()->json([
            'message' => 'タスクが見つかりません'
        ], 404);
    }

    $task->delete();

    return response()->json(null, 204);
}
```

| 行 | コード | 説明 |
|:---|:---|:---|
| 1 | `$task->delete();` | タスクを削除 |
| 2 | `null` | レスポンスボディなし |
| 3 | `204` | ステータスコード（No Content） |

---

#### ステップ3: ルーティングを設定する

**何を考えているか**：
- 「`apiResource`で一括登録しよう」
- 「これで5つのルートが自動生成される」

**ファイル**: `routes/api.php`

```php
<?php

use App\Http\Controllers\TaskController;
use Illuminate\Support\Facades\Route;

Route::get('/hello', function () {
    return response()->json(['message' => 'Hello, API!']);
});

Route::apiResource('tasks', TaskController::class);
```

**apiResourceが生成するルート**:

| HTTPメソッド | URL | コントローラーメソッド |
|-------------|-----|---------------------|
| GET | /api/tasks | index |
| POST | /api/tasks | store |
| GET | /api/tasks/{id} | show |
| PUT/PATCH | /api/tasks/{id} | update |
| DELETE | /api/tasks/{id} | destroy |

---

#### ステップ4: Postmanで動作確認する

**何を考えているか**：
- 「各操作が正しく動作するか確認しよう」
- 「ステータスコードも確認しよう」

**タスク一覧を取得（GET）**:
- メソッド: `GET`
- URL: `http://localhost/api/tasks`
- 期待: ステータスコード `200 OK`

**レスポンス例**:

```json
{
  "data": [
    {
      "id": 1,
      "user_id": 1,
      "title": "企画書を作成する",
      "description": "来週の会議に向けて企画書を準備する",
      "status": "pending",
      ...
    },
    ...
  ]
}
```

> 💡 **ポイント**: シーダーで作成されたサンプルタスクが表示されます。

---

**タスクを作成（POST）**:
- メソッド: `POST`
- URL: `http://localhost/api/tasks`
- Headers:
  - `Content-Type: application/json`
- Body（JSON）:

```json
{
  "title": "新しいタスク",
  "description": "これはテストタスクです"
}
```

- 期待: ステータスコード `201 Created`

---

**タスク詳細を取得（GET）**:
- メソッド: `GET`
- URL: `http://localhost/api/tasks/1`
- 期待: ステータスコード `200 OK`

---

**タスクを更新（PUT）**:
- メソッド: `PUT`
- URL: `http://localhost/api/tasks/1`
- Headers:
  - `Content-Type: application/json`
- Body（JSON）:

```json
{
  "title": "更新されたタスク",
  "description": "説明も更新しました",
  "status": "completed"
}
```

- 期待: ステータスコード `200 OK`

---

**タスクを削除（DELETE）**:
- メソッド: `DELETE`
- URL: `http://localhost/api/tasks/1`
- 期待: ステータスコード `204 No Content`

---

**エラーケースの確認**

**バリデーションエラー（422）**:
- メソッド: `POST`
- URL: `http://localhost/api/tasks`
- Headers:
  - `Content-Type: application/json`
  - `Accept: application/json`
- Body（JSON）:

```json
{
  "title": ""
}
```

- 期待: ステータスコード `422 Unprocessable Entity`

**レスポンス例**:

```json
{
  "message": "The title field is required.",
  "errors": {
    "title": [
      "The title field is required."
    ]
  }
}
```

> 💡 **ポイント**: `Accept: application/json`ヘッダーを付けることで、エラーがJSON形式で返ります。

---

**存在しないタスク（404）**:
- メソッド: `GET`
- URL: `http://localhost/api/tasks/9999`
- 期待: ステータスコード `404 Not Found`

**レスポンス例**:

```json
{
  "message": "タスクが見つかりません"
}
```

---

### ✨ 完成！

これでタスク管理APIのCRUD実装が完了しました！

**自分で作成したプロジェクトと比較してみましょう**：
- `task-crud-practice/app/Http/Controllers/TaskController.php`: 自分で作成したコード
- `task-crud-sample/app/Http/Controllers/TaskController.php`: 一緒に作成したコード

両方のファイルを比較して、実装内容を確認してみてください。

---

## 🚨 うまくいかない場合

### エラー1: 500 Internal Server Error

**原因**: Taskモデルの`$fillable`が設定されていない可能性

**対処法**: `app/Models/Task.php`を確認

```php
protected $fillable = [
    'user_id',
    'title',
    'description',
    'status',
];
```

---

### エラー2: HTMLが返ってくる

**原因**: `Accept: application/json`ヘッダーがない

**対処法**: PostmanのHeadersタブで`Accept: application/json`を追加

---

### デバッグの方法

```php
public function store(Request $request)
{
    \Log::info('リクエストデータ:', $request->all());
    
    // ... 以下省略
}
```

```bash
sail logs
```

---

## 📖 模範解答

### TaskController.php

```php
<?php

namespace App\Http\Controllers;

use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    public function index()
    {
        $tasks = Task::all();

        return response()->json([
            'data' => $tasks
        ], 200);
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
        ]);

        $task = Task::create([
            'user_id' => 1,
            'title' => $validated['title'],
            'description' => $validated['description'] ?? null,
            'status' => 'pending',
        ]);

        return response()->json([
            'message' => 'タスクを作成しました',
            'data' => $task
        ], 201);
    }

    public function show(string $id)
    {
        $task = Task::find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        return response()->json([
            'data' => $task
        ], 200);
    }

    public function update(Request $request, string $id)
    {
        $task = Task::find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'status' => 'required|in:pending,in_progress,completed',
        ]);

        $task->update($validated);

        return response()->json([
            'message' => 'タスクを更新しました',
            'data' => $task
        ], 200);
    }

    public function destroy(string $id)
    {
        $task = Task::find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        $task->delete();

        return response()->json(null, 204);
    }
}
```

### routes/api.php

```php
<?php

use App\Http\Controllers\TaskController;
use Illuminate\Support\Facades\Route;

Route::apiResource('tasks', TaskController::class);
```

---

## 📤 GitHubに push しよう

5-1-7 で覚えた手順を使って、成果物をGitHubの **publicリポジトリ** に push しましょう。

```bash
# task-crud-practice ディレクトリに移動
cd ~/api-practice/11-2-8_hands-on/task-crud-practice

# Git の初期化、commit、リモート設定、push
git init
git add .
git commit -m "first commit"
git remote add origin <あなたのリポジトリのURL>
git branch -M main
git push -u origin main
```

> ⚠️ **詰まったときは**: Tutorial 5-1-7「📤 GitHubに push しよう」や Tutorial 4-4-2〜4-4-3 を見直してみましょう。

### ✅ push 完了チェック

- [ ] GitHub に `task-crud-practice` リポジトリを作成した（**public** で作成）
- [ ] 「📦 GitHubでのコード管理」の雛形を参考に `README.md` を **自分の言葉で** 作成した
- [ ] `commit` と `push` を完了して、GitHubに反映されている

---

## 🚀 まとめ

このハンズオンでは、タスク管理APIのCRUD操作を実装しました。

| Step | 学んだこと |
|------|-----------|
| 1 | TaskControllerを作成する |
| 2 | CRUDメソッドを実装する |
| 3 | ルーティングを設定する |
| 4 | Postmanで動作確認する |

**実装したAPI**:

| HTTPメソッド | URL | 操作 | ステータスコード |
|-------------|-----|------|----------------|
| GET | /api/tasks | 一覧取得 | 200 |
| POST | /api/tasks | 作成 | 201 / 422 |
| GET | /api/tasks/{id} | 詳細取得 | 200 / 404 |
| PUT | /api/tasks/{id} | 更新 | 200 / 404 / 422 |
| DELETE | /api/tasks/{id} | 削除 | 204 / 404 |

次のChapter 3では、このAPIにセキュリティ対策を追加します。

---
