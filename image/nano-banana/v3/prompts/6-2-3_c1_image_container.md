# 6-2-3_c1: イメージとコンテナの関係

## 対象Section
- Tutorial 6-2-3: イメージとコンテナの関係
- 説明: たい焼きの型（イメージ）とたい焼き（コンテナ）の概念図

## リサーチメモ
- イメージ = 読み取り専用のテンプレート（レイヤー構造）
- コンテナ = イメージから作成された実行可能なインスタンス
- 1つのイメージから複数のコンテナを作成可能
- docker run でイメージからコンテナを起動
- 類似比喩: クラスとインスタンス、設計図と実体、型と成型物
- 図解パターン: 左に1つのイメージ、右に複数コンテナ、矢印で接続
- Sources: [Docker Documentation](https://docs.docker.com/get-started/), [Docker Hub](https://hub.docker.com/)

## プロンプト

```
Create a clean, modern educational diagram explaining "Docker Image and Container Relationship" using taiyaki (fish-shaped cake) metaphor for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with metaphor visualization
- Colors: 3-color palette (blue for image/mold, orange for containers/taiyaki, green for variations)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"イメージとコンテナの関係" centered at top
Subtitle: "〜たい焼きの型とたい焼き〜"

## Elements
Left: Image (mold icon)
- Label: "イメージ（型）"
- "設計図・定義"

Right: Multiple containers (multiple taiyaki)
- Container 1: "コンテナA"
- Container 2: "コンテナB"
- Container 3: "コンテナC"

Arrow from Image to Containers: "new" / "docker run"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                    イメージとコンテナの関係                          │
│                    〜たい焼きの型とたい焼き〜                         │
│                                                                     │
│      【イメージ】                      【コンテナ】                  │
│      （型・設計図）                    （実体）                      │
│                                                                     │
│   ┌──────────────────┐             ┌──────────────────┐           │
│   │                  │   docker   │   🐟 コンテナA    │           │
│   │   🔲 イメージ     │    run     │   （あんこ）      │           │
│   │                  │ ─────────→ ├──────────────────┤           │
│   │   nginx:latest  │             │   🐟 コンテナB    │           │
│   │                  │   1つの     │   （クリーム）    │           │
│   │  「こういう形の  │   型から    ├──────────────────┤           │
│   │   コンテナを    │   複数作成   │   🐟 コンテナC    │           │
│   │   作る」定義    │   できる！   │   （チョコ）      │           │
│   │                  │             │                  │           │
│   └──────────────────┘             └──────────────────┘           │
│                                                                     │
│   ┌────────────────────────────────────────────────────┐           │
│   │  イメージ = たい焼きの型                            │           │
│   │            設計図であり、それ自体は食べられない      │           │
│   │                                                    │           │
│   │  コンテナ = たい焼き                                │           │
│   │            型から作られた実体、それぞれ独立して動く  │           │
│   └────────────────────────────────────────────────────┘           │
│                                                                     │
│   ★ 1つのイメージから、複数の独立したコンテナを作成できる           │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Clear taiyaki metaphor (mold vs actual taiyaki)
- One image creates multiple containers
- Each container is independent
- Include legend explaining the metaphor
```
