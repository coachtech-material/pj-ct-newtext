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

#### 利用できるスキル（Claude Code）

Claude Code には、このプロジェクト専用の「スキル」（あらかじめ用意された作業手順のまとまり）が登録されています。プロンプトでスラッシュコマンドとして入力するか、自然な言葉で依頼すると呼び出せます。

| スキル | 呼び出し例 | 用途 |
|:-------|:-----------|:-----|
| verify-handson | `/verify-handson` | ハンズオンSectionの検証。要件・手順の抜けや不整合をチェックする |
| section-fix | `/section-fix` | Issue・セクションの修正ワークフロー（対象ファイルとガイドを読む → 修正案を提示 → 承認後に修正 → コミット → PR） |
| lms-sync | `/lms-sync` | 教材の公開（LMS同期）の運用手順をガイドする（下の「教材の公開フロー（LMS同期）」を参照） |
| quiz-add | `/quiz-add` | 確認問題（`quiz/` の `question.md` / `model-answer.md`）を追加する |

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
| `quiz/README.md` | 確認問題（quiz）の仕組みと追加方法 | 確認問題を追加・修正する時に読む |

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
| Labels | 該当するラベルを選択 | `bug`, `handson` 等 |
| Milestone | 該当するマイルストーンを選択（あれば） | `ハンズオン品質改善`（例） |

### Issueの一覧と確認

リポジトリの「Issues」タブから一覧を確認できます。

**ラベルの意味:**

| ラベル | 意味 |
|:-------|:-----|
| `bug` | 内容の誤り・不具合 |
| `improvement` | 要改善（内容に問題がある） |
| `handson` | ハンズオンSection関連 |
| `section` | 通常Section関連 |
| `slack-inquiry` | Slackからの問い合わせ |
| `教材について` | 教材内容に関する問い合わせ |
| `needs-clarification` | 情報不足・要確認 |
| `possibly-no-fix` | 前提誤認の可能性・要レビュー |

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

マイルストーンは、関連するIssueをまとめて進捗を管理する機能です。あるテーマ（たとえばハンズオンの品質改善や、画像の整備など）に関するIssueを1つのマイルストーンに紐づけておくと、全体で何件中何件が完了したかがパーセンテージで表示され、進み具合をひと目で把握できます。

マイルストーンは、その時々の重点テーマに合わせて追加され、完了するとクローズされます。固定の一覧はこのドキュメントには載せません。**いま進行中のマイルストーンと最新の状況は、必ず GitHub の Milestones ページで確認してください。**

**マイルストーンの確認方法:**
1. リポジトリの「Issues」タブを開く
2. 「Milestones」をクリック
3. 各マイルストーンの進捗（完了率）と、紐づいたIssueの一覧を確認できる
4. 過去に完了したマイルストーンを見たい場合は「Closed」タブに切り替える

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

Co-Authored-By: Claude <noreply@anthropic.com>"
```

> AIツール（Claude Code など）で修正した場合は、AIによる共同作業であることを示す `Co-Authored-By` 行を添えます。ツールが自動で付与することが多く、行末の名前にモデルのバージョン名が含まれることもありますが、`Co-Authored-By: Claude <noreply@anthropic.com>` の形であれば問題ありません。AIツールを使わずに手動修正した場合は、この行は不要です。

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

> 💡 **TIP**: PRをマージしただけでは、まだ受講生が見るLMS（学習管理システム）には反映されません。反映するには、次の「教材の公開フロー（LMS同期）」の手順を実行します。

### Claude Codeでの作業例

Claude Codeを使う場合、以下の一言でステップ2〜5が自動で実行されます。

```
> Issue #129 を修正してください
```

Claude Codeが自動で: ブランチ作成 → ファイル読み込み → 修正案を提示 → 承認後に修正 → コミット → PR作成まで一貫して行います（`section-fix` スキル）。

---

## 教材の公開フロー（LMS同期）

修正した教材を、受講生が見る形（LMS: 学習管理システム）に反映するには、GitHub Actions を**手動で**実行します。ここでは、新しく参加したメンバーが自分の手で実行できるように、手順を具体的に説明します。

### ブランチと環境の対応

| ブランチ | 反映先 | 用途 |
|:---------|:-------|:-----|
| `main` | 本番（Production）LMS | 受講生が実際に見る環境 |
| `staging` | Staging（検証）LMS | 公開前に表示を確認する環境 |

> ⚠️ **注意**: `main` と `staging` は自動では同期されません。必ず `staging` で確認してから、内容を `main` に反映（PR/マージ）してください。時期によっては、両ブランチの内容が食い違っていることがあります。

### 4本のワークフロー

公開に使うワークフローは4本あります。すべて「手動実行（`workflow_dispatch`）」で、GitHub の「Actions」タブから起動します。実行環境はいずれも Node.js 20 です。

| Actions上の表示名 | ファイル | 対象ブランチ | 役割 |
|:------------------|:---------|:-------------|:-----|
| 画像リンクをS3 URLに置換（staging） | `.github/workflows/replace-image-links-staging.yml` | `staging` | 画像をS3へアップロードし、本文の `src` を公開URLに書き換える |
| 教材を登録・更新（staging） | `.github/workflows/sync-curriculums-staging.yml` | `staging` | `curriculums/` を読み取り、Staging LMS に登録・更新する |
| 画像リンクをS3 URLに置換（main） | `.github/workflows/replace-image-links-main.yml` | `main` | 画像をS3へアップロードし、本文の `src` を公開URLに書き換える（本番用） |
| 教材を登録・更新（main） | `.github/workflows/sync-curriculums-production.yml` | `main` | `curriculums/` を読み取り、本番 LMS に登録・更新する |

**それぞれの役割:**

- **画像リンクをS3 URLに置換**: 本文中の `<img alt="ファイル名.png" src="">`（`src` が空のタグ）を探し、`image/` にある同名ファイルを S3 にアップロードして、`src` を公開URLに書き換えます。変更が発生した場合は `chore/replace-image-links-{タイムスタンプ}` という名前のブランチが自動作成され、push されます（PR は自動では作られないので、あとで手動でPRを作成してマージします）。`alt` が無い、または `image/` に対応する画像ファイルが無い場合は、エラーで失敗します。
- **教材を登録・更新**: `curriculums/` 配下をすべて走査し、チュートリアル → チャプター → セクションの構造を JSON にまとめて、LMS の API に送信します。各セクションの「タイトル」は、ファイル名から `.md` を除いた文字列がそのまま使われます。

### 推奨する公開手順（必ず staging → main の順で）

いきなり本番（`main`）へ反映せず、まず `staging` で見た目を確認してから `main` に進めます。

**① staging で確認する**

1. 修正内容のPRを **`staging` ブランチ** にマージする
2. 「**画像リンクをS3 URLに置換（staging）**」を実行する
   - 実行後、`chore/replace-image-links-*` ブランチが自動作成されていたら、そのブランチから `staging` へのPRを作成し、内容を確認してマージする
   - 画像を追加・変更していない場合は「変更なし」となり、ブランチは作られません。その場合は次へ進みます
3. 「**教材を登録・更新（staging）**」を実行する
4. **Staging LMS** で該当ページを開き、文章と画像が正しく表示されるか確認する

**② main（本番）へ反映する**

5. `staging` の内容を **`main` ブランチ** に反映する（PRを作成してマージ）
6. 「**画像リンクをS3 URLに置換（main）**」を実行する
   - `chore/replace-image-links-*` ブランチが作成されたら、`main` へのPRを作成・確認してマージする
7. 「**教材を登録・更新（main）**」を実行する
8. **本番 LMS** で該当ページを開き、表示を最終確認する

### 実行方法

#### 方法A: Actions タブから実行する（推奨）

1. GitHub リポジトリの「**Actions**」タブを開く
2. 左側の一覧から、実行したいワークフロー名（例:「教材を登録・更新（staging）」）をクリック
3. 右側に表示される「**Run workflow**」ボタンをクリック
4. ブランチを選ぶプルダウンが表示されます。各ワークフローは名前のとおり対象ブランチ（`main` / `staging`）を対象にするよう設定されているため、ここはデフォルトのままで構いません
5. もう一度「**Run workflow**」（緑のボタン）をクリックして実行

#### 方法B: gh コマンドで実行する

`gh`（GitHub CLI）が使える場合は、ターミナルからでも起動できます。表示名には括弧や日本語が含まれるため、**ファイル名を指定するのが確実**です。

```bash
# staging: 画像置換 → 同期
gh workflow run replace-image-links-staging.yml
gh workflow run sync-curriculums-staging.yml

# main（本番）: 画像置換 → 同期
gh workflow run replace-image-links-main.yml
gh workflow run sync-curriculums-production.yml
```

実行状況は `gh run list`（一覧）や `gh run watch`（進行中のログ追跡）でも確認できます。

### 実行後の確認方法

1. 「Actions」タブで、今実行したワークフローの実行（run）をクリックし、ジョブのログを開く
2. **画像リンク置換**のログでは、末尾の「`=== 処理結果サマリー ===`」を確認する
   - `対象imgタグ数(src="")` / `S3アップロード成功数` / `置換成功数` が表示されます
   - `alt` 無しや画像ファイルの欠落があると「`=== エラー一覧 ===`」が出て、ジョブは赤い×（失敗）になります。その場合はエラー内容に沿って、`alt` の記載・ファイル名・`image/` への配置を直してから再実行します
   - 成功して変更があった場合は `chore/replace-image-links-*` ブランチが push されているので、PRにして対象ブランチへマージします
3. **教材の登録・更新**のログでは、次を確認する
   - `Collected: X curriculums, Y chapters, Z sections`（収集された件数）
   - `HTTP Status Code`（2xx なら成功。成功時は `✅ Successfully synced curriculums` と表示されます）
   - 2xx 以外は失敗（赤い×）です。ログのレスポンス本文を見て原因を確認します
4. 最後に、対象の LMS（Staging または本番）で該当ページを開き、文章・画像・見出しが意図どおりか目視で確認する

> 💡 **TIP**: ワークフローの詳細な仕様は `.github/README.md` にもまとまっています。

### Secrets と Variables について

これらのワークフローは、S3 や LMS API に接続するための認証情報（Secrets）と設定値（Variables）を使います。

- これらは**リポジトリ管理者が GitHub 側にすでに設定済み**です。新しく参加したメンバーが値を入力・変更する必要はありません（値は秘匿情報のため、このドキュメントにも記載しません）。
- 参考として、使われている項目の**名前だけ**を挙げます（値は触らないでください）。
  - 画像置換: Secrets `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`、Variables `AWS_REGION` / `S3_BUCKET` / `S3_PUBLIC_BASE_URL`
  - 同期（staging）: Secrets `STAGING_API_URL` / `STAGING_API_KEY` / `STAGING_WORKSPACE_ID`
  - 同期（main / 本番）: Secrets `PRODUCTION_API_URL` / `PRODUCTION_API_KEY` / `PRODUCTION_WORKSPACE_ID`
- 「値が設定されていない」といったエラーで失敗する場合は、自分で値を設定しようとせず、管理者に連絡してください。

---

## 教材構成の概要

```
curriculums/
└── tutorial-{N}: {タイトル}/
    └── chapter-{M}: {章タイトル}/
        └── {N}-{M}-{S}_{ファイル名}.md
```

- Tutorial 1〜13 で構成
- 多くのChapterには、章の総まとめとしてハンズオンSectionが用意されています（ファイル名は通常のSectionと同じ `{N}-{M}-{S}_{見出し名}.md` 形式で、見出し名に「ハンズオン」が含まれます。例: `10-2-4_ミドルウェア-ハンズオン演習.md`）
- 画像は `image/` ディレクトリに `{N}-{M}-{S}_{連番}.png` 形式で配置
- 各概念Sectionの確認問題は `quiz/` に、`curriculums/` と同じ階層構造で配置（詳細は `quiz/README.md`）

---

## よくある質問

### Q: どのファイルを修正すればいいですか？

GitHub Issuesに修正対象が記載されています。不明な場合はIssueのコメントで質問してください。

### Q: 修正ルールが分かりません

`.claude/CLAUDE.md` と `guides/` のガイドに詳しく記載されています。それでも不明な場合はチームメンバーに聞いてください。

### Q: 修正はいつ受講生に見えるようになりますか？

PRをマージしただけでは反映されません。「教材の公開フロー（LMS同期）」の手順で GitHub Actions を実行して、初めて LMS に反映されます。必ず `staging` で確認してから `main`（本番）に反映してください。

### Q: Claude Code のスキル（`/verify-handson` など）とは？

このプロジェクト用にあらかじめ用意された作業手順です。Claude Codeのプロンプトで `/verify-handson`（ハンズオンSectionの検証）のようにスラッシュコマンドを入力すると実行されます。利用できるスキルの一覧は「セットアップ」の「利用できるスキル（Claude Code）」を参照してください。

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
- 公開（LMS同期）は必ず `staging` で確認してから `main`（本番）に反映する
- Secrets / Variables の値は管理者が設定済み。新メンバーは値を触らない（不足エラー時は管理者に連絡）
- 不明点は必ず確認する（勝手な判断で修正しない）
