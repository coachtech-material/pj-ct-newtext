# 9-1-3: MVCアーキテクチャ（v2スタイル改善版）

## プロンプト本文

```
Create a clean, modern infographic explaining the MVC Architecture for a programming tutorial.

## Layout & Style
- Aspect ratio: 16:9 horizontal
- Resolution: 4K
- Background: Soft gradient from light gray (#F5F5F5) to white
- Style: Flat design, Corporate Memphis meets Swiss Design
- Typography: Clean sans-serif, bold headings
- No legend, no watermarks, no extra annotations

## Title (Top Center)
"MVC Architecture" in large, bold, dark gray text
Subtitle: "Model-View-Controller Pattern" in smaller text below

## Components (5 Rounded Boxes)

1. USER (Left side)
   - Light blue (#E3F2FD) rounded box
   - Computer/browser icon
   - Label: "USER" in bold

2. ROUTING (Top)
   - Orange (#FF9800) rounded box
   - Label: "ROUTING" in bold white text
   - Sublabel: "web.php" in smaller text

3. CONTROLLER (Center, largest)
   - Blue (#2196F3) rounded box, 1.5x larger than others
   - Label: "CONTROLLER" in bold white text
   - Sublabel: "司令塔 / UserController" in smaller text
   - This is the visual focal point

4. MODEL (Bottom right)
   - Green (#4CAF50) rounded box
   - Label: "MODEL" in bold white text
   - Sublabel: "データ処理 / User::all()"
   - Next to it: Database cylinder icon (#607D8B)

5. VIEW (Right)
   - Pink/Magenta (#E91E63) rounded box
   - Label: "VIEW" in bold white text
   - Sublabel: "表示 / index.blade.php"

## Data Flow (Numbered Arrows)
Draw smooth, curved arrows with circled numbers (①②③④⑤⑥⑦):
① USER → ROUTING (dark arrow)
② ROUTING → CONTROLLER
③ CONTROLLER → MODEL
④ MODEL ↔ DATABASE (bidirectional)
⑤ MODEL → CONTROLLER (return data)
⑥ CONTROLLER → VIEW
⑦ VIEW → USER (curved around back)

Arrows should be thick (3-4px), dark gray (#424242), with clear direction.

## Important Constraints
- NO direct connection between VIEW and MODEL
- CONTROLLER must be visually dominant (center, largest)
- Clean spacing between elements
- Modern, professional appearance
- No cluttered decorations or clip-art
- No legend box or explanatory text at bottom
```
