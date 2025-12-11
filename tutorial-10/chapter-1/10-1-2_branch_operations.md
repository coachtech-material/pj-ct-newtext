# Tutorial 10-1-2: ブランチの作成と切り替え

## 🎯 このセクションで学ぶこと

*   `git branch`と`git switch`を使って、ブランチを作成・切り替える方法を学ぶ。
*   ブランチの一覧を確認する方法を学ぶ。
*   ブランチを削除する方法を学ぶ。

---

## 導入：ブランチ操作の基本

ブランチ戦略を実践するには、**ブランチの作成・切り替え・削除**ができる必要があります。このセクションでは、これらの基本操作を学びます。

---

## 詳細解説

### 🔧 ブランチの確認

#### 現在のブランチを確認

```bash
git branch
```

**実行結果**

```
* main
  develop
  feature/add-login
```

`*`が付いているのが、現在のブランチです。

---

#### すべてのブランチを確認（リモートブランチを含む）

```bash
git branch -a
```

**実行結果**

```
* main
  develop
  feature/add-login
  remotes/origin/main
  remotes/origin/develop
  remotes/origin/feature/add-login
```

---

### 🔧 ブランチの作成

#### 新しいブランチを作成

```bash
git branch feature/add-profile
```

これで、`feature/add-profile`ブランチが作成されます。ただし、**ブランチは切り替わりません**。

---

#### ブランチを作成して切り替え

```bash
git switch -c feature/add-profile
```

`-c`オプションを使うと、ブランチを作成して切り替えます。

**従来の方法（`git checkout`）**

```bash
git checkout -b feature/add-profile
```

`git checkout`も使えますが、**`git switch`の方が推奨**されています。

---

### 🔧 ブランチの切り替え

#### 既存のブランチに切り替え

```bash
git switch main
```

**従来の方法（`git checkout`）**

```bash
git checkout main
```

---

### 💡 TIP: `git switch`と`git checkout`の違い

*   `git switch`: ブランチの切り替え専用（Git 2.23以降）
*   `git checkout`: ブランチの切り替え、ファイルの復元など多機能

`git switch`の方が**用途が明確**なので、推奨されています。

---

### 🚀 実践例1: 新機能開発の流れ

#### ステップ1: `main`ブランチに切り替え

```bash
git switch main
```

#### ステップ2: 最新の状態に更新

```bash
git pull origin main
```

#### ステップ3: 新しいブランチを作成

```bash
git switch -c feature/add-login
```

#### ステップ4: 機能開発

```bash
# コードを書く
git add .
git commit -m "Add login feature"
```

#### ステップ5: リモートにプッシュ

```bash
git push origin feature/add-login
```

---

### 🔧 ブランチの削除

#### ローカルブランチを削除

```bash
git branch -d feature/add-login
```

`-d`オプションは、**マージ済みのブランチのみ削除**します。

---

#### 強制的に削除

```bash
git branch -D feature/add-login
```

`-D`オプションは、**マージされていないブランチも削除**します。

---

#### リモートブランチを削除

```bash
git push origin --delete feature/add-login
```

---

### 🚀 実践例2: ブランチの削除

#### ステップ1: `main`ブランチに切り替え

```bash
git switch main
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

### 💡 TIP: ブランチの命名規則

*   `feature/機能名`: 新機能開発
*   `bugfix/バグ名`: バグ修正
*   `hotfix/バグ名`: 緊急バグ修正

**例**

*   `feature/add-login`
*   `bugfix/fix-validation-error`
*   `hotfix/fix-critical-bug`

---

### 🚀 実践例3: 複数のブランチを切り替える

#### ステップ1: `main`ブランチに切り替え

```bash
git switch main
```

#### ステップ2: `feature/add-login`ブランチに切り替え

```bash
git switch feature/add-login
```

#### ステップ3: `feature/add-profile`ブランチに切り替え

```bash
git switch feature/add-profile
```

---

### 🚨 よくある間違い

#### 間違い1: ブランチを切り替えずにコミット

```bash
# NG: mainブランチで直接開発
git switch main
git add .
git commit -m "Add new feature"
```

**対処法**: 必ず`feature`ブランチを作成してから開発します。

```bash
# OK
git switch main
git switch -c feature/add-new-feature
git add .
git commit -m "Add new feature"
```

---

#### 間違い2: 未コミットの変更があるままブランチを切り替え

```bash
# NG: 変更をコミットせずにブランチを切り替え
git add .
git switch main
```

**エラーメッセージ**

```
error: Your local changes to the following files would be overwritten by checkout:
	file.txt
Please commit your changes or stash them before you switch branches.
```

**対処法**: 変更をコミットするか、`git stash`で一時保存します。

```bash
# OK: コミットする
git add .
git commit -m "Work in progress"
git switch main

# OK: 一時保存する
git stash
git switch main
git stash pop
```

---

#### 間違い3: ブランチ名を間違える

```bash
# NG: ブランチ名が存在しない
git switch feature/add-logn
```

**エラーメッセージ**

```
fatal: invalid reference: feature/add-logn
```

**対処法**: `git branch`でブランチ一覧を確認します。

```bash
git branch
```

---

### 💡 TIP: `git stash`の使い方

`git stash`は、**未コミットの変更を一時保存**するコマンドです。

#### 変更を一時保存

```bash
git stash
```

#### 一時保存した変更を復元

```bash
git stash pop
```

#### 一時保存した変更の一覧を確認

```bash
git stash list
```

---

### 🚀 実践例4: `git stash`を使った開発

#### ステップ1: `feature/add-login`ブランチで開発中

```bash
git switch feature/add-login
# コードを書く
```

#### ステップ2: 緊急のバグ修正が必要になった

```bash
# 変更を一時保存
git stash
```

#### ステップ3: `main`ブランチに切り替えてバグ修正

```bash
git switch main
git switch -c hotfix/fix-critical-bug
# バグを修正
git add .
git commit -m "Fix critical bug"
git push origin hotfix/fix-critical-bug
```

#### ステップ4: `feature/add-login`ブランチに戻る

```bash
git switch feature/add-login
git stash pop
# 開発を続ける
```

---

## ✨ まとめ

このセクションでは、ブランチの作成と切り替えについて学びました。

*   `git branch`でブランチの一覧を確認できる。
*   `git switch -c`でブランチを作成して切り替えられる。
*   `git switch`でブランチを切り替えられる。
*   `git branch -d`でブランチを削除できる。
*   `git stash`で未コミットの変更を一時保存できる。

次のセクションでは、マージの基礎について学びます。

---

## 📝 学習のポイント

- [ ] `git branch`と`git switch`を使って、ブランチを作成・切り替えられる。
- [ ] ブランチの一覧を確認できる。
- [ ] ブランチを削除できる。
- [ ] `git stash`で未コミットの変更を一時保存できる。
