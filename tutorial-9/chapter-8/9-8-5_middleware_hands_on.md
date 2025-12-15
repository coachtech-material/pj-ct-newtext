# Tutorial 9-8-5: ミドルウェア - ハンズオン演習

## 📝 このセクションの目的

Chapter 8で学んだミドルウェアを実際に手を動かして確認します。カスタムミドルウェアを作成して、リクエストの前処理・後処理を実装しましょう。

---

## 🎯 演習課題：管理者専用ページの実装

### 📋 要件

1. `CheckAdmin`ミドルウェアを作成
2. ユーザーが管理者でない場合は403エラーを返す
3. `/admin`ルートにミドルウェアを適用

---

## 💡 ヒント

```bash
php artisan make:middleware CheckAdmin
```

```php
public function handle(Request $request, Closure $next)
{
    if (!auth()->user()->is_admin) {
        abort(403);
    }
    return $next($request);
}
```

---

## 📖 模範解答

### CheckAdmin.php

```php
<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class CheckAdmin
{
    public function handle(Request $request, Closure $next)
    {
        if (!auth()->check() || !auth()->user()->is_admin) {
            abort(403, '管理者権限が必要です');
        }
        
        return $next($request);
    }
}
```

### app/Http/Kernel.php

```php
protected $middlewareAliases = [
    // ...
    'admin' => \App\Http\Middleware\CheckAdmin::class,
];
```

### routes/web.php

```php
Route::get('/admin', [AdminController::class, 'index'])->middleware('admin');
```

---

## 💪 自己評価チェックリスト

- [ ] カスタムミドルウェアを作成できた
- [ ] ミドルウェアを登録できた
- [ ] ルートにミドルウェアを適用できた
- [ ] abort()でエラーを返せた

すべてチェックできたら、Chapter 9に進みましょう！
