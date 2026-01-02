# Tutorial 10-1-1: ブランチ戦略の基礎（Git FlowとGitHub Flow）

## 🎯 このセクションで学ぶこと

*   Git FlowとGitHub Flowの違いを理解する。
*   チーム開発におけるブランチ戦略の重要性を学ぶ。
*   自分のプロジェクトに適したブランチ戦略を選択できるようになる。

---

## 導入：なぜブランチ戦略が必要なのか？

個人開発では、`main`ブランチに直接コミットしても問題ありません。しかし、**チーム開発**では、複数人が同時に開発を進めるため、以下のような問題が発生します。

*   他の人の作業と競合する
*   未完成の機能が本番環境にデプロイされる
*   バグ修正と新機能開発が混在する

これらの問題を解決するために、**ブランチ戦略**が必要です。

---

## 詳細解説

### 🔍 ブランチ戦略とは？

**ブランチ戦略**とは、**チーム開発におけるブランチの使い方のルール**です。代表的なブランチ戦略には、以下の2つがあります。

*   **Git Flow**: 複雑なリリースサイクルに対応
*   **GitHub Flow**: シンプルで継続的デプロイに適している

---

### 🔧 Git Flow

#### 概要

Git Flowは、**複数のブランチを使い分ける戦略**です。以下のブランチを使います。

*   `main`: 本番環境にデプロイされるブランチ
*   `develop`: 開発の中心となるブランチ
*   `feature/*`: 新機能開発用のブランチ
*   `release/*`: リリース準備用のブランチ
*   `hotfix/*`: 緊急バグ修正用のブランチ

#### ブランチの流れ

```
main
  └─ hotfix/fix-bug
develop
  ├─ feature/add-login
  ├─ feature/add-profile
  └─ release/v1.0.0
```

#### 開発の流れ

1. `develop`ブランチから`feature/*`ブランチを作成
2. 機能開発が完了したら、`develop`にマージ
3. リリース準備ができたら、`release/*`ブランチを作成
4. テストが完了したら、`main`と`develop`にマージ
5. 本番環境で緊急バグが発生したら、`hotfix/*`ブランチを作成
6. 修正が完了したら、`main`と`develop`にマージ

#### メリット

*   複数のバージョンを並行して管理できる
*   リリースサイクルが明確
*   大規模プロジェクトに適している

#### デメリット

*   ブランチが多く、複雑
*   小規模プロジェクトには過剰

---

### 🔧 GitHub Flow

#### 概要

GitHub Flowは、**シンプルなブランチ戦略**です。以下のブランチを使います。

*   `main`: 本番環境にデプロイされるブランチ
*   `feature/*`: 新機能開発・バグ修正用のブランチ

#### ブランチの流れ

```
main
  ├─ feature/add-login
  ├─ feature/add-profile
  └─ feature/fix-bug
```

#### 開発の流れ

1. `main`ブランチから`feature/*`ブランチを作成
2. 機能開発・バグ修正が完了したら、プルリクエストを作成
3. コードレビューが完了したら、`main`にマージ
4. `main`にマージされたら、自動的に本番環境にデプロイ

#### メリット

*   シンプルで理解しやすい
*   継続的デプロイに適している
*   小規模〜中規模プロジェクトに適している

#### デメリット

*   複数のバージョンを並行して管理しにくい
*   リリースサイクルが不明確

---

### 🔍 Git FlowとGitHub Flowの比較

| 項目 | Git Flow | GitHub Flow |
|------|----------|-------------|
| ブランチ数 | 多い（5種類） | 少ない（2種類） |
| 複雑さ | 複雑 | シンプル |
| リリースサイクル | 明確 | 不明確 |
| デプロイ | 手動 | 自動（CI/CD） |
| 適用規模 | 大規模 | 小〜中規模 |

---

### 💡 TIP: どちらを選ぶべきか？

*   **Git Flow**: 複数のバージョンを並行して管理する必要がある場合（例：モバイルアプリ、パッケージソフトウェア）
*   **GitHub Flow**: 継続的デプロイを行う場合（例：Webアプリケーション、SaaS）

---

### 🚀 実践例1: GitHub Flowの流れ

#### ステップ1: `main`ブランチから`feature`ブランチを作成

```bash
git switch main
git pull origin main
git switch -c feature/add-login
```

#### ステップ2: 機能開発

```bash
# コードを書く
git add .
git commit -m "Add login feature"
git push origin feature/add-login
```

#### ステップ3: プルリクエストを作成

GitHubでプルリクエストを作成し、コードレビューを依頼します。

#### ステップ4: レビュー後、`main`にマージ

レビューが完了したら、`main`にマージします。

#### ステップ5: ブランチを削除

```bash
git switch main
git pull origin main
git branch -d feature/add-login
```

---

### 🚀 実践例2: Git Flowの流れ

#### ステップ1: `develop`ブランチから`feature`ブランチを作成

```bash
git switch develop
git pull origin develop
git switch -c feature/add-login
```

#### ステップ2: 機能開発

```bash
# コードを書く
git add .
git commit -m "Add login feature"
git push origin feature/add-login
```

#### ステップ3: `develop`にマージ

```bash
git switch develop
git merge feature/add-login
git push origin develop
git branch -d feature/add-login
```

#### ステップ4: リリース準備

```bash
git switch develop
git switch -c release/v1.0.0
# リリース準備（バージョン番号の更新など）
git add .
git commit -m "Prepare release v1.0.0"
```

#### ステップ5: `main`と`develop`にマージ

```bash
git switch main
git merge release/v1.0.0
git tag v1.0.0
git push origin main --tags

git switch develop
git merge release/v1.0.0
git push origin develop

git branch -d release/v1.0.0
```

---

### 💡 TIP: ブランチ名の命名規則

*   `feature/機能名`: 新機能開発
*   `bugfix/バグ名`: バグ修正
*   `hotfix/バグ名`: 緊急バグ修正
*   `release/バージョン`: リリース準備

**例**

*   `feature/add-login`
*   `bugfix/fix-validation-error`
*   `hotfix/fix-critical-bug`
*   `release/v1.0.0`

---

### 🚨 よくある間違い

#### 間違い1: `main`ブランチに直接コミット

```bash
# NG
git switch main
git add .
git commit -m "Add new feature"
git push origin main
```

**対処法**: 必ず`feature`ブランチを作成してから開発します。

---

#### 間違い2: ブランチ名が不明確

```bash
# NG
git switch -c test
git switch -c fix
git switch -c new
```

**対処法**: 命名規則に従って、わかりやすいブランチ名を付けます。

---

## ✨ まとめ

このセクションでは、ブランチ戦略の基礎を学びました。

*   Git Flowは、複数のブランチを使い分ける複雑な戦略。
*   GitHub Flowは、シンプルで継続的デプロイに適した戦略。
*   プロジェクトの規模やリリースサイクルに応じて、適切なブランチ戦略を選択する。

次のセクションでは、ブランチの作成と切り替えについて学びます。

---
