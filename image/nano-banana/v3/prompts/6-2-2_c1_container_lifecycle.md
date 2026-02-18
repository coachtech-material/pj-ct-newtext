# 6-2-2_c1: コンテナのライフサイクル

## 対象Section
- Tutorial 6-2-2: Dockerの基本コマンド
- 説明: コンテナのライフサイクル（run/ps/stop/rm）の概念図

## リサーチメモ
- コンテナの5つの状態: Created → Running → Paused → Stopped → Deleted
- docker run = docker create + docker start（イメージ→実行中を一発）
- docker stop: SIGTERM送信 → graceful shutdown
- docker rm: 停止中のコンテナを削除（-f で強制削除）
- 遷移ルール: Running → Paused, Running → Stopped, Stopped → Deleted
- 図解パターン: 状態遷移図（state diagram）が業界標準
- Sources: [K21Academy](https://k21academy.com/kubernetes/docker-container-lifecycle-management/), [Last9](https://last9.io/blog/docker-container-lifecycle/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Docker Container Lifecycle" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with state diagram
- Colors: 4-color scheme (green for running, orange for stopped, blue for image, gray for removed)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"コンテナのライフサイクル" centered at top
Subtitle: "〜作成から削除までの流れ〜"

## Elements (states)
1. Image (blue): "イメージ"
2. Running (green): "実行中"
3. Stopped (orange): "停止中"
4. Removed (gray): "削除済み"

## Flow (commands as arrows)
- Image → Running: "docker run"
- Running → Stopped: "docker stop"
- Stopped → Running: "docker start"
- Stopped → Removed: "docker rm"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                    コンテナのライフサイクル                          │
│                     〜作成から削除までの流れ〜                        │
│                                                                     │
│   ┌──────────────┐                                                 │
│   │   🖼️ イメージ │                                                 │
│   │  （設計図）   │                                                 │
│   └──────┬───────┘                                                 │
│          │                                                          │
│          │ docker run                                               │
│          ▼                                                          │
│   ┌──────────────┐      docker stop      ┌──────────────┐          │
│   │              │ ──────────────────→  │              │          │
│   │  🟢 実行中   │                      │  🟠 停止中   │          │
│   │  (Running)  │ ←──────────────────  │  (Stopped)   │          │
│   │              │     docker start     │              │          │
│   └──────────────┘                      └──────┬───────┘          │
│          │                                      │                  │
│          │ docker ps で確認                     │ docker rm        │
│          │                                      ▼                  │
│          │                              ┌──────────────┐          │
│          │                              │  ⚫ 削除済み  │          │
│          │                              │  (Removed)   │          │
│          │                              └──────────────┘          │
│          │                                                         │
│   ┌──────────────────────────────────────────────────────┐        │
│   │ コマンド早見表                                        │        │
│   │ docker run    : イメージからコンテナを作成・実行      │        │
│   │ docker ps     : 実行中のコンテナを一覧表示            │        │
│   │ docker stop   : コンテナを停止                        │        │
│   │ docker rm     : 停止したコンテナを削除                │        │
│   └──────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show state transitions clearly
- Commands as arrow labels
- Include command reference table
- Color-coded states for easy identification
```
