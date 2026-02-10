# Tutorial 7-4-2: PHPファイル間のデータ受け渡し

## 🎯 このセクションで学ぶこと

*   複数のPHPファイル間で、データを受け渡す方法を理解する。
*   フォームを使った、ページ間のデータ送信の仕組みを学ぶ。
*   `header()`関数を使った、リダイレクトの基本を理解する。
*   `include`と`require`を使った、ファイルの読み込みを学ぶ。

---

## 導入

Webアプリケーションでは、1つのPHPファイルだけで、すべての処理を行うことは、ほとんどありません。例えば、ユーザー登録の流れを考えてみましょう。

1. **入力画面**（`form.php`）：ユーザーが情報を入力
2. **確認画面**（`confirm.php`）：入力内容を確認
3. **完了画面**（`complete.php`）：登録完了を表示

このように、複数のPHPファイルが連携して、一つの機能を実現します。このとき、「入力画面で入力されたデータを、確認画面に渡す」といった、**ファイル間のデータ受け渡し**が必要になります。

このセクションでは、PHPファイル間でデータを受け渡す、様々な方法について学んでいきます。

---

## 詳細解説

### 🧠 先輩エンジニアの思考プロセス

> 「PHPファイル間でデータを渡す方法はいくつかあるな。フォームで送信する方法、URLパラメータで渡す方法、セッションを使う方法...。まずは基本的なフォーム送信から理解しよう。」

---

### 📝 フォームを使ったデータ送信（復習）

7-4-1で学んだ、フォームを使ったデータ送信を、もう一度確認しましょう。これが、PHPファイル間のデータ受け渡しの、最も基本的な方法です。

**入力画面（`input.php`）**

```php
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>入力画面</title>
</head>
<body>
    <h1>ユーザー情報入力</h1>
    <form action="process.php" method="post">
        <p>
            <label>お名前：</label>
            <input type="text" name="name">
        </p>
        <p>
            <label>メールアドレス：</label>
            <input type="email" name="email">
        </p>
        <button type="submit">送信</button>
    </form>
</body>
</html>
```

**処理画面（`process.php`）**

```php
<?php
// フォームから送信されたデータを受け取る
$name = $_POST["name"];
$email = $_POST["email"];
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>処理結果</title>
</head>
<body>
    <h1>入力内容</h1>
    <p>お名前：<?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?></p>
    <p>メールアドレス：<?php echo htmlspecialchars($email, ENT_QUOTES, 'UTF-8'); ?></p>
</body>
</html>
```

**コードリーディング**：

```php
<form action="process.php" method="post">
```
→ `action`属性で、データの送信先を指定します。ここでは`process.php`に送信されます。

```php
$name = $_POST["name"];
```
→ `$_POST`は連想配列で、フォームの`name`属性の値がキーになります。`name="name"`の入力欄の値は、`$_POST["name"]`で取得できます。

---

### 🔗 URLパラメータを使ったデータ受け渡し

フォームを使わずに、URLに直接データを含めて渡す方法もあります。これを**URLパラメータ**（クエリストリング）と呼びます。

**リンク元（`list.php`）**

```php
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>商品一覧</title>
</head>
<body>
    <h1>商品一覧</h1>
    <ul>
        <li><a href="detail.php?id=1&name=りんご">りんご</a></li>
        <li><a href="detail.php?id=2&name=みかん">みかん</a></li>
        <li><a href="detail.php?id=3&name=バナナ">バナナ</a></li>
    </ul>
</body>
</html>
```

**リンク先（`detail.php`）**

```php
<?php
// URLパラメータを受け取る
$id = $_GET["id"];
$name = $_GET["name"];
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>商品詳細</title>
</head>
<body>
    <h1>商品詳細</h1>
    <p>商品ID：<?php echo htmlspecialchars($id, ENT_QUOTES, 'UTF-8'); ?></p>
    <p>商品名：<?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?></p>
    <p><a href="list.php">一覧に戻る</a></p>
</body>
</html>
```

**コードリーディング**：

```php
<a href="detail.php?id=1&name=りんご">りんご</a>
```
→ URLの`?`以降がパラメータです。`id=1`と`name=りんご`の2つのパラメータを、`&`で区切って渡しています。

```php
$id = $_GET["id"];
```
→ URLパラメータは`$_GET`で受け取ります。`$_POST`と同様に連想配列です。

| 受け渡し方法 | 使用する変数 | 特徴 |
| :--- | :--- | :--- |
| フォーム（POST） | `$_POST` | データがURLに表示されない。機密情報に適している。 |
| URLパラメータ（GET） | `$_GET` | データがURLに表示される。ブックマークや共有に適している。 |

---

### 🔄 リダイレクトを使ったページ遷移

処理が完了した後、別のページに自動的に移動させたい場合は、`header()`関数を使って**リダイレクト**します。

**処理画面（`save.php`）**

```php
<?php
// フォームから送信されたデータを受け取る
$name = $_POST["name"];

// ここでデータベースへの保存などの処理を行う
// （今回は省略）

// 処理が完了したら、完了画面にリダイレクト
header("Location: complete.php");
exit;
?>
```

**完了画面（`complete.php`）**

```php
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>完了</title>
</head>
<body>
    <h1>登録が完了しました</h1>
    <p><a href="input.php">入力画面に戻る</a></p>
</body>
</html>
```

**コードリーディング**：

```php
header("Location: complete.php");
```
→ ブラウザに「`complete.php`に移動してください」という指示を送ります。ユーザーのブラウザは自動的に`complete.php`に移動します。

```php
exit;
```
→ `header()`の後は必ず`exit`を書きます。これがないと、リダイレクト後もスクリプトが実行され続けてしまいます。

**注意点**：`header()`関数は、HTMLを出力する前に呼び出す必要があります。HTMLタグや空白、改行を出力した後に`header()`を呼び出すと、エラーになります。

---

### 📤 リダイレクト時のデータ受け渡し

リダイレクト先にデータを渡したい場合は、URLパラメータを使います。

**処理画面（`save.php`）**

```php
<?php
$name = $_POST["name"];

// 処理が完了したら、名前をURLパラメータで渡してリダイレクト
$encoded_name = urlencode($name);
header("Location: complete.php?name=" . $encoded_name);
exit;
?>
```

**完了画面（`complete.php`）**

```php
<?php
$name = isset($_GET["name"]) ? $_GET["name"] : "ゲスト";
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>完了</title>
</head>
<body>
    <h1><?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?>さん、登録が完了しました</h1>
</body>
</html>
```

**コードリーディング**：

```php
$encoded_name = urlencode($name);
```
→ `urlencode()`関数で、URLに含められない文字（日本語やスペースなど）を、安全な形式に変換します。

```php
$name = isset($_GET["name"]) ? $_GET["name"] : "ゲスト";
```
→ `isset()`で、パラメータが存在するかチェックします。存在しない場合は「ゲスト」をデフォルト値として使用します。

---

### 📦 `include`と`require`を使ったファイル読み込み

複数のPHPファイルで、共通の処理やHTMLを使いたい場合は、`include`や`require`を使って、別のファイルを読み込みます。

**共通ヘッダー（`header.php`）**

```php
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title><?php echo $page_title; ?></title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        header { background-color: #333; color: white; padding: 10px; }
        nav a { color: white; margin-right: 15px; }
    </style>
</head>
<body>
    <header>
        <nav>
            <a href="index.php">ホーム</a>
            <a href="about.php">会社概要</a>
            <a href="contact.php">お問い合わせ</a>
        </nav>
    </header>
```

**共通フッター（`footer.php`）**

```php
    <footer>
        <p>&copy; 2024 サンプル会社</p>
    </footer>
</body>
</html>
```

**メインページ（`index.php`）**

```php
<?php
$page_title = "ホーム";
include "header.php";
?>

<main>
    <h1>ようこそ</h1>
    <p>これはサンプルサイトです。</p>
</main>

<?php include "footer.php"; ?>
```

**コードリーディング**：

```php
$page_title = "ホーム";
include "header.php";
```
→ `include`の前に変数を定義しておくと、読み込まれるファイル内でその変数を使用できます。

```php
include "header.php";
```
→ `header.php`の内容が、この位置に挿入されます。

| 命令 | ファイルが見つからない場合 |
| :--- | :--- |
| `include` | 警告（Warning）を出すが、処理は続行する |
| `require` | エラー（Fatal Error）を出し、処理を停止する |

**使い分けの目安**：
- `require`：必須のファイル（設定ファイル、データベース接続など）
- `include`：なくても動作するファイル（オプションの機能など）

---

## ✨ まとめ

このセクションでは、PHPファイル間でデータを受け渡す方法について学びました。

| 方法 | 使用する変数/関数 | 用途 |
| :--- | :--- | :--- |
| フォーム送信（POST） | `$_POST` | ユーザー入力データの送信 |
| URLパラメータ（GET） | `$_GET` | 検索条件やIDの受け渡し |
| リダイレクト | `header()` | 処理完了後のページ遷移 |
| ファイル読み込み | `include` / `require` | 共通部品の再利用 |
| 隠しフィールド | `<input type="hidden">` | 確認画面でのデータ保持 |

これらの方法を組み合わせることで、複数のPHPファイルが連携する、本格的なWebアプリケーションを作成できるようになります。

---
