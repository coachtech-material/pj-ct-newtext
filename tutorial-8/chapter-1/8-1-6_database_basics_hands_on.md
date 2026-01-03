# Tutorial 8-1-6: データベースの基礎 - ハンズオン演習

## 📝 このセクションの目的

Chapter 1で学んだデータベースの基礎知識を実際に手を動かして確認します。テーブル設計を行い、主キーと外部キーの関係を理解しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

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

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？データベース設計はシステム開発の土台となる重要な工程です。一緒に手を動かしながら、図書館管理システムのデータベースを設計していきましょう。

### 💭 実装の思考プロセス

図書館管理システムのデータベースを設計する際、以下の順番で考えると効率的です：

1. **管理する対象を特定**：書籍、会員、貸出の3つのエンティティ
2. **各エンティティの属性を洗い出す**：各テーブルに必要なカラムを考える
3. **主キーを決める**：各レコードを一意に識別するIDを設定
4. **リレーションを考える**：テーブル間の関係を1対多、多対多などで表現
5. **外部キーを設定**：リレーションを実現するための外部キーを追加

データベース設計のポイントは「データの重複を避け、整合性を保つ」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: booksテーブルを設計する

**何を考えているか**：
- 「書籍にはどんな情報が必要？」
- 「タイトル、著者、出版社、出版年、ISBNを管理しよう」
- 「主キーはbook_idで、AUTO_INCREMENTで自動採番しよう」

まず、booksテーブルを設計します：

```sql
CREATE TABLE books (
    book_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publisher VARCHAR(100),
    published_year INT,
    isbn VARCHAR(20) UNIQUE
);
```

**コードリーディング**：

```sql
CREATE TABLE books (
```
→ `CREATE TABLE`文でbooksテーブルを作成します。

```sql
    book_id INT PRIMARY KEY AUTO_INCREMENT,
```
→ `book_id`カラムを主キーとして定義します。`INT`は整数型、`PRIMARY KEY`は主キー、`AUTO_INCREMENT`は自動採番を意味します。これにより、1, 2, 3...と自動で番号が振られます。

```sql
    title VARCHAR(200) NOT NULL,
```
→ `title`カラムを定義します。`VARCHAR(200)`は最大200文字の可変長文字列、`NOT NULL`はNULL値を許可しない制約です。タイトルは必須項目なので`NOT NULL`を設定します。

```sql
    author VARCHAR(100) NOT NULL,
    publisher VARCHAR(100),
    published_year INT,
```
→ 著者、出版社、出版年を定義します。著者は必須、出版社と出版年は任意項目とします。

```sql
    isbn VARCHAR(20) UNIQUE
);
```
→ ISBNカラムを定義します。`UNIQUE`制約により、同じISBNが重複して登録されることを防ぎます。

---

#### ステップ2: membersテーブルを設計する

**何を考えているか**：
- 「会員にはどんな情報が必要？」
- 「名前、メール、電話番号、入会日を管理しよう」
- 「メールは重複不可にしよう」

次に、membersテーブルを設計します：

```sql
CREATE TABLE members (
    member_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    joined_date DATE NOT NULL
);
```

**コードリーディング**：

```sql
CREATE TABLE members (
```
→ membersテーブルを作成します。

```sql
    member_id INT PRIMARY KEY AUTO_INCREMENT,
```
→ 会員IDを主キーとして定義し、自動採番します。

```sql
    name VARCHAR(100) NOT NULL,
```
→ 会員名を必須項目として定義します。

```sql
    email VARCHAR(150) UNIQUE NOT NULL,
```
→ メールアドレスを定義します。`UNIQUE`で重複不可、`NOT NULL`で必須項目とします。メールアドレスはログインIDとして使用することが多いため、重複不可にします。

```sql
    phone VARCHAR(20),
    joined_date DATE NOT NULL
);
```
→ 電話番号は任意項目、入会日は必須項目とします。`DATE`型は日付を格納するデータ型です。

---

#### ステップ3: loansテーブルを設計する

**何を考えているか**：
- 「貸出は書籍と会員を結びつける中間テーブル」
- 「外部キーでbooksとmembersを参照しよう」
- 「貸出日、返却日、返却期限を管理しよう」

最後に、loansテーブルを設計します：

```sql
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

**コードリーディング**：

```sql
CREATE TABLE loans (
```
→ loansテーブルを作成します。

```sql
    loan_id INT PRIMARY KEY AUTO_INCREMENT,
```
→ 貸出IDを主キーとして定義し、自動採番します。

```sql
    book_id INT NOT NULL,
    member_id INT NOT NULL,
```
→ 書籍IDと会員IDを定義します。これらは外部キーとして使用されます。`NOT NULL`で必須項目とします。

```sql
    loan_date DATE NOT NULL,
    return_date DATE,
    due_date DATE NOT NULL,
```
→ 貸出日、返却日、返却期限を定義します。`return_date`は返却前はNULLなので、`NOT NULL`制約を付けません。

```sql
    FOREIGN KEY (book_id) REFERENCES books(book_id),
```
→ `book_id`を外部キーとして定義し、booksテーブルの`book_id`を参照します。これにより、存在しない書籍IDを登録することを防ぎます。

```sql
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);
```
→ `member_id`を外部キーとして定義し、membersテーブルの`member_id`を参照します。

---

#### ステップ4: サンプルデータを挿入する

**何を考えているか**：
- 「テーブルを作成したら、テストデータを入れて確認しよう」
- 「外部キーの制約が機能するか確認しよう」
- 「親テーブル（books, members）から先にデータを入れよう」

サンプルデータを挿入します：

```sql
-- booksテーブルにデータ挿入
INSERT INTO books (title, author, publisher, published_year, isbn) VALUES
('PHPの教科書', '山田太郎', '技術評論社', 2023, '978-4-1234-5678-9'),
('Laravelマスター', '佐藤花子', '翔泳社', 2024, '978-4-2345-6789-0'),
('データベース入門', '鈴木一郎', 'オライリー', 2022, '978-4-3456-7890-1');

-- membersテーブルにデータ挿入
INSERT INTO members (name, email, phone, joined_date) VALUES
('田中太郎', 'tanaka@example.com', '090-1234-5678', '2024-01-15'),
('高橋美咲', 'takahashi@example.com', '080-2345-6789', '2024-02-20'),
('伊藤健太', 'ito@example.com', '070-3456-7890', '2024-03-10');

-- loansテーブルにデータ挿入
INSERT INTO loans (book_id, member_id, loan_date, return_date, due_date) VALUES
(1, 1, '2024-12-01', '2024-12-08', '2024-12-15'),
(2, 2, '2024-12-05', NULL, '2024-12-19'),
(3, 1, '2024-12-10', NULL, '2024-12-24');
```

**コードリーディング**：

```sql
INSERT INTO books (title, author, publisher, published_year, isbn) VALUES
```
→ `INSERT INTO`文でbooksテーブルにデータを挿入します。カラム名を指定して、`VALUES`以降に値を指定します。

```sql
('PHPの教科書', '山田太郎', '技術評論社', 2023, '978-4-1234-5678-9'),
```
→ 1行目のデータを挿入します。カンマで区切って複数行を一度に挿入できます。

```sql
INSERT INTO loans (book_id, member_id, loan_date, return_date, due_date) VALUES
(1, 1, '2024-12-01', '2024-12-08', '2024-12-15'),
```
→ loansテーブルにデータを挿入します。`book_id`と1、`member_id`と1を指定することで、外部キー制約により、存在する書籍と会員を参照します。

```sql
(2, 2, '2024-12-05', NULL, '2024-12-19'),
```
→ `return_date`に`NULL`を指定することで、まだ返却されていない貸出を表現します。

---

### ✨ 完成！

これで図書館管理システムのデータベース設計が完成しました！テーブル設計、主キー、外部キー、リレーションの設定を実践できましたね。

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

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ テーブル構造を設計できる
- ✅ 主キーを適切に設定できる
- ✅ 外部キーでテーブル間の関係を表現できる
- ✅ 正規化の基本を理解できているか

引き続き、次のセクションも頑張りましょう！

---
