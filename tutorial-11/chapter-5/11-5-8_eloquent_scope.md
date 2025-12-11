# Tutorial 11-5-8: Eloquentスコープの活用

## 🎯 このセクションで学ぶこと

*   Eloquentスコープとは何かを理解する。
*   ローカルスコープを使って、クエリを再利用可能にする方法を学ぶ。
*   グローバルスコープを使って、常に適用されるクエリを定義する方法を学ぶ。
*   スコープのメリットとデメリットを理解する。

---

## 導入：なぜEloquentスコープを使うのか

**同じクエリ**を何度も書くと、**コードが重複**します。

**Eloquentスコープ**を使うと、**クエリを再利用可能**にでき、**コードを簡潔に**書けます。

---

## 詳細解説

### 🔍 クエリが重複する例

以下のコードは、同じクエリが重複しています。

```php
// コントローラー1
$tasks = Task::where('user_id', auth()->id())
    ->where('status', 'pending')
    ->orderBy('created_at', 'desc')
    ->get();

// コントローラー2
$tasks = Task::where('user_id', auth()->id())
    ->where('status', 'completed')
    ->orderBy('created_at', 'desc')
    ->get();
```

**問題点**:
*   `where('user_id', auth()->id())`が重複している
*   `orderBy('created_at', 'desc')`が重複している

---

### 🔍 ローカルスコープを作成する

ローカルスコープを作成して、クエリを再利用可能にします。

**ファイル**: `app/Models/Task.php`

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class Task extends Model
{
    public function scopeForUser($query, $userId)
    {
        return $query->where('user_id', $userId);
    }

    public function scopeWithStatus($query, $status)
    {
        return $query->where('status', $status);
    }

    public function scopeLatestFirst($query)
    {
        return $query->orderBy('created_at', 'desc');
    }
}
```

**ポイント**:
*   メソッド名は`scope`で始める
*   第1引数は`$query`
*   第2引数以降は、スコープに渡すパラメータ

---

### 🔍 ローカルスコープを使う

コントローラーで、ローカルスコープを使います。

```php
// コントローラー1
$tasks = Task::forUser(auth()->id())
    ->withStatus('pending')
    ->latestFirst()
    ->get();

// コントローラー2
$tasks = Task::forUser(auth()->id())
    ->withStatus('completed')
    ->latestFirst()
    ->get();
```

**改善点**:
*   クエリが簡潔になった
*   再利用可能になった

---

### 🔍 スコープをチェーンする

スコープは、メソッドチェーンで繋げられます。

```php
$tasks = Task::forUser(auth()->id())
    ->withStatus('pending')
    ->latestFirst()
    ->get();
```

---

### 🔍 スコープに複数のパラメータを渡す

スコープに複数のパラメータを渡すこともできます。

```php
public function scopeWithPriority($query, $min, $max)
{
    return $query->whereBetween('priority', [$min, $max]);
}
```

```php
$tasks = Task::withPriority(1, 3)->get();
```

---

### 🔍 スコープの中でスコープを使う

スコープの中で、別のスコープを使うこともできます。

```php
public function scopeMyPendingTasks($query)
{
    return $query->forUser(auth()->id())
        ->withStatus('pending')
        ->latestFirst();
}
```

```php
$tasks = Task::myPendingTasks()->get();
```

---

### 🔍 グローバルスコープとは

**グローバルスコープ**は、**常に適用されるクエリ**を定義します。

例えば、**論理削除されたデータを除外する**場合に使います。

---

### 🔍 グローバルスコープを作成する

グローバルスコープを作成します。

```bash
mkdir -p app/Models/Scopes
touch app/Models/Scopes/ActiveScope.php
```

**ファイル**: `app/Models/Scopes/ActiveScope.php`

```php
<?php

namespace App\Models\Scopes;

use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Scope;

class ActiveScope implements Scope
{
    public function apply(Builder $builder, Model $model)
    {
        $builder->where('is_active', true);
    }
}
```

---

### 🔍 グローバルスコープを適用する

モデルに、グローバルスコープを適用します。

**ファイル**: `app/Models/Task.php`

```php
<?php

namespace App\Models;

use App\Models\Scopes\ActiveScope;
use Illuminate\Database\Eloquent\Model;

class Task extends Model
{
    protected static function booted()
    {
        static::addGlobalScope(new ActiveScope());
    }
}
```

**ポイント**:
*   `booted()`メソッドで、グローバルスコープを追加する
*   すべてのクエリに、自動的に`where('is_active', true)`が追加される

---

### 🔍 グローバルスコープを無効にする

グローバルスコープを無効にするには、`withoutGlobalScope()`を使います。

```php
$tasks = Task::withoutGlobalScope(ActiveScope::class)->get();
```

---

### 🔍 実践演習: スコープを作成してください

以下のクエリを、スコープを使ってリファクタリングしてください。

```php
$tasks = Task::where('user_id', auth()->id())
    ->where('status', 'completed')
    ->where('priority', '>=', 3)
    ->orderBy('created_at', 'desc')
    ->get();
```

---

**解答例**:

**ファイル**: `app/Models/Task.php`

```php
public function scopeForUser($query, $userId)
{
    return $query->where('user_id', $userId);
}

public function scopeWithStatus($query, $status)
{
    return $query->where('status', $status);
}

public function scopeHighPriority($query)
{
    return $query->where('priority', '>=', 3);
}

public function scopeLatestFirst($query)
{
    return $query->orderBy('created_at', 'desc');
}
```

**コントローラー**:

```php
$tasks = Task::forUser(auth()->id())
    ->withStatus('completed')
    ->highPriority()
    ->latestFirst()
    ->get();
```

---

### 🔍 スコープのメリット

*   **再利用可能**: 同じクエリを何度も書かなくてよい
*   **可読性が高い**: クエリの意図が分かりやすい
*   **テストしやすい**: スコープ単体でテストできる

---

### 🔍 スコープのデメリット

*   **学習コストがある**: スコープの書き方を覚える必要がある
*   **過度に使うと複雑になる**: スコープが多すぎると、逆に分かりにくくなる

---

### 💡 TIP: 動的スコープ

スコープは、動的に条件を変えることもできます。

```php
public function scopeFilter($query, $filters)
{
    if (isset($filters['status'])) {
        $query->where('status', $filters['status']);
    }
    
    if (isset($filters['priority'])) {
        $query->where('priority', $filters['priority']);
    }
    
    return $query;
}
```

```php
$tasks = Task::filter($request->all())->get();
```

---

### 🚨 よくある間違い

#### 間違い1: scopeを付け忘れる

スコープのメソッド名は、`scope`で始める必要があります。

```php
// ❌ 間違い
public function forUser($query, $userId)
{
    return $query->where('user_id', $userId);
}

// ✅ 正しい
public function scopeForUser($query, $userId)
{
    return $query->where('user_id', $userId);
}
```

---

#### 間違い2: $queryを返し忘れる

スコープは、`$query`を返す必要があります。

```php
// ❌ 間違い
public function scopeForUser($query, $userId)
{
    $query->where('user_id', $userId);
}

// ✅ 正しい
public function scopeForUser($query, $userId)
{
    return $query->where('user_id', $userId);
}
```

---

#### 間違い3: スコープを使いすぎる

スコープは便利ですが、使いすぎると複雑になります。

**対処法**: 本当に再利用するクエリだけをスコープにします。

---

## ✨ まとめ

このセクションでは、Eloquentスコープの活用を学びました。

*   ローカルスコープを使って、クエリを再利用可能にした。
*   グローバルスコープを使って、常に適用されるクエリを定義した。
*   スコープのメリットとデメリットを理解した。

次のセクションでは、コードの可読性を高める方法について学びます。

---

## 📝 学習のポイント

- [ ] ローカルスコープを作成した。
- [ ] グローバルスコープを作成した。
- [ ] スコープをチェーンした。
- [ ] スコープのメリットとデメリットを理解した。
