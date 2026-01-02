# Tutorial 9-2-2: Bladeの基本構文

## 🎯 このセクションで学ぶこと

*   Bladeの変数展開、制御構文（@if、@foreach）を実際に使えるようになる。
*   コントローラーからビューにデータを渡し、Bladeで表示できるようになる。
*   Bladeの便利な機能（@forelse、@isset、@emptyなど）を使いこなせるようになる。

---

## 導入：実際に手を動かしてBladeを学ぶ

前のセクションで、Bladeテンプレートエンジンの概念と、このカリキュラムにおける位置づけを学びました。このセクションでは、実際にBladeファイルを作成し、コントローラーからデータを渡して表示する方法を、手を動かしながら学んでいきます。

Bladeの構文は非常にシンプルで、一度覚えてしまえば、直感的にHTMLを生成できるようになります。

---

## 詳細解説

### 🏃 実践：ユーザー一覧を表示する

まず、シンプルなユーザー一覧ページを作成してみましょう。

#### ステップ1: ルーティングを定義する

`routes/web.php`に、以下のルートを追加します。

```php
<?php
use App\Http\Controllers\UserController;

Route::get('/users', [UserController::class, 'index']);
```

#### ステップ2: コントローラーを作成する

`app/Http/Controllers/UserController.php`を作成します（まだ存在しない場合）。

```bash
docker compose exec php php artisan make:controller UserController
```

コントローラーに、以下のコードを追加します。

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

#### ステップ3: ビューを作成する

`resources/views/users/index.blade.php`を作成します。まず、ディレクトリを作成します。

```bash
mkdir -p resources/views/users
```

次に、`resources/views/users/index.blade.php`を作成し、以下の内容を記述します。

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ユーザー一覧</title>
</head>
<body>
    <h1>ユーザー一覧</h1>

    <ul>
        @foreach ($users as $user)
            <li>
                <strong>{{ $user->name }}</strong> ({{ $user->email }})
            </li>
        @endforeach
    </ul>
</body>
</html>
```

**コードリーディング**

*   `@foreach ($users as $user)`: コントローラーから渡された`$users`配列をループします。
*   `{{ $user->name }}`: `$user`オブジェクトの`name`プロパティを出力します。`{{ }}`は自動的にHTMLエスケープを行います。
*   `@endforeach`: ループの終了を示します。

#### ステップ4: ブラウザで確認する

ブラウザで`http://localhost:8080/users`にアクセスすると、データベースに登録されているユーザーの一覧が表示されます。

**[ここに、ユーザー一覧画面のスクリーンショットを挿入]**

---

### 🔀 条件分岐（@if、@elseif、@else）

Bladeでは、`@if`ディレクティブを使って条件分岐を行うことができます。

**例：ユーザーが管理者かどうかで表示を変える**

```blade
@foreach ($users as $user)
    <li>
        {{ $user->name }}
        @if ($user->is_admin)
            <span style="color: red;">（管理者）</span>
        @else
            <span style="color: gray;">（一般ユーザー）</span>
        @endif
    </li>
@endforeach
```

**複数の条件を扱う場合**

```blade
@if ($user->role === 'admin')
    <span>管理者</span>
@elseif ($user->role === 'moderator')
    <span>モデレーター</span>
@else
    <span>一般ユーザー</span>
@endif
```

### 🔍 便利なディレクティブ

Bladeには、よくあるパターンを簡潔に書くための便利なディレクティブが用意されています。

#### 1. `@forelse` - 空の場合の処理

配列が空の場合に、特別なメッセージを表示したい場合は、`@forelse`と`@empty`を使います。

```blade
<ul>
    @forelse ($users as $user)
        <li>{{ $user->name }}</li>
    @empty
        <li>ユーザーが見つかりません</li>
    @endforelse
</ul>
```

これは、以下のコードと同じ意味です。

```blade
@if (count($users) > 0)
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }}</li>
        @endforeach
    </ul>
@else
    <p>ユーザーが見つかりません</p>
@endif
```

`@forelse`を使うことで、コードが簡潔になります。

#### 2. `@isset` - 変数が存在するかチェック

変数が存在するかどうかをチェックする場合は、`@isset`を使います。

```blade
@isset($user)
    <p>ユーザー名: {{ $user->name }}</p>
@endisset
```

これは、`isset($user)`と同じ意味です。

#### 3. `@empty` - 変数が空かチェック

変数が空（`null`, `false`, `''`, `[]`など）かどうかをチェックする場合は、`@empty`を使います。

```blade
@empty($users)
    <p>ユーザーが見つかりません</p>
@endempty
```

#### 4. `@auth` と `@guest` - 認証状態のチェック

ユーザーがログインしているかどうかをチェックする場合は、`@auth`と`@guest`を使います。

```blade
@auth
    <p>こんにちは、{{ auth()->user()->name }}さん！</p>
@endauth

@guest
    <p><a href="/login">ログインしてください</a></p>
@endguest
```

これらは、認証機能を実装した後に使います。

### 🔢 ループ内の便利な変数（$loop）

`@foreach`や`@for`の中では、`$loop`という特別な変数が使えます。これは、ループの状態を表す情報を持っています。

| プロパティ | 説明 |
|:---|:---|
| `$loop->index` | 現在のインデックス（0から始まる） |
| `$loop->iteration` | 現在の繰り返し回数（1から始まる） |
| `$loop->first` | 最初のループかどうか（boolean） |
| `$loop->last` | 最後のループかどうか（boolean） |
| `$loop->count` | ループ対象の要素数 |
| `$loop->remaining` | 残りのループ回数 |

**例：最初と最後の要素に特別なスタイルを適用する**

```blade
<ul>
    @foreach ($users as $user)
        <li style="
            @if ($loop->first) font-weight: bold; @endif
            @if ($loop->last) color: red; @endif
        ">
            {{ $loop->iteration }}. {{ $user->name }}
        </li>
    @endforeach
</ul>
```

**実行結果のイメージ**

```
1. 山田太郎（太字）
2. 鈴木花子
3. 佐藤次郎（赤字）
```

### 📝 コメント

Bladeには、HTMLとして出力されないコメントを書くことができます。

```blade
{{-- これはBladeのコメントです。HTMLには出力されません。 --}}

<!-- これはHTMLのコメントです。ブラウザのソースコードに表示されます。 -->
```

機密情報や開発メモは、Bladeのコメント（`{{-- --}}`）を使いましょう。

### 🔗 URLの生成

Bladeでは、名前付きルートを使ってURLを生成できます。

```blade
<a href="{{ route('users.show', ['id' => $user->id]) }}">
    {{ $user->name }}
</a>
```

これにより、ルート定義が変更されても、ビューを修正する必要がなくなります。

---

## 💡 TIP: Bladeはキャッシュされる

Bladeファイルは、初回アクセス時にPHPコードにコンパイルされ、`storage/framework/views/`にキャッシュされます。そのため、2回目以降のアクセスは高速です。

もし、Bladeファイルを編集したのに変更が反映されない場合は、以下のコマンドでキャッシュをクリアしてください。

```bash
docker compose exec php php artisan view:clear
```

---

## ✨ まとめ

このセクションでは、Bladeの基本構文を実際に使いながら学びました。

*   `{{ }}`で変数を出力し、自動的にHTMLエスケープされる。
*   `@foreach`, `@if`, `@elseif`, `@else`などのディレクティブで、制御構文を書くことができる。
*   `@forelse`を使うと、配列が空の場合の処理を簡潔に書ける。
*   `@isset`, `@empty`, `@auth`, `@guest`などの便利なディレクティブがある。
*   `$loop`変数を使うと、ループ内で現在の状態を取得できる。
*   `route()`ヘルパーを使って、名前付きルートからURLを生成できる。

次のセクションでは、BladeでAPIレスポンスを可視化する実践的な方法を学びます。

---
