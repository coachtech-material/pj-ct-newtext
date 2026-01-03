# Tutorial 7-4-3: フォームとデータ受け渡し - ハンズオン演習

## 📝 このセクションの目的

Chapter 4で学んだフォームデータの受け取りとPHPファイル間のデータ受け渡しを実際に手を動かして確認します。入力→確認→完了の3ステップで動作するユーザー登録フォームを作成しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

**学習のポイント**：
- フォームからデータを送信できるか
- `$_POST`でデータを受け取れるか
- 複数のPHPファイル間でデータを受け渡せるか
- `htmlspecialchars`でセキュリティ対策ができるか

---

## 🎯 演習課題：ユーザー登録フォームを作成しよう

### 課題の概要

入力→確認→完了の3ステップで動作するユーザー登録フォームを作成してください。3つのPHPファイルを連携させて、データを受け渡します。

### 📋 要件

以下の要件を満たす3つのPHPファイルを作成してください。

> 📁 **作業ディレクトリ**: Tutorial 7-1-2で作成した`~/php-practice/src/`ディレクトリ内にファイルを作成してください。ブラウザで`http://localhost:8000/input.php`にアクセスして確認します。

#### 1. 入力画面（`input.php`）

**入力項目**：
- お名前（テキスト入力）
- メールアドレス（メール入力）
- 年齢（数値入力）

**動作**：
- 「確認画面へ」ボタンを押すと、`confirm.php`にデータを送信

#### 2. 確認画面（`confirm.php`）

**表示内容**：
- 入力された内容を表示
- 「戻る」ボタンと「登録する」ボタン

**動作**：
- 「戻る」ボタンで入力画面に戻る
- 「登録する」ボタンで`complete.php`にデータを送信

#### 3. 完了画面（`complete.php`）

**表示内容**：
- 登録完了メッセージ
- 入力された名前を使った挨拶

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: フォームの基本構造

```php
<form action="confirm.php" method="post">
    <input type="text" name="name">
    <button type="submit">送信</button>
</form>
```

### ヒント2: データの受け取り

```php
$name = $_POST["name"];
```

### ヒント3: セキュリティ対策

```php
echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8');
```

### ヒント4: 隠しフィールド

```php
<input type="hidden" name="name" value="<?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?>">
```

### ヒント5: 戻るボタン

```php
<button type="button" onclick="history.back()">戻る</button>
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？フォームとデータ受け渡しはWebアプリケーションの基本です。一緒に手を動かしながら、ユーザー登録フォームを作っていきましょう。

### 💭 実装の思考プロセス

ユーザー登録フォームを作る際、以下の順番で考えると効率的です：

1. **入力画面を作る**：フォームを作成し、確認画面にデータを送信
2. **確認画面を作る**：受け取ったデータを表示し、完了画面に渡す
3. **完了画面を作る**：登録完了メッセージを表示

ポイントは「データの流れ」を意識することです。入力画面→確認画面→完了画面と、データがどう渡されるかを考えましょう。

---

### 📝 ステップバイステップで実装

#### Step 1: 入力画面を作成する

**何を考えているか**：
- 「ユーザーに名前、メールアドレス、年齢を入力してもらおう」
- 「送信先は確認画面（`confirm.php`）にしよう」
- 「`method="post"`でデータを送信しよう」

まず、ターミナルで以下のコマンドを実行して、`input.php`ファイルを作成します：

```bash
# php-practiceディレクトリに移動
cd ~/php-practice

# input.phpを作成
touch src/input.php
```

`src/input.php`をエディタで開き、以下の内容を記述します：

```php
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ユーザー登録 - 入力</title>
</head>
<body>
    <h1>ユーザー登録（1/3）入力</h1>
    <form action="confirm.php" method="post">
        <p>
            <label>お名前：</label>
            <input type="text" name="name" required>
        </p>
        <p>
            <label>メールアドレス：</label>
            <input type="email" name="email" required>
        </p>
        <p>
            <label>年齢：</label>
            <input type="number" name="age" min="0" max="120" required>
        </p>
        <button type="submit">確認画面へ</button>
    </form>
</body>
</html>
```

**コードリーディング**：

```php
<form action="confirm.php" method="post">
```
→ `action`属性で送信先を`confirm.php`に指定します。`method="post"`でPOSTメソッドを使用します。

```php
<input type="text" name="name" required>
```
→ `name="name"`で、PHP側で`$_POST["name"]`として受け取れます。`required`は入力必須を意味します。

```php
<input type="email" name="email" required>
```
→ `type="email"`で、メールアドレス形式のバリデーションが自動的に行われます。

```php
<input type="number" name="age" min="0" max="120" required>
```
→ `type="number"`で数値入力欄になります。`min`と`max`で入力範囲を制限します。

---

#### Step 2: 確認画面を作成する

**何を考えているか**：
- 「入力画面から`$_POST`でデータを受け取ろう」
- 「受け取ったデータを表示して、ユーザーに確認してもらおう」
- 「完了画面にデータを渡すために、`hidden`フィールドを使おう」
- 「XSS対策のために`htmlspecialchars`を使おう」

次に、ターミナルで以下のコマンドを実行して、`confirm.php`ファイルを作成します：

```bash
# confirm.phpを作成
touch src/confirm.php
```

`src/confirm.php`をエディタで開き、以下の内容を記述します：

```php
<?php
// 入力データを受け取る
$name = $_POST["name"];
$email = $_POST["email"];
$age = $_POST["age"];
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ユーザー登録 - 確認</title>
</head>
<body>
    <h1>ユーザー登録（2/3）確認</h1>
    <p>以下の内容で登録します。よろしいですか？</p>
    
    <table border="1">
        <tr>
            <th>お名前</th>
            <td><?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?></td>
        </tr>
        <tr>
            <th>メールアドレス</th>
            <td><?php echo htmlspecialchars($email, ENT_QUOTES, 'UTF-8'); ?></td>
        </tr>
        <tr>
            <th>年齢</th>
            <td><?php echo htmlspecialchars($age, ENT_QUOTES, 'UTF-8'); ?>歳</td>
        </tr>
    </table>
    
    <!-- 確認画面から完了画面へデータを渡すためのフォーム -->
    <form action="complete.php" method="post">
        <!-- hidden属性で、データを隠して送信 -->
        <input type="hidden" name="name" value="<?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?>">
        <input type="hidden" name="email" value="<?php echo htmlspecialchars($email, ENT_QUOTES, 'UTF-8'); ?>">
        <input type="hidden" name="age" value="<?php echo htmlspecialchars($age, ENT_QUOTES, 'UTF-8'); ?>">
        
        <p>
            <button type="button" onclick="history.back()">戻る</button>
            <button type="submit">登録する</button>
        </p>
    </form>
</body>
</html>
```

**コードリーディング**：

```php
$name = $_POST["name"];
```
→ 入力画面から送信されたデータを`$_POST`で受け取ります。

```php
<?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?>
```
→ `htmlspecialchars`でXSS対策をします。ユーザー入力を表示する際は必ず使用します。

```php
<input type="hidden" name="name" value="<?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?>">
```
→ `type="hidden"`で隠しフィールドを作成します。画面には表示されませんが、フォーム送信時にデータが送られます。これで確認画面から完了画面へデータを渡せます。

```php
<button type="button" onclick="history.back()">戻る</button>
```
→ `type="button"`でフォーム送信を防ぎ、`history.back()`で前のページに戻ります。

---

#### Step 3: 完了画面を作成する

**何を考えているか**：
- 「確認画面から`$_POST`でデータを受け取ろう」
- 「実際のアプリケーションでは、ここでデータベースに保存する」
- 「登録完了のメッセージを表示しよう」

最後に、ターミナルで以下のコマンドを実行して、`complete.php`ファイルを作成します：

```bash
# complete.phpを作成
touch src/complete.php
```

`src/complete.php`をエディタで開き、以下の内容を記述します：

```php
<?php
// 確認画面から送信されたデータを受け取る
$name = $_POST["name"];
$email = $_POST["email"];
$age = $_POST["age"];

// ここでデータベースへの保存などの処理を行う
// （今回は省略）
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ユーザー登録 - 完了</title>
</head>
<body>
    <h1>ユーザー登録（3/3）完了</h1>
    <p><?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?>さん、登録が完了しました！</p>
    <p>確認メールを <?php echo htmlspecialchars($email, ENT_QUOTES, 'UTF-8'); ?> に送信しました。</p>
    <p><a href="input.php">最初に戻る</a></p>
</body>
</html>
```

**コードリーディング**：

```php
$name = $_POST["name"];
```
→ 確認画面の隠しフィールドから送信されたデータを受け取ります。

```php
// ここでデータベースへの保存などの処理を行う
```
→ 実際のアプリケーションでは、ここでデータベースへの保存処理を行います。

```php
<a href="input.php">最初に戻る</a>
```
→ 通常のリンクで入力画面に戻れるようにします。

---

### ✨ 完成！

これでユーザー登録フォームが完成しました！3つのPHPファイルが連携して、データを受け渡しながら動作します。

---

## ✅ 完成イメージ

完成すると、以下のような流れで動作します：

**入力画面（input.php）**
```
ユーザー登録（1/3）入力

お名前：[田中太郎        ]
メールアドレス：[tanaka@example.com]
年齢：[25]

[確認画面へ]
```

**確認画面（confirm.php）**
```
ユーザー登録（2/3）確認

以下の内容で登録します。よろしいですか？

| お名前         | 田中太郎           |
| メールアドレス | tanaka@example.com |
| 年齢           | 25歳               |

[戻る] [登録する]
```

**完了画面（complete.php）**
```
ユーザー登録（3/3）完了

田中太郎さん、登録が完了しました！
確認メールを tanaka@example.com に送信しました。

最初に戻る
```

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### input.php

```php
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ユーザー登録 - 入力</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            border-bottom: 3px solid #0066cc;
            padding-bottom: 10px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        button {
            width: 100%;
            padding: 12px;
            background-color: #0066cc;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #0052a3;
        }
        .step {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <p class="step">ステップ 1/3</p>
        <h1>ユーザー登録</h1>
        
        <form action="confirm.php" method="post">
            <div class="form-group">
                <label for="name">お名前</label>
                <input type="text" id="name" name="name" required>
            </div>
            
            <div class="form-group">
                <label for="email">メールアドレス</label>
                <input type="email" id="email" name="email" required>
            </div>
            
            <div class="form-group">
                <label for="age">年齢</label>
                <input type="number" id="age" name="age" min="0" max="120" required>
            </div>
            
            <button type="submit">確認画面へ</button>
        </form>
    </div>
</body>
</html>
```

### confirm.php

```php
<?php
$name = $_POST["name"];
$email = $_POST["email"];
$age = $_POST["age"];
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ユーザー登録 - 確認</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            border-bottom: 3px solid #ff9900;
            padding-bottom: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f9f9f9;
            width: 40%;
        }
        .buttons {
            display: flex;
            gap: 10px;
        }
        button {
            flex: 1;
            padding: 12px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .btn-back {
            background-color: #999;
            color: white;
        }
        .btn-submit {
            background-color: #ff9900;
            color: white;
        }
        .btn-back:hover { background-color: #777; }
        .btn-submit:hover { background-color: #e68a00; }
        .step {
            text-align: center;
            color: #666;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <p class="step">ステップ 2/3</p>
        <h1>入力内容の確認</h1>
        
        <p>以下の内容で登録します。よろしいですか？</p>
        
        <table>
            <tr>
                <th>お名前</th>
                <td><?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?></td>
            </tr>
            <tr>
                <th>メールアドレス</th>
                <td><?php echo htmlspecialchars($email, ENT_QUOTES, 'UTF-8'); ?></td>
            </tr>
            <tr>
                <th>年齢</th>
                <td><?php echo htmlspecialchars($age, ENT_QUOTES, 'UTF-8'); ?>歳</td>
            </tr>
        </table>
        
        <form action="complete.php" method="post">
            <input type="hidden" name="name" value="<?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?>">
            <input type="hidden" name="email" value="<?php echo htmlspecialchars($email, ENT_QUOTES, 'UTF-8'); ?>">
            <input type="hidden" name="age" value="<?php echo htmlspecialchars($age, ENT_QUOTES, 'UTF-8'); ?>">
            
            <div class="buttons">
                <button type="button" class="btn-back" onclick="history.back()">戻る</button>
                <button type="submit" class="btn-submit">登録する</button>
            </div>
        </form>
    </div>
</body>
</html>
```

### complete.php

```php
<?php
$name = $_POST["name"];
$email = $_POST["email"];
$age = $_POST["age"];
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ユーザー登録 - 完了</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 500px;
            margin: 50px auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }
        h1 {
            color: #28a745;
            border-bottom: 3px solid #28a745;
            padding-bottom: 10px;
        }
        .success-icon {
            font-size: 60px;
            margin: 20px 0;
        }
        .message {
            font-size: 18px;
            margin: 20px 0;
        }
        .email-info {
            background-color: #f0f8ff;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        a {
            display: inline-block;
            margin-top: 20px;
            padding: 12px 30px;
            background-color: #0066cc;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }
        a:hover {
            background-color: #0052a3;
        }
        .step {
            color: #666;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <p class="step">ステップ 3/3</p>
        <h1>登録完了</h1>
        
        <div class="success-icon">✓</div>
        
        <p class="message">
            <strong><?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?></strong>さん、<br>
            登録が完了しました！
        </p>
        
        <div class="email-info">
            確認メールを<br>
            <strong><?php echo htmlspecialchars($email, ENT_QUOTES, 'UTF-8'); ?></strong><br>
            に送信しました。
        </div>
        
        <a href="input.php">最初に戻る</a>
    </div>
</body>
</html>
```

---

## 🔍 よくある間違い

### 間違い1: `$_POST`のキー名の間違い

```php
// ❌ 間違い（HTMLのname属性と一致していない）
<input type="text" name="username">
$name = $_POST["name"];  // undefined index エラー

// ✅ 正しい
<input type="text" name="name">
$name = $_POST["name"];
```

### 間違い2: `htmlspecialchars`の忘れ

```php
// ❌ 間違い（XSS脆弱性あり）
echo $_POST["name"];

// ✅ 正しい
echo htmlspecialchars($_POST["name"], ENT_QUOTES, 'UTF-8');
```

### 間違い3: hiddenフィールドの`value`忘れ

```php
// ❌ 間違い（valueがないのでデータが渡らない）
<input type="hidden" name="name">

// ✅ 正しい
<input type="hidden" name="name" value="<?php echo htmlspecialchars($name, ENT_QUOTES, 'UTF-8'); ?>">
```

### 間違い4: `method`の指定忘れ

```php
// ❌ 間違い（methodがないとGETになる）
<form action="confirm.php">

// ✅ 正しい
<form action="confirm.php" method="post">
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ フォームからデータを送信できる
- ✅ `$_POST`でデータを受け取れる
- ✅ 複数のPHPファイル間でデータを受け渡せる
- ✅ `htmlspecialchars`でセキュリティ対策ができる
- ✅ 隠しフィールドでデータを保持できる

これらの技術は、Laravelでのフォーム処理の基礎となります。引き続き頑張りましょう！

---
