# Tutorial 9-9-6: 認可機能 - ハンズオン演習

## 📝 このセクションの目的

Chapter 9で学んだ認可機能を実際に手を動かして確認します。ポリシーを使って、ユーザーごとのアクセス制御を実装しましょう。

---

## 🎯 演習課題：投稿の編集権限制御

### 📋 要件

1. `PostPolicy`を作成
2. 投稿の作成者のみが編集・削除できるようにする
3. コントローラーで`authorize()`を使用

---

## 💡 ヒント

```bash
php artisan make:policy PostPolicy --model=Post
```

```php
public function update(User $user, Post $post)
{
    return $user->id === $post->user_id;
}

// コントローラー
$this->authorize('update', $post);
```

---

## 📖 模範解答

### PostPolicy.php

```php
<?php

namespace App\Policies;

use App\Models\Post;
use App\Models\User;

class PostPolicy
{
    public function update(User $user, Post $post)
    {
        return $user->id === $post->user_id;
    }

    public function delete(User $user, Post $post)
    {
        return $user->id === $post->user_id;
    }
}
```

### PostController.php

```php
public function edit($id)
{
    $post = Post::findOrFail($id);
    $this->authorize('update', $post);
    return view('posts.edit', ['post' => $post]);
}

public function update(Request $request, $id)
{
    $post = Post::findOrFail($id);
    $this->authorize('update', $post);
    $post->update($request->all());
    return redirect('/posts');
}

public function destroy($id)
{
    $post = Post::findOrFail($id);
    $this->authorize('delete', $post);
    $post->delete();
    return redirect('/posts');
}
```

### posts/index.blade.php

```blade
@foreach ($posts as $post)
    <div>
        <h3>{{ $post->title }}</h3>
        @can('update', $post)
            <a href="{{ route('posts.edit', $post->id) }}">編集</a>
        @endcan
        @can('delete', $post)
            <form action="{{ route('posts.destroy', $post->id) }}" method="POST">
                @csrf
                @method('DELETE')
                <button type="submit">削除</button>
            </form>
        @endcan
    </div>
@endforeach
```

---

## 💪 自己評価チェックリスト

- [ ] ポリシーを作成できた
- [ ] authorize()で認可チェックができた
- [ ] @canでビューに認可ロジックを適用できた

すべてチェックできたら、Chapter 10に進みましょう！
