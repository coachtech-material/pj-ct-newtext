# Tutorial 9-3-6: トランザクション処理

## 🎯 このセクションで学ぶこと

*   トランザクション処理の概念を理解する。
*   Laravelでトランザクション処理を実装できるようになる。
*   データの整合性を保つ方法を学ぶ。

---

## 導入：「全部成功」か「全部失敗」か

Webアプリケーションでは、複数のデータベース操作を一連の処理として実行することがあります。例えば、以下のような状況を考えてみましょう。

**例: 銀行の送金処理**

1. Aさんの口座から1万円を引き落とす
2. Bさんの口座に1万円を入金する

この2つの処理は、**どちらも成功するか、どちらも失敗するか**でなければなりません。もし、Aさんの口座から引き落としが成功したのに、Bさんの口座への入金が失敗したら、1万円が消えてしまいます。

このような問題を防ぐために、**トランザクション処理**という仕組みを使います。

---

## 詳細解説

### 🔒 トランザクション処理とは？

トランザクション処理とは、**複数のデータベース操作を1つの単位として扱う仕組み**です。トランザクションには、以下の特性があります。

#### ACID特性

| 特性 | 説明 |
|:---|:---|
| **Atomicity（原子性）** | 全ての操作が成功するか、全て失敗するか |
| **Consistency（一貫性）** | データベースの整合性が保たれる |
| **Isolation（独立性）** | 複数のトランザクションが互いに影響しない |
| **Durability（永続性）** | コミットされたデータは永続的に保存される |

---

### 📝 Laravelでのトランザクション処理

Laravelでは、`DB::transaction()`を使って、トランザクション処理を簡単に実装できます。

#### 基本的な使い方

```php
use Illuminate\Support\Facades\DB;

DB::transaction(function () {
    // ここに複数のデータベース操作を書く
    $user = User::create([...]);
    $post = Post::create([...]);
});
```

もし、この中で例外が発生した場合、**全ての操作が自動的にロールバック**されます。

---

### 🚀 実践例1: ユーザー登録とプロフィール作成

ユーザー登録時に、ユーザーテーブルとプロフィールテーブルの両方にデータを挿入する例です。

**コントローラー**

```php
use Illuminate\Support\Facades\DB;
use App\Models\User;
use App\Models\Profile;

public function register(Request $request)
{
    $validated = $request->validate([
        'name' => 'required',
        'email' => 'required|email|unique:users',
        'password' => 'required|min:8',
    ]);

    DB::transaction(function () use ($validated) {
        // ユーザーを作成
        $user = User::create([
            'name' => $validated['name'],
            'email' => $validated['email'],
            'password' => Hash::make($validated['password']),
        ]);

        // プロフィールを作成
        Profile::create([
            'user_id' => $user->id,
            'bio' => '',
            'avatar' => 'default.png',
        ]);
    });

    return redirect('/login')->with('success', 'ユーザー登録が完了しました');
}
```

**コードリーディング**

*   `DB::transaction(function () { ... })`: トランザクションを開始します。
*   もし、`Profile::create()`で例外が発生した場合、`User::create()`もロールバックされます。

---

### 🚀 実践例2: 送金処理

銀行の送金処理のような、複数のレコードを更新する例です。

**コントローラー**

```php
use Illuminate\Support\Facades\DB;
use App\Models\Account;

public function transfer(Request $request)
{
    $validated = $request->validate([
        'from_account_id' => 'required|exists:accounts,id',
        'to_account_id' => 'required|exists:accounts,id',
        'amount' => 'required|numeric|min:1',
    ]);

    DB::transaction(function () use ($validated) {
        $fromAccount = Account::findOrFail($validated['from_account_id']);
        $toAccount = Account::findOrFail($validated['to_account_id']);

        // 残高チェック
        if ($fromAccount->balance < $validated['amount']) {
            throw new \Exception('残高が不足しています');
        }

        // 送金元から引き落とす
        $fromAccount->decrement('balance', $validated['amount']);

        // 送金先に入金する
        $toAccount->increment('balance', $validated['amount']);

        // 送金履歴を記録
        TransferLog::create([
            'from_account_id' => $fromAccount->id,
            'to_account_id' => $toAccount->id,
            'amount' => $validated['amount'],
        ]);
    });

    return redirect('/accounts')->with('success', '送金が完了しました');
}
```

**コードリーディング**

*   `throw new \Exception('...')`: 例外を投げると、トランザクションが自動的にロールバックされます。
*   `decrement()`、`increment()`: レコードの値を増減させます。

---

### 🔍 手動でトランザクションを制御する

より細かい制御が必要な場合は、手動でトランザクションを開始・コミット・ロールバックできます。

```php
use Illuminate\Support\Facades\DB;

DB::beginTransaction();

try {
    // データベース操作
    $user = User::create([...]);
    $post = Post::create([...]);

    // コミット
    DB::commit();
} catch (\Exception $e) {
    // ロールバック
    DB::rollBack();
    
    // エラーハンドリング
    return back()->withErrors(['error' => '処理に失敗しました']);
}
```

**コードリーディング**

*   `DB::beginTransaction()`: トランザクションを開始します。
*   `DB::commit()`: トランザクションをコミットします（変更を確定します）。
*   `DB::rollBack()`: トランザクションをロールバックします（変更を取り消します）。

---

### 💡 TIP: ネストしたトランザクション

Laravelは、ネストしたトランザクションをサポートしています。

```php
DB::transaction(function () {
    // 外側のトランザクション
    $user = User::create([...]);

    DB::transaction(function () use ($user) {
        // 内側のトランザクション
        $post = Post::create(['user_id' => $user->id]);
    });
});
```

ただし、ネストしたトランザクションは、複雑になりやすいため、できるだけ避けるべきです。

---

### 🚨 トランザクション処理のベストプラクティス

#### 1. トランザクションは短く保つ

トランザクションが長いと、データベースのロックが長時間保持され、パフォーマンスが低下します。

**悪い例**

```php
DB::transaction(function () {
    $user = User::create([...]);
    
    // 外部APIを呼び出す（時間がかかる）
    $response = Http::post('https://api.example.com/notify', [...]);
    
    $post = Post::create([...]);
});
```

**良い例**

```php
DB::transaction(function () {
    $user = User::create([...]);
    $post = Post::create([...]);
});

// トランザクション外で外部APIを呼び出す
Http::post('https://api.example.com/notify', [...]);
```

#### 2. 例外を適切にハンドリングする

トランザクション内で例外が発生した場合、適切にハンドリングします。

```php
try {
    DB::transaction(function () {
        // データベース操作
    });
} catch (\Exception $e) {
    // ログに記録
    Log::error('トランザクションエラー: ' . $e->getMessage());
    
    // ユーザーにエラーメッセージを表示
    return back()->withErrors(['error' => '処理に失敗しました']);
}
```

#### 3. デッドロックに注意する

複数のトランザクションが同時に実行されると、**デッドロック**が発生する可能性があります。

**デッドロックとは**

*   トランザクションAがテーブル1をロックし、テーブル2を待つ
*   トランザクションBがテーブル2をロックし、テーブル1を待つ
*   お互いに待ち続けて、処理が進まなくなる

**対策**

*   テーブルへのアクセス順序を統一する
*   トランザクションを短く保つ
*   デッドロックが発生した場合は、リトライする

```php
$maxAttempts = 3;
$attempt = 0;

while ($attempt < $maxAttempts) {
    try {
        DB::transaction(function () {
            // データベース操作
        });
        break; // 成功したらループを抜ける
    } catch (\Illuminate\Database\QueryException $e) {
        if ($e->getCode() == '40001') { // デッドロックエラー
            $attempt++;
            sleep(1); // 1秒待ってリトライ
        } else {
            throw $e; // その他のエラーは再スロー
        }
    }
}
```

---

### 🔍 生のSQLでトランザクション処理を実装する

Laravelでは、生のSQLを使ってトランザクション処理を実装することもできます。

```php
DB::statement('START TRANSACTION');

try {
    DB::statement('UPDATE accounts SET balance = balance - 1000 WHERE id = 1');
    DB::statement('UPDATE accounts SET balance = balance + 1000 WHERE id = 2');
    
    DB::statement('COMMIT');
} catch (\Exception $e) {
    DB::statement('ROLLBACK');
    throw $e;
}
```

**コードリーディング**

*   `START TRANSACTION`: トランザクションを開始します。
*   `COMMIT`: トランザクションをコミットします。
*   `ROLLBACK`: トランザクションをロールバックします。

---

## ✨ まとめ

このセクションでは、トランザクション処理について学びました。

*   トランザクション処理は、複数のデータベース操作を1つの単位として扱う仕組みである。
*   `DB::transaction()`を使うことで、簡単にトランザクション処理を実装できる。
*   トランザクション内で例外が発生すると、自動的にロールバックされる。
*   手動で`DB::beginTransaction()`、`DB::commit()`、`DB::rollBack()`を使うこともできる。
*   トランザクションは短く保ち、デッドロックに注意する必要がある。

これで、Chapter 3「データベースとマイグレーション」の全6セクションが完了しました。次は、Chapter 4「Eloquent ORMの基礎」の残りのセクションに進みます。

---

## 📝 学習のポイント

- [ ] トランザクション処理が、複数のデータベース操作を1つの単位として扱う仕組みであることを理解した。
- [ ] `DB::transaction()`を使って、トランザクション処理を実装できる。
- [ ] トランザクション内で例外が発生すると、自動的にロールバックされる。
- [ ] 手動で`DB::beginTransaction()`、`DB::commit()`、`DB::rollBack()`を使える。
- [ ] トランザクションは短く保ち、デッドロックに注意する必要がある。
