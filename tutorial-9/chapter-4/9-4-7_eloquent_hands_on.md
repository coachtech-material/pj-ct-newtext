# Tutorial 9-4-7: Eloquent ORM - ハンズオン演習

## 📝 このセクションの目的

Chapter 4で学んだEloquent ORMを実際に手を動かして確認します。モデルを使って、オブジェクト指向的にデータベースを操作しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

**学習のポイント**：
- Eloquentモデルを作成できるか
- モデルを使ってCRUD操作ができるか
- リレーションシップを定義できるか

---

## 🎯 演習課題：ブログシステムのモデル作成

### 📋 要件

#### 1. Postモデルの作成

`Post`モデルとマイグレーションを同時に作成してください。

**カラム構成**：
- id, title (VARCHAR 200), content (TEXT), user_id (INTEGER), published_at (DATETIME nullable), timestamps

#### 2. CRUD操作の実装

`PostController`に以下のメソッドを実装してください：

- `index()`: すべての投稿を取得（最新順）
- `store()`: 新しい投稿を作成
- `update($id)`: 投稿を更新
- `destroy($id)`: 投稿を削除

#### 3. リレーションシップの定義

`Post`モデルに`user()`メソッドを追加し、`User`モデルとのリレーションシップを定義してください。

---

## 💡 ヒント

```bash
php artisan make:model Post -m
```

```php
// モデルでの取得
$posts = Post::all();
$post = Post::find($id);

// 作成
Post::create([
    'title' => 'タイトル',
    'content' => '本文',
]);

// 更新
$post->update(['title' => '新しいタイトル']);

// 削除
$post->delete();

// リレーションシップ
public function user()
{
    return $this->belongsTo(User::class);
}
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？Eloquent ORMはオブジェクト指向でデータベースを操作できる強力な機能です。一緒に手を動かしながら、ブログシステムのモデルを作成していきましょう。

### 💭 実装の思考プロセス

Eloquentを使った開発では、以下の順番で考えると効率的です：

1. **モデルとマイグレーションを同時作成**：一度に両方を生成
2. **マイグレーションでテーブル構造を定義**：カラムと外部キーを設定
3. **モデルで属性を設定**：$fillableとリレーションを定義
4. **コントローラーでCRUD操作を実装**：モデルを使ってデータ操作
5. **リレーションを活用**：関連データを簡単に取得

Eloquentのポイントは「モデルを中心に、オブジェクト指向でデータベースを操作する」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: モデルとマイグレーションを同時作成する

**何を考えているか**：
- 「投稿を管理するPostモデルが必要だ」
- 「`-m`オプションでマイグレーションも同時に作ろう」
- 「効率的に開発を進めよう」

ターミナルで以下のコマンドを実行します：

```bash
php artisan make:model Post -m
```

**コマンド解説**：

```bash
php artisan make:model Post -m
```
→ `Post`モデルとマイグレーションファイルを同時に生成します。`-m`オプションでマイグレーションも作成されます。

---

#### ステップ2: マイグレーションでテーブル構造を定義する

**何を考えているか**：
- 「投稿テーブルにはタイトル、本文、ユーザーID、公開日が必要だ」
- 「外部キーでUserテーブルと関連付けよう」
- 「公開日はnullableにしよう」

生成されたマイグレーションファイルを開いて、`up`メソッドを以下のように編集します：

```php
public function up(): void
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->string('title', 200);
        $table->text('content');
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->dateTime('published_at')->nullable();
        $table->timestamps();
    });
}
```

**コードリーディング**：

```php
$table->string('title', 200);
$table->text('content');
```
→ タイトルは`VARCHAR(200)`、本文は`TEXT`型で定義します。

```php
$table->foreignId('user_id')->constrained()->onDelete('cascade');
```
→ `foreignId`で外部キーを作成します。`constrained()`で`users`テーブルと関連付け、`onDelete('cascade')`でユーザー削除時に投稿も削除されるようにします。

```php
$table->dateTime('published_at')->nullable();
```
→ 公開日を`DATETIME`型で定義し、`nullable()`でNULLを許可します。下書き保存時にNULLにできます。

マイグレーションを実行します：

```bash
php artisan migrate
```

---

#### ステップ3: モデルで属性を設定する

**何を考えているか**：
- 「一括代入可能な属性を$fillableで指定しよう」
- 「日付型の属性を$castsで定義しよう」
- 「Userモデルとのリレーションを定義しよう」

`app/Models/Post.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    protected $fillable = [
        'title',
        'content',
        'user_id',
        'published_at',
    ];

    protected $casts = [
        'published_at' => 'datetime',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

**コードリーディング**：

```php
protected $fillable = [
    'title',
    'content',
    'user_id',
    'published_at',
];
```
→ `$fillable`で一括代入可能な属性を指定します。`create()`や`update()`で使用できる属性を制限し、セキュリティを向上させます。

```php
protected $casts = [
    'published_at' => 'datetime',
];
```
→ `$casts`で属性の型変換を定義します。`published_at`を`datetime`型にキャストし、Carbonインスタンスとして扱えるようにします。

```php
public function user()
{
    return $this->belongsTo(User::class);
}
```
→ `belongsTo`でUserモデルとのリレーションを定義します。「投稿は1人のユーザーに属する」という関係を表します。

---

#### ステップ4: コントローラーでCRUD操作を実装する

**何を考えているか**：
- 「全投稿を取得するindexメソッドを作ろう」
- 「新しい投稿を作成するstoreメソッドを作ろう」
- 「更新と削除のメソッドも実装しよう」

`PostController`を作成します：

```bash
php artisan make:controller PostController
```

`app/Http/Controllers/PostController.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function index()
    {
        $posts = Post::with('user')->latest()->get();
        return view('posts.index', ['posts' => $posts]);
    }

    public function store(Request $request)
    {
        Post::create([
            'title' => $request->title,
            'content' => $request->content,
            'user_id' => auth()->id(),
            'published_at' => now(),
        ]);
        return redirect('/posts');
    }

    public function update(Request $request, $id)
    {
        $post = Post::findOrFail($id);
        $post->update([
            'title' => $request->title,
            'content' => $request->content,
        ]);
        return redirect('/posts');
    }

    public function destroy($id)
    {
        Post::findOrFail($id)->delete();
        return redirect('/posts');
    }
}
```

**コードリーディング**：

```php
$posts = Post::with('user')->latest()->get();
```
→ `Post::with('user')`でユーザー情報をEager Loadingします。`latest()`で最新順に並び替え、`get()`で全データを取得します。

```php
Post::create([
    'title' => $request->title,
    'content' => $request->content,
    'user_id' => auth()->id(),
    'published_at' => now(),
]);
```
→ `Post::create()`で新しい投稿を作成します。`auth()->id()`でログイン中のユーザーIDを取得します。

```php
$post = Post::findOrFail($id);
$post->update([
    'title' => $request->title,
    'content' => $request->content,
]);
```
→ `findOrFail($id)`で投稿を取得し、見つからなければ4 04エラーを返します。`update()`でデータを更新します。

```php
Post::findOrFail($id)->delete();
```
→ 投稿を取得して、`delete()`で削除します。メソッドチェーンで簡潔に書けます。

---

### ✨ 完成！

これでEloquent ORMを使ったデータベース操作が実践できました！モデル、リレーション、CRUD操作をオブジェクト指向で実装できましたね。

---

## 📖 模範解答

### マイグレーションファイル

```php
public function up(): void
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->string('title', 200);
        $table->text('content');
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->dateTime('published_at')->nullable();
        $table->timestamps();
    });
}
```

### Post.php

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Post extends Model
{
    protected $fillable = [
        'title',
        'content',
        'user_id',
        'published_at',
    ];

    protected $casts = [
        'published_at' => 'datetime',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```

### PostController.php

```php
public function index()
{
    $posts = Post::with('user')->latest()->get();
    return view('posts.index', ['posts' => $posts]);
}

public function store(Request $request)
{
    Post::create([
        'title' => $request->title,
        'content' => $request->content,
        'user_id' => auth()->id(),
        'published_at' => now(),
    ]);
    return redirect('/posts');
}

public function update(Request $request, $id)
{
    $post = Post::findOrFail($id);
    $post->update([
        'title' => $request->title,
        'content' => $request->content,
    ]);
    return redirect('/posts');
}

public function destroy($id)
{
    Post::findOrFail($id)->delete();
    return redirect('/posts');
}
```

---

## 💪 自己評価チェックリスト

- [ ] Eloquentモデルを作成できた
- [ ] $fillableを設定できた
- [ ] モデルでCRUD操作ができた
- [ ] リレーションシップを定義できた
- [ ] with()でN+1問題を回避できた

すべてチェックできたら、Chapter 5に進みましょう！
