# 13-4-2 モデル作成とリレーション定義

## 🎯 このセクションで学ぶこと

このセクションでは、タスク管理アプリのモデルを作成し、テーブル間のリレーションを定義します。

- モデルファイルの作成方法
- `$fillable` プロパティによるマスアサインメント保護
- 1対多リレーションの定義（hasMany / belongsTo）
- リレーションを使ったデータ取得

> **📌 対応Issue**: #2 モデル作成とリレーション定義

---

## 🧠 先輩エンジニアの思考プロセス

モデルを作成する際、先輩エンジニアは以下のように考えます。

> 「マイグレーションでテーブルを作成したら、次はモデルを作成する。モデルはテーブルとPHPコードをつなぐ役割だ。リレーションを定義しておけば、`$user->tasks` のように直感的にデータを取得できるようになる。」

### モデルとテーブルの対応

| モデル | テーブル | 役割 |
|:---|:---|:---|
| User | users | ユーザー情報を管理 |
| Category | categories | カテゴリー情報を管理 |
| Task | tasks | タスク情報を管理 |

### リレーションの設計

| 関係 | 説明 |
|:---|:---|
| User → Task | 1対多（1人のユーザーは複数のタスクを持つ） |
| Category → Task | 1対多（1つのカテゴリーには複数のタスクが属する） |
| Task → User | 多対1（1つのタスクは1人のユーザーに属する） |
| Task → Category | 多対1（1つのタスクは1つのカテゴリーに属する） |

---

## 🔀 ブランチの作成

Issue駆動開発のワークフローに従い、まずはIssue #2に対応するブランチを作成します。

```bash
# 現在のブランチを確認（mainにいることを確認）
git branch

# mainブランチの最新状態を取得
git pull origin main

# Issue #2 に対応するブランチを作成して切り替え
git switch -c feature/issue-2-models
```

### コマンドのコードリーディング

| コマンド | 説明 |
|:---|:---|
| `git branch` | 現在のブランチ一覧を表示（`*`が付いているのが現在のブランチ） |
| `git pull origin main` | リモートのmainブランチの最新状態をローカルに取り込む |
| `git switch -c feature/issue-2-models` | 新しいブランチを作成して切り替え |

> **💡 ポイント**: 新しいブランチを作成する前に、必ず `git pull` でmainブランチを最新状態にしておきましょう。

---

## 🏃 実践

### ステップ1: Categoryモデルの作成

カテゴリーモデルを作成します。

```bash
# モデルファイルの作成
sail artisan make:model Category
```

#### コマンドの構文

```
sail artisan make:model {モデル名}
```

| 部分 | 説明 |
|:---|:---|
| `sail artisan` | Laravel Sailを使ってArtisanコマンドを実行 |
| `make:model` | モデルファイルを作成するArtisanコマンド |
| `Category` | モデル名（単数形・パスカルケース） |

#### モデルファイルの編集

`app/Models/Category.php` を以下のように編集します。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

class Category extends Model
{
    use HasFactory;

    /**
     * 複数代入可能な属性
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'name',
    ];

    /**
     * このカテゴリーに属するタスクを取得
     */
    public function tasks(): HasMany
    {
        return $this->hasMany(Task::class);
    }
}
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `namespace App\Models` | このクラスが属する名前空間 |
| `use HasFactory` | ファクトリ機能を使用可能にするトレイト |
| `protected $fillable = ['name']` | `create()` や `update()` で一括代入できるカラム |
| `public function tasks(): HasMany` | リレーションメソッド（戻り値の型を明示） |
| `return $this->hasMany(Task::class)` | 「このカテゴリーは複数のタスクを持つ」という関係を定義 |

#### $fillableの役割

`$fillable` は、マスアサインメント（一括代入）を許可するカラムを指定します。

```php
// $fillableに'name'が含まれているので、以下のコードが動作する
Category::create(['name' => '仕事']);

// $fillableに含まれていないカラムは無視される（セキュリティ対策）
Category::create(['name' => '仕事', 'id' => 999]); // idは無視される
```

---

### ステップ2: Taskモデルの作成

タスクモデルを作成します。

```bash
# モデルファイルの作成
sail artisan make:model Task
```

#### モデルファイルの編集

`app/Models/Task.php` を以下のように編集します。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Task extends Model
{
    use HasFactory;

    /**
     * 複数代入可能な属性
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'user_id',
        'category_id',
        'title',
        'description',
        'priority',
    ];

    /**
     * このタスクを所有するユーザーを取得
     */
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    /**
     * このタスクが属するカテゴリーを取得
     */
    public function category(): BelongsTo
    {
        return $this->belongsTo(Category::class);
    }

    /**
     * 優先度のラベルを取得
     */
    public function getPriorityLabelAttribute(): string
    {
        return match ($this->priority) {
            1 => '低',
            2 => '中',
            3 => '高',
            default => '不明',
        };
    }
}
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `protected $fillable = [...]` | 一括代入を許可するカラムの配列 |
| `public function user(): BelongsTo` | ユーザーへのリレーション（多対1） |
| `return $this->belongsTo(User::class)` | 「このタスクは1人のユーザーに属する」という関係 |
| `public function category(): BelongsTo` | カテゴリーへのリレーション（多対1） |
| `getPriorityLabelAttribute()` | アクセサ（`$task->priority_label` で呼び出し可能） |
| `match ($this->priority) { ... }` | PHP 8のmatch式で優先度を日本語ラベルに変換 |

#### アクセサの使い方

`getPriorityLabelAttribute()` はアクセサと呼ばれる特殊なメソッドです。

```php
$task = Task::find(1);

// priority が 3 の場合
echo $task->priority;       // 3
echo $task->priority_label; // 高
```

---

### ステップ3: Userモデルの編集

既存の `User` モデルにリレーションを追加します。

`app/Models/User.php` を編集し、`tasks()` メソッドを追加します。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Laravel\Sanctum\HasApiTokens;

class User extends Authenticatable
{
    use HasApiTokens, HasFactory, Notifiable;

    /**
     * 複数代入可能な属性
     *
     * @var array<int, string>
     */
    protected $fillable = [
        'name',
        'email',
        'password',
    ];

    /**
     * シリアライズ時に非表示にする属性
     *
     * @var array<int, string>
     */
    protected $hidden = [
        'password',
        'remember_token',
    ];

    /**
     * キャストする属性
     *
     * @var array<string, string>
     */
    protected $casts = [
        'email_verified_at' => 'datetime',
        'password' => 'hashed',
    ];

    /**
     * このユーザーが所有するタスクを取得
     */
    public function tasks(): HasMany
    {
        return $this->hasMany(Task::class);
    }
}
```

#### 追加したコードのコードリーディング

| コード | 説明 |
|:---|:---|
| `use Illuminate\Database\Eloquent\Relations\HasMany` | HasMany型のインポート |
| `public function tasks(): HasMany` | タスクへのリレーション（1対多） |
| `return $this->hasMany(Task::class)` | 「このユーザーは複数のタスクを持つ」という関係 |

---

### ステップ4: リレーションの動作確認

Tinkerを使ってリレーションが正しく動作するか確認します。

```bash
# Tinkerを起動
sail artisan tinker
```

```php
// カテゴリーを作成
$category = \App\Models\Category::create(['name' => '仕事']);

// ユーザーを作成
$user = \App\Models\User::create([
    'name' => 'テストユーザー',
    'email' => 'test@example.com',
    'password' => bcrypt('password'),
]);

// タスクを作成
$task = \App\Models\Task::create([
    'user_id' => $user->id,
    'category_id' => $category->id,
    'title' => '会議の準備',
    'description' => '資料を作成する',
    'priority' => 3,
]);

// リレーションの確認
$task->user;          // タスクの所有者を取得
$task->category;      // タスクのカテゴリーを取得
$task->priority_label; // '高'

$user->tasks;         // ユーザーのタスク一覧を取得
$category->tasks;     // カテゴリーのタスク一覧を取得

// Tinkerを終了
exit
```

---

## 💡 TIP: リレーションメソッドの命名規則

| リレーション | メソッド名 | 例 |
|:---|:---|:---|
| hasMany（1対多） | 複数形 | `tasks()`, `comments()` |
| belongsTo（多対1） | 単数形 | `user()`, `category()` |
| hasOne（1対1） | 単数形 | `profile()`, `address()` |

---

## 🚀 実践例: リレーションを使ったデータ取得

### 実践例1: ユーザーのタスク一覧を取得

```php
// ログイン中のユーザーのタスク一覧を取得
$tasks = auth()->user()->tasks;

// カテゴリー情報も一緒に取得（N+1問題を回避）
$tasks = auth()->user()->tasks()->with('category')->get();
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `auth()->user()` | ログイン中のユーザーを取得 |
| `->tasks` | ユーザーのタスク一覧を取得（リレーション） |
| `->tasks()` | クエリビルダを取得（メソッドとして呼び出し） |
| `->with('category')` | カテゴリー情報をEager Loadingで取得 |
| `->get()` | クエリを実行して結果を取得 |

### 実践例2: カテゴリーごとのタスク数を取得

```php
// カテゴリーとタスク数を取得
$categories = Category::withCount('tasks')->get();

foreach ($categories as $category) {
    echo "{$category->name}: {$category->tasks_count}件";
}
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `Category::withCount('tasks')` | タスク数を `tasks_count` として取得 |
| `$category->tasks_count` | そのカテゴリーに属するタスクの数 |

---

## ❌ よくある間違い

### 1. $fillableを設定し忘れる

```php
// ❌ NG: $fillableが設定されていない
Task::create([
    'title' => 'テスト',
    'user_id' => 1,
    // ...
]);
// エラー: Add [title] to fillable property to allow mass assignment
```

**対処法**: モデルに `$fillable` プロパティを追加する。

### 2. リレーションメソッドの戻り値を間違える

```php
// ❌ NG: hasManyなのにbelongsToを使っている
public function tasks()
{
    return $this->belongsTo(Task::class); // 間違い
}
```

**対処法**: 「1対多」なら `hasMany`、「多対1」なら `belongsTo` を使う。

### 3. リレーションメソッド名を間違える

```php
// ❌ NG: 外部キーと一致しないメソッド名
public function owner() // user_idなのにowner
{
    return $this->belongsTo(User::class);
}
// エラー: owner_idカラムを探そうとする
```

**対処法**: 外部キー名と一致するメソッド名にするか、第2引数で外部キーを明示する。

```php
// ✅ OK: 外部キーを明示
public function owner()
{
    return $this->belongsTo(User::class, 'user_id');
}
```

---

## ✅ 完了条件

以下の条件を満たしていることを確認してください。

- [ ] `Category` モデルが作成されている
- [ ] `Task` モデルが作成されている
- [ ] `User` モデルに `tasks()` リレーションが追加されている
- [ ] 各モデルに `$fillable` が正しく設定されている
- [ ] Tinkerでリレーションが正しく動作することを確認した

---

## ✨ まとめ

このセクションでは、タスク管理アプリのモデルを作成し、リレーションを定義しました。

| 学んだこと | 内容 |
|:---|:---|
| モデルの作成 | `sail artisan make:model` コマンド |
| $fillable | マスアサインメントを許可するカラムを指定 |
| hasMany | 1対多リレーション（親→子） |
| belongsTo | 多対1リレーション（子→親） |
| アクセサ | `get{属性名}Attribute()` で計算プロパティを定義 |

次のChapterでは、認証機能を実装します。

---

## 🔄 Git操作とプルリクエスト

作業が完了したら、変更をコミットしてプッシュし、プルリクエストを作成します。

### ステップ1: コミットとプッシュ

```bash
# 変更をステージング
git add .

# コミット（Issue番号を含める）
git commit -m "feat: モデル作成とリレーション定義 #2"

# リモートにプッシュ
git push origin feature/issue-2-models
```

### ステップ2: プルリクエストの作成

1. GitHubのリポジトリページを開く
2. 「Pull requests」タブをクリックする
3. 「New pull request」ボタンをクリックする
4. `base: main` ← `compare: feature/issue-2-models` を選択する
5. 「Create pull request」ボタンをクリックする
6. 以下の内容を入力する

**タイトル**:
```
feat: モデル作成とリレーション定義
```

**説明欄**:
```markdown
## 概要
Eloquentモデルを作成し、リレーションを定義しました。

## 変更内容
- Categoryモデルの作成
- Taskモデルの作成
- Userモデルにtasks()リレーションを追加
- 各モデルに$fillableを設定

## 対応Issue
close #2
```

7. 「Create pull request」ボタンをクリックする

### ステップ3: プルリクエストのマージ

1. PRのページで「Merge pull request」ボタンをクリックする
2. 「Confirm merge」ボタンをクリックする
3. マージが完了すると、Issue #2が自動的にクローズされる

### ステップ4: ローカルのmainブランチを更新

```bash
# mainブランチに切り替え
git switch main

# リモートの変更を取り込む
git pull origin main
```

> **📌 Issue対応**: PRをマージすると、説明欄の `close #2` によりIssue #2が自動的にクローズされます。
