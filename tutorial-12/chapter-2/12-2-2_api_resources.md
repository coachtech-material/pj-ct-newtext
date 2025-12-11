# Tutorial 12-2-2: APIリソースによるレスポンスの整形

## 🎯 このセクションで学ぶこと

*   APIリソース（API Resource）の概念と使い方を学ぶ。
*   レスポンスの整形方法を理解する。
*   リソースコレクションの使い方を学ぶ。

---

## 導入：なぜAPIリソースが必要なのか

前のセクションでは、`response()->json()`を使ってレスポンスを返しました。

しかし、この方法には以下のような問題があります。

*   **レスポンスの形式が統一されない**: コントローラーごとに異なる形式になる可能性がある
*   **コードの重複**: 同じような処理を何度も書く必要がある
*   **変更に弱い**: レスポンスの形式を変更する際に、全てのコントローラーを修正する必要がある

**APIリソース（API Resource）**を使うことで、これらの問題を解決できます。

---

## 詳細解説

### 🔍 APIリソースとは

**APIリソース**とは、**モデルをJSON形式に変換するためのクラス**です。

APIリソースを使うことで、以下のようなメリットがあります。

*   **レスポンスの形式が統一される**: 全てのAPIで同じ形式のレスポンスを返せる
*   **コードの重複が減る**: 変換ロジックを一箇所にまとめられる
*   **変更に強い**: レスポンスの形式を変更する際に、リソースクラスのみを修正すればよい

---

### 🔍 APIリソースの作成

```bash
php artisan make:resource TaskResource
```

これにより、`app/Http/Resources/TaskResource.php`が作成されます。

---

**ファイル**: `app/Http/Resources/TaskResource.php`

```php
<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class TaskResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     *
     * @return array<string, mixed>
     */
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

### 🔍 コードリーディング

#### `$this->id`

*   `$this`は、Taskモデルのインスタンスを指します。
*   `$this->id`は、タスクのIDを取得します。

---

#### `$this->due_date?->format('Y-m-d')`

*   `?->`は、**Null Safe Operator**です。
*   `due_date`がnullの場合、nullを返します。
*   `due_date`がnullでない場合、`format('Y-m-d')`を実行します。

---

### 🔍 APIリソースの使い方

**ファイル**: `app/Http/Controllers/Api/TaskController.php`

```php
<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\TaskResource;
use App\Models\Task;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class TaskController extends Controller
{
    /**
     * タスク一覧を取得する
     */
    public function index()
    {
        $tasks = Task::where('user_id', Auth::id())->get();

        return TaskResource::collection($tasks);
    }

    /**
     * タスクを作成する
     */
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

    /**
     * タスク詳細を取得する
     */
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

    /**
     * タスクを更新する
     */
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

    /**
     * タスクを削除する
     */
    public function destroy(string $id)
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

### 🔍 コードリーディング

#### `return new TaskResource($task);`

*   単一のタスクを返す場合は、`new TaskResource($task)`を使います。

---

#### `return TaskResource::collection($tasks);`

*   複数のタスクを返す場合は、`TaskResource::collection($tasks)`を使います。

---

### 🔍 レスポンスの形式

APIリソースを使うと、以下のような形式のレスポンスが返されます。

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

---

**複数のタスク**:

```json
{
  "data": [
    {
      "id": 1,
      "title": "タスク1",
      "description": "これはタスク1です",
      "status": "pending",
      "due_date": "2024-12-31",
      "created_at": "2024-01-01 00:00:00",
      "updated_at": "2024-01-01 00:00:00"
    },
    {
      "id": 2,
      "title": "タスク2",
      "description": "これはタスク2です",
      "status": "completed",
      "due_date": "2024-11-30",
      "created_at": "2024-01-01 00:00:00",
      "updated_at": "2024-01-01 00:00:00"
    }
  ]
}
```

---

### 🔍 リソースに追加情報を含める

APIリソースでは、モデルのデータだけでなく、追加情報を含めることもできます。

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

    /**
     * ステータスのラベルを取得する
     */
    private function getStatusLabel(): string
    {
        return match ($this->status) {
            'pending' => '未着手',
            'in_progress' => '進行中',
            'completed' => '完了',
            default => '不明',
        };
    }

    /**
     * 期限切れかどうかを判定する
     */
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

### 🔍 リレーションシップを含める

APIリソースでは、リレーションシップも簡単に含めることができます。

**ファイル**: `app/Http/Resources/TaskResource.php`

```php
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'title' => $this->title,
        'description' => $this->description,
        'status' => $this->status,
        'due_date' => $this->due_date?->format('Y-m-d'),
        'user' => [
            'id' => $this->user->id,
            'name' => $this->user->name,
        ],
        'created_at' => $this->created_at->format('Y-m-d H:i:s'),
        'updated_at' => $this->updated_at->format('Y-m-d H:i:s'),
    ];
}
```

---

### 🔍 条件付きで属性を含める

`when()`メソッドを使うことで、条件付きで属性を含めることができます。

```php
public function toArray(Request $request): array
{
    return [
        'id' => $this->id,
        'title' => $this->title,
        'description' => $this->description,
        'status' => $this->status,
        'due_date' => $this->due_date?->format('Y-m-d'),
        'user' => $this->when($request->user()->isAdmin(), [
            'id' => $this->user->id,
            'name' => $this->user->name,
        ]),
        'created_at' => $this->created_at->format('Y-m-d H:i:s'),
        'updated_at' => $this->updated_at->format('Y-m-d H:i:s'),
    ];
}
```

---

### 💡 TIP: リソースコレクションのカスタマイズ

リソースコレクションをカスタマイズする場合は、`ResourceCollection`を作成します。

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

### 🚨 よくある間違い

#### 間違い1: リソースを使わずに、直接モデルを返す

**対処法**: APIリソースを使って、レスポンスの形式を統一します。

---

#### 間違い2: リソースに複雑なロジックを書く

**対処法**: 複雑なロジックは、モデルやサービスクラスに移動します。

---

#### 間違い3: リレーションシップをEager Loadingしない

**対処法**: `with()`を使って、Eager Loadingを行います。

```php
$tasks = Task::with('user')->where('user_id', Auth::id())->get();
```

---

## ✨ まとめ

このセクションでは、APIリソースによるレスポンスの整形について学びました。

*   APIリソースは、モデルをJSON形式に変換するためのクラスである。
*   APIリソースを使うことで、レスポンスの形式が統一される。
*   `new TaskResource($task)`で単一のタスクを返し、`TaskResource::collection($tasks)`で複数のタスクを返す。
*   リソースに追加情報やリレーションシップを含めることができる。

次のセクションでは、API認証について学びます。

---

## 📝 学習のポイント

- [ ] APIリソース（API Resource）の概念と使い方を学んだ。
- [ ] レスポンスの整形方法を理解した。
- [ ] リソースコレクションの使い方を学んだ。
