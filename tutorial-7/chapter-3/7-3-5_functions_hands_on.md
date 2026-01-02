# Tutorial 7-3-5: 関数 - ハンズオン演習

## 📝 このセクションの目的

Chapter 3で学んだ関数の知識を実際に手を動かして確認します。関数を使ってコードを整理し、再利用可能なプログラムを作成しましょう。

**学習のポイント**：
- 関数を定義して呼び出せるか
- 引数と戻り値を正しく使えるか
- 複数の関数を組み合わせられるか

---

## 🎯 演習課題：BMI計算プログラムを作成しよう

### 課題の概要

BMI（Body Mass Index）を計算するプログラムを作成してください。関数を使って、計算処理と判定処理を分離します。

### 📋 要件

以下の要件を満たすPHPファイル（`bmi_calculator.php`）を作成してください。

> 📁 **作業ディレクトリ**: Tutorial 7-1-2で作成した`~/php-practice/src/`ディレクトリ内にファイルを作成してください。ブラウザで`http://localhost:8000/bmi_calculator.php`にアクセスして確認します。

#### 1. 関数の定義

以下の3つの関数を定義してください：

**関数1: `calculateBMI($weight, $height)`**
- 引数：体重（kg）、身長（m）
- 戻り値：BMI値（小数点第1位まで）
- 計算式：`BMI = 体重(kg) ÷ (身長(m) × 身長(m))`

**関数2: `getBMICategory($bmi)`**
- 引数：BMI値
- 戻り値：判定結果（文字列）
- 判定基準：

| BMI | 判定 |
|-----|------|
| 18.5未満 | 低体重 |
| 18.5以上25未満 | 普通体重 |
| 25以上30未満 | 肥満（1度） |
| 30以上 | 肥満（2度以上） |

**関数3: `displayBMIResult($name, $weight, $height)`**
- 引数：名前、体重（kg）、身長（cm）
- 戻り値：なし（直接HTMLを出力）
- 処理：BMIを計算して、結果を表示

#### 2. テストデータ

以下のデータを使って、関数をテストしてください：

```php
$people = [
    ["name" => "田中太郎", "weight" => 70, "height" => 175],
    ["name" => "佐藤花子", "weight" => 52, "height" => 160],
    ["name" => "鈴木一郎", "weight" => 85, "height" => 170],
    ["name" => "高橋美咲", "weight" => 48, "height" => 158],
];
```

**注意**：身長はcm単位で格納されているため、m単位に変換する必要があります。

#### 3. 表示要件

各人について、以下の情報を表示してください：

```
田中太郎さんのBMI結果
身長: 175cm
体重: 70kg
BMI: 22.9
判定: 普通体重
```

---

## 💡 ヒント

詰まったときは、以下のヒントを参考にしてください。

### ヒント1: BMI計算関数

```php
function calculateBMI($weight, $height) {
    $bmi = $weight / ($height * $height);
    return round($bmi, 1);
}
```

### ヒント2: BMI判定関数

```php
function getBMICategory($bmi) {
    if ($bmi < 18.5) {
        return "低体重";
    } elseif ($bmi < 25) {
        return "普通体重";
    } elseif ($bmi < 30) {
        return "肥満（1度）";
    } else {
        return "肥満（2度以上）";
    }
}
```

### ヒント3: 身長の単位変換

```php
$height_m = $height_cm / 100;
```

### ヒント4: 関数の呼び出し

```php
$bmi = calculateBMI(70, 1.75);
$category = getBMICategory($bmi);
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？関数はコードを再利用可能にする強力な機能です。一緒に手を動かしながら、BMI計算プログラムを作っていきましょう。

### 💭 実装の思考プロセス

BMI計算プログラムを作る際、以下の順番で考えると効率的です：

1. **BMI計算関数を作る**：体重と身長からBMIを計算
2. **判定関数を作る**：BMI値から体型を判定
3. **表示関数を作る**：結果を見やすく表示
4. **ユーザーデータを定義**：複数人のデータを配列で管理
5. **関数を組み合わせて実行**：各関数を呼び出して結果を表示

関数のポイントは「1つの関数に1つの役割」を持たせることです。

---

### 📝 ステップバイステップで実装

#### ステップ1: BMI計算関数を作る

**何を考えているか**：
- 「BMIの計算式は：体重(kg) ÷ (身長(m) × 身長(m))」
- 「小数点第1位まで表示したい」
- 「`round()`関数で四捨五入しよう」

まず、`~/php-practice/src/bmi_calculator.php`を作成して、BMIを計算する関数を作成します：

```php
<?php
// BMI計算関数
function calculateBMI($weight, $height) {
    $bmi = $weight / ($height * $height);
    return round($bmi, 1);
}
```

**コードリーディング**：

```php
function calculateBMI($weight, $height) {
```
→ 関数`calculateBMI`を定義します。引数として`$weight`（体重）と`$height`（身長）を受け取ります。

```php
    $bmi = $weight / ($height * $height);
```
→ BMIを計算します。身長を二乗するために`$height * $height`とし、体重をそれで割ります。括弧で囲むことで、先に二乗の計算が行われます。

```php
    return round($bmi, 1);
}
```
→ `round()`関数でBMI値を小数点第1位まで四捨五入して返します。第2引数の`1`が小数点以下の桁数を指定します。

---

#### ステップ2: BMI判定関数を作る

**何を考えているか**：
- 「BMI値に応じて体型を判定しよう」
- 「if文で範囲をチェックしよう」
- 「低い値から順番に判定するとわかりやすい」

次に、BMI値から体型を判定する関数を作成します：

```php
// BMI判定関数
function judgeBMI($bmi) {
    if ($bmi < 18.5) {
        return "低体重（痩せ型）";
    } elseif ($bmi < 25) {
        return "普通体重";
    } elseif ($bmi < 30) {
        return "肥満（1度）";
    } elseif ($bmi < 35) {
        return "肥満（2度）";
    } else {
        return "肥満（3度）";
    }
}
```

**コードリーディング**：

```php
function judgeBMI($bmi) {
```
→ 関数`judgeBMI`を定義します。引数としてBMI値を受け取ります。

```php
    if ($bmi < 18.5) {
        return "低体重（痩せ型）";
    }
```
→ BMIが18.5未満の場合、「低体重（痩せ型）」を返します。`<`は「未満」を意味します。

```php
    } elseif ($bmi < 25) {
        return "普通体重";
    }
```
→ BMIが18.5以上25未満の場合、「普通体重」を返します。前の条件ではじかれているので、18.5以上であることが保証されています。

```php
    } else {
        return "肥満（3度）";
    }
}
```
→ どの条件にも当てはまらない場合（BMI 35以上）、「肥満（3度）」を返します。

---

#### ステップ3: 結果表示関数を作る

**何を考えているか**：
- 「複数の情報を受け取って見やすく表示しよう」
- 「身長はcmに変換して表示しよう」
- 「HTMLタグを使って整形しよう」

次に、結果を表示する関数を作成します：

```php
// 結果表示関数
function displayResult($name, $height, $weight, $bmi, $judgment) {
    $height_cm = $height * 100;
    echo "<h3>{$name}さんのBMI結果</h3>";
    echo "身長: {$height_cm}cm<br>";
    echo "体重: {$weight}kg<br>";
    echo "BMI: {$bmi}<br>";
    echo "判定: <strong>{$judgment}</strong><br><br>";
}
```

**コードリーディング**：

```php
function displayResult($name, $height, $weight, $bmi, $judgment) {
```
→ 関数`displayResult`を定義します。5つの引数を受け取ります。

```php
    $height_cm = $height * 100;
```
→ 身長をm単位からcm単位に変換します。`1.75 * 100 = 175`という計算です。

```php
    echo "<h3>{$name}さんのBMI結果</h3>";
```
→ 名前を含む見出しを表示します。`<h3>`タグで見出しを作成します。

```php
    echo "判定: <strong>{$judgment}</strong><br><br>";
}
```
→ 判定結果を`<strong>`タグで太字にして表示します。`<br><br>`で空行を入れます。

---

#### ステップ4: ユーザーデータを定義して関数を実行する

**何を考えているか**：
- 「複数人のデータを配列で管理しよう」
- 「foreachでループして全員分を処理しよう」
- 「作成した3つの関数を組み合わせよう」

最後に、ユーザーデータを定義して、関数を実行します：

```php
// ユーザーデータの定義
$users = [
    ["name" => "田中太郎", "height" => 1.75, "weight" => 70],
    ["name" => "佐藤花子", "height" => 1.60, "weight" => 52],
    ["name" => "鈴木一郎", "height" => 1.70, "weight" => 85],
    ["name" => "高橋美咲", "height" => 1.58, "weight" => 48],
];

echo "<h2>BMI計算システム</h2>";

// 各ユーザーのBMIを計算して表示
foreach ($users as $user) {
    $bmi = calculateBMI($user["weight"], $user["height"]);
    $judgment = judgeBMI($bmi);
    displayResult($user["name"], $user["height"], $user["weight"], $bmi, $judgment);
}
?>
```

**コードリーディング**：

```php
$users = [
    ["name" => "田中太郎", "height" => 1.75, "weight" => 70],
    ...
];
```
→ ユーザーデータを配列の配列で定義します。身長はm単位で格納します。

```php
foreach ($users as $user) {
```
→ 各ユーザーのデータを順番に処理します。

```php
    $bmi = calculateBMI($user["weight"], $user["height"]);
```
→ `calculateBMI`関数を呼び出してBMIを計算します。体重と身長を引数として渡します。

```php
    $judgment = judgeBMI($bmi);
```
→ `judgeBMI`関数を呼び出して体型を判定します。

```php
    displayResult($user["name"], $user["height"], $user["weight"], $bmi, $judgment);
}
```
→ `displayResult`関数を呼び出して結果を表示します。必要な情報をすべて引数として渡します。

---

### ✨ 完成！

これでBMI計算プログラムが完成しました！関数の定義、引数、戻り値、関数の組み合わせを実践できましたね。

---

## ✅ 完成イメージ

完成すると、以下のような表示になります：

```
BMI計算システム

田中太郎さんのBMI結果
身長: 175cm
体重: 70kg
BMI: 22.9
判定: 普通体重

佐藤花子さんのBMI結果
身長: 160cm
体重: 52kg
BMI: 20.3
判定: 普通体重

鈴木一郎さんのBMI結果
身長: 170cm
体重: 85kg
BMI: 29.4
判定: 肥満（1度）

高橋美咲さんのBMI結果
身長: 158cm
体重: 48kg
BMI: 19.2
判定: 普通体重
```

---

## 🚀 チャレンジ

基本要件をクリアしたら、以下の追加課題にも挑戦してみましょう。

1. **適正体重の計算**：BMI 22を基準に、適正体重を計算する関数を追加

2. **体重の増減**：適正体重との差を計算して表示

3. **入力フォーム**：HTMLフォームから身長と体重を入力できるようにする

4. **グラフ表示**：BMI値を視覚的に表示（プログレスバーなど）

---

## 📖 模範解答

自分で実装してから、以下の模範解答を確認してください。

### bmi_calculator.php

```php
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BMI計算システム</title>
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
        .result {
            background-color: #f0f8ff;
            padding: 20px;
            margin: 20px 0;
            border-radius: 8px;
            border-left: 4px solid #0066cc;
        }
        .result h3 {
            color: #0066cc;
            margin-top: 0;
        }
        .result p {
            margin: 8px 0;
            font-size: 16px;
        }
        .bmi-value {
            font-size: 24px;
            font-weight: bold;
            color: #0066cc;
        }
        .category {
            font-size: 20px;
            font-weight: bold;
        }
        .category-normal { color: #28a745; }
        .category-underweight { color: #ffc107; }
        .category-overweight { color: #fd7e14; }
        .category-obese { color: #dc3545; }
    </style>
</head>
<body>
    <div class="container">
        <h1>BMI計算システム</h1>
        
        <?php
        // 関数1: BMI計算
        function calculateBMI($weight, $height) {
            $bmi = $weight / ($height * $height);
            return round($bmi, 1);
        }
        
        // 関数2: BMI判定
        function getBMICategory($bmi) {
            if ($bmi < 18.5) {
                return "低体重";
            } elseif ($bmi < 25) {
                return "普通体重";
            } elseif ($bmi < 30) {
                return "肥満（1度）";
            } else {
                return "肥満（2度以上）";
            }
        }
        
        // 関数3: BMI結果表示
        function displayBMIResult($name, $weight, $height) {
            // 身長をcmからmに変換
            $height_m = $height / 100;
            
            // BMI計算
            $bmi = calculateBMI($weight, $height_m);
            
            // 判定
            $category = getBMICategory($bmi);
            
            // CSSクラスの決定
            $categoryClass = "category-normal";
            if ($bmi < 18.5) {
                $categoryClass = "category-underweight";
            } elseif ($bmi >= 25 && $bmi < 30) {
                $categoryClass = "category-overweight";
            } elseif ($bmi >= 30) {
                $categoryClass = "category-obese";
            }
            
            // 結果の表示
            echo "<div class='result'>";
            echo "<h3>{$name}さんのBMI結果</h3>";
            echo "<p>身長: {$height}cm</p>";
            echo "<p>体重: {$weight}kg</p>";
            echo "<p>BMI: <span class='bmi-value'>{$bmi}</span></p>";
            echo "<p>判定: <span class='category {$categoryClass}'>{$category}</span></p>";
            echo "</div>";
        }
        
        // テストデータ
        $people = [
            ["name" => "田中太郎", "weight" => 70, "height" => 175],
            ["name" => "佐藤花子", "weight" => 52, "height" => 160],
            ["name" => "鈴木一郎", "weight" => 85, "height" => 170],
            ["name" => "高橋美咲", "weight" => 48, "height" => 158],
        ];
        
        // 各人のBMIを計算して表示
        foreach ($people as $person) {
            displayBMIResult($person["name"], $person["weight"], $person["height"]);
        }
        ?>
    </div>
</body>
</html>
```

---

## 🎓 解説

### ポイント1: 関数の定義

```php
function calculateBMI($weight, $height) {
    $bmi = $weight / ($height * $height);
    return round($bmi, 1);
}
```

- `function`キーワードで関数を定義
- `$weight`と`$height`は引数（パラメータ）
- `return`で計算結果を返す
- `round($bmi, 1)`で小数点第1位まで丸める

### ポイント2: 関数の呼び出し

```php
$bmi = calculateBMI(70, 1.75);
```

- 関数名と引数を指定して呼び出し
- 戻り値を変数に代入

### ポイント3: 関数の再利用

```php
function displayBMIResult($name, $weight, $height) {
    $height_m = $height / 100;
    $bmi = calculateBMI($weight, $height_m);  // 他の関数を呼び出し
    $category = getBMICategory($bmi);         // 他の関数を呼び出し
    // ...
}
```

- 関数の中から他の関数を呼び出せる
- 処理を小さな関数に分割して、組み合わせる

### ポイント4: 引数の型変換

```php
$height_m = $height / 100;  // cmをmに変換
```

- 関数に渡す前に、適切な単位に変換
- 関数内で変換することも可能

### ポイント5: 戻り値のない関数

```php
function displayBMIResult($name, $weight, $height) {
    echo "結果を表示";
    // returnなし
}
```

- `return`がない関数は、処理のみを行う
- 画面に直接出力する関数など

---

## 🔍 よくある間違い

### 間違い1: 関数名のスペルミス

```php
// ❌ 間違い（定義と呼び出しで名前が違う）
function calculateBMI($weight, $height) {
    // ...
}

$bmi = calculateBmi(70, 1.75);  // 小文字のbmi

// ✅ 正しい
$bmi = calculateBMI(70, 1.75);
```

### 間違い2: 引数の順序

```php
// ❌ 間違い（引数の順序が逆）
function calculateBMI($weight, $height) {
    return $weight / ($height * $height);
}

$bmi = calculateBMI(1.75, 70);  // 身長と体重が逆

// ✅ 正しい
$bmi = calculateBMI(70, 1.75);
```

### 間違い3: returnの忘れ

```php
// ❌ 間違い（returnがない）
function calculateBMI($weight, $height) {
    $bmi = $weight / ($height * $height);
    // returnなし
}

// ✅ 正しい
function calculateBMI($weight, $height) {
    $bmi = $weight / ($height * $height);
    return $bmi;
}
```

### 間違い4: 単位の変換忘れ

```php
// ❌ 間違い（身長がcm単位のまま）
$bmi = calculateBMI(70, 175);

// ✅ 正しい（m単位に変換）
$height_m = 175 / 100;
$bmi = calculateBMI(70, $height_m);
```

---

## 📚 次のステップ

関数をマスターしたら、次はオブジェクト指向を学びましょう！

Chapter 4では、クラスとオブジェクトを使った、より高度なプログラミング手法を学びます。

---

## 💪 自己評価チェックリスト

以下の項目ができたかチェックしましょう：

- [ ] 関数を定義できた
- [ ] 引数を正しく使えた
- [ ] 戻り値を返せた
- [ ] 関数を呼び出せた
- [ ] 複数の関数を組み合わせられた
- [ ] 関数の中から他の関数を呼び出せた
- [ ] 単位変換を正しく行えた
- [ ] ブラウザで正しく表示されることを確認できた

すべてチェックできたら、Chapter 4に進みましょう！
