# 9-4-7_c1: ソフトデリート（論理削除）

## 対象Section
- Tutorial 9-4-7: ソフトデリート（論理削除）の実装
- 説明: 物理削除とソフトデリートの違いを示す概念図

## リサーチメモ
- Webでよく使われる構図: before/after でテーブルの変化を見せる
- 物理削除（Hard Delete）: DELETE文でレコードが消える
- ソフトデリート（Soft Delete）: deleted_atカラムにタイムスタンプを記録
- 重要な違い:
  - 物理削除 → レコードが消える → 復元不可
  - ソフトデリート → レコードは残る → 復元可能
- 通常クエリではdeleted_at=NULLのみ取得（削除済みは見えない）
- 比較表形式がわかりやすい

## プロンプト

```
Create a clean, modern educational diagram comparing "Physical Delete vs Soft Delete" for programming beginners.

## Style
- Aspect ratio: 16:9
- Background: Clean white
- Design: Before/After table visualization with 2-column comparison
- Colors: Red for physical delete, Blue for soft delete
- Typography: Sans-serif, bold labels in Japanese
- No decorations, no characters, no comic elements

## Title
"物理削除 vs ソフトデリート" centered at top
Subtitle: "〜削除の2つの方法〜"

## Layout
Top: Before state (same for both)
Bottom: After state (2 columns showing difference)

## Elements

### Before (shared)
Table with 3 records:
| id | name   | deleted_at |
| 1  | 山田   | NULL       |
| 2  | 佐藤   | NULL       | ← このレコードを削除
| 3  | 田中   | NULL       |

### After Left: 物理削除 (red)
DELETE: record id=2 disappears
Table with 2 records:
| id | name   | deleted_at |
| 1  | 山田   | NULL       |
| 3  | 田中   | NULL       |
Label: レコードが消える

### After Right: ソフトデリート (blue)
UPDATE: deleted_at gets timestamp
Table with 3 records:
| id | name   | deleted_at |
| 1  | 山田   | NULL       |
| 2  | 佐藤   | 2024-01-01 | ← 日時が入る
| 3  | 田中   | NULL       |
Label: レコードは残る

### Comparison box (bottom)
| 項目 | 物理削除 | ソフトデリート |
| 復元 | ❌ 不可 | ✅ 可能 |
| データ | 消える | 残る |

## ASCII構図イメージ
┌─────────────────────────────────────────────────────────────────────┐
│                   物理削除 vs ソフトデリート                         │
│                      〜削除の2つの方法〜                             │
│                                                                     │
│   【削除前】共通                                                     │
│   ┌────┬────────┬─────────────┐                                     │
│   │ id │  name  │ deleted_at  │   ← id=2 を削除する                │
│   ├────┼────────┼─────────────┤                                     │
│   │ 1  │ 山田   │    NULL     │                                     │
│   │ 2  │ 佐藤   │    NULL     │  ← 対象                            │
│   │ 3  │ 田中   │    NULL     │                                     │
│   └────┴────────┴─────────────┘                                     │
│              ↓                           ↓                          │
│   【物理削除】                    【ソフトデリート】                  │
│   ┌────┬────────┬───────────┐    ┌────┬────────┬─────────────┐     │
│   │ id │  name  │deleted_at │    │ id │  name  │ deleted_at  │     │
│   ├────┼────────┼───────────┤    ├────┼────────┼─────────────┤     │
│   │ 1  │ 山田   │   NULL    │    │ 1  │ 山田   │    NULL     │     │
│   │ 3  │ 田中   │   NULL    │    │ 2  │ 佐藤   │ 2024-01-01  │ ←!  │
│   └────┴────────┴───────────┘    │ 3  │ 田中   │    NULL     │     │
│     レコードが消える              └────┴────────┴─────────────┘     │
│                                    レコードは残る（日時が入る）      │
│                                                                     │
│   【比較】                                                           │
│   ┌──────────┬────────────┬────────────────┐                        │
│   │   項目   │  物理削除   │ ソフトデリート │                        │
│   ├──────────┼────────────┼────────────────┤                        │
│   │   復元   │  ❌ 不可   │    ✅ 可能    │                        │
│   │ データ   │   消える   │    残る       │                        │
│   └──────────┴────────────┴────────────────┘                        │
│                                                                     │
│   ★ ソフトデリート = deleted_atに日時を入れて「削除済み」とマーク    │
└─────────────────────────────────────────────────────────────────────┘

## Important
- Show BEFORE state (same for both methods)
- Show AFTER state side by side to compare difference
- Physical: record row disappears
- Soft: deleted_at column gets timestamp value
- Include comparison table with ❌/✅ icons
```
