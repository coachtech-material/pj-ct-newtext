# 13-3-3_c1: Issue駆動ワークフロー

## 対象Section
- Tutorial 13-3-3: Git/GitHub準備とIssue登録
- 説明: Issue駆動開発とPRベースの開発フローを示す概念図

## リサーチメモ
- Issue駆動開発: すべての作業をIssueとして管理
- 開発フロー: Issue確認 → ブランチ作成 → 実装 → コミット（#N） → PR作成（close #N） → マージ
- PRの説明欄に `close #1` でマージ時に自動クローズ
- コミットメッセージに `#1` でIssueと紐付け
- メリット: 作業の可視化、進捗追跡、履歴の記録
- Sources: [GitHub Docs](https://docs.github.com/en/issues), [GitHub Flow](https://docs.github.com/get-started/quickstart/github-flow)

## プロンプト

```
Create a clean, modern educational diagram explaining "Issue-Driven Development Workflow" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic showing cyclical workflow
- Colors: 4-color palette (blue for Issue, orange for branch/commit, green for PR, purple for merge)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Issue駆動開発の流れ" centered at top
Subtitle: "〜IssueからPRマージまで〜"

## Layout
Cyclical workflow diagram with GitHub icon in center

## Elements

### 7-Step Workflow
① Issueを確認する
② 作業用ブランチを作成する (feature/issue-1-xxx)
③ 実装する
④ コミットする (git commit -m "xxx #1")
⑤ プッシュする
⑥ PRを作成する (close #1)
⑦ PRをマージ → Issueが自動クローズ

### Key Points
- コミットメッセージに #1 → Issueと紐付け
- PRの説明欄に close #1 → マージ時に自動クローズ

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                       Issue駆動開発の流れ                            │
│                       〜IssueからPRマージまで〜                        │
│                                                                     │
│  【開発ワークフロー】                                                │
│                                                                     │
│  ① Issueを確認                                                       │
│     Issue #1: 「マイグレーション作成」                                │
│            │                                                        │
│            ▼                                                        │
│  ② ブランチ作成                                                      │
│     git switch -c feature/issue-1-migrations                        │
│            │                                                        │
│            ▼                                                        │
│  ③ 実装                                                              │
│     コードを書く                                                     │
│            │                                                        │
│            ▼                                                        │
│  ④ コミット                                                          │
│     git commit -m "マイグレーション作成 #1"  ← Issue紐付け            │
│            │                                                        │
│            ▼                                                        │
│  ⑤ プッシュ                                                          │
│     git push origin feature/issue-1-migrations                      │
│            │                                                        │
│            ▼                                                        │
│  ⑥ PR作成                                                            │
│     説明欄: close #1  ← 自動クローズキーワード                        │
│            │                                                        │
│            ▼                                                        │
│  ⑦ マージ                                                            │
│     → Issue #1 が自動的にクローズ ✅                                  │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【ポイント】                                                        │
│                                                                     │
│  ┌─────────────────────────┬─────────────────────────┐             │
│  │  コミットメッセージ     │  PRの説明欄             │             │
│  ├─────────────────────────┼─────────────────────────┤             │
│  │  xxx #1                 │  close #1               │             │
│  │  → Issueと紐付け       │  → マージ時に自動クローズ │             │
│  └─────────────────────────┴─────────────────────────┘             │
│                                                                     │
│  【自動クローズキーワード】                                          │
│  close #1 / closes #1 / fix #1 / fixes #1 / resolve #1              │
│                                                                     │
│  ★ Issueを先に登録 → 何をやるか明確 → 抜け漏れ防止                   │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show 7-step vertical workflow
- Highlight #1 in commit message (linking)
- Highlight "close #1" in PR description (auto-close)
- Include all auto-close keywords
- Emphasize: register Issues first, clear task management
```

