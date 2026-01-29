# Tutorial 9-2-4: Bladeファイルの読み解き方（レイアウトとコンポーネント）

## 🎯 このセクションで学ぶこと

*   `@extends`, `@section`によるレイアウト継承の仕組みを理解する。
*   **コンポーネントの「読み方」**を身につける：
    *   `<x-app-layout>`が`resources/views/components/app-layout.blade.php`を指していること。
    *   `<x-slot name="header">`がレイアウト側の`{{ $header }}`に差し込まれること。
*   他人が作ったBladeファイルを読み解き、データを正しく渡せるようになる。

---

## 導入：「作る」より「読む」スキル

実際の開発現場では、Bladeのレイアウトやコンポーネントを**ゼロから自作する**ことは少なく、**既存のものを読み解いて使う**ことが多いです。

例えば、以下のようなケースがあります。

*   フロントエンドエンジニアが作成したBladeファイルを受け取る
*   Laravel Breezeなどのスターターキットが生成したファイルを使う
*   既存プロジェクトのコードを引き継ぐ

このセクションでは、**「自分で作る」のではなく「他人が作ったものをどう使うか」**に焦点を当てて、レイアウトとコンポーネントの読み方を学びます。

---

## 詳細解説

### 📐 レイアウト継承：`@extends`と`@section`

#### レイアウトとは？

Webサイトでは、ヘッダー、フッター、ナビゲーションなど、**全ページで共通の部分**があります。これらを毎回書くのは非効率なので、**レイアウトファイル**として共通部分をまとめます。

```
resources/views/
├── layouts/
│   └── app.blade.php      ← レイアウトファイル（共通部分）
└── users/
    └── index.blade.php    ← 子ビュー（個別のコンテンツ）
```

#### レイアウトファイルの例

**`resources/views/layouts/app.blade.php`**

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>@yield('title', 'My App')</title>
</head>
<body>
    <header>
        <h1>My Application</h1>
        <nav>
            <a href="/">ホーム</a>
            <a href="/users">ユーザー</a>
        </nav>
    </header>

    <main>
        @yield('content')
    </main>

    <footer>
        <p>&copy; 2024 My Application</p>
    </footer>
</body>
</html>
```

**読み解きポイント**

*   `@yield('title', 'My App')`: 子ビューから`title`セクションが渡されればそれを表示、なければ`'My App'`を表示。
*   `@yield('content')`: 子ビューから`content`セクションが渡される場所。

#### 子ビューでレイアウトを継承する

**`resources/views/users/index.blade.php`**

```blade
@extends('layouts.app')

@section('title', 'ユーザー一覧')

@section('content')
    <h2>ユーザー一覧</h2>
    
    @forelse ($users as $user)
        <p>{{ $user->name }}</p>
    @empty
        <p>ユーザーがいません</p>
    @endforelse
@endsection
```

**読み解きポイント**

*   `@extends('layouts.app')`: `resources/views/layouts/app.blade.php`を継承する。
*   `@section('title', 'ユーザー一覧')`: レイアウトの`@yield('title')`に`'ユーザー一覧'`を渡す。
*   `@section('content') ... @endsection`: レイアウトの`@yield('content')`にこの内容を渡す。

#### 継承の仕組み（図解）

```
レイアウト（layouts/app.blade.php）
┌─────────────────────────────────┐
│ <head>                          │
│   <title>@yield('title')</title>│  ← 'ユーザー一覧' が入る
│ </head>                         │
│ <body>                          │
│   <header>...</header>          │
│   <main>                        │
│     @yield('content')           │  ← 子ビューの内容が入る
│   </main>                       │
│   <footer>...</footer>          │
│ </body>                         │
└─────────────────────────────────┘
          ↑
          │ @extends で継承
          │
子ビュー（users/index.blade.php）
┌─────────────────────────────────┐
│ @section('title', 'ユーザー一覧')│
│ @section('content')             │
│   <h2>ユーザー一覧</h2>          │
│   ...                           │
│ @endsection                     │
└─────────────────────────────────┘
```

---

### 🧩 Bladeコンポーネント：`<x-component-name>`

#### コンポーネントとは？

コンポーネントは、**再利用可能なBladeの部品**です。ボタン、カード、アラートなど、よく使うUIパーツをコンポーネントとして定義します。

```
resources/views/
└── components/
    ├── app-layout.blade.php    ← レイアウトコンポーネント
    ├── button.blade.php        ← ボタンコンポーネント
    └── alert.blade.php         ← アラートコンポーネント
```

#### コンポーネントの呼び出し方

コンポーネントは、`<x-コンポーネント名>`という形式で呼び出します。

```blade
<x-button>送信</x-button>
```

これは、`resources/views/components/button.blade.php`を読み込みます。

**ファイル名とタグ名の対応**

| ファイルパス | 呼び出し方 |
|:---|:---|
| `components/button.blade.php` | `<x-button>` |
| `components/alert.blade.php` | `<x-alert>` |
| `components/app-layout.blade.php` | `<x-app-layout>` |
| `components/forms/input.blade.php` | `<x-forms.input>` |

> 💡 **ポイント**: ファイル名のハイフン（`-`）は、そのままハイフンで呼び出します。ディレクトリの区切りはドット（`.`）で表現します。

---

### 📖 コンポーネントの「読み方」

#### 例：Laravel Breezeのレイアウトコンポーネント

Laravel Breezeなどのスターターキットを使うと、以下のようなコンポーネントが生成されます。

**`resources/views/components/app-layout.blade.php`**

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{{ $title ?? 'My App' }}</title>
</head>
<body>
    <header>
        {{ $header }}
    </header>

    <main>
        {{ $slot }}
    </main>
</body>
</html>
```

**読み解きポイント**

*   `{{ $title ?? 'My App' }}`: `$title`が渡されればそれを表示、なければ`'My App'`を表示。
*   `{{ $header }}`: 名前付きスロット`header`の内容が入る。
*   `{{ $slot }}`: デフォルトスロット（タグの間の内容）が入る。

#### コンポーネントを使う側

```blade
<x-app-layout>
    <x-slot name="title">ユーザー一覧</x-slot>
    
    <x-slot name="header">
        <h1>ユーザー管理</h1>
    </x-slot>

    {{-- ここがデフォルトスロット（$slot）に入る --}}
    <h2>ユーザー一覧</h2>
    @forelse ($users as $user)
        <p>{{ $user->name }}</p>
    @empty
        <p>ユーザーがいません</p>
    @endforelse
</x-app-layout>
```

**読み解きポイント**

*   `<x-app-layout>`: `components/app-layout.blade.php`を呼び出す。
*   `<x-slot name="title">`: コンポーネント内の`{{ $title }}`に渡す。
*   `<x-slot name="header">`: コンポーネント内の`{{ $header }}`に渡す。
*   タグの間の内容: コンポーネント内の`{{ $slot }}`に渡す。

#### スロットの仕組み（図解）

```
コンポーネント（components/app-layout.blade.php）
┌─────────────────────────────────┐
│ <title>{{ $title }}</title>     │  ← 'ユーザー一覧' が入る
│ <header>{{ $header }}</header>  │  ← <h1>ユーザー管理</h1> が入る
│ <main>{{ $slot }}</main>        │  ← 残りの内容が入る
└─────────────────────────────────┘
          ↑
          │
使う側
┌─────────────────────────────────┐
│ <x-app-layout>                  │
│   <x-slot name="title">         │
│     ユーザー一覧                 │
│   </x-slot>                     │
│   <x-slot name="header">        │
│     <h1>ユーザー管理</h1>        │
│   </x-slot>                     │
│   <h2>ユーザー一覧</h2>          │  ← これが $slot に入る
│   ...                           │
│ </x-app-layout>                 │
└─────────────────────────────────┘
```

---

### 🔍 既存のBladeファイルを読み解く手順

他人が作ったBladeファイルを読み解く際は、以下の手順で進めます。

#### ステップ1: 使われているコンポーネントを特定する

```blade
<x-app-layout>
```

→ `resources/views/components/app-layout.blade.php`を確認する。

#### ステップ2: コンポーネント内の変数を確認する

コンポーネントファイルを開いて、以下を確認します。

*   `{{ $slot }}`: デフォルトスロット
*   `{{ $header }}`: 名前付きスロット
*   `{{ $title ?? 'デフォルト値' }}`: 属性として渡す値

#### ステップ3: 必要なデータを渡す

コンポーネントが期待するデータを、コントローラーから渡します。

```php
return view('users.index', compact('users'));
```

#### ステップ4: デバッグで確認する

データが正しく渡されているか、`@dd()`で確認します。

```blade
<x-app-layout>
    @dd($users)  {{-- デバッグ用 --}}
    ...
</x-app-layout>
```

---

### 💡 よくあるパターン

#### パターン1: 属性としてデータを渡す

```blade
<x-alert type="success" message="保存しました" />
```

コンポーネント側:

```blade
<div class="alert alert-{{ $type }}">
    {{ $message }}
</div>
```

#### パターン2: 動的な属性

```blade
<x-button :disabled="$isSubmitting">送信</x-button>
```

`:属性名`で、PHPの変数を渡せます。

#### パターン3: クラスのマージ

```blade
<x-button class="mt-4">送信</x-button>
```

コンポーネント側で`{{ $attributes }}`を使うと、渡された属性がマージされます。

---

## ✨ まとめ

このセクションでは、Bladeファイルの読み解き方を学びました。

*   **レイアウト継承**: `@extends`でレイアウトを継承し、`@section`でコンテンツを渡す。`@yield`で受け取る。
*   **コンポーネント**: `<x-component-name>`で呼び出し、`resources/views/components/`以下のファイルを読み込む。
*   **スロット**: `{{ $slot }}`はデフォルトスロット、`{{ $header }}`などは名前付きスロット。`<x-slot name="header">`で渡す。
*   **読み解く手順**: コンポーネントを特定 → 変数を確認 → データを渡す → デバッグで確認。

**重要**: このカリキュラムでは、コンポーネントを「自作する」スキルは不要です。**「他人が作ったものをどう使うか」**を理解することが重要です。

次のセクションでは、ハンズオン演習として、提供されたBladeファイルを読み解き、コントローラーから適切なデータを渡す練習をします。

---
