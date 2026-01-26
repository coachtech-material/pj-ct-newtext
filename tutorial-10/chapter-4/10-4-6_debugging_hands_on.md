# Tutorial 10-4-6: デバッグ - ハンズオン演習

## 📝 このセクションの目的

Chapter 4で学んだデバッグ手法を実際に手を動かして確認します。エラーを特定し、修正する方法をマスターしましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのプロジェクトを作成します。

```
~/coachtech/laravel-practice/
├── 10-4-6_hands-on/                      ← このハンズオン用のディレクトリ
│   ├── debugging-app-practice/           ← 要件を見て自分で作成するプロジェクト
│   │   ├── app/
│   │   │   ├── Http/Controllers/
│   │   │   └── Models/
│   │   └── ...
│   └── debugging-app-sample/             ← 実践で一緒に作成するプロジェクト
│       ├── app/
│       │   ├── Http/Controllers/
│       │   └── Models/
│       └── ...
└── ...
```

| ディレクトリ | 用途 | URL |
|:---|:---|:---|
| `debugging-app-practice/` | 📋 要件を見て、自分の力で作成する | `http://localhost/users` |
| `debugging-app-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する | `http://localhost/users` |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

> ⚠️ **注意**: 2つのプロジェクトを同時に起動することはできません（ポートが競合するため）。一方のプロジェクトで作業する際は、もう一方を停止してください。

---

## 🎯 演習課題：エラーを修正しよう

### 🖼️ 完成イメージ

<!-- エラー画面と修正後の動作確認のスクリーンショットをここに配置 -->
![10-4-6 完成イメージ](images/10-4-6_debugging_complete.png)

**この演習で作るもの**：
エラーが含まれたコードをデバッグし、正しく動作する「ユーザー登録機能」に修正します。

---

### 📋 要件

以下のコードにあるエラーを見つけて修正してください。

```php
public function store(Request $request)
{
    $user = new User;
    $user->name = $request->name;
    $user->email = $request->email;
    $user->save();
    
    return redirect('/users');
}
```

**エラー内容**：
- Mass assignment エラーが発生する

---

### ✅ 完成品の確認方法

**🌐 ブラウザでの確認（推奨）**

- **動作確認URL**: `http://localhost/users/create`
- **確認手順**:
  1. Sailを起動する（`./vendor/bin/sail up -d`）
  2. マイグレーションを実行（`./vendor/bin/sail artisan migrate`）
  3. ブラウザで `http://localhost/users/create` にアクセス
  4. フォームに入力して送信

**正しく修正できていれば**:
- [ ] ユーザー登録フォームが表示される
- [ ] フォーム送信時にMass assignmentエラーが発生しない
- [ ] ユーザーがデータベースに保存される
- [ ] ユーザー一覧ページにリダイレクトされる

**🔧 Tinkerでデータ確認**:

```bash
./vendor/bin/sail artisan tinker
```

```php
use App\Models\User;
User::all();  // 登録したユーザーが表示されればOK
```

> 📌 **Bladeファイルについて**: バックエンド実装に集中するため、動作確認用のシンプルなBladeファイルを以下に用意しています。

<details>
<summary>📄 確認用Bladeファイル（クリックで展開）</summary>

`resources/views/users/create.blade.php`:

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ユーザー登録</title>
</head>
<body>
    <h1>ユーザー登録</h1>

    @if ($errors->any())
        <div style="color: red;">
            @foreach ($errors->all() as $error)
                <p>{{ $error }}</p>
            @endforeach
        </div>
    @endif

    <form action="/users" method="POST">
        @csrf
        <p><label>名前: <input type="text" name="name" value="{{ old('name') }}"></label></p>
        <p><label>メール: <input type="email" name="email" value="{{ old('email') }}"></label></p>
        <button type="submit">登録</button>
    </form>
</body>
</html>
```

`resources/views/users/index.blade.php`:

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>ユーザー一覧</title>
</head>
<body>
    <h1>ユーザー一覧</h1>
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }} ({{ $user->email }})</li>
        @endforeach
    </ul>
    <p><a href="/users/create">新規登録</a></p>
</body>
</html>
```

</details>

---

### 📁 Step 0: 環境を準備する（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

> **📌 前のハンズオンのプロジェクトを停止**
> 
> 前のハンズオン（10-3-6）のプロジェクトが起動している場合は、先に停止してください。
> ```bash
> cd ~/coachtech/laravel-practice/10-3-6_hands-on/authorization-app-sample
> ./vendor/bin/sail down
> ```

```bash
# laravel-practiceディレクトリに移動
cd ~/coachtech/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 10-4-6_hands-on
cd 10-4-6_hands-on

# Laravel 10.xプロジェクトを作成（自分で作成する用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 debugging-app-practice
```

```bash
# プロジェクトディレクトリに移動
cd debugging-app-practice

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql

# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate

# データベースのマイグレーション
./vendor/bin/sail artisan migrate
```

**✅ ディレクトリ構造の確認**

```
~/coachtech/laravel-practice/
└── 10-4-6_hands-on/
    └── debugging-app-practice/     ← 自分で作成する用（今ここ）
        ├── app/
        │   ├── Http/Controllers/
        │   └── Models/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

> 💡 **ポイント**: このハンズオンでは、Laravelのデフォルトの`users`テーブルを使用します。マイグレーションを実行すれば、テーブルは自動的に作成されます。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

```php
// dd()でデバッグ
dd($request->all());

// ログ出力
\Log::info('User created', ['user_id' => $user->id]);

// $fillableの設定
protected $fillable = ['name', 'email'];
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？デバッグは開発において不可欠なスキルです。一緒に手を動かしながら、エラーを特定して修正していきましょう。

> 📌 **注意**: ここからは`debugging-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### 💻 環境準備（実践用プロジェクト）

まず、**自分で作成する用のプロジェクトを停止**します：

```bash
# debugging-app-practiceディレクトリに移動
cd ~/coachtech/laravel-practice/10-4-6_hands-on/debugging-app-practice

# Sailを停止
./vendor/bin/sail down
```

次に、**実践用のプロジェクトを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/coachtech/laravel-practice/10-4-6_hands-on

# Laravel 10.xプロジェクトを作成（実践用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 debugging-app-sample
```

```bash
# プロジェクトディレクトリに移動
cd debugging-app-sample

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql

# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate

# データベースのマイグレーション
./vendor/bin/sail artisan migrate
```

**✅ ディレクトリ構造の確認**

```
~/coachtech/laravel-practice/
└── 10-4-6_hands-on/
    ├── debugging-app-practice/     ← 自分で作成した用（停止中）
    └── debugging-app-sample/       ← 実践用（今ここ、起動中）
        ├── app/
        │   ├── Http/Controllers/
        │   └── Models/
        └── ...
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

---

### 💭 実装の思考プロセス

デバッグを進める際、以下の順番で考えると効率的です：

1. **エラーメッセージを読む**：何が問題かを理解する
2. **dd()でデータを確認**：変数の中身を調べる
3. **ログを出力**：処理の流れを追跡する
4. **原因を特定**：エラーの根本原因を見つける
5. **修正してテスト**：修正後に動作を確認する

デバッグのポイントは「仮説を立てて検証し、一歩ずつ原因を絞り込む」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: エラーメッセージを読む

**何を考えているか**：
- 「エラーメッセージには重要な情報が含まれている」
- 「Mass assignmentエラーということは$fillableが設定されていない」
- 「まずはエラーの種類を理解しよう」

エラーメッセージの例：

```
Illuminate\Database\Eloquent\MassAssignmentException
Add [name] to fillable property to allow mass assignment on [App\Models\User].
```

**エラー分析**：

→ このエラーは「Mass Assignment」が原因です。Laravelはセキュリティ対策として、モデルの`$fillable`または`$guarded`で一括代入可能な属性を指定する必要があります。

---

#### ステップ2: dd()でデータを確認する

**何を考えているか**：
- 「リクエストデータが正しく送られているか確認しよう」
- 「dd()で処理を停止して変数を調べよう」
- 「期待する値が含まれているかチェックしよう」

コントローラーに`dd()`を追加します：

```php
public function store(Request $request)
{
    dd($request->all());
    
    $user = new User;
    $user->name = $request->name;
    $user->email = $request->email;
    $user->save();
    
    return redirect('/users');
}
```

**コード解説**：

```php
dd($request->all());
```
→ `dd()`（Dump and Die）でリクエストデータを表示し、処理を停止します。データの中身を確認できます。

---

#### ステップ3: ログを出力する

**何を考えているか**：
- 「処理の流れを追跡したい」
- 「本番環境でも使えるデバッグ手法が必要だ」
- 「ログファイルで後から確認できる」

コントローラーにログ出力を追加します：

```php
public function store(Request $request)
{
    \Log::info('User registration attempt', $request->all());
    
    $user = new User;
    $user->name = $request->name;
    $user->email = $request->email;
    $user->save();
    
    \Log::info('User created successfully', ['user_id' => $user->id]);
    
    return redirect('/users');
}
```

**コード解説**：

```php
\Log::info('User registration attempt', $request->all());
```
→ `\Log::info()`で情報レベルのログを出力します。第1引数はメッセージ、第2引数はコンテキストデータです。

```php
\Log::info('User created successfully', ['user_id' => $user->id]);
```
→ ユーザー作成後にログを出力します。処理が成功したことを記録します。

ログは`storage/logs/laravel.log`に出力されます。

---

#### ステップ4: 原因を特定して修正する

**何を考えているか**：
- 「Mass assignmentエラーの原因は$fillableが未設定」
- 「モデルに$fillableを追加しよう」
- 「セキュアにコードを書き換えよう」

`app/Models/User.php`を開いて、`$fillable`を追加します：

```php
protected $fillable = ['name', 'email', 'password'];
```

コントローラーを修正します：

```php
public function store(Request $request)
{
    \Log::info('User registration attempt', $request->all());
    
    $user = User::create([
        'name' => $request->name,
        'email' => $request->email,
        'password' => bcrypt($request->password),
    ]);
    
    \Log::info('User created successfully', ['user_id' => $user->id]);
    
    return redirect('/users');
}
```

**コード解説**：

```php
protected $fillable = ['name', 'email', 'password'];
```
→ `$fillable`で一括代入可能な属性を指定します。これによりMass assignmentエラーが解決します。

```php
$user = User::create([
    'name' => $request->name,
    'email' => $request->email,
    'password' => bcrypt($request->password),
]);
```
→ `User::create()`でユーザーを作成します。`bcrypt()`でパスワードをハッシュ化します。

---

#### ステップ5: 修正後にテストする

**何を考えているか**：
- 「修正が正しく動作するか確認しよう」
- 「ユーザー登録が成功するかテストしよう」
- 「ログを確認して処理の流れを追跡しよう」

テスト手順：

**tinkerでユーザー作成をテスト**：

```bash
sail artisan tinker
```

```php
>>> use App\Models\User;

// ユーザーを作成（$fillableが正しく設定されていれば成功）
>>> User::create([
...     'name' => 'テストユーザー',
...     'email' => 'test@example.com',
...     'password' => bcrypt('password'),
... ]);

// ユーザーが作成されたか確認
>>> User::all();

>>> exit
```

**ログファイルを確認**：

```bash
# ログの最後の10行を表示
tail -10 storage/logs/laravel.log
```

ログに`User registration attempt`と`User created successfully`が出力されていれば成功です。

---

### ✨ 完成！

これでデバッグ手法を実践できました！エラーメッセージを読み、dd()とログで原因を特定し、修正できましたね。

**自分で作成したコードと比較してみましょう**：
- `debugging-app-practice/`: 自分で作成したプロジェクト
- `debugging-app-sample/`: 一緒に作成したプロジェクト

両方のプロジェクトを見比べて、違いがあれば確認してみてください。

---

## 📖 模範解答

### 修正後のコード

```php
// User.php
protected $fillable = ['name', 'email', 'password'];

// UserController.php
public function store(Request $request)
{
    // デバッグ用
    \Log::info('User registration attempt', $request->all());
    
    $user = User::create([
        'name' => $request->name,
        'email' => $request->email,
        'password' => bcrypt($request->password),
    ]);
    
    \Log::info('User created successfully', ['user_id' => $user->id]);
    
    return redirect('/users');
}
```

### デバッグ手順

1. `dd($request->all())`でリクエストデータを確認
2. `\Log::info()`でログ出力
3. `storage/logs/laravel.log`でログを確認
4. `$fillable`を設定してMass assignment対策

---

## 🧪 動作確認の方法

### プロジェクトの切り替え

2つのプロジェクトを切り替えて動作確認する方法：

```bash
# debugging-app-practiceで確認したい場合
cd ~/coachtech/laravel-practice/10-4-6_hands-on/debugging-app-sample
./vendor/bin/sail down

cd ~/coachtech/laravel-practice/10-4-6_hands-on/debugging-app-practice
./vendor/bin/sail up -d

# debugging-app-sampleで確認したい場合
cd ~/coachtech/laravel-practice/10-4-6_hands-on/debugging-app-practice
./vendor/bin/sail down

cd ~/coachtech/laravel-practice/10-4-6_hands-on/debugging-app-sample
./vendor/bin/sail up -d
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ エラーメッセージを読んで問題を理解できる
- ✅ `dd()`でデータを確認してデバッグできる
- ✅ `\Log::info()`でログを出力して処理を追跡できる
- ✅ Mass assignmentエラーを修正できる

引き続き、次のセクションも頑張りましょう！

### 🛑 Sailの停止

次のセクションに進む前に、Sailを停止しておきましょう。

```bash
./vendor/bin/sail down
```

> 💡 **なぜ停止するの？**: Sailを起動したままだと、次のセクションで別のプロジェクトを起動する際にポートが競合してエラーになることがあります。セクションの終わりには必ずSailを停止する習慣をつけましょう。

---
