# Tutorial 10-2-5: GitHub連携 - ハンズオン演習

## 📝 このセクションの目的

Chapter 2で学んだGitHub連携を実際に手を動かして確認します。Issue、Pull Request、レビューのワークフローを実践しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 🎯 演習課題：Pull Requestを作成しよう

### 📋 要件

1. GitHubでIssueを作成
2. Issueに対応するブランチを作成
3. 機能を実装してコミット
4. Pull Requestを作成
5. レビューコメントを追加

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

### 💭 実装の思考プロセス

GitHubコラボレーションを進める際、以下の順番で考えると効率的です。Issueでタスクを管理し、Pull Requestでレビューを受けることが重要です。

---

### 📝 ステップバイステップで実装

#### ステップ1: GitHubでIssueを作成する

タスクを管理するためにGitHubでIssueを作成します。要件を明確に記載し、チームで共有します。

---

#### ステップ2: Issueに対応するブランチを作成する

Issue番号をブランチ名に含めることで、どのIssueに対応しているかがわかりやすくなります。

```bash
git checkout -b feature/issue-1-add-contact-form
```

---

#### ステップ3: 機能を実装する

Issueの要件に従って機能を実装します。お問い合わせフォームを作成します。

---

#### ステップ4: コミット・プッシュする

コミットメッセージに`Fix #1`を含めることで、マージ時に自動的にIssueがクローズされます。

```bash
git add contact.html
git commit -m "Fix #1: Add contact form"
git push origin feature/issue-1-add-contact-form
```

---

#### ステップ5: Pull Requestを作成する

GitHubでPull Requestを作成し、レビューを依頼します。変更内容を明確に説明します。

---

### ✨ 完成！

これでGitHubコラボレーションが実践できました！IssueからPull Requestまでのワークフローを理解できましたね。

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

## 💪 自己評価チェックリスト

- [ ] Issueを作成できた
- [ ] Issueに対応するブランチを作成できた
- [ ] Pull Requestを作成できた
- [ ] レビューコメントを追加できた
- [ ] マージができた

すべてチェックできたら、Chapter 3に進みましょう！
