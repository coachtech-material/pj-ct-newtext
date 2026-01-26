# Tutorial 12-2-4: GitHub連携 - ハンズオン演習

## 📝 このセクションの目的

Chapter 2で学んだGitHub連携を実際に手を動かして確認します。Issue、Pull Request、レビューのワークフローを実践しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのリポジトリを作成します。

```
~/git-practice/
├── 12-2-4_hands-on/                         ← このハンズオン用のディレクトリ
│   ├── github-collab-practice/              ← 要件を見て自分で作成するリポジトリ
│   │   └── contact.html
│   └── github-collab-sample/                ← 実践で一緒に作成するリポジトリ
│       └── contact.html
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

### 🖼️ 完成イメージ

<!-- GitHubのIssueとPull Request画面のスクリーンショットをここに配置 -->
![12-2-4 完成イメージ](images/12-2-4_github_collaboration_complete.png)

**この演習で作るもの**：
Issueを作成し、ブランチで開発し、Pull Requestを作成する「GitHubコラボレーションワークフロー」を実践します。

---

### 📋 要件

1. GitHubでIssueを作成
2. Issueに対応するブランチを作成
3. 機能を実装してコミット
4. Pull Requestを作成
5. レビューコメントを追加

---

### ✅ 完成品の確認方法

**🌐 GitHubでの確認**

- **確認場所**: GitHubリポジトリの「Issues」タブと「Pull requests」タブ
- **確認手順**:
  1. GitHubリポジトリにアクセス
  2. 「Issues」タブでIssueが作成されていることを確認
  3. 「Pull requests」タブでPRが作成されていることを確認
  4. PRにレビューコメントが追加されていることを確認

**正しく実装できていれば**:
- [ ] Issueが作成されている
- [ ] Issueに対応するブランチが作成されている
- [ ] Pull Requestが作成されている
- [ ] PRにレビューコメントが追加されている
- [ ] PRのDescriptionにIssue番号がリンクされている

**🔧 コマンドラインでの確認**:

```bash
# リモートブランチの確認
git branch -r

# プッシュ済みコミットの確認
git log --oneline origin/main
```

---

## 🔧 環境準備（自分で作成する用）

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

# mainブランチに切り替え
git branch -M main

# 初期ファイルを作成してコミット（GitHubにプッシュするため）
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
git remote add origin https://github.com/あなたのユーザー名/github-collab-practice.git

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
git checkout -b feature/issue-1-add-contact-form

# 実装後
git add .
git commit -m "Fix #1: Add contact form"
git push origin feature/issue-1-add-contact-form
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？GitHubコラボレーションはチーム開発の基本です。一緒に手を動かしながら、IssueからPull Requestまでのワークフローを実践していきましょう。

> 📌 **注意**: ここからは`github-collab-sample/`ディレクトリで作業します。自分で作成したリポジトリと比較できるように、別のリポジトリで進めましょう。

---

### 💻 環境準備（実践用リポジトリ）

### Step 1: ローカルリポジトリを作成

```bash
# ハンズオンディレクトリに移動
cd ~/git-practice/12-2-4_hands-on

# 実践用のリポジトリを作成
mkdir github-collab-sample
cd github-collab-sample

# Gitリポジトリを初期化
git init

# mainブランチに切り替え
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
git remote add origin https://github.com/あなたのユーザー名/github-collab-sample.git

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

### 💭 実装の思考プロセス

GitHubコラボレーションを進める際、以下の順番で考えると効率的です：

1. **Issueでタスクを管理**：何をするかを明確にする
2. **ブランチを作成**：Issue番号を含めて紐付ける
3. **機能を実装**：Issueの要件に従う
4. **Pull Requestを作成**：レビューを依頼する
5. **レビュー・マージ**：チームで確認して統合

---

### 📝 ステップバイステップで実装

#### ステップ1: GitHubでIssueを作成する

**何を考えているか**：
- 「タスクを管理するためにIssueを作成しよう」
- 「要件を明確に記載して、チームで共有しよう」

GitHubでリポジトリを開き、「Issues」タブ → 「New issue」をクリックします。

**タイトル**: お問い合わせフォームの追加

**本文**:
```
## 概要
お問い合わせフォームを追加する

## 要件
- [ ] contact.htmlを作成
- [ ] 名前、メール、メッセージの入力欄
- [ ] 送信ボタン

## 期限
2024-12-20
```

「Submit new issue」をクリックしてIssueを作成します。

---

#### ステップ2: Issueに対応するブランチを作成する

**何を考えているか**：
- 「Issue番号をブランチ名に含めよう」
- 「どのIssueに対応しているかがわかりやすくなる」

ターミナルで以下のコマンドを実行します：

```bash
git checkout -b feature/issue-1-add-contact-form
```

**コマンド解説**：

```bash
git checkout -b feature/issue-1-add-contact-form
```
→ `feature/issue-1-`という接頭辞で、Issue #1に対応するブランチであることがわかります。

---

#### ステップ3: 機能を実装する

**何を考えているか**：
- 「Issueの要件に従って機能を実装しよう」
- 「お問い合わせフォームを作成しよう」

`contact.html`を作成します：

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>お問い合わせ</title>
</head>
<body>
    <h1>お問い合わせ</h1>
    <form>
        <div>
            <label>名前</label>
            <input type="text" name="name" required>
        </div>
        <div>
            <label>メールアドレス</label>
            <input type="email" name="email" required>
        </div>
        <div>
            <label>メッセージ</label>
            <textarea name="message" required></textarea>
        </div>
        <button type="submit">送信</button>
    </form>
</body>
</html>
```

---

#### ステップ4: コミット・プッシュする

**何を考えているか**：
- 「コミットメッセージにIssue番号を含めよう」
- 「`Fix #1`を含めると、マージ時に自動的にIssueがクローズされる」

ターミナルで以下のコマンドを実行します：

```bash
git add contact.html
git commit -m "Fix #1: Add contact form"
git push origin feature/issue-1-add-contact-form
```

**コマンド解説**：

```bash
git commit -m "Fix #1: Add contact form"
```
→ `Fix #1`を含めることで、このコミットがIssue #1に対応していることがわかります。Pull Requestがマージされると、自動的にIssue #1がクローズされます。

---

#### ステップ5: Pull Requestを作成する

**何を考えているか**：
- 「GitHubでPull Requestを作成しよう」
- 「変更内容を明確に説明しよう」
- 「レビューを依頼しよう」

GitHubでリポジトリを開くと、「Compare & pull request」ボタンが表示されます。クリックして、以下の内容でPull Requestを作成します。

**タイトル**: お問い合わせフォームの追加

**本文**:
```
## 概要
Issue #1 に対応して、お問い合わせフォームを追加しました。

## 変更内容
- contact.htmlを作成
- 名前、メール、メッセージの入力欄を実装
- 送信ボタンを追加

## 確認方法
contact.htmlをブラウザで開いて、フォームが正しく表示されることを確認してください。

Closes #1
```

「Create pull request」をクリックします。

---

#### ステップ6: レビューコメントを追加する

**何を考えているか**：
- 「コードをレビューしてコメントを追加しよう」
- 「良い点や改善点をフィードバックしよう」

Pull Requestの「Files changed」タブで、コードの特定の行にコメントを追加できます。

**承認コメント例**:
```
LGTM! 👍
お問い合わせフォームが正しく実装されています。
```

**修正依頼コメント例**:
```
フォームにバリデーションを追加してください。
- 名前は必須
- メールアドレスは正しい形式
```

---

### ✨ 完成！

これでGitHubコラボレーションが実践できました！IssueからPull Requestまでのワークフローを理解できましたね。

**自分で作成したリポジトリと比較してみましょう**：
- `github-collab-practice/`: 自分で作成したリポジトリ
- `github-collab-sample/`: 一緒に作成したリポジトリ

両方のGitHubリポジトリを開いて、IssueやPull Requestを比較してみてください。

---

## 📖 模範解答

### 手順１: GitHubでIssue作成

**タイトル**: お問い合わせフォームの追加

**本文**:
```
## 概要
お問い合わせフォームを追加する

## 要件
- [ ] contact.htmlを作成
- [ ] 名前、メール、メッセージの入力欄
- [ ] 送信ボタン

## 期限
2024-12-20
```

### 手順2: ブランチ作成

```bash
git checkout -b feature/issue-1-add-contact-form
```

### 手順3: ファイル作成

```html
<!-- contact.html -->
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>お問い合わせ</title>
</head>
<body>
    <h1>お問い合わせ</h1>
    <form>
        <div>
            <label>名前</label>
            <input type="text" name="name" required>
        </div>
        <div>
            <label>メールアドレス</label>
            <input type="email" name="email" required>
        </div>
        <div>
            <label>メッセージ</label>
            <textarea name="message" required></textarea>
        </div>
        <button type="submit">送信</button>
    </form>
</body>
</html>
```

### 手順4: コミット・プッシュ

```bash
git add contact.html
git commit -m "Fix #1: Add contact form"
git push origin feature/issue-1-add-contact-form
```

### 手順5: Pull Request作成

**タイトル**: お問い合わせフォームの追加

**本文**:
```
## 概要
Issue #1 に対応して、お問い合わせフォームを追加しました。

## 変更内容
- contact.htmlを作成
- 名前、メール、メッセージの入力欄を実装
- 送信ボタンを追加

## 確認方法
contact.htmlをブラウザで開いて、フォームが正しく表示されることを確認してください。

Closes #1
```

### 手順6: レビューコメント例

**承認コメント**:
```
LGTM! 👍
お問い合わせフォームが正しく実装されています。
```

**修正依頼コメント**:
```
フォームにバリデーションを追加してください。
- 名前は必須
- メールアドレスは正しい形式
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ GitHubでIssueを作成できる
- ✅ Issueに対応するブランチを作成できる
- ✅ コミットメッセージでIssueを参照できる
- ✅ Pull Requestを作成できる
- ✅ レビューコメントを追加できる

引き続き、次のセクションも頑張りましょう！

---
