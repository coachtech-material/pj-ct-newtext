# Tutorial 9-2-2: 制御構文とデータの展開

## 🎯 このセクションで学ぶこと

*   コレクションの展開：`@foreach`を使ってデータをループ表示できるようになる。
*   防御的プログラミング：`@if`、`@isset`、特に**`@forelse`**（データが0件の時の表示）を使いこなせるようになる。
*   `$loop`変数を使って、ループ内の状態を取得できるようになる。

---

## 導入：データを「安全に」表示する

前のセクションで、Bladeの基本的な変数出力を学びました。しかし、実際のアプリケーションでは、単に変数を表示するだけでなく、**条件によって表示を変えたり**、**配列やコレクションをループして表示したり**する必要があります。

また、データが存在しない場合（0件の場合）にも、適切なメッセージを表示する**防御的プログラミング**が重要です。「データがありません」と表示するか、何も表示しないかで、ユーザー体験は大きく変わります。

---

## 詳細解説

### 🔄 コレクションの展開：`@foreach`

データベースから取得したデータ（コレクション）をループして表示するには、`@foreach`を使います。

```blade
<ul>
    @foreach ($users as $user)
        <li>{{ $user->name }} ({{ $user->email }})</li>
    @endforeach
</ul>
```

**コードリーディング**

*   `@foreach ($users as $user)`: `$users`コレクションをループし、各要素を`$user`として取り出します。
*   `{{ $user->name }}`: 各ユーザーの名前を出力します。
*   `@endforeach`: ループの終了を示します。

---

### 🛡️ 防御的プログラミング：`@forelse`（推奨）

**`@forelse`は、データが0件の場合の表示を簡潔に書ける、非常に便利なディレクティブです。**

実際のアプリケーションでは、データが0件の場合も考慮する必要があります。例えば、検索結果が0件の場合、「検索結果がありません」と表示するのが親切です。

#### `@forelse`を使う場合（推奨）

```blade
<ul>
    @forelse ($users as $user)
        <li>{{ $user->name }}</li>
    @empty
        <li>ユーザーが見つかりません</li>
    @endforelse
</ul>
```

**コードリーディング**

*   `@forelse ($users as $user)`: `$users`が空でなければループします。
*   `@empty`: `$users`が空の場合に実行されます。
*   `@endforelse`: ループの終了を示します。

#### `@foreach`と`@if`を使う場合（冗長）

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

`@forelse`を使うことで、コードが簡潔になります。**データをループ表示する場合は、`@forelse`を使うことを推奨します。**

---

### 🔀 条件分岐：`@if`、`@elseif`、`@else`

条件によって表示を変える場合は、`@if`を使います。

```blade
@if ($user->is_admin)
    <span style="color: red;">管理者</span>
@elseif ($user->is_moderator)
    <span style="color: blue;">モデレーター</span>
@else
    <span style="color: gray;">一般ユーザー</span>
@endif
```

**コードリーディング**

*   `@if ($user->is_admin)`: `$user->is_admin`がtrueの場合に実行されます。
*   `@elseif ($user->is_moderator)`: 最初の条件がfalseで、この条件がtrueの場合に実行されます。
*   `@else`: どの条件にも当てはまらない場合に実行されます。
*   `@endif`: 条件分岐の終了を示します。

---

### 🔍 変数の存在チェック：`@isset`

変数が存在するかどうかをチェックする場合は、`@isset`を使います。

```blade
@isset($user)
    <p>ユーザー名: {{ $user->name }}</p>
@endisset
```

これは、PHPの`isset($user)`と同じ意味です。変数が定義されていない場合、このブロックは実行されません。

#### `@unless` - 条件が偽の場合に実行

```blade
@unless ($user->is_admin)
    <p>管理者権限がありません</p>
@endunless
```

`@unless`は、`@if (!条件)`と同じ意味です。条件が偽の場合に実行されます。

---

### 🔢 ループ内の便利な変数：`$loop`

`@foreach`や`@forelse`の中では、`$loop`という特別な変数が使えます。これは、ループの状態を表す情報を持っています。

| プロパティ | 説明 |
|:---|:---|
| `$loop->index` | 現在のインデックス（0から始まる） |
| `$loop->iteration` | 現在の繰り返し回数（1から始まる） |
| `$loop->first` | 最初のループかどうか（boolean） |
| `$loop->last` | 最後のループかどうか（boolean） |
| `$loop->count` | ループ対象の要素数 |
| `$loop->remaining` | 残りのループ回数 |

#### 実践例：番号付きリストと最後の要素の強調

```blade
<ul>
    @forelse ($users as $user)
        <li>
            {{ $loop->iteration }}. {{ $user->name }}
            @if ($loop->first)
                <span style="color: green;">（最初）</span>
            @endif
            @if ($loop->last)
                <span style="color: red;">（最後）</span>
            @endif
        </li>
    @empty
        <li>ユーザーが見つかりません</li>
    @endforelse
</ul>
```

**実行結果のイメージ**

```
1. 山田太郎（最初）
2. 鈴木花子
3. 佐藤次郎（最後）
```

---

### 🔗 URLの生成

Bladeでは、名前付きルートを使ってURLを生成できます。

```blade
<a href="{{ route('users.show', ['user' => $user->id]) }}">
    {{ $user->name }}
</a>
```

これにより、ルート定義が変更されても、ビューを修正する必要がなくなります。

---

### 🏃 実践例：ユーザー一覧ページ

コントローラーとBladeを組み合わせた実践例を見てみましょう。

#### コントローラー

```php
public function index()
{
    $users = User::all();
    return view('users.index', compact('users'));
}
```

#### Blade（`resources/views/users/index.blade.php`）

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ユーザー一覧</title>
</head>
<body>
    <h1>ユーザー一覧</h1>

    <table border="1">
        <thead>
            <tr>
                <th>No.</th>
                <th>名前</th>
                <th>メールアドレス</th>
                <th>権限</th>
            </tr>
        </thead>
        <tbody>
            @forelse ($users as $user)
                <tr>
                    <td>{{ $loop->iteration }}</td>
                    <td>{{ $user->name }}</td>
                    <td>{{ $user->email }}</td>
                    <td>
                        @if ($user->is_admin)
                            <span style="color: red;">管理者</span>
                        @else
                            一般ユーザー
                        @endif
                    </td>
                </tr>
            @empty
                <tr>
                    <td colspan="4">ユーザーが登録されていません</td>
                </tr>
            @endforelse
        </tbody>
    </table>

    <p>全{{ $users->count() }}件</p>
</body>
</html>
```

**コードリーディング**

*   `@forelse ($users as $user)`: ユーザーが存在すればループ、存在しなければ`@empty`ブロックを実行。
*   `$loop->iteration`: 1から始まる番号を表示。
*   `@if ($user->is_admin)`: 管理者かどうかで表示を変更。
*   `$users->count()`: コレクションの件数を表示。

---

### 💡 TIP: 認証状態のチェック

ユーザーがログインしているかどうかをチェックする場合は、`@auth`と`@guest`を使います。

```blade
@auth
    <p>こんにちは、{{ auth()->user()->name }}さん！</p>
    <a href="{{ route('logout') }}">ログアウト</a>
@endauth

@guest
    <p><a href="{{ route('login') }}">ログインしてください</a></p>
@endguest
```

これらは、認証機能を実装した後に使います。

---

## ✨ まとめ

このセクションでは、Bladeの制御構文を学びました。

*   **`@foreach`**: コレクションをループして表示する。
*   **`@forelse`（推奨）**: データが0件の場合の表示を簡潔に書ける。防御的プログラミングに最適。
*   **`@if`、`@elseif`、`@else`**: 条件によって表示を変える。
*   **`@isset`**: 変数が存在するかどうかをチェックする。
*   **`$loop`変数**: ループ内で現在の状態（番号、最初/最後など）を取得できる。

**重要**: データをループ表示する場合は、`@forelse`を使って、0件の場合の表示も必ず実装しましょう。

次のセクションでは、フォームとデータ送信について学びます。

---
