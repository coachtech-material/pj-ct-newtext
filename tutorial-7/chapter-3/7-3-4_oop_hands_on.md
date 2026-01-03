# Tutorial 7-3-4: オブジェクト指向 - ハンズオン演習

## 📝 このセクションの目的

Chapter 3で学んだオブジェクト指向の基礎を実際に手を動かして確認します。シンプルなクラスを作成して、オブジェクト指向の基本を体験しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

**学習のポイント**：
- クラスを定義できるか
- プロパティを設定できるか
- メソッドを作成して呼び出せるか
- コンストラクタで初期化できるか

---

## 🎯 演習課題：ユーザー管理プログラムを作成しよう

### 課題の概要

ユーザー情報を管理するシンプルなプログラムを作成してください。`User`クラスを定義し、ユーザーの情報を表示する機能を実装します。

### 📋 要件

以下の要件を満たすPHPファイル（`user.php`）を作成してください。

> 📁 **作業ディレクトリ**: Tutorial 7-1-2で作成した`~/php-practice/src/`ディレクトリ内にファイルを作成してください。ブラウザで`http://localhost:8000/user.php`にアクセスして確認します。

#### 1. Userクラスの定義

**プロパティ**：
- `$name`（名前）：文字列
- `$age`（年齢）：数値

**メソッド**：

1. **`__construct($name, $age)`**
   - コンストラクタ
   - 名前と年齢を初期化

2. **`introduce()`**
   - 自己紹介を表示
   - 例：「こんにちは、私は田中太郎です。25歳です。」

3. **`isAdult()`**
   - 成人かどうかを判定
   - 戻り値：18歳以上なら`true`、未満なら`false`

#### 2. テストデータ

以下のユーザーを作成してテストしてください：

| 名前 | 年齢 |
| :--- | :--- |
| 田中太郎 | 25 |
| 佐藤花子 | 17 |
| 鈴木一郎 | 30 |

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: クラスの定義

```php
class User {
    public $name;
    public $age;
}
```

### ヒント2: コンストラクタ

```php
public function __construct($name, $age) {
    $this->name = $name;
    $this->age = $age;
}
```

### ヒント3: 自己紹介メソッド

```php
public function introduce() {
    echo "こんにちは、私は{$this->name}です。{$this->age}歳です。<br>";
}
```

### ヒント4: 成人判定メソッド

```php
public function isAdult() {
    return $this->age >= 18;
}
```

### ヒント5: オブジェクトの生成

```php
$user1 = new User("田中太郎", 25);
$user1->introduce();
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？オブジェクト指向の基本は「データと処理をまとめる」ことです。一緒に手を動かしながら、ユーザー管理プログラムを作っていきましょう。

### 💭 実装の思考プロセス

ユーザー管理プログラムを作る際、以下の順番で考えると効率的です：

1. **クラスを定義する**：`User`クラスを作成
2. **プロパティを追加**：名前と年齢を変数として定義
3. **コンストラクタを作る**：オブジェクト生成時に初期値を設定
4. **メソッドを実装**：自己紹介と成人判定の機能を作る
5. **オブジェクトを生成して使う**：クラスからオブジェクトを作成してメソッドを呼び出す

---

### 📝 ステップバイステップで実装

#### ステップ1: クラスを定義してプロパティを追加する

**何を考えているか**：
- 「`User`クラスを作ろう」
- 「ユーザーに必要なデータをプロパティとして定義しよう」
- 「まずは`public`でシンプルに作ろう」

まず、ターミナルで以下のコマンドを実行して、`user.php`ファイルを作成します：

```bash
# php-practiceディレクトリに移動
cd ~/php-practice

# VSCodeでプロジェクトを開く
code .
```

VSCodeが開いたら、エクスプローラーで`src`フォルダを右クリックし、「新しいファイル」を選択して`user.php`を作成してください。

`src/user.php`ファイルに、クラスを定義します：

```php
<?php
class User {
    public $name;
    public $age;
}
```

**コードリーディング**：

```php
class User {
```
→ `class`キーワードでクラスを定義します。クラス名は大文字で始めるのが慣例です。`User`という名前で、ユーザーを表すクラスを作成します。

```php
    public $name;
    public $age;
}
```
→ `public`でプロパティを定義します。`public`は外部からもアクセスできることを意味します。`$name`は名前、`$age`は年齢を格納します。

---

#### ステップ2: コンストラクタを作る

**何を考えているか**：
- 「オブジェクト生成時に名前と年齢を設定したい」
- 「`__construct()`メソッドを使おう」
- 「引数で受け取った値をプロパティに代入しよう」

次に、コンストラクタを追加します：

```php
class User {
    public $name;
    public $age;
    
    public function __construct($name, $age) {
        $this->name = $name;
        $this->age = $age;
    }
}
```

**コードリーディング**：

```php
    public function __construct($name, $age) {
```
→ コンストラクタを定義します。`__construct()`はオブジェクト生成時に自動的に呼び出される特殊なメソッドです。引数として名前と年齢を受け取ります。

```php
        $this->name = $name;
```
→ `$this`は現在のオブジェクト自身を指します。`$this->name`でプロパティにアクセスし、引数で受け取った`$name`の値を代入します。

```php
        $this->age = $age;
    }
```
→ 同様に年齢を設定します。これで、オブジェクト生成時に名前と年齢が初期化されます。

---

#### ステップ3: 自己紹介メソッドを作る

**何を考えているか**：
- 「ユーザーの情報を表示するメソッドを作ろう」
- 「プロパティの値を使って文章を組み立てよう」

次に、自己紹介メソッドを追加します：

```php
    public function introduce() {
        echo "こんにちは、私は{$this->name}です。{$this->age}歳です。<br>";
    }
```

**コードリーディング**：

```php
    public function introduce() {
```
→ `public`メソッド`introduce`を定義します。引数はありません。

```php
        echo "こんにちは、私は{$this->name}です。{$this->age}歳です。<br>";
    }
```
→ `$this->name`と`$this->age`でプロパティの値を取得し、自己紹介文を表示します。`{}`で囲むことで、文字列の中に変数を埋め込めます。

---

#### ステップ4: 成人判定メソッドを作る

**何を考えているか**：
- 「18歳以上かどうかを判定しよう」
- 「結果を`true`または`false`で返そう」

次に、成人判定メソッドを追加します：

```php
    public function isAdult() {
        return $this->age >= 18;
    }
```

**コードリーディング**：

```php
    public function isAdult() {
```
→ 成人かどうかを判定するメソッドを定義します。

```php
        return $this->age >= 18;
    }
```
→ `$this->age >= 18`は、年齢が18以上なら`true`、未満なら`false`を返します。比較演算子`>=`は「以上」を意味します。

---

#### ステップ5: オブジェクトを生成して使う

**何を考えているか**：
- 「`new`キーワードでオブジェクトを生成しよう」
- 「メソッドを呼び出して動作を確認しよう」
- 「複数のオブジェクトを作成してみよう」

最後に、オブジェクトを生成して使用します：

```php
echo "<h2>ユーザー管理プログラム</h2>";

// ユーザーを作成
$user1 = new User("田中太郎", 25);
$user2 = new User("佐藤花子", 17);
$user3 = new User("鈴木一郎", 30);

// 自己紹介
echo "<h3>自己紹介</h3>";
$user1->introduce();
$user2->introduce();
$user3->introduce();

// 成人判定
echo "<h3>成人判定</h3>";
if ($user1->isAdult()) {
    echo "{$user1->name}さんは成人です。<br>";
} else {
    echo "{$user1->name}さんは未成年です。<br>";
}

if ($user2->isAdult()) {
    echo "{$user2->name}さんは成人です。<br>";
} else {
    echo "{$user2->name}さんは未成年です。<br>";
}

if ($user3->isAdult()) {
    echo "{$user3->name}さんは成人です。<br>";
} else {
    echo "{$user3->name}さんは未成年です。<br>";
}
?>
```

**コードリーディング**：

```php
$user1 = new User("田中太郎", 25);
```
→ `new`キーワードで`User`クラスのオブジェクトを生成します。コンストラクタに名前と年齢を渡します。

```php
$user1->introduce();
```
→ `->` 演算子でオブジェクトのメソッドを呼び出します。`introduce`メソッドで自己紹介を表示します。

```php
if ($user1->isAdult()) {
```
→ `isAdult()`メソッドの戻り値（`true`または`false`）を使って条件分岐します。

```php
    echo "{$user1->name}さんは成人です。<br>";
```
→ `$user1->name`でプロパティに直接アクセスして名前を取得します（`public`なのでアクセス可能）。

---

### ✨ 完成！

これでユーザー管理プログラムが完成しました！クラス、プロパティ、メソッド、コンストラクタ、オブジェクトの生成と使用を実践できましたね。

---

## ✅ 完成イメージ

完成すると、以下のような表示になります：

```
ユーザー管理プログラム

自己紹介
こんにちは、私は田中太郎です。25歳です。
こんにちは、私は佐藤花子です。17歳です。
こんにちは、私は鈴木一郎です。30歳です。

成人判定
田中太郎さんは成人です。
佐藤花子さんは未成年です。
鈴木一郎さんは成人です。
```

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### user.php

```php
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ユーザー管理プログラム</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 600px;
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
        h2 {
            color: #0066cc;
            margin-top: 30px;
        }
        .user-info {
            background-color: #f0f8ff;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
            border-left: 4px solid #0066cc;
        }
        .adult { color: #28a745; }
        .minor { color: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>ユーザー管理プログラム</h1>
        
        <?php
        // Userクラスの定義
        class User {
            public $name;
            public $age;
            
            // コンストラクタ
            public function __construct($name, $age) {
                $this->name = $name;
                $this->age = $age;
            }
            
            // 自己紹介メソッド
            public function introduce() {
                echo "<div class='user-info'>";
                echo "こんにちは、私は{$this->name}です。{$this->age}歳です。";
                echo "</div>";
            }
            
            // 成人判定メソッド
            public function isAdult() {
                return $this->age >= 18;
            }
        }
        
        // ユーザーを作成
        $user1 = new User("田中太郎", 25);
        $user2 = new User("佐藤花子", 17);
        $user3 = new User("鈴木一郎", 30);
        
        // 自己紹介
        echo "<h2>自己紹介</h2>";
        $user1->introduce();
        $user2->introduce();
        $user3->introduce();
        
        // 成人判定
        echo "<h2>成人判定</h2>";
        
        $users = [$user1, $user2, $user3];
        foreach ($users as $user) {
            if ($user->isAdult()) {
                echo "<p class='adult'>✓ {$user->name}さんは成人です。</p>";
            } else {
                echo "<p class='minor'>✗ {$user->name}さんは未成年です。</p>";
            }
        }
        ?>
    </div>
</body>
</html>
```

---

## 🔍 よくある間違い

### 間違い1: `$this`の書き忘れ

```php
// ❌ 間違い（$thisがない）
public function introduce() {
    echo "私は{$name}です。";  // $nameは未定義
}

// ✅ 正しい
public function introduce() {
    echo "私は{$this->name}です。";
}
```

### 間違い2: アロー演算子の間違い

```php
// ❌ 間違い（ドットを使っている）
$user1.introduce();

// ✅ 正しい（アロー演算子を使う）
$user1->introduce();
```

### 間違い3: newの書き忘れ

```php
// ❌ 間違い（newがない）
$user1 = User("田中太郎", 25);

// ✅ 正しい
$user1 = new User("田中太郎", 25);
```

### 間違い4: コンストラクタ名のスペルミス

```php
// ❌ 間違い（アンダースコアが1つ）
public function _construct($name, $age) {
    // ...
}

// ✅ 正しい（アンダースコアが2つ）
public function __construct($name, $age) {
    // ...
}
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ クラスを定義できる
- ✅ プロパティを設定できる
- ✅ メソッドを作成して呼び出せる
- ✅ コンストラクタで初期化できる

次のChapter 4では、より実践的なオブジェクト指向の使い方を学んでいきます。引き続き頑張りましょう！

---
