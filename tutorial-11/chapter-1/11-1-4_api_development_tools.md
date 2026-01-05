# Tutorial 11-1-4: API開発環境の準備

> **📝 本チュートリアルでのツール選定について**
>
> APIテストツールの業界標準は**Postman**ですが、本チュートリアルでは**Thunder Client**を使用します。
>
> | 項目 | Thunder Client | Postman |
> |:---|:---|:---|
> | 環境 | VSCode拡張機能 | スタンドアロンアプリ |
> | 導入 | 拡張機能をインストールするだけ | 別途アプリのインストールが必要 |
> | 動作 | 軽量・高速 | 機能豊富だがやや重い |
> | 学習コスト | 低い | やや高い |
>
> Thunder Clientは、VSCodeから離れずにAPIテストができるため、学習段階ではよりシンプルに始められます。Postmanの基本的な使い方も本セクションで紹介しますので、実務ではチームの方針に合わせて選択してください。

---

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
2. URLを入力: `http://localhost/api/tasks`
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
2. URLを入力: `http://localhost/api/tasks`
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
2. `header` / `value` の入力欄に直接入力

**例**:

| header | value |
|------|-----|
| Authorization | Bearer トークン |
| Content-Type | application/json |

> 💡 **ポイント**: Thunder Clientでは、「Body」タブで「JSON」を選択すると、`Content-Type: application/json`は自動的に設定されます。

---

### 2-4. リクエストを保存する

リクエストを保存すると、後で再利用できます。

Thunder Clientでは、「Send」後に自動的に「Activity」に履歴が保存されます。これをCollectionに保存することで、整理して管理できます。

**Collectionへの保存手順**:

1. 「Send」でリクエストを送信
2. 左サイドバーの「Activity」に表示されたリクエストを右クリック
3. 「Save to Collection」を選択
4. 保存先のCollectionを選択（または「New Collection」で新規作成）
5. 「New Name」に名前を入力（例: 「タスク一覧取得」）
6. 「Submit」をクリック

保存したリクエストは、左側の「Collections」に表示されます。

> 💡 **ポイント**: Collectionを作成しておくと、「タスクAPI」「ユーザーAPI」などカテゴリごとにリクエストを整理できます。

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
| BASE_URL | http://localhost |

URLを`{{BASE_URL}}/api/tasks`と書くと、`http://localhost/api/tasks`に置き換えられます。

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

**対処法**: `./vendor/bin/sail up -d`でDockerコンテナを起動します。

```bash
# プロジェクトディレクトリで実行
cd ~/laravel-practice/your-project-name
./vendor/bin/sail up -d
```

---

## 💡 TIP: curlコマンドを使う

ターミナルから、curlコマンドでAPIをテストすることもできます。

```bash
# GETリクエスト
curl http://localhost/api/tasks

# POSTリクエスト
curl -X POST http://localhost/api/tasks \
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
