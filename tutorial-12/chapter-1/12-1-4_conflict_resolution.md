# Tutorial 12-1-4: コンフリクト解決の実践

## 🎯 このセクションで学ぶこと

*   コンフリクト（競合）が発生する原因を理解する。
*   コンフリクトを解決する方法を学ぶ。
*   実践的な演習を通じて、コンフリクト解決の流れを体験する。

---

## 導入：コンフリクトとは何か？

**コンフリクト（conflict）**とは、**同じファイルの同じ行を、異なるブランチで変更した場合に発生する競合**です。

例えば、以下のような状況でコンフリクトが発生します。

*   Aさんが`main`ブランチで`file.txt`の1行目を変更
*   Bさんが`feature`ブランチで`file.txt`の1行目を変更
*   Bさんが`feature`ブランチを`main`にマージしようとする

この場合、Gitは**どちらの変更を採用すべきか判断できない**ため、コンフリクトが発生します。

---

## 詳細解説

### 🔍 コンフリクトが発生する状況

#### 例

**`main`ブランチの`file.txt`**

```
Hello World
```

**`feature`ブランチの`file.txt`**

```
Hello Laravel
```

この状態で`feature`ブランチを`main`にマージすると、コンフリクトが発生します。

---

### 🚀 実践例1: コンフリクトの発生

#### ステップ1: `main`ブランチで`file.txt`を作成

```bash
git switch main
echo "Hello World" > file.txt
git add file.txt
git commit -m "Add file.txt"
```

#### ステップ2: `feature`ブランチを作成

```bash
git switch -c feature/update-greeting
```

#### ステップ3: `feature`ブランチで`file.txt`を変更

```bash
echo "Hello Laravel" > file.txt
git add file.txt
git commit -m "Update greeting to Laravel"
```

#### ステップ4: `main`ブランチに切り替えて、`file.txt`を変更

```bash
git switch main
echo "Hello PHP" > file.txt
git add file.txt
git commit -m "Update greeting to PHP"
```

#### ステップ5: `feature`ブランチをマージ

```bash
git merge feature/update-greeting
```

**実行結果**

```
Auto-merging file.txt
CONFLICT (content): Merge conflict in file.txt
Automatic merge failed; fix conflicts and then commit the result.
```

コンフリクトが発生しました！

---

### 🔧 コンフリクトの確認

#### `git status`でコンフリクトを確認

```bash
git status
```

**実行結果**

```
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   file.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

`both modified: file.txt`と表示されます。

---

#### ファイルの内容を確認

```bash
cat file.txt
```

**実行結果**

```
<<<<<<< HEAD
Hello PHP
=======
Hello Laravel
>>>>>>> feature/update-greeting
```

*   `<<<<<<< HEAD`: 現在のブランチ（`main`）の変更
*   `=======`: 区切り線
*   `>>>>>>> feature/update-greeting`: マージ元のブランチ（`feature`）の変更

---

### 🔧 コンフリクトの解決

#### ステップ1: ファイルを編集

エディタで`file.txt`を開き、コンフリクトマーカーを削除して、正しい内容に修正します。

**修正前**

```
<<<<<<< HEAD
Hello PHP
=======
Hello Laravel
>>>>>>> feature/update-greeting
```

**修正後**

```
Hello Laravel
```

---

#### ステップ2: 変更をステージング

```bash
git add file.txt
```

---

#### ステップ3: マージコミットを作成

```bash
git commit
```

デフォルトのマージコミットメッセージが表示されます。

```
Merge branch 'feature/update-greeting' into main

# Conflicts:
#	file.txt
```

保存して終了します。

---

### 💡 TIP: VSCodeでのコンフリクト解決

VSCodeでは、コンフリクトを視覚的に解決できます。

1. VSCodeで`file.txt`を開く
2. コンフリクトマーカーの上に、以下のボタンが表示される
   - **Accept Current Change**: 現在のブランチの変更を採用
   - **Accept Incoming Change**: マージ元のブランチの変更を採用
   - **Accept Both Changes**: 両方の変更を採用
   - **Compare Changes**: 変更を比較
3. ボタンをクリックして、コンフリクトを解決
4. `git add`と`git commit`を実行

---

### 🚀 実践例2: 複数ファイルのコンフリクト

#### ステップ1: `main`ブランチで2つのファイルを作成

```bash
git switch main
echo "File 1" > file1.txt
echo "File 2" > file2.txt
git add .
git commit -m "Add file1 and file2"
```

#### ステップ2: `feature`ブランチを作成

```bash
git switch -c feature/update-files
```

#### ステップ3: `feature`ブランチでファイルを変更

```bash
echo "File 1 - Feature" > file1.txt
echo "File 2 - Feature" > file2.txt
git add .
git commit -m "Update files in feature branch"
```

#### ステップ4: `main`ブランチに切り替えて、ファイルを変更

```bash
git switch main
echo "File 1 - Main" > file1.txt
echo "File 2 - Main" > file2.txt
git add .
git commit -m "Update files in main branch"
```

#### ステップ5: `feature`ブランチをマージ

```bash
git merge feature/update-files
```

**実行結果**

```
Auto-merging file2.txt
CONFLICT (content): Merge conflict in file2.txt
Auto-merging file1.txt
CONFLICT (content): Merge conflict in file1.txt
Automatic merge failed; fix conflicts and then commit the result.
```

2つのファイルでコンフリクトが発生しました。

---

#### ステップ6: コンフリクトを解決

```bash
# file1.txtを編集
echo "File 1 - Feature" > file1.txt
git add file1.txt

# file2.txtを編集
echo "File 2 - Feature" > file2.txt
git add file2.txt

# マージコミットを作成
git commit
```

---

### 💡 TIP: `git merge --abort`

マージを中止したい場合は、`git merge --abort`を使います。

```bash
git merge --abort
```

これで、マージ前の状態に戻ります。

---

### 🚀 実践例3: コンフリクトを避ける方法

#### 方法1: こまめにマージする

`main`ブランチの変更を、こまめに`feature`ブランチにマージします。

```bash
git switch feature/add-login
git merge main
```

---

#### 方法2: リベースを使う

`git rebase`を使って、`feature`ブランチを`main`ブランチの最新の状態に更新します。

```bash
git switch feature/add-login
git rebase main
```

---

### 🚨 よくある間違い

#### 間違い1: コンフリクトマーカーを残したままコミット

```bash
# NG: コンフリクトマーカーを削除していない
git add file.txt
git commit -m "Resolve conflict"
```

**対処法**: コンフリクトマーカーを削除してからコミットします。

---

#### 間違い2: 間違った変更を採用

```bash
# NG: 誤って現在のブランチの変更を採用
echo "Hello PHP" > file.txt
git add file.txt
git commit
```

**対処法**: コンフリクトを解決する前に、チームメンバーに確認します。

---

### 💡 TIP: コンフリクト解決のベストプラクティス

1. **コンフリクトが発生したら、落ち着いて対処する**
2. **ファイルの内容を確認し、どちらの変更を採用すべきか判断する**
3. **わからない場合は、チームメンバーに相談する**
4. **コンフリクトマーカーを削除してからコミットする**
5. **テストを実行して、正しく動作することを確認する**

---

### 🚀 実践例4: チーム開発でのコンフリクト解決

#### シナリオ

*   Aさんが`main`ブランチで`login.php`の1行目を変更
*   Bさんが`feature/add-login`ブランチで`login.php`の1行目を変更
*   Bさんが`feature/add-login`ブランチを`main`にマージしようとする

#### ステップ1: Bさんがコンフリクトを確認

```bash
git merge main
```

**実行結果**

```
CONFLICT (content): Merge conflict in login.php
```

---

#### ステップ2: Bさんがファイルを確認

```bash
cat login.php
```

**実行結果**

```
<<<<<<< HEAD
// Feature: Add login
=======
// Main: Update login
>>>>>>> main
```

---

#### ステップ3: Bさんがチームメンバーに相談

「`login.php`の1行目でコンフリクトが発生しました。どちらの変更を採用すべきですか？」

---

#### ステップ4: チームで決定

「Featureブランチの変更を採用しましょう」

---

#### ステップ5: Bさんがコンフリクトを解決

```bash
echo "// Feature: Add login" > login.php
git add login.php
git commit
```

---

## ✨ まとめ

このセクションでは、コンフリクト解決の実践を学びました。

*   コンフリクトは、同じファイルの同じ行を異なるブランチで変更した場合に発生する。
*   `git status`でコンフリクトを確認できる。
*   ファイルを編集して、コンフリクトマーカーを削除する。
*   `git add`と`git commit`でコンフリクトを解決する。
*   VSCodeを使うと、視覚的にコンフリクトを解決できる。

次のセクションでは、イシュー駆動開発について学びます。

---
