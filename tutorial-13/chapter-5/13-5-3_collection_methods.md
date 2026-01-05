# Tutorial 13-5-3: コレクションメソッド

## 🎯 このセクションで学ぶこと

- Laravelコレクションの便利なメソッドを学ぶ
- foreachをコレクションメソッドで置き換える
- メソッドチェーンでデータを加工する

---

## Step 1: コレクションとは

### 1-1. コレクションの取得

Eloquentでデータを取得すると、**Collection**オブジェクトが返されます。

```php
$books = Book::all();  // Illuminate\Database\Eloquent\Collection

$books = Book::where('rating', '>=', 4)->get();  // Collection
```

### 1-2. 配列との違い

| 配列 | コレクション |
|:---|:---|
| PHPの組み込み機能 | Laravelのクラス |
| `array_map`, `array_filter`など | `map`, `filter`などのメソッド |
| メソッドチェーン不可 | メソッドチェーン可能 |

---

## Step 2: よく使うコレクションメソッド

### 2-1. map（各要素を変換）

```php
// 書籍タイトルの一覧を取得
$titles = $books->map(function ($book) {
    return $book->title;
});

// アロー関数で短く書く
$titles = $books->map(fn($book) => $book->title);

// pluckでさらに短く
$titles = $books->pluck('title');
```

### 2-2. filter（条件で絞り込み）

```php
// 評価4以上の書籍のみ
$highRatedBooks = $books->filter(function ($book) {
    return $book->rating >= 4;
});

// アロー関数で短く
$highRatedBooks = $books->filter(fn($book) => $book->rating >= 4);
```

### 2-3. sortBy / sortByDesc（並び替え）

```php
// 評価の高い順
$sortedBooks = $books->sortByDesc('rating');

// タイトルのアルファベット順
$sortedBooks = $books->sortBy('title');
```

### 2-4. groupBy（グループ化）

```php
// カテゴリごとにグループ化
$groupedBooks = $books->groupBy('category_id');

// カテゴリ名でグループ化
$groupedBooks = $books->groupBy(fn($book) => $book->category->name);
```

### 2-5. sum / avg / count（集計）

```php
// 評価の合計
$totalRating = $books->sum('rating');

// 評価の平均
$averageRating = $books->avg('rating');

// 書籍数
$bookCount = $books->count();
```

---

## Step 3: メソッドチェーン

### 3-1. 複数のメソッドを連結

```php
// 評価4以上の書籍を、評価の高い順に並べ、タイトルのみ取得
$titles = $books
    ->filter(fn($book) => $book->rating >= 4)
    ->sortByDesc('rating')
    ->pluck('title');
```

### 3-2. foreachとの比較

**Before（foreach）**:

```php
$highRatedTitles = [];
foreach ($books as $book) {
    if ($book->rating >= 4) {
        $highRatedTitles[] = $book->title;
    }
}
usort($highRatedTitles, fn($a, $b) => $b <=> $a);
```

**After（コレクションメソッド）**:

```php
$highRatedTitles = $books
    ->filter(fn($book) => $book->rating >= 4)
    ->sortByDesc('rating')
    ->pluck('title');
```

---

## Step 4: 実践例

### 4-1. カテゴリ別の書籍数を表示

```php
// コントローラー
public function index()
{
    $books = auth()->user()->books()->with('category')->get();
    
    // カテゴリ別の書籍数
    $categoryStats = $books
        ->groupBy(fn($book) => $book->category?->name ?? '未分類')
        ->map(fn($books) => $books->count());
    
    return view('books.index', compact('books', 'categoryStats'));
}
```

```blade
{{-- ビュー --}}
<h3>カテゴリ別書籍数</h3>
<ul>
    @foreach ($categoryStats as $category => $count)
        <li>{{ $category }}: {{ $count }}冊</li>
    @endforeach
</ul>
```

### 4-2. 評価の平均を計算

```php
$averageRating = $books->avg('rating');
$roundedAverage = round($averageRating, 1);  // 小数点1桁
```

---

## ✨ まとめ

このセクションでは、コレクションメソッドについて学びました。

| メソッド | 用途 |
|:---|:---|
| `map` | 各要素を変換 |
| `filter` | 条件で絞り込み |
| `sortBy` / `sortByDesc` | 並び替え |
| `groupBy` | グループ化 |
| `sum` / `avg` / `count` | 集計 |
| `pluck` | 特定のカラムのみ取得 |

コレクションメソッドを使うことで、foreachよりも簡潔で読みやすいコードが書けます。

---
