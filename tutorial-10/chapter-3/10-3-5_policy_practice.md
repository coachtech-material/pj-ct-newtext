# Tutorial 10-3-5: 実践: ポリシーを使った権限管理

## 🎯 このセクションで学ぶこと

*   小さな実践演習を通じて、ポリシーの作成から適用までを一気通貫で学ぶ。
*   ロールベースの権限管理を実装できるようになる。
*   実際に手を動かして、ポリシーを体感する。

---

## 導入：「理論」から「実践」へ

これまで、ポリシーの作成と適用について学んできました。このセクションでは、**小さな実践演習**を通じて、ポリシーの作成から適用までを一気通貫で学びます。

---

## 実践演習: ブログ記事の権限管理

### 📝 演習の目標

*   ユーザーのロール（一般ユーザー、編集者、管理者）に基づいて、投稿の権限を管理する
*   ポリシーを作成し、コントローラーとBladeで適用する

---

### 🔧 ステップ1: ユーザーテーブルにロールを追加

#### マイグレーション

```bash
sail artisan make:migration add_role_to_users_table
```

**`database/migrations/xxxx_add_role_to_users_table.php`**

```php
public function up()
{
    Schema::table('users', function (Blueprint $table) {
        $table->string('role')->default('user'); // user, editor, admin
    });
}

public function down()
{
    Schema::table('users', function (Blueprint $table) {
        $table->dropColumn('role');
    });
}
```

```bash
sail artisan migrate
```

---

### 🔧 ステップ2: Userモデルにヘルパーメソッドを追加

**`app/Models/User.php`**

```php
public function isAdmin()
{
    return $this->role === 'admin';
}

public function isEditor()
{
    return $this->role === 'editor';
}

public function isUser()
{
    return $this->role === 'user';
}
```

---

### 🔧 ステップ3: ポリシーを作成

```bash
sail artisan make:policy PostPolicy --model=Post
```

**`app/Policies/PostPolicy.php`**

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    // 管理者は全てのアクションを許可
    public function before(User $user, $ability)
    {
        if ($user->isAdmin()) {
            return true;
        }
    }

    // 投稿一覧を閲覧できるか
    public function viewAny(?User $user)
    {
        return true; // 誰でも閲覧可能
    }

    // 投稿を表示できるか
    public function view(?User $user, Post $post)
    {
        // 公開済みの投稿は誰でも閲覧可能
        if ($post->is_published) {
            return true;
        }

        // 下書きは自分のみ閲覧可能
        return $user && $user->id === $post->user_id;
    }

    // 投稿を作成できるか
    public function create(User $user)
    {
        // 認証済みユーザーは投稿を作成できる
        return true;
    }

    // 投稿を更新できるか
    public function update(User $user, Post $post)
    {
        // 編集者は全ての投稿を更新できる
        if ($user->isEditor()) {
            return true;
        }

        // 自分の投稿のみ更新できる
        return $user->id === $post->user_id;
    }

    // 投稿を削除できるか
    public function delete(User $user, Post $post)
    {
        // 編集者は全ての投稿を削除できる
        if ($user->isEditor()) {
            return true;
        }

        // 自分の投稿のみ削除できる
        return $user->id === $post->user_id;
    }

    // 投稿を公開できるか
    public function publish(User $user, Post $post)
    {
        // 編集者以上は全ての投稿を公開できる
        if ($user->isEditor() || $user->isAdmin()) {
            return true;
        }

        // 自分の投稿のみ公開できる
        return $user->id === $post->user_id;
    }
}
```

---

### 🔧 ステップ4: ポリシーを登録

**`app/Providers/AuthServiceProvider.php`**

```php
protected $policies = [
    Post::class => PostPolicy::class,
];
```

---

### 🔧 ステップ5: コントローラーを作成

**`app/Http/Controllers/PostController.php`**

```php
<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function __construct()
    {
        $this->middleware('auth')->except(['index', 'show']);
    }

    public function index()
    {
        $this->authorize('viewAny', Post::class);

        $posts = Post::where('is_published', true)->get();

        return view('posts.index', compact('posts'));
    }

    public function show($id)
    {
        $post = Post::findOrFail($id);

        $this->authorize('view', $post);

        return view('posts.show', compact('post'));
    }

    public function store(Request $request)
    {
        $this->authorize('create', Post::class);

        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'content' => 'required|string',
        ]);

        $post = $request->user()->posts()->create([
            'title' => $validated['title'],
            'content' => $validated['content'],
            'is_published' => false,
        ]);

        return redirect()->route('posts.show', $post->id)
            ->with('success', '投稿を作成しました');
    }

    public function update(Request $request, $id)
    {
        $post = Post::findOrFail($id);

        $this->authorize('update', $post);

        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'content' => 'required|string',
        ]);

        $post->update($validated);

        return redirect()->route('posts.show', $post->id)
            ->with('success', '投稿を更新しました');
    }

    public function destroy($id)
    {
        $post = Post::findOrFail($id);

        $this->authorize('delete', $post);

        $post->delete();

        return redirect()->route('posts.index')
            ->with('success', '投稿を削除しました');
    }

    public function publish($id)
    {
        $post = Post::findOrFail($id);

        $this->authorize('publish', $post);

        $post->update(['is_published' => true]);

        return redirect()->route('posts.show', $post->id)
            ->with('success', '投稿を公開しました');
    }
}
```

---

### 🔧 ステップ6: ルートを定義

**`routes/web.php`**

```php
use App\Http\Controllers\PostController;

Route::get('/posts', [PostController::class, 'index'])->name('posts.index');
Route::get('/posts/{id}', [PostController::class, 'show'])->name('posts.show');

Route::middleware('auth')->group(function () {
    Route::post('/posts', [PostController::class, 'store'])->name('posts.store');
    Route::put('/posts/{id}', [PostController::class, 'update'])->name('posts.update');
    Route::delete('/posts/{id}', [PostController::class, 'destroy'])->name('posts.destroy');
    Route::post('/posts/{id}/publish', [PostController::class, 'publish'])->name('posts.publish');
});
```

---

### 🚀 ステップ7: 動作確認

#### シナリオ1: 一般ユーザー

*   投稿を作成できる
*   自分の投稿のみ更新・削除できる
*   自分の投稿のみ公開できる

#### シナリオ2: 編集者

*   投稿を作成できる
*   全ての投稿を更新・削除できる
*   全ての投稿を公開できる

#### シナリオ3: 管理者

*   全てのアクションを実行できる

---

### 🔍 テストケース

#### テスト1: 一般ユーザーが自分の投稿を更新

1. 一般ユーザーとしてログイン
2. 自分の投稿（ID: 1）の編集画面にアクセス
3. タイトルと内容を変更して保存

**期待される結果**: 成功（投稿が更新される）

---

#### テスト2: 一般ユーザーが他人の投稿を更新

1. 一般ユーザーとしてログイン
2. 他のユーザーの投稿（ID: 2）の編集画面にアクセス

**期待される結果**: 403エラー（アクセス拒否）

---

#### テスト3: 編集者が他人の投稿を更新

1. 編集者としてログイン
2. 他のユーザーの投稿（ID: 2）の編集画面にアクセス
3. タイトルと内容を変更して保存

**期待される結果**: 成功（投稿が更新される）

---

### 💡 TIP: Bladeでの表示制御

```blade
<h1>{{ $post->title }}</h1>
<p>{{ $post->content }}</p>

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

@can('publish', $post)
    @if(!$post->is_published)
        <form action="/posts/{{ $post->id }}/publish" method="POST">
            @csrf
            <button type="submit">公開</button>
        </form>
    @endif
@endcan
```

---

### 🚀 発展演習: ロールの追加

#### 新しいロール: モデレーター

*   投稿を作成できる
*   全ての投稿を閲覧できる
*   不適切な投稿を削除できる

#### ポリシーの更新

```php
public function delete(User $user, Post $post)
{
    // 編集者、モデレーター、管理者は全ての投稿を削除できる
    if ($user->isEditor() || $user->isModerator() || $user->isAdmin()) {
        return true;
    }

    // 自分の投稿のみ削除できる
    return $user->id === $post->user_id;
}
```

---

## ✨ まとめ

このセクションでは、小さな実践演習を通じて、ポリシーの作成から適用までを一気通貫で学びました。

*   ロールベースの権限管理を実装した。
*   ポリシーを作成し、コントローラーで適用した。
*   `before`メソッドを使って、管理者に全ての権限を付与した。

これで、Chapter 9「認可とポリシー」の全5セクションが完了しました。次は、Chapter 10「デバッグとエラーハンドリング」の残りのセクションに進みます。

---
