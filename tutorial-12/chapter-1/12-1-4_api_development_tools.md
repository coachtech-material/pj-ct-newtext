# Tutorial 12-1-4: API開発環境の準備

## 🎯 このセクションで学ぶこと

*   APIテストツールの必要性を理解する。
*   Thunder Client（VSCode拡張）をインストールして使う方法を学ぶ。
*   Postmanの基本的な使い方を学ぶ。
*   APIリクエストの送信方法を学ぶ。

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

- リクエストの保存
- レスポンスの確認
- 認証ヘッダーの設定

---

### 理由3: チームでの共有

APIの仕様を**ツールで共有**できます。

Postmanのコレクションを共有すれば、チーム全員が同じAPIをテストできます。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| 1 | Postmanのインストール | 最も人気のあるAPIツール |
| 2 | 基本的な使い方 | GETリクエストの送信 |
| 3 | リクエストの保存 | 繰り返し使えるように |

> 💡 **ポイント**: 開発ツールを使いこなすと、API開発の効率が大幅に上がります。

---

## 導入：なぜAPIテストツールが必要なのか

APIを開発する際、**ブラウザだけではテストできない**ことがあります。

*   **POST、PUT、DELETEリクエスト**は、ブラウザから送信しにくい
*   **ヘッダーやボディ**を自由に設定したい
*   **レスポンスを確認**したい

**APIテストツール**を使うと、これらの問題を解決できます。

---

## 詳細解説

### 🔍 Thunder Client（推奨）

**Thunder Client**は、**VSCodeの拡張機能**です。

**メリット**:
*   **VSCodeから出ずにAPIテストができる**
*   **軽量で高速**
*   **無料で使える**

**デメリット**:
*   **VSCodeでしか使えない**

---

### 🔍 Thunder Clientのインストール

1.  VSCodeを開く
2.  左側の拡張機能アイコンをクリック
3.  「Thunder Client」と検索
4.  「インストール」をクリック

---

### 🔍 Thunder Clientの使い方

1.  左側に稲妻アイコンが表示される
2.  稲妻アイコンをクリック
3.  「New Request」をクリック
4.  リクエストを設定して送信

---

### 🔍 GETリクエストを送信する

**例**: タスク一覧を取得する

1.  メソッドを「GET」に設定
2.  URLを入力: `http://localhost:8000/api/tasks`
3.  「Send」をクリック

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

### 🔍 POSTリクエストを送信する

**例**: タスクを作成する

1.  メソッドを「POST」に設定
2.  URLを入力: `http://localhost:8000/api/tasks`
3.  「Body」タブをクリック
4.  「JSON」を選択
5.  以下のJSONを入力:

```json
{
  "title": "新しいタスク",
  "description": "テスト説明",
  "status": "pending",
  "priority": 3
}
```

6.  「Send」をクリック

---

### 🔍 ヘッダーを設定する

APIによっては、ヘッダーを設定する必要があります。

1.  「Headers」タブをクリック
2.  「Add Header」をクリック
3.  キーと値を入力

**例**:

*   キー: `Authorization`
*   値: `Bearer トークン`

---

### 🔍 Thunder Clientでリクエストを保存する

リクエストを保存すると、後で再利用できます。

1.  リクエストを設定
2.  「Save」をクリック
3.  名前を入力（例: 「タスク一覧取得」）
4.  「Save」をクリック

保存したリクエストは、左側の「Collections」に表示されます。

---

### 🔍 Postman（業界標準）

**Postman**は、**業界標準のAPIテストツール**です。

**メリット**:
*   **機能が豊富**
*   **チームで共有できる**
*   **業界標準**

**デメリット**:
*   **アプリを別途起動する必要がある**
*   **やや重い**

---

### 🔍 Postmanのインストール

1.  [Postman公式サイト](https://www.postman.com/)にアクセス
2.  「Download」をクリック
3.  インストーラーをダウンロード
4.  インストーラーを実行

---

### 🔍 Postmanの使い方

1.  Postmanを起動
2.  「New」→「HTTP Request」をクリック
3.  リクエストを設定して送信

**基本的な使い方は、Thunder Clientと同じです。**

---

### 🔍 実践演習: Thunder ClientでGETリクエストを送信してください

以下のAPIにGETリクエストを送信してください。

**URL**: `https://jsonplaceholder.typicode.com/users/1`

**期待されるレスポンス**:

```json
{
  "id": 1,
  "name": "Leanne Graham",
  "username": "Bret",
  "email": "Sincere@april.biz",
  ...
}
```

---

### 🔍 Thunder ClientとPostmanの使い分け

**Thunder Client（推奨）**:
*   **日常的な開発**: VSCodeから出ずにAPIテストができる
*   **個人開発**: 軽量で高速

**Postman**:
*   **チーム開発**: リクエストを共有したい
*   **複雑なテスト**: 環境変数やスクリプトを使いたい
*   **業界標準として知っておきたい**

---

### 🔍 環境変数を使う

Thunder ClientとPostmanでは、環境変数を使えます。

**例**:

*   変数名: `BASE_URL`
*   値: `http://localhost:8000`

URLを`{{BASE_URL}}/api/tasks`と書くと、`http://localhost:8000/api/tasks`に置き換えられます。

---

### 🔍 Thunder Clientで環境変数を設定する

1.  左側の「Env」をクリック
2.  「New Environment」をクリック
3.  名前を入力（例: 「Local」）
4.  変数を追加

**例**:

*   変数名: `BASE_URL`
*   値: `http://localhost:8000`

---

### 💡 TIP: curlコマンドを使う

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

### 🚨 よくある間違い

#### 間違い1: Content-Typeを設定し忘れる

POSTリクエストでJSONを送信する場合、`Content-Type: application/json`を設定します。

Thunder Clientでは、「Body」→「JSON」を選択すると、自動的に設定されます。

---

#### 間違い2: URLを間違える

URLを間違えると、404エラーが返されます。

**対処法**: URLを確認します。

---

#### 間違い3: サーバーが起動していない

サーバーが起動していないと、接続エラーが返されます。

**対処法**: `php artisan serve`でサーバーを起動します。

---

## ✨ まとめ

このセクションでは、API開発環境の準備を学びました。

*   Thunder Client（VSCode拡張）をインストールした。
*   GETリクエストとPOSTリクエストを送信した。
*   ヘッダーとボディを設定した。
*   Postmanの基本的な使い方を学んだ。

次のセクションでは、LaravelでのAPI開発の準備について学びます。

---

## 📝 学習のポイント

- [ ] Thunder Clientをインストールした。
- [ ] GETリクエストを送信した。
- [ ] POSTリクエストを送信した。
- [ ] ヘッダーを設定した。
- [ ] リクエストを保存した。
