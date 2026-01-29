# Tutorial 13-2-3: 書籍登録機能の実装

## 🎯 このセクションで学ぶこと

- 書籍登録画面のcreate/storeメソッドを実装する
- バリデーションを設定する
- イシュー駆動開発のフローを継続する

---

## Step 0: 開発の準備（チケット駆動）

### 0-1. GitHubでIssueを確認

GitHubで `#2 書籍登録機能` のIssueを確認します。

### 0-2. mainブランチを最新化

```bash
git checkout main
git pull origin main
```

### 0-3. Issue番号付きブランチを作成

```bash
git switch -c feature/issue-2-book-create
```

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ一覧の次に登録機能なのか？」

一覧画面ができたら、次は**登録機能**を作ります。

### 理由1: データを増やせるようになる

```
❌ 詳細・編集・削除から作る
→ テストデータがTinkerで作った1件だけ
→ テストのバリエーションが少ない

✅ 登録機能を先に作る
→ 画面からデータを作成できる
→ 色々なデータでテストできる
```

### 理由2: CRUDの「C」から始める

CRUDの順番は「作成→読み取り→更新→削除」ですが、一覧（R）の次は登録（C）が自然です。

---

### このセクションの実装順序

| 順番 | 作業 | 理由 |
|:---:|:---|:---|
| 1 | createメソッド実装 | 登録画面を表示するため |
| 2 | storeメソッド実装 | フォーム送信を受け取るため |
| 3 | 動作確認 | 登録が正しく動くかテスト |

---

### コードの実装順序（storeメソッド）

```php
public function store(Request $request)
{
    // ① まずバリデーション
    $validated = $request->validate([...]);
    
    // ② 検証済みデータで作成
    Book::create($validated);
    
    // ③ 一覧にリダイレクト
    return redirect()->route('books.index')->with('success', '...');
}
```

| 順番 | コード | 考え方 |
|:---:|:---|:---|
| ① | `$request->validate([...])` | 「入力は正しいか？」を確認 |
| ② | `Book::create($validated)` | 「データを保存」 |
| ③ | `return redirect()...` | 「結果を見せる」 |

---

## Step 1: createメソッドの実装

### 1-1. BookControllerを編集

**ファイル**: `app/Http/Controllers/BookController.php`

```php
/**
 * 書籍登録画面を表示
 */
public function create()
{
    return view('books.create');
}
```

---

## Step 2: storeメソッドの実装

### 2-1. storeメソッドを実装

**ファイル**: `app/Http/Controllers/BookController.php`

```php
/**
 * 書籍を登録
 */
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|max:255',
        'author' => 'required|max:255',
        'rating' => 'required|integer|min:1|max:5',
        'review' => 'nullable|max:10000',
    ]);

    Book::create($validated);

    return redirect()
        ->route('books.index')
        ->with('success', '書籍を登録しました。');
}
```

---

### 2-2. コードリーディング

#### `$request->validate([...])`の分解

| 部分 | 説明 |
|:---|:---|
| `$request` | HTTPリクエストオブジェクト |
| `->validate([...])` | バリデーションを実行 |
| 戻り値 | 検証済みデータの配列 |

#### バリデーションルールの読み方

| ルール | 説明 |
|:---|:---|
| `'required'` | 必須項目（空はエラー） |
| `'max:255'` | 最大255文字 |
| `'integer'` | 整数のみ許可 |
| `'min:1\|max:5'` | 1以上5以下 |
| `'nullable'` | NULL許可（任意項目） |

#### `redirect()->route('books.index')->with('success', '...')`の分解

| 部分 | 説明 | 戻り値 |
|:---|:---|:---|
| `redirect()` | リダイレクトレスポンスを作成 | RedirectResponse |
| `->route('books.index')` | books.indexルートにリダイレクト | RedirectResponse |
| `->with('success', '...')` | フラッシュメッセージをセッションに保存 | RedirectResponse |

> 💡 **メソッドチェーンの流れ**: `redirect()` → `route()` → `with()` と順番に処理が連鎖します。

---

## Step 3: 動作確認

### 3-1. ブラウザで確認

1. `http://localhost/books`にアクセス
2. 「新規登録」ボタンをクリック
3. フォームに入力して「登録」をクリック
4. 一覧画面にリダイレクトされ、成功メッセージが表示されることを確認

### 3-2. バリデーションエラーの確認

1. タイトルを空にして「登録」をクリック
2. エラーメッセージが表示されることを確認

---

## Step 4: コミット、PR、マージ

### 4-1. コミット

```bash
git add .
git commit -m "feat: 書籍登録機能の実装 (Closes #2)"
```

### 4-2. プッシュ

```bash
git push origin feature/issue-2-book-create
```

### 4-3. PR作成とマージ

1. GitHubでPRを作成
2. セルフレビュー（Diff確認）
3. マージ
4. Issue #2が自動クローズされることを確認

### 4-4. ローカルの更新

```bash
git checkout main
git pull origin main
git branch -d feature/issue-2-book-create
```

---

## 🚨 よくある間違い

### 間違い1: バリデーションエラーが表示されない

**対処法**: Bladeテンプレートに`@error`ディレクティブがあるか確認します。

```blade
@error('title')
    <p class="text-red-500 text-sm mt-1">{{ $message }}</p>
@enderror
```

---

### 間違い2: old()で入力値が復元されない

**対処法**: inputタグに`value="{{ old('title') }}"`が設定されているか確認します。

---

## ✨ まとめ

このセクションでは、書籍登録機能の実装について学びました。

| Step | 学んだこと |
|:---|:---|
| Step 0 | イシュー駆動開発の流れ（ブランチ作成） |
| Step 1-2 | create/storeメソッドの実装 |
| Step 3 | バリデーションの動作確認 |
| Step 4 | コミット、PR、マージ |

次のセクションでは、書籍詳細画面を実装します。

---
