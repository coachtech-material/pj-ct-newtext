# Tutorial 9-4-9: Eloquent ORM - ハンズオン演習

## 📝 このセクションの目的

Chapter 4で学んだEloquent ORMを実際に手を動かして確認します。モデルを使って、オブジェクト指向的にデータベースを操作しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

**学習のポイント**：
- Eloquentモデルを作成できるか
- モデルを使ってCRUD操作ができるか
- リレーションシップを定義できるか

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのプロジェクトを作成します。

```
~/laravel-practice/
├── 9-4-9_hands-on/                       ← このハンズオン用のディレクトリ
│   ├── eloquent-app-practice/            ← 要件を見て自分で作成するプロジェクト
│   │   ├── app/
│   │   ├── database/
│   │   ├── routes/
│   │   └── ...
│   └── eloquent-app-sample/              ← 実践で一緒に作成するプロジェクト
│       ├── app/
│       ├── database/
│       ├── routes/
│       └── ...
└── ...
```

| ディレクトリ | 用途 | URL |
|:---|:---|:---|
| `eloquent-app-practice/` | 📋 要件を見て、自分の力で作成する | `http://localhost/posts` |
| `eloquent-app-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する | `http://localhost/posts` |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

> ⚠️ **注意**: 2つのプロジェクトを同時に起動することはできません（ポートが競合するため）。一方のプロジェクトで作業する際は、もう一方を停止してください。

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

### 📁 Step 0: 環境を準備する（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

> **📌 前のハンズオンのプロジェクトを停止**
> 
> 前のハンズオン（9-3-8）のプロジェクトが起動している場合は、先に停止してください。
> ```bash
> cd ~/laravel-practice/9-3-8_hands-on/database-app-sample
> ./vendor/bin/sail down
> ```

```bash
# laravel-practiceディレクトリに移動
cd ~/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 9-4-9_hands-on
cd 9-4-9_hands-on

# Laravel 10.xプロジェクトを作成（自分で作成する用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 eloquent-app-practice
```

```bash
# プロジェクトディレクトリに移動
cd eloquent-app-practice

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql

# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate

# データベースのマイグレーション
./vendor/bin/sail artisan migrate
```

**📦 テストユーザーの作成**

投稿を作成するにはユーザーが必要です。`tinker`を使ってテストユーザーを作成します：

```bash
# tinkerを起動
sail artisan tinker
```

```php
# tinker内で実行
App\Models\User::create([
    'name' => 'テストユーザー',
    'email' => 'test@example.com',
    'password' => bcrypt('password'),
]);

# 作成されたユーザーを確認
App\Models\User::first();

# tinkerを終了
exit
```

> 💡 **ポイント**: このユーザーのIDは`1`になります。後で投稿を作成する際に`user_id = 1`として使用します。

**✅ ディレクトリ構造の確認**

```
~/laravel-practice/
└── 9-4-9_hands-on/
    └── eloquent-app-practice/     ← 自分で作成する用（今ここ）
        ├── app/
        ├── database/
        ├── routes/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

```bash
sail artisan make:model Post -m
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

> 📌 **注意**: ここからは`eloquent-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### 💻 環境準備（実践用プロジェクト）

まず、**自分で作成する用のプロジェクトを停止**します：

```bash
# eloquent-app-practiceディレクトリに移動
cd ~/laravel-practice/9-4-9_hands-on/eloquent-app-practice

# Sailを停止
./vendor/bin/sail down
```

次に、**実践用のプロジェクトを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/laravel-practice/9-4-9_hands-on

# Laravel 10.xプロジェクトを作成（実践用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 eloquent-app-sample
```

```bash
# プロジェクトディレクトリに移動
cd eloquent-app-sample

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql

# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate

# データベースのマイグレーション
./vendor/bin/sail artisan migrate
```

**📦 テストユーザーの作成**

投稿を作成するにはユーザーが必要です。`tinker`を使ってテストユーザーを作成します：

```bash
# tinkerを起動
sail artisan tinker
```

```php
# tinker内で実行
App\Models\User::create([
    'name' => 'テストユーザー',
    'email' => 'test@example.com',
    'password' => bcrypt('password'),
]);

# 作成されたユーザーを確認
App\Models\User::first();

# tinkerを終了
exit
```

> 💡 **ポイント**: このユーザーのIDは`1`になります。後で投稿を作成する際に`user_id = 1`として使用します。

**✅ ディレクトリ構造の確認**

```
~/laravel-practice/
└── 9-4-9_hands-on/
    ├── eloquent-app-practice/     ← 自分で作成した用（停止中）
    └── eloquent-app-sample/       ← 実践用（今ここ、起動中）
        ├── app/
        ├── database/
        ├── routes/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

---

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
sail artisan make:model Post -m
```

**コマンド解説**：

```bash
sail artisan make:model Post -m
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
sail artisan migrate
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
sail artisan make:controller PostController
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
            'user_id' => 1,
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
    'user_id' => 1,
    'published_at' => now(),
]);
```
→ `Post::create()`で新しい投稿を作成します。`user_id`は固定値`1`を使用しています（認証機能は別途学習します）。

```php
$post = Post::findOrFail($id);
$post->update([
    'title' => $request->title,
    'content' => $request->content,
]);
```
→ `findOrFail($id)`で投稿を取得し、見つからなければ404エラーを返します。`update()`でデータを更新します。

```php
Post::findOrFail($id)->delete();
```
→ 投稿を取得して、`delete()`で削除します。メソッドチェーンで簡潔に書けます。

---

### ✨ 完成！

これでEloquent ORMを使ったデータベース操作が実践できました！モデル、リレーション、CRUD操作をオブジェクト指向で実装できましたね。

**自分で作成したコードと比較してみましょう**：
- `eloquent-app-practice/`: 自分で作成したプロジェクト
- `eloquent-app-sample/`: 一緒に作成したプロジェクト

両方のプロジェクトを見比べて、違いがあれば確認してみてください。

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
        'user_id' => 1,
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

## 🧪 動作確認の方法

### プロジェクトの切り替え

2つのプロジェクトを切り替えて動作確認する方法：

```bash
# eloquent-app-practiceで確認したい場合
cd ~/laravel-practice/9-4-9_hands-on/eloquent-app-sample
./vendor/bin/sail down

cd ~/laravel-practice/9-4-9_hands-on/eloquent-app-practice
./vendor/bin/sail up -d

# eloquent-app-sampleで確認したい場合
cd ~/laravel-practice/9-4-9_hands-on/eloquent-app-practice
./vendor/bin/sail down

cd ~/laravel-practice/9-4-9_hands-on/eloquent-app-sample
./vendor/bin/sail up -d
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ Eloquentモデルを作成できる
- ✅ モデルを使ってCRUD操作ができる
- ✅ リレーションシップを定義できる

引き続き、次のセクションも頑張りましょう！

---
