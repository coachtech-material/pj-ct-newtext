# 9-5-1: 1対多リレーション

## リサーチ結果

**検索キーワード**: one to many relationship database diagram 1対多

**標準的な構図パターン**:
- 2つのテーブルを並べる（親テーブル・子テーブル）
- 親テーブルの主キー(PK) → 子テーブルの外部キー(FK) を線で接続
- Crow's foot記法（カラスの足）で「多」側を示す
- または 1:N 表記

**例**: 顧客(Customers) 1 --- * 注文(Orders)

**参考**: [Miro - ER Diagram One-to-Many](https://miro.com/diagramming/er-diagram-one-to-many-relationship/), [ノベルティ - DBリレーション解説](https://noveltyinc.jp/media/db-relation_er)

---

## プロンプト

```
データベースの1対多リレーションシップを図解してください。

## 構成要素
左側: 親テーブル「customers」（顧客）
- id (PK) 🔑
- name
- email
- サンプルデータ: id=1 田中太郎, id=2 山田花子

右側: 子テーブル「orders」（注文）
- id (PK) 🔑
- customer_id (FK) → customersのidを参照
- product
- price
- サンプルデータ:
  - id=1, customer_id=1, ノートPC
  - id=2, customer_id=1, マウス
  - id=3, customer_id=2, キーボード

## 関係の表現
- customersのidとordersのcustomer_idを線で接続
- customers側に「1」、orders側に「多(N)」または Crow's foot 記号
- 「1人の顧客が複数の注文を持てる」と注釈

## スタイル
- シンプルなER図スタイル
- テーブルは角丸の四角形
- PKは黄色またはオレンジでハイライト
- FKは青でハイライト
- 背景は白
```

## 構図イメージ

```
  ┌─ customers ─────────────┐          ┌─ orders ────────────────────┐
  │ 🔑 id (PK)  │ name      │          │ 🔑 id (PK)  │ customer_id (FK)│ product │
  │─────────────┼───────────│          │─────────────┼─────────────────┼─────────│
  │  1          │ 田中太郎   │ ──1──┐   │  1          │  1              │ ノートPC │
  │  2          │ 山田花子   │      │   │  2          │  1              │ マウス   │
  └─────────────────────────┘      N   │  3          │  2              │ キーボード│
                                   └── └───────────────────────────────────────┘

                    「1人の顧客 → 複数の注文」
```

## 挿入情報

- ファイル: `curriculums/tutorial-9.../9-5-1_one_to_many.md`
- 画像ファイル名: `9-5-1_c1.png`
