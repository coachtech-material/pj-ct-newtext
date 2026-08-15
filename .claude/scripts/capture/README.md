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

### 2. tmuxでセッションを操作して撮る

```bash
tmux new-session -d -s cap -x 100 -y 32 -c /path/to/題材アプリ
tmux send-keys -t cap "CLAUDE_CONFIG_DIR=~/.claude-capture claude" Enter
sleep 8
tmux capture-pane -e -p -t cap > 01-startup.ans
tmux send-keys -t cap "/context" Enter
sleep 8
tmux capture-pane -e -p -t cap > 02-context.ans
tmux kill-session -t cap
```

### 3. マスクしてPNG化する

```bash
python3 ansi2png.py 01-startup.ans 14-1-2_1.png 100 --mask mask.json
```

`mask.json` は「置換前→置換後」の辞書。**必ず同じ文字数で置換する**（ターミナルは文字グリッドなので、長さが変わると罫線が崩れる。長さ不一致はスクリプトがエラーで止める）。例:

```json
{
  "Welcome back Yotaro!": "Welcome back Wakaba!",
  "yotaro6163@gmail.com's Organization": "wakaba@example.com's Organization  ",
  "Sonnet 5 with xhigh effort · Claude Max": "Sonnet 5 with high effort · Claude Pro "
}
```

## 教材への挿入規約

- 執筆時は `<img alt="{節番号}_{連番}.png" src="">` を置くだけ（撮影は後工程で一括）
- 画像ファイルは `image/` へ。既存のimg規約（alt=ファイル名・リリース時src空）に従う
- UI変化に備え、画像の近くに「2026年◯月時点」を添える
