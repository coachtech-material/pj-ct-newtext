# Tutorial 11-3-5: コードレビュー - ハンズオン演習

## 📝 このセクションの目的

Chapter 3で学んだコードレビューを実際に手を動かして確認します。レビュアーとレビュイーの両方の立場を体験しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

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

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？コードレビューはコード品質を向上させる重要なプロセスです。一緒に手を動かしながら、レビューの観点と修正方法を学んでいきましょう。

### 💭 実装の思考プロセス

コードレビューを進める際、以下の観点で考えると効率的です。セキュリティ、パフォーマンス、保守性を意識します。

---

### 📝 ステップバイステップで実装

#### ステップ1: コードを読んで理解する

まずはコード全体を読んで、何をしているかを理解します。このコードはユーザーの一覧表示と登録機能を実装しています。

---

#### ステップ2: セキュリティの観点でレビューする

セキュリティの観点で問題を探します。このコードには以下の問題があります：

1. **バリデーションがない**：不正なデータが登録される可能性
2. **パスワードがハッシュ化されていない**：平文で保存される危険
3. **Mass assignmentの脆弱性**：予期しないフィールドが更新される可能性

---

#### ステップ3: 具体的な改善提案をする

問題を指摘するだけでなく、具体的な改善方法を提案します。建設的なフィードバックを心がけます。

---

#### ステップ4: コードを修正する

レビューコメントに基づいてコードを修正します。セキュリティ問題を解決し、コード品質を向上させます。

---

### ✨ 完成！

これでコードレビューが実践できました！セキュリティの観点で問題を発見し、具体的な改善提案をするスキルが身につきましたね。

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

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ Chapter 3で学んだコードレビューを実際に手を動かして確認します。レビュアーとレビュイーの両方の立場を体験しましょう。

引き続き、次のセクションも頑張りましょう！

---
