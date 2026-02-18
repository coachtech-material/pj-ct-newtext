# 5-3-1_c1: レスポンシブデザイン

## 対象Section
- Tutorial 5-3-1: レスポンシブデザインとは
- 説明: PC↔モバイルのレイアウト変化を示す概念図

## リサーチメモ
- レスポンシブWebデザイン: 画面サイズに応じてレイアウトを変更
- Ethan Marcotte（2010年）が提唱、流動的グリッド+流動的画像+メディアクエリ
- モバイルファーストアプローチ: 小さい画面から設計し、min-widthで拡張
- メディアクエリ: @media (min-width: 768px) {} でブレークポイント設定
- 一般的なブレークポイント: 480px, 768px, 1024px
- 図解パターン: PC（横並び）↔ モバイル（縦積み）の比較が効果的
- Sources: [MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design), [W3Schools](https://www.w3schools.com/css/css_rwd_mediaqueries.asp)

## プロンプト

```
Create a clean, modern educational diagram explaining "Responsive Design" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with device mockups
- Colors: 3-color palette (blue for PC, orange for tablet, green for mobile)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"レスポンシブデザイン" centered at top
Subtitle: "〜画面サイズに応じて変わるレイアウト〜"

## Elements
Left: PC layout (wide, horizontal arrangement)
- Header, Main+Sidebar side by side, Footer

Right: Mobile layout (narrow, vertical stacking)
- Header, Main, Sidebar, Footer (all stacked)

Center: Arrow showing transformation

## Labels
- PC: "PC表示（横並び）"
- Mobile: "スマホ表示（縦積み）"
- Arrow: "@media で切り替え"

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                     レスポンシブデザイン                             │
│                〜画面サイズに応じて変わるレイアウト〜                  │
│                                                                     │
│     【PC表示】                              【スマホ表示】           │
│                                                                     │
│  ┌───────────────────┐                    ┌─────────┐              │
│  │      Header       │                    │ Header  │              │
│  ├─────────┬─────────┤      @media        ├─────────┤              │
│  │         │         │                    │         │              │
│  │  Main   │  Side   │  ─────────────→   │  Main   │              │
│  │         │         │    画面幅で         │         │              │
│  │         │         │    切り替え         ├─────────┤              │
│  ├─────────┴─────────┤                    │  Side   │              │
│  │      Footer       │                    ├─────────┤              │
│  └───────────────────┘                    │ Footer  │              │
│                                            └─────────┘              │
│                                                                     │
│      横並びレイアウト                        縦積みレイアウト         │
│      （サイドバーあり）                      （1カラム）             │
│                                                                     │
│   ★ 1つのHTMLで、CSSの@mediaを使って表示を切り替える                 │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Side-by-side comparison of PC and mobile layouts
- Show same content reorganized for different screen sizes
- Arrow indicating the transformation
- Mention @media query as the mechanism
```
