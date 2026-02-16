# 6-2-3: Dockerfile→Image→Container（A3: 比喩シーン）

**Gem**: v4.1 | **テンプレート**: A3 | **ステータス**: テスト中

## プロンプト本文

```
Dockerの3つの中核概念の関係を、「たい焼き」の比喩を使って図解してください。

## 内容
- Dockerfile = レシピ・設計書
- Image = たい焼きの型（1つの型から何個でも作れる）
- Container = たい焼き（実際に食べられる＝動く実体）

## 描いてほしいもの
左から右への流れ:

1. 左側: 紙のレシピ/設計書のイラスト
   → ラベル「Dockerfile（設計書）」
   → 矢印に「docker build」

2. 中央: たい焼きの型のイラスト
   → ラベル「Image（たい焼きの型）」
   → 矢印に「docker run」

3. 右側: 3つのたい焼きのイラスト（それぞれ少し違う表情や中身）
   → ラベル「Container A」「Container B」「Container C」
   → 吹き出し「1つの型から何個でも作れる！」

各要素は手描き風のイラストで描き、温かみのあるタッチにする。
タイトル: 「Dockerfile・Image・Containerの関係」

## 概念の強調
- 「Dockerfile」「Image」「Container」の3つの技術用語を最も大きく太い文字で描く
- 比喩名（設計書、たい焼きの型等）はその下に小さく添える
- 「docker build」「docker run」のコマンド名も矢印上に目立つように描く
- たい焼きのイラストは概念を伝えるための補助。主役は3つの技術用語とその関係の矢印
```

## 構図イメージ（ASCIIアート）

```
┌──────────────────────────────────────────────────────────────┐
│          「Dockerfile・Image・Containerの関係」                │
│                                                               │
│   📄 Dockerfile    docker build    🔲 Image     docker run    │
│   (設計書)        ══════════▶     (たい焼きの型)  ═══════▶    │
│                                                               │
│                                              🐟 Container A   │
│                                              🐟 Container B   │
│                                              🐟 Container C   │
│                                                               │
│                                    💬「1つの型から             │
│                                       何個でも作れる！」       │
└──────────────────────────────────────────────────────────────┘
```

## 挿入情報

- ファイル: `curriculums/tutorial-6: 環境構築を楽にするdockerを学ぼう🐳/chapter-2: dockerの使い方/6-2-3_image_and_container_relationship.md`
- 挿入位置: 「たい焼きの型とたい焼き」の比喩説明の直後（L17付近）
- 画像ファイル名: `6-2-3_c1.png`

## 確認項目

- [ ] 技術用語のラベルが正確か（Dockerfile, Image, Container）
- [ ] フローの方向が左→右で、docker build → docker run の順序が正しいか
- [ ] 教材内の比喩・表現と一致しているか（設計書、たい焼きの型、たい焼き）
- [ ] Containerが複数（3つ）描かれ、「1つの型から複数作れる」ことが伝わるか
