# 8-1-1_c1: データベースとは何か

## 対象Section
- Tutorial 8-1-1: データベースとは何か
- 説明: データベースを「高機能なExcelシート」として示す概念図

## リサーチメモ
- データベース = 構造化されたデータの集合を効率的に管理するシステム
- DBMS (Database Management System) がデータの追加・検索・更新・削除を行う
- メリット: 大量データ対応、高速検索、同時アクセス、セキュリティ
- ACID特性: 原子性、一貫性、独立性、永続性
- Excelとの比較は初学者向け教育で一般的な説明手法
- 図解パターン: Before/After比較（Excel → Database の進化）
- Sources: [Oracle](https://www.oracle.com/database/what-is-database/), [IBM](https://www.ibm.com/topics/database)

## プロンプト

```
Create a clean, modern educational diagram explaining "What is a Database" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with comparison layout
- Colors: 3-color palette (blue for database, orange for Excel, green for advantages)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"データベースとは何か" centered at top
Subtitle: "〜高機能なExcelシート〜"

## Elements
Left side: Excel (simple spreadsheet)
- Label: "Excel（ファイル）"
- Simple table with rows and columns

Right side: Database (enhanced version)
- Label: "データベース"
- Similar table with extra features (search, security icons)

## Comparison Table
Show key differences:
- データ量: 数万行 → 数億行
- 検索: 手動フィルタ → SQL高速検索
- 同時アクセス: ファイル破損リスク → 安全に処理
- セキュリティ: ファイル単位 → 細かい権限

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                      データベースとは何か                            │
│                      〜高機能なExcelシート〜                          │
│                                                                     │
│     【Excel】                              【データベース】           │
│    ┌──────────────────┐               ┌──────────────────┐          │
│    │  id │ name │ age │               │  id │ name │ age │          │
│    │  1  │ 山田 │ 25  │     ──→      │  1  │ 山田 │ 25  │          │
│    │  2  │ 佐藤 │ 30  │    パワーUP   │  2  │ 佐藤 │ 30  │          │
│    └──────────────────┘               └──────────────────┘          │
│       シンプルな表                      ＋高速検索                    │
│                                        ＋同時アクセス                │
│                                        ＋セキュリティ                │
│                                                                     │
│    ┌────────────────────────────────────────────────────┐          │
│    │ 項目        │  Excel      │  データベース          │          │
│    │ データ量    │  数万行     │  数億行でも高速       │          │
│    │ 検索       │  手動        │  SQL（専門言語）      │          │
│    │ 同時アクセス │  破損リスク │  安全に処理           │          │
│    │ セキュリティ │  ファイル単位│  細かい権限設定       │          │
│    └────────────────────────────────────────────────────┘          │
│                                                                     │
│    ★ データベース = 「データを扱う」専門家                           │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show database as "powered-up Excel"
- Clear comparison table with advantages
- Emphasize scale (millions of rows), speed, safety
- Simple, approachable design for beginners
```
