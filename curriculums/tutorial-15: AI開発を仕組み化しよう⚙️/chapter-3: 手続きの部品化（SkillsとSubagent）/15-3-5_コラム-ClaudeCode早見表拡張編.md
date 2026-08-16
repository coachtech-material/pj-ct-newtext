# 15-3-5: コラム: Claude Code早見表【拡張編】

## 🎯 このセクションで学ぶこと

- 置きたいものから、それをどこに置くのかを引けるようになる。
- 設定ファイルとフックに何が書けるのかを、名前の一覧で見渡せるようになる。
- ここに載せていないものを、公式ドキュメントで探せるようになる。

---

## 導入

14-1-7の早見表は、入力欄に打つコマンドとキー操作を集めたものでした。こちらは、`.claude/` の中に置くもの側の早見表です。Chapter 2からChapter 5までで作るものが、どのファイルのどこに収まるのかを、1か所に並べます。

以下はすべて2026年8月時点のものです。名前や既定値が違うときは、公式ドキュメントの設定リファレンスが正です。14-1-7に載せた行は、ここでは繰り返しません。

---

## `.claude/` の地図

同じものを、このプロジェクトだけに効く場所と、自分の全プロジェクトに効く場所のどちらにも置けます。

| 置くもの | このプロジェクトだけ | 自分の全プロジェクト | 扱う節 |
|:--|:--|:--|:--|
| 決まりごとの1枚 | `CLAUDE.md`（リポジトリ直下） | `~/.claude/CLAUDE.md` | 15-2-1 |
| 話題ごとに分けた決まり | `.claude/rules/<話題>.md` | `~/.claude/rules/<話題>.md` | 15-2-3 |
| 手順の部品 | `.claude/skills/<名前>/SKILL.md` | `~/.claude/skills/<名前>/SKILL.md` | 15-3-1 |
| サブエージェント | `.claude/agents/<名前>.md` | `~/.claude/agents/<名前>.md` | 15-3-3 |
| 設定 | `.claude/settings.json` | `~/.claude/settings.json` | 15-4-1 |
| 自分用のコマンド | `.claude/commands/<名前>.md` | （この教材では扱いません） | 参考 |

同じ名前のSkillが複数の場所にあるときは、自分用のほうがプロジェクトのものより優先されます。プロジェクトに `code-review` という名前のSkillを置くと、同梱の `/code-review` はそちらに置き換わります。ただし同梱側の別名 `/review` は、自分のSkillを呼びません。

`.claude/commands/` のファイルは、ファイル名がそのまま `/名前` になります。Skillと同じ名札が使えますが、`name` と `paths` は読まれません。同じ名前のSkillがあるとSkillが勝ちます。公式はSkillのほうを勧めているので、この教材でもSkillだけを使います。

Claudeが自分で書き足していくメモ（auto memory・15-2-1）は、リポジトリの外に置かれます。場所は `~/.claude/projects/<プロジェクト>/memory/` で、`<プロジェクト>` はgitリポジトリから決まります。同じリポジトリのworktreeとサブフォルダは、1つのフォルダを共有します。このメモは自分のパソコンの中だけのもので、ほかのマシンやクラウドの環境には渡りません。

---

## ルールの早見

| 書き方 | いつ読まれるか |
|:--|:--|
| `paths` を書かない | 起動時に読み込まれ、`.claude/CLAUDE.md` と同じ優先度で効く |
| `paths` を書く | 指定した場所のファイルをClaudeが読んだときに読み込まれる（道具を使うたびではない） |

`paths` はファイルの先頭の名札に書きます。書けるのは、ファイル名の当てはめ方（glob）です。

```markdown
---
paths:
  - "database/migrations/**"
  - "**/*.php"
---
```

- `.claude/rules/` の中は、`frontend/`・`backend/` のようなサブフォルダに分けて置けます。`.md` は下まで探されます。
- `CLAUDE.md` からは、`@path/to/import` の書き方でほかのファイルを取り込めます。取り込んだ先からさらに取り込むのは4段までです。
- `.claude/rules/` はsymlinkに対応しています。`ln -s ~/shared-claude-rules .claude/rules/shared` の形で、共通のルールを複数のプロジェクトから使えます。

---

## `settings.json` に書けるもの

| 項目 | 何を決めるか | 扱う節 |
|:--|:--|:--|
| `permissions` | 許可の指定（allow・ask・deny） | 15-4-1 |
| `defaultMode` | 新しいセッションが始まるときの許可のモード。`default`・`acceptEdits`・`plan`・`auto`・`dontAsk`・`bypassPermissions`・`manual` | 15-4-1 |
| `hooks` | 決まった場面で走らせるコマンド | 15-4-2 |
| `autoMemoryEnabled` | Claudeが自分で取るメモの入り切り。既定は `true` | 15-2-1 |

`defaultMode` の `auto` は、プロジェクトの設定ファイルからは効きません。使うなら `~/.claude/settings.json` に書きます。`autoMemoryEnabled` は `/memory` の切り替えでも変えられ、そのときは `~/.claude/settings.json` に保存されます。

書ける項目はこれで全部ではありません。全量は公式ドキュメントの設定リファレンスにあります。

---

## Hooksの場面

| 場面 | イベント名 |
|:--|:--|
| セッションの始まりと終わり | `SessionStart` / `SessionEnd` |
| あなたが入力を送ったとき | `UserPromptSubmit` |
| 道具を使う前と後 | `PreToolUse` / `PostToolUse` / `PostToolUseFailure` |
| 応答が終わろうとするとき | `Stop` / `StopFailure` / `SubagentStop` |
| そのほか | `Notification` / `PreCompact` |

この教材で使うのは `PostToolUse` の1つだけです（15-4-2）。

---

## サブエージェント定義の項目

| 項目 | 書くもの |
|:--|:--|
| `name` | 必須。小文字とハイフンで付ける名前。ファイル名と同じでなくてもよい |
| `description` | 必須。いつこの担当に任せるか |
| `tools` | 任意。使ってよい道具。書かないと、使える道具を全部引き継ぐ |
| `model` | 任意。既定は `inherit`（呼んだ側と同じもの） |

---

## 同梱Skillとプラグイン

2026年8月時点で入っている同梱のSkillには、`/code-review`・`/verify`・`/run`・`/run-skill-generator`・`/debug`・`/simplify`・`/loop`・`/batch`・`/claude-api`・`/dataviz`・`/design-sync`・`/fewer-permission-prompts`・`/doctor` があります。手元で使えるものは、`/` を打って出る候補で確かめられます。

公式が配っているSkillのまとまりは、次の2行で入ります（15-3-2で使ったもの）。

```text
/plugin marketplace add anthropics/skills
/plugin install example-skills@anthropic-agent-skills
```

標準（`.claude/` に置く形）と、プラグイン（まとめて配る形）の使い分けは、次のとおりです。

| 形 | 呼び出す名前 | 向いている用途 |
|:--|:--|:--|
| 標準（`.claude/`） | `/hello` | 自分の作業、このプロジェクト固有のもの、試作 |
| プラグイン | `/plugin-name:hello` | チームへの共有、配布、版を切って出すもの |

公式の勧め方も同じです。まず `.claude/` に置いて手早く直しながら育て、人に渡す段になったらプラグインにします。

---

## MCPの管理

| やりたいこと | 打つもの |
|:--|:--|
| 追加する | `claude mcp add [options] <name> -- <command> [args...]`（14-4-4） |
| 一覧で見る | `claude mcp list` |
| 1つの中身を見る | `claude mcp get <name>` |
| セッションの中から管理する | `/mcp`（14-1-7） |

保存先は `-s`（`--scope`）で選びます。

| スコープ | どこまで効くか | 保存される場所 | チームに渡るか |
|:--|:--|:--|:--|
| Local（既定） | このプロジェクトだけ | `~/.claude.json` | 渡らない |
| Project | このプロジェクトだけ | リポジトリ直下の `.mcp.json` | gitで渡る |
| User | 自分の全プロジェクト | `~/.claude.json` | 渡らない |

---

## 書く場所を増やす起動フラグ

| フラグ | 何をするか |
|:--|:--|
| `--worktree`, `-w` | `<リポジトリ>/.claude/worktrees/<名前>` にworktreeを作って、そこでセッションを開く。名前を省くと自動で付く |
| `-w #<番号>` | プルリクエストの番号・GitHubのPRのURL・GitLabのMRのURLを渡すと、それを `origin` から取ってきて、そこから枝分かれさせる |
| `--tmux` | worktree用のtmuxセッションを作る（`--worktree` と一緒に使う）。iTerm2ではネイティブのペイン、`--tmux=classic` で従来のtmux |

使い方は15-5-1で扱います。

---

## 変動が大きいもの

ここに挙げる2つは、この教材では使いません。名前と調べ先だけ載せます。

- **サンドボックス**: `settings.json` の `sandbox` に書く設定です。bashで動かすコマンドを、ファイルシステムとネットワークから隔離します。`sandbox.enabled` の既定は `false` です（macOS・Linux・WSL2）。
- **`/goal`**: 終わるときの条件を、そのセッションのあいだだけ付ける簡易な仕組みです。

---

## 💰 追加課金になるもの

定額の外になるコマンドは14-1-7にまとめてあります。

---

## 考え方の広がり

**仕様駆動開発**

14-3-3では、設計書を書かせてから、それを渡して実装させました。この進め方には **仕様駆動開発**（Spec-Driven Development、SDD）という呼び名が付いていて、同じ形をなぞる道具も公開されています。

| 名前 | 何か | 見に行く先 |
|:--|:--|:--|
| **Spec Kit** | GitHubが公開しているオープンソースの道具立て。どのAIコーディングエージェントとも使えます | `https://github.com/github/spec-kit` |
| **Kiro** | AWSが作って運用しているもの。IDE・CLI・ウェブから使えます | `https://kiro.dev/` |
| **cc-sdd** | `npx cc-sdd@latest` で入るもの。Claude Codeでこの流れをなぞれます | `https://github.com/gotalab/cc-sdd` |

どれも**要件 → 設計 → タスク → 実装**の順に進みます。14-3-3でたどったのは、この並びの要件・設計・実装にあたります。

**デザインをAIと作る**

15-3-1で同梱の棚を1周したときに名前だけ見た `/design-sync` は、Claude Design への入口です。Claude Designは、作りたいものを言葉で説明すると、Claudeが下書きを作るものです。2026年8月時点ではbeta（試しに出している段階）で、Proプランなら追加の課金なしに使えます。紹介は `https://claude.com/product/design` にあります。

デザインシステム（画面の部品と決まりの一式）は、GitHubやローカルのコードベースから持ち込めます。持ち込んでおくと、Claudeは実際に存在するコンポーネントで組み、自分が出したものをデザインシステムと突き合わせて、直してから見せます。`/design-sync [hint]` が取り込むのはリポジトリの中のReactのデザインシステムで、初めて取り込むときは大きいリポジトリだと数時間かかることがあります。このアプリはReactを使っていないので、この教材では扱いません。

---

## ✨ まとめ

- 置き場所を思い出せないときは、この地図 → 公式ドキュメントの設定リファレンスの順で引く。
- 同じものを、このプロジェクトだけの場所と、自分の全プロジェクトの場所のどちらにも置ける。渡したい範囲で選ぶ。
- ここに載せたのは、Tutorial 15で触るものと、その隣にあるものだけ。全量は公式ドキュメントにある。

---
