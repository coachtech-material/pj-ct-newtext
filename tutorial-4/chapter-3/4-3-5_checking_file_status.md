# Tutorial 4-3-5: ファイルの状態確認 (git status)

## 🎯 このセクションで学ぶこと

*   `git status` コマンドの重要性を再確認する。
*   ファイルの3つの主要な状態（`modified`, `staged`, `untracked`）を理解する。
*   `git status` の出力を読んで、各ファイルがどの状態にあるのかを判断できるようになる。

---

## 導入

これまでのセクションで、あなたは `git status` というコマンドを、何度か使ってきました。そして、その度に、Gitが現在の状況を、非常に丁寧に教えてくれることに、気づいたかもしれません。

`git status` は、Gitを使いこなす上で、**あなたの現在地を教えてくれる、最も重要なコンパス**です。何か操作に迷ったら、あるいは、次に何をすべきか分からなくなったら、まずは `git status` を実行する。これは、全てのGitユーザーが身につけるべき、基本的な習慣です。

このセクションでは、`git status` の出力結果を、より深く理解することに焦点を当てます。ファイルが変更されてからコミットされるまでの間に、ファイルの状態がどのように変化していくのか、そのライフサイクルを追いかけてみましょう。

---

## 詳細解説

### 📖 ファイルの状態遷移

Gitの管理下にあるファイルは、主に以下の3つの状態を持ちます。

1.  **Modified (変更済み)**
    *   ファイルは変更されたが、まだステージングエリアには追加されていない状態。ワーキングディレクトリに、最新のコミットとは異なる変更が存在することを示します。

2.  **Staged (ステージング済み)**
    *   変更されたファイルが、`git add` によって、次のコミットに含める準備ができている状態。ステージングエリアに変更が置かれていることを示します。

3.  **Committed (コミット済み)**
    *   ファイルの変更が、`git commit` によって、リポジトリに安全に記録された状態。

これに加えて、まだ一度もGitの管理下に置かれていない、**Untracked (追跡されていない)** という状態があります。

これらの状態が、どのように移り変わっていくのか、実際にファイルを変更しながら見ていきましょう。

### 1. ファイルを変更する (`Modified` 状態)

まず、`README.md` ファイルの内容を、少し変更してみます。以下のコマンドを実行して、ファイルに新しい行を追加してください。

```bash
# "Add a new line." というテキストを、README.md の末尾に追記
echo "Add a new line." >> README.md
```

ここで、コンパスである `git status` を実行します。

```bash
git status
```

```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
```

Gitは、「コミットのためにステージングされていない変更があります (`Changes not staged for commit`)」と教えてくれます。そして、`modified: README.md` という行で、`README.md` ファイルが**変更済み (Modified)** の状態であることを、明確に示しています。

### 2. 変更をステージングする (`Staged` 状態)

次に、この変更を、`git add` を使ってステージングエリアに追加します。

```bash
git add README.md
```

もう一度、`git status` を実行してみましょう。

```bash
git status
```

```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   README.md
```

今度は、「コミットされるべき変更があります (`Changes to be committed`)」というセクションに、`README.md` が表示されています。これは、ファイルが**ステージング済み (Staged)** の状態になったことを意味します。

### 3. 変更をコミットする (`Committed` 状態)

最後に、このステージング済みの変更を、リポジトリにコミットします。

```bash
git commit -m "Update README.md"
```

コミット後、`git status` を実行すると、おなじみのメッセージが返ってきます。

```bash
git status
```

```
On branch main
nothing to commit, working tree clean
```

ワーキングツリーは「clean」な状態です。これは、`README.md` の変更が、無事に**コミット済み (Committed)** の状態になったことを示しています。

### 4. 新しいファイルを追加する (`Untracked` 状態)

もう一度、`Untracked` の状態も確認しておきましょう。`LICENSE` という新しいファイルを作成します。

```bash
touch LICENSE
```

`git status` を実行します。

```bash
git status
```

```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        LICENSE

nothing added to commit but untracked files present (use "git add" to track)
```

`LICENSE` ファイルが、`Untracked files` のセクションに表示されています。これは、このファイルがまだGitの管理下に置かれていない、**追跡されていない (Untracked)** 状態であることを示しています。このファイルをバージョン管理に含めるには、`git add LICENSE` を実行する必要があります。

---

## ✨ まとめ

このセクションでは、`git status` コマンドの重要性と、その出力からファイルの様々な状態を読み解く方法について、詳しく学びました。

*   **`git status` はコンパス**: Gitを使っていて、次に何をすべきか迷ったら、まず `git status` を実行する習慣をつけましょう。Gitは、常に的確なヒントを与えてくれます。
*   **ファイルのライフサイクル**: 
    1.  **Untracked**: 新しく作成され、まだGitに追跡されていない状態。
    2.  **Modified**: Gitに追跡されているファイルが、変更された状態。
    3.  **Staged**: `git add` によって、次のコミットの準備ができた状態。
    4.  **Committed**: `git commit` によって、変更がリポジトリに記録された状態。

`git status` の出力を正確に読めるようになることは、Gitを自信を持って使いこなすための、非常に重要なスキルです。

これで、Gitの基本的なローカルでの操作は、一通りマスターしました。次のチャプターでは、いよいよ、ローカルリポジトリでの変更を、GitHub上のリモートリポジトリと連携させる方法を学んでいきます。

---

## 📝 学習のポイント

- [ ] `git status` が、現在のリポジトリの状態を確認するための最も重要なコマンドであることを理解している。
- [ ] `modified`, `staged`, `untracked` という、ファイルの主要な状態を説明できる。
- [ ] `git status` の出力を見て、どのファイルがどの状態にあるのかを判断できる。
