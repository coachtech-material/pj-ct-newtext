# Tutorial 4-3-5: ファイルの状態確認 (git status)

## 🎯 このセクションで学ぶこと

*   `git status` コマンドの出力を、詳しく読み解く方法を学ぶ。
*   Gitが管理するファイルの4つの状態（Untracked, Staged, Modified, Unmodified）を理解する。
*   ファイルの状態遷移を理解し、現在の作業状況を正確に把握できるようになる。

---

## 導入

これまでのセクションで、あなたは `git add` でファイルをステージングし、`git commit` で変更を記録し、`git log` で履歴を確認する方法を学びました。その過程で、何度も `git status` コマンドを使ってきました。

`git status` は、「今、リポジトリがどのような状態にあるのか」を教えてくれる、**あなたの現在地を示すコンパス**のような存在です。何か操作に迷ったら、あるいは、次に何をすべきか分からなくなったら、まずは `git status` を実行する。これは、全てのGitユーザーが身につけるべき、基本的な習慣です。

このセクションでは、`git status` の出力を**詳しく読み解く**方法を学びます。`git status` の出力を正確に理解できるようになれば、「今、自分は何をすべきか」「次に何をすべきか」が、常に明確になります。

---

## 詳細解説

### 📊 ファイルの4つの状態

Gitは、リポジトリ内のファイルを、以下の4つの状態で管理しています。

```
                   git add
  Untracked ─────────────────────────► Staged
      │                                   │
      │                                   │ git commit
      │                                   ▼
      │                              Unmodified
      │                                   │
      │                                   │ ファイルを編集
      │                                   ▼
      └───────────────────────────── Modified
                                          │
                                          │ git add
                                          ▼
                                       Staged
```

| 状態 | 説明 |
| :--- | :--- |
| **Untracked (未追跡)** | Gitの管理下にない、新しく作成されたファイル。まだ一度も `git add` されていない。 |
| **Staged (ステージ済み)** | `git add` によって、次のコミットに含める準備ができた状態。 |
| **Unmodified (変更なし)** | 最後のコミット以降、変更されていないファイル。 |
| **Modified (変更あり)** | 最後のコミット以降、変更されたが、まだ `git add` されていないファイル。 |

### 🔍 `git status` の出力を読み解く

それでは、実際に `git status` の出力を見ながら、各状態を確認していきましょう。

#### 状態1: クリーンな状態（全てコミット済み）

全ての変更がコミットされ、ワーキングディレクトリがクリーンな状態では、以下のように表示されます。

```bash
git status
```

```
On branch main
nothing to commit, working tree clean
```

*   `On branch main`: 現在、`main` ブランチにいることを示しています。
*   `nothing to commit, working tree clean`: コミットすべき変更がなく、作業ディレクトリがクリーンであることを示しています。

#### 状態2: Untracked（新しいファイルがある）

新しいファイルを作成したが、まだ `git add` していない状態です。

```bash
# 新しいファイルを作成
touch LICENSE
git status
```

```
On branch main
Untracked files:
  (use "git add <file>..." to include in what will be committed)
        LICENSE

nothing added to commit but untracked files present (use "git add" to track)
```

*   `Untracked files`: Gitがまだ追跡していないファイルの一覧です。
*   赤色で表示されるファイル名は、まだステージングされていないことを示します。
*   Gitは親切に「`git add` を使ってください」と次の操作を教えてくれています。

#### 状態3: Staged（ステージング済み）

`git add` でファイルをステージングした状態です。

```bash
git add LICENSE
git status
```

```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   LICENSE
```

*   `Changes to be committed`: 次のコミットに含まれる変更の一覧です。
*   緑色で表示されるファイル名は、ステージングされていることを示します。
*   `new file:` は、このファイルが新規作成されたことを示しています。

#### 状態4: Modified（変更あり、未ステージング）

既にコミット済みのファイルを編集したが、まだ `git add` していない状態です。

```bash
# 既存のファイルを編集
echo "Add a new line." >> README.md
git status
```

```
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md
```

*   `Changes not staged for commit`: 変更されたが、まだステージングされていないファイルの一覧です。
*   `modified:` は、このファイルが変更されたことを示しています。
*   赤色で表示されます。

#### 状態5: 複合状態（複数の状態が混在）

実際の開発では、複数の状態が同時に存在することがよくあります。

```
On branch main
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        new file:   LICENSE

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        temp.txt
```

この出力は以下を意味します：
*   `LICENSE`: ステージング済み（緑色）→ 次のコミットに含まれる
*   `README.md`: 変更あり、未ステージング（赤色）→ `git add` が必要
*   `temp.txt`: 未追跡（赤色）→ `git add` するか、無視するか決める

### 📋 `git status -s` で簡潔に表示

ファイルが多い場合、`git status` の出力は長くなります。`-s`（short）オプションを使うと、簡潔な形式で表示できます。

```bash
git status -s
```

```
A  LICENSE
 M README.md
?? temp.txt
```

| 記号 | 意味 |
| :--- | :--- |
| `A` | 新規追加（Staged） |
| `M` | 変更あり（左側がステージング状態、右側がワーキングディレクトリ状態） |
| `??` | 未追跡（Untracked） |

---

## ✨ まとめ

このセクションでは、`git status` コマンドの出力を詳しく読み解く方法を学びました。

*   **`git status` はコンパス**: Gitを使っていて、次に何をすべきか迷ったら、まず `git status` を実行する習慣をつけましょう。Gitは、常に的確なヒントを与えてくれます。
*   **ファイルの4つの状態**: Untracked（未追跡）、Staged（ステージ済み）、Unmodified（変更なし）、Modified（変更あり）
*   **`git status` の読み方**:
    *   `Changes to be committed`: ステージング済み（緑色）→ コミット準備OK
    *   `Changes not staged for commit`: 変更あり、未ステージング（赤色）→ `git add` が必要
    *   `Untracked files`: 未追跡（赤色）→ 新しいファイル
*   **`git status -s`**: 簡潔な形式で状態を表示

`git status` は、Gitを使う上で最も頻繁に使うコマンドの一つです。作業の前後、コミットの前後など、こまめに `git status` を実行して、現在の状況を把握する習慣をつけましょう。「迷ったら `git status`」を合言葉に、Gitと上手に付き合っていきましょう。

これで、Gitの基本的なローカルでの操作は、一通りマスターしました。次のチャプターでは、いよいよ、ローカルリポジトリでの変更を、GitHub上のリモートリポジトリと連携させる方法を学んでいきます。

---
