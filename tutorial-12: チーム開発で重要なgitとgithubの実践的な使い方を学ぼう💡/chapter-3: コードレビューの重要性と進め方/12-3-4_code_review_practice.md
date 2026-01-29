# Tutorial 12-3-4: 実践: コードレビュー演習

## 🎯 このセクションで学ぶこと

*   実践的なコードレビュー演習を通じて、レビューのスキルを身につける。
*   様々なコードの問題点を発見し、改善提案を行う。
*   レビューのフィードバックを実際に書いてみる。

---

## 導入：実践演習の目的

このセクションでは、**実践的なコードレビュー演習**を行います。

様々なコードを見て、問題点を発見し、改善提案を行います。

---

## 詳細解説

### 🚀 演習1: セキュリティの問題

#### コード

```php
public function login(Request $request)
{
    $user = User::where('email', $request->email)->first();
    
    if ($user->password === $request->password) {
        Auth::login($user);
        return redirect('/dashboard');
    }
    
    return back()->withErrors(['email' => 'ログインに失敗しました']);
}
```

---

#### 問題点を見つけてみましょう

<details>
<summary>答えを見る</summary>

**問題点**:

1. パスワードをハッシュ化せずに比較している
2. ユーザーが存在しない場合の処理が不足している

**改善提案**:

```
パスワードをハッシュ化せずに比較しているので、セキュリティ上の問題があります。
`Hash::check()`を使ってください。

また、ユーザーが存在しない場合の処理が不足しています。
`$user`が`null`の場合、`$user->password`でエラーが発生します。
```

**修正例**:

```php
public function login(Request $request)
{
    $user = User::where('email', $request->email)->first();
    
    if ($user && Hash::check($request->password, $user->password)) {
        Auth::login($user);
        return redirect('/dashboard');
    }
    
    return back()->withErrors(['email' => 'ログインに失敗しました']);
}
```

</details>

---

### 🚀 演習2: 可読性の問題

#### コード

```php
public function getUsers()
{
    $users = DB::select('SELECT * FROM users WHERE deleted_at IS NULL');
    $result = [];
    foreach ($users as $user) {
        $result[] = [
            'id' => $user->id,
            'name' => $user->name,
            'email' => $user->email,
        ];
    }
    return $result;
}
```

---

#### 問題点を見つけてみましょう

<details>
<summary>答えを見る</summary>

**問題点**:

1. 生のSQLを使っている
2. 不要なループ処理がある

**改善提案**:

```
Eloquentを使った方が可読性が高く、保守性も向上します。
また、不要なループ処理を削除できます。
```

**修正例**:

```php
public function getUsers()
{
    return User::select('id', 'name', 'email')->get();
}
```

</details>

---

### 🚀 演習3: パフォーマンスの問題

#### コード

```php
public function getUsersWithPosts()
{
    $users = User::all();
    
    foreach ($users as $user) {
        $user->posts = Post::where('user_id', $user->id)->get();
    }
    
    return $users;
}
```

---

#### 問題点を見つけてみましょう

<details>
<summary>答えを見る</summary>

**問題点**:

1. N+1問題が発生している

**改善提案**:

```
N+1問題が発生しています。
Eager Loadingを使って、パフォーマンスを改善してください。
```

**修正例**:

```php
public function getUsersWithPosts()
{
    return User::with('posts')->get();
}
```

</details>

---

### 🚀 演習4: バリデーションの問題

#### コード

```php
public function store(Request $request)
{
    $user = new User();
    $user->name = $request->name;
    $user->email = $request->email;
    $user->password = Hash::make($request->password);
    $user->save();
    
    return redirect('/users');
}
```

---

#### 問題点を見つけてみましょう

<details>
<summary>答えを見る</summary>

**問題点**:

1. バリデーションが不足している

**改善提案**:

```
バリデーションが不足しています。
以下のバリデーションを追加してください：

- name: 必須、文字列、最大255文字
- email: 必須、メールアドレス形式、ユニーク
- password: 必須、文字列、最小8文字
```

**修正例**:

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'name' => 'required|string|max:255',
        'email' => 'required|email|unique:users',
        'password' => 'required|string|min:8',
    ]);
    
    $user = new User();
    $user->name = $validated['name'];
    $user->email = $validated['email'];
    $user->password = Hash::make($validated['password']);
    $user->save();
    
    return redirect('/users');
}
```

</details>

---

### 🚀 演習5: テストの問題

#### コード

```php
public function testLogin()
{
    $response = $this->post('/login', [
        'email' => 'test@example.com',
        'password' => 'password',
    ]);
    
    $response->assertStatus(302);
}
```

---

#### 問題点を見つけてみましょう

<details>
<summary>答えを見る</summary>

**問題点**:

1. テストデータが不足している
2. アサーションが不足している

**改善提案**:

```
テストデータが不足しています。
ユーザーを作成してからテストを実行してください。

また、アサーションが不足しています。
以下のアサーションを追加してください：

- リダイレクト先が正しいか
- ユーザーが認証されているか
```

**修正例**:

```php
public function testLogin()
{
    $user = User::factory()->create([
        'email' => 'test@example.com',
        'password' => Hash::make('password'),
    ]);
    
    $response = $this->post('/login', [
        'email' => 'test@example.com',
        'password' => 'password',
    ]);
    
    $response->assertRedirect('/dashboard');
    $this->assertAuthenticatedAs($user);
}
```

</details>

---

### 🚀 演習6: 関数の長さの問題

#### コード

```php
public function processOrder(Request $request)
{
    // バリデーション
    $validated = $request->validate([
        'product_id' => 'required|exists:products,id',
        'quantity' => 'required|integer|min:1',
    ]);
    
    // 商品を取得
    $product = Product::find($validated['product_id']);
    
    // 在庫チェック
    if ($product->stock < $validated['quantity']) {
        return back()->withErrors(['quantity' => '在庫が不足しています']);
    }
    
    // 注文を作成
    $order = new Order();
    $order->user_id = auth()->id();
    $order->product_id = $product->id;
    $order->quantity = $validated['quantity'];
    $order->total_price = $product->price * $validated['quantity'];
    $order->save();
    
    // 在庫を減らす
    $product->stock -= $validated['quantity'];
    $product->save();
    
    // メール送信
    Mail::to(auth()->user())->send(new OrderConfirmation($order));
    
    return redirect('/orders')->with('success', '注文が完了しました');
}
```

---

#### 問題点を見つけてみましょう

<details>
<summary>答えを見る</summary>

**問題点**:

1. 関数が長すぎる
2. 単一責任の原則に違反している

**改善提案**:

```
この関数は長すぎるので、分割することをお勧めします。

以下のように分割できます：

- `validateOrder()`: バリデーション
- `checkStock()`: 在庫チェック
- `createOrder()`: 注文作成
- `updateStock()`: 在庫更新
- `sendOrderConfirmation()`: メール送信
```

**修正例**:

```php
public function processOrder(Request $request)
{
    $validated = $this->validateOrder($request);
    $product = Product::find($validated['product_id']);
    
    if (!$this->checkStock($product, $validated['quantity'])) {
        return back()->withErrors(['quantity' => '在庫が不足しています']);
    }
    
    $order = $this->createOrder($product, $validated['quantity']);
    $this->updateStock($product, $validated['quantity']);
    $this->sendOrderConfirmation($order);
    
    return redirect('/orders')->with('success', '注文が完了しました');
}

private function validateOrder(Request $request)
{
    return $request->validate([
        'product_id' => 'required|exists:products,id',
        'quantity' => 'required|integer|min:1',
    ]);
}

private function checkStock(Product $product, int $quantity): bool
{
    return $product->stock >= $quantity;
}

private function createOrder(Product $product, int $quantity): Order
{
    $order = new Order();
    $order->user_id = auth()->id();
    $order->product_id = $product->id;
    $order->quantity = $quantity;
    $order->total_price = $product->price * $quantity;
    $order->save();
    
    return $order;
}

private function updateStock(Product $product, int $quantity): void
{
    $product->stock -= $quantity;
    $product->save();
}

private function sendOrderConfirmation(Order $order): void
{
    Mail::to(auth()->user())->send(new OrderConfirmation($order));
}
```

</details>

---

### 💡 TIP: レビューのチェックリスト

以下のチェックリストを使って、レビューを行いましょう。

- [ ] **セキュリティ**: セキュリティ上の問題がないか
- [ ] **可読性**: コードが読みやすいか
- [ ] **パフォーマンス**: パフォーマンスに問題がないか
- [ ] **バリデーション**: バリデーションが適切か
- [ ] **テスト**: テストが書かれているか
- [ ] **関数の長さ**: 関数が長すぎないか
- [ ] **単一責任の原則**: 1つの関数が1つの責任を持っているか
- [ ] **命名**: 変数名や関数名が適切か
- [ ] **コメント**: 必要なコメントが書かれているか
- [ ] **エラーハンドリング**: エラーハンドリングが適切か

---

### 🚀 演習7: 実際のプルリクエストをレビューしてみよう

#### ステップ1: GitHubでプルリクエストを開く

---

#### ステップ2: 「Files changed」タブをクリック

---

#### ステップ3: コードを確認

---

#### ステップ4: 問題点を見つけたら、コメントを追加

---

#### ステップ5: レビューを送信

---

## ✨ まとめ

このセクションでは、実践的なコードレビュー演習を行いました。

*   セキュリティ、可読性、パフォーマンス、バリデーション、テスト、関数の長さなど、様々な観点からコードをレビューした。
*   チェックリストを使って、レビューの漏れを防ぐ方法を学んだ。
*   実際のプルリクエストをレビューする流れを体験した。

これで、Tutorial 10「チーム開発の作法」は完了です。次のTutorialでは、より高度なトピックについて学びます。

---
