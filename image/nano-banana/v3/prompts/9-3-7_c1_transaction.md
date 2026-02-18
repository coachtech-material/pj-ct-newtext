# 9-3-7_c1: トランザクション処理

## 対象Section
- Tutorial 9-3-7: トランザクション処理
- 説明: トランザクション（全部成功 or 全部失敗）の概念図

## リサーチメモ
- トランザクション: 複数の操作を「ひとまとまり」として扱う
- ACID特性: Atomicity（原子性）、Consistency（一貫性）、Isolation（独立性）、Durability（永続性）
- COMMIT: 全操作成功時に確定・保存
- ROLLBACK: 1つでも失敗したら全て取り消し
- 銀行送金が典型例（引き落とし + 入金のセット）
- Laravel: DB::transaction() または DB::beginTransaction()
- 図解パターン: 成功パス（COMMIT）vs 失敗パス（ROLLBACK）の分岐
- Sources: [MySQL Docs](https://dev.mysql.com/doc/refman/8.0/en/commit.html), [Laravel Docs](https://laravel.com/docs/database#database-transactions)

## プロンプト

```
Create a clean, modern educational diagram explaining "Database Transactions" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with success/failure comparison
- Colors: 3-color palette (blue for operations, green for success/commit, red for failure/rollback)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"トランザクション処理" centered at top
Subtitle: "〜全部成功か、全部失敗か〜"

## Elements
Bank transfer example:
1. Operation A: Aさんから1万円引き落とし
2. Operation B: Bさんに1万円入金

Two scenarios:
- Success path: Both succeed → COMMIT
- Failure path: One fails → ROLLBACK (all undone)

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      トランザクション処理                            │
│                                                                     │
│  【送金処理】  ① Aさんから引き落とし  ② Bさんに入金                  │
│                                                                     │
│          ↓                                      ↓                   │
│                                                                     │
│  ✅ 両方成功                           ❌ 途中で失敗                 │
│                                                                     │
│  ① 成功                               ① 成功                       │
│  ② 成功                               ② 失敗                       │
│          ↓                                      ↓                   │
│      COMMIT                               ROLLBACK                  │
│     （確定）                             （全取消）                  │
│          ↓                                      ↓                   │
│  Aさん: -1万円                          Aさん: 元通り                │
│  Bさん: +1万円                          Bさん: 元通り                │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Use bank transfer as concrete example
- Show two paths: success (commit) and failure (rollback)
- Emphasize "all or nothing" principle
- Show that rollback prevents data inconsistency
```
