# Tutorial 9-1-4: MVCアーキテクチャ

## 🎯 このセクションで学ぶこと

*   MVCアーキテクチャ（Model-View-Controller）の概念を理解する。
*   Model、View、Controllerがそれぞれどのような役割を持ち、どのように連携するのかを説明できるようになる。
*   Laravelにおける「データの流れ」を、MVCの観点から理解する。

---

## 導入：なぜ「役割分担」が重要なのか？

前のセクションで、Laravelのディレクトリ構成を学びました。その中で、`app/Http/Controllers/`（コントローラー）、`app/Models/`（モデル）、`resources/views/`（ビュー）という3つのディレクトリが頻繁に登場しました。これらは、Laravelが採用している**MVCアーキテクチャ**という設計思想に基づいています。

MVCとは、**Model（モデル）**、**View（ビュー）**、**Controller（コントローラー）**の頭文字を取ったもので、Webアプリケーションを3つの役割に分けて設計する手法です。

なぜ、わざわざ役割を分けるのでしょうか？それは、**コードの保守性と拡張性を高めるため**です。もし全てのコードを1つのファイルに書いてしまうと、以下のような問題が起こります。

*   コードが長くなり、どこに何が書いてあるか分からなくなる
*   一部を修正すると、他の部分に予期しない影響が出る
*   チームで開発する際に、誰がどこを担当するか決めにくい

MVCアーキテクチャは、これらの問題を解決し、「データの処理」「画面の表示」「リクエストの制御」を明確に分離することで、読みやすく、変更しやすいコードを実現します。

---

## 詳細解説

### 🏗️ MVCアーキテクチャの全体像

MVCアーキテクチャは、以下の3つの要素で構成されます。

| 要素 | 役割 | Laravelでの配置場所 |
|:---|:---|:---|
| **Model（モデル）** | データベースとのやり取りを担当。データの取得・作成・更新・削除を行う。 | `app/Models/` |
| **View（ビュー）** | ユーザーに表示する画面（HTML）を担当。データを受け取り、整形して表示する。 | `resources/views/` |
| **Controller（コントローラー）** | リクエストを受け取り、モデルとビューを橋渡しする。処理の流れを制御する。 | `app/Http/Controllers/` |

これらの要素は、以下のような流れで連携します。

```
1. ユーザーがブラウザでURLにアクセス（例：/users）
   ↓
2. ルーティング（routes/web.php）が、URLとコントローラーを紐付ける
   ↓
3. Controller（コントローラー）が、リクエストを受け取る
   ↓
4. Controller が、Model（モデル）にデータの取得を依頼
   ↓
5. Model が、データベースからデータを取得し、Controller に返す
   ↓
6. Controller が、取得したデータを View（ビュー）に渡す
   ↓
7. View が、データを使ってHTMLを生成し、ブラウザに返す
   ↓
8. ユーザーのブラウザに画面が表示される
```

この流れを、具体的なコード例で見ていきましょう。まずは**データベースを使わない**シンプルな例から始め、その後で**データベースを使う**例に進みます。

---

## 🔍 具体例①：シンプルなページを表示する（データベース不使用）

まずは、MVCの基本的な流れを理解するために、**データベースを使わない**シンプルな例から始めましょう。「ようこそページ」を表示する機能を実装します。

### ステップ1: ルーティングを定義する（`routes/web.php`）

まず、URLとコントローラーを紐付けます。

```php
<?php
use App\Http\Controllers\WelcomeController;

Route::get('/welcome', [WelcomeController::class, 'index']);
```

この定義により、「`/welcome`というURLにGETリクエストが来たら、`WelcomeController`クラスの`index`メソッドを実行する」という動作が設定されます。

### ステップ2: Controller（コントローラー）を作成する

ターミナルで以下のコマンドを実行し、コントローラーを作成します。

```bash
sail artisan make:controller WelcomeController
```

`app/Http/Controllers/WelcomeController.php`が作成されるので、以下のように編集します。

```php
<?php
namespace App\Http\Controllers;

class WelcomeController extends Controller
{
    public function index()
    {
        // データを準備（この段階ではデータベースを使わない）
        $message = 'Laravelへようこそ！';
        $currentTime = now()->format('Y年m月d日 H:i');

        // View にデータを渡す
        return view('welcome-page', compact('message', 'currentTime'));
    }
}
```

**コードリーディング**

*   `$message = 'Laravelへようこそ！';`: 表示するメッセージを変数に格納します。
*   `now()->format('Y年m月d日 H:i')`: Laravelのヘルパー関数`now()`で現在時刻を取得し、フォーマットします。
*   `view('welcome-page', compact('message', 'currentTime'))`: `resources/views/welcome-page.blade.php`というビューファイルを読み込み、`$message`と`$currentTime`をビューに渡します。

### ステップ3: View（ビュー）を作成する

`resources/views/welcome-page.blade.php`を作成します。

```blade
<!DOCTYPE html>
<html>
<head>
    <title>ようこそ</title>
</head>
<body>
    <h1>{{ $message }}</h1>
    <p>現在時刻: {{ $currentTime }}</p>
</body>
</html>
```

**コードリーディング**

*   `{{ $message }}`: コントローラーから渡された`$message`変数を表示します。
*   `{{ $currentTime }}`: コントローラーから渡された`$currentTime`変数を表示します。
*   `{{ }}`は、自動的にHTMLエスケープを行い、XSS攻撃を防ぎます。

### ステップ4: ブラウザでアクセスする

ブラウザで`http://localhost/welcome`にアクセスすると、「Laravelへようこそ！」というメッセージと現在時刻が表示されます。

**[ここに、ようこそページのスクリーンショットを挿入]**

> 💡 **ポイント**: この例では、データベースを使わずに、コントローラーで直接データを準備してビューに渡しています。これが、MVCの最も基本的な流れです。

---

## 🔍 具体例②：ユーザー一覧を表示する（データベース使用）

次に、**データベースを使う**例を見ていきましょう。「全てのユーザーをデータベースから取得し、一覧として表示する」という機能を実装します。

> ⚠️ **重要**: この例では、データベースからデータを取得します。そのため、**事前にデータベースのテーブルを作成する必要があります**。テーブルが存在しない状態でアクセスすると、500エラーが発生します。

### 事前準備：マイグレーションの実行

Laravelでは、データベースのテーブルを「**マイグレーション**」という仕組みで管理します。マイグレーションについては、Chapter 3で詳しく学びますが、ここでは最低限の手順だけ説明します。

Laravelをインストールすると、`users`テーブルを作成するためのマイグレーションファイルが最初から用意されています（`database/migrations/xxxx_create_users_table.php`）。このファイルを使って、テーブルを作成します。

```bash
sail artisan migrate
```

このコマンドを実行すると、以下のような出力が表示されます。

```
Migration table created successfully.
Running migrations...
   2014_10_12_000000_create_users_table .............. DONE
   2014_10_12_100000_create_password_reset_tokens_table  DONE
   2019_08_19_000000_create_failed_jobs_table ........ DONE
   2019_12_14_000001_create_personal_access_tokens_table DONE
```

これで、`users`テーブルがデータベースに作成されました。phpMyAdmin（`http://localhost:8080`）でテーブルが作成されていることを確認できます。

> ⚠️ **マイグレーションを実行しないとどうなる？**
> 
> マイグレーションを実行せずに、`User::all()`を含むページにアクセスすると、以下のようなエラーが発生します。
> 
> ```
> SQLSTATE[42S02]: Base table or view not found: 1146 Table 'laravel.users' doesn't exist
> ```
> 
> これは、「`users`テーブルが存在しない」というエラーです。データベースを使う機能を実装する前に、必ずマイグレーションを実行してテーブルを作成してください。

### ステップ1: ルーティングを定義する（`routes/web.php`）

```php
<?php
use App\Http\Controllers\UserController;

Route::get('/users', [UserController::class, 'index']);
```

### ステップ2: Controller（コントローラー）を作成する

```bash
sail artisan make:controller UserController
```

`app/Http/Controllers/UserController.php`を以下のように編集します。

```php
<?php
namespace App\Http\Controllers;

use App\Models\User;

class UserController extends Controller
{
    public function index()
    {
        // Model（User）にデータ取得を依頼
        $users = User::all();

        // View（users.index）にデータを渡す
        return view('users.index', compact('users'));
    }
}
```

**コードリーディング**

*   `use App\Models\User;`: `User`モデルをインポートします。
*   `User::all()`: `User`モデルの`all()`メソッドを呼び出し、データベースから全てのユーザーを取得します。これは、SQLの`SELECT * FROM users`に相当します。
*   `view('users.index', compact('users'))`: `resources/views/users/index.blade.php`というビューファイルを読み込み、`$users`という変数をビューに渡します。

### ステップ3: Model（モデル）を確認する

`app/Models/User.php`は、Laravelインストール時に自動生成されています。

```php
<?php
namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable
{
    // テーブル名は自動的に「users」と推測される
    // $fillable などの設定は後のセクションで学びます
}
```

**重要なポイント**

*   `User`モデルは、`users`テーブルと対応しています。Laravelは、クラス名を複数形・小文字にしたものをテーブル名として自動的に推測します（`User` → `users`）。
*   `User::all()`を呼び出すと、Eloquent ORMが内部的に`SELECT * FROM users`というSQLを実行し、結果をPHPのオブジェクトとして返します。

### ステップ4: View（ビュー）を作成する

`resources/views/users/index.blade.php`を作成します。まず、`users`ディレクトリを作成してください。

```bash
mkdir resources/views/users
```

そして、`resources/views/users/index.blade.php`を作成します。

```blade
<!DOCTYPE html>
<html>
<head>
    <title>ユーザー一覧</title>
</head>
<body>
    <h1>ユーザー一覧</h1>
    
    @if ($users->isEmpty())
        <p>ユーザーが登録されていません。</p>
    @else
        <ul>
            @foreach ($users as $user)
                <li>{{ $user->name }} ({{ $user->email }})</li>
            @endforeach
        </ul>
    @endif
</body>
</html>
```

**コードリーディング**

*   `@if ($users->isEmpty())`: ユーザーが0件の場合の処理を分岐します。
*   `@foreach ($users as $user)`: コントローラーから渡された`$users`配列をループします。
*   `{{ $user->name }}`: `$user`オブジェクトの`name`プロパティを表示します。

### ステップ5: ブラウザでアクセスする

ブラウザで`http://localhost/users`にアクセスすると、ユーザー一覧が表示されます。

まだユーザーを登録していない場合は、「ユーザーが登録されていません。」と表示されます。phpMyAdminから手動でユーザーを追加するか、後のセクションで学ぶシーダーを使ってテストデータを投入することで、一覧が表示されるようになります。

**[ここに、ユーザー一覧画面のスクリーンショットを挿入]**

---

### 🔄 データの流れを図解する

上記の例を、図で表すと以下のようになります。

```
[ブラウザ]
   ↓ GET /users
[ルーティング (routes/web.php)]
   ↓ UserController@index を呼び出す
[Controller (UserController.php)]
   ↓ User::all() を呼び出す
[Model (User.php)]
   ↓ SELECT * FROM users を実行
[データベース (MySQL)]
   ↑ ユーザーデータを返す
[Model (User.php)]
   ↑ データをオブジェクトに変換して返す
[Controller (UserController.php)]
   ↓ view('users.index', compact('users')) を呼び出す
[View (users/index.blade.php)]
   ↓ HTMLを生成
[ブラウザ]
   ← HTMLが表示される
```

この流れを理解することが、Laravelでの開発において最も重要です。

---

### 🧩 MVCの役割分担のメリット

MVCアーキテクチャで役割を分けることで、以下のようなメリットがあります。

#### 1. **変更の影響範囲が限定される**

例えば、「ユーザー一覧の表示を、リストからテーブル形式に変更したい」という場合、変更するのはビュー（`users/index.blade.php`）だけです。コントローラーやモデルを触る必要はありません。

逆に、「データベースのテーブル名を変更したい」という場合は、モデルだけを修正すれば、コントローラーやビューには影響しません。

#### 2. **コードの再利用性が高まる**

同じモデル（`User::all()`）を、複数のコントローラーやビューで使い回すことができます。例えば、「管理画面のユーザー一覧」と「API用のユーザー一覧」で、同じモデルを使うことができます。

#### 3. **チーム開発がしやすくなる**

デザイナーはビューを担当し、バックエンドエンジニアはコントローラーとモデルを担当する、といった役割分担が明確になります。

---

## 💡 TIP: MVCは「絶対的なルール」ではない

MVCアーキテクチャは、あくまで「設計の指針」であり、絶対的なルールではありません。実際の開発では、MVCだけでは表現しきれない複雑な処理も出てきます。

Laravelでは、MVCに加えて、以下のような要素も使われます。

*   **Service（サービス）**: 複雑なビジネスロジックをコントローラーから分離する
*   **Repository（リポジトリ）**: データベースアクセスのロジックをモデルから分離する
*   **Middleware（ミドルウェア）**: リクエストの前後処理を行う

これらは、より高度な設計パターンであり、後のチュートリアルで学びます。今は、「MVC」という基本的な役割分担を理解することが重要です。

---

## ✨ まとめ

このセクションでは、MVCアーキテクチャの概念と、Laravelにおけるデータの流れを学びました。

*   MVCアーキテクチャは、Model（データ）、View（表示）、Controller（制御）の3つに役割を分ける設計思想である。
*   **Model**は、データベースとのやり取りを担当し、`app/Models/`に配置される。
*   **View**は、HTMLの生成を担当し、`resources/views/`に配置される。
*   **Controller**は、リクエストを受け取り、モデルとビューを橋渡しする役割を持ち、`app/Http/Controllers/`に配置される。
*   MVCの学習は、**まずデータベースを使わない例**から始め、**その後でデータベースを使う例**に進むと理解しやすい。
*   データベースを使う場合は、**事前にマイグレーションを実行**してテーブルを作成する必要がある。
*   MVCで役割を分けることで、変更の影響範囲が限定され、コードの再利用性が高まり、チーム開発がしやすくなる。

次のセクションでは、MVCの最初のステップである「ルーティング」について、より詳しく学んでいきます。

---
