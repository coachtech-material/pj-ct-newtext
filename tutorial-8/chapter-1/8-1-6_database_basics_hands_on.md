# Tutorial 8-1-6: データベースの基礎 - ハンズオン演習

## 📝 このセクションの目的

Chapter 1で学んだデータベースの基礎知識を実際に手を動かして確認します。テーブル設計を行い、主キーと外部キーの関係を理解しましょう。

**学習のポイント**：
- テーブル構造を設計できるか
- 主キーを適切に設定できるか
- 外部キーでテーブル間の関係を表現できるか
- 正規化の基本を理解できているか

---

## 🎯 演習課題：図書館管理システムのデータベース設計

### 課題の概要

図書館の蔵書と貸出を管理するデータベースを設計してください。以下の3つのテーブルを設計し、ER図を作成します。

### 📋 要件

#### 1. テーブル設計

以下の3つのテーブルを設計してください：

**テーブル1: books（書籍）**

| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| book_id | INT | PRIMARY KEY, AUTO_INCREMENT | 書籍ID |
| title | VARCHAR(200) | NOT NULL | 書籍名 |
| author | VARCHAR(100) | NOT NULL | 著者名 |
| publisher | VARCHAR(100) | NULL | 出版社 |
| published_year | INT | NULL | 出版年 |
| isbn | VARCHAR(20) | UNIQUE | ISBN番号 |

**テーブル2: members（会員）**

| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| member_id | INT | PRIMARY KEY, AUTO_INCREMENT | 会員ID |
| name | VARCHAR(100) | NOT NULL | 会員名 |
| email | VARCHAR(150) | UNIQUE, NOT NULL | メールアドレス |
| phone | VARCHAR(20) | NULL | 電話番号 |
| joined_date | DATE | NOT NULL | 入会日 |

**テーブル3: loans（貸出）**

| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| loan_id | INT | PRIMARY KEY, AUTO_INCREMENT | 貸出ID |
| book_id | INT | FOREIGN KEY (books) | 書籍ID |
| member_id | INT | FOREIGN KEY (members) | 会員ID |
| loan_date | DATE | NOT NULL | 貸出日 |
| return_date | DATE | NULL | 返却日 |
| due_date | DATE | NOT NULL | 返却期限 |

#### 2. リレーションシップ

- **books ← loans**: 1対多（1冊の本は複数回貸し出される）
- **members ← loans**: 1対多（1人の会員は複数の本を借りる）

#### 3. ER図の作成

テーブル間の関係を示すER図を紙またはツールで作成してください。

#### 4. サンプルデータの考案

各テーブルに3件ずつサンプルデータを考えてください。

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: 主キーの選択

- 各テーブルには必ず主キーが必要
- `AUTO_INCREMENT`を使うと、自動的に連番が振られる
- 主キーは重複しない値である必要がある

### ヒント2: 外部キーの設定

```
loans.book_id → books.book_id
loans.member_id → members.member_id
```

- 外部キーは、他のテーブルの主キーを参照する
- これにより、テーブル間の関係を表現できる

### ヒント3: データ型の選択

- 文字列: `VARCHAR(長さ)`
- 整数: `INT`
- 日付: `DATE`
- ISBN番号は文字列（ハイフンを含むため）

### ヒント4: 制約の設定

- `NOT NULL`: 必須項目
- `UNIQUE`: 重複不可
- `PRIMARY KEY`: 主キー
- `FOREIGN KEY`: 外部キー

---

## ✅ 完成イメージ

### ER図

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   books     │       │    loans    │       │  members    │
├─────────────┤       ├─────────────┤       ├─────────────┤
│ book_id (PK)│◄──────│ loan_id (PK)│──────►│member_id(PK)│
│ title       │       │ book_id (FK)│       │ name        │
│ author      │       │member_id(FK)│       │ email       │
│ publisher   │       │ loan_date   │       │ phone       │
│published_year│      │ return_date │       │ joined_date │
│ isbn        │       │ due_date    │       │             │
└─────────────┘       └─────────────┘       └─────────────┘
     1                                             1
     │                                             │
     └──────────────── * ─────────────────────────┘
                    (1対多)
```

### サンプルデータ

**books**:
| book_id | title | author | publisher | published_year | isbn |
|---------|-------|--------|-----------|----------------|------|
| 1 | PHPの教科書 | 山田太郎 | 技術評論社 | 2023 | 978-4-1234-5678-9 |
| 2 | Laravelマスター | 佐藤花子 | 翔泳社 | 2024 | 978-4-2345-6789-0 |
| 3 | データベース入門 | 鈴木一郎 | オライリー | 2022 | 978-4-3456-7890-1 |

**members**:
| member_id | name | email | phone | joined_date |
|-----------|------|-------|-------|-------------|
| 1 | 田中太郎 | tanaka@example.com | 090-1234-5678 | 2024-01-15 |
| 2 | 高橋美咲 | takahashi@example.com | 080-2345-6789 | 2024-02-20 |
| 3 | 伊藤健太 | ito@example.com | 070-3456-7890 | 2024-03-10 |

**loans**:
| loan_id | book_id | member_id | loan_date | return_date | due_date |
|---------|---------|-----------|-----------|-------------|----------|
| 1 | 1 | 1 | 2024-12-01 | 2024-12-08 | 2024-12-15 |
| 2 | 2 | 2 | 2024-12-05 | NULL | 2024-12-19 |
| 3 | 3 | 1 | 2024-12-10 | NULL | 2024-12-24 |

---

## 🚀 チャレンジ

基本要件をクリアしたら、以下の追加課題にも挑戦してみましょう。

1. **カテゴリテーブル**：書籍のカテゴリを管理するテーブルを追加

2. **延滞管理**：返却期限を過ぎた貸出を管理する仕組みを考える

3. **予約機能**：書籍の予約を管理するテーブルを追加

4. **在庫管理**：同じ書籍の複数の在庫を管理する仕組みを考える

---

## 📖 模範解答

自分で設計してから、以下の模範解答を確認してください。

### CREATE TABLE文

```sql
-- booksテーブル
CREATE TABLE books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publisher VARCHAR(100),
    published_year INT,
    isbn VARCHAR(20) UNIQUE
);

-- membersテーブル
CREATE TABLE members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    joined_date DATE NOT NULL
);

-- loansテーブル
CREATE TABLE loans (
    loan_id INT PRIMARY KEY AUTO_INCREMENT,
    book_id INT NOT NULL,
    member_id INT NOT NULL,
    loan_date DATE NOT NULL,
    return_date DATE,
    due_date DATE NOT NULL,
    FOREIGN KEY (book_id) REFERENCES books(book_id),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);
```

### サンプルデータのINSERT文

```sql
-- booksにデータを挿入
INSERT INTO books (title, author, publisher, published_year, isbn) VALUES
('PHPの教科書', '山田太郎', '技術評論社', 2023, '978-4-1234-5678-9'),
('Laravelマスター', '佐藤花子', '翔泳社', 2024, '978-4-2345-6789-0'),
('データベース入門', '鈴木一郎', 'オライリー', 2022, '978-4-3456-7890-1');

-- membersにデータを挿入
INSERT INTO members (name, email, phone, joined_date) VALUES
('田中太郎', 'tanaka@example.com', '090-1234-5678', '2024-01-15'),
('高橋美咲', 'takahashi@example.com', '080-2345-6789', '2024-02-20'),
('伊藤健太', 'ito@example.com', '070-3456-7890', '2024-03-10');

-- loansにデータを挿入
INSERT INTO loans (book_id, member_id, loan_date, return_date, due_date) VALUES
(1, 1, '2024-12-01', '2024-12-08', '2024-12-15'),
(2, 2, '2024-12-05', NULL, '2024-12-19'),
(3, 1, '2024-12-10', NULL, '2024-12-24');
```

---

## 🎓 解説

### ポイント1: 主キーの設計

```sql
book_id INT PRIMARY KEY AUTO_INCREMENT
```

- `PRIMARY KEY`: 主キーとして設定
- `AUTO_INCREMENT`: 自動的に連番を振る
- 各レコードを一意に識別できる

### ポイント2: 外部キーの設計

```sql
FOREIGN KEY (book_id) REFERENCES books(book_id)
```

- `loansテーブル`の`book_id`が`booksテーブル`の`book_id`を参照
- これにより、存在しない`book_id`は登録できない（参照整合性）

### ポイント3: データ型の選択

- `VARCHAR(長さ)`: 可変長文字列（タイトル、名前など）
- `INT`: 整数（ID、年など）
- `DATE`: 日付（貸出日、返却日など）

### ポイント4: 制約の活用

- `NOT NULL`: 必須項目（空欄不可）
- `UNIQUE`: 重複不可（メールアドレス、ISBNなど）
- `FOREIGN KEY`: 他のテーブルとの関連付け

### ポイント5: 正規化

- 各テーブルは1つの主題に焦点を当てる
- 重複データを避ける
- テーブル間の関係を外部キーで表現

---

## 🔍 よくある間違い

### 間違い1: 主キーの設定忘れ

```sql
-- ❌ 間違い（主キーがない）
CREATE TABLE books (
    title VARCHAR(200),
    author VARCHAR(100)
);

-- ✅ 正しい
CREATE TABLE books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200),
    author VARCHAR(100)
);
```

### 間違い2: 外部キーの参照先が間違っている

```sql
-- ❌ 間違い（存在しないカラムを参照）
FOREIGN KEY (book_id) REFERENCES books(id)

-- ✅ 正しい
FOREIGN KEY (book_id) REFERENCES books(book_id)
```

### 間違い3: データ型の選択ミス

```sql
-- ❌ 間違い（ISBNを数値型にしている）
isbn INT

-- ✅ 正しい（ISBNはハイフンを含むため文字列）
isbn VARCHAR(20)
```

---

## 📚 次のステップ

データベース設計の基礎をマスターしたら、次はMySQLの基本操作を学びましょう！

Chapter 2では、phpMyAdminを使って、実際にテーブルを作成し、データを挿入・取得する方法を学びます。

---

## 💪 自己評価チェックリスト

以下の項目ができたかチェックしましょう：

- [ ] テーブル構造を設計できた
- [ ] 主キーを適切に設定できた
- [ ] 外部キーでテーブル間の関係を表現できた
- [ ] 適切なデータ型を選択できた
- [ ] 制約（NOT NULL、UNIQUEなど）を設定できた
- [ ] ER図を作成できた
- [ ] サンプルデータを考案できた
- [ ] CREATE TABLE文を書けた

すべてチェックできたら、Chapter 2に進みましょう！
