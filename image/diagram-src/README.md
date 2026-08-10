# diagram-src — 教材掲載図のSVGソース

Mermaidに標準記法の図種がない図（ユースケース図・ワイヤーフレーム等）は、PNG画像として教材に掲載します。このディレクトリはそのPNGの**編集可能なソース（SVG）**の置き場です。

- ファイル名はPNGと同名（`{N}-{M}-{S}_{連番}.svg` → `image/{N}-{M}-{S}_{連番}.png`）
- 図を修正するときはSVGを編集し、下記コマンドで再書き出しする（PNGを直接編集しない）
- 規約の詳細は `guides/design-section-structure.md` の「教材に載せる図の作り方（執筆者向け）」を参照

## SVG→PNGの書き出し（要Chrome）

```bash
# リポジトリルートで実行。--window-size はSVGの width/height に合わせる
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --screenshot=image/13-2-2_1.png --window-size=920,560 --force-device-scale-factor=2 \
  --default-background-color=FFFFFFFF "file://$(pwd)/image/diagram-src/13-2-2_1.svg"
```

## ファイル一覧

| SVG | 出力PNG | サイズ | 内容 |
|:----|:--------|:-------|:-----|
| `13-2-2_1.svg` | `image/13-2-2_1.png` | 920×560 | ユースケース図の実例（図書館アプリ・アクター2） |
| `13-2-2_2.svg` | `image/13-2-2_2.png` | 760×520 | 🏃答え合わせ（9-4-9ブログシステム・アクター1） |
| `13-2-3_1.svg` | `image/13-2-3_1.png` | 920×560 | 📖模範解答（カフェのモバイルオーダーアプリ・アクター2） |
