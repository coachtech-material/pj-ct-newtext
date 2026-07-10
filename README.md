# COACHTECH 教材リポジトリ（pj-ct-newtext）

プログラミング初学者向けの学習教材（Markdown ファイル集）を管理するリポジトリです。ここに置かれた教材は、GitHub Actions を通じて COACHTECH の LMS（学習管理システム）へ公開されます。

このファイルは、リポジトリ全体を俯瞰するための「入口」です。細かい操作手順は、各所からリンクする詳細ドキュメントを参照してください。

## このリポジトリについて

| 項目 | 内容 |
|:--|:--|
| 何のリポジトリか | プログラミング初学者向け教材（Markdown ファイル集）。Tutorial 1〜13 で段階的に学べる構成です。 |
| 教材の対象読者 | プログラミング未経験・IT リテラシーが高くない学習者 |
| 教材が扱う技術 | Laravel / PHP を中心とした Web 開発 |
| リポジトリの仕組み | Markdown で執筆 → GitHub Actions（Node.js 20）で画像を S3 にアップロードし、教材を LMS の API へ同期 |

> このリポジトリを触るチームメンバー自身は、Git と Markdown の基本操作ができれば十分です。

## ディレクトリ構成

```
pj-ct-newtext/
├── README.md      ← このファイル（リポジトリの入口）
├── ONBOARDING.md  ← 新メンバー向けの詳しい作業手順
├── curriculums/   ← 教材本体。Tutorial / Chapter / Section の3階層（Markdown）
├── image/         ← 教材で使う画像。Actions が S3 へ上げて src を差し替える
├── quiz/          ← 各概念Sectionの確認問題（question.md）と模範解答（model-answer.md）
├── guides/        ← 執筆ガイドライン（文体・Section構成・検証・画像生成）
├── references/    ← 過去の執筆ガイドライン（参照用）
├── .github/       ← GitHub Actions・Issue テンプレート・CI スクリプト
├── .claude/       ← Claude Code 設定（CLAUDE.md・settings.json・skills）
└── local/         ← 個人用の作業スペース（gitignore 済み・共有されない）
```

教材ファイルは `curriculums/{tutorial}/{chapter}/{section}.md` の3階層で並びます。ファイル名は次の規則に従い、拡張子 `.md` を除いた文字列が、そのまま LMS 上の Section タイトルになります。

```
{Tutorial番号}-{Chapter番号}-{Section番号}_{見出し名}.md
例: 10-2-1_ミドルウェアとは.md
```

## 教材から LMS への公開フロー（最重要）

教材は自動では公開されません。ブランチと LMS 環境が次のように対応しており、**担当者が GitHub Actions を手動で実行**して反映します。

| ブランチ | 反映先の LMS |
|:--|:--|
| `main` | 本番（Production）LMS — 受講生が実際に見る環境 |
| `staging` | Staging（検証）LMS — 本番に出す前の確認用 |

> ⚠️ `main` と `staging` は自動同期されません。片方に加えた変更は、手動で PR / マージしてもう片方へ反映します（放置すると内容が食い違っていきます）。

### 4本のワークフロー

公開に関わる GitHub Actions は4本です。**すべて手動実行（`workflow_dispatch`）**で、Node.js 20 上で動きます。

| # | ワークフロー（Actions タブでの表示名） | 対象ブランチ | 役割 |
|:-:|:--|:--|:--|
| 1 | 画像リンクをS3 URLに置換（staging） | `staging` | `image/` の画像を S3 へアップロードし、本文の `src=""` を S3 の公開 URL に置き換える |
| 2 | 教材を登録・更新（staging） | `staging` | `curriculums/` を JSON 化して LMS API（`/deploy/sections/upsert`）へ送信し、**Staging LMS** に反映 |
| 3 | 画像リンクをS3 URLに置換（main） | `main` | 1 と同じ処理を `main` ブランチで実行 |
| 4 | 教材を登録・更新（main） | `main` | `curriculums/` を JSON 化して LMS API へ送信し、**本番 LMS** に反映 |

- スクリプトの実体: 画像置換 = `.github/scripts/replace-image-links.js` / 教材同期 = `.github/scripts/sync-curriculums.js`
- 画像は S3 の `s3://{S3_BUCKET}/curriculums/images/{ファイル名}` にアップロードされ、本文の `src` は `{S3_PUBLIC_BASE_URL}/curriculums/images/{ファイル名}` に書き換わります。
- 画像置換ワークフローは、変更があれば `chore/replace-image-links-{タイムスタンプ}` という新ブランチを作って push します（**PR は手動で作成**が必要です）。
- これらのワークフローは、管理者が GitHub 側に設定済みの Secrets / Variables（AWS 認証情報、S3 の設定、LMS API の URL・キー・ワークスペース ID）を使って動きます。新しく参加したメンバーがこれらの値を扱う必要はありません。

> ⚠️ 画像は本文に `<img alt="9-1-8_1.png" src="">` の形式で書き、実ファイルを `image/` に同じ名前で置いてください。`alt` が空、または `image/` に対応ファイルが無いと、画像置換ワークフローはエラーで失敗します。

### 全体像

```
[修正 PR] ──マージ──▶  staging ブランチ
                          │
                          ├─(1) 画像リンクをS3 URLに置換（staging）
                          │        └─ chore/replace-image-links-* を作成 → staging にマージ
                          │
                          └─(2) 教材を登録・更新（staging）
                                   └─▶ Staging LMS で表示を確認 ✅

              │ 問題なければ staging の内容を main へ反映（PR / マージ）
              ▼

                        main ブランチ
                          │
                          ├─(3) 画像リンクをS3 URLに置換（main）
                          │        └─ chore/replace-image-links-* を作成 → main にマージ
                          │
                          └─(4) 教材を登録・更新（main）
                                   └─▶ 本番 LMS で表示を確認 ✅
```

### 推奨手順（必ず staging で検証してから main へ）

1. 修正内容の PR を `staging` ブランチにマージします。
2. 「画像リンクをS3 URLに置換（staging）」を実行します。自動作成された `chore/replace-image-links-*` の PR を確認し、`staging` にマージします。
3. 「教材を登録・更新（staging）」を実行し、**Staging LMS** で表示を確認します。
4. 問題がなければ、`staging` の内容を `main` へ反映します（PR / マージ）。
5. 「画像リンクをS3 URLに置換（main）」を実行し、作成された `chore` PR を確認して `main` にマージします。
6. 「教材を登録・更新（main）」を実行し、**本番 LMS** で表示を確認します。

ワークフローの起動は、Actions タブ → 対象ワークフローを選択 →「Run workflow」→ ブランチを選んで実行、または `gh workflow run` です。**手順の詳細と実行ログの見方は、次のドキュメントを参照してください。**

- [.github/README.md](.github/README.md) — ワークフローの実行方法・実行結果の確認方法
- [ONBOARDING.md](ONBOARDING.md) — 参加後の作業の流れ全体

## 執筆・修正の進め方

詳しい手順は [ONBOARDING.md](ONBOARDING.md) にありますが、要点は次のとおりです。

- **`main` に直接 push しない**。変更は必ず PR 経由でマージします。
- **ブランチ命名**
  - マイルストーンに紐づく作業: `milestone/{マイルストーン名}`
  - 単発の Issue 修正: `fix/{Section番号}-{説明}`（例: `fix/10-2-4-middleware-handson`）
- **コミットメッセージ**は `{Tutorial番号}: {修正内容の要約}` の形式にします（例: `10-3-6: ハンズオン要件を追加`）。AI ツールを併用した場合は、末尾に `Co-Authored-By:` 行を添えます。
- 修正前に**対象ファイルと関連ガイドを必ず読み**、既存の文体・構成に合わせます。

修正タスクは GitHub の Issue で管理します。ラベルは次のとおりです。

| ラベル | 意味 |
|:--|:--|
| `bug` | 内容の誤り・不具合 |
| `improvement` | 要改善（内容に問題がある） |
| `handson` | ハンズオンSection関連 |
| `section` | 通常Section関連 |
| `slack-inquiry` | Slack からの問い合わせ |
| `教材について` | 教材内容に関する問い合わせ |
| `needs-clarification` | 情報不足・要確認 |
| `possibly-no-fix` | 前提誤認の可能性・要レビュー |

> マイルストーンは進行中のものだけを扱います。過去のマイルストーンはすべてクローズ済みです。最新の状況は、GitHub の「Issues」→「Milestones」ページで確認してください。

文体・Section 構成のルールは、[.claude/CLAUDE.md](.claude/CLAUDE.md) と `guides/` 配下のガイドにまとまっています（末尾のドキュメントリンク集を参照）。

## Claude Code ハーネス

このリポジトリは、Claude Code（Anthropic の CLI）で作業しやすいように設定されています。`.claude/` 配下に、プロジェクトのルールと、作業を型どおりに進めるための「スキル」が入っています。

| 構成要素 | 役割 |
|:--|:--|
| `.claude/CLAUDE.md` | プロジェクトのルール・構成。**最初に読むファイル**（起動時に自動で読み込まれます） |
| `.claude/settings.json` | チーム共有の権限設定（許可コマンドなど） |
| `.claude/skills/verify-handson` | ハンズオンSectionの要件・手順を検証するスキル |
| `.claude/skills/section-fix` | Issue / Section 修正ワークフローのスキル |
| `.claude/skills/lms-sync` | LMS への公開（同期）手順を案内するスキル |
| `.claude/skills/quiz-add` | 確認問題（`question.md` / `model-answer.md`）を追加するスキル |

> `settings.local.json` は個人用の設定で、`.gitignore` により共有されません。チームで共有したい権限は `settings.json` に書きます。

### 起動方法

```bash
# 初回のみ: Claude Code をインストール
npm install -g @anthropic-ai/claude-code

# リポジトリのルートで起動
cd pj-ct-newtext
claude
```

起動すると `.claude/CLAUDE.md` が自動で読み込まれ、ルールを理解した状態で作業できます。スキルは会話の内容に応じて自動で呼ばれるほか、`/verify-handson` のように `/スキル名` で明示的に呼び出せます。

例として、`Issue #129 を修正してください` と伝えると、ブランチ作成 → ファイル確認 → 修正案の提示 → 承認後の修正 → コミット → PR 作成までを、型どおりに進めます。

## ドキュメントリンク集

| ドキュメント | 内容 |
|:--|:--|
| [ONBOARDING.md](ONBOARDING.md) | 新メンバー向けの入門・作業手順の全体像 |
| [.claude/CLAUDE.md](.claude/CLAUDE.md) | プロジェクトのルール・構成（最初に読む） |
| [.github/README.md](.github/README.md) | GitHub Actions の実行方法・確認方法 |
| [guides/writing-rules.md](guides/writing-rules.md) | 文体・スタイルルール |
| [guides/section-structure.md](guides/section-structure.md) | 通常Section の構成ガイド |
| [guides/handson-structure.md](guides/handson-structure.md) | ハンズオンSection の構成ガイド |
| [guides/verification.md](guides/verification.md) | Section の検証ガイド |
| [guides/nano-banana-workflow.md](guides/nano-banana-workflow.md) | 概念図（ナノバナナ）の生成・挿入手順 |
| [quiz/README.md](quiz/README.md) | 確認問題・模範解答の作り方 |
| [.claude/skills/verify-handson/SKILL.md](.claude/skills/verify-handson/SKILL.md) | ハンズオン検証スキルの詳細 |
| [references/complete_writing_guidelines_v15.md](references/complete_writing_guidelines_v15.md) | 過去の執筆ガイドライン（参照用） |

---

丁寧語・読点多め・専門用語の言い換えが、教材とチームドキュメントに共通する文体です。詳しくは [guides/writing-rules.md](guides/writing-rules.md) を参照してください。
