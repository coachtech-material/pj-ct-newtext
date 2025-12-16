# Tutorial 9-4-3: ページネーションの実装

## 🎯 このセクションで学ぶこと

*   ページネーションの概念と必要性を理解する。
*   Laravelのページネーション機能を使って、大量のデータを分割表示できるようになる。
*   `paginate()`メソッドと`simplePaginate()`メソッドの違いを理解する。

---

## 導入：大量のデータを扱う際の課題

前のセクションで、Eloquentを使ってデータを取得する方法を学びました。しかし、実際のアプリケーションでは、データベースに数千、数万件のレコードが保存されることがあります。

**例えば、以下のような状況を考えてみましょう**：

*   ブログサイトに1,000件の記事がある
*   ECサイトに10,000件の商品がある
*   SNSに100,000件の投稿がある

これらのデータを**すべて一度に表示**すると、以下の問題が発生します：

1. **ページの読み込みが遅くなる**：大量のHTMLを生成・転送するため
2. **メモリ不足**：サーバーのメモリを大量に消費する
3. **ユーザー体験の低下**：スクロールが長すぎて、目的のデータを見つけにくい

この問題を解決するのが**ページネーション**です。

---

## 詳細解説

### 📄 ページネーションとは

**ページネーション**（Pagination）とは、大量のデータを**複数のページに分割して表示**する機能です。

**身近な例**：
Googleの検索結果を思い浮かべてください。検索結果は、1ページに10件ずつ表示され、「次へ」ボタンで次のページに移動できます。これがページネーションです。

```
[1] [2] [3] [4] [5] ... [次へ]
```

---

### 🔧 Laravelのページネーション機能

Laravelは、ページネーション機能を**標準で提供**しています。`paginate()`メソッドを使うだけで、簡単にページネーションを実装できます。

#### 基本的な使い方

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;

class PostController extends Controller
{
    public function index()
    {
        // 1ページに15件ずつ表示
        $posts = Post::paginate(15);
        
        return view('posts.index', ['posts' => $posts]);
    }
}
```

**コードリーディング**：

*   `Post::paginate(15)`：1ページに15件ずつ表示するページネーションを生成
*   Laravelが自動的に、現在のページ番号（`?page=2`など）を取得し、適切なデータを取得します

---

### 🎨 ビューでページネーションリンクを表示

コントローラーで`paginate()`を使うと、ビューで**ページネーションリンク**を簡単に表示できます。

#### resources/views/posts/index.blade.php

```blade
<!DOCTYPE html>
<html>
<head>
    <title>投稿一覧</title>
</head>
<body>
    <h1>投稿一覧</h1>
    
    <ul>
        @foreach ($posts as $post)
            <li>{{ $post->title }}</li>
        @endforeach
    </ul>
    
    <!-- ページネーションリンク -->
    {{ $posts->links() }}
</body>
</html>
```

**コードリーディング**：

*   `{{ $posts->links() }}`：ページネーションリンクを自動生成
*   Laravelが、現在のページ、前後のページ、最初・最後のページへのリンクを生成します

**生成されるHTML**：

```html
<nav>
    <ul class="pagination">
        <li class="page-item disabled"><span class="page-link">« 前へ</span></li>
        <li class="page-item active"><span class="page-link">1</span></li>
        <li class="page-item"><a class="page-link" href="?page=2">2</a></li>
        <li class="page-item"><a class="page-link" href="?page=3">3</a></li>
        <li class="page-item"><a class="page-link" href="?page=2">次へ »</a></li>
    </ul>
</nav>
```

---

### 🔍 検索条件と組み合わせる

ページネーションは、`where()`などの検索条件と組み合わせて使えます。

```php
public function index(Request $request)
{
    $query = Post::query();
    
    // 検索条件がある場合
    if ($request->has('keyword')) {
        $query->where('title', 'like', '%' . $request->keyword . '%');
    }
    
    // ページネーション
    $posts = $query->paginate(15);
    
    return view('posts.index', ['posts' => $posts]);
}
```

**重要なポイント**：

*   検索条件を適用した後に`paginate()`を呼び出す
*   Laravelが自動的に、検索条件を保持したままページネーションリンクを生成します

---

### ⚡ simplePaginate()との違い

Laravelには、`paginate()`の他に`simplePaginate()`というメソッドもあります。

| メソッド | 特徴 | 表示 |
|---------|------|------|
| **paginate()** | 総ページ数を表示 | `[1] [2] [3] [4] [5]` |
| **simplePaginate()** | 「前へ」「次へ」のみ表示 | `[前へ] [次へ]` |

#### simplePaginate()の使い方

```php
$posts = Post::simplePaginate(15);
```

**メリット**：

*   **パフォーマンスが良い**：総件数を数える必要がないため、大量のデータでも高速
*   **シンプル**：ページ番号が不要な場合に適している

**デメリット**：

*   **総ページ数がわからない**：ユーザーが「あと何ページあるか」を把握できない

---

### 🎨 ページネーションのカスタマイズ

#### 1ページあたりの件数を変更

```php
$posts = Post::paginate(20); // 20件ずつ表示
```

#### 特定のページを取得

```php
$posts = Post::paginate(15, ['*'], 'page', 2); // 2ページ目を取得
```

#### ページネーションのスタイルを変更

Laravelは、デフォルトで**Bootstrap**のスタイルを使います。**Tailwind CSS**に変更することもできます。

**config/app.php**

```php
'pagination' => 'tailwind',
```

または、ビューで指定：

```blade
{{ $posts->links('pagination::tailwind') }}
```

---

### 📊 ページネーション情報の取得

ページネーションオブジェクトから、様々な情報を取得できます。

```php
$posts = Post::paginate(15);

$posts->total();        // 総件数
$posts->perPage();      // 1ページあたりの件数
$posts->currentPage();  // 現在のページ番号
$posts->lastPage();     // 最終ページ番号
$posts->hasMorePages(); // 次のページがあるか
```

#### ビューで使う例

```blade
<p>全{{ $posts->total() }}件中、{{ $posts->firstItem() }}〜{{ $posts->lastItem() }}件を表示</p>

{{ $posts->links() }}
```

**表示例**：

```
全150件中、16〜30件を表示
[1] [2] [3] [4] [5] ... [10]
```

---

### 🔗 URLクエリパラメータの保持

検索フォームと組み合わせる場合、検索条件をURLに保持する必要があります。

```blade
{{ $posts->appends(['keyword' => request('keyword')])->links() }}
```

**生成されるURL**：

```
?keyword=Laravel&page=2
```

**コードリーディング**：

*   `appends(['keyword' => request('keyword')])`：URLクエリパラメータを追加
*   ページネーションリンクをクリックしても、検索条件が保持されます

---

### 💡 実践例：ブログの記事一覧

#### コントローラー

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function index(Request $request)
    {
        $query = Post::query();
        
        // カテゴリーで絞り込み
        if ($request->has('category')) {
            $query->where('category', $request->category);
        }
        
        // キーワード検索
        if ($request->has('keyword')) {
            $query->where('title', 'like', '%' . $request->keyword . '%');
        }
        
        // 新しい順に並べ替え
        $query->orderBy('created_at', 'desc');
        
        // ページネーション（1ページに20件）
        $posts = $query->paginate(20);
        
        return view('posts.index', ['posts' => $posts]);
    }
}
```

#### ビュー

```blade
<!DOCTYPE html>
<html>
<head>
    <title>投稿一覧</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>投稿一覧</h1>
        
        <!-- 検索フォーム -->
        <form method="GET" action="/posts" class="mb-4">
            <div class="row">
                <div class="col-md-4">
                    <input type="text" name="keyword" class="form-control" placeholder="キーワード検索" value="{{ request('keyword') }}">
                </div>
                <div class="col-md-2">
                    <button type="submit" class="btn btn-primary">検索</button>
                </div>
            </div>
        </form>
        
        <!-- 件数表示 -->
        <p>全{{ $posts->total() }}件中、{{ $posts->firstItem() }}〜{{ $posts->lastItem() }}件を表示</p>
        
        <!-- 記事一覧 -->
        <div class="list-group mb-4">
            @foreach ($posts as $post)
                <a href="/posts/{{ $post->id }}" class="list-group-item list-group-item-action">
                    <h5>{{ $post->title }}</h5>
                    <small>{{ $post->created_at->format('Y年m月d日') }}</small>
                </a>
            @endforeach
        </div>
        
        <!-- ページネーションリンク -->
        {{ $posts->appends(request()->query())->links() }}
    </div>
</body>
</html>
```

**コードリーディング**：

*   `request()->query()`：現在のURLクエリパラメータを全て取得
*   `appends(request()->query())`：検索条件を保持したままページネーション

---

## 💡 TIP

### パフォーマンスの最適化

大量のデータをページネーションする場合、以下の点に注意しましょう。

#### 1. インデックスを追加

```php
// マイグレーション
$table->string('category')->index();
$table->timestamp('created_at')->index();
```

検索条件やソート条件に使うカラムには、インデックスを追加することで、クエリが高速化されます。

#### 2. 必要なカラムのみ取得

```php
$posts = Post::select(['id', 'title', 'created_at'])->paginate(20);
```

不要なカラムを取得しないことで、メモリ使用量を削減できます。

#### 3. Eager Loadingを使う

```php
$posts = Post::with('author')->paginate(20);
```

N+1問題を回避するために、関連データは事前に読み込みます。

---

### ページネーションのデザイン

Laravelのページネーションは、Bootstrapのスタイルをデフォルトで使います。独自のデザインにカスタマイズすることもできます。

#### ページネーションビューを公開

```bash
php artisan vendor:publish --tag=laravel-pagination
```

`resources/views/vendor/pagination/`に、ページネーションビューが生成されます。これを編集することで、デザインをカスタマイズできます。

---

## ✨ まとめ

*   **ページネーション**は、大量のデータを複数のページに分割して表示する機能
*   Laravelの`paginate()`メソッドを使うと、簡単にページネーションを実装できる
*   `simplePaginate()`は、「前へ」「次へ」のみを表示するシンプルなページネーション
*   検索条件と組み合わせる場合は、`appends()`でURLクエリパラメータを保持する
*   パフォーマンス最適化のために、インデックスの追加やEager Loadingを活用する

---

## 📝 学習のポイント

- [ ] ページネーションの概念と必要性を理解している
- [ ] `paginate()`メソッドを使って、ページネーションを実装できる
- [ ] `paginate()`と`simplePaginate()`の違いを説明できる
- [ ] ビューで`links()`を使って、ページネーションリンクを表示できる
- [ ] 検索条件を保持したままページネーションを実装できる
- [ ] ページネーション情報（総件数、現在のページなど）を取得できる
