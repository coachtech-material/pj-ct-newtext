# Tutorial 9-2-5: Bladeテンプレート - ハンズオン演習

## 📝 このセクションの目的

Chapter 2で学んだBladeテンプレートを実際に手を動かして確認します。**提供されたBladeファイルを読み解き、コントローラーから適切なデータを渡して画面を表示させる**演習を行います。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 🎯 演習課題：提供されたBladeファイルを動かそう

### 📋 シナリオ

あなたは、フロントエンドエンジニアから以下のBladeファイルを受け取りました。このファイルを読み解き、コントローラーから適切なデータを渡して、画面を正しく表示させてください。

### 📁 提供されるBladeファイル

以下の内容で`resources/views/products/index.blade.php`を作成してください。

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

### 📝 課題

1. 上記のBladeファイルを読み解き、**必要な変数**を特定してください。
2. `ProductController`を作成し、適切なデータを渡してください。
3. ルーティングを設定し、ブラウザで表示を確認してください。

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

### 💭 実装の思考プロセス

Bladeファイルを読み解く際は、以下の順番で考えると効率的です：

1. **変数を特定**：`{{ $変数名 }}`を探す
2. **データ構造を推測**：`$products->count()`ならコレクション、`$product->name`ならオブジェクトのプロパティ
3. **条件分岐を確認**：`@if`や`@isset`で何がチェックされているか
4. **コントローラーでデータを準備**：特定した変数を全て渡す
5. **デバッグで確認**：`@dd()`で渡されているか確認

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

#### ステップ5: ブラウザで確認する

**何を考えているか**：
- 「ブラウザでアクセスして、正しく表示されるか確認しよう」
- 「エラーが出たら、@dd()でデバッグしよう」

ブラウザで`http://localhost/products`にアクセスします。

**期待される表示**：

```
商品一覧
全3件の商品があります。

┌────┬──────────────────┬──────────┬──────────┬──────────┐
│No. │商品名            │カテゴリ  │価格      │在庫状況  │
├────┼──────────────────┼──────────┼──────────┼──────────┤
│ 1  │ノートパソコン    │電子機器  │¥89,800  │在庫あり  │
│ 2  │ワイヤレスマウス  │周辺機器  │¥3,980   │在庫あり  │
│ 3  │USBハブ          │周辺機器  │¥2,480   │在庫なし  │
└────┴──────────────────┴──────────┴──────────┴──────────┘

最終更新: 2024年1月1日 12:00
```

---

#### ステップ6: デバッグの練習

**何を考えているか**：
- 「もしエラーが出たら、どうデバッグするか練習しよう」

Bladeファイルの先頭に`@dd()`を追加して、データが渡されているか確認します：

```blade
@dd($products)

<h1>{{ $pageTitle }}</h1>
...
```

これで、`$products`の中身が表示されます。確認後は`@dd()`を削除してください。

---

### ✨ 完成！

これでBladeファイルを読み解き、コントローラーから適切なデータを渡す演習ができました！

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

---
