# 4-4-4_c1: git pull（fetch + merge）

## 対象Section
- Tutorial 4-4-4: 変更のダウンロード
- 説明: git pull（fetch + merge）の仕組みを示す概念図

## リサーチメモ
- git pull = git fetch + git merge（2つのコマンドを1つで実行）
- git fetch: リモートの変更をダウンロードするが、ワーキングディレクトリは変更しない（安全）
- git merge: ローカルブランチにfetchした変更を統合
- fetch → review → merge の2ステップワークフローがベストプラクティス
- --rebase オプションでマージコミットを避けられる
- 図解パターン: Remote → fetch → Local staging → merge → Working Dir
- Sources: [Atlassian](https://www.atlassian.com/git/tutorials/syncing/git-pull), [GitLab](https://about.gitlab.com/blog/git-pull-vs-git-fetch-whats-the-difference/)

## プロンプト

```
Create a clean, modern educational diagram explaining "git pull (fetch + merge)" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with minimal elements
- Colors: 3-color palette (green for local, blue for remote, orange for operations)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"git pull の仕組み" centered at top
Subtitle: "〜リモートの変更を取り込む〜"

## Elements
Top: Remote repository (blue cloud/cylinder)
Bottom: Local repository (green computer/cylinder)

## Flow (showing pull = fetch + merge)
Step 1 - git fetch:
- Arrow from Remote to Local (dotted)
- Label: "① git fetch（情報だけ取得）"
- Note: "まだファイルは変わらない"

Step 2 - git merge:
- Arrow within Local
- Label: "② git merge（統合）"
- Note: "ここでファイルが更新される"

Combined:
- Big arrow labeled "git pull = fetch + merge"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                        git pull の仕組み                            │
│                     〜リモートの変更を取り込む〜                       │
│                                                                     │
│                      【リモートリポジトリ】                          │
│                      ┌──────────────────┐                          │
│                      │   ☁️ GitHub      │                          │
│                      │   最新の変更あり  │                          │
│                      └────────┬─────────┘                          │
│                               │                                     │
│             ┌─────────────────┼─────────────────┐                  │
│             │                 │                 │                  │
│             │  git pull       │                 │                  │
│             │  (一発で実行)   │                 │                  │
│             │                 ▼                 │                  │
│             │       ① git fetch                │                  │
│             │       （情報だけ取得）             │                  │
│             │       ※ファイルは変わらない       │                  │
│             │                 │                 │                  │
│             │                 ▼                 │                  │
│             │       ② git merge                │                  │
│             │       （統合）                    │                  │
│             │       ※ここでファイルが更新       │                  │
│             │                 │                 │                  │
│             └─────────────────┼─────────────────┘                  │
│                               ▼                                     │
│                      【ローカルリポジトリ】                          │
│                      ┌──────────────────┐                          │
│                      │   💻 自分のPC    │                          │
│                      │   最新に更新完了  │                          │
│                      └──────────────────┘                          │
│                                                                     │
│   ★ 作業を始める前に git pull で最新の状態にする習慣を！              │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show that pull = fetch + merge (two-step process)
- Emphasize fetch doesn't change files, merge does
- Include habit tip: always pull before starting work
- Clear visual flow from remote to local
```
