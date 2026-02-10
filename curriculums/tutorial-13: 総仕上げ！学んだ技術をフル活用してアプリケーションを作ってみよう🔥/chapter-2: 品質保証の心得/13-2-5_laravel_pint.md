# Tutorial 13-2-5: Laravel Pint

## 🎯 このセクションで学ぶこと

- Laravel Pintとは何かを理解する
- コードフォーマッターの重要性を学ぶ
- Pintの基本的な使い方を知る

> ⚠️ **注意**: このChapterでは**実際のコードは書きません**。品質の高いコードを書くための「心得」を学びます。実際にPintを実行するのはChapter 3以降です。

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜ品質保証の最後にLaravel Pintなのか？」

DRY原則、命名規則、コレクションメソッド、可読性を学んだら、最後に**コードフォーマッター**を紹介します。

### 理由1: 一貫性を自動で保つ

前のセクションで「一貫性」の重要性を学びました。しかし、人間が手動で一貫性を保つのは大変です。**Laravel Pint**を使えば、コードスタイルを**自動で統一**できます。

### 理由2: チーム開発での必須ツール

チーム開発では、メンバーごとにコードスタイルが異なると、レビューが大変になります。Pintを使えば、**全員が同じスタイル**でコードを書けます。

### 理由3: 本質的な作業に集中できる

インデントや空白の調整に時間を使う必要がなくなり、**ロジックの実装**に集中できます。

---

## Laravel Pintとは

### 概要

**Laravel Pint**は、Laravelの公式コードフォーマッターです。PHP-CS-Fixerをベースにしており、Laravel向けに最適化されています。

```
Laravel Pint = PHP-CS-Fixer + Laravel向けの設定
```

### 何ができるか

| 機能 | 説明 |
|:---|:---|
| **インデントの統一** | タブ/スペースを統一 |
| **空白の調整** | 演算子の前後、カンマの後など |
| **括弧の位置** | PSR-12に準拠 |
| **use文の整理** | アルファベット順にソート |
| **不要な空行の削除** | 余分な空行を削除 |

### Before / After

**Before（フォーマット前）**:

```php
<?php
namespace App\Http\Controllers;
use App\Models\Task;
use Illuminate\Http\Request;
use App\Http\Requests\StoreTaskRequest;

class TaskController extends Controller{
    public function index(){
        $tasks=auth()->user()->tasks()->with('category')->get();
        return view('tasks.index',compact('tasks'));
    }
    
    
    public function store(StoreTaskRequest $request){
        auth()->user()->tasks()->create($request->validated());
        return redirect()->route('tasks.index')->with('success','タスクを登録しました。');
    }
}
```

**After（フォーマット後）**:

```php
<?php

namespace App\Http\Controllers;

use App\Http\Requests\StoreTaskRequest;
use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    public function index()
    {
        $tasks = auth()->user()->tasks()->with('category')->get();

        return view('tasks.index', compact('tasks'));
    }

    public function store(StoreTaskRequest $request)
    {
        auth()->user()->tasks()->create($request->validated());

        return redirect()->route('tasks.index')->with('success', 'タスクを登録しました。');
    }
}
```

**改善点**:
- `namespace`の前後に空行が追加
- `use`文がアルファベット順にソート
- 括弧の位置がPSR-12に準拠
- 演算子の前後に空白が追加
- カンマの後に空白が追加
- 余分な空行が削除

---

## Pintの基本的な使い方

### インストール

Laravel 9以降では、Pintは**標準でインストール**されています。

```bash
# インストール確認
./vendor/bin/pint --version
```

### 基本コマンド

```bash
# 全ファイルをフォーマット
./vendor/bin/pint

# 特定のディレクトリをフォーマット
./vendor/bin/pint app/Http/Controllers

# 特定のファイルをフォーマット
./vendor/bin/pint app/Http/Controllers/TaskController.php

# プレビュー（実際には変更しない）
./vendor/bin/pint --test

# 変更内容を表示
./vendor/bin/pint -v
```

### コードリーディング

| コマンド | 説明 |
|:---|:---|
| `./vendor/bin/pint` | プロジェクト全体をフォーマット |
| `--test` | 変更が必要なファイルを表示（実際には変更しない） |
| `-v` | 変更内容を詳細に表示 |

---

## 設定ファイル

### pint.json

プロジェクトルートに`pint.json`を作成すると、カスタム設定ができます。

```json
{
    "preset": "laravel",
    "rules": {
        "concat_space": {
            "spacing": "one"
        }
    },
    "exclude": [
        "app/Console"
    ]
}
```

### コードリーディング

| 項目 | 説明 |
|:---|:---|
| `preset` | ベースとなるルールセット（`laravel`, `psr12`, `symfony`など） |
| `rules` | 個別のルールをカスタマイズ |
| `exclude` | フォーマット対象から除外するディレクトリ |

### プリセット

| プリセット | 説明 |
|:---|:---|
| `laravel` | Laravel推奨のスタイル（デフォルト） |
| `psr12` | PSR-12に準拠 |
| `symfony` | Symfonyのスタイル |

---

## 実務での使い方

### 開発フロー

```
1. コードを書く
2. git add する前に Pint を実行
3. フォーマットされたコードをコミット
```

```bash
# 開発フローの例
./vendor/bin/pint
git add .
git commit -m "タスク一覧機能を実装"
```

### Git Hooks との連携

`pre-commit`フックを設定すると、コミット前に自動でPintが実行されます。

```bash
# .git/hooks/pre-commit
#!/bin/sh
./vendor/bin/pint --test
if [ $? -ne 0 ]; then
    echo "コードスタイルに問題があります。./vendor/bin/pint を実行してください。"
    exit 1
fi
```

### CI/CD での使用

GitHub Actionsなどで、プルリクエスト時にPintをチェックできます。

```yaml
# .github/workflows/pint.yml
name: Laravel Pint
on: [pull_request]
jobs:
  pint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run Pint
        run: ./vendor/bin/pint --test
```

---

## Pintを使うメリット

| メリット | 説明 |
|:---|:---|
| **時間の節約** | フォーマットを手動で行う必要がない |
| **一貫性の確保** | チーム全員が同じスタイルでコードを書ける |
| **レビューの効率化** | スタイルの指摘が不要になり、ロジックに集中できる |
| **学習コストの低減** | 細かいスタイルルールを覚える必要がない |

---

## 🚨 よくある間違い

### 間違い1: Pintを実行せずにコミット

```bash
# ❌ Pintを実行せずにコミット
git add .
git commit -m "機能追加"

# ✅ Pintを実行してからコミット
./vendor/bin/pint
git add .
git commit -m "機能追加"
```

### 間違い2: 全ファイルを毎回フォーマット

```bash
# ❌ 毎回全ファイルをフォーマット（時間がかかる）
./vendor/bin/pint

# ✅ 変更したファイルのみフォーマット
./vendor/bin/pint app/Http/Controllers/TaskController.php
```

### 間違い3: フォーマットと機能追加を同じコミットに

```bash
# ❌ フォーマットと機能追加が混在
git commit -m "タスク機能追加とフォーマット修正"

# ✅ 別々のコミットに分ける
git commit -m "コードフォーマットを修正"
git commit -m "タスク機能を追加"
```

---

## ✨ まとめ

このセクションでは、Laravel Pintについて学びました。

- **Laravel Pint**はLaravel公式のコードフォーマッター
- コードスタイルを**自動で統一**できる
- チーム開発での**一貫性確保**に必須
- `./vendor/bin/pint`で実行

### 品質保証の心得まとめ

| セクション | 学んだこと |
|:---|:---|
| 13-2-1 | DRY原則で重複を排除 |
| 13-2-2 | 命名規則で意図を明確に |
| 13-2-3 | コレクションメソッドで簡潔に |
| 13-2-4 | 可読性を高めるテクニック |
| 13-2-5 | Laravel Pintで一貫性を自動確保 |

次のChapterでは、いよいよ**環境構築**を行い、実際にコードを書いていきます。ここで学んだ「心得」を意識しながら、品質の高いコードを書いていきましょう。

---
