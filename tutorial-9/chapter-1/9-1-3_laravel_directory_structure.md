# Tutorial 9-1-3: Laravelのディレクトリ構成

## 🎯 このセクションで学ぶこと

- Laravelプロジェクトで**よく触るディレクトリとファイル**を把握する
- 開発時に必要なファイルがどこにあるかを理解する

---

## 導入：全てを覚える必要はない

Laravelプロジェクトには大量のフォルダとファイルがありますが、**実際に触るのはごく一部**です。

このセクションでは、開発で**本当に必要なディレクトリとファイルだけ**を紹介します。

---

## 📁 よく触るディレクトリとファイル

### 全体像

```
src/
├── app/
│   ├── Http/Controllers/  ← コントローラー（★よく触る）
│   └── Models/            ← モデル（★よく触る）
├── database/
│   └── migrations/        ← マイグレーション（★よく触る）
├── resources/
│   └── views/             ← Bladeテンプレート（★よく触る）
├── routes/
│   └── web.php            ← ルーティング（★よく触る）
└── .env                   ← 環境設定（★最初に触る）
```

---

### 1. `app/Http/Controllers/` - コントローラー

**役割**: リクエストを受け取り、処理を行い、レスポンスを返す

```php
// app/Http/Controllers/TaskController.php
class TaskController extends Controller
{
    public function index()
    {
        $tasks = Task::all();
        return view('tasks.index', compact('tasks'));
    }
}
```

---

### 2. `app/Models/` - モデル

**役割**: データベースのテーブルと対応し、データの取得・保存を行う

```php
// app/Models/Task.php
class Task extends Model
{
    protected $fillable = ['title', 'description'];
}
```

---

### 3. `database/migrations/` - マイグレーション

**役割**: データベースのテーブル構造を定義する

```php
// database/migrations/xxxx_create_tasks_table.php
Schema::create('tasks', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->timestamps();
});
```

---

### 4. `resources/views/` - Bladeテンプレート

**役割**: HTMLを生成するテンプレート

```html
<!-- resources/views/tasks/index.blade.php -->
@foreach ($tasks as $task)
    <p>{{ $task->title }}</p>
@endforeach
```

---

### 5. `routes/web.php` - ルーティング

**役割**: URLとコントローラーを紐付ける

```php
// routes/web.php
Route::get('/tasks', [TaskController::class, 'index']);
Route::post('/tasks', [TaskController::class, 'store']);
```

---

### 6. `.env` - 環境設定

**役割**: データベース接続情報などの環境変数を設定する

```env
DB_CONNECTION=mysql
DB_HOST=mysql
DB_DATABASE=laravel_db
DB_USERNAME=laravel_user
DB_PASSWORD=laravel_pass
```

> **📌 注意**: `.env`ファイルはGitで管理されません。本番環境と開発環境で異なる設定を持つことができます。

---

## 💡 TIP: 迷ったらこの順番で探す

開発中に「このファイルはどこ？」と迷ったら、以下の順番で探してみてください。

| やりたいこと | 探す場所 |
|:---|:---|
| URLを追加したい | `routes/web.php` |
| 処理を書きたい | `app/Http/Controllers/` |
| データベースを操作したい | `app/Models/` |
| テーブルを作りたい | `database/migrations/` |
| 画面を作りたい | `resources/views/` |
| 環境設定を変えたい | `.env` |

---

## ✨ まとめ

このセクションでは、Laravelでよく触るディレクトリとファイルを学びました。

| ディレクトリ/ファイル | 役割 |
|:---|:---|
| `app/Http/Controllers/` | コントローラー（リクエスト処理） |
| `app/Models/` | モデル（データベース操作） |
| `database/migrations/` | マイグレーション（テーブル定義） |
| `resources/views/` | Bladeテンプレート（HTML生成） |
| `routes/web.php` | ルーティング（URL定義） |
| `.env` | 環境設定 |

> **📌 ポイント**
> 
> 全てを覚える必要はありません。開発を進めていく中で、自然と覚えていきます。
> 迷ったら、このセクションを見返してください。

次のセクションでは、Laravelの設計思想である「MVCアーキテクチャ」について学びます。

---
