# 12-2-3_c1: プルリクエストワークフロー

## 対象Section
- Tutorial 12-2-3: プルリクエストの作成とレビュー
- 説明: プルリクエストの作成からマージまでの流れを示す概念図

## リサーチメモ
- Pull Request = ブランチの変更をマージするためのリクエスト
- base（マージ先）とcompare（マージ元）の関係
- レビュープロセス: Comment / Approve / Request changes
- 3つのマージ方法: Merge commit, Squash and merge, Rebase and merge
- LGTM = Looks Good To Me（承認の合図）
- Sources: [GitHub Docs](https://docs.github.com/en/pull-requests), [Hybesis Medium](https://medium.com/@urna.hybesis/pull-request-workflow-with-git-6-steps-guide-3858e30b5fa4)

## プロンプト

```
Create a clean, modern educational diagram explaining "Pull Request Workflow" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic showing PR lifecycle
- Colors: 4-color palette (blue for developer, orange for PR, green for approved/merge, red for request changes)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"プルリクエスト (Pull Request)" centered at top
Subtitle: "〜コードレビューとマージの仕組み〜"

## Layout
Two sections:
- Top: PR creation and review workflow
- Bottom: 3 merge methods comparison

## Elements

### PR Workflow
1. Developer A creates feature branch and pushes
2. Opens PR (base: main ← compare: feature)
3. Reviewer B reviews code
4. Review options: Comment / Approve / Request changes
5. If approved → Merge
6. If changes requested → Developer fixes → Re-review

### 3 Merge Methods
- Merge commit: Creates merge commit (non-linear)
- Squash and merge: Combines all commits into one
- Rebase and merge: Linear history

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                    プルリクエスト (Pull Request)                     │
│                    〜コードレビューとマージの仕組み〜                  │
│                                                                     │
│  【PRの流れ】                                                        │
│                                                                     │
│   開発者A                    GitHub                   レビュアーB    │
│      │                                                    │        │
│      │  ① feature ブランチで開発                           │        │
│      │                                                    │        │
│      │  ② PR作成 ──────────────────→ ┌────────────┐       │        │
│      │     base: main               │ Pull       │ ←───── │        │
│      │     compare: feature         │ Request    │   ③ レビュー    │
│      │                              └────────────┘        │        │
│      │                                    │               │        │
│      │                                    ▼               │        │
│      │                          ┌─────────────────┐       │        │
│      │                          │  レビュー結果   │       │        │
│      │                          ├─────────────────┤       │        │
│      │                          │ ✅ Approve     │────→ マージ可能│
│      │  ← フィードバック対応 ←── │ ❌ Request     │       │        │
│      │                          │    changes     │       │        │
│      │                          │ 💬 Comment    │       │        │
│      │                          └─────────────────┘       │        │
│      │                                                    │        │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【3つのマージ方法】                                                 │
│                                                                     │
│  ┌────────────────────┬────────────────────┬────────────────────┐ │
│  │   Merge commit     │  Squash and merge  │  Rebase and merge  │ │
│  ├────────────────────┼────────────────────┼────────────────────┤ │
│  │   A───B───M        │    A───B───C'      │    A───B───C───D   │ │
│  │       \   /        │   (全コミットを    │   (履歴が一直線)   │ │
│  │        C─┘         │    1つにまとめる)  │                    │ │
│  ├────────────────────┼────────────────────┼────────────────────┤ │
│  │ マージの履歴が残る  │ 履歴がシンプルに   │ 履歴が線形に       │ │
│  └────────────────────┴────────────────────┴────────────────────┘ │
│                                                                     │
│  ★ LGTM = Looks Good To Me（いいね！）= 承認の合図                  │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show PR as a bridge between developer and reviewer
- Include base/compare relationship
- Show 3 review options (Approve, Request changes, Comment)
- Compare 3 merge methods with visual commit diagrams
- Include LGTM as common review term
```

