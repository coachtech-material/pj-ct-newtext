#!/usr/bin/env python3
"""PostToolUse hook: 教材本文の編集直後に機械チェックを実行する。

Claude Code の Edit / Write ツール実行後に呼ばれる（.claude/settings.json の hooks 参照）。
stdin の JSON（PostToolUse ペイロード）から tool_input.file_path を取り出し、
プロジェクト配下 curriculums/**/*.md のときだけ .claude/scripts/lint_curriculum.py
（書式・構造の機械チェックの単一の正）を実行する。

🔴 違反があれば stderr に出力して exit 2 する。PostToolUse の exit 2 は非ブロッキングで、
stderr が Claude にフィードバックされる（編集自体は完了済み）。対象外のファイルは exit 0。
自動修正は行わない。修正の判断は Claude / 執筆者に委ねる。

lint_curriculum.py の 🟡（警告）は exit 0 のためこの hook からは通知されない
（部分編集のたびに構造警告を出さないための意図的仕様。🟡 は執筆時の
セルフチェックと独立レビューが拾う）。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

SUBPROCESS_TIMEOUT = 60  # 秒


def resolve_project_dir() -> Path:
    """プロジェクトルートを解決する。$CLAUDE_PROJECT_DIR 優先、なければスクリプト位置から導出。"""
    env = os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env).resolve()
    # .claude/hooks/post-edit-lint.py → 2 つ上がプロジェクトルート
    return Path(__file__).resolve().parents[2]


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return 0  # ペイロードが読めない場合はチェックせず通す

    tool_input = payload.get("tool_input") or {}
    file_path = tool_input.get("file_path")
    if not file_path:
        return 0  # file_path を持たないツール（Bash 等）は対象外

    root = resolve_project_dir()
    target = Path(file_path)
    if not target.is_absolute():
        target = root / target
    target = target.resolve()

    # プロジェクト配下 curriculums/**/*.md のみ検査する
    try:
        rel = target.relative_to(root)
    except ValueError:
        return 0
    if rel.parts[:1] != ("curriculums",) or target.suffix.lower() != ".md":
        return 0
    if not target.is_file():
        return 0  # 削除・リネーム直後など

    lint_script = root / ".claude" / "scripts" / "lint_curriculum.py"
    if not lint_script.is_file():
        return 0

    try:
        result = subprocess.run(
            [sys.executable, str(lint_script), str(target)],
            capture_output=True, text=True, timeout=SUBPROCESS_TIMEOUT, cwd=str(root),
        )
    except subprocess.TimeoutExpired:
        print("post-edit-lint: lint_curriculum.py がタイムアウトしました", file=sys.stderr)
        return 0  # 検査失敗で編集フローを妨げない

    if result.returncode == 2:
        output = (result.stdout + result.stderr).strip()
        print(
            f"機械チェック（.claude/scripts/lint_curriculum.py）が 🔴 違反を検出しました:\n{output}",
            file=sys.stderr,
        )
        return 2
    if result.returncode not in (0, 2):
        # スクリプト自体のエラーは通知だけして通す
        err = (result.stdout + result.stderr).strip()
        print(f"post-edit-lint: lint_curriculum.py がエラー終了しました:\n{err}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
