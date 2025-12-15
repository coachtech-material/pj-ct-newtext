# Tutorial 9-3-7: データベース操作 - ハンズオン演習

## 📝 このセクションの目的

Chapter 3で学んだLaravelのデータベース操作を実際に手を動かして確認します。マイグレーション、シーダー、クエリビルダを使って、データベースを操作しましょう。

**学習のポイント**：
- マイグレーションファイルを作成できるか
- シーダーでテストデータを投入できるか
- クエリビルダでデータを取得・挿入・更新・削除できるか

---

## 🎯 演習課題：商品管理システムのデータベース構築

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

## 💡 ヒント

```bash
php artisan make:migration create_products_table
php artisan make:seeder ProductSeeder
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
php artisan make:migration create_products_table
```

**コマンド解説**：

```bash
php artisan make:migration create_products_table
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
php artisan migrate
```

**コマンド解説**：

```bash
php artisan migrate
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
php artisan make:seeder ProductSeeder
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
php artisan db:seed --class=ProductSeeder
```

---

#### ステップ4: クエリビルダでデータを取得する

**何を考えているか**：
- 「全商品を取得して表示したい」
- 「クエリビルダで簡単に取得できる」
- 「コントローラーでデータを取得してビューに渡そう」

`ProductController`を作成します：

```bash
php artisan make:controller ProductController
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

---

## 📖 模範解答

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

## 💪 自己評価チェックリスト

- [ ] マイグレーションを作成・実行できた
- [ ] シーダーを作成・実行できた
- [ ] クエリビルダでCRUD操作ができた

すべてチェックできたら、Chapter 4に進みましょう！
