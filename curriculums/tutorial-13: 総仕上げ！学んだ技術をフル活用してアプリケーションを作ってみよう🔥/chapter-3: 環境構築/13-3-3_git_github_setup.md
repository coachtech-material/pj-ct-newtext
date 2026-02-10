# Tutorial 13-3-3: Git/GitHub準備とIssue登録

## 🎯 このセクションで学ぶこと

- GitHubリポジトリの作成とローカルリポジトリの初期化を行う
- GitHub Issueを使ったタスク管理の方法を学ぶ
- 実務で使われるIssue駆動開発の流れを理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ開発前にIssueを登録するのか？」

開発を始める前に、**やるべきことをIssueとして登録**しておくことで、以下のメリットがあります。

### メリット1: 「何をやるか」が明確になる

```
❌ Issueなしで開発
→ 「次は何をすればいいんだっけ？」と迷う
→ 作業の抜け漏れが発生しやすい

✅ 先にIssueを登録
→ 「このIssueを消化すればいい」と明確
→ 作業の進捗が可視化される
```

### メリット2: コミットとIssueが紐づく

GitHubでは、コミットメッセージに`#1`のようにIssue番号を書くと、自動的に紐づきます。

```bash
git commit -m "タスクCRUD実装 #3"
```

### メリット3: チーム開発での情報共有

Issueを見れば、誰が何をやっているかがわかります。

---

## Step 1: GitHubリポジトリの作成

### 1-1. GitHubでリポジトリを作成する

1. GitHubにログインする
2. 右上の「+」ボタンから「New repository」を選択する
3. 以下の情報を入力する

| 項目 | 値 |
|:---|:---|
| Repository name | `task-manager` |
| Description | タスク管理アプリ |
| Public / Private | Private（推奨） |
| Initialize with README | チェックしない |

4. 「Create repository」ボタンをクリックする

---

### 1-2. ローカルリポジトリを初期化する

プロジェクトのルートディレクトリで以下のコマンドを実行します。

```bash
# Gitリポジトリを初期化
git init

# 全ファイルをステージング
git add .

# 初回コミット
git commit -m "Initial commit"

# mainブランチに名前を変更（必要な場合）
git branch -M main

# リモートリポジトリを追加
git remote add origin https://github.com/あなたのユーザー名/task-manager.git

# プッシュ
git push -u origin main
```

### コマンドのコードリーディング

| コマンド | 説明 |
|:---|:---|
| `git init` | 現在のディレクトリをGitリポジトリとして初期化 |
| `git add .` | 全ファイルをステージングエリアに追加 |
| `git commit -m "..."` | ステージングされたファイルをコミット |
| `git branch -M main` | 現在のブランチ名を`main`に変更 |
| `git remote add origin ...` | リモートリポジトリを`origin`という名前で追加 |
| `git push -u origin main` | `main`ブランチをリモートにプッシュ（`-u`で追跡設定） |

---

## Step 2: GitHub Issueの登録

### 2-1. Issueとは？

**Issue**は、GitHubで「やるべきこと」を管理する機能です。

| 用途 | 例 |
|:---|:---|
| 機能追加 | 「タスクCRUD機能を実装する」 |
| バグ修正 | 「ログイン後にリダイレクトされない」 |
| 改善 | 「パフォーマンスを改善する」 |

---

### 2-2. このTutorialで登録するIssue一覧

以下のIssueを登録します。各Issueは、後のChapterで消化していきます。

| # | タイトル | 消化するChapter |
|:---:|:---|:---|
| 1 | マイグレーション作成（users/tasks/categories） | Chapter 4 |
| 2 | モデル作成とリレーション定義 | Chapter 4 |
| 3 | 認証機能の実装（Fortify） | Chapter 5 |
| 4 | カテゴリーCRUD実装 | Chapter 6 |
| 5 | タスクCRUD実装 | Chapter 6 |
| 6 | タスクPolicy実装 | Chapter 6 |
| 7 | 公開API実装 | Chapter 7 |
| 8 | CRUDテスト実装 | Chapter 8 |
| 9 | 認証テスト実装 | Chapter 8 |
| 10 | APIテスト実装 | Chapter 8 |

---

### 2-3. Issueを登録する

GitHubのリポジトリページで、以下の手順でIssueを登録します。

1. 「Issues」タブをクリックする
2. 「New issue」ボタンをクリックする
3. タイトルと説明を入力する
4. 「Submit new issue」ボタンをクリックする

---

### Issue #1: マイグレーション作成（users/tasks/categories）

**タイトル**: マイグレーション作成（users/tasks/categories）

**説明**:
```markdown
## 概要
データベースのテーブルを作成するマイグレーションファイルを作成する。

## 作成するテーブル
- users（既存のマイグレーションを確認）
- categories
- tasks

## 完了条件
- [ ] categoriesテーブルのマイグレーションが作成されている
- [ ] tasksテーブルのマイグレーションが作成されている
- [ ] `sail artisan migrate`が正常に実行できる
```

---

### Issue #2: モデル作成とリレーション定義

**タイトル**: モデル作成とリレーション定義

**説明**:
```markdown
## 概要
Eloquentモデルを作成し、リレーションを定義する。

## 作成するモデル
- Category
- Task

## リレーション
- User hasMany Task
- Task belongsTo User
- Category hasMany Task
- Task belongsTo Category

## 完了条件
- [ ] Categoryモデルが作成されている
- [ ] Taskモデルが作成されている
- [ ] リレーションが正しく定義されている
- [ ] Tinkerでリレーションが動作することを確認
```

---

### Issue #3: 認証機能の実装（Fortify）

**タイトル**: 認証機能の実装（Fortify）

**説明**:
```markdown
## 概要
Laravel Fortifyを使用して認証機能を実装する。

## 実装する機能
- ユーザー登録
- ログイン
- ログアウト

## 完了条件
- [ ] Fortifyがインストールされている
- [ ] 登録画面からユーザー登録ができる
- [ ] ログイン画面からログインできる
- [ ] ログアウトができる
```

---

### Issue #4: カテゴリーCRUD実装

**タイトル**: カテゴリーCRUD実装

**説明**:
```markdown
## 概要
カテゴリーのCRUD機能を実装する。

## 実装する機能
- カテゴリー一覧表示
- カテゴリー登録
- カテゴリー編集
- カテゴリー削除

## 完了条件
- [ ] CategoryControllerが作成されている
- [ ] ルーティングが設定されている
- [ ] 一覧・登録・編集・削除が動作する
```

---

### Issue #5: タスクCRUD実装

**タイトル**: タスクCRUD実装

**説明**:
```markdown
## 概要
タスクのCRUD機能を実装する。

## 実装する機能
- タスク一覧表示（ログインユーザーのタスクのみ）
- タスク詳細表示
- タスク登録
- タスク編集
- タスク削除

## 完了条件
- [ ] TaskControllerが作成されている
- [ ] ルーティングが設定されている
- [ ] 一覧・詳細・登録・編集・削除が動作する
```

---

### Issue #6: タスクPolicy実装

**タイトル**: タスクPolicy実装

**説明**:
```markdown
## 概要
タスクの認可（所有者チェック）をPolicyで実装する。

## 実装する内容
- TaskPolicyの作成
- 所有者のみが編集・削除できるようにする

## 完了条件
- [ ] TaskPolicyが作成されている
- [ ] 自分のタスクのみ編集・削除できる
- [ ] 他人のタスクにアクセスすると403エラーになる
```

---

### Issue #7: 公開API実装

**タイトル**: 公開API実装

**説明**:
```markdown
## 概要
タスク情報を取得する公開APIを実装する。

## 実装するエンドポイント
- GET /api/tasks - タスク一覧取得
- GET /api/tasks/{id} - タスク詳細取得

## 完了条件
- [ ] Api\TaskControllerが作成されている
- [ ] APIルーティングが設定されている
- [ ] JSON形式でレスポンスが返る
```

---

### Issue #8: CRUDテスト実装

**タイトル**: CRUDテスト実装

**説明**:
```markdown
## 概要
カテゴリー・タスクCRUD機能のFeatureテストを実装する。

## 実装するテスト
- カテゴリー一覧・登録・編集・削除テスト
- タスク一覧・登録・編集・削除テスト
- 認可テスト（他人のタスクにアクセスできないこと）

## 完了条件
- [ ] CategoryControllerTestが作成されている
- [ ] TaskControllerTestが作成されている
- [ ] 全てのテストがパスする
```

---

### Issue #9: 認証テスト実装

**タイトル**: 認証テスト実装

**説明**:
```markdown
## 概要
認証機能のFeatureテストを実装する。

## 実装するテスト
- ログインテスト
- ユーザー登録テスト
- 未認証時のリダイレクトテスト

## 完了条件
- [ ] AuthenticationTestが作成されている
- [ ] 全てのテストがパスする
```

---

### Issue #10: APIテスト実装

**タイトル**: APIテスト実装

**説明**:
```markdown
## 概要
公開APIのFeatureテストを実装する。

## 実装するテスト
- タスク一覧API（GET /api/tasks）テスト
- タスク詳細API（GET /api/tasks/{id}）テスト

## 完了条件
- [ ] ApiTaskControllerTestが作成されている
- [ ] 全てのテストがパスする
```

---

## Step 3: Issueの活用方法

### 3-1. 開発時のワークフロー

Issueを活用した開発の流れは以下のようになります。

```
1. Issueを確認する
   ↓
2. 作業用ブランチを作成する
   git switch -c feature/issue-1-migrations
   ↓
3. 実装する
   ↓
4. コミットする（Issue番号を含める）
   git commit -m "マイグレーション作成 #1"
   ↓
5. プッシュする
   git push origin feature/issue-1-migrations
   ↓
6. GitHubでプルリクエスト(PR)を作成する
   - PRの説明欄に `close #1` を記載
   ↓
7. PRをマージする
   → Issueが自動でクローズされる
```

> **💡 ポイント**: コミットメッセージでは `#1` のみ（Issueとの紐付け）、PRの説明欄で `close #1`（Issueの自動クローズ）という使い分けをします。

---

### 3-2. プルリクエスト(PR)の作成方法

プルリクエストは、ブランチの変更をmainブランチに取り込むためのリクエストです。

**GitHubでの手順**:

1. GitHubのリポジトリページを開く
2. 「Pull requests」タブをクリックする
3. 「New pull request」ボタンをクリックする
4. `base: main` ← `compare: feature/issue-1-migrations` を選択する
5. 「Create pull request」ボタンをクリックする
6. タイトルと説明を入力する
   - **タイトル例**: `feat: マイグレーション作成（users/tasks/categories）`
   - **説明欄**: `close #1` を記載（これでマージ時にIssueが自動クローズされる）
7. 「Create pull request」ボタンをクリックする

---

### 3-3. PRのマージ方法

PRを作成したら、以下の手順でマージします。

1. PRのページで「Merge pull request」ボタンをクリックする
2. 「Confirm merge」ボタンをクリックする
3. マージが完了すると、PRの説明欄に `close #1` があればIssue #1が自動的にクローズされる

> **💡 チーム開発では**: PRを作成した後、他のメンバーにコードレビューを依頼し、承認を得てからマージするのが一般的です。

---

### 3-4. コミットメッセージとIssueの紐付け

コミットメッセージにIssue番号を含めると、GitHubが自動的に紐付けます。

```bash
# Issue #1 に紐付くコミット（Issueはクローズされない）
git commit -m "categoriesテーブルのマイグレーション作成 #1"
```

### PRでIssueを自動クローズするキーワード

PRの説明欄に以下のキーワードを含めると、マージ時にIssueが自動クローズされます。

| キーワード | 効果 |
|:---|:---|
| `close #1` | Issue #1 をクローズ |
| `closes #1` | Issue #1 をクローズ |
| `fix #1` | Issue #1 をクローズ |
| `fixes #1` | Issue #1 をクローズ |
| `resolve #1` | Issue #1 をクローズ |
| `resolves #1` | Issue #1 をクローズ |

---

## 🚨 よくある間違い

### 間違い1: Issueを登録せずに開発を始める

**問題**: 作業の進捗が把握できず、抜け漏れが発生しやすい。

**対処法**: 開発前にIssueを登録し、1つずつ消化していく習慣をつけましょう。

---

### 間違い2: コミットメッセージにIssue番号を書かない

**問題**: コミットとIssueが紐付かず、後から追跡しにくい。

**対処法**: コミットメッセージには必ずIssue番号を含めましょう。

```bash
# NG
git commit -m "マイグレーション作成"

# OK
git commit -m "マイグレーション作成 #1"
```

---

### 間違い3: 1つのIssueに複数の作業を詰め込む

**問題**: Issueが大きすぎると、進捗が見えにくくなる。

**対処法**: 1つのIssueは1つの作業単位にしましょう。

```
❌ 「認証とCRUDを実装する」（大きすぎる）
✅ 「認証機能を実装する」「タスクCRUDを実装する」（適切な粒度）
```

---

### 間違い4: PRを作成せずに直接mainにマージする

**問題**: コードレビューの機会が失われ、品質管理が難しくなる。

**対処法**: 必ずPRを作成し、変更内容を明確にしてからマージしましょう。

```
❌ ローカルでmainにマージしてプッシュ
✅ PRを作成 → レビュー → マージ
```

---

## ✨ まとめ

このセクションでは、Git/GitHub準備とIssue登録について学びました。

- GitHubリポジトリを作成し、ローカルリポジトリを初期化した
- GitHub Issueを使ったタスク管理の方法を学んだ
- Issue駆動開発とPRベースの開発フローを理解した

次のChapterでは、マイグレーションとモデルの作成について学びます。

---
