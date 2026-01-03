# Tutorial 5-2-5: レイアウトの基礎（Flexbox）

## 🎯 このセクションで学ぶこと

*   モダンCSSレイアウトの主流である、Flexboxの基本的な概念を理解する。
*   `display: flex` を使って、要素を横並びにできることを知る。

---

## 詳細解説

通常、HTMLの `<div>` タグなどは、縦に並んで表示されます。しかし、ナビゲーションメニューやカードリストなど、要素を**横並び**にしたい場面は多くあります。

そこで使われるのが、**Flexbox (Flexible Box Layout)** です。

### 📦 Flexboxの基本

Flexboxを使うには、**親要素**に `display: flex;` を指定するだけです。

```html
<div class="container">
  <div class="item">アイテム1</div>
  <div class="item">アイテム2</div>
  <div class="item">アイテム3</div>
</div>
```

```css
.container {
  display: flex;
}
```

これだけで、子要素（`.item`）が**横一列に並びます**。

### 📝 よく見るプロパティ

Flexboxでは、親要素（Flexコンテナ）に指定するプロパティで、子要素の配置をコントロールします。

| プロパティ | 役割 | よく使う値 |
| :--- | :--- | :--- |
| `justify-content` | **水平方向**の配置 | `center`（中央）, `space-between`（両端揃え） |
| `align-items` | **垂直方向**の配置 | `center`（中央） |

```css
.container {
  display: flex;
  justify-content: center;  /* 水平方向に中央揃え */
  align-items: center;      /* 垂直方向に中央揃え */
}
```

---

## ✨ まとめ

*   **Flexbox**: 要素を柔軟に配置するためのレイアウト方法
*   **使い方**: 親要素に `display: flex;` を指定するだけで、子要素が横並びになる
*   **配置の調整**: `justify-content`（水平）と `align-items`（垂直）で、子要素の位置を調整できる

CSSのコードで `display: flex` を見かけたら、「子要素を横並びにしている」と理解すれば大丈夫です。

---
