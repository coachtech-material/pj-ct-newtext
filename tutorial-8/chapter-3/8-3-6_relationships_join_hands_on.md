# Tutorial 8-3-6: リレーションシップとJOIN - ハンズオン演習

## 📝 このセクションの目的

Chapter 3で学んだリレーションシップとJOINを実際に手を動かして確認します。複数のテーブルを結合して、関連するデータを取得する方法をマスターしましょう。

**学習のポイント**：
- 外部キーでテーブル間の関係を構築できるか
- INNER JOINで関連データを取得できるか
- LEFT JOINの使い方を理解できているか
- 複数テーブルを結合できるか

---

## 🎯 演習課題：ECサイトの注文管理システム

### 課題の概要

ECサイトの注文管理システムを構築し、顧客・商品・注文の関連データを取得するクエリを作成してください。

### 📋 要件

#### 1. テーブルの作成

以下の3つのテーブルを作成してください：

**テーブル1: customers（顧客）**

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20)
);
```

**テーブル2: products（商品）**

```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(200) NOT NULL,
    price INT NOT NULL,
    stock INT DEFAULT 0
);
```

**テーブル3: orders（注文）**

```sql
CREATE TABLE orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT,
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
```

#### 2. サンプルデータの挿入

**customers**:
```sql
INSERT INTO customers (name, email, phone) VALUES
('田中太郎', 'tanaka@example.com', '090-1234-5678'),
('佐藤花子', 'sato@example.com', '080-2345-6789'),
('鈴木一郎', 'suzuki@example.com', '070-3456-7890');
```

**products**:
```sql
INSERT INTO products (product_name, price, stock) VALUES
('ノートPC', 120000, 10),
('マウス', 2000, 50),
('キーボード', 5000, 30),
('モニター', 30000, 15);
```

**orders**:
```sql
INSERT INTO orders (customer_id, product_id, quantity) VALUES
(1, 1, 1),  -- 田中太郎がノートPCを1台
(1, 2, 2),  -- 田中太郎がマウスを2個
(2, 3, 1),  -- 佐藤花子がキーボードを1個
(3, 1, 1),  -- 鈴木一郎がノートPCを1台
(3, 4, 2);  -- 鈴木一郎がモニターを2台
```

#### 3. クエリの作成

以下のクエリを作成して実行してください：

1. **すべての注文情報を取得**（顧客名、商品名、数量、注文日を表示）

2. **田中太郎さんの注文履歴を取得**

3. **ノートPCを購入した顧客の一覧を取得**

4. **各顧客の注文合計金額を計算**（顧客名と合計金額を表示）

5. **注文されていない商品を取得**（LEFT JOINを使用）

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: INNER JOIN

```sql
SELECT customers.name, products.product_name, orders.quantity
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id;
```

### ヒント2: WHERE句との組み合わせ

```sql
SELECT customers.name, products.product_name
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
WHERE customers.name = '田中太郎';
```

### ヒント3: 合計金額の計算

```sql
SELECT customers.name, SUM(products.price * orders.quantity) AS total
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
GROUP BY customers.customer_id;
```

### ヒント4: LEFT JOIN

```sql
SELECT products.product_name
FROM products
LEFT JOIN orders ON products.product_id = orders.product_id
WHERE orders.order_id IS NULL;
```

---

## ✅ 完成イメージ

### クエリ1: すべての注文情報

| name | product_name | quantity | order_date |
|------|--------------|----------|------------|
| 田中太郎 | ノートPC | 1 | 2024-12-15 10:00:00 |
| 田中太郎 | マウス | 2 | 2024-12-15 10:00:00 |
| 佐藤花子 | キーボード | 1 | 2024-12-15 10:00:00 |
| 鈴木一郎 | ノートPC | 1 | 2024-12-15 10:00:00 |
| 鈴木一郎 | モニター | 2 | 2024-12-15 10:00:00 |

### クエリ4: 各顧客の注文合計金額

| name | total |
|------|-------|
| 田中太郎 | 124000 |
| 佐藤花子 | 5000 |
| 鈴木一郎 | 180000 |

---

## 🚀 チャレンジ

基本要件をクリアしたら、以下の追加課題にも挑戦してみましょう。

1. **最も多く注文された商品**：商品ごとの注文数を集計

2. **顧客別の注文件数**：各顧客が何件注文したかを表示

3. **高額注文の抽出**：合計金額が10万円以上の注文を抽出

4. **在庫切れ商品**：在庫が0の商品を表示

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### クエリ1: すべての注文情報を取得

```sql
SELECT 
    customers.name,
    products.product_name,
    orders.quantity,
    orders.order_date
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
ORDER BY orders.order_date;
```

### クエリ2: 田中太郎さんの注文履歴を取得

```sql
SELECT 
    products.product_name,
    orders.quantity,
    products.price,
    (products.price * orders.quantity) AS subtotal
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
WHERE customers.name = '田中太郎';
```

### クエリ3: ノートPCを購入した顧客の一覧を取得

```sql
SELECT DISTINCT
    customers.name,
    customers.email
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
WHERE products.product_name = 'ノートPC';
```

### クエリ4: 各顧客の注文合計金額を計算

```sql
SELECT 
    customers.name,
    SUM(products.price * orders.quantity) AS total
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
GROUP BY customers.customer_id, customers.name
ORDER BY total DESC;
```

### クエリ5: 注文されていない商品を取得

```sql
SELECT 
    products.product_name,
    products.price,
    products.stock
FROM products
LEFT JOIN orders ON products.product_id = orders.product_id
WHERE orders.order_id IS NULL;
```

---

## 🎓 解説

### ポイント1: INNER JOIN

```sql
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
```

- 両方のテーブルに一致するレコードのみを取得
- `ON`句で結合条件を指定

### ポイント2: 複数テーブルのJOIN

```sql
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
```

- 3つ以上のテーブルも結合可能
- 順番に結合していく

### ポイント3: 集計関数とGROUP BY

```sql
SELECT customers.name, SUM(products.price * orders.quantity) AS total
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
GROUP BY customers.customer_id;
```

- `SUM()`で合計を計算
- `GROUP BY`で顧客ごとに集計

### ポイント4: LEFT JOIN

```sql
FROM products
LEFT JOIN orders ON products.product_id = orders.product_id
WHERE orders.order_id IS NULL
```

- 左側のテーブル（products）のすべてのレコードを取得
- 右側のテーブル（orders）に一致するレコードがない場合は`NULL`
- `WHERE orders.order_id IS NULL`で、注文されていない商品を抽出

### ポイント5: DISTINCT

```sql
SELECT DISTINCT customers.name
```

- 重複を除外
- 同じ顧客が複数回注文していても、1回だけ表示

---

## 🔍 よくある間違い

### 間違い1: ON句の条件が間違っている

```sql
-- ❌ 間違い（結合条件が逆）
INNER JOIN customers ON orders.product_id = customers.customer_id

-- ✅ 正しい
INNER JOIN customers ON orders.customer_id = customers.customer_id
```

### 間違い2: GROUP BYの忘れ

```sql
-- ❌ 間違い（GROUP BYがない）
SELECT customers.name, SUM(products.price * orders.quantity)
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id;

-- ✅ 正しい
SELECT customers.name, SUM(products.price * orders.quantity)
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
GROUP BY customers.customer_id;
```

### 間違い3: テーブル名の省略

```sql
-- ❌ 間違い（どのテーブルのnameか不明）
SELECT name FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id;

-- ✅ 正しい
SELECT customers.name FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id;
```

---

## 📚 次のステップ

リレーションシップとJOINをマスターしたら、次はSQL応用操作を学びましょう！

Chapter 4では、WHERE句、ORDER BY句、集計関数、サブクエリなど、より高度なSQL操作を学びます。

---

## 💪 自己評価チェックリスト

以下の項目ができたかチェックしましょう：

- [ ] 外部キーでテーブル間の関係を構築できた
- [ ] INNER JOINで関連データを取得できた
- [ ] 複数のテーブルを結合できた
- [ ] WHERE句と組み合わせて条件を指定できた
- [ ] 集計関数（SUM）とGROUP BYを使えた
- [ ] LEFT JOINの使い方を理解できた
- [ ] DISTINCTで重複を除外できた
- [ ] テーブル名を明示してカラムを指定できた

すべてチェックできたら、Chapter 4に進みましょう！
