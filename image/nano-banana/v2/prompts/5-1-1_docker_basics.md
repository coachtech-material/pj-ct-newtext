# 5-1-1: Docker基礎（Dockerfile・Image・Container）

## リサーチ結果

**検索キーワード**: Docker Dockerfile Image Container 図解 関係

**標準的な構図パターン**:
- 3段階の左→右フロー
- Dockerfile → docker build → Image → docker run → Container
- 設計図 → 型 → 実体 の比喩がよく使われる

**参考**: [Docker初心者がDockerfile,Image,Containerの関係を感覚的に理解する](https://cpptake.com/archives/491)

---

## プロンプト

```
DockerのDockerfile・Image・Containerの関係を図解してください。

## 構成要素（左から右へ3つ）
1. Dockerfile
   - 📄 テキストファイルのアイコン
   - 「設計図」
   - FROM, RUN, COPY などのコマンド例

2. Docker Image
   - 📦 パッケージまたはスナップショットのアイコン
   - 「型・テンプレート」
   - 読み取り専用

3. Docker Container
   - 🐳 コンテナまたは実行中のアイコン
   - 「実行環境」
   - 書き込み可能

## 矢印とコマンド
- Dockerfile → Image: 「docker build」
- Image → Container: 「docker run」
- 1つのImageから複数のContainerが作れることを示す（1対多）

## スタイル
- シンプルな技術図解
- 背景は白
- Docker公式カラー（青系）を使用
- 各要素のラベルは英語で大きく、日本語説明を小さく添える
```

## 構図イメージ

```
                docker build              docker run
              ─────────────→           ─────────────→   ┌──────────────┐
┌──────────────┐          ┌──────────────┐            │  Container A │
│  Dockerfile  │          │ Docker Image │ ─────────→ └──────────────┘
│              │          │              │            ┌──────────────┐
│  📄 設計図    │          │  📦 型       │ ─────────→ │  Container B │
│              │          │              │            └──────────────┘
│ FROM node    │          │  読み取り専用  │            ┌──────────────┐
│ RUN npm i    │          │              │ ─────────→ │  Container C │
└──────────────┘          └──────────────┘            └──────────────┘
                                                        🐳 実行環境
                                            「1つのImageから複数Container作成可能」
```

## 挿入情報

- ファイル: `curriculums/tutorial-5.../5-1-1_docker_basics.md`
- 画像ファイル名: `5-1-1_c1.png`
