# Tutorial 5-4-3: Tailwind CSS - ハンズオン演習

## 📝 このセクションの目的

Chapter 4で学んだTailwind CSSの知識を実際に手を動かして確認します。ユーティリティクラスを使って、効率的にスタイリングする方法を体験しましょう。

**学習のポイント**：
- Tailwind CSSのユーティリティクラスを使えるか
- レスポンシブデザインをTailwindで実装できるか
- カスタムCSSとTailwindを使い分けられるか

---

## 🎯 演習課題：Tailwind CSSで自己紹介ページを作り直そう

### 課題の概要

これまで作成してきた自己紹介ページを、Tailwind CSSを使って作り直してください。カスタムCSSファイル（style.css）は使わず、Tailwind CSSのユーティリティクラスのみで実装します。

### 📋 要件

以下の要件を満たすHTMLファイル（`self-introduction-tailwind.html`）を作成してください。

#### 1. Tailwind CSSの読み込み

`<head>`内に、Tailwind CSSのCDNリンクを追加してください：

```html
<script src="https://cdn.tailwindcss.com"></script>
```

#### 2. レイアウトの要件

**全体のスタイル**：
- `body`要素：
  - 背景色: `bg-gray-100`（薄いグレー）
  - パディング: `p-5`
  - フォント: デフォルト

**コンテンツエリア（containerクラス）**：
- 最大幅: `max-w-3xl`（約800px）
- 中央揃え: `mx-auto`
- 背景色: `bg-white`（白）
- パディング: `p-10`
- 角を丸くする: `rounded-lg`
- 影: `shadow-lg`

#### 3. テキストのスタイル

**メインタイトル（h1）**：
- 文字色: `text-gray-800`
- 文字サイズ: `text-4xl`
- フォントの太さ: `font-bold`
- 中央揃え: `text-center`
- 下マージン: `mb-8`

**セクション見出し（h2）**：
- 文字色: `text-blue-600`
- 文字サイズ: `text-2xl`
- フォントの太さ: `font-semibold`
- 下ボーダー: `border-b-2 border-blue-600`
- 下パディング: `pb-2`
- 下マージン: `mb-4`
- 上マージン: `mt-8`（最初のh2以外）

**段落（p）**：
- 文字色: `text-gray-600`
- 下マージン: `mb-2`

#### 4. リストのスタイル

**順序なしリスト（ul）**：
- リストスタイル: `list-disc`
- 左マージン: `ml-5`
- 下マージン: `mb-4`

**順序付きリスト（ol）**：
- リストスタイル: `list-decimal`
- 左マージン: `ml-5`
- 下マージン: `mb-4`

**リストアイテム（li）**：
- 文字色: `text-gray-600`
- 下マージン: `mb-2`

#### 5. リンクのスタイル

**リンク（a）**：
- 文字色: `text-blue-600`
- ホバー時の文字色: `hover:text-blue-800`
- 下線: `underline`

#### 6. 画像のスタイル

**画像（img）**：
- 最大幅: `max-w-full`
- 高さ: `h-auto`
- 角を丸くする: `rounded-lg`
- 影: `shadow-md`

#### 7. レスポンシブ対応

**スマートフォン（デフォルト）**：
- コンテンツエリアのパディング: `p-5`
- h1のフォントサイズ: `text-2xl`
- h2のフォントサイズ: `text-xl`

**タブレット以上（md:）**：
- コンテンツエリアのパディング: `md:p-8`
- h1のフォントサイズ: `md:text-3xl`
- h2のフォントサイズ: `md:text-2xl`

**デスクトップ（lg:）**：
- コンテンツエリアのパディング: `lg:p-10`
- h1のフォントサイズ: `lg:text-4xl`

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: Tailwind CSSのクラスの組み合わせ

```html
<div class="max-w-3xl mx-auto bg-white p-10 rounded-lg shadow-lg">
    <!-- コンテンツ -->
</div>
```

### ヒント2: レスポンシブクラス

```html
<h1 class="text-2xl md:text-3xl lg:text-4xl">
    タイトル
</h1>
```

- `text-2xl`: デフォルト（スマホ）
- `md:text-3xl`: タブレット以上
- `lg:text-4xl`: デスクトップ

### ヒント3: ホバー効果

```html
<a href="#" class="text-blue-600 hover:text-blue-800 underline">
    リンク
</a>
```

### ヒント4: マージンの調整

```html
<h2 class="mt-8 mb-4">見出し</h2>
```

- `mt-8`: 上マージン
- `mb-4`: 下マージン

---

## ✅ 完成イメージ

完成すると、以下のような見た目になります：

- 白い背景のカードデザイン
- 青い見出しと下線
- レスポンシブ対応（スマホ、タブレット、デスクトップ）
- ホバーすると色が変わるリンク
- 影と角丸のある画像

---

## 🚀 チャレンジ

基本要件をクリアしたら、以下の追加課題にも挑戦してみましょう。

1. **ボタンスタイル**：リンクをボタンのようなデザインに変更
   - クラス: `inline-block bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition`

2. **グリッドレイアウト**：好きな風景の画像を3枚並べて、グリッドレイアウトで表示
   - クラス: `grid grid-cols-1 md:grid-cols-3 gap-4`

3. **ダークモード**：Tailwindのダークモードクラスを使って、ダークテーマを追加

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### self-introduction-tailwind.html

```html
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>自己紹介 - 山田太郎</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 p-5">
    <div class="max-w-3xl mx-auto bg-white p-5 md:p-8 lg:p-10 rounded-lg shadow-lg">
        <!-- メインタイトル -->
        <h1 class="text-2xl md:text-3xl lg:text-4xl font-bold text-gray-800 text-center mb-8">
            自己紹介
        </h1>

        <!-- プロフィール -->
        <h2 class="text-xl md:text-2xl font-semibold text-blue-600 border-b-2 border-blue-600 pb-2 mb-4">
            プロフィール
        </h2>
        <p class="text-gray-600 mb-2">名前: 山田太郎</p>
        <p class="text-gray-600 mb-2">年齢: 25歳</p>
        <p class="text-gray-600 mb-2">出身地: 東京都</p>
        <p class="text-gray-600 mb-2">趣味: プログラミング、読書</p>

        <!-- 好きなもの -->
        <h2 class="text-xl md:text-2xl font-semibold text-blue-600 border-b-2 border-blue-600 pb-2 mb-4 mt-8">
            好きなもの
        </h2>
        <ul class="list-disc ml-5 mb-4">
            <li class="text-gray-600 mb-2">ラーメン</li>
            <li class="text-gray-600 mb-2">カレー</li>
            <li class="text-gray-600 mb-2">寿司</li>
        </ul>

        <!-- 今年の目標 -->
        <h2 class="text-xl md:text-2xl font-semibold text-blue-600 border-b-2 border-blue-600 pb-2 mb-4 mt-8">
            今年の目標
        </h2>
        <ol class="list-decimal ml-5 mb-4">
            <li class="text-gray-600 mb-2">Laravelをマスターする</li>
            <li class="text-gray-600 mb-2">毎日コードを書く</li>
            <li class="text-gray-600 mb-2">ポートフォリオを作成する</li>
        </ol>

        <!-- リンク -->
        <h2 class="text-xl md:text-2xl font-semibold text-blue-600 border-b-2 border-blue-600 pb-2 mb-4 mt-8">
            リンク
        </h2>
        <a href="https://github.com/yamada-taro" target="_blank" class="text-blue-600 hover:text-blue-800 underline">
            私のGitHub
        </a>

        <!-- 好きな風景 -->
        <h2 class="text-xl md:text-2xl font-semibold text-blue-600 border-b-2 border-blue-600 pb-2 mb-4 mt-8">
            好きな風景
        </h2>
        <img src="landscape.jpg" alt="好きな風景" class="max-w-full h-auto rounded-lg shadow-md">
    </div>
</body>
</html>
```

---

## 🎓 解説

### ポイント1: Tailwind CSSのCDN読み込み

```html
<script src="https://cdn.tailwindcss.com"></script>
```

- `<head>`内に記述する
- CDN版は開発用で、本番環境では別の方法を推奨
- カスタムCSSファイルは不要

### ポイント2: ユーティリティクラスの組み合わせ

```html
<div class="max-w-3xl mx-auto bg-white p-10 rounded-lg shadow-lg">
```

- `max-w-3xl`: 最大幅を約800pxに制限
- `mx-auto`: 左右のマージンを自動で中央揃え
- `bg-white`: 背景色を白に
- `p-10`: パディングを2.5rem（40px）に
- `rounded-lg`: 角を大きく丸くする
- `shadow-lg`: 大きな影を追加

### ポイント3: レスポンシブクラス

```html
<h1 class="text-2xl md:text-3xl lg:text-4xl">
```

- `text-2xl`: デフォルト（スマホ）のフォントサイズ
- `md:text-3xl`: 768px以上（タブレット）のフォントサイズ
- `lg:text-4xl`: 1024px以上（デスクトップ）のフォントサイズ

Tailwindのブレークポイント：
- `sm`: 640px以上
- `md`: 768px以上
- `lg`: 1024px以上
- `xl`: 1280px以上
- `2xl`: 1536px以上

### ポイント4: 色のクラス

```html
<h2 class="text-blue-600 border-b-2 border-blue-600">
```

- `text-blue-600`: 文字色を青に
- `border-blue-600`: ボーダーの色を青に
- 数字（100〜900）で色の濃さを指定
  - 100: 薄い
  - 500: 中間
  - 900: 濃い

### ポイント5: ホバー効果

```html
<a class="text-blue-600 hover:text-blue-800">
```

- `hover:`: マウスを乗せたときのスタイル
- `hover:text-blue-800`: ホバー時に濃い青に変更

---

## 🔍 よくある間違い

### 間違い1: CDNリンクの記述場所

```html
<!-- ❌ 間違い（bodyの中に書いている） -->
<body>
    <script src="https://cdn.tailwindcss.com"></script>
</body>

<!-- ✅ 正しい（headの中に書く） -->
<head>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
```

### 間違い2: クラス名のスペルミス

```html
<!-- ❌ 間違い -->
<div class="bg-whit p-10">

<!-- ✅ 正しい -->
<div class="bg-white p-10">
```

### 間違い3: レスポンシブクラスの順序

```html
<!-- ❌ 間違い（大きい画面から小さい画面の順） -->
<h1 class="lg:text-4xl md:text-3xl text-2xl">

<!-- ✅ 正しい（小さい画面から大きい画面の順） -->
<h1 class="text-2xl md:text-3xl lg:text-4xl">
```

---

## 📊 Tailwind CSS vs カスタムCSS

### カスタムCSS

```css
.container {
    max-width: 800px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
```

### Tailwind CSS

```html
<div class="max-w-3xl mx-auto bg-white p-10 rounded-lg shadow-lg">
```

**Tailwind CSSの利点**：
- CSSファイルを書かなくて良い
- クラス名を考えなくて良い
- レスポンシブ対応が簡単
- 一貫性のあるデザイン

**カスタムCSSの利点**：
- 複雑なスタイルを管理しやすい
- HTMLがシンプルになる
- 独自のデザインシステムを構築できる

---

## 📚 次のステップ

Tailwind CSSをマスターしたら、次はDockerを学びましょう！

Tutorial 6では、開発環境を簡単に構築できるDockerの使い方を学びます。

---

## 💪 自己評価チェックリスト

以下の項目ができたかチェックしましょう：

- [ ] Tailwind CSSのCDNを読み込めた
- [ ] ユーティリティクラスを組み合わせてスタイリングできた
- [ ] レスポンシブクラス（md:、lg:）を使えた
- [ ] 色のクラス（text-blue-600など）を使えた
- [ ] ホバー効果（hover:）を実装できた
- [ ] マージンとパディングのクラスを使えた
- [ ] ブラウザで正しく表示されることを確認できた
- [ ] カスタムCSSとTailwind CSSの違いを理解できた

すべてチェックできたら、Tutorial 6に進みましょう！
