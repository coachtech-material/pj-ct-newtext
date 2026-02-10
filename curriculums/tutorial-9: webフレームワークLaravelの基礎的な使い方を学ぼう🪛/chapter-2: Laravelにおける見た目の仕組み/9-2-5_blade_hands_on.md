# Tutorial 9-2-5: Bladeテンプレート - ハンズオン演習

## 📌 このハンズオンについて

Chapter 2で学んだBladeテンプレートを実際に手を動かして確認します。**提供されたBladeファイルを読み解き、コントローラーから適切なデータを渡して画面を表示させる**演習を行います。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

### ディレクトリ構成

このハンズオンでは、「自分で作成する用」と「解答を確認する用」の2つのプロジェクトを作成します。

```
~/laravel-practice/
├── 9-2-5_hands-on/                       ← このハンズオン用のディレクトリ
│   ├── blade-app-practice/               ← 要件を見て自分で作成するプロジェクト
│   │   ├── app/
│   │   ├── resources/
│   │   ├── routes/
│   │   └── ...
│   └── blade-app-sample/                 ← 実践で一緒に作成するプロジェクト
│       ├── app/
│       ├── resources/
│       ├── routes/
│       └── ...
└── ...
```

| ディレクトリ | 用途 | URL |
|:---|:---|:---|
| `blade-app-practice/` | 📋 要件を見て、自分の力で作成する | `http://localhost/products` |
| `blade-app-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する | `http://localhost/products` |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

> ⚠️ **注意**: 2つのプロジェクトを同時に起動することはできません（ポートが競合するため）。一方のプロジェクトで作業する際は、もう一方を停止してください。

---

## 🎯 演習課題：提供されたBladeファイルを動かそう

**この演習で作るもの**：
提供されたBladeファイルを読み解き、コントローラーから適切なデータを渡して「商品一覧ページ」を表示させます。

### 🖼️ 完成イメージ

**商品一覧ページ完成画面**

<img alt="9-2-5_1.png" src="https://s3.ap-northeast-1.amazonaws.com/coachtech-lms-bucket-dev/curriculums/images/9-2-5_1.png">

---

### 📋 要件

フロントエンドエンジニアから提供されたBladeファイルを読み解き、コントローラーから適切なデータを渡して画面を表示させます。

- `/products`にアクセスすると、商品一覧ページが表示される
- 商品データ（名前、カテゴリ、価格、在庫状況）がテーブル形式で表示される
- 在庫ありは緑色、在庫なしは赤色で表示される

---

### ✅ 完成チェックリスト

- [ ] `/products`にアクセスすると「商品一覧」というタイトルが表示される
- [ ] 「全3件の商品があります」と表示される
- [ ] 商品がテーブル形式で表示される（No.、商品名、カテゴリ、価格、在庫状況）
- [ ] 在庫ありの商品は緑色、在庫なしの商品は赤色で表示される
- [ ] 最終更新日時が表示される

> 💡 **動作確認**: `http://localhost/products` にアクセス

---

### ✏️ 実装タスク

1. Bladeファイルを読み解き、必要な変数を特定する
2. `ProductController`を作成し、データを渡す
3. ルーティングを設定する
4. Bladeファイルを配置する

> 💡 Bladeファイルは「⚙️ 環境準備」セクションで提供します。

---

## ⚙️ 環境準備（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

> **📌 前のハンズオンのプロジェクトを停止**
>
> 前のハンズオン（9-1-8）のプロジェクトが起動している場合は、先に停止してください。
> ```bash
> cd ~/laravel-practice/9-1-8_hands-on/profile-app-sample
> ./vendor/bin/sail down
> ```

```bash
# laravel-practiceディレクトリに移動
cd ~/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 9-2-5_hands-on
cd 9-2-5_hands-on
```

```bash
# Laravel 10.xプロジェクトを作成（自分で作成する用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 blade-app-practice
```

```bash
# プロジェクトディレクトリに移動
cd blade-app-practice

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql
```

<details>
<summary>⚠️ M1/M2/M3 Mac（Apple Silicon）をお使いの方</summary>

Apple Silicon搭載のMacでは、`sail up -d`実行時に以下のエラーが発生することがあります：

```
no matching manifest for linux/arm64/v8
```

**解決方法**: `compose.yaml`を開き、mysqlサービスに`platform: 'linux/amd64'`を追加してください。

```yaml
mysql:
    image: 'mysql/mysql-server:8.0'
    platform: 'linux/amd64'  # ← この行を追加
    ports:
        ...
```

編集後、保存してから`sail up -d`を実行してください。

</details>

```bash
# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate
```

**✅ ディレクトリ構造の確認**

```
~/laravel-practice/
└── 9-2-5_hands-on/
    └── blade-app-practice/     ← 自分で作成する用（今ここ）
        ├── app/
        ├── resources/
        ├── routes/
        └── ...
```

> 💡 **環境構築が完了！**
>
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

---

### 📄 提供ファイル

**`resources/views/products/index.blade.php`**

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{{ $pageTitle }}</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f5f5f5; }
        .in-stock { color: green; }
        .out-of-stock { color: red; }
        .category { background-color: #e0e0e0; padding: 2px 8px; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>{{ $pageTitle }}</h1>
    <p>全{{ $products->count() }}件の商品があります。</p>

    <table>
        <thead>
            <tr>
                <th>No.</th>
                <th>商品名</th>
                <th>カテゴリ</th>
                <th>価格</th>
                <th>在庫状況</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($products as $product)
                <tr>
                    <td>{{ $loop->iteration }}</td>
                    <td>{{ $product->name }}</td>
                    <td><span class="category">{{ $product->category }}</span></td>
                    <td>¥{{ number_format($product->price) }}</td>
                    <td>
                        @if ($product->in_stock)
                            <span class="in-stock">在庫あり</span>
                        @else
                            <span class="out-of-stock">在庫なし</span>
                        @endif
                    </td>
                </tr>
            @empty
                <tr>
                    <td colspan="5">商品が登録されていません</td>
                </tr>
            @endforelse
        </tbody>
    </table>

    @isset($lastUpdated)
        <p><small>最終更新: {{ $lastUpdated }}</small></p>
    @endisset
</body>
</html>
```

---

---

> 🚀 **ここから先は、自分の力で実装してみましょう！**

---

---

## 💡 ヒント

### Bladeファイルから必要な変数を読み取る

Bladeファイル内で使われている変数を探しましょう。

```blade
{{ $pageTitle }}        ← 文字列が必要
{{ $products->count() }} ← コレクションが必要
{{ $product->name }}     ← 各商品にnameプロパティが必要
{{ $product->category }} ← 各商品にcategoryプロパティが必要
{{ $product->price }}    ← 各商品にpriceプロパティが必要
{{ $product->in_stock }} ← 各商品にin_stockプロパティが必要
@isset($lastUpdated)     ← オプション（なくてもOK）
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？Bladeファイルを読み解いて、必要なデータを渡すスキルは、実際の開発で非常に重要です。一緒に手を動かしながら、解答を確認していきましょう。

> 📌 **注意**: ここからは`blade-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### ⚙️ 環境準備（実践用プロジェクト）

まず、**自分で作成する用のプロジェクトを停止**します：

```bash
# blade-app-practiceディレクトリに移動
cd ~/laravel-practice/9-2-5_hands-on/blade-app-practice

# Sailを停止
./vendor/bin/sail down
```

次に、**実践用のプロジェクトを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/laravel-practice/9-2-5_hands-on

# Laravel 10.xプロジェクトを作成（実践用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 blade-app-sample
```

```bash
# プロジェクトディレクトリに移動
cd blade-app-sample

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql

# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate
```

**✅ ディレクトリ構造の確認**

```
~/laravel-practice/
└── 9-2-5_hands-on/
    ├── blade-app-practice/     ← 自分で作成した用（停止中）
    └── blade-app-sample/       ← 実践用（今ここ、起動中）
        ├── app/
        ├── resources/
        ├── routes/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

---

### 🧠 先輩エンジニアの思考プロセス

先輩エンジニアは要件を以下のように構造化し、実装タスクに落とし込みます：

| Step | やること | 説明 |
|:-----|:---------|:-----|
| 1 | Bladeファイルを読み解く | 変数を特定し、データ構造を推測する |
| 2 | コントローラーを作成 | Artisanコマンドで生成 |
| 3 | ルーティングを設定 | URLとコントローラーを結びつける |
| 4 | Bladeファイルを配置 | 提供されたファイルを配置 |

Bladeを読み解くポイント：
- `{{ $変数名 }}`で変数を特定
- `$products->count()`ならコレクション、`$product->name`ならオブジェクトのプロパティ
- `@if`や`@isset`で条件分岐を確認

---

### 📝 ステップバイステップで実装

#### ステップ1: Bladeファイルを読み解く

**何を考えているか**：
- 「どんな変数が使われているか確認しよう」
- 「各変数のデータ型は何か推測しよう」

Bladeファイルを読み解いた結果：

| 変数名 | データ型 | 必須/オプション |
|:---|:---|:---|
| `$pageTitle` | 文字列 | 必須 |
| `$products` | コレクション | 必須 |
| `$product->name` | 文字列 | 必須 |
| `$product->category` | 文字列 | 必須 |
| `$product->price` | 数値 | 必須 |
| `$product->in_stock` | 真偽値 | 必須 |
| `$lastUpdated` | 文字列 | オプション |

---

#### ステップ2: コントローラーを作成する

**何を考えているか**：
- 「ProductControllerを作成しよう」
- 「indexメソッドで商品一覧を返そう」
- 「今はモデルがないので、配列でダミーデータを作ろう」

```bash
sail artisan make:controller ProductController
```

`app/Http/Controllers/ProductController.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Http\Controllers;

class ProductController extends Controller
{
    public function index()
    {
        // ダミーデータを作成（本来はデータベースから取得）
        $products = collect([
            (object) [
                'name' => 'ノートパソコン',
                'category' => '電子機器',
                'price' => 89800,
                'in_stock' => true,
            ],
            (object) [
                'name' => 'ワイヤレスマウス',
                'category' => '周辺機器',
                'price' => 3980,
                'in_stock' => true,
            ],
            (object) [
                'name' => 'USBハブ',
                'category' => '周辺機器',
                'price' => 2480,
                'in_stock' => false,
            ],
        ]);

        return view('products.index', [
            'pageTitle' => '商品一覧',
            'products' => $products,
            'lastUpdated' => '2024年1月1日 12:00',
        ]);
    }
}
```

**コードリーディング**：

```php
$products = collect([...]);
```
→ `collect()`でコレクションを作成します。Bladeで`$products->count()`が使えるようになります。

```php
(object) ['name' => '...', ...]
```
→ 配列をオブジェクトに変換します。Bladeで`$product->name`のようにアクセスできます。

```php
return view('products.index', [...]);
```
→ Bladeファイルに必要な変数を全て渡します。

---

#### ステップ3: ルーティングを設定する

**何を考えているか**：
- 「/productsにアクセスしたら商品一覧を表示したい」

`routes/web.php`に以下を追加します：

```php
use App\Http\Controllers\ProductController;

Route::get('/products', [ProductController::class, 'index']);
```

---

#### ステップ4: Bladeファイルを配置する

**何を考えているか**：
- 「resources/views/products/ディレクトリを作成しよう」
- 「提供されたBladeファイルを配置しよう」

```bash
mkdir -p resources/views/products
```

提供されたBladeファイルを`resources/views/products/index.blade.php`として保存します。

---

### ✨ 完成！

ブラウザで `http://localhost/products` にアクセスして、商品一覧が表示されれば完成です！

これでBladeファイルを読み解き、コントローラーから適切なデータを渡す演習ができました。

> 💡 **エラーが出たら**: Bladeファイルの先頭に`@dd($products)`を追加して、データが渡されているか確認しましょう。確認後は削除してください。

**自分で作成したコードと比較してみましょう**：
- `blade-app-practice/`: 自分で作成したプロジェクト
- `blade-app-sample/`: 一緒に作成したプロジェクト

両方のプロジェクトを見比べて、違いがあれば確認してみてください。

---

## 📖 模範解答

### ProductController.php

```php
<?php

namespace App\Http\Controllers;

class ProductController extends Controller
{
    public function index()
    {
        $products = collect([
            (object) [
                'name' => 'ノートパソコン',
                'category' => '電子機器',
                'price' => 89800,
                'in_stock' => true,
            ],
            (object) [
                'name' => 'ワイヤレスマウス',
                'category' => '周辺機器',
                'price' => 3980,
                'in_stock' => true,
            ],
            (object) [
                'name' => 'USBハブ',
                'category' => '周辺機器',
                'price' => 2480,
                'in_stock' => false,
            ],
        ]);

        return view('products.index', [
            'pageTitle' => '商品一覧',
            'products' => $products,
            'lastUpdated' => '2024年1月1日 12:00',
        ]);
    }
}
```

### routes/web.php

```php
use App\Http\Controllers\ProductController;

Route::get('/products', [ProductController::class, 'index']);
```

### products/index.blade.php

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{{ $pageTitle }}</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f5f5f5; }
        .in-stock { color: green; }
        .out-of-stock { color: red; }
        .category { background-color: #e0e0e0; padding: 2px 8px; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>{{ $pageTitle }}</h1>
    <p>全{{ $products->count() }}件の商品があります。</p>

    <table>
        <thead>
            <tr>
                <th>No.</th>
                <th>商品名</th>
                <th>カテゴリ</th>
                <th>価格</th>
                <th>在庫状況</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($products as $product)
                <tr>
                    <td>{{ $loop->iteration }}</td>
                    <td>{{ $product->name }}</td>
                    <td><span class="category">{{ $product->category }}</span></td>
                    <td>¥{{ number_format($product->price) }}</td>
                    <td>
                        @if ($product->in_stock)
                            <span class="in-stock">在庫あり</span>
                        @else
                            <span class="out-of-stock">在庫なし</span>
                        @endif
                    </td>
                </tr>
            @empty
                <tr>
                    <td colspan="5">商品が登録されていません</td>
                </tr>
            @endforelse
        </tbody>
    </table>

    @isset($lastUpdated)
        <p><small>最終更新: {{ $lastUpdated }}</small></p>
    @endisset
</body>
</html>
```

---

## 🧪 動作確認の方法

### プロジェクトの切り替え

2つのプロジェクトを切り替えて動作確認する方法：

```bash
# blade-app-practiceで確認したい場合
cd ~/laravel-practice/9-2-5_hands-on/blade-app-sample
./vendor/bin/sail down

cd ~/laravel-practice/9-2-5_hands-on/blade-app-practice
./vendor/bin/sail up -d
# ブラウザで http://localhost/products にアクセス

# blade-app-sampleで確認したい場合
cd ~/laravel-practice/9-2-5_hands-on/blade-app-practice
./vendor/bin/sail down

cd ~/laravel-practice/9-2-5_hands-on/blade-app-sample
./vendor/bin/sail up -d
# ブラウザで http://localhost/products にアクセス
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ 提供されたBladeファイルを読み解き、必要な変数を特定できる
- ✅ コントローラーから適切なデータを渡して、画面を表示できる
- ✅ `@dd()`を使ってデバッグできる

**重要なポイント**：
- Bladeファイルを読むときは、`{{ $変数名 }}`や`$変数->プロパティ`を探す
- データ構造（文字列、コレクション、オブジェクト）を推測する
- エラーが出たら、まず`@dd()`でデータを確認する

引き続き、次のChapterも頑張りましょう！

### 🛑 Sailの停止

次のセクションに進む前に、Sailを停止しておきましょう。

```bash
./vendor/bin/sail down
```

> 💡 **なぜ停止するの？**: Sailを起動したままだと、次のセクションで別のプロジェクトを起動する際にポートが競合してエラーになることがあります。セクションの終わりには必ずSailを停止する習慣をつけましょう。

---
