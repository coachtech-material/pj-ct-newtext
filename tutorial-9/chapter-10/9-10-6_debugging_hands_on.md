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
