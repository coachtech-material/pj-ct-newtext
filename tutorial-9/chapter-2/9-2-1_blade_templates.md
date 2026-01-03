# Tutorial 9-2-1: Bladeテンプレートの基本（データの表示）

## 🎯 このセクションで学ぶこと

*   Bladeテンプレートエンジンが何であるか、MVCのViewとしての役割を理解する。
*   XSS対策：`{{ $var }}`（エスケープあり）と`{!! $var !!}`（エスケープなし）の使い分けとリスクを理解する。
*   デバッグ習慣：画面が真っ白になったらまず`@dd($var)`を仕込むテクニックを身につける。

---

## 導入：PHPとHTMLを分離する意義（MVCのView）

これまでのセクションで、ルーティングとコントローラーを学びました。MVCアーキテクチャでは、**Controller**がリクエストを処理し、**Model**がデータを扱い、**View**がデータを表示します。

Laravelでは、**Blade（ブレード）**というテンプレートエンジンがViewの役割を担います。

**なぜPHPとHTMLを分離するのか？**

生のPHPでHTMLを生成する場合、以下のような問題があります。

```php
<?php
$users = [
    ['name' => '山田太郎', 'email' => 'taro@example.com'],
    ['name' => '鈴木花子', 'email' => 'hanako@example.com'],
];
?>

<ul>
    <?php foreach ($users as $user): ?>
        <li><?php echo htmlspecialchars($user['name']); ?> (<?php echo htmlspecialchars($user['email']); ?>)</li>
    <?php endforeach; ?>
</ul>
```

このコードには、以下のような問題があります。

*   `<?php ?>` タグが頻繁に登場し、読みにくい
*   XSS攻撃を防ぐために、毎回`htmlspecialchars()`を書く必要がある
*   HTMLとPHPが混在し、コードの見通しが悪い

**Bladeを使う場合**

```blade
<ul>
    @foreach ($users as $user)
        <li>{{ $user->name }} ({{ $user->email }})</li>
    @endforeach
</ul>
```

Bladeを使うと、以下のようなメリットがあります。

*   `@foreach`, `@if`などの直感的な構文で、コードが読みやすい
*   `{{ }}`による出力は、自動的にHTMLエスケープされ、XSS攻撃を防ぐ
*   HTMLとロジックが分離され、コードの見通しが良い

---

## 詳細解説

### 🎨 Bladeの基本構文：変数の出力

Bladeでは、`{{ }}`で変数を出力します。

```blade
<p>こんにちは、{{ $name }}さん！</p>
```

コントローラーから渡された`$name`変数の値が、HTMLに埋め込まれます。

### 🔒 XSS対策：エスケープありとなしの使い分け

**XSS（クロスサイトスクリプティング）攻撃**とは、悪意のあるスクリプトをWebページに埋め込む攻撃です。

例えば、ユーザーが入力した名前が`<script>alert('攻撃')</script>`だった場合、そのままHTMLに出力すると、スクリプトが実行されてしまいます。

#### `{{ }}` - エスケープあり（推奨）

```blade
{{ $userInput }}
```

`{{ }}`で出力すると、HTMLの特殊文字が自動的にエスケープされます。

| 入力値 | 出力結果 |
|:---|:---|
| `<script>alert('攻撃')</script>` | `&lt;script&gt;alert('攻撃')&lt;/script&gt;` |
| `<b>太字</b>` | `&lt;b&gt;太字&lt;/b&gt;` |

スクリプトは実行されず、文字列として表示されます。**ユーザーからの入力は、必ず`{{ }}`で出力してください。**

#### `{!! !!}` - エスケープなし（危険）

```blade
{!! $htmlContent !!}
```

`{!! !!}`で出力すると、HTMLがそのまま出力されます。

| 入力値 | 出力結果 |
|:---|:---|
| `<script>alert('攻撃')</script>` | スクリプトが実行される |
| `<b>太字</b>` | **太字**（HTMLとして解釈される） |

> ⚠️ **警告**: `{!! !!}`は、XSS攻撃のリスクがあります。**信頼できるデータ（管理者が入力したHTMLなど）にのみ使用してください。**ユーザーからの入力には絶対に使わないでください。

#### 使い分けの判断基準

| 状況 | 使用する構文 |
|:---|:---|
| ユーザーからの入力を表示 | `{{ }}` |
| データベースから取得した文字列を表示 | `{{ }}` |
| 管理者が入力したHTML（リッチテキスト）を表示 | `{!! !!}`（要注意） |
| 自分で書いたHTMLを変数に入れて表示 | `{!! !!}` |

---

### 🐛 デバッグ習慣：`@dd()`を使いこなす

開発中、「画面が真っ白になった」「期待したデータが表示されない」という問題に遭遇することがあります。そんなときは、**`@dd()`ディレクティブ**を使ってデバッグしましょう。

#### `@dd()` - Dump and Die

```blade
@dd($users)
```

`@dd()`は、変数の内容を表示して、処理を停止します。

**実行結果のイメージ**

```
array:2 [▼
  0 => array:2 [▼
    "name" => "山田太郎"
    "email" => "taro@example.com"
  ]
  1 => array:2 [▼
    "name" => "鈴木花子"
    "email" => "hanako@example.com"
  ]
]
```

#### デバッグの手順

画面が真っ白になったり、期待したデータが表示されない場合は、以下の手順でデバッグします。

1. **Bladeファイルの先頭に`@dd($変数名)`を追加**
2. **ブラウザをリロード**
3. **変数の内容を確認**
   - 変数が`null`なら、コントローラーからデータが渡されていない
   - 変数が空の配列なら、データベースにデータがない
   - 変数に期待したデータがあれば、Bladeの書き方に問題がある

```blade
{{-- デバッグ用：確認後は削除する --}}
@dd($users)

<h1>ユーザー一覧</h1>
@foreach ($users as $user)
    <li>{{ $user->name }}</li>
@endforeach
```

> 💡 **TIP**: `@dd()`は「Dump and Die」の略で、変数をダンプして処理を停止します。デバッグが終わったら、必ず削除してください。

#### `@dump()` - 処理を停止しない

```blade
@dump($users)
```

`@dump()`は、変数の内容を表示しますが、処理は停止しません。複数の変数を確認したい場合に便利です。

---

### 📂 Bladeファイルの配置場所

Bladeファイルは、`resources/views/`ディレクトリに配置し、`.blade.php`という拡張子を付けます。

```
resources/
└── views/
    ├── welcome.blade.php
    ├── users/
    │   ├── index.blade.php
    │   └── show.blade.php
    └── posts/
        └── index.blade.php
```

コントローラーから、以下のようにビューを呼び出します。

```php
// resources/views/users/index.blade.php を読み込む
return view('users.index', compact('users'));
```

ディレクトリの区切りは、ドット（`.`）で表現します。

---

### 🏃 実践：コントローラーからデータを渡す

#### ステップ1: コントローラーでデータを準備

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;

class UserController extends Controller
{
    public function index()
    {
        // データベースから全てのユーザーを取得
        $users = User::all();

        // ビューにデータを渡す
        return view('users.index', compact('users'));
    }
}
```

**コードリーディング**

*   `User::all()`: Eloquentを使って、全てのユーザーを取得します。
*   `compact('users')`: `$users`変数をビューに渡します。`['users' => $users]`と同じ意味です。

#### ステップ2: Bladeでデータを表示

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ユーザー一覧</title>
</head>
<body>
    {{-- デバッグ：データが渡されているか確認（確認後は削除） --}}
    {{-- @dd($users) --}}

    <h1>ユーザー一覧</h1>

    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }} ({{ $user->email }})</li>
        @endforeach
    </ul>
</body>
</html>
```

**コードリーディング**

*   `@foreach ($users as $user)`: コントローラーから渡された`$users`をループします。
*   `{{ $user->name }}`: `$user`オブジェクトの`name`プロパティを出力します。自動的にHTMLエスケープされます。

---

### 📝 コメント

Bladeには、HTMLとして出力されないコメントを書くことができます。

```blade
{{-- これはBladeのコメントです。HTMLには出力されません。 --}}

<!-- これはHTMLのコメントです。ブラウザのソースコードに表示されます。 -->
```

機密情報や開発メモは、Bladeのコメント（`{{-- --}}`）を使いましょう。HTMLコメント（`<!-- -->`）は、ブラウザの「ソースを表示」で見えてしまいます。

---

## ✨ まとめ

このセクションでは、Bladeテンプレートエンジンの基本概念を学びました。

*   **MVCのView**: BladeはLaravelのViewを担当し、PHPとHTMLを分離することで、コードの見通しを良くする。
*   **XSS対策**: `{{ }}`はHTMLエスケープあり（安全）、`{!! !!}`はエスケープなし（危険）。ユーザー入力は必ず`{{ }}`で出力する。
*   **デバッグ習慣**: 画面が真っ白になったら、まず`@dd($変数名)`を仕込んで、データが渡されているか確認する。
*   **ファイル配置**: Bladeファイルは`resources/views/`に`.blade.php`拡張子で配置する。

次のセクションでは、`@foreach`、`@if`、`@forelse`などの制御構文を詳しく学びます。

---
