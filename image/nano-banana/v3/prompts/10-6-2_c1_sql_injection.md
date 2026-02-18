# 10-6-2_c1: SQLインジェクション攻撃

## 対象Section
- Tutorial 10-6-2: SQLインジェクション対策
- 説明: SQLインジェクション攻撃の仕組みを示す概念図

## リサーチメモ
- OWASP Top 10の1位に位置する重大な脆弱性
- 攻撃者がSQLコードを入力として注入 → データベースが意図しないクエリを実行
- 教材の例: `admin' OR '1'='1` で全ユーザー取得、パスワードなしでログイン
- 対策: プリペアドステートメント（Eloquent/クエリビルダーは自動保護）
- Sources: [PortSwigger](https://portswigger.net/web-security/sql-injection), [ResearchGate](https://www.researchgate.net/figure/SQL-injection-attack-Flowchart_fig2_318601090)

## プロンプト

```
Create a clean, modern educational diagram explaining "SQL Injection Attack" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic showing vulnerable vs secure code comparison
- Colors: 3-color palette (red for dangerous/attack, green for safe/defense, blue for database)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"SQLインジェクション" centered at top
Subtitle: "〜データベースへの不正アクセス〜"

## Layout
Two-section layout:
- Top: Attack scenario (how it works)
- Bottom: Defense (prepared statements)

## Elements

### Attack Scenario
Show the flow:
1. Login form with username/password fields
2. Attacker enters: `admin' OR '1'='1`
3. Vulnerable SQL: `SELECT * FROM users WHERE username='admin' OR '1'='1'`
4. Database returns ALL users (attack succeeds)

### Defense
Show prepared statement:
1. SQL template: `SELECT * FROM users WHERE username = ?`
2. Data passed separately: `['admin\' OR \'1\'=\'1']`
3. Attack neutralized (special characters escaped)

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                       SQLインジェクション                            │
│                                                                     │
│                                                                     │
│        ❌ 危険                              ✅ 安全                 │
│                                                                     │
│   入力: admin' OR '1'='1             入力: admin' OR '1'='1        │
│           │                                   │                    │
│           ▼                                   ▼                    │
│   ┌───────────────┐                   ┌───────────────┐            │
│   │  SQL文に      │                   │  SQLとデータ  │            │
│   │  直接埋め込み  │                   │  を分離（?）  │            │
│   └───────┬───────┘                   └───────┬───────┘            │
│           ▼                                   ▼                    │
│   ┌───────────────┐                   ┌───────────────┐            │
│   │   Database    │                   │   Database    │            │
│   │  全データ漏洩  │                   │  0件（安全）  │            │
│   └───────────────┘                   └───────────────┘            │
│                                                                     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show the dangerous pattern (direct string concatenation) clearly
- Show how `' OR '1'='1` breaks the query logic
- Contrast with safe pattern (prepared statements)
- Emphasize that Eloquent/Query Builder auto-protects
- Use red for dangerous, green for safe
```
