# 5-2-4_c1: ボックスモデル

## 対象Section
- Tutorial 5-2-4: ボックスモデル
- 説明: CSSボックスモデル（Content・Padding・Border・Margin）の概念図

## リサーチメモ
- 4層構造: Content（中身）→ Padding（内側余白）→ Border（枠線）→ Margin（外側余白）
- DevToolsでの表示色: Content=青、Padding=緑、Border=黄、Margin=オレンジ
- box-sizing: content-box（デフォルト）vs border-box（推奨）
- 図解パターン: 同心円的な入れ子構造が業界標準
- width/heightはデフォルトでContentのみに適用
- Sources: [W3Schools](https://www.w3schools.com/css/css_boxmodel.asp), [MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Styling_basics/Box_model), [web.dev](https://web.dev/learn/css/box-model)

## プロンプト

```
Create a clean, modern educational diagram explaining "CSS Box Model" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with nested boxes
- Colors: 4-color scheme (blue for content, green for padding, orange for border, gray for margin)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"CSSボックスモデル" centered at top
Subtitle: "〜すべての要素は箱でできている〜"

## Elements (nested boxes from outside to inside)
1. Margin (gray, outermost): "外側の余白（他の要素との距離）"
2. Border (orange): "枠線"
3. Padding (green): "内側の余白（緩衝材）"
4. Content (blue, center): "コンテンツ（中身）"

## Layout
Concentric rectangles showing the 4 layers

## Labels with metaphors
- Content: "箱の中身（テキスト、画像）"
- Padding: "箱の中の緩衝材"
- Border: "箱の外枠"
- Margin: "箱と箱の間隔"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      CSSボックスモデル                               │
│                  〜すべての要素は箱でできている〜                      │
│                                                                     │
│        ┌─────────────────────────────────────────────┐             │
│        │  Margin（外側の余白）                        │             │
│        │  ┌─────────────────────────────────────┐   │             │
│        │  │  Border（枠線）                      │   │             │
│        │  │  ┌───────────────────────────────┐ │   │             │
│        │  │  │  Padding（内側の余白）          │ │   │             │
│        │  │  │  ┌─────────────────────────┐ │ │   │             │
│        │  │  │  │                         │ │ │   │             │
│        │  │  │  │    Content（中身）       │ │ │   │             │
│        │  │  │  │   テキスト、画像など     │ │ │   │             │
│        │  │  │  │                         │ │ │   │             │
│        │  │  │  └─────────────────────────┘ │ │   │             │
│        │  │  │                               │ │   │             │
│        │  │  └───────────────────────────────┘ │   │             │
│        │  │                                     │   │             │
│        │  └─────────────────────────────────────┘   │             │
│        │                                             │             │
│        └─────────────────────────────────────────────┘             │
│                                                                     │
│   ┌────────────────────────────────────────────────────┐           │
│   │  Content  = 箱の中身（テキスト、画像）              │           │
│   │  Padding  = 箱の中の緩衝材（内側の余白）            │           │
│   │  Border   = 箱の外枠（枠線）                        │           │
│   │  Margin   = 箱と箱の間隔（外側の余白）              │           │
│   └────────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Clear nested box structure showing all 4 layers
- Each layer has distinct color
- Include legend explaining each layer with metaphors
- Center-focused design with labels
```
