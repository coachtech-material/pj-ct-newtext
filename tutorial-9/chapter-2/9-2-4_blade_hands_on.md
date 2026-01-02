# Tutorial 9-2-4: Bladeテンプレート - ハンズオン演習

## 📝 このセクションの目的

Chapter 2で学んだBladeテンプレートを実際に手を動かして確認します。レイアウト、継承、ディレクティブを実践しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 🎯 演習課題：ブログ記事一覧ページを作成しよう

### 📋 要件

1. レイアウトファイル`layouts/app.blade.php`を作成
2. 記事一覧ページ`posts/index.blade.php`を作成
3. 記事データをコントローラーから渡す
4. @foreach、@if、@extendを使用

---

## 💡 ヒント

\`\`\`blade
@extends('layouts.app')

@section('content')
    <!-- コンテンツ -->
@endsection
\`\`\`

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？Bladeテンプレートはレイアウト継承でコードを再利用できる強力な機能です。一緒に手を動かしながら、ブログ記事一覧ページを作成していきましょう。

### 💭 実装の思考プロセス

Bladeテンプレートでページを作成する際、以下の順番で考えると効率的です：

1. **レイアウトファイルを作成**：共通のHTML構造を定義
2. **コントローラーでデータを準備**：記事データを配列で用意
3. **子ビューでレイアウトを継承**：@extendsでレイアウトを継承
4. **ディレクティブでデータを表示**：@foreachと@ifで動的に表示
5. **ルートを追加して確認**：ブラウザで表示を確認

Bladeのポイントは「レイアウト継承で共通部分を再利用し、ディレクティブで動的な表示を実現する」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: レイアウトファイルを作成する

**何を考えているか**：
- 「全ページで共通のレイアウトを作ろう」
- 「ヘッダー、フッター、コンテンツ部分を分けよう」
- 「@yieldでコンテンツを挿入できるようにしよう」

`resources/views/layouts/app.blade.php`を作成します：

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>@yield('title', 'ブログ')</title>
</head>
<body>
    <header>
        <h1>My Blog</h1>
    </header>
    <main>
        @yield('content')
    </main>
    <footer>
        <p>&copy; 2024 My Blog</p>
    </footer>
</body>
</html>
```

**コードリーディング**：

```blade
<title>@yield('title', 'ブログ')</title>
```
→ `@yield`ディレクティブでセクションを定義します。第2引数はデフォルト値で、子ビューで指定がない場合に使用されます。

```blade
@yield('content')
```
→ メインコンテンツを挿入する位置を定義します。子ビューから`@section('content')`で内容を渡します。

---

#### ステップ2: コントローラーでデータを準備する

**何を考えているか**：
- 「記事データを配列で用意しよう」
- 「タイトルと本文を含むデータを作ろう」
- 「ビューにデータを渡そう」

まず、`PostController`を作成します：

```bash
php artisan make:controller PostController
```

`app/Http/Controllers/PostController.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Http\Controllers;

class PostController extends Controller
{
    public function index()
    {
        $posts = [
            ['title' => '初めての記事', 'content' => 'こんにちは'],
            ['title' => '2つ目の記事', 'content' => 'Laravelは楽しい'],
        ];
        
        return view('posts.index', ['posts' => $posts]);
    }
}
```

**コードリーディング**：

```php
$posts = [
    ['title' => '初めての記事', 'content' => 'こんにちは'],
    ['title' => '2つ目の記事', 'content' => 'Laravelは楽しい'],
];
```
→ 記事データを配列で用意します。各記事はタイトルと本文を持ちます。

```php
return view('posts.index', ['posts' => $posts]);
```
→ `posts.index`ビューにデータを渡します。`posts.index`は`resources/views/posts/index.blade.php`を意味します。

---

#### ステップ3: 子ビューでレイアウトを継承する

**何を考えているか**：
- 「レイアウトを継承して、共通部分を再利用しよう」
- 「@extendsでレイアウトを指定しよう」
- 「@sectionでコンテンツを定義しよう」

`resources/views/posts/index.blade.php`を作成します：

```blade
@extends('layouts.app')

@section('title', '記事一覧')

@section('content')
    <h2>記事一覧</h2>
    @if (count($posts) > 0)
        @foreach ($posts as $post)
            <article>
                <h3>{{ $post['title'] }}</h3>
                <p>{{ $post['content'] }}</p>
            </article>
        @endforeach
    @else
        <p>記事がありません</p>
    @endif
@endsection
```

**コードリーディング**：

```blade
@extends('layouts.app')
```
→ `@extends`ディレクティブでレイアウトを継承します。`layouts.app`は`resources/views/layouts/app.blade.php`を意味します。

```blade
@section('title', '記事一覧')
```
→ `@section`でタイトルを定義します。第2引数で直接値を指定できます。

```blade
@section('content')
    <!-- コンテンツ -->
@endsection
```
→ `@section`と`@endsection`でコンテンツを定義します。この内容がレイアウトの`@yield('content')`に挿入されます。

---

#### ステップ4: ディレクティブでデータを表示する

**何を考えているか**：
- 「記事があるかどうかをチェックしよう」
- 「@ifで条件分岐しよう」
- 「@foreachで記事をループ表示しよう」

コンテンツ部分を詳しく見ていきましょう：

```blade
@if (count($posts) > 0)
```
→ `@if`ディレクティブで条件分岐します。`count($posts) > 0`で記事があるかどうかをチェックします。

```blade
@foreach ($posts as $post)
    <article>
        <h3>{{ $post['title'] }}</h3>
        <p>{{ $post['content'] }}</p>
    </article>
@endforeach
```
→ `@foreach`ディレクティブで記事をループ表示します。`$posts`配列の各要素を`$post`として取り出し、タイトルと本文を表示します。

```blade
@else
    <p>記事がありません</p>
@endif
```
→ `@else`で記事がない場合の表示を定義します。`@endif`で条件分岐を終了します。

---

#### ステップ5: ルートを追加して確認する

**何を考えているか**：
- 「`/posts`にアクセスしたら記事一覧を表示したい」
- 「ルートを追加して、ブラウザで確認しよう」

`routes/web.php`に以下を追加します：

```php
use App\Http\Controllers\PostController;

Route::get('/posts', [PostController::class, 'index']);
```

ブラウザで`http://localhost:8000/posts`にアクセスして、記事一覧が表示されることを確認します。

---

### ✨ 完成！

これでBladeテンプレートのレイアウト継承とディレクティブが実践できました！@extends、@section、@foreach、@ifを使って動的なページを作成できましたね。

---

## 📖 模範解答

### layouts/app.blade.php

\`\`\`blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>@yield('title', 'ブログ')</title>
</head>
<body>
    <header>
        <h1>My Blog</h1>
    </header>
    <main>
        @yield('content')
    </main>
    <footer>
        <p>&copy; 2024 My Blog</p>
    </footer>
</body>
</html>
\`\`\`

### posts/index.blade.php

\`\`\`blade
@extends('layouts.app')

@section('title', '記事一覧')

@section('content')
    <h2>記事一覧</h2>
    @if (count(\$posts) > 0)
        @foreach (\$posts as \$post)
            <article>
                <h3>{{ \$post['title'] }}</h3>
                <p>{{ \$post['content'] }}</p>
            </article>
        @endforeach
    @else
        <p>記事がありません</p>
    @endif
@endsection
\`\`\`

### PostController.php

\`\`\`php
public function index()
{
    \$posts = [
        ['title' => '初めての記事', 'content' => 'こんにちは'],
        ['title' => '2つ目の記事', 'content' => 'Laravelは楽しい'],
    ];
    
    return view('posts.index', ['posts' => \$posts]);
}
\`\`\`
---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ Chapter 2で学んだBladeテンプレートを実際に手を動かして確認します。レイアウト、継承、ディレクティブを実践しましょう。

引き続き、次のセクションも頑張りましょう！

---
