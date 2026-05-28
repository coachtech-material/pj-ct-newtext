# 9-4-9: Eloquent ORM - ハンズオン演習

## 📌 このハンズオンについて

Chapter 4で学んだEloquent ORMを実際に手を動かして確認します。モデルを使って、オブジェクト指向的にデータベースを操作しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

> 💡 **このハンズオンのポイント**: Eloquentモデルを作成し、CRUD操作を実装することで、オブジェクト指向的なデータベース操作を理解することが目的です。

---

### ディレクトリ構成

このハンズオンでは、「自分で作成する用」と「解答を確認する用」の2つのプロジェクトを作成します。

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

**この演習で作るもの**：
Eloquentモデルを使って「ブログシステム」の投稿一覧機能を作成します。

### 🖼️ 完成イメージ

<details>
<summary>📸 完成画面を確認する（クリックで展開）</summary>

**投稿一覧ページ**

<img alt="9-4-9_1.png" src="https://s3.ap-northeast-1.amazonaws.com/coachtech-lms-bucket-dev/curriculums/images/9-4-9_1.png">

**投稿作成ページ**

<img alt="9-4-9_2.png" src="https://s3.ap-northeast-1.amazonaws.com/coachtech-lms-bucket-dev/curriculums/images/9-4-9_2.png">

**投稿編集ページ**

<img alt="9-4-9_3.png" src="https://s3.ap-northeast-1.amazonaws.com/coachtech-lms-bucket-dev/curriculums/images/9-4-9_3.png">

</details>

---

### 📋 要件

- 投稿の一覧が表示できる
- 新しい投稿を作成できる
- 投稿を編集できる
- 投稿を削除できる
- 公開日時が表示できる

**postsテーブルのカラム構成**：

| カラム名 | 型 | 備考 |
|:---------|:---|:-----|
| id | BIGINT | 主キー、自動採番 |
| title | VARCHAR(200) | タイトル |
| content | TEXT | 本文 |
| published_at | DATETIME | 公開日時（nullable） |
| created_at | TIMESTAMP | 作成日時 |
| updated_at | TIMESTAMP | 更新日時 |

---

### 📦 GitHubでのコード管理

完成した成果物を **GitHubのpublicリポジトリ** で管理します。

- `~/laravel-practice/9-4-9_hands-on/eloquent-app-practice/` ディレクトリの中身（Laravelプロジェクト一式）を **publicリポジトリ** で管理する
- リポジトリ名は **`eloquent-app-practice`** とする
- 下記の雛形をもとに、`README.md` を **自分の言葉で** 作成する
- コミットとpushを完了させる

> 💡 **`practice/` と `sample/` の使い分け**:
> - **`eloquent-app-practice/`** が **「提出物」** です。最終的にここにある成果物をGitHubに push します
> - **`eloquent-app-sample/`** は **「答え合わせ用」** で、ローカルでの比較確認のみに使います。GitHubには push しません

<details>
<summary>📄 README.md の雛形（クリックで展開）</summary>

`eloquent-app-practice/README.md` に、以下の雛形をベースに **自分の言葉で** 記載しましょう（Laravelデフォルトの README を置き換えてOK）。

````markdown
# eloquent-app-practice

## 概要
COACHTECH 教材 Tutorial 9-4「Eloquent ORM ハンズオン演習」で作成した成果物です。
（**ここに、何を作ったかを1〜2行で書きましょう**）

## 使用技術
- PHP 8.x
- Laravel 10.x
- Eloquent ORM
- MySQL
（**他に使ったものがあれば追記してください**）

## 学んだこと
- （**自分の言葉で2〜3項目書きましょう**）
- 
- 

## 動作確認
（**どうやって動かして確認するかを記載してください**）
````

> 💡 **「学んだこと」の書き方の例（参考）**:
> - Eloquent モデルを使ったCRUD操作（`Model::all()`, `create()`, `update()`, `delete()`）
> - `$fillable` を使ったマスアサインメント対策の必要性
> - リソースコントローラ（`index`/`create`/`store`/`edit`/`update`/`destroy`）の役割

任意で以下も追加すると、より評価されやすくなります:
- 詰まったポイントと解決方法
- 開発の工夫
- 動作確認のスクショ

</details>

---

### ✅ 完成チェックリスト

- [ ] `/posts`にアクセスすると投稿一覧が表示される
- [ ] 「新規作成」から投稿を追加できる
- [ ] 「編集」から投稿を更新できる
- [ ] 「削除」で投稿が削除される

> 💡 **動作確認**: `http://localhost/posts` にアクセス

---

### ✏️ 実装タスク

1. Postモデルとマイグレーションを同時作成する
2. マイグレーションでテーブル構造を定義・実行する
3. モデルで属性を設定する
4. コントローラーを作成し、CRUD操作を実装する
5. ルーティングを設定する（個別ルート定義）
6. Bladeファイルを配置する

> 💡 Bladeファイルは「⚙️ 環境準備」セクションで提供します。

---

## ⚙️ 環境準備（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

> **📌 Dockerが起動していることを確認**
>
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

> **📌 前のハンズオンのプロジェクトを停止**
>
> 前のハンズオン（9-3-9）のプロジェクトが起動している場合は、先に停止してください。
> ```bash
> cd ~/laravel-practice/9-3-9_hands-on/database-app-sample
> ./vendor/bin/sail down
> ```

```bash
# laravel-practiceディレクトリに移動
cd ~/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 9-4-9_hands-on
cd 9-4-9_hands-on
```

```bash
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
```

<details>
<summary>⚠️ M1/M2/M3 Mac（Apple Silicon）をお使いの方</summary>

Apple Silicon搭載のMacでは、`sail up -d`実行時に以下のエラーが発生することがあります：

```
no matching manifest for linux/arm64/v8
```

**解決方法**: `compose.yaml`を開き、mysqlサービスに`platform: 'linux/amd64'`を追加してください。

```yaml
mysql:
    image: 'mysql/mysql-server:8.0'
    platform: 'linux/amd64'  # ← この行を追加
    ports:
        ...
```

編集後、保存してから`sail up -d`を実行してください。

</details>

```bash
# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate

# データベースをリセットしてマイグレーション実行
./vendor/bin/sail artisan migrate:fresh
```

> 💡 `migrate:fresh`を使うことで、前のハンズオンのデータをクリアして新しい状態から始められます。

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

> 💡 **テスト投稿の作成について**: 実際に投稿データを作成するのは、Postモデルとマイグレーションを作成した後です。「💡 ヒント」セクションのTinkerコマンドを参考にしてください。

---

### 📄 提供ファイル

**`resources/views/posts/index.blade.php`**（投稿一覧）

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>投稿一覧</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; max-width: 800px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f5f5f5; }
        h1 { color: #333; }
        .btn { display: inline-block; padding: 5px 10px; margin: 2px; text-decoration: none; border: 1px solid #333; border-radius: 3px; }
        .btn-primary { background-color: #007bff; color: white; border-color: #007bff; }
        .btn-danger { background-color: #dc3545; color: white; border-color: #dc3545; }
    </style>
</head>
<body>
    <h1>投稿一覧</h1>
    <p><a href="/posts/create" class="btn btn-primary">新規作成</a></p>
    <p>全{{ count($posts) }}件の投稿があります。</p>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>タイトル</th>
                <th>公開日時</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            @foreach ($posts as $post)
                <tr>
                    <td>{{ $post->id }}</td>
                    <td>{{ $post->title }}</td>
                    <td>{{ $post->published_at?->format('Y/m/d H:i') ?? '下書き' }}</td>
                    <td>
                        <a href="/posts/{{ $post->id }}/edit" class="btn">編集</a>
                        <form action="/posts/{{ $post->id }}" method="POST" style="display:inline;">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-danger">削除</button>
                        </form>
                    </td>
                </tr>
            @endforeach
        </tbody>
    </table>
</body>
</html>
```

**create.blade.php**（投稿作成）

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>投稿作成</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        h1 { color: #333; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input, textarea { width: 100%; max-width: 400px; padding: 8px; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>投稿作成</h1>
    <form action="/posts" method="POST">
        @csrf
        <div class="form-group">
            <label>タイトル</label>
            <input type="text" name="title" required>
        </div>
        <div class="form-group">
            <label>内容</label>
            <textarea name="content" rows="5"></textarea>
        </div>
        <button type="submit">作成</button>
    </form>
    <p><a href="/posts">← 一覧に戻る</a></p>
</body>
</html>
```

**edit.blade.php**（投稿編集）

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>投稿編集</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        h1 { color: #333; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input, textarea { width: 100%; max-width: 400px; padding: 8px; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>投稿編集</h1>
    <form action="/posts/{{ $post->id }}" method="POST">
        @csrf
        @method('PUT')
        <div class="form-group">
            <label>タイトル</label>
            <input type="text" name="title" value="{{ $post->title }}" required>
        </div>
        <div class="form-group">
            <label>内容</label>
            <textarea name="content" rows="5">{{ $post->content }}</textarea>
        </div>
        <button type="submit">更新</button>
    </form>
    <p><a href="/posts">← 一覧に戻る</a></p>
</body>
</html>
```

---

---

> 🚀 **ここから先は、自分の力で実装してみましょう！**

---

---

## 💡 ヒント

```bash
sail artisan make:model Post -m
sail artisan make:controller PostController
```

```php
// モデルでの取得
$posts = Post::all();
$post = Post::find($id);

// 作成
Post::create([
    'title' => 'タイトル',
    'content' => '本文',
    'published_at' => now(),
]);

// 更新
$post->update(['title' => '新しいタイトル']);

// 削除
$post->delete();
```

**テストデータ作成（Tinker）**

```bash
sail artisan tinker
```

```php
# Postモデルとマイグレーション作成後に実行
use App\Models\Post;

Post::create([
    'title' => 'はじめての投稿',
    'content' => 'これはテスト投稿です。',
    'published_at' => now(),
]);

Post::create([
    'title' => '2つ目の投稿',
    'content' => 'Eloquentで作成しました。',
    'published_at' => now(),
]);
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？Eloquent ORMはオブジェクト指向でデータベースを操作できる強力な機能です。一緒に手を動かしながら、ブログシステムのモデルを作成していきましょう。

> 📌 **注意**: ここからは`eloquent-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### ⚙️ 環境準備（実践用プロジェクト）

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

# データベースをリセットしてマイグレーション実行
./vendor/bin/sail artisan migrate:fresh
```

> 💡 `migrate:fresh`を使うことで、前のハンズオンのデータをクリアして新しい状態から始められます。

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

### 🧠 先輩エンジニアの思考プロセス

先輩エンジニアは要件を以下のように構造化し、実装タスクに落とし込みます：

| Step | やること | 説明 |
|:-----|:---------|:-----|
| 1 | モデルとマイグレーションを同時作成 | `-m`オプションで一度に両方を生成 |
| 2 | マイグレーションでテーブル構造を定義・実行 | 必要なカラムを設定 |
| 3 | モデルで属性を設定 | $fillableと$castsを定義 |
| 4 | コントローラーでCRUD操作を実装 | index, create, store, edit, update, delete |
| 5 | ルーティングを設定 | 個別ルートでURLとメソッドを結びつける |
| 6 | Bladeファイルを配置 | 一覧・作成・編集画面を作成 |

Eloquentのポイントは「モデルを中心に、オブジェクト指向でデータベースを操作する」ことです。Chapter 4で学んだ`create()`, `update()`, `delete()`を実際に使ってみましょう。

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

#### ステップ2: マイグレーションでテーブル構造を定義・実行する

**何を考えているか**：
- 「投稿テーブルにはタイトル、本文、公開日が必要だ」
- 「公開日はnullableにしよう」

生成されたマイグレーションファイルを開いて、`up`メソッドを以下のように編集します：

```php
public function up(): void
{
    Schema::create('posts', function (Blueprint $table) {
        $table->id();
        $table->string('title', 200);
        $table->text('content');
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
        'published_at',
    ];

    protected $casts = [
        'published_at' => 'datetime',
    ];
}
```

**コードリーディング**：

```php
protected $fillable = [
    'title',
    'content',
    'published_at',
];
```
→ `$fillable`で一括代入可能な属性を指定します。`create()`や`update()`で使用できる属性を制限し、セキュリティを向上させます。

```php
protected $casts = [
    'published_at' => 'datetime',
];
```
→ `$casts`で属性の型変換を定義します。`published_at`を`datetime`型にキャストし、Carbonインスタンスとして扱えるようにします。Carbonインスタンスにすることで、日付のフォーマット変換（`->format('Y/m/d')`）や日付の比較・計算が簡単にできるようになります。

---

#### ステップ4: コントローラーでCRUD操作を実装する

**何を考えているか**：
- 「Chapter 4で学んだcreate(), update(), delete()を使おう」
- 「一覧表示、作成フォーム、編集フォームを表示するメソッドが必要だ」
- 「データ操作のメソッド（store, update, delete）も実装しよう」

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
        $posts = Post::latest()->get();
        return view('posts.index', ['posts' => $posts]);
    }

    public function create()
    {
        return view('posts.create');
    }

    public function store(Request $request)
    {
        Post::create([
            'title' => $request->title,
            'content' => $request->content,
            'published_at' => now(),
        ]);
        return redirect('/posts');
    }

    public function edit($id)
    {
        $post = Post::findOrFail($id);
        return view('posts.edit', ['post' => $post]);
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

    public function delete($id)
    {
        Post::findOrFail($id)->delete();
        return redirect('/posts');
    }
}
```

**コードリーディング**：

```php
$posts = Post::latest()->get();
```
→ `Post::latest()`で最新順に並び替え、`get()`で全データを取得します。

```php
public function create()
{
    return view('posts.create');
}
```
→ 作成フォームを表示します。フォームからPOSTで`store`メソッドにデータが送信されます。

```php
Post::create([
    'title' => $request->title,
    'content' => $request->content,
    'published_at' => now(),
]);
```
→ Chapter 4-5で学んだ`create()`で新しい投稿を作成します。`now()`で現在日時を公開日に設定します。

```php
public function edit($id)
{
    $post = Post::findOrFail($id);
    return view('posts.edit', ['post' => $post]);
}
```
→ 編集フォームを表示します。既存のデータをフォームに表示するために`$post`を渡します。

```php
$post = Post::findOrFail($id);
$post->update([
    'title' => $request->title,
    'content' => $request->content,
]);
```
→ Chapter 4-6で学んだ`update()`でデータを更新します。`findOrFail($id)`は見つからなければ404エラーを返します。

```php
Post::findOrFail($id)->delete();
```
→ Chapter 4-6で学んだ`delete()`で削除します。メソッドチェーンで簡潔に書けます。

---

#### ステップ5: ルーティングを設定する

**何を考えているか**：
- 「CRUD操作に必要なルートを定義しよう」
- 「GETで画面表示、POSTで作成、PUTで更新、DELETEで削除」

`routes/web.php`を開いて、以下のルートを追加します：

```php
use App\Http\Controllers\PostController;

Route::get('/posts', [PostController::class, 'index']);
Route::get('/posts/create', [PostController::class, 'create']);
Route::post('/posts', [PostController::class, 'store']);
Route::get('/posts/{id}/edit', [PostController::class, 'edit']);
Route::put('/posts/{id}', [PostController::class, 'update']);
Route::delete('/posts/{id}', [PostController::class, 'delete']);
```

**コードリーディング**：

```php
Route::get('/posts', [PostController::class, 'index']);
Route::get('/posts/create', [PostController::class, 'create']);
```
→ GETリクエストで画面を表示します。`/posts`で一覧、`/posts/create`で作成フォームを表示します。

```php
Route::post('/posts', [PostController::class, 'store']);
```
→ POSTリクエストでデータを作成します。作成フォームから送信されたデータを`store`メソッドで処理します。

```php
Route::get('/posts/{id}/edit', [PostController::class, 'edit']);
Route::put('/posts/{id}', [PostController::class, 'update']);
```
→ `{id}`はURLパラメータです。`/posts/1/edit`でID=1の投稿の編集フォームを表示し、PUTリクエストで更新します。

```php
Route::delete('/posts/{id}', [PostController::class, 'delete']);
```
→ DELETEリクエストで削除します。HTMLフォームからは`@method('DELETE')`で送信します。

> 💡 **ポイント**: `Route::resource()`を使えば、これらのルートを1行で定義できます。ここでは個別に定義して、各ルートの役割を理解しましょう。

---

#### ステップ6: Bladeファイルを配置する

**何を考えているか**：
- 「一覧、作成フォーム、編集フォームの3画面が必要だ」
- 「環境準備で提供されているBladeファイルを配置しよう」

`resources/views/posts/`ディレクトリを作成し、3つのBladeファイルを配置します：

```bash
mkdir -p resources/views/posts
```

「⚙️ 環境準備」セクションで提供されているBladeファイルを`resources/views/posts/`に配置します：
- `index.blade.php` - 投稿一覧
- `create.blade.php` - 投稿作成フォーム
- `edit.blade.php` - 投稿編集フォーム

**コードリーディング**：

```blade
<form action="/posts" method="POST">
    @csrf
    ...
</form>
```
→ `@csrf`はCSRFトークンを生成します。Laravelのセキュリティ機能で、フォーム送信時に必須です。

```blade
<form action="/posts/{{ $post->id }}" method="POST">
    @csrf
    @method('PUT')
    ...
</form>
```
→ HTMLフォームはGET/POSTしかサポートしないため、`@method('PUT')`でPUTリクエストを擬似的に送信します。

---

### ✨ 完成！

まず、テストデータを作成します：

```bash
sail artisan tinker
```

```php
use App\Models\Post;

Post::create([
    'title' => 'はじめての投稿',
    'content' => 'これはテスト投稿です。',
    'published_at' => now(),
]);

Post::create([
    'title' => '2つ目の投稿',
    'content' => 'Eloquentで作成しました。',
    'published_at' => now(),
]);

exit
```

ブラウザで `http://localhost/posts` にアクセスして、以下を確認しましょう：
- 投稿一覧が表示される
- 「新規作成」から投稿を追加できる
- 「編集」から投稿を更新できる
- 「削除」で投稿が削除される

これでEloquent ORMを使ったCRUD操作が実践できました！Chapter 4で学んだ`create()`, `update()`, `delete()`をコントローラーで活用できましたね。

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
        'published_at',
    ];

    protected $casts = [
        'published_at' => 'datetime',
    ];
}
```

### PostController.php

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function index()
    {
        $posts = Post::latest()->get();
        return view('posts.index', ['posts' => $posts]);
    }

    public function create()
    {
        return view('posts.create');
    }

    public function store(Request $request)
    {
        Post::create([
            'title' => $request->title,
            'content' => $request->content,
            'published_at' => now(),
        ]);
        return redirect('/posts');
    }

    public function edit($id)
    {
        $post = Post::findOrFail($id);
        return view('posts.edit', ['post' => $post]);
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

    public function delete($id)
    {
        Post::findOrFail($id)->delete();
        return redirect('/posts');
    }
}
```

### routes/web.php（追加部分）

```php
use App\Http\Controllers\PostController;

Route::get('/posts', [PostController::class, 'index']);
Route::get('/posts/create', [PostController::class, 'create']);
Route::post('/posts', [PostController::class, 'store']);
Route::get('/posts/{id}/edit', [PostController::class, 'edit']);
Route::put('/posts/{id}', [PostController::class, 'update']);
Route::delete('/posts/{id}', [PostController::class, 'delete']);
```

### resources/views/posts/index.blade.php

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>投稿一覧</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; max-width: 800px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background-color: #f5f5f5; }
        h1 { color: #333; }
        .btn { display: inline-block; padding: 5px 10px; margin: 2px; text-decoration: none; border: 1px solid #333; border-radius: 3px; }
        .btn-primary { background-color: #007bff; color: white; border-color: #007bff; }
        .btn-danger { background-color: #dc3545; color: white; border-color: #dc3545; }
    </style>
</head>
<body>
    <h1>投稿一覧</h1>
    <p><a href="/posts/create" class="btn btn-primary">新規作成</a></p>
    <p>全{{ count($posts) }}件の投稿があります。</p>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>タイトル</th>
                <th>公開日時</th>
                <th>操作</th>
            </tr>
        </thead>
        <tbody>
            @foreach ($posts as $post)
                <tr>
                    <td>{{ $post->id }}</td>
                    <td>{{ $post->title }}</td>
                    <td>{{ $post->published_at?->format('Y/m/d H:i') ?? '下書き' }}</td>
                    <td>
                        <a href="/posts/{{ $post->id }}/edit" class="btn">編集</a>
                        <form action="/posts/{{ $post->id }}" method="POST" style="display:inline;">
                            @csrf
                            @method('DELETE')
                            <button type="submit" class="btn btn-danger">削除</button>
                        </form>
                    </td>
                </tr>
            @endforeach
        </tbody>
    </table>
</body>
</html>
```

### resources/views/posts/create.blade.php

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>投稿作成</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        h1 { color: #333; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input, textarea { width: 100%; max-width: 400px; padding: 8px; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>投稿作成</h1>
    <form action="/posts" method="POST">
        @csrf
        <div class="form-group">
            <label>タイトル</label>
            <input type="text" name="title" required>
        </div>
        <div class="form-group">
            <label>内容</label>
            <textarea name="content" rows="5"></textarea>
        </div>
        <button type="submit">作成</button>
    </form>
    <p><a href="/posts">← 一覧に戻る</a></p>
</body>
</html>
```

### resources/views/posts/edit.blade.php

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>投稿編集</title>
    <style>
        body { font-family: sans-serif; margin: 20px; }
        h1 { color: #333; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input, textarea { width: 100%; max-width: 400px; padding: 8px; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>投稿編集</h1>
    <form action="/posts/{{ $post->id }}" method="POST">
        @csrf
        @method('PUT')
        <div class="form-group">
            <label>タイトル</label>
            <input type="text" name="title" value="{{ $post->title }}" required>
        </div>
        <div class="form-group">
            <label>内容</label>
            <textarea name="content" rows="5">{{ $post->content }}</textarea>
        </div>
        <button type="submit">更新</button>
    </form>
    <p><a href="/posts">← 一覧に戻る</a></p>
</body>
</html>
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

## 📤 GitHubに push しよう

5-1-7 で覚えた手順を使って、成果物をGitHubの **publicリポジトリ** に push しましょう。

```bash
# eloquent-app-practice ディレクトリに移動
cd ~/laravel-practice/9-4-9_hands-on/eloquent-app-practice

# Git の初期化、commit、リモート設定、push
git init
git add .
git commit -m "first commit"
git remote add origin <あなたのリポジトリのURL>
git branch -M main
git push -u origin main
```

> ⚠️ **詰まったときは**: Tutorial 5-1-7「📤 GitHubに push しよう」や Tutorial 4-4-2〜4-4-3 を見直してみましょう。

### ✅ push 完了チェック

- [ ] GitHub に `eloquent-app-practice` リポジトリを作成した（**public** で作成）
- [ ] 「📦 GitHubでのコード管理」の雛形を参考に `README.md` を **自分の言葉で** 作成した
- [ ] `commit` と `push` を完了して、GitHubに反映されている

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ Eloquentモデルを作成できる
- ✅ `create()`, `update()`, `delete()`でCRUD操作ができる
- ✅ コントローラーとルーティングを連携できる

引き続き、次のセクションも頑張りましょう！

### 🛑 Sailの停止

次のセクションに進む前に、Sailを停止しておきましょう。

```bash
./vendor/bin/sail down
```

> 💡 **なぜ停止するの？**: Sailを起動したままだと、次のセクションで別のプロジェクトを起動する際にポートが競合してエラーになることがあります。セクションの終わりには必ずSailを停止する習慣をつけましょう。

---
