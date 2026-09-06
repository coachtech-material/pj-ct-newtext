# 5-1-7: HTMLの基礎 - ハンズオン演習

> 📝 **ハンズオンとは？**: 「ハンズオン（hands-on）」とは、実際に手を動かすセクションです。このチャプターで学んだ知識を、実際に手を動かしながら実践しましょう。

## 📌 このハンズオンについて

Chapter 1で学んだHTMLの基礎知識を実際に手を動かして確認します。要件に従って、自分の力でHTMLファイルを作成してみましょう。

> 🔥 分からないことがあったら、すぐに答えを見るのではなく、過去の教材を見返したり、AIに「質問」したりして、自分の力で実装してみましょう。この段階では、コードそのものをAIに書かせるのはぐっと我慢です。1-1-6でお話しした通り、設計ができる人は「自分の手でコードを書いたことがある人」だからです。

**学習のポイント**：
- HTMLの基本構造を正しく書けるか
- 見出し、段落、リストを適切に使えるか
- リンクと画像を埋め込めるか
- フォーム要素（input、textarea、select、label）を使えるか
- 調べながら進めることで、知識を定着させる

---

## 📁 ディレクトリ構成

このハンズオンでは、「自分で作成する用」と「解答を確認する用」の2つのディレクトリを作成します。

```
~/html-practice/
└── 5-1-7_hands-on/                    ← このハンズオン用のディレクトリ
    ├── self-introduction-practice/    ← 要件を見て自分で作成するディレクトリ
    └── self-introduction-sample/      ← 実践で一緒に作成するディレクトリ
```

| ディレクトリ | 用途 |
|:---|:---|
| `self-introduction-practice/` | 📋 要件を見て、自分の力で作成する |
| `self-introduction-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

---

## 🎯 演習課題：自己紹介ページを作成しよう

### この演習で作るもの

あなた自身の自己紹介ページを作成してください。このページには、以下の要素を含める必要があります。

### 🖼️ 完成イメージ

**自己紹介ページ**

<img alt="5-1-7_1.png" src="https://s3.ap-northeast-1.amazonaws.com/coachtech-lms-bucket-dev/curriculums/images/5-1-7_1.png">

---

### 📋 要件

以下の要件を満たすHTMLファイル（`self-introduction.html`）を`self-introduction-practice/`ディレクトリ内に作成してください。

#### 1. 基本構造
- HTML5の基本構造（`<!DOCTYPE html>`、`<html>`、`<head>`、`<body>`）を正しく記述する
- `<head>`内に、ページタイトル「自己紹介 - あなたの名前」を設定する
- 文字コードは`UTF-8`を指定する

#### 2. ページの内容

**メインタイトル**：
- `<h1>`タグで「自己紹介」というタイトルを表示

**プロフィール**：
- `<h2>`タグで「プロフィール」という見出しを表示
- 以下の情報を`<p>`タグで記述：
  - 名前
  - 年齢
  - 出身地
  - 趣味

**好きなもの**：
- `<h2>`タグで「好きなもの」という見出しを表示
- 好きな食べ物を3つ、`<ul>`（順序なしリスト）で箇条書き

**目標**：
- `<h2>`タグで「今年の目標」という見出しを表示
- 目標を3つ、`<ol>`（順序付きリスト）で番号付きリスト

**リンク**：
- `<h2>`タグで「リンク」という見出しを表示
- あなたのSNSやポートフォリオサイトへのリンクを1つ以上追加
  - リンクテキストは「私のGitHub」や「私のTwitter」など
  - リンクは新しいタブで開くように設定（`target="_blank"`）（5-1-5で学んだ属性です）

**画像**：
- `<h2>`タグで「好きな風景」という見出しを表示
- 好きな風景の画像を1枚表示
  - 画像ファイル名は`landscape.jpg`とする
  - `alt`属性に「好きな風景」という説明を追加
  - 画像の幅は`400px`に設定

**お問い合わせフォーム**：
- `<h2>`タグで「お問い合わせ」という見出しを表示
- `<form>`タグでフォームを作成（`action="/submit"` `method="POST"`）
- 以下の入力フィールドを含める：
  - お名前：`<input type="text">`でテキスト入力欄
  - お問い合わせ種別：`<select>`でドロップダウン（「一般的なお問い合わせ」「ご意見・ご要望」の2つ）
  - お問い合わせ内容：`<textarea>`で複数行テキスト入力欄
  - 送信ボタン：`<button type="submit">`で送信ボタン
- 各入力フィールドには`<label>`タグを関連付ける
- お名前、お問い合わせ内容には`required`属性を付ける

> 💡 **動作確認**: VSCodeで`self-introduction.html`を右クリック →「Finderで表示する」→ ファイルをダブルクリックしてブラウザで開く

#### 3. GitHubでのコード管理

完成した成果物を **GitHubのpublicリポジトリ** で管理します。

- `self-introduction-practice/` ディレクトリの中身を **publicリポジトリ** で管理する
- リポジトリ名は **`self-introduction-practice`** とする
- 下記の雛形をもとに、`README.md` を **自分の言葉で** 作成する
- コミットとpushを完了させる

> 💡 **`practice/` と `sample/` の使い分け**:
> - **`practice/`** が **「提出物」** です。最終的にここにある成果物をGitHubに push します
> - **`sample/`** は **「答え合わせ用」** で、ローカルでの比較確認のみに使います。GitHubには push しません
> - `practice/` で完成できなかった場合は、`sample/` を参考にしながら `practice/` を完成させてから push しましょう（「最終的に動く成果物が残っている」ことが目的です）

> 💡 **なぜpublic？**: あなたの成果物がGitHubのcontribution graph（草）として記録され、フリーランス案件への参画や転職の面談など、**スキルを伝える場面**で有利に働きます。詳しくは Tutorial 4-4-5 を参照してください。

<details>
<summary>📄 README.md の雛形（クリックで展開）</summary>

`self-introduction-practice/README.md` に、以下の雛形をベースに **自分の言葉で** 記載しましょう。

````markdown
# self-introduction-practice

## 概要
COACHTECH 教材 Tutorial 5-1「HTMLの基礎 ハンズオン演習」で作成した成果物です。
（**ここに、何を作ったかを1〜2行で書きましょう**）

## 使用技術
- HTML5
（**他に使ったものがあれば追記してください**）

## 学んだこと
- （**自分の言葉で2〜3項目書きましょう**）
- 
- 

## 動作確認
（**どうやって動かして確認するかを記載してください**）
````

> 💡 **「学んだこと」の書き方の例（参考）**:
> - HTMLの基本構造（DOCTYPE / html / head / body）の役割
> - 見出し（h1〜h2）の使い分けと、段落・リストの使い方
> - フォームの基本構造と、`label` によるアクセシビリティ
>
> 👆 こんな感じで「**自分が理解したこと**」を書きます。コピペではなく、自分で考えて書くことが評価につながります。

任意で以下も追加すると、より評価されやすくなります:
- 詰まったポイントと解決方法
- 画面キャプチャ
- 開発の工夫

</details>

---

## ⚙️ 環境準備（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

ターミナルで以下のコマンドを実行してください。

```bash
# ホームディレクトリに移動
cd ~

# HTML練習用ディレクトリを作成（既に存在する場合はスキップされます）
mkdir -p html-practice

# ハンズオン用ディレクトリを作成
mkdir -p html-practice/5-1-7_hands-on/self-introduction-practice
mkdir -p html-practice/5-1-7_hands-on/self-introduction-sample

# 自分で作成する用のディレクトリに移動
cd html-practice/5-1-7_hands-on/self-introduction-practice

# HTMLファイルを作成
touch self-introduction.html

# VSCodeでプロジェクトを開く
code .
```

**コマンド解説**：

| コマンド | 説明 |
|:---|:---|
| `mkdir -p` | ディレクトリを作成します。`-p`オプションで、親ディレクトリも一緒に作成します |
| `cd` | ディレクトリを移動します |
| `touch` | 空のファイルを作成します |
| `code .` | 現在のディレクトリをVSCodeで開きます |

> ⚠️ **`code .` で「command not found」と表示された場合**
>
> VSCodeのシェルコマンドがインストールされていない可能性があります。以下の手順でインストールしてください。
>
> 1. VSCodeを開く
> 2. `Cmd + Shift + P`（Mac）または `Ctrl + Shift + P`（Windows）でコマンドパレットを開く
> 3. 「Shell Command: Install 'code' command in PATH」と入力して選択する
> 4. インストール完了後、ターミナルを再起動してから、もう一度 `code .` を実行する

> 🚀 **ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: HTMLの基本構造

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ここにタイトル</title>
</head>
<body>
    <!-- ここにコンテンツを書く -->
</body>
</html>
```

### ヒント2: 見出しと段落

```html
<h1>大見出し</h1>
<h2>中見出し</h2>
<p>これは段落です。</p>
```

### ヒント3: リスト

```html
<!-- 順序なしリスト -->
<ul>
    <li>項目1</li>
    <li>項目2</li>
</ul>

<!-- 順序付きリスト -->
<ol>
    <li>項目1</li>
    <li>項目2</li>
</ol>
```

### ヒント4: リンク

```html
<a href="https://example.com" target="_blank">リンクテキスト</a>
```

### ヒント5: 画像

```html
<img src="landscape.jpg" alt="説明" width="400">
```

### ヒント6: フォームの基本構造

```html
<form action="/submit" method="POST">
    <!-- 入力フィールドをここに配置 -->
</form>
```

### ヒント7: テキスト入力とラベル

```html
<label for="name">お名前:</label>
<input type="text" id="name" name="name" required>
```

### ヒント8: ドロップダウン選択

```html
<select name="category">
    <option value="">-- 選択してください --</option>
    <option value="general">一般</option>
</select>
```

### ヒント9: 複数行テキスト入力

```html
<textarea name="message" rows="5"></textarea>
```

### ヒント10: 送信ボタン

```html
<button type="submit">送信する</button>
```

---

## 🏃 実践

ちゃんとできましたか？もし詰まってしまった方や、実装の流れを確認したい方のために、一緒に手を動かしながら作っていきましょう。

> 📌 **注意**: ここからは`self-introduction-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のディレクトリで進めましょう。

---

### ⚙️ 環境準備（実践用プロジェクト）

**実践用のディレクトリ**に移動します。

```bash
# 実践用ディレクトリに移動
cd ~/html-practice/5-1-7_hands-on/self-introduction-sample

# VSCodeでプロジェクトを開く
code .
```

`self-introduction.html`という名前のファイルを作成します。

```bash
touch self-introduction.html
```

---

### 🧠 先輩エンジニアの思考プロセス

先輩エンジニアは要件を以下のように構造化し、実装タスクに落とし込みます：

| Step | やること | 説明 |
|:-----|:---------|:-----|
| 1 | HTML5の基本構造を書く | まず骨組みを作る |
| 2 | タイトルを設定する | `<head>`内に必要な情報を記述 |
| 3 | メインタイトルを追加する | 大きな構造（`<h1>`）から作る |
| 4 | プロフィールセクションを追加する | 見出しと段落で情報を表示 |
| 5 | 好きなものセクションを追加する | 順序なしリスト（`<ul>`）を使う |
| 6 | 目標セクションを追加する | 順序付きリスト（`<ol>`）を使う |
| 7 | リンクセクションを追加する | `<a>`タグでリンクを作成 |
| 8 | 画像セクションを追加する | `<img>`タグで画像を表示 |
| 9 | お問い合わせフォームを追加する | `<form>`と各種入力要素を使う |
| 10 | ブラウザで確認する | 意図通りに表示されるかチェック |

この順番で作ることで、「どこまでできているか」が明確になり、エラーが出ても原因を特定しやすくなります。

---

### 📝 ステップバイステップで実装

#### ステップ1: HTML5の基本構造を書く

VSCodeのエクスプローラーに`self-introduction.html`が表示されるので、クリックして開いてください。

**何を考えているか**：
- 「まずはHTMLの土台を作ろう」
- 「VSCodeのEmmet機能を使えば、一瞬で雛形が作れるな」

**Emmetで雛形を生成**：

ファイルの1行目に `!` と入力し、`Tab`キーを押してください。

```
! + Tab
```

すると、以下のようなHTML5の雛形が自動生成されます：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>

</body>
</html>
```

> 💡 **Emmetとは？**: VSCodeに標準搭載されている機能で、短い記法からHTMLやCSSのコードを自動生成できます。`!`はHTML5の雛形を生成するショートカットです。

**日本語ページ用に修正**：

`lang="en"`を`lang="ja"`に変更します：

```html
<html lang="ja">
```

**コードリーディング（生成されたコードの解説）**：

```html
<!DOCTYPE html>
```
→ これはHTML5の文書であることをブラウザに伝える宣言です。必ず最初に書きます。

```html
<html lang="ja">
```
→ HTMLドキュメント全体を囲むタグです。`lang="ja"`で日本語のページであることを示します。

```html
<head>
```
→ ページの設定情報（メタデータ）を記述する部分の開始タグです。

```html
    <meta charset="UTF-8">
```
→ 文字コードをUTF-8に設定します。これがないと日本語が文字化けする可能性があります。

```html
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
```
→ スマートフォンやタブレットでの表示を最適化するための設定です。レスポンシブデザインに必要な記述です。

```html
    <title>Document</title>
```
→ ブラウザのタブに表示されるタイトルを設定します。次のステップで変更します。

```html
</head>
```
→ head部分の終了タグです。

```html
<body>

</body>
```
→ 実際にブラウザに表示される内容を書く部分です。ここにコンテンツを追加していきます。

```html
</html>
```
→ HTMLドキュメント全体の終了タグです。

---

#### ステップ2: タイトルを設定する

**何を考えているか**：
- 「ブラウザのタブに表示されるタイトルを設定しよう」
- 「自己紹介ページだから、『自己紹介 - 自分の名前』にしよう」

```html
<title>自己紹介 - 山田太郎</title>
```

**コードリーディング**：

```html
<title>自己紹介 - 山田太郎</title>
```
→ `<title>`タグの中身を「自己紹介 - 山田太郎」に変更しました。これでブラウザのタブに「自己紹介 - 山田太郎」と表示されます。

---

#### ステップ3: メインタイトルを追加する

**何を考えているか**：
- 「ページ全体のタイトルは`<h1>`を使うんだったな」
- 「`<h1>`はページに1つだけが基本」

```html
<body>
    <h1>自己紹介</h1>
</body>
```

**コードリーディング**：

```html
    <h1>自己紹介</h1>
```
→ `<h1>`タグでページ全体のメインタイトル「自己紹介」を表示します。`<h1>`は最も大きな見出しで、ページに1つだけ使うのが推奨されます。

---

#### ステップ4: プロフィールセクションを追加する

**何を考えているか**：
- 「プロフィールという見出しは`<h2>`を使おう」
- 「名前、年齢、出身地、趣味は、それぞれ`<p>`タグで段落にしよう」

```html
<body>
    <h1>自己紹介</h1>

    <h2>プロフィール</h2>
    <p>名前: 山田太郎</p>
    <p>年齢: 25歳</p>
    <p>出身地: 東京都</p>
    <p>趣味: プログラミング、読書</p>
</body>
```

**コードリーディング**：

```html
    <h2>プロフィール</h2>
```
→ `<h2>`タグで「プロフィール」という中見出しを表示します。`<h1>`の次の階層の見出しです。

```html
    <p>名前: 山田太郎</p>
```
→ `<p>`タグで段落を作成し、名前を表示します。

```html
    <p>年齢: 25歳</p>
    <p>出身地: 東京都</p>
    <p>趣味: プログラミング、読書</p>
```
→ 同様に、年齢、出身地、趣味もそれぞれ`<p>`タグで段落として表示します。

---

#### ステップ5: 好きなものセクションを追加する（順序なしリスト）

**何を考えているか**：
- 「好きな食べ物は順序が重要じゃないから、`<ul>`（順序なしリスト）を使おう」
- 「各項目は`<li>`タグで囲む」

```html
    <h2>好きなもの</h2>
    <ul>
        <li>ラーメン</li>
        <li>カレー</li>
        <li>寿司</li>
    </ul>
```

**コードリーディング**：

```html
    <h2>好きなもの</h2>
```
→ 「好きなもの」という見出しを`<h2>`で表示します。

```html
    <ul>
```
→ 順序なしリスト（Unordered List）の開始タグです。箇条書きで表示されます。

```html
        <li>ラーメン</li>
        <li>カレー</li>
        <li>寿司</li>
```
→ `<li>`タグ（List Item）で各項目を記述します。ブラウザでは「・ラーメン」「・カレー」「・寿司」のように表示されます。

```html
    </ul>
```
→ 順序なしリストの終了タグです。

---

#### ステップ6: 目標セクションを追加する（順序付きリスト）

**何を考えているか**：
- 「目標は優先順位があるから、`<ol>`（順序付きリスト）を使おう」
- 「番号が自動で振られるから便利」

```html
    <h2>今年の目標</h2>
    <ol>
        <li>Laravelをマスターする</li>
        <li>毎日コードを書く</li>
        <li>ポートフォリオを作成する</li>
    </ol>
```

**コードリーディング**：

```html
    <h2>今年の目標</h2>
```
→ 「今年の目標」という見出しを表示します。

```html
    <ol>
```
→ 順序付きリスト（Ordered List）の開始タグです。番号付きで表示されます。

```html
        <li>Laravelをマスターする</li>
        <li>毎日コードを書く</li>
        <li>ポートフォリオを作成する</li>
```
→ 各目標を`<li>`タグで記述します。ブラウザでは「1. Laravelをマスターする」「2. 毎日コードを書く」「3. ポートフォリオを作成する」のように番号付きで表示されます。

```html
    </ol>
```
→ 順序付きリストの終了タグです。

---

#### ステップ7: リンクセクションを追加する

**何を考えているか**：
- 「リンクは`<a>`タグを使う」
- 「新しいタブで開くには`target="_blank"`を追加する」

```html
    <h2>リンク</h2>
    <a href="https://github.com/yamada-taro" target="_blank">私のGitHub</a>
```

**コードリーディング**：

```html
    <h2>リンク</h2>
```
→ 「リンク」という見出しを表示します。

```html
    <a href="https://github.com/yamada-taro" target="_blank">私のGitHub</a>
```
→ `<a>`タグでリンクを作成します。
- `href="https://github.com/yamada-taro"`: リンク先のURLを指定します
- `target="_blank"`: 新しいタブでリンクを開くように指定します
- `私のGitHub`: クリックできるリンクテキストです

---

#### ステップ8: 画像セクションを追加する

**何を考えているか**：
- 「画像は`<img>`タグを使う」
- 「`alt`属性は必須（アクセシビリティのため）」
- 「幅は`width`属性で指定する」

```html
    <h2>好きな風景</h2>
    <img src="landscape.jpg" alt="好きな風景" width="400">
```

**コードリーディング**：

```html
    <h2>好きな風景</h2>
```
→ 「好きな風景」という見出しを表示します。

```html
    <img src="landscape.jpg" alt="好きな風景" width="400">
```
→ `<img>`タグで画像を表示します。
- `src="landscape.jpg"`: 表示する画像ファイルのパスを指定します
- `alt="好きな風景"`: 画像が表示されない場合の代替テキストです（スクリーンリーダーでも読み上げられます）
- `width="400"`: 画像の幅を400ピクセルに設定します

**注意**: `<img>`タグは終了タグが不要です（自己完結型タグ）。

---

#### ステップ9: お問い合わせフォームセクションを追加する

**何を考えているか**：
- 「フォームは`<form>`タグで囲む」
- 「各入力フィールドには`<label>`を関連付ける（アクセシビリティのため）」
- 「必須項目には`required`属性を付ける」

```html
    <h2>お問い合わせ</h2>
    <form action="/submit" method="POST">
        <div>
            <label for="contact-name">お名前:</label>
            <input type="text" id="contact-name" name="name" required>
        </div>
        <div>
            <label for="contact-category">お問い合わせ種別:</label>
            <select id="contact-category" name="category">
                <option value="">-- 選択してください --</option>
                <option value="general">一般的なお問い合わせ</option>
                <option value="feedback">ご意見・ご要望</option>
            </select>
        </div>
        <div>
            <label for="contact-message">お問い合わせ内容:</label>
            <textarea id="contact-message" name="message" rows="5" required></textarea>
        </div>
        <div>
            <button type="submit">送信する</button>
        </div>
    </form>
```

**コードリーディング**：

```html
    <form action="/submit" method="POST">
```
→ `<form>`タグでフォーム全体を囲みます。
- `action="/submit"`: フォームデータの送信先を指定します
- `method="POST"`: データをPOSTメソッドで送信します

```html
        <label for="contact-name">お名前:</label>
        <input type="text" id="contact-name" name="name" required>
```
→ `<label>`の`for`属性と`<input>`の`id`属性を同じ値にすることで、ラベルと入力フィールドを関連付けます。`required`属性で必須項目にします。

```html
        <select id="contact-category" name="category">
            <option value="">-- 選択してください --</option>
            <option value="general">一般的なお問い合わせ</option>
        </select>
```
→ `<select>`タグでドロップダウンリストを作成します。`<option>`タグで各選択肢を定義します。

```html
        <textarea id="contact-message" name="message" rows="5" required></textarea>
```
→ `<textarea>`タグで複数行のテキスト入力欄を作成します。`rows="5"`で表示行数を指定します。

```html
        <button type="submit">送信する</button>
```
→ `<button>`タグで送信ボタンを作成します。`type="submit"`でフォーム送信用のボタンになります。

---

#### ステップ10: ブラウザで確認する

**何を考えているか**：
- 「ファイルを保存して、ブラウザで開いてみよう」
- 「意図通りに表示されているか確認しよう」

ファイルを保存したら、ブラウザで開いて確認します。

**ブラウザでファイルを開く方法**：

1. VSCodeのエクスプローラーで`self-introduction.html`を右クリック
2. 「Finderで表示する」を選択（Finderでファイルの場所が開きます）
3. Finderで`self-introduction.html`をダブルクリック

ブラウザが起動し、作成したHTMLページが表示されます。以下を確認しましょう：

- タイトルがブラウザのタブに表示されているか
- 見出しが正しい階層で表示されているか
- リストが箇条書き・番号付きで表示されているか
- リンクがクリックできるか、新しいタブで開くか
- 画像が表示されているか（画像ファイルが同じフォルダにある場合）
- フォームの各フィールドに入力できるか
- ラベルをクリックするとフィールドにフォーカスが当たるか
- 必須項目を空にして送信しようとすると警告が出るか

> 💡 **注意**: 今の段階では、「送信する」ボタンを押しても、実際にはデータはどこにも送られません（エラーページが表示されるかもしれません）。データを受け取って処理するには、サーバーサイドのプログラム（PHPなど）が必要です。これは、後のチュートリアルで学びます。

---

### ✨ 完成！

これで自己紹介ページが完成しました！段階的に作ることで、どこまでできているかが明確になり、エラーが出ても原因を特定しやすくなります。

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### self-introduction.html

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自己紹介 - 山田太郎</title>
</head>
<body>
    <!-- メインタイトル -->
    <h1>自己紹介</h1>

    <!-- プロフィール -->
    <h2>プロフィール</h2>
    <p>名前: 山田太郎</p>
    <p>年齢: 25歳</p>
    <p>出身地: 東京都</p>
    <p>趣味: プログラミング、読書</p>

    <!-- 好きなもの -->
    <h2>好きなもの</h2>
    <ul>
        <li>ラーメン</li>
        <li>カレー</li>
        <li>寿司</li>
    </ul>

    <!-- 今年の目標 -->
    <h2>今年の目標</h2>
    <ol>
        <li>Laravelをマスターする</li>
        <li>毎日コードを書く</li>
        <li>ポートフォリオを作成する</li>
    </ol>

    <!-- リンク -->
    <h2>リンク</h2>
    <a href="https://github.com/yamada-taro" target="_blank">私のGitHub</a>

    <!-- 好きな風景 -->
    <h2>好きな風景</h2>
    <img src="landscape.jpg" alt="好きな風景" width="400">

    <!-- お問い合わせフォーム -->
    <h2>お問い合わせ</h2>
    <form action="/submit" method="POST">
        <div>
            <label for="contact-name">お名前:</label>
            <input type="text" id="contact-name" name="name" required>
        </div>
        <div>
            <label for="contact-category">お問い合わせ種別:</label>
            <select id="contact-category" name="category">
                <option value="">-- 選択してください --</option>
                <option value="general">一般的なお問い合わせ</option>
                <option value="feedback">ご意見・ご要望</option>
            </select>
        </div>
        <div>
            <label for="contact-message">お問い合わせ内容:</label>
            <textarea id="contact-message" name="message" rows="5" required></textarea>
        </div>
        <div>
            <button type="submit">送信する</button>
        </div>
    </form>
</body>
</html>
```

---

---

## 🔍 よくある間違い

### 間違い1: タグの閉じ忘れ

```html
<!-- ❌ 間違い -->
<p>これは段落です

<!-- ✅ 正しい -->
<p>これは段落です</p>
```

### 間違い2: 見出しの順序

```html
<!-- ❌ 間違い（h1の後にいきなりh3） -->
<h1>タイトル</h1>
<h3>見出し</h3>

<!-- ✅ 正しい -->
<h1>タイトル</h1>
<h2>見出し</h2>
```

### 間違い3: 画像のalt属性の省略

```html
<!-- ❌ 間違い -->
<img src="landscape.jpg">

<!-- ✅ 正しい -->
<img src="landscape.jpg" alt="好きな風景">
```
---

## 📤 GitHubに push しよう

ハンズオンが完成したら、成果物をGitHubのpublicリポジトリに公開します。Tutorial 4 で学んだ手順を使って push しましょう。

> 💡 **初回なので丁寧に解説します**。次回以降のハンズオンでは、ここで覚えた手順を活用してください。

### Step 1: GitHubでリポジトリを作成

GitHubにログインし、新しいリポジトリを作成します。

1. 右上の「+」→「New repository」をクリック
2. **Repository name** に `self-introduction-practice` を入力
3. **Public** を選択
4. 「Initialize this repository with」のチェックは **すべて外す**（Tutorial 4-4-1 で学んだ通り）
5. 「Create repository」をクリック

### Step 2: README.md を作成

`practice/` ディレクトリに `README.md` を作成します。

```bash
cd ~/html-practice/5-1-7_hands-on/self-introduction-practice
touch README.md
```

VSCodeで `README.md` を開き、要件3の雛形をベースに **自分の言葉で** 内容を記載しましょう。

### Step 3: ローカルでGit初期化＆commit

```bash
# practice ディレクトリにいることを確認
cd ~/html-practice/5-1-7_hands-on/self-introduction-practice

# Git の初期化
git init

# ファイルをステージング
git add .

# 初回コミット
git commit -m "first commit"
```

### Step 4: リモートと接続して push

GitHub のリポジトリ作成後のページに表示されているコマンドを参考に、リモートと接続します。

```bash
# リモートを設定（URLは自分のリポジトリのものに置き換える）
git remote add origin <あなたのリポジトリのURL>

# ブランチ名を main に統一（必要に応じて）
git branch -M main

# push
git push -u origin main
```

> ⚠️ **詰まったときは**: Tutorial 4-4-2「ローカルとリモートの接続」、4-4-3「変更のアップロード」を見直してみましょう。

### Step 5: GitHubで確認

ブラウザで自分のリポジトリページを開き、`self-introduction.html` と `README.md` が表示されていることを確認します。

---

## ✅ 完成チェックリスト

ここまでで、以下が完了していることを確認しましょう。

- [ ] 要件1〜2を満たして、`self-introduction.html` が正しく動く状態になっている
- [ ] ブラウザで動作確認した
- [ ] GitHub に `self-introduction-practice` リポジトリを作成した（public）
- [ ] 要件3の雛形を参考に `README.md` を **自分の言葉で** 作成した
- [ ] `commit` と `push` を完了して、GitHubに反映されている

> 💡 **これ以降のハンズオンでも README を作ろう**: ここで使った雛形のパターンは、これからのハンズオンでも使っていきます（技術スタックや学んだことの中身は、各ハンズオンの内容に合わせて書き換えてください）。あなたの学習履歴として残り、面談時にも見せられる資産になります。

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ HTMLの基本構造を正しく書ける
- ✅ 見出し、段落、リストを適切に使える
- ✅ リンクと画像を埋め込めるか
- ✅ フォーム要素（input、textarea、select、label）を使える
- ✅ 調べながら進めることで、知識を定着させる

引き続き、次のセクションも頑張りましょう！

---
