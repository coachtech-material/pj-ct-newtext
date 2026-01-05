# Tutorial 12-1-5: Gitワークフロー - ハンズオン演習

## 📝 このセクションの目的

Chapter 1で学んだGitワークフローを実際に手を動かして確認します。ブランチ戦略、マージ、コンフリクト解決を実践しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのリポジトリを作成します。

```
~/git-practice/
├── 12-1-5_hands-on/                      ← このハンズオン用のディレクトリ
│   ├── git-workflow-practice/            ← 要件を見て自分で作成するリポジトリ
│   │   └── profile.html
│   └── git-workflow-sample/              ← 実践で一緒に作成するリポジトリ
│       └── profile.html
└── ...
```

| ディレクトリ | 用途 |
|:---|:---|
| `git-workflow-practice/` | 📋 要件を見て、自分の力で作成する |
| `git-workflow-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したリポジトリと、解答を見ながら作成したリポジトリを比較することで、理解が深まります。

---

## 🎯 演習課題：機能開発ブランチでの作業

### 📋 要件

1. `main`ブランチから`feature/user-profile`ブランチを作成
2. `profile.html`を作成してコミット
3. `main`ブランチにマージ
4. コンフリクトが発生した場合は解決

---

## 🔧 環境準備（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のリポジトリを準備します。

```bash
# git-practiceディレクトリに移動（なければ作成）
mkdir -p ~/git-practice
cd ~/git-practice

# ハンズオン用ディレクトリを作成
mkdir -p 12-1-5_hands-on
cd 12-1-5_hands-on

# 自分で作成する用のリポジトリを作成
mkdir git-workflow-practice
cd git-workflow-practice

# Gitリポジトリを初期化
git init

# mainブランチに切り替え（Git 2.28以降）
git branch -M main
```

**✅ ディレクトリ構造の確認**

```
~/git-practice/
└── 12-1-5_hands-on/
    └── git-workflow-practice/     ← 自分で作成する用（今ここ）
        └── .git/
```

> 💡 **環境構築が完了！**
> 
> `git status`を実行して、Gitリポジトリが初期化されていることを確認してください。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

```bash
# ブランチ作成
git checkout -b feature/user-profile

# ファイル作成・コミット
git add profile.html
git commit -m "Add user profile page"

# mainブランチに切り替え
git checkout main

# マージ
git merge feature/user-profile
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？Gitワークフローはチーム開発において不可欠なスキルです。一緒に手を動かしながら、ブランチ戦略を実践していきましょう。

> 📌 **注意**: ここからは`git-workflow-sample/`ディレクトリで作業します。自分で作成したリポジトリと比較できるように、別のリポジトリで進めましょう。

---

### 💻 環境準備（実践用リポジトリ）

**実践用のリポジトリを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/git-practice/12-1-5_hands-on

# 実践用のリポジトリを作成
mkdir git-workflow-sample
cd git-workflow-sample

# Gitリポジトリを初期化
git init

# mainブランチに切り替え
git branch -M main
```

**✅ ディレクトリ構造の確認**

```
~/git-practice/
└── 12-1-5_hands-on/
    ├── git-workflow-practice/     ← 自分で作成した用
    └── git-workflow-sample/       ← 実践用（今ここ）
        └── .git/
```

---

### 💭 実装の思考プロセス

Gitワークフローを進める際、以下の順番で考えると効率的です：

1. **機能ブランチを作成**：mainから分岐して作業
2. **ファイルを作成・編集**：機能を実装
3. **変更をコミット**：意味のある単位で保存
4. **mainブランチにマージ**：機能を統合
5. **使用済みブランチを削除**：整理して終了

Gitワークフローのポイントは「ブランチで機能を分離し、安全に開発を進める」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: 機能ブランチを作成する

**何を考えているか**：
- 「新しい機能を開発するためのブランチが必要だ」
- 「mainブランチに影響を与えずに作業したい」
- 「feature/という接頭辞で機能ブランチとわかるようにしよう」

ターミナルで以下のコマンドを実行します：

```bash
git checkout -b feature/user-profile
```

**コマンド解説**：

```bash
git checkout -b feature/user-profile
```
→ `git checkout -b`で新しいブランチを作成し、同時にそのブランチに切り替えます。`feature/user-profile`という名前で、ユーザープロフィール機能を開発するブランチであることがわかります。

現在のブランチを確認するには：

```bash
git branch
```

---

#### ステップ2: ファイルを作成・編集する

**何を考えているか**：
- 「ユーザープロフィールページを作成しよう」
- 「シンプルなHTMLでプロフィール情報を表示しよう」

`profile.html`を作成します：

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>プロフィール</title>
</head>
<body>
    <h1>ユーザープロフィール</h1>
    <p>名前: 山田太郎</p>
    <p>メール: yamada@example.com</p>
</body>
</html>
```

**コード解説**：

→ シンプルなHTMLファイルでユーザープロフィールを表示します。実際の開発では、このように機能を少しずつ実装していきます。

---

#### ステップ3: 変更をコミットする

**何を考えているか**：
- 「作成したファイルをGitに追加しよう」
- 「意味のあるコミットメッセージを書こう」
- 「英語で簡潔に説明しよう」

ターミナルで以下のコマンドを実行します：

```bash
git add profile.html
git commit -m "Add user profile page"
```

**コマンド解説**：

```bash
git add profile.html
```
→ `git add`でファイルをステージングエリアに追加します。コミットする変更を準備します。

```bash
git commit -m "Add user profile page"
```
→ `git commit`で変更をコミットします。`-m`オプションでコミットメッセージを指定します。メッセージは「何をしたか」を簡潔に表現します。

コミット履歴を確認するには：

```bash
git log --oneline
```

---

#### ステップ4: mainブランチにマージする

**何を考えているか**：
- 「機能開発が完了したのでmainに統合しよう」
- 「まずmainブランチに切り替えよう」
- 「マージで変更を統合しよう」

ターミナルで以下のコマンドを実行します：

```bash
git checkout main
git merge feature/user-profile
```

**コマンド解説**：

```bash
git checkout main
```
→ `git checkout`でmainブランチに切り替えます。マージ先のブランチに移動します。

```bash
git merge feature/user-profile
```
→ `git merge`で`feature/user-profile`ブランチの変更をmainブランチに統合します。コンフリクトがなければ、自動的にマージされます。

マージ後の状態を確認するには：

```bash
git log --oneline --graph
```

---

#### ステップ5: 使用済みブランチを削除する

**何を考えているか**：
- 「マージが完了したブランチは不要だ」
- 「ブランチを削除して整理しよう」
- 「-dオプションで安全に削除しよう」

ターミナルで以下のコマンドを実行します：

```bash
git branch -d feature/user-profile
```

**コマンド解説**：

```bash
git branch -d feature/user-profile
```
→ `git branch -d`でブランチを削除します。`-d`オプションはマージ済みのブランチのみ削除できる安全な削除です。マージされていない場合はエラーが出ます。

ブランチ一覧を確認するには：

```bash
git branch
```

---

### 🔥 コンフリクト解決の実践

**何を考えているか**：
- 「コンフリクトが発生したらどうする？」
- 「手動でマージして解決する必要がある」

コンフリクトが発生した場合の手順：

1. **コンフリクトファイルを確認**：

```bash
git status
```

2. **ファイルを開いて編集**：

```html
<<<<<<< HEAD
<p>名前: 山田花子</p>
=======
<p>名前: 山田太郎</p>
>>>>>>> feature/user-profile
```

3. **コンフリクトマーカーを削除して正しい内容に修正**：

```html
<p>名前: 山田太郎</p>
```

4. **解決後にコミット**：

```bash
git add profile.html
git commit -m "Resolve merge conflict"
```

---

### ✨ 完成！

これでGitワークフローが実践できました！ブランチで機能を分離し、マージで統合する流れを理解できましたね。

**自分で作成したリポジトリと比較してみましょう**：
- `git-workflow-practice/`: 自分で作成したリポジトリ
- `git-workflow-sample/`: 一緒に作成したリポジトリ

両方のリポジトリで`git log --oneline`を実行して、コミット履歴を比較してみてください。

---

## 📖 模範解答

### 手順１: ブランチ作成

```bash
git checkout -b feature/user-profile
```

### 手順2: ファイル作成

```html
<!-- profile.html -->
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>プロフィール</title>
</head>
<body>
    <h1>ユーザープロフィール</h1>
    <p>名前: 山田太郎</p>
    <p>メール: yamada@example.com</p>
</body>
</html>
```

### 手順3: コミット

```bash
git add profile.html
git commit -m "Add user profile page"
```

### 手順4: mainブランチにマージ

```bash
git checkout main
git merge feature/user-profile
```

### 手順5: ブランチ削除

```bash
git branch -d feature/user-profile
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ 機能ブランチを作成できる
- ✅ ブランチで作業してコミットできる
- ✅ mainブランチにマージできる
- ✅ コンフリクトを解決できる
- ✅ 使用済みブランチを削除できる

引き続き、次のセクションも頑張りましょう！

---
