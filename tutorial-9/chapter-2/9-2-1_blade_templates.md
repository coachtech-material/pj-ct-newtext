# Tutorial 9-2-1: Bladeテンプレートとは

## 🎯 このセクションで学ぶこと

*   Bladeテンプレートエンジンが何であるか、その役割を理解する。
*   なぜBladeを使うのか、「生のPHP」との違いを説明できるようになる。
*   Bladeの基本的な書き方を理解する。

---

## 導入：HTMLに動的なデータを埋め込む

これまでのセクションで、ルーティングとコントローラーを使って、リクエストを処理し、レスポンスを返す方法を学びました。しかし、実際のWebアプリケーションでは、静的なHTMLを返すだけでなく、**データベースから取得したデータを使って、動的にHTMLを生成する**必要があります。

例えば、ユーザー一覧ページでは、データベースから取得したユーザー情報を使って、以下のようなHTMLを生成します。

```html
<ul>
    <li>山田太郎 (taro@example.com)</li>
    <li>鈴木花子 (hanako@example.com)</li>
    <li>佐藤次郎 (jiro@example.com)</li>
</ul>
```

このように、「データ」と「HTML」を組み合わせて動的なページを生成するための仕組みが、**テンプレートエンジン**です。Laravelには、**Blade（ブレード）**という強力なテンプレートエンジンが標準で組み込まれています。

---

## 詳細解説

### 🔧 テンプレートエンジンとは？

テンプレートエンジンとは、HTMLの中にプログラムのコード（変数や制御構文）を埋め込み、動的にHTMLを生成する仕組みです。

**生のPHPでHTMLを生成する場合**

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
*   HTMLとPHPが混在し、デザイナーが編集しにくい

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
*   HTMLとロジックが分離され、デザイナーとエンジニアが協力しやすい

### 🎨 Bladeの基本構文

Bladeには、以下のような基本構文があります。

#### 1. 変数の出力

```blade
{{ $変数名 }}
```

`{{ }}`で囲むと、変数の値が出力されます。自動的にHTMLエスケープされるため、XSS攻撃を防ぐことができます。

```blade
<p>こんにちは、{{ $name }}さん！</p>
```

もし、HTMLエスケープをしたくない場合（信頼できるHTMLを出力する場合）は、`{!! !!}`を使います。

```blade
{!! $htmlContent !!}
```

**⚠️ 注意**: `{!! !!}`は、XSS攻撃のリスクがあるため、信頼できるデータにのみ使用してください。

#### 2. 制御構文

Bladeには、PHPの制御構文に対応する、読みやすいディレクティブが用意されています。

**条件分岐（`@if`, `@elseif`, `@else`）**

```blade
@if ($user->isAdmin())
    <p>管理者権限があります</p>
@elseif ($user->isModerator())
    <p>モデレーター権限があります</p>
@else
    <p>一般ユーザーです</p>
@endif
```

**ループ（`@foreach`, `@for`, `@while`）**

```blade
@foreach ($users as $user)
    <li>{{ $user->name }}</li>
@endforeach
```

**空の場合の処理（`@forelse`, `@empty`）**

```blade
@forelse ($users as $user)
    <li>{{ $user->name }}</li>
@empty
    <p>ユーザーが見つかりません</p>
@endforelse
```

#### 3. コメント

Bladeのコメントは、HTMLとして出力されません。

```blade
{{-- これはBladeのコメントです。HTMLには出力されません。 --}}
```

通常のHTMLコメント（`<!-- -->`）は、ブラウザのソースコードに表示されてしまうため、機密情報を書かないように注意してください。

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

## 💡 Bladeの学習について

このカリキュラムでは、Bladeの高度な機能（レイアウト継承、コンポーネント、スロットなど）は扱いません。まずは基本的な書き方を身につけ、**1ファイルにHTMLをベタ書きするシンプルな書き方**で十分です。

Bladeはシンプルに「データを表示する」ことに徹し、まずは基本をしっかり学びましょう。

---

## ✨ まとめ

このセクションでは、Bladeテンプレートエンジンの基本概念を学びました。

*   Bladeは、Laravelに標準で組み込まれたテンプレートエンジンで、HTMLに動的なデータを埋め込むための仕組みを提供する。
*   `{{ }}`で変数を出力し、`@if`, `@foreach`などのディレクティブで制御構文を書くことができる。
*   Bladeファイルは、`resources/views/`ディレクトリに`.blade.php`という拡張子で配置する。
*   まずはシンプルな書き方で基本を身につけることが大切。

次のセクションでは、Bladeの基本構文をより詳しく学び、実際に手を動かしてBladeファイルを作成していきます。

---
