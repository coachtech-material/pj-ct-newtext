#!/usr/bin/env python3
"""教材本文（curriculums/**/*.md）の機械チェック。

このスクリプトが執筆・レビュー時の機械チェックの単一の正（Single Source of Truth）。
`guides/writing-rules.md`・`guides/handson-structure.md` 等の書式ルールのうち、
機械判定できるものを実装する。標準ライブラリのみで動作する。

使い方:
    python3 .claude/scripts/lint_curriculum.py [--release] [--json] <file|dir>...

    --release はリリース（LMS反映）前検査: 執筆中は 🟡 の残作業（画像ファイル未配置）を 🔴 に昇格する。

検出ルール:
    🔴 broken-bold             CommonMark/GFM で太字が実際に壊れる ** の使い方
                               （閉じ ** の内側末尾が約物＋直後が文字: 「**強調。**です」／
                                 開き ** の直前が文字＋内側先頭が約物: 「です**「注意」**」）。
                               半角スペースを入れると直る
    🔴 dash-char               ダッシュ記号（– — ―）。読点・括弧・コロン等で言い換える
    🟡 code-fence-language     言語指定なしコードブロック（非コードコンテンツには text を指定する。
                               既存教材に多数残存するため 🟡。新規執筆分はセルフチェックでゼロにする）
    🔴 absolute-path           環境依存の絶対パス（/Users/ /home/）。教材上のプレースホルダー
                               （YourName・あなたのユーザー名 等）は許容する
    🔴 img-alt-missing         <img> タグに alt 属性が無い・空
    🔴 img-src-invalid         <img> タグの src が「空」でも「https URL」でもない
                               （src は空にして GitHub Actions の S3 置換に任せるのが規約）
    🔴 phase-boilerplate-drift フェーズ別AIスタンス定型文（> 🔥 で始まる引用）が正本と不一致
                               （正本は guides/ai-exercise-structure.md の P1〜P4。コピーして使う運用）
    🟡 sentence-bold           文全体の太字（** の中身が 30 字以上。太字は語句・キーフレーズに限定する）
    🟡 img-alt-format          alt が画像ファイル名の命名規則（{N}-{M}-{S}_{連番}.png 等）に合っていない
    🟡 image-file-missing      src が空の <img> の alt が指す画像ファイルが image/ に無い（--release で 🔴）
    🟡 image-md-relative       相対パスの Markdown 形式画像（![](...)）。S3 置換の対象外になるため
                               <img alt="..." src=""> 形式にする（外部 URL の Markdown 画像は対象外）
    🟡 step-numbering          Step 見出しの連番が +1 で増えていない（飛び・重複。1 への戻りは
                               「環境準備」→「実践」等の正当なリセットとして許容する）
    🟡 missing-goal-heading    「## 🎯」見出しが無い
    🟡 missing-summary-heading 「## ✨」「## 🚀」いずれの見出しも無い（まとめ欠落）

導入しないルール（判断の記録）:
    - 絵文字の許可リスト: 既存教材が 40 種以上の絵文字を機能的に使い分けているため導入しない。
      絵文字の使い分けは `guides/writing-rules.md` の表とレビューで担保する。

検査スコープ:
    - コードブロック内・インラインコード内は太字・ダッシュ・画像タグの検査対象外（フェンス追跡）
    - HTML コメント内も検査対象外
    - 絶対パスはコードブロック内も検査する（コピペ手順への環境依存パス混入を検出するため）

出力:  path:line: [🔴|🟡] rule-id: メッセージ（--json で JSON 配列。severity は error=🔴 / warning=🟡）
終了コード:  🔴 違反あり = 2 / クリーン（🟡 のみを含む）= 0 / 引数・入出力エラー = 1
    （🟡 のみのファイルは exit 0 のため PostToolUse hook からは通知されない。
      部分編集のたびに構造警告を出さないための意図的仕様で、🟡 は執筆時の
      セルフチェックと独立レビューが拾う）
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

# ---------------------------------------------------------------------------
# 定数
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[2]  # .claude/scripts/ の2つ上
IMAGE_DIR = REPO_ROOT / "image"
PHASE_GUIDE = REPO_ROOT / "guides" / "ai-exercise-structure.md"

# 禁止ダッシュ（– — ― を使わない）
DASH_CHARS = {"–", "—", "―"}

# 太字スパン（同一行内で完結する ** ペア）
BOLD_RE = re.compile(r"\*\*([^*\n]+?)\*\*")

# インラインコード（`...` / ``...``。同じ長さの空白に置換して位置を保つ）
INLINE_CODE_RE = re.compile(r"(`+)([^`]+?)\1")

# コードフェンス（blockquote 記号を剥がした後に判定）
FENCE_RE = re.compile(r"^( {0,3})(`{3,}|~{3,})[ \t]*(.*)$")
BLOCKQUOTE_PREFIX_RE = re.compile(r"^(?:[ \t]{0,3}>[ \t]?)+")

# 環境依存の絶対パス（直前が英数字・ピリオドなら URL のパス部とみなして除外）
ABS_PATH_RE = re.compile(r"(?<![A-Za-z0-9.])/(?:Users|home)/[^\s'\"`)\]]*")
# 教材上のプレースホルダーとして許容するパス（実在の個人名でない目印を含む）
ABS_PATH_PLACEHOLDER_RE = re.compile(
    r"(?i)/(?:Users|home)/[^/\s]*(?:your|user|name|example|sample|demo|ubuntu|あなた|ユーザ)"
)

# <img> タグ（alt / src 属性を個別に取り出す）
IMG_TAG_RE = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
IMG_ALT_RE = re.compile(r'\balt\s*=\s*"([^"]*)"', re.IGNORECASE)
IMG_SRC_RE = re.compile(r'\bsrc\s*=\s*"([^"]*)"', re.IGNORECASE)

# 画像ファイル名の命名規則: {T}-{C}-{S}_{連番}.png（旧形式 {T}-{C}_{連番}・概念図 _c{連番}・_v{版} 追記を許容）
IMG_FILENAME_RE = re.compile(r"^\d+(-\d+){1,2}_c?\d+(_v\d+)?\.(png|jpg|jpeg|gif)$", re.IGNORECASE)

# Markdown 形式画像（URL は空白か ) まで）
MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(\s*([^)\s]*)[^)]*\)")

# フェーズ別AIスタンス定型文（正本ガイドの見出しと引用行）
PHASE_HEADING_RE = re.compile(r"^###\s+(P\d)\b")
PHASE_QUOTE_PREFIX_RE = re.compile(r"^ {0,3}>\s*🔥")

# Step 見出し（## / ### / #### の「Step N」。🏃 等の前置きも許容）
STEP_HEADING_RE = re.compile(r"^ {0,3}#{2,4}\s*[^#\n]*?\bStep\s*(\d+)\b")

# 構造見出し
GOAL_HEADING_RE = re.compile(r"^ {0,3}##\s*🎯")
SUMMARY_HEADING_RE = re.compile(r"^ {0,3}##\s*[✨🚀]")

HTML_COMMENT_OPEN = "<!--"
HTML_COMMENT_CLOSE = "-->"

SEVERITY_ERROR = "error"      # 🔴
SEVERITY_WARNING = "warning"  # 🟡
MARKS = {SEVERITY_ERROR: "🔴", SEVERITY_WARNING: "🟡"}

FULL_BOLD_THRESHOLD = 30  # ** の中身がこの字数以上なら「文全体の太字」とみなす


# ---------------------------------------------------------------------------
# 判定ヘルパー
# ---------------------------------------------------------------------------

def is_punctuation(ch: str) -> bool:
    """CommonMark の flanking 判定で「約物」扱いになる文字か（Unicode P* / S* カテゴリ）。"""
    return unicodedata.category(ch)[0] in ("P", "S")


def is_letter_or_digit(ch: str) -> bool:
    """CommonMark の flanking 判定で「文字」扱いになる文字か（空白でも約物でもない）。"""
    return unicodedata.category(ch)[0] in ("L", "N", "M")


def mask_inline_code(line: str) -> str:
    """インラインコードを同じ長さの空白に置換する（列位置を保ったまま検査対象外にする）。"""
    return INLINE_CODE_RE.sub(lambda m: " " * len(m.group(0)), line)


def mask_html_comments(line: str, in_comment: bool) -> tuple[str, bool]:
    """HTML コメント部分を空白に置換する。

    戻り値: (マスク済みの行, 行末時点でコメント内か)。複数行コメントにも対応する。
    """
    out: list[str] = []
    i = 0
    n = len(line)
    while i < n:
        if in_comment:
            end = line.find(HTML_COMMENT_CLOSE, i)
            if end == -1:
                out.append(" " * (n - i))
                i = n
            else:
                out.append(" " * (end + len(HTML_COMMENT_CLOSE) - i))
                i = end + len(HTML_COMMENT_CLOSE)
                in_comment = False
        else:
            start = line.find(HTML_COMMENT_OPEN, i)
            if start == -1:
                out.append(line[i:])
                i = n
            else:
                out.append(line[i:start])
                i = start
                in_comment = True
    return "".join(out), in_comment


def load_phase_boilerplates() -> dict[str, str]:
    """guides/ai-exercise-structure.md から P1〜P4 の定型文（> 🔥 行）を読む。

    見出し「### P1（...」の直後のコードフェンス内にある引用行を正本とする。
    ガイドが見つからない・解析できない場合は空 dict を返し、drift 検査をスキップする。
    """
    try:
        text = PHASE_GUIDE.read_text(encoding="utf-8")
    except OSError:
        return {}
    boilerplates: dict[str, str] = {}
    current: str | None = None
    in_fence = False
    for raw in text.splitlines():
        m = PHASE_HEADING_RE.match(raw)
        if m:
            current = m.group(1)
            in_fence = False
            continue
        if current is None:
            continue
        if FENCE_RE.match(raw):
            if in_fence:
                current = None  # フェンスが閉じたら次の見出しまで読まない
            in_fence = not in_fence
            continue
        if in_fence and PHASE_QUOTE_PREFIX_RE.match(raw):
            boilerplates[current] = raw.rstrip()
    return boilerplates


# ---------------------------------------------------------------------------
# Lint 本体
# ---------------------------------------------------------------------------

class Finding:
    __slots__ = ("path", "line", "severity", "rule", "message")

    def __init__(self, path: str, line: int, severity: str, rule: str, message: str):
        self.path = path
        self.line = line
        self.severity = severity
        self.rule = rule
        self.message = message

    def format(self) -> str:
        return f"{self.path}:{self.line}: {MARKS[self.severity]} {self.rule}: {self.message}"

    def to_json(self) -> dict:
        return {
            "path": self.path,
            "line": self.line,
            "severity": self.severity,
            "mark": MARKS[self.severity],
            "rule": self.rule,
            "message": self.message,
        }


def lint_file(path: Path, phase_boilerplates: dict[str, str],
              release: bool = False) -> list[Finding]:
    findings: list[Finding] = []
    display = str(path)

    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise RuntimeError(f"{display}: 読み込みに失敗しました: {exc}") from exc

    lines = text.splitlines()

    in_fence = False
    fence_char = ""
    fence_len = 0
    in_comment = False  # 複数行 HTML コメントの追跡（フェンス外のみ）

    has_goal = False
    has_summary = False
    step_expect = 1  # Step 連番の期待値（1 への戻りはリセットとして許容）

    residue_severity = SEVERITY_ERROR if release else SEVERITY_WARNING

    for lineno, raw in enumerate(lines, start=1):
        # blockquote 記号（> ）を剥がしてフェンス判定する（引用内のコードブロックに対応）
        bq = BLOCKQUOTE_PREFIX_RE.match(raw)
        content = raw[bq.end():] if bq else raw

        fence_m = FENCE_RE.match(content)

        if in_fence:
            # 閉じフェンス: 同種の記号が開始時以上の長さで、後続文字列なし
            if (
                fence_m
                and fence_m.group(2)[0] == fence_char
                and len(fence_m.group(2)) >= fence_len
                and fence_m.group(3).strip() == ""
            ):
                in_fence = False
            else:
                # フェンス内: 絶対パスのみ検査（コピペ手順への環境依存パス混入を検出）
                check_absolute_path(findings, display, lineno, raw)
            continue

        if fence_m:
            # 開きフェンス
            in_fence = True
            fence_char = fence_m.group(2)[0]
            fence_len = len(fence_m.group(2))
            if fence_m.group(3).strip() == "":
                findings.append(Finding(
                    display, lineno, SEVERITY_WARNING, "code-fence-language",
                    "言語指定なしコードブロックです。コードは言語名、非コードコンテンツ"
                    "（ディレクトリツリー・コマンド出力等）は text を指定してください",
                ))
            continue

        # ---- フェンス外の検査 ----

        # HTML コメントをマスクする
        visible, in_comment = mask_html_comments(raw, in_comment)

        # 構造チェック用の見出し検出
        if GOAL_HEADING_RE.match(visible):
            has_goal = True
        if SUMMARY_HEADING_RE.match(visible):
            has_summary = True

        # Step 連番の検査（1 への戻りは環境準備→実践等の正当なリセットとして許容）
        sm = STEP_HEADING_RE.match(visible)
        if sm:
            n = int(sm.group(1))
            if n != step_expect and n != 1:
                findings.append(Finding(
                    display, lineno, SEVERITY_WARNING, "step-numbering",
                    f"Step 連番が飛んでいます（期待: Step {step_expect} または Step 1 / 実際: Step {n}）",
                ))
            step_expect = n + 1

        # フェーズ別AIスタンス定型文の正本一致（> 🔥 で始まる引用行）
        if phase_boilerplates and PHASE_QUOTE_PREFIX_RE.match(visible):
            if visible.rstrip() not in phase_boilerplates.values():
                findings.append(Finding(
                    display, lineno, SEVERITY_ERROR, "phase-boilerplate-drift",
                    "フェーズ別AIスタンス定型文（> 🔥）が正本と一致しません。"
                    "guides/ai-exercise-structure.md の P1〜P4 からコピーしてください"
                    "（文言を変える場合はガイドを先に更新し、全 Section へ一括反映する運用です）",
                ))

        # 絶対パス（インラインコード内も対象とするため raw で検査）
        check_absolute_path(findings, display, lineno, raw)

        # <img> タグの検査（コメントマスク後・インラインコードマスク前の visible で検査）
        for im in IMG_TAG_RE.finditer(mask_inline_code(visible)):
            tag = im.group(0)
            alt_m = IMG_ALT_RE.search(tag)
            src_m = IMG_SRC_RE.search(tag)
            alt = alt_m.group(1).strip() if alt_m else ""
            if not alt:
                findings.append(Finding(
                    display, lineno, SEVERITY_ERROR, "img-alt-missing",
                    "alt 属性の無い <img> タグです。alt に画像ファイル名"
                    "（{N}-{M}-{S}_{連番}.png）を記載してください",
                ))
            elif not IMG_FILENAME_RE.match(alt):
                findings.append(Finding(
                    display, lineno, SEVERITY_WARNING, "img-alt-format",
                    f"alt「{alt}」が画像ファイル名の命名規則（{{N}}-{{M}}-{{S}}_{{連番}}.png 等）に"
                    "合っていません",
                ))
            src = src_m.group(1).strip() if src_m else None
            if src is None:
                findings.append(Finding(
                    display, lineno, SEVERITY_ERROR, "img-src-invalid",
                    '<img> タグに src 属性がありません。src="" と空で書いてください'
                    "（公開時に GitHub Actions が S3 URL へ自動置換します）",
                ))
            elif src and not src.startswith(("https://", "http://")):
                findings.append(Finding(
                    display, lineno, SEVERITY_ERROR, "img-src-invalid",
                    f'src「{src}」は規約外です。src="" と空で書くか（S3 置換用）、'
                    "置換済みの https URL のままにしてください",
                ))
            # 画像ファイルの実在（src が空＝未置換のときだけ確認する）
            if alt and IMG_FILENAME_RE.match(alt) and src == "":
                if not (IMAGE_DIR / alt).is_file():
                    findings.append(Finding(
                        display, lineno, residue_severity, "image-file-missing",
                        f"画像ファイル「image/{alt}」がまだありません"
                        "（撮影後に配置してください。LMS 反映前には必須です）",
                    ))

        # 相対パスの Markdown 形式画像（S3 置換の対象外になる）
        for mm in MD_IMAGE_RE.finditer(mask_inline_code(visible)):
            url = mm.group(2).strip()
            if url and not re.match(r"^[a-z][a-z0-9+.-]*:", url) and not url.startswith("#"):
                findings.append(Finding(
                    display, lineno, SEVERITY_WARNING, "image-md-relative",
                    f"相対パスの Markdown 形式画像「{url}」です。S3 置換の対象外になるため"
                    '<img alt="ファイル名" src=""> 形式にしてください',
                ))

        # 以降はインラインコードを除外した本文で検査
        work = mask_inline_code(visible)

        # ダッシュ記号
        dashes = sorted({ch for ch in work if ch in DASH_CHARS})
        if dashes:
            findings.append(Finding(
                display, lineno, SEVERITY_ERROR, "dash-char",
                f"ダッシュ記号 {' '.join(dashes)} は使いません。読点・括弧・コロン等で言い換えてください",
            ))

        # 太字の書式
        for m in BOLD_RE.finditer(work):
            inner = m.group(1)
            if len(inner) >= FULL_BOLD_THRESHOLD:
                findings.append(Finding(
                    display, lineno, SEVERITY_WARNING, "sentence-bold",
                    f"文全体の太字です（{len(inner)} 字）。太字は語句・キーフレーズに限定してください",
                ))
            # CommonMark の flanking 規則で実際に壊れる形だけを検出する:
            # 閉じ ** は「直前（内側末尾）が約物 かつ 直後が文字」だと閉じ判定されない
            nxt = work[m.end():m.end() + 1]
            if inner and is_punctuation(inner[-1]) and nxt and is_letter_or_digit(nxt):
                findings.append(Finding(
                    display, lineno, SEVERITY_ERROR, "broken-bold",
                    f"「**{inner}**{nxt}」は太字が適用されません（** の内側末尾が約物で、"
                    f"直後に文字が続く形）。閉じ ** の後に半角スペースを入れてください",
                ))
            # 開き ** は「直前が文字 かつ 直後（内側先頭）が約物」だと開き判定されない
            prv = work[m.start() - 1] if m.start() > 0 else ""
            if inner and is_punctuation(inner[0]) and prv and is_letter_or_digit(prv):
                findings.append(Finding(
                    display, lineno, SEVERITY_ERROR, "broken-bold",
                    f"「{prv}**{inner}**」は太字が適用されません（** の直前が文字で、"
                    f"内側先頭が約物の形）。開き ** の前に半角スペースを入れてください",
                ))

    # ---- ファイル全体の構造チェック ----
    if not has_goal:
        findings.append(Finding(
            display, 1, SEVERITY_WARNING, "missing-goal-heading",
            "「## 🎯 このセクションで学ぶこと」見出しがありません（Section の必須構造）",
        ))
    if not has_summary:
        findings.append(Finding(
            display, 1, SEVERITY_WARNING, "missing-summary-heading",
            "まとめ見出し（「## ✨ まとめ」または「## 🚀 まとめ」）がありません（Section の必須構造）",
        ))

    return findings


def check_absolute_path(findings: list[Finding], path: str, lineno: int, line: str) -> None:
    m = ABS_PATH_RE.search(line)
    if m and not ABS_PATH_PLACEHOLDER_RE.match(m.group(0)):
        findings.append(Finding(
            path, lineno, SEVERITY_ERROR, "absolute-path",
            f"環境依存の絶対パス「{m.group(0)}」が含まれています。"
            "プレースホルダー（/Users/YourName/... 等）に置き換えてください",
        ))


# ---------------------------------------------------------------------------
# エントリポイント
# ---------------------------------------------------------------------------

def collect_targets(inputs: list[str]) -> list[Path]:
    """引数のファイル・ディレクトリから検査対象の .md を集める。"""
    targets: list[Path] = []
    for arg in inputs:
        p = Path(arg)
        if not p.exists():
            raise RuntimeError(f"{arg}: ファイルまたはディレクトリが見つかりません")
        if p.is_dir():
            for md in sorted(p.rglob("*.md")):
                if any(part.startswith(".") or part == "node_modules" for part in md.parts):
                    continue
                targets.append(md)
        else:
            targets.append(p)
    return targets


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="lint_curriculum.py",
        description="教材本文（Markdown）の書式・構造の機械チェック（執筆・レビューの単一の正）",
    )
    parser.add_argument("paths", nargs="+", metavar="<file|dir>", help="検査対象の .md ファイルまたはディレクトリ")
    parser.add_argument("--release", action="store_true",
                        help="リリース前検査（画像ファイル未配置を 🔴 に昇格）")
    parser.add_argument("--json", action="store_true", dest="as_json", help="結果を JSON 配列で出力する")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:  # argparse の引数エラー exit 2 を、exit 契約（違反あり=2）と衝突しないよう 1 に写像する
        return 0 if exc.code == 0 else 1

    phase_boilerplates = load_phase_boilerplates()

    try:
        targets = collect_targets(args.paths)
        findings: list[Finding] = []
        for target in targets:
            findings.extend(lint_file(target, phase_boilerplates, release=args.release))
    except RuntimeError as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1

    findings.sort(key=lambda f: (f.path, f.line, f.rule))

    if args.as_json:
        print(json.dumps([f.to_json() for f in findings], ensure_ascii=False, indent=2))
    else:
        for f in findings:
            print(f.format())
        errors = sum(1 for f in findings if f.severity == SEVERITY_ERROR)
        warnings = len(findings) - errors
        if findings:
            print(f"\n🔴 {errors} 件 / 🟡 {warnings} 件（検査対象 {len(targets)} ファイル）")

    return 2 if any(f.severity == SEVERITY_ERROR for f in findings) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
