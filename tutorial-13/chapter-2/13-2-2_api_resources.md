# Tutorial 13-2-2: API Resourcesの活用

## 🎯 このセクションで学ぶこと

- API Resourcesとは何かを理解する
- API Resourcesを使ってレスポンスを整形する方法を学ぶ
- レスポンスから不要なデータを除外する方法を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜCRUD実装の後に『API Resources』を学ぶのか？」

CRUD APIが完成したら、次は「レスポンスの整形」です。

---

### 理由1: レスポンスの一貫性

現在のAPIは、モデルのデータをそのまま返しています。

```json
{
  "data": {
    "id": 1,
    "user_id": 1,
    "title": "タスク1",
    "description": "説明",
    "status": "pending",
    "due_date": "2024-12-31",
    "created_at": "2024-01-01T00:00:00.000000Z",
    "updated_at": "2024-01-01T00:00:00.000000Z"
  }
}
```

しかし、以下の問題があります。

| 問題 | 説明 |
|------|------|
| 不要なデータが含まれる | `user_id`はクライアントに不要かもしれない |
| 日付フォーマットが統一されていない | `2024-01-01T00:00:00.000000Z`は読みにくい |
| 構造が固定されている | 将来の変更に対応しにくい |

---

### 理由2: API Resourcesで解決

**API Resources**を使うと、レスポンスの形式を自由にカスタマイズできます。

```json
{
  "data": {
    "id": 1,
    "title": "タスク1",
    "description": "説明",
    "status": "pending",
    "due_date": "2024-12-31",
    "created_at": "2024-01-01 00:00:00"
  }
}
```

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | API Resourcesの基本 | 概念を理解する |
| Step 2 | TaskResourceの作成 | 実際に作成する |
| Step 3 | コントローラーでの使用 | APIに適用する |

> 💡 **ポイント**: API Resourcesは「レスポンスの変換層」です。

---

## Step 1: API Resourcesの基本

### 1-1. API Resourcesとは

**API Resources**は、Eloquentモデルを**JSONレスポンスに変換**するクラスです。

| 役割 | 説明 |
|------|------|
| データの整形 | 必要なフィールドだけを選択 |
| フォーマットの統一 | 日付形式などを統一 |
| 構造の定義 | レスポンスの構造を明確化 |

---

### 1-2. なぜ必要なのか

モデルをそのまま返すと、以下の問題があります。

| 問題 | 説明 |
|------|------|
| 内部構造の露出 | データベースの構造がそのまま見える |
| 不要なデータ | クライアントに不要なフィールドも含まれる |
| 変更に弱い | データベースを変更するとAPIも変わる |

API Resourcesを使うと、**モデルとAPIレスポンスを分離**できます。

---

### 1-3. 処理の流れ

```
データベース
    ↓
Eloquentモデル
    ↓
API Resource（変換）
    ↓
JSONレスポンス
```

---

## Step 2: TaskResourceの作成

### 2-1. Resourceを生成する

```bash
sail artisan make:resource TaskResource
```

**生成されるファイル**: `app/Http/Resources/TaskResource.php`

---

### 2-2. TaskResourceの実装

**ファイル**: `app/Http/Resources/TaskResource.php`

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class TaskResource extends JsonResource
{
    public function toArray(Request $request)
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'description' => $this->description,
            'status' => $this->status,
            'status_label' => $this->getStatusLabel(),
            'due_date' => $this->formatDueDate(),
            'created_at' => $this->created_at->format('Y-m-d H:i:s'),
            'updated_at' => $this->updated_at->format('Y-m-d H:i:s'),
        ];
    }

    /**
     * ステータスの日本語ラベルを取得
     */
    private function getStatusLabel()
    {
        $labels = [
            'pending' => '未着手',
            'in_progress' => '進行中',
            'completed' => '完了',
        ];

        if (isset($labels[$this->status])) {
            return $labels[$this->status];
        }

        return $this->status;
    }

    /**
     * 期限日をフォーマット
     */
    private function formatDueDate()
    {
        if ($this->due_date) {
            return $this->due_date->format('Y-m-d');
        }

        return null;
    }
}
```

---

### 2-3. コードリーディング

#### `class TaskResource extends JsonResource`

```php
class TaskResource extends JsonResource
```

| 部分 | 説明 |
|------|------|
| `class TaskResource` | クラス名 |
| `extends JsonResource` | LaravelのJsonResourceクラスを継承 |

---

#### `public function toArray(Request $request)`

```php
public function toArray(Request $request)
{
    return [
        'id' => $this->id,
        // ...
    ];
}
```

| 部分 | 説明 |
|------|------|
| `toArray()` | JSONに変換するメソッド |
| `$request` | 現在のリクエスト（条件分岐に使える） |
| `$this->id` | モデルのidプロパティにアクセス |

---

#### `$this->id`

```php
'id' => $this->id,
```

| 部分 | 説明 |
|------|------|
| `$this` | TaskResourceに渡されたTaskモデル |
| `->id` | モデルのidカラムの値 |

TaskResourceは、渡されたモデルを`$this`として扱えます。

---

#### `$this->created_at->format('Y-m-d H:i:s')`

```php
'created_at' => $this->created_at->format('Y-m-d H:i:s'),
```

| 部分 | 説明 |
|------|------|
| `$this->created_at` | Carbonオブジェクト（日付） |
| `->format('Y-m-d H:i:s')` | 日付を文字列に変換 |

---

#### `private function getStatusLabel()`

```php
private function getStatusLabel()
{
    $labels = [
        'pending' => '未着手',
        'in_progress' => '進行中',
        'completed' => '完了',
    ];

    if (isset($labels[$this->status])) {
        return $labels[$this->status];
    }

    return $this->status;
}
```

| 部分 | 説明 |
|------|------|
| `private function` | このクラス内でのみ使えるメソッド |
| `$labels = [...]` | ステータスと日本語ラベルの対応表 |
| `isset($labels[$this->status])` | キーが存在するか確認 |
| `$labels[$this->status]` | 対応する日本語ラベルを取得 |

---

#### `private function formatDueDate()`

```php
private function formatDueDate()
{
    if ($this->due_date) {
        return $this->due_date->format('Y-m-d');
    }

    return null;
}
```

| 部分 | 説明 |
|------|------|
| `if ($this->due_date)` | due_dateがnullでない場合 |
| `->format('Y-m-d')` | 日付を文字列に変換 |
| `return null` | nullの場合はnullを返す |

---

### 2-4. レスポンスの比較

**Before（API Resourceなし）**:

```json
{
  "data": {
    "id": 1,
    "user_id": 1,
    "title": "タスク1",
    "description": "説明",
    "status": "pending",
    "due_date": "2024-12-31",
    "created_at": "2024-01-01T00:00:00.000000Z",
    "updated_at": "2024-01-01T00:00:00.000000Z"
  }
}
```

**After（API Resourceあり）**:

```json
{
  "data": {
    "id": 1,
    "title": "タスク1",
    "description": "説明",
    "status": "pending",
    "status_label": "未着手",
    "due_date": "2024-12-31",
    "created_at": "2024-01-01 00:00:00",
    "updated_at": "2024-01-01 00:00:00"
  }
}
```

| 変更点 | 説明 |
|--------|------|
| `user_id`が削除された | クライアントに不要なデータを除外 |
| `status_label`が追加された | 日本語ラベルを追加 |
| 日付フォーマットが統一された | 読みやすい形式に変換 |

---

## Step 3: コントローラーでの使用

### 3-1. コントローラーの修正

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\TaskResource;
use App\Models\Task;
use Illuminate\Http\Request;

class TaskController extends Controller
{
    /**
     * タスク一覧を取得
     */
    public function index()
    {
        $tasks = Task::where('user_id', 1)->get();

        return TaskResource::collection($tasks);
    }

    /**
     * タスクを作成
     */
    public function store(Request $request)
    {
        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'due_date' => 'nullable|date',
        ]);

        $data = array_merge($validated, [
            'user_id' => 1,
            'status' => 'pending',
        ]);
        
        $task = Task::create($data);

        return (new TaskResource($task))
            ->additional(['message' => 'タスクを作成しました'])
            ->response()
            ->setStatusCode(201);
    }

    /**
     * タスク詳細を取得
     */
    public function show(string $id)
    {
        $task = Task::where('user_id', 1)->find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        return new TaskResource($task);
    }

    /**
     * タスクを更新
     */
    public function update(Request $request, string $id)
    {
        $task = Task::where('user_id', 1)->find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        $validated = $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'status' => 'required|in:pending,in_progress,completed',
            'due_date' => 'nullable|date',
        ]);

        $task->update($validated);

        return (new TaskResource($task))
            ->additional(['message' => 'タスクを更新しました']);
    }

    /**
     * タスクを削除
     */
    public function destroy(string $id)
    {
        $task = Task::where('user_id', 1)->find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        $task->delete();

        return response()->json(null, 204);
    }
}
```

---

### 3-2. コードリーディング

#### `use App\Http\Resources\TaskResource`

```php
use App\Http\Resources\TaskResource;
```

| 部分 | 説明 |
|------|------|
| `use` | クラスをインポート |
| `App\Http\Resources\TaskResource` | 作成したTaskResourceクラス |

---

#### `TaskResource::collection($tasks)`

```php
return TaskResource::collection($tasks);
```

| 部分 | 説明 |
|------|------|
| `TaskResource::collection()` | 複数のモデルをResourceに変換 |
| `$tasks` | Taskモデルのコレクション |

**レスポンス例**:

```json
{
  "data": [
    { "id": 1, "title": "タスク1", ... },
    { "id": 2, "title": "タスク2", ... }
  ]
}
```

---

#### `new TaskResource($task)`

```php
return new TaskResource($task);
```

| 部分 | 説明 |
|------|------|
| `new TaskResource(...)` | 単一のモデルをResourceに変換 |
| `$task` | Taskモデルのインスタンス |

**レスポンス例**:

```json
{
  "data": {
    "id": 1,
    "title": "タスク1",
    ...
  }
}
```

---

#### `->additional(['message' => '...'])`

```php
return (new TaskResource($task))
    ->additional(['message' => 'タスクを作成しました'])
    ->response()
    ->setStatusCode(201);
```

| 部分 | 説明 |
|------|------|
| `->additional([...])` | レスポンスに追加データを含める |
| `->response()` | レスポンスオブジェクトを取得 |
| `->setStatusCode(201)` | ステータスコードを設定 |

**レスポンス例**:

```json
{
  "data": {
    "id": 1,
    "title": "新しいタスク",
    ...
  },
  "message": "タスクを作成しました"
}
```

---

### 3-3. Thunder Clientでテスト

#### タスク一覧を取得

- メソッド: `GET`
- URL: `http://localhost/api/tasks`
- 期待: `status_label`が含まれたレスポンス

---

#### タスクを作成

- メソッド: `POST`
- URL: `http://localhost/api/tasks`
- Headers: `Content-Type: application/json`
- Body（JSON）:

```json
{
  "title": "新しいタスク",
  "description": "テスト"
}
```

- 期待: `message`と`data`が含まれたレスポンス

---

## 🚨 よくある間違い

### 間違い1: collectionとnewを間違える

**問題**: 複数のモデルに`new`を使う

```php
// ❌ 間違い
return new TaskResource($tasks);

// ✅ 正しい
return TaskResource::collection($tasks);
```

---

### 間違い2: useを忘れる

**問題**: クラスが見つからないエラー

```php
// ❌ 間違い（useなし）
return new TaskResource($task);

// ✅ 正しい（useあり）
use App\Http\Resources\TaskResource;
return new TaskResource($task);
```

---

### 間違い3: toArrayの戻り値が配列でない

**問題**: JSONに変換できない

```php
// ❌ 間違い
public function toArray(Request $request)
{
    return $this->title;  // 文字列を返している
}

// ✅ 正しい
public function toArray(Request $request)
{
    return [
        'title' => $this->title,
    ];
}
```

---

## ✨ まとめ

このセクションでは、API Resourcesを使ったレスポンスの整形を学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | API Resourcesの概念と役割 |
| Step 2 | TaskResourceの作成と実装 |
| Step 3 | コントローラーでの使用方法 |

次のセクションでは、GET APIの詳細取得について学びます。

---
