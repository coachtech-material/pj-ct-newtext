# Tutorial 10-1-5: Gitワークフロー - ハンズオン演習

## 📝 このセクションの目的

Chapter 1で学んだGitワークフローを実際に手を動かして確認します。ブランチ戦略、マージ、コンフリクト解決を実践しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 🎯 演習課題：機能開発ブランチでの作業

### 📋 要件

1. `main`ブランチから`feature/user-profile`ブランチを作成
2. `profile.html`を作成してコミット
3. `main`ブランチにマージ
4. コンフリクトが発生した場合は解決

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
- 「機能開発が完了したのmainに統合しよう」
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

これでGitワークフローが実践できました！ブランチで機能を分離し、マージで統合する流れを理解できましたね```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？Gitワークフローはチーム開発において不可欠なスキルです。一緒に手を動かしながら、ブランチ戦略を実践していきましょう。

### 💭 実装の思考プロセス

Gitワークフローを進める際、以下の順番で考えると効率的です。ブランチで機能を分離し、安全に開発を進めることが重要です。

---

### 📝 ステップバイステップで実装

#### ステップ1: 機能ブランチを作成する

新しい機能を開発するため、mainブランチから分岐して機能ブランチを作成します。`feature/`という接頭辞で機能ブランチとわかるようにします。

```bash
git checkout -b feature/user-profile
```

`git checkout -b`で新しいブランチを作成し、同時にそのブランチに切り替えます。

---

#### ステップ2: ファイルを作成・編集する

ユーザープロフィールページを作成します。シンプルなHTMLでプロフィール情報を表示します。

---

#### ステップ3: 変更をコミットする

作成したファイルをGitに追加し、意味のあるコミットメッセージでコミットします。

```bash
git add profile.html
git commit -m "Add user profile page"
```

---

#### ステップ4: mainブランチにマージする

機能開発が完了したのmainブランチに統合します。

```bash
git checkout main
git merge feature/user-profile
```

---

#### ステップ5: 使用済みブランチを削除する

マージが完了したブランチは不要なので削除して整理します。

```bash
git branch -d feature/user-profile
```

---

### ✨ 完成！

これでGitワークフローが実践できました！ブランチで機能を分離し、マージで統合する流れを理解できましたね。

---

## 📖 模範解答

### 手順１: ブランチ作成

```bash
git checkout -b feature/user-profile``

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

- ✅ Chapter 1で学んだGitワークフローを実際に手を動かして確認します。ブランチ戦略、マージ、コンフリクト解決を実践しましょう。

引き続き、次のセクションも頑張りましょう！

---
