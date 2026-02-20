# 9-6-1_c1: バリデーションの基礎

## 対象Section
- Tutorial 9-6-1: バリデーションの基礎
- 説明: バリデーション（入力検証）の概念図

## リサーチメモ
- バリデーション = ユーザー入力が正しい形式かチェックする処理
- 3つの役割: ユーザビリティ向上、サーバー負荷軽減、セキュリティ対策
- フロー: 入力 → チェック → OK:処理続行 / NG:エラー表示＆再入力
- よく使われる構図: フローチャート形式（分岐を明示）
- ルール例: required, email, min, max, unique
- エラー時は即座にフィードバック→修正を促進

## プロンプト

```
Create a clean, modern educational diagram explaining "Validation (Input Verification)" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flowchart style with clear branching
- Colors: Blue for input, Green for success, Red for error
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"バリデーション" centered at top
Subtitle: "〜入力データの検証〜"

## Layout
Flowchart: Input → Validation Check (diamond) → OK/NG branches

## Elements

### Start: User Input (blue)
- Form icon with fields
- Label: フォーム入力
- Example: name, email, password

### Decision: Validation Check (orange diamond)
- Diamond shape (decision point)
- Label: バリデーション
- Inside: ルール適用

### Branch 1: Success (green) - top path
- ✅ OK
- Arrow to: 処理を続行（データ保存）
- Green box

### Branch 2: Failure (red) - bottom path
- ❌ NG
- Arrow to: エラーメッセージ表示
- Arrow back to input (re-entry loop)
- Red box

### Rules Box (side)
- List of validation rules:
  - required（必須）
  - email（形式）
  - min:8（文字数）

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                        バリデーション                                │
│                      〜入力データの検証〜                            │
│                                                                     │
│                                                                     │
│   ┌────────────┐      ┌─────────┐      ┌─────────────┐            │
│   │            │      │  ／＼   │      │             │            │
│   │  フォーム  │ ──→ │＜ OK? ＞│ ──→ │  ✅ 処理続行 │            │
│   │    入力    │      │  ＼／   │ Yes │   データ保存 │            │
│   │            │      └────┬────┘      └─────────────┘            │
│   └────────────┘           │ No                                    │
│         ↑                  ↓                                       │
│         │           ┌─────────────┐                                │
│         │           │             │                                │
│         └─────────← │ ❌ エラー表示│                                │
│          再入力     │   修正を促す │                                │
│                     └─────────────┘                                │
│                                                                     │
│   【チェックルール】                                                 │
│   ┌─────────────┬───────────────────┬──────────────────┐           │
│   │   ルール    │      意味        │      例         │           │
│   ├─────────────┼───────────────────┼──────────────────┤           │
│   │ required    │ 必須             │ 空欄NG          │           │
│   │ email       │ メールアドレス形式│ abc@example.com │           │
│   │ min:8       │ 最小8文字        │ パスワード      │           │
│   │ max:255     │ 最大255文字      │ 名前            │           │
│   └─────────────┴───────────────────┴──────────────────┘           │
│                                                                     │
│   ★ 不正な入力はエラーで返し、正しい入力のみ通す                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Use flowchart with diamond decision shape
- Show two clear branches: OK (green) and NG (red)
- Include feedback loop (error → re-input)
- Display validation rules table with examples
```
