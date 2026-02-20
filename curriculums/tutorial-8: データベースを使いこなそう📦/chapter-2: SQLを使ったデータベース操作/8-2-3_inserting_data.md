# Tutorial 8-2-3: データの挿入（INSERT）

## 🎯 このセクションで学ぶこと

*   `INSERT` 文を使って、テーブルに新しいレコード（データ）を追加できるようになる。
*   `INSERT` 文の基本的な2つの構文（カラム名を指定する方法としない方法）を理解する。
*   一度に複数のレコードを挿入する方法を知る。
*   phpMyAdminのGUIを使ってデータを挿入する方法も知る。

---

## 導入

前のセクションで、`CREATE` 文を使って`users` テーブルという「空の住所録」を作成しました。しかし、現時点ではまだ誰も登録されていません。このセクションでは、DML（データ操作言語）の一つである**`INSERT`** 文を使って、このテーブルに最初のユーザーデータを追加する方法を学びます。

`INSERT` は、その名の通り、テーブルに新しい行（レコード）を「挿入（insert）」するためのコマンドです。ここから、データベースが単なる構造から、意味のある情報を持つ存在へと変わっていきます。

---

## 詳細解説

### 👤 1件のデータを挿入する (`INSERT INTO ... VALUES`)

`INSERT` 文の最も基本的な構文は以下の通りです。

```sql
INSERT INTO table_name (column1, column2, column3, ...)
VALUES (value1, value2, value3, ...);
```

*   `INSERT INTO table_name`: どのテーブルにデータを挿入するかを指定します。
*   `(column1, column2, ...)`: どのカラムに値を設定するかを列挙します。
*   `VALUES (value1, value2, ...)`: 上記で指定したカラムに対応する値を列挙します。

それでは、実際に`users` テーブルに1件のユーザーデータを追加してみましょう。

```sql
INSERT INTO users (name, email, password)
VALUES ('John Doe', 'john.doe@example.com', 'password123');
```

このSQL文を分解してみましょう。

*   `INSERT INTO users`: `users` テーブルに挿入します。
*   `(name, email, password)`: `name`, `email`, `password` の3つのカラムに値を設定します。
*   `VALUES ('John Doe', 'john.doe@example.com', 'password123')`: `name` には `'John Doe'` を、`email` には `'john.doe@example.com'` を、`password` には `'password123'` をそれぞれ設定します。

**`id`、`created_at`、`updated_at` はどうなった？**

`CREATE TABLE` の際に、以下の設定をしました。

*   `id` カラム: `AUTO_INCREMENT` を設定
*   `created_at` カラム: `DEFAULT CURRENT_TIMESTAMP` を設定
*   `updated_at` カラム: `DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP` を設定

そのため、`INSERT` 文でこれらの値を指定しなくても、MySQLが自動的に適切な値を設定してくれます。

*   `id`: 自動で`1` が割り振られます。
*   `created_at`: このSQLが実行された日時が自動で記録されます。
*   `updated_at`: このSQLが実行された日時が自動で記録されます。

#### カラム名を省略する構文

もし、テーブルの全てのカラムに対して順番通りに値を指定する場合は、カラムリストを省略することもできます。

```sql
-- この構文は、あまり推奨されない
INSERT INTO users
VALUES (2, 'Jane Smith', 'jane.smith@example.com', 'password456', NOW(), NOW());
```

この構文は、`CREATE TABLE` で定義されたカラムの順番（`id`, `name`, `email`, `password`, `created_at`, `updated_at`）を正確に覚えておく必要があります。`NOW()` は現在日時を返すMySQLの関数です。

**なぜ、推奨されないのか？**

将来的にテーブルのカラムの順番が変わったり、新しいカラムが追加されたりした場合、このSQL文はエラーになるか、意図しないカラムにデータが入ってしまう可能性があります。そのため、**カラム名を明示的に指定する最初の構文の方が安全で可読性も高い**と言えます。

### 👥 複数のデータを一度に挿入する

`VALUES` 句の後にカンマで区切って値のセットを複数記述することで、一度の`INSERT` 文で複数のレコードを挿入することができます。その方が何度も`INSERT` 文を実行するよりも効率的です。

```sql
INSERT INTO users (name, email, password)
VALUES
    ('Alice', 'alice@example.com', 'pass_alice'),
    ('Bob', 'bob@example.com', 'pass_bob'),
    ('Charlie', 'charlie@example.com', 'pass_charlie');
```

この1つのSQL文で、3人のユーザーが`users` テーブルに追加されます。

**phpMyAdminでの実行と確認**

1.  phpMyAdminで、`practice_db` データベースを選択します。
2.  「SQL」タブを開き、上記の`INSERT` 文を実行します。
3.  成功したら、「表示」タブをクリックします。

<img alt="8-2-3_1.png" src="">

`id` が自動で連番になっていること、`created_at` と `updated_at` に日時が入っていること、そして指定した`name`, `email`, `password` が正しく格納されていることを確認できます。

#### GUIでのデータ挿入

phpMyAdminでは、GUI操作でデータを挿入することもできます。

1.  `users` テーブルを選択します。
2.  上部の「挿入」タブをクリックします。
3.  各カラムに対応する入力フォームが表示されます。

<img alt="8-2-3_2.png" src="">

*   **値**: 挿入したいデータを入力します。（`id` は自動採番なので、空のままでOKです）
*   **関数**: `created_at` や `updated_at` のように日時を入れたい場合、プルダウンから`NOW()` を選択することができます。

フォームに値を入力し、「実行」ボタンを押すと、データが挿入されます。この時も、phpMyAdminが生成した`INSERT` 文が表示されるので、SQLの学習に役立てましょう。

---

## ✨ まとめ

このセクションでは、`INSERT` 文を使ってテーブルに新しいデータを追加する方法を学びました。

*   テーブルにデータを追加するには、`INSERT INTO ... VALUES ...` 文を使う。
*   安全性のために、挿入するカラム名を明示的に指定する構文が推奨される。
*   `AUTO_INCREMENT` や `DEFAULT` が設定されたカラムは、値を指定しなくても自動で補完される。
*   `VALUES` 句に複数の値のセットを記述することで、一度に複数のレコードを挿入できる。
*   phpMyAdminの「挿入」タブを使えば、GUIで直感的にデータを追加できる。

これで、データベースにデータを蓄積する方法がわかりました。しかし、ただ入れるだけでは意味がありません。次のセクションでは、データベースの真骨頂とも言えるデータの取得（検索）を行う`SELECT` 文について学んでいきます。

---
