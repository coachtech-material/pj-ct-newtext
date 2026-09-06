# Claude Code 操作画面の自動キャプチャ

教材に載せるClaude Codeの画面画像を、実セッションの実出力から自動生成するパイプライン。試作と検証は済んでいる（方針・注意点の正本はAIパート再設計方針Artifactの07）。

## 仕組み

```
tmuxで実セッションを操作
  → tmux capture-pane -e でANSIごと取得
  → 置換辞書で個人情報を受講生視点の表示に正規化（同一文字数置換）
  → ansi2png.py がHTML化し、Chromeヘッドレスで2x PNGにレンダリング
```

1枚あたり数秒・完全自動。実出力なので作り物ではない（加工はターミナル風の枠とマスクのみ）。

## 撮影手順

### 1. 撮影用プロファイルを用意する（初回のみ）

普段の環境（名前・メール・プラン表示・MCP警告・スキル）が画面に写らないよう、設定ディレクトリを分離した素のプロファイルで撮る。

```bash
CLAUDE_CONFIG_DIR=~/.claude-capture claude
# 初回はログインを求められる。撮影用アカウントでログインする
```

プロファイルを作ったら、撮る前に次まで済ませておく（どれも画面に写るため）。

| やること | 手順 | 理由 |
|:--|:--|:--|
| モデルを Sonnet に | `/model` → Sonnet → Enter | 教材の標準がSonnet。ヘッダの表示が変わる |
| エフォートを high に | `/effort` → high → Enter | 同上 |
| Chrome連携を切る | `/chrome` → `Enabled by default` を No | 拡張機能を入れている人だけ起動時に確認が出る |

### 2. tmuxでセッションを操作して撮る

tmuxの通知行（`tmux detected · scroll with PgUp/PgDn`／`tmux focus-events off`）が
Claude Codeの入力欄の上に出る。受講生の画面には出ないので、撮影用のtmux設定で消す。

```bash
# capture.tmux.conf
set -g mouse on
set -g focus-events on
set -g status off
set -g default-terminal "xterm-256color"
```

`CLAUDE_CONFIG_DIR` はコマンド行に書くと画面に写る。`clear` の前に export しておく。
シェルのプロンプトも `PS1` を差し替えて、ホスト名とユーザー名を写さない。

```bash
tmux -f capture.tmux.conf new-session -d -s cap -x 100 -y 24 -c /path/to/題材アプリ
tmux send-keys -t cap 'export CLAUDE_CONFIG_DIR=~/.claude-capture; PS1="%1~ %# "; clear' Enter
tmux send-keys -t cap "claude" Enter
sleep 12
tmux capture-pane -e -p -t cap > 01-startup.ans
tmux send-keys -t cap "/context" Enter
sleep 8
tmux capture-pane -e -p -t cap > 02-context.ans
tmux kill-session -t cap
```

「走っている画面」は完了後ではなく**実行の途中**で `capture-pane` する
（`send-keys` → 短い `sleep` → capture）。

### 3. マスクしてPNG化する

```bash
python3 ansi2png.py 01-startup.ans 14-1-2_1.png 100 --mask mask.json --drop '▎' --drop '\+1 more'
```

`mask.json` は「置換前→置換後」の辞書。**必ず同じ文字数で置換する**（ターミナルは文字グリッドなので、長さが変わると罫線が崩れる。長さ不一致はスクリプトがエラーで止める）。例:

```json
{
  "yotaro6163@gmail.com's Organization": "student@example.com's Organization ",
  "Claude Max": "Claude Pro",
  "yotaro": "wakaba"
}
```

長いほうの語句から先に書く（辞書は書いた順に適用されるので、`yotaro` を先に置くと
メールアドレスの項目に届かなくなる）。

`--drop` は正規表現にあたる行を丸ごと落とす。**撮影アカウント固有の告知行**
（プラン限定機能のお知らせ等、標準プランの受講生には出ないもの）に限って使う。
本文の内容を消すために使わないこと。

## 教材への挿入規約

- 執筆時は `<img alt="{節番号}_{連番}.png" src="">` を置くだけ（撮影は後工程で一括）
- 画像ファイルは `image/` へ。既存のimg規約（alt=ファイル名・リリース時src空）に従う
- UI変化に備え、画像の近くに「2026年◯月時点」を添える
