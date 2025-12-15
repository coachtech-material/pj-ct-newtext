# Tutorial 9-2-6: Bladeテンプレート - ハンズオン演習

## 📝 このセクションの目的

Chapter 2で学んだBladeテンプレートを実際に手を動かして確認します。レイアウト、継承、ディレクティブを実践しましょう。

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

## 💪 自己評価チェックリスト

- [ ] レイアウトファイルを作成できた
- [ ] @extendsで継承できた
- [ ] @yieldでコンテンツを挿入できた
- [ ] @foreachでループできた
- [ ] @ifで条件分岐できた

すべてチェックできたら、Chapter 3に進みましょう！
