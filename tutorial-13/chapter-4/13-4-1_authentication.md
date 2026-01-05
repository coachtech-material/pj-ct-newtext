# Tutorial 13-4-1: 認証機能の実装

## 🎯 このセクションで学ぶこと

- Laravel Fortifyを使った認証機能を実装する
- ログイン・ログアウト・ユーザー登録画面を作成する
- イシュー駆動開発のフローを継続する

---

## Step 0: 開発の準備（チケット駆動）

### 0-1. GitHubでIssueを確認

GitHubで `#7 ユーザー認証機能` のIssueを確認します。

### 0-2. ブランチを作成

```bash
git checkout main
git pull origin main
git switch -c feature/issue-7-authentication
```

---

## Step 1: Laravel Fortifyのインストール

### 1-1. Fortifyをインストール

```bash
sail composer require laravel/fortify
```

### 1-2. Fortifyの設定ファイルを公開

```bash
sail artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

### 1-3. マイグレーションを実行

```bash
sail artisan migrate
```

---

## Step 2: FortifyServiceProviderの設定

### 2-1. config/app.phpにプロバイダを登録

**ファイル**: `config/app.php`

```php
'providers' => [
    // ...
    App\Providers\FortifyServiceProvider::class,
],
```

### 2-2. FortifyServiceProviderを編集

**ファイル**: `app/Providers/FortifyServiceProvider.php`

```php
<?php

namespace App\Providers;

use App\Actions\Fortify\CreateNewUser;
use Illuminate\Support\ServiceProvider;
use Laravel\Fortify\Fortify;

class FortifyServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        //
    }

    public function boot(): void
    {
        Fortify::createUsersUsing(CreateNewUser::class);

        // ログイン画面
        Fortify::loginView(function () {
            return view('auth.login');
        });

        // ユーザー登録画面
        Fortify::registerView(function () {
            return view('auth.register');
        });
    }
}
```

---

## Step 3: 認証用Bladeファイルの配置

### 3-1. ログイン画面

**ファイル**: `resources/views/auth/login.blade.php`

```blade
<x-app-layout>
    <x-slot name="title">ログイン</x-slot>
    
    <div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 class="text-2xl font-bold text-gray-800 mb-6 text-center">ログイン</h1>
        
        <form action="{{ route('login') }}" method="POST">
            @csrf
            
            {{-- メールアドレス --}}
            <div class="mb-4">
                <label for="email" class="block text-gray-700 font-medium mb-2">メールアドレス</label>
                <input type="email" name="email" id="email" value="{{ old('email') }}"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
                @error('email')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- パスワード --}}
            <div class="mb-6">
                <label for="password" class="block text-gray-700 font-medium mb-2">パスワード</label>
                <input type="password" name="password" id="password"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
                @error('password')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- ボタン --}}
            <button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded">
                ログイン
            </button>
        </form>
        
        <p class="text-center text-gray-600 mt-4">
            アカウントをお持ちでない方は
            <a href="{{ route('register') }}" class="text-blue-500 hover:underline">新規登録</a>
        </p>
    </div>
</x-app-layout>
```

### 3-2. ユーザー登録画面

**ファイル**: `resources/views/auth/register.blade.php`

```blade
<x-app-layout>
    <x-slot name="title">新規登録</x-slot>
    
    <div class="max-w-md mx-auto bg-white rounded-lg shadow-md p-6">
        <h1 class="text-2xl font-bold text-gray-800 mb-6 text-center">新規登録</h1>
        
        <form action="{{ route('register') }}" method="POST">
            @csrf
            
            {{-- 名前 --}}
            <div class="mb-4">
                <label for="name" class="block text-gray-700 font-medium mb-2">名前</label>
                <input type="text" name="name" id="name" value="{{ old('name') }}"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
                @error('name')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- メールアドレス --}}
            <div class="mb-4">
                <label for="email" class="block text-gray-700 font-medium mb-2">メールアドレス</label>
                <input type="email" name="email" id="email" value="{{ old('email') }}"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
                @error('email')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- パスワード --}}
            <div class="mb-4">
                <label for="password" class="block text-gray-700 font-medium mb-2">パスワード</label>
                <input type="password" name="password" id="password"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
                @error('password')
                    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
                @enderror
            </div>
            
            {{-- パスワード確認 --}}
            <div class="mb-6">
                <label for="password_confirmation" class="block text-gray-700 font-medium mb-2">パスワード（確認）</label>
                <input type="password" name="password_confirmation" id="password_confirmation"
                    class="w-full border border-gray-300 rounded px-3 py-2 focus:outline-none focus:border-blue-500">
            </div>
            
            {{-- ボタン --}}
            <button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white py-2 rounded">
                登録
            </button>
        </form>
        
        <p class="text-center text-gray-600 mt-4">
            すでにアカウントをお持ちの方は
            <a href="{{ route('login') }}" class="text-blue-500 hover:underline">ログイン</a>
        </p>
    </div>
</x-app-layout>
```

---

## Step 4: ルートの保護

### 4-1. web.phpでミドルウェアを適用

**ファイル**: `routes/web.php`

```php
<?php

use App\Http\Controllers\BookController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return redirect()->route('books.index');
});

// 認証が必要なルート
Route::middleware('auth')->group(function () {
    Route::resource('books', BookController::class);
});
```

> 💡 **ポイント**: `middleware('auth')`を適用すると、ログインしていないユーザーはログイン画面にリダイレクトされます。

---

## Step 5: 動作確認

### 5-1. ログアウト状態で確認

1. `http://localhost/books`にアクセス
2. ログイン画面にリダイレクトされることを確認

### 5-2. ユーザー登録

1. 「新規登録」リンクをクリック
2. フォームに入力して登録
3. 書籍一覧画面が表示されることを確認

### 5-3. ログアウト

1. ナビゲーションの「ログアウト」をクリック
2. ログイン画面にリダイレクトされることを確認

---

## Step 6: コミット、PR、マージ

### 6-1. コミット

```bash
git add .
git commit -m "feat: 認証機能の実装 (Closes #7)"
```

### 6-2. プッシュ、PR、マージ

```bash
git push origin feature/issue-7-authentication
```

GitHubでPRを作成し、セルフレビュー後にマージします。

---

## ✨ まとめ

このセクションでは、認証機能の実装について学びました。

| Step | 学んだこと |
|:---|:---|
| Step 1 | Laravel Fortifyのインストール |
| Step 2 | FortifyServiceProviderの設定 |
| Step 3 | ログイン・登録画面の作成 |
| Step 4 | ルートの保護（authミドルウェア） |
| Step 5-6 | 動作確認、コミット、PR、マージ |

次のセクションでは、ユーザーと書籍の関連付けを実装します。

---
