# Tutorial 13-1-5: Git/GitHubの準備とIssue登録

## 🎯 このセクションで学ぶこと

- Gitリポジトリを初期化し、最初のコミットを作成する方法を学ぶ
- GitHubリポジトリを作成し、ローカルリポジトリと連携する方法を学ぶ
- **機能一覧をGitHub Issuesに登録し、イシュー駆動開発の準備をする**

---

## 導入：イシュー駆動開発とは

このチュートリアルでは、**イシュー駆動開発（Issue-Driven Development）**を実践します。

イシュー駆動開発とは、**GitHub Issuesに機能やタスクを登録し、Issue単位で開発を進める手法**です。実務では、チーム開発でこの手法がよく使われます。

**イシュー駆動開発の流れ**:

1. **Issue登録**: 機能一覧をGitHub Issuesに登録
2. **ブランチ作成**: Issue番号付きブランチを作成（例: `feature/issue-1-book-list`）
3. **実装**: 機能を実装してコミット
4. **プルリクエスト**: PRを作成し、セルフレビュー
5. **マージ**: PRをマージし、Issueを自動クローズ

> 💡 **ポイント**: このチュートリアルでは、**1人チーム開発ごっこ**として、この流れを繰り返し練習します。手癖になるまで繰り返すことが目的です。

---

## 詳細解説

## Step 1: Gitリポジトリの初期化

プロジェクトディレクトリで、Gitリポジトリを初期化します。

```bash
cd book-review-app
git init
```

**出力例**:

```
Initialized empty Git repository in /path/to/book-review-app/.git/
```

---

## Step 2: 最初のコミット

ファイルをステージングエリアに追加し、コミットを作成します。

```bash
git add .
git commit -m "Initial commit: Laravel 10 + Tailwind CSS setup"
```

---

## Step 3: GitHubリポジトリの作成

GitHubにログインし、新しいリポジトリを作成します。

1. GitHubの右上の「+」ボタンをクリック
2. 「New repository」を選択
3. リポジトリ名を入力: `book-review-app`
4. 「Public」または「Private」を選択
5. 「Create repository」をクリック

---

## Step 4: リモートリポジトリの追加とプッシュ

ローカルリポジトリとGitHubリポジトリを連携します。

```bash
git remote add origin https://github.com/your-username/book-review-app.git
git branch -M main
git push -u origin main
```

`your-username`は、GitHubのユーザー名に置き換えます。

---

## Step 5: GitHub Issuesに機能を登録

ここからが**イシュー駆動開発の準備**です。13-1-1で作成した機能一覧をGitHub Issuesに登録します。

### 5-1. Issuesタブを開く

GitHubでリポジトリを開き、「Issues」タブをクリックします。

### 5-2. 機能をIssueとして登録

以下の機能を1つずつIssueとして登録します。

| Issue # | タイトル | 説明 |
|:---:|:---|:---|
| #1 | 書籍一覧機能 | 登録された書籍の一覧を表示する |
| #2 | 書籍登録機能 | 新しい書籍を登録する |
| #3 | 書籍詳細機能 | 書籍の詳細情報を表示する |
| #4 | 書籍編集機能 | 書籍情報を編集する |
| #5 | 書籍削除機能 | 書籍を削除する |
| #6 | 公開API実装 | 認証なしで書籍データをJSONで取得できるAPIを実装 |
| #7 | ユーザー認証機能 | ユーザー登録・ログイン・ログアウト |
| #8 | ユーザー別レビュー管理 | ログインユーザーのレビューのみ表示・編集可能にする |

### 5-3. Issue登録の手順

1. 「New issue」をクリック
2. 「Title」に機能名を入力（例: `書籍一覧機能`）
3. 「Description」に説明を入力（例: `登録された書籍の一覧を表示する`）
4. 「Submit new issue」をクリック

これを8回繰り返し、すべての機能をIssueとして登録します。

---

## Step 6: これからの開発フロー

これ以降の学習は、**Issueを消化していく作業**になります。

各セクションで以下のフローを繰り返します。

```
1. GitHubで対応するIssueを確認
   ↓
2. mainブランチをpullして最新化
   $ git checkout main
   $ git pull origin main
   ↓
3. Issue番号付きブランチを作成
   $ git switch -c feature/issue-1-book-list
   ↓
4. 機能を実装
   ↓
5. コミットしてプッシュ
   $ git add .
   $ git commit -m "feat: 書籍一覧画面の実装 (Closes #1)"
   $ git push origin feature/issue-1-book-list
   ↓
6. GitHubでプルリクエストを作成
   ↓
7. セルフレビュー（Diff確認）
   ↓
8. マージしてIssueをクローズ
   ↓
9. ローカルのブランチ削除とmainの更新
   $ git checkout main
   $ git pull origin main
   $ git branch -d feature/issue-1-book-list
```

> 💡 **ポイント**: コミットメッセージに`Closes #1`を含めると、PRがマージされたときにIssue #1が自動的にクローズされます。

---

### 💡 TIP: コミットメッセージの書き方

コミットメッセージには、以下のプレフィックスを使うと分かりやすくなります。

| プレフィックス | 用途 |
|:---|:---|
| `feat:` | 新機能の追加 |
| `fix:` | バグ修正 |
| `docs:` | ドキュメントの変更 |
| `style:` | コードスタイルの変更（機能に影響なし） |
| `refactor:` | リファクタリング |
| `test:` | テストの追加・修正 |

**例**:

```
feat: 書籍一覧画面の実装 (Closes #1)
fix: 書籍削除時のエラーを修正 (Closes #5)
```

---

### 🚨 よくある間違い

#### 間違い1: mainブランチで直接開発してしまう

**対処法**: 必ずfeatureブランチを作成してから開発します。mainブランチは常にクリーンな状態を保ちます。

---

#### 間違い2: Issueを作らずに開発を始める

**対処法**: 開発を始める前に、必ずIssueを作成します。これにより、何を開発するかが明確になります。

---

#### 間違い3: コミットメッセージにIssue番号を書き忘れる

**対処法**: コミットメッセージに`Closes #番号`を含めることで、PRマージ時にIssueが自動クローズされます。

---

## ✨ まとめ

このセクションでは、Git/GitHubの準備とイシュー駆動開発の準備について学びました。

- Gitリポジトリを初期化し、GitHubにプッシュした
- 機能一覧をGitHub Issuesに登録した
- イシュー駆動開発の流れを理解した

次のセクションでは、提供アセットの配置について学びます。

---
