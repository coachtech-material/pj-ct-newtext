# オンボーディングガイド

このドキュメントは、教材修正チームに新しく参加するメンバー向けの入門ガイドです。

---

## 前提条件

- GitHub アカウントを持っていること
- Git の基本操作（clone, branch, commit, push, PR）ができること
- Markdown の基本的な記法を知っていること

---

## セットアップ

### 1. リポジトリのクローン

```bash
git clone https://github.com/coachtech-material/pj-ct-newtext.git
cd pj-ct-newtext
```

### 2. AIツールの準備（いずれかを選択）

#### Claude Code を使う場合

```bash
# Claude Code のインストール
npm install -g @anthropic-ai/claude-code

# プロジェクトディレクトリで起動
cd pj-ct-newtext
claude
```

起動すると `.claude/CLAUDE.md` が自動読み込みされ、プロジェクトのルール・構成を理解した状態で作業できます。

#### Cursor / 他のAIツールを使う場合

`.claude/CLAUDE.md` にプロジェクトのルール・構成がまとまっています。AIツールのコンテキストとしてこのファイルを読み込ませてください。

### 3. ガイドの確認

作業を始める前に、以下のガイドに目を通してください。

| ガイド | 内容 | いつ読むか |
|:-------|:-----|:-----------|
| `.claude/CLAUDE.md` | プロジェクト概要・ルール全体 | **最初に必ず読む** |
| `guides/writing-rules.md` | 文体・スタイルルール | **最初に必ず読む** |
| `guides/handson-structure.md` | ハンズオンSection構成 | ハンズオン修正時に読む |
| `guides/section-structure.md` | 通常Section構成 | 通常Section修正時に読む |
| `guides/verification.md` | 検証ガイド | 検証作業時に読む |
| `guides/nano-banana-workflow.md` | ナノバナナ画像生成ワークフロー | 概念図の生成・挿入時に読む |

---

## Issueとマイルストーンの使い方

教材の修正タスクは、すべてGitHub Issueで管理しています。修正箇所を見つけたらIssueを作成し、作業するときはIssueを自分にアサインしてから着手します。

### Issueの作成

修正が必要な箇所を見つけたら、Issueを作成してください。

1. リポジトリの「Issues」タブを開く
2. 「New issue」をクリック
3. 以下を記入して作成

| 項目 | 記入内容 | 例 |
|:-----|:---------|:---|
| Title | `Tutorial {番号} の修正` または具体的な内容 | `Tutorial 9-3-2 の修正` |
| 本文 | 修正が必要な箇所と理由 | 「手順3のコマンドが動作しない」 |
| Labels | 該当するラベルを選択 | `bug`, `handson`, `critical` 等 |
| Milestone | 該当するマイルストーンを選択（あれば） | `ハンズオン品質改善` |

### Issueの一覧と確認

リポジトリの「Issues」タブから一覧を確認できます。

**ラベルの意味:**

| ラベル | 意味 |
|:-------|:-----|
| `bug` | 内容の誤り・不具合 |
| `improvement` | 要改善: 内容に問題がある |
| `handson` | ハンズオンSection関連 |
| `section` | 通常Section関連 |

**フィルター例:**
- ラベルで絞り込み: `label:bug` で不具合Issueだけ表示
- マイルストーンで絞り込み: 特定の修正プロジェクトに関するIssueだけ表示

### Issueのアサインと着手

1. 作業するIssueを開く
2. 右サイドバーの「Assignees」で自分を選択
3. アサインしてからブランチを作成して作業開始

### Issueの閉じ方

PRの本文に `Closes #番号` を含めると、PRがマージされたときにIssueが自動で閉じられます。

```
Closes #129
```

### マイルストーンについて

マイルストーンは、関連するIssueをまとめて進捗を管理する機能です。

例えば「reviewer-feedback」というマイルストーンに関連Issue 13件を紐づけると、何件完了したかがパーセンテージで表示されます。

**現在のマイルストーン:**

| マイルストーン | 内容 |
|:---------------|:-----|
| `reviewer-feedback` | レビュアーのフィードバック対応（最優先） |
| `section-type-clarity` | 通常/ハンズオンSectionの区別を明確化 |
| `image-insertion` | 画像挿入・プレースホルダー整備 |
| `misc-checks` | その他の確認・磨き上げ |

```
📦 reviewer-feedback（3/13完了・23%）
  ├── ✅ Issue #139
  ├── ✅ Issue #140
  ├── ✅ Issue #141
  ├── ⬜ Issue #142
  ├── ⬜ Issue #143
  │   ...
  └── ⬜ Issue #151
```

**マイルストーンの確認方法:**
1. リポジトリの「Issues」タブを開く
2. 「Milestones」をクリック
3. 各マイルストーンの進捗と紐づいたIssueを確認できる

**Issueをマイルストーンに紐づける方法:**
- Issue作成時: 右サイドバーの「Milestone」から選択
- 既存のIssue: Issueを開いて右サイドバーの「Milestone」から選択

---

## 作業の流れ

### 1. Issueの確認

GitHub Issuesで作業対象を確認し、自分にアサインします（詳しくは上の「Issueとマイルストーンの使い方」を参照）。

### 2. ブランチの作成

```bash
git checkout main
git pull origin main
git checkout -b fix/{Section番号}-{説明}
```

例: `fix/10-2-4-middleware-handson`

### 3. ファイルの修正

1. 対象ファイルと関連ガイドを**必ず読む**
2. 修正内容を具体的にリストアップ
3. レビュー者に修正方針を共有（PRのdescriptionに記載）
4. 修正を実施

### 4. コミット

```bash
git add {変更ファイル}
git commit -m "{Tutorial番号}: {修正内容の要約}

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>"
```

> AIツールを使わずに手動修正した場合は、Co-Authored-By 行は不要です。

### 5. プルリクエストの作成

```bash
git push -u origin fix/{Section番号}-{説明}
```

GitHubでPRを作成し、以下を記載してください:

- 修正内容の概要
- 修正前後の比較（該当箇所のdiff）
- 動作確認が必要な場合はその旨

### 6. レビュー & マージ

- レビュー者のフィードバックに対応
- 承認後にマージ

### Claude Codeでの作業例

Claude Codeを使う場合、以下の一言でステップ2〜5が自動で実行されます。

```
> Issue #129 を修正してください
```

Claude Codeが自動で: ブランチ作成 → ファイル読み込み → 修正案を提示 → 承認後に修正 → コミット → PR作成まで一貫して行います。

---

## 教材構成の概要

```
curriculums/
└── tutorial-{N}: {タイトル}/
    └── chapter-{M}: {章タイトル}/
        └── {N}-{M}-{S}_{ファイル名}.md
```

- Tutorial 1〜13 で構成
- 各Chapterの最後にハンズオンSection（`_hands_on.md`）がある場合がある
- 画像は `image/` ディレクトリに `{N}-{M}-{S}_{連番}.png` 形式で配置

---

## よくある質問

### Q: どのファイルを修正すればいいですか？

GitHub Issuesに修正対象が記載されています。不明な場合はIssueのコメントで質問してください。

### Q: 修正ルールが分かりません

`.claude/CLAUDE.md` と `guides/` のガイドに詳しく記載されています。それでも不明な場合はチームメンバーに聞いてください。

### Q: Claude Code の `/verify-handson` コマンドとは？

ハンズオンSectionの検証を自動で行うClaude Codeのスキルです。Claude Codeのプロンプトで `/verify-handson` と入力すると実行されます。

### Q: mainに直接pushしてしまいました

管理者に連絡してください。ブランチ保護ルールが設定されていれば拒否されますが、設定前の場合はrevertが必要になる可能性があります。

---

## `local/` ディレクトリの活用

`local/` は `.gitignore` で除外されている個人用の作業スペースです。cloneした時点では存在しないので、必要に応じて作成してください。

```bash
mkdir -p local/memo local/log local/scratch
```

### 推奨構成

| ディレクトリ | 用途 | 例 |
|:-------------|:-----|:---|
| `local/memo/` | 外部からの入力を保存 | Notionの修正リスト、スプシのエクスポート |
| `local/log/` | 個人の作業ログ | セッション再開時にClaude Codeへ引き継ぎ |
| `local/scratch/` | 下書き・作業用 | 修正案の仮置き |

### 活用例: 修正リストからIssue起票

```bash
# 1. Notionの修正リストをlocal/memo/にコピペ保存
# 2. Claude Codeに整形・起票を依頼
claude
> local/memo/notion-fix-list.md を読んで、
> トラッキングIssueに整形して起票してください
```

---

## 注意事項

- **mainに直接pushしない**（必ずPR経由）
- 修正前に**必ず対象ファイルを読む**（既存の文体・構成を理解してから修正する）
- practice / sample の2プロジェクト構成は維持する
- スターターキット使用部分は勝手に変更しない
- 不明点は必ず確認する（勝手な判断で修正しない）
