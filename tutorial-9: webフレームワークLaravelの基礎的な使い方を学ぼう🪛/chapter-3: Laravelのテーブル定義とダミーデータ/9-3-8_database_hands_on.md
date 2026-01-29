# Tutorial 9-3-8: データベース操作 ハンズオン演習

## 📝 このセクションの目的

Chapter 3で学んだLaravelのデータベース操作を実際に手を動かして確認します。マイグレーション、シーダー、クエリビルダを使って、データベースを操作しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

**学習のポイント**：
- マイグレーションファイルを作成できるか
- シーダーでテストデータを投入できるか
- クエリビルダでデータを取得・挿入・更新・削除できるか

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのプロジェクトを作成します。

```
~/laravel-practice/
├── 9-3-8_hands-on/                       ← このハンズオン用のディレクトリ
│   ├── database-app-practice/            ← 要件を見て自分で作成するプロジェクト
│   │   ├── app/
│   │   ├── database/
│   │   ├── routes/
│   │   └── ...
│   └── database-app-sample/              ← 実践で一緒に作成するプロジェクト
│       ├── app/
│       ├── database/
│       ├── routes/
│       └── ...
└── ...
```

| ディレクトリ | 用途 | URL |
|:---|:---|:---|
| `database-app-practice/` | 📋 要件を見て、自分の力で作成する | `http://localhost/products` |
| `database-app-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する | `http://localhost/products` |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

> ⚠️ **注意**: 2つのプロジェクトを同時に起動することはできません（ポートが競合するため）。一方のプロジェクトで作業する際は、もう一方を停止してください。

---

## 🎯 演習課題：商品管理システムのデータベース構築

### 🖼️ 完成イメージ

<!-- Tinkerでのデータ確認のスクリーンショットをここに配置 -->
![9-3-8 完成イメージ](images/9-3-8_database_complete.png)

**この演習で作るもの**：
マイグレーションでテーブルを作成し、シーダーでテストデータを投入し、クエリビルダでデータを操作する「商品管理システム」のデータベースを構築します。

---

### 📋 要件

#### 1. マイグレーションの作成

`products`テーブルを作成するマイグレーションを作成してください。

**カラム構成**：
- id, name (VARCHAR 200), price (INTEGER), stock (INTEGER, default 0), category (VARCHAR 50), timestamps

#### 2. シーダーの作成

5件の商品データを挿入するシーダーを作成してください。

#### 3. クエリビルダの実装

`ProductController`に全件取得、1件取得、挿入、更新、削除のメソッドを実装してください。

---

### ✅ 完成品の確認方法

**🔧 Tinkerでの確認（推奨）**

この演習ではデータベース操作が主なため、Tinkerで確認します。

```bash
./vendor/bin/sail artisan tinker
```

**確認コマンド**:
```php
// テーブルが存在するか確認
Schema::hasTable('products');

// シーダーのデータが入っているか確認
DB::table('products')->count();

// 全件取得
DB::table('products')->get();
```

**正しく実装できていれば**:
- [ ] `products`テーブルが存在する（`true`が返る）
- [ ] 5件の商品データが存在する（`5`が返る）
- [ ] 商品データが正しく取得できる

**🌐 ブラウザでの確認（代替方法）**

- **動作確認URL**: `http://localhost/products`
- **確認手順**:
  1. Sailを起動する（`./vendor/bin/sail up -d`）
  2. ブラウザで `http://localhost/products` にアクセス
  3. 商品一覧が表示されることを確認

> 📌 **Bladeファイルについて**: バックエンド実装に集中するため、動作確認用のシンプルなBladeファイルを以下に用意しています。

<details>
<summary>📄 確認用Bladeファイル（クリックで展開）</summary>

`resources/views/products/index.blade.php`:

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>商品一覧</title>
</head>
<body>
    <h1>商品一覧</h1>
    <table border="1">
        <tr><th>ID</th><th>商品名</th><th>価格</th><th>在庫</th><th>カテゴリ</th></tr>
        @foreach ($products as $product)
            <tr>
                <td>{{ $product->id }}</td>
                <td>{{ $product->name }}</td>
                <td>¥{{ number_format($product->price) }}</td>
                <td>{{ $product->stock }}</td>
                <td>{{ $product->category }}</td>
            </tr>
        @endforeach
    </table>
</body>
</html>
```

</details>

---

### 📁 Step 0: 環境を準備する（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

> **📌 前のハンズオンのプロジェクトを停止**
> 
> 前のハンズオン（9-2-5）のプロジェクトが起動している場合は、先に停止してください。
> ```bash
> cd ~/laravel-practice/9-2-5_hands-on/blade-app-sample
> ./vendor/bin/sail down
> ```

```bash
# laravel-practiceディレクトリに移動
cd ~/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 9-3-8_hands-on
cd 9-3-8_hands-on

# Laravel 10.xプロジェクトを作成（自分で作成する用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 database-app-practice
```

```bash
# プロジェクトディレクトリに移動
cd database-app-practice

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
└── 9-3-8_hands-on/
    └── database-app-practice/     ← 自分で作成する用（今ここ）
        ├── app/
        ├── database/
        ├── routes/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

> 💡 **ポイント**: このハンズオンでは、シーダーを作成してデータを投入します。実践セクションの「ステップ3」でシーダーの作成方法を学びます。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

```bash
sail artisan make:migration create_products_table
sail artisan make:seeder ProductSeeder
```

```php
Schema::create('products', function (Blueprint $table) {
    $table->id();
    $table->string('name', 200);
    $table->integer('price');
    $table->integer('stock')->default(0);
    $table->string('category', 50);
    $table->timestamps();
});
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？Laravelのデータベース操作はマイグレーション、シーダー、クエリビルダの3本柱です。一緒に手を動かしながら、商品管理システムのデータベースを構築していきましょう。

> 📌 **注意**: ここからは`database-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### 💻 環境準備（実践用プロジェクト）

まず、**自分で作成する用のプロジェクトを停止**します：

```bash
# database-app-practiceディレクトリに移動
cd ~/laravel-practice/9-3-8_hands-on/database-app-practice

# Sailを停止
./vendor/bin/sail down
```

次に、**実践用のプロジェクトを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/laravel-practice/9-3-8_hands-on

# Laravel 10.xプロジェクトを作成（実践用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 database-app-sample
```

```bash
# プロジェクトディレクトリに移動
cd database-app-sample

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
└── 9-3-8_hands-on/
    ├── database-app-practice/     ← 自分で作成した用（停止中）
    └── database-app-sample/       ← 実践用（今ここ、起動中）
        ├── app/
        ├── database/
        ├── routes/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

---

### 💭 実装の思考プロセス

データベースを構築する際、以下の順番で考えると効率的です：

1. **マイグレーションでテーブルを定義**：テーブル構造をコードで管理
2. **マイグレーションを実行**：テーブルを作成
3. **シーダーでテストデータを投入**：開発用データを準備
4. **クエリビルダでデータ操作**：取得、挿入、更新、削除を実装
5. **コントローラーでロジックを統合**：データ操作をアプリに組み込む

Laravelのデータベース操作のポイントは「マイグレーションでテーブル構造をバージョン管理し、クエリビルダで安全にデータを操作する」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: マイグレーションを作成する

**何を考えているか**：
- 「商品テーブルを作成するマイグレーションが必要だ」
- 「Artisanコマンドでマイグレーションファイルを生成しよう」
- 「カラム構成を定義しよう」

ターミナルで以下のコマンドを実行します：

```bash
sail artisan make:migration create_products_table
```

**コマンド解説**：

```bash
sail artisan make:migration create_products_table
```
→ `create_products_table`という名前のマイグレーションファイルを生成します。`database/migrations/`ディレクトリにファイルが作成されます。

生成されたマイグレーションファイルを開いて、`up`メソッドを以下のように編集します：

```php
public function up(): void
{
    Schema::create('products', function (Blueprint $table) {
        $table->id();
        $table->string('name', 200);
        $table->integer('price');
        $table->integer('stock')->default(0);
        $table->string('category', 50);
        $table->timestamps();
    });
}
```

**コードリーディング**：

```php
Schema::create('products', function (Blueprint $table) {
```
→ `Schema::create`で`products`テーブルを作成します。`Blueprint $table`はテーブル定義のためのオブジェクトです。

```php
$table->id();
```
→ 主キー`id`を自動採番で作成します。`BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY`に相当します。

```php
$table->string('name', 200);
$table->integer('price');
$table->integer('stock')->default(0);
$table->string('category', 50);
```
→ 各カラムを定義します。`string`は`VARCHAR`、`integer`は`INT`に相当します。`default(0)`でデフォルト値を設定します。

```php
$table->timestamps();
```
→ `created_at`と`updated_at`カラムを自動的に追加します。Laravelが自動的にタイムスタンプを管理します。

---

#### ステップ2: マイグレーションを実行する

**何を考えているか**：
- 「マイグレーションを実行してテーブルを作成しよう」
- 「`php artisan migrate`で実行できる」

ターミナルで以下のコマンドを実行します：

```bash
sail artisan migrate
```

**コマンド解説**：

```bash
sail artisan migrate
```
→ 未実行のマイグレーションをすべて実行して、テーブルを作成します。`products`テーブルがデータベースに作成されます。

---

#### ステップ3: シーダーを作成する

**何を考えているか**：
- 「テストデータを投入するシーダーを作ろう」
- 「5件の商品データを準備しよう」
- 「DBファサードでデータを挿入しよう」

ターミナルで以下のコマンドを実行します：

```bash
sail artisan make:seeder ProductSeeder
```

`database/seeders/ProductSeeder.php`を開いて、`run`メソッドを以下のように編集します：

```php
public function run(): void
{
    DB::table('products')->insert([
        ['name' => 'ノートPC', 'price' => 120000, 'stock' => 10, 'category' => '電子機器', 'created_at' => now(), 'updated_at' => now()],
        ['name' => 'マウス', 'price' => 2000, 'stock' => 50, 'category' => '電子機器', 'created_at' => now(), 'updated_at' => now()],
        ['name' => 'キーボード', 'price' => 5000, 'stock' => 30, 'category' => '電子機器', 'created_at' => now(), 'updated_at' => now()],
        ['name' => 'デスク', 'price' => 25000, 'stock' => 5, 'category' => '家具', 'created_at' => now(), 'updated_at' => now()],
        ['name' => 'チェア', 'price' => 15000, 'stock' => 8, 'category' => '家具', 'created_at' => now(), 'updated_at' => now()],
    ]);
}
```

**コードリーディング**：

```php
DB::table('products')->insert([
```
→ `DB`ファサードで`products`テーブルにデータを挿入します。`insert`メソッドは配列を受け取ります。

```php
['name' => 'ノートPC', 'price' => 120000, 'stock' => 10, 'category' => '電子機器', 'created_at' => now(), 'updated_at' => now()],
```
→ 各商品のデータを連想配列で定義します。`now()`で現在のタイムスタンプを取得します。
シーダーを実行します：

```bash
sail artisan db:seed --class=ProductSeeder
```

**データが投入されたか確認しましょう**：

```bash
sail artisan tinker
```

```php
>>> use Illuminate\Support\Facades\DB;
>>> DB::table('products')->get();
```

5件の商品データが表示されれば成功です。`exit`でtinkerを終了します。

---

#### ステップ4: クエリビルダーでデータを取得する

**何を考えているか**：
- 「全商品を取得して表示したい」
- 「クエリビルダで簡単に取得できる」
- 「コントローラーでデータを取得してビューに渡そう」

`ProductController`を作成します：

```bash
sail artisan make:controller ProductController
```

`app/Http/Controllers/ProductController.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class ProductController extends Controller
{
    public function index()
    {
        $products = DB::table('products')->get();
        return view('products.index', ['products' => $products]);
    }
}
```

**コードリーディング**：

```php
use Illuminate\Support\Facades\DB;
```
→ `DB`ファサードをインポートします。クエリビルダを使用するために必要です。

```php
$products = DB::table('products')->get();
```
→ `DB::table('products')`で`products`テーブルにアクセスし、`get()`で全データを取得します。結果はコレクションとして返されます。

```php
return view('products.index', ['products' => $products]);
```
→ 取得したデータをビューに渡します。

---

#### ステップ5: クエリビルダでデータを挿入する

**何を考えているか**：
- 「新しい商品を登録したい」
- 「`insert`メソッドでデータを挿入しよう」
- 「リクエストからデータを取得しよう」

`ProductController`に`store`メソッドを追加します：

```php
public function store(Request $request)
{
    DB::table('products')->insert([
        'name' => $request->name,
        'price' => $request->price,
        'stock' => $request->stock,
        'category' => $request->category,
        'created_at' => now(),
        'updated_at' => now(),
    ]);
    return redirect('/products');
}
```

**コードリーディング**：

```php
public function store(Request $request)
```
→ `Request $request`でリクエストデータを受け取ります。

```php
DB::table('products')->insert([
    'name' => $request->name,
    'price' => $request->price,
    'stock' => $request->stock,
    'category' => $request->category,
    'created_at' => now(),
    'updated_at' => now(),
]);
```
→ `insert`メソッドでデータを挿入します。`$request->name`でリクエストからデータを取得します。

```php
return redirect('/products');
```
→ 挿入後、商品一覧ページにリダイレクトします。

---

### ✨ 完成！

これでLaravelのデータベース操作が実践できました！マイグレーション、シーダー、クエリビルダを使って、データベースを構築・操作できましたね。

**自分で作成したコードと比較してみましょう**：
- `database-app-practice/`: 自分で作成したプロジェクト
- `database-app-sample/`: 一緒に作成したプロジェクト

両方のプロジェクトを見比べて、違いがあれば確認してみてください。

---

## 📖 模範解答

> 💡 模範解答ではCSSでスタイリングしていますが、この演習ではCSSの実装は不要です。機能の実装に集中してください。

### マイグレーションファイル

```php
public function up(): void
{
    Schema::create('products', function (Blueprint $table) {
        $table->id();
        $table->string('name', 200);
        $table->integer('price');
        $table->integer('stock')->default(0);
        $table->string('category', 50);
        $table->timestamps();
    });
}
```

### ProductSeeder.php

```php
public function run(): void
{
    DB::table('products')->insert([
        ['name' => 'ノートPC', 'price' => 120000, 'stock' => 10, 'category' => '電子機器', 'created_at' => now(), 'updated_at' => now()],
        ['name' => 'マウス', 'price' => 2000, 'stock' => 50, 'category' => '電子機器', 'created_at' => now(), 'updated_at' => now()],
        ['name' => 'キーボード', 'price' => 5000, 'stock' => 30, 'category' => '電子機器', 'created_at' => now(), 'updated_at' => now()],
        ['name' => 'デスク', 'price' => 25000, 'stock' => 5, 'category' => '家具', 'created_at' => now(), 'updated_at' => now()],
        ['name' => 'チェア', 'price' => 15000, 'stock' => 8, 'category' => '家具', 'created_at' => now(), 'updated_at' => now()],
    ]);
}
```

### ProductController.php

```php
public function index()
{
    $products = DB::table('products')->get();
    return view('products.index', ['products' => $products]);
}

public function store(Request $request)
{
    DB::table('products')->insert([
        'name' => $request->name,
        'price' => $request->price,
        'stock' => $request->stock,
        'category' => $request->category,
        'created_at' => now(),
        'updated_at' => now(),
    ]);
    return redirect('/products');
}
```

---

## 🧪 動作確認の方法

### プロジェクトの切り替え

2つのプロジェクトを切り替えて動作確認する方法：

```bash
# database-app-practiceで確認したい場合
cd ~/laravel-practice/9-3-8_hands-on/database-app-sample
./vendor/bin/sail down

cd ~/laravel-practice/9-3-8_hands-on/database-app-practice
./vendor/bin/sail up -d
# マイグレーションとシーダーを実行
./vendor/bin/sail artisan migrate
./vendor/bin/sail artisan db:seed --class=ProductSeeder

# database-app-sampleで確認したい場合
cd ~/laravel-practice/9-3-8_hands-on/database-app-practice
./vendor/bin/sail down

cd ~/laravel-practice/9-3-8_hands-on/database-app-sample
./vendor/bin/sail up -d
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ マイグレーションファイルを作成できる
- ✅ シーダーでテストデータを投入できる
- ✅ クエリビルダでデータを取得・挿入・更新・削除できる

引き続き、次のセクションも頑張りましょう！

### 🛑 Sailの停止

次のセクションに進む前に、Sailを停止しておきましょう。

```bash
./vendor/bin/sail down
```

> 💡 **なぜ停止するの？**: Sailを起動したままだと、次のセクションで別のプロジェクトを起動する際にポートが競合してエラーになることがあります。セクションの終わりには必ずSailを停止する習慣をつけましょう。

---
