# 12-2-1_c1: イシュー駆動開発

## 対象Section
- Tutorial 12-2-1: イシュー駆動開発とは
- 説明: イシュー駆動開発の7ステップを示す概念図

## リサーチメモ
- Issue-Driven Development = すべての作業をIssueとして管理
- 7ステップ: Issue作成 → ブランチ作成 → 開発 → PR作成 → レビュー → マージ → クローズ
- キーワード: Closes #1, Fixes #1, Resolves #1 でIssueと紐付け
- ブランチ名にIssue番号を含める（例: feature/1-add-login）
- メリット: 作業の可視化、分担、進捗管理、履歴記録
- Sources: [GitHub Docs](https://docs.github.com/en/issues), [GitHub Flow](https://docs.github.com/get-started/quickstart/github-flow)

## プロンプト

```
Create a clean, modern educational diagram explaining "Issue-Driven Development" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic showing cyclical workflow
- Colors: 4-color palette (blue for Issue, orange for Branch/Dev, green for PR/Review, purple for Merge/Close)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"イシュー駆動開発" centered at top
Subtitle: "〜すべての作業をIssueで管理〜"

## Layout
Circular workflow diagram with 7 numbered steps

## Elements

### 7-Step Workflow (circular flow)
① イシュー作成 (Issue #1を作成)
② ブランチ作成 (feature/1-add-login)
③ 開発 (コミット: "Add login #1")
④ プルリクエスト作成
⑤ コードレビュー
⑥ マージ
⑦ イシュークローズ

### Benefits Box
- 作業の可視化
- 作業の分担
- 進捗管理
- 履歴の記録

### Linking Keywords
Closes #1, Fixes #1, Resolves #1

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                       イシュー駆動開発                               │
│                     〜すべての作業をIssueで管理〜                     │
│                                                                     │
│  【7ステップの流れ】                                                 │
│                                                                     │
│         ① イシュー作成                                               │
│            Issue #1                                                 │
│              │                                                      │
│              ▼                                                      │
│         ② ブランチ作成                                               │
│            feature/1-add-login                                      │
│              │                                                      │
│              ▼                                                      │
│         ③ 開発                                                       │
│            git commit -m "Add login #1"                             │
│              │                                                      │
│              ▼                                                      │
│         ④ プルリクエスト作成                                          │
│            Closes #1                                                │
│              │                                                      │
│              ▼                                                      │
│         ⑤ コードレビュー ←→ フィードバック対応                        │
│              │                                                      │
│              ▼                                                      │
│         ⑥ マージ                                                     │
│            main にマージ                                             │
│              │                                                      │
│              ▼                                                      │
│         ⑦ イシュークローズ                                           │
│            Issue #1 自動クローズ                                     │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【イシュー駆動開発のメリット】                                       │
│                                                                     │
│  ┌───────────────┬───────────────┬───────────────┬───────────────┐ │
│  │ 作業の可視化   │ 作業の分担    │ 進捗管理      │ 履歴の記録    │ │
│  │ 誰が何を      │ 担当者を      │ 状態を        │ なぜその変更を │ │
│  │ 作っているか  │ 割り当て      │ 管理できる    │ 行ったか記録  │ │
│  └───────────────┴───────────────┴───────────────┴───────────────┘ │
│                                                                     │
│  【紐付けキーワード】                                                │
│  Closes #1 / Fixes #1 / Resolves #1 → PRマージ時にIssueが自動クローズ│
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show 7 steps as a vertical flow
- Include Issue number in branch name and commit message
- Show "Closes #1" keyword for auto-closing
- Highlight 4 benefits of issue-driven development
- Emphasize traceability between Issue, Branch, Commit, and PR
```

