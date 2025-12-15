# Tutorial 7-1-5: PHPの基礎 - ハンズオン演習

## 📝 このセクションの目的

Chapter 1で学んだPHPの基礎知識を実際に手を動かして確認します。変数、データ型、演算子、文字列操作を使った簡単なプログラムを作成しましょう。

**学習のポイント**：
- 変数を正しく宣言して使えるか
- データ型を理解できているか
- 文字列の連結や展開ができるか
- 演算子を適切に使えるか

---

## 🎯 演習課題：商品価格計算プログラムを作成しよう

### 課題の概要

オンラインショップの商品価格を計算するプログラムを作成してください。商品の価格、数量、消費税率を使って、合計金額を計算します。

### 📋 要件

以下の要件を満たすPHPファイル（`price_calculator.php`）を作成してください。

#### 1. 変数の定義

以下の変数を定義してください：

```php
$product_name = "ノートパソコン";
$price = 80000;
$quantity = 2;
$tax_rate = 0.1;
```

#### 2. 計算処理

以下の計算を行ってください：

- **小計**：`$price × $quantity`
- **消費税額**：`小計 × $tax_rate`
- **合計金額**：`小計 + 消費税額`

計算結果は、以下の変数に格納してください：

```php
$subtotal = ...;
$tax_amount = ...;
$total = ...;
```

#### 3. 結果の表示

以下の形式で結果を表示してください：

```
商品名: ノートパソコン
単価: 80,000円
数量: 2個
小計: 160,000円
消費税(10%): 16,000円
合計金額: 176,000円
```

**表示の要件**：
- 金額は`number_format()`関数を使って、3桁ごとにカンマ区切りで表示
- HTMLの`<br>`タグを使って改行
- 変数を文字列に埋め込んで表示

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: 変数の定義

```php
<?php
$product_name = "ノートパソコン";
$price = 80000;
$quantity = 2;
$tax_rate = 0.1;
?>
```

### ヒント2: 計算

```php
$subtotal = $price * $quantity;
$tax_amount = $subtotal * $tax_rate;
$total = $subtotal + $tax_amount;
```

### ヒント3: 金額のフォーマット

```php
$formatted_price = number_format($price);
// 結果: "80,000"
```

### ヒント4: 文字列の連結

```php
echo "商品名: " . $product_name . "<br>";
```

### ヒント5: 変数の展開

```php
echo "商品名: {$product_name}<br>";
```

---

## ✅ 完成イメージ

完成すると、ブラウザに以下のように表示されます：

```
商品名: ノートパソコン
単価: 80,000円
数量: 2個
小計: 160,000円
消費税(10%): 16,000円
合計金額: 176,000円
```

---

## 🚀 チャレンジ

基本要件をクリアしたら、以下の追加課題にも挑戦してみましょう。

1. **割引機能**：割引率（例: 10%）を追加して、割引後の金額を計算

2. **複数商品**：2つ目の商品を追加して、合計金額を計算

3. **HTMLテーブル**：結果をHTMLのテーブル形式で表示

4. **型の確認**：`var_dump()`を使って、各変数の型を確認

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### price_calculator.php

```php
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>商品価格計算</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .result {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
        }
        .line {
            margin: 10px 0;
            font-size: 18px;
            color: #555;
        }
        .total {
            margin-top: 20px;
            padding-top: 20px;
            border-top: 2px solid #0066cc;
            font-size: 20px;
            font-weight: bold;
            color: #0066cc;
        }
    </style>
</head>
<body>
    <div class="result">
        <h1>商品価格計算</h1>
        
        <?php
        // 変数の定義
        $product_name = "ノートパソコン";
        $price = 80000;
        $quantity = 2;
        $tax_rate = 0.1;
        
        // 計算処理
        $subtotal = $price * $quantity;
        $tax_amount = $subtotal * $tax_rate;
        $total = $subtotal + $tax_amount;
        
        // 結果の表示
        echo "<div class='line'>商品名: {$product_name}</div>";
        echo "<div class='line'>単価: " . number_format($price) . "円</div>";
        echo "<div class='line'>数量: {$quantity}個</div>";
        echo "<div class='line'>小計: " . number_format($subtotal) . "円</div>";
        echo "<div class='line'>消費税(10%): " . number_format($tax_amount) . "円</div>";
        echo "<div class='total'>合計金額: " . number_format($total) . "円</div>";
        ?>
    </div>
</body>
</html>
```

---

## 🎓 解説

### ポイント1: 変数の命名規則

```php
$product_name = "ノートパソコン";  // スネークケース（推奨）
$productName = "ノートパソコン";   // キャメルケース（どちらでもOK）
```

- PHPでは、変数名は`$`で始まる
- スネークケース（`snake_case`）が一般的
- 意味のある名前を付ける

### ポイント2: データ型

```php
$product_name = "ノートパソコン";  // 文字列（string）
$price = 80000;                    // 整数（integer）
$tax_rate = 0.1;                   // 浮動小数点数（float）
```

- PHPは動的型付け言語（型を明示的に宣言しなくてOK）
- 自動的に適切な型が推論される

### ポイント3: 演算子

```php
$subtotal = $price * $quantity;    // 乗算
$tax_amount = $subtotal * $tax_rate;  // 乗算
$total = $subtotal + $tax_amount;  // 加算
```

- `*`: 乗算
- `+`: 加算
- `-`: 減算
- `/`: 除算
- `%`: 剰余

### ポイント4: number_format()関数

```php
$price = 80000;
echo number_format($price);  // "80,000"
```

- 数値を3桁ごとにカンマ区切りで表示
- 読みやすい金額表示に便利

### ポイント5: 文字列の連結と展開

```php
// 連結演算子（.）を使う方法
echo "商品名: " . $product_name . "<br>";

// 変数展開を使う方法（ダブルクォートの中）
echo "商品名: {$product_name}<br>";
echo "商品名: $product_name<br>";  // 波括弧なしでもOK
```

- `.`（ドット）で文字列を連結
- ダブルクォート内では変数が展開される
- シングルクォート内では変数は展開されない

---

## 🔍 よくある間違い

### 間違い1: 変数名の$忘れ

```php
// ❌ 間違い
price = 80000;

// ✅ 正しい
$price = 80000;
```

### 間違い2: セミコロンの忘れ

```php
// ❌ 間違い
$price = 80000
$quantity = 2;

// ✅ 正しい
$price = 80000;
$quantity = 2;
```

### 間違い3: シングルクォートでの変数展開

```php
// ❌ 間違い（変数が展開されない）
echo '商品名: $product_name';
// 結果: 商品名: $product_name

// ✅ 正しい（ダブルクォートを使う）
echo "商品名: $product_name";
// 結果: 商品名: ノートパソコン
```

### 間違い4: 計算の順序

```php
// ❌ 間違い（小計を計算する前に消費税を計算）
$tax_amount = $price * $tax_rate;
$subtotal = $price * $quantity;

// ✅ 正しい（先に小計を計算）
$subtotal = $price * $quantity;
$tax_amount = $subtotal * $tax_rate;
```

---

## 🧪 動作確認の方法

### 方法1: ローカル環境で実行

1. `price_calculator.php`を作成
2. PHPが実行できる環境（XAMPP、MAMPなど）に配置
3. ブラウザで`http://localhost/price_calculator.php`にアクセス

### 方法2: コマンドラインで実行

```bash
php price_calculator.php
```

HTMLタグが含まれていますが、計算結果を確認できます。

---

## 📚 次のステップ

PHPの基礎をマスターしたら、次は制御構文を学びましょう！

Chapter 2では、if文、switch文、for文、while文などを使って、プログラムの流れを制御する方法を学びます。

---

## 💪 自己評価チェックリスト

以下の項目ができたかチェックしましょう：

- [ ] 変数を正しく宣言できた（$を忘れずに）
- [ ] 適切なデータ型を使えた（文字列、整数、浮動小数点数）
- [ ] 演算子を使って計算できた
- [ ] `number_format()`で金額をフォーマットできた
- [ ] 文字列の連結（.）を使えた
- [ ] 変数展開（ダブルクォート内）を使えた
- [ ] ブラウザで正しく表示されることを確認できた
- [ ] セミコロンを忘れずに記述できた

すべてチェックできたら、Chapter 2に進みましょう！
