# 4-3-5_c1: Gitファイルの4つの状態

## 対象Section
- Tutorial 4-3-5: ファイルの状態確認
- 説明: Gitファイルの4つの状態遷移を示す概念図

## リサーチメモ
- Gitファイルは4つの状態を循環: Untracked → Staged → Committed/Unmodified → Modified
- Untracked: Gitが追跡していない新規ファイル
- Staged: git add でステージングエリアに登録済み
- Committed/Unmodified: コミット済みで変更なし
- Modified: コミット後に編集された状態
- 図解パターン: サイクル図（循環矢印）が業界標準
- git status で現在の状態を確認
- Sources: [Git Documentation](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository)

## プロンプト

```
Create a clean, modern educational diagram explaining "Git File States" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with minimal elements
- Colors: 4-color scheme (red for Untracked, orange for Staged, blue for Unmodified, green for Modified)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Gitファイルの4つの状態" centered at top
Subtitle: "〜ファイルのライフサイクル〜"

## Elements (4 states as rounded rectangles)
1. Untracked (red): "未追跡（新規ファイル）"
2. Staged (orange): "ステージ済み（コミット準備OK）"
3. Unmodified (blue): "変更なし（コミット済み）"
4. Modified (green): "変更あり（編集済み）"

## Flow (arrows with command labels)
- Untracked → Staged: "git add"
- Staged → Unmodified: "git commit"
- Unmodified → Modified: "ファイルを編集"
- Modified → Staged: "git add"

## Layout
Circular flow showing the lifecycle

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                     Gitファイルの4つの状態                           │
│                      〜ファイルのライフサイクル〜                      │
│                                                                     │
│          ┌─────────────────┐      git add      ┌─────────────────┐ │
│          │                 │ ─────────────────→│                 │ │
│          │  🔴 Untracked   │                   │  🟠 Staged      │ │
│          │  （未追跡）      │                   │  （ステージ済み） │ │
│          │                 │                   │                 │ │
│          │  新規ファイル    │                   │  コミット準備OK  │ │
│          └─────────────────┘                   └────────┬────────┘ │
│                    ↑                                    │          │
│                    │                              git commit       │
│                    │                                    │          │
│                    │                                    ▼          │
│          ┌─────────┴───────┐                   ┌─────────────────┐ │
│          │                 │    ファイルを編集  │                 │ │
│          │  🟢 Modified    │ ←─────────────────│  🔵 Unmodified  │ │
│          │  （変更あり）    │                   │  （変更なし）    │ │
│          │                 │                   │                 │ │
│          │  編集済み       │      git add      │  コミット済み    │ │
│          │                 │ ─────────────────→│                 │ │
│          └─────────────────┘    (Staged経由)    └─────────────────┘ │
│                                                                     │
│   ★ 迷ったら git status で現在の状態を確認！                         │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show 4 distinct states with different colors
- Arrows showing transitions with git commands
- Lifecycle flows in a circular pattern
- Emphasize "git status" as the way to check current state
```
