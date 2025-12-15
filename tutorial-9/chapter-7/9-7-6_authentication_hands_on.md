# Tutorial 9-7-6: 認証機能 - ハンズオン演習

## 📝 このセクションの目的

Chapter 7で学んだ認証機能を実際に手を動かして確認します。ログイン・ログアウト機能を実装し、認証が必要なページを作成しましょう。

---

## 🎯 演習課題：マイページ機能の実装

### 📋 要件

1. ログイン・ログアウト機能を実装
2. `/mypage`にマイページを作成（認証必須）
3. 未ログイン時はログインページにリダイレクト
4. マイページにユーザー情報を表示

---

## 💡 ヒント

```bash
php artisan make:controller AuthController
```

```php
// ログイン
if (Auth::attempt(['email' => $email, 'password' => $password])) {
    return redirect('/mypage');
}

// ログアウト
Auth::logout();

// 認証済みユーザー取得
$user = Auth::user();

// ミドルウェア
Route::get('/mypage', [MypageController::class, 'index'])->middleware('auth');
```

---

## 📖 模範解答

### AuthController.php

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class AuthController extends Controller
{
    public function showLoginForm()
    {
        return view('auth.login');
    }

    public function login(Request $request)
    {
        $credentials = $request->only('email', 'password');

        if (Auth::attempt($credentials)) {
            $request->session()->regenerate();
            return redirect()->intended('/mypage');
        }

        return back()->withErrors([
            'email' => 'メールアドレスまたはパスワードが正しくありません',
        ]);
    }

    public function logout(Request $request)
    {
        Auth::logout();
        $request->session()->invalidate();
        $request->session()->regenerateToken();
        return redirect('/');
    }
}
```

### MypageController.php

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class MypageController extends Controller
{
    public function index()
    {
        $user = Auth::user();
        return view('mypage.index', ['user' => $user]);
    }
}
```

### routes/web.php

```php
use App\Http\Controllers\AuthController;
use App\Http\Controllers\MypageController;

Route::get('/login', [AuthController::class, 'showLoginForm'])->name('login');
Route::post('/login', [AuthController::class, 'login']);
Route::post('/logout', [AuthController::class, 'logout']);

Route::get('/mypage', [MypageController::class, 'index'])->middleware('auth');
```

### auth/login.blade.php

```blade
@extends('layouts.app')

@section('content')
<div class="container">
    <h1>ログイン</h1>
    
    <form action="{{ route('login') }}" method="POST">
        @csrf
        <div class="mb-3">
            <label>メールアドレス</label>
            <input type="email" name="email" class="form-control" value="{{ old('email') }}" required>
            @error('email')
                <p class="text-danger">{{ $message }}</p>
            @enderror
        </div>
        <div class="mb-3">
            <label>パスワード</label>
            <input type="password" name="password" class="form-control" required>
        </div>
        <button type="submit" class="btn btn-primary">ログイン</button>
    </form>
</div>
@endsection
```

### mypage/index.blade.php

```blade
@extends('layouts.app')

@section('content')
<div class="container">
    <h1>マイページ</h1>
    
    <div class="card">
        <div class="card-body">
            <h2>ユーザー情報</h2>
            <p>名前: {{ $user->name }}</p>
            <p>メールアドレス: {{ $user->email }}</p>
        </div>
    </div>
    
    <form action="/logout" method="POST" class="mt-3">
        @csrf
        <button type="submit" class="btn btn-secondary">ログアウト</button>
    </form>
</div>
@endsection
```

---

## 💪 自己評価チェックリスト

- [ ] ログイン機能を実装できた
- [ ] ログアウト機能を実装できた
- [ ] authミドルウェアを使えた
- [ ] Auth::user()でユーザー情報を取得できた
- [ ] 未ログイン時にリダイレクトできた

すべてチェックできたら、Chapter 8に進みましょう！
