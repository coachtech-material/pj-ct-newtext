#!/usr/bin/env python3
"""ターミナル出力（ANSI）をターミナル風PNGにレンダリングする。

教材のClaude Code操作画面を実セッションから自動生成するためのツール。

使い方:
    tmux capture-pane -e -p -t <session> > shot.ans
    python3 ansi2png.py shot.ans shot.png [列数=100] [--mask mask.json] [--drop 正規表現] [--skip 行数]

--mask には {"置換前": "置換後", ...} のJSONを渡す。個人情報（名前・メール・
プラン表示）を受講生視点の表示に正規化する用途。**置換前後は同じ文字数にする**
（ターミナルは文字グリッドなので、長さが変わると罫線・レイアウトが崩れる）。
長さが違う場合はエラーで止まる。

--drop は、正規表現にあたる行を丸ごと落とす。**撮影アカウント固有の告知行**
（プラン限定機能のお知らせ等、標準プランの受講生には出ないもの）を消す用途に
限る。行を落としても文字グリッドは崩れない（崩れるのは横方向だけ）。本文の
内容を消すために使わないこと。複数指定できる。

--skip は上から指定行数を落とす。前の画面の切れ端が上に残ったときの構図合わせ用。

前提: macOS + Google Chrome（ヘッドレスでPNG化に使用）。
"""
import html as htmlmod
import json
import re
import subprocess
import sys
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# 16色パレット（ダークテーマ想定）
BASE16 = [
    "#3b3b3a", "#e05561", "#8cc265", "#d1a458", "#4aa5f0", "#c162de", "#42b3c2", "#d7dae0",
    "#5a5a59", "#ff616e", "#a5e075", "#f0a45d", "#4dc4ff", "#de73ff", "#4cd1e0", "#ffffff",
]

def xterm256(n: int) -> str:
    if n < 16:
        return BASE16[n]
    if n < 232:
        n -= 16
        r, g, b = n // 36, (n % 36) // 6, n % 6
        conv = lambda v: 0 if v == 0 else 55 + v * 40
        return f"#{conv(r):02x}{conv(g):02x}{conv(b):02x}"
    v = 8 + (n - 232) * 10
    return f"#{v:02x}{v:02x}{v:02x}"

SGR_RE = re.compile(r"\x1b\[([0-9;:]*)m")
OTHER_ESC = re.compile(r"\x1b(?:\][^\x07\x1b]*(?:\x07|\x1b\\)|\[[0-9;?]*[A-Za-ln-z]|[()][0AB]|[=>])")

# ブロック要素（U+2580〜U+259F）は、フォントに任せるとセルを埋めきらず、行間に隙間が
# できてロゴや進捗バーが割れる。ターミナルは cell いっぱいに塗るので、こちらも文字を
# 使わずCSSの矩形で塗る。値は (x, y, 幅, 高さ) をセルに対する割合で並べたもの。
BLOCK_RECTS = {
    "▀": [(0, 0, 1, 1 / 2)],                    # ▀ 上半分
    "▁": [(0, 7 / 8, 1, 1 / 8)],                # ▁
    "▂": [(0, 3 / 4, 1, 1 / 4)],                # ▂
    "▃": [(0, 5 / 8, 1, 3 / 8)],                # ▃
    "▄": [(0, 1 / 2, 1, 1 / 2)],                # ▄ 下半分
    "▅": [(0, 3 / 8, 1, 5 / 8)],                # ▅
    "▆": [(0, 1 / 4, 1, 3 / 4)],                # ▆
    "▇": [(0, 1 / 8, 1, 7 / 8)],                # ▇
    "█": [(0, 0, 1, 1)],                        # █ 全体
    "▉": [(0, 0, 7 / 8, 1)],                    # ▉
    "▊": [(0, 0, 3 / 4, 1)],                    # ▊
    "▋": [(0, 0, 5 / 8, 1)],                    # ▋
    "▌": [(0, 0, 1 / 2, 1)],                    # ▌ 左半分
    "▍": [(0, 0, 3 / 8, 1)],                    # ▍
    "▎": [(0, 0, 1 / 4, 1)],                    # ▎
    "▏": [(0, 0, 1 / 8, 1)],                    # ▏
    "▐": [(1 / 2, 0, 1 / 2, 1)],                # ▐ 右半分
    "▔": [(0, 0, 1, 1 / 8)],                    # ▔
    "▕": [(7 / 8, 0, 1 / 8, 1)],                # ▕
    "▖": [(0, 1 / 2, 1 / 2, 1 / 2)],            # ▖ 左下
    "▗": [(1 / 2, 1 / 2, 1 / 2, 1 / 2)],        # ▗ 右下
    "▘": [(0, 0, 1 / 2, 1 / 2)],                # ▘ 左上
    "▙": [(0, 0, 1 / 2, 1), (0, 1 / 2, 1, 1 / 2)],      # ▙ 右上以外
    "▚": [(0, 0, 1 / 2, 1 / 2), (1 / 2, 1 / 2, 1 / 2, 1 / 2)],  # ▚
    "▛": [(0, 0, 1, 1 / 2), (0, 0, 1 / 2, 1)],          # ▛ 右下以外
    "▜": [(0, 0, 1, 1 / 2), (1 / 2, 0, 1 / 2, 1)],      # ▜ 左下以外
    "▝": [(1 / 2, 0, 1 / 2, 1 / 2)],            # ▝ 右上
    "▞": [(1 / 2, 0, 1 / 2, 1 / 2), (0, 1 / 2, 1 / 2, 1 / 2)],  # ▞
    "▟": [(1 / 2, 0, 1 / 2, 1), (0, 1 / 2, 1, 1 / 2)],  # ▟ 左上以外
}
SHADE_ALPHA = {"░": 25, "▒": 50, "▓": 75}  # ░▒▓

# 罫線（U+2500〜）も同じ理由で、隣のセルとつながらず破線に見える。
# 上・右・下・左に伸びる線の太さ（0=なし / 1=細 / 2=太 / 3=二重）で表す。
BOX_LINES = {
    "─": (0, 1, 0, 1), "━": (0, 2, 0, 2), "│": (1, 0, 1, 0), "┃": (2, 0, 2, 0),
    "┌": (0, 1, 1, 0), "┐": (0, 0, 1, 1), "└": (1, 1, 0, 0), "┘": (1, 0, 0, 1),
    "╭": (0, 1, 1, 0), "╮": (0, 0, 1, 1), "╰": (1, 1, 0, 0), "╯": (1, 0, 0, 1),
    "┏": (0, 2, 2, 0), "┓": (0, 0, 2, 2), "┗": (2, 2, 0, 0), "┛": (2, 0, 0, 2),
    "├": (1, 1, 1, 0), "┤": (1, 0, 1, 1), "┬": (0, 1, 1, 1), "┴": (1, 1, 0, 1),
    "┣": (2, 2, 2, 0), "┫": (2, 0, 2, 2), "┳": (0, 2, 2, 2), "┻": (2, 2, 0, 2),
    "┼": (1, 1, 1, 1), "╋": (2, 2, 2, 2),
    "═": (0, 3, 0, 3), "║": (3, 0, 3, 0),
    "╔": (0, 3, 3, 0), "╗": (0, 0, 3, 3), "╚": (3, 3, 0, 0), "╝": (3, 0, 0, 3),
    "╠": (3, 3, 3, 0), "╣": (3, 0, 3, 3), "╦": (0, 3, 3, 3), "╩": (3, 3, 0, 3),
    "╬": (3, 3, 3, 3),
}
THICK = {1: "0.12em", 2: "0.24em"}  # 細線・太線の太さ
DOUBLE_GAP = "0.12em"               # 二重線の線と線の間隔

# 破線の罫線。(向き, 太さ, 1セルに入る破片の数) で表す。
DASH_LINES = {
    "╌": ("h", 1, 2), "╍": ("h", 2, 2), "╎": ("v", 1, 2), "╏": ("v", 2, 2),
    "┄": ("h", 1, 3), "┅": ("h", 2, 3), "┆": ("v", 1, 3), "┇": ("v", 2, 3),
    "┈": ("h", 1, 4), "┉": ("h", 2, 4), "┊": ("v", 1, 4), "┋": ("v", 2, 4),
}

BLOCK_CHARS = set(BLOCK_RECTS) | set(SHADE_ALPHA) | set(BOX_LINES) | set(DASH_LINES)

def tileable(ch: str) -> bool:
    """横に並べても継ぎ目の要らない字か。罫線や進捗バーはまとめて1つの矩形で塗る。"""
    if ch in SHADE_ALPHA:
        return True
    if ch in BLOCK_RECTS:
        return all(x == 0 and w >= 1 for x, _, w, _ in BLOCK_RECTS[ch])
    if ch in BOX_LINES:
        up, right, down, left = BOX_LINES[ch]
        return up == 0 and down == 0 and right == left
    return False

def box_bg(ch: str) -> str:
    """罫線1文字ぶんの background を組み立てる。中心から各方向へ棒を伸ばす。"""
    up, right, down, left = BOX_LINES[ch]
    layers = []

    def arm(direction: str, weight: int, shift: str = "0em"):
        t = THICK.get(weight, THICK[1])
        if direction in ("right", "left"):
            size = f"50% {t}"
            x = "100%" if direction == "right" else "0"
            y = f"calc(50% + {shift})" if shift != "0em" else "50%"
        else:
            size = f"{t} 50%"
            y = "100%" if direction == "down" else "0"
            x = f"calc(50% + {shift})" if shift != "0em" else "50%"
        layers.append(f"linear-gradient(currentColor,currentColor) {x} {y}/{size} no-repeat")

    for direction, weight in (("up", up), ("right", right), ("down", down), ("left", left)):
        if weight == 0:
            continue
        if weight == 3:
            arm(direction, 1, f"-{DOUBLE_GAP}")
            arm(direction, 1, DOUBLE_GAP)
        else:
            arm(direction, weight)
    return ",".join(layers)

def dash_bg(ch: str) -> str:
    """破線1文字ぶん。1セルを破片の数で割り、前半だけ塗るのを繰り返す。"""
    axis, weight, n = DASH_LINES[ch]
    t = THICK.get(weight, THICK[1])
    on, period = 62 / n, 100 / n
    side = "to right" if axis == "h" else "to bottom"
    grad = (f"repeating-linear-gradient({side},"
            f"currentColor 0 {on:.4g}%,transparent {on:.4g}% {period:.4g}%)")
    if axis == "h":
        return f"{grad} 0 50%/100% {t} no-repeat"
    return f"{grad} 50% 0/{t} 100% no-repeat"

def block_bg(ch: str) -> str:
    """ブロック文字1つぶんの background を組み立てる。"""
    if ch in DASH_LINES:
        return dash_bg(ch)
    if ch in BOX_LINES:
        return box_bg(ch)
    if ch in SHADE_ALPHA:
        paint = f"color-mix(in srgb, currentColor {SHADE_ALPHA[ch]}%, transparent)"
        return f"linear-gradient({paint},{paint}) 0 0/100% 100% no-repeat"
    layers = []
    for x, y, w, h in BLOCK_RECTS[ch]:
        # 背景の位置指定は割合なので、左端からの距離ではなく「残り幅に対する割合」で書く
        px = 0 if w >= 1 else x / (1 - w) * 100
        py = 0 if h >= 1 else y / (1 - h) * 100
        layers.append(
            f"linear-gradient(currentColor,currentColor) "
            f"{px:.4g}% {py:.4g}%/{w * 100:.4g}% {h * 100:.4g}% no-repeat"
        )
    return ",".join(layers)

def ansi_to_html(text: str) -> str:
    text = OTHER_ESC.sub("", text)
    out = []
    state = {"fg": None, "bg": None, "bold": False, "dim": False, "italic": False,
             "underline": False, "reverse": False, "strike": False}

    def style() -> str:
        fg = state["fg"]; bg = state["bg"]
        if state["reverse"]:
            fg, bg = (bg or "var(--tbg)"), (fg or "var(--tfg)")
        css = []
        if fg: css.append(f"color:{fg}")
        if bg: css.append(f"background:{bg}")
        if state["bold"]: css.append("font-weight:700")
        if state["dim"]: css.append("opacity:.55")
        if state["italic"]: css.append("font-style:italic")
        if state["underline"]: css.append("text-decoration:underline")
        if state["strike"]: css.append("text-decoration:line-through")
        return ";".join(css)

    def emit(seg: str):
        """1区間ぶんのHTMLを積む。ブロック文字だけは文字ではなく矩形で塗る。"""
        st = style()
        fg = state["fg"]; bg = state["bg"]
        if state["reverse"]:
            fg, bg = (bg or "var(--tbg)"), (fg or "var(--tfg)")
        buf = []

        def flush():
            if buf:
                esc = htmlmod.escape("".join(buf))
                out.append(f'<span style="{st}">{esc}</span>' if st else esc)
                buf.clear()

        i = 0
        while i < len(seg):
            ch = seg[i]
            if ch not in BLOCK_CHARS:
                buf.append(ch)
                i += 1
                continue
            flush()
            n = 1
            if tileable(ch):
                while i + n < len(seg) and seg[i + n] == ch:
                    n += 1
            css = [f"color:{fg or 'var(--tfg)'}"]
            if n > 1:
                css.append(f"width:{n}ch")
            layers = block_bg(ch)
            css.append(f"background:{layers},{bg}" if bg else f"background:{layers}")
            out.append(f'<i class="blk" style="{";".join(css)}"></i>')
            i += n
        flush()

    pos = 0
    for m in SGR_RE.finditer(text):
        seg = text[pos:m.start()]
        if seg:
            emit(seg)
        pos = m.end()
        params = [int(p) if p else 0 for p in m.group(1).replace(":", ";").split(";")] or [0]
        i = 0
        while i < len(params):
            p = params[i]
            if p == 0: state.update(fg=None, bg=None, bold=False, dim=False, italic=False, underline=False, reverse=False, strike=False)
            elif p == 1: state["bold"] = True
            elif p == 2: state["dim"] = True
            elif p == 3: state["italic"] = True
            elif p == 4: state["underline"] = True
            elif p == 7: state["reverse"] = True
            elif p == 9: state["strike"] = True
            elif p == 22: state["bold"] = state["dim"] = False
            elif p == 23: state["italic"] = False
            elif p == 24: state["underline"] = False
            elif p == 27: state["reverse"] = False
            elif p == 29: state["strike"] = False
            elif 30 <= p <= 37: state["fg"] = BASE16[p - 30]
            elif p == 38 and i + 1 < len(params):
                if params[i + 1] == 5 and i + 2 < len(params):
                    state["fg"] = xterm256(params[i + 2]); i += 2
                elif params[i + 1] == 2 and i + 4 < len(params):
                    state["fg"] = f"#{params[i+2]:02x}{params[i+3]:02x}{params[i+4]:02x}"; i += 4
            elif p == 39: state["fg"] = None
            elif 40 <= p <= 47: state["bg"] = BASE16[p - 40]
            elif p == 48 and i + 1 < len(params):
                if params[i + 1] == 5 and i + 2 < len(params):
                    state["bg"] = xterm256(params[i + 2]); i += 2
                elif params[i + 1] == 2 and i + 4 < len(params):
                    state["bg"] = f"#{params[i+2]:02x}{params[i+3]:02x}{params[i+4]:02x}"; i += 4
            elif p == 49: state["bg"] = None
            elif 90 <= p <= 97: state["fg"] = BASE16[p - 90 + 8]
            elif 100 <= p <= 107: state["bg"] = BASE16[p - 100 + 8]
            i += 1
    seg = text[pos:]
    if seg:
        emit(seg)
    return "".join(out)

def apply_mask(text: str, mask_path: Path) -> str:
    mask = json.loads(mask_path.read_text())
    for before, after in mask.items():
        if before.startswith("re:"):
            # 正規表現。置換結果が短い場合は、元と同じ幅になるよう空白で埋める
            def _sub(m, tmpl=after):
                rep = m.expand(tmpl)
                if len(rep) > len(m.group(0)):
                    sys.exit(f"mask長さ超過: {m.group(0)!r} → {rep!r}")
                return rep + " " * (len(m.group(0)) - len(rep))
            text = re.sub(before[3:], _sub, text, flags=re.M)
            continue
        if len(before) == len(after):
            text = text.replace(before, after)
            continue
        if len(after) > len(before):
            sys.exit(f"mask長さ超過: {before!r}({len(before)}) → {after!r}({len(after)})")
        # 行末にあるものだけは短い置換を許し、余った分は空白で埋める（見た目は変わらない）
        pad = after + " " * (len(before) - len(after))
        new = re.sub(re.escape(before) + r"(?=[ \t]*(?:\x1b\[[0-9;]*m)*[ \t]*$)",
                     pad.replace("\\", "\\\\"), text, flags=re.M)
        if new == text and before in text:
            sys.exit(f"mask長さ不一致: {before!r}({len(before)}) → {after!r}({len(after)})。"
                     "行末以外では同じ文字数にすること")
        text = new
    return text

def drop_lines(lines: list[str], patterns: list[str]) -> list[str]:
    res = [re.compile(p) for p in patterns]
    return [l for l in lines if not any(r.search(l) for r in res)]

def render(ans_path: Path, png_path: Path, cols: int = 100, mask_path: Path | None = None,
           drops: list[str] | None = None, skip: int = 0):
    raw = ans_path.read_text(errors="replace")
    if mask_path:
        raw = apply_mask(raw, mask_path)
    lines = raw.split("\n")
    if drops:
        lines = drop_lines(lines, drops)
    if skip:
        lines = lines[skip:]
    while lines and not lines[-1].strip():
        lines.pop()
    while lines and not lines[0].strip():
        lines.pop(0)
    body = ansi_to_html("\n".join(lines))
    n_lines = len(lines)
    html_doc = f"""<!doctype html><meta charset="utf-8"><style>
:root{{--tbg:#1b1b1a;--tfg:#d7dae0;--lh:1.4}}
body{{margin:0;background:#0e0e0d;display:flex;align-items:flex-start;justify-content:flex-start}}
.win{{margin:16px;background:var(--tbg);border-radius:10px;box-shadow:0 8px 30px rgba(0,0,0,.5);overflow:hidden;border:1px solid #333}}
.bar{{height:30px;background:#2a2a29;display:flex;align-items:center;padding:0 12px;gap:7px}}
.dot{{width:11px;height:11px;border-radius:50%}}
pre{{margin:0;padding:14px 16px;font:12.5px/var(--lh) "SF Mono",Menlo,monospace;color:var(--tfg);white-space:pre}}
/* ブロック文字はフォントに描かせず、セルいっぱいの矩形で塗る（行間の隙間を作らない） */
/* 1セルの幅は端数（約7.5px）なので、そのまま並べると隣との境目に髪の毛ほどの隙間や
   段差が残り、罫線が破線に見える。右と下へ0.5pxだけはみ出させ、同じ分だけ余白を
   詰めることで、レイアウトを変えずに境目を隠す */
.blk{{display:inline-block;width:1ch;height:calc(1em*var(--lh));vertical-align:top;
     box-sizing:content-box;padding:0 .5px .5px 0;margin:0 -.5px -.5px 0}}
</style><div class="win"><div class="bar"><span class="dot" style="background:#ff5f57"></span><span class="dot" style="background:#febc2e"></span><span class="dot" style="background:#28c840"></span></div><pre>{body}</pre></div>"""
    html_path = png_path.with_suffix(".html")
    html_path.write_text(html_doc)
    width = int(cols * 7.53) + 32 + 34
    height = int(n_lines * 17.5) + 30 + 28 + 34
    subprocess.run([CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
                    "--force-device-scale-factor=2", f"--window-size={width},{height}",
                    f"--screenshot={png_path.resolve()}", f"file://{html_path.resolve()}"],
                   check=True, capture_output=True)
    html_path.unlink()
    print(f"OK {png_path.name} ({width}x{height})")

if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    mask = None
    if "--mask" in args:
        i = args.index("--mask")
        mask = Path(args[i + 1])
        del args[i:i + 2]
    skip = 0
    if "--skip" in args:
        i = args.index("--skip")
        skip = int(args[i + 1])
        del args[i:i + 2]
    drops = []
    while "--drop" in args:
        i = args.index("--drop")
        drops.append(args[i + 1])
        del args[i:i + 2]
    if len(args) < 2:
        sys.exit(__doc__)
    render(Path(args[0]), Path(args[1]), int(args[2]) if len(args) > 2 else 100, mask, drops, skip)
