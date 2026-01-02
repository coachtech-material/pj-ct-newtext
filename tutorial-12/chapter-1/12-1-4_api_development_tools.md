# Tutorial 12-1-4: API開発環境の準備

## 🎯 このセクションで学ぶこと

- APIテストツールの必要性を理解する
- Thunder Client（VSCode拡張）をインストールして使う方法を学ぶ
- Postmanの基本的な使い方を学ぶ
- APIリクエストの送信方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜJSONの後に『開発ツール』を学ぶのか？」

JSONを理解したら、次は「開発ツール」です。

---

### 理由1: ブラウザだけでは不十分

WebアプリケーションはブラウザでテストできますがAPIは**専用のツール**が必要です。

POST、PUT、DELETEリクエストは、ブラウザのアドレスバーからは送れません。

---

### 理由2: 効率的な開発

**Postman**や**Thunder Client**などのツールを使うと、APIの開発・テストが効率的になります。

| 機能 | 説明 |
|------|------|
| リクエストの保存 | 繰り返し使える |
| レスポンスの確認 | 見やすく整形される |
| 認証ヘッダーの設定 | 簡単に設定できる |

---

### 理由3: チームでの共有

APIの仕様を**ツールで共有**できます。

Postmanのコレクションを共有すれば、チーム全員が同じAPIをテストできます。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | Thunder Clientのインストール | VSCodeから使える |
| Step 2 | リクエストの送信 | GET/POSTの基本 |
| Step 3 | Postmanの使い方 | 業界標準ツール |

> 💡 **ポイント**: 開発ツールを使いこなすと、API開発の効率が大幅に上がります。

---

## Step 1: Thunder Clientのインストール

### 1-1. Thunder Clientとは

**Thunder Client**は、**VSCodeの拡張機能**です。

| メリット | デメリット |
|----------|------------|
| VSCodeから出ずにAPIテストができる | VSCodeでしか使えない |
| 軽量で高速 | |
| 無料で使える | |

---

### 1-2. インストール手順

1. VSCodeを開く
2. 左側の拡張機能アイコンをクリック
3. 「Thunder Client」と検索
4. 「インストール」をクリック

---

### 1-3. 基本的な使い方

1. 左側に稲妻アイコンが表示される
2. 稲妻アイコンをクリック
3. 「New Request」をクリック
4. リクエストを設定して送信

---

## Step 2: リクエストの送信

### 2-1. GETリクエストを送信する

**例**: タスク一覧を取得する

1. メソッドを「GET」に設定
2. URLを入力: `http://localhost:8000/api/tasks`
3. 「Send」をクリック

**レスポンス例**:

```json
[
  {
    "id": 1,
    "title": "Laravelを学ぶ",
    "status": "pending"
  },
  {
    "id": 2,
    "title": "APIを実装する",
    "status": "in_progress"
  }
]
```

---

### 2-2. POSTリクエストを送信する

**例**: タスクを作成する

1. メソッドを「POST」に設定
2. URLを入力: `http://localhost:8000/api/tasks`
3. 「Body」タブをクリック
4. 「JSON」を選択
5. 以下のJSONを入力:

```json
{
  "title": "新しいタスク",
  "description": "テスト説明",
  "status": "pending",
  "priority": 3
}
```

6. 「Send」をクリック

---

### 2-3. ヘッダーを設定する

APIによっては、ヘッダーを設定する必要があります。

1. 「Headers」タブをクリック
2. 「Add Header」をクリック
3. キーと値を入力

**例**:

| キー | 値 |
|------|-----|
| Authorization | Bearer トークン |
| Content-Type | application/json |

---

### 2-4. リクエストを保存する

リクエストを保存すると、後で再利用できます。

1. リクエストを設定
2. 「Save」をクリック
3. 名前を入力（例: 「タスク一覧取得」）
4. 「Save」をクリック

保存したリクエストは、左側の「Collections」に表示されます。

---

### 2-5. 実践演習

以下のAPIにGETリクエストを送信してください。

**URL**: `https://jsonplaceholder.typicode.com/users/1`

**期待されるレスポンス**:

```json
{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz"
}
```

---

## Step 3: Postmanの使い方

### 3-1. Postmanとは

**Postman**は、**業界標準のAPIテストツール**です。

| メリット | デメリット |
|----------|------------|
| 機能が豊富 | アプリを別途起動する必要がある |
| チームで共有できる | やや重い |
| 業界標準 | |

---

### 3-2. インストール手順

1. [Postman公式サイト](https://www.postman.com/)にアクセス
2. 「Download」をクリック
3. インストーラーをダウンロード
4. インストーラーを実行

---

### 3-3. 基本的な使い方

1. Postmanを起動
2. 「New」→「HTTP Request」をクリック
3. リクエストを設定して送信

**基本的な使い方は、Thunder Clientと同じです。**

---

### 3-4. Thunder ClientとPostmanの使い分け

| ツール | 用途 |
|--------|------|
| Thunder Client | 日常的な開発、個人開発 |
| Postman | チーム開発、複雑なテスト |

---

### 3-5. 環境変数を使う

Thunder ClientとPostmanでは、環境変数を使えます。

**設定例**:

| 変数名 | 値 |
|--------|-----|
| BASE_URL | http://localhost:8000 |

URLを`{{BASE_URL}}/api/tasks`と書くと、`http://localhost:8000/api/tasks`に置き換えられます。

---

## 🚨 よくある間違い

### 間違い1: Content-Typeを設定し忘れる

**問題**: POSTリクエストでJSONを送信する場合、`Content-Type: application/json`が必要

**対処法**: Thunder Clientでは、「Body」→「JSON」を選択すると、自動的に設定されます。

---

### 間違い2: URLを間違える

**問題**: URLを間違えると、404エラーが返される

**対処法**: URLを確認します。

---

### 間違い3: サーバーが起動していない

**問題**: サーバーが起動していないと、接続エラーが返される

**対処法**: `php artisan serve`でサーバーを起動します。

---

## 💡 TIP: curlコマンドを使う

ターミナルから、curlコマンドでAPIをテストすることもできます。

```bash
# GETリクエスト
curl http://localhost:8000/api/tasks

# POSTリクエスト
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"新しいタスク","status":"pending"}'
```

---

## ✨ まとめ

このセクションでは、API開発環境の準備を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | Thunder Clientのインストールと設定 |
| Step 2 | GET/POSTリクエストの送信とヘッダー設定 |
| Step 3 | Postmanの使い方と環境変数 |

次のセクションでは、LaravelでのAPIルーティングについて学びます。

---
