#!/usr/bin/env python3
"""Stage 1 サムネイルを Gemini の画像生成 API で作る。

  export GEMINI_API_KEY=...
  python3 scripts/generate.py t13 t14 t15 t16

prompts/<slug>.md の「## プロンプト本文」直下のコードブロックをそのまま API に渡し、
生成結果を後処理して output/<slug>.png に保存する。

後処理を挟むのは、生成モデルがプロンプトの厳守事項（四隅は直角・色帯は画像の
最外周から）を守りきらないため。外周に残った白い余白を切り落とし、角が丸く
なっていれば色帯と同じ色で埋めて直角にし、既存サムネと同じ 1264x848 に揃える。

出力は毎回変わるので、気に入らなければ同じコマンドを再実行すればよい。
"""
import base64
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request

from PIL import Image, ImageDraw

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
MODEL = os.environ.get("IMG_MODEL", "gemini-3-pro-image")
SIZE = (1264, 848)


def extract_prompt(slug: str) -> str:
    md = io.open(f"{BASE}/prompts/{slug}.md", encoding="utf-8").read()
    body = md.split("## プロンプト本文", 1)[1]
    return re.search(r"```\n(.*?)\n```", body, re.S).group(1).strip()


def call_api(prompt: str) -> bytes:
    key = os.environ["GEMINI_API_KEY"]
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {"aspectRatio": "3:2"},
        },
    }
    req = urllib.request.Request(
        f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}",
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        d = json.load(r)
    for part in d.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        inline = part.get("inlineData") or part.get("inline_data")
        if inline:
            return base64.b64decode(inline["data"])
    raise RuntimeError(f"画像が返らなかった: {json.dumps(d)[:300]}")


def is_bg(c, tol=16) -> bool:
    return all(v >= 255 - tol for v in c[:3])


def postprocess(raw: bytes, out_path: str) -> str:
    im = Image.open(io.BytesIO(raw)).convert("RGB")
    w, h = im.size
    px = im.load()
    cx, cy = w // 2, h // 2

    # 辺の中央から内側へ走査し、白い余白の内側（＝色帯の外端）を探す
    top = 0
    while top < h - 1 and is_bg(px[cx, top]):
        top += 1
    bot = h - 1
    while bot > 0 and is_bg(px[cx, bot]):
        bot -= 1
    left = 0
    while left < w - 1 and is_bg(px[left, cy]):
        left += 1
    right = w - 1
    while right > 0 and is_bg(px[right, cy]):
        right -= 1

    im = im.crop((left, top, right + 1, bot + 1))
    w2, h2 = im.size

    # 角が丸く残っていれば色帯と同じ色で埋めて直角にする
    frame = im.getpixel((w2 // 2, 1))
    filled = 0
    for xy in ((0, 0), (w2 - 1, 0), (0, h2 - 1), (w2 - 1, h2 - 1)):
        if is_bg(im.getpixel(xy)):
            ImageDraw.floodfill(im, xy, frame, thresh=40)
            filled += 1

    im.resize(SIZE, Image.LANCZOS).save(out_path)
    return f"crop=({left},{top})-({right},{bot}) / 角丸埋め {filled}箇所 / 帯色 {frame}"


def main(slugs):
    os.makedirs(f"{BASE}/output", exist_ok=True)
    for slug in slugs:
        out = f"{BASE}/output/{slug}.png"
        try:
            info = postprocess(call_api(extract_prompt(slug)), out)
            print(f"{slug}: {out} ({os.path.getsize(out)} bytes) {info}")
        except urllib.error.HTTPError as e:
            print(f"{slug}: HTTP {e.code} -> {e.read().decode()[:300]}", file=sys.stderr)
        except Exception as e:
            print(f"{slug}: {type(e).__name__} -> {e}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1:] or ["t13", "t14", "t15", "t16"])
