# Tutorial 13-5-2: 命名規則

## 🎯 このセクションで学ぶこと

- 変数・メソッド・クラスの命名規則を学ぶ
- 意図が伝わる名前の付け方を理解する
- Laravelの命名規則に従う重要性を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜDRYの次に命名規則なのか？」

DRY原則で重複を排除したら、次は**命名規則**を見直します。

### 理由1: コードは「読まれる」もの

```
コードを書く時間 ＜ コードを読む時間
```

自分が書いたコードも、1週間後には「他人のコード」のように感じます。

### 理由2: 命名は「コメント」の代わり

良い命名は、コメントがなくても意図が伝わります。

---

## Step 1: なぜ命名が重要なのか

### 1-1. 悪い命名の例

```php
// ❌ 何を表しているかわからない
$d = Book::find(1);
$x = $d->title;

// ❌ 省略しすぎ
$bk = Book::find(1);
$cat = Category::find(1);
```

### 1-2. 良い命名の例

```php
// ✅ 意図が明確
$book = Book::find(1);
$bookTitle = $book->title;

// ✅ 省略せず完全な単語を使用
$category = Category::find(1);
```

---

## Step 2: Laravelの命名規則

### 2-1. モデル

| 規則 | 例 |
|:---|:---|
| 単数形 | `Book`, `Category`, `User` |
| PascalCase | `BookReview`, `UserProfile` |

### 2-2. テーブル

| 規則 | 例 |
|:---|:---|
| 複数形 | `books`, `categories`, `users` |
| snake_case | `book_reviews`, `user_profiles` |

### 2-3. コントローラー

| 規則 | 例 |
|:---|:---|
| 単数形 + Controller | `BookController`, `CategoryController` |
| リソースコントローラーのメソッド | `index`, `create`, `store`, `show`, `edit`, `update`, `destroy` |

### 2-4. 変数・メソッド

| 規則 | 例 |
|:---|:---|
| camelCase | `$bookTitle`, `$categoryName` |
| 動詞で始める（メソッド） | `getBooks()`, `createBook()`, `updateRating()` |

---

## Step 3: 具体的な命名のコツ

### 3-1. コレクションは複数形

```php
// ❌ 単数形
$book = Book::all();

// ✅ 複数形
$books = Book::all();
```

### 3-2. 真偽値はis/has/canで始める

```php
// ❌ 曖昧
$published = true;
$admin = false;

// ✅ 明確
$isPublished = true;
$isAdmin = false;
$hasReview = true;
$canEdit = true;
```

### 3-3. メソッドは動詞で始める

```php
// ❌ 名詞のみ
public function books() { ... }
public function rating() { ... }

// ✅ 動詞で始める（取得系）
public function getBooks() { ... }
public function calculateAverageRating() { ... }

// ✅ リレーションメソッドは例外（名詞でOK）
public function books() { return $this->hasMany(Book::class); }
```

---

## Step 4: 実践例

### 4-1. Before（悪い命名）

```php
public function idx()
{
    $d = auth()->user()->books;
    return view('books.index', ['d' => $d]);
}

public function str(Request $r)
{
    $v = $r->validate([...]);
    auth()->user()->books()->create($v);
    return redirect()->route('books.index');
}
```

### 4-2. After（良い命名）

```php
public function index()
{
    $books = auth()->user()->books()->with('category')->latest()->get();
    return view('books.index', compact('books'));
}

public function store(StoreBookRequest $request)
{
    auth()->user()->books()->create($request->validated());
    return redirect()->route('books.index')->with('success', '書籍を登録しました。');
}
```

---

## ✨ まとめ

このセクションでは、命名規則について学びました。

| 対象 | 規則 | 例 |
|:---|:---|:---|
| モデル | 単数形・PascalCase | `Book`, `Category` |
| テーブル | 複数形・snake_case | `books`, `categories` |
| 変数 | camelCase | `$bookTitle` |
| コレクション | 複数形 | `$books` |
| 真偽値 | is/has/can | `$isPublished` |
| メソッド | 動詞で始める | `getBooks()` |

良い命名は、コードの可読性を大幅に向上させます。

---
