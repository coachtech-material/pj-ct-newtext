# Tutorial 9-10-1: デバッグツールの活用

## 🎯 このセクションで学ぶこと

*   Laravelのデバッグツール（`dd()`, `dump()`, `logger()`）を使えるようになる。
*   Laravel Debugbarを使って、SQLクエリやパフォーマンスを確認できるようになる。
*   エラーログの読み方を理解し、問題を特定できるようになる。

---

## 導入：バグは必ず発生する

プログラミングをしていると、必ず「思った通りに動かない」という状況に遭遇します。これは、初心者だけでなく、経験豊富な開発者でも同じです。重要なのは、**バグを素早く特定し、修正する能力**です。

Laravelには、デバッグを効率化するための強力なツールが用意されています。このセクションでは、それらのツールを使って、問題を素早く特定する方法を学びます。

---

## 詳細解説

### 🔍 `dd()`と`dump()`

Laravelで最もよく使われるデバッグツールは、`dd()`（Dump and Die）と`dump()`です。

#### `dd()` - 変数の内容を表示して処理を停止

`dd()`は、変数の内容を見やすく表示し、その場で処理を停止します。

```php
$user = User::find(1);
dd($user);
```

**実行結果のイメージ**

```
App\Models\User {#1234
  id: 1
  name: "山田太郎"
  email: "taro@example.com"
  created_at: "2024-12-11 12:00:00"
  updated_at: "2024-12-11 12:00:00"
}
```

処理はここで停止し、以降のコードは実行されません。

#### `dump()` - 変数の内容を表示して処理を継続

`dump()`は、変数の内容を表示しますが、処理は継続します。

```php
$user = User::find(1);
dump($user);

$posts = Post::all();
dump($posts);
```

複数の変数をデバッグしたい場合に便利です。

---

### 📊 SQLクエリのデバッグ

Eloquent ORMは、内部的にSQLクエリを生成しています。「どんなSQLが実行されているか」を確認することで、パフォーマンスの問題やバグを特定できます。

#### 方法1: `toSql()`メソッド

```php
$query = User::where('is_admin', true)->orderBy('created_at', 'desc');
dd($query->toSql());
```

**実行結果**

```
"select * from `users` where `is_admin` = ? order by `created_at` desc"
```

ただし、`?`の部分には実際の値が表示されません。

#### 方法2: `DB::enableQueryLog()`

```php
use Illuminate\Support\Facades\DB;

DB::enableQueryLog();

$users = User::where('is_admin', true)->get();

dd(DB::getQueryLog());
```

**実行結果**

```php
[
    [
        "query" => "select * from `users` where `is_admin` = ?",
        "bindings" => [1],
        "time" => 2.5
    ]
]
```

これにより、実際の値（`bindings`）と実行時間（`time`）も確認できます。

---

### 🛠️ Laravel Debugbar

Laravel Debugbarは、開発中にSQLクエリ、パフォーマンス、ログなどを画面下部に表示してくれる便利なツールです。

#### インストール

```bash
docker compose exec php composer require barryvdh/laravel-debugbar --dev
```

`--dev`オプションを付けることで、開発環境でのみインストールされます。

#### 使い方

インストール後、ブラウザでアプリケーションにアクセスすると、画面下部にDebugbarが表示されます。

**Debugbarで確認できる情報**

*   **Timeline**: リクエストの処理時間
*   **Queries**: 実行されたSQLクエリと実行時間
*   **Models**: Eloquentで取得したモデルの一覧
*   **Route**: 現在のルート情報
*   **Views**: レンダリングされたビューの一覧
*   **Logs**: ログメッセージ

特に、**Queries**タブは、N+1問題を発見するのに非常に役立ちます。

---

### 📝 ログの活用

Laravelは、エラーやデバッグ情報を`storage/logs/laravel.log`に記録します。

#### ログの書き込み

```php
use Illuminate\Support\Facades\Log;

Log::info('ユーザーがログインしました', ['user_id' => $user->id]);
Log::warning('不正なアクセスを検知しました', ['ip' => $request->ip()]);
Log::error('データベース接続に失敗しました', ['error' => $e->getMessage()]);
```

#### ログレベル

| レベル | 説明 | 用途 |
|:---|:---|:---|
| `emergency` | システムが使用不可能 | 致命的なエラー |
| `alert` | 即座に対応が必要 | データベース全体がダウン |
| `critical` | 重大な状態 | アプリケーションコンポーネントが利用不可 |
| `error` | エラー | 例外が発生 |
| `warning` | 警告 | 非推奨のAPIを使用 |
| `notice` | 通知 | 通常だが重要なイベント |
| `info` | 情報 | ユーザーのログイン |
| `debug` | デバッグ | 詳細なデバッグ情報 |

#### ログの確認

```bash
docker compose exec php tail -f storage/logs/laravel.log
```

これにより、リアルタイムでログを監視できます。

---

### 🚨 エラーページの読み方

Laravelでエラーが発生すると、詳細なエラーページが表示されます。

**エラーページの構成**

1. **エラーメッセージ**: 何が起こったか
2. **スタックトレース**: エラーが発生した場所と、そこに至るまでの関数呼び出しの履歴
3. **リクエスト情報**: HTTPメソッド、URL、パラメータ

**スタックトレースの読み方**

```
ErrorException: Undefined variable $user

at app/Http/Controllers/UserController.php:25
   21|     public function show($id)
   22|     {
   23|         $post = Post::find($id);
   24|
>  25|         return view('users.show', compact('user'));
   26|     }
```

この例では、`UserController.php`の25行目で、`$user`という変数が定義されていないことが原因です。

---

### 💡 TIP: `dd()`のバリエーション

Laravelには、`dd()`のバリエーションがいくつかあります。

*   `ddd()`: 複数の変数をダンプして停止
*   `ray()`: Ray（有料デバッグツール）に情報を送信
*   `dump()`: 変数をダンプして処理を継続

---

## ✨ まとめ

このセクションでは、Laravelのデバッグツールの活用方法を学びました。

*   `dd()`は、変数の内容を表示して処理を停止する。
*   `dump()`は、変数の内容を表示して処理を継続する。
*   `toSql()`や`DB::getQueryLog()`を使って、実行されたSQLクエリを確認できる。
*   Laravel Debugbarを使うと、SQLクエリやパフォーマンスを視覚的に確認できる。
*   `Log`ファサードを使って、ログを記録できる。
*   エラーページのスタックトレースを読むことで、問題の原因を特定できる。

次のセクションでは、エラーハンドリングとカスタムエラーページの作成方法を学びます。

---
