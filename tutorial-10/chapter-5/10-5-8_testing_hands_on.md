# Tutorial 10-5-8: テスト - ハンズオン演習

## 📝 このセクションの目的

Chapter 5で学んだテストを実際に手を動かして確認します。フィーチャーテストを作成して、アプリケーションの動作を検証しましょう。

> 分からない文法や実装があっても、すぐに答えを見るのではなく、過去の教材を見たり、AIにヒントをもらいながら進めるなど、自身で創意工夫しながら進めてみましょう🔥

---

## 📁 ディレクトリ構成

このハンズオンでは、**「自分で作成する用」**と**「解答を確認する用」**の2つのプロジェクトを作成します。

```
~/laravel-practice/
├── 10-5-8_hands-on/                      ← このハンズオン用のディレクトリ
│   ├── testing-app-practice/             ← 要件を見て自分で作成するプロジェクト
│   │   ├── app/
│   │   │   ├── Http/Controllers/
│   │   │   └── Models/
│   │   └── tests/
│   │       └── Feature/
│   │           └── TaskTest.php
│   └── testing-app-sample/               ← 実践で一緒に作成するプロジェクト
│       ├── app/
│       │   ├── Http/Controllers/
│       │   └── Models/
│       └── tests/
│           └── Feature/
│               └── TaskTest.php
└── ...
```

| ディレクトリ | 用途 |
|:---|:---|
| `testing-app-practice/` | 📋 要件を見て、自分の力で作成する |
| `testing-app-sample/` | 🏃 実践セクションで、一緒に手を動かしながら作成する |

> 💡 **なぜ2つに分けるのか？**: 自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

> ⚠️ **注意**: 2つのプロジェクトを同時に起動することはできません（ポートが競合するため）。一方のプロジェクトで作業する際は、もう一方を停止してください。

---

## 🎯 演習課題：タスク作成機能のテスト

### 📋 要件

1. `TaskTest`を作成
2. タスク作成のテストを実装
3. バリデーションのテストを実装

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
> cd ~/laravel-practice/10-4-6_hands-on/debugging-app-sample
> ./vendor/bin/sail down
> ```

```bash
# laravel-practiceディレクトリに移動
cd ~/laravel-practice

# ハンズオン用ディレクトリを作成
mkdir -p 10-5-8_hands-on
cd 10-5-8_hands-on

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
~/laravel-practice/
└── 10-5-8_hands-on/
    └── testing-app-practice/     ← 自分で作成する用（今ここ）
        ├── app/
        │   ├── Http/Controllers/
        │   └── Models/
        └── tests/
            └── Feature/
```

> 💡 **環境構築が完了！**
> 
> ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されれば成功です。

**ここから先は、自分の力で実装してみましょう！**

---

## 💡 ヒント

```bash
sail artisan make:test TaskTest
```

```php
public function test_task_can_be_created()
{
    $response = $this->post('/tasks', [
        'title' => 'テストタスク',
        'description' => 'テスト説明',
    ]);
    
    $response->assertStatus(302);
    $this->assertDatabaseHas('tasks', [
        'title' => 'テストタスク',
    ]);
}
```

---

## 🏃 実践: 一緒に作ってみましょう！

ちゃんとできましたか？テストはアプリケーションの品質を保つために不可欠です。一緒に手を動かしながら、タスク作成機能のテストを実装していきましょう。

> 📌 **注意**: ここからは`testing-app-sample/`ディレクトリで作業します。自分で作成したコードと比較できるように、別のプロジェクトで進めましょう。

---

### 💻 環境準備（実践用プロジェクト）

まず、**自分で作成する用のプロジェクトを停止**します：

```bash
# testing-app-practiceディレクトリに移動
cd ~/laravel-practice/10-5-8_hands-on/testing-app-practice

# Sailを停止
./vendor/bin/sail down
```

次に、**実践用のプロジェクトを作成**します：

```bash
# ハンズオンディレクトリに移動
cd ~/laravel-practice/10-5-8_hands-on

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
~/laravel-practice/
└── 10-5-8_hands-on/
    ├── testing-app-practice/     ← 自分で作成した用（停止中）
    └── testing-app-sample/       ← 実践用（今ここ、起動中）
        ├── app/
        │   ├── Http/Controllers/
        │   └── Models/
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
4. **異常系テストを実装**：バリデーションエラーをテスト
5. **テストを実行**：全テストがパスすることを確認

テストのポイントは「正常系と異常系の両方をテストし、アプリケーションの品質を保つ」ことです。

---

### 📝 ステップバイステップで実装

#### ステップ1: テストクラスを作成する

**何を考えているか**：
- 「タスク機能をテストするクラスが必要だ」
- 「TaskTestという名前にしよう」
- 「Artisanコマンドで簡単に生成できる」

ターミナルで以下のコマンドを実行します：

```bash
sail artisan make:test TaskTest
```

**コマンド解説**：

```bash
sail artisan make:test TaskTest
```
→ `TaskTest`フィーチャーテストを生成します。`tests/Feature/TaskTest.php`が作成されます。

---

#### ステップ2: RefreshDatabaseを使用する

**何を考えているか**：
- 「テストごとにデータベースをリセットしたい」
- 「RefreshDatabaseトレイトで簡単に実現できる」
- 「テスト間の干渉を防ぐ」

`tests/Feature/TaskTest.php`を開いて、以下のように編集します：

```php
<?php

namespace Tests\Feature;

use App\Models\Task;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class TaskTest extends TestCase
{
    use RefreshDatabase;
}
```

**コード解説**：

```php
use Illuminate\Foundation\Testing\RefreshDatabase;
```
→ `RefreshDatabase`トレイトをインポートします。

```php
use RefreshDatabase;
```
→ `RefreshDatabase`トレイトを使用します。各テストの前にデータベースがリセットされ、テスト間の干渉を防ぎます。

---

#### ステップ3: 正常系テストを実装する

**何を考えているか**：
- 「タスクが正しく作成されることをテストしよう」
- 「テストユーザーを作成して認証しよう」
- 「データベースにデータが保存されることを確認しよう」

テストメソッドを追加します：

```php
public function test_task_can_be_created()
{
    $user = User::factory()->create();
    
    $response = $this->actingAs($user)->post('/tasks', [
        'title' => 'テストタスク',
        'description' => 'テスト説明',
        'status' => 'pending',
    ]);
    
    $response->assertStatus(302);
    $response->assertRedirect('/tasks');
    
    $this->assertDatabaseHas('tasks', [
        'title' => 'テストタスク',
        'description' => 'テスト説明',
    ]);
}
```

**コード解説**：

```php
$user = User::factory()->create();
```
→ `User::factory()->create()`でテスト用ユーザーを作成します。Factoryでダミーデータを簡単に生成できます。

```php
$response = $this->actingAs($user)->post('/tasks', [
    'title' => 'テストタスク',
    'description' => 'テスト説明',
    'status' => 'pending',
]);
```
→ `actingAs($user)`でユーザーとして認証し、`post()`でタスク作成リクエストを送信します。

```php
$response->assertStatus(302);
$response->assertRedirect('/tasks');
```
→ `assertStatus(302)`でリダイレクトステータスを確認し、`assertRedirect()`でリダイレクト先を確認します。

```php
$this->assertDatabaseHas('tasks', [
    'title' => 'テストタスク',
    'description' => 'テスト説明',
]);
```
→ `assertDatabaseHas()`でデータベースにデータが保存されていることを確認します。

---

#### ステップ4: 異常系テストを実装する

**何を考えているか**：
- 「バリデーションエラーが正しく発生することをテストしよう」
- 「必須項目が空の場合のテストを追加しよう」

テストメソッドを追加します：

```php
public function test_task_title_is_required()
{
    $user = User::factory()->create();
    
    $response = $this->actingAs($user)->post('/tasks', [
        'description' => 'テスト説明',
    ]);
    
    $response->assertSessionHasErrors('title');
}
```

**コード解説**：

```php
$response = $this->actingAs($user)->post('/tasks', [
    'description' => 'テスト説明',
]);
```
→ `title`を含まないデータでリクエストを送信します。

```php
$response->assertSessionHasErrors('title');
```
→ `assertSessionHasErrors()`で`title`フィールドにバリデーションエラーがあることを確認します。

---

#### ステップ5: テストを実行する

**何を考えているか**：
- 「全テストがパスすることを確認しよう」
- 「sail artisan testで実行できる」

ターミナルで以下のコマンドを実行します：

```bash
sail artisan test
```

**コマンド解説**：

```bash
sail artisan test
```
→ 全テストを実行します。緑色のチェックマークが表示されればテスト成功です。

特定のテストファイルだけを実行する場合：

```bash
sail artisan test --filter TaskTest
```

---

### ✨ 完成！

これでフィーチャーテストが実装できました！正常系と異常系の両方をテストし、アプリケーションの品質を保つことができましたね。

**自分で作成したコードと比較してみましょう**：
- `testing-app-practice/`: 自分で作成したプロジェクト
- `testing-app-sample/`: 一緒に作成したプロジェクト

両方のプロジェクトを見比べて、違いがあれば確認してみてください。

---

## 📖 模範解答

### TaskTest.php

```php
<?php

namespace Tests\Feature;

use App\Models\Task;
use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class TaskTest extends TestCase
{
    use RefreshDatabase;

    public function test_task_can_be_created()
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)->post('/tasks', [
            'title' => 'テストタスク',
            'description' => 'テスト説明',
            'status' => 'pending',
        ]);
        
        $response->assertStatus(302);
        $response->assertRedirect('/tasks');
        
        $this->assertDatabaseHas('tasks', [
            'title' => 'テストタスク',
            'description' => 'テスト説明',
        ]);
    }

    public function test_task_title_is_required()
    {
        $user = User::factory()->create();
        
        $response = $this->actingAs($user)->post('/tasks', [
            'description' => 'テスト説明',
        ]);
        
        $response->assertSessionHasErrors('title');
    }

    public function test_task_can_be_updated()
    {
        $user = User::factory()->create();
        $task = Task::factory()->create();
        
        $response = $this->actingAs($user)->put("/tasks/{$task->id}", [
            'title' => '更新されたタスク',
            'description' => '更新された説明',
            'status' => 'completed',
        ]);
        
        $response->assertStatus(302);
        
        $this->assertDatabaseHas('tasks', [
            'id' => $task->id,
            'title' => '更新されたタスク',
        ]);
    }

    public function test_task_can_be_deleted()
    {
        $user = User::factory()->create();
        $task = Task::factory()->create();
        
        $response = $this->actingAs($user)->delete("/tasks/{$task->id}");
        
        $response->assertStatus(302);
        
        $this->assertDatabaseMissing('tasks', [
            'id' => $task->id,
        ]);
    }
}
```

### テスト実行

```bash
sail artisan test
sail artisan test --filter TaskTest
```

---

## 🧪 動作確認の方法

### プロジェクトの切り替え

2つのプロジェクトを切り替えて動作確認する方法：

```bash
# testing-app-practiceで確認したい場合
cd ~/laravel-practice/10-5-8_hands-on/testing-app-sample
./vendor/bin/sail down

cd ~/laravel-practice/10-5-8_hands-on/testing-app-practice
./vendor/bin/sail up -d

# testing-app-sampleで確認したい場合
cd ~/laravel-practice/10-5-8_hands-on/testing-app-practice
./vendor/bin/sail down

cd ~/laravel-practice/10-5-8_hands-on/testing-app-sample
./vendor/bin/sail up -d
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

- ✅ フィーチャーテストを作成できる
- ✅ RefreshDatabaseトレイトでテスト用データベースをリセットできる
- ✅ 正常系テスト（タスク作成）を実装できる
- ✅ 異常系テスト（バリデーションエラー）を実装できる
- ✅ テストを実行して結果を確認できる

引き続き、次のセクションも頑張りましょう！

---
