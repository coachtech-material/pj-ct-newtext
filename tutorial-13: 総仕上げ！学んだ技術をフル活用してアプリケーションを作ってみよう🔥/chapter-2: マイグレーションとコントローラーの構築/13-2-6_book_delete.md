# Tutorial 13-2-6: 書籍削除機能の実装

## 🎯 このセクションで学ぶこと

- 書籍削除機能のdestroyメソッドを実装する
- DELETEメソッドの送信方法を理解する
- イシュー駆動開発のフローを継続する

---

## Step 0: 開発の準備（チケット駆動）

### 0-1. GitHubでIssueを確認

GitHubで `#5 書籍削除機能` のIssueを確認します。

### 0-2. ブランチを作成

```bash
git checkout main
git pull origin main
git switch -c feature/issue-5-book-delete
```

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ編集の次に削除機能なのか？」

編集機能ができたら、最後に**削除機能**を作ります。

### 理由1: CRUDの「D」（削除）で完成

```
C: Create（作成） → ✅ 完了
R: Read（読み取り） → ✅ 完了
U: Update（更新） → ✅ 完了
D: Delete（削除） → このセクション
```

### 理由2: 削除は慣重に

削除は「取り消しができない」操作です。そのため、確認ダイアログを表示して誤操作を防ぎます。

---

### このセクションの実装順序

| 順番 | 作業 | 理由 |
|:---:|:---|:---|
| 1 | destroyメソッド実装 | 削除処理を行うため |
| 2 | 動作確認 | 削除が正しく動くかテスト |

---

### コードの実装順序（destroyメソッド）

```php
public function destroy(Book $book)
{
    // ① データを削除
    $book->delete();
    
    // ② 一覧にリダイレクト
    return redirect()->route('books.index')->with('success', '...');
}
```

| 順番 | コード | 考え方 |
|:---:|:---|:---|
| ① | `$book->delete()` | 「データを削除」 |
| ② | `return redirect()...` | 「結果を見せる」 |

---

## Step 1: destroyメソッドの実装

### 1-1. BookControllerを編集

**ファイル**: `app/Http/Controllers/BookController.php`

```php
/**
 * 書籍を削除
 */
public function destroy(Book $book)
{
    $book->delete();

    return redirect()
        ->route('books.index')
        ->with('success', '書籍を削除しました。');
}
```

---

### 1-2. コードリーディング

#### `$book->delete()`の分解

| 部分 | 説明 |
|:---|:---|
| `$book` | ルートモデルバインディングで取得したBookインスタンス |
| `->` | インスタンスメソッド呼び出し |
| `delete()` | データベースからレコードを削除 |

> 💡 **delete()の戻り値**: `delete()`は削除が成功したら`true`を返しますが、通常は戻り値を使いません。

---

## Step 2: DELETEメソッドの送信

HTMLフォームは、GETとPOSTしかサポートしていません。DELETEメソッドを送信するには、`@method('DELETE')`を使います。

```blade
<form action="{{ route('books.destroy', $book) }}" method="POST">
    @csrf
    @method('DELETE')
    <button type="submit">削除</button>
</form>
```

**動作**:

1. フォームはPOSTで送信される
2. `@method('DELETE')`が`<input type="hidden" name="_method" value="DELETE">`を生成
3. Laravelがこの隠しフィールドを見て、DELETEリクエストとして処理

---

## Step 3: 動作確認

### 3-1. ブラウザで確認

1. `http://localhost/books`にアクセス
2. 書籍のタイトルをクリックして詳細画面へ
3. 「削除」ボタンをクリック
4. 確認ダイアログで「OK」をクリック
5. 一覧画面にリダイレクトされ、書籍が削除されていることを確認

---

## Step 4: コミット、PR、マージ

### 4-1. コミット

```bash
git add .
git commit -m "feat: 書籍削除機能の実装 (Closes #5)"
```

### 4-2. プッシュ、PR、マージ

```bash
git push origin feature/issue-5-book-delete
```

GitHubでPRを作成し、セルフレビュー後にマージします。

### 4-3. ローカルの更新

```bash
git checkout main
git pull origin main
git branch -d feature/issue-5-book-delete
```

---

## Step 5: CRUD機能の完成

これで、書籍のCRUD機能が完成しました。

| 機能 | メソッド | URL | HTTPメソッド |
|:---|:---|:---|:---|
| 一覧 | index | /books | GET |
| 登録画面 | create | /books/create | GET |
| 登録処理 | store | /books | POST |
| 詳細 | show | /books/{id} | GET |
| 編集画面 | edit | /books/{id}/edit | GET |
| 更新処理 | update | /books/{id} | PUT |
| 削除処理 | destroy | /books/{id} | DELETE |

---

## ✨ まとめ

このセクションでは、書籍削除機能の実装について学びました。

| Step | 学んだこと |
|:---|:---|
| Step 0 | イシュー駆動開発の流れ |
| Step 1 | destroyメソッドの実装 |
| Step 2 | @method('DELETE')の使い方 |
| Step 3-4 | 動作確認、コミット、PR、マージ |

次のChapterでは、公開APIの実装に進みます。

---
