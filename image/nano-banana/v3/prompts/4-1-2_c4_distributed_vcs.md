# 4-1-2_c4: 分散型バージョン管理システム

## 対象Section
- Tutorial 4-1-2: Gitとは
- 説明: 分散型バージョン管理システムの構造を示す概念図

## リサーチメモ
- 分散型（DVCS）: Git, Mercurial, Darcs など
- 構造: 各開発者がフルリポジトリ（全履歴）を持つ
- 中央サーバーは「便宜上」存在するが必須ではない
- メリット:
  - オフラインで作業可能
  - 高速（ほとんどの操作がローカル）
  - サーバー障害時も各自のリポジトリから復元可能
- 図解パターン: 各PCにリポジトリアイコン、メッシュ状に接続可能
- Sources: [Git公式ドキュメント](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control), [エンジニアブログ](https://scominc.co.jp/blog/2024/09/post-6.html)

## プロンプト

```
Create a clean, modern educational diagram explaining "Distributed Version Control System" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with minimal elements
- Colors: 3-color palette (green for local repos, blue for remote, orange for sync arrows)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"分散型バージョン管理システム" centered at top
Subtitle: "〜各自が完全なリポジトリを持つ〜"

## Layout
Each developer has their own repository, with optional central server

## Elements

### Developer PCs with Local Repos (green, left/right)
- 3 computer icons, each with a small cylinder (repository) icon
- Labels: "開発者A", "開発者B", "開発者C"
- Sub-label under each: "全履歴のコピー"

### Central Server (blue, center-top, optional)
- Server icon with "(便宜上の) リモートサーバー" label
- Dashed border to show it's optional

### Sync Arrows (orange)
- Arrows showing sync between local repos and remote
- Labels: "push/pull"

### Benefits box (green, bottom)
- Checkmark icon
- Text list:
  - "オフラインで作業可能"
  - "高速な動作"
  - "サーバー障害でも復元可能"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                   分散型バージョン管理システム                        │
│                   〜各自が完全なリポジトリを持つ〜                     │
│                                                                     │
│                    ┌ ─ ─ ─ ─ ─ ─ ─ ─ ┐                             │
│                      リモートサーバー                                │
│                    │    （GitHub等）   │                             │
│                          ┌───┐                                      │
│                    │     │ DB │        │                             │
│                          └───┘                                      │
│                    └ ─ ─ ─ ┬ ─ ─ ─ ─ ┘                             │
│                   push/pull │ push/pull                              │
│              ┌──────────────┼──────────────┐                        │
│              ↓              ↓              ↓                        │
│       ┌──────────┐   ┌──────────┐   ┌──────────┐                   │
│       │ 💻       │   │ 💻       │   │ 💻       │                   │
│       │ ┌───┐    │   │ ┌───┐    │   │ ┌───┐    │                   │
│       │ │ DB │   │   │ │ DB │   │   │ │ DB │   │                   │
│       │ └───┘    │   │ └───┘    │   │ └───┘    │                   │
│       │ 全履歴   │   │ 全履歴   │   │ 全履歴   │                   │
│       │ 開発者A  │   │ 開発者B  │   │ 開発者C  │                   │
│       └──────────┘   └──────────┘   └──────────┘                   │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ ✅ 分散型のメリット                                          │  │
│   │   • オフラインで作業可能（コミット、履歴確認）                  │  │
│   │   • 動作が高速（ほとんどの操作がローカル）                      │  │
│   │   • サーバー障害でも各自のリポジトリから復元可能                 │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│   ★ 各開発者が完全な履歴を持つ = バックアップが分散                  │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Each developer has complete repository (show cylinder icon on each PC)
- Central server shown with dashed border (optional)
- Emphasize offline capability and redundancy
- Keep consistent with Tutorial 4 flat design style
```
