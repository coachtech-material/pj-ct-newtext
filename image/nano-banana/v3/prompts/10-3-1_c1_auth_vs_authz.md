# 10-3-1_c1: 認証 vs 認可

## 対象Section
- Tutorial 10-3-1: 認可とポリシーの基礎
- 説明: 認証（Authentication）vs 認可（Authorization）の概念図

## リサーチメモ
- 一般的な図解パターン: 2つの概念を左右 or 上下に並べて比較
- 空港のアナロジー: IDを見せる（認証）→ 搭乗券を見せる（認可）
- 認証は認可の前に行われる（sequential process）
- 教材の覚え方: 「あなたは誰ですか？」vs「あなたはこれをしても良いですか？」
- Sources: [Auth0](https://auth0.com/docs/get-started/identity-fundamentals/authentication-and-authorization), [IBM](https://www.ibm.com/think/topics/authentication-vs-authorization)

## プロンプト

```
Create a clean, modern educational diagram explaining "Authentication vs Authorization" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with two-column comparison
- Colors: 3-color palette (blue for authentication, green for authorization, gray for shared elements)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"認証と認可" centered at top
Subtitle: "〜「誰か」と「何ができるか」〜"

## Layout
Two-column comparison with flow showing sequential relationship:
- Left: Authentication (認証)
- Right: Authorization (認可)
- Arrow between them showing "first → then" relationship

## Elements

### Authentication (Left)
- Question: "あなたは誰ですか？"
- English: Authentication
- Icon: Key or ID card
- Methods: Login, Token verification
- Result: User identity established

### Authorization (Right)
- Question: "あなたはこれをしても良いですか？"
- English: Authorization
- Icon: Lock or permission badge
- Methods: Policy, Role-based access
- Result: Action permitted or denied

### Flow
Show: Authentication → Authorization (sequential, authentication first)

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                         認証と認可                                  │
│                                                                     │
│                                                                     │
│   ┌───────────────────┐             ┌───────────────────┐          │
│   │                   │             │                   │          │
│   │       認証        │ ─────────→  │       認可        │          │
│   │  Authentication   │             │  Authorization    │          │
│   │                   │             │                   │          │
│   ├───────────────────┤             ├───────────────────┤          │
│   │                   │             │                   │          │
│   │ 「誰ですか？」     │             │ 「許可されてる？」 │          │
│   │                   │             │                   │          │
│   │  → ユーザー特定   │             │  → 許可 or 拒否   │          │
│   │                   │             │                   │          │
│   └───────────────────┘             └───────────────────┘          │
│                                                                     │
│          ① まず認証                     ② 次に認可                 │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Clear two-column comparison layout
- Show sequential relationship: Authentication FIRST, then Authorization
- Include both Japanese and English terms
- Use concrete blog app example from textbook
- Emphasize the key questions: "Who?" vs "What can you do?"
```
