# Tutorial 11-1-4: API設計（オプション）

## 🎯 このセクションで学ぶこと

*   RESTful APIのエンドポイントを設計する方法を学ぶ。
*   HTTPメソッド（GET、POST、PUT、DELETE）の使い分けを理解する。
*   APIのリクエストとレスポンスの形式を設計する。

---

## 導入：なぜAPI設計が重要なのか

**API（Application Programming Interface）**とは、**アプリケーション間でデータをやり取りするための仕組み**です。

API設計を行うことで、以下のようなメリットがあります。

*   **フロントエンドとバックエンドの分離**: フロントエンドとバックエンドを独立して開発できる
*   **モバイルアプリとの連携**: 同じAPIを使って、Webアプリとモバイルアプリを開発できる
*   **外部サービスとの連携**: 他のサービスがAPIを使ってデータを取得できる

このセクションでは、タスク管理システムのAPIを設計します。

**注意**: このセクションはオプションです。API開発を行わない場合は、スキップしても構いません。

---

## 詳細解説

### 🔍 RESTful APIとは

**RESTful API**とは、**REST（Representational State Transfer）の原則に従ったAPI**です。

RESTful APIの特徴は、以下の通りです。

*   **リソース指向**: URLでリソース（タスク、ユーザーなど）を表現する
*   **HTTPメソッドの使用**: GET、POST、PUT、DELETEなどのHTTPメソッドを使う
*   **ステートレス**: サーバーはクライアントの状態を保持しない

---

### 🔍 HTTPメソッドの使い分け

RESTful APIでは、HTTPメソッドを使って操作を表現します。

| HTTPメソッド | 操作 | 例 |
|---|---|---|
| GET | リソースの取得 | タスク一覧を取得 |
| POST | リソースの作成 | 新しいタスクを作成 |
| PUT | リソースの更新（全体） | タスクを更新 |
| PATCH | リソースの更新（一部） | タスクのステータスを更新 |
| DELETE | リソースの削除 | タスクを削除 |

---

### 🔍 タスク管理システムのAPIエンドポイント

タスク管理システムのAPIエンドポイントを設計します。

#### 1. タスク一覧の取得

**エンドポイント**: `GET /api/tasks`

**説明**: ログインユーザーのタスク一覧を取得する

**リクエスト**: なし

**レスポンス**:

```json
{
  "data": [
    {
      "id": 1,
      "title": "タスク1",
      "description": "これはタスク1の説明です。",
      "due_date": "2024-12-31",
      "status": "未完了",
      "created_at": "2024-12-01T10:00:00Z",
      "updated_at": "2024-12-01T10:00:00Z"
    },
    {
      "id": 2,
      "title": "タスク2",
      "description": "これはタスク2の説明です。",
      "due_date": "2024-12-25",
      "status": "完了",
      "created_at": "2024-12-01T11:00:00Z",
      "updated_at": "2024-12-01T11:00:00Z"
    }
  ]
}
```

---

#### 2. タスクの詳細取得

**エンドポイント**: `GET /api/tasks/{id}`

**説明**: 指定したIDのタスクの詳細を取得する

**リクエスト**: なし

**レスポンス**:

```json
{
  "data": {
    "id": 1,
    "title": "タスク1",
    "description": "これはタスク1の説明です。",
    "due_date": "2024-12-31",
    "status": "未完了",
    "created_at": "2024-12-01T10:00:00Z",
    "updated_at": "2024-12-01T10:00:00Z"
  }
}
```

---

#### 3. タスクの作成

**エンドポイント**: `POST /api/tasks`

**説明**: 新しいタスクを作成する

**リクエスト**:

```json
{
  "title": "新しいタスク",
  "description": "これは新しいタスクの説明です。",
  "due_date": "2024-12-31",
  "status": "未完了"
}
```

**レスポンス**:

```json
{
  "data": {
    "id": 3,
    "title": "新しいタスク",
    "description": "これは新しいタスクの説明です。",
    "due_date": "2024-12-31",
    "status": "未完了",
    "created_at": "2024-12-01T12:00:00Z",
    "updated_at": "2024-12-01T12:00:00Z"
  }
}
```

---

#### 4. タスクの更新

**エンドポイント**: `PUT /api/tasks/{id}`

**説明**: 指定したIDのタスクを更新する

**リクエスト**:

```json
{
  "title": "更新されたタスク",
  "description": "これは更新されたタスクの説明です。",
  "due_date": "2024-12-31",
  "status": "完了"
}
```

**レスポンス**:

```json
{
  "data": {
    "id": 1,
    "title": "更新されたタスク",
    "description": "これは更新されたタスクの説明です。",
    "due_date": "2024-12-31",
    "status": "完了",
    "created_at": "2024-12-01T10:00:00Z",
    "updated_at": "2024-12-01T13:00:00Z"
  }
}
```

---

#### 5. タスクの削除

**エンドポイント**: `DELETE /api/tasks/{id}`

**説明**: 指定したIDのタスクを削除する

**リクエスト**: なし

**レスポンス**:

```json
{
  "message": "タスクを削除しました。"
}
```

---

### 🔍 認証エンドポイント

ユーザー認証のためのエンドポイントも設計します。

#### 1. ユーザー登録

**エンドポイント**: `POST /api/register`

**説明**: 新しいユーザーを登録する

**リクエスト**:

```json
{
  "name": "Test User",
  "email": "test@example.com",
  "password": "password",
  "password_confirmation": "password"
}
```

**レスポンス**:

```json
{
  "data": {
    "id": 1,
    "name": "Test User",
    "email": "test@example.com",
    "created_at": "2024-12-01T10:00:00Z",
    "updated_at": "2024-12-01T10:00:00Z"
  },
  "token": "1|abcdefghijklmnopqrstuvwxyz"
}
```

---

#### 2. ログイン

**エンドポイント**: `POST /api/login`

**説明**: ユーザーがログインする

**リクエスト**:

```json
{
  "email": "test@example.com",
  "password": "password"
}
```

**レスポンス**:

```json
{
  "data": {
    "id": 1,
    "name": "Test User",
    "email": "test@example.com",
    "created_at": "2024-12-01T10:00:00Z",
    "updated_at": "2024-12-01T10:00:00Z"
  },
  "token": "1|abcdefghijklmnopqrstuvwxyz"
}
```

---

#### 3. ログアウト

**エンドポイント**: `POST /api/logout`

**説明**: ユーザーがログアウトする

**リクエスト**: なし（認証トークンが必要）

**レスポンス**:

```json
{
  "message": "ログアウトしました。"
}
```

---

### 🔍 エラーレスポンス

APIでエラーが発生した場合、適切なエラーレスポンスを返します。

#### バリデーションエラー

**ステータスコード**: `422 Unprocessable Entity`

**レスポンス**:

```json
{
  "message": "The given data was invalid.",
  "errors": {
    "title": [
      "タイトルは必須です。"
    ],
    "due_date": [
      "期限は日付形式で入力してください。"
    ]
  }
}
```

---

#### 認証エラー

**ステータスコード**: `401 Unauthorized`

**レスポンス**:

```json
{
  "message": "Unauthenticated."
}
```

---

#### リソースが見つからない

**ステータスコード**: `404 Not Found`

**レスポンス**:

```json
{
  "message": "タスクが見つかりません。"
}
```

---

### 🔍 ページネーション

タスク一覧が多い場合、ページネーションを実装します。

**エンドポイント**: `GET /api/tasks?page=1`

**レスポンス**:

```json
{
  "data": [
    {
      "id": 1,
      "title": "タスク1",
      "description": "これはタスク1の説明です。",
      "due_date": "2024-12-31",
      "status": "未完了",
      "created_at": "2024-12-01T10:00:00Z",
      "updated_at": "2024-12-01T10:00:00Z"
    }
  ],
  "links": {
    "first": "http://localhost/api/tasks?page=1",
    "last": "http://localhost/api/tasks?page=3",
    "prev": null,
    "next": "http://localhost/api/tasks?page=2"
  },
  "meta": {
    "current_page": 1,
    "from": 1,
    "last_page": 3,
    "per_page": 15,
    "to": 15,
    "total": 45
  }
}
```

---

### 💡 TIP: API設計ツール

API設計を効率的に行うためのツールがあります。

*   **Postman**: APIのテストとドキュメント作成
*   **Swagger**: OpenAPI仕様に基づいたAPIドキュメント
*   **Insomnia**: APIのテストツール

---

### 🚨 よくある間違い

#### 間違い1: HTTPメソッドを正しく使っていない

**対処法**: GET、POST、PUT、DELETEを適切に使い分けます。

---

#### 間違い2: エラーレスポンスが不明確

**対処法**: エラーメッセージとステータスコードを適切に設定します。

---

#### 間違い3: 認証を考慮していない

**対処法**: 認証が必要なエンドポイントには、トークン認証を実装します。

---

## ✨ まとめ

このセクションでは、API設計について学びました。

*   RESTful APIは、REST の原則に従ったAPI。
*   HTTPメソッド（GET、POST、PUT、DELETE）を使って操作を表現する。
*   エンドポイント、リクエスト、レスポンスの形式を設計する。
*   エラーレスポンスとページネーションも考慮する。

次のセクションでは、開発環境の準備について学びます。

---

## 📝 学習のポイント

- [ ] RESTful APIのエンドポイントを設計した。
- [ ] HTTPメソッドの使い分けを理解した。
- [ ] リクエストとレスポンスの形式を設計した。
- [ ] エラーレスポンスを設計した。
