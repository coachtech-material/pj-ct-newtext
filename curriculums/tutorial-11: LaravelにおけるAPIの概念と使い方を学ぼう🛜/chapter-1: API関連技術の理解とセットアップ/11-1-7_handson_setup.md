# Tutorial 11-1-7: ハンズオン - API開発環境の構築と疎通確認

## 📌 このハンズオンについて

Chapter 1で学んだAPI開発の基礎知識を実際に手を動かして確認します。スターターキットを使って環境を構築し、Postmanで疎通確認を行いましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

### 📁 ディレクトリ構成

このハンズオンでは、「自分で作成する用」と「解答を確認する用」の2つのプロジェクトを作成します。

```
~/api-practice/
├── 11-1-7_hands-on/                         ← このハンズオン用のディレクトリ
│   ├── api-setup-practice/                  ← 要件を見て自分で作成するプロジェクト
│   │   └── routes/api.php
│   └── api-setup-sample/                    ← 実践で一緒に作成するプロジェクト
│       └── routes/api.php
└── ...
```

| ディレクトリ | 用途 |
|:---|:---|
| `api-setup-practice/` | 📋 要件を見て、自分の力で作成する |
| `api-setup-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したプロジェクトと、解答を見ながら作成したプロジェクトを比較することで、理解が深まります。

---

## 🎯 演習課題：API疎通確認

### この演習で作るもの

API開発専用のプロジェクトをセットアップし、「Hello World」レベルの疎通確認を行います。

このハンズオンでは、**Tutorial 11専用のスターターキット**を使用します。

### スターターキットに含まれるもの

| 項目 | 内容 |
|------|------|
| Laravel | 10.x |
| データベース | `users`テーブル、`tasks`テーブル（マイグレーション済み） |
| 初期データ | テスト用ユーザー（ID: 1）、サンプルタスク5件がシーダーで作成済み |
| 認証 | なし（認証機能は含まれていません） |

> 💡 **ポイント**: このスターターキットを使うことで、環境構築に時間を取られることなく、API開発の本質的な学習に集中できます。

### 📋 要件

- `/api/hello`にGETリクエストを送ると、JSONレスポンスが返ってくる
- Postmanでリクエスト送信・レスポンス確認ができる

### ✅ 完成チェックリスト

- [ ] `http://localhost/api/hello`にGETリクエストを送信できる
- [ ] ステータスコード`200 OK`が返ってくる
- [ ] `{"message": "Hello, API!"}`というJSONが返ってくる

> 💡 **動作確認**: PostmanでGETリクエストを送信

### ✏️ 実装タスク

1. `routes/api.php`に疎通確認用のAPIを作成する
2. Postmanで動作確認する

---

## ⚙️ 環境準備（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

### Step 1: ディレクトリを作成

```bash
# api-practiceディレクトリに移動（なければ作成）
mkdir -p ~/api-practice
cd ~/api-practice

# ハンズオン用ディレクトリを作成
mkdir -p 11-1-7_hands-on
cd 11-1-7_hands-on
```

### Step 2: スターターキットをクローン

```bash
# 自分で作成する用のプロジェクトをクローン
git clone https://github.com/coachtech-material/laravel-api-starter.git api-setup-practice
cd api-setup-practice
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
└── 11-1-7_hands-on/
    └── api-setup-practice/     ← 自分で作成する用（今ここ）
        ├── routes/
        │   └── api.php
        └── ...
```

> 💡 **環境構築が完了！**
> 
> `routes/api.php`に疎通確認用のAPIを作成してみましょう。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

```php
// routes/api.php

Route::get('/hello', function () {
    return response()->json(['message' => 'Hello, API!']);
});
```

---

## 🏃 実践セクション：一緒に作ってみましょう！

ちゃんとできましたか？API開発環境の構築は、API開発の第一歩です。一緒に手を動かしながら、疎通確認用のAPIを作成していきましょう。

> 📌 **注意**: ここからは`api-setup-sample/`ディレクトリで作業します。自分で作成したプロジェクトと比較できるように、別のプロジェクトで進めましょう。

---

### ⚙️ 環境準備（実践用プロジェクト）

### Step 1: 自分で作成したプロジェクトを停止

まず、自分で作成したプロジェクトのDockerコンテナを停止します。

```bash
# api-setup-practiceディレクトリで実行
cd ~/api-practice/11-1-7_hands-on/api-setup-practice
sail down
```

### Step 2: 実践用のプロジェクトをクローン

```bash
# ハンズオンディレクトリに移動
cd ~/api-practice/11-1-7_hands-on

# 実践用のプロジェクトをクローン
git clone https://github.com/coachtech-material/laravel-api-starter.git api-setup-sample
cd api-setup-sample
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
└── 11-1-7_hands-on/
    ├── api-setup-practice/     ← 自分で作成した用
    └── api-setup-sample/       ← 実践用（今ここ）
        ├── routes/
        │   └── api.php
        └── ...
```

---

### 🧠 先輩エンジニアの思考プロセス

先輩エンジニアは要件を以下のように構造化し、実装タスクに落とし込みます：

| Step | やること | 説明 |
|:-----|:---------|:-----|
| 1 | `routes/api.php`に疎通確認用のAPIを作成する | GETリクエストでJSONを返すシンプルなエンドポイント |
| 2 | Postmanで動作確認する | ステータスコードとレスポンスを確認 |

---

### 📝 ステップバイステップで実装

#### ステップ1: routes/api.phpに疎通確認用のAPIを作成する

**何を考えているか**：
- 「疎通確認用のシンプルなAPIを作成しよう」
- 「GETリクエストでJSONを返すエンドポイントを作ろう」

**ファイル**: `routes/api.php`

以下のコードを追加します。

```php
<?php

use Illuminate\Support\Facades\Route;

Route::get('/hello', function () {
    return response()->json(['message' => 'Hello, API!']);
});
```

**コードリーディング**

```php
Route::get('/hello', function () {
```

| 部分 | 説明 |
|------|------|
| `Route::get()` | GETリクエストを受け付けるルートを定義 |
| `'/hello'` | URLパス（`/api/hello`になる） |
| `function () { ... }` | リクエストを処理するクロージャ |

```php
return response()->json(['message' => 'Hello, API!']);
```

| 部分 | 説明 |
|------|------|
| `response()` | レスポンスを作成するヘルパー関数 |
| `->json()` | JSON形式でレスポンスを返す |
| `['message' => 'Hello, API!']` | レスポンスのデータ |

> 💡 **ポイント**: `routes/api.php`に定義したルートは、自動的に`/api`プレフィックスが付きます。`/hello`と定義すると、実際のURLは`http://localhost/api/hello`になります。

---

#### ステップ2: Postmanで動作確認する

**何を考えているか**：
- 「APIが正常に動作するか確認しよう」
- 「Postmanでリクエストを送信しよう」

1. Postmanを起動する
2. 「+」タブをクリックして新しいリクエストを作成
3. メソッド: `GET`
4. URL: `http://localhost/api/hello`
5. 「Send」ボタンをクリック

**レスポンスを確認**

以下のJSONレスポンスが返ってくることを確認します。

```json
{
  "message": "Hello, API!"
}
```

**ステータスコード**: `200 OK`

---

### ✨ 完成！

これでAPI開発環境の構築と疎通確認が完了しました！

**確認ポイント**

| 確認項目 | 期待値 |
|----------|--------|
| ステータスコード | 200 OK |
| Content-Type | application/json |
| レスポンスボディ | `{"message": "Hello, API!"}` |

**自分で作成したプロジェクトと比較してみましょう**：
- `api-setup-practice/routes/api.php`: 自分で作成したコード
- `api-setup-sample/routes/api.php`: 一緒に作成したコード

両方のファイルを比較して、実装内容を確認してみてください。

---

## 📖 模範解答

### routes/api.php

```php
<?php

use Illuminate\Support\Facades\Route;

Route::get('/hello', function () {
    return response()->json(['message' => 'Hello, API!']);
});
```

---

## 🚨 うまくいかない場合

### エラー1: Connection refused

**原因**: Dockerコンテナが起動していない

**対処法**:

```bash
sail up -d
```

---

### エラー2: 404 Not Found

**原因**: ルートが正しく定義されていない

**対処法**:

1. `routes/api.php`のコードを確認
2. URLが`http://localhost/api/hello`になっているか確認

---

### エラー3: 500 Internal Server Error

**原因**: PHPのエラーが発生している

**対処法**:

```bash
sail logs
```

ログを確認してエラーの原因を特定します。

---

## 💡 TIP: デバッグの方法

意図しない挙動になった場合は、`\Log::info()`を使ってデバッグできます。

**routes/api.php**:

```php
Route::get('/hello', function () {
    \Log::info('Hello APIが呼ばれました');
    return response()->json(['message' => 'Hello, API!']);
});
```

**ログの確認**:

```bash
sail logs
```

---

## 🚀 まとめ

このハンズオンでは、API開発環境の構築と疎通確認を行いました。

| Step | 学んだこと |
|------|-----------|
| 1 | `routes/api.php`に疎通確認用のAPIを作成する |
| 2 | Postmanで動作確認する |

**確認できたこと**:

- ✅ Laravelプロジェクトが正常に起動している
- ✅ `routes/api.php`にルートを定義できる
- ✅ PostmanでAPIにリクエストを送信できる
- ✅ JSONレスポンスが正しく返ってくる

次のChapter 2では、このプロジェクトにタスク管理APIのCRUD機能を実装します。

---
