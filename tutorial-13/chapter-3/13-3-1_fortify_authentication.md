# Tutorial 13-3-1: 認証機能の実装（Laravel Fortify）

## 🎯 このセクションで学ぶこと

- 提供された認証画面を読み解き、Fortifyの設定方法を学ぶ
- Laravel Fortifyを使った認証機能を実装する方法を学ぶ
- 認証済みユーザーのみがタスクにアクセスできるようにする

---

## 🧠 先輩エンジニアの思考プロセス

### 認証機能の実装タイミング

CRUDが完成したら、次は「認証」機能です。なぜこのタイミングなのでしょうか？

| 理由 | 説明 |
|:---|:---|
| まずは機能を動かす | 最初から認証を入れると、ログインしないとテストできない |
| セキュリティの確保 | 現状では誰でもタスクを見たり編集したりできてしまう |
| リレーションシップの準備 | 「このタスクは誰のもの？」という問題に対応する |

### 提供コードありきのフロー

今回も「提供コードありき」のフローで進めます：

```
1. 画面アクセス＆エラー確認（認証画面の確認）
2. Bladeの解読（フォームの構造を確認）
3. Fortifyの設定（バックエンドの実装）
4. 動作確認
```

---

## Step 1: 提供された認証画面を確認する

### 1-1. 認証画面のBladeファイルを確認する

提供アセットには、以下の認証画面が含まれています：

| ファイル | 内容 |
|:---|:---|
| `resources/views/auth/register.blade.php` | ユーザー登録画面 |
| `resources/views/auth/login.blade.php` | ログイン画面 |

### 1-2. ブラウザでアクセスする

```
http://localhost/register
```

### 1-3. エラーを確認する

```
Route [register] not defined.
```

**読み解き**：Fortifyがまだインストールされていないため、認証関連のルートが定義されていません。

---

## Step 2: Bladeの解読

### 2-1. register.blade.phpを読む

`resources/views/auth/register.blade.php`を開いて、フォームの構造を確認します。

```blade
<form action="{{ route('register') }}" method="POST">
    @csrf
    
    <div class="form-group">
        <label for="name">名前</label>
        <input type="text" id="name" name="name" value="{{ old('name') }}" required>
        @error('name')
            <p class="error">{{ $message }}</p>
        @enderror
    </div>
    
    <div class="form-group">
        <label for="email">メールアドレス</label>
        <input type="email" id="email" name="email" value="{{ old('email') }}" required>
        @error('email')
            <p class="error">{{ $message }}</p>
        @enderror
    </div>
    
    <div class="form-group">
        <label for="password">パスワード</label>
        <input type="password" id="password" name="password" required>
        @error('password')
            <p class="error">{{ $message }}</p>
        @enderror
    </div>
    
    <div class="form-group">
        <label for="password_confirmation">パスワード（確認）</label>
        <input type="password" id="password_confirmation" name="password_confirmation" required>
    </div>
    
    <button type="submit">登録</button>
</form>
```

### 2-2. フォーム項目を整理する

| フィールド名 | name属性 | 説明 |
|:---|:---|:---|
| 名前 | `name` | ユーザーの表示名 |
| メールアドレス | `email` | ログインに使用 |
| パスワード | `password` | 8文字以上 |
| パスワード確認 | `password_confirmation` | パスワードと一致する必要がある |

### 2-3. login.blade.phpを読む

`resources/views/auth/login.blade.php`を開いて、フォームの構造を確認します。

```blade
<form action="{{ route('login') }}" method="POST">
    @csrf
    
    <div class="form-group">
        <label for="email">メールアドレス</label>
        <input type="email" id="email" name="email" value="{{ old('email') }}" required>
    </div>
    
    <div class="form-group">
        <label for="password">パスワード</label>
        <input type="password" id="password" name="password" required>
    </div>
    
    <div class="form-group">
        <input type="checkbox" id="remember" name="remember">
        <label for="remember">ログイン状態を保持する</label>
    </div>
    
    <button type="submit">ログイン</button>
</form>
```

### 2-4. 必要なルートを特定する

Bladeファイルから、以下のルートが必要であることがわかります：

| ルート名 | 用途 |
|:---|:---|
| `register` | ユーザー登録（GET: フォーム表示、POST: 登録処理） |
| `login` | ログイン（GET: フォーム表示、POST: ログイン処理） |
| `logout` | ログアウト（POST） |

これらのルートは**Fortifyが自動的に登録**します。

---

## Step 3: Fortifyのインストールと設定

### 3-1. Fortifyをインストールする

```bash
sail composer require laravel/fortify
```

### 3-2. 設定ファイルを公開する

```bash
sail artisan vendor:publish --provider="Laravel\Fortify\FortifyServiceProvider"
```

このコマンドを実行すると、以下のファイルが作成されます：

| ファイル | 説明 |
|:---|:---|
| `config/fortify.php` | Fortifyの設定ファイル |
| `app/Providers/FortifyServiceProvider.php` | Fortifyのサービスプロバイダー |
| `app/Actions/Fortify/` | 認証アクションのディレクトリ |

### 3-3. 機能を有効にする

**ファイル**: `config/fortify.php`

```php
'features' => [
    Features::registration(),
    Features::resetPasswords(),
    // Features::emailVerification(),
],
```

### 3-4. ビューを指定する

**ファイル**: `app/Providers/FortifyServiceProvider.php`

`boot()`メソッドに以下を追加します：

```php
use Laravel\Fortify\Fortify;

public function boot(): void
{
    // 既存のコード...
    
    // ビューの指定
    Fortify::registerView(function () {
        return view('auth.register');
    });

    Fortify::loginView(function () {
        return view('auth.login');
    });
    
    // 既存のコード...
}
```

**コードリーディング**：

```php
Fortify::registerView(function () {
    return view('auth.register');
});
```
→ `/register`にアクセスしたときに表示するビューを指定します。Fortifyは、このビューを自動的に表示します。

---

## Step 4: ルートの保護

### 4-1. 認証済みユーザーのみアクセスできるようにする

**ファイル**: `routes/web.php`

```php
use App\Http\Controllers\TaskController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return redirect()->route('tasks.index');
});

// 認証済みユーザーのみアクセス可能
Route::middleware(['auth'])->group(function () {
    Route::resource('tasks', TaskController::class);
});
```

**コードリーディング**：

```php
Route::middleware(['auth'])->group(function () { ... });
```
→ `auth`ミドルウェアを適用したルートグループを作成します。このグループ内のルートは、**ログインしていないとアクセスできません**。未ログインでアクセスすると、自動的にログインページにリダイレクトされます。

### 4-2. Fortifyが登録するルートを確認する

```bash
sail artisan route:list | grep -E "(register|login|logout)"
```

**実行結果**：

```
GET|HEAD  login .................... login › Laravel\Fortify
POST      login ..................... Laravel\Fortify
POST      logout .................... logout › Laravel\Fortify
GET|HEAD  register .................. register › Laravel\Fortify
POST      register .................. Laravel\Fortify
```

> **💡 ポイント**: Fortifyは認証関連のルートを自動的に登録します。コントローラーを自分で作成する必要はありません。

---

## Step 5: 動作確認

### 5-1. ユーザー登録をテストする

```
http://localhost/register
```

1. 名前、メールアドレス、パスワードを入力
2. 「登録」ボタンをクリック

| 確認項目 | 期待する結果 |
|:---|:---|
| ユーザーが作成される | データベースに保存される |
| 自動的にログインされる | タスク一覧ページにリダイレクト |

### 5-2. Tinkerでユーザーを確認する

```bash
sail artisan tinker
```

```php
>>> App\Models\User::all();
```

**期待する結果**：登録したユーザーが表示される

### 5-3. ログアウトをテストする

タスク一覧ページのログアウトボタンをクリックします。

| 確認項目 | 期待する結果 |
|:---|:---|
| ログアウトされる | ログインページにリダイレクト |

### 5-4. ログインをテストする

```
http://localhost/login
```

1. メールアドレス、パスワードを入力
2. 「ログイン」ボタンをクリック

| 確認項目 | 期待する結果 |
|:---|:---|
| ログインが成功する | タスク一覧ページにリダイレクト |

### 5-5. ルート保護を確認する

1. ログアウトする
2. `http://localhost/tasks`にアクセスする

| 確認項目 | 期待する結果 |
|:---|:---|
| ログインページにリダイレクトされる | 未認証ユーザーはアクセスできない |

---

## 💡 TIP: シーダーでテストユーザーを作成

毎回ユーザー登録するのは手間なので、シーダーでテストユーザーを作成しておきます。

**ファイル**: `database/seeders/DatabaseSeeder.php`

```php
public function run(): void
{
    \App\Models\User::factory()->create([
        'name' => 'Test User',
        'email' => 'test@example.com',
        'password' => bcrypt('password'),
    ]);
}
```

シーダーを実行します：

```bash
sail artisan db:seed
```

これで、`test@example.com` / `password`でログインできます。

---

## 💡 TIP: auth()ヘルパー

認証済みユーザーの情報を取得するには、`auth()`ヘルパーを使います。

```php
// ログインしているか確認
auth()->check();  // true or false

// ログインユーザーを取得
auth()->user();  // Userモデル or null

// ログインユーザーのIDを取得
auth()->id();  // int or null
```

Bladeでも使えます：

```blade
@auth
    <p>{{ auth()->user()->name }}さん、こんにちは！</p>
@endauth

@guest
    <p>ログインしてください</p>
@endguest
```

---

## ✨ まとめ

このセクションでは、「提供コードありき」の開発フローでFortify認証を実装しました。

| ステップ | 学んだこと |
|:---|:---|
| Step 1 | 提供された認証画面を確認し、エラーを確認 |
| Step 2 | Bladeを読み解いて、必要なルートを特定 |
| Step 3 | Fortifyをインストールし、ビューを指定 |
| Step 4 | authミドルウェアでルートを保護 |
| Step 5 | 認証機能の動作確認とTinkerでの確認 |

次のセクションでは、ユーザーとタスクのリレーションシップを実装します。

---
