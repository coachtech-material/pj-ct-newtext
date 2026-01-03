
# Tutorial 8-3-4: 多対多のリレーションシップ - 中間テーブルを使いこなす

## 🎯 このセクションで学ぶこと

*   「多対多」のリレーションシップがどのような場面で必要になるかを理解する。
*   なぜ多対多の関係を表現するために「中間テーブル（ピボットテーブル）」が必要なのかを説明できるようになる。
*   `posts`（投稿）と`tags`（タグ）を例に、中間テーブル`post_tag`をSQLで作成できるようになる。
*   中間テーブルに複合ユニークキーを設定し、データの重複を防ぐ方法を理解する。
*   中間テーブルにデータを`INSERT`することで、多対多の関連付けを実際に作成できるようになる。

---

## 導入：投稿に複数のタグを付けたい！

1対多のリレーションシップを実装し、ユーザーと投稿を関連付けることができました。では、次のような要求が来たらどう対応すればよいでしょうか？

> 「ブログの投稿に、複数の『タグ』を付けられるようにしたい。例えば、ある投稿には『PHP』と『Laravel』の両方のタグを付けたい。また、『PHP』というタグが付いた投稿を一覧表示できるようにしたい。」

この関係性を考えてみましょう。

*   **1つ**の投稿は、**複数**のタグを持つことができる。（例: 投稿Aに #PHP, #Laravel）
*   **1つ**のタグは、**複数**の投稿で使われることがある。（例: #PHPタグが投稿Aと投稿Bの両方に付く）

このように、お互いが「多」の関係にあるのが**多対多（Many-to-Many）**リレーションシップです。

この関係は、`posts`テーブルに`tag_id`カラムを追加するだけでは表現できません。もし`tag_id`を置くと、1つの投稿に1つのタグしか紐付けられないからです。かといって`tag_id1`, `tag_id2`...とカラムを増やしていくのは、付けられるタグの数が固定されてしまい、非常に柔軟性のない設計（アンチパターン）です。

この問題をエレガントに解決するのが、**中間テーブル（Intermediate Table）**、またはLaravelの世界では**ピボットテーブル（Pivot Table）**と呼ばれる第三のテーブルです。

---

## 詳細解説

### 1. 中間テーブルによる解決策

多対多の関係は、2つの「1対多」の関係に分解することで表現できます。その中心的な役割を果たすのが中間テーブルです。

*   `posts`テーブルと`tags`テーブルを用意する。
*   その間に、両者をつなぐためだけの`post_tag`テーブルを置く。

この`post_tag`テーブルは、どの投稿（`post_id`）とどのタグ（`tag_id`）が関連付いているか、という情報だけをペアで記録します。

*   `posts`と`post_tag`の関係は「1対多」です。（1つの投稿は、`post_tag`テーブルに複数のレコードを持つことができる）
*   `tags`と`post_tag`の関係も「1対多」です。（1つのタグは、`post_tag`テーブルに複数のレコードを持つことができる）

**[ここに、posts, post_tag, tagsの3つのエンティティが描かれたER図を挿入。post_tagが中央にあり、postsとtagsの両方から「1対多」の線が引かれている図]**

### 2. テーブルのSQL実装

それでは、実際に`tags`テーブルと`post_tag`テーブルをSQLで作成してみましょう。

#### `tags`テーブルの作成

まずはタグそのものを格納するシンプルなテーブルです。

```sql
CREATE TABLE tags (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id)
);
```
*   `name`カラムに`UNIQUE`制約を付けているのがポイントです。これにより、「PHP」というタグが2つ登録されるのを防ぎます。

#### `post_tag`中間テーブルの作成

次に、このセクションの主役である中間テーブルを作成します。

```sql
CREATE TABLE post_tag (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    post_id BIGINT UNSIGNED NOT NULL,
    tag_id BIGINT UNSIGNED NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),

    -- 外部キー制約
    FOREIGN KEY (post_id) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,

    -- 複合ユニークキー制約
    UNIQUE KEY post_tag_unique (post_id, tag_id)
);
```

このSQL文には重要な点が3つあります。

1.  **2つの外部キー**: `post_id`が`posts`テーブルの`id`を、`tag_id`が`tags`テーブルの`id`をそれぞれ参照しています。これにより、存在しない投稿やタグとの関連付けを防ぎます。
2.  **両方に`ON DELETE CASCADE`**: `posts`のレコードが削除されたら、この中間テーブルの関連レコードも削除。同様に、`tags`のレコードが削除されたら、関連レコードも削除。データの整合性を保ちます。
3.  **複合ユニークキー**: `UNIQUE KEY post_tag_unique (post_id, tag_id)` この一行が非常に重要です。これは、「`post_id`と`tag_id`の**組み合わせ**が重複してはならない」という制約です。これにより、1つの投稿に同じタグが2回紐付けられる、といった無駄なデータが登録されるのを防ぎます。

### 3. SQLの実行とデータの登録

1.  phpMyAdminで、上記の`CREATE TABLE`文を`tags`、`post_tag`の順に実行します。
2.  デザイナービューで、3つのテーブルが正しく関連付いていることを確認しましょう。
3.  次に、サンプルデータを登録して、多対多の関係を実際に作ってみます。

```sql
-- タグを登録
INSERT INTO tags (name) VALUES ('PHP'), ('Laravel'), ('SQL');

-- 投稿を登録（すでにあれば不要）
-- INSERT INTO posts (user_id, title, content) VALUES (1, 'Laravel入門', 'Laravelは楽しい！');
-- INSERT INTO posts (user_id, title, content) VALUES (1, 'SQLの基本', 'SELECT文を学びました');

-- 中間テーブルにデータを登録して、投稿とタグを紐付ける
-- 前提：投稿ID=1「Laravel入門」、投稿ID=2「SQLの基本」
-- 前提：タグID=1「PHP」、タグID=2「Laravel」、タグID=3「SQL」

-- 投稿ID=1に、タグID=1(PHP)とタグID=2(Laravel)を紐付ける
INSERT INTO post_tag (post_id, tag_id) VALUES (1, 1);
INSERT INTO post_tag (post_id, tag_id) VALUES (1, 2);

-- 投稿ID=2に、タグID=3(SQL)を紐付ける
INSERT INTO post_tag (post_id, tag_id) VALUES (2, 3);
```

`post_tag`テーブルの中身を見てみましょう。

| id | post_id | tag_id |
|:---|:---|:---|
| 1 | 1 | 1 |
| 2 | 1 | 2 |
| 3 | 2 | 3 |

この中間テーブルを見ることで、「投稿ID=1は、タグID=1と2に関連している」という多対多の関係が見事に表現できています。

もしここで、再度 `INSERT INTO post_tag (post_id, tag_id) VALUES (1, 1);` を実行しようとすると、先ほど設定した複合ユニークキー制約によってエラーとなり、重複した関連付けが防がれます。

**[ここに、複合ユニークキー制約違反のエラーメッセージが表示されたスクリーンショットを挿入]**

---

## ✨ まとめ

このセクションでは、複雑に見える「多対多」のリレーションシップを、中間テーブルを使って実装する方法を学びました。

*   「多対多」の関係は、そのままでは表現できないため、2つの「1対多」の関係に分解する。
*   その中心となるのが**中間テーブル（ピボットテーブル）**である。
*   中間テーブルには、関連付けたい2つのテーブルのIDを外部キーとして格納する。
*   データの整合性を保つため、中間テーブルには**複合ユニークキー制約**を設定し、同じ組み合わせの関連が重複して登録されるのを防ぐことが重要。

この中間テーブルを使った多対多の表現は、非常に多くのアプリケーションで使われる応用範囲の広いテクニックです。例えば、「ユーザー」と「商品」の間の「お気に入り登録」機能や、「学生」と「講義」の間の「履修登録」機能なども、この多対多の関係で実現されています。

次のセクションでは、これらのリレーションシップを使って、複数のテーブルからデータを取得する方法、つまり`JOIN`について学んでいきます。

---
