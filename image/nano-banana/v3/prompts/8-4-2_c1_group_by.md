# 8-4-2_c1: 集計とグループ化

## 対象Section
- Tutorial 8-4-2: データの集計とグループ化
- 説明: GROUP BYによるデータのグループ化・集計の概念図

## リサーチメモ
- GROUP BY: 指定カラムで行をグループ化
- 集計関数: COUNT, SUM, AVG, MAX, MIN
- WHERE: グループ化前のフィルタリング
- HAVING: グループ化後のフィルタリング（集計関数と併用）
- 実行順序: FROM → WHERE → GROUP BY → HAVING → SELECT
- 図解パターン: 元データ → グループ化処理 → 集計結果のフロー
- Sources: [W3Schools](https://www.w3schools.com/sql/sql_groupby.asp), [MySQL Docs](https://dev.mysql.com/doc/refman/8.0/en/group-by-handling.html)

## プロンプト

```
Create a clean, modern educational diagram explaining "GROUP BY and Aggregation" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with data flow visualization
- Colors: 3-color palette (blue for original data, orange for grouping, green for result)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"GROUP BYによる集計" centered at top
Subtitle: "〜データをグループ化して要約〜"

## Elements
1. Original data (scattered records)
2. Grouping process (arrows gathering by key)
3. Aggregated result (COUNT, SUM, AVG)

## Flow
Raw data → GROUP BY user_id → COUNT per group

## Aggregate functions list
- COUNT: 件数
- SUM: 合計
- AVG: 平均
- MAX/MIN: 最大/最小

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                       GROUP BYによる集計                             │
│                     〜データをグループ化して要約〜                     │
│                                                                     │
│  【元データ: posts】                                                 │
│  ┌──────────────────┐                                              │
│  │ id │ user_id │   │     GROUP BY user_id                        │
│  │  1 │    1    │   │    ──────────────────→                       │
│  │  2 │    1    │   │         グループ化                            │
│  │  3 │    2    │   │                                              │
│  │  4 │    1    │   │                                              │
│  │  5 │    2    │   │                                              │
│  └──────────────────┘                                              │
│                                                                     │
│                     ↓ user_id でまとめる                            │
│                                                                     │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                                                               │ │
│  │   user_id = 1 のグループ         user_id = 2 のグループ        │ │
│  │  ┌─────────────────┐           ┌─────────────────┐           │ │
│  │  │ id: 1, 2, 4     │           │ id: 3, 5        │           │ │
│  │  │ → COUNT = 3     │           │ → COUNT = 2     │           │ │
│  │  └─────────────────┘           └─────────────────┘           │ │
│  │                                                               │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                     │
│                     ↓ 集計結果                                      │
│                                                                     │
│  【結果】                                                            │
│  ┌────────────────────────┐                                        │
│  │ user_id │ post_count   │     ┌─────────────────────────────┐  │
│  │    1    │      3       │     │ 集計関数                    │  │
│  │    2    │      2       │     │ COUNT: 件数  SUM: 合計     │  │
│  └────────────────────────┘     │ AVG: 平均   MAX/MIN: 最大最小│  │
│                                  └─────────────────────────────┘  │
│                                                                     │
│  ★ WHERE: グループ化「前」の絞り込み                                 │
│  ★ HAVING: グループ化「後」の絞り込み                                │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show data flow: original → grouped → aggregated
- Visualize grouping process clearly
- List common aggregate functions
- Mention WHERE vs HAVING difference
```
