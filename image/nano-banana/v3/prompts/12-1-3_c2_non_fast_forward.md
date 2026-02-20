# 12-1-3_c2: Non-fast-forwardマージ

## 対象Section
- Tutorial 12-1-3: マージの基礎
- 説明: Non-fast-forwardマージとマージコミットの概念図

## リサーチメモ
- Non-fast-forward = マージ先に新しいコミットがある場合に発生
- マージコミット（M）が作成される
- 履歴が非線形になる（branch topology preserved）
- ブランチの境界が明確に残る
- --no-ff オプションで強制的にマージコミットを作成可能
- Sources: [Lei Mao's Blog](https://leimao.github.io/blog/Git-Fast-Forward-VS-Non-Fast-Forward/), [GitLab Docs](https://docs.gitlab.com/user/project/merge_requests/methods/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Git Non-Fast-Forward Merge" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design showing Before/After commit timeline with merge commit
- Colors: 4-color palette (blue for main branch, orange for feature branch, green for merge commit, gray for diverged commits)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Non-fast-forwardマージ" centered at top
Subtitle: "〜マージコミットが作成される〜"

## Layout
Before/After comparison showing the merge process with merge commit

## Elements

### Before (マージ前)
- main branch: A --- B --- E (diverged)
- feature branch: branches from B → C --- D

### After (マージ後)
- main branch: A --- B --- E --- M (merge commit)
- feature branch: C --- D merged into M

### Key Points
- mainに新しいコミットがある → マージコミット必要
- 履歴が非線形になる
- ブランチの境界が明確に残る

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                    Non-fast-forwardマージ                           │
│                   〜マージコミットが作成される〜                       │
│                                                                     │
│  【条件】mainに新しいコミットがある                                   │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【Before】マージ前                                                  │
│                                                                     │
│    A───B───E ← main（ここで別の変更が入った）                        │
│         \                                                           │
│          C───D ← feature                                            │
│                                                                     │
│        ★ mainとfeatureが「分岐」している                             │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【After】マージ後                                                   │
│                                                                     │
│    A───B───E───────M ← main（マージコミット）                        │
│         \         /                                                 │
│          C───D────                                                  │
│                                                                     │
│        ★ マージコミット（M）が作成される                              │
│        ★ 履歴が非線形になる                                          │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【--no-ff オプション】                                              │
│                                                                     │
│  $ git merge --no-ff feature/add-login                              │
│                                                                     │
│  → Fast-forward可能でも強制的にマージコミットを作成                   │
│  → マージの履歴が明確になる                                          │
│                                                                     │
│  ────────────────────────────────────────────────────────────────  │
│                                                                     │
│  【Fast-forward vs Non-fast-forward】                               │
│                                                                     │
│  ┌─────────────────────┬─────────────────────┐                     │
│  │   Fast-forward      │  Non-fast-forward   │                     │
│  ├─────────────────────┼─────────────────────┤                     │
│  │ マージコミットなし   │ マージコミットあり   │                     │
│  │ 線形の履歴          │ 非線形の履歴        │                     │
│  │ シンプル            │ 分岐が明確          │                     │
│  └─────────────────────┴─────────────────────┘                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show Before/After clearly
- Emphasize: main has new commits (diverged branches)
- Show merge commit (M) being created
- Include --no-ff option explanation
- Add comparison table with Fast-forward
```

