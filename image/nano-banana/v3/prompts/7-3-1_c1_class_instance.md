# 7-3-1_c1: クラスとインスタンス

## 対象Section
- Tutorial 7-3-1: クラスとインスタンスの基礎
- 説明: クラス（設計図）とインスタンス（実体）の関係を示す概念図

## リサーチメモ
- クラス = 設計図/テンプレート/型定義（それ自体は実体ではない）
- インスタンス = クラスから生成された実体（オブジェクト）
- UMLクラス図: 3分割ボックス（クラス名/属性/メソッド）
- 1つのクラスから複数のインスタンスを生成可能
- new演算子でインスタンス化
- 図解パターン: 左にクラス、右に複数インスタンス、矢印で接続
- Sources: [Lucidchart](https://www.lucidchart.com/pages/uml-class-diagram), [Visual Paradigm](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/uml-class-diagram-tutorial/), [Wikipedia](https://en.wikipedia.org/wiki/Class_diagram)

## プロンプト

```
Create a clean, modern educational diagram explaining "Class and Instance" using taiyaki metaphor for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with metaphor visualization
- Colors: 3-color palette (blue for class/blueprint, orange for instances, green for properties)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"クラスとインスタンス" centered at top
Subtitle: "〜設計図と実体の関係〜"

## Elements
Left: Class (blueprint)
- Label: "クラス（設計図）"
- "User class definition"

Right: Multiple instances
- Instance 1: $user1 (田中さん)
- Instance 2: $user2 (佐藤さん)

Arrow: "new" keyword creating instances

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      クラスとインスタンス                            │
│                      〜設計図と実体の関係〜                          │
│                                                                     │
│      【クラス】                        【インスタンス】              │
│      （設計図）                        （実体）                      │
│                                                                     │
│   ┌──────────────────┐             ┌──────────────────┐           │
│   │                  │             │   📦 $user1      │           │
│   │   📋 class User  │    new      │   名前: 田中     │           │
│   │   {              │ ─────────→ │   年齢: 25       │           │
│   │     $name;       │             └──────────────────┘           │
│   │     $age;        │                                             │
│   │                  │    new      ┌──────────────────┐           │
│   │     function     │ ─────────→ │   📦 $user2      │           │
│   │       greet()    │             │   名前: 佐藤     │           │
│   │   }              │             │   年齢: 30       │           │
│   │                  │             └──────────────────┘           │
│   │  「ユーザーとは  │                                             │
│   │   こういうもの」 │    new      ┌──────────────────┐           │
│   │   という定義     │ ─────────→ │   📦 $user3      │           │
│   │                  │             │   名前: 鈴木     │           │
│   └──────────────────┘             │   年齢: 22       │           │
│                                     └──────────────────┘           │
│                                                                     │
│   ┌────────────────────────────────────────────────────┐           │
│   │  クラス = 設計図（定義）、それ自体は実体ではない    │           │
│   │  インスタンス = 設計図から作られた実体              │           │
│   │  → 1つのクラスから複数のインスタンスを作成できる   │           │
│   └────────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show class as blueprint/definition
- Multiple instances from one class
- Each instance has different property values
- "new" keyword creates instances
```
