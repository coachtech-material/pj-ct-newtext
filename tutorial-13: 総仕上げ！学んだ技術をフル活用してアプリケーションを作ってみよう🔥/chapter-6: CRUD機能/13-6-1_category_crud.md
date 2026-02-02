# 13-6-1 カテゴリーCRUD実装

## 🎯 このセクションで学ぶこと

このセクションでは、カテゴリーのCRUD（Create, Read, Update, Delete）機能を実装します。

- リソースコントローラの作成
- ルーティングの設定（リソースルート）
- バリデーションの実装
- CRUD用ビューの作成

> **📌 対応Issue**: #4 カテゴリーCRUD実装

---

## 🧠 先輩エンジニアの思考プロセス

CRUD機能を実装する際、先輩エンジニアは以下のように考えます。

> 「CRUDはWebアプリの基本だ。Laravelではリソースコントローラを使うと、CRUD操作に対応する7つのメソッドが自動で用意される。ルーティングも`Route::resource()`で一括設定できるから効率的だ。」

### リソースコントローラの7つのメソッド

| メソッド | HTTPメソッド | URL | 用途 |
|:---|:---|:---|:---|
| `index` | GET | /categories | 一覧表示 |
| `create` | GET | /categories/create | 作成フォーム表示 |
| `store` | POST | /categories | 新規作成処理 |
| `show` | GET | /categories/{id} | 詳細表示 |
| `edit` | GET | /categories/{id}/edit | 編集フォーム表示 |
| `update` | PUT/PATCH | /categories/{id} | 更新処理 |
| `destroy` | DELETE | /categories/{id} | 削除処理 |

---

## 🔀 ブランチの作成

Issue駆動開発のワークフローに従い、まずはIssue #4に対応するブランチを作成します。

```bash
# 現在のブランチを確認（mainにいることを確認）
git branch

# mainブランチの最新状態を取得
git pull origin main

# Issue #4 に対応するブランチを作成して切り替え
git switch -c feature/issue-4-category-crud
```

---

## 🏃 実践

### ステップ1: カテゴリーコントローラの作成

リソースコントローラを作成します。

```bash
# リソースコントローラの作成
sail artisan make:controller CategoryController --resource
```

#### コマンドのコードリーディング

| オプション | 説明 |
|:---|:---|
| `--resource` | CRUD操作用の7つのメソッドを自動生成 |

---

### ステップ2: コントローラの実装

`app/Http/Controllers/CategoryController.php` を以下のように編集します。

```php
<?php

namespace App\Http\Controllers;

use App\Models\Category;
use Illuminate\Http\Request;

class CategoryController extends Controller
{
    /**
     * カテゴリー一覧を表示
     */
    public function index()
    {
        $categories = Category::withCount('tasks')->orderBy('created_at', 'desc')->get();

        return view('categories.index', compact('categories'));
    }

    /**
     * カテゴリー作成フォームを表示
     */
    public function create()
    {
        return view('categories.create');
    }

    /**
     * カテゴリーを新規作成
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255|unique:categories,name',
        ], [
            'name.required' => 'カテゴリー名は必須です。',
            'name.max' => 'カテゴリー名は255文字以内で入力してください。',
            'name.unique' => 'このカテゴリー名は既に使用されています。',
        ]);

        Category::create($validated);

        return redirect()->route('categories.index')
            ->with('success', 'カテゴリーを作成しました。');
    }

    /**
     * カテゴリー詳細を表示
     */
    public function show(Category $category)
    {
        $category->load('tasks');

        return view('categories.show', compact('category'));
    }

    /**
     * カテゴリー編集フォームを表示
     */
    public function edit(Category $category)
    {
        return view('categories.edit', compact('category'));
    }

    /**
     * カテゴリーを更新
     */
    public function update(Request $request, Category $category)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255|unique:categories,name,' . $category->id,
        ], [
            'name.required' => 'カテゴリー名は必須です。',
            'name.max' => 'カテゴリー名は255文字以内で入力してください。',
            'name.unique' => 'このカテゴリー名は既に使用されています。',
        ]);

        $category->update($validated);

        return redirect()->route('categories.index')
            ->with('success', 'カテゴリーを更新しました。');
    }

    /**
     * カテゴリーを削除
     */
    public function destroy(Category $category)
    {
        // カテゴリーに紐づくタスクがある場合は削除不可
        if ($category->tasks()->count() > 0) {
            return redirect()->route('categories.index')
                ->with('error', 'タスクが紐づいているカテゴリーは削除できません。');
        }

        $category->delete();

        return redirect()->route('categories.index')
            ->with('success', 'カテゴリーを削除しました。');
    }
}
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `Category::withCount('tasks')` | 各カテゴリーのタスク数を`tasks_count`として取得 |
| `$request->validate([...])` | リクエストデータのバリデーション |
| `'unique:categories,name,' . $category->id` | 更新時は自分自身を除外してユニークチェック |
| `compact('categories')` | 変数をビューに渡す（`['categories' => $categories]`と同等） |
| `Category $category` | ルートモデルバインディング（IDから自動的にモデルを取得） |
| `$category->load('tasks')` | リレーションを遅延ロード |
| `->with('success', ...)` | フラッシュメッセージをセッションに保存 |

---

### ステップ3: ルーティングの設定

`routes/web.php` にカテゴリーのルーティングを追加します。

```php
<?php

use App\Http\Controllers\CategoryController;
use App\Http\Controllers\TaskController;
use Illuminate\Support\Facades\Route;

Route::get('/', function () {
    return redirect()->route('login');
});

// 認証が必要なルート
Route::middleware('auth')->group(function () {
    // カテゴリーのCRUDルート
    Route::resource('categories', CategoryController::class);

    // タスクのCRUDルート（次のセクションで追加）
    // Route::resource('tasks', TaskController::class);
});
```

#### コードリーディング

| コード | 説明 |
|:---|:---|
| `Route::middleware('auth')` | 認証済みユーザーのみアクセス可能 |
| `->group(function () {...})` | グループ内のルートに共通のミドルウェアを適用 |
| `Route::resource('categories', ...)` | 7つのCRUDルートを一括登録 |

#### 登録されるルートの確認

```bash
# ルート一覧を確認
sail artisan route:list --name=categories
```

---

### ステップ4: ビューの確認

カテゴリー用のビューファイルは、Chapter 3-2で配置済みです。

| ファイル | 説明 |
|:---|:---|
| `resources/views/categories/index.blade.php` | 一覧画面 |
| `resources/views/categories/create.blade.php` | 作成画面 |
| `resources/views/categories/edit.blade.php` | 編集画面 |

> **📌 補足**: ビューの詳細な内容については、Chapter 3-2「提供アセット」を参照してください。

---

### ステップ5: 動作確認

以下のURLにアクセスして動作を確認してください。

| URL | 機能 |
|:---|:---|
| `http://localhost/categories` | カテゴリー一覧 |
| `http://localhost/categories/create` | カテゴリー作成 |
| `http://localhost/categories/1` | カテゴリー詳細 |
| `http://localhost/categories/1/edit` | カテゴリー編集 |

#### 確認手順

1. ログインする
2. カテゴリー一覧画面にアクセス
3. 「新規作成」からカテゴリーを作成
4. 作成したカテゴリーを編集
5. カテゴリーを削除

---

## 💡 TIP: ルートモデルバインディング

Laravelでは、コントローラのメソッド引数にモデルを型宣言すると、URLのIDから自動的にモデルを取得してくれます。

```php
// ルートモデルバインディングを使用
public function show(Category $category)
{
    // $category には ID=1 のカテゴリーが自動的に入る
    return view('categories.show', compact('category'));
}

// 手動で取得する場合（ルートモデルバインディングを使わない）
public function show($id)
{
    $category = Category::findOrFail($id);
    return view('categories.show', compact('category'));
}
```

---

## ❌ よくある間違い

### 1. @method を忘れる

```php
// ❌ NG: @method('PUT') がない
<form method="POST" action="{{ route('categories.update', $category) }}">
    @csrf
    <!-- @method('PUT') がない -->
</form>
// 結果: store メソッドが呼ばれてしまう
```

**対処法**: 更新（PUT/PATCH）や削除（DELETE）には必ず `@method` を追加する。

### 2. バリデーションエラーメッセージを日本語化していない

```php
// ❌ NG: エラーメッセージが英語
$request->validate([
    'name' => 'required|string|max:255',
]);
// エラー: "The name field is required."
```

**対処法**: バリデーションの第2引数でカスタムメッセージを指定する。

---

## ✅ 完了条件

以下の条件を満たしていることを確認してください。

- [ ] CategoryControllerが作成されている
- [ ] ルーティングが設定されている
- [ ] カテゴリー一覧が表示される
- [ ] カテゴリーの作成・編集・削除ができる
- [ ] バリデーションが動作する

---

## ✨ まとめ

このセクションでは、カテゴリーのCRUD機能を実装しました。

| 学んだこと | 内容 |
|:---|:---|
| リソースコントローラ | `sail artisan make:controller --resource` |
| リソースルート | `Route::resource()` で7つのルートを一括登録 |
| ルートモデルバインディング | URLのIDから自動的にモデルを取得 |
| バリデーション | `$request->validate()` でリクエストを検証 |

次のセクションでは、タスクのCRUD機能を実装します。

---

## 🔄 Git操作とプルリクエスト

作業が完了したら、変更をコミットしてプッシュし、プルリクエストを作成して変更内容を確認しましょう。

### ステップ1: コミットとプッシュ

```bash
# 変更をステージング
git add .

# コミット（Issue番号を含める）
git commit -m "feat: カテゴリーCRUD実装 #4"

# リモートにプッシュ
git push origin feature/issue-4-category-crud
```

### ステップ2: プルリクエストの作成と確認

GitHubでプルリクエストを作成し、変更内容を確認してみましょう。

1. GitHubのリポジトリページを開く
2. 「Pull requests」タブをクリックする
3. 「New pull request」ボタンをクリックする
4. `base: main` ← `compare: feature/issue-4-category-crud` を選択する
5. 「Create pull request」ボタンをクリックする
6. 以下の内容を入力する

**タイトル**:
```
feat: カテゴリーCRUD実装
```

**説明欄**:
```markdown
## 概要
カテゴリーのCRUD機能を実装しました。

## 変更内容
- CategoryControllerの作成
- カテゴリー用ビューの作成（index, create, show, edit）
- ルーティングの設定

## 動作確認
- [ ] カテゴリー一覧が表示される
- [ ] カテゴリーの作成ができる
- [ ] カテゴリーの編集ができる
- [ ] カテゴリーの削除ができる

## 対応Issue
close #4
```

7. 「Create pull request」ボタンをクリックする

> **💡 確認ポイント**: PRを作成したら、「Files changed」タブで変更内容を確認してみましょう。コントローラ、ビュー、ルーティングがそれぞれどのように実装されているかを確認することで、コードの全体像を把握できます。

### ステップ3: プルリクエストのマージ

変更内容を確認したら、PRをマージします。

1. PRのページで「Merge pull request」ボタンをクリックする
2. 「Confirm merge」ボタンをクリックする
3. マージが完了すると、Issue #4が自動的にクローズされる

### ステップ4: ローカルのmainブランチを更新し、ブランチを削除

```bash
# mainブランチに切り替え
git switch main

# リモートの変更を取り込む
git pull origin main

# マージ済みのブランチを削除
git branch -d feature/issue-4-category-crud
```

> **📌 Issue対応**: PRをマージすると、説明欄の `close #4` によりIssue #4が自動的にクローズされます。
