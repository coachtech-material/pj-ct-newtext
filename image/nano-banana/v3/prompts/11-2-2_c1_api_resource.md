# 11-2-2_c1: APIリソース

## 対象Section
- Tutorial 11-2-2: API Resourcesの活用
- 説明: APIリソースによるレスポンス整形の概念図

## リサーチメモ
- API Resource = レスポンスの変換層（Transformation Layer）
- 生データ → 整形データへの変換
- 不要データ除外、フォーマット統一

## プロンプト

```
Create a clean, modern educational diagram explaining "API Resource" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design with before/after transformation
- Colors: 3-color (gray for raw, green for clean, orange for resource)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"API Resource" centered at top
Subtitle: "〜レスポンスを整形する〜"

## Layout
Left: Raw data (gray, messy)
Center: API Resource (transformation arrow)
Right: Clean data (green, organized)

## Elements
Before (gray box):
- id: 1
- user_id: 1 ← marked as "不要"
- title: "タスク"
- status: "pending"
- created_at: "2024-01-01T12:00:00.000000Z" ← marked as "長い"

After (green box):
- id: 1
- title: "タスク"
- status_label: "未着手" ← marked as "分かりやすく"
- date: "2024/01/01" ← marked as "整形"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                         API Resource                                │
│                    〜レスポンスを整形する〜                           │
│                                                                     │
│   ❌ そのまま返すと...              ✅ API Resourceで整形すると...    │
│                                                                     │
│   ┌──────────────────┐              ┌──────────────────┐           │
│   │ {                │              │ {                │           │
│   │   id: 1,         │              │   id: 1,         │           │
│   │   user_id: 1, ←削除             │   title: "タスク",│           │
│   │   title: "タスク",│              │   status: "未着手",│ ←変換    │
│   │   status: "pending",│           │   date: "2024/01/01"│ ←整形  │
│   │   created_at:    │              │ }                │           │
│   │     "2024-01-01  │              └──────────────────┘           │
│   │      T12:00:00   │                                              │
│   │      .000000Z"   │ ←長すぎる                                    │
│   │ }                │                                              │
│   └──────────────────┘                                              │
│                                                                     │
│   【変換内容】                                                       │
│   ┌────────────────┬────────────────┬────────────────┐             │
│   │     削除       │     変換       │     整形       │             │
│   │   user_id      │ pending→未着手 │ 日付を短く     │             │
│   └────────────────┴────────────────┴────────────────┘             │
│                                                                     │
│   ★ 不要なデータを削除、分かりやすい形式に変換して返す                 │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Use ❌/✅ icons for clear before/after distinction
- Show JSON format to make it realistic
- Highlight 3 types of transformation: 削除, 変換, 整形
- Make raw data look messy (long date), clean data look organized
```
