---
name: section-write
description: 新規Sectionの執筆ワークフロー（マイルストーンの章Issueベース）。「#276を執筆して」「13-1を書いて」「T13 Ch1を量産して」「次の章を書いて」など、新設Tutorial（T13/T14/T15等）のSectionを書き起こす依頼で必ず使う。既存Sectionの修正・Issue対応は section-fix を使う（棲み分け）。複数Sectionの量産はサブエージェント分担の量産ループで回す。
---

# 新規 Section 執筆ワークフロー (section-write)

マイルストーンに起票された**章 Issue**（節構成が本文に転記済み）を仕様として、新規 Section を執筆・検収するワークフローです。既存教材の修正は `section-fix`、様式が固まる前の試作は `style-lock` を使います。

## スコープの解釈

| 入力 | 対象 |
|:--|:--|
| `#276` / 「Issue 276」 | 章 Issue の全 Section（量産ループ） |
| `13-1`（章番号） | `gh issue list --milestone` で対応する章 Issue を特定し、その全 Section |
| `T13` / `13`（Tutorial番号） | Tutorial 全体。対応するマイルストーン（Stage 1 は `stage1-design-ai`）から配下の章 Issue を特定し、章順に量産ループで処理 |
| `13-1-2`（節番号） | Section 単体 |

## 1. ゲート検査（最初に）

1. **様式ロック**: 対象マイルストーンの様式ロック Issue（Stage 1 は #274）に「様式ロック完了」の進捗コメントがあるか確認する。未了なら停止して `style-lock` を案内する（パイロット自体の執筆は `style-lock` 経由のため免除）
2. **節構成**: 章 Issue 本文（`gh issue view <番号>`）に節構成があるか確認する。無ければ停止し、マイルストーン Description の仕様（構成確定版）とあわせてユーザーに確認する

## 2. 準備

1. `.claude/CLAUDE.md`・`guides/writing-rules.md` を Read する
2. **種別ガイドを選ぶ**（対象 Section の種別ごと）:

   | 対象 | 種別ガイド |
   |:--|:--|
   | T13 の概念・設計演習 Section | `guides/design-section-structure.md` |
   | T14 / T15 の概念・AI演習 Section | `guides/ai-exercise-structure.md` |
   | 従来型ハンズオン Section | `guides/handson-structure.md` |
   | 通常 Section | `guides/section-structure.md` |

   フェーズ別AIスタンス定型文の正本は `guides/ai-exercise-structure.md`。**T1〜T12 の P1・P2 のみ**で、各 Section へは**コピーして使う**（lint が正本一致を検査する）。**T13 以降では定型文を置かない**（P3・P4 は廃止済み）
3. 章 Issue の節構成・接続情報（`gh issue view <番号>`）と、マイルストーン Description が指す仕様を確認する
4. 前後 Section・接続先 Section（Issue の「接続」欄）と、**配布スターターアプリ**の実コードを確認する（過去 Tutorial のハンズオン成果物には依存しない）

## 3. 方針合わせ

執筆前に、対象 Section の見出し構成を提示して方向性を揃えます。

- 章 Issue の節構成どおりなら「節構成のとおり執筆します」と骨子（見出しレベルまで）を提示するだけでよい
- 節構成から外れる場合は理由を添えて提示し、**承認後に Issue へ変更をコメントしてから**執筆する
- 複数 Section の量産では、この提示は量産ループのランプラン承認（1回）に統合する

## 4. 執筆

- **単一 Section**: このセッションで執筆してよい。種別ガイドと執筆規律（`.claude/agents/section-writer.md` の「執筆規律」）に従う。quiz（`quiz/` の確認問題）はアイデア段階の試行のため**新規Sectionでは作成しない**
- **複数 Section（章 Issue 単位以上）**: `references/production-loop.md` を Read し、そのプロトコルで進める。量産ループのタスク単位は**1章**（1体の `section-writer` が章の全節を一括執筆する。ガイド・ブリーフの読み込みが章1回で済み、章内の用語・題材の一貫性も上がる）。メインセッションはオーケストレーションに徹し、執筆・セルフチェックは `section-writer`、検収は `independent-reviewer` に分担する（書き手と審査員の分離）

### サブエージェントへの渡し方

- **ファイルパスで渡す**: ガイド類・章 Issue の節構成（本文を貼る）・ブリーフ・前後 Section・AI臭チェック基準（`.claude/skills/section-write/references/ai-slop-curriculum.md`）はパスで渡し、サブエージェント自身に Read させる。ルールの要約をプロンプトに埋め込まない
- **完了報告は定型で受け取る**: `section-writer` の STATUS / FILES_CHANGED / REFERENCES_CONSULTED / SELF_CHECK / FIRST_TIME_SKILLS / SCORE / CONCERNS（章タスクでは FILES_CHANGED・SELF_CHECK・SCORE 等が節別に列挙される）。定型フィールド以外の自己申告は成果の根拠にしない
- **検収条件**: REFERENCES_CONSULTED に種別ガイドが含まれていない報告は不合格として差し戻す

## 5. セルフチェック・検収

1. **機械的検証**: `python3 .claude/scripts/lint_curriculum.py <対象>` — **新規ファイルは 🔴🟡 ともゼロ**（編集時 hook は 🔴 のみ通知するため、🟡 はここで必ず拾う）
2. **独立レビュー（予算を先に決める）**: `independent-reviewer` を**章まとめて1回**起動し、対象パス（章の全節）・章 Issue 番号・種別ガイドを渡して、**節別の指摘表**で返させる（単一 Section の執筆ではその Section だけを渡す）。REJECTED なら REMEDIATION に沿って一括修正する。**フル再レビューは最大1回**まで（構造級の指摘=説明の運び・節構成レベルがあった場合のみ）。それでも REJECTED ならユーザーにエスカレーションする。**軽微**（文言・表記）のみなら一括修正後に lint ＋変更差分の確認で通す。往復を減らす主役は lint なので、機械判定できる指摘が返ってきたら `lint_curriculum.py` にルールを足すことを検討する
3. **quizを作っていないこと**: quiz はアイデア段階の試行のため、新規 Section では作成しない（誤って作られていたら削除する）

## 6. 完了処理

- **コミットは検収後にのみ行う**: lint クリア＋レビュー APPROVED を確認してからコミットする。この規律により**「コミット済み＝検収済み」が進捗台帳になる**（専用の進捗ファイルは作らない）
- コミット単位は 1 Section（関連画像・図ソースを含む）。メッセージは `{節番号}: {要約}` ＋本文に `Refs #{章Issue番号}`
- **章完了時**: ①指摘を反映する ②章 Issue へ進捗コメント（Section ごとの検収結果の表）を残し、本文の完了条件チェックボックスを更新する。**Issue はクローズしない**（クローズは最終 PR の `Closes` で行う）
- **`learner-persona` の通読は Tutorial に1回**（章ごとには回さない）。章単位で回すと同じ指摘が繰り返し返り、往復だけが増えるため
- **横断的決定の前送り**: 執筆中に決めた用語・題材・表記は、ガイドの該当箇所へ反映する（ガイドに馴染まない一時的な話は章 Issue にコメント）
- **再開**: 中断後に同じスコープで再実行すると、`git log --oneline`（節番号で検索）と実ファイルの有無から未完タスクを再構成する。実ファイルがあるのに未コミットの Section は「残工程」（検収からやり直し）として扱う
- **完了主張は証拠の範囲まで**: 「完了」と報告してよいのは、この執筆パスで lint とレビュー判定を実際に確認した範囲だけ。サブエージェントの成功報告そのものは証拠にしない
