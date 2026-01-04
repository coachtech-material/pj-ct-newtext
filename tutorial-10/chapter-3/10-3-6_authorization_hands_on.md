# Tutorial 10-3-6: 認可機能 - ハンズオン演習

## 📝 このセクションの目的

Chapter 9で学んだ認可機能を実際に手を動かして確認します。ポリシーを使って、ユーザーごとのアクセス制御を実装しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 🎯 演習課題：投稿の編集権限制御

### 📋 要件

1. `PostPolicy`を作成
2. 投稿の作成者のみが編集・削除できるようにする
3. コントローラーで`authorize()`を使用

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

---

### 💻 環境準備

#### プロジェクトのディレクトリ構造

本教材では、ホームディレクトリ直下の`laravel-practice`フォルダ内に、ハンズオンごとにプロジェクトを作成します。

```
~/laravel-practice/
├── ... (前のハンズオンのプロジェクト)
├── authorization-app/   ← このハンズオンで作成
└── ...
```

#### 新しいプロジェクトを作成する

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

**Step 1: Laravelプロジェクトの作成**

```bash
cd ~/laravel-practice

docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 authorization-app
```

**Step 2: プロジェクトディレクトリに移動してSailをセットアップ**

```bash
cd authorization-app

docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql
```

**Step 3: Sailの起動と初期設定**

```bash
./vendor/bin/sail up -d
./vendor/bin/sail artisan key:generate
./vendor/bin/sail artisan migrate
```

> 💡 **環境構築が完了！** `http://localhost` にアクセスして確認してください。

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

テスト手順：

1. **ユーザーAでログイン**：投稿を作成
2. **編集・削除ボタンが表示されることを確認**：作成者なので権限あり
3. **ユーザーBでログイン**：同じ投稿を表示
4. **編集・削除ボタンが表示されないことを確認**：他ユーザーなので権限なし
5. **直接URLでアクセス**：403エラーが表示されることを確認

---

### ✨ 完成！

これで認可機能が実装できました！ポリシーで権限ロジックを集約管理し、ユーザーごとのアクセス制御を実現できましたね。

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

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ Chapter 9で学んだ認可機能を実際に手を動かして確認します。ポリシーを使って、ユーザーごとのアクセス制御を実装しましょう。

引き続き、次のセクションも頑張りましょう！

---
