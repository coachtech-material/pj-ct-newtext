# Tutorial 12-1-1: ブランチ戦略の基礎（Git FlowとGitHub Flow）

## 🎯 このセクションで学ぶこと

- Git FlowとGitHub Flowの違いを理解する
- チーム開発におけるブランチ戦略の重要性を学ぶ
- 自分のプロジェクトに適したブランチ戦略を選択できるようになる

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜブランチ戦略を学ぶのか？」

個人開発では、`main`ブランチに直接コミットしても問題ありません。しかし、**チーム開発**では、複数人が同時に開発を進めるため、以下のような問題が発生します。

- 他の人の作業と競合する
- 未完成の機能が本番環境にデプロイされる
- バグ修正と新機能開発が混在する

これらの問題を解決するために、**ブランチ戦略**が必要です。

---

### 先輩エンジニアの視点

> 「ブランチ戦略は、チームの**交通ルール**のようなものです。ルールがないと、みんなが好き勝手に走って事故が起きます。ルールがあれば、安全に目的地に到着できます。」

**実務での経験**

私がチーム開発に参加したとき、最初はブランチ戦略がありませんでした。その結果：

- 誰かが`main`に直接プッシュして、本番環境が壊れた
- 同じファイルを複数人が編集して、マージ時に大量のコンフリクトが発生
- どのブランチが最新かわからなくなった

ブランチ戦略を導入してからは、これらの問題がほぼなくなりました。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | ブランチ戦略の基本を理解 | なぜ必要かを知る |
| Step 2 | Git Flowを学ぶ | 複雑なリリースサイクルに対応 |
| Step 3 | GitHub Flowを学ぶ | シンプルで継続的デプロイに適している |
| Step 4 | 実践例で流れを確認 | 実際のコマンドを学ぶ |

---

## 詳細解説

### 🔍 ブランチ戦略とは？

**ブランチ戦略**とは、**チーム開発におけるブランチの使い方のルール**です。代表的なブランチ戦略には、以下の2つがあります。

| 戦略 | 特徴 | 適したプロジェクト |
|------|------|-------------------|
| **Git Flow** | 複雑なリリースサイクルに対応 | モバイルアプリ、パッケージソフトウェア |
| **GitHub Flow** | シンプルで継続的デプロイに適している | Webアプリケーション、SaaS |

---

## 🔧 Git Flow

### 概要

Git Flowは、**複数のブランチを使い分ける戦略**です。2010年にVincent Driessenが提唱しました。

**Git Flowの考え方**

Git Flowは、「**本番環境は常に安定した状態を保つ**」という考え方に基づいています。そのため、開発中のコードと本番環境のコードを明確に分離します。

---

### Git Flowで使うブランチ

| ブランチ | 役割 | 寿命 |
|---------|------|------|
| `main` | 本番環境にデプロイされるブランチ | 永続的 |
| `develop` | 開発の中心となるブランチ | 永続的 |
| `feature/*` | 新機能開発用のブランチ | 一時的 |
| `release/*` | リリース準備用のブランチ | 一時的 |
| `hotfix/*` | 緊急バグ修正用のブランチ | 一時的 |

---

### Git Flowの全体像（図解）

```
時間の流れ →

main     ●─────────────────────●───────────●─────────────●
          │                     ↑           ↑             ↑
          │                     │           │             │
hotfix    │                     │           │    ●───────●
          │                     │           │    │ 緊急修正
          │                     │           │    ↓
develop  ●───●───●───●───●───●───●───●───●───●───●───●
              │   ↑   │   ↑       ↑   │   ↑
              │   │   │   │       │   │   │
feature       ●───●   ●───●       │   ●───●
              機能A   機能B       │   機能C
                                  │
release                          ●───●
                                 v1.0.0
```

**図の読み方**

- `●` はコミットを表します
- `↑` はマージを表します
- 横軸は時間の流れです
- `feature`ブランチは`develop`から分岐し、`develop`にマージされます
- `release`ブランチは`develop`から分岐し、`main`と`develop`にマージされます
- `hotfix`ブランチは`main`から分岐し、`main`と`develop`にマージされます

---

### Git Flowの開発の流れ

**ステップ1: 機能開発**

```
develop ●───●───●
             │
feature      ●───●───●
             機能開発
```

1. `develop`ブランチから`feature/*`ブランチを作成
2. 機能開発を行う
3. 完了したら`develop`にマージ

**ステップ2: リリース準備**

```
develop ●───●───●───●───●
                     │   ↑
release              ●───●
                     v1.0.0
```

1. `develop`ブランチから`release/*`ブランチを作成
2. バージョン番号の更新、最終テストを行う
3. 完了したら`main`と`develop`にマージ

**ステップ3: 緊急バグ修正**

```
main    ●───────────●───●
                    │   ↑
hotfix              ●───●
                    緊急修正
```

1. `main`ブランチから`hotfix/*`ブランチを作成
2. バグ修正を行う
3. 完了したら`main`と`develop`にマージ

---

### Git Flowのメリット・デメリット

| メリット | デメリット |
|---------|-----------|
| 複数のバージョンを並行して管理できる | ブランチが多く、複雑 |
| リリースサイクルが明確 | 小規模プロジェクトには過剰 |
| 大規模プロジェクトに適している | 学習コストが高い |

---

## 🔧 GitHub Flow

### 概要

GitHub Flowは、**シンプルなブランチ戦略**です。GitHubが提唱しました。

**GitHub Flowの考え方**

GitHub Flowは、「**mainブランチは常にデプロイ可能な状態を保つ**」という考え方に基づいています。機能開発やバグ修正は、すべて`feature`ブランチで行い、プルリクエストを通じて`main`にマージします。

---

### GitHub Flowで使うブランチ

| ブランチ | 役割 | 寿命 |
|---------|------|------|
| `main` | 本番環境にデプロイされるブランチ | 永続的 |
| `feature/*` | 新機能開発・バグ修正用のブランチ | 一時的 |

Git Flowと比べて、ブランチの種類が少なく、シンプルです。

---

### GitHub Flowの全体像（図解）

```
時間の流れ →

main     ●───●───●───●───●───●───●───●───●
              ↑       ↑       ↑       ↑
              │       │       │       │
feature       ●───●   ●───●   ●───●   ●───●
              機能A   機能B   バグ修正  機能C
```

**図の読み方**

- すべての作業は`main`から分岐し、`main`にマージされます
- `feature`ブランチは、機能開発だけでなくバグ修正にも使います
- マージは**プルリクエスト**を通じて行います

---

### GitHub Flowの開発の流れ

```
1. mainから分岐      2. 開発           3. プルリクエスト   4. マージ
   
main    ●            ●                 ●                   ●───●
        │            │                 │                       ↑
feature ●            ●───●───●         ●───●───● → PR → レビュー → マージ
```

**詳細な流れ**

1. `main`ブランチから`feature/*`ブランチを作成
2. 機能開発・バグ修正を行う
3. GitHubでプルリクエストを作成
4. チームメンバーがコードレビューを行う
5. レビューが承認されたら、`main`にマージ
6. `main`にマージされたら、自動的に本番環境にデプロイ（CI/CD）

---

### GitHub Flowのメリット・デメリット

| メリット | デメリット |
|---------|-----------|
| シンプルで理解しやすい | 複数のバージョンを並行して管理しにくい |
| 継続的デプロイに適している | リリースサイクルが不明確 |
| 小規模〜中規模プロジェクトに適している | 大規模プロジェクトには不向き |

---

### 🔍 Git FlowとGitHub Flowの比較

| 項目 | Git Flow | GitHub Flow |
|------|----------|-------------|
| ブランチ数 | 多い（5種類） | 少ない（2種類） |
| 複雑さ | 複雑 | シンプル |
| リリースサイクル | 明確（バージョン管理） | 不明確（継続的デプロイ） |
| デプロイ | 手動（リリースブランチ経由） | 自動（CI/CD） |
| 適用規模 | 大規模 | 小〜中規模 |
| 学習コスト | 高い | 低い |

---

### 💡 TIP: どちらを選ぶべきか？

**Git Flowを選ぶ場合**

- 複数のバージョンを並行して管理する必要がある
- リリースサイクルが明確（例：月1回のリリース）
- 例：モバイルアプリ、パッケージソフトウェア、エンタープライズシステム

**GitHub Flowを選ぶ場合**

- 継続的デプロイを行う
- シンプルなワークフローが好ましい
- 例：Webアプリケーション、SaaS、スタートアップ

> 💡 **初心者へのアドバイス**: 最初は**GitHub Flow**から始めることをおすすめします。シンプルで理解しやすく、チーム開発の基本を学ぶのに適しています。

---

## 🚀 実践例1: GitHub Flowの流れ

### ステップ1: `main`ブランチから`feature`ブランチを作成

```bash
git switch main
git pull origin main
git switch -c feature/add-login
```

**コードリーディング**

| コマンド | 説明 |
|:---|:---|
| `git switch main` | `main`ブランチに切り替えます |
| `git pull origin main` | リモートの`main`ブランチの最新の変更を取得します |
| `git switch -c feature/add-login` | `feature/add-login`という新しいブランチを作成して切り替えます |

**構文解説: `git switch -c`**

```bash
git switch -c <ブランチ名>
```

| オプション | 説明 |
|:---|:---|
| `-c` | 新しいブランチを作成します（`--create`の省略形） |
| `<ブランチ名>` | 作成するブランチの名前 |

---

### ステップ2: 機能開発

```bash
# コードを書く
git add .
git commit -m "Add login feature"
git push origin feature/add-login
```

**コードリーディング**

| コマンド | 説明 |
|:---|:---|
| `git add .` | 変更したすべてのファイルをステージングエリアに追加します |
| `git commit -m "Add login feature"` | ステージングエリアの変更をコミットします |
| `git push origin feature/add-login` | ローカルのブランチをリモートにプッシュします |

**構文解説: `git push origin <ブランチ名>`**

```bash
git push origin <ブランチ名>
```

| 要素 | 説明 |
|:---|:---|
| `origin` | リモートリポジトリの名前（デフォルト） |
| `<ブランチ名>` | プッシュするブランチの名前 |

---

### ステップ3: プルリクエストを作成

GitHubでプルリクエストを作成し、コードレビューを依頼します。

**プルリクエストの作成手順**

1. GitHubのリポジトリページにアクセス
2. 「Pull requests」タブをクリック
3. 「New pull request」ボタンをクリック
4. `base: main` ← `compare: feature/add-login` を選択
5. タイトルと説明を入力
6. 「Create pull request」ボタンをクリック

---

### ステップ4: レビュー後、`main`にマージ

レビューが完了したら、GitHubの「Merge pull request」ボタンをクリックして`main`にマージします。

---

### ステップ5: ブランチを削除

```bash
git switch main
git pull origin main
git branch -d feature/add-login
```

**コードリーディング**

| コマンド | 説明 |
|:---|:---|
| `git switch main` | `main`ブランチに切り替えます |
| `git pull origin main` | マージされた最新の変更を取得します |
| `git branch -d feature/add-login` | ローカルの`feature/add-login`ブランチを削除します |

**構文解説: `git branch -d`**

```bash
git branch -d <ブランチ名>
```

| オプション | 説明 |
|:---|:---|
| `-d` | マージ済みのブランチを削除します（`--delete`の省略形） |
| `-D` | マージされていなくても強制的に削除します |

---

## 🚀 実践例2: Git Flowの流れ

### ステップ1: `develop`ブランチから`feature`ブランチを作成

```bash
git switch develop
git pull origin develop
git switch -c feature/add-login
```

**コードリーディング**

| コマンド | 説明 |
|:---|:---|
| `git switch develop` | `develop`ブランチに切り替えます |
| `git pull origin develop` | リモートの`develop`ブランチの最新の変更を取得します |
| `git switch -c feature/add-login` | `feature/add-login`という新しいブランチを作成して切り替えます |

> 💡 **ポイント**: Git Flowでは、`main`ではなく`develop`から`feature`ブランチを作成します。

---

### ステップ2: 機能開発

```bash
# コードを書く
git add .
git commit -m "Add login feature"
git push origin feature/add-login
```

---

### ステップ3: `develop`にマージ

```bash
git switch develop
git merge feature/add-login
git push origin develop
git branch -d feature/add-login
```

**コードリーディング**

| コマンド | 説明 |
|:---|:---|
| `git switch develop` | `develop`ブランチに切り替えます |
| `git merge feature/add-login` | `feature/add-login`ブランチを`develop`にマージします |
| `git push origin develop` | マージした`develop`ブランチをリモートにプッシュします |
| `git branch -d feature/add-login` | ローカルの`feature/add-login`ブランチを削除します |

**構文解説: `git merge`**

```bash
git merge <ブランチ名>
```

| 要素 | 説明 |
|:---|:---|
| `<ブランチ名>` | 現在のブランチにマージするブランチの名前 |

---

### ステップ4: リリース準備

```bash
git switch develop
git switch -c release/v1.0.0
# リリース準備（バージョン番号の更新など）
git add .
git commit -m "Prepare release v1.0.0"
```

**コードリーディング**

| コマンド | 説明 |
|:---|:---|
| `git switch develop` | `develop`ブランチに切り替えます |
| `git switch -c release/v1.0.0` | `release/v1.0.0`という新しいブランチを作成して切り替えます |
| `git add .` | 変更したファイルをステージングエリアに追加します |
| `git commit -m "Prepare release v1.0.0"` | リリース準備のコミットを作成します |

---

### ステップ5: `main`と`develop`にマージ

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

**コードリーディング**

| コマンド | 説明 |
|:---|:---|
| `git switch main` | `main`ブランチに切り替えます |
| `git merge release/v1.0.0` | `release/v1.0.0`ブランチを`main`にマージします |
| `git tag v1.0.0` | `v1.0.0`というタグを作成します |
| `git push origin main --tags` | `main`ブランチとタグをリモートにプッシュします |
| `git switch develop` | `develop`ブランチに切り替えます |
| `git merge release/v1.0.0` | `release/v1.0.0`ブランチを`develop`にもマージします |
| `git push origin develop` | `develop`ブランチをリモートにプッシュします |
| `git branch -d release/v1.0.0` | ローカルの`release/v1.0.0`ブランチを削除します |

**構文解説: `git tag`**

```bash
git tag <タグ名>
```

| 要素 | 説明 |
|:---|:---|
| `<タグ名>` | 作成するタグの名前（通常はバージョン番号） |

**構文解説: `git push --tags`**

```bash
git push origin <ブランチ名> --tags
```

| オプション | 説明 |
|:---|:---|
| `--tags` | ローカルのタグをリモートにプッシュします |

---

### 💡 TIP: ブランチ名の命名規則

| プレフィックス | 用途 | 例 |
|---------------|------|-----|
| `feature/` | 新機能開発 | `feature/add-login` |
| `bugfix/` | バグ修正 | `bugfix/fix-validation-error` |
| `hotfix/` | 緊急バグ修正 | `hotfix/fix-critical-bug` |
| `release/` | リリース準備 | `release/v1.0.0` |

**良いブランチ名の例**

```bash
feature/add-user-authentication
feature/implement-search-function
bugfix/fix-login-redirect
hotfix/fix-security-vulnerability
release/v2.1.0
```

**悪いブランチ名の例**

```bash
test        # 何のテストかわからない
fix         # 何を修正するのかわからない
new         # 何が新しいのかわからない
```

---

## 🚨 よくある間違い

### 間違い1: `main`ブランチに直接コミット

```bash
# NG
git switch main
git add .
git commit -m "Add new feature"
git push origin main
```

**なぜダメなのか？**

- コードレビューを経ずに本番環境に反映される
- 他のメンバーの作業と競合する可能性がある
- 問題が発生した場合、切り戻しが難しい

**対処法**: 必ず`feature`ブランチを作成してから開発します。

```bash
# OK
git switch main
git switch -c feature/add-new-feature
# 開発作業
git add .
git commit -m "Add new feature"
git push origin feature/add-new-feature
# プルリクエストを作成
```

---

### 間違い2: ブランチ名が不明確

```bash
# NG
git switch -c test
git switch -c fix
git switch -c new
```

**なぜダメなのか？**

- 何の作業をしているブランチかわからない
- チームメンバーが混乱する
- 後から見返したときに理解できない

**対処法**: 命名規則に従って、わかりやすいブランチ名を付けます。

```bash
# OK
git switch -c feature/add-user-profile
git switch -c bugfix/fix-login-error
git switch -c hotfix/fix-security-issue
```

---

### 間違い3: `git pull`を忘れる

```bash
# NG
git switch main
git switch -c feature/add-login  # 古いmainから分岐
```

**なぜダメなのか？**

- 古いコードをベースに開発してしまう
- マージ時にコンフリクトが発生しやすくなる

**対処法**: ブランチを作成する前に、必ず`git pull`で最新の状態を取得します。

```bash
# OK
git switch main
git pull origin main  # 最新の状態を取得
git switch -c feature/add-login
```

---

## ✨ まとめ

このセクションでは、ブランチ戦略の基礎を学びました。

| 項目 | Git Flow | GitHub Flow |
|------|----------|-------------|
| ブランチ数 | 5種類（main, develop, feature, release, hotfix） | 2種類（main, feature） |
| 複雑さ | 複雑 | シンプル |
| 適したプロジェクト | 大規模、明確なリリースサイクル | 小〜中規模、継続的デプロイ |

**重要なポイント**

- ブランチ戦略は、チーム開発の「交通ルール」
- Git Flowは複雑だが、大規模プロジェクトに適している
- GitHub Flowはシンプルで、継続的デプロイに適している
- 初心者はGitHub Flowから始めるのがおすすめ

次のセクションでは、ブランチの作成と切り替えについて詳しく学びます。

---
