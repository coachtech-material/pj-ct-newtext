# Tutorial 9-6-2: バリデーションルール

## 🎯 このセクションで学ぶこと

*   よく使うバリデーションルールを理解し、使えるようになる。
*   複数のルールを組み合わせて、複雑なバリデーションを実装できるようになる。
*   条件付きバリデーションを実装できるようになる。

---

## 導入：「ルール」の種類は無限大

前のセクションで、バリデーションの基礎を学びました。しかし、Laravelには、**非常に多くのバリデーションルール**が用意されています。

このセクションでは、よく使うバリデーションルールを学び、実践的なバリデーションを実装できるようになります。

---

## 詳細解説

### 📝 基本的なバリデーションルール

**`required`: 必須**

```php
$request->validate([
    'name' => 'required',
]);
```

空文字列、null、空配列は、バリデーションエラーになります。

---

**`nullable`: null を許可**

```php
$request->validate([
    'bio' => 'nullable|string',
]);
```

`bio`が送信されない場合、またはnullの場合、バリデーションエラーにはなりません。

---

**`string`: 文字列**

```php
$request->validate([
    'name' => 'required|string',
]);
```

---

**`integer`: 整数**

```php
$request->validate([
    'age' => 'required|integer',
]);
```

---

**`numeric`: 数値**

```php
$request->validate([
    'price' => 'required|numeric',
]);
```

`integer`と異なり、小数も許可されます。

---

**`boolean`: 真偽値**

```php
$request->validate([
    'is_admin' => 'required|boolean',
]);
```

`true`、`false`、`1`、`0`、`"1"`、`"0"`が許可されます。

---

**`array`: 配列**

```php
$request->validate([
    'tags' => 'required|array',
]);
```

---

### 📏 サイズに関するルール

**`min`: 最小値**

```php
$request->validate([
    'name' => 'required|string|min:3',
    'age' => 'required|integer|min:18',
]);
```

*   文字列の場合: 最小文字数
*   数値の場合: 最小値

---

**`max`: 最大値**

```php
$request->validate([
    'name' => 'required|string|max:255',
    'age' => 'required|integer|max:120',
]);
```

---

**`between`: 範囲**

```php
$request->validate([
    'age' => 'required|integer|between:18,65',
]);
```

---

**`size`: サイズ**

```php
$request->validate([
    'name' => 'required|string|size:10',
]);
```

*   文字列の場合: 文字数が10
*   数値の場合: 値が10
*   ファイルの場合: サイズが10KB

---

### 📧 フォーマットに関するルール

**`email`: メールアドレス**

```php
$request->validate([
    'email' => 'required|email',
]);
```

---

**`url`: URL**

```php
$request->validate([
    'website' => 'required|url',
]);
```

---

**`ip`: IPアドレス**

```php
$request->validate([
    'ip_address' => 'required|ip',
]);
```

---

**`date`: 日付**

```php
$request->validate([
    'birth_date' => 'required|date',
]);
```

---

**`date_format`: 日付フォーマット**

```php
$request->validate([
    'birth_date' => 'required|date_format:Y-m-d',
]);
```

---

**`regex`: 正規表現**

```php
$request->validate([
    'phone' => 'required|regex:/^[0-9]{10,11}$/',
]);
```

---

### 🔍 データベースに関するルール

**`unique`: 一意性**

```php
$request->validate([
    'email' => 'required|email|unique:users',
]);
```

`users`テーブルの`email`カラムに、同じ値が存在しないことを確認します。

**更新時に自分自身を除外**

```php
$request->validate([
    'email' => 'required|email|unique:users,email,' . $user->id,
]);
```

---

**`exists`: 存在確認**

```php
$request->validate([
    'user_id' => 'required|exists:users,id',
]);
```

`users`テーブルの`id`カラムに、指定された値が存在することを確認します。

---

### 🔐 パスワードに関するルール

**`confirmed`: 確認**

```php
$request->validate([
    'password' => 'required|confirmed',
]);
```

`password_confirmation`フィールドと一致することを確認します。

---

**`min` for パスワード**

```php
$request->validate([
    'password' => 'required|string|min:8',
]);
```

---

**`Password::min()`: より厳格なパスワードルール**

```php
use Illuminate\Validation\Rules\Password;

$request->validate([
    'password' => ['required', 'confirmed', Password::min(8)
        ->letters()
        ->mixedCase()
        ->numbers()
        ->symbols()],
]);
```

*   `letters()`: 文字を含む
*   `mixedCase()`: 大文字と小文字を含む
*   `numbers()`: 数字を含む
*   `symbols()`: 記号を含む

---

### 📁 ファイルに関するルール

**`file`: ファイル**

```php
$request->validate([
    'document' => 'required|file',
]);
```

---

**`image`: 画像**

```php
$request->validate([
    'avatar' => 'required|image',
]);
```

---

**`mimes`: MIMEタイプ**

```php
$request->validate([
    'document' => 'required|file|mimes:pdf,doc,docx',
]);
```

---

**`max` for ファイル**

```php
$request->validate([
    'avatar' => 'required|image|max:2048', // 最大2MB
]);
```

---

### 🔄 条件付きバリデーション

**`required_if`: 条件付き必須**

```php
$request->validate([
    'is_company' => 'required|boolean',
    'company_name' => 'required_if:is_company,true',
]);
```

`is_company`が`true`の場合、`company_name`は必須になります。

---

**`required_with`: 他のフィールドが存在する場合に必須**

```php
$request->validate([
    'address' => 'required_with:city,state',
]);
```

`city`または`state`が存在する場合、`address`は必須になります。

---

**`required_without`: 他のフィールドが存在しない場合に必須**

```php
$request->validate([
    'email' => 'required_without:phone',
]);
```

`phone`が存在しない場合、`email`は必須になります。

---

**`sometimes`: 条件付きバリデーション**

```php
$validator = Validator::make($request->all(), [
    'email' => 'required|email',
]);

$validator->sometimes('reason', 'required|max:500', function ($input) {
    return $input->status === 'rejected';
});
```

`status`が`rejected`の場合、`reason`は必須になります。

---

### 🚀 実践例：ユーザー登録

ユーザー登録フォームのバリデーション実装例です。

```php
public function register(Request $request)
{
    $validated = $request->validate([
        'name' => 'required|string|max:255',
        'email' => 'required|email|unique:users',
        'password' => ['required', 'confirmed', Password::min(8)
            ->letters()
            ->numbers()],
        'birth_date' => 'required|date|before:today',
        'phone' => 'nullable|regex:/^[0-9]{10,11}$/',
        'avatar' => 'nullable|image|max:2048',
    ]);

    $user = User::create([
        'name' => $validated['name'],
        'email' => $validated['email'],
        'password' => Hash::make($validated['password']),
        'birth_date' => $validated['birth_date'],
        'phone' => $validated['phone'] ?? null,
    ]);

    if ($request->hasFile('avatar')) {
        $path = $request->file('avatar')->store('avatars', 'public');
        $user->avatar = $path;
        $user->save();
    }

    return redirect('/login');
}
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `$request->validate([...])` | リクエストデータをバリデーションし、検証済みデータを返します |
| `'name' => 'required\|string\|max:255'` | 名前は必須、文字列、最大255文字 |
| `'email' => 'required\|email\|unique:users'` | メールは必須、メール形式、usersテーブルで一意 |
| `Password::min(8)->letters()->numbers()` | パスワードは最低8文字、英字と数字を含む |
| `'birth_date' => 'required\|date\|before:today'` | 生年月日は必須、日付形式、今日より前 |
| `'phone' => 'nullable\|regex:/^[0-9]{10,11}$/'` | 電話番号は任意、10〜11桁の数字 |
| `'avatar' => 'nullable\|image\|max:2048'` | アバターは任意、画像ファイル、最大2MB |

**バリデーションルールの詳細解説**：

```php
'name' => 'required|string|max:255',
```
→ `required`で必須入力、`string`で文字列型、`max:255`で最大255文字に制限します。

```php
'email' => 'required|email|unique:users',
```
→ `email`でメールアドレス形式をチェックし、`unique:users`で`users`テーブルに同じメールアドレスが存在しないことを確認します。

```php
'password' => ['required', 'confirmed', Password::min(8)
    ->letters()
    ->numbers()],
```
→ 配列形式でルールを指定しています。`confirmed`は`password_confirmation`フィールドとの一致をチェックします。`Password::min(8)->letters()->numbers()`で、最低8文字かつ英字と数字を含むことを要求します。

```php
'birth_date' => 'required|date|before:today',
```
→ `date`で日付形式をチェックし、`before:today`で今日より前の日付であることを確認します。未来の日付は許可されません。

```php
'phone' => 'nullable|regex:/^[0-9]{10,11}$/',
```
→ `nullable`で任意入力とし、`regex`で正規表現パターンにマッチするかをチェックします。`^[0-9]{10,11}$`は「10〜11桁の数字のみ」を意味します。

**処理の流れ**：

```
1. バリデーション実行
   - 失敗時: 自動的にリダイレクトし、エラーメッセージを表示
   - 成功時: $validatedに検証済みデータが格納される
    ↓
2. ユーザーを作成
   - Hash::make()でパスワードをハッシュ化
   - $validated['phone'] ?? null でnull合体演算子を使用
    ↓
3. アバター画像があれば保存
   - hasFile()でファイルの存在をチェック
   - store()でpublic/avatarsディレクトリに保存
    ↓
4. ログインページにリダイレクト
```

**構文解説**：

| 構文 | 説明 |
|:---|:---|
| `$validated['phone'] ?? null` | null合体演算子。`$validated['phone']`がnullまたは未定義の場合、`null`を返します |
| `$request->hasFile('avatar')` | リクエストにファイルが含まれているかをチェックします |
| `$request->file('avatar')->store('avatars', 'public')` | ファイルを`storage/app/public/avatars`ディレクトリに保存し、パスを返します |

---

### 🚀 実践例：投稿の作成

ブログ投稿の作成フォームのバリデーション実装例です。

```php
public function store(Request $request)
{
    $validated = $request->validate([
        'title' => 'required|string|max:255',
        'content' => 'required|string',
        'category_id' => 'required|exists:categories,id',
        'tags' => 'nullable|array',
        'tags.*' => 'exists:tags,id',
        'is_published' => 'required|boolean',
        'published_at' => 'required_if:is_published,true|date|after:now',
        'thumbnail' => 'nullable|image|max:5120',
    ]);

    $post = Auth::user()->posts()->create([
        'title' => $validated['title'],
        'content' => $validated['content'],
        'category_id' => $validated['category_id'],
        'is_published' => $validated['is_published'],
        'published_at' => $validated['published_at'] ?? null,
    ]);

    if (isset($validated['tags'])) {
        $post->tags()->attach($validated['tags']);
    }

    return redirect('/posts/' . $post->id);
}
```

**コードリーディング**：

| コード | 説明 |
|:---|:---|
| `'title' => 'required\|string\|max:255'` | タイトルは必須、文字列、最大255文字 |
| `'content' => 'required\|string'` | 本文は必須、文字列 |
| `'category_id' => 'required\|exists:categories,id'` | カテゴリIDは必須、categoriesテーブルに存在すること |
| `'tags' => 'nullable\|array'` | タグは任意、配列形式 |
| `'tags.*' => 'exists:tags,id'` | タグ配列の各要素がtagsテーブルに存在すること |
| `'is_published' => 'required\|boolean'` | 公開フラグは必須、真偽値 |
| `'published_at' => 'required_if:is_published,true\|date\|after:now'` | 公開時は公開日時が必須、未来の日付 |
| `'thumbnail' => 'nullable\|image\|max:5120'` | サムネイルは任意、画像ファイル、最大5MB |

**バリデーションルールの詳細解説**：

```php
'category_id' => 'required|exists:categories,id',
```
→ `exists:categories,id`で、送信された`category_id`が`categories`テーブルの`id`カラムに存在することを確認します。存在しないカテゴリIDが送信された場合、バリデーションエラーになります。

```php
'tags' => 'nullable|array',
'tags.*' => 'exists:tags,id',
```
→ `tags`は配列として受け取り、`tags.*`で配列の**各要素**に対してバリデーションを適用します。`*`はワイルドカードで、配列のすべての要素を意味します。各タグIDが`tags`テーブルに存在することを確認します。

```php
'published_at' => 'required_if:is_published,true|date|after:now',
```
→ `required_if:is_published,true`で、`is_published`が`true`の場合のみ`published_at`を必須にします。`after:now`で現在時刻より後の日時であることを確認します。

**処理の流れ**：

```
1. バリデーション実行
   - 失敗時: 自動的にリダイレクトし、エラーメッセージを表示
   - 成功時: $validatedに検証済みデータが格納される
    ↓
2. 投稿を作成
   - Auth::user()->posts()->create()でログインユーザーに紐づく投稿を作成
   - リレーションシップを通じてuser_idが自動的に設定される
    ↓
3. タグがあれば中間テーブルに登録
   - isset()でタグの存在をチェック
   - attach()で多対多リレーションシップを登録
    ↓
4. 作成した投稿の詳細ページにリダイレクト
```

**構文解説**：

| 構文 | 説明 |
|:---|:---|
| `Auth::user()->posts()->create([...])` | ログインユーザーのpostsリレーションシップを通じて投稿を作成します。`user_id`は自動的に設定されます |
| `isset($validated['tags'])` | `$validated['tags']`が存在し、nullでないかをチェックします |
| `$post->tags()->attach($validated['tags'])` | 多対多リレーションシップの中間テーブルにレコードを追加します。タグIDの配列を渡すと、複数のタグを一度に関連付けられます |

**配列バリデーションのポイント**：

```php
'tags' => 'nullable|array',
'tags.*' => 'exists:tags,id',
```

この書き方により、以下のようなリクエストデータをバリデーションできます：

```php
// リクエストデータの例
[
    'tags' => [1, 3, 5]  // タグIDの配列
]
```

`tags.*`の`*`は配列のインデックスを表し、`tags.0`、`tags.1`、`tags.2`...のすべてに対してルールが適用されます。

---

### 💡 TIP: 配列のバリデーション

**配列の各要素をバリデーション**

```php
$request->validate([
    'tags' => 'required|array',
    'tags.*' => 'string|max:50',
]);
```

**ネストした配列のバリデーション**

```php
$request->validate([
    'users' => 'required|array',
    'users.*.name' => 'required|string',
    'users.*.email' => 'required|email',
]);
```

---

### 🚨 よくある間違い

**間違い1: `required`と`nullable`を同時に使う**

```php
$request->validate([
    'bio' => 'required|nullable|string', // 矛盾している
]);
```

**対処法**: どちらか一方のみを使います。

---

**間違い2: `unique`で更新時に自分自身を除外しない**

```php
$request->validate([
    'email' => 'required|email|unique:users', // 自分自身もエラーになる
]);
```

**対処法**: 自分自身を除外します。

```php
$request->validate([
    'email' => 'required|email|unique:users,email,' . $user->id,
]);
```

---

## ✨ まとめ

このセクションでは、よく使うバリデーションルールを学びました。

*   `required`、`nullable`、`string`、`integer`などの基本的なルールを使える。
*   `min`、`max`、`between`などのサイズに関するルールを使える。
*   `email`、`url`、`date`などのフォーマットに関するルールを使える。
*   `unique`、`exists`などのデータベースに関するルールを使える。
*   `required_if`、`required_with`などの条件付きバリデーションを実装できる。

次のセクションでは、カスタムバリデーションルールの作成方法を学びます。

---
