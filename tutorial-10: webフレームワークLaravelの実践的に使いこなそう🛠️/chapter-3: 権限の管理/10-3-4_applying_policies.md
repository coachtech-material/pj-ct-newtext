# Tutorial 10-3-4: ポリシーの適用

## 🎯 このセクションで学ぶこと

*   コントローラーやBladeでポリシーを適用し、アクセス制御を実現できるようになる。
*   `authorize()`、`can()`、`cannot()`を使い分けられるようになる。
*   ミドルウェアでポリシーを適用できるようになる。

---

## 導入：「ポリシー」を実際に使う

前のセクションで、ポリシーの作成方法を学びました。このセクションでは、**ポリシーを実際に適用**し、アクセス制御を実現します。

Laravelでは、以下の方法でポリシーを適用できます。

*   コントローラーで`$this->authorize()`を使う
*   `Gate::allows()`や`Gate::denies()`を使う
*   Bladeで`@can`ディレクティブを使う
*   ミドルウェアで`can`を使う

---

## 詳細解説

### 🔧 方法1: コントローラーで`$this->authorize()`

最も一般的な方法は、コントローラーで`$this->authorize()`を使うことです。

**コントローラー**

```php
public function update(Request $request, $id)
{
    $post = Post::findOrFail($id);

    // ポリシーの'update'メソッドをチェック
    $this->authorize('update', $post);

    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'content' => 'required|string',
    ]);

    $post->update($validated);

    return response()->json(['message' => 'Post updated successfully', 'post' => $post]);
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `$this->authorize('update', $post)` | ポリシーの`update`メソッドをチェックします。許可されない場合、自動的に403エラーが返されます |

---

### 🔧 方法2: `Gate::allows()`や`Gate::denies()`

**コントローラー**

```php
use Illuminate\Support\Facades\Gate;

public function destroy($id)
{
    $post = Post::findOrFail($id);

    if (Gate::denies('delete', $post)) {
        return response()->json(['message' => 'Unauthorized'], 403);
    }

    $post->delete();

    return response()->json(['message' => 'Post deleted successfully']);
}
```

---

### 🔧 方法3: `$request->user()->can()`

**コントローラー**

```php
public function show(Request $request, $id)
{
    $post = Post::findOrFail($id);

    if ($request->user()->cannot('view', $post)) {
        return response()->json(['message' => 'Unauthorized'], 403);
    }

    return response()->json(['post' => $post]);
}
```

---

### 🚀 実践例1: Bladeで`@can`ディレクティブ

Bladeテンプレートでポリシーに基づいて表示を切り替える例です。

**Bladeテンプレート**

```blade
@can('update', $post)
    <a href="/posts/{{ $post->id }}/edit">編集</a>
@endcan

@can('delete', $post)
    <form action="/posts/{{ $post->id }}" method="POST">
        @csrf
        @method('DELETE')
        <button type="submit">削除</button>
    </form>
@endcan

@cannot('update', $post)
    <p>編集する権限がありません</p>
@endcannot
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `@can('update', $post)` | ログインユーザーが`$post`に対して`update`権限を持つ場合のみ、内部のHTMLを表示します |
| `@endcan` | `@can`ブロックの終了を示します |
| `@can('delete', $post)` | ログインユーザーが`$post`に対して`delete`権限を持つ場合のみ、削除フォームを表示します |
| `@csrf` | CSRF保護のためのトークンを埋め込みます |
| `@method('DELETE')` | DELETEメソッドをシミュレートするための隠しフィールドを生成します |
| `@cannot('update', $post)` | `update`権限を持たない場合のみ、内部のHTMLを表示します |
| `@endcannot` | `@cannot`ブロックの終了を示します |

---

### 🚀 実践例2: ミドルウェアでポリシーを適用

ルート定義でミドルウェアを使ってポリシーを適用する例です。

**ルート**

```php
Route::put('/posts/{post}', [PostController::class, 'update'])
    ->middleware('can:update,post');
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `Route::put('/posts/{post}', ...)` | PUTメソッドで`/posts/{post}`へのルートを定義します。`{post}`はルートパラメータです |
| `->middleware('can:update,post')` | `can`ミドルウェアを適用し、ポリシーの`update`メソッドをチェックします |
| `can:update,post` | `update`はポリシーのメソッド名、`post`はルートパラメータ名です。Laravelが自動的にモデルを解決します |

---

### 🚀 実践例3: リソースコントローラーでポリシーを自動適用

リソースコントローラーの全メソッドに対して、ポリシーを自動的に適用する例です。

**コントローラー**

```php
class PostController extends Controller
{
    public function __construct()
    {
        $this->authorizeResource(Post::class, 'post');
    }

    public function index()
    {
        // viewAnyポリシーが自動適用される
        $posts = Post::all();
        return view('posts.index', compact('posts'));
    }

    public function show(Post $post)
    {
        // viewポリシーが自動適用される
        return view('posts.show', compact('post'));
    }

    public function edit(Post $post)
    {
        // updateポリシーが自動適用される
        return view('posts.edit', compact('post'));
    }

    public function update(Request $request, Post $post)
    {
        // updateポリシーが自動適用される
        $post->update($request->validated());
        return redirect()->route('posts.show', $post);
    }

    public function destroy(Post $post)
    {
        // deleteポリシーが自動適用される
        $post->delete();
        return redirect()->route('posts.index');
    }
}
```

**コードリーディング**

| コード | 説明 |
|:---|:---|
| `public function __construct()` | コントローラーのコンストラクタです。インスタンス生成時に実行されます |
| `$this->authorizeResource(Post::class, 'post')` | リソースコントローラーのメソッドに対して、自動的にポリシーを適用します |
| `Post::class` | ポリシーを適用するモデルクラスを指定します |
| `'post'` | ルートパラメータ名を指定します。`{post}`に対応します |

**メソッドとポリシーの対応表**

| コントローラーメソッド | ポリシーメソッド |
|:---|:---|
| `index` | `viewAny` |
| `show` | `view` |
| `create` | `create` |
| `store` | `create` |
| `edit` | `update` |
| `update` | `update` |
| `destroy` | `delete` |

---

### 💡 TIP: `forUser()`

特定のユーザーに対してポリシーをチェックする場合、`forUser()`を使います。

```php
if (Gate::forUser($otherUser)->allows('update', $post)) {
    // ...
}
```

---

### 🚨 よくある間違い

**間違い1: ポリシーをチェックせずにアクションを実行**

```php
public function destroy($id)
{
    $post = Post::findOrFail($id);

    // ポリシーをチェックしていない
    $post->delete(); // NG

    return response()->json(['message' => 'Post deleted successfully']);
}
```

**対処法**: ポリシーをチェックします。

```php
public function destroy($id)
{
    $post = Post::findOrFail($id);

    $this->authorize('delete', $post); // OK

    $post->delete();

    return response()->json(['message' => 'Post deleted successfully']);
}
```

---

**間違い2: ルートパラメータ名を間違える**

```php
// ルート
Route::put('/posts/{id}', [PostController::class, 'update'])
    ->middleware('can:update,post'); // NG: パラメータ名は'id'

// 正しい
Route::put('/posts/{post}', [PostController::class, 'update'])
    ->middleware('can:update,post'); // OK
```

---

## ✨ まとめ

このセクションでは、ポリシーの適用方法を学びました。

*   コントローラーで`$this->authorize()`を使って、ポリシーを適用できる。
*   `Gate::allows()`や`Gate::denies()`を使って、ポリシーをチェックできる。
*   Bladeで`@can`ディレクティブを使って、ポリシーに基づいて表示を切り替えられる。
*   ミドルウェアで`can`を使って、ルート全体にポリシーを適用できる。

次のセクションでは、ポリシーを使った権限管理の実践演習を行います。

---
