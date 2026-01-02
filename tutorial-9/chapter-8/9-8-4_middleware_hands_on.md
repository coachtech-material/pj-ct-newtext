# Tutorial 9-8-4: ミドルウェア - ハンズオン演習

## 📝 このセクションの目的

Chapter 8で学んだミドルウェアを実際に手を動かして確認します。カスタムミドルウェアを作成して、リクエストの前処理・後処理を実装しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

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

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？ミドルウェアはリクエストの前後に処理を挿入できる強力な機能です。一緒に手を動かしながら、管理者専用ページを実装していきましょう。

### 💭 実装の思考プロセス

ミドルウェアを実装する際、以下の順番で考えると効率的です：

1. **カスタムミドルウェアを作成**：Artisanコマンドで生成
2. **handleメソッドにロジックを実装**：管理者チェックを追加
3. **ミドルウェアを登録**：Kernel.phpでエイリアスを設定
4. **ルートに適用**：middleware()でミドルウェアを適用
5. **テスト**：管理者と一般ユーザーで動作確認

ミドルウェアのポイントは「リクエストの前後に共通処理を挿入し、コードの再利用性を高める」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: カスタムミドルウェアを作成する

**何を考えているか**：
- 「管理者かどうかをチェックするミドルウェアが必要だ」
- 「CheckAdminという名前にしよう」
- 「Artisanコマンドで簡単に生成できる」

ターミナルで以下のコマンドを実行します：

```bash
php artisan make:middleware CheckAdmin
```

**コマンド解説**：

```bash
php artisan make:middleware CheckAdmin
```
→ `CheckAdmin`ミドルウェアを生成します。`app/Http/Middleware/CheckAdmin.php`が作成されます。

---

#### ステップ2: handleメソッドにロジックを実装する

**何を考えているか**：
- 「ユーザーがログインしているかチェックしよう」
- 「管理者フラグをチェックしよう」
- 「権限がなければ403エラーを返そう」

`app/Http/Middleware/CheckAdmin.php`を開いて、以下のように編集します：

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

**コードリーディング**：

```php
public function handle(Request $request, Closure $next)
```
→ `handle`メソッドはミドルウェアのエントリーポイントです。`$request`でリクエストを受け取り、`$next`で次の処理に進みます。

```php
if (!auth()->check() || !auth()->user()->is_admin) {
    abort(403, '管理者権限が必要です');
}
```
→ `auth()->check()`でログイン状態を確認し、`auth()->user()->is_admin`で管理者フラグをチェックします。条件を満たさない場合、`abort(403)`で403エラーを返します。

```php
return $next($request);
```
→ チェックをパスしたら、`$next($request)`で次の処理（コントローラー）に進みます。ミドルウェアの基本パターンです。

---

#### ステップ3: ミドルウェアを登録する

**何を考えているか**：
- 「ミドルウェアを使えるように登録しよう」
- 「エイリアスを設定して簡単に使えるようにしよう」
- 「Kernel.phpで登録する必要がある」

`app/Http/Kernel.php`を開いて、`$middlewareAliases`配列に以下を追加します：

```php
protected $middlewareAliases = [
    // ...
    'admin' => \App\Http\Middleware\CheckAdmin::class,
];
```

**コードリーディング**：

```php
'admin' => \App\Http\Middleware\CheckAdmin::class,
```
→ `admin`というエイリアスで`CheckAdmin`ミドルウェアを登録します。ルートで`middleware('admin')`と書くだけで使用できます。

---

#### ステップ4: ルートに適用する

**何を考えているか**：
- 「管理者専用ページにミドルウェアを適用しよう」
- 「`/admin`ルートを作成しよう」
- 「`middleware('admin')`で簡単に適用できる」

まず、`AdminController`を作成します：

```bash
php artisan make:controller AdminController
```

`app/Http/Controllers/AdminController.php`を開いて、以下のように編集します：

```php
<?php

namespace App\Http\Controllers;

class AdminController extends Controller
{
    public function index()
    {
        return view('admin.index');
    }
}
```

`routes/web.php`を開いて、以下を追加します：

```php
use App\Http\Controllers\AdminController;

Route::get('/admin', [AdminController::class, 'index'])->middleware('admin');
```

**コードリーディング**：

```php
Route::get('/admin', [AdminController::class, 'index'])->middleware('admin');
```
→ `/admin`ルートに`admin`ミドルウェアを適用します。このルートにアクセスすると、まず`CheckAdmin`ミドルウェアが実行され、チェックをパスした場合のみコントローラーが実行されます。

---

#### ステップ5: テストする

**何を考えているか**：
- 「管理者と一般ユーザーで動作を確認しよう」
- 「管理者はアクセスできて、一般ユーザーは403エラーになるはず」

テスト手順：

1. **管理者ユーザーでログイン**：`is_admin = 1`のユーザーでログイン
2. **`/admin`にアクセス**：管理者ページが表示されることを確認
3. **一般ユーザーでログイン**：`is_admin = 0`のユーザーでログイン
4. **`/admin`にアクセス**：403エラーが表示されることを確認

---

### ✨ 完成！

これでカスタムミドルウェアが実装できました！リクエストの前後に処理を挿入し、管理者専用ページを作成できましたね。

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
