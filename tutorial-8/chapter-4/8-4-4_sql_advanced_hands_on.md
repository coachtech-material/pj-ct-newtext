# Tutorial 8-4-4: SQL応用操作 - ハンズオン演習

## 📝 このセクションの目的

Chapter 4で学んだSQL応用操作を実際に手を動かして確認します。WHERE句、ORDER BY句、集計関数、サブクエリを使って、複雑なデータ分析を行いましょう。

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
| ノートPC | 240000 |

---

## 🚀 チャレンジ

基本要件をクリアしたら、以下の追加課題にも挑戦してみましょう。

1. **日別の売上推移**：日付ごとの売上合計を表示

2. **売上TOP3**：売上が高い商品のTOP3を取得

3. **カテゴリ別の平均単価**：各カテゴリの平均単価を計算

4. **在庫管理**：販売数量が10個以上の商品を抽出

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

## 🎓 解説

### ポイント1: 集計関数

```sql
SUM(price * quantity)   -- 合計
AVG(price * quantity)   -- 平均
COUNT(*)                -- 件数
MAX(price)              -- 最大値
MIN(price)              -- 最小値
```

### ポイント2: GROUP BY

```sql
SELECT category, SUM(price * quantity) AS total
FROM sales
GROUP BY category;
```

- カテゴリごとにグループ化
- 各グループの合計を計算

### ポイント3: HAVING句

```sql
SELECT category, SUM(price * quantity) AS total
FROM sales
GROUP BY category
HAVING total > 100000;
```

- `WHERE`はグループ化前の条件
- `HAVING`はグループ化後の条件

### ポイント4: サブクエリ

```sql
WHERE (price * quantity) > (
    SELECT AVG(price * quantity)
    FROM sales
)
```

- カッコ内のクエリが先に実行される
- その結果を外側のクエリで使用

### ポイント5: LIMIT句

```sql
SELECT * FROM sales
ORDER BY (price * quantity) DESC
LIMIT 3;
```

- 取得する件数を制限
- TOP3を取得する場合などに使用

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

## 📚 次のステップ

SQL応用操作をマスターしたら、次はLaravelを学びましょう！

Tutorial 9では、LaravelフレームワークでWebアプリケーションを開発する方法を学びます。

---

## 💪 自己評価チェックリスト

以下の項目ができたかチェックしましょう：

- [ ] WHERE句で複雑な条件を指定できた
- [ ] ORDER BY句で並び替えができた
- [ ] 集計関数（SUM、AVG、COUNT、MAX、MIN）を使えた
- [ ] GROUP BYでグループ化できた
- [ ] HAVING句で集計後の条件を指定できた
- [ ] サブクエリを使えた
- [ ] LIMIT句で取得件数を制限できた
- [ ] 計算式（price × quantity）を使えた

すべてチェックできたら、Tutorial 9に進みましょう！
