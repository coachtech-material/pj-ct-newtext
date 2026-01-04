# Tutorial 13-1-7: ハンズオン - API開発環境の構築と疎通確認

## 🎯 このハンズオンで学ぶこと

- API開発専用のプロジェクトをセットアップする
- Thunder Clientを使って「Hello World」レベルの通信を確認する
- APIが正常に動作することを確認する

---

## 🛠️ 事前準備

このハンズオンでは、**Tutorial 13専用のスターターキット**を使用します。

スターターキットには以下が含まれています:

| 項目 | 内容 |
|------|------|
| Laravel | 10.x |
| データベース | `users`テーブル、`tasks`テーブル（マイグレーション済み） |
| 初期データ | テスト用ユーザー（ID: 1）がシーダーで作成済み |
| 認証 | なし（認証機能は含まれていません） |

> 💡 **ポイント**: このスターターキットを使うことで、環境構築に時間を取られることなく、API開発の本質的な学習に集中できます。

---

## Step 1: プロジェクトのセットアップ

### 1-1. スターターキットをクローン

ターミナルで以下のコマンドを実行します。

```bash
git clone https://github.com/coachtech/laravel-api-starter.git api-practice
```

| 部分 | 説明 |
|------|------|
| `git clone` | リポジトリをコピーする |
| `https://github.com/...` | スターターキットのURL |
| `api-practice` | プロジェクトのディレクトリ名 |

---

### 1-2. プロジェクトディレクトリに移動

```bash
cd api-practice
```

---

### 1-3. 環境変数ファイルを作成

```bash
cp .env.example .env
```

---

### 1-4. Docker環境を起動

```bash
./vendor/bin/sail up -d
```

| 部分 | 説明 |
|------|------|
| `./vendor/bin/sail` | Laravel Sailコマンド |
| `up` | コンテナを起動 |
| `-d` | バックグラウンドで実行 |

> 💡 **ポイント**: 初回起動時は、Dockerイメージのダウンロードに時間がかかる場合があります。

---

### 1-5. データベースの準備

```bash
sail artisan migrate:fresh --seed
```

| 部分 | 説明 |
|------|------|
| `migrate:fresh` | テーブルを再作成 |
| `--seed` | シーダーを実行（テストユーザーを作成） |

---

### 1-6. セットアップ完了の確認

ブラウザで `http://localhost` にアクセスし、Laravelのウェルカムページが表示されることを確認します。

---

## Step 2: 疎通確認用APIの作成

### 2-1. api.phpを編集

**ファイル**: `routes/api.php`

以下のコードを追加します。

```php
<?php

use Illuminate\Support\Facades\Route;

Route::get('/hello', function () {
    return response()->json(['message' => 'Hello, API!']);
});
```

---

### 2-2. コードリーディング

#### `Route::get('/hello', function () { ... })`

```php
Route::get('/hello', function () {
```

| 部分 | 説明 |
|------|------|
| `Route::get()` | GETリクエストを受け付けるルートを定義 |
| `'/hello'` | URLパス（`/api/hello`になる） |
| `function () { ... }` | リクエストを処理するクロージャ |

---

#### `return response()->json(['message' => 'Hello, API!'])`

```php
return response()->json(['message' => 'Hello, API!']);
```

| 部分 | 説明 |
|------|------|
| `response()` | レスポンスを作成するヘルパー関数 |
| `->json()` | JSON形式でレスポンスを返す |
| `['message' => 'Hello, API!']` | レスポンスのデータ |

---

### 2-3. APIのURLについて

`routes/api.php`に定義したルートは、自動的に`/api`プレフィックスが付きます。

| 定義 | 実際のURL |
|------|----------|
| `/hello` | `http://localhost/api/hello` |
| `/tasks` | `http://localhost/api/tasks` |

---

## Step 3: Thunder Clientで動作確認

### 3-1. Thunder Clientを開く

VS Codeの左サイドバーから、Thunder Clientのアイコンをクリックします。

---

### 3-2. 新しいリクエストを作成

1. 「New Request」をクリック
2. メソッド: `GET`
3. URL: `http://localhost/api/hello`

---

### 3-3. リクエストを送信

「Send」ボタンをクリックします。

---

### 3-4. レスポンスを確認

以下のJSONレスポンスが返ってくることを確認します。

```json
{
  "message": "Hello, API!"
}
```

**ステータスコード**: `200 OK`

---

### 3-5. 成功の確認ポイント

| 確認項目 | 期待値 |
|----------|--------|
| ステータスコード | 200 OK |
| Content-Type | application/json |
| レスポンスボディ | `{"message": "Hello, API!"}` |

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

## ✨ まとめ

このハンズオンでは、API開発環境の構築と疎通確認を行いました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | スターターキットのセットアップ |
| Step 2 | 疎通確認用APIの作成 |
| Step 3 | Thunder Clientでの動作確認 |

**確認できたこと**:

- Laravelプロジェクトが正常に起動している
- `routes/api.php`にルートを定義できる
- Thunder ClientでAPIにリクエストを送信できる
- JSONレスポンスが正しく返ってくる

次のChapter 2では、このプロジェクトにタスク管理APIのCRUD機能を実装します。

---
