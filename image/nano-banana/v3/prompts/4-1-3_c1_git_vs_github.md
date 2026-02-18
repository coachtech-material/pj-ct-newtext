# 4-1-3_c1: GitとGitHubの関係

## 対象Section
- Tutorial 4-1-3: GitHubとは
- 説明: GitとGitHubの関係を示す概念図

## リサーチメモ
- Git = 分散バージョン管理システム（ソフトウェア、ローカルで動作）
- GitHub = Gitリポジトリのホスティングサービス（Webサービス、クラウド）
- 他のホスティング: GitLab, Bitbucket など
- GitはGitHubなしでも使える（ローカルのみ）
- GitHubはGitを使ってアクセス（push/pull/clone）
- 図解パターン: 左右比較（ツール | サービス）が効果的
- Sources: [Git Documentation](https://git-scm.com/), [GitHub](https://github.com/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Git vs GitHub" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with minimal elements
- Colors: 3-color palette (orange for Git, blue for GitHub, green for connection)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"GitとGitHubの関係" centered at top
Subtitle: "〜ツールとサービスの違い〜"

## Elements
Left box - Git:
- Git logo (orange)
- Label "Git（ツール）"
- Sub-labels: "バージョン管理ソフトウェア", "自分のPCで動く", "無料"

Right box - GitHub:
- GitHub logo (blue/black)
- Label "GitHub（サービス）"
- Sub-labels: "Gitリポジトリのホスティング", "インターネット上で動く", "チーム共有"

Center - Connection:
- Green arrow connecting both
- Label "Gitを使ってGitHubにアクセス"

## Comparison table at bottom
| 項目 | Git | GitHub |
| 種類 | ソフトウェア | Webサービス |
| 場所 | 自分のPC | インターネット |
| 役割 | バージョン管理 | コード共有・公開 |

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      GitとGitHubの関係                              │
│                     〜ツールとサービスの違い〜                        │
│                                                                     │
│   ┌──────────────────┐              ┌──────────────────┐           │
│   │                  │              │                  │           │
│   │   🔶 Git         │    連携      │   🐙 GitHub      │           │
│   │  （ツール）       │ ──────────→ │  （サービス）     │           │
│   │                  │              │                  │           │
│   │ • バージョン管理   │              │ • リポジトリ公開  │           │
│   │   ソフトウェア    │              │   ホスティング    │           │
│   │ • 自分のPCで動く  │              │ • インターネット上│           │
│   │ • 無料           │              │ • チーム共有      │           │
│   └──────────────────┘              └──────────────────┘           │
│                                                                     │
│   ┌────────────────────────────────────────────────────┐           │
│   │   項目   │      Git       │      GitHub           │           │
│   │──────────│────────────────│───────────────────────│           │
│   │   種類   │ ソフトウェア    │ Webサービス           │           │
│   │   場所   │ 自分のPC       │ インターネット         │           │
│   │   役割   │ バージョン管理  │ コード共有・公開       │           │
│   └────────────────────────────────────────────────────┘           │
│                                                                     │
│   ★ Git = 道具、GitHub = その道具を使うための場所                    │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Clear visual distinction between Git (tool) and GitHub (service)
- Comparison table for easy understanding
- Simple metaphor: Git = tool, GitHub = platform to use the tool
```
