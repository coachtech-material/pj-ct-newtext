---
name: section-fix
description: 教材（curriculums/配下のMarkdown）の内容を修正・改善するときの標準ワークフロー。「Issue #NN を修正して」「Section 10-2-4 を直して」「この教材の誤りを直して」「レビュー指摘に対応して」などで必ず使う。対象ファイルと関連ガイドの読み込み → 修正方針の提示・承認 → ブランチ作成 → 修正 → コミット → PR作成（Closes #）までを一貫して案内する。教材本文・コード・手順・画像プレースホルダーを触る依頼なら、明示的に「ワークフロー」と言われなくても使うこと。
---

# 教材Section修正ワークフロー (section-fix)

このスキルは、教材（`curriculums/` 配下のMarkdown）を修正・加筆するときの進め方をまとめたものです。初学者向け教材なので、**既存の文体・構成を壊さないこと**と、**着手前にユーザーの承認を得ること**を最優先にします。

## なぜ承認を先に取るのか

教材は多くの受講生が読む公開物で、GitHub Actions 経由で LMS に同期されます。思い込みで直すと、正しい記述を壊したり、別Sectionとの前提がずれたりします。だから「何を・なぜ直すか」を先に共有し、合意してから手を動かします。

## 手順

### 1. 対象を特定する

- **Issue番号が渡された場合**: `gh issue view {番号}` で内容を確認する。
- **Issueにマイルストーンが紐づく場合**: `gh api repos/coachtech-material/pj-ct-newtext/milestones` でDescriptionを確認し、方針を把握する。
- **Section番号だけ渡された場合**: 命名規則 `{T}-{C}-{S}_{見出し名}.md` で `curriculums/` から対象ファイルを探す。

### 2. 対象ファイルと関連ガイドを読む

必ず本文を読んでから判断します。あわせて種別に応じたガイドを読みます。

| 読むもの | いつ |
|:--|:--|
| `.claude/CLAUDE.md` | 常に（プロジェクト全体のルール） |
| `guides/writing-rules.md` | 常に（文体・表現） |
| `guides/section-structure.md` | 通常Sectionのとき |
| `guides/handson-structure.md` | ハンズオンSectionのとき |
| `guides/verification.md` | 検証するとき |
| `quiz/` の対応ディレクトリ | そのSectionに確認問題があるとき |

### 3. 現状確認と修正方針の提示（承認を得る）

- 指摘事項ごとに現状を確認し、**すでに修正済みなら報告してスキップ**する。
- 修正が必要な項目について、具体的な修正方針（どこを・どう変えるか）をリストアップして提示する。
- → **ユーザーの承認を得る。承認前に本文を書き換えない。**

### 4. ブランチを準備する

最新の main から切ります。

```bash
git checkout main
git pull --ff-only origin main
```

- **マイルストーンあり**: `milestone/{マイルストーン名}` が無ければ作成、あればチェックアウト。
- **マイルストーンなし**: `git checkout -b fix/{Section番号}-{説明}`（例: `fix/10-2-4-middleware-handson`）。

### 5. 1Sectionずつ修正する

- 修正案を提示 → 承認 → 実行、を1Sectionずつ繰り返す。
- 文体は丁寧語、専門用語は言い換えを併記、絵文字・TIP/注意の記法は `.claude/CLAUDE.md` の規約に合わせる。
- 画像は `<img alt="{N}-{M}-{S}_{連番}.png" src="">`（`src` は空）。実ファイルは `image/` に置く。空の `src` は公開時に GitHub Actions が S3 URL へ自動置換する。
- コードブロックは必ず言語指定し、ファイルパスをコメントで明記する。

### 6. 検証する

- ハンズオンSectionを触った場合は `/verify-handson` で検証する。
- リンク・画像プレースホルダー・見出し番号の整合を確認する。

### 7. コミット → push → PR

```bash
git add {変更ファイル}
git commit -m "{Tutorial番号}: {修正内容の要約}

Co-Authored-By: Claude <noreply@anthropic.com>"
git push -u origin {ブランチ名}
gh pr create --base main --title "{要約}" --body "修正概要 ...

Closes #{Issue番号}"
```

- PR本文には修正概要を書き、Issue対応なら `Closes #{番号}` を必ず入れる。
- AIツールを使わず手動修正した場合は `Co-Authored-By` 行は不要。
- **main へ直接 push しない**。マージはレビューとCI通過後。

## 注意

- 既存の動作する記述・スターターキット使用部分を勝手に変えない。
- practice / sample の2プロジェクト構成は維持する。
- Tutorial間の依存（前Sectionの前提）に注意する。
