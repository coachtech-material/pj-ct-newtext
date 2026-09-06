# 8-2-7: MySQL基本操作 - ハンズオン演習

## 📌 このハンズオンについて

Chapter 2で学んだMySQL基本操作を実際に手を動かして確認します。phpMyAdminを使って、テーブルの作成からデータの挿入・取得・更新・削除まで一連のCRUD操作を行いましょう。

> 🔥 分からないことがあったら、すぐに答えを見るのではなく、過去の教材を見返したり、AIに「質問」したりして、自分の力で実装してみましょう。この段階では、コードそのものをAIに書かせるのはぐっと我慢です。1-1-6でお話しした通り、設計ができる人は「自分の手でコードを書いたことがある人」だからです。

**学習のポイント**：
- CREATE TABLE文でテーブルを作成できるか
- INSERT文でデータを挿入できるか
- SELECT文でデータを取得できるか
- UPDATE文でデータを更新できるか
- DELETE文でデータを削除できるか

---

## 🎯 演習課題：タスク管理システムのデータベース構築

### 課題の概要

シンプルなタスク管理システムのデータベースを構築し、CRUD操作（作成・読取・更新・削除）を実行してください。

### 📋 要件

#### 1. データベースの作成

データベース名: `task_management`

#### 2. テーブルの作成

テーブル名: `tasks`

| カラム名 | データ型 | 制約 | 説明 |
|---------|---------|------|------|
| task_id | INT | PRIMARY KEY, AUTO_INCREMENT | タスクID |
| title | VARCHAR(200) | NOT NULL | タスク名 |
| description | TEXT | NULL | 詳細説明 |
| status | ENUM('未着手', '進行中', '完了') | DEFAULT '未着手' | ステータス |
| priority | INT | DEFAULT 3 | 優先度（1:高、2:中、3:低） |
| due_date | DATE | NULL | 期限 |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | 作成日時 |

**ステータスの説明**：
- **未着手**：まだ作業を開始していないタスク
- **進行中**：現在作業中のタスク
- **完了**：作業が完了したタスク

> 💡 **ポイント**：`ENUM`型は、指定した値のいずれかしか入力できないデータ型です。上記の3つ以外の値を入力しようとするとエラーになります。これにより、データの整合性を保つことができます。

#### 3. データの挿入（INSERT）

以下の5件のタスクを挿入してください：

1. タイトル: 「データベース設計」、ステータス: 「完了」、優先度: 1、期限: 2024-12-10
2. タイトル: 「API開発」、ステータス: 「進行中」、優先度: 1、期限: 2024-12-20
3. タイトル: 「テスト作成」、ステータス: 「未着手」、優先度: 2、期限: 2024-12-25
4. タイトル: 「ドキュメント作成」、ステータス: 「未着手」、優先度: 3、期限: 2024-12-30
5. タイトル: 「デプロイ準備」、ステータス: 「未着手」、優先度: 2、期限: 2025-01-05

#### 4. データの取得（SELECT）

以下のクエリを実行してください：

1. すべてのタスクを取得
2. ステータスが「未着手」のタスクのみ取得
3. 優先度が1（高）のタスクのみ取得
4. タスクを優先度の高い順に並び替えて取得

#### 5. データの更新（UPDATE）

以下の更新を実行してください：

1. 「API開発」のステータスを「完了」に変更
2. 「テスト作成」のステータスを「進行中」、優先度を1に変更

#### 6. データの削除（DELETE）

「ドキュメント作成」タスクを削除してください。

### ✏️ 実装タスク

1. データベースを作成する
2. テーブルを作成する
3. データを挿入する
4. データを取得する
5. データを更新する
6. データを削除する

### ✅ 完成チェックリスト

- [ ] phpMyAdminでtask_managementデータベースが表示される
- [ ] `SELECT * FROM tasks;` で5件のデータが表示される
- [ ] WHERE句で条件を指定してデータを絞り込めた
- [ ] UPDATE後、対象タスクのステータスが変更されている
- [ ] DELETE後、対象タスクが削除されている

> 💡 **動作確認**: 各SQL実行後に `SELECT * FROM tasks;` で結果を確認しましょう

---

## ⚙️ 環境準備

8-2-1で作成したDocker環境を使用します。

**Docker環境の起動**：

```bash
cd ~/mysql-practice
docker compose up -d
```

**phpMyAdminにアクセス**：

ブラウザで `http://localhost:8080` を開き、phpMyAdminが表示されることを確認してください。

> 💡 **ポイント**: phpMyAdminの「SQL」タブでSQL文を入力・実行します。

> 🚀 **ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: データベースの作成

```sql
CREATE DATABASE task_management CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

### ヒント2: テーブルの作成

```sql
CREATE TABLE tasks (
    task_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status ENUM('未着手', '進行中', '完了') DEFAULT '未着手',
    priority INT DEFAULT 3,
    due_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### ヒント3: データの挿入

```sql
INSERT INTO tasks (title, status, priority, due_date) VALUES
('データベース設計', '完了', 1, '2024-12-10');
```

### ヒント4: WHERE句の使い方

```sql
-- 条件付き検索
SELECT * FROM tasks WHERE status = '未着手';

-- 並び替え
SELECT * FROM tasks ORDER BY priority ASC;
```

### ヒント5: データの更新・削除

```sql
-- 更新
UPDATE tasks SET status = '完了' WHERE task_id = 2;

-- 削除
DELETE FROM tasks WHERE task_id = 4;
```

---

## 🏃 実践

ちゃんとできましたか？MySQLの基本操作はWebアプリケーション開発の基礎です。一緒に手を動かしながら、タスク管理システムのデータベースを構築していきましょう。

### 🧠 先輩エンジニアの思考プロセス

先輩エンジニアは要件を以下のように構造化し、実装タスクに落とし込みます：

| Step | やること | 説明 |
|:-----|:---------|:-----|
| 1 | データベースを作成する | `CREATE DATABASE`でデータの入れ物を用意 |
| 2 | テーブルを作成する | `CREATE TABLE`でカラム・データ型・制約を定義 |
| 3 | データを挿入する | `INSERT INTO`で初期データを登録 |
| 4 | データを取得する | `SELECT`で条件付き検索・並び替え |
| 5 | データを更新する | `UPDATE`でデータを変更（WHERE必須） |
| 6 | データを削除する | `DELETE`でデータを削除（WHERE必須） |

ポイントは「CRUD操作の各SQL文の構造を理解する」ことです。特にUPDATE/DELETEでは`WHERE`句を忘れると全データに影響するので注意が必要です。

---

### 📝 ステップバイステップで実装

#### ステップ1: データベースを作成する

**何を考えているか**：
- 「データベースはテーブルをまとめる入れ物」
- 「プロジェクトごとにデータベースを分けよう」
- 「文字コードはutf8mb4で統一しよう」

phpMyAdminの「SQL」タブで、以下のSQLを実行します：

```sql
CREATE DATABASE task_management CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

実行後、phpMyAdminの左ペインに`task_management`が表示されます。クリックして選択してください。

**コードリーディング**：

```sql
CREATE DATABASE task_management CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```
→ `CREATE DATABASE`文でデータベースを作成します。`CHARACTER SET utf8mb4`で文字コードを指定し、絵文字なども扱えるようにします。`COLLATE utf8mb4_general_ci`は文字列の比較方法を指定します。

---

#### ステップ2: テーブルを作成する

**何を考えているか**：
- 「タスクに必要な項目を洗い出そう」
- 「ID、タイトル、ステータス、優先度、期限を管理しよう」
- 「主キーはAUTO_INCREMENTで自動採番しよう」

`task_management`データベースを選択した状態で、「SQL」タブに以下を入力して実行します：

```sql
CREATE TABLE tasks (
    task_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status ENUM('未着手', '進行中', '完了') DEFAULT '未着手',
    priority INT DEFAULT 3,
    due_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**コードリーディング**：

```sql
task_id INT PRIMARY KEY AUTO_INCREMENT,
```
→ タスクIDを主キーとして定義し、自動採番します。データを挿入するたびに1, 2, 3...と番号が振られます。

```sql
title VARCHAR(200) NOT NULL,
```
→ タスクのタイトルを必須項目として定義します。

```sql
description TEXT,
```
→ 詳細説明をTEXT型で定義します。長い文章を格納できます。NULL許可なので、省略可能です。

```sql
status ENUM('未着手', '進行中', '完了') DEFAULT '未着手',
```
→ `ENUM`型でステータスを3つの値に制限します。`DEFAULT '未着手'`で、値を指定しない場合は自動的に「未着手」が設定されます。

```sql
priority INT DEFAULT 3,
```
→ 優先度を整数で定義し、デフォルトを3（低）に設定します。

```sql
created_at DATETIME DEFAULT CURRENT_TIMESTAMP
```
→ 作成日時を定義し、`DEFAULT CURRENT_TIMESTAMP`でデータ挿入時の日時が自動的に設定されます。

---

#### ステップ3: データを挿入する

**何を考えているか**：
- 「テストデータを複数件挿入しよう」
- 「カラム名を指定して、値を順番に渡そう」
- 「複数行を一度に挿入できる」

「SQL」タブで以下を実行します：

```sql
INSERT INTO tasks (title, status, priority, due_date) VALUES
('データベース設計', '完了', 1, '2024-12-10'),
('API開発', '進行中', 1, '2024-12-20'),
('テスト作成', '未着手', 2, '2024-12-25'),
('ドキュメント作成', '未着手', 3, '2024-12-30'),
('デプロイ準備', '未着手', 2, '2025-01-05');
```

**コードリーディング**：

```sql
INSERT INTO tasks (title, status, priority, due_date) VALUES
```
→ `INSERT INTO`文でtasksテーブルにデータを挿入します。括弧内にカラム名を指定し、`VALUES`以降に値を指定します。`task_id`はAUTO_INCREMENT、`description`はNULL許可、`created_at`はDEFAULT値があるため、指定する必要がありません。

```sql
('データベース設計', '完了', 1, '2024-12-10'),
('API開発', '進行中', 1, '2024-12-20'),
```
→ カンマで区切って複数行を一度に挿入できます。最後の行のみセミコロンで終わります。

挿入後、`SELECT * FROM tasks;` を実行して、5件のデータが挿入されたことを確認しましょう。

---

#### ステップ4: データを取得する

**何を考えているか**：
- 「全データを取得して確認しよう」
- 「条件を指定して絞り込み検索しよう」
- 「並び替えも試そう」

「SQL」タブで以下のSQLをそれぞれ実行します：

```sql
-- すべてのタスクを取得
SELECT * FROM tasks;

-- ステータスが「未着手」のタスクのみ取得
SELECT * FROM tasks WHERE status = '未着手';

-- 優先度が1（高）のタスクのみ取得
SELECT * FROM tasks WHERE priority = 1;

-- 優先度の高い順に並び替えて取得
SELECT * FROM tasks ORDER BY priority ASC;
```

**コードリーディング**：

```sql
SELECT * FROM tasks;
```
→ `SELECT`文でデータを取得します。`*`は全カラムを意味します。

```sql
SELECT * FROM tasks WHERE status = '未着手';
```
→ `WHERE`句で条件を指定します。ステータスが「未着手」のタスクのみを取得します。

```sql
SELECT * FROM tasks ORDER BY priority ASC;
```
→ `ORDER BY`句で並び替えを指定します。`priority ASC`で優先度の昇順（数値が小さい=優先度が高い順）に並べ替えます。`DESC`を使うと降順になります。

---

#### ステップ5: データを更新する

**何を考えているか**：
- 「特定のタスクのステータスを変更しよう」
- 「WHERE句で更新対象を特定しよう」
- 「WHEREを忘れると全データが更新されるので注意」

「SQL」タブで以下のSQLをそれぞれ実行します：

```sql
-- 「API開発」（task_id: 2）のステータスを「完了」に変更
UPDATE tasks SET status = '完了' WHERE task_id = 2;

-- 「テスト作成」（task_id: 3）のステータスと優先度を変更
UPDATE tasks SET status = '進行中', priority = 1 WHERE task_id = 3;
```

実行後、`SELECT * FROM tasks;` で変更が反映されていることを確認しましょう。

**コードリーディング**：

```sql
UPDATE tasks SET status = '完了' WHERE task_id = 2;
```
→ `UPDATE`文でデータを更新します。`SET`以降に更新するカラムと値を指定します。`WHERE task_id = 2`で対象レコードを特定します。

```sql
UPDATE tasks SET status = '進行中', priority = 1 WHERE task_id = 3;
```
→ 複数のカラムを同時に更新する場合、カンマで区切って指定します。

> ⚠️ **注意**: `WHERE`句を忘れると、テーブル内の**全レコード**が更新されてしまいます。UPDATE文を実行する前に、必ず`WHERE`句を確認しましょう。

---

#### ステップ6: データを削除する

**何を考えているか**：
- 「不要なタスクを削除しよう」
- 「WHERE句で削除対象を特定しよう」
- 「削除は復元できないので慎重に」

「SQL」タブで以下のSQLを実行します：

```sql
-- 「ドキュメント作成」（task_id: 4）を削除
DELETE FROM tasks WHERE task_id = 4;
```

**コードリーディング**：

```sql
DELETE FROM tasks WHERE task_id = 4;
```
→ `DELETE FROM`文でデータを削除します。`WHERE task_id = 4`で対象レコードを特定します。

> ⚠️ **注意**: `WHERE`句を忘れると、テーブル内の**全データ**が削除されてしまいます。DELETE文を実行する前に、`SELECT`文で対象データを確認してから削除すると安全です。

---

### ✨ 完成！

これでタスク管理システムのデータベース構築とCRUD操作が完成しました！

最後に `SELECT * FROM tasks;` を実行して、以下の結果になっていることを確認しましょう：

**最終データ確認**：

| task_id | title | status | priority | due_date |
|---------|-------|--------|----------|----------|
| 1 | データベース設計 | 完了 | 1 | 2024-12-10 |
| 2 | API開発 | 完了 | 1 | 2024-12-20 |
| 3 | テスト作成 | 進行中 | 1 | 2024-12-25 |
| 5 | デプロイ準備 | 未着手 | 2 | 2025-01-05 |

→ 「API開発」が「完了」に、「テスト作成」が「進行中」（優先度1）に変更され、「ドキュメント作成」（task_id: 4）が削除されていれば成功です！

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### 1. データベースの作成

```sql
CREATE DATABASE task_management CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

> 📌 phpMyAdminの左ペインで`task_management`をクリックして選択してから、以下を実行してください。

### 2. テーブルの作成

```sql
CREATE TABLE tasks (
    task_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    status ENUM('未着手', '進行中', '完了') DEFAULT '未着手',
    priority INT DEFAULT 3,
    due_date DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 3. データの挿入

```sql
INSERT INTO tasks (title, status, priority, due_date) VALUES
('データベース設計', '完了', 1, '2024-12-10'),
('API開発', '進行中', 1, '2024-12-20'),
('テスト作成', '未着手', 2, '2024-12-25'),
('ドキュメント作成', '未着手', 3, '2024-12-30'),
('デプロイ準備', '未着手', 2, '2025-01-05');
```

### 4. データの取得

```sql
-- すべてのタスクを取得
SELECT * FROM tasks;

-- ステータスが「未着手」のタスクのみ
SELECT * FROM tasks WHERE status = '未着手';

-- 優先度が1（高）のタスクのみ
SELECT * FROM tasks WHERE priority = 1;

-- 優先度の高い順に並び替え
SELECT * FROM tasks ORDER BY priority ASC;
```

### 5. データの更新

```sql
-- 「API開発」のステータスを「完了」に変更
UPDATE tasks SET status = '完了' WHERE task_id = 2;

-- 「テスト作成」のステータスと優先度を変更
UPDATE tasks SET status = '進行中', priority = 1 WHERE task_id = 3;
```

### 6. データの削除

```sql
-- 「ドキュメント作成」タスクを削除
DELETE FROM tasks WHERE task_id = 4;
```

---

## 🔍 よくある間違い

### 間違い1: WHERE句の忘れ

```sql
-- ❌ 間違い（すべてのタスクが「完了」になる）
UPDATE tasks SET status = '完了';

-- ✅ 正しい
UPDATE tasks SET status = '完了' WHERE task_id = 2;
```

### 間違い2: シングルクォートの忘れ

```sql
-- ❌ 間違い
SELECT * FROM tasks WHERE status = 未着手;

-- ✅ 正しい
SELECT * FROM tasks WHERE status = '未着手';
```

### 間違い3: カラム名のスペルミス

```sql
-- ❌ 間違い
SELECT * FROM tasks WHERE titel = 'API開発';

-- ✅ 正しい
SELECT * FROM tasks WHERE title = 'API開発';
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ CREATE TABLE文でテーブルを作成できる
- ✅ INSERT文でデータを挿入できる
- ✅ SELECT文でデータを取得できる
- ✅ UPDATE文でデータを更新できる
- ✅ DELETE文でデータを削除できる

### 🧹 後片付け（任意）

このハンズオンで作成した`task_management`データベースは、演習専用のデータベースです。次のChapter以降では使用しません。

phpMyAdminの左ペインを整理したい場合は、以下のSQLでデータベースを削除できます。ただし、削除すると元に戻せないので、注意してください。

```sql
DROP DATABASE task_management;
```

> 💡 **ポイント**：`practice_db`データベースは、Chapter 3以降でも使用するので、削除しないでください。

---
