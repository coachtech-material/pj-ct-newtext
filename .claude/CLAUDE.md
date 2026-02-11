# プロジェクト CLAUDE.md

## このプロジェクトについて

- **プログラミング初学者向け教材**のMarkdownファイル集
- Tutorial 1〜13で構成（段階的に学習が進む）
- Laravel/PHPを中心としたWeb開発カリキュラム
- **対象者**: プログラミング未経験・ITリテラシーが高くない学習者

---

## 教材のコンセプト

1. **初学者第一**: 専門用語は必ず日常の言葉で言い換える。「なぜこれをやるのか」を最初に説明する
2. **実践重視**: 各セクションに実践パートを設け、ステップバイステップで手を動かせる内容にする
3. **現場直結スキル**: デバッグ力、命名力、Git運用、環境変数管理など、実務で即戦力となるスキルを重視
4. **構造とデータ重視**: HTML/CSSは最小限に抑え、データの流れとAPI設計に集中する
5. **段階的理解**: 前提知識を確認し、前セクションからの接続を明示する

---

## ディレクトリ構成

```
pj-ct-newtext/
├── .claude/                     # Claude Code設定
│   ├── CLAUDE.md                # このファイル（プロジェクトルール）
│   └── skills/                  # Claude Codeスキル
│       └── verify-handson/      # /verify-handson スキル
│
├── curriculums/                 # 教材本体
│   └── tutorial-{N}: {タイトル}/
│       └── chapter-{M}: {章タイトル}/
│           └── {N}-{M}-{S}_{ファイル名}.md
│
├── image/                       # 画像ファイル
│   └── {N}-{M}-{S}_{連番}.png
│
├── guides/                      # 執筆ガイドライン（チーム共有）
│   ├── writing-rules.md         # 文体・スタイルルール
│   ├── handson-structure.md     # ハンズオンSection構成ガイド
│   ├── section-structure.md     # 通常Section構成ガイド
│   └── verification.md          # 検証ガイド
│
├── references/                  # 過去の執筆ガイドライン（参照用）
│   ├── complete_writing_guidelines_v12.md
│   ├── complete_writing_guidelines_v15.md
│   └── FEEDBACK_CHANGES_SUMMARY.md
│
├── .github/                     # GitHub設定
│   ├── ISSUE_TEMPLATE/          # Issue テンプレート
│   ├── workflows/               # GitHub Actions
│   └── scripts/                 # CI/CDスクリプト
│
├── ONBOARDING.md                # チームメンバー向け入門ガイド
└── local/                       # 個人用（gitignore済み）
```

---

## セクション命名規則

```
{Tutorial番号}-{Chapter番号}-{Section番号}_{名前}.md
```

- 通常Section: `10-2-1_what_is_middleware.md`
- ハンズオンSection: `10-2-4_middleware_hands_on.md`（末尾は `_hands_on.md`）

---

## 修正ワークフロー

### Issue修正（「Issue #XX を修正して」と言われた場合）

1. `gh issue view {番号}` でIssue内容を確認する
2. `git checkout -b fix/{Section番号}-{説明}` でブランチを作成する
3. 対象ファイルと関連ガイドを読む
4. 修正案を具体的にリストアップしてユーザーに提示する
5. ユーザーの承認を得てから修正を実行する
6. `git commit` → `git push` → `gh pr create`（本文に `Closes #{Issue番号}` を含める）

### 通常の修正依頼

1. 対象ファイルと関連ガイドを読む
2. 修正案を具体的にリストアップしてユーザーに提示する
3. ユーザーの承認を得てから修正を実行する
4. ブランチ作成 → コミット → push → PR作成

> ⚠️ **重要**: 修正前に必ずユーザー承認を得ること。勝手に修正しない。

---

## ブランチ・PR運用

- **mainに直接pushしない**（必ずPR経由）
- ブランチ命名: `fix/{Section番号}-{説明}`
  - 例: `fix/10-2-4-middleware-handson`
  - 例: `fix/9-1-8-crud-handson`
- PR作成時はレビューを依頼する
- CIが通ることを確認してからマージ

---

## 文体・スタイルルール

### 基本方針

- **丁寧語**で統一（「〜です」「〜ます」）
- **読点を多めに**使用（「、」で適切に区切る）
- 身近で実用的な**比喩**を活用（「書類」「ノート」等。「魔法の杖」等の凝った比喩は避ける）
- **専門用語は必ず言い換え**を併記（例: 「リポジトリ（プロジェクトの保管庫）」）

### コードブロック

- 必ず**言語指定**をする（```php, ```bash, ```blade 等）
- **ファイルパス**をコメントで明記
- 省略する場合は `// ...` で示す

### マークダウン要素

| 要素 | 用途 |
|:-----|:-----|
| `> 💡 **TIP**` | 補足情報 |
| `> ⚠️ **注意**` | 警告・注意事項 |
| `<details><summary>` | 折りたたみ |
| 表形式 | 比較や一覧の整理 |

### 絵文字の使い分け

| 絵文字 | 用途 |
|:-------|:-----|
| 🎯 | 学習目標、次のステップ |
| ✨ | まとめ |
| 💡 | TIP、補足情報 |
| ⚠️ | 注意事項 |
| 🏃 | 実践 |
| 📝 | 学習のポイント |
| 🔑 | 重要な概念 |
| ⚙️ | ツール、コマンド |

詳細は `guides/writing-rules.md` を参照。

---

## 画像の扱い

### imgタグ形式

```html
**画像の説明**

<img alt="{Tutorial}-{Chapter}-{Section}_{連番}.png" src="">
```

- `alt`属性にファイル名を記載
- `src`属性は**空**（後でGitHub Actionsで S3 URLに自動置換される）
- 画像ファイルは `image/` ディレクトリに配置

### 完成イメージの表示

- **画像1枚**: トグル不要、直接表示
- **画像2枚以上**: `<details><summary>📸 完成画面を確認する（クリックで展開）</summary>` で折りたたみ

---

## コミットメッセージ形式

```
{Tutorial番号}: {修正内容の要約}

Co-Authored-By: Claude Opus 4.6 <noreply@anthropic.com>
```

例: `10-3-6: ハンズオン要件を追加`

---

## 作業に応じて参照するガイド

| 作業内容 | 参照するガイド |
|:---------|:---------------|
| ハンズオンSectionの修正 | `guides/handson-structure.md` |
| 通常Sectionの修正 | `guides/section-structure.md` |
| 文体・表現のチェック | `guides/writing-rules.md` |
| Sectionの検証 | `guides/verification.md` |
| 過去のガイドラインの確認 | `references/complete_writing_guidelines_v15.md` |

---

## 注意事項

- practice / sample の2プロジェクト構成は維持する
- スターターキット使用部分は勝手に変更しない
- 既存の動作する実装は壊さない
- Tutorial間の依存関係に注意する
- 既存の文体・スタイルを維持すること
