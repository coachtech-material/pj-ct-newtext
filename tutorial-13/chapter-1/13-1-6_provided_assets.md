# Tutorial 13-1-6: 提供アセットの配置

## 🎯 このセクションで学ぶこと

*   フロントエンドエンジニアから納品されたBladeファイルを配置する方法を学ぶ。
*   提供されたアセット（CSS、JavaScript）をプロジェクトに組み込む方法を理解する。
*   「提供コードありき」の開発フローを理解する。

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

このフローにより、**「データが取れていないのに画面を作っても動かない」** という問題を防げます。

---

## Step 1: 提供されるBladeファイル一覧

このTutorialでは、以下のBladeファイルが提供されます。

### レイアウト

| ファイル | 説明 |
|:---|:---|
| `layouts/app.blade.php` | 共通レイアウト |
| `components/navigation.blade.php` | ナビゲーションコンポーネント |

### タスク関連

| ファイル | 説明 |
|:---|:---|
| `tasks/index.blade.php` | タスク一覧画面 |
| `tasks/show.blade.php` | タスク詳細画面 |
| `tasks/create.blade.php` | タスク作成画面 |
| `tasks/edit.blade.php` | タスク編集画面 |

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
mkdir -p resources/views/tasks
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
    <title>{{ $title ?? 'タスク管理システム' }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Noto Sans JP', sans-serif;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.6;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .card {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            padding: 20px;
            margin-bottom: 20px;
        }
        .btn {
            display: inline-block;
            padding: 10px 20px;
            border-radius: 4px;
            text-decoration: none;
            cursor: pointer;
            border: none;
            font-size: 14px;
        }
        .btn-primary {
            background-color: #3490dc;
            color: white;
        }
        .btn-primary:hover {
            background-color: #2779bd;
        }
        .btn-danger {
            background-color: #e3342f;
            color: white;
        }
        .btn-danger:hover {
            background-color: #cc1f1a;
        }
        .btn-secondary {
            background-color: #6c757d;
            color: white;
        }
        .form-group {
            margin-bottom: 15px;
        }
        .form-group label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        .form-control {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        .form-control:focus {
            outline: none;
            border-color: #3490dc;
        }
        .error {
            color: #e3342f;
            font-size: 12px;
            margin-top: 5px;
        }
        .alert {
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        .status-pending { color: #ffc107; }
        .status-in_progress { color: #17a2b8; }
        .status-completed { color: #28a745; }
    </style>
</head>
<body>
    <x-navigation />
    
    <main class="container">
        @if(session('success'))
            <div class="alert alert-success">
                {{ session('success') }}
            </div>
        @endif
        
        @if(session('error'))
            <div class="alert alert-danger">
                {{ session('error') }}
            </div>
        @endif
        
        {{ $slot }}
    </main>
</body>
</html>
```

---

### 2-3. ナビゲーションコンポーネントを配置する

**ファイル**: `resources/views/components/navigation.blade.php`

```blade
<nav style="background-color: #343a40; padding: 15px 0;">
    <div class="container" style="display: flex; justify-content: space-between; align-items: center;">
        <a href="{{ route('tasks.index') }}" style="color: white; text-decoration: none; font-size: 20px; font-weight: bold;">
            タスク管理システム
        </a>
        
        <div>
            @auth
                <span style="color: #adb5bd; margin-right: 15px;">
                    {{ auth()->user()->name }}さん
                </span>
                <form action="{{ route('logout') }}" method="POST" style="display: inline;">
                    @csrf
                    <button type="submit" style="background: none; border: none; color: #adb5bd; cursor: pointer;">
                        ログアウト
                    </button>
                </form>
            @else
                <a href="{{ route('login') }}" style="color: #adb5bd; margin-right: 15px; text-decoration: none;">
                    ログイン
                </a>
                <a href="{{ route('register') }}" style="color: #adb5bd; text-decoration: none;">
                    新規登録
                </a>
            @endauth
        </div>
    </div>
</nav>
```

---

### 2-4. タスク一覧画面を配置する

**ファイル**: `resources/views/tasks/index.blade.php`

```blade
<x-app-layout>
    <x-slot name="title">タスク一覧</x-slot>
    
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h1>タスク一覧</h1>
            <a href="{{ route('tasks.create') }}" class="btn btn-primary">新規作成</a>
        </div>
        
        {{-- 検索フォーム --}}
        <form action="{{ route('tasks.index') }}" method="GET" style="margin-bottom: 20px;">
            <div style="display: flex; gap: 10px;">
                <input type="text" name="keyword" class="form-control" placeholder="キーワード検索" value="{{ request('keyword') }}" style="flex: 1;">
                <select name="status" class="form-control" style="width: 150px;">
                    <option value="">全てのステータス</option>
                    <option value="pending" {{ request('status') === 'pending' ? 'selected' : '' }}>未着手</option>
                    <option value="in_progress" {{ request('status') === 'in_progress' ? 'selected' : '' }}>進行中</option>
                    <option value="completed" {{ request('status') === 'completed' ? 'selected' : '' }}>完了</option>
                </select>
                <select name="category_id" class="form-control" style="width: 150px;">
                    <option value="">全てのカテゴリー</option>
                    @foreach($categories as $category)
                        <option value="{{ $category->id }}" {{ request('category_id') == $category->id ? 'selected' : '' }}>
                            {{ $category->name }}
                        </option>
                    @endforeach
                </select>
                <button type="submit" class="btn btn-primary">検索</button>
            </div>
        </form>
        
        @forelse($tasks as $task)
            <div class="card" style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3>
                        <a href="{{ route('tasks.show', $task) }}" style="text-decoration: none; color: #333;">
                            {{ $task->title }}
                        </a>
                    </h3>
                    <p style="color: #6c757d; font-size: 14px;">
                        <span class="status-{{ $task->status }}">
                            @if($task->status === 'pending') 未着手
                            @elseif($task->status === 'in_progress') 進行中
                            @else 完了
                            @endif
                        </span>
                        @if($task->category)
                            | カテゴリー: {{ $task->category->name }}
                        @endif
                        @if($task->due_date)
                            | 期限: {{ $task->due_date->format('Y/m/d') }}
                        @endif
                    </p>
                </div>
                <div>
                    <a href="{{ route('tasks.edit', $task) }}" class="btn btn-secondary">編集</a>
                </div>
            </div>
        @empty
            <p style="text-align: center; color: #6c757d; padding: 40px;">
                タスクがありません。「新規作成」ボタンからタスクを追加してください。
            </p>
        @endforelse
        
        {{-- ページネーション --}}
        <div style="margin-top: 20px;">
            {{ $tasks->links() }}
        </div>
    </div>
</x-app-layout>
```

---

### 2-5. タスク詳細画面を配置する

**ファイル**: `resources/views/tasks/show.blade.php`

```blade
<x-app-layout>
    <x-slot name="title">{{ $task->title }}</x-slot>
    
    <div class="card">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h1>{{ $task->title }}</h1>
            <div>
                <a href="{{ route('tasks.edit', $task) }}" class="btn btn-secondary">編集</a>
                <form action="{{ route('tasks.destroy', $task) }}" method="POST" style="display: inline;" onsubmit="return confirm('本当に削除しますか？');">
                    @csrf
                    @method('DELETE')
                    <button type="submit" class="btn btn-danger">削除</button>
                </form>
            </div>
        </div>
        
        <table>
            <tr>
                <th style="width: 150px;">ステータス</th>
                <td>
                    <span class="status-{{ $task->status }}">
                        @if($task->status === 'pending') 未着手
                        @elseif($task->status === 'in_progress') 進行中
                        @else 完了
                        @endif
                    </span>
                </td>
            </tr>
            <tr>
                <th>カテゴリー</th>
                <td>{{ $task->category->name ?? '未設定' }}</td>
            </tr>
            <tr>
                <th>期限</th>
                <td>{{ $task->due_date ? $task->due_date->format('Y年m月d日') : '未設定' }}</td>
            </tr>
            <tr>
                <th>説明</th>
                <td>{!! nl2br(e($task->description)) ?: '説明なし' !!}</td>
            </tr>
            <tr>
                <th>作成日時</th>
                <td>{{ $task->created_at->format('Y年m月d日 H:i') }}</td>
            </tr>
            <tr>
                <th>更新日時</th>
                <td>{{ $task->updated_at->format('Y年m月d日 H:i') }}</td>
            </tr>
        </table>
        
        <div style="margin-top: 20px;">
            <a href="{{ route('tasks.index') }}" class="btn btn-secondary">一覧に戻る</a>
        </div>
    </div>
</x-app-layout>
```

---

### 2-6. タスク作成画面を配置する

**ファイル**: `resources/views/tasks/create.blade.php`

```blade
<x-app-layout>
    <x-slot name="title">タスク作成</x-slot>
    
    <div class="card">
        <h1 style="margin-bottom: 20px;">タスク作成</h1>
        
        <form action="{{ route('tasks.store') }}" method="POST">
            @csrf
            
            <div class="form-group">
                <label for="title">タイトル <span style="color: red;">*</span></label>
                <input type="text" id="title" name="title" class="form-control" value="{{ old('title') }}" required>
                @error('title')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div class="form-group">
                <label for="description">説明</label>
                <textarea id="description" name="description" class="form-control" rows="5">{{ old('description') }}</textarea>
                @error('description')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div class="form-group">
                <label for="category_id">カテゴリー</label>
                <select id="category_id" name="category_id" class="form-control">
                    <option value="">選択してください</option>
                    @foreach($categories as $category)
                        <option value="{{ $category->id }}" {{ old('category_id') == $category->id ? 'selected' : '' }}>
                            {{ $category->name }}
                        </option>
                    @endforeach
                </select>
                @error('category_id')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div class="form-group">
                <label for="status">ステータス</label>
                <select id="status" name="status" class="form-control">
                    <option value="pending" {{ old('status') === 'pending' ? 'selected' : '' }}>未着手</option>
                    <option value="in_progress" {{ old('status') === 'in_progress' ? 'selected' : '' }}>進行中</option>
                    <option value="completed" {{ old('status') === 'completed' ? 'selected' : '' }}>完了</option>
                </select>
                @error('status')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div class="form-group">
                <label for="due_date">期限</label>
                <input type="date" id="due_date" name="due_date" class="form-control" value="{{ old('due_date') }}">
                @error('due_date')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div style="display: flex; gap: 10px;">
                <button type="submit" class="btn btn-primary">作成</button>
                <a href="{{ route('tasks.index') }}" class="btn btn-secondary">キャンセル</a>
            </div>
        </form>
    </div>
</x-app-layout>
```

---

### 2-7. タスク編集画面を配置する

**ファイル**: `resources/views/tasks/edit.blade.php`

```blade
<x-app-layout>
    <x-slot name="title">タスク編集</x-slot>
    
    <div class="card">
        <h1 style="margin-bottom: 20px;">タスク編集</h1>
        
        <form action="{{ route('tasks.update', $task) }}" method="POST">
            @csrf
            @method('PUT')
            
            <div class="form-group">
                <label for="title">タイトル <span style="color: red;">*</span></label>
                <input type="text" id="title" name="title" class="form-control" value="{{ old('title', $task->title) }}" required>
                @error('title')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div class="form-group">
                <label for="description">説明</label>
                <textarea id="description" name="description" class="form-control" rows="5">{{ old('description', $task->description) }}</textarea>
                @error('description')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div class="form-group">
                <label for="category_id">カテゴリー</label>
                <select id="category_id" name="category_id" class="form-control">
                    <option value="">選択してください</option>
                    @foreach($categories as $category)
                        <option value="{{ $category->id }}" {{ old('category_id', $task->category_id) == $category->id ? 'selected' : '' }}>
                            {{ $category->name }}
                        </option>
                    @endforeach
                </select>
                @error('category_id')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div class="form-group">
                <label for="status">ステータス</label>
                <select id="status" name="status" class="form-control">
                    <option value="pending" {{ old('status', $task->status) === 'pending' ? 'selected' : '' }}>未着手</option>
                    <option value="in_progress" {{ old('status', $task->status) === 'in_progress' ? 'selected' : '' }}>進行中</option>
                    <option value="completed" {{ old('status', $task->status) === 'completed' ? 'selected' : '' }}>完了</option>
                </select>
                @error('status')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div class="form-group">
                <label for="due_date">期限</label>
                <input type="date" id="due_date" name="due_date" class="form-control" value="{{ old('due_date', $task->due_date?->format('Y-m-d')) }}">
                @error('due_date')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div style="display: flex; gap: 10px;">
                <button type="submit" class="btn btn-primary">更新</button>
                <a href="{{ route('tasks.show', $task) }}" class="btn btn-secondary">キャンセル</a>
            </div>
        </form>
    </div>
</x-app-layout>
```

---

### 2-8. 認証画面を配置する

**ファイル**: `resources/views/auth/login.blade.php`

```blade
<x-app-layout>
    <x-slot name="title">ログイン</x-slot>
    
    <div class="card" style="max-width: 400px; margin: 50px auto;">
        <h1 style="text-align: center; margin-bottom: 20px;">ログイン</h1>
        
        <form method="POST" action="{{ route('login') }}">
            @csrf
            
            <div class="form-group">
                <label for="email">メールアドレス</label>
                <input type="email" id="email" name="email" class="form-control" value="{{ old('email') }}" required autofocus>
                @error('email')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div class="form-group">
                <label for="password">パスワード</label>
                <input type="password" id="password" name="password" class="form-control" required>
                @error('password')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <button type="submit" class="btn btn-primary" style="width: 100%;">ログイン</button>
        </form>
        
        <p style="text-align: center; margin-top: 15px;">
            <a href="{{ route('register') }}">アカウントをお持ちでない方はこちら</a>
        </p>
    </div>
</x-app-layout>
```

**ファイル**: `resources/views/auth/register.blade.php`

```blade
<x-app-layout>
    <x-slot name="title">ユーザー登録</x-slot>
    
    <div class="card" style="max-width: 400px; margin: 50px auto;">
        <h1 style="text-align: center; margin-bottom: 20px;">ユーザー登録</h1>
        
        <form method="POST" action="{{ route('register') }}">
            @csrf
            
            <div class="form-group">
                <label for="name">名前</label>
                <input type="text" id="name" name="name" class="form-control" value="{{ old('name') }}" required>
                @error('name')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div class="form-group">
                <label for="email">メールアドレス</label>
                <input type="email" id="email" name="email" class="form-control" value="{{ old('email') }}" required>
                @error('email')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div class="form-group">
                <label for="password">パスワード</label>
                <input type="password" id="password" name="password" class="form-control" required>
                @error('password')
                    <p class="error">{{ $message }}</p>
                @enderror
            </div>
            
            <div class="form-group">
                <label for="password_confirmation">パスワード（確認）</label>
                <input type="password" id="password_confirmation" name="password_confirmation" class="form-control" required>
            </div>
            
            <button type="submit" class="btn btn-primary" style="width: 100%;">登録</button>
        </form>
        
        <p style="text-align: center; margin-top: 15px;">
            <a href="{{ route('login') }}">すでにアカウントをお持ちの方はこちら</a>
        </p>
    </div>
</x-app-layout>
```

---

## Step 3: 提供コードの読み解き方

Bladeファイルを配置したら、**中身を読み解く**ことが重要です。

### 3-1. 必要な変数を特定する

`tasks/index.blade.php`を見てみましょう：

```blade
@foreach($categories as $category)
    <option value="{{ $category->id }}">{{ $category->name }}</option>
@endforeach

@forelse($tasks as $task)
    <h3>{{ $task->title }}</h3>
    <span>{{ $task->category->name }}</span>
@empty
```

**読み解きポイント**：

| 変数 | 必要なデータ |
|:---|:---|
| `$categories` | カテゴリーの一覧（Categoryモデルのコレクション） |
| `$tasks` | タスクの一覧（Taskモデルのコレクション） |
| `$task->category` | タスクとカテゴリーのリレーション |

---

### 3-2. 必要なリレーションを特定する

`$task->category->name`という記述から、**TaskモデルにCategoryへのリレーションが必要**だとわかります。

```php
// Taskモデルに必要なリレーション
public function category()
{
    return $this->belongsTo(Category::class);
}
```

---

### 3-3. 必要なルートを特定する

```blade
<a href="{{ route('tasks.index') }}">
<a href="{{ route('tasks.create') }}">
<a href="{{ route('tasks.show', $task) }}">
<a href="{{ route('tasks.edit', $task) }}">
<form action="{{ route('tasks.destroy', $task) }}" method="POST">
```

**読み解きポイント**：

| ルート名 | HTTPメソッド | 必要なアクション |
|:---|:---|:---|
| `tasks.index` | GET | 一覧表示 |
| `tasks.create` | GET | 作成フォーム表示 |
| `tasks.store` | POST | 作成処理 |
| `tasks.show` | GET | 詳細表示 |
| `tasks.edit` | GET | 編集フォーム表示 |
| `tasks.update` | PUT | 更新処理 |
| `tasks.destroy` | DELETE | 削除処理 |

→ **リソースコントローラー**を使えば、これらのルートを一括で定義できます。

---

## Step 4: 動作確認（エラーを確認する）

Bladeファイルを配置したら、**あえてエラーを出して**何が足りないかを確認します。

### 4-1. ブラウザでアクセスする

```
http://localhost/tasks
```

### 4-2. エラーを確認する

```
Target class [App\Http\Controllers\TaskController] does not exist.
```

→ **TaskControllerが存在しない**ことがわかります。

### 4-3. コントローラーを作成する

```bash
sail artisan make:controller TaskController --resource
```

### 4-4. 再度アクセスする

```
Undefined variable $tasks
```

→ **$tasks変数がビューに渡されていない**ことがわかります。

---

## 💡 TIP: エラーから学ぶ

エラーは「何が足りないか」を教えてくれる**最高の先生**です。

| エラーメッセージ | 意味 | 対処法 |
|:---|:---|:---|
| `Target class does not exist` | コントローラーがない | コントローラーを作成する |
| `Undefined variable` | 変数が渡されていない | コントローラーで変数を渡す |
| `Route not defined` | ルートがない | ルートを定義する |
| `Call to undefined relationship` | リレーションがない | モデルにリレーションを定義する |

---

## ✨ まとめ

このセクションでは、提供アセットの配置について学びました。

*   フロントエンドエンジニアから納品されたBladeファイルを配置する方法を学んだ
*   Bladeファイルを読み解いて、必要な変数・リレーション・ルートを特定する方法を学んだ
*   「エラーを確認する」ことで、何が足りないかを把握する方法を学んだ

次のChapterでは、このBladeファイルを動かすために必要なバックエンド実装を行います。

---
