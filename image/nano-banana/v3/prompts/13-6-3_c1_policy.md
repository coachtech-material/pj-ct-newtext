# 13-6-3_c1: タスクPolicy

## 対象Section
- Tutorial 13-6-3: タスクPolicy実装
- 説明: Policyによる認可処理の概念図

## リサーチメモ
- Policy = 認可ロジックを集約するクラス
- Before: 各メソッドに所有者チェックのコードが重複
- After: Policyに認可ロジックを1箇所にまとめる
- メリット: コード集約、再利用性、テスト容易性、Blade連携（@can）
- 命名規則: モデル名 + Policy（Task → TaskPolicy）
- メソッド: view(), update(), delete() など

## プロンプト

```
Create a clean, modern educational diagram explaining "Laravel Policy for Authorization" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Before/After comparison showing code centralization
- Colors: Red for scattered code, Green for centralized Policy
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Policyで認可ロジックを集約" centered at top
Subtitle: "〜誰が何をできるかを一元管理〜"

## Layout
Left: Before (scattered checks in each method)
Right: After (centralized in Policy)

## Elements

### Before (red, scattered)
- show() に所有者チェック
- edit() に所有者チェック
- update() に所有者チェック
- destroy() に所有者チェック
- Label: ❌ 同じコードが重複

### After (green, centralized)
- TaskPolicy
  - view() { return $user->id === $task->user_id; }
  - update() { ... }
  - delete() { ... }
- Controller uses $this->authorize()
- Label: ✅ 1箇所で管理

### Benefits box
- コード集約
- 再利用可能
- @can でBlade連携

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                   Policyで認可ロジックを集約                         │
│                 〜誰が何をできるかを一元管理〜                        │
│                                                                     │
│   ❌ Before（コードが分散）           ✅ After（Policyに集約）       │
│                                                                     │
│   ┌─────────────────────┐           ┌─────────────────────┐        │
│   │ TaskController       │           │ TaskPolicy          │        │
│   │                     │           │                     │        │
│   │ show() {            │           │ view() {            │        │
│   │   if($task->user_id │           │   return $user->id  │        │
│   │     !== auth()->id) │           │     === $task->     │        │
│   │     abort(403);     │   ───→    │        user_id;     │        │
│   │ }                   │           │ }                   │        │
│   │                     │           │                     │        │
│   │ edit() {            │           │ update() { ... }    │        │
│   │   // 同じチェック    │           │                     │        │
│   │ }                   │           │ delete() { ... }    │        │
│   │                     │           │                     │        │
│   │ destroy() {         │           └─────────────────────┘        │
│   │   // 同じチェック    │                    ↓ 呼び出し             │
│   │ }                   │           ┌─────────────────────┐        │
│   └─────────────────────┘           │ $this->authorize()  │        │
│                                     │ @can('update', $task)│        │
│   同じコードが何度も...             └─────────────────────┘        │
│                                                                     │
│   【Policyのメリット】                                               │
│   ┌───────────────┬────────────────────────────────────┐           │
│   │ コード集約     │ 認可ロジックが1箇所にまとまる       │           │
│   │ 再利用性      │ 同じロジックを複数箇所で使える       │           │
│   │ Blade連携     │ @can で簡単に認可チェック           │           │
│   └───────────────┴────────────────────────────────────┘           │
│                                                                     │
│   ★ 「このユーザーはこのタスクを操作できるか」をPolicyで判定          │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Before/After comparison
- Show code duplication problem
- Show Policy centralizes authorization logic
- Include @can directive for Blade
```
