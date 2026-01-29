# Tutorial 13-5-4: コードの可読性

## 🎯 このセクションで学ぶこと

- 読みやすいコードを書くためのテクニックを学ぶ
- 早期リターンでネストを減らす
- コメントの適切な使い方を理解する

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜコレクションの次に可読性なのか？」

コレクションメソッドを学んだら、最後に**コードの可読性**を高めます。

### 理由1: リファクタリングの仕上げ

```
DRY原則 → 重複を排除
命名規則 → 意図を明確に
コレクション → 簡潔に
可読性 → 読みやすくする  ← 仕上げ
```

### 理由2: 「読みやすさ」は主観的

可読性は主観的な概念ですが、**定石のテクニック**があります。

---

## Step 1: 早期リターン（Early Return）

### 1-1. ネストが深いコード（悪い例）

```php
public function update(Request $request, Book $book)
{
    if (auth()->check()) {
        if ($book->user_id === auth()->id()) {
            $validated = $request->validate([...]);
            $book->update($validated);
            return redirect()->route('books.show', $book);
        } else {
            abort(403);
        }
    } else {
        return redirect()->route('login');
    }
}
```

### 1-2. 早期リターンで改善（良い例）

```php
public function update(Request $request, Book $book)
{
    if (!auth()->check()) {
        return redirect()->route('login');
    }

    if ($book->user_id !== auth()->id()) {
        abort(403);
    }

    $validated = $request->validate([...]);
    $book->update($validated);
    
    return redirect()->route('books.show', $book);
}
```

### コードリーディング

#### 早期リターンのパターン

| 部分 | 説明 |
|:---|:---|
| `if (!auth()->check())` | 未ログインなら即座にリダイレクト |
| `if ($book->user_id !== auth()->id())` | 所有者でなければ403エラー |
| 残りのコード | メインロジック（ネストなし） |

> 💡 **ポイント**: 「異常系を先に処理して、正常系を後に書く」のが早期リターンのコツです。

### 1-3. さらにPolicyで改善

```php
public function update(StoreBookRequest $request, Book $book)
{
    $this->authorize('update', $book);
    
    $book->update($request->validated());
    
    return redirect()->route('books.show', $book)->with('success', '書籍を更新しました。');
}
```

---

## Step 2: 三項演算子の適切な使用

### 2-1. シンプルな条件分岐

```php
// ✅ 適切な使用
$status = $book->rating >= 4 ? 'おすすめ' : '普通';

// ✅ Bladeでの使用
<span class="{{ $book->rating >= 4 ? 'text-green-500' : 'text-gray-500' }}">
```

### 2-2. 複雑な条件は避ける

```php
// ❌ 複雑すぎる
$message = $book->rating >= 5 ? '最高！' : ($book->rating >= 4 ? '良い' : ($book->rating >= 3 ? '普通' : '改善の余地あり'));

// ✅ matchを使う
$message = match(true) {
    $book->rating >= 5 => '最高！',
    $book->rating >= 4 => '良い',
    $book->rating >= 3 => '普通',
    default => '改善の余地あり',
};
```

---

## Step 3: コメントの書き方

### 3-1. 悪いコメント

```php
// ❌ コードを説明しているだけ
// 書籍を取得
$book = Book::find($id);

// ❌ 古い情報
// タスクを削除（2023年に追加）
$book->delete();
```

### 3-2. 良いコメント

```php
// ✅ なぜそうするのかを説明
// 論理削除ではなく物理削除を使用（GDPR対応のため）
$book->forceDelete();

// ✅ 複雑なロジックの意図を説明
// 評価が4以上かつレビューが100文字以上の書籍を「おすすめ」として表示
$recommendedBooks = $books->filter(fn($book) => 
    $book->rating >= 4 && strlen($book->review) >= 100
);
```

### 3-3. PHPDocコメント

```php
/**
 * 書籍を登録する
 *
 * @param StoreBookRequest $request バリデーション済みのリクエスト
 * @return \Illuminate\Http\RedirectResponse
 */
public function store(StoreBookRequest $request)
{
    auth()->user()->books()->create($request->validated());
    
    return redirect()->route('books.index')->with('success', '書籍を登録しました。');
}
```

---

## Step 4: 一貫性を保つ

### 4-1. 命名の一貫性

```php
// ❌ 一貫性がない
$book = Book::find($id);
$bookData = Book::find($id);
$bookInfo = Book::find($id);

// ✅ 一貫性がある
$book = Book::find($id);
```

### 4-2. フォーマットの一貫性

```php
// ❌ 一貫性がない
if($condition){
    // ...
}

if ($condition)
{
    // ...
}

// ✅ 一貫性がある（PSR-12準拠）
if ($condition) {
    // ...
}
```

---

## ✨ まとめ

このセクションでは、コードの可読性について学びました。

| テクニック | 効果 |
|:---|:---|
| 早期リターン | ネストを減らし、メインロジックを明確に |
| 三項演算子 | シンプルな条件分岐を1行で |
| 適切なコメント | 「なぜ」を説明 |
| 一貫性 | 読み手の負担を軽減 |

読みやすいコードは、将来の自分や他の開発者への贈り物です。

---
