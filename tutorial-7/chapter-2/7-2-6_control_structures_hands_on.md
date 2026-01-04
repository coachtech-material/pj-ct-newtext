# Tutorial 7-2-6: 制御構文 - ハンズオン演習

## 📝 このセクションの目的

Chapter 2で学んだ制御構文（if文、switch文、for文、while文）を実際に手を動かして確認します。条件分岐とループ処理を使った実践的なプログラムを作成しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

**学習のポイント**：
- if文で条件分岐ができるか
- switch文を適切に使えるか
- for文でループ処理ができるか
- while文を正しく使えるか

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのディレクトリを作成します。

Tutorial 6で作成した`php-practice`ディレクトリ内の`src/`フォルダに、ハンズオン用のディレクトリを作成します。

```
~/php-practice/
├── docker/
│   └── nginx/
│       └── default.conf
├── src/
│   ├── index.php                         ← Tutorial 6で作成済み
│   ├── 7-1-5_hands-on/                   ← Tutorial 7-1-5のハンズオン
│   │   ├── practice/
│   │   └── sample/
│   └── 7-2-6_hands-on/                   ← このハンズオン用のディレクトリ
│       ├── practice/                     ← 要件を見て自分で作成するディレクトリ
│       │   └── grade_calculator.php
│       └── sample/                       ← 実践で一緒に作成するディレクトリ
│           └── grade_calculator.php
└── docker-compose.yml
```

| ディレクトリ | 用途 | アクセスURL |
|:---|:---|:---|
| `practice/` | 📋 要件を見て、自分の力で作成する | `http://localhost:8000/7-2-6_hands-on/practice/grade_calculator.php` |
| `sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する | `http://localhost:8000/7-2-6_hands-on/sample/grade_calculator.php` |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

---

## 🎯 演習課題：成績判定プログラムを作成しよう

### 課題の概要

学生の成績を判定するプログラムを作成してください。点数に応じて評価を表示し、複数の学生の成績を一覧表示します。

---

### 📁 Step 0: 環境を準備する

まず、ハンズオン用のディレクトリを作成します。ターミナルで以下のコマンドを実行してください。

```bash
# php-practiceディレクトリに移動
cd ~/php-practice

# ハンズオン用ディレクトリを作成
mkdir -p src/7-2-6_hands-on/practice
mkdir -p src/7-2-6_hands-on/sample

# 自分で作成する用のディレクトリに移動
cd src/7-2-6_hands-on/practice

# VSCodeでphp-practiceプロジェクト全体を開く
code ~/php-practice
```

**コマンド解説**：

| コマンド | 説明 |
|:---|:---|
| `cd ~/php-practice` | php-practiceディレクトリに移動します |
| `mkdir -p` | ディレクトリを作成します。`-p`オプションで、親ディレクトリも一緒に作成します |
| `code ~/php-practice` | php-practiceディレクトリ全体をVSCodeで開きます |

**Docker環境の起動**：

```bash
# php-practiceディレクトリでDocker環境を起動
cd ~/php-practice
docker-compose up -d
```

> 📌 **確認**: ブラウザで`http://localhost:8000`にアクセスして、「Hello from Docker!」が表示されることを確認してください。

---

### 📋 要件

以下の要件を満たすPHPファイル（`grade_calculator.php`）を`practice/`ディレクトリ内に作成してください。

#### 1. 学生データの定義

以下の配列を定義してください：

```php
$students = [
    ["name" => "田中太郎", "score" => 85],
    ["name" => "佐藤花子", "score" => 92],
    ["name" => "鈴木一郎", "score" => 78],
    ["name" => "高橋美咲", "score" => 65],
    ["name" => "伊藤健太", "score" => 58],
];
```

#### 2. 成績判定ロジック

点数に応じて、以下の評価を返す処理を実装してください：

| 点数 | 評価 | 判定 |
|------|------|------|
| 90点以上 | A | 優秀 |
| 80点以上90点未満 | B | 良好 |
| 70点以上80点未満 | C | 普通 |
| 60点以上70点未満 | D | 要努力 |
| 60点未満 | F | 不合格 |

#### 3. 表示要件

以下の情報を表示してください：

1. **個別の成績表示**：
   - 各学生の名前、点数、評価、判定を表示
   - 例: 「田中太郎: 85点 - 評価B（良好）」

2. **統計情報**：
   - 合格者数（60点以上）
   - 不合格者数（60点未満）
   - 平均点

3. **HTMLテーブル**：
   - 成績を表形式で見やすく表示

#### 4. 使用する制御構文

- **if文**：点数に応じた評価の判定
- **for文**：学生データのループ処理
- **条件演算子**：合格/不合格の判定

**動作確認URL**: `http://localhost:8000/7-2-6_hands-on/practice/grade_calculator.php`

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: 配列のループ

```php
foreach ($students as $student) {
    echo $student["name"];
    echo $student["score"];
}
```

### ヒント2: if-elseif-else文

```php
if ($score >= 90) {
    $grade = "A";
    $status = "優秀";
} elseif ($score >= 80) {
    $grade = "B";
    $status = "良好";
} else {
    $grade = "F";
    $status = "不合格";
}
```

### ヒント3: カウンター変数

```php
$pass_count = 0;
$fail_count = 0;

foreach ($students as $student) {
    if ($student["score"] >= 60) {
        $pass_count++;
    } else {
        $fail_count++;
    }
}
```

### ヒント4: 平均点の計算

```php
$total_score = 0;
foreach ($students as $student) {
    $total_score += $student["score"];
}
$average = $total_score / count($students);
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？制御構文はif文とループが基本です。一緒に手を動かしながら、成績判定プログラムを作っていきましょう。

> 📌 **注意**: ここからは`sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のディレクトリで進めましょう。

### 💭 実装の思考プロセス

成績判定プログラムを作る際、以下の順番で考えると効率的です：

1. **学生データを配列で定義**：複数の学生の名前と点数を格納
2. **評価判定ロジックを作る**：if文で点数に応じて評価を返す
3. **ループで全員の成績を処理**：foreachで配列をループ
4. **統計情報を計算**：合格者数、不合格者数、平均点を計算
5. **結果を表示**：echoで見やすく出力

制御構文のポイントは「条件分岐」と「繰り返し」を組み合わせることです。

---

### 📝 ステップバイステップで実装

#### ステップ1: 実践用ディレクトリに移動し、PHPファイルを作成する

**何を考えているか**：
- 「`sample/`ディレクトリに`grade_calculator.php`を作ろう」
- 「複数の学生のデータをまとめて管理したい」
- 「連想配列を使って名前と点数をペアにしよう」

まず、ターミナルで以下のコマンドを実行して、実践用ディレクトリに移動します：

```bash
# 実践用ディレクトリに移動
cd ~/php-practice/src/7-2-6_hands-on/sample

# PHPファイルを作成
touch grade_calculator.php
```

VSCodeのエクスプローラーで`src/7-2-6_hands-on/sample/grade_calculator.php`を開いてください。

**✅ ディレクトリ構造の確認**

ファイルを作成すると、以下のようなディレクトリ構造になります。この構造になっていれば正解です！

```
~/php-practice/
├── docker/
│   └── nginx/
│       └── default.conf
├── src/
│   ├── index.php
│   ├── 7-1-5_hands-on/
│   │   ├── practice/
│   │   └── sample/
│   └── 7-2-6_hands-on/
│       ├── practice/
│       │   └── grade_calculator.php    ← 自分で作成したファイル
│       └── sample/
│           └── grade_calculator.php    ← これから一緒に作成するファイル
└── docker-compose.yml
```

`src/7-2-6_hands-on/sample/grade_calculator.php`ファイルに、学生データを定義します：

```php
<?php
// 学生データの定義
$students = [
    ["name" => "田中太郎", "score" => 85],
    ["name" => "佐藤花子", "score" => 92],
    ["name" => "鈴木一郎", "score" => 78],
    ["name" => "高橋美咲", "score" => 65],
    ["name" => "伊藤健太", "score" => 58],
];
```

**コードリーディング**：

```php
$students = [
```
→ 変数`$students`に配列を代入します。`[`と`]`で配列を定義します。

```php
    ["name" => "田中太郎", "score" => 85],
```
→ 配列の中に連想配列を入れます。`=>`でキーと値を結びつけます。`"name"`キーに「田中太郎」、`"score"`キーに`85`を格納します。

```php
    ["name" => "佐藤花子", "score" => 92],
```
→ 2番目の学生のデータです。同じ構造で名前と点数を格納します。

```php
];
```
→ 配列の終了です。最後にセミコロンを付けます。

---

#### ステップ2: 評価判定関数を作る

**何を考えているか**：
- 「点数を受け取って評価を返す関数を作ろう」
- 「if文で点数の範囲を判定しよう」
- 「高い点数から順番に判定するとシンプル」

次に、評価判定関数を作成します：

```php
// 評価判定関数
function getGrade($score) {
    if ($score >= 90) {
        return "A";
    } elseif ($score >= 80) {
        return "B";
    } elseif ($score >= 70) {
        return "C";
    } elseif ($score >= 60) {
        return "D";
    } else {
        return "F";
    }
}
```

**コードリーディング（1行ずつ）**：

```php
function getGrade($score) {
```
→ 関数`getGrade`を定義します。引数`$score`で点数を受け取ります。

```php
    if ($score >= 90) {
```
→ if文で条件判定を開始します。`>=`は「以上」を意味します。90点以上かどうかをチェックします。

```php
        return "A";
```
→ 条件が真の場合、文字列「A」を返します。`return`で関数から値を返し、関数の実行を終了します。

```php
    } elseif ($score >= 80) {
```
→ `elseif`で次の条件をチェックします。80点以上90点未満の場合にこの条件が真になります。

```php
        return "B";
```
→ 80点以上の場合、「B」を返します。

```php
    } else {
        return "F";
    }
}
```
→ `else`で、どの条件にも当てはまらない場合（60点未満）に「F」を返します。

---

#### ステップ3: 全員の成績をループで処理する

**何を考えているか**：
- 「foreachで配列をループしよう」
- 「各学生の点数を取得して評価を判定しよう」
- 「結果を表示しながら、統計情報も集計しよう」

次に、ループで全員の成績を処理します：

```php
// 統計情報の初期化
$pass_count = 0;
$fail_count = 0;
$total_score = 0;

echo "<h2>成績判定システム</h2>";
echo "<h3>【個別成績】</h3>";

// 各学生の成績を処理
foreach ($students as $student) {
    $name = $student["name"];
    $score = $student["score"];
    $grade = getGrade($score);
    
    // 合格・不合格のカウント
    if ($score >= 60) {
        $pass_count++;
    } else {
        $fail_count++;
    }
    
    // 合計点の集計
    $total_score += $score;
    
    // 結果の表示
    echo "{$name}: {$score}点 - 評価{$grade}<br>";
}
```

**コードリーディング**：

```php
$pass_count = 0;
$fail_count = 0;
$total_score = 0;
```
→ 統計情報を格納する変数を0で初期化します。ループ内で値を加算していきます。

```php
foreach ($students as $student) {
```
→ `foreach`で配列`$students`をループします。各要素が`$student`に代入されて、ループが実行されます。

```php
    $name = $student["name"];
    $score = $student["score"];
```
→ 連想配列から名前と点数を取得して、変数に格納します。

```php
    $grade = getGrade($score);
```
→ 先ほど作成した`getGrade`関数を呼び出して、評価を取得します。

```php
    if ($score >= 60) {
        $pass_count++;
    } else {
        $fail_count++;
    }
```
→ 60点以上かどうかで、合格者数または不合格者数をインクリメントします。`++`は1を加算する演算子です。

```php
    $total_score += $score;
```
→ 合計点に現在の学生の点数を加算します。`+=`は加算代入演算子です。

```php
    echo "{$name}: {$score}点 - 評価{$grade}<br>";
}
```
→ 各学生の成績を表示します。`{$name}`のように中括弧で囲むと、ダブルクォート内で変数を展開できます。

---

#### ステップ4: 統計情報を表示する

**何を考えているか**：
- 「平均点を計算しよう：合計点÷人数」
- 「統計情報を見やすく表示しよう」

最後に、統計情報を表示します：

```php
// 平均点の計算
$average = $total_score / count($students);

echo "<h3>【統計情報】</h3>";
echo "合格者数: {$pass_count}人<br>";
echo "不合格者数: {$fail_count}人<br>";
echo "平均点: " . number_format($average, 1) . "点<br>";
?>
```

**コードリーディング**：

```php
$average = $total_score / count($students);
```
→ 平均点を計算します。`count()`関数で配列の要素数を取得し、合計点を割ります。

```php
echo "平均点: " . number_format($average, 1) . "点<br>";
```
→ `number_format($average, 1)`で小数点以下1桁にフォーマットします。`75.6`のように表示されます。

---

#### ステップ5: ブラウザで確認する

**何を考えているか**：
- 「ファイルを保存してブラウザで開こう」
- 「意図通りに表示されているか確認しよう」

1. ファイルを保存します
2. Docker環境が起動していることを確認します（`docker-compose up -d`）
3. ブラウザで`http://localhost:8000/7-2-6_hands-on/sample/grade_calculator.php`を開きます
4. 成績一覧と統計情報が表示されることを確認します

---

### ✨ 完成！

これで成績判定プログラムが完成しました！if文、foreachループ、関数の使い方を実践できましたね。

**自分で作成したコードと比較してみましょう**：
- `practice/grade_calculator.php`: 自分で作成したコード
- `sample/grade_calculator.php`: 一緒に作成したコード

両方のファイルを見比べて、違いがあれば確認してみてください。

---

## ✅ 完成イメージ

完成すると、以下のような表示になります：

```
成績判定システム

【個別成績】
田中太郎: 85点 - 評価B（良好）
佐藤花子: 92点 - 評価A（優秀）
鈴木一郎: 78点 - 評価C（普通）
高橋美咲: 65点 - 評価D（要努力）
伊藤健太: 58点 - 評価F（不合格）

【統計情報】
合格者数: 4人
不合格者数: 1人
平均点: 75.6点
```

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### grade_calculator.php

```php
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>成績判定システム</title>
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
            background-color: #0066cc;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .stats {
            background-color: #f0f8ff;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .stats p {
            margin: 10px 0;
            font-size: 18px;
        }
        .grade-A { color: #28a745; font-weight: bold; }
        .grade-B { color: #17a2b8; font-weight: bold; }
        .grade-C { color: #ffc107; font-weight: bold; }
        .grade-D { color: #fd7e14; font-weight: bold; }
        .grade-F { color: #dc3545; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>成績判定システム</h1>
        
        <?php
        // 学生データの定義
        $students = [
            ["name" => "田中太郎", "score" => 85],
            ["name" => "佐藤花子", "score" => 92],
            ["name" => "鈴木一郎", "score" => 78],
            ["name" => "高橋美咲", "score" => 65],
            ["name" => "伊藤健太", "score" => 58],
        ];
        
        // 成績判定関数
        function getGrade($score) {
            if ($score >= 90) {
                return ["grade" => "A", "status" => "優秀"];
            } elseif ($score >= 80) {
                return ["grade" => "B", "status" => "良好"];
            } elseif ($score >= 70) {
                return ["grade" => "C", "status" => "普通"];
            } elseif ($score >= 60) {
                return ["grade" => "D", "status" => "要努力"];
            } else {
                return ["grade" => "F", "status" => "不合格"];
            }
        }
        
        // 統計情報の初期化
        $pass_count = 0;
        $fail_count = 0;
        $total_score = 0;
        
        // 個別成績の表示
        echo "<h2>【個別成績】</h2>";
        echo "<table>";
        echo "<tr><th>名前</th><th>点数</th><th>評価</th><th>判定</th></tr>";
        
        foreach ($students as $student) {
            $name = $student["name"];
            $score = $student["score"];
            $result = getGrade($score);
            $grade = $result["grade"];
            $status = $result["status"];
            
            // 統計情報の集計
            $total_score += $score;
            if ($score >= 60) {
                $pass_count++;
            } else {
                $fail_count++;
            }
            
            // テーブル行の表示
            echo "<tr>";
            echo "<td>{$name}</td>";
            echo "<td>{$score}点</td>";
            echo "<td class='grade-{$grade}'>{$grade}</td>";
            echo "<td>{$status}</td>";
            echo "</tr>";
        }
        
        echo "</table>";
        
        // 平均点の計算
        $average = $total_score / count($students);
        
        // 統計情報の表示
        echo "<h2>【統計情報】</h2>";
        echo "<div class='stats'>";
        echo "<p>合格者数: <strong>{$pass_count}人</strong></p>";
        echo "<p>不合格者数: <strong>{$fail_count}人</strong></p>";
        echo "<p>平均点: <strong>" . number_format($average, 1) . "点</strong></p>";
        echo "</div>";
        ?>
    </div>
</body>
</html>
```

---

---

## 🔍 よくある間違い

### 間違い1: elseifのスペル

```php
// ❌ 間違い
else if ($score >= 80) {

// ✅ 正しい
elseif ($score >= 80) {
```

PHPでは`elseif`を1語で書きます（`else if`も動作しますが、`elseif`が推奨）。

### 間違い2: 条件の順序

```php
// ❌ 間違い（60点以上が先に評価される）
if ($score >= 60) {
    $grade = "D";
} elseif ($score >= 90) {
    $grade = "A";
}

// ✅ 正しい（高い点数から評価）
if ($score >= 90) {
    $grade = "A";
} elseif ($score >= 60) {
    $grade = "D";
}
```

### 間違い3: 配列のキー名の間違い

```php
// ❌ 間違い
echo $student["nama"];  // キー名が違う

// ✅ 正しい
echo $student["name"];
```

### 間違い4: カウンターの初期化忘れ

```php
// ❌ 間違い（初期化していない）
foreach ($students as $student) {
    $pass_count++;
}

// ✅ 正しい（先に初期化）
$pass_count = 0;
foreach ($students as $student) {
    $pass_count++;
}
```

---

## 🧪 動作確認の方法

### Docker環境で実行

Tutorial 6で構築したDocker環境を使用します。

1. Docker環境を起動（`cd ~/php-practice && docker-compose up -d`）
2. ブラウザで以下のURLにアクセス：
   - 自分で作成したコード: `http://localhost:8000/7-2-6_hands-on/practice/grade_calculator.php`
   - 一緒に作成したコード: `http://localhost:8000/7-2-6_hands-on/sample/grade_calculator.php`

> 💡 **ヒント**: ファイルを保存すると、ブラウザをリロードするだけで変更が反映されます。

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ if文で条件分岐ができる
- ✅ switch文を適切に使える
- ✅ for文でループ処理ができる
- ✅ while文を正しく使える

引き続き、次のセクションも頑張りましょう！

---
