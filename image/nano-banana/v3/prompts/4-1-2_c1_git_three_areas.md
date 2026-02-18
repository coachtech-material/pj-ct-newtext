# 4-1-2_c1: Gitの3つのエリア

## 対象Section
- Tutorial 4-1-2: Gitとは
- 説明: Gitの3つのエリア（ワーキングツリー・ステージ・リポジトリ）の概念図

## リサーチメモ
- Gitは3層アーキテクチャ（多くのVCSは2層）
- Working Tree: ファイルを編集する場所（scratch space）
- Staging Area (Index): 次のコミットに含める変更を選択（git add）
- Repository (.git): コミット履歴を保存（git commit）
- 標準的な図解: 3つのボックスを横並びにし、矢印でフローを示す
- Sources: [Git Official](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F), [Frontend Masters](https://frontendmasters.com/courses/git-in-depth/working-area-staging-area-repository/), [KodeKloud](https://kodekloud.com/blog/how-git-works/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Git's Three Areas" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with minimal elements
- Colors: 3-color palette (green for Working Tree, orange for Stage, blue for Repository)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Gitの3つのエリア" centered at top
Subtitle: "〜変更を記録するまでの3ステップ〜"

## Elements (3 boxes, left to right)
1. Working Tree (green): Large rounded rectangle, label "ワーキングツリー（作業場所）"
2. Stage (orange): Medium rounded rectangle, label "ステージ（準備エリア）"
3. Repository (blue): Large rounded rectangle with cylinder icon, label "リポジトリ（保管庫）"

## Flow (arrows with labels)
① Working Tree → Stage: "git add" (orange arrow)
② Stage → Repository: "git commit" (blue arrow)

## Sub-labels
- Working Tree: "ファイルを編集する場所"
- Stage: "コミットに含める変更を選ぶ"
- Repository: "変更履歴を保存"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                       Gitの3つのエリア                               │
│                   〜変更を記録するまでの3ステップ〜                    │
│                                                                     │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐     │
│   │              │      │              │      │              │     │
│   │ ワーキング    │  ①   │   ステージ    │  ②   │  リポジトリ   │     │
│   │  ツリー       │ ───→ │  （準備エリア）│ ───→ │  （保管庫）   │     │
│   │ （作業場所）   │      │              │      │              │     │
│   │              │ git  │              │ git  │    ┌───┐    │     │
│   │  📝 編集     │ add  │  📋 選択     │commit│    │ DB │    │     │
│   │              │      │              │      │    └───┘    │     │
│   └──────────────┘      └──────────────┘      └──────────────┘     │
│                                                                     │
│    ファイルを            コミットに含める        変更履歴を           │
│    編集する場所          変更を選ぶ            保存                  │
│                                                                     │
│   ★ 変更はすぐにリポジトリには入らない。ステージを経由する。           │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Three distinct colored boxes in horizontal layout
- Clear numbered arrows showing the flow
- Japanese labels must be readable
- Emphasize that changes go through Stage before Repository
```
