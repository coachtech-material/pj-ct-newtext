# Tutorial 9-4-6: データの更新と削除

## 🎯 このセクションで学ぶこと

*   Eloquentを使って、データを更新できるようになる。
*   Eloquentを使って、データを削除できるようになる。
*   **`$user->save()`と`$user->update()`の違いを理解する。**
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

> **💡 Tutorial 7の復習**: どちらも`->`を使っています。これは**インスタンスのメソッド**を呼び出しているからです。`$user`はUserクラスのインスタンスなので、`->`を使ってメソッドにアクセスします。

---

### 🔄 `save()`メソッドを使った更新

#### 基本的な使い方

```php
$user = User::find(1);
$user->name = '佐藤花子';
$user->email = 'hanako@example.com';
$user->save();
```

**コードリーディング（1行ずつ分解）**

| 行 | コード | 意味 | 演算子 |
|:---:|:---|:---|:---:|
| 1 | `$user = User::find(1);` | ID=1のユーザーを取得し、インスタンスを`$user`に格納 | `::` |
| 2 | `$user->name = '佐藤花子';` | インスタンスのnameプロパティを変更 | `->` |
| 3 | `$user->email = 'hanako@example.com';` | インスタンスのemailプロパティを変更 | `->` |
| 4 | `$user->save();` | 変更をデータベースに保存 | `->` |

> **💡 ポイント**: 1行目は`User::find()`で**クラスの静的メソッド**を呼び出しています（`::`）。2〜4行目は`$user`という**インスタンス**に対して操作しています（`->`）。

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

**コードリーディング（1行ずつ分解）**

| 行 | コード | 意味 | 演算子 |
|:---:|:---|:---|:---:|
| 1 | `$user = User::find(1);` | ID=1のユーザーを取得し、インスタンスを`$user`に格納 | `::` |
| 2-5 | `$user->update([...]);` | 配列のデータでインスタンスを更新し、DBに保存 | `->` |

> **💡 ポイント**: `update()`は**インスタンスメソッド**なので、`$user->`で呼び出します。`save()`と違い、`update()`は自動的にDBに保存されます。

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

#### 処理の流れの違い

**`save()`の場合**

```
$user = User::find(1);   // ① インスタンス取得
↓
$user->name = '...';     // ② プロパティ変更（まだDBには反映されない）
↓
$user->save();           // ③ DBに保存
```

**`update()`の場合**

```
$user = User::find(1);   // ① インスタンス取得
↓
$user->update([...]);    // ② プロパティ変更 + DBに保存（一度に実行）
```

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

**コードリーディング**

| 行 | コード | 意味 |
|:---:|:---|:---|
| 8 | `$post = Post::findOrFail($id);` | 指定IDの投稿を取得（なければ404エラー） |
| 9 | `$post->title = $validated['title'];` | インスタンスのtitleプロパティを変更 |
| 10 | `$post->content = $validated['content'];` | インスタンスのcontentプロパティを変更 |
| 11 | `$post->save();` | 変更をDBに保存 |

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

**コードリーディング**

| 行 | コード | 意味 |
|:---:|:---|:---|
| 8 | `$post = Post::findOrFail($id);` | 指定IDの投稿を取得（なければ404エラー） |
| 9 | `$post->update($validated);` | バリデーション済みデータで更新し、DBに保存 |

> **💡 ポイント**: `update()`を使うと、コードが短くなります。

---

### 📊 複数のレコードを一度に更新する

`where()`と`update()`を組み合わせることで、複数のレコードを一度に更新できます。

```php
Post::where('user_id', 1)->update(['is_published' => false]);
```

**コードリーディング（メソッドチェーンの分解）**

| ステップ | コード | 戻り値 | 意味 |
|:---:|:---|:---|:---|
| 1 | `Post::where('user_id', 1)` | クエリビルダ | user_id=1の条件を設定 |
| 2 | `->update(['is_published' => false])` | 更新件数（整数） | 条件に一致するレコードを全て更新 |

> **⚠️ 注意**: この場合の`update()`は**クエリビルダのメソッド**であり、インスタンスメソッドではありません。複数レコードを一括更新するため、`$fillable`のチェックは行われません。

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

**コードリーディング（1行ずつ分解）**

| 行 | コード | 意味 | 演算子 |
|:---:|:---|:---|:---:|
| 1 | `$user = User::find(1);` | ID=1のユーザーを取得し、インスタンスを`$user`に格納 | `::` |
| 2 | `$user->delete();` | インスタンスをデータベースから削除 | `->` |

> **💡 ポイント**: `delete()`は**インスタンスメソッド**なので、`$user->`で呼び出します。

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

**コードリーディング**

| コード | 意味 | 演算子 |
|:---|:---|:---:|
| `User::destroy(1)` | ID=1のユーザーを直接削除 | `::` |

> **💡 ポイント**: `destroy()`は**静的メソッド**なので、`User::`で呼び出します。インスタンスを取得せずに、直接削除できます。

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

### 🔍 `delete()`と`destroy()`の違い

| メソッド | 演算子 | 対象 | 特徴 |
|:---|:---:|:---|:---|
| `delete()` | `->` | インスタンス | インスタンスを取得してから削除 |
| `destroy()` | `::` | クラス（静的メソッド） | IDを指定して直接削除 |

#### 使い分けの目安

| メソッド | 使い所 |
|:---|:---|
| `delete()` | 削除前にデータを確認したい場合、関連データも処理したい場合 |
| `destroy()` | IDが分かっていて、すぐに削除したい場合 |

---

### 📊 複数のレコードを一度に削除する

`where()`と`delete()`を組み合わせることで、複数のレコードを一度に削除できます。

```php
Post::where('user_id', 1)->delete();
```

**コードリーディング（メソッドチェーンの分解）**

| ステップ | コード | 戻り値 | 意味 |
|:---:|:---|:---|:---|
| 1 | `Post::where('user_id', 1)` | クエリビルダ | user_id=1の条件を設定 |
| 2 | `->delete()` | 削除件数（整数） | 条件に一致するレコードを全て削除 |

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

**コードリーディング**

| 行 | コード | 意味 |
|:---|:---|:---|
| `use SoftDeletes;` | SoftDeletesトレイトを使用する宣言 |

> **💡 Tutorial 7の復習**: `use`はトレイトを使用するための構文です。トレイトを使うと、クラスに機能を追加できます。

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

**コードリーディング（メソッドチェーンの分解）**

| ステップ | コード | 戻り値 | 意味 |
|:---:|:---|:---|:---|
| 1 | `Post::withTrashed()` | クエリビルダ | 削除済みも含める条件を設定 |
| 2 | `->get()` | Collection | 全レコードを取得 |

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

**コードリーディング**

| 行 | コード | 意味 |
|:---:|:---|:---|
| 1 | `Post::withTrashed()->find(1)` | 削除済みも含めてID=1の投稿を取得 |
| 2 | `$post->restore();` | インスタンスを復元（deleted_atをNULLに） |

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

#### 間違い3: `delete()`に`::`を使う

```php
// ❌ NG: delete()はインスタンスメソッドなので::は使えない
$user = User::find(1);
User::delete();  // エラー！

// ✅ OK: インスタンスには->を使う
$user = User::find(1);
$user->delete();  // 正しい
```

#### 間違い4: `destroy()`に`->`を使う

```php
// ❌ NG: destroy()は静的メソッドなので->は使えない
$user = User::find(1);
$user->destroy(1);  // 動作するが意味がない

// ✅ OK: クラスには::を使う
User::destroy(1);  // 正しい
```

---

## ✨ まとめ

このセクションでは、Eloquentを使ってデータを更新・削除する方法を学びました。

### 演算子の使い分け

| メソッド | 演算子 | 対象 | 用途 |
|:---|:---:|:---|:---|
| `find()` | `::` | クラス | レコードを取得 |
| `save()` | `->` | インスタンス | 変更を保存 |
| `update()` | `->` | インスタンス | 配列で更新 |
| `delete()` | `->` | インスタンス | レコードを削除 |
| `destroy()` | `::` | クラス | IDで直接削除 |

### ポイント

*   `save()`は、プロパティを変更してから保存する。
*   `update()`は、配列を渡して、一度に更新する。
*   `delete()`は、モデルのインスタンスを取得してから削除する。
*   `destroy()`は、IDを指定して、直接削除する。
*   ソフトデリートを使うことで、データを物理的に削除せず、削除フラグを立てることができる。
*   ソフトデリートされたレコードは、`withTrashed()`や`onlyTrashed()`で取得できる。

次のセクションでは、マスアサインメントと`$fillable`について、さらに詳しく学びます。

---
