# Tutorial 7-4-5: オブジェクト指向 - ハンズオン演習

## 📝 このセクションの目的

Chapter 4で学んだオブジェクト指向の知識を実際に手を動かして確認します。クラスとオブジェクトを使って、実践的なプログラムを作成しましょう。

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

## 🚀 チャレンジ

基本要件をクリアしたら、以下の追加課題にも挑戦してみましょう。

1. **取引履歴**：入出金の履歴を記録する機能を追加

2. **利息計算**：年利を設定して、利息を計算するメソッドを追加

3. **振込機能**：他の口座への振込メソッドを追加

4. **口座タイプ**：普通預金と定期預金を継承で実装

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

## 📚 次のステップ

オブジェクト指向をマスターしたら、次はデータベースを学びましょう！

Tutorial 8では、MySQLを使ったデータベースの基礎を学びます。

---

## 💪 自己評価チェックリスト

以下の項目ができたかチェックしましょう：

- [ ] クラスを定義できた
- [ ] プロパティを宣言できた
- [ ] コンストラクタを実装できた
- [ ] メソッドを定義できた
- [ ] `$this`を使ってプロパティにアクセスできた
- [ ] オブジェクトを生成できた
- [ ] メソッドを呼び出せた
- [ ] ブラウザで正しく表示されることを確認できた

すべてチェックできたら、Tutorial 8に進みましょう！
