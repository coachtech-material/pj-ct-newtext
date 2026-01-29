# Tutorial 9-5-2: 多対多のリレーションシップ（belongsToMany）

## 🎯 このセクションで学ぶこと

*   Tutorial 8で学んだ多対多のリレーションシップを、Laravelで実装する方法を理解する。
*   `belongsToMany()`を使った、多対多のリレーションシップの定義方法を理解する。
*   中間テーブルの設計と、`attach()`、`detach()`、`sync()`メソッドの使い方を理解する。

---

## 導入：「中間テーブル」をLaravelで扱う

Tutorial 8では、多対多のリレーションシップを実装するために、**中間テーブル（ピボットテーブル）**を使いました。

例えば、「ユーザー」と「役割（ロール）」の関係を考えてみましょう。

*   1人のユーザーは、複数の役割を持つことができる
*   1つの役割は、複数のユーザーに割り当てられる

このような関係を実装するには、中間テーブルが必要です。

Laravelでは、`belongsToMany()`を使って、多対多のリレーションシップを簡単に実装できます。

---

## 詳細解説

### 🔗 多対多のリレーションシップとは？

多対多のリレーションシップとは、**複数のレコードが、複数のレコードと関連する関係**です。

**例**

*   ユーザーと役割（1人のユーザーは複数の役割を持ち、1つの役割は複数のユーザーに割り当てられる）
*   投稿とタグ（1つの投稿は複数のタグを持ち、1つのタグは複数の投稿に割り当てられる）
*   学生と授業（1人の学生は複数の授業を受講し、1つの授業は複数の学生が受講する）

---

### 📝 テーブル設計の復習

Tutorial 8で学んだように、多対多のリレーションシップを実装するには、**中間テーブル**を使います。

**テーブル構成**

```
users テーブル
+----+----------+
| id | name     |
+----+----------+
| 1  | 山田太郎 |
| 2  | 佐藤花子 |
+----+----------+

roles テーブル
+----+--------+
| id | name   |
+----+--------+
| 1  | admin  |
| 2  | editor |
| 3  | viewer |
+----+--------+

role_user テーブル（中間テーブル）
+----+---------+---------+
| id | user_id | role_id |
+----+---------+---------+
| 1  | 1       | 1       |
| 2  | 1       | 2       |
| 3  | 2       | 3       |
+----+---------+---------+
```

---

### 🔧 マイグレーションの作成

**rolesテーブルの作成**

```bash
sail artisan make:migration create_roles_table
```

**マイグレーションファイル**

```php
public function up()
{
    Schema::create('roles', function (Blueprint $table) {
        $table->id();
        $table->string('name');
        $table->timestamps();
    });
}
```

**中間テーブルの作成**

```bash
sail artisan make:migration create_role_user_table
```

**マイグレーションファイル**

```php
public function up()
{
    Schema::create('role_user', function (Blueprint $table) {
        $table->id();
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->foreignId('role_id')->constrained()->onDelete('cascade');
        $table->timestamps();
    });
}
```

**重要なポイント**

*   中間テーブルの名前は、**アルファベット順**で2つのテーブル名を単数形でつなげます（`role_user`）
*   外部キー制約を設定し、親レコードが削除されたら、中間テーブルのレコードも削除されるようにします

---

### 🔗 Laravelでのリレーションシップ定義

**`belongsToMany()`: 多対多のリレーションシップ**

**`app/Models/User.php`**

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable
{
    public function roles()
    {
        return $this->belongsToMany(Role::class);
    }
}
```

**`app/Models/Role.php`**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    protected $fillable = ['name'];

    public function users()
    {
        return $this->belongsToMany(User::class);
    }
}
```

**コードリーディング**

*   `belongsToMany(Role::class)`: このユーザーは、複数の役割を持つ
*   `belongsToMany(User::class)`: この役割は、複数のユーザーに割り当てられる
*   メソッド名は、複数形（`roles`、`users`）にするのが慣例

---

### 🚀 実践例：データの取得

**ユーザーの全ての役割を取得**

```php
$user = User::find(1);
$roles = $user->roles;

foreach ($roles as $role) {
    echo $role->name;
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `User::find(1)` | `users`テーブルから`id`が1のユーザーを取得します |
| `$user->roles` | Userモデルで定義した`roles()`メソッドを通じて、関連する役割を取得します |
| `foreach ($roles as $role)` | 取得した役割のコレクションをループで処理します |
| `$role->name` | 各役割の`name`カラムの値を取得します |

**処理の流れ**

1. `User::find(1)`で、`users`テーブルから`id = 1`のユーザーを取得
2. `$user->roles`にアクセスすると、Laravelが自動的に中間テーブル（`role_user`）を経由して`roles`テーブルからデータを取得
3. 取得したデータはEloquentコレクションとして返され、`foreach`でループ処理が可能

**実行されるSQL**

```sql
SELECT roles.* FROM roles 
INNER JOIN role_user ON roles.id = role_user.role_id 
WHERE role_user.user_id = 1;
```

**SQLの解説**

*   `INNER JOIN role_user`: `roles`テーブルと中間テーブル`role_user`を結合
*   `ON roles.id = role_user.role_id`: `roles`テーブルの`id`と中間テーブルの`role_id`で結合条件を指定
*   `WHERE role_user.user_id = 1`: 中間テーブルで`user_id`が1のレコードのみを抽出

---

**役割を持つ全てのユーザーを取得**

```php
$role = Role::find(1);
$users = $role->users;

foreach ($users as $user) {
    echo $user->name;
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `Role::find(1)` | `roles`テーブルから`id`が1の役割（admin）を取得します |
| `$role->users` | Roleモデルで定義した`users()`メソッドを通じて、関連するユーザーを取得します |
| `foreach ($users as $user)` | 取得したユーザーのコレクションをループで処理します |
| `$user->name` | 各ユーザーの`name`カラムの値を取得します |

**実行されるSQL**

```sql
SELECT users.* FROM users 
INNER JOIN role_user ON users.id = role_user.user_id 
WHERE role_user.role_id = 1;
```

---

### 🔗 データの追加：`attach()`

`attach()`メソッドを使って、中間テーブルにレコードを追加します。

```php
$user = User::find(1);
$user->roles()->attach(1); // role_id = 1 を追加
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$user->roles()` | リレーションシップのクエリビルダーを取得します（`()`を付けることでメソッドとして呼び出し） |
| `->attach(1)` | 中間テーブルに`user_id = 1`、`role_id = 1`のレコードを追加します |

**`$user->roles`と`$user->roles()`の違い**

*   `$user->roles`（プロパティアクセス）: 関連するデータをコレクションとして取得
*   `$user->roles()`（メソッド呼び出し）: クエリビルダーを取得し、`attach()`などのメソッドを呼び出せる

**実行されるSQL**

```sql
INSERT INTO role_user (user_id, role_id) VALUES (1, 1);
```

**複数の役割を一度に追加**

```php
$user->roles()->attach([1, 2, 3]);
```

**コードリーディング**

*   配列を渡すことで、複数のレコードを一度に追加できます
*   上記の場合、`role_id`が1、2、3の3つのレコードが中間テーブルに追加されます

---

### 🔗 データの削除：`detach()`

`detach()`メソッドを使って、中間テーブルのレコードを削除します。

```php
$user = User::find(1);
$user->roles()->detach(1); // role_id = 1 を削除
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$user->roles()` | リレーションシップのクエリビルダーを取得します |
| `->detach(1)` | 中間テーブルから`user_id = 1`かつ`role_id = 1`のレコードを削除します |

**実行されるSQL**

```sql
DELETE FROM role_user WHERE user_id = 1 AND role_id = 1;
```

**全ての役割を削除**

```php
$user->roles()->detach();
```

**コードリーディング**

*   引数を省略すると、そのユーザーに関連する全ての役割が中間テーブルから削除されます
*   `roles`テーブル自体のデータは削除されません（中間テーブルの関連のみ削除）

---

### 🔄 データの同期：`sync()`

`sync()`メソッドを使って、中間テーブルのレコードを同期します。

```php
$user = User::find(1);
$user->roles()->sync([1, 2]); // role_id = 1, 2 のみを保持
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$user->roles()` | リレーションシップのクエリビルダーを取得します |
| `->sync([1, 2])` | 中間テーブルの状態を、指定した配列の内容と完全に一致させます |

**動作**

*   既存のレコードのうち、`[1, 2]`に含まれないものは削除される
*   `[1, 2]`に含まれるが、既存のレコードにないものは追加される

**具体例**

現在の中間テーブルの状態が以下の場合：

```
role_user テーブル
+---------+---------+
| user_id | role_id |
+---------+---------+
| 1       | 1       |
| 1       | 3       |
+---------+---------+
```

`$user->roles()->sync([1, 2])`を実行すると：

1. `role_id = 3`は配列に含まれないので**削除**
2. `role_id = 1`は既に存在するので**そのまま**
3. `role_id = 2`は存在しないので**追加**

結果：

```
role_user テーブル
+---------+---------+
| user_id | role_id |
+---------+---------+
| 1       | 1       |
| 1       | 2       |
+---------+---------+
```

**実行されるSQL**

```sql
-- 既存のレコードを削除
DELETE FROM role_user WHERE user_id = 1 AND role_id NOT IN (1, 2);

-- 新しいレコードを追加
INSERT INTO role_user (user_id, role_id) VALUES (1, 1), (1, 2);
```

---

### 💡 TIP: `syncWithoutDetaching()`

`syncWithoutDetaching()`を使うと、既存のレコードを削除せずに、新しいレコードのみを追加します。

```php
$user->roles()->syncWithoutDetaching([1, 2, 3]);
```

**コードリーディング**

*   既存のレコードは削除されず、配列に含まれる新しいレコードのみが追加されます
*   `attach()`との違いは、既に存在するレコードを重複して追加しようとしてもエラーにならない点です

---

### 🔍 中間テーブルのカラムにアクセス

中間テーブルに追加のカラムがある場合、`pivot`プロパティを使ってアクセスできます。

**マイグレーションに追加のカラムを定義**

```php
Schema::create('role_user', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->foreignId('role_id')->constrained()->onDelete('cascade');
    $table->timestamp('assigned_at')->nullable(); // 追加
    $table->timestamps();
});
```

**モデルで追加のカラムを指定**

```php
public function roles()
{
    return $this->belongsToMany(Role::class)
                ->withPivot('assigned_at')
                ->withTimestamps();
}
```

**コードリーディング**

| メソッド | 説明 |
|:---|:---|
| `->withPivot('assigned_at')` | 中間テーブルの`assigned_at`カラムにアクセスできるようにします |
| `->withTimestamps()` | 中間テーブルの`created_at`、`updated_at`を自動的に更新します |

**追加のカラムにアクセス**

```php
$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->name;
    echo $role->pivot->assigned_at; // 中間テーブルのカラムにアクセス
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$role->pivot` | 中間テーブルのレコードにアクセスするためのオブジェクト |
| `$role->pivot->assigned_at` | 中間テーブルの`assigned_at`カラムの値を取得 |

---

### 🚀 実践例：投稿とタグ

ブログシステムでよく使われる「投稿とタグ」の多対多リレーションシップを実装してみましょう。

**マイグレーションの作成**

```bash
sail artisan make:migration create_tags_table
sail artisan make:migration create_post_tag_table
```

**tagsテーブル**

```php
Schema::create('tags', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->timestamps();
});
```

**コードリーディング**

*   `$table->id()`: 自動増分の主キーを作成
*   `$table->string('name')`: タグ名を格納するカラム（例：「Laravel」「PHP」「初心者」）

**post_tagテーブル（中間テーブル）**

```php
Schema::create('post_tag', function (Blueprint $table) {
    $table->id();
    $table->foreignId('post_id')->constrained()->onDelete('cascade');
    $table->foreignId('tag_id')->constrained()->onDelete('cascade');
    $table->timestamps();
});
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$table->foreignId('post_id')` | `posts`テーブルへの外部キーカラムを作成 |
| `->constrained()` | `posts`テーブルの`id`カラムへの外部キー制約を自動設定 |
| `->onDelete('cascade')` | 投稿が削除されたら、関連する中間テーブルのレコードも削除 |

**モデルの定義**

**`app/Models/Post.php`**

```php
public function tags()
{
    return $this->belongsToMany(Tag::class);
}
```

**`app/Models/Tag.php`**

```php
public function posts()
{
    return $this->belongsToMany(Post::class);
}
```

**コードリーディング**

*   `belongsToMany(Tag::class)`: 1つの投稿は複数のタグを持つ
*   `belongsToMany(Post::class)`: 1つのタグは複数の投稿に付けられる
*   Laravelは自動的に中間テーブル`post_tag`を探します（アルファベット順）

**コントローラーでの使用例**

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required',
        'content' => 'required',
        'tags' => 'array',
    ]);

    $post = Post::create([
        'title' => $validated['title'],
        'content' => $validated['content'],
        'user_id' => Auth::id(),
    ]);

    // タグを追加
    $post->tags()->attach($validated['tags']);

    return redirect('/posts/' . $post->id);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$request->validate([...])` | リクエストデータのバリデーションを実行 |
| `'tags' => 'array'` | `tags`は配列であることを検証（フォームからタグIDの配列が送信される想定） |
| `Post::create([...])` | 新しい投稿を作成してデータベースに保存 |
| `Auth::id()` | 現在ログイン中のユーザーのIDを取得 |
| `$post->tags()->attach($validated['tags'])` | 作成した投稿に、選択されたタグを関連付け |
| `redirect('/posts/' . $post->id)` | 作成した投稿の詳細ページにリダイレクト |

**処理の流れ**

1. フォームから送信されたデータをバリデーション
2. `Post::create()`で新しい投稿をデータベースに保存
3. `$post->tags()->attach()`で中間テーブル（`post_tag`）にレコードを追加
4. 投稿詳細ページにリダイレクト

**フォームからの送信例**

```html
<form method="POST" action="/posts">
    @csrf
    <input type="text" name="title">
    <textarea name="content"></textarea>
    
    <!-- タグの選択（複数選択可能） -->
    <select name="tags[]" multiple>
        <option value="1">Laravel</option>
        <option value="2">PHP</option>
        <option value="3">初心者</option>
    </select>
    
    <button type="submit">投稿</button>
</form>
```

**コードリーディング**

*   `name="tags[]"`: 配列として送信するため、名前の末尾に`[]`を付ける
*   `multiple`: 複数選択を可能にする属性
*   選択されたタグのIDが配列として`$request->tags`に格納される

---

### 🔍 リレーションシップの存在チェック

**特定の役割を持つユーザーのみを取得**

```php
$users = User::whereHas('roles', function ($query) {
    $query->where('name', 'admin');
})->get();
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `User::whereHas('roles', ...)` | `roles`リレーションシップが存在するユーザーを絞り込む |
| `function ($query) { ... }` | リレーションシップに対する追加の条件を指定するクロージャ |
| `$query->where('name', 'admin')` | 役割名が`admin`であるという条件を追加 |
| `->get()` | 条件に一致するユーザーをコレクションとして取得 |

---

### 🚨 よくある間違い

**間違い1: 中間テーブルの名前が間違っている**

Laravelは、デフォルトで**アルファベット順**で2つのテーブル名を単数形でつなげた名前を期待します。

*   正しい: `role_user`
*   間違い: `user_role`、`roles_users`

もし、異なる名前を使う場合は、第2引数で指定します。

```php
public function roles()
{
    return $this->belongsToMany(Role::class, 'user_roles');
}
```

**間違い2: 外部キーの名前が間違っている**

もし、外部キーの名前が異なる場合は、第3、第4引数で指定します。

```php
public function roles()
{
    return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
}
```

**コードリーディング**

| 引数 | 説明 |
|:---|:---|
| 第1引数 `Role::class` | 関連するモデルクラス |
| 第2引数 `'role_user'` | 中間テーブル名 |
| 第3引数 `'user_id'` | 現在のモデル（User）の外部キー |
| 第4引数 `'role_id'` | 関連するモデル（Role）の外部キー |

---

## ✨ まとめ

このセクションでは、Tutorial 8で学んだ多対多のリレーションシップを、Laravelで実装する方法を学びました。

*   `belongsToMany()`を使って、多対多のリレーションシップを定義できる。
*   中間テーブルは、アルファベット順で2つのテーブル名を単数形でつなげた名前にする。
*   `attach()`を使って、中間テーブルにレコードを追加できる。
*   `detach()`を使って、中間テーブルのレコードを削除できる。
*   `sync()`を使って、中間テーブルのレコードを同期できる。
*   `withPivot()`を使って、中間テーブルの追加のカラムにアクセスできる。



---
