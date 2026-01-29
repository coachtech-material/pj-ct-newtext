# Tutorial 13-4-2: APIコントローラーの実装

## 🎯 このセクションで学ぶこと

- API専用のコントローラーを作成する
- JSONレスポンスを返す方法を学ぶ
- APIリソースで出力形式を整える

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜWeb用とAPI用でコントローラーを分けるのか？」

### 理由1: 返すものが違う

```
Web用コントローラー
→ return view('books.index', ...);  // HTMLを返す

API用コントローラー
→ return response()->json([...]);   // JSONを返す
```

### 理由2: 認証の扱いが違う

| 種類 | 認証 | 用途 |
|:---|:---|:---|
| Web用 | 必要（authミドルウェア） | ブラウザからのアクセス |
| API用 | 不要（公開） | プログラムからのアクセス |

---

### このセクションの実装順序

| 順番 | 作業 | 理由 |
|:---:|:---|:---|
| 1 | APIコントローラー作成 | JSONを返す処理を作る |
| 2 | APIルーティング設定 | /api/booksでアクセスできるように |
| 3 | Thunder Clientでテスト | APIが動くか確認 |
| 4 | APIリソースで整形 | 出力形式を統一 |

---

## Step 1: APIコントローラーの作成

### 1-1. Api/BookControllerを生成する

API用のコントローラーは、`Api`ディレクトリに作成します。

```bash
sail artisan make:controller Api/BookController
```

### 1-2. コントローラーを実装する

**ファイル**: `app/Http/Controllers/Api/BookController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\Book;

class BookController extends Controller
{
    /**
     * 書籍一覧を取得
     */
    public function index()
    {
        $books = Book::latest()->get();
        
        return response()->json([
            'data' => $books,
        ]);
    }

    /**
     * 書籍詳細を取得
     */
    public function show(Book $book)
    {
        return response()->json([
            'data' => $book,
        ]);
    }
}
```

---

### 1-3. コードリーディング

#### `namespace App\Http\Controllers\Api`の分解

| 部分 | 説明 |
|:---|:---|
| `namespace` | 名前空間の宣言 |
| `App\Http\Controllers\Api` | Apiディレクトリ内のコントローラー |

#### `response()->json([...])`の分解

| 部分 | 説明 | 戻り値 |
|:---|:---|:---|
| `response()` | レスポンスヘルパーを取得 | ResponseFactory |
| `->json([...])` | JSON形式でレスポンスを作成 | JsonResponse |

> 💡 **メソッドチェーンの流れ**: `response()` → `json()` と順番に処理が連鎖します。

---

## Step 2: APIルーティングの設定

### 2-1. api.phpにルートを追加

**ファイル**: `routes/api.php`

```php
<?php

use App\Http\Controllers\Api\BookController;
use Illuminate\Support\Facades\Route;

Route::get('/books', [BookController::class, 'index']);
Route::get('/books/{book}', [BookController::class, 'show']);
```

### 2-2. ルート一覧を確認

```bash
sail artisan route:list --path=api
```

**出力例**:

```
GET|HEAD   api/books .......... Api\BookController@index
GET|HEAD   api/books/{book} ... Api\BookController@show
```

> 💡 **ポイント**: `routes/api.php`に定義したルートは、自動的に`/api`プレフィックスが付きます。

---

## Step 3: 動作確認（Thunder Client）

### 3-1. Thunder Clientを開く

VSCodeでThunder Clientを開きます。

### 3-2. 書籍一覧APIをテスト

1. 「New Request」をクリック
2. メソッド: `GET`
3. URL: `http://localhost/api/books`
4. 「Send」をクリック

**レスポンス例**:

```json
{
  "data": [
    {
      "id": 1,
      "title": "リーダブルコード",
      "author": "Dustin Boswell",
      "rating": 5,
      "review": "読みやすいコードを書くための必読書です。",
      "created_at": "2024-01-01T00:00:00.000000Z",
      "updated_at": "2024-01-01T00:00:00.000000Z"
    }
  ]
}
```

### 3-3. 書籍詳細APIをテスト

1. URL: `http://localhost/api/books/1`
2. 「Send」をクリック

---

## Step 4: APIリソースで出力形式を整える

### 4-1. BookResourceを生成する

```bash
sail artisan make:resource BookResource
```

### 4-2. BookResourceを編集する

**ファイル**: `app/Http/Resources/BookResource.php`

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class BookResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     */
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'author' => $this->author,
            'rating' => $this->rating,
            'review' => $this->review,
            'created_at' => $this->created_at->format('Y-m-d H:i:s'),
        ];
    }
}
```

### 4-3. コントローラーでBookResourceを使用する

**ファイル**: `app/Http/Controllers/Api/BookController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\BookResource;
use App\Models\Book;

class BookController extends Controller
{
    /**
     * 書籍一覧を取得
     */
    public function index()
    {
        $books = Book::latest()->get();
        
        return BookResource::collection($books);
    }

    /**
     * 書籍詳細を取得
     */
    public function show(Book $book)
    {
        return new BookResource($book);
    }
}
```

### 4-4. 再度Thunder Clientで確認

レスポンスの形式が整えられていることを確認します。

```json
{
  "data": [
    {
      "id": 1,
      "title": "リーダブルコード",
      "author": "Dustin Boswell",
      "rating": 5,
      "review": "読みやすいコードを書くための必読書です。",
      "created_at": "2024-01-01 00:00:00"
    }
  ]
}
```

> 💡 **ポイント**: `created_at`の形式が`Y-m-d H:i:s`に整えられています。

---

## Step 5: コミット、PR、マージ

### 5-1. コミット

```bash
git add .
git commit -m "feat: 公開APIの実装 (Closes #8)"
```

### 5-2. プッシュ、PR、マージ

```bash
git push origin feature/issue-8-public-api
```

GitHubでPRを作成し、セルフレビュー後にマージします。

### 5-3. ローカルの更新

```bash
git checkout main
git pull origin main
git branch -d feature/issue-8-public-api
```

---

## ✨ まとめ

このセクションでは、APIコントローラーの実装について学びました。

| Step | 学んだこと |
|:---|:---|
| Step 1 | Api/BookControllerの作成 |
| Step 2 | routes/api.phpでのルーティング |
| Step 3 | Thunder Clientでの動作確認 |
| Step 4 | BookResourceで出力形式を整える |
| Step 5 | コミット、PR、マージ |

次のChapterでは、認証機能を実装します。

---
