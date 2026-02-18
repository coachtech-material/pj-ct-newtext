# 9-5-3_c1: Eager Loading

## 対象Section
- Tutorial 9-5-3: Eager Loadingとレイジーローディング
- 説明: Lazy Loading vs Eager Loading（N+1問題）の概念図

## リサーチメモ
- N+1問題: N件の親エンティティに対して、各々の子を取得するとN+1回のクエリが発生
- 例: 5部門の従業員を取得 → 1(部門) + 5(各部門の従業員) = 6クエリ
- Eager Loading: 関連データを事前に一括取得（IN句やJOIN）
- パフォーマンス比較: 1000ユーザーで Eager 25-37ms vs N+1 1.8秒
- Laravel: with(), Django: select_related/prefetch_related, Hibernate: JOIN FETCH
- 可視化ツール: AppMap, Zipkin, Jaeger
- Sources: [Learn Enough](https://news.learnenough.com/eager-loading), [Baeldung](https://www.baeldung.com/spring-hibernate-n1-problem), [Laravel Daily](https://laraveldaily.com/lesson/eloquent-performance/n1-query-debugbar-eager-loading)

## プロンプト

```
Create a clean, modern educational diagram explaining "N+1 Problem and Eager Loading" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Flat design infographic with comparison layout
- Colors: 3-color palette (red for problem/lazy, green for solution/eager, blue for database)
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"Eager Loading" centered at top
Subtitle: "〜N+1問題を解決する〜"

## Elements
Two columns:

Left (Bad): Lazy Loading
- Post::all() → 1 query
- foreach → N queries for users
- Total: N+1 queries

Right (Good): Eager Loading
- Post::with('user')->get() → 2 queries
- foreach → no additional queries
- Total: 2 queries

## Visual representation
Show database being hit multiple times vs twice

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                         Eager Loading                               │
│                                                                     │
│   ❌ N+1問題                          ✅ Eager Loading               │
│                                                                     │
│   Post::all();                        Post::with('user')->get();    │
│                                                                     │
│   ┌──────────────────┐                ┌──────────────────┐         │
│   │ SELECT posts     │                │ SELECT posts     │         │
│   │ SELECT user(1)   │                │ SELECT users     │         │
│   │ SELECT user(2)   │                │   WHERE IN(1,2,3)│         │
│   │ SELECT user(3)   │                │                  │         │
│   │ ...              │                │                  │         │
│   └──────────────────┘                └──────────────────┘         │
│                                                                     │
│   N+1回のクエリ                        2回のクエリ                   │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Clear comparison: Lazy vs Eager
- Show query count difference dramatically
- Use red/green coloring for problem/solution
- Emphasize performance impact
```
