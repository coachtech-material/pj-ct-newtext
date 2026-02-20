# 6-1-1_c1: Dockerコンテナの概念

## 対象Section
- Tutorial 6-1-1: Dockerとは何か
- 説明: コンテナの概念（アプリ+環境をパッケージング）の概念図

## リサーチメモ
- Docker = クライアント-サーバーアーキテクチャ
- Image = 読み取り専用のテンプレート（設計図/クラス）
- Container = Imageから作成される実行中のインスタンス
- レイヤー構造: 各Dockerfile命令が1レイヤーを生成
- 主要コンポーネント: Client → Docker Daemon → Images/Containers/Registry
- 「Works on my machine」問題の解決が主なメリット
- Sources: [Spacelift](https://spacelift.io/blog/docker-architecture), [GeeksforGeeks](https://www.geeksforgeeks.org/devops/architecture-of-docker/), [LabEx](https://labex.io/questions/how-to-understand-docker-image-layers-148983)

## プロンプト

```
Create a clean, modern educational diagram explaining "Docker Container Concept" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with container visualization
- Colors: 3-color palette (blue for Docker, orange for app, green for environment)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Dockerコンテナの概念" centered at top
Subtitle: "〜アプリ+環境を丸ごとパッケージング〜"

## Elements
Container box containing:
- Application icon (orange)
- PHP/MySQL/Nginx icons (green)
- Linux base (blue)

Outside: Different machines (Mac, Windows, Linux server)

## Key message
"どこでも同じ環境で動く"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                     Dockerコンテナの概念                             │
│                  〜アプリ+環境を丸ごとパッケージング〜                 │
│                                                                     │
│                    ┌───────────────────────────┐                   │
│                    │     📦 コンテナ            │                   │
│                    │  ┌─────────────────────┐  │                   │
│                    │  │  🚀 アプリケーション  │  │                   │
│                    │  │    (Laravelなど)     │  │                   │
│                    │  └─────────────────────┘  │                   │
│                    │  ┌─────────────────────┐  │                   │
│                    │  │ PHP 8.1 + MySQL 8.0 │  │                   │
│                    │  │ + Nginx + 設定ファイル│  │                   │
│                    │  └─────────────────────┘  │                   │
│                    │  ┌─────────────────────┐  │                   │
│                    │  │     Linux OS        │  │                   │
│                    │  └─────────────────────┘  │                   │
│                    └───────────────────────────┘                   │
│                               │                                     │
│          ┌───────────────────┼───────────────────┐                 │
│          │                   │                   │                 │
│          ▼                   ▼                   ▼                 │
│     ┌─────────┐        ┌─────────┐        ┌─────────┐             │
│     │  🍎 Mac │        │ 🪟 Win  │        │ 🐧 Linux │             │
│     │  開発者A │        │ 開発者B │        │ 本番サーバー│             │
│     └─────────┘        └─────────┘        └─────────┘             │
│                                                                     │
│   ★ 「自分のPCでは動いたのに...」問題を解決！                        │
│   ★ どの環境でも全く同じように動作する                               │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show container as a package containing app + dependencies + OS
- Multiple target environments (Mac, Windows, Linux)
- Key message: same container works everywhere
- Solve "works on my machine" problem
```
