# Tutorial 7-1-5: PHPの基礎 - ハンズオン演習

## 📝 このセクションの目的

Chapter 1で学んだPHPの基礎知識を実際に手を動かして確認します。変数、データ型、演算子、文字列操作を使った簡単なプログラムを作成しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

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

> 📁 **作業ディレクトリ**: Tutorial 7-1-2で作成した`~/php-practice/src/`ディレクトリ内にファイルを作成してください。ブラウザで`http://localhost:8000/price_calculator.php`にアクセスして確認します。

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

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？PHPの基本は変数と演算です。一緒に手を動かしながら、商品価格計算プログラムを作っていきましょう。

### 💭 実装の思考プロセス

PHPで計算プログラムを作る際、以下の順番で考えると効率的です：

1. **PHPファイルを作成して開始タグを書く**：`<?php`でPHPコードを開始
2. **入力データを変数に格納**：商品名、価格、数量、税率を定義
3. **計算を実行**：小計、消費税額、合計を計算
4. **結果を表示**：`echo`でHTMLを出力
5. **ブラウザで確認**：意図通りに表示されているかチェック

PHPのプログラムは「データを入力→処理→出力」という流れで考えるとわかりやすいです。

---

### 📝 ステップバイステップで実装

#### ステップ1: PHPファイルを作成して変数を定義する

**何を考えているか**：
- 「`~/php-practice/src/price_calculator.php`というファイルを作ろう」
- 「`<?php`でPHPコードを開始しよう」
- 「商品情報を変数に格納しよう」

まず、`~/php-practice/src/`ディレクトリに`price_calculator.php`を作成して、入力データを変数に格納します。

**✅ ディレクトリ構造の確認**

ファイルを作成すると、以下のようなディレクトリ構造になります。この構造になっていれば正解です！

```
php-practice/
├── docker/
│   └── nginx/
│       └── default.conf
├── src/
│   ├── index.php               # Tutorial 7-1-2で作成したファイル
│   └── price_calculator.php    # 今回作成するファイル
└── docker-compose.yml
```

その後、以下の手順で実行環境を構築してください。
1. Docker環境を起動（`cd ~/php-practice && docker-compose up -d`）
2. ブラウザでhttp://localhost:8000/price_calculator.php にアクセス

以下のコードを`price_calculator.php`に記述します：

```php
<?php
// 商品情報の定義
$product_name = "ノートパソコン";
$price = 80000;
$quantity = 2;
$tax_rate = 0.1;
```

**コードリーディング（1行ずつ）**：

```php
<?php
```
→ PHPコードの開始タグです。このタグ以降がPHPとして実行されます。

```php
// 商品情報の定義
```
→ コメントです。`//`の後ろは実行されず、コードの説明を書くために使います。

```php
$product_name = "ノートパソコン";
```
→ 変数`$product_name`に文字列「ノートパソコン」を代入します。PHPの変数は`$`で始まります。

```php
$price = 80000;
```
→ 変数`$price`に整数`80000`を代入します。数値はクォートで囲みません。

```php
$quantity = 2;
```
→ 変数`$quantity`に整数`2`を代入します。購入数量を表します。

```php
$tax_rate = 0.1;
```
→ 変数`$tax_rate`に小数`0.1`を代入します。10%を小数で表現しています。

---

#### ステップ2: 計算を実行する

**何を考えているか**：
- 「小計を計算しよう：価格×数量」
- 「消費税額を計算しよう：小計×税率」
- 「合計を計算しよう：小計＋消費税額」

次に、計算処理を追加します：

```php
// 計算処理
$subtotal = $price * $quantity;
$tax_amount = $subtotal * $tax_rate;
$total = $subtotal + $tax_amount;
```

**コードリーディング**：

```php
$subtotal = $price * $quantity;
```
→ 小計を計算します。`*`は乗算演算子です。`80000 * 2 = 160000`という計算が行われ、結果が`$subtotal`に格納されます。

```php
$tax_amount = $subtotal * $tax_rate;
```
→ 消費税額を計算します。`160000 * 0.1 = 16000`という計算が行われ、結果が`$tax_amount`に格納されます。

```php
$total = $subtotal + $tax_amount;
```
→ 合計金額を計算します。`+`は加算演算子です。`160000 + 16000 = 176000`という計算が行われ、結果が`$total`に格納されます。

---

#### ステップ3: 結果を表示する

**何を考えているか**：
- 「`echo`を使ってHTMLを出力しよう」
- 「数値にカンマを付けて読みやすくしよう」
- 「`<br>`で改行して見やすくしよう」

最後に、計算結果を表示します：

```php
// 結果の表示
echo "商品名: " . $product_name . "<br>";
echo "単価: " . number_format($price) . "円<br>";
echo "数量: " . $quantity . "個<br>";
echo "小計: " . number_format($subtotal) . "円<br>";
echo "消費税(" . ($tax_rate * 100) . "%): " . number_format($tax_amount) . "円<br>";
echo "<strong>合計金額: " . number_format($total) . "円</strong><br>";
?>
```

**コードリーディング（1行ずつ）**：

```php
echo "商品名: " . $product_name . "<br>";
```
→ `echo`で文字列を出力します。`.`は文字列連結演算子で、文字列と変数をつなげます。`<br>`はHTMLの改行タグです。

```php
echo "単価: " . number_format($price) . "円<br>";
```
→ `number_format()`関数で数値にカンマを付けます。`80000`が`80,000`に変換されます。

```php
echo "数量: " . $quantity . "個<br>";
```
→ 数量をそのまま表示します。小さい数値なのでカンマは不要です。

```php
echo "小計: " . number_format($subtotal) . "円<br>";
```
→ 小計をカンマ付きで表示します。`160000`が`160,000`に変換されます。

```php
echo "消費税(" . ($tax_rate * 100) . "%): " . number_format($tax_amount) . "円<br>";
```
→ 消費税率をパーセント表示に変換します。`0.1 * 100 = 10`という計算で`10%`と表示します。`($tax_rate * 100)`のように括弧で囲むと、先に計算されます。

```php
echo "<strong>合計金額: " . number_format($total) . "円</strong><br>";
```
→ 合計金額を`<strong>`タグで囲んで太字にします。重要な情報を強調します。

```php
?>
```
→ PHPコードの終了タグです。ファイルの最後に置きます。

---

#### ステップ4: ブラウザで確認する

**何を考えているか**：
- 「ファイルを保存してブラウザで開こう」
- 「意図通りに表示されているか確認しよう」

1. ファイルを`~/php-practice/src/price_calculator.php`として保存します
2. Docker環境が起動していることを確認します（`docker-compose up -d`）
3. ブラウザで`http://localhost:8000/price_calculator.php`を開きます
3. 以下のように表示されることを確認します：
   - 商品名: ノートパソコン
   - 単価: 80,000円
   - 数量: 2個
   - 小計: 160,000円
   - 消費税(10%): 16,000円
   - 合計金額: 176,000円

---

### ✨ 完成！

これでPHPで商品価格計算プログラムが完成しました！変数、演算子、文字列連結、関数の使い方を実践できましたね。

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

### Docker環境で実行

Tutorial 7-1-2で構築したDocker環境を使用します。

1. `~/php-practice/src/price_calculator.php`を作成
2. Docker環境を起動（`cd ~/php-practice && docker-compose up -d`）
3. ブラウザで`http://localhost:8000/price_calculator.php`にアクセス

> 💡 **ヒント**: ファイルを保存すると、ブラウザをリロードするだけで変更が反映されます。

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
