# Tutorial 8-2-7: MySQL基本操作 - ハンズオン演習

## 📝 このセクションの目的

Chapter 2で学んだMySQL基本操作を実際に手を動かして確認します。phpMyAdminを使って、テーブルの作成からデータの挿入・取得・更新・削除まで一連の操作を行いましょう。

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
4. 期限が2024年12月中のタスクを取得
5. タスクを優先度の高い順に並び替えて取得

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

## 🚀 チャレンジ

基本要件をクリアしたら、以下の追加課題にも挑戦してみましょう。

1. **カテゴリ追加**：タスクにカテゴリカラムを追加

2. **担当者管理**：担当者テーブルを作成し、外部キーで関連付け

3. **検索機能**：タイトルに特定の文字列を含むタスクを検索（LIKE句）

4. **集計機能**：ステータスごとのタスク数を集計（COUNT、GROUP BY）

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

-- 期限が2024年12月中のタスク
SELECT * FROM tasks WHERE due_date BETWEEN '2024-12-01' AND '2024-12-31';

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

## 🎓 解説

### ポイント1: ENUM型

```sql
status ENUM('未着手', '進行中', '完了') DEFAULT '未着手'
```

- 選択肢を限定できる
- デフォルト値を設定可能
- データの整合性を保てる

### ポイント2: CURRENT_TIMESTAMP

```sql
created_at DATETIME DEFAULT CURRENT_TIMESTAMP
```

- レコード作成時に自動的に現在日時が設定される
- 手動で日時を入力する必要がない

### ポイント3: WHERE句

```sql
SELECT * FROM tasks WHERE status = '未着手';
```

- 条件に一致するレコードのみを取得
- `=`、`<`、`>`、`BETWEEN`などの演算子が使える

### ポイント4: ORDER BY句

```sql
SELECT * FROM tasks ORDER BY priority ASC;
```

- `ASC`: 昇順（小さい順）
- `DESC`: 降順（大きい順）
- 複数のカラムで並び替えも可能

### ポイント5: UPDATE文の注意点

```sql
UPDATE tasks SET status = '完了' WHERE title = 'API開発';
```

- **WHERE句を忘れると、すべてのレコードが更新される**
- 必ず条件を指定する

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

## 📚 次のステップ

MySQL基本操作をマスターしたら、次はリレーションシップとJOINを学びましょう！

Chapter 3では、複数のテーブルを結合して、より複雑なデータを取得する方法を学びます。

---

## 💪 自己評価チェックリスト

以下の項目ができたかチェックしましょう：

- [ ] CREATE DATABASE文でデータベースを作成できた
- [ ] CREATE TABLE文でテーブルを作成できた
- [ ] INSERT文でデータを挿入できた
- [ ] SELECT文でデータを取得できた
- [ ] WHERE句で条件を指定できた
- [ ] ORDER BY句で並び替えができた
- [ ] UPDATE文でデータを更新できた
- [ ] DELETE文でデータを削除できた

すべてチェックできたら、Chapter 3に進みましょう！
