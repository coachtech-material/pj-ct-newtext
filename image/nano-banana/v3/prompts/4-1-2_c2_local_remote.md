# 4-1-2_c2: ローカル/リモートリポジトリ

## 対象Section
- Tutorial 4-1-2: Gitとは
- 説明: ローカルリポジトリとリモートリポジトリの関係を示す概念図

## リサーチメモ
- ローカル = 自分のPCにあるリポジトリ
- リモート = サーバー上（GitHub等）にあるリポジトリ
- push: ローカルの変更をリモートにアップロード
- fetch: リモートの変更をローカルに取得（マージしない）
- pull: fetch + merge（リモートの変更を取り込む）
- 図解パターン: 左右分割（Local | Remote）で双方向矢印
- 初学者向けにはfetch省略し push/pull のみでOK
- Sources: [Git Documentation](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)

## プロンプト

```
Create a clean, modern educational diagram explaining "Local and Remote Repositories" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with minimal elements
- Colors: 3-color palette (green for local, blue for remote, orange for arrows)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"ローカルとリモートリポジトリ" centered at top
Subtitle: "〜自分のPCとクラウドの連携〜"

## Elements
Left side - Local:
- Computer icon with "自分のPC" label
- Cylinder icon labeled "ローカルリポジトリ"

Right side - Remote:
- Cloud icon with GitHub logo
- Cylinder icon labeled "リモートリポジトリ"
- Label "GitHub（クラウド）"

## Flow (bidirectional arrows)
① Local → Remote: "git push（アップロード）" (orange arrow, pointing right)
② Remote → Local: "git pull（ダウンロード）" (orange arrow, pointing left)

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                  ローカルとリモートリポジトリ                          │
│                    〜自分のPCとクラウドの連携〜                        │
│                                                                     │
│      【自分のPC】                           【GitHub（クラウド）】    │
│                                                                     │
│   ┌──────────────┐                      ┌──────────────┐           │
│   │   💻         │    git push          │    ☁️        │           │
│   │              │    （アップロード）    │              │           │
│   │  ┌───┐       │  ─────────────────→  │  ┌───┐       │           │
│   │  │ DB │      │                      │  │ DB │      │           │
│   │  └───┘       │  ←─────────────────  │  └───┘       │           │
│   │  ローカル     │    git pull          │  リモート     │           │
│   │  リポジトリ   │    （ダウンロード）    │  リポジトリ   │           │
│   └──────────────┘                      └──────────────┘           │
│                                                                     │
│   ★ push: 自分の変更をチームに共有                                   │
│   ★ pull: チームの変更を自分に取り込む                               │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Clear separation between local (left) and remote (right)
- Bidirectional arrows with Japanese labels
- Computer and cloud icons for visual distinction
- Emphasize push/pull as team collaboration mechanism
```
