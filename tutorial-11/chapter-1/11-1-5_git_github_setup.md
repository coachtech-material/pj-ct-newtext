# Tutorial 11-1-5: Git/GitHubの準備

## 🎯 このセクションで学ぶこと

*   Gitリポジトリを初期化し、最初のコミットを作成する方法を学ぶ。
*   GitHubリポジトリを作成し、ローカルリポジトリと連携する方法を学ぶ。
*   .gitignoreファイルを設定し、不要なファイルをコミットしないようにする。

---

## 導入：なぜGit/GitHubが必要なのか

**Git**とは、**バージョン管理システム**です。**GitHub**とは、**Gitリポジトリをホスティングするサービス**です。

Git/GitHubを使うことで、以下のようなメリットがあります。

*   **変更履歴の管理**: コードの変更履歴を記録し、いつでも過去の状態に戻せる
*   **チーム開発**: 複数人で同じプロジェクトを開発できる
*   **バックアップ**: コードをクラウドに保存し、ローカルのデータが失われても復元できる

---

## 詳細解説

## Step 1: Gitのインストール確認

Gitがインストールされているか確認します。

```bash
git --version
```

**出力例**:

```
git version 2.39.0
```

Gitがインストールされていない場合は、[Git公式サイト](https://git-scm.com/)からダウンロードしてインストールします。

---

## Step 2: Gitの初期設定

Gitの初期設定を行います。

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

設定を確認します。

```bash
git config --global user.name
git config --global user.email
```

---

## Step 3: Gitリポジトリの初期化

プロジェクトディレクトリで、Gitリポジトリを初期化します。

```bash
cd task-manager
git init
```

**出力例**:

```
Initialized empty Git repository in /path/to/task-manager/.git/
```

---

## Step 4: .gitignoreファイルの確認

Laravelプロジェクトには、デフォルトで`.gitignore`ファイルが含まれています。

**ファイル**: `.gitignore`

```gitignore
/.phpunit.cache
/node_modules
/public/build
/public/hot
/public/storage
/storage/*.key
/vendor
.env
.env.backup
.env.production
.phpunit.result.cache
Homestead.json
Homestead.yaml
auth.json
npm-debug.log
yarn-error.log
/.fleet
/.idea
/.vscode
```

`.gitignore`ファイルは、**Gitで管理しないファイルを指定するファイル**です。

重要なファイル（`.env`、`vendor`、`node_modules`など）は、Gitで管理しないようにします。

---

## Step 5: 最初のコミット

ファイルをステージングエリアに追加します。

```bash
git add .
```

コミットを作成します。

```bash
git commit -m "Initial commit"
```

**出力例**:

```
[main (root-commit) abc1234] Initial commit
 100 files changed, 10000 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 README.md
 ...
```

---

## Step 6: GitHubリポジトリの作成

GitHubにログインし、新しいリポジトリを作成します。

1. GitHubの右上の「+」ボタンをクリック
2. 「New repository」を選択
3. リポジトリ名を入力（例: `task-manager`）
4. 「Public」または「Private」を選択
5. 「Create repository」をクリック

---

## Step 7: リモートリポジトリの追加

ローカルリポジトリとGitHubリポジトリを連携します。

```bash
git remote add origin https://github.com/your-username/task-manager.git
```

`your-username`は、GitHubのユーザー名に置き換えます。

---

## Step 8: リモートリポジトリへのプッシュ

ローカルリポジトリの変更を、GitHubリポジトリにプッシュします。

```bash
git branch -M main
git push -u origin main
```

**出力例**:

```
Enumerating objects: 100, done.
Counting objects: 100% (100/100), done.
Delta compression using up to 8 threads
Compressing objects: 100% (80/80), done.
Writing objects: 100% (100/100), 50.00 KiB | 5.00 MiB/s, done.
Total 100 (delta 10), reused 0 (delta 0), pack-reused 0
To https://github.com/your-username/task-manager.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

---

## Step 9: GitHubでリポジトリを確認

GitHubでリポジトリを開き、ファイルがプッシュされていることを確認します。

---

## Step 10: ブランチの作成

新しい機能を開発するときは、ブランチを作成します。

```bash
git checkout -b feature/task-crud
```

**出力例**:

```
Switched to a new branch 'feature/task-crud'
```

---

## Step 11: 変更のコミット

ファイルを編集したら、変更をコミットします。

```bash
git add .
git commit -m "Add task CRUD functionality"
```

---

## Step 12: ブランチのプッシュ

ブランチをGitHubにプッシュします。

```bash
git push origin feature/task-crud
```

---

## Step 13: プルリクエストの作成

GitHubでプルリクエストを作成します。

1. GitHubでリポジトリを開く
2. 「Pull requests」タブをクリック
3. 「New pull request」をクリック
4. `feature/task-crud`ブランチを選択
5. 「Create pull request」をクリック

---

## Step 14: プルリクエストのマージ

プルリクエストをレビューし、問題がなければマージします。

1. プルリクエストを開く
2. 「Merge pull request」をクリック
3. 「Confirm merge」をクリック

---

## Step 15: mainブランチの更新

ローカルの`main`ブランチを更新します。

```bash
git checkout main
git pull origin main
```

---

### 💡 TIP: Gitコマンド一覧

よく使うGitコマンドをまとめます。

| コマンド | 説明 |
|---|---|
| `git status` | 変更されたファイルを確認 |
| `git add .` | すべてのファイルをステージング |
| `git commit -m "message"` | コミットを作成 |
| `git push origin branch` | ブランチをプッシュ |
| `git pull origin branch` | ブランチをプル |
| `git checkout -b branch` | 新しいブランチを作成して切り替え |
| `git branch` | ブランチ一覧を表示 |
| `git log` | コミット履歴を表示 |

---

### 🚨 よくある間違い

#### 間違い1: .envファイルをコミットしてしまう

**対処法**: `.gitignore`に`.env`が含まれていることを確認します。

もし誤ってコミットしてしまった場合は、以下のコマンドで削除します。

```bash
git rm --cached .env
git commit -m "Remove .env from repository"
git push origin main
```

---

#### 間違い2: vendorディレクトリをコミットしてしまう

**対処法**: `.gitignore`に`/vendor`が含まれていることを確認します。

---

#### 間違い3: コミットメッセージが不明確

**対処法**: コミットメッセージは、何を変更したかが分かるように書きます。

**良い例**:

```
Add task CRUD functionality
Fix bug in task deletion
Update README with installation instructions
```

**悪い例**:

```
update
fix
test
```

---

## ✨ まとめ

このセクションでは、Git/GitHubの準備について学びました。

*   Gitリポジトリを初期化し、最初のコミットを作成した。
*   GitHubリポジトリを作成し、ローカルリポジトリと連携した。
*   ブランチを作成し、プルリクエストを作成した。

次のChapterでは、CRUD機能の実装について学びます。

---

## 📝 学習のポイント

- [ ] Gitリポジトリを初期化した。
- [ ] GitHubリポジトリを作成した。
- [ ] ブランチを作成し、プルリクエストを作成した。
- [ ] .gitignoreファイルを設定した。
