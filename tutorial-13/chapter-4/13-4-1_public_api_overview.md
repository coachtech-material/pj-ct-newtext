# Tutorial 13-3-1: 公開APIの概要

## 🎯 このセクションで学ぶこと

- 公開APIの概念と用途を理解する
- Tutorial 11で学んだAPI知識を実践に活かす
- イシュー駆動開発のフローを継続する

---

## Step 0: 開発の準備（チケット駆動）

### 0-1. GitHubでIssueを確認

GitHubで `#6 公開API実装` のIssueを確認します。

### 0-2. ブランチを作成

```bash
git checkout main
git pull origin main
git switch -c feature/issue-6-public-api
```

---

## 公開APIとは

**公開API（Public API）**とは、**認証なしでアクセスできるAPI**のことです。

### 公開APIの用途

| 用途 | 例 |
|:---|:---|
| 外部サービスとの連携 | 他のアプリから書籍データを取得 |
| モバイルアプリ対応 | iOSやAndroidアプリからデータを取得 |
| データの公開 | 書籍レビューデータをオープンデータとして提供 |

### 今回実装するAPI

| エンドポイント | メソッド | 説明 |
|:---|:---|:---|
| `/api/books` | GET | 書籍一覧をJSON形式で取得 |
| `/api/books/{id}` | GET | 書籍詳細をJSON形式で取得 |

> 💡 **ポイント**: 認証なしでアクセスできるため、**読み取り専用**（GET）のみを提供します。書籍の登録・編集・削除は、認証が必要なWeb画面から行います。

---

## Tutorial 11との関連

Tutorial 11で学んだAPI開発の知識を活かします。

| Tutorial 11で学んだこと | 今回の実践 |
|:---|:---|
| APIルーティング（`routes/api.php`） | 書籍APIのルートを定義 |
| JSONレスポンス | 書籍データをJSON形式で返す |
| APIリソース | BookResourceで出力形式を整える |
| Thunder Clientでのテスト | APIの動作確認 |

---

## ✨ まとめ

このセクションでは、公開APIの概要について学びました。

- 公開APIは認証なしでアクセスできるAPI
- 読み取り専用（GET）のみを提供
- Tutorial 11で学んだ知識を実践に活かす

次のセクションでは、APIコントローラーを実装します。

---
