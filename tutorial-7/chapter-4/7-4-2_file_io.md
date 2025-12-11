# Tutorial 7-4-2: ファイルの読み書き

## 🎯 このセクションで学ぶこと

*   PHPで、サーバー上の、テキストファイルを、読み込む方法を学ぶ。
*   PHPで、サーバー上の、テキストファイルに、データを書き込む方法を学ぶ。
*   `file_get_contents`関数と、`file_put_contents`関数の、基本的な使い方を理解する。
*   ファイル操作における、パーミッション（権限）の、基本的な考え方を理解する。

---

## 導入

Webアプリケーションは、ユーザーからの入力を、受け取るだけでなく、そのデータを、**永続化（保存）**する必要があります。例えば、ユーザーが、掲示板に投稿した内容は、ブラウザを閉じても、消えずに、残っていなければなりません。

本格的な、アプリケーションでは、データベース（MySQLなど）を使って、データを管理しますが、より、手軽な、データの保存方法として、**ファイルへの書き込み**があります。例えば、アプリケーションの、設定情報や、ログ（記録）、簡単な、メッセージなどを、テキストファイルに、保存するケースは、よくあります。

このセクションでは、PHPを使って、サーバー上の、テキストファイルを、読み書きする、基本的な方法について、学んでいきます。

---

## 詳細解説

PHPには、ファイルの読み書きを、簡単に行うための、便利な関数が、用意されています。今回は、その中でも、特に、使いやすい、`file_get_contents`と、`file_put_contents`を紹介します。

### 📖 ファイルの読み込み: `file_get_contents`

`file_get_contents`関数は、指定したファイルの内容を、**全て、一度に、文字列として**、読み込みます。非常に、シンプルで、直感的に使えます。

```php
// 読み込むファイル名を指定
$filename = "data.txt";

// ファイルが存在するかどうかを確認
if (file_exists($filename)) {
    // ファイルの内容を、文字列として取得
    $content = file_get_contents($filename);

    // 読み込んだ内容を表示（htmlspecialcharsを忘れずに）
    echo htmlspecialchars($content, ENT_QUOTES, 'UTF-8');
} else {
    echo "ファイルが見つかりません。";
}
```

*   **`file_exists($filename)`**: ファイルや、ディレクトリが、存在するかどうかを、チェックする関数です。ファイルを読み込む前に、存在確認をするのは、良い習慣です。
*   **`file_get_contents($filename)`**: ファイルの内容を、全て、文字列として返します。ファイルが、存在しない場合や、読み込めない場合は、`false`を返し、警告（Warning）が発生します。

### ✍️ ファイルへの書き込み: `file_put_contents`

`file_put_contents`関数は、指定したファイルに、文字列を書き込みます。この関数も、非常に、シンプルです。

```php
// 書き込むファイル名
$filename = "data.txt";

// 書き込む内容
$content = "こんにちは、世界！\n"; // \n は改行コード

// ファイルに、内容を書き込む
// 戻り値は、書き込んだバイト数。失敗した場合は false。
$result = file_put_contents($filename, $content);

if ($result !== false) {
    echo "ファイルへの書き込みが成功しました。";
} else {
    echo "ファイルへの書き込みが失敗しました。";
}
```

#### 書き込みモード

`file_put_contents`は、デフォルトでは、**ファイルを上書き**します。もし、ファイルが、存在しない場合は、新しく作成されます。

ファイルに、**追記**したい場合は、第3引数に、`FILE_APPEND`という、定数を指定します。

```php
// 追記する内容
$additional_content = "これは追記です。\n";

// FILE_APPENDフラグを付けて、追記モードで書き込む
file_put_contents($filename, $additional_content, FILE_APPEND);
```

### 🗂️ 掲示板風アプリケーションの例

フォームからのデータ受け取りと、ファイルへの書き込みを組み合わせて、簡単な、一行掲示板を、作ってみましょう。

**`bbs.php` (フォーム表示と、投稿内容表示)**
```php
<?php
$filename = "bbs_data.txt";
$posts = [];

// ファイルが存在すれば、投稿内容を読み込む
if (file_exists($filename)) {
    // ファイルの内容を、1行ずつ、配列として読み込む
    $posts = file($filename, FILE_IGNORE_NEW_LINES);
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>一行掲示板</title>
</head>
<body>
    <h1>一行掲示板</h1>

    <!-- 投稿フォーム -->
    <form action="post.php" method="post">
        <input type="text" name="message" size="50">
        <button type="submit">投稿</button>
    </form>

    <hr>

    <!-- 投稿内容の表示 -->
    <h2>投稿一覧</h2>
    <?php if (!empty($posts)): ?>
        <ul>
            <?php foreach ($posts as $post): ?>
                <li><?php echo htmlspecialchars($post, ENT_QUOTES, 'UTF-8'); ?></li>
            <?php endforeach; ?>
        </ul>
    <?php else: ?>
        <p>まだ投稿はありません。</p>
    <?php endif; ?>
</body>
</html>
```

*   **`file($filename, FILE_IGNORE_NEW_LINES)`**: `file_get_contents`と似ていますが、こちらは、ファイルの内容を、**1行ずつ、配列の要素として**、読み込みます。`FILE_IGNORE_NEW_LINES`は、各行の、末尾の改行コードを、取り除くオプションです。

**`post.php` (投稿処理)**
```php
<?php
// フォームデータが送信されたかチェック
if ($_SERVER["REQUEST_METHOD"] === "POST" && !empty($_POST["message"])) {
    $filename = "bbs_data.txt";
    $message = $_POST["message"];

    // メッセージの末尾に改行を追加
    $data_to_write = $message . "\n";

    // 追記モードでファイルに書き込む
    file_put_contents($filename, $data_to_write, FILE_APPEND);
}

// 処理が終わったら、掲示板ページにリダイレクトする
header("Location: bbs.php");
exit;
?>
```

*   **`$_SERVER["REQUEST_METHOD"]`**: リクエストが、`POST`なのか、`GET`なのかを、判別できます。
*   **`header("Location: bbs.php")`**: ユーザーのブラウザに、「`bbs.php`に移動してください」という、指示を送ります（リダイレクト）。これにより、ユーザーが、`post.php`のページで、再読み込み（F5キー）をして、同じ内容が、二重に投稿されてしまうのを、防ぐことができます。

### ⚠️ パーミッションについて

`file_put_contents`で、ファイルへの書き込みが、失敗する、最も、一般的な原因は、**パーミッション（権限）の問題**です。

Webサーバー（ApacheやNginx）を実行しているユーザーが、ファイルを書き込む先の、ディレクトリに対して、「書き込み権限」を持っていないと、PHPは、ファイルを作成したり、書き換えたりすることができません。

Laravelでは、`storage`ディレクトリや、`bootstrap/cache`ディレクトリに、適切な、書き込み権限を、設定する必要がありますが、これは、後の、環境構築のセクションで、詳しく、解説します。現時点では、「**PHPが、ファイルを書き込むには、サーバー上の、適切な権限が必要**」ということを、覚えておいてください。

---

## ✨ まとめ

このセクションでは、PHPを使った、基本的な、ファイルの読み書きについて学びました。

*   **ファイルの読み込み**: `file_get_contents()`（全てを文字列として）や、`file()`（1行ずつ配列として）を使う。
*   **ファイルの書き込み**: `file_put_contents()` を使う。デフォルトは上書き。
*   **追記**: `file_put_contents()` の第3引数に、`FILE_APPEND` を指定する。
*   **リダイレクト**: `header("Location: ...")` を使うことで、二重投稿などを防ぐことができる。
*   **パーミッション**: ファイルの書き込みに失敗する、主な原因は、サーバーの、書き込み権限の問題。

ファイル操作は、データベースほど、高機能ではありませんが、ログの記録や、設定ファイルの管理など、様々な場面で、役立つ、基本的なスキルです。

---

## 📝 学習のポイント

- [ ] `file_get_contents`と、`file_put_contents`の、基本的な使い方を、説明できる。
- [ ] `file_put_contents`で、上書きと、追記を、切り替える方法を、説明できる。
- [ ] ファイルへの書き込みが、失敗した場合、パーミッションの問題を、疑うことができる。
- [ ] 簡単な、掲示板のように、フォームからの入力を、ファイルに保存し、表示する、一連の流れを、作成できる。
