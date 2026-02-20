# 6-2-4_c1: Docker Compose

## 対象Section
- Tutorial 6-2-4: Docker Composeの基礎
- 説明: 複数コンテナ連携（Web+PHP+DB）のDocker Compose概念図

## リサーチメモ
- Docker Compose: 複数コンテナをYAMLファイルで定義・管理
- docker-compose.yml で services, networks, volumes を宣言
- docker compose up -d: 全コンテナをバックグラウンドで起動
- docker compose down: 全コンテナ停止・削除
- 自動ネットワーク作成: サービス名でコンテナ間通信可能
- 典型的な構成: Web(Nginx) → App(PHP) → DB(MySQL)
- 図解パターン: YAMLファイル → 複数コンテナの接続図
- Sources: [Docker Docs](https://docs.docker.com/compose/), [Docker Hub](https://hub.docker.com/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Docker Compose" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with multi-container architecture
- Colors: 4-color scheme (blue for web, orange for app, green for db, gray for compose file)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Docker Compose" centered at top
Subtitle: "〜複数コンテナを一括管理〜"

## Elements
Three connected containers:
1. Web (blue): Nginx
2. App (orange): PHP
3. DB (green): MySQL

docker-compose.yml file icon on the side

## Commands
- "docker compose up" → starts all
- "docker compose down" → stops all

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                        Docker Compose                               │
│                      〜複数コンテナを一括管理〜                       │
│                                                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                     docker-compose.yml                       │  │
│   │   services:                                                  │  │
│   │     web:   ...                                               │  │
│   │     app:   ...                                               │  │
│   │     db:    ...                                               │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                               │                                     │
│               docker compose up -d                                  │
│                               ▼                                     │
│   ┌─────────────────────────────────────────────────────────────┐  │
│   │                                                              │  │
│   │  ┌──────────┐      ┌──────────┐      ┌──────────┐          │  │
│   │  │   Web    │      │   App    │      │    DB    │          │  │
│   │  │  Nginx   │ ───→ │   PHP    │ ───→ │  MySQL   │          │  │
│   │  │ (8080番) │      │          │      │          │          │  │
│   │  └──────────┘      └──────────┘      └──────────┘          │  │
│   │                                                              │  │
│   │       リクエスト受付    PHPコード実行    データ保存           │  │
│   │                                                              │  │
│   └─────────────────────────────────────────────────────────────┘  │
│                               │                                     │
│               docker compose down                                   │
│                               ▼                                     │
│                          全て停止                                   │
│                                                                     │
│   ★ 1つのコマンドで複数コンテナを起動・停止できる                    │
│   ★ コンテナ間のネットワークも自動設定                              │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show docker-compose.yml as the configuration source
- Three connected containers (web, app, db)
- Single command controls all containers
- Automatic networking between containers
```
