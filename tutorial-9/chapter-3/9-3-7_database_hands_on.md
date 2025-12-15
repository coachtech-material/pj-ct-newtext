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
