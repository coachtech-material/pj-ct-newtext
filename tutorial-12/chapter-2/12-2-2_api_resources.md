# Tutorial 12-2-2: APIリソースによるレスポンスの整形

## 🎯 このセクションで学ぶこと

- APIリソース（API Resource）の概念と使い方を学ぶ
- レスポンスの整形方法を理解する
- リソースコレクションの使い方を学ぶ

---

## 🧠 先輩エンジニアの思考プロセス

### 「なぜCRUD全体像の後に『API Resources』を学ぶのか？」

CRUD APIの全体像を把握したら、次は「API Resources」です。

---

### 理由1: レスポンス形式の統一

APIのレスポンスは、**一貫した形式**であるべきです。

API Resourcesを使うと、モデルのデータを**決まった形式のJSONに変換**できます。

---

### 理由2: 不要なデータを隠す

モデルには、APIで公開したくないデータ（パスワードなど）が含まれることがあります。

API Resourcesを使うと、**公開するフィールドを制御**できます。

```php
return [
    'id' => $this->id,
    'title' => $this->title,
    // passwordは含めない
];
```

---

### 理由3: データの加工

日付のフォーマットや、リレーションデータの整形など、**データを加工**してから返せます。

---

### このセクションでやること

| 順番 | 作業 | 理由 |
|------|------|------|
| Step 1 | API Resourceの作成 | `php artisan make:resource` |
| Step 2 | コントローラーで使用 | `return new TaskResource($task)` |
| Step 3 | 高度な機能 | リレーションや条件付き属性 |

> 💡 **ポイント**: API Resourcesは、モデルとJSONレスポンスの間の「変換層」です。

---

## Step 1: APIリソースの作成

### 1-1. APIリソースとは

**APIリソース**とは、**モデルをJSON形式に変換するためのクラス**です。

| メリット | 説明 |
|----------|------|
| レスポンスの形式が統一される | 全てのAPIで同じ形式 |
| コードの重複が減る | 変換ロジックを一箇所に |
| 変更に強い | リソースクラスのみを修正 |

---

### 1-2. リソースクラスを生成する

```bash
php artisan make:resource TaskResource
```

これにより、`app/Http/Resources/TaskResource.php`が作成されます。

---

### 1-3. リソースクラスの実装

**ファイル**: `app/Http/Resources/TaskResource.php`

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class TaskResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'description' => $this->description,
            'status' => $this->status,
            'due_date' => $this->due_date?->format('Y-m-d'),
            'created_at' => $this->created_at->format('Y-m-d H:i:s'),
            'updated_at' => $this->updated_at->format('Y-m-d H:i:s'),
        ];
    }
}
```

---

### 1-4. コードリーディング

| コード | 説明 |
|--------|------|
| `$this->id` | Taskモデルのインスタンスからidを取得 |
| `$this->due_date?->format('Y-m-d')` | Null Safe Operator（nullの場合はnullを返す） |

---

## Step 2: コントローラーでの使用

### 2-1. コントローラーの修正

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\TaskResource;
use App\Models\Task;
use Illuminate\Http\Request;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Auth;

class TaskController extends Controller
{
    public function index()
    {
        $tasks = Task::where('user_id', Auth::id())->get();

        return TaskResource::collection($tasks);
    }

    public function store(Request $request)
    {
        $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'due_date' => 'nullable|date',
        ]);

        $task = Task::create([
            'user_id' => Auth::id(),
            'title' => $request->title,
            'description' => $request->description,
            'status' => 'pending',
            'due_date' => $request->due_date,
        ]);

        return new TaskResource($task);
    }

    public function show(string $id)
    {
        $task = Task::where('user_id', Auth::id())->find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        return new TaskResource($task);
    }

    public function update(Request $request, string $id)
    {
        $task = Task::where('user_id', Auth::id())->find($id);

        if (!$task) {
            return response()->json([
                'message' => 'タスクが見つかりません'
            ], 404);
        }

        $request->validate([
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
            'status' => 'required|in:pending,in_progress,completed',
            'due_date' => 'nullable|date',
        ]);

        $task->update($request->only(['title', 'description', 'status', 'due_date']));

        return new TaskResource($task);
    }

    public function destroy(string $id): JsonResponse
    {
        $task = Task::where('user_id', Auth::id())->find($id);

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

### 2-2. 使い分け

| 用途 | コード |
|------|--------|
| 単一のタスク | `return new TaskResource($task);` |
| 複数のタスク | `return TaskResource::collection($tasks);` |

---

### 2-3. レスポンスの形式

**単一のタスク**:

```json
{
  "data": {
    "id": 1,
    "title": "タスク1",
    "description": "これはタスク1です",
    "status": "pending",
    "due_date": "2024-12-31",
    "created_at": "2024-01-01 00:00:00",
    "updated_at": "2024-01-01 00:00:00"
  }
}
```

**複数のタスク**:

```json
{
  "data": [
    {
      "id": 1,
      "title": "タスク1",
      "status": "pending"
    },
    {
      "id": 2,
      "title": "タスク2",
      "status": "completed"
    }
  ]
}
```

---

## Step 3: 高度な機能

### 3-1. 追加情報を含める

**ファイル**: `app/Http/Resources/TaskResource.php`

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class TaskResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => $this->id,
            'title' => $this->title,
            'description' => $this->description,
            'status' => $this->status,
            'status_label' => $this->getStatusLabel(),
            'due_date' => $this->due_date?->format('Y-m-d'),
            'is_overdue' => $this->isOverdue(),
            'created_at' => $this->created_at->format('Y-m-d H:i:s'),
            'updated_at' => $this->updated_at->format('Y-m-d H:i:s'),
        ];
    }

    private function getStatusLabel(): string
    {
        return match ($this->status) {
            'pending' => '未着手',
            'in_progress' => '進行中',
            'completed' => '完了',
            default => '不明',
        };
    }

    private function isOverdue(): bool
    {
        if (!$this->due_date) {
            return false;
        }

        return $this->due_date->isPast() && $this->status !== 'completed';
    }
}
```

---

### 3-2. リレーションシップを含める

```php
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'title' => $this->title,
        'status' => $this->status,
        'user' => [
            'id' => $this->user->id,
            'name' => $this->user->name,
        ],
        'created_at' => $this->created_at->format('Y-m-d H:i:s'),
    ];
}
```

---

### 3-3. 条件付きで属性を含める

```php
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'title' => $this->title,
        'status' => $this->status,
        'user' => $this->when($request->user()->isAdmin(), [
            'id' => $this->user->id,
            'name' => $this->user->name,
        ]),
    ];
}
```

---

### 3-4. リソースコレクションのカスタマイズ

```bash
php artisan make:resource TaskCollection
```

**ファイル**: `app/Http/Resources/TaskCollection.php`

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\ResourceCollection;

class TaskCollection extends ResourceCollection
{
    public function toArray(Request $request): array
    {
        return [
            'data' => $this->collection,
            'meta' => [
                'total' => $this->collection->count(),
                'pending_count' => $this->collection->where('status', 'pending')->count(),
                'completed_count' => $this->collection->where('status', 'completed')->count(),
            ],
        ];
    }
}
```

---

## 🚨 よくある間違い

### 間違い1: リソースを使わずに、直接モデルを返す

**問題**: レスポンス形式が統一されない

**対処法**: APIリソースを使って、レスポンスの形式を統一します。

---

### 間違い2: リソースに複雑なロジックを書く

**問題**: リソースクラスが肥大化する

**対処法**: 複雑なロジックは、モデルやサービスクラスに移動します。

---

### 間違い3: リレーションシップをEager Loadingしない

**問題**: N+1問題が発生する

**対処法**: `with()`を使って、Eager Loadingを行います。

```php
$tasks = Task::with('user')->where('user_id', Auth::id())->get();
```

---

## ✨ まとめ

このセクションでは、APIリソースによるレスポンスの整形について学びました。

| Step | 学んだこと |
|------|-----------|
| Step 1 | APIリソースの作成とtoArray()メソッド |
| Step 2 | コントローラーでの使用方法 |
| Step 3 | リレーションや条件付き属性などの高度な機能 |

次のセクションでは、GET APIの詳細実装について学びます。

---
