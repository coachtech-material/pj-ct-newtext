#!/usr/bin/env python3
"""ターミナル出力（ANSI）をターミナル風PNGにレンダリングする。

教材のClaude Code操作画面を実セッションから自動生成するためのツール。

使い方:
    tmux capture-pane -e -p -t <session> > shot.ans
    python3 ansi2png.py shot.ans shot.png [列数=100] [--mask mask.json]

--mask には {"置換前": "置換後", ...} のJSONを渡す。個人情報（名前・メール・
プラン表示）を受講生視点の表示に正規化する用途。**置換前後は同じ文字数にする**
（ターミナルは文字グリッドなので、長さが変わると罫線・レイアウトが崩れる）。
長さが違う場合はエラーで止まる。

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

    pos = 0
    for m in SGR_RE.finditer(text):
        seg = text[pos:m.start()]
        if seg:
            st = style()
            esc = htmlmod.escape(seg)
            out.append(f'<span style="{st}">{esc}</span>' if st else esc)
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
        st = style()
        esc = htmlmod.escape(seg)
        out.append(f'<span style="{st}">{esc}</span>' if st else esc)
    return "".join(out)

def apply_mask(text: str, mask_path: Path) -> str:
    mask = json.loads(mask_path.read_text())
    for before, after in mask.items():
        if len(before) != len(after):
            sys.exit(f"mask長さ不一致: {before!r}({len(before)}) → {after!r}({len(after)})。同じ文字数にすること")
        text = text.replace(before, after)
    return text

def render(ans_path: Path, png_path: Path, cols: int = 100, mask_path: Path | None = None):
    raw = ans_path.read_text(errors="replace")
    if mask_path:
        raw = apply_mask(raw, mask_path)
    lines = raw.split("\n")
    while lines and not lines[-1].strip():
        lines.pop()
    body = ansi_to_html("\n".join(lines))
    n_lines = len(lines)
    html_doc = f"""<!doctype html><meta charset="utf-8"><style>
:root{{--tbg:#1b1b1a;--tfg:#d7dae0}}
body{{margin:0;background:#0e0e0d;display:flex;align-items:flex-start;justify-content:flex-start}}
.win{{margin:16px;background:var(--tbg);border-radius:10px;box-shadow:0 8px 30px rgba(0,0,0,.5);overflow:hidden;border:1px solid #333}}
.bar{{height:30px;background:#2a2a29;display:flex;align-items:center;padding:0 12px;gap:7px}}
.dot{{width:11px;height:11px;border-radius:50%}}
pre{{margin:0;padding:14px 16px;font:12.5px/1.4 "SF Mono",Menlo,monospace;color:var(--tfg);white-space:pre}}
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
    if len(args) < 2:
        sys.exit(__doc__)
    render(Path(args[0]), Path(args[1]), int(args[2]) if len(args) > 2 else 100, mask)
