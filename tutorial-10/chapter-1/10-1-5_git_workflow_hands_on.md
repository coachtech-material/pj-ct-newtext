# Tutorial 10-1-5: Gitワークフロー - ハンズオン演習

## 📝 このセクションの目的

Chapter 1で学んだGitワークフローを実際に手を動かして確認します。ブランチ戦略、マージ、コンフリクト解決を実践しましょう。

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

## 📖 模範解答

### 手順1: ブランチ作成

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

## 🚀 チャレンジ: コンフリクト解決

### シナリオ

1. `main`ブランチで`index.html`の1行目を編集してコミット
2. `feature/update-title`ブランチを作成
3. 同じ`index.html`の1行目を別の内容で編集してコミット
4. `main`にマージしてコンフリクトを解決

### コンフリクト解決手順

```bash
# mainブランチで編集
git checkout main
echo "<h1>メインタイトル</h1>" > index.html
git add index.html
git commit -m "Update main title"

# featureブランチで編集
git checkout -b feature/update-title
echo "<h1>新しいタイトル</h1>" > index.html
git add index.html
git commit -m "Update title in feature branch"

# mainにマージ（コンフリクト発生）
git checkout main
git merge feature/update-title

# コンフリクトを手動で解決
# index.htmlを編集して、どちらのタイトルを採用するか決定

# 解決後
git add index.html
git commit -m "Resolve merge conflict"
```

---

## 💪 自己評価チェックリスト

- [ ] ブランチを作成できた
- [ ] ブランチを切り替えられた
- [ ] マージができた
- [ ] コンフリクトを解決できた
- [ ] ブランチを削除できた

すべてチェックできたら、Chapter 2に進みましょう！
