# Tutorial 9-9-4: ポリシーの適用

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

#### コントローラー

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

*   `$this->authorize('update', $post)`: ポリシーの`update`メソッドをチェック
*   許可されない場合、自動的に403エラーが返される

---

### 🔧 方法2: `Gate::allows()`や`Gate::denies()`

#### コントローラー

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

#### コントローラー

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

#### Bladeテンプレート

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

---

### 🚀 実践例2: ミドルウェアでポリシーを適用

#### ルート

```php
Route::put('/posts/{id}', [PostController::class, 'update'])
    ->middleware('can:update,post');
```

**コードリーディング**

*   `can:update,post`: ポリシーの`update`メソッドをチェック
*   `post`は、ルートパラメータ`{id}`から自動的に解決される

---

### 🚀 実践例3: リソースコントローラーでポリシーを自動適用

#### コントローラー

```php
public function __construct()
{
    $this->authorizeResource(Post::class, 'post');
}
```

**コードリーディング**

*   `authorizeResource()`: リソースコントローラーのメソッドに対して、自動的にポリシーを適用
*   `index` → `viewAny`
*   `show` → `view`
*   `create` → `create`
*   `store` → `create`
*   `edit` → `update`
*   `update` → `update`
*   `destroy` → `delete`

---

### 🚀 実践例4: カスタムメッセージ

#### コントローラー

```php
public function destroy($id)
{
    $post = Post::findOrFail($id);

    $this->authorize('delete', $post);

    $post->delete();

    return response()->json(['message' => 'Post deleted successfully']);
}
```

#### ポリシー

```php
use Illuminate\Auth\Access\Response;

public function delete(User $user, Post $post)
{
    if ($user->id === $post->user_id) {
        return Response::allow();
    }

    return Response::deny('You do not own this post.');
}
```

---

### 🚀 実践例5: 複数のモデルをチェック

#### コントローラー

```php
public function addComment(Request $request, $postId)
{
    $post = Post::findOrFail($postId);

    // 投稿を表示できるかチェック
    $this->authorize('view', $post);

    // コメントを作成できるかチェック
    $this->authorize('create', Comment::class);

    $validated = $request->validate([
        'content' => 'required|string',
    ]);

    $comment = $post->comments()->create([
        'user_id' => auth()->id(),
        'content' => $validated['content'],
    ]);

    return response()->json(['message' => 'Comment added successfully', 'comment' => $comment], 201);
}
```

---

### 💡 TIP: `forUser()`

特定のユーザーに対してポリシーをチェックする場合、`forUser()`を使います。

```php
if (Gate::forUser($otherUser)->allows('update', $post)) {
    // ...
}
```

---

### 🚀 実践例6: APIレスポンスでポリシーをチェック

#### コントローラー

```php
public function index(Request $request)
{
    $posts = Post::all();

    $posts = $posts->map(function ($post) use ($request) {
        return [
            'id' => $post->id,
            'title' => $post->title,
            'content' => $post->content,
            'can_update' => $request->user()->can('update', $post),
            'can_delete' => $request->user()->can('delete', $post),
        ];
    });

    return response()->json(['posts' => $posts]);
}
```

---

### 🚨 よくある間違い

#### 間違い1: ポリシーをチェックせずにアクションを実行

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

#### 間違い2: ルートパラメータ名を間違える

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
