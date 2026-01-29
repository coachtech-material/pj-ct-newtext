# Tutorial 13-1-6: 提供アセットの配置

## 🎯 このセクションで学ぶこと

- フロントエンドエンジニアから納品されたBladeファイルを配置する方法を学ぶ
- Tailwind CSSを使用したBladeテンプレートの構造を理解する
- 「提供コードありき」の開発フローを理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜGit/GitHub準備の次にアセット配置なのか？」

Git/GitHubの準備が終わったら、**開発を始める前に**フロントエンドのアセット（Bladeテンプレート）を配置します。

### 理由1: 「何を作るか」が視覚的にわかる

```
❌ 白紙からBladeを作る
→ 「どんな画面にすればいいんだろう？」と迷う
→ デザインを考えながらコードを書くので効率が悪い

✅ 先にBladeを配置する
→ 「この画面を動かせばいいんだ」と明確
→ バックエンド実装に集中できる
```

### 理由2: 実務の流れを再現

実務では、フロントエンドエンジニアが先にHTML/CSSを作り、バックエンドエンジニアがそれを動かします。この流れを練習します。

### 理由3: Bladeを読む力が身につく

「このBladeには`$books`という変数が必要だな」と読み取る力は、実務で必須です。

---

### このセクションの実装順序

| 順番 | 作業 | 理由 |
|:---:|:---|:---|
| 1 | ディレクトリ作成 | ファイルを置く場所を用意 |
| 2 | レイアウト配置 | 共通部分を先に配置 |
| 3 | コンポーネント配置 | 再利用部品を配置 |
| 4 | 各画面のBlade配置 | 個別画面を配置 |

---

## 導入：実務での開発フロー

実務では、**フロントエンドエンジニアとバックエンドエンジニアが分業**することが一般的です。

```
フロントエンドエンジニア: 画面のデザイン・HTML/CSS/JSを作成
バックエンドエンジニア: データベース・ロジック・APIを実装
```

このTutorialでは、**「フロントエンドエンジニアから成果物（Blade）が納品された」** という想定で開発を進めます。

---

## 💡 このTutorialの開発フロー

従来の「白紙から全部作る」アプローチではなく、以下のフローで進めます：

| ステップ | 内容 | 目的 |
|:---|:---|:---|
| 1 | 画面アクセス＆エラー確認 | 何が足りないかを把握する |
| 2 | Bladeの解読 | 必要な変数・リレーションを特定する |
| 3 | Tinker検証 | データ構造を確認する |
| 4 | バックエンド実装 | モデル・コントローラーを実装する |

---

## Step 1: 提供されるBladeファイル一覧

このTutorialでは、以下のBladeファイルが提供されます。すべて**Tailwind CSS**でスタイリングされています。

### レイアウト

| ファイル | 説明 |
|:---|:---|
| `layouts/app.blade.php` | 共通レイアウト |
| `components/navigation.blade.php` | ナビゲーションコンポーネント |

### 書籍関連

| ファイル | 説明 |
|:---|:---|
| `books/index.blade.php` | 書籍一覧画面 |
| `books/show.blade.php` | 書籍詳細画面 |
| `books/create.blade.php` | 書籍登録画面 |
| `books/edit.blade.php` | 書籍編集画面 |

### 認証関連

| ファイル | 説明 |
|:---|:---|
| `auth/login.blade.php` | ログイン画面 |
| `auth/register.blade.php` | ユーザー登録画面 |

---

## Step 2: Bladeファイルの配置

### 2-1. ディレクトリを作成する

```bash
mkdir -p resources/views/layouts
mkdir -p resources/views/components
mkdir -p resources/views/books
mkdir -p resources/views/auth
```

---

### 2-2. レイアウトファイルを配置する

**ファイル**: `resources/views/layouts/app.blade.php`

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="csrf-token" content="{{ csrf_token() }}">
    <title>{{ $title ?? '書籍レビューアプリ' }}</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="bg-gray-100 min-h-screen">
    <x-navigation />
    
    <main class="container mx-auto px-4 py-8 max-w-4xl">
        {{-- 成功メッセージ --}}
        @if(session('success'))
            <div class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
                {{ session('success') }}
            </div>
        @endif
        
        {{-- エラーメッセージ --}}
        @if(session('error'))
            <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
                {{ session('error') }}
            </div>
        @endif
        
        {{ $slot }}
    </main>
</body>
</html>
```

### レイアウトのコードリーディング

| コード | 説明 |
|:---|:---|
| `@vite([...])` | ViteでCSS/JSを読み込み |
| `<x-navigation />` | navigationコンポーネントを呼び出し |
| `{{ $slot }}` | 子コンポーネントの内容を表示 |
| `session('success')` | フラッシュメッセージを取得 |
| `bg-gray-100` | Tailwind: 背景色をグレーに |
| `container mx-auto` | Tailwind: 中央寄せのコンテナ |
| `px-4 py-8` | Tailwind: パディング（左右1rem、上下2rem） |

---

### 2-3. ナビゲーションコンポーネントを配置する

**ファイル**: `resources/views/components/navigation.blade.php`

```blade
<nav class="bg-gray-800 shadow-lg">
    <div class="container mx-auto px-4 max-w-4xl">
        <div class="flex justify-between items-center py-4">
            {{-- ロゴ --}}
            <a href="{{ route('books.index') }}" class="text-white text-xl font-bold hover:text-gray-300">
                📚 書籍レビューアプリ
            </a>
            
            {{-- ナビゲーションリンク --}}
            <div class="flex items-center space-x-4">
                @auth
                    <span class="text-gray-300">
                        {{ auth()->user()->name }}さん
                    </span>
                    <form action="{{ route('logout') }}" method="POST" class="inline">
                        @csrf
                        <button type="submit" class="text-gray-300 hover:text-white">
                            ログアウト
                        </button>
                    </form>
                @else
                    <a href="{{ route('login') }}" class="text-gray-300 hover:text-white">
                        ログイン
                    </a>
                    <a href="{{ route('register') }}" class="text-gray-300 hover:text-white">
                        新規登録
                    </a>
                @endauth
            </div>
        </div>
    </div>
</nav>
```

### ナビゲーションのコードリーディング

| コード | 説明 |
|:---|:---|
| `@auth ... @else ... @endauth` | ログイン状態で表示を切り替え |
| `auth()->user()->name` | ログインユーザーの名前を取得 |
| `route('logout')` | ログアウトルートのURLを生成 |
| `@csrf` | CSRFトークンを埋め込み |
| `flex justify-between` | Tailwind: 左右に配置 |
| `space-x-4` | Tailwind: 子要素間に余白 |

---

### 2-4. 書籍一覧画面を配置する

**ファイル**: `resources/views/books/index.blade.php`

```blade
<x-app-layout>
    <x-slot name="title">書籍一覧</x-slot>
    
    <div class="bg-white rounded-lg shadow-md p-6">
        {{-- ヘッダー --}}
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-2xl font-bold text-gray-800">書籍一覧</h1>
            <a href="{{ route('books.create') }}" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
                新規登録
            </a>
        </div>
        
        {{-- 書籍リスト --}}
        @forelse($books as $book)
            <div class="border-b border-gray-200 py-4 last:border-b-0">
                <div class="flex justify-between items-start">
                    <div>
                        <h2 class="text-lg font-semibold">
                            <a href="{{ route('books.show', $book) }}" class="text-gray-800 hover:text-blue-500">
                                {{ $book->title }}
                            </a>
                        </h2>
                        <p class="text-gray-600 text-sm mt-1">
                            著者: {{ $book->author }}
                        </p>
                        <div class="flex items-center mt-2">
                            {{-- 評価（星表示） --}}
                            <div class="text-yellow-400">
                                @for($i = 1; $i <= 5; $i++)
                                    @if($i <= $book->rating)
                                        ★
                                    @else
                                        ☆
                                    @endif
                                @endfor
                            </div>
                            <span class="text-gray-500 text-sm ml-2">
                                ({{ $book->rating }}/5)
                            </span>
                        </div>
                    </div>
                    <a href="{{ route('books.edit', $book) }}" class="bg-gray-500 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm">
                        編集
                    </a>
                </div>
            </div>
        @empty
            <p class="text-center text-gray-500 py-8">
                書籍がありません。「新規登録」ボタンから書籍を追加してください。
            </p>
        @endforelse
    </div>
</x-app-layout>
```

### 書籍一覧のコードリーディング

| コード | 説明 |
|:---|:---|
| `<x-app-layout>` | appレイアウトを使用 |
| `<x-slot name="title">` | レイアウトの$title変数に値を渡す |
| `@forelse($books as $book)` | $booksが空なら@empty以下を表示 |
| `route('books.show', $book)` | 書籍詳細ページのURLを生成 |
| `$book->title` | 書籍モデルのtitleプロパティにアクセス |
| `@for($i = 1; $i <= 5; $i++)` | 評価の星をループで表示 |

> 💡 **ポイント**: このBladeを動かすには、コントローラーから`$books`変数（Bookモデルのコレクション）を渡す必要があります。

---

### 2-5. 書籍詳細画面を配置する

**ファイル**: `resources/views/books/show.blade.php`

```blade
<x-app-layout>
    <x-slot name="title">{{ $book->title }}</x-slot>
    
    <div class="bg-white rounded-lg shadow-md p-6">
        {{-- ヘッダー --}}
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-2xl font-bold text-gray-800">{{ $book->title }}</h1>
            <a href="{{ route('books.index') }}" class="text-blue-500 hover:text-blue-600">
                ← 一覧に戻る
            </a>
        </div>
        
        {{-- 書籍情報 --}}
        <div class="space-y-4">
            <div>
                <span class="text-gray-500 text-sm">著者</span>
                <p class="text-gray-800">{{ $book->author }}</p>
            </div>
            
            <div>
                <span class="text-gray-500 text-sm">評価</span>
                <div class="flex items-center">
                    <div class="text-yellow-400 text-xl">
                        @for($i = 1; $i <= 5; $i++)
                            @if($i <= $book->rating)
                                ★
                            @else
                                ☆
                            @endif
                        @endfor
                    </div>
                    <span class="text-gray-500 ml-2">({{ $book->rating }}/5)</span>
                </div>
            </div>
            
            <div>
                <span class="text-gray-500 text-sm">レビュー</span>
                <p class="text-gray-800 whitespace-pre-wrap">{{ $book->review ?? 'レビューはありません' }}</p>
            </div>
            
            <div>
                <span class="text-gray-500 text-sm">登録日</span>
                <p class="text-gray-800">{{ $book->created_at->format('Y年m月d日') }}</p>
            </div>
        </div>
        
        {{-- アクションボタン --}}
        <div class="flex space-x-4 mt-8 pt-6 border-t border-gray-200">
            <a href="{{ route('books.edit', $book) }}" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
                編集
            </a>
            <form action="{{ route('books.destroy', $book) }}" method="POST" onsubmit="return confirm('本当に削除しますか？');">
                @csrf
                @method('DELETE')
                <button type="submit" class="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded">
                    削除
                </button>
            </form>
        </div>
    </div>
</x-app-layout>
```

### 書籍詳細のコードリーディング

| コード | 説明 |
|:---|:---|
| `$book->title` | 書籍モデルのタイトル |
| `$book->created_at->format('Y年m月d日')` | Carbonのフォーマットメソッドで日付整形 |
| `@method('DELETE')` | フォームでDELETEメソッドを使用 |
| `route('books.destroy', $book)` | 削除ルートのURLを生成 |
| `onsubmit="return confirm(...)"` | 削除前に確認ダイアログを表示 |
| `whitespace-pre-wrap` | Tailwind: 改行を保持して表示 |

> 💡 **ポイント**: このBladeを動かすには、コントローラーから`$book`変数（Bookモデルのインスタンス）を渡す必要があります。

---

### 2-6. 書籍登録画面を配置する

**ファイル**: `resources/views/books/create.blade.php`

```blade
<x-app-layout>
    <x-slot name="title">書籍登録</x-slot>
    
    <div class="bg-white rounded-lg shadow-md p-6">
        <h1 class="text-2xl font-bold text-gray-800 mb-6">書籍登録</h1>
        
        <form action="{{ route('books.store') }}" method="POST">
            @csrf
            
            {{-- タイトル --}}
            <div class="mb-4">
                <label for="title" class="block text-gray-700 font-medium mb-2">タイトル</label>
                <input type="text" name="title" id="title" value="{{ old('title') }}"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
                @error('title')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- 著者 --}}
            <div class="mb-4">
                <label for="author" class="block text-gray-700 font-medium mb-2">著者</label>
                <input type="text" name="author" id="author" value="{{ old('author') }}"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
                @error('author')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- 評価 --}}
            <div class="mb-4">
                <label for="rating" class="block text-gray-700 font-medium mb-2">評価</label>
                <select name="rating" id="rating"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
                    @for($i = 1; $i <= 5; $i++)
                        <option value="{{ $i }}" {{ old('rating') == $i ? 'selected' : '' }}>
                            {{ $i }} - {{ str_repeat('★', $i) }}{{ str_repeat('☆', 5 - $i) }}
                        </option>
                    @endfor
                </select>
                @error('rating')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- レビュー --}}
            <div class="mb-6">
                <label for="review" class="block text-gray-700 font-medium mb-2">レビュー</label>
                <textarea name="review" id="review" rows="5"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">{{ old('review') }}</textarea>
                @error('review')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- ボタン --}}
            <div class="flex space-x-4">
                <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
                    登録
                </button>
                <a href="{{ route('books.index') }}" class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded">
                    キャンセル
                </a>
            </div>
        </form>
    </div>
</x-app-layout>
```

### 書籍登録のコードリーディング

| コード | 説明 |
|:---|:---|
| `route('books.store')` | 書籍保存ルートのURLを生成 |
| `old('title')` | バリデーションエラー時に入力値を復元 |
| `@error('title') ... @enderror` | titleフィールドのエラーメッセージを表示 |
| `{{ $message }}` | エラーメッセージの内容 |
| `str_repeat('★', $i)` | 星を$i回繰り返して表示 |
| `focus:border-blue-500` | Tailwind: フォーカス時に枠線を青に |

> 💡 **ポイント**: このBladeはコントローラーから変数を渡す必要はありません。フォーム送信先の`store`メソッドを実装すれば動きます。

---

### 2-7. 書籍編集画面を配置する

**ファイル**: `resources/views/books/edit.blade.php`

```blade
<x-app-layout>
    <x-slot name="title">書籍編集</x-slot>
    
    <div class="bg-white rounded-lg shadow-md p-6">
        <h1 class="text-2xl font-bold text-gray-800 mb-6">書籍編集</h1>
        
        <form action="{{ route('books.update', $book) }}" method="POST">
            @csrf
            @method('PUT')
            
            {{-- タイトル --}}
            <div class="mb-4">
                <label for="title" class="block text-gray-700 font-medium mb-2">タイトル</label>
                <input type="text" name="title" id="title" value="{{ old('title', $book->title) }}"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
                @error('title')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- 著者 --}}
            <div class="mb-4">
                <label for="author" class="block text-gray-700 font-medium mb-2">著者</label>
                <input type="text" name="author" id="author" value="{{ old('author', $book->author) }}"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
                @error('author')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- 評価 --}}
            <div class="mb-4">
                <label for="rating" class="block text-gray-700 font-medium mb-2">評価</label>
                <select name="rating" id="rating"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
                    @for($i = 1; $i <= 5; $i++)
                        <option value="{{ $i }}" {{ old('rating', $book->rating) == $i ? 'selected' : '' }}>
                            {{ $i }} - {{ str_repeat('★', $i) }}{{ str_repeat('☆', 5 - $i) }}
                        </option>
                    @endfor
                </select>
                @error('rating')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- レビュー --}}
            <div class="mb-6">
                <label for="review" class="block text-gray-700 font-medium mb-2">レビュー</label>
                <textarea name="review" id="review" rows="5"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">{{ old('review', $book->review) }}</textarea>
                @error('review')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- ボタン --}}
            <div class="flex space-x-4">
                <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded">
                    更新
                </button>
                <a href="{{ route('books.show', $book) }}" class="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded">
                    キャンセル
                </a>
            </div>
        </form>
    </div>
</x-app-layout>
```

### 書籍編集のコードリーディング

| コード | 説明 |
|:---|:---|
| `route('books.update', $book)` | 書籍更新ルートのURLを生成 |
| `@method('PUT')` | フォームでPUTメソッドを使用 |
| `old('title', $book->title)` | エラー時はold値、なければ$bookの値を表示 |
| `old('rating', $book->rating) == $i` | 現在の評価値を選択状態に |

> 💡 **ポイント**: このBladeを動かすには、コントローラーから`$book`変数（Bookモデルのインスタンス）を渡す必要があります。

---

## Step 3: 認証関連のBladeファイル

認証関連のBladeファイルは、Chapter 4（認証とパーソナライズ）で配置します。

---

## 🚨 よくある間違い

### 間違い1: Tailwindのスタイルが適用されない

**対処法**: `sail npm run dev`が実行されているか確認します。

```bash
# 別のターミナルで実行
sail npm run dev
```

---

### 間違い2: コンポーネントが見つからないエラー

**エラー例**:
```
Unable to locate a class or view for component [navigation]
```

**対処法**: `resources/views/components/navigation.blade.php`が正しい場所に配置されているか確認します。

---

## ✨ まとめ

このセクションでは、提供アセットの配置について学びました。

- Tailwind CSSを使用したBladeテンプレートを配置した
- レイアウト、コンポーネント、各画面のBladeファイルを理解した
- 実務での「提供コードありき」の開発フローを理解した

次のChapterでは、書籍レビュー機能（CRUD）の実装に進みます。

---
