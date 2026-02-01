# Tutorial 12-1-3: マージの基礎

## 🎯 このセクションで学ぶこと

*   `git merge`を使って、ブランチをマージする方法を学ぶ。
*   Fast-forwardマージとNon-fast-forwardマージの違いを理解する。
*   マージコミットの作成方法を学ぶ。

---

## 導入：マージとは何か？

マージ（merge）とは、**別のブランチの変更を現在のブランチに統合すること**です。

例えば、`feature/add-login`ブランチで開発した機能を、`main`ブランチに統合する場合、マージを使います。

---

## 詳細解説

### 🔧 マージの基本

#### ステップ1: マージ先のブランチに切り替え

```bash
git switch main
```

#### ステップ2: マージ元のブランチをマージ

```bash
git merge feature/add-login
```

これで、`feature/add-login`ブランチの変更が`main`ブランチに統合されます。

---

### 🔍 Fast-forwardマージ

#### 概要

**Fast-forwardマージ**とは、**マージ先のブランチに新しいコミットがない場合**に行われるマージです。

#### 例

```
main:    A --- B
              \
feature:       C --- D
```

`main`ブランチに`feature`ブランチをマージすると、以下のようになります。

```
main:    A --- B --- C --- D
```

`main`ブランチのポインタが`D`に移動するだけで、**マージコミットは作成されません**。

---

### 🔍 Non-fast-forwardマージ

#### 概要

**Non-fast-forwardマージ**とは、**マージ先のブランチに新しいコミットがある場合**に行われるマージです。

#### 例

```
main:    A --- B --- E
              \
feature:       C --- D
```

`main`ブランチに`feature`ブランチをマージすると、以下のようになります。

```
main:    A --- B --- E --- M
              \           /
feature:       C --- D ---
```

**マージコミット（M）**が作成されます。

---

### 🚀 実践例1: Fast-forwardマージ

#### ステップ1: `main`ブランチから`feature`ブランチを作成

```bash
git switch main
git switch -c feature/add-login
```

#### ステップ2: 機能開発

```bash
# コードを書く
git add .
git commit -m "Add login feature"
```

#### ステップ3: `main`ブランチに切り替え

```bash
git switch main
```

#### ステップ4: `feature`ブランチをマージ

```bash
git merge feature/add-login
```

**実行結果**

```
Updating a1b2c3d..e4f5g6h
Fast-forward
 login.php | 10 ++++++++++
 1 file changed, 10 insertions(+)
```

`Fast-forward`と表示されます。

---

### 🚀 実践例2: Non-fast-forwardマージ

#### ステップ1: `main`ブランチから`feature`ブランチを作成

```bash
git switch main
git switch -c feature/add-login
```

#### ステップ2: 機能開発

```bash
# コードを書く
git add .
git commit -m "Add login feature"
```

#### ステップ3: `main`ブランチに切り替えて、別の変更をコミット

```bash
git switch main
# 別のコードを書く
git add .
git commit -m "Update README"
```

#### ステップ4: `feature`ブランチをマージ

```bash
git merge feature/add-login
```

**実行結果**

```
Merge made by the 'recursive' strategy.
 login.php | 10 ++++++++++
 1 file changed, 10 insertions(+)
```

マージコミットが作成されます。

---

### 💡 TIP: `--no-ff`オプション

`--no-ff`オプションを使うと、**Fast-forwardマージでもマージコミットを作成**できます。

```bash
git merge --no-ff feature/add-login
```

これにより、**マージの履歴が明確**になります。

---

### 🚀 実践例3: `--no-ff`オプションを使ったマージ

#### ステップ1: `main`ブランチから`feature`ブランチを作成

```bash
git switch main
git switch -c feature/add-login
```

#### ステップ2: 機能開発

```bash
# コードを書く
git add .
git commit -m "Add login feature"
```

#### ステップ3: `main`ブランチに切り替え

```bash
git switch main
```

#### ステップ4: `--no-ff`オプションを使ってマージ

```bash
git merge --no-ff feature/add-login
```

**実行結果**

```
Merge made by the 'recursive' strategy.
 login.php | 10 ++++++++++
 1 file changed, 10 insertions(+)
```

マージコミットが作成されます。

---

### 🔍 マージコミットのメッセージ

マージコミットのメッセージは、デフォルトで以下のようになります。

```
Merge branch 'feature/add-login' into main
```

`-m`オプションを使って、カスタムメッセージを指定できます。

```bash
git merge --no-ff -m "Merge login feature" feature/add-login
```

---

### 💡 TIP: マージ後のブランチ削除

マージが完了したら、`feature`ブランチを削除します。

```bash
git branch -d feature/add-login
```

---

### 🚀 実践例4: マージ後のブランチ削除

#### ステップ1: `feature`ブランチをマージ

```bash
git switch main
git merge feature/add-login
```

#### ステップ2: ローカルブランチを削除

```bash
git branch -d feature/add-login
```

#### ステップ3: リモートブランチを削除

```bash
git push origin --delete feature/add-login
```

---

### 🚨 よくある間違い

#### 間違い1: マージ先のブランチを間違える

```bash
# NG: featureブランチでmainをマージ
git switch feature/add-login
git merge main
```

**対処法**: マージ先のブランチに切り替えてからマージします。

```bash
# OK
git switch main
git merge feature/add-login
```

---

#### 間違い2: 未コミットの変更があるままマージ

```bash
# NG: 変更をコミットせずにマージ
git add .
git merge feature/add-login
```

**エラーメッセージ**

```
error: Your local changes to the following files would be overwritten by merge:
	file.txt
Please commit your changes or stash them before you merge.
```

**対処法**: 変更をコミットするか、`git stash`で一時保存します。

```bash
# OK: コミットする
git add .
git commit -m "Work in progress"
git merge feature/add-login

# OK: 一時保存する
git stash
git merge feature/add-login
git stash pop
```

---

### 💡 TIP: マージの取り消し

マージを取り消すには、`git reset`を使います。

```bash
git reset --hard HEAD~1
```

ただし、**リモートにプッシュした後は取り消せません**。

---

### 🚀 実践例5: GitHub Flowの流れ

#### ステップ1: `main`ブランチから`feature`ブランチを作成

```bash
git switch main
git pull origin main
git switch -c feature/add-login
```

#### ステップ2: 機能開発

```bash
# コードを書く
git add .
git commit -m "Add login feature"
git push origin feature/add-login
```

#### ステップ3: GitHubでプルリクエストを作成

#### ステップ4: レビュー後、`main`にマージ

GitHubでマージボタンをクリックします。

#### ステップ5: ローカルの`main`ブランチを更新

```bash
git switch main
git pull origin main
```

#### ステップ6: ブランチを削除

```bash
git branch -d feature/add-login
```

---

## ✨ まとめ

このセクションでは、マージの基礎を学びました。

*   `git merge`を使って、ブランチをマージできる。
*   Fast-forwardマージは、マージコミットを作成しない。
*   Non-fast-forwardマージは、マージコミットを作成する。
*   `--no-ff`オプションを使うと、Fast-forwardマージでもマージコミットを作成できる。

次のセクションでは、コンフリクト解決の実践について学びます。

---
