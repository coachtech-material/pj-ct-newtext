# Tutorial 11-2-4: 実践: イシュー駆動でチームメンバー紹介リストを開発しよう

## 🎯 このセクションで学ぶこと

*   イシュー駆動開発の流れを、実践的な演習を通じて体験する。
*   チームメンバー紹介リスト（DBなし、JSONファイル読み込み等の簡易アプリ）を開発する。
*   Git操作とコンフリクト解決に集中する。

---

## 導入：実践演習の目的

このセクションでは、**イシュー駆動開発の流れを体験**します。題材は、**チームメンバー紹介リスト**です。

**特徴**:

*   DBなし、JSONファイル読み込み等の簡易アプリ
*   ロジックがほぼ無い単純な題材
*   **Git操作**とコンフリクト解決に集中

---

## 詳細解説

### 🎯 演習の目標

*   イシューを作成する
*   ブランチを作成する
*   開発する
*   プルリクエストを作成する
*   コードレビューを行う
*   マージする
*   コンフリクトを解決する

---

### 🔧 準備

#### ステップ1: リポジトリを作成

GitHubで新しいリポジトリを作成します。

**リポジトリ名**: `team-member-list`

---

#### ステップ2: ローカルにクローン

```bash
git clone https://github.com/your-username/team-member-list.git
cd team-member-list
```

---

#### ステップ3: 初期ファイルを作成

**`index.html`**

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>チームメンバー紹介</title>
</head>
<body>
    <h1>チームメンバー紹介</h1>
    <div id="members"></div>
    <script src="app.js"></script>
</body>
</html>
```

**`app.js`**

```javascript
// メンバーデータを読み込んで表示
fetch('members.json')
    .then(response => response.json())
    .then(data => {
        const membersDiv = document.getElementById('members');
        data.members.forEach(member => {
            const memberDiv = document.createElement('div');
            memberDiv.innerHTML = `<h2>${member.name}</h2><p>${member.role}</p>`;
            membersDiv.appendChild(memberDiv);
        });
    });
```

**`members.json`**

```json
{
    "members": []
}
```

---

#### ステップ4: GitHubにプッシュ

```bash
git add .
git commit -m "Initial commit"
git push origin main
```

---

### 🚀 演習1: メンバー追加機能の実装

#### ステップ1: イシューを作成

GitHubで新しいイシューを作成します。

**タイトル**: メンバー追加機能の実装

**説明**:

```
## 概要
チームメンバーを追加できる機能を実装する

## タスク
- [ ] members.jsonに自分の情報を追加
- [ ] 表示を確認
```

イシュー番号は`#1`とします。

---

#### ステップ2: ブランチを作成

```bash
git switch main
git pull origin main
git switch -c feature/1-add-member
```

---

#### ステップ3: メンバー情報を追加

**`members.json`**

```json
{
    "members": [
        {
            "name": "田中太郎",
            "role": "フロントエンドエンジニア"
        }
    ]
}
```

---

#### ステップ4: コミット

```bash
git add members.json
git commit -m "Add member: 田中太郎 #1"
git push origin feature/1-add-member
```

---

#### ステップ5: プルリクエストを作成

GitHubでプルリクエストを作成します。

**タイトル**: メンバー追加: 田中太郎 #1

**説明**:

```
## 概要
田中太郎をメンバーに追加しました

Closes #1
```

---

#### ステップ6: マージ

「Merge pull request」ボタンをクリックします。

---

### 🚀 演習2: 別のメンバーを追加（コンフリクトなし）

#### ステップ1: イシューを作成

**タイトル**: メンバー追加: 佐藤花子

イシュー番号は`#2`とします。

---

#### ステップ2: ブランチを作成

```bash
git switch main
git pull origin main
git switch -c feature/2-add-member
```

---

#### ステップ3: メンバー情報を追加

**`members.json`**

```json
{
    "members": [
        {
            "name": "田中太郎",
            "role": "フロントエンドエンジニア"
        },
        {
            "name": "佐藤花子",
            "role": "バックエンドエンジニア"
        }
    ]
}
```

---

#### ステップ4: コミット

```bash
git add members.json
git commit -m "Add member: 佐藤花子 #2"
git push origin feature/2-add-member
```

---

#### ステップ5: プルリクエストを作成

**タイトル**: メンバー追加: 佐藤花子 #2

**説明**:

```
## 概要
佐藤花子をメンバーに追加しました

Closes #2
```

---

#### ステップ6: マージ

「Merge pull request」ボタンをクリックします。

---

### 🚀 演習3: コンフリクトの発生と解決

#### シナリオ

*   Aさんが`feature/3-add-member-a`ブランチで「鈴木一郎」を追加
*   Bさんが`feature/4-add-member-b`ブランチで「高橋次郎」を追加
*   Aさんが先にマージ
*   Bさんがマージしようとすると、コンフリクトが発生

---

#### ステップ1: Aさんがイシューを作成

**タイトル**: メンバー追加: 鈴木一郎

イシュー番号は`#3`とします。

---

#### ステップ2: Aさんがブランチを作成

```bash
git switch main
git pull origin main
git switch -c feature/3-add-member-a
```

---

#### ステップ3: Aさんがメンバー情報を追加

**`members.json`**

```json
{
    "members": [
        {
            "name": "田中太郎",
            "role": "フロントエンドエンジニア"
        },
        {
            "name": "佐藤花子",
            "role": "バックエンドエンジニア"
        },
        {
            "name": "鈴木一郎",
            "role": "デザイナー"
        }
    ]
}
```

---

#### ステップ4: Aさんがコミット

```bash
git add members.json
git commit -m "Add member: 鈴木一郎 #3"
git push origin feature/3-add-member-a
```

---

#### ステップ5: Aさんがプルリクエストを作成してマージ

**タイトル**: メンバー追加: 鈴木一郎 #3

マージします。

---

#### ステップ6: Bさんがイシューを作成

**タイトル**: メンバー追加: 高橋次郎

イシュー番号は`#4`とします。

---

#### ステップ7: Bさんがブランチを作成（Aさんがマージする前）

```bash
git switch main
git pull origin main
git switch -c feature/4-add-member-b
```

---

#### ステップ8: Bさんがメンバー情報を追加

**`members.json`**

```json
{
    "members": [
        {
            "name": "田中太郎",
            "role": "フロントエンドエンジニア"
        },
        {
            "name": "佐藤花子",
            "role": "バックエンドエンジニア"
        },
        {
            "name": "高橋次郎",
            "role": "プロジェクトマネージャー"
        }
    ]
}
```

---

#### ステップ9: Bさんがコミット

```bash
git add members.json
git commit -m "Add member: 高橋次郎 #4"
git push origin feature/4-add-member-b
```

---

#### ステップ10: Bさんがプルリクエストを作成

**タイトル**: メンバー追加: 高橋次郎 #4

---

#### ステップ11: コンフリクトが発生

GitHubで「This branch has conflicts that must be resolved」と表示されます。

---

#### ステップ12: Bさんがコンフリクトを解決

```bash
git switch feature/4-add-member-b
git merge main
```

**実行結果**

```
CONFLICT (content): Merge conflict in members.json
```

---

#### ステップ13: ファイルを編集

**`members.json`**

```json
{
    "members": [
        {
            "name": "田中太郎",
            "role": "フロントエンドエンジニア"
        },
        {
            "name": "佐藤花子",
            "role": "バックエンドエンジニア"
        },
        {
            "name": "鈴木一郎",
            "role": "デザイナー"
        },
        {
            "name": "高橋次郎",
            "role": "プロジェクトマネージャー"
        }
    ]
}
```

---

#### ステップ14: コミット

```bash
git add members.json
git commit -m "Resolve conflict"
git push origin feature/4-add-member-b
```

---

#### ステップ15: マージ

「Merge pull request」ボタンをクリックします。

---

### 💡 TIP: コンフリクトを避ける方法

*   こまめに`main`ブランチをマージする
*   同じファイルを同時に編集しない
*   作業を小さく分割する

---

## ✨ まとめ

このセクションでは、イシュー駆動開発の流れを実践的な演習を通じて体験しました。

*   イシューを作成し、ブランチを作成して開発を進めた。
*   プルリクエストを作成し、マージした。
*   コンフリクトを解決した。

次のセクションでは、コードレビューの基礎について学びます。

---
