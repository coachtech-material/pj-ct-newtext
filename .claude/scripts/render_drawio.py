#!/usr/bin/env python3
"""`.drawio` のソースから、app.diagrams.net で描画するための URL を組み立てる。

教材に載せる図は draw.io 由来の PNG に統一している（`guides/design-section-structure.md`
「教材に載せる図の作り方」）。受講生が draw.io で描くのと同じ見た目の画像を、
`.drawio` の XML から機械的に書き出すためのヘルパー。

使い方:
    python3 .claude/scripts/render_drawio.py image/diagram-src/13-5-2_1.drawio [--scale 2]

出力（3行）:
    URL <描画用URL>
    VIEWPORT <幅> <高さ>     ← ブラウザのウィンドウサイズに使う
    OUT image/13-5-2_1.png   ← 保存先

書き出しの手順:
    1. このスクリプトで URL と VIEWPORT を得る
    2. ブラウザを VIEWPORT のサイズにして URL を開く
    3. `svg` 要素のスクリーンショットを撮って OUT へ保存する

`--scale` は解像度を上げるための倍率。ソースの `.drawio` は等倍のまま置いておき、
描画時だけ座標・フォントサイズ・線幅を倍にする（受講生へ配る `.drawio` は等倍のため）。
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.parse
from pathlib import Path

MARGIN = 60  # 図の周囲に残す余白（描画後の px）

GEOMETRY_ATTRS = ("x", "y", "width", "height")
SCALED_STYLE_KEYS = ("fontSize", "strokeWidth")


def scale_geometry(xml: str, factor: float) -> str:
    """mxGeometry の座標・寸法を factor 倍にする。"""

    def repl(m: re.Match[str]) -> str:
        tag = m.group(0)
        for attr in GEOMETRY_ATTRS:
            tag = re.sub(
                rf'\b{attr}="(-?[\d.]+)"',
                lambda a, _attr=attr: f'{_attr}="{float(a.group(1)) * factor:g}"',
                tag,
            )
        return tag

    return re.sub(r"<mxGeometry\b[^>]*/?>", repl, xml)


def scale_styles(xml: str, factor: float) -> str:
    """style 属性の中の fontSize / strokeWidth を factor 倍にする。"""

    def repl(m: re.Match[str]) -> str:
        style = m.group(1)
        for key in SCALED_STYLE_KEYS:
            style = re.sub(
                rf"\b{key}=([\d.]+)",
                lambda a, _k=key: f"{_k}={float(a.group(1)) * factor:g}",
                style,
            )
        # fontSize の指定が無い図形には既定値（12）を倍にして補う
        if "fontSize=" not in style:
            style = style.rstrip(";") + f";fontSize={12 * factor:g};"
        return f'style="{style}"'

    return re.sub(r'style="([^"]*)"', repl, xml)


def content_size(xml: str) -> tuple[float, float]:
    """図形の座標から、描画に必要な幅と高さを見積もる。"""
    xs: list[float] = []
    ys: list[float] = []
    for m in re.finditer(r"<mxGeometry\b[^>]*/?>", xml):
        tag = m.group(0)
        if 'as="geometry"' not in tag:
            continue
        x = re.search(r'\bx="(-?[\d.]+)"', tag)
        y = re.search(r'\by="(-?[\d.]+)"', tag)
        w = re.search(r'\bwidth="(-?[\d.]+)"', tag)
        h = re.search(r'\bheight="(-?[\d.]+)"', tag)
        if x and w:
            xs.extend([float(x.group(1)), float(x.group(1)) + float(w.group(1))])
        if y and h:
            ys.extend([float(y.group(1)), float(y.group(1)) + float(h.group(1))])
    if not xs or not ys:
        raise SystemExit("図形の座標を読み取れませんでした（mxGeometry が見つかりません）")
    return max(xs) - min(xs), max(ys) - min(ys)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", help=".drawio ファイル")
    ap.add_argument("--scale", type=float, default=2.0, help="描画倍率（既定: 2）")
    args = ap.parse_args()

    src = Path(args.source)
    text = src.read_text(encoding="utf-8")

    m = re.search(r"<mxGraphModel\b.*?</mxGraphModel>", text, re.S)
    if not m:
        raise SystemExit(f"{src}: mxGraphModel が見つかりません")
    xml = m.group(0)

    w, h = content_size(xml)
    xml = scale_styles(scale_geometry(xml, args.scale), args.scale)

    url = (
        "https://app.diagrams.net/?splash=0&ui=min&chrome=0#R"
        + urllib.parse.quote(xml, safe="")
    )
    out = Path("image") / (src.stem + ".png")

    print(f"URL {url}")
    print(f"VIEWPORT {int(w * args.scale) + MARGIN * 2} {int(h * args.scale) + MARGIN * 2}")
    print(f"OUT {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
