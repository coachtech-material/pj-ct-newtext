# Tutorial 7-4-5: オブジェクト指向 - ハンズオン演習

## 📝 このセクションの目的

Chapter 4で学んだオブジェクト指向の知識を実際に手を動かして確認します。クラスとオブジェクトを使って、実践的なプログラムを作成しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

**学習のポイント**：
- クラスを定義できるか
- プロパティとメソッドを正しく使えるか
- オブジェクトを生成して操作できるか
- コンストラクタを活用できるか

---

## 🎯 演習課題：銀行口座管理システムを作成しよう

### 課題の概要

銀行口座を管理するシステムを、オブジェクト指向で作成してください。`BankAccount`クラスを定義し、入金・出金・残高照会の機能を実装します。

### 📋 要件

以下の要件を満たすPHPファイル（`bank_account.php`）を作成してください。

> 📁 **作業ディレクトリ**: Tutorial 7-1-2で作成した`~/php-practice/src/`ディレクトリ内にファイルを作成してください。ブラウザで`http://localhost:8000/bank_account.php`にアクセスして確認します。

#### 1. BankAccountクラスの定義

**プロパティ**：
- `$account_number`（口座番号）：文字列
- `$account_holder`（口座名義人）：文字列
- `$balance`（残高）：数値（初期値: 0）

**メソッド**：

1. **`__construct($account_number, $account_holder)`**
   - コンストラクタ
   - 口座番号と名義人を初期化

2. **`deposit($amount)`**
   - 入金処理
   - 引数：入金額
   - 処理：残高に入金額を加算
   - 戻り値：なし（メッセージを出力）

3. **`withdraw($amount)`**
   - 出金処理
   - 引数：出金額
   - 処理：残高が足りる場合のみ出金
   - 戻り値：成功/失敗（boolean）

4. **`getBalance()`**
   - 残高照会
   - 引数：なし
   - 戻り値：現在の残高

5. **`displayInfo()`**
   - 口座情報表示
   - 引数：なし
   - 処理：口座番号、名義人、残高を表示

#### 2. テストシナリオ

以下の操作を実行してください：

1. 田中太郎さんの口座を作成（口座番号: 1001）
2. 100,000円を入金
3. 30,000円を出金
4. 残高を確認
5. 口座情報を表示

6. 佐藤花子さんの口座を作成（口座番号: 1002）
7. 50,000円を入金
8. 60,000円を出金（残高不足）
9. 残高を確認
10. 口座情報を表示

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: クラスの定義

```php
class BankAccount {
    // プロパティ
    private $account_number;
    private $account_holder;
    private $balance = 0;
    
    // メソッド
    public function __construct($account_number, $account_holder) {
        // 初期化処理
    }
}
```

### ヒント2: コンストラクタ

```php
public function __construct($account_number, $account_holder) {
    $this->account_number = $account_number;
    $this->account_holder = $account_holder;
}
```

### ヒント3: 入金メソッド

```php
public function deposit($amount) {
    $this->balance += $amount;
    echo "入金: " . number_format($amount) . "円<br>";
}
```

### ヒント4: 出金メソッド

```php
public function withdraw($amount) {
    if ($this->balance >= $amount) {
        $this->balance -= $amount;
        return true;
    } else {
        return false;
    }
}
```

### ヒント5: オブジェクトの生成

```php
$account1 = new BankAccount("1001", "田中太郎");
$account1->deposit(100000);
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？オブジェクト指向はデータと処理をまとめる強力な手法です。一緒に手を動かしながら、銀行口座管理システムを作っていきましょう。

### 💭 実装の思考プロセス

銀行口座管理システムを作る際、以下の順番で考えると効率的です：

1. **クラスを設計する**：銀行口座に必要なデータ（プロパティ）と機能（メソッド）を考える
2. **プロパティを定義**：口座番号、名義人、残高を変数として定義
3. **コンストラクタを作る**：オブジェクト生成時に初期値を設定
4. **メソッドを実装**：入金、出金、残高照会の機能を作る
5. **オブジェクトを生成して使う**：クラスからオブジェクトを作成してメソッドを呼び出す

オブジェクト指向のポイントは「データとそれを操作する機能を一つにまとめる」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: クラスを定義してプロパティを追加する

**何を考えているか**：
- 「`BankAccount`クラスを作ろう」
- 「口座に必要なデータをプロパティとして定義しよう」
- 「`private`で外部から直接アクセスできないようにしよう」

まず、`~/php-practice/src/bank_account.php`を作成して、クラスを定義してプロパティを追加します：

```php
<?php
class BankAccount {
    private $account_number;
    private $account_holder;
    private $balance;
}
```

**コードリーディング**：

```php
class BankAccount {
```
→ `class`キーワードでクラスを定義します。クラス名は大文字で始めるのが慣例です。

```php
    private $account_number;
    private $account_holder;
    private $balance;
}
```
→ `private`でプロパティを定義します。`private`はクラス内部からしかアクセスできないことを意味します。これにより、データを保護します。

---

#### ステップ2: コンストラクタを作る

**何を考えているか**：
- 「オブジェクト生成時に口座番号と名義人を設定したい」
- 「`__construct()`メソッドを使おう」
- 「残高は0円で初期化しよう」

次に、コンストラクタを追加します：

```php
class BankAccount {
    private $account_number;
    private $account_holder;
    private $balance;
    
    public function __construct($account_number, $account_holder) {
        $this->account_number = $account_number;
        $this->account_holder = $account_holder;
        $this->balance = 0;
    }
}
```

**コードリーディング**：

```php
    public function __construct($account_number, $account_holder) {
```
→ コンストラクタを定義します。`__construct()`はオブジェクト生成時に自動的に呼び出される特殊なメソッドです。`public`は外部からアクセス可能であることを意味します。

```php
        $this->account_number = $account_number;
```
→ `$this`は現在のオブジェクト自身を指します。`$this->account_number`でプロパティにアクセスし、引数で受け取った値を代入します。

```php
        $this->account_holder = $account_holder;
        $this->balance = 0;
    }
```
→ 同様に名義人を設定し、残高を0で初期化します。

---

#### ステップ3: 入金メソッドを作る

**何を考えているか**：
- 「入金額を受け取って残高に加算しよう」
- 「負の値は入金できないようにチェックしよう」
- 「成功メッセージを表示しよう」

次に、入金メソッドを追加します：

```php
    public function deposit($amount) {
        if ($amount > 0) {
            $this->balance += $amount;
            echo "入金: " . number_format($amount) . "円<br>";
        } else {
            echo "エラー: 正の金額を指定してください<br>";
        }
    }
```

**コードリーディング**：

```php
    public function deposit($amount) {
```
→ `public`メソッド`deposit`を定義します。引数として入金額を受け取ります。

```php
        if ($amount > 0) {
```
→ 入金額が正の値かどうかをチェックします。負の値やゼロは入金できません。

```php
            $this->balance += $amount;
```
→ 残高に入金額を加算します。`+=`は加算代入演算子です。

```php
            echo "入金: " . number_format($amount) . "円<br>";
        } else {
            echo "エラー: 正の金額を指定してください<br>";
        }
    }
```
→ 成功メッセージまたはエラーメッセージを表示します。

---

#### ステップ4: 出金メソッドを作る

**何を考えているか**：
- 「出金額を受け取って残高から減算しよう」
- 「残高不足の場合はエラーを表示しよう」
- 「負の値は出金できないようにチェックしよう」

次に、出金メソッドを追加します：

```php
    public function withdraw($amount) {
        if ($amount <= 0) {
            echo "エラー: 正の金額を指定してください<br>";
        } elseif ($amount > $this->balance) {
            echo "出金失敗: 残高不足です（残高: " . number_format($this->balance) . "円、出金額: " . number_format($amount) . "円）<br>";
        } else {
            $this->balance -= $amount;
            echo "出金: " . number_format($amount) . "円<br>";
        }
    }
```

**コードリーディング**：

```php
    public function withdraw($amount) {
```
→ 出金メソッド`withdraw`を定義します。

```php
        if ($amount <= 0) {
            echo "エラー: 正の金額を指定してください<br>";
        }
```
→ 出金額がゼロ以下の場合、エラーを表示します。

```php
        } elseif ($amount > $this->balance) {
            echo "出金失敗: 残高不足です...<br>";
        }
```
→ 出金額が残高より大きい場合、残高不足エラーを表示します。

```php
        } else {
            $this->balance -= $amount;
            echo "出金: " . number_format($amount) . "円<br>";
        }
    }
```
→ 条件を満たす場合、残高から出金額を減算して、成功メッセージを表示します。

---

#### ステップ5: 口座情報表示メソッドを作る

**何を考えているか**：
- 「口座番号、名義人、残高を表示しよう」
- 「`private`プロパティにアクセスするためのメソッドを作ろう」

最後に、口座情報表示メソッドを追加します：

```php
    public function displayInfo() {
        echo "<h3>口座情報:</h3>";
        echo "口座番号: {$this->account_number}<br>";
        echo "名義人: {$this->account_holder}<br>";
        echo "残高: " . number_format($this->balance) . "円<br><br>";
    }
    
    public function getBalance() {
        return $this->balance;
    }
}
```

**コードリーディング**：

```php
    public function displayInfo() {
```
→ 口座情報を表示するメソッドを定義します。

```php
        echo "口座番号: {$this->account_number}<br>";
        echo "名義人: {$this->account_holder}<br>";
        echo "残高: " . number_format($this->balance) . "円<br><br>";
    }
```
→ `$this`でプロパティにアクセスして、口座情報を表示します。

```php
    public function getBalance() {
        return $this->balance;
    }
}
```
→ 残高を取得するメソッドを定義します。`private`プロパティに外部からアクセスするために、このようなメソッド（ゲッター）を作成します。

---

#### ステップ6: オブジェクトを生成して使う

**何を考えているか**：
- 「`new`キーワードでオブジェクトを生成しよう」
- 「メソッドを呼び出して入出金を実行しよう」
- 「複数のオブジェクトを作成して、それぞれ独立して管理しよう」

最後に、オブジェクトを生成して使用します：

```php
echo "<h2>銀行口座管理システム</h2>";

// 田中太郎さんの口座
echo "<h3>【田中太郎さんの口座】</h3>";
$account1 = new BankAccount("1001", "田中太郎");
$account1->deposit(100000);
$account1->withdraw(30000);
echo "現在の残高: " . number_format($account1->getBalance()) . "円<br><br>";
$account1->displayInfo();

// 佐藤花子さんの口座
echo "<h3>【佐藤花子さんの口座】</h3>";
$account2 = new BankAccount("1002", "佐藤花子");
$account2->deposit(50000);
$account2->withdraw(60000);
echo "現在の残高: " . number_format($account2->getBalance()) . "円<br><br>";
$account2->displayInfo();
?>
```

**コードリーディング**：

```php
$account1 = new BankAccount("1001", "田中太郎");
```
→ `new`キーワードで`BankAccount`クラスのオブジェクトを生成します。コンストラクタに口座番号と名義人を渡します。

```php
$account1->deposit(100000);
```
→ `->` 演算子でオブジェクトのメソッドを呼び出します。`deposit`メソッドで100,000円を入金します。

```php
$account1->withdraw(30000);
```
→ 同様に`withdraw`メソッドで30,000円を出金します。

```php
echo "現在の残高: " . number_format($account1->getBalance()) . "円<br><br>";
```
→ `getBalance()`メソッドで残高を取得して表示します。

```php
$account1->displayInfo();
```
→ `displayInfo()`メソッドで口座情報を表示します。

```php
$account2 = new BankAccount("1002", "佐藤花子");
```
→ 2番目のオブジェクトを生成します。`$account1`と`$account2`はそれぞれ独立したオブジェクトで、別々のデータを持ちます。

---

### ✨ 完成！

これで銀行口座管理システムが完成しました！クラス、プロパティ、メソッド、コンストラクタ、オブジェクトの生成と使用を実践できましたね。

---

## ✅ 完成イメージ

完成すると、以下のような表示になります：

```
銀行口座管理システム

【田中太郎さんの口座】
入金: 100,000円
出金: 30,000円
現在の残高: 70,000円

口座情報:
口座番号: 1001
名義人: 田中太郎
残高: 70,000円

【佐藤花子さんの口座】
入金: 50,000円
出金失敗: 残高不足です（残高: 50,000円、出金額: 60,000円）
現在の残高: 50,000円

口座情報:
口座番号: 1002
名義人: 佐藤花子
残高: 50,000円
```

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### bank_account.php

```php
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>銀行口座管理システム</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
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
            border-left: 4px solid #0066cc;
            padding-left: 10px;
        }
        .transaction {
            background-color: #f0f8ff;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
        }
        .success {
            color: #28a745;
            font-weight: bold;
        }
        .error {
            color: #dc3545;
            font-weight: bold;
        }
        .info {
            background-color: #e7f3ff;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            border-left: 4px solid #0066cc;
        }
        .info p {
            margin: 8px 0;
            font-size: 16px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>銀行口座管理システム</h1>
        
        <?php
        // BankAccountクラスの定義
        class BankAccount {
            // プロパティ
            private $account_number;
            private $account_holder;
            private $balance = 0;
            
            // コンストラクタ
            public function __construct($account_number, $account_holder) {
                $this->account_number = $account_number;
                $this->account_holder = $account_holder;
            }
            
            // 入金メソッド
            public function deposit($amount) {
                $this->balance += $amount;
                echo "<div class='transaction'>";
                echo "<span class='success'>入金: " . number_format($amount) . "円</span>";
                echo "</div>";
            }
            
            // 出金メソッド
            public function withdraw($amount) {
                if ($this->balance >= $amount) {
                    $this->balance -= $amount;
                    echo "<div class='transaction'>";
                    echo "<span class='success'>出金: " . number_format($amount) . "円</span>";
                    echo "</div>";
                    return true;
                } else {
                    echo "<div class='transaction'>";
                    echo "<span class='error'>出金失敗: 残高不足です";
                    echo "（残高: " . number_format($this->balance) . "円、";
                    echo "出金額: " . number_format($amount) . "円）</span>";
                    echo "</div>";
                    return false;
                }
            }
            
            // 残高照会メソッド
            public function getBalance() {
                return $this->balance;
            }
            
            // 口座情報表示メソッド
            public function displayInfo() {
                echo "<div class='info'>";
                echo "<p><strong>口座情報:</strong></p>";
                echo "<p>口座番号: {$this->account_number}</p>";
                echo "<p>名義人: {$this->account_holder}</p>";
                echo "<p>残高: <strong>" . number_format($this->balance) . "円</strong></p>";
                echo "</div>";
            }
        }
        
        // 田中太郎さんの口座
        echo "<h2>【田中太郎さんの口座】</h2>";
        $account1 = new BankAccount("1001", "田中太郎");
        $account1->deposit(100000);
        $account1->withdraw(30000);
        echo "<p>現在の残高: <strong>" . number_format($account1->getBalance()) . "円</strong></p>";
        $account1->displayInfo();
        
        // 佐藤花子さんの口座
        echo "<h2>【佐藤花子さんの口座】</h2>";
        $account2 = new BankAccount("1002", "佐藤花子");
        $account2->deposit(50000);
        $account2->withdraw(60000);  // 残高不足
        echo "<p>現在の残高: <strong>" . number_format($account2->getBalance()) . "円</strong></p>";
        $account2->displayInfo();
        ?>
    </div>
</body>
</html>
```

---

## 🎓 解説

### ポイント1: クラスの定義

```php
class BankAccount {
    private $account_number;
    private $account_holder;
    private $balance = 0;
}
```

- `class`キーワードでクラスを定義
- `private`でプロパティを非公開に（カプセル化）
- プロパティに初期値を設定可能

### ポイント2: コンストラクタ

```php
public function __construct($account_number, $account_holder) {
    $this->account_number = $account_number;
    $this->account_holder = $account_holder;
}
```

- `__construct()`はオブジェクト生成時に自動実行
- `$this`は自分自身のオブジェクトを指す
- プロパティの初期化に使用

### ポイント3: メソッドの定義

```php
public function deposit($amount) {
    $this->balance += $amount;
}
```

- `public`で外部から呼び出し可能に
- `$this->balance`でプロパティにアクセス

### ポイント4: オブジェクトの生成

```php
$account1 = new BankAccount("1001", "田中太郎");
```

- `new`キーワードでオブジェクトを生成
- コンストラクタの引数を渡す

### ポイント5: メソッドの呼び出し

```php
$account1->deposit(100000);
$account1->withdraw(30000);
$balance = $account1->getBalance();
```

- `->`演算子でメソッドを呼び出し
- 戻り値を変数に代入可能

---

## 🔍 よくある間違い

### 間違い1: $thisの忘れ

```php
// ❌ 間違い
public function deposit($amount) {
    balance += $amount;  // $thisがない
}

// ✅ 正しい
public function deposit($amount) {
    $this->balance += $amount;
}
```

### 間違い2: アクセス修飾子の省略

```php
// ❌ 間違い（publicを省略）
function deposit($amount) {
    // ...
}

// ✅ 正しい
public function deposit($amount) {
    // ...
}
```

### 間違い3: newの忘れ

```php
// ❌ 間違い
$account1 = BankAccount("1001", "田中太郎");

// ✅ 正しい
$account1 = new BankAccount("1001", "田中太郎");
```

### 間違い4: メソッド呼び出しの演算子

```php
// ❌ 間違い（.を使っている）
$account1.deposit(100000);

// ✅ 正しい（->を使う）
$account1->deposit(100000);
```

---

## 📊 関数 vs オブジェクト指向

### 関数を使った実装

```php
$balance1 = 0;
$balance2 = 0;

function deposit(&$balance, $amount) {
    $balance += $amount;
}

deposit($balance1, 100000);
deposit($balance2, 50000);
```

### オブジェクト指向の実装

```php
$account1 = new BankAccount("1001", "田中太郎");
$account2 = new BankAccount("1002", "佐藤花子");

$account1->deposit(100000);
$account2->deposit(50000);
```

**オブジェクト指向の利点**：
- データとメソッドをまとめて管理
- 複数のオブジェクトを簡単に扱える
- コードの再利用性が高い
- 実世界のモデルを表現しやすい
---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ クラスを定義できる
- ✅ プロパティとメソッドを正しく使える
- ✅ オブジェクトを生成して操作できる
- ✅ コンストラクタを活用できる

引き続き、次のセクションも頑張りましょう！

---
