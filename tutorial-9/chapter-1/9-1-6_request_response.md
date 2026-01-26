# Tutorial 9-1-6: リクエストとレスポンスの基礎

## 🎯 このセクションで学ぶこと

- HTTPリクエストとレスポンスの概念を理解する
- `Request`オブジェクトを使って、ユーザーからの入力データを取得できるようになる
- **「入力 → 処理 → 出力」というWebアプリの基本サイクル**を体験する

> **📌 このセクションのポイント**
> 
> このセクションでは、**データベースは使いません**。
> 「ユーザーの入力が、どうやってコントローラーに届き、どうやって画面に返されるか」という**データの流れ**に集中して学びます。

---

## 導入：Webアプリケーションの「会話」

Webアプリケーションは、ユーザー（ブラウザ）とサーバーの「会話」で成り立っています。

```
【ユーザー】                    【サーバー】
    |                              |
    |  ① リクエスト（お願い）       　|
    | ─────────────────────────→   |
    |  「名前を送るよ」            　 |
    |                              |
    |  ② レスポンス（返事）    　  　 |
    | ←─────────────────────────   |
    |  「こんにちは、〇〇さん」        |
    |                              |
```

1. **リクエスト（Request）**: ユーザーがブラウザでURLにアクセスしたり、フォームを送信したりすると、サーバーに「リクエスト」が送られます。
2. **レスポンス（Response）**: サーバーはリクエストを処理し、HTMLページやJSONデータなどの「レスポンス」を返します。

Laravelでは、この「リクエスト」と「レスポンス」を簡単に扱うための機能が用意されています。

---

## 🎯 実践フロー：挨拶アプリを作ろう

**データベースを使わずに**、リクエストとレスポンスの流れを体験しましょう。

### 完成イメージ

1. **入力画面**: 名前を入力するフォーム
2. **結果画面**: 「こんにちは、〇〇さん！」と表示

```
【入力画面】                    【結果画面】
┌─────────────────┐           ┌─────────────────┐
│  名前を入力  　   │           │                 │
│  ┌───────────┐  │   送信  　 │  こんにちは、     │
│  │ 山田太郎 　 │　│  ───→     │  山田太郎さん！　　│
│  └───────────┘  │           │                 │
│  [送信]       　 │           │  [戻る]   　     │
└─────────────────┘           └─────────────────┘
```

---

### Step 1: ルーティングを定義する

まず、2つのルートを定義します。

**`routes/web.php`**

```php
<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\GreetingController;

Route::get('/', function () {
    return view('welcome');
});

// 挨拶アプリのルーティング
Route::get('/greeting', [GreetingController::class, 'showForm'])->name('greeting.form');
Route::post('/greeting', [GreetingController::class, 'greet'])->name('greeting.greet');
```

| URL | メソッド | 名前 | 処理 |
|:---|:---|:---|:---|
| `/greeting` | GET | `greeting.form` | 入力フォームを表示 |
| `/greeting` | POST | `greeting.greet` | 名前を受け取って挨拶を表示 |

> **💡 ポイント**
> 
> 同じURL `/greeting` でも、**HTTPメソッドが違えば別のルート**として扱われます。
> - GET: フォームを「見せて」
> - POST: データを「受け取って」

---

### Step 2: コントローラーを作成する

**ターミナルでプロジェクトのルートディレクトリに移動**してから、以下のコマンドを実行します。

> **📌 コマンドの実行場所**
> 
> `sail artisan`コマンドは、**Laravelプロジェクトのルートディレクトリ**（`docker-compose.yml`があるディレクトリ）で実行する必要があります。
> ```bash
> # 例: プロジェクトディレクトリに移動
> cd ~/coachtech/laravel-practice
> ```

```bash
sail artisan make:controller GreetingController
```

このコマンドを実行すると、`app/Http/Controllers/GreetingController.php`が自動生成されます。

**`app/Http/Controllers/GreetingController.php`**

```php
<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class GreetingController extends Controller
{
    /**
     * 入力フォームを表示する（GET /greeting）
     */
    public function showForm()
    {
        return view('greeting.form');
    }

    /**
     * 名前を受け取って挨拶を表示する（POST /greeting）
     */
    public function greet(Request $request)
    {
        // ① リクエストから名前を取得
        $name = $request->input('name');

        // ② ビューにデータを渡して表示
        return view('greeting.result', ['name' => $name]);
    }
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `use Illuminate\Http\Request;` | `Request`クラスをインポート |
| `Request $request` | Laravelが自動的にリクエスト情報を渡してくれる |
| `$request->input('name')` | フォームから送信された`name`フィールドの値を取得 |
| `return view('greeting.result', ['name' => $name])` | 取得した名前をビューに渡す |

---

### Step 3: 入力フォームを作成する

まず、ビューファイルを配置するディレクトリを作成します。

> **📌 ディレクトリの作成**
> 
> `resources/views/greeting/`ディレクトリはまだ存在しないので、新しく作成する必要があります。
> 
> **方法1: ターミナルで作成**
> ```bash
> mkdir -p resources/views/greeting
> ```
> 
> **方法2: エディタ（VSCodeなど）で作成**
> `resources/views/`フォルダを右クリックして「新しいフォルダ」を選択し、`greeting`と入力します。

次に、`greeting`ディレクトリ内に`form.blade.php`ファイルを作成します。

> **💡 Bladeテンプレートについて**
> 
> 以下のコードには`@csrf`や`{{ }}`などの**Blade構文**が含まれています。
> Bladeの詳細は**次のChapter（Chapter 2: ビューとBlade）**で学びます。
> 今は「こういう書き方をするんだな」と思いながら、**コピペでOK**です。

**`resources/views/greeting/form.blade.php`**

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>挨拶アプリ</title>
    <style>
        body {
            font-family: sans-serif;
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
        }
        h1 {
            color: #333;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input[type="text"] {
            width: 100%;
            padding: 10px;
            font-size: 16px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <h1>挨拶アプリ</h1>
    
    {{-- フォームの送信先を名前付きルートで指定 --}}
    <form action="{{ route('greeting.greet') }}" method="POST">
        {{-- CSRFトークン（セキュリティ対策） --}}
        @csrf
        
        <div class="form-group">
            <label for="name">お名前を入力してください</label>
            <input type="text" id="name" name="name" placeholder="例: 山田太郎">
        </div>
        
        <button type="submit">送信</button>
    </form>
</body>
</html>
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `action="{{ route('greeting.greet') }}"` | フォームの送信先を名前付きルートで指定 |
| `method="POST"` | POSTメソッドでデータを送信 |
| `@csrf` | CSRF対策のトークンを自動生成（Laravelのセキュリティ機能） |
| `name="name"` | この名前でコントローラーがデータを受け取る |

> **📌 @csrf について**
> 
> `@csrf`は、悪意のある第三者からの不正なリクエストを防ぐためのセキュリティ対策です。
> LaravelでPOSTフォームを作成する際は、**必ず`@csrf`を入れる**ことを覚えておきましょう。

---

### Step 4: 結果画面を作成する

同じ`greeting`ディレクトリ内に、`result.blade.php`ファイルを新規作成します。

> **📌 ファイルの作成方法**
> 
> **方法1: ターミナルで作成**
> ```bash
> touch resources/views/greeting/result.blade.php
> ```
> 
> **方法2: エディタ（VSCodeなど）で作成**
> `resources/views/greeting/`フォルダを右クリックして「新しいファイル」を選択し、`result.blade.php`と入力します。

**`resources/views/greeting/result.blade.php`**

```blade
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>挨拶</title>
    <style>
        body {
            font-family: sans-serif;
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
            text-align: center;
        }
        h1 {
            color: #333;
        }
        .greeting {
            font-size: 24px;
            color: #007bff;
            margin: 30px 0;
        }
        a {
            color: #007bff;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <h1>挨拶</h1>
    
    <p class="greeting">
        こんにちは、{{ $name }}さん！
    </p>
    
    {{-- 戻るリンクも名前付きルートで --}}
    <a href="{{ route('greeting.form') }}">← 戻る</a>
</body>
</html>
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `{{ $name }}` | コントローラーから渡された`$name`を表示 |
| `route('greeting.form')` | 入力フォームへのリンクを名前付きルートで生成 |

---

### Step 5: ブラウザで確認する

1. ブラウザで `http://localhost/greeting` にアクセス
2. 名前を入力して「送信」ボタンをクリック
3. 「こんにちは、〇〇さん！」と表示されれば成功！

---

### データの流れを確認しよう

```
① ユーザーが /greeting にアクセス（GET）
       ↓
② ルーティングが greeting.form を見つける
       ↓
③ GreetingController の showForm() が実行される
       ↓
④ form.blade.php が表示される
       ↓
⑤ ユーザーが名前を入力して送信（POST）
       ↓
⑥ ルーティングが greeting.greet を見つける
       ↓
⑦ GreetingController の greet() が実行される
       ↓
⑧ $request->input('name') で名前を取得
       ↓
⑨ result.blade.php に名前を渡して表示
```

> **📌 これがWebアプリの基本サイクル！**
> 
> **入力（Request）→ 処理（Controller）→ 出力（Response）**
> 
> この流れを理解することが、Laravelを使いこなす第一歩です。

---

## 📥 リクエストの詳細

### Requestオブジェクトとは

`Request`オブジェクトには、ユーザーからのリクエストに関する様々な情報が含まれています。

| 情報 | 説明 | 例 |
|:---|:---|:---|
| **URL** | アクセス先のURL | `/greeting` |
| **HTTPメソッド** | リクエストの種類 | GET, POST |
| **フォームデータ** | POSTで送信されたデータ | `name=山田太郎` |
| **クエリパラメータ** | URLの`?`以降のパラメータ | `?page=2` |

---

### フォームデータの取得方法

#### `input()` - 値を取得する（最も基本的）

```php
// 'name'フィールドの値を取得
$name = $request->input('name');

// デフォルト値を指定（値がない場合に使用）
$name = $request->input('name', 'ゲスト');
```

#### `all()` - 全ての入力データを取得

```php
// 全てのフォームデータを配列で取得
$data = $request->all();
// 例: ['name' => '山田太郎', 'email' => 'yamada@example.com']
```

#### `only()` - 指定したフィールドのみ取得

```php
// 'name'と'email'のみ取得
$data = $request->only(['name', 'email']);
```

---

### 値の存在チェック

#### `has()` - キーが存在するか確認

```php
if ($request->has('name')) {
    // 'name'キーが存在する（値が空でも true）
}
```

#### `filled()` - 値が空でないか確認

```php
if ($request->filled('name')) {
    // 'name'が存在し、かつ空でない
}
```

| メソッド | 値がない | 値が空文字 | 値がある |
|:---|:---|:---|:---|
| `has()` | false | true | true |
| `filled()` | false | false | true |

---

## 📤 レスポンスの種類

コントローラーのメソッドは、様々な形式でレスポンスを返すことができます。

### 1. ビューを返す（最も一般的）

```php
// シンプルにビューを返す
return view('greeting.form');

// データをビューに渡す（配列形式）
return view('greeting.result', ['name' => $name]);

// compact()を使う（変数名と同じキーで渡す）
return view('greeting.result', compact('name'));
```

> **📌 compact()関数とは？**
> 
> `compact()`はPHPの組み込み関数で、**変数名をキー、変数の値を値とする配列**を作成します。
> 
> ```php
> $name = '山田太郎';
> $age = 25;
> 
> // compact()を使う場合
> return view('profile', compact('name', 'age'));
> 
> // ↑ これは以下と同じ意味 ↓
> return view('profile', ['name' => $name, 'age' => $age]);
> ```
> 
> | 書き方 | 特徴 |
> |:---|:---|
> | `['name' => $name]` | キー名と変数名を自由に指定できる |
> | `compact('name')` | 変数名とキー名が同じ場合に短く書ける |
> 
> どちらを使ってもOKですが、チームで統一しておくと読みやすくなります。

### 2. リダイレクトする

別のページに転送します。

```php
// 名前付きルートにリダイレクト
return redirect()->route('greeting.form');

// フラッシュメッセージ付きでリダイレクト
return redirect()->route('greeting.form')
    ->with('success', '送信しました');
```

**フラッシュメッセージの表示（Blade）**

```blade
@if (session('success'))
    <div style="color: green;">
        {{ session('success') }}
    </div>
@endif
```

### 3. JSONを返す（API用）

```php
return response()->json([
    'message' => '成功しました',
    'name' => $name
]);
```

---

## 🔄 挨拶アプリを改良してみよう

基本の流れが理解できたら、以下の改良に挑戦してみましょう。

### 改良1: 空の名前をチェックする

```php
public function greet(Request $request)
{
    $name = $request->input('name');

    // 名前が空の場合はデフォルト値を使用
    if (empty($name)) {
        $name = 'ゲスト';
    }

    return view('greeting.result', ['name' => $name]);
}
```

### 改良2: 時間帯によって挨拶を変える

```php
public function greet(Request $request)
{
    $name = $request->input('name', 'ゲスト');
    $hour = now()->hour;

    if ($hour < 12) {
        $greeting = 'おはようございます';
    } elseif ($hour < 18) {
        $greeting = 'こんにちは';
    } else {
        $greeting = 'こんばんは';
    }

    return view('greeting.result', [
        'name' => $name,
        'greeting' => $greeting
    ]);
}
```

```blade
{{-- result.blade.php --}}
<p class="greeting">
    {{ $greeting }}、{{ $name }}さん！
</p>
```

---

## ✨ まとめ

このセクションでは、**データベースを使わずに**リクエストとレスポンスの基本的な流れを体験しました。

| Step | 内容 | ファイル |
|:---|:---|:---|
| 1 | ルーティングを定義 | `routes/web.php` |
| 2 | コントローラーを作成 | `GreetingController.php` |
| 3 | 入力フォームを作成 | `greeting/form.blade.php` |
| 4 | 結果画面を作成 | `greeting/result.blade.php` |
| 5 | ブラウザで確認 | `http://localhost/greeting` |

### 学んだこと

| 項目 | 内容 |
|:---|:---|
| **リクエスト** | ユーザーからサーバーへの要求（フォームデータなど） |
| **レスポンス** | サーバーからユーザーへの応答（ビュー、リダイレクトなど） |
| **$request->input()** | フォームから送信されたデータを取得 |
| **view()** | ビューを返すヘルパー。第2引数でデータを渡せる |
| **compact()** | 変数名をキーとする配列を作成するPHP関数 |
| **@csrf** | POSTフォームに必須のセキュリティ対策 |
| **route()** | 名前付きルートからURLを生成 |

> **📌 ポイント**
> 
> **入力（Request）→ 処理（Controller）→ 出力（Response）**
> 
> この「データのバケツリレー」がWebアプリケーションの基本です。
> データベースを使う場合も、この流れは変わりません。
> 
> 次のセクションでは、実際に手を動かしてページを作成するハンズオンを行います。

---
