# Tutorial 8-4-4: SQL応用操作 - ハンズオン演習

## 📝 このセクションの目的

Chapter 4で学んだSQL応用操作を実際に手を動かして確認します。WHERE句、ORDER BY句、集計関数、サブクエリを使って、複雑なデータ分析を行いましょう。

> 📌 **使用するデータベース**：このハンズオンでは、新しいデータベース`sales_analysis`を作成して進めます。まず、phpMyAdminで以下のSQLを実行してデータベースを作成し、そのデータベースを選択してから演習を始めてください。
>
> ```sql
> CREATE DATABASE sales_analysis;
> ```

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

**学習のポイント**：
- WHERE句で複雑な条件を指定できるか
- ORDER BY句で並び替えができるか
- 集計関数（COUNT、SUM、AVG、MAX、MIN）を使えるか
- サブクエリを活用できるか

---

## 🎯 演習課題：売上分析システム

### 課題の概要

売上データを分析するクエリを作成してください。集計関数やサブクエリを使って、様々な角度から売上を分析します。

### 📋 要件

#### 1. テーブルの作成とデータ挿入

**salesテーブル**:

```sql
CREATE TABLE sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price INT NOT NULL,
    quantity INT NOT NULL,
    sale_date DATE NOT NULL
);

INSERT INTO sales (product_name, category, price, quantity, sale_date) VALUES
('ノートPC', '電子機器', 120000, 2, '2024-12-01'),
('マウス', '電子機器', 2000, 10, '2024-12-01'),
('キーボード', '電子機器', 5000, 5, '2024-12-02'),
('モニター', '電子機器', 30000, 3, '2024-12-02'),
('デスク', '家具', 25000, 2, '2024-12-03'),
('チェア', '家具', 15000, 4, '2024-12-03'),
('本棚', '家具', 10000, 3, '2024-12-04'),
('ノートPC', '電子機器', 120000, 1, '2024-12-05'),
('マウス', '電子機器', 2000, 15, '2024-12-05'),
('デスク', '家具', 25000, 1, '2024-12-06');
```

#### 2. クエリの作成

以下のクエリを作成して実行してください：

1. **売上合計金額を計算**（price × quantity の合計）

2. **カテゴリ別の売上合計を計算**

3. **最も売上が高い商品を取得**

4. **売上が10万円以上の取引を取得**

5. **12月3日以降の売上を日付順に取得**

6. **平均売上金額を計算**

7. **平均以上の売上がある取引を取得**（サブクエリを使用）

8. **各カテゴリの商品数を集計**

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: 売上金額の計算

```sql
SELECT product_name, (price * quantity) AS total
FROM sales;
```

### ヒント2: 集計関数

```sql
SELECT SUM(price * quantity) AS total_sales
FROM sales;
```

### ヒント3: GROUP BY

```sql
SELECT category, SUM(price * quantity) AS total
FROM sales
GROUP BY category;
```

### ヒント4: ORDER BY と LIMIT

```sql
SELECT product_name, (price * quantity) AS total
FROM sales
ORDER BY total DESC
LIMIT 1;
```

### ヒント5: サブクエリ

```sql
SELECT *
FROM sales
WHERE (price * quantity) > (
    SELECT AVG(price * quantity)
    FROM sales
);
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？SQL応用操作はデータ分析の強力なツールです。一緒に手を動かしながら、売上分析システムを構築していきましょう。

### 💭 実装の思考プロセス

売上分析システムを構築する際、以下の順番で考えると効率的です：

1. **テーブルを作成してデータを準備**：分析対象のデータを用意
2. **集計関数で合計を計算**：SUMで売上合計を取得
3. **GROUP BYでカテゴリ別に集計**：カテゴリごとの売上を分析
4. **ORDER BYで並び替え**：売上が高い順に表示
5. **サブクエリで複雑な条件を指定**：平均以上の売上を抽出

SQL応用操作のポイントは「集計関数とGROUP BYを組み合わせて、多角的にデータを分析する」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: テーブルを作成してデータを挿入する

**何を考えているか**：
- 「売上データを管理するテーブルを作ろう」
- 「商品名、カテゴリ、価格、数量、売上日を管理しよう」
- 「テストデータを複数件挿入しよう」

まず、salesテーブルを作成してデータを挿入します：

```sql
CREATE TABLE sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price INT NOT NULL,
    quantity INT NOT NULL,
    sale_date DATE NOT NULL
);

INSERT INTO sales (product_name, category, price, quantity, sale_date) VALUES
('ノートPC', '電子機器', 120000, 2, '2024-12-01'),
('マウス', '電子機器', 2000, 5, '2024-12-02'),
('キーボード', '電子機器', 5000, 3, '2024-12-03'),
('モニター', '電子機器', 30000, 5, '2024-12-04'),
('デスク', '家具', 50000, 2, '2024-12-05'),
('チェア', '家具', 30000, 3, '2024-12-06');
```

**コードリーディング**：

```sql
CREATE TABLE sales (
    sale_id INT PRIMARY KEY AUTO_INCREMENT,
```
→ salesテーブルを作成し、sale_idを主キーとして自動採番します。

```sql
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    price INT NOT NULL,
    quantity INT NOT NULL,
    sale_date DATE NOT NULL
);
```
→ 商品名、カテゴリ、価格、数量、売上日を定義します。すべて必須項目とします。

```sql
INSERT INTO sales (product_name, category, price, quantity, sale_date) VALUES
('ノートPC', '電子機器', 120000, 2, '2024-12-01'),
...
```
→ テストデータを複数件挿入します。カンマで区切って一度に複数行を挿入できます。

---

#### ステップ2: 売上合計金額を計算する

**何を考えているか**：
- 「全売上の合計金額を知りたい」
- 「価格×数量を計算して、SUMで合計しよう」
- 「SUM関数を使うと簡単に集計できる」

売上合計金額を計算します：

```sql
SELECT SUM(price * quantity) AS total_sales FROM sales;
```

**コードリーディング**：

```sql
SELECT SUM(price * quantity) AS total_sales FROM sales;
```
→ `SUM`関数で合計金額を計算します。`price * quantity`で各売上の金額を計算し、`SUM`で全体を合計します。`AS total_sales`で別名を付けて、結果をわかりやすくします。

---

#### ステップ3: カテゴリ別の売上合計を計算する

**何を考えているか**：
- 「カテゴリごとの売上を知りたい」
- 「GROUP BYでカテゴリごとにグループ化しよう」
- 「売上が高い順に並べ替えよう」

カテゴリ別の売上合計を計算します：

```sql
SELECT 
    category,
    SUM(price * quantity) AS total
FROM sales
GROUP BY category
ORDER BY total DESC;
```

**コードリーディング**：

```sql
SELECT 
    category,
    SUM(price * quantity) AS total
```
→ カテゴリと合計金額を取得します。

```sql
FROM sales
GROUP BY category
```
→ `GROUP BY category`でカテゴリごとにグループ化します。集計関数を使用する場合、`GROUP BY`が必要です。

```sql
ORDER BY total DESC;
```
→ `ORDER BY total DESC`で合計金額の降順（高い順）に並べ替えます。`DESC`は降順、`ASC`は昇順を意味します。

---

#### ステップ4: 最も売上が高い商品を取得する

**何を考えているか**：
- 「商品ごとの売上を集計しよう」
- 「売上が高い順に並べて、上位1件だけ取得しよう」
- 「LIMIT 1で上位1件に絞り込もう」

最も売上が高い商品を取得します：

```sql
SELECT 
    product_name,
    SUM(price * quantity) AS total
FROM sales
GROUP BY product_name
ORDER BY total DESC
LIMIT 1;
```

**コードリーディング**：

```sql
GROUP BY product_name
```
→ 商品ごとにグループ化します。

```sql
ORDER BY total DESC
```
→ 合計金額の降順に並べ替えます。

```sql
LIMIT 1;
```
→ `LIMIT 1`で上位1件のみを取得します。これにより、最も売上が高い商品だけを取得できます。

---

#### ステップ5: 売上が10万円以上の取引を取得する

**何を考えているか**：
- 「高額の取引だけを抽出したい」
- 「WHERE句で金額の条件を指定しよう」
- 「計算式を条件に使える」

売上が10万円以上の取引を取得します：

```sql
SELECT 
    product_name,
    (price * quantity) AS total,
    sale_date
FROM sales
WHERE (price * quantity) >= 100000
ORDER BY total DESC;
```

**コードリーディング**：

```sql
SELECT 
    product_name,
    (price * quantity) AS total,
    sale_date
```
→ 商品名、売上金額（価格×数量）、売上日を取得します。`AS total`で計算結果に別名を付けます。

```sql
FROM sales
WHERE (price * quantity) >= 100000
```
→ `WHERE`句で条件を指定します。`(price * quantity)`の計算結果が10万円以上のレコードだけを抽出します。計算式は括弧で囲むと明確になります。

```sql
ORDER BY total DESC;
```
→ 売上金額の降順（高い順）に並べ替えます。

---

#### ステップ6: 12月3日以降の売上を日付順に取得する

**何を考えているか**：
- 「特定の日付以降のデータを抽出したい」
- 「WHERE句で日付の比較をしよう」
- 「日付順に並べ替えよう」

12月3日以降の売上を日付順に取得します：

```sql
SELECT 
    product_name,
    category,
    (price * quantity) AS total,
    sale_date
FROM sales
WHERE sale_date >= '2024-12-03'
ORDER BY sale_date;
```

**コードリーディング**：

```sql
SELECT 
    product_name,
    category,
    (price * quantity) AS total,
    sale_date
```
→ 商品名、カテゴリ、売上金額、売上日を取得します。

```sql
FROM sales
WHERE sale_date >= '2024-12-03'
```
→ `WHERE`句で日付の条件を指定します。`>=`は「以上」を意味し、2024年12月3日以降のデータを抽出します。日付は`'YYYY-MM-DD'`形式の文字列で指定します。

```sql
ORDER BY sale_date;
```
→ 日付の昇順（古い順）に並べ替えます。`ASC`は省略可能で、デフォルトで昇順になります。

---

#### ステップ7: 平均売上金額を計算する

**何を考えているか**：
- 「全取引の平均売上を知りたい」
- 「AVG関数で平均を計算しよう」
- 「この値は後でサブクエリでも使える」

平均売上金額を計算します：

```sql
SELECT AVG(price * quantity) AS average_sales
FROM sales;
```

**コードリーディング**：

```sql
SELECT AVG(price * quantity) AS average_sales
```
→ `AVG`関数で平均値を計算します。`price * quantity`で各取引の売上金額を計算し、その平均を取得します。

```sql
FROM sales;
```
→ salesテーブルの全データを対象にします。

> 💡 **ポイント**：`AVG`関数の結果は小数になることがあります。必要に応じて`ROUND`関数で丸めることもできます。

---

#### ステップ8: 平均以上の売上がある取引を取得する（サブクエリ）

**何を考えているか**：
- 「平均売上を計算して、それ以上の取引を抽出したい」
- 「サブクエリで平均値を計算しよう」
- 「WHERE句の条件にサブクエリを使おう」

平均以上の売上がある取引を取得します：

```sql
SELECT 
    product_name,
    (price * quantity) AS total,
    sale_date
FROM sales
WHERE (price * quantity) > (
    SELECT AVG(price * quantity)
    FROM sales
)
ORDER BY total DESC;
```

**コードリーディング**：

```sql
SELECT 
    product_name,
    (price * quantity) AS total,
    sale_date
FROM sales
```
→ 商品名、売上金額、売上日を取得します。

```sql
WHERE (price * quantity) > (
    SELECT AVG(price * quantity)
    FROM sales
)
```
→ `WHERE`句の条件にサブクエリを使用します。サブクエリ`(SELECT AVG(price * quantity) FROM sales)`が先に実行され、平均値が計算されます。その平均値より大きい売上の取引だけが抽出されます。

```sql
ORDER BY total DESC;
```
→ 売上金額の降順（高い順）に並べ替えます。

> 💡 **サブクエリのポイント**：サブクエリは括弧`()`で囲む必要があります。サブクエリが先に実行され、その結果が外側のクエリの条件として使われます。

---

#### ステップ9: 各カテゴリの商品数を集計する

**何を考えているか**：
- 「カテゴリごとの商品種類数を知りたい」
- 「COUNT関数で件数を数えよう」
- 「DISTINCTで重複を除いてユニークな商品名を数えよう」

各カテゴリの商品数を集計します：

```sql
SELECT 
    category,
    COUNT(DISTINCT product_name) AS product_count,
    SUM(quantity) AS total_quantity
FROM sales
GROUP BY category;
```

**コードリーディング**：

```sql
SELECT 
    category,
    COUNT(DISTINCT product_name) AS product_count,
    SUM(quantity) AS total_quantity
```
→ カテゴリ、商品種類数、総数量を取得します。

```sql
COUNT(DISTINCT product_name) AS product_count
```
→ `COUNT`関数で件数を数えます。`DISTINCT`を付けることで、重複を除いたユニークな商品名の数をカウントします。例えば、「ノートPC」が2回登場しても、1としてカウントされます。

```sql
SUM(quantity) AS total_quantity
```
→ `SUM`関数で数量の合計を計算します。

```sql
FROM sales
GROUP BY category;
```
→ `GROUP BY category`でカテゴリごとにグループ化します。集計関数は各グループに対して実行されます。

---

### ✨ 完成！

これで売上分析システムが完成しました！集計関数、GROUP BY、ORDER BY、LIMIT、HAVING、サブクエリを実践できましたね。

---

## ✅ 完成イメージ

### クエリ1: 売上合計金額

| total_sales |
|-------------|
| 725000 |

### クエリ2: カテゴリ別の売上合計

| category | total |
|----------|-------|
| 電子機器 | 535000 |
| 家具 | 190000 |

### クエリ3: 最も売上が高い商品

| product_name | total |
|--------------|-------|
| ノートPC | 360000 |

### クエリ4: 売上が10万円以上の取引

| product_name | total | sale_date |
|--------------|-------|------------|
| ノートPC | 240000 | 2024-12-01 |
| ノートPC | 120000 | 2024-12-05 |

### クエリ5: 12月3日以降の売上

| product_name | category | total | sale_date |
|--------------|----------|-------|------------|
| デスク | 家具 | 50000 | 2024-12-03 |
| チェア | 家具 | 60000 | 2024-12-03 |
| 本棚 | 家具 | 30000 | 2024-12-04 |
| ノートPC | 電子機器 | 120000 | 2024-12-05 |
| マウス | 電子機器 | 30000 | 2024-12-05 |
| デスク | 家具 | 25000 | 2024-12-06 |

### クエリ6: 平均売上金額

| average_sales |
|---------------|
| 72500.0000 |

### クエリ7: 平均以上の売上がある取引

| product_name | total | sale_date |
|--------------|-------|------------|
| ノートPC | 240000 | 2024-12-01 |
| ノートPC | 120000 | 2024-12-05 |
| モニター | 90000 | 2024-12-02 |

### クエリ8: 各カテゴリの商品数

| category | product_count | total_quantity |
|----------|---------------|----------------|
| 電子機器 | 4 | 36 |
| 家具 | 3 | 12 |

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### クエリ1: 売上合計金額を計算

```sql
SELECT SUM(price * quantity) AS total_sales
FROM sales;
```

### クエリ2: カテゴリ別の売上合計を計算

```sql
SELECT 
    category,
    SUM(price * quantity) AS total
FROM sales
GROUP BY category
ORDER BY total DESC;
```

### クエリ3: 最も売上が高い商品を取得

```sql
SELECT 
    product_name,
    SUM(price * quantity) AS total
FROM sales
GROUP BY product_name
ORDER BY total DESC
LIMIT 1;
```

### クエリ4: 売上が10万円以上の取引を取得

```sql
SELECT 
    product_name,
    (price * quantity) AS total,
    sale_date
FROM sales
WHERE (price * quantity) >= 100000
ORDER BY total DESC;
```

### クエリ5: 12月3日以降の売上を日付順に取得

```sql
SELECT 
    product_name,
    category,
    (price * quantity) AS total,
    sale_date
FROM sales
WHERE sale_date >= '2024-12-03'
ORDER BY sale_date;
```

### クエリ6: 平均売上金額を計算

```sql
SELECT AVG(price * quantity) AS average_sales
FROM sales;
```

### クエリ7: 平均以上の売上がある取引を取得（サブクエリ）

```sql
SELECT 
    product_name,
    (price * quantity) AS total,
    sale_date
FROM sales
WHERE (price * quantity) > (
    SELECT AVG(price * quantity)
    FROM sales
)
ORDER BY total DESC;
```

### クエリ8: 各カテゴリの商品数を集計

```sql
SELECT 
    category,
    COUNT(DISTINCT product_name) AS product_count,
    SUM(quantity) AS total_quantity
FROM sales
GROUP BY category;
```

---

---

## 🔍 よくある間違い

### 間違い1: GROUP BYなしで集計関数を使用

```sql
-- ❌ 間違い
SELECT category, SUM(price * quantity)
FROM sales;

-- ✅ 正しい
SELECT category, SUM(price * quantity)
FROM sales
GROUP BY category;
```

### 間違い2: WHEREとHAVINGの混同

```sql
-- ❌ 間違い（集計後の条件はHAVINGを使う）
SELECT category, SUM(price * quantity) AS total
FROM sales
WHERE total > 100000
GROUP BY category;

-- ✅ 正しい
SELECT category, SUM(price * quantity) AS total
FROM sales
GROUP BY category
HAVING total > 100000;
```

### 間違い3: サブクエリのカッコ忘れ

```sql
-- ❌ 間違い
WHERE (price * quantity) > SELECT AVG(price * quantity) FROM sales

-- ✅ 正しい
WHERE (price * quantity) > (SELECT AVG(price * quantity) FROM sales)
```

---

## 📊 集計関数の使い分け

| 関数 | 用途 | 例 |
|------|------|-----|
| COUNT() | 件数を数える | 注文件数 |
| SUM() | 合計を計算 | 売上合計 |
| AVG() | 平均を計算 | 平均単価 |
| MAX() | 最大値を取得 | 最高売上 |
| MIN() | 最小値を取得 | 最低価格 |
---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ WHERE句で複雑な条件を指定できる
- ✅ ORDER BY句で並び替えができる
- ✅ 集計関数（COUNT、SUM、AVG、MAX、MIN）を使える
- ✅ サブクエリを活用できる

これでTutorial 8の学習は完了です！お疲れ様でした！

---

## 🧹 後片付け（任意）

このハンズオンで作成した`sales_analysis`データベースは、演習専用のデータベースです。

phpMyAdminの左ペインを整理したい場合は、以下のSQLでデータベースを削除できます。ただし、削除すると元に戻せないので、注意してください。

```sql
DROP DATABASE sales_analysis;
```

> 💡 **Tutorial 8で作成したデータベースのまとめ**：
> - `practice_db`：Chapter 2・3・4で使用したメインのデータベース
> - `task_management`：Chapter 2のハンズオンで作成
> - `sales_analysis`：Chapter 4のハンズオンで作成
>
> これらはすべて演習用なので、学習が終わったら削除しても構いません。

---
