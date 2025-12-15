# Tutorial 9-4-7: Eloquent ORM - ハンズオン演習

## 📝 このセクションの目的

Chapter 4で学んだEloquent ORMを実際に手を動かして確認します。モデルを使って、オブジェクト指向的にデータベースを操作しましょう。

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
