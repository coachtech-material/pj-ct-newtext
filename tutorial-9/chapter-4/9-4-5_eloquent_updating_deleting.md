# Tutorial 9-4-5: データの更新と削除

## 🎯 このセクションで学ぶこと

*   Eloquentを使って、データを更新できるようになる。
*   Eloquentを使って、データを削除できるようになる。
*   ソフトデリートの概念を理解する。

---

## 導入：データは「変わる」もの

Webアプリケーションでは、データを作成するだけでなく、更新したり削除したりすることも重要です。

例えば、以下のような状況を考えてみましょう。

*   **ユーザーがプロフィールを編集する**
*   **投稿のタイトルを修正する**
*   **不要なコメントを削除する**

このセクションでは、Eloquentを使ってデータを更新・削除する方法を学びます。

---

## 詳細解説

### 📝 データの更新

Eloquentでは、データを更新する方法が主に2つあります。

1. **`save()`メソッド**: モデルのインスタンスを取得してから、プロパティを変更して保存する
2. **`update()`メソッド**: 配列を渡して、一度に更新する

---

### 🔄 `save()`メソッドを使った更新

#### 基本的な使い方

```php
$user = User::find(1);
$user->name = '佐藤花子';
$user->email = 'hanako@example.com';
$user->save();
```

これは、以下のSQLと同じです。

```sql
UPDATE users SET name = '佐藤花子', email = 'hanako@example.com', updated_at = '2024-12-11 10:00:00' WHERE id = 1;
```

**重要なポイント**

*   `save()`は、`updated_at`を自動的に更新します。
*   変更されたカラムのみがSQLに含まれます。

---

### 🔄 `update()`メソッドを使った更新

#### 基本的な使い方

```php
$user = User::find(1);
$user->update([
    'name' => '佐藤花子',
    'email' => 'hanako@example.com',
]);
```

これも、以下のSQLと同じです。

```sql
UPDATE users SET name = '佐藤花子', email = 'hanako@example.com', updated_at = '2024-12-11 10:00:00' WHERE id = 1;
```

**重要なポイント**

*   `update()`を使うには、モデルに`$fillable`または`$guarded`を定義する必要があります。

---

### 🔍 `save()`と`update()`の違い

| メソッド | 特徴 | 使い所 |
|:---|:---|:---|
| `save()` | プロパティを変更してから保存 | 複雑なロジックがある場合 |
| `update()` | 配列を渡して、一度に更新 | フォームから送信されたデータを保存する場合 |

---

### 🚀 実践例：投稿の編集

#### `save()`を使った例

```php
public function update(Request $request, $id)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'content' => 'required',
    ]);

    $post = Post::findOrFail($id);
    $post->title = $validated['title'];
    $post->content = $validated['content'];
    $post->save();

    return redirect('/posts/' . $post->id);
}
```

#### `update()`を使った例

```php
public function update(Request $request, $id)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'content' => 'required',
    ]);

    $post = Post::findOrFail($id);
    $post->update($validated);

    return redirect('/posts/' . $post->id);
}
```

---

### 📊 複数のレコードを一度に更新する

`where()`と`update()`を組み合わせることで、複数のレコードを一度に更新できます。

```php
Post::where('user_id', 1)->update(['is_published' => false]);
```

これは、以下のSQLと同じです。

```sql
UPDATE posts SET is_published = 0, updated_at = '2024-12-11 10:00:00' WHERE user_id = 1;
```

---

### 🗑️ データの削除

Eloquentでは、データを削除する方法が主に2つあります。

1. **`delete()`メソッド**: モデルのインスタンスを取得してから、削除する
2. **`destroy()`メソッド**: IDを指定して、直接削除する

---

### 🗑️ `delete()`メソッドを使った削除

#### 基本的な使い方

```php
$user = User::find(1);
$user->delete();
```

これは、以下のSQLと同じです。

```sql
DELETE FROM users WHERE id = 1;
```

---

### 🗑️ `destroy()`メソッドを使った削除

#### 基本的な使い方

```php
User::destroy(1);
```

これも、以下のSQLと同じです。

```sql
DELETE FROM users WHERE id = 1;
```

#### 複数のIDを指定して削除

```php
User::destroy([1, 2, 3]);
```

これは、以下のSQLと同じです。

```sql
DELETE FROM users WHERE id IN (1, 2, 3);
```

---

### 📊 複数のレコードを一度に削除する

`where()`と`delete()`を組み合わせることで、複数のレコードを一度に削除できます。

```php
Post::where('user_id', 1)->delete();
```

これは、以下のSQLと同じです。

```sql
DELETE FROM posts WHERE user_id = 1;
```

---

### 🔄 ソフトデリート（論理削除）

ソフトデリートとは、**データを物理的に削除せず、削除フラグを立てる**仕組みです。これにより、削除されたデータを後から復元できます。

#### ステップ1: マイグレーションに`deleted_at`カラムを追加

```php
Schema::create('posts', function (Blueprint $table) {
    $table->id();
    $table->string('title');
    $table->text('content');
    $table->timestamps();
    $table->softDeletes(); // 追加
});
```

#### ステップ2: モデルに`SoftDeletes`トレイトを追加

**`app/Models/Post.php`**

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;

class Post extends Model
{
    use SoftDeletes;

    protected $fillable = ['title', 'content'];
}
```

#### ステップ3: ソフトデリートを実行

```php
$post = Post::find(1);
$post->delete();
```

これは、以下のSQLと同じです。

```sql
UPDATE posts SET deleted_at = '2024-12-11 10:00:00' WHERE id = 1;
```

**重要なポイント**

*   ソフトデリートされたレコードは、通常のクエリでは取得されません。

```php
$posts = Post::all(); // ソフトデリートされたレコードは含まれない
```

---

### 🔍 ソフトデリートされたレコードを取得する

#### ソフトデリートされたレコードも含めて取得

```php
$posts = Post::withTrashed()->get();
```

#### ソフトデリートされたレコードのみを取得

```php
$posts = Post::onlyTrashed()->get();
```

---

### 🔄 ソフトデリートされたレコードを復元する

```php
$post = Post::withTrashed()->find(1);
$post->restore();
```

これは、以下のSQLと同じです。

```sql
UPDATE posts SET deleted_at = NULL WHERE id = 1;
```

---

### 🗑️ ソフトデリートされたレコードを完全に削除する

```php
$post = Post::withTrashed()->find(1);
$post->forceDelete();
```

これは、以下のSQLと同じです。

```sql
DELETE FROM posts WHERE id = 1;
```

---

### 💡 TIP: `increment()`と`decrement()`

数値カラムを増減させる場合は、`increment()`と`decrement()`を使うと便利です。

```php
$post = Post::find(1);
$post->increment('views'); // viewsを1増やす
$post->increment('views', 10); // viewsを10増やす
$post->decrement('views'); // viewsを1減らす
```

これは、以下のSQLと同じです。

```sql
UPDATE posts SET views = views + 1, updated_at = '2024-12-11 10:00:00' WHERE id = 1;
```

---

### 🚨 よくある間違い

#### 間違い1: `save()`を忘れる

```php
$user = User::find(1);
$user->name = '佐藤花子';
// $user->save(); を忘れる
```

これでは、データベースに保存されません。必ず`save()`を呼び出します。

#### 間違い2: `update()`の後に`save()`を呼ぶ

```php
$user = User::find(1);
$user->update(['name' => '佐藤花子']);
$user->save(); // 不要
```

`update()`は、自動的に保存されるため、`save()`は不要です。

---

## ✨ まとめ

このセクションでは、Eloquentを使ってデータを更新・削除する方法を学びました。

*   `save()`は、プロパティを変更してから保存する。
*   `update()`は、配列を渡して、一度に更新する。
*   `delete()`は、モデルのインスタンスを取得してから削除する。
*   `destroy()`は、IDを指定して、直接削除する。
*   ソフトデリートを使うことで、データを物理的に削除せず、削除フラグを立てることができる。
*   ソフトデリートされたレコードは、`withTrashed()`や`onlyTrashed()`で取得できる。

次のセクションでは、マスアサインメントと`$fillable`について、さらに詳しく学びます。

---

## 📝 学習のポイント

- [ ] `save()`と`update()`の違いを理解し、使い分けられる。
- [ ] `delete()`と`destroy()`の違いを理解し、使い分けられる。
- [ ] ソフトデリートの概念を理解し、実装できる。
- [ ] ソフトデリートされたレコードを取得・復元・完全削除できる。
