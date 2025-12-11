# Tutorial 9-7-1: Laravel Sanctumとは

## 🎯 このセクションで学ぶこと

*   Laravel Sanctumが何であるか、その役割を理解する。
*   トークンベース認証の仕組みを理解する。
*   なぜSanctumを使うのか、従来のセッションベース認証との違いを説明できるようになる。

---

## 導入：API開発における認証の必要性

これまでのセクションで、データベース操作、バリデーション、リレーションシップなど、Laravelの基本的な機能を学んできました。しかし、実際のWebアプリケーションでは、**「誰がアクセスしているのか」を識別する仕組み**が必要です。これが**認証（Authentication）**です。

従来のWebアプリケーションでは、**セッションベース認証**が主流でした。これは、ログイン時にサーバー側でセッションを作成し、ブラウザにCookieを保存する方式です。しかし、現代のWeb開発では、フロントエンドとバックエンドを分離し、**REST APIとしてバックエンドを構築する**ことが一般的です。

REST APIでは、セッションベース認証ではなく、**トークンベース認証**が使われます。そして、Laravelでトークンベース認証を実装するための最もシンプルな方法が、**Laravel Sanctum**です。

---

## 詳細解説

### 🔐 セッションベース認証 vs トークンベース認証

まず、2つの認証方式の違いを理解しましょう。

#### セッションベース認証（従来の方式）

```
1. ユーザーがログインフォームにメールアドレスとパスワードを入力
   ↓
2. サーバーがデータベースでユーザーを確認
   ↓
3. サーバーがセッションを作成し、セッションIDをCookieに保存
   ↓
4. 以降のリクエストでは、Cookieに含まれるセッションIDでユーザーを識別
```

**メリット**

*   ブラウザが自動的にCookieを送信するため、実装が簡単

**デメリット**

*   **Cookieはドメインに依存する**: フロントエンド（`frontend.com`）とバックエンド（`api.backend.com`）が異なるドメインの場合、Cookieが送信されない
*   **モバイルアプリでは使えない**: モバイルアプリはCookieを扱いにくい
*   **CSRF攻撃のリスク**: Cookieは自動送信されるため、CSRF攻撃に対する対策が必要

#### トークンベース認証（REST APIの標準）

```
1. ユーザーがログインAPIにメールアドレスとパスワードを送信
   ↓
2. サーバーがデータベースでユーザーを確認
   ↓
3. サーバーがトークン（ランダムな文字列）を生成し、クライアントに返す
   ↓
4. クライアントは、トークンをローカルストレージやメモリに保存
   ↓
5. 以降のリクエストでは、HTTPヘッダーの`Authorization: Bearer {トークン}`でトークンを送信
   ↓
6. サーバーは、トークンをデータベースで照合し、ユーザーを識別
```

**メリット**

*   **ドメインに依存しない**: フロントエンドとバックエンドが異なるドメインでも動作する
*   **モバイルアプリでも使える**: HTTPヘッダーでトークンを送信するだけなので、どのプラットフォームでも使える
*   **CSRF攻撃のリスクがない**: トークンは自動送信されないため、CSRF攻撃を受けにくい

**デメリット**

*   **トークンの管理が必要**: クライアント側でトークンを安全に保存する必要がある

---

### 🛡️ Laravel Sanctumとは？

Laravel Sanctumは、**トークンベース認証を簡単に実装するためのパッケージ**です。以下の2つの機能を提供します。

#### 1. **APIトークン認証（Personal Access Tokens）**

モバイルアプリやSPA（Single Page Application）向けに、トークンベース認証を提供します。ユーザーがログインすると、トークンが発行され、以降のリクエストでそのトークンを使ってユーザーを識別します。

#### 2. **SPA認証（Cookie-based Authentication）**

同一ドメインのSPA（例：LaravelとVue.jsが同じサーバーで動作）向けに、Cookieベースの認証を提供します。これは、セッションベース認証に似ていますが、CSRF保護が強化されています。

このカリキュラムでは、**APIトークン認証**に焦点を当てます。

---

### 📝 Sanctumのインストール

Laravel 11では、Sanctumがデフォルトでインストールされています。もしインストールされていない場合は、以下のコマンドで追加できます。

```bash
docker compose exec php composer require laravel/sanctum
docker compose exec php php artisan vendor:publish --provider="Laravel\Sanctum\SanctumServiceProvider"
docker compose exec php php artisan migrate
```

これにより、`personal_access_tokens`というテーブルが作成されます。このテーブルに、発行されたトークンが保存されます。

---

### 🔑 Sanctumの動作フロー

Sanctumを使った認証の流れは、以下の通りです。

#### 1. ユーザー登録

```
POST /api/register
{
  "name": "山田太郎",
  "email": "taro@example.com",
  "password": "password123"
}

→ レスポンス
{
  "user": { "id": 1, "name": "山田太郎", "email": "taro@example.com" },
  "token": "1|abcdefghijklmnopqrstuvwxyz"
}
```

#### 2. ログイン

```
POST /api/login
{
  "email": "taro@example.com",
  "password": "password123"
}

→ レスポンス
{
  "user": { "id": 1, "name": "山田太郎", "email": "taro@example.com" },
  "token": "2|zyxwvutsrqponmlkjihgfedcba"
}
```

#### 3. 認証が必要なAPIにアクセス

```
GET /api/user
Headers:
  Authorization: Bearer 2|zyxwvutsrqponmlkjihgfedcba

→ レスポンス
{
  "id": 1,
  "name": "山田太郎",
  "email": "taro@example.com"
}
```

#### 4. ログアウト

```
POST /api/logout
Headers:
  Authorization: Bearer 2|zyxwvutsrqponmlkjihgfedcba

→ レスポンス
{
  "message": "ログアウトしました"
}
```

---

### 🔒 Sanctumのセキュリティ

Sanctumは、以下のセキュリティ機能を提供します。

*   **トークンのハッシュ化**: データベースに保存されるトークンは、ハッシュ化されています。万が一データベースが漏洩しても、トークンを悪用されにくくなります。
*   **トークンの有効期限**: トークンに有効期限を設定できます（デフォルトは無期限）。
*   **トークンの権限管理**: トークンに「投稿の作成」「ユーザーの削除」などの権限を付与できます（Abilities）。

---

## 💡 TIP: SanctumとPassportの違い

Laravelには、もう一つの認証パッケージである**Laravel Passport**があります。Passportは、OAuth2プロトコルを完全にサポートしており、サードパーティアプリケーション（例：「Googleでログイン」）を実装する際に使います。

*   **Sanctum**: シンプルなトークンベース認証。自社アプリ向け。
*   **Passport**: OAuth2対応。サードパーティアプリ向け。

このカリキュラムでは、シンプルで使いやすいSanctumを使います。

---

## ✨ まとめ

このセクションでは、Laravel Sanctumの概念と、トークンベース認証の仕組みを学びました。

*   Laravel Sanctumは、トークンベース認証を簡単に実装するためのパッケージである。
*   トークンベース認証は、セッションベース認証と異なり、ドメインに依存せず、モバイルアプリでも使える。
*   Sanctumは、ユーザー登録・ログイン時にトークンを発行し、以降のリクエストでそのトークンを使ってユーザーを識別する。
*   トークンは、HTTPヘッダーの`Authorization: Bearer {トークン}`で送信する。

次のセクションでは、実際にSanctumを使って、ユーザー登録・ログイン・ログアウトのAPIを実装します。

---

## 📝 学習のポイント

- [ ] Laravel Sanctumが、トークンベース認証を実装するためのパッケージであることを理解した。
- [ ] トークンベース認証が、セッションベース認証と異なり、ドメインに依存しないことを理解した。
- [ ] Sanctumの動作フロー（登録→ログイン→トークン発行→認証APIアクセス→ログアウト）を理解した。
- [ ] トークンは、HTTPヘッダーの`Authorization: Bearer {トークン}`で送信することを理解した。
