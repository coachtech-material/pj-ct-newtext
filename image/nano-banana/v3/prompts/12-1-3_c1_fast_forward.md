# 12-1-3_c1: Fast-forwardマージ

## 対象Section
- Tutorial 12-1-3: マージの基礎
- 説明: Fast-forwardマージの仕組みを示す概念図

## リサーチメモ
- Fast-forward = マージ先に新しいコミットがない場合に発生
- ブランチポインタを移動するだけ（マージコミット不要）
- 履歴が線形になる（linear history）
- シンプルだが、マージの痕跡が残らない
- Sources: [Atlassian](https://www.atlassian.com/git/tutorials/using-branches/git-merge), [Graphite](https://graphite.com/guides/git-fast-forward-merge)

## プロンプト

```
Create a clean, modern educational diagram explaining "Git Fast-Forward Merge" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design showing Before/After commit timeline
- Colors: 3-color palette (blue for main branch, orange for feature branch, green for merged result)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Fast-forwardマージ" centered at top
Subtitle: "〜ポインタを移動するだけ〜"

## Layout
Before/After comparison showing the merge process

## Elements

### Before (マージ前)
- main branch: A --- B (pointer at B)
- feature branch: branches from B → C --- D

### After (マージ後)
- main branch: A --- B --- C --- D (pointer moved to D)
- No merge commit created

### Key Points
- mainに新しいコミットがない → Fast-forward可能
- ポインタが移動するだけ（マージコミットなし）
- 履歴が線形になる

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      Fast-forwardマージ                             │
│                      〜ポインタを移動するだけ〜                        │
│                                                                     │
│  【条件】mainに新しいコミットがない                                   │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【Before】マージ前                                                  │
│                                                                     │
│          B ← main（ここで止まっている）                              │
│         /                                                           │
│    A───●                                                            │
│         \                                                           │
│          C───D ← feature                                            │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【After】マージ後                                                   │
│                                                                     │
│    A───B───C───D ← main（ポインタが移動しただけ）                    │
│                                                                     │
│        ★ マージコミットは作成されない                                 │
│        ★ 履歴が線形（linear）になる                                   │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【コマンド】                                                        │
│                                                                     │
│  $ git switch main                                                  │
│  $ git merge feature/add-login                                      │
│                                                                     │
│  実行結果: "Fast-forward" と表示される                               │
│                                                                     │
│  ★ ポイント: mainブランチのポインタがfeatureの先端に移動するだけ      │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show Before/After clearly
- Emphasize: main has no new commits (condition for fast-forward)
- Show pointer movement (no merge commit)
- Result is linear history
- Include command example from curriculum
```

