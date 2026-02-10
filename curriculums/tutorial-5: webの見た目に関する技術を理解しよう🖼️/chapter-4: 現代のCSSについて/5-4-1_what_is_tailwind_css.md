# Tutorial 5-4-1: Tailwind CSSとは

## 📌 BEエンジニア志望者へ

このChapterで学ぶTailwind CSSは、BEエンジニアとして**自分でゼロからデザインを組む必要はありません**。ただし、以下の理由から、概念として理解しておくことが重要です。

- 提供されたBladeテンプレートのコードを読んで、何が書かれているか理解できる
- 簡単な修正（余白の調整、色の変更など）ができるようになる
- フロントエンドエンジニアとの協業時に、共通言語として話せる

**「こういうものがある」「クラス名を見れば何となく意味がわかる」程度の理解で十分です。**

---

## 📌 模擬案件での使用について

この教材の模擬案件では、**Tailwind CSSが適用されたBladeテンプレートが提供**されます。あなたは、そのテンプレートを使って、バックエンドの開発（ルーティング、コントローラー、データベース操作など）に集中します。

そのため、Tailwindについては「クラス名を見れば何となく意味がわかる」レベルで問題ありません。自分でゼロからTailwindを使ってデザインを組む必要はありません。

---

## 🎯 このセクションで学ぶこと

*   Tailwind CSSとは何か、従来のCSSとの違いを理解する。
*   ユーティリティファーストという考え方を知る。

---

## 詳細解説

### 🎨 Tailwind CSSとは？

**Tailwind CSS** は、**ユーティリティファースト**のCSSフレームワークです。

従来のCSSでは、自分でクラス名を考えて、CSSファイルにスタイルを書いていました。

```html
<!-- 従来のCSS -->
<button class="submit-button">送信</button>
```

```css
/* CSSファイル */
.submit-button {
  background-color: blue;
  color: white;
  padding: 10px 20px;
  border-radius: 5px;
}
```

Tailwind CSSでは、**あらかじめ用意されたクラス名**をHTMLに直接書くだけで、スタイルを適用できます。

```html
<!-- Tailwind CSS -->
<button class="bg-blue-500 text-white px-5 py-2 rounded">送信</button>
```

CSSファイルを書く必要がなく、HTMLだけでデザインが完結します。

### 📝 クラス名の読み方

Tailwindのクラス名は、**何をするかが名前から推測できる**ように設計されています。

| クラス名 | 意味 | 従来のCSS相当 |
| :--- | :--- | :--- |
| `bg-blue-500` | 背景色を青に | `background-color: #3b82f6;` |
| `text-white` | 文字色を白に | `color: white;` |
| `px-5` | 左右のpaddingを設定 | `padding-left: 1.25rem; padding-right: 1.25rem;` |
| `py-2` | 上下のpaddingを設定 | `padding-top: 0.5rem; padding-bottom: 0.5rem;` |
| `rounded` | 角を丸く | `border-radius: 0.25rem;` |
| `mt-4` | 上のmarginを設定 | `margin-top: 1rem;` |
| `flex` | Flexboxを適用 | `display: flex;` |
| `hidden` | 非表示に | `display: none;` |

### 👍 Tailwind CSSのメリット

*   **クラス名を考える必要がない**: あらかじめ用意されたクラス名を使うだけ。
*   **CSSファイルを編集しなくて済む**: スタイルの変更は、HTMLファイル内で完結する。
*   **変更が安全**: ある要素のクラスを変更しても、他の要素に影響しない。

---

## ✨ まとめ

*   **Tailwind CSS**: あらかじめ用意されたクラス名をHTMLに書くだけでスタイルを適用できるCSSフレームワーク
*   **ユーティリティファースト**: 一つのクラスが一つの機能を持つ設計思想
*   **クラス名の規則**: `bg-`（背景）、`text-`（文字）、`p-`（padding）、`m-`（margin）など、名前から機能が推測できる

Bladeテンプレートで `class="bg-blue-500 text-white p-4"` のような記述を見かけたら、「青い背景、白い文字、余白あり」と読み替えられれば十分です。

---
