# Tutorial 8-2-7: MySQL基本操作 - ハンズオン演習

## 📝 このセクションの目的

Chapter 2で学んだMySQL基本操作を実際に手を動かして確認します。phpMyAdminを使って、テーブルの作成からデータの挿入・取得・更新・削除まで一連の操作を行いましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

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

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: データベースの作成

phpMyAdminの左側メニューから「新規作成」をクリックし、データベース名を入力して「作成」をクリック。

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

### ヒント4: データの取得

```sql
-- すべてのタスクを取得
SELECT * FROM tasks;

-- ステータスが「未着手」のタスクのみ
SELECT * FROM tasks WHERE status = '未着手';

-- 優先度順に並び替え
SELECT * FROM tasks ORDER BY priority ASC;
```

### ヒント5: データの更新

```sql
UPDATE tasks SET status = '完了' WHERE title = 'API開発';
```

### ヒント6: データの削除

```sql
DELETE FROM tasks WHERE title = 'ドキュメント作成';
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？MySQLの基本操作はWebアプリケーション開発の基礎です。一緒に手を動かしながら、タスク管理システムのデータベースを構築していきましょう。

### 💭 実装の思考プロセス

タスク管理システムのデータベースを構築する際、以下の順番で考えると効率的です：

1. **データベースを作成**：まずは器（データベース）を用意
2. **テーブルを設計・作成**：データを格納する構造を定義
3. **データを挿入**：INSERT文で初期データを登録
4. **データを検索**：SELECT文でデータを取得・確認
5. **データを更新**：UPDATE文でデータを変更
6. **データを削除**：DELETE文で不要なデータを削除

CRUD操作のポイントは「各操作の役割とSQL文の構造を理解する」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: データベースを作成する

**何を考えているか**：
- 「データベースはテーブルをまとめる入れ物」
- 「プロジェクトごとにデータベースを分けよう」
- 「文字コードはutf8mb4で統一しよう」

まず、データベースを作成します：

```sql
CREATE DATABASE task_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE task_management;
```

**コードリーディング**：

```sql
CREATE DATABASE task_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
→ `CREATE DATABASE`文でデータベースを作成します。`CHARACTER SET utf8mb4`で文字コードを指定し、絵文字なども扱えるようにします。`COLLATE utf8mb4_unicode_ci`は文字列の比較方法を指定します。

```sql
USE task_management;
```
→ `USE`文で作成したデータベースを選択します。これ以降のSQL文はこのデータベースに対して実行されます。

---

#### ステップ2: テーブルを作成する

**何を考えているか**：
- 「タスクに必要な項目を洗い出そう」
- 「ID、タイトル、ステータス、優先度、期限を管理しよう」
- 「主キーはAUTO_INCREMENTで自動採番しよう」

次に、tasksテーブルを作成します：

```sql
CREATE TABLE tasks (
    task_id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    status VARCHAR(50) DEFAULT '未着手',
    priority INT DEFAULT 3,
    due_date DATE
);
```

**コードリーディング**：

```sql
CREATE TABLE tasks (
```
→ `CREATE TABLE`文でtasksテーブルを作成します。

```sql
    task_id INT PRIMARY KEY AUTO_INCREMENT,
```
→ タスクIDを主キーとして定義し、自動採番します。データを挿入するたびに1, 2, 3...と番号が振られます。

```sql
    title VARCHAR(200) NOT NULL,
```
→ タスクのタイトルを必須項目として定義します。

```sql
    status VARCHAR(50) DEFAULT '未着手',
```
→ ステータスを定義し、`DEFAULT '未着手'`でデフォルト値を設定します。値を指定しない場合、自動的に「未着手」が設定されます。

```sql
    priority INT DEFAULT 3,
```
→ 優先度を整数で定義し、デフォルトを3（低）に設定します。

```sql
    due_date DATE
);
```
→ 期限をDATE型で定義します。任意項目なので、NULLを許可します。

---

#### ステップ3: データを挿入する

**何を考えているか**：
- 「テストデータを複数件挿入しよう」
- 「カラム名を指定して、値を順番に渡そう」
- 「複数行を一度に挿入できる」

次に、データを挿入します：

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
→ `INSERT INTO`文でtasksテーブルにデータを挿入します。括弧内にカラム名を指定し、`VALUES`以降に値を指定します。

```sql
('データベース設計', '完了', 1, '2024-12-10'),
```
→ 1行目のデータを挿入します。カラムの順番に合わせて値を指定します。`task_id`はAUTO_INCREMENTなので、指定する必要がありません。

```sql
('API開発', '進行中', 1, '2024-12-20'),
...
```
→ カンマで区切って複数行を一度に挿入できます。最後の行のみセミコロンで終わります。

---

#### ステップ4: データを検索する

**何を考えているか**：
- 「全データを取得して確認しよう」
- 「条件を指定して絞り込み検索しよう」
- 「並び替えや件数制限も試そう」

次に、データを検索します：

```sql
-- 全データを取得
SELECT * FROM tasks;

-- 優先度が1のタスクを取得
SELECT * FROM tasks WHERE priority = 1;

-- 未着手のタスクを期限順に並べ替え
SELECT * FROM tasks WHERE status = '未着手' ORDER BY due_date ASC;
```

**コードリーディング**：

```sql
SELECT * FROM tasks;
```
→ `SELECT`文でデータを取得します。`*`は全カラムを意味します。`FROM tasks`でtasksテーブルからデータを取得します。

```sql
SELECT * FROM tasks WHERE priority = 1;
```
→ `WHERE`句で条件を指定します。`priority = 1`で優先度が1のタスクのみを取得します。

```sql
SELECT * FROM tasks WHERE status = '未着手' ORDER BY due_date ASC;
```
→ `ORDER BY`句で並び替えを指定します。`due_date ASC`で期限の昇順（古い順）に並べ替えます。`DESC`を使うと降順になります。

---

#### ステップ5: データを更新する

**何を考えているか**：
- 「特定のタスクのステータスを変更しよう」
- 「WHERE句で更新対象を特定しよう」
- 「WHEREを忘れると全データが更新されるので注意」

次に、データを更新します：

```sql
-- task_idで2のタスクを完了に変更
UPDATE tasks SET status = '完了' WHERE task_id = 2;

-- task_idで3のタスクのステータスと優先度を変更
UPDATE tasks SET status = '進行中', priority = 1 WHERE task_id = 3;
```

**コードリーディング**：

```sql
UPDATE tasks SET status = '完了' WHERE task_id = 2;
```
→ `UPDATE`文でデータを更新します。`SET`以降に更新するカラムと値を指定します。`WHERE task_id = 2`でtask_idで2のレコードのみを更新します。

```sql
UPDATE tasks SET status = '進行中', priority = 1 WHERE task_id = 3;
```
→ 複数のカラムを同時に更新する場合、カンマで区切って指定します。

---

#### ステップ6: データを削除する

**何を考えているか**：
- 「不要なタスクを削除しよう」
- 「WHERE句で削除対象を特定しよう」
- 「削除は復元できないので慎重に」

最後に、データを削除します：

```sql
-- task_idで4のタスクを削除
DELETE FROM tasks WHERE task_id = 4;
```

**コードリーディング**：

```sql
DELETE FROM tasks WHERE task_id = 4;
```
→ `DELETE FROM`文でデータを削除します。`WHERE task_id = 4`でtask_idで4のレコードのみを削除します。**重要**：`WHERE`句を忘れると、テーブル内の全データが削除されてしまうので注意が必要です。

---

### ✨ 完成！

これでタスク管理システムのデータベース構築とCRUD操作が完成しました！CREATE、INSERT、SELECT、UPDATE、DELETEの各SQL文を実践できましたね。

---

## ✅ 完成イメージ

### 初期データ挿入後

| task_id | title | status | priority | due_date |
|---------|-------|--------|----------|----------|
| 1 | データベース設計 | 完了 | 1 | 2024-12-10 |
| 2 | API開発 | 進行中 | 1 | 2024-12-20 |
| 3 | テスト作成 | 未着手 | 2 | 2024-12-25 |
| 4 | ドキュメント作成 | 未着手 | 3 | 2024-12-30 |
| 5 | デプロイ準備 | 未着手 | 2 | 2025-01-05 |

### 更新・削除後

| task_id | title | status | priority | due_date |
|---------|-------|--------|----------|----------|
| 1 | データベース設計 | 完了 | 1 | 2024-12-10 |
| 2 | API開発 | 完了 | 1 | 2024-12-20 |
| 3 | テスト作成 | 進行中 | 1 | 2024-12-25 |
| 5 | デプロイ準備 | 未着手 | 2 | 2025-01-05 |

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### 1. データベースとテーブルの作成

```sql
-- データベースの作成
CREATE DATABASE task_management;

-- データベースの選択
USE task_management;

-- テーブルの作成
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

### 2. データの挿入

```sql
INSERT INTO tasks (title, status, priority, due_date) VALUES
('データベース設計', '完了', 1, '2024-12-10'),
('API開発', '進行中', 1, '2024-12-20'),
('テスト作成', '未着手', 2, '2024-12-25'),
('ドキュメント作成', '未着手', 3, '2024-12-30'),
('デプロイ準備', '未着手', 2, '2025-01-05');
```

### 3. データの取得

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

### 4. データの更新

```sql
-- 「API開発」のステータスを「完了」に変更
UPDATE tasks SET status = '完了' WHERE title = 'API開発';

-- 「テスト作成」のステータスと優先度を変更
UPDATE tasks SET status = '進行中', priority = 1 WHERE title = 'テスト作成';
```

### 5. データの削除

```sql
-- 「ドキュメント作成」タスクを削除
DELETE FROM tasks WHERE title = 'ドキュメント作成';
```

---

---

## 🔍 よくある間違い

### 間違い1: WHERE句の忘れ

```sql
-- ❌ 間違い（すべてのタスクが「完了」になる）
UPDATE tasks SET status = '完了';

-- ✅ 正しい
UPDATE tasks SET status = '完了' WHERE title = 'API開発';
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

引き続き、次のセクションも頑張りましょう！

---

## 🧹 後片付け（任意）

このハンズオンで作成した`task_management`データベースは、演習専用のデータベースです。次のChapter以降では使用しません。

phpMyAdminの左ペインを整理したい場合は、以下のSQLでデータベースを削除できます。ただし、削除すると元に戻せないので、注意してください。

```sql
DROP DATABASE task_management;
```

> 💡 **ポイント**：`practice_db`データベースは、Chapter 3以降でも使用するので、削除しないでください。

---
