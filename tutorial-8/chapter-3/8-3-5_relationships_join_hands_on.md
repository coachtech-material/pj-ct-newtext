# Tutorial 8-3-5: リレーションシップとJOIN - ハンズオン演習

## 📝 このセクションの目的

Chapter 3で学んだリレーションシップとJOINを実際に手を動かして確認します。複数のテーブルを結合して、関連するデータを取得する方法をマスターしましょう。

> 📌 **使用するデータベース**：このハンズオンでは、引き続き`practice_db`データベースを使用します。phpMyAdminで`practice_db`を選択してから、演習を始めてください。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

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
    price INT NOT NULL
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
INSERT INTO products (product_name, price) VALUES
('ノートPC', 120000),
('マウス', 2000),
('キーボード', 5000),
('モニター', 30000);
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

2. **田中太郎さんの注文履歴を取得**（商品名と数量を表示）

3. **ノートPCを購入した顧客の一覧を取得**（顧客名を表示）

4. **注文されていない商品を取得**（LEFT JOINを使用）

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

> 💡 **ヒントの見方**：以下のヒントは**完成形のコード**です。まずは自分で考えてから、答え合わせとして使ってください。

### ヒント1: すべての注文情報を取得（クエリ1の完成形）

```sql
SELECT customers.name, products.product_name, orders.quantity, orders.order_date
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id;
```

### ヒント2: 田中太郎さんの注文履歴を取得（クエリ2の完成形）

```sql
SELECT products.product_name, orders.quantity
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
WHERE customers.name = '田中太郎';
```

### ヒント3: ノートPCを購入した顧客の一覧（クエリ3の完成形）

```sql
SELECT customers.name
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
WHERE products.product_name = 'ノートPC';
```

### ヒント4: 注文されていない商品を取得（クエリ4の完成形）

```sql
SELECT products.product_name
FROM products
LEFT JOIN orders ON products.product_id = orders.product_id
WHERE orders.order_id IS NULL;
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？リレーションシップとJOINはデータベースの最も重要な機能の一つです。一緒に手を動かしながら、ECサイトの注文管理システムを構築していきましょう。

### 💭 実装の思考プロセス

ECサイトの注文管理システムを構築する際、以下の順番で考えると効率的です：

1. **テーブル間の関係を理解**：顧客、商品、注文の3つのエンティティとその関係
2. **外部キーで関係を構築**：ordersテーブルにcustomer_idとproduct_id
3. **INNER JOINで関連データを取得**：注文情報と顧客・商品情報を結合
4. **LEFT JOINで全データを取得**：注文がない商品も含めて取得

JOINのポイントは「どのカラムでテーブルを結合するかを明確にする」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: テーブルを作成する【要件1に対応】

**何を考えているか**：
- 「顧客テーブルと商品テーブルを先に作ろう」
- 「注文テーブルは外部キーで他のテーブルを参照しよう」
- 「外部キー制約でデータの整合性を保とう」

まず、customersテーブルを作成します：

```sql
CREATE TABLE customers (
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20)
);
```

**コードリーディング**：

```sql
CREATE TABLE customers (
```
→ customersテーブルを作成します。

```sql
    customer_id INT PRIMARY KEY AUTO_INCREMENT,
```
→ 顧客IDを主キーとして定義し、自動採番します。

```sql
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20)
);
```
→ 顧客名、メール、電話番号を定義します。メールは重複不可にします。

次に、productsテーブルを作成します：

```sql
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(200) NOT NULL,
    price INT NOT NULL
);
```

最後に、ordersテーブルを作成します：

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

**コードリーディング**：

```sql
    customer_id INT NOT NULL,
    product_id INT NOT NULL,
```
→ 顧客IDと商品IDを定義します。これらは外部キーとして使用されます。

```sql
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
```
→ 外部キー制約を設定します。`customer_id`はcustomersテーブルの`customer_id`を、`product_id`はproductsテーブルの`product_id`を参照します。これにより、存在しない顧客や商品を注文に登録することを防ぎます。

---

#### ステップ2: データを挿入する【要件2に対応】

**何を考えているか**：
- 「親テーブル（customers, products）から先にデータを入れよう」
- 「外部キー制約があるので、順番が重要」
- 「テストデータを複数件挿入しよう」

データを挿入します：

```sql
-- 顧客データを挿入
INSERT INTO customers (name, email, phone) VALUES
('田中太郎', 'tanaka@example.com', '090-1234-5678'),
('佐藤花子', 'sato@example.com', '080-2345-6789'),
('鈴木一郎', 'suzuki@example.com', '070-3456-7890');

-- 商品データを挿入
INSERT INTO products (product_name, price) VALUES
('ノートPC', 120000),
('マウス', 2000),
('キーボード', 5000),
('モニター', 30000);

-- 注文データを挿入
INSERT INTO orders (customer_id, product_id, quantity) VALUES
(1, 1, 1),  -- 田中太郎がノートPCを1台注文
(1, 2, 2),  -- 田中太郎がマウスを2個注文
(2, 3, 1),  -- 佐藤花子がキーボードを1個注文
(3, 1, 1),  -- 鈴木一郎がノートPCを1台注文
(3, 4, 2);  -- 鈴木一郎がモニターを2台注文
```

**コードリーディング**：

```sql
INSERT INTO customers (name, email, phone) VALUES
('田中太郎', 'tanaka@example.com', '090-1234-5678'),
...
```
→ まず、customersテーブルに顧客データを挿入します。外部キー制約があるため、親テーブルから先にデータを入れる必要があります。

```sql
INSERT INTO orders (customer_id, product_id, quantity) VALUES
(1, 1, 1),  -- 田中太郎がノートPCを1台注文
```
→ ordersテーブルに注文データを挿入します。`customer_id`に1、`product_id`に1を指定することで、外部キー制約により、存在する顧客と商品を参照します。

---

#### ステップ3: すべての注文情報を取得する【要件3-1に対応】

**何を考えているか**：
- 「注文情報だけではIDしかわからない」
- 「顧客名や商品名も一緒に表示したい」
- 「INNER JOINでテーブルを結合しよう」

すべての注文情報を取得します：

```sql
SELECT 
    customers.name,
    products.product_name,
    orders.quantity,
    orders.order_date
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id;
```

**コードリーディング**：

```sql
SELECT 
    customers.name,
    products.product_name,
    orders.quantity,
    orders.order_date
```
→ 取得するカラムを指定します。`テーブル名.カラム名`の形式で、どのテーブルのカラムかを明確にします。

```sql
FROM orders
```
→ メインのテーブルとしてordersテーブルを指定します。

```sql
INNER JOIN customers ON orders.customer_id = customers.customer_id
```
→ `INNER JOIN`でcustomersテーブルを結合します。`ON`以降に結合条件を指定します。`orders.customer_id = customers.customer_id`で、両テーブルの`customer_id`が一致する行を結合します。

```sql
INNER JOIN products ON orders.product_id = products.product_id;
```
→ さらにproductsテーブルを結合します。複数のテーブルを結合する場合、`INNER JOIN`を繰り返します。

---

#### ステップ4: 田中太郎さんの注文履歴を取得する【要件3-2に対応】

**何を考えているか**：
- 「特定の顧客の注文だけを抽出したい」
- 「JOINした後にWHERE句で絞り込もう」

田中太郎さんの注文履歴を取得します：

```sql
SELECT 
    products.product_name,
    orders.quantity
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
WHERE customers.name = '田中太郎';
```

**コードリーディング**：

```sql
WHERE customers.name = '田中太郎';
```
→ `WHERE`句で顧客名が「田中太郎」のレコードだけに絞り込みます。JOINでテーブルを結合した後に、条件で絞り込むことができます。

---

#### ステップ5: ノートPCを購入した顧客の一覧を取得する【要件3-3に対応】

**何を考えているか**：
- 「特定の商品を購入した顧客を知りたい」
- 「商品名で絞り込もう」

ノートPCを購入した顧客の一覧を取得します：

```sql
SELECT 
    customers.name
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
WHERE products.product_name = 'ノートPC';
```

**コードリーディング**：

```sql
WHERE products.product_name = 'ノートPC';
```
→ `WHERE`句で商品名が「ノートPC」のレコードだけに絞り込みます。

---

#### ステップ6: 注文されていない商品を取得する【要件3-4に対応】

**何を考えているか**：
- 「注文がない商品も表示したい」
- 「LEFT JOINを使うと左側のテーブルの全データが取得される」
- 「注文がない場合はorder_idがNULLになる」

注文されていない商品を取得します：

```sql
SELECT 
    products.product_name
FROM products
LEFT JOIN orders ON products.product_id = orders.product_id
WHERE orders.order_id IS NULL;
```

**コードリーディング**：

```sql
FROM products
LEFT JOIN orders ON products.product_id = orders.product_id
```
→ `LEFT JOIN`を使用することで、左側のテーブル（products）の全データを取得します。注文がない商品も結果に含まれ、ordersのカラムはNULLになります。

```sql
WHERE orders.order_id IS NULL;
```
→ `order_id`がNULLのレコード、つまり注文がない商品だけを抽出します。

---

### ✨ 完成！

これでECサイトの注文管理システムが完成しました！リレーションシップ、外部キー、INNER JOIN、LEFT JOINを実践できましたね。

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

### クエリ2: 田中太郎さんの注文履歴

| product_name | quantity |
|--------------|----------|
| ノートPC | 1 |
| マウス | 2 |

### クエリ3: ノートPCを購入した顧客の一覧

| name |
|------|
| 田中太郎 |
| 鈴木一郎 |

### クエリ4: 注文されていない商品

| product_name |
|--------------|
| キーボード |

> 💡 **注意**：クエリ4の結果は、サンプルデータでは「キーボード」が佐藤花子さんに注文されているため、実際には空の結果になります。もし結果を確認したい場合は、キーボードの注文データを削除してから実行してください。

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
    orders.quantity
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
WHERE customers.name = '田中太郎';
```

### クエリ3: ノートPCを購入した顧客の一覧を取得

```sql
SELECT 
    customers.name
FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id
INNER JOIN products ON orders.product_id = products.product_id
WHERE products.product_name = 'ノートPC';
```

### クエリ4: 注文されていない商品を取得

```sql
SELECT 
    products.product_name
FROM products
LEFT JOIN orders ON products.product_id = orders.product_id
WHERE orders.order_id IS NULL;
```

---

## 🔍 よくある間違い

### 間違い1: ON句の条件が間違っている

```sql
-- ❌ 間違い（結合条件が逆）
INNER JOIN customers ON orders.product_id = customers.customer_id

-- ✅ 正しい
INNER JOIN customers ON orders.customer_id = customers.customer_id
```

### 間違い2: テーブル名の省略

```sql
-- ❌ 間違い（どのテーブルのnameか不明）
SELECT name FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id;

-- ✅ 正しい
SELECT customers.name FROM orders
INNER JOIN customers ON orders.customer_id = customers.customer_id;
```

### 間違い3: LEFT JOINとINNER JOINの混同

```sql
-- ❌ 間違い（INNER JOINでは注文がない商品は取得できない）
SELECT products.product_name
FROM products
INNER JOIN orders ON products.product_id = orders.product_id
WHERE orders.order_id IS NULL;

-- ✅ 正しい（LEFT JOINを使用）
SELECT products.product_name
FROM products
LEFT JOIN orders ON products.product_id = orders.product_id
WHERE orders.order_id IS NULL;
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ 外部キーでテーブル間の関係を構築できる
- ✅ INNER JOINで関連データを取得できる
- ✅ WHERE句と組み合わせて条件で絞り込める
- ✅ LEFT JOINで全データを取得できる
- ✅ 複数テーブルを結合できる

引き続き、次のセクションも頑張りましょう！

---

## 🧹 後片付け（任意）

このハンズオンで作成した`customers`、`products`、`orders`テーブルは、`practice_db`データベース内に作成されています。これらは演習専用のテーブルで、Chapter 4以降では使用しません。

phpMyAdminのテーブル一覧を整理したい場合は、以下のSQLでテーブルを削除できます。ただし、削除すると元に戻せないので、注意してください。

```sql
-- 外部キー制約があるため、順番に削除する必要があります
DROP TABLE orders;
DROP TABLE customers;
DROP TABLE products;
```

> 💡 **ポイント**：`users`、`posts`、`tags`、`post_tag`テーブルは、Chapter 4でも使用するので、削除しないでください。

---
