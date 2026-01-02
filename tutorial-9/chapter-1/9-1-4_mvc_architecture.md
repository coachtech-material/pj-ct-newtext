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

この流れを、具体的なコード例で見ていきましょう。

---

### 🔍 具体例：ユーザー一覧を表示する

「全てのユーザーをデータベースから取得し、一覧として表示する」という機能を、MVCアーキテクチャで実装してみます。

#### ステップ1: ルーティングを定義する（`routes/web.php`）

まず、URLとコントローラーを紐付けます。

```php
<?php
use App\Http\Controllers\UserController;

Route::get('/users', [UserController::class, 'index']);
```

この定義により、「`/users`というURLにGETリクエストが来たら、`UserController`クラスの`index`メソッドを実行する」という動作が設定されます。

#### ステップ2: Controller（コントローラー）を作成する

`app/Http/Controllers/UserController.php`を作成します。

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
*   `view('users.index', compact('users'))`: `resources/views/users/index.blade.php`というビューファイルを読み込み、`$users`という変数をビューに渡します。`compact('users')`は、`['users' => $users]`と同じ意味です。

#### ステップ3: Model（モデル）を確認する

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

#### ステップ4: View（ビュー）を作成する

`resources/views/users/index.blade.php`を作成します。

```blade
<!DOCTYPE html>
<html>
<head>
    <title>ユーザー一覧</title>
</head>
<body>
    <h1>ユーザー一覧</h1>
    <ul>
        @foreach ($users as $user)
            <li>{{ $user->name }} ({{ $user->email }})</li>
        @endforeach
    </ul>
</body>
</html>
```

**コードリーディング**

*   `@foreach ($users as $user)`: コントローラーから渡された`$users`配列をループします。
*   `{{ $user->name }}`: `$user`オブジェクトの`name`プロパティを表示します。`{{ }}`は、自動的にHTMLエスケープを行い、XSS攻撃を防ぎます。
*   `@endforeach`: ループの終了を示します。

#### ステップ5: ブラウザでアクセスする

ブラウザで`http://localhost:8080/users`にアクセスすると、データベースから取得したユーザーの一覧が表示されます。

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
*   データの流れは、「ルーティング → コントローラー → モデル → データベース → モデル → コントローラー → ビュー → ブラウザ」という順序で進む。
*   MVCで役割を分けることで、変更の影響範囲が限定され、コードの再利用性が高まり、チーム開発がしやすくなる。

次のセクションでは、MVCの最初のステップである「ルーティング」について、より詳しく学んでいきます。

---
