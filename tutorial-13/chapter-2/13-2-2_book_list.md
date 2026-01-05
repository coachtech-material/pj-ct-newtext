# Tutorial 13-2-2: 書籍一覧画面の実装

## 🎯 このセクションで学ぶこと

- 書籍一覧画面のルーティングとコントローラーを実装する
- Bladeテンプレートにデータを渡す方法を学ぶ
- イシュー駆動開発のフローを継続する

---

## Step 0: 現在のブランチを確認

前のセクションで作成したブランチで作業を続けます。

```bash
git branch
```

`feature/issue-1-book-list`にいることを確認します。

---

## Step 1: コントローラーの作成

### 1-1. BookControllerを生成する

```bash
sail artisan make:controller BookController --resource
```

`--resource`オプションを付けると、CRUD操作に必要なメソッドが自動生成されます。

### 1-2. indexメソッドを実装する

**ファイル**: `app/Http/Controllers/BookController.php`

```php
<?php

namespace App\Http\Controllers;

use App\Models\Book;
use Illuminate\Http\Request;

class BookController extends Controller
{
    /**
     * 書籍一覧を表示
     */
    public function index()
    {
        $books = Book::latest()->get();
        
        return view('books.index', compact('books'));
    }

    // 他のメソッドは後で実装します
    public function create() {}
    public function store(Request $request) {}
    public function show(Book $book) {}
    public function edit(Book $book) {}
    public function update(Request $request, Book $book) {}
    public function destroy(Book $book) {}
}
```

---

### 1-3. コードリーディング

| コード | 説明 |
|:---|:---|
| `Book::latest()` | 最新順（created_at降順）で取得 |
| `->get()` | 結果をコレクションとして取得 |
| `view('books.index', ...)` | `resources/views/books/index.blade.php`を表示 |
| `compact('books')` | `['books' => $books]`と同じ |

---

## Step 2: ルーティングの設定

### 2-1. web.phpにルートを追加

**ファイル**: `routes/web.php`

```php
<?php

use App\Http\Controllers\BookController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return redirect()->route('books.index');
});

Route::resource('books', BookController::class);
```

### 2-2. ルート一覧を確認

```bash
sail artisan route:list
```

**出力例**:

```
GET|HEAD   books .............. books.index › BookController@index
GET|HEAD   books/create ....... books.create › BookController@create
POST       books .............. books.store › BookController@store
GET|HEAD   books/{book} ....... books.show › BookController@show
GET|HEAD   books/{book}/edit .. books.edit › BookController@edit
PUT|PATCH  books/{book} ....... books.update › BookController@update
DELETE     books/{book} ....... books.destroy › BookController@destroy
```

> 💡 **ポイント**: `Route::resource()`を使うと、CRUD操作に必要な7つのルートが自動生成されます。

---

## Step 3: 動作確認

### 3-1. Vite開発サーバーを起動

Tailwind CSSを適用するため、別のターミナルでViteを起動します。

```bash
sail npm run dev
```

> 🚨 **注意**: このコマンドは開発中、常に実行したままにしてください。

### 3-2. ブラウザで確認

`http://localhost/books`にアクセスします。

書籍一覧画面が表示されれば成功です。Tinkerで作成したテストデータが表示されているはずです。

### 3-3. Tailwindが適用されない場合

スタイルが適用されていない場合は、以下を確認してください。

1. `sail npm run dev`が実行されているか
2. `resources/views/layouts/app.blade.php`に`@vite`ディレクティブがあるか

```blade
@vite(['resources/css/app.css', 'resources/js/app.js'])
```

---

## Step 4: コミット

### 4-1. 変更をコミット

```bash
git add .
git commit -m "feat: 書籍一覧画面の実装"
```

---

## Step 5: プルリクエストとマージ

### 5-1. プッシュ

```bash
git push origin feature/issue-1-book-list
```

### 5-2. GitHubでプルリクエストを作成

1. GitHubでリポジトリを開く
2. 「Compare & pull request」をクリック
3. タイトルを入力: `feat: 書籍一覧機能の実装 (Closes #1)`
4. 説明を入力（実装内容の概要）
5. 「Create pull request」をクリック

### 5-3. セルフレビュー

PRのDiffを確認し、以下をチェックします。

- [ ] デバッグコード（`dd()`など）が残っていないか
- [ ] インデントは正しいか
- [ ] 不要なコメントが残っていないか

### 5-4. マージ

1. 「Merge pull request」をクリック
2. 「Confirm merge」をクリック
3. Issue #1が自動的にClosedになることを確認

### 5-5. ローカルの更新

```bash
git checkout main
git pull origin main
git branch -d feature/issue-1-book-list
```

---

## 🚨 よくある間違い

### 間違い1: ルートが見つからない

**エラー例**:

```
404 | NOT FOUND
```

**対処法**: `routes/web.php`にルートが正しく設定されているか確認します。

---

### 間違い2: ビューが見つからない

**エラー例**:

```
View [books.index] not found.
```

**対処法**: `resources/views/books/index.blade.php`が存在するか確認します。

---

### 間違い3: Tailwindが適用されない

**対処法**: `sail npm run dev`が実行されているか確認します。

---

## ✨ まとめ

このセクションでは、書籍一覧画面の実装について学びました。

| Step | 学んだこと |
|:---|:---|
| Step 1 | BookControllerの作成とindexメソッドの実装 |
| Step 2 | Route::resource()によるルーティング設定 |
| Step 3 | ブラウザでの動作確認 |
| Step 4-5 | コミット、PR作成、セルフレビュー、マージ |

次のセクションでは、書籍登録機能を実装します。

---
