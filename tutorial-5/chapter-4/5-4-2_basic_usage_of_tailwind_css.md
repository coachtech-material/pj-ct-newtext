# Tutorial 5-4-2: Tailwind CSSの基本的な使い方

## 🎯 このセクションで学ぶこと

*   よく使われるTailwindのユーティリティクラスを知る。
*   クラス名から、何が適用されているかを読み取れるようになる。

---

## 詳細解説

### 📦 余白（Padding / Margin）

余白を設定するクラスは、以下のパターンで構成されています。

```
{p|m}{方向}-{サイズ}
```

| 記号 | 意味 |
| :--- | :--- |
| `p` | padding（内側の余白） |
| `m` | margin（外側の余白） |
| `t` | top（上） |
| `b` | bottom（下） |
| `l` | left（左） |
| `r` | right（右） |
| `x` | 左右 |
| `y` | 上下 |
| なし | 全方向 |

**例:**

| クラス名 | 意味 |
| :--- | :--- |
| `p-4` | 全方向にpadding |
| `pt-2` | 上にpadding |
| `mx-auto` | 左右のmarginを自動（中央寄せ） |
| `mb-8` | 下にmargin |

### 🎨 色（Background / Text）

色を設定するクラスは、以下のパターンで構成されています。

```
{bg|text}-{色名}-{濃さ}
```

| 記号 | 意味 |
| :--- | :--- |
| `bg` | background-color（背景色） |
| `text` | color（文字色） |

**濃さ**: 50（薄い）〜 900（濃い）

**例:**

| クラス名 | 意味 |
| :--- | :--- |
| `bg-white` | 白い背景 |
| `bg-gray-100` | 薄いグレーの背景 |
| `bg-blue-500` | 青い背景（中間の濃さ） |
| `text-gray-700` | 濃いグレーの文字 |
| `text-red-500` | 赤い文字 |

### 📐 サイズ（Width / Height）

| クラス名 | 意味 |
| :--- | :--- |
| `w-full` | 幅100% |
| `w-1/2` | 幅50% |
| `h-screen` | 高さ100vh（画面いっぱい） |
| `max-w-md` | 最大幅を中サイズに制限 |

### 📝 レイアウト（Flexbox）

| クラス名 | 意味 |
| :--- | :--- |
| `flex` | Flexboxを有効化 |
| `justify-center` | 水平方向に中央揃え |
| `justify-between` | 両端揃え |
| `items-center` | 垂直方向に中央揃え |
| `gap-4` | 子要素間の隙間 |

### 📱 レスポンシブ修飾子

Tailwind CSSでは、クラス名の前に**プレフィックス**を付けることで、特定の画面サイズでのみスタイルを適用できます。

| プレフィックス | 意味 |
| :--- | :--- |
| `sm:` | 640px以上で適用 |
| `md:` | 768px以上で適用 |
| `lg:` | 1024px以上で適用 |

**例:**

```html
<div class="w-full md:w-1/2">
  <!-- スマホでは幅100%、タブレット以上では幅50% -->
</div>
```

### 🔲 その他よく見るクラス

| クラス名 | 意味 |
| :--- | :--- |
| `rounded` | 角を丸く |
| `rounded-lg` | 角を大きく丸く |
| `shadow` | 影を付ける |
| `border` | 枠線を付ける |
| `hidden` | 非表示 |
| `block` | ブロック要素として表示 |

---

## 📖 実際のコードを読んでみよう

以下は、Bladeテンプレートでよく見るコードの例です。

```html
<div class="bg-white p-6 rounded-lg shadow">
  <h2 class="text-xl font-bold mb-4">タイトル</h2>
  <p class="text-gray-600">本文テキストがここに入ります。</p>
  <button class="mt-4 bg-blue-500 text-white px-4 py-2 rounded">
    送信
  </button>
</div>
```

**読み方:**

| 要素 | クラス | 意味 |
| :--- | :--- | :--- |
| 外側のdiv | `bg-white p-6 rounded-lg shadow` | 白背景、余白あり、角丸、影付き |
| h2 | `text-xl font-bold mb-4` | 大きめの文字、太字、下に余白 |
| p | `text-gray-600` | グレーの文字 |
| button | `mt-4 bg-blue-500 text-white px-4 py-2 rounded` | 上に余白、青背景、白文字、左右・上下に余白、角丸 |

---

## ✨ まとめ

*   **余白**: `p-`（padding）、`m-`（margin）+ 方向（t/b/l/r/x/y）+ サイズ
*   **色**: `bg-`（背景）、`text-`（文字）+ 色名 + 濃さ
*   **レイアウト**: `flex`、`justify-center`、`items-center` など
*   **レスポンシブ**: `md:`、`lg:` などのプレフィックスで画面サイズに応じたスタイルを適用

Tailwindのクラス名は規則的なので、パターンを覚えれば、初めて見るクラスでも意味を推測できるようになります。

これで、Tutorial 5「HTML・CSS基礎」は終了です。BEエンジニアとして、フロントエンドのコードを読んで理解できる基礎知識が身につきました。

---
