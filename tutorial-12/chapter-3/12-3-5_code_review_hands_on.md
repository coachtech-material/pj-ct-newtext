# Tutorial 12-3-5: コードレビュー - ハンズオン演習

## 📝 このセクションの目的

Chapter 3で学んだコードレビューを実際に手を動かして確認します。レビュアーとレビュイーの両方の立場を体験しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのディレクトリを作成します。

```
~/git-practice/
├── 12-3-5_hands-on/                      ← このハンズオン用のディレクトリ
│   ├── code-review-practice/             ← 要件を見て自分で修正するディレクトリ
│   │   └── UserController.php
│   └── code-review-sample/               ← 実践で一緒に修正するディレクトリ
│       └── UserController.php
└── ...
```

| ディレクトリ | 用途 |
|:---|:---|
| `code-review-practice/` | 📋 要件を見て、自分の力でコードを修正する |
| `code-review-sample/` | 🏃 実践セクションで、一緒に手を動かしながら修正する |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて修正したコードと、解答を見ながら修正したコードを比較することで、理解が深まります。

---

## 🎯 演習課題：コードレビューを実践しよう

### 🖼️ 完成イメージ

<!-- レビュー前後のコード比較のスクリーンショットをここに配置 -->
![12-3-5 完成イメージ](images/12-3-5_code_review_complete.png)

**この演習で作るもの**：
問題のあるコードをレビューし、改善点を指摘し、修正する「コードレビュー」を実践します。

---

### 📋 要件

1. 以下のコードをレビューして、改善点を指摘してください
2. 指摘に基づいてコードを修正してください

---

### ✅ 完成品の確認方法

**🔧 コードの確認**

- **確認方法**: 修正後のコードを模範解答と比較
- **確認手順**:
  1. レビューコメントを文書化
  2. コードを修正
  3. 模範解答と比較

**正しく実装できていれば**:
- [ ] バリデーションが追加されている
- [ ] エラーハンドリングが追加されている
- [ ] N+1問題が解決されている
- [ ] セキュリティ上の問題が修正されている
- [ ] コードの可読性が向上している

**レビューコメントの例**:

```markdown
## レビューコメント

### 1. バリデーションがない
- 場所: store()メソッド
- 問題: 入力値のバリデーションが行われていない
- 提案: FormRequestまたはvalidate()を使用

### 2. N+1問題
- 場所: index()メソッド
- 問題: User::all()ではリレーションが遅延読み込みされる
- 提案: with()でEager Loadingを使用
```

---

## 🔧 環境準備（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のディレクトリを準備します。

```bash
# git-practiceディレクトリに移動（なければ作成）
mkdir -p ~/git-practice
cd ~/git-practice

# ハンズオン用ディレクトリを作成
mkdir -p 12-3-5_hands-on
cd 12-3-5_hands-on

# 自分で作成する用のディレクトリを作成
mkdir code-review-practice
cd code-review-practice
```

**レビュー対象のコードを作成**します。以下の内容で`UserController.php`を作成してください：

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

**✅ ディレクトリ構造の確認**

```
~/git-practice/
└── 12-3-5_hands-on/
    └── code-review-practice/     ← 自分で作成する用（今ここ）
        └── UserController.php
```

> 💡 **環境構築が完了！**
> 
> このコードをレビューして、問題点を見つけ、修正してみましょう。

**ここから先は、自分の力でレビュー・修正してみましょう！**

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

> 📌 **注意**: ここからは`code-review-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のディレクトリで進めましょう。

---

### 💻 環境準備（実践用ディレクトリ）

**実践用のディレクトリを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/git-practice/12-3-5_hands-on

# 実践用のディレクトリを作成
mkdir code-review-sample
cd code-review-sample
```

**レビュー対象のコードを作成**します。以下の内容で`UserController.php`を作成してください：

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

**✅ ディレクトリ構造の確認**

```
~/git-practice/
└── 12-3-5_hands-on/
    ├── code-review-practice/     ← 自分で作成した用
    │   └── UserController.php
    └── code-review-sample/       ← 実践用（今ここ）
        └── UserController.php
```

---

### 💭 実装の思考プロセス

コードレビューを進める際、以下の観点で考えると効率的です：

1. **セキュリティ**：脆弱性がないか
2. **パフォーマンス**：効率的な処理か
3. **可読性**：読みやすいコードか
4. **ベストプラクティス**：規約に従っているか

---

### 📝 ステップバイステップで実装

#### ステップ1: コードを読んで理解する

**何を考えているか**：
- 「このコードは何をしているのか？」
- 「ユーザーの一覧表示と登録機能を実装している」

まずはコード全体を読んで、何をしているかを理解します。このコードはユーザーの一覧表示と登録機能を実装しています。

---

#### ステップ2: セキュリティの観点でレビューする

**何を考えているか**：
- 「セキュリティの問題はないか？」
- 「バリデーションはあるか？」
- 「パスワードは安全に保存されているか？」

セキュリティの観点で問題を探します。このコードには以下の問題があります：

| 問題 | 説明 | リスク |
|:---|:---|:---|
| **バリデーションがない** | 不正なデータが登録される可能性 | 高 |
| **パスワードがハッシュ化されていない** | 平文で保存される危険 | 高 |
| **Mass assignmentの脆弱性** | 予期しないフィールドが更新される可能性 | 中 |

---

#### ステップ3: パフォーマンスの観点でレビューする

**何を考えているか**：
- 「パフォーマンスの問題はないか？」
- 「大量のデータがあった場合どうなるか？」

パフォーマンスの観点で問題を探します：

| 問題 | 説明 | リスク |
|:---|:---|:---|
| **User::all()** | 全件取得はメモリを圧迫する | 中 |
| **ページネーションがない** | 大量のユーザーがいると表示が遅くなる | 中 |

---

#### ステップ4: 具体的な改善提案をする

**何を考えているか**：
- 「問題を指摘するだけでなく、解決策を提案しよう」
- 「建設的なフィードバックを心がけよう」

問題を指摘するだけでなく、具体的な改善方法を提案します。

**レビューコメント例**：

```
【指摘1】バリデーションを追加してください。
- 名前は必須、最大50文字
- メールアドレスは必須、メール形式、ユニーク
- パスワードは必須、最小8文字

【指摘2】パスワードをハッシュ化してください。
bcrypt()またはHash::make()を使用してください。

【指摘3】$fillableを設定して、create()メソッドを使用してください。

【指摘4】User::all()をpaginate()に変更してください。
```

---

#### ステップ5: コードを修正する

**何を考えているか**：
- 「レビューコメントに基づいてコードを修正しよう」
- 「セキュリティ問題を解決しよう」

`UserController.php`を以下のように修正します：

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

**修正内容の解説**：

| 修正箇所 | 修正前 | 修正後 | 理由 |
|:---|:---|:---|:---|
| 一覧取得 | `User::all()` | `User::latest()->paginate(20)` | パフォーマンス向上 |
| バリデーション | なし | `$request->validate()` | セキュリティ向上 |
| パスワード | `$request->password` | `Hash::make()` | セキュリティ向上 |
| 登録方法 | `new User` + `save()` | `User::create()` | ベストプラクティス |
| リダイレクト | `redirect('/users')` | `redirect()->route()` | 保守性向上 |

---

### ✨ 完成！

これでコードレビューが実践できました！セキュリティの観点で問題を発見し、具体的な改善提案をするスキルが身につきましたね。

**自分で修正したコードと比較してみましょう**：
- `code-review-practice/UserController.php`: 自分で修正したコード
- `code-review-sample/UserController.php`: 一緒に修正したコード

両方のファイルを比較して、修正内容を確認してみてください。

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
// User.php（モデル）
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

- ✅ コードをセキュリティの観点でレビューできる
- ✅ パフォーマンスの問題を発見できる
- ✅ 具体的な改善提案ができる
- ✅ レビューコメントに基づいてコードを修正できる

引き続き、次のセクションも頑張りましょう！

---
