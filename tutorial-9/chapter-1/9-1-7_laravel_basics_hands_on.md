# Tutorial 9-1-7: Laravel基礎 - ハンズオン演習

## 📝 このセクションの目的

Chapter 1で学んだLaravelの基礎を実際に手を動かして確認します。ルーティング、コントローラー、ビューの連携を実践しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 🎯 演習課題：自己紹介ページを作成しよう

### 📋 要件

1. `/profile`にアクセスすると、自己紹介ページが表示される
2. `ProfileController`を作成する
3. `profile.blade.php`ビューを作成する
4. 名前、年齢、趣味を表示する

---

## 💡 ヒント

\`\`\`bash
php artisan make:controller ProfileController
\`\`\`

\`\`\`php
Route::get('/profile', [ProfileController::class, 'index']);
\`\`\`

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？Laravelの基本はルーティング、コントローラー、ビューの連携です。一緒に手を動かしながら、自己紹介ページを作成していきましょう。

### 💭 実装の思考プロセス

Laravelでページを作成する際、以下の順番で考えると効率的です：

1. **コントローラーを作成**：Artisanコマンドでコントローラーを生成
2. **ルーティングを定義**：URLとコントローラーを結びつける
3. **コントローラーにロジックを追加**：データを準備してビューに渡す
4. **ビューを作成**：BladeテンプレートでHTMLを記述
5. **ブラウザで確認**：実際にアクセスして表示を確認

Laravel開発のポイントは「ルーティング→コントローラー→ビューの流れを理解する」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: コントローラーを作成する

**何を考えているか**：
- 「プロフィールページを表示するコントローラーが必要だ」
- 「Artisanコマンドで簡単に生成できる」
- 「ProfileControllerという名前にしよう」

ターミナルで以下のコマンドを実行します：

```bash
php artisan make:controller ProfileController
```

**コマンド解説**：

```bash
php artisan make:controller ProfileController
```
→ Artisanコマンドで`ProfileController`を生成します。`app/Http/Controllers/ProfileController.php`が作成されます。

---

#### ステップ2: ルーティングを定義する

**何を考えているか**：
- 「`/profile`にアクセスしたらProfileControllerの処理を実行したい」
- 「`routes/web.php`にルートを追加しよう」
- 「コントローラーの`index`メソッドを呼び出そう」

`routes/web.php`を開いて、以下を追加します：

```php
use App\Http\Controllers\ProfileController;

Route::get('/profile', [ProfileController::class, 'index']);
```

**コードリーディング**：

```php
use App\Http\Controllers\ProfileController;
```
→ ProfileControllerクラスをインポートします。名前空間を使用するために必要です。

```php
Route::get('/profile', [ProfileController::class, 'index']);
```
→ `/profile`へのGETリクエストを`ProfileController`の`index`メソッドにルーティングします。`[ProfileController::class, 'index']`は配列形式のルート定義です。

---

#### ステップ3: コントローラーにロジックを追加する

**何を考えているか**：
- 「プロフィール情報（名前、年齢、趣味）を準備しよう」
- 「データを配列でまとめて、ビューに渡そう」
- 「`view()`ヘルパーでビューを返そう」

`app/Http/Controllers/ProfileController.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Http\Controllers;

class ProfileController extends Controller
{
    public function index()
    {
        $data = [
            'name' => '山田太郎',
            'age' => 25,
            'hobbies' => ['プログラミング', '読書', '旅行'],
        ];
        
        return view('profile', $data);
    }
}
```

**コードリーディング**：

```php
namespace App\Http\Controllers;
```
→ コントローラーの名前空間を定義します。Laravelのコントローラーはこの名前空間に配置されます。

```php
class ProfileController extends Controller
```
→ `Controller`クラスを継承します。Laravelのコントローラーの基本機能を利用できます。

```php
public function index()
```
→ `index`メソッドを定義します。ルートから呼び出されるメソッドです。

```php
$data = [
    'name' => '山田太郎',
    'age' => 25,
    'hobbies' => ['プログラミング', '読書', '旅行'],
];
```
→ プロフィール情報を配列で準備します。名前、年齢、趣味のデータを含んでいます。

```php
return view('profile', $data);
```
→ `view()`ヘルパーで`profile`ビューを返します。第2引数に`$data`を渡すことで、ビュー側でデータを利用できます。

---

#### ステップ4: ビューを作成する

**何を考えているか**：
- 「`resources/views/profile.blade.php`を作成しよう」
- 「BladeテンプレートでHTMLを記述しよう」
- 「コントローラーから渡されたデータを表示しよう」

`resources/views/profile.blade.php`を作成して、以下のように記述します：

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>プロフィール</title>
</head>
<body>
    <h1>プロフィール</h1>
    <p>名前: {{ $name }}</p>
    <p>年齢: {{ $age }}歳</p>
    <p>趣味:</p>
    <ul>
        @foreach ($hobbies as $hobby)
            <li>{{ $hobby }}</li>
        @endforeach
    </ul>
</body>
</html>
```

**コードリーディング**：

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>プロフィール</title>
</head>
```
→ 基本的なHTML構造を定義します。

```blade
<p>名前: {{ $name }}</p>
<p>年齢: {{ $age }}歳</p>
```
→ `{{ }}`で変数を出力します。Bladeテンプレートの基本構文で、自動的にHTMLエスケープされます。

```blade
@foreach ($hobbies as $hobby)
    <li>{{ $hobby }}</li>
@endforeach
```
→ `@foreach`ディレクティブで配列をループ処理します。`$hobbies`配列の各要素を`$hobby`として取り出し、リスト表示します。

---

#### ステップ5: ブラウザで確認する

**何を考えているか**：
- 「開発サーバーを起動しよう」
- 「`/profile`にアクセスして表示を確認しよう」
- 「データが正しく表示されているかチェックしよう」

ターミナルで以下のコマンドを実行します：

```bash
php artisan serve
```

ブラウザで`http://localhost:8000/profile`にアクセスして、プロフィールページが表示されることを確認します。

---

### ✨ 完成！

これでLaravelの基本的なページ作成が完成しました！ルーティング、コントローラー、ビューの連携を実践できましたね。

---

## 📖 模範解答

### ProfileController.php

\`\`\`php
<?php

namespace App\Http\Controllers;

class ProfileController extends Controller
{
    public function index()
    {
        $data = [
            'name' => '山田太郎',
            'age' => 25,
            'hobbies' => ['プログラミング', '読書', '旅行'],
        ];
        
        return view('profile', $data);
    }
}
\`\`\`

### routes/web.php

\`\`\`php
use App\Http\Controllers\ProfileController;

Route::get('/profile', [ProfileController::class, 'index']);
\`\`\`

### profile.blade.php

\`\`\`blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>プロフィール</title>
</head>
<body>
    <h1>プロフィール</h1>
    <p>名前: {{ \$name }}</p>
    <p>年齢: {{ \$age }}歳</p>
    <p>趣味:</p>
    <ul>
        @foreach (\$hobbies as \$hobby)
            <li>{{ \$hobby }}</li>
        @endforeach
    </ul>
</body>
</html>
\`\`\`
---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ Chapter 1で学んだLaravelの基礎を実際に手を動かして確認します。ルーティング、コントローラー、ビューの連携を実践しましょう。

引き続き、次のセクションも頑張りましょう！

---
