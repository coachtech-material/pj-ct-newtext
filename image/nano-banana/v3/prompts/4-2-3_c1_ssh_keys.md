# 4-2-3_c1: SSH公開鍵・秘密鍵

## 対象Section
- Tutorial 4-2-3: GitHubのセットアップ
- 説明: SSH公開鍵・秘密鍵の仕組みを示す概念図

## リサーチメモ
- 非対称暗号（公開鍵暗号）: 2つの鍵をペアで使用
- 秘密鍵: クライアント側で保持、絶対に外部に漏らさない
- 公開鍵: サーバー側に登録、共有しても問題なし
- 認証フロー: サーバーがチャレンジ送信 → クライアントが秘密鍵で署名 → サーバーが公開鍵で検証
- アルゴリズム: RSA, ECDSA, Ed25519 など
- 図解パターン: 左右（Client | Server）で双方向フローを表示
- Sources: [DigitalOcean](https://www.digitalocean.com/community/tutorials/understanding-the-ssh-encryption-and-connection-process), [Sectigo](https://www.sectigo.com/resource-library/what-is-an-ssh-key)

## プロンプト

```
Create a clean, modern educational diagram explaining "SSH Public and Private Keys" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with minimal elements
- Colors: 3-color palette (green for private key, blue for public key, orange for secure connection)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"SSH公開鍵・秘密鍵の仕組み" centered at top
Subtitle: "〜合い鍵でセキュアに接続〜"

## Elements
Left side - Your PC:
- Computer icon
- Key icon (green) labeled "秘密鍵（自分だけが持つ）"
- Note: "絶対に他人に見せない"

Right side - GitHub:
- GitHub/Server icon
- Key icon (blue) labeled "公開鍵（サーバーに登録）"
- Note: "見られてもOK"

Center - Connection process:
1. Your PC sends request with private key signature
2. GitHub verifies with matching public key
3. Secure connection established (orange lock icon)

## Metaphor
- Private key = 自分だけの印鑑
- Public key = 銀行に届け出た印影

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                   SSH公開鍵・秘密鍵の仕組み                          │
│                     〜合い鍵でセキュアに接続〜                        │
│                                                                     │
│      【自分のPC】                           【GitHub】              │
│                                                                     │
│   ┌──────────────┐                      ┌──────────────┐           │
│   │   💻         │                      │   🐙         │           │
│   │              │     ① 接続要求       │              │           │
│   │  🔑 秘密鍵   │  ─────────────────→  │  🔓 公開鍵   │           │
│   │ （自分だけ）  │                      │ （登録済み）  │           │
│   │              │  ←─────────────────  │              │           │
│   │  ⚠️ 絶対に   │     ② 照合OK        │  ✓ 見られて  │           │
│   │  見せない！  │                      │   もOK       │           │
│   └──────────────┘                      └──────────────┘           │
│                         🔒                                          │
│                    ③ 安全な接続確立                                 │
│                                                                     │
│   ┌────────────────────────────────────────────────────┐           │
│   │  秘密鍵 = 自分だけの印鑑（絶対に人に渡さない）        │           │
│   │  公開鍵 = 銀行に届けた印影（見られても問題なし）      │           │
│   │  → ペアで使うことで本人確認ができる                  │           │
│   └────────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Clear distinction: private key (secret) vs public key (shareable)
- Show the verification flow
- Include metaphor (stamp/seal analogy)
- Emphasize NEVER share private key
```
