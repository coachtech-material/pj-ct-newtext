# Tutorial 9-2-3: 実践: BladeでAPIレスポンスを可視化しよう

## 🎯 このセクションで学ぶこと

*   BladeテンプレートをAPIのデバッグ/検証ツールとして活用できるようになる。
*   コントローラーからBladeにデータを渡し、表示できるようになる。
*   「泥臭い」1ファイル完結のBladeで、素早くAPIレスポンスを確認できるようになる。

---

## 導入：APIのレスポンスを「目で見て」確認したい

これまでのセクションで、Laravelのルーティング、コントローラー、Bladeの基本構文を学びました。しかし、API開発をしていると、「このエンドポイントが正しくデータを返しているか」を確認したくなります。

もちろん、PostmanやcURLでAPIを叩くこともできますが、**ブラウザで視覚的に確認できる方が、開発効率が上がる**ことがあります。特に、以下のような場合です。

*   **複数のデータを一覧表示したい**: JSON配列を見やすく表示したい
*   **リレーションシップを確認したい**: ユーザーと投稿の関係を視覚的に確認したい
*   **バリデーションエラーを確認したい**: エラーメッセージを見やすく表示したい

このセクションでは、**BladeをAPIのデバッグ/検証ツールとして活用する方法**を学びます。

---

## 詳細解説

### 🎨 「泥臭い」Bladeで十分

v10カリキュラムでは、Bladeを**API開発のデバッグ/検証ツール**として位置づけています。そのため、以下のような「泥臭い」書き方で十分です。

*   **1ファイルにHTMLをベタ書きする**: レイアウト継承やコンポーネントは不要
*   **CSSは最小限**: 見やすければOK、デザインは気にしない
*   **ロジックはコントローラーに**: Bladeはあくまで表示のみ

これにより、素早くAPIレスポンスを確認できます。

---

### 📝 実践: ユーザー一覧を表示する

#### ステップ1: ルートを定義する

**`routes/web.php`**

```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\UserDebugController;

Route::get('/debug/users', [UserDebugController::class, 'index']);
```

**重要なポイント**

*   `/debug/`というプレフィックスを付けることで、「これはデバッグ用のエンドポイントだ」とわかりやすくします。
*   本番環境では、このルートを削除するか、ミドルウェアで保護します。

#### ステップ2: コントローラーを作成する

```bash
docker compose exec php php artisan make:controller UserDebugController
```

**`app/Http/Controllers/UserDebugController.php`**

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;

class UserDebugController extends Controller
{
    public function index()
    {
        $users = User::all();
        return view('debug.users', compact('users'));
    }
}
```

**コードリーディング**

*   `User::all()`: 全てのユーザーを取得します。
*   `view('debug.users', compact('users'))`: `resources/views/debug/users.blade.php`にデータを渡します。
*   `compact('users')`: `['users' => $users]`と同じ意味です。

#### ステップ3: Bladeビューを作成する

```bash
docker compose exec php mkdir -p resources/views/debug
docker compose exec php touch resources/views/debug/users.blade.php
```

**`resources/views/debug/users.blade.php`**

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ユーザー一覧（デバッグ用）</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            border-collapse: collapse;
            width: 100%;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>ユーザー一覧（デバッグ用）</h1>
    <p>全{{ count($users) }}件</p>

    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>名前</th>
                <th>メールアドレス</th>
                <th>作成日時</th>
            </tr>
        </thead>
        <tbody>
            @foreach ($users as $user)
                <tr>
                    <td>{{ $user->id }}</td>
                    <td>{{ $user->name }}</td>
                    <td>{{ $user->email }}</td>
                    <td>{{ $user->created_at->format('Y-m-d H:i:s') }}</td>
                </tr>
            @endforeach
        </tbody>
    </table>
</body>
</html>
```

**コードリーディング**

*   `count($users)`: ユーザーの件数を表示します。
*   `@foreach ($users as $user)`: ユーザーをループで表示します。
*   `{{ $user->created_at->format('Y-m-d H:i:s') }}`: 日時をフォーマットして表示します。

#### ステップ4: ブラウザで確認する

```
http://localhost/debug/users
```

これで、全てのユーザーが表形式で表示されます。

---

### 🔍 実践: ユーザーと投稿を一緒に表示する

次に、リレーションシップを持つデータを表示してみましょう。

#### コントローラーを修正する

**`app/Http/Controllers/UserDebugController.php`**

```php
public function index()
{
    $users = User::with('posts')->get();
    return view('debug.users', compact('users'));
}
```

**コードリーディング**

*   `User::with('posts')->get()`: ユーザーと一緒に、関連する投稿も取得します（Eager Loading）。

#### Bladeビューを修正する

**`resources/views/debug/users.blade.php`**

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ユーザー一覧（デバッグ用）</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        .user {
            border: 1px solid #ddd;
            padding: 15px;
            margin-bottom: 20px;
        }
        .posts {
            margin-left: 20px;
            margin-top: 10px;
        }
        .post {
            border-left: 3px solid #007bff;
            padding-left: 10px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <h1>ユーザーと投稿一覧（デバッグ用）</h1>
    <p>全{{ count($users) }}件</p>

    @foreach ($users as $user)
        <div class="user">
            <h2>{{ $user->name }} (ID: {{ $user->id }})</h2>
            <p>メール: {{ $user->email }}</p>
            <p>投稿数: {{ $user->posts->count() }}件</p>

            @if ($user->posts->count() > 0)
                <div class="posts">
                    <h3>投稿一覧</h3>
                    @foreach ($user->posts as $post)
                        <div class="post">
                            <strong>{{ $post->title }}</strong>
                            <p>{{ Str::limit($post->content, 100) }}</p>
                            <small>作成日: {{ $post->created_at->format('Y-m-d H:i') }}</small>
                        </div>
                    @endforeach
                </div>
            @else
                <p>投稿がありません</p>
            @endif
        </div>
    @endforeach
</body>
</html>
```

**コードリーディング**

*   `$user->posts->count()`: ユーザーの投稿数を表示します。
*   `@if ($user->posts->count() > 0)`: 投稿がある場合のみ、投稿一覧を表示します。
*   `Str::limit($post->content, 100)`: 投稿内容を100文字に制限して表示します。

---

### 🚀 実践: APIレスポンスとBladeを並行して確認する

API開発では、以下のような流れで開発することが多いです。

1. **APIエンドポイントを作成する** (`/api/users`)
2. **Bladeでデバッグ用ページを作成する** (`/debug/users`)
3. **Bladeで視覚的に確認しながら、APIのロジックを修正する**
4. **APIが完成したら、Postmanで最終確認する**

#### 例: APIエンドポイントとデバッグページを並行開発

**`routes/api.php`**

```php
Route::get('/users', [UserController::class, 'index']);
```

**`app/Http/Controllers/UserController.php`**

```php
public function index()
{
    $users = User::with('posts')->get();
    return response()->json($users);
}
```

**`routes/web.php`**

```php
Route::get('/debug/users', [UserDebugController::class, 'index']);
```

**`app/Http/Controllers/UserDebugController.php`**

```php
public function index()
{
    $users = User::with('posts')->get();
    return view('debug.users', compact('users'));
}
```

これにより、以下の2つのエンドポイントができます。

*   **API**: `http://localhost/api/users` → JSON形式で返す
*   **デバッグ**: `http://localhost/debug/users` → HTML形式で視覚的に表示

---

### 💡 TIP: `dd()`と組み合わせる

Bladeでデータ構造を確認したい場合は、`dd()`を使うこともできます。

```blade
@php
    dd($users);
@endphp
```

これにより、`$users`の内容が見やすく表示され、処理が停止します。

---

### 🔒 本番環境での注意点

デバッグ用のエンドポイントは、**本番環境では削除するか、認証で保護する**必要があります。

#### 方法1: 環境変数で制御する

**`routes/web.php`**

```php
if (config('app.debug')) {
    Route::get('/debug/users', [UserDebugController::class, 'index']);
}
```

これにより、`APP_DEBUG=false`の本番環境では、デバッグルートが登録されません。

#### 方法2: ミドルウェアで保護する

```php
Route::middleware('auth')->group(function () {
    Route::get('/debug/users', [UserDebugController::class, 'index']);
});
```

---

## ✨ まとめ

このセクションでは、BladeをAPIのデバッグ/検証ツールとして活用する方法を学びました。

*   BladeはAPI開発のデバッグ/検証ツールとして非常に有用である。
*   1ファイルにHTMLをベタ書きする「泥臭い」書き方で十分である。
*   コントローラーからBladeにデータを渡し、`@foreach`や`@if`で表示できる。
*   APIエンドポイントとデバッグページを並行開発することで、開発効率が上がる。
*   本番環境では、デバッグルートを削除するか、認証で保護する。

次のセクションでは、Bladeでフォームを作成し、CSRFトークンについて学びます。

---

## 📝 学習のポイント

- [ ] BladeをAPIのデバッグ/検証ツールとして活用できる。
- [ ] コントローラーから`view()`でBladeにデータを渡せる。
- [ ] `@foreach`や`@if`を使って、データを視覚的に表示できる。
- [ ] APIエンドポイントとデバッグページを並行開発すると効率的である。
- [ ] 本番環境では、デバッグルートを削除するか、認証で保護する必要がある。
