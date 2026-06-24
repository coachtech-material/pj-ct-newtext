# 12-2-4: ハンズオン - GitHub連携演習

## 📌 このハンズオンについて

Chapter 2で学んだGitHub連携を実際に手を動かして確認します。Issue、Pull Request のワークフローを実践しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

> ⚠️ **重要**: このハンズオンで作成するリポジトリとPull Requestは、**12-3-5（コードレビューハンズオン）** でも使用します。マージせずにそのまま残しておいてください。

### 📁 ディレクトリ構成

このハンズオンでは、「自分で作成する用」と「解答を確認する用」の2つのリポジトリを作成します。

```
~/git-practice/
├── 12-2-4_hands-on/                         ← このハンズオン用のディレクトリ
│   ├── github-collab-practice/              ← 要件を見て自分で作成するリポジトリ
│   │   └── UserController.php
│   └── github-collab-sample/                ← 実践で一緒に作成するリポジトリ
│       └── UserController.php
└── ...
```

| ディレクトリ | 用途 |
|:---|:---|
| `github-collab-practice/` | 📋 要件を見て、自分の力で作成する |
| `github-collab-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したリポジトリと、解答を見ながら作成したリポジトリを比較することで、理解が深まります。

> ⚠️ **注意**: このハンズオンではGitHubリポジトリを作成します。それぞれ別のGitHubリポジトリとして作成してください。

---

## 🎯 演習課題：Pull Requestを作成しよう

### この演習で作るもの

Issueを作成し、ブランチで開発し、Pull Requestを作成する「GitHubコラボレーションワークフロー」を実践します。

### 🖼️ 完成イメージ

<details>
<summary>📸 完成画面を確認する（クリックで展開）</summary>

**GitHub Issue**

<img alt="12-2-4_1.png" src="https://s3.ap-northeast-1.amazonaws.com/coachtech-lms-bucket-dev/curriculums/images/12-2-4_1.png">

**GitHub Pull Request**

<img alt="12-2-4_2.png" src="https://s3.ap-northeast-1.amazonaws.com/coachtech-lms-bucket-dev/curriculums/images/12-2-4_2.png">

</details>

### 📋 ユースケース

あなたはチーム開発に参加しています。「ユーザー登録機能の追加」という機能を担当することになりました。

- タスクをIssueとして登録し、チームで共有したい
- Issue番号をブランチ名やコミットに含めて、作業を紐づけたい
- 開発が完了したらPull Requestを作成し、レビューを依頼したい

このワークフローを実践してみましょう。

> 💡 **ポイント**: 今回作成するコードには意図的に「改善すべき点」が含まれています。これは次の12-3-5（コードレビューハンズオン）でレビューの練習に使うためです。

### ✅ 完成チェックリスト

- [ ] Issueが作成されている
- [ ] Issue番号を含むブランチが作成されている
- [ ] `UserController.php`がコミットされている
- [ ] Pull Requestが作成されている
- [ ] PRの説明に`Closes #1`が含まれている

> 💡 **動作確認**: GitHubリポジトリの「Issues」タブと「Pull requests」タブを確認

### ✏️ 実装タスク

1. GitHubでIssueを作成する
2. `feature/issue-1-add-user-registration`ブランチを作成する
3. `UserController.php`を作成・コミット・プッシュする
4. Pull Requestを作成する

**作成するファイル**

`UserController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class UserController extends Controller
{
    public function index()
    {
        $users = User::all();
        return view('users.index', ['users' => $users]);
    }

    public function store(Request $request)
    {
        $user = new User;
        $user->name = $request->name;
        $user->email = $request->email;
        $user->password = $request->password;
        $user->save();

        return redirect('/users');
    }
}
```

> ⚠️ **注意**: このコードには意図的に問題点が含まれています。12-3-5でレビューの練習をするため、そのままコミットしてください。

---

## ⚙️ 環境準備（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のリポジトリを準備します。

### Step 1: ローカルリポジトリを作成

```bash
# git-practiceディレクトリに移動（なければ作成）
mkdir -p ~/git-practice
cd ~/git-practice

# ハンズオン用ディレクトリを作成
mkdir -p 12-2-4_hands-on
cd 12-2-4_hands-on

# 自分で作成する用のリポジトリを作成
mkdir github-collab-practice
cd github-collab-practice

# Gitリポジトリを初期化
git init
git branch -M main

# 初期ファイルを作成してコミット
echo "# GitHub Collaboration Practice" > README.md
git add README.md
git commit -m "Initial commit"
```

### Step 2: GitHubリポジトリを作成

1. GitHubにログイン
2. 右上の「+」ボタン → 「New repository」をクリック
3. リポジトリ名: `github-collab-practice`
4. 「Create repository」をクリック

### Step 3: リモートリポジトリを追加してプッシュ

```bash
# リモートリポジトリを追加（URLは自分のものに置き換え）
git remote add origin git@github.com:あなたのユーザー名/github-collab-practice.git

# プッシュ
git push -u origin main
```

**✅ ディレクトリ構造の確認**

```
~/git-practice/
└── 12-2-4_hands-on/
    └── github-collab-practice/     ← 自分で作成する用（今ここ）
        ├── .git/
        └── README.md
```

> 💡 **環境構築が完了！**
>
> GitHubでリポジトリが作成され、README.mdがプッシュされていることを確認してください。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

```bash
# Issueに対応するブランチ作成
git switch -c feature/issue-1-add-user-registration

# 実装後
git add UserController.php
git commit -m "Add #1: Add user registration feature"
git push origin feature/issue-1-add-user-registration
```

---

## 🏃 実践セクション：一緒に作ってみましょう！

ちゃんとできましたか？GitHubコラボレーションはチーム開発の基本です。一緒に手を動かしながら、IssueからPull Requestまでのワークフローを実践していきましょう。

> 📌 **注意**: ここからは`github-collab-sample/`ディレクトリで作業します。自分で作成したリポジトリと比較できるように、別のリポジトリで進めましょう。

---

### ⚙️ 環境準備（実践用プロジェクト）

### Step 1: ローカルリポジトリを作成

```bash
# ハンズオンディレクトリに移動
cd ~/git-practice/12-2-4_hands-on

# 実践用のリポジトリを作成
mkdir github-collab-sample
cd github-collab-sample

# Gitリポジトリを初期化
git init
git branch -M main

# 初期ファイルを作成してコミット
echo "# GitHub Collaboration Sample" > README.md
git add README.md
git commit -m "Initial commit"
```

### Step 2: GitHubリポジトリを作成

1. GitHubにログイン
2. 右上の「+」ボタン → 「New repository」をクリック
3. リポジトリ名: `github-collab-sample`
4. 「Create repository」をクリック

### Step 3: リモートリポジトリを追加してプッシュ

```bash
# リモートリポジトリを追加（URLは自分のものに置き換え）
git remote add origin git@github.com:あなたのユーザー名/github-collab-sample.git

# プッシュ
git push -u origin main
```

**✅ ディレクトリ構造の確認**

```
~/git-practice/
└── 12-2-4_hands-on/
    ├── github-collab-practice/     ← 自分で作成した用
    └── github-collab-sample/       ← 実践用（今ここ）
        ├── .git/
        └── README.md
```

---

### 🧠 先輩エンジニアの思考プロセス

先輩エンジニアは要件を以下のように構造化し、実装タスクに落とし込みます：

| Step | やること | 説明 |
|:-----|:---------|:-----|
| 1 | GitHubでIssueを作成する | タスクを明確にしてチームで共有 |
| 2 | `feature/issue-1-add-user-registration`ブランチを作成する | Issue番号を含めて紐づけ |
| 3 | `UserController.php`を作成・コミット・プッシュする | Issueの要件に従って実装 |
| 4 | Pull Requestを作成する | レビューを依頼 |

---

### 📝 ステップバイステップで実装

#### ステップ1: GitHubでIssueを作成する

**何を考えているか**：
- 「タスクを管理するためにIssueを作成しよう」
- 「要件を明確に記載して、チームで共有しよう」

GitHubでリポジトリを開き、「Issues」タブ → 「New issue」をクリックします。

**タイトル**: ユーザー登録機能の追加

**本文**:

```
## 概要
ユーザー登録機能を追加する

## 要件
- [ ] UserController.phpを作成
- [ ] ユーザー一覧表示機能（index）
- [ ] ユーザー登録機能（store）
```

「Submit new issue」をクリックしてIssueを作成します。

**コードリーディング**

| 部分 | 説明 |
|------|------|
| `## 概要` | Markdownの見出し記法 |
| `- [ ]` | チェックボックス（タスクリスト） |

---

#### ステップ2: `feature/issue-1-add-user-registration`ブランチを作成する

**何を考えているか**：
- 「Issue番号をブランチ名に含めよう」
- 「どのIssueに対応しているかがわかりやすくなる」

ターミナルで以下のコマンドを実行します：

```bash
git switch -c feature/issue-1-add-user-registration
```

**コードリーディング**

| 部分 | 説明 |
|------|------|
| `git switch -c` | 新しいブランチを作成し、同時に切り替える |
| `feature/issue-1-...` | Issue #1に対応するブランチであることがわかる命名 |

---

#### ステップ3: `UserController.php`を作成・コミット・プッシュする

**何を考えているか**：
- 「Issueの要件に従って機能を実装しよう」
- 「コミットメッセージにIssue番号を含めよう」

`UserController.php`を作成します：

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class UserController extends Controller
{
    public function index()
    {
        $users = User::all();
        return view('users.index', ['users' => $users]);
    }

    public function store(Request $request)
    {
        $user = new User;
        $user->name = $request->name;
        $user->email = $request->email;
        $user->password = $request->password;
        $user->save();

        return redirect('/users');
    }
}
```

> ⚠️ **注意**: このコードには意図的に問題点が含まれています。12-3-5でレビューの練習をするため、そのままコミットしてください。

ターミナルで以下のコマンドを実行します：

```bash
git add UserController.php
git commit -m "Add #1: Add user registration feature"
git push origin feature/issue-1-add-user-registration
```

**コードリーディング**

| コマンド | 説明 |
|----------|------|
| `git commit -m "Add #1: ..."` | Issue #1に紐づくコミット |
| `git push origin ...` | featureブランチをリモートにプッシュ |

---

#### ステップ4: Pull Requestを作成する

**何を考えているか**：
- 「GitHubでPull Requestを作成しよう」
- 「変更内容を明確に説明しよう」
- 「`Closes #1`でIssueと紐づけよう」

GitHubでリポジトリを開くと、「Compare & pull request」ボタンが表示されます。クリックして、以下の内容でPull Requestを作成します。

**タイトル**: ユーザー登録機能の追加

**本文**:

```
## 概要
Issue #1 に対応して、ユーザー登録機能を追加しました。

## 変更内容
- UserController.phpを作成
- ユーザー一覧表示機能（index）を実装
- ユーザー登録機能（store）を実装

## 確認方法
コードレビューをお願いします。

Closes #1
```

「Create pull request」をクリックします。

**コードリーディング**

| 部分 | 説明 |
|------|------|
| `Closes #1` | PRがマージされると、Issue #1が自動的にクローズされる |

> ⚠️ **重要**: このPull Requestは**マージせずにそのまま残してください**。12-3-5（コードレビューハンズオン）でレビューの練習に使用します。

---

### ✨ 完成！

これでGitHubコラボレーションが実践できました！IssueからPull Requestまでのワークフローを理解できましたね。

**確認ポイント**

| 確認項目 | 期待値 |
|----------|--------|
| Issues タブ | Issue #1 が作成されている |
| Pull requests タブ | PRが作成されている（Open状態） |
| PRの説明 | `Closes #1` が含まれている |

**自分で作成したリポジトリと比較してみましょう**：
- `github-collab-practice/`: 自分で作成したリポジトリ
- `github-collab-sample/`: 一緒に作成したリポジトリ

両方のGitHubリポジトリを開いて、IssueやPull Requestを比較してみてください。

> ⚠️ **重要**: Pull Requestは**マージしないでください**。12-3-5（コードレビューハンズオン）でこのPRに対してレビューの練習を行います。

---

## 📖 模範解答

### Issue作成

**タイトル**: ユーザー登録機能の追加

**本文**:

```
## 概要
ユーザー登録機能を追加する

## 要件
- [ ] UserController.phpを作成
- [ ] ユーザー一覧表示機能（index）
- [ ] ユーザー登録機能（store）
```

### ブランチ作成

```bash
git switch -c feature/issue-1-add-user-registration
```

### ファイル作成

```php
// UserController.php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class UserController extends Controller
{
    public function index()
    {
        $users = User::all();
        return view('users.index', ['users' => $users]);
    }

    public function store(Request $request)
    {
        $user = new User;
        $user->name = $request->name;
        $user->email = $request->email;
        $user->password = $request->password;
        $user->save();

        return redirect('/users');
    }
}
```

### コミット・プッシュ

```bash
git add UserController.php
git commit -m "Add #1: Add user registration feature"
git push origin feature/issue-1-add-user-registration
```

### Pull Request作成

**タイトル**: ユーザー登録機能の追加

**本文**:

```
## 概要
Issue #1 に対応して、ユーザー登録機能を追加しました。

## 変更内容
- UserController.phpを作成
- ユーザー一覧表示機能（index）を実装
- ユーザー登録機能（store）を実装

## 確認方法
コードレビューをお願いします。

Closes #1
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

| Step | 学んだこと |
|------|-----------|
| 1 | GitHubでIssueを作成する |
| 2 | `feature/issue-1-add-user-registration`ブランチを作成する |
| 3 | `UserController.php`を作成・コミット・プッシュする |
| 4 | Pull Requestを作成する |

**確認できたこと**:

- ✅ GitHubでIssueを作成できる
- ✅ Issue番号を含むブランチを作成できる
- ✅ コミットメッセージでIssueを参照できる
- ✅ Pull Requestを作成できる

> 💡 **次のステップ**: 12-3-5（コードレビューハンズオン）で、このPRに対してレビューの練習を行います。PRはマージせずにそのまま残しておいてください。

次のChapter 3では、コードレビューの重要性と進め方について学びます。

---
