# Tutorial 10-3-5: 認可機能 - ハンズオン演習

## 📝 このセクションの目的

Chapter 3で学んだ認可機能を実際に手を動かして確認します。ポリシーを使って、ユーザーごとのアクセス制御を実装しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのプロジェクトを作成します。

```
~/laravel-practice/
├── 10-3-6_hands-on/                      ← このハンズオン用のディレクトリ
│   ├── authorization-app-practice/       ← 要件を見て自分で作成するプロジェクト
│   │   ├── app/
│   │   │   ├── Http/Controllers/
│   │   │   └── Policies/
│   │   └── ...
│   └── authorization-app-sample/         ← 実践で一緒に作成するプロジェクト
│       ├── app/
│       │   ├── Http/Controllers/
│       │   └── Policies/
│       └── ...
└── ...
```

| ディレクトリ | 用途 | URL |
|:---|:---|:---|
| `authorization-app-practice/` | 📋 要件を見て、自分の力で作成する | `http://localhost/posts` |
| `authorization-app-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する | `http://localhost/posts` |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

> ⚠️ **注意**: 2つのプロジェクトを同時に起動することはできません（ポートが競合するため）。一方のプロジェクトで作業する際は、もう一方を停止してください。

---

## 🎯 演習課題：投稿の編集権限制御

### 📋 要件

1. `PostPolicy`を作成
2. 投稿の作成者のみが編集・削除できるようにする
3. コントローラーで`authorize()`を使用

---

### 📁 Step 0: 環境を準備する（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

> **📌 前のハンズオンのプロジェクトを停止**
> 
> 前のハンズオン（10-2-5）のプロジェクトが起動している場合は、先に停止してください。
> ```bash
> cd ~/laravel-practice/10-2-5_hands-on/lifecycle-app-sample
> ./vendor/bin/sail down
> ```

```bash
# laravel-practiceディレクトリに移動
cd ~/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 10-3-6_hands-on
cd 10-3-6_hands-on

# Laravel 10.xプロジェクトを作成（自分で作成する用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 authorization-app-practice
```

```bash
# プロジェクトディレクトリに移動
cd authorization-app-practice

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

**✅ ディレクトリ構造の確認**

```
~/laravel-practice/
└── 10-3-6_hands-on/
    └── authorization-app-practice/     ← 自分で作成する用（今ここ）
        ├── app/
        │   ├── Http/Controllers/
        │   └── Policies/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

> 💡 **ポイント**: 認可機能のテストには、複数のユーザーと投稿データが必要です。実践セクションの「ステップ5: テストする」で、tinkerを使ってテストデータを作成します。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

```bash
sail artisan make:policy PostPolicy --model=Post
```

```php
public function update(User $user, Post $post)
{
    return $user->id === $post->user_id;
}

// コントローラー
$this->authorize('update', $post);
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？認可機能はユーザーごとのアクセス制御を実現する重要な機能です。一緒に手を動かしながら、投稿の編集権限制御を実装していきましょう。

> 📌 **注意**: ここからは`authorization-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### 💻 環境準備（実践用プロジェクト）

まず、**自分で作成する用のプロジェクトを停止**します：

```bash
# authorization-app-practiceディレクトリに移動
cd ~/laravel-practice/10-3-6_hands-on/authorization-app-practice

# Sailを停止
./vendor/bin/sail down
```

次に、**実践用のプロジェクトを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/laravel-practice/10-3-6_hands-on

# Laravel 10.xプロジェクトを作成（実践用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 authorization-app-sample
```

```bash
# プロジェクトディレクトリに移動
cd authorization-app-sample

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

**✅ ディレクトリ構造の確認**

```
~/laravel-practice/
└── 10-3-6_hands-on/
    ├── authorization-app-practice/     ← 自分で作成した用（停止中）
    └── authorization-app-sample/       ← 実践用（今ここ、起動中）
        ├── app/
        │   ├── Http/Controllers/
        │   └── Policies/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

> 💡 **ポイント**: 認可機能のテストには、複数のユーザーと投稿データが必要です。ステップ5でtinkerを使ってテストデータを作成します。

---

### 💭 実装の思考プロセス

認可機能を実装する際、以下の順番で考えると効率的です：

1. **ポリシーを作成**：Artisanコマンドで生成
2. **権限チェックロジックを実装**：作成者とユーザーIDを比較
3. **コントローラーでauthorizeを使用**：権限チェックを実行
4. **ビューで@canを使用**：権限に応じて表示を切り替え
5. **テスト**：作成者と他ユーザーで動作確認

認可のポイントは「ポリシーで権限ロジックを集約管理し、再利用性を高める」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: ポリシーを作成する

**何を考えているか**：
- 「投稿の権限を管理するポリシーが必要だ」
- 「`--model`オプションでPostモデルと紐付けよう」
- 「Artisanコマンドで簡単に生成できる」

ターミナルで以下のコマンドを実行します：

```bash
sail artisan make:policy PostPolicy --model=Post
```

**コマンド解説**：

```bash
sail artisan make:policy PostPolicy --model=Post
```
→ `PostPolicy`ポリシーを生成します。`--model=Post`でPostモデルと紐付け、基本的なメソッドが自動生成されます。`app/Policies/PostPolicy.php`が作成されます。

---

#### ステップ2: 権限チェックロジックを実装する

**何を考えているか**：
- 「投稿の作成者とログイン中のユーザーIDを比較しよう」
- 「編集と削除の権限を定義しよう」
- 「作成者のみがtrueを返すようにしよう」

`app/Policies/PostPolicy.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    public function update(User $user, Post $post)
    {
        return $user->id === $post->user_id;
    }

    public function delete(User $user, Post $post)
    {
        return $user->id === $post->user_id;
    }
}
```

**コードリーディング**：

```php
public function update(User $user, Post $post)
{
    return $user->id === $post->user_id;
}
```
→ `update`メソッドで編集権限を定義します。`$user->id === $post->user_id`でログイン中のユーザーIDと投稿の作成者IDを比較し、一致すれば`true`を返します。

```php
public function delete(User $user, Post $post)
{
    return $user->id === $post->user_id;
}
```
→ `delete`メソッドで削除権限を定義します。同じく作成者のみが削除できるようにします。

---

#### ステップ3: コントローラーでauthorizeを使用する

**何を考えているか**：
- 「編集、更新、削除の前に権限チェックをしよう」
- 「`$this->authorize()`で簡単にチェックできる」
- 「権限がない場合は自動的に403エラーを返す」

`app/Http/Controllers/PostController.php`を開いて、以下のように編集します：

```php
public function edit($id)
{
    $post = Post::findOrFail($id);
    $this->authorize('update', $post);
    return view('posts.edit', ['post' => $post]);
}

public function update(Request $request, $id)
{
    $post = Post::findOrFail($id);
    $this->authorize('update', $post);
    $post->update($request->all());
    return redirect('/posts');
}

public function destroy($id)
{
    $post = Post::findOrFail($id);
    $this->authorize('delete', $post);
    $post->delete();
    return redirect('/posts');
}
```

**コードリーディング**：

```php
$this->authorize('update', $post);
```
→ `authorize()`メソッドで権限チェックを実行します。第1引数にアクション名、第2引数にモデルインスタンスを渡します。Laravelが自動的に`PostPolicy`の`update`メソッドを呼び出します。

```php
$this->authorize('delete', $post);
```
→ 削除権限をチェックします。権限がない場合、自動的に403エラーが返されます。

---

#### ステップ4: ビューで@canを使用する

**何を考えているか**：
- 「権限がある場合のみ編集・削除ボタンを表示したい」
- 「@canディレクティブで簡単に制御できる」
- 「ユーザーエクスペリエンスを向上させよう」

`resources/views/posts/index.blade.php`を開いて、以下のように編集します：

```blade
@foreach ($posts as $post)
    <div>
        <h3>{{ $post->title }}</h3>
        <p>{{ $post->content }}</p>
        
        @can('update', $post)
            <a href="{{ route('posts.edit', $post->id) }}">編集</a>
        @endcan
        
        @can('delete', $post)
            <form action="{{ route('posts.destroy', $post->id) }}" method="POST">
                @csrf
                @method('DELETE')
                <button type="submit">削除</button>
            </form>
        @endcan
    </div>
@endforeach
```

**コードリーディング**：

```blade
@can('update', $post)
    <a href="{{ route('posts.edit', $post->id) }}">編集</a>
@endcan
```
→ `@can`ディレクティブで権限チェックを行います。権限がある場合のみ編集リンクが表示されます。ユーザーに不必要なボタンを見せないことで、UXが向上します。

```blade
@can('delete', $post)
    <form action="{{ route('posts.destroy', $post->id) }}" method="POST">
        @csrf
        @method('DELETE')
        <button type="submit">削除</button>
    </form>
@endcan
```
→ 削除権限がある場合のみ削除ボタンが表示されます。

---

#### ステップ5: テストする

**何を考えているか**：
- 「作成者と他ユーザーで動作を確認しよう」
- 「作成者は編集・削除できて、他ユーザーはできないはず」

**テストデータの作成**：

まず、tinkerでテスト用のユーザーと投稿を作成します：

```bash
sail artisan tinker
```

```php
>>> use App\Models\User;
>>> use App\Models\Post;

// ユーザーAを作成
>>> $userA = User::create([
...     'name' => 'ユーザーA',
...     'email' => 'user_a@example.com',
...     'password' => bcrypt('password'),
... ]);

// ユーザーBを作成
>>> $userB = User::create([
...     'name' => 'ユーザーB',
...     'email' => 'user_b@example.com',
...     'password' => bcrypt('password'),
... ]);

// ユーザーAの投稿を作成
>>> Post::create([
...     'user_id' => $userA->id,
...     'title' => 'ユーザーAの投稿',
...     'content' => 'これはユーザーAが作成した投稿です。',
... ]);

// ユーザーBの投稿を作成
>>> Post::create([
...     'user_id' => $userB->id,
...     'title' => 'ユーザーBの投稿',
...     'content' => 'これはユーザーBが作成した投稿です。',
... ]);

>>> exit
```

**テスト手順**：

1. **ユーザーAでログイン**（`user_a@example.com` / `password`）
2. **ユーザーAの投稿に編集・削除ボタンが表示されることを確認**：作成者なので権限あり
3. **ユーザーBの投稿には編集・削除ボタンが表示されないことを確認**：他ユーザーの投稿なので権限なし
4. **ログアウトしてユーザーBでログイン**（`user_b@example.com` / `password`）
5. **ユーザーAの投稿に編集・削除ボタンが表示されないことを確認**：他ユーザーの投稿なので権限なし
6. **直接URLでアクセス**（`http://localhost/posts/1/edit`）：403エラーが表示されることを確認

---

### ✨ 完成！

これで認可機能が実装できました！ポリシーで権限ロジックを集約管理し、ユーザーごとのアクセス制御を実現できましたね。

**自分で作成したコードと比較してみましょう**：
- `authorization-app-practice/`: 自分で作成したプロジェクト
- `authorization-app-sample/`: 一緒に作成したプロジェクト

両方のプロジェクトを見比べて、違いがあれば確認してみてください。

---

## 📖 模範解答

### PostPolicy.php

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    public function update(User $user, Post $post)
    {
        return $user->id === $post->user_id;
    }

    public function delete(User $user, Post $post)
    {
        return $user->id === $post->user_id;
    }
}
```

### PostController.php

```php
public function edit($id)
{
    $post = Post::findOrFail($id);
    $this->authorize('update', $post);
    return view('posts.edit', ['post' => $post]);
}

public function update(Request $request, $id)
{
    $post = Post::findOrFail($id);
    $this->authorize('update', $post);
    $post->update($request->all());
    return redirect('/posts');
}

public function destroy($id)
{
    $post = Post::findOrFail($id);
    $this->authorize('delete', $post);
    $post->delete();
    return redirect('/posts');
}
```

### posts/index.blade.php

```blade
@foreach ($posts as $post)
    <div>
        <h3>{{ $post->title }}</h3>
        @can('update', $post)
            <a href="{{ route('posts.edit', $post->id) }}">編集</a>
        @endcan
        @can('delete', $post)
            <form action="{{ route('posts.destroy', $post->id) }}" method="POST">
                @csrf
                @method('DELETE')
                <button type="submit">削除</button>
            </form>
        @endcan
    </div>
@endforeach
```

---

## 🧪 動作確認の方法

### プロジェクトの切り替え

2つのプロジェクトを切り替えて動作確認する方法：

```bash
# authorization-app-practiceで確認したい場合
cd ~/laravel-practice/10-3-6_hands-on/authorization-app-sample
./vendor/bin/sail down

cd ~/laravel-practice/10-3-6_hands-on/authorization-app-practice
./vendor/bin/sail up -d

# authorization-app-sampleで確認したい場合
cd ~/laravel-practice/10-3-6_hands-on/authorization-app-practice
./vendor/bin/sail down

cd ~/laravel-practice/10-3-6_hands-on/authorization-app-sample
./vendor/bin/sail up -d
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ ポリシーを作成して権限ロジックを集約管理できる
- ✅ コントローラーで`authorize()`を使って権限チェックができる
- ✅ ビューで`@can`ディレクティブを使って表示を制御できる
- ✅ ユーザーごとのアクセス制御を実装できる

引き続き、次のセクションも頑張りましょう！

---
