# 3-1_c1: ターミナル・シェル・カーネル

## 対象Section
- Tutorial 3-1: コマンドラインとは
- 説明: ターミナル・シェル・カーネルの関係を示す概念図

## リサーチメモ
- ターミナル = テキストベースのUIを提供するプログラム（端末エミュレータ）
- シェル = コマンドを解釈し、カーネルに伝えるインターフェース（bash, zsh等）
- カーネル = OSの核心部、ハードウェアを直接制御
- 標準的な図解: 垂直レイヤー構造（User → Terminal → Shell → Kernel → Hardware）
- ターミナルとシェルは別物（ターミナルは窓、シェルは通訳）
- Sources: [Wikipedia](https://en.wikipedia.org/wiki/Shell_(computing)), [DigitalOcean](https://www.digitalocean.com/community/tutorials/what-is-the-shell)

## プロンプト

```
Create a clean, modern educational diagram explaining "Terminal, Shell, and Kernel" relationship for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with layered structure
- Colors: 4-color palette (blue for terminal, orange for shell, green for kernel, gray for hardware)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"ターミナル・シェル・カーネルの関係" centered at top
Subtitle: "〜コマンドが実行されるまでの流れ〜"

## Elements (layered from top to bottom)
1. User: "ユーザー（あなた）"
2. Terminal (blue): "ターミナル（入力画面）"
3. Shell (orange): "シェル（通訳）"
4. Kernel (green): "カーネル（OS の核）"
5. Hardware (gray): "ハードウェア（CPU、メモリ）"

## Flow (arrows connecting layers)
User → Terminal → Shell → Kernel → Hardware

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                ターミナル・シェル・カーネルの関係                     │
│                  〜コマンドが実行されるまでの流れ〜                   │
│                                                                     │
│                        👤 ユーザー（あなた）                         │
│                              │                                      │
│                              ▼ コマンドを入力                       │
│                    ┌─────────────────────┐                         │
│                    │   ターミナル         │                         │
│                    │   （入力画面）        │                         │
│                    │   文字を表示する窓    │                         │
│                    └──────────┬──────────┘                         │
│                               │                                     │
│                               ▼ 入力を渡す                          │
│                    ┌─────────────────────┐                         │
│                    │     シェル           │                         │
│                    │    （通訳）          │                         │
│                    │  コマンドを解釈する   │                         │
│                    └──────────┬──────────┘                         │
│                               │                                     │
│                               ▼ 命令を伝える                        │
│                    ┌─────────────────────┐                         │
│                    │    カーネル          │                         │
│                    │   （OSの核）         │                         │
│                    │  ハードウェアを制御   │                         │
│                    └──────────┬──────────┘                         │
│                               │                                     │
│                               ▼ 実行                                │
│                    ┌─────────────────────┐                         │
│                    │   ハードウェア        │                         │
│                    │ （CPU、メモリ、HDD）  │                         │
│                    └─────────────────────┘                         │
│                                                                     │
│   ★ ターミナル = 画面（入出力装置）                                  │
│   ★ シェル = 通訳（コマンドを解釈）                                  │
│   ★ カーネル = OSの心臓部（ハードウェアを制御）                       │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Clear vertical layered structure
- Each layer has distinct color
- Arrows showing the flow from user to hardware
- Japanese labels explaining each component's role
```
