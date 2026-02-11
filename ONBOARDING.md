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

---

## 作業の流れ

### 1. Issueの確認

GitHub Issuesで作業対象を確認し、自分にアサインします。

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

## 注意事項

- **mainに直接pushしない**（必ずPR経由）
- 修正前に**必ず対象ファイルを読む**（既存の文体・構成を理解してから修正する）
- practice / sample の2プロジェクト構成は維持する
- スターターキット使用部分は勝手に変更しない
- 不明点は必ず確認する（勝手な判断で修正しない）
