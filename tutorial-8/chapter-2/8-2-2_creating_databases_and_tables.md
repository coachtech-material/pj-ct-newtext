""
# Tutorial 8-2-2: データベースとテーブルの作成（CREATE）

## 🎯 このセクションで学ぶこと

*   `CREATE DATABASE` 文を使って、新しい、データベースを、作成できるようになる。
*   `CREATE TABLE` 文を使って、新しい、テーブルを、作成できるようになる。
*   テーブル作成時に、カラム名と、データ型を、指定する方法を、理解する。
*   `PRIMARY KEY` や `AUTO_INCREMENT` といった、制約の、基本的な、設定方法を、理解する。
*   phpMyAdminの、GUIを、使って、データベースと、テーブルを、作成する、方法も、知る。

---

## 導入

データベースを、操作するための、言語である、SQL（Structured Query Language）は、大きく、4つの、カテゴリに、分類されます。

1.  **DDL (Data Definition Language)**: データ定義言語
    *   `CREATE`, `ALTER`, `DROP` など。データベースや、テーブルの、構造そのものを、定義・変更・削除する。
2.  **DML (Data Manipulation Language)**: データ操作言語
    *   `INSERT`, `UPDATE`, `DELETE` など。テーブル内の、レコード（データ）を、操作する。
3.  **DQL (Data Query Language)**: データ問い合わせ言語
    *   `SELECT`。テーブルから、データを、取得（検索）する。
4.  **DCL (Data Control Language)**: データ制御言語
    *   `GRANT`, `REVOKE` など。ユーザーの、アクセス権限を、制御する。

このセクションでは、まず、DDLの、最も、基本的な、コマンドである、**`CREATE`** を、使って、データベースと、テーブルという、「データの、器」を、作成する方法を学びます。

家を、建てる前に、土地を、用意し、部屋の、間取りを、決めるように、データを、格納する前に、まずは、その、土台となる、データベースと、テーブルの、構造を、定義する必要があるのです。

---

## 詳細解説

### 📦 データベースの作成 (`CREATE DATABASE`)

まず、最初に、プロジェクトの、データを、まとめて、格納しておくための、「大きな箱」である、データベースを、作成します。

SQL文は、非常に、シンプルです。

```sql
CREATE DATABASE sample_db;
```

これは、「`sample_db` という、名前の、データベースを、作成してください」という、命令です。

#### 文字コードと照合順序

実際には、日本語のような、マルチバイト文字を、正しく、扱うために、**文字コード**と、**照合順序**を、指定するのが、一般的です。

*   **文字コード (Character Set)**: どの、文字の、種類を、使うかの、ルール。`utf8mb4` を、指定しておけば、絵文字なども、含めて、ほぼ、全ての、文字を、扱うことができます。
*   **照合順序 (Collation)**: 文字を、並べ替えたり、比較したりする際の、ルール。`utf8mb4_general_ci` は、大文字と、小文字を、区別しない（case-insensitive）という、一般的な、ルールです。

これらを、指定した、完全な、コマンドは、以下のようになります。

```sql
CREATE DATABASE sample_db CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```

> 💡 **ポイント**: Tutorial 8-2-1で、Docker環境を、構築した際に、`practice_db`という、データベースが、すでに、自動作成されています。このセクションでは、その`practice_db`を、使用して、学習を、進めます。

**phpMyAdminでの確認手順**

1.  phpMyAdminに、アクセスします（`http://localhost:8080`）。
2.  左ペインの、データベース一覧に、`practice_db` が、表示されていることを、確認します。

この`practice_db`は、`docker-compose.yml`の、`MYSQL_DATABASE: practice_db`という、設定によって、MySQLコンテナ起動時に、自動的に、作成されたものです。

### 📝 テーブルの作成 (`CREATE TABLE`)

データベースという、「土地」が、用意できたら、次はその上に、「家」（テーブル）を、建てていきます。

ここでは、ユーザー情報を、格納する、`users`テーブルを、作成してみましょう。テーブル作成の、`CREATE TABLE` 文は、少し、複雑になります。

```sql
CREATE TABLE users (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
```

> 💡 **ポイント**：`id`カラムに`BIGINT UNSIGNED`を使用しています。これは、Laravelのマイグレーションがデフォルトで使用する形式です。後のセクションで、このテーブルを参照する外部キーを作成する際に、型を一致させる必要があります。

この、SQL文を、分解して、見ていきましょう。

*   `CREATE TABLE users (...)`: `users` という、名前の、テーブルを、作成します。`()` の中に、カラムの、定義を、記述していきます。
*   `id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT`: `id` という、名前の、カラムを、作成します。
    *   `BIGINT UNSIGNED`: データ型は、符号なしの大きな整数です。Laravelのデフォルト形式で、外部キーとの型一致に重要です。
    *   `NOT NULL`: NULL値を、許可しません。
    *   `AUTO_INCREMENT`: 新しい、レコードが、追加されるたびに、自動で、連番を、割り振ります。
*   `PRIMARY KEY (id)`: `id`カラムを、主キーに、設定します。
*   `name VARCHAR(255) NOT NULL`: `name` という、名前の、カラムを、作成します。
    *   `VARCHAR(255)`: データ型は、最大255文字の、可変長文字列です。
    *   `NOT NULL`: このカラムに、NULL（空の値）を、許可しません。必ず、何らかの、値を、入力する必要があります。
*   `email VARCHAR(255) NOT NULL UNIQUE`: `email` という、名前の、カラムを、作成します。
    *   `UNIQUE`: このカラムの値は、テーブル内で、重複してはならない、という、一意性制約を、設定します。同じ、メールアドレスで、複数の、ユーザーが、登録されるのを、防ぎます。
*   `password VARCHAR(255) NOT NULL`: `password` という、名前の、カラムを、作成します。
*   `created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP`: `created_at` という、名前の、カラムを、作成します。
    *   `TIMESTAMP`: データ型は、タイムスタンプです。
    *   `DEFAULT CURRENT_TIMESTAMP`: レコードが、作成された際に、自動的に、現在の日時を、設定します。
*   `updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP`: `updated_at` という、名前の、カラムを、作成します。
    *   `ON UPDATE CURRENT_TIMESTAMP`: レコードが、更新された際に、自動的に、現在の日時を、設定します。

**phpMyAdminでの実行手順**

1.  左ペインで、`practice_db` データベースを、クリックして、選択状態にします。（重要！）
2.  上部の、「SQL」タブを、クリックします。
3.  上記の、`CREATE TABLE` 文を、テキストエリアに、貼り付けます。
4.  「実行」ボタンを、クリックします。

成功すると、左ペインの、`practice_db` の下に、`users` テーブルが、表示されます。

#### GUIでのテーブル作成

phpMyAdminでは、SQLを、書かずに、GUI操作で、テーブルを、作成することもできます。

1.  `practice_db` データベースを、選択します。
2.  メインコンテンツエリアに、表示される、「テーブルを作成」の、フォームに、テーブル名（例: `posts`）と、カラム数を、入力して、「実行」を、クリックします。
3.  次の画面で、各カラムの、「名前」「データ型」「長さ/値」「デフォルト値」「インデックス（主キーなど）」「A_I（オートインクリメント）」などを、フォームに、入力・選択していきます。

**[ここに、GUIでの、テーブル作成画面の、スクリーンショットを、挿入]**

この方法は、直感的で、分かりやすいですが、どのような、`CREATE TABLE` 文が、生成されるのかを、意識することが、重要です。GUIで、作成した後に、phpMyAdminが、表示する、SQL文を、確認する癖を、つけておくと、学習効果が、高まります。

---

## ✨ まとめ

このセクションでは、DDLの、`CREATE` 文を使って、データベースと、テーブルを、作成する方法を学びました。

*   データベースを、作成するには、`CREATE DATABASE` 文を、使う。
    *   日本語を、扱うために、文字コード (`utf8mb4`) と、照合順序 (`utf8mb4_general_ci`) を、指定することが、推奨される。
*   テーブルを、作成するには、`CREATE TABLE` 文を、使う。
    *   `()` の中に、各カラムの、**名前**、**データ型**、そして、**制約**（`PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `AUTO_INCREMENT`, `DEFAULT` など）を、定義していく。
*   これらの、操作は、phpMyAdminの、GUIを、使っても、行うことができるが、裏側で、どのような、SQLが、実行されているかを、意識することが、大切。

これで、ようやく、データを入れるための、「器」が、準備できました。次のセクションでは、いよいよ、この、`users`テーブルに、実際の、データを、追加していく、DMLの、`INSERT` 文を、学んでいきます。

---
