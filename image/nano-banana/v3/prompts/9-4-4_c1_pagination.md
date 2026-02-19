# 9-4-4_c1: ページネーションの実装

## 対象Section
- Tutorial 9-4-4: ページネーションの実装
- 説明: 大量のデータを分割表示する概念図

## リサーチメモ
- ページネーション = 大量のデータを複数のページに分割して表示する機能
- Googleの検索結果が身近な例（1ページ10件）
- 標準的な構成要素（Webでよく見る形式）:
  - 最初へ(<<) / 前へ(<) / ページ番号 / 次へ(>) / 最後へ(>>)
- 3つの状態: disabled（操作不可）、active（現在ページ）、通常
- 件数表示: 「全150件中 16〜30件を表示」

## プロンプト

```
Create a clean, modern educational diagram explaining "Pagination" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design showing pagination component anatomy
- Colors: Blue for active page, Gray for disabled, Black for normal
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"ページネーション" centered at top
Subtitle: "〜大量データをページ分割〜"

## Layout
Center: Large pagination component breakdown
Show each element with labels

## Elements

### Main: Pagination Navigation Bar
Show standard pagination with 5 components:
- [<<] 最初へ (gray/disabled on page 1)
- [<] 前へ (gray/disabled on page 1)
- [1] [2] [3] [4] [5] ... [10] ← page numbers
- [>] 次へ
- [>>] 最後へ

### Current Page Indicator
- Page 2 highlighted in blue (active state)
- Label: 現在のページ

### Status Display
- Above navigation: "全150件中 16〜30件を表示"

### State Legend (bottom)
- Blue box: 現在のページ (active)
- Gray box: 操作不可 (disabled)
- White box: 移動可能 (normal)

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                        ページネーション                              │
│                     〜大量データをページ分割〜                        │
│                                                                     │
│                                                                     │
│                    全150件中 16〜30件を表示                          │
│                                                                     │
│         ┌───────────────────────────────────────────┐               │
│         │ [<<] [<]  [1] [2] [3] [4] [5] ... [10] [>] [>>] │         │
│         └───────────────────────────────────────────┘               │
│              ↑    ↑      ↑                          ↑    ↑         │
│           最初へ 前へ   ページ番号                 次へ 最後へ       │
│                         ↑                                           │
│                    現在のページ                                      │
│                   （青くハイライト）                                 │
│                                                                     │
│   【3つの状態】                                                      │
│   ┌────────┬────────┬────────┐                                      │
│   │ 🔵青   │ ⚫灰色  │ ⚪白   │                                      │
│   │ active │disabled│ normal │                                      │
│   │現在ページ│操作不可│移動可能│                                      │
│   └────────┴────────┴────────┘                                      │
│                                                                     │
│   ★ ユーザーが「今どこにいるか」「全体の量」を把握できる              │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show standard pagination bar with all 5 navigation elements
- Highlight current page in different color (active state)
- Include "全○件中 ○〜○件を表示" status text
- Show 3 states: active, disabled, normal with legend
```
