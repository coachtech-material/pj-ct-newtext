# 9-1-3: MVCアーキテクチャ（プロフェッショナル版）

## ASCIIアート構図

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         MVCアーキテクチャ                                 │
│                                                                         │
│                              ┌──────────┐                               │
│  ┌────┐      ┌────────┐     │Controller│                   ┌────────┐  │
│  │    │  →   │ Router │  →  │  (青)    │                   │   DB   │  │
│  │ 🖥️ │      │(オレンジ)│     └────┬─────┘                   │        │  │
│  │    │                      ↙     ↘                       │        │  │
│  └────┘               ┌──────┐     ┌──────┐                └────────┘  │
│  ブラウザ     ←        │ View │     │Model │        ↔       データベース  │
│                       │ (緑) │     │ (赤) │                            │
│                       └──────┘     └──────┘                            │
└─────────────────────────────────────────────────────────────────────────┘
```

## プロンプト本文

```
Create a professional, modern infographic explaining "MVC Architecture" for a programming tutorial.

## Style
- Aspect ratio: 16:9
- Resolution: 4K
- Background: Soft gradient from white to very light gray
- Design: Clean, modern, professional tech infographic
- Colors: Sophisticated color palette with gradient fills
- Typography: Clean sans-serif, bold labels
- Overall impression: Polished, corporate-quality diagram

## Title (Top Center)
"MVCアーキテクチャ" in bold, dark text
Subtitle: "Webアプリケーションの基本構造"

## Layout and Elements

【Left】Browser
- Modern, flat computer/monitor icon
- Label: "ブラウザ"

【Upper Left】Router
- Rounded rectangle with orange gradient fill
- Label: "Router"
- Subtle shadow for depth

【Upper Center - Largest】Controller
- Large ellipse with blue gradient fill (most prominent)
- Label: "Controller"
- This is the visual focal point

【Lower Left】View
- Ellipse with green gradient fill
- Label: "View"

【Lower Right】Model
- Ellipse with coral/salmon gradient fill
- Label: "Model"

【Right】Database
- Modern database cylinder icon (gray/silver)
- Label: "データベース"

## Arrows
- Smooth, curved arrows with slight gradient or shadow
- Clean arrowheads
- Flow: Browser → Router → Controller
- Controller ↔ View (bidirectional)
- Controller ↔ Model (bidirectional)
- Model ↔ Database (bidirectional)
- View → Browser (response)

## Important
- No direct connection between View and Model
- Controller is the central hub, visually dominant
- Professional, polished appearance
- Balanced whitespace
- No cluttered decorations
```
