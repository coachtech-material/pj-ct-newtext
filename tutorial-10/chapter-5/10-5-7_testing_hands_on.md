# Tutorial 10-5-7: テスト - ハンズオン演習

## 📝 このセクションの目的

Chapter 5で学んだテストを実際に手を動かして確認します。Laravelに最初から用意されている機能を使って、シンプルなテストを作成しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのプロジェクトを作成します。

```
~/coachtech/laravel-practice/
├── 10-5-7_hands-on/                      ← このハンズオン用のディレクトリ
│   ├── testing-app-practice/             ← 要件を見て自分で作成するプロジェクト
│   │   └── tests/
│   │       └── Feature/
│   │           └── UserTest.php
│   └── testing-app-sample/               ← 実践で一緒に作成するプロジェクト
│       └── tests/
│           └── Feature/
│               └── UserTest.php
└── ...
```

| ディレクトリ | 用途 |
|:---|:---|
| `testing-app-practice/` | 📋 要件を見て、自分の力で作成する |
| `testing-app-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

> ⚠️ **注意**: 2つのプロジェクトを同時に起動することはできません（ポートが競合するため）。一方のプロジェクトで作業する際は、もう一方を停止してください。

---

## 🎯 演習課題：ユーザー作成機能のテスト

### 🖼️ 完成イメージ

<!-- テスト実行結果のスクリーンショットをここに配置 -->
![10-5-7 完成イメージ](images/10-5-7_testing_complete.png)

**この演習で作るもの**：
Laravelのテスト機能を使って、ユーザー作成機能のテストコードを作成します。

---

### 📋 要件

このハンズオンでは、**Laravelに最初から用意されているUserモデル**を使ってテストを作成します。

1. `UserTest`を作成
2. ユーザーがデータベースに保存されることをテスト
3. メールアドレスの重複チェックをテスト

> 💡 **ポイント**: Laravelプロジェクトには最初から`User`モデルと`users`テーブルのマイグレーションが用意されています。新しくモデルやコントローラーを作成する必要はありません。

---

### ✅ 完成品の確認方法

**🔧 コマンドラインでの確認**

- **テスト実行コマンド**: `./vendor/bin/sail artisan test`
- **確認手順**:
  1. Sailを起動する（`./vendor/bin/sail up -d`）
  2. マイグレーションを実行（`./vendor/bin/sail artisan migrate`）
  3. テストを実行（`./vendor/bin/sail artisan test`）

**正しく実装できていれば**:
- [ ] テストが全てパスする（緑色の`PASS`が表示される）
- [ ] ユーザーがデータベースに保存されるテストがパス
- [ ] メールアドレス重複チェックのテストがパス

**テスト実行結果の例**:

```
   PASS  Tests\Feature\UserTest
  ✓ user can be created
  ✓ email must be unique

  Tests:  2 passed
  Time:   0.50s
```

---

### 📁 Step 0: 環境を準備する（自分で作成する用）

まず、ハンズオン用のディレクトリを作成し、**自分で作成する用**のプロジェクトを準備します。

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

> **📌 前のハンズオンのプロジェクトを停止**
> 
> 前のハンズオン（10-4-6）のプロジェクトが起動している場合は、先に停止してください。
> ```bash
> cd ~/coachtech/laravel-practice/10-4-6_hands-on/debugging-app-sample
> ./vendor/bin/sail down
> ```

```bash
# laravel-practiceディレクトリに移動
cd ~/coachtech/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 10-5-7_hands-on
cd 10-5-7_hands-on

# Laravel 10.xプロジェクトを作成（自分で作成する用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 testing-app-practice
```

```bash
# プロジェクトディレクトリに移動
cd testing-app-practice

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql

# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate

# データベースのマイグレーション
./vendor/bin/sail artisan migrate
```

**✅ ディレクトリ構造の確認**

```
~/coachtech/laravel-practice/
└── 10-5-7_hands-on/
    └── testing-app-practice/     ← 自分で作成する用（今ここ）
        ├── app/
        │   └── Models/
        │       └── User.php      ← 最初から用意されている
        ├── database/
        │   └── migrations/
        │       └── ..._create_users_table.php  ← 最初から用意されている
        └── tests/
            └── Feature/
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

### ヒント1: テストファイルの作成

```bash
sail artisan make:test UserTest
```

### ヒント2: RefreshDatabaseトレイト

テストごとにデータベースをリセットするには、`RefreshDatabase`トレイトを使います。

```php
use Illuminate\Foundation\Testing\RefreshDatabase;

class UserTest extends TestCase
{
    use RefreshDatabase;
}
```

### ヒント3: ユーザーの作成

`User::factory()->create()`でテスト用ユーザーを作成できます。

```php
$user = User::factory()->create([
    'name' => 'テストユーザー',
    'email' => 'test@example.com',
]);
```

### ヒント4: データベースの確認

`assertDatabaseHas()`でデータベースにデータが存在することを確認できます。

```php
$this->assertDatabaseHas('users', [
    'email' => 'test@example.com',
]);
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？テストはアプリケーションの品質を保つために不可欠です。一緒に手を動かしながら、ユーザー作成機能のテストを実装していきましょう。

> 📌 **注意**: ここからは`testing-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### 💻 環境準備（実践用プロジェクト）

まず、**自分で作成する用のプロジェクトを停止**します：

```bash
# testing-app-practiceディレクトリに移動
cd ~/coachtech/laravel-practice/10-5-7_hands-on/testing-app-practice

# Sailを停止
./vendor/bin/sail down
```

次に、**実践用のプロジェクトを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/coachtech/laravel-practice/10-5-7_hands-on

# Laravel 10.xプロジェクトを作成（実践用）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 testing-app-sample
```

```bash
# プロジェクトディレクトリに移動
cd testing-app-sample

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql

# Sailの起動
./vendor/bin/sail up -d

# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate

# データベースのマイグレーション
./vendor/bin/sail artisan migrate
```

**✅ ディレクトリ構造の確認**

```
~/coachtech/laravel-practice/
└── 10-5-7_hands-on/
    ├── testing-app-practice/     ← 自分で作成した用（停止中）
    └── testing-app-sample/       ← 実践用（今ここ、起動中）
        ├── app/
        │   └── Models/
        │       └── User.php
        └── tests/
            └── Feature/
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

---

### 💭 実装の思考プロセス

テストを実装する際、以下の順番で考えると効率的です：

1. **テストクラスを作成**：Artisanコマンドで生成
2. **RefreshDatabaseを使用**：テスト用データベースをリセット
3. **正常系テストを実装**：機能が正しく動作することを確認
4. **異常系テストを実装**：エラーケースをテスト
5. **テストを実行**：全テストがパスすることを確認

テストのポイントは「正常系と異常系の両方をテストし、アプリケーションの品質を保つ」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: テストクラスを作成する

**何を考えているか**：
- 「ユーザー機能をテストするクラスが必要だ」
- 「UserTestという名前にしよう」
- 「Artisanコマンドで簡単に生成できる」

ターミナルで以下のコマンドを実行します：

```bash
sail artisan make:test UserTest
```

**コマンド解説**：

| 部分 | 説明 |
|------|------|
| `make:test` | テストファイルを作成 |
| `UserTest` | テストクラス名 |

→ `tests/Feature/UserTest.php`が作成されます。

---

#### ステップ2: RefreshDatabaseを使用する

**何を考えているか**：
- 「テストごとにデータベースをリセットしたい」
- 「RefreshDatabaseトレイトで簡単に実現できる」
- 「テスト間の干渉を防ぐ」

`tests/Feature/UserTest.php`を開いて、以下のように編集します：

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class UserTest extends TestCase
{
    use RefreshDatabase;
}
```

**コード解説**：

| 行 | コード | 説明 |
|:---|:---|:---|
| 1 | `use App\Models\User;` | Userモデルをインポート |
| 2 | `use Illuminate\Foundation\Testing\RefreshDatabase;` | RefreshDatabaseトレイトをインポート |
| 3 | `use RefreshDatabase;` | 各テストの前にデータベースをリセット |

---

#### ステップ3: 正常系テストを実装する

**何を考えているか**：
- 「ユーザーがデータベースに保存されることをテストしよう」
- 「User::factory()でテストユーザーを作成しよう」
- 「assertDatabaseHas()でデータベースを確認しよう」

テストメソッドを追加します：

```php
public function test_user_can_be_created()
{
    // ユーザーを作成
    $user = User::factory()->create([
        'name' => 'テストユーザー',
        'email' => 'test@example.com',
    ]);
    
    // データベースにユーザーが存在することを確認
    $this->assertDatabaseHas('users', [
        'name' => 'テストユーザー',
        'email' => 'test@example.com',
    ]);
}
```

**コード解説**：

| 行 | コード | 説明 |
|:---|:---|:---|
| 1 | `User::factory()->create([...])` | 指定した属性でユーザーを作成 |
| 2 | `'name' => 'テストユーザー'` | ユーザー名を指定 |
| 3 | `'email' => 'test@example.com'` | メールアドレスを指定 |
| 4 | `$this->assertDatabaseHas('users', [...])` | usersテーブルにデータが存在することを確認 |

---

#### ステップ4: 異常系テストを実装する

**何を考えているか**：
- 「メールアドレスの重複をテストしよう」
- 「同じメールアドレスで2人目のユーザーを作成しようとするとエラーになるはず」

テストメソッドを追加します：

```php
public function test_email_must_be_unique()
{
    // 1人目のユーザーを作成
    User::factory()->create([
        'email' => 'duplicate@example.com',
    ]);
    
    // 同じメールアドレスで2人目を作成しようとすると例外が発生
    $this->expectException(\Illuminate\Database\QueryException::class);
    
    User::factory()->create([
        'email' => 'duplicate@example.com',
    ]);
}
```

**コード解説**：

| 行 | コード | 説明 |
|:---|:---|:---|
| 1 | `User::factory()->create([...])` | 1人目のユーザーを作成 |
| 2 | `$this->expectException(...)` | 例外が発生することを期待 |
| 3 | `QueryException::class` | データベースエラーの例外クラス |

> 💡 **ポイント**: `users`テーブルの`email`カラムには`unique`制約があるため、同じメールアドレスで2人目を作成しようとすると`QueryException`が発生します。

---

#### ステップ5: テストを実行する

**何を考えているか**：
- 「全テストがパスすることを確認しよう」
- 「sail artisan testで実行できる」

ターミナルで以下のコマンドを実行します：

```bash
sail artisan test --filter UserTest
```

**コマンド解説**：

| 部分 | 説明 |
|------|------|
| `test` | テストを実行 |
| `--filter UserTest` | UserTestクラスのテストのみ実行 |

**期待される出力**：

```
PASS  Tests\Feature\UserTest
✓ user can be created
✓ email must be unique

Tests:    2 passed (3 assertions)
Duration: 0.50s
```

緑色のチェックマークが表示されればテスト成功です！

---

### ✨ 完成！

これでフィーチャーテストが実装できました！正常系と異常系の両方をテストし、アプリケーションの品質を保つことができましたね。

**自分で作成したコードと比較してみましょう**：
- `testing-app-practice/tests/Feature/UserTest.php`: 自分で作成したテスト
- `testing-app-sample/tests/Feature/UserTest.php`: 一緒に作成したテスト

両方のファイルを比較して、実装内容を確認してみてください。

---

## 📖 模範解答

### tests/Feature/UserTest.php

```php
<?php

namespace Tests\Feature;

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class UserTest extends TestCase
{
    use RefreshDatabase;

    /**
     * ユーザーがデータベースに保存されることをテスト
     */
    public function test_user_can_be_created()
    {
        // ユーザーを作成
        $user = User::factory()->create([
            'name' => 'テストユーザー',
            'email' => 'test@example.com',
        ]);
        
        // データベースにユーザーが存在することを確認
        $this->assertDatabaseHas('users', [
            'name' => 'テストユーザー',
            'email' => 'test@example.com',
        ]);
    }

    /**
     * メールアドレスの重複チェックをテスト
     */
    public function test_email_must_be_unique()
    {
        // 1人目のユーザーを作成
        User::factory()->create([
            'email' => 'duplicate@example.com',
        ]);
        
        // 同じメールアドレスで2人目を作成しようとすると例外が発生
        $this->expectException(\Illuminate\Database\QueryException::class);
        
        User::factory()->create([
            'email' => 'duplicate@example.com',
        ]);
    }
}
```

---

## 🚨 うまくいかない場合

### エラー1: テストが見つからない

**原因**: テストファイルが正しい場所にない

**対処法**:

```bash
# テストファイルの場所を確認
ls tests/Feature/
```

`UserTest.php`が存在することを確認してください。

---

### エラー2: RefreshDatabase関連のエラー

**原因**: データベース接続の問題

**対処法**:

```bash
# Sailが起動しているか確認
sail ps

# 起動していない場合
sail up -d
```

---

### エラー3: User::factory()が見つからない

**原因**: Factoryが存在しない

**対処法**:

Laravelプロジェクトには最初から`database/factories/UserFactory.php`が用意されています。ファイルが存在することを確認してください。

```bash
ls database/factories/
```

---

## ✨ まとめ

このハンズオンでは、Laravelのテスト機能を使ってユーザー作成機能のテストを実装しました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | `make:test`でテストファイルを作成 |
| Step 2 | `RefreshDatabase`でテストごとにDBをリセット |
| Step 3 | `User::factory()->create()`でテストデータを作成 |
| Step 4 | `assertDatabaseHas()`でDBの状態を確認 |
| Step 5 | `expectException()`で例外発生をテスト |

**テストの重要なポイント**:

- ✅ 正常系テスト：期待通りに動作することを確認
- ✅ 異常系テスト：エラーケースを確認
- ✅ RefreshDatabase：テスト間の干渉を防ぐ
- ✅ Factory：テストデータを簡単に作成

次のChapter 6では、Webセキュリティについて学びます。

### 🛑 Sailの停止

次のセクションに進む前に、Sailを停止しておきましょう。

```bash
./vendor/bin/sail down
```

> 💡 **なぜ停止するの？**: Sailを起動したままだと、次のセクションで別のプロジェクトを起動する際にポートが競合してエラーになることがあります。セクションの終わりには必ずSailを停止する習慣をつけましょう。

---
