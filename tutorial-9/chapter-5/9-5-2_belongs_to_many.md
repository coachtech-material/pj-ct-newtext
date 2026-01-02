# Tutorial 9-5-2: 多対多のリレーションシップ（belongsToMany）

## 🎯 このセクションで学ぶこと

*   Tutorial 8で学んだ多対多のリレーションシップを、Laravelで実装できるようになる。
*   `belongsToMany()`を使って、多対多のリレーションシップを定義できるようになる。
*   中間テーブルを設計し、`attach()`、`detach()`、`sync()`メソッドを使えるようになる。

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

#### ステップ1: rolesテーブルを作成

```bash
php artisan make:migration create_roles_table
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

#### ステップ2: 中間テーブルを作成

```bash
php artisan make:migration create_role_user_table
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

#### `belongsToMany()`: 多対多のリレーションシップ

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

#### ユーザーの全ての役割を取得

```php
$user = User::find(1);
$roles = $user->roles;

foreach ($roles as $role) {
    echo $role->name;
}
```

**実行されるSQL**

```sql
SELECT roles.* FROM roles 
INNER JOIN role_user ON roles.id = role_user.role_id 
WHERE role_user.user_id = 1;
```

#### 役割を持つ全てのユーザーを取得

```php
$role = Role::find(1);
$users = $role->users;

foreach ($users as $user) {
    echo $user->name;
}
```

---

### 🔗 データの追加：`attach()`

`attach()`メソッドを使って、中間テーブルにレコードを追加します。

```php
$user = User::find(1);
$user->roles()->attach(1); // role_id = 1 を追加
```

**実行されるSQL**

```sql
INSERT INTO role_user (user_id, role_id) VALUES (1, 1);
```

#### 複数の役割を一度に追加

```php
$user->roles()->attach([1, 2, 3]);
```

---

### 🔗 データの削除：`detach()`

`detach()`メソッドを使って、中間テーブルのレコードを削除します。

```php
$user = User::find(1);
$user->roles()->detach(1); // role_id = 1 を削除
```

**実行されるSQL**

```sql
DELETE FROM role_user WHERE user_id = 1 AND role_id = 1;
```

#### 全ての役割を削除

```php
$user->roles()->detach();
```

---

### 🔄 データの同期：`sync()`

`sync()`メソッドを使って、中間テーブルのレコードを同期します。

```php
$user = User::find(1);
$user->roles()->sync([1, 2]); // role_id = 1, 2 のみを保持
```

**動作**

*   既存のレコードのうち、`[1, 2]`に含まれないものは削除される
*   `[1, 2]`に含まれるが、既存のレコードにないものは追加される

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

---

### 🔍 中間テーブルのカラムにアクセス

中間テーブルに追加のカラムがある場合、`pivot`プロパティを使ってアクセスできます。

#### マイグレーションに追加のカラムを定義

```php
Schema::create('role_user', function (Blueprint $table) {
    $table->id();
    $table->foreignId('user_id')->constrained()->onDelete('cascade');
    $table->foreignId('role_id')->constrained()->onDelete('cascade');
    $table->timestamp('assigned_at')->nullable(); // 追加
    $table->timestamps();
});
```

#### モデルで追加のカラムを指定

```php
public function roles()
{
    return $this->belongsToMany(Role::class)
                ->withPivot('assigned_at')
                ->withTimestamps();
}
```

#### 追加のカラムにアクセス

```php
$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->name;
    echo $role->pivot->assigned_at; // 中間テーブルのカラムにアクセス
}
```

---

### 🚀 実践例：投稿とタグ

#### マイグレーション

```bash
php artisan make:migration create_tags_table
php artisan make:migration create_post_tag_table
```

**tagsテーブル**

```php
Schema::create('tags', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->timestamps();
});
```

**post_tagテーブル**

```php
Schema::create('post_tag', function (Blueprint $table) {
    $table->id();
    $table->foreignId('post_id')->constrained()->onDelete('cascade');
    $table->foreignId('tag_id')->constrained()->onDelete('cascade');
    $table->timestamps();
});
```

#### モデル

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

#### コントローラー

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

---

### 🔍 リレーションシップの存在チェック

#### 特定の役割を持つユーザーのみを取得

```php
$users = User::whereHas('roles', function ($query) {
    $query->where('name', 'admin');
})->get();
```

---

### 🚨 よくある間違い

#### 間違い1: 中間テーブルの名前が間違っている

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

#### 間違い2: 外部キーの名前が間違っている

もし、外部キーの名前が異なる場合は、第3、第4引数で指定します。

```php
public function roles()
{
    return $this->belongsToMany(Role::class, 'role_user', 'user_id', 'role_id');
}
```

---

## ✨ まとめ

このセクションでは、Tutorial 8で学んだ多対多のリレーションシップを、Laravelで実装する方法を学びました。

*   `belongsToMany()`を使って、多対多のリレーションシップを定義できる。
*   中間テーブルは、アルファベット順で2つのテーブル名を単数形でつなげた名前にする。
*   `attach()`を使って、中間テーブルにレコードを追加できる。
*   `detach()`を使って、中間テーブルのレコードを削除できる。
*   `sync()`を使って、中間テーブルのレコードを同期できる。
*   `withPivot()`を使って、中間テーブルの追加のカラムにアクセスできる。

次のセクションでは、Eager Loadingとレイジーローディングについて学びます。

---
