# 12-1-1_c1: Git Flow

## 対象Section
- Tutorial 12-1-1: ブランチ戦略とは
- 説明: Git Flowの5つのブランチタイプを示す概念図

## リサーチメモ
- Git Flow = Vincent Driessen氏が提唱した複雑なブランチモデル
- 5種類のブランチ: main, develop, feature, release, hotfix
- main: 本番環境（タグでバージョン管理）
- develop: 開発の統合ブランチ
- feature: 機能開発（develop から分岐、develop にマージ）
- release: リリース準備（develop → main）
- hotfix: 緊急修正（main から分岐、main と develop にマージ）
- Sources: [Atlassian](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow), [nvie](https://nvie.com/posts/a-successful-git-branching-model/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Git Flow Branching Strategy" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic showing branch timeline with horizontal flow
- Colors: 5-color palette (dark blue for main, green for develop, orange for feature, purple for release, red for hotfix)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Git Flow" centered at top
Subtitle: "〜5種類のブランチによる開発フロー〜"

## Layout
Horizontal timeline showing parallel branches with merge arrows

## Elements

### Branch Types (top to bottom)
1. hotfix (red) - Emerges from main, merges back to main AND develop
2. release (purple) - Emerges from develop, merges to main AND develop
3. main (dark blue) - Horizontal line at top, receives merges from release and hotfix
4. develop (green) - Horizontal line below main, integration branch
5. feature (orange) - Multiple branches from develop, merge back to develop

### Key Points Box
- main: 本番環境のコード
- develop: 開発の統合ブランチ
- feature: 機能開発用
- release: リリース準備用
- hotfix: 緊急修正用

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                            Git Flow                                 │
│                    〜5種類のブランチによる開発フロー〜                 │
│                                                                     │
│  【ブランチの流れ】                                                  │
│                                                                     │
│  hotfix ───────────●─────────────────────────────────●──────────── │
│                    │                                 │              │
│  main    ●─────────●─────────────────────────────────●──●───────── │
│          │         ↑                                 ↑  │           │
│          │         │                                 │  │           │
│          ↓         │  release ──────●────────────────●  │           │
│  develop ●─────────●─────────●──────●────────────────●──●───────── │
│          │         │         │      ↑                   │           │
│          │         │         │      │                   │           │
│  feature │    ●────●    ●────●──────●                   │           │
│          │    ↑    │    ↑    │                          │           │
│          └────┴────┴────┴────┘                          │           │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【5つのブランチの役割】                                             │
│                                                                     │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐          │
│  │  main    │ develop  │ feature  │ release  │ hotfix   │          │
│  │ (本番)   │ (開発統合) │ (機能開発) │ (リリース) │ (緊急修正) │          │
│  │ 青       │ 緑        │ オレンジ   │ 紫        │ 赤        │          │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘          │
│                                                                     │
│  ★ 大規模プロジェクト向け                                            │
│  ★ リリースサイクルが決まっているプロジェクトに最適                    │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show 5 branch types with distinct colors
- Illustrate the flow: feature → develop → release → main
- Show hotfix branching directly from main
- Use horizontal timeline layout (common Git Flow visualization)
- Include merge arrows showing where branches connect
- Label each branch with Japanese role description
```

