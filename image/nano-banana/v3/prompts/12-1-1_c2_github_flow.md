# 12-1-1_c2: GitHub Flow

## 対象Section
- Tutorial 12-1-1: ブランチ戦略とは
- 説明: GitHub Flowのシンプルな2ブランチ構成を示す概念図

## リサーチメモ
- GitHub Flow = GitHubが提唱したシンプルなワークフロー
- 2種類のブランチのみ: main + feature
- mainは常にデプロイ可能な状態を維持
- Pull Request中心のワークフロー
- 継続的デプロイに最適
- Git Flowより圧倒的にシンプル
- Sources: [GitHub Docs](https://docs.github.com/en/get-started/using-github/github-flow), [AWS](https://docs.aws.amazon.com/prescriptive-guidance/latest/choosing-git-branch-approach/github-flow.html)

## プロンプト

```
Create a clean, modern educational diagram explaining "GitHub Flow Branching Strategy" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic showing simple branch timeline
- Colors: 3-color palette (dark blue for main, orange for feature, green for PR/merge)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"GitHub Flow" centered at top
Subtitle: "〜シンプルな2ブランチ戦略〜"

## Layout
Horizontal timeline showing main branch with feature branches and PR workflow

## Elements

### Branch Structure
1. main (dark blue) - Single horizontal line, always deployable
2. feature branches (orange) - Branch from main, merge back via PR

### Workflow Steps (numbered)
① Create branch from main
② Add commits
③ Open Pull Request
④ Review & discuss
⑤ Merge to main
⑥ Deploy

### Comparison with Git Flow
- Git Flow: 5ブランチ（複雑）
- GitHub Flow: 2ブランチ（シンプル）

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                          GitHub Flow                                │
│                      〜シンプルな2ブランチ戦略〜                      │
│                                                                     │
│  【ブランチの流れ】                                                  │
│                                                                     │
│         ① ブランチ作成   ② コミット追加    ③ PR作成                  │
│              ↓              ↓              ↓                       │
│  feature    ●──────────●────●────●────────●                        │
│             │                              │  ④ レビュー            │
│             │                              │  ⑤ マージ              │
│  main   ────●──────────────────────────────●────────→ ⑥ デプロイ   │
│                                                                     │
│                                                                     │
│  【複数の feature ブランチが並行して進む】                             │
│                                                                     │
│  feature/A  ●────────●────●─────────────────●                      │
│             │                               │                       │
│  feature/B      ●────────●────●─────────────────●                  │
│                 │                               │                   │
│  main   ────●───●───────────────────────────●───●────────────→     │
│             ↑   ↑                           ↑   ↑                   │
│           分岐 分岐                        マージ マージ             │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【Git Flow との比較】                                               │
│                                                                     │
│  ┌─────────────────────────┬─────────────────────────┐             │
│  │      Git Flow           │     GitHub Flow          │             │
│  ├─────────────────────────┼─────────────────────────┤             │
│  │ 5種類のブランチ          │ 2種類のブランチ           │             │
│  │ main, develop, feature  │ main + feature のみ      │             │
│  │ release, hotfix         │                          │             │
│  ├─────────────────────────┼─────────────────────────┤             │
│  │ 複雑・大規模向け         │ シンプル・継続的デプロイ向け│             │
│  └─────────────────────────┴─────────────────────────┘             │
│                                                                     │
│  ★ mainは常にデプロイ可能な状態を維持                                 │
│  ★ Pull Requestでコードレビューを行う                                │
│  ★ 小規模〜中規模プロジェクトに最適                                   │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show simplicity: only main + feature branches
- Illustrate the 6-step workflow
- Show multiple feature branches running in parallel
- Include comparison table with Git Flow
- Emphasize PR-centric workflow
- main is always deployable
```

