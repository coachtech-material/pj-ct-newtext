# 12-4-1: GitHubプロフィールを整えよう

## 🎯 このセクションで学ぶこと

*   GitHub Profile README とは何かを理解する。
*   自分のユーザー名と同じ名前のリポジトリで Profile README を作成する方法を学ぶ。
*   学習成果物のリンクを Profile README にまとめる。
*   （オプション）contribution stats バッジで自分の活動を可視化する。

---

## 導入

Tutorial 5〜11 のハンズオンを通して、あなたは GitHub に **20個ほどの成果物リポジトリ** を作ってきました。これらは、あなたが学習を続けてきた証であり、フリーランス案件への参画や転職の面談など、**スキルを伝える場面** で強力な武器になります。

ただし、リポジトリが並んでいるだけでは、はじめて訪れた人はどれを見ればいいか迷ってしまいます。そこで、自分のGitHubプロフィールページの「顔」となる **Profile README** を作成して、あなたの自己紹介と成果物リストをまとめましょう。

---

## 詳細解説

### 🏠 GitHub Profile README とは

GitHubには、**自分のユーザー名と同じ名前のリポジトリ** を作ると、その中の `README.md` がプロフィールページの最上部に表示される、という特殊な仕組みがあります。これを **Profile README** と呼びます。

例えば、ユーザー名が `yamada-taro` なら、`yamada-taro/yamada-taro` というリポジトリを作り、その中に `README.md` を置きます。すると、 `https://github.com/yamada-taro` を訪れた人の目に、最初に飛び込んでくるのがこの README です。

> 💡 **「ユーザー名と同じ名前のリポジトリ」がポイント**: 一文字でも違うと普通のリポジトリ扱いになり、プロフィールには表示されません。

---

### 📝 Profile README の作成手順

#### Step 1: 特殊リポジトリを作成

GitHubで新しいリポジトリを作成します。

1. 右上の「+」→「New repository」をクリック
2. **Repository name** に **自分のGitHubユーザー名** を入力（例: `yamada-taro`）
3. ⚠️ **特殊な仕組みのお知らせ**: ユーザー名と同じ名前を入れると、GitHub が「Special repository」として認識し、「You found a secret!」のような確認メッセージが表示されます。これは「OK、Profile READMEを作る」というサインです
4. **Public** を選択
5. **Initialize this repository with: Add a README file** に **チェック**（今回はGitHub側で初期 README を作ってもらいます）
6. 「Create repository」をクリック

#### Step 2: README.md を編集

Profile README は **マークダウン** で書きます。以下の雛形を **自分の言葉でカスタマイズ** しましょう。

````markdown
# こんにちは、〇〇です 👋

## 🎓 学習中

COACHTECH でフルスタックWeb開発を学習中です。
PHP / Laravel を中心に、HTML / CSS / SQL なども学んでいます。

## 🛠️ 使える技術

- **バックエンド**: PHP, Laravel
- **フロントエンド**: HTML5, CSS, Blade
- **データベース**: MySQL
- **その他**: Docker, Git/GitHub

## 📂 学習成果物（COACHTECH ハンズオン）

### Tutorial 5: HTMLの基礎
- [self-introduction-practice](https://github.com/<あなたのユーザー名>/self-introduction-practice) — 自己紹介ページ

### Tutorial 7: PHPの基礎
- [php-basics-practice](https://github.com/<あなたのユーザー名>/php-basics-practice) — 商品価格計算プログラム
- [php-control-practice](https://github.com/<あなたのユーザー名>/php-control-practice) — 成績判定プログラム
- [php-oop-practice](https://github.com/<あなたのユーザー名>/php-oop-practice) — オブジェクト指向の実装
- [php-form-practice](https://github.com/<あなたのユーザー名>/php-form-practice) — フォームとデータ受け渡し

### Tutorial 9: Laravelの基礎
- [setup-app-practice](https://github.com/<あなたのユーザー名>/setup-app-practice) — Laravel環境構築
- [profile-app-practice](https://github.com/<あなたのユーザー名>/profile-app-practice) — Laravelの基本フロー
- [blade-app-practice](https://github.com/<あなたのユーザー名>/blade-app-practice) — Bladeテンプレート
- [database-app-practice](https://github.com/<あなたのユーザー名>/database-app-practice) — DB操作
- [eloquent-app-practice](https://github.com/<あなたのユーザー名>/eloquent-app-practice) — Eloquent ORM
- [relation-app-practice](https://github.com/<あなたのユーザー名>/relation-app-practice) — リレーション
- [validation-app-practice](https://github.com/<あなたのユーザー名>/validation-app-practice) — バリデーション

### Tutorial 10: Laravel 応用
- [auth-app-practice](https://github.com/<あなたのユーザー名>/auth-app-practice) — 認証機能
- [middleware-app-practice](https://github.com/<あなたのユーザー名>/middleware-app-practice) — ミドルウェア
- [authorization-app-practice](https://github.com/<あなたのユーザー名>/authorization-app-practice) — 認可機能
- [debug-app-practice](https://github.com/<あなたのユーザー名>/debug-app-practice) — デバッグ
- [test-app-practice](https://github.com/<あなたのユーザー名>/test-app-practice) — テスト
- [security-app-practice](https://github.com/<あなたのユーザー名>/security-app-practice) — Webセキュリティ

### Tutorial 11: API開発
- [api-setup-practice](https://github.com/<あなたのユーザー名>/api-setup-practice) — API開発環境
- [task-api-practice](https://github.com/<あなたのユーザー名>/task-api-practice) — タスク管理APIのCRUD実装

## 📫 連絡先
- Email: your-email@example.com
- Twitter: [@your_twitter](https://twitter.com/your_twitter)
````

> 💡 **学習成果物リストの作り方**: Tutorial 5〜11 で push したリポジトリへのリンクを、Tutorial ごとにまとめておきましょう。リストが長くなりすぎるなら、Tutorial 9〜10 を「Laravel系」とひとまとめにするなど工夫しても良いです。

#### Step 3: 自分の言葉でカスタマイズ

雛形をそのままコピーするのではなく、**自分の言葉で書き換える** ことが大事です。

- **興味のある分野** を一言（「Webサービスを作るのが楽しいです」「ユーザー体験を考えるのが好きです」など）
- **これから挑戦したいこと** を一行
- **趣味や個性** を少しだけ（読み手に「人柄」が伝わると、面談での話題のきっかけになります）

#### Step 4: commit & push

GitHubのWeb上で README を直接編集する場合は、編集後「Commit changes」をクリックするだけで反映されます。

ローカルで作業する場合は、Tutorial 4 で学んだ手順で push しましょう。

#### Step 5: プロフィールページで確認

ブラウザで `https://github.com/<あなたのユーザー名>` にアクセスし、README がページの最上部に表示されていることを確認します。

---

### 🎨 (オプション) contribution stats バッジで彩りを加える

Profile README には、外部サービスを使って「自分のGitHub活動を可視化するバッジ」を貼ることもできます。

> 💡 **オプション扱い**: ここからは必須ではありません。「興味があれば」程度の温度感で読んでください。

**主な無料サービス**:

| サービス | 内容 | リンク |
|:--------|:-----|:-------|
| github-readme-stats | コード言語の比率やコミット数などを画像化 | https://github.com/anuraghazra/github-readme-stats |
| github-readme-streak-stats | 連続コミットの記録（ストリーク）を画像化 | https://github.com/DenverCoder1/github-readme-streak-stats |

**使い方**: ログイン不要で、README に `<img>` タグや markdown 画像記法を貼るだけです。

```markdown
## 📊 GitHubの活動

![Your stats](https://github-readme-stats.vercel.app/api?username=<あなたのユーザー名>&show_icons=true&theme=default)

![Your streak](https://github-readme-streak-stats.herokuapp.com/?user=<あなたのユーザー名>&theme=default)
```

> ⚠️ **過剰な装飾に注意**: バッジを並べすぎると、逆に「派手にしすぎ」「内容のなさを隠している」と見られることもあります。**自分のGitHub活動を可視化する** 程度の温度感で、2〜3個までに留めるのがおすすめです。

---

## ✅ 完成チェックリスト

- [ ] GitHubに `<あなたのユーザー名>/<あなたのユーザー名>` リポジトリを作成した
- [ ] `README.md` に自己紹介・使える技術・学習成果物リストを記載した
- [ ] 自分の言葉で内容を書いた（雛形そのままになっていない）
- [ ] プロフィールページ（`https://github.com/<あなたのユーザー名>`）の最上部に README が表示されている

---

## ✨ まとめ

このセクションでは、GitHub Profile README を作成して、自分の学習成果をプロフィールに集約しました。

*   **Profile README の正体**: ユーザー名と同じ名前のリポジトリで作る、プロフィール最上部に表示される「自己紹介ページ」
*   **コアの3要素**: 自己紹介 / 使える技術 / 学習成果物リスト
*   **大事なこと**: 雛形通りではなく、**自分の言葉で** 書く。読み手に「人柄」が伝わるとさらに良い
*   **オプション**: contribution stats バッジで活動を可視化（やりすぎ注意）

これで、Tutorial 12「チーム開発で重要なGitとGitHubの実践的な使い方」の全Chapterが完了です。学習を続ける限り、Profile README も成長させていきましょう。お疲れ様でした！

---
