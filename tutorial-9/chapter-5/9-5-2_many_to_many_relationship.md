# Tutorial 9-5-2: 多対多のリレーションシップ

## 🎯 このセクションで学ぶこと

*   Eloquentで多対多のリレーションシップを定義できるようになる。
*   中間テーブル（ピボットテーブル）の役割を理解し、`belongsToMany()`メソッドを使えるようになる。
*   中間テーブルに追加データを保存し、取得できるようになる。

---

## 導入：Tutorial 8で学んだ多対多の関係をEloquentで実装する

Tutorial 8で、多対多のリレーションシップを学びました。例えば、「1人のユーザーは複数のロールを持ち、1つのロールは複数のユーザーに割り当てられる」という関係を、**中間テーブル（ピボットテーブル）**を使って表現しました。

```sql
-- ユーザーテーブル
CREATE TABLE users (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255)
);

-- ロールテーブル
CREATE TABLE roles (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255)
);

-- 中間テーブル（ユーザーとロールを紐付ける）
CREATE TABLE role_user (
    user_id BIGINT,
    role_id BIGINT,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (role_id) REFERENCES roles(id)
);
```

Eloquent ORMでは、この多対多の関係を`belongsToMany()`メソッドで定義することで、中間テーブルを意識せずに関連データを取得できます。

---

## 詳細解説

### 🏗️ 多対多のリレーションシップの定義

多対多のリレーションシップは、両方のモデルに`belongsToMany()`メソッドを定義します。

#### ステップ1: マイグレーションでテーブルを作成する

まず、`users`, `roles`, `role_user`の3つのテーブルを作成します。

**`database/migrations/xxxx_create_roles_table.php`**

```php
public function up(): void
{
    Schema::create('roles', function (Blueprint $table) {
        $table->id();
        $table->string('name');
        $table->timestamps();
    });
}
```

**`database/migrations/xxxx_create_role_user_table.php`**

```php
public function up(): void
{
    Schema::create('role_user', function (Blueprint $table) {
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->foreignId('role_id')->constrained()->onDelete('cascade');
        $table->primary(['user_id', 'role_id']);
        $table->timestamps(); // 中間テーブルにもタイムスタンプを追加できる
    });
}
```

**重要なポイント**

*   中間テーブルの名前は、**2つのテーブル名を単数形・アルファベット順で結合したもの**にします（`role_user`）。
*   `primary(['user_id', 'role_id'])`: 複合主キーを設定します。これにより、同じユーザーに同じロールを重複して割り当てることを防ぎます。

マイグレーションを実行します。

```bash
docker compose exec php php artisan migrate
```

#### ステップ2: `User`モデルに`belongsToMany()`を定義する

`app/Models/User.php`に、以下のメソッドを追加します。

```php
<?php

namespace App\Models;

use Illuminate\Foundation\Auth\User as Authenticatable;

class User extends Authenticatable
{
    /**
     * このユーザーが持つロール
     */
    public function roles()
    {
        return $this->belongsToMany(Role::class);
    }
}
```

**コードリーディング**

*   `public function roles()`: メソッド名は複数形にします（`roles`）。
*   `return $this->belongsToMany(Role::class)`: 「このユーザーは複数の`Role`を持つ」という関係を定義します。
*   Laravelは、中間テーブル名（`role_user`）を自動的に推測します。

#### ステップ3: `Role`モデルに`belongsToMany()`を定義する

`app/Models/Role.php`を作成し、以下のコードを記述します。

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Role extends Model
{
    /**
     * このロールを持つユーザー
     */
    public function users()
    {
        return $this->belongsToMany(User::class);
    }
}
```

---

### 🔍 リレーションシップを使ったデータ取得

リレーションシップを定義すると、以下のように関連データを取得できます。

#### 1. ユーザーのロールを取得する

```php
$user = User::find(1);
$roles = $user->roles; // このユーザーの全てのロールを取得
```

**Bladeでの表示**

```blade
<h2>{{ $user->name }}のロール</h2>
<ul>
    @foreach ($user->roles as $role)
        <li>{{ $role->name }}</li>
    @endforeach
</ul>
```

#### 2. ロールを持つユーザーを取得する

```php
$role = Role::find(1);
$users = $role->users; // このロールを持つ全てのユーザーを取得
```

---

### 🔗 リレーションシップを使ったデータの追加と削除

多対多のリレーションシップでは、中間テーブルにレコードを追加・削除することで、関連付けを行います。

#### データを追加する（`attach()`）

```php
$user = User::find(1);
$user->roles()->attach(1); // ロールID=1を追加
```

複数のロールを一度に追加することもできます。

```php
$user->roles()->attach([1, 2, 3]);
```

#### データを削除する（`detach()`）

```php
$user->roles()->detach(1); // ロールID=1を削除
```

全てのロールを削除する場合は、引数を省略します。

```php
$user->roles()->detach(); // 全てのロールを削除
```

#### データを同期する（`sync()`）

既存の関連付けを全て削除し、新しい関連付けを設定します。

```php
$user->roles()->sync([1, 2]); // ロールID=1,2だけを設定（他は削除）
```

#### データを切り替える（`toggle()`）

既に関連付けられている場合は削除し、関連付けられていない場合は追加します。

```php
$user->roles()->toggle([1, 2]); // ロールID=1,2を切り替え
```

---

### 📝 中間テーブルに追加データを保存する

中間テーブルには、外部キー以外のカラムを追加することもできます。例えば、「ユーザーにロールを割り当てた日時」を保存したい場合、`assigned_at`カラムを追加します。

#### マイグレーションで追加カラムを定義する

```php
public function up(): void
{
    Schema::create('role_user', function (Blueprint $table) {
        $table->foreignId('user_id')->constrained()->onDelete('cascade');
        $table->foreignId('role_id')->constrained()->onDelete('cascade');
        $table->primary(['user_id', 'role_id']);
        $table->timestamp('assigned_at')->nullable(); // 追加カラム
        $table->timestamps();
    });
}
```

#### モデルで追加カラムを指定する

`belongsToMany()`の`withPivot()`メソッドで、追加カラムを指定します。

```php
public function roles()
{
    return $this->belongsToMany(Role::class)->withPivot('assigned_at');
}
```

#### データを追加する際に追加カラムを設定する

```php
$user->roles()->attach(1, ['assigned_at' => now()]);
```

#### 追加カラムを取得する

```php
$user = User::find(1);

foreach ($user->roles as $role) {
    echo $role->name;
    echo $role->pivot->assigned_at; // 中間テーブルのデータは$pivotでアクセス
}
```

---

### ⚡ Eager Loadingで中間テーブルも読み込む

多対多のリレーションシップでも、N+1問題を避けるためにEager Loadingを使います。

```php
$users = User::with('roles')->get();

foreach ($users as $user) {
    foreach ($user->roles as $role) {
        echo $role->name;
    }
}
```

---

### 🔍 中間テーブルの名前をカスタマイズする

もし、中間テーブルの名前が規約に従っていない場合（例：`user_roles`）、`belongsToMany()`の第2引数で明示的に指定します。

```php
public function roles()
{
    return $this->belongsToMany(Role::class, 'user_roles');
}
```

外部キーのカラム名もカスタマイズできます。

```php
public function roles()
{
    return $this->belongsToMany(Role::class, 'user_roles', 'user_id', 'role_id');
}
```

---

## 💡 TIP: 中間テーブルに`timestamps()`を追加する

中間テーブルに`timestamps()`を追加すると、関連付けが作成・更新された日時を記録できます。

**マイグレーション**
```php
$table->timestamps();
```

**モデル**
```php
public function roles()
{
    return $this->belongsToMany(Role::class)->withTimestamps();
}
```

これにより、`$role->pivot->created_at`と`$role->pivot->updated_at`にアクセスできます。

---

## ✨ まとめ

このセクションでは、Eloquentで多対多のリレーションシップを定義し、中間テーブルを扱う方法を学びました。

*   多対多のリレーションシップは、両方のモデルに`belongsToMany()`を定義する。
*   中間テーブルの名前は、2つのテーブル名を単数形・アルファベット順で結合したものにする（`role_user`）。
*   `attach()`, `detach()`, `sync()`, `toggle()`を使って、関連付けを追加・削除できる。
*   中間テーブルに追加カラムを保存する場合は、`withPivot()`を使う。
*   `$role->pivot`で、中間テーブルのデータにアクセスできる。


---

## 📝 学習のポイント

- [ ] `belongsToMany()`を使って、多対多のリレーションシップを定義できる。
- [ ] 中間テーブルの命名規則（単数形・アルファベット順）を理解した。
- [ ] `attach()`, `detach()`, `sync()`を使って、関連付けを操作できる。
- [ ] `withPivot()`を使って、中間テーブルの追加カラムを扱える。
- [ ] `$role->pivot`で、中間テーブルのデータにアクセスできる。
