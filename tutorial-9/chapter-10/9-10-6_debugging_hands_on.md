# Tutorial 9-10-6: デバッグ - ハンズオン演習

## 📝 このセクションの目的

Chapter 10で学んだデバッグ手法を実際に手を動かして確認します。エラーを特定し、修正する方法をマスターしましょう。

---

## 🎯 演習課題：エラーを修正しよう

### 📋 要件

以下のコードにあるエラーを見つけて修正してください。

```php
public function store(Request $request)
{
    $user = new User;
    $user->name = $request->name;
    $user->email = $request->email;
    $user->save();
    
    return redirect('/users');
}
```

**エラー内容**：
- Mass assignment エラーが発生する

---

## 💡 ヒント

```php
// dd()でデバッグ
dd($request->all());

// ログ出力
\Log::info('User created', ['user_id' => $user->id]);

// $fillableの設定
protected $fillable = ['name', 'email'];
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？デバッグは開発において不可欠なスキルです。一緒に手を動かしながら、エラーを特定して修正していきましょう。

### 💭 実装の思考プロセス

デバッグを進める際、以下の順番で考えると効率的です：

1. **エラーメッセージを読む**：何が問題かを理解する
2. **dd()でデータを確認**：変数の中身を調べる
3. **ログを出力**：処理の流れを追跡する
4. **原因を特定**：エラーの根本原因を見つける
5. **修正してテスト**：修正後に動作を確認する

デバッグのポイントは「仮説を立てて検証し、一歩ずつ原因を絞り込む」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: エラーメッセージを読む

**何を考えているか**：
- 「エラーメッセージには重要な情報が含まれている」
- 「Mass assignmentエラーということは$fillableが設定されていない」
- 「まずはエラーの種類を理解しよう」

エラーメッセージの例：

```
Illuminate\Database\Eloquent\MassAssignmentException
Add [name] to fillable property to allow mass assignment on [App\Models\User].
```

**エラー分析**：

→ このエラーは「Mass Assignment」が原因です。Laravelはセキュリティ対策として、モデルの`$fillable`または`$guarded`で一括代入可能な属性を指定する必要があります。

---

#### ステップ2: dd()でデータを確認する

**何を考えているか**：
- 「リクエストデータが正しく送られているか確認しよう」
- 「dd()で処理を停止して変数を調べよう」
- 「期待する値が含まれているかチェックしよう」

コントローラーに`dd()`を追加します：

```php
public function store(Request $request)
{
    dd($request->all());
    
    $user = new User;
    $user->name = $request->name;
    $user->email = $request->email;
    $user->save();
    
    return redirect('/users');
}
```

**コード解説**：

```php
dd($request->all());
```
→ `dd()`（Dump and Die）でリクエストデータを表示し、処理を停止します。データの中身を確認できます。

---

#### ステップ3: ログを出力する

**何を考えているか**：
- 「処理の流れを追跡したい」
- 「本番環境でも使えるデバッグ手法が必要だ」
- 「ログファイルで後から確認できる」

コントローラーにログ出力を追加します：

```php
public function store(Request $request)
{
    \Log::info('User registration attempt', $request->all());
    
    $user = new User;
    $user->name = $request->name;
    $user->email = $request->email;
    $user->save();
    
    \Log::info('User created successfully', ['user_id' => $user->id]);
    
    return redirect('/users');
}
```

**コード解説**：

```php
\Log::info('User registration attempt', $request->all());
```
→ `\Log::info()`で情報レベルのログを出力します。第1引数はメッセージ、第2引数はコンテキストデータです。

```php
\Log::info('User created successfully', ['user_id' => $user->id]);
```
→ ユーザー作成後にログを出力します。処理が成功したことを記録します。

ログは`storage/logs/laravel.log`に出力されます。

---

#### ステップ4: 原因を特定して修正する

**何を考えているか**：
- 「Mass assignmentエラーの原因は$fillableが未設定」
- 「モデルに$fillableを追加しよう」
- 「セキュアにコードを書き換えよう」

`app/Models/User.php`を開いて、`$fillable`を追加します：

```php
protected $fillable = ['name', 'email', 'password'];
```

コントローラーを修正します：

```php
public function store(Request $request)
{
    \Log::info('User registration attempt', $request->all());
    
    $user = User::create([
        'name' => $request->name,
        'email' => $request->email,
        'password' => bcrypt($request->password),
    ]);
    
    \Log::info('User created successfully', ['user_id' => $user->id]);
    
    return redirect('/users');
}
```

**コード解説**：

```php
protected $fillable = ['name', 'email', 'password'];
```
→ `$fillable`で一括代入可能な属性を指定します。これによりMass assignmentエラーが解決します。

```php
$user = User::create([
    'name' => $request->name,
    'email' => $request->email,
    'password' => bcrypt($request->password),
]);
```
→ `User::create()`でユーザーを作成します。`bcrypt()`でパスワードをハッシュ化します。

---

#### ステップ5: 修正後にテストする

**何を考えているか**：
- 「修正が正しく動作するか確認しよう」
- 「ユーザー登録が成功するかテストしよう」
- 「ログを確認して処理の流れを追跡しよう」

テスト手順：

1. **フォームからユーザー登録を実行**：エラーが発生しないことを確認
2. **データベースを確認**：ユーザーが正しく保存されていることを確認
3. **ログファイルを確認**：`storage/logs/laravel.log`でログが出力されていることを確認

---

### ✨ 完成！

これでデバッグ手法を実践できました！エラーメッセージを読み、dd()とログで原因を特定し、修正できましたね。

---

## 📖 模範解答

### 修正後のコード

```php
// User.php
protected $fillable = ['name', 'email', 'password'];

// UserController.php
public function store(Request $request)
{
    // デバッグ用
    \Log::info('User registration attempt', $request->all());
    
    $user = User::create([
        'name' => $request->name,
        'email' => $request->email,
        'password' => bcrypt($request->password),
    ]);
    
    \Log::info('User created successfully', ['user_id' => $user->id]);
    
    return redirect('/users');
}
```

### デバッグ手順

1. `dd($request->all())`でリクエストデータを確認
2. `\Log::info()`でログ出力
3. `storage/logs/laravel.log`でログを確認
4. `$fillable`を設定してMass assignment対策

---

## 💪 自己評価チェックリスト

- [ ] dd()でデバッグできた
- [ ] ログ出力ができた
- [ ] エラーメッセージを読めた
- [ ] $fillableの重要性を理解できた

すべてチェックできたら、Chapter 11に進みましょう！
