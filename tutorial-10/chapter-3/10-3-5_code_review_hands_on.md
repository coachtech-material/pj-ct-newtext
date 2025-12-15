# Tutorial 10-3-5: コードレビュー - ハンズオン演習

## 📝 このセクションの目的

Chapter 3で学んだコードレビューを実際に手を動かして確認します。レビュアーとレビュイーの両方の立場を体験しましょう。

---

## 🎯 演習課題：コードレビューを実践しよう

### 📋 要件

1. 以下のコードをレビューして、改善点を指摘してください
2. 指摘に基づいてコードを修正してください

---

## 💡 レビュー対象のコード

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;

class UserController extends Controller
{
    public function index()
    {
        $users = User::all();
        return view('users.index', ['users' => $users]);
    }

    public function store(Request $request)
    {
        $user = new User;
        $user->name = $request->name;
        $user->email = $request->email;
        $user->password = $request->password;
        $user->save();
        
        return redirect('/users');
    }
}
```

---

## 📖 レビューコメント例

### 指摘1: バリデーションがない

```
バリデーションを追加してください。
- 名前は必須、最大50文字
- メールアドレスは必須、メール形式、ユニーク
- パスワードは必須、最小8文字
```

### 指摘2: パスワードがハッシュ化されていない

```
パスワードをハッシュ化してください。
bcrypt()またはHash::make()を使用してください。
```

### 指摘3: Mass assignmentの脆弱性

```
$fillableを設定して、create()メソッドを使用してください。
```

---

## 📖 修正後のコード

```php
<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class UserController extends Controller
{
    public function index()
    {
        $users = User::latest()->paginate(20);
        return view('users.index', ['users' => $users]);
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|max:50',
            'email' => 'required|email|unique:users',
            'password' => 'required|min:8|confirmed',
        ]);

        User::create([
            'name' => $validated['name'],
            'email' => $validated['email'],
            'password' => Hash::make($validated['password']),
        ]);
        
        return redirect()->route('users.index')
            ->with('success', 'ユーザーを作成しました');
    }
}
```

```php
// User.php
protected $fillable = [
    'name',
    'email',
    'password',
];
```

---

## 🎓 レビューのポイント

### セキュリティ

- [ ] バリデーションが実装されているか
- [ ] パスワードがハッシュ化されているか
- [ ] Mass assignmentの脆弱性がないか
- [ ] SQLインジェクション対策がされているか

### パフォーマンス

- [ ] N+1問題がないか
- [ ] ページネーションが実装されているか
- [ ] 不要なクエリがないか

### 可読性

- [ ] 変数名が適切か
- [ ] コメントが適切か
- [ ] コードが整理されているか

### ベストプラクティス

- [ ] Laravelの規約に従っているか
- [ ] DRY原則が守られているか
- [ ] エラーハンドリングが適切か

---

## 💪 自己評価チェックリスト

- [ ] セキュリティの問題を指摘できた
- [ ] パフォーマンスの問題を指摘できた
- [ ] 可読性の問題を指摘できた
- [ ] 建設的なコメントを書けた
- [ ] 指摘に基づいてコードを修正できた

すべてチェックできたら、Tutorial 11に進みましょう！
