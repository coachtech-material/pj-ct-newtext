# 4-1-2_c3: 集中型バージョン管理システム

## 対象Section
- Tutorial 4-1-2: Gitとは
- 説明: 集中型バージョン管理システムの構造を示す概念図

## リサーチメモ
- 集中型（CVCS）: CVS, Subversion, Perforce など
- 構造: 中央サーバー1つに全クライアントが接続（星形トポロジー）
- 特徴: 単一のリポジトリに全履歴を保存
- 問題点:
  - サーバーダウン時は誰も作業できない
  - サーバー破損時に履歴喪失のリスク
  - オフライン作業ができない
- 図解パターン: 中央にサーバー、周囲に複数のPC（開発者）を配置
- Sources: [Git公式ドキュメント](https://git-scm.com/book/en/v2/Getting-Started-About-Version-Control), [ramble](https://ramble.impl.co.jp/5948/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Centralized Version Control System" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with minimal elements
- Colors: 3-color palette (blue for server, gray for clients, red accent for problem)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"集中型バージョン管理システム" centered at top
Subtitle: "〜中央サーバーに全員が依存〜"

## Layout
Star topology: Central server in middle, 3 developer PCs around it

## Elements

### Central Server (blue, center)
- Large server/cylinder icon
- Label: "中央サーバー（リポジトリ）"
- Sub-label: "全ての履歴を保存"

### Developer PCs (gray, surrounding)
- 3 computer icons arranged around the server
- Labels: "開発者A", "開発者B", "開発者C"
- Each with arrow pointing to/from central server

### Arrows
- Bidirectional arrows from each PC to server
- Label on arrows: "接続必須"

### Problem callout (red accent, bottom)
- Warning icon
- Text: "サーバーがダウンすると全員が作業不可"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                   集中型バージョン管理システム                        │
│                    〜中央サーバーに全員が依存〜                       │
│                                                                     │
│                         ┌──────────┐                               │
│          開発者A         │          │         開発者B               │
│          💻 ←─────────→ │  中央    │ ←─────────→ 💻                │
│                         │ サーバー  │                               │
│                         │  📦      │                               │
│                         │ 全履歴   │                               │
│                         └────┬─────┘                               │
│                              │                                      │
│                              ↕                                      │
│                             💻                                      │
│                           開発者C                                   │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │ ⚠️ サーバーがダウンすると...                                  │  │
│   │   • 誰もコミットできない                                      │  │
│   │   • 履歴を確認できない                                        │  │
│   │   • 最悪の場合、全履歴が消失                                   │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│   ★ 全員が中央サーバーに接続しないと作業できない                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Star topology with central server
- Show dependency of all developers on single server
- Highlight single point of failure risk
- Keep consistent with Tutorial 4 flat design style
```
