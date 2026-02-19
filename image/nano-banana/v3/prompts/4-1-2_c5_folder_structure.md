# 4-1-2_c5: Gitの3つのエリア（シンプル版）

## 対象Section
- Tutorial 4-1-2: Gitとは
- 説明: Gitの3つのエリアをシンプルに示す概念図

## リサーチメモ
- よく使われる図解: 3つのボックスを横並びにし、矢印でフローを示す
- シンプルさが重要: 情報量を最小限に
- コマンド（git add, git commit）を矢印上に配置
- 各エリアの役割は1行で簡潔に
- Sources: [サル先生のGit入門](https://backlog.com/ja/git-tutorial/intro/04/), [図解 Git](https://marklodato.github.io/visual-git-guide/index-ja.html)

## プロンプト

```
Create a clean, simple educational diagram explaining "Git's Three Areas" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Extremely simple flat design, minimal elements
- Colors: Green for Working Tree, Orange for Stage, Blue for Repository
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements, no extra details

## Title
"Gitの3つのエリア" centered at top

## Layout
3 boxes in a horizontal row, connected by 2 arrows
Very simple and clean

## Elements

### Three Boxes (equal size, rounded rectangles)
1. Left (green): "ワークツリー" with sub-label "編集する場所"
2. Center (orange): "ステージ" with sub-label "次のコミットを準備"
3. Right (blue): "リポジトリ" with sub-label "履歴を保存"

### Two Arrows
1. Green box → Orange box: "git add"
2. Orange box → Blue box: "git commit"

### Bottom summary (one line)
"★ 編集 → 選択 → 記録 の3ステップ"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                        Gitの3つのエリア                              │
│                                                                     │
│                                                                     │
│   ┌──────────────┐      ┌──────────────┐      ┌──────────────┐     │
│   │              │      │              │      │              │     │
│   │  ワークツリー │      │   ステージ   │      │  リポジトリ   │     │
│   │              │ git  │              │ git  │              │     │
│   │  編集する場所 │ add  │ 次のコミット │commit│  履歴を保存   │     │
│   │              │ ───→ │   を準備    │ ───→ │              │     │
│   │              │      │              │      │              │     │
│   └──────────────┘      └──────────────┘      └──────────────┘     │
│                                                                     │
│                                                                     │
│              ★ 編集 → 選択 → 記録 の3ステップ                        │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Keep it EXTREMELY simple - only 3 boxes and 2 arrows
- No folder structures, no file icons, no extra details
- Each box has only: area name + one-line description
- Consistent with Tutorial 4 flat design style
```
