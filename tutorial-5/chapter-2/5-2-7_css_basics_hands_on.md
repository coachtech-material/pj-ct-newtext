# Tutorial 5-2-7: CSSの基礎 - ハンズオン演習

## 📝 このセクションの目的

Chapter 2で学んだCSSの基礎知識を実際に手を動かして確認します。Chapter 1で作成した自己紹介ページにスタイルを追加して、見た目を整えましょう。

**学習のポイント**：
- CSSの基本的な書き方を理解できているか
- セレクタを適切に使えるか
- ボックスモデルを理解できているか
- Flexboxで簡単なレイアウトを作れるか

---

## 🎯 演習課題：自己紹介ページにスタイルを追加しよう

### 課題の概要

Chapter 1で作成した`self-introduction.html`に、CSSを使ってスタイルを追加してください。

### 📋 要件

以下の要件を満たすCSSファイル（`style.css`）を作成し、HTMLファイルにリンクしてください。

#### 1. ファイル構成

```
your-project/
├── self-introduction.html
├── style.css
└── landscape.jpg
```

#### 2. HTMLファイルの修正

`self-introduction.html`の`<head>`内に、以下のリンクタグを追加してください：

```html
<link rel="stylesheet" href="style.css">
```

#### 3. CSSの要件

**全体のスタイル**：
- `body`要素に以下を適用：
  - フォントファミリー: `Arial, sans-serif`
  - 背景色: `#f5f5f5`（薄いグレー）
  - 余白: `20px`
  - 行の高さ: `1.6`

**メインタイトル（h1）**：
- 文字色: `#333`（濃いグレー）
- 文字サイズ: `32px`
- 中央揃え
- 下マージン: `30px`

**セクション見出し（h2）**：
- 文字色: `#0066cc`（青）
- 文字サイズ: `24px`
- 下ボーダー: `2px solid #0066cc`
- 下パディング: `10px`
- 下マージン: `20px`

**段落（p）**：
- 文字色: `#555`
- 下マージン: `10px`

**リスト（ul, ol）**：
- 左マージン: `20px`
- 下マージン: `20px`

**リンク（a）**：
- 文字色: `#0066cc`
- 下線なし（`text-decoration: none`）
- ホバー時の文字色: `#003d7a`（濃い青）
- ホバー時に下線を表示

**画像（img）**：
- 最大幅: `100%`
- 高さ: 自動
- 角を丸くする: `8px`
- 影を追加: `0 2px 8px rgba(0,0,0,0.1)`

**コンテンツエリア**：
- クラス名: `container`
- 最大幅: `800px`
- 中央揃え
- 背景色: `#ffffff`（白）
- パディング: `40px`
- 角を丸くする: `10px`
- 影を追加: `0 4px 6px rgba(0,0,0,0.1)`

#### 4. HTMLの修正

`<body>`タグの直下に`<div class="container">`を追加し、すべてのコンテンツをこの中に入れてください。

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: CSSファイルの基本構造

```css
/* セレクタ {
    プロパティ: 値;
} */

body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
}
```

### ヒント2: クラスセレクタ

```css
.container {
    max-width: 800px;
    margin: 0 auto; /* 中央揃え */
}
```

### ヒント3: ホバー効果

```css
a:hover {
    color: #003d7a;
    text-decoration: underline;
}
```

### ヒント4: ボックスシャドウ

```css
img {
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

### ヒント5: ボーダー

```css
h2 {
    border-bottom: 2px solid #0066cc;
}
```

---

## ✅ 完成イメージ

完成すると、以下のような見た目になります：

- 白い背景のカードのようなデザイン
- 青い見出しと下線
- ホバーすると色が変わるリンク
- 影と角丸のある画像
- 読みやすい行間とマージン

---

## 🚀 チャレンジ

基本要件をクリアしたら、以下の追加課題にも挑戦してみましょう。

1. **ボタンスタイル**：リンクをボタンのようなデザインに変更
   - パディング: `10px 20px`
   - 背景色: `#0066cc`
   - 文字色: `#ffffff`
   - 角を丸くする: `5px`

2. **リストのスタイル**：リストアイテムの間隔を調整
   - 各`<li>`に下マージン`10px`を追加

3. **セクション間の余白**：各`<h2>`の上マージンを`40px`に設定して、セクション間を広げる

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### style.css

```css
/* 全体のスタイル */
body {
    font-family: Arial, sans-serif;
    background-color: #f5f5f5;
    margin: 20px;
    line-height: 1.6;
}

/* コンテンツエリア */
.container {
    max-width: 800px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* メインタイトル */
h1 {
    color: #333;
    font-size: 32px;
    text-align: center;
    margin-bottom: 30px;
}

/* セクション見出し */
h2 {
    color: #0066cc;
    font-size: 24px;
    border-bottom: 2px solid #0066cc;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

/* 段落 */
p {
    color: #555;
    margin-bottom: 10px;
}

/* リスト */
ul, ol {
    margin-left: 20px;
    margin-bottom: 20px;
}

/* リンク */
a {
    color: #0066cc;
    text-decoration: none;
}

a:hover {
    color: #003d7a;
    text-decoration: underline;
}

/* 画像 */
img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

### self-introduction.html（修正版）

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>自己紹介 - 山田太郎</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="container">
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
        <img src="landscape.jpg" alt="好きな風景">
    </div>
</body>
</html>
```

---

## 🎓 解説

### ポイント1: CSSファイルのリンク

```html
<link rel="stylesheet" href="style.css">
```

- `<head>`内に記述する
- `rel="stylesheet"`: CSSファイルであることを指定
- `href`: CSSファイルのパス

### ポイント2: ボックスモデル

```css
.container {
    padding: 40px;        /* 内側の余白 */
    margin: 0 auto;       /* 外側の余白（中央揃え） */
    border-radius: 10px;  /* 角を丸くする */
}
```

- `padding`: 要素の内側の余白
- `margin`: 要素の外側の余白
- `margin: 0 auto`: 左右のマージンを自動で均等にして中央揃え

### ポイント3: 色の指定

```css
h1 {
    color: #333;              /* 16進数カラーコード */
    background-color: #f5f5f5; /* 背景色 */
}
```

- `#333`: 濃いグレー（`#333333`の省略形）
- `#f5f5f5`: 薄いグレー
- `#0066cc`: 青

### ポイント4: ボーダー

```css
h2 {
    border-bottom: 2px solid #0066cc;
}
```

- `2px`: ボーダーの太さ
- `solid`: ボーダーのスタイル（実線）
- `#0066cc`: ボーダーの色

### ポイント5: シャドウ

```css
.container {
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
```

- `0`: 水平方向のオフセット
- `4px`: 垂直方向のオフセット
- `6px`: ぼかしの範囲
- `rgba(0,0,0,0.1)`: 影の色（黒の10%透明度）

### ポイント6: ホバー効果

```css
a:hover {
    color: #003d7a;
    text-decoration: underline;
}
```

- `:hover`: マウスを乗せたときのスタイル
- リンクの色を変えて、下線を表示

---

## 🔍 よくある間違い

### 間違い1: CSSファイルのリンク忘れ

```html
<!-- ❌ 間違い（CSSがリンクされていない） -->
<head>
    <title>自己紹介</title>
</head>

<!-- ✅ 正しい -->
<head>
    <title>自己紹介</title>
    <link rel="stylesheet" href="style.css">
</head>
```

### 間違い2: セレクタのスペルミス

```css
/* ❌ 間違い（クラス名が違う） */
.contaner {
    max-width: 800px;
}

/* ✅ 正しい */
.container {
    max-width: 800px;
}
```

### 間違い3: セミコロンの忘れ

```css
/* ❌ 間違い */
h1 {
    color: #333
    font-size: 32px;
}

/* ✅ 正しい */
h1 {
    color: #333;
    font-size: 32px;
}
```

---

## 📚 次のステップ

CSSの基礎をマスターしたら、次はレスポンシブデザインを学びましょう！

Chapter 3では、スマートフォンやタブレットなど、様々なデバイスに対応したデザインの作り方を学びます。

---

## 💪 自己評価チェックリスト

以下の項目ができたかチェックしましょう：

- [ ] CSSファイルを作成し、HTMLにリンクできた
- [ ] bodyやh1、h2などの要素セレクタを使えた
- [ ] クラスセレクタ（.container）を使えた
- [ ] 色を16進数カラーコードで指定できた
- [ ] margin、padding、borderを使えた
- [ ] box-shadowで影を追加できた
- [ ] :hoverでホバー効果を実装できた
- [ ] ブラウザで正しくスタイルが適用されることを確認できた

すべてチェックできたら、Chapter 3に進みましょう！
