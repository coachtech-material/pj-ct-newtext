#!/usr/bin/env python3
"""Tutorial 13 の解答例から、配布用の answers/ ツリーを組み立てる。

受講生が `docs/` に作る設計書の答えを、スターターキット
(coachtech-material/laravel-post-starter) の `answers/` として配るためのもの。
教材が単一の正で、こちらは生成物。教材を直したら再生成する。

    python3 .claude/scripts/build_design_answers.py <出力先>

抜き出すのは、答え合わせ／模範解答の `**〜（解答例）**` の直下にあるもの。
本文（地の文）は落とし、表・見出し・箇条書き・コードブロック・引用だけを残す。
図は image/diagram-src/*.drawio と image/*.png をそのまま複製する。
"""
import pathlib, re, shutil, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
CUR = ROOT / "curriculums"
IMG = ROOT / "image"

# 出力ファイル → (H1, [(節, 解答例見出し, その見出しの下に置くH2 or None)])
DOCS = {
    "13-2/post-feature-list.md": ("投稿アプリ 機能一覧", [
        ("13-2-1", "機能一覧（解答例）", "## 機能一覧"),
        ("13-2-1", "今回作らないもの（解答例）", "## 今回作らないもの")]),
    "13-2/post-questions.md": ("投稿アプリ 確認事項リスト", [
        ("13-2-1", "確認事項リスト（解答例）", None)]),
    "13-2/post-uc-05.md": ("投稿アプリ ユースケース記述", [
        ("13-2-2", "UC-05: 投稿を編集する（記述の解答例）", None)]),
    "13-2/cafe-feature-list.md": ("カフェのモバイルオーダーアプリ 機能一覧", [
        ("13-2-3", "機能一覧（解答例）", "## 機能一覧"),
        ("13-2-3", "今回作らないもの（解答例）", "## 今回作らないもの"),
        ("13-2-3", "機能一覧とユースケースの対応（解答例）", "## 機能一覧とユースケースの対応")]),
    "13-2/cafe-questions.md": ("カフェのモバイルオーダーアプリ 確認事項リスト", [
        ("13-2-3", "確認事項リスト（解答例）", None)]),
    "13-2/cafe-uc-02.md": ("カフェのモバイルオーダーアプリ ユースケース記述", [
        ("13-2-3", "UC-02: 商品を注文する（記述の解答例）", None),
        ("13-2-3", "UC-05: 注文を受け渡す（記述の解答例）", None)]),

    "13-3/post-screen-list.md": ("投稿アプリ 画面一覧", [
        ("13-3-1", "投稿アプリの画面一覧（解答例）", None)]),
    "13-3/post-screen-items.md": ("投稿編集画面 画面項目定義", [
        ("13-3-3", "投稿編集画面の画面項目定義（解答例）", None)]),
    "13-3/post-input-check.md": ("投稿編集画面 入力チェック表", [
        ("13-3-4", "入力チェック表（解答例）", None),
        ("13-3-4", "決めた理由（解答例）", None)]),
    "13-3/post-messages.md": ("投稿編集画面 メッセージ一覧", [
        ("13-3-4", "メッセージ一覧（解答例）", None)]),
    "13-3/cafe-screen-list.md": ("カフェのモバイルオーダーアプリ 画面一覧", [
        ("13-3-5", "画面一覧（解答例）", None)]),
    "13-3/cafe-screen-items.md": ("メニュー画面 画面項目定義", [
        ("13-3-5", "メニュー画面の画面項目定義（解答例）", None)]),
    "13-3/cafe-input-check.md": ("カフェのモバイルオーダーアプリ 入力チェック表", [
        ("13-3-5", "入力チェック表（解答例）", None),
        ("13-3-5", "決めた理由（解答例）", None)]),
    "13-3/cafe-messages.md": ("カフェのモバイルオーダーアプリ メッセージ一覧", [
        ("13-3-5", "メッセージ一覧（解答例）", None)]),

    "13-4/post-api.md": ("投稿アプリ API設計書", [
        ("13-4-1", "エンドポイント一覧（解答例）", "## エンドポイント一覧"),
        ("13-4-1", "API-03の詳細（解答例）", "## 各エンドポイントの詳細"),
        ("13-4-1", "エラーレスポンス一覧（解答例）", "## エラーレスポンス一覧")]),
    "13-4/post-permission-matrix.md": ("投稿アプリ 権限マトリクス", [
        ("13-4-2", "権限マトリクス（解答例）", None)]),
    "13-4/cafe-api.md": ("カフェのモバイルオーダーアプリ API設計書", [
        ("13-4-3", "エンドポイント一覧（解答例）", "## エンドポイント一覧"),
        ("13-4-3", "API-02の詳細（解答例）", "## 各エンドポイントの詳細"),
        ("13-4-3", "API-06の詳細（解答例）", None),
        ("13-4-3", "エラーレスポンス一覧（解答例）", "## エラーレスポンス一覧")]),
    "13-4/cafe-permission-matrix.md": ("カフェのモバイルオーダーアプリ 権限マトリクス", [
        ("13-4-3", "権限マトリクス（解答例）", None)]),

    "13-5/post-concept.md": ("投稿アプリ 概念モデル", [
        ("13-5-1", "エンティティ一覧（解答例）", "## エンティティ一覧"),
        ("13-5-1", "関係の一覧（解答例）", "## 関係の一覧")]),
    "13-5/post-crud.md": ("投稿アプリ CRUD表", [
        ("13-5-4", "CRUD表（解答例）", None),
        ("13-5-4", "表の下に書く2〜3文（解答例）", None)]),
    "13-5/cafe-concept.md": ("カフェのモバイルオーダーアプリ 概念モデル", [
        ("13-5-5", "エンティティ一覧（解答例）", "## エンティティ一覧"),
        ("13-5-5", "関係の一覧（解答例）", "## 関係の一覧")]),
    "13-5/cafe-crud.md": ("カフェのモバイルオーダーアプリ CRUD表", [
        ("13-5-5", "CRUD表（解答例）", None)]),

    "13-6/post-state-table.md": ("投稿アプリ 遷移表", [
        ("13-6-2", "遷移表（解答例）", "## 遷移表"),
        ("13-6-2", "増える設計書（解答例）", "## この設計で増える設計書")]),
    "13-6/post-exceptions.md": ("投稿アプリ 例外一覧", [
        ("13-6-3", "投稿アプリの例外一覧（解答例）", None)]),
    "13-6/cafe-state-table.md": ("カフェのモバイルオーダーアプリ 遷移表", [
        ("13-6-4", "遷移表（解答例）", None)]),
    "13-6/cafe-exceptions.md": ("カフェのモバイルオーダーアプリ 例外一覧", [
        ("13-6-4", "例外一覧（解答例）", None)]),

    "13-8/register-viewpoints.md": ("会員登録 テスト観点表", [
        ("13-8-1", "テスト観点表（解答例）", None),
        ("13-8-1", "書けなかったものの覚え書き（解答例）", None)]),
    "13-8/register-cases.md": ("会員登録 テストケース", [
        ("13-8-1", "テストケース（解答例）", None)]),
}

# 図: 出力先 → 教材の画像連番
FIGS = {
    "13-2/post-usecase": "13-2-2_2",
    "13-2/cafe-usecase": "13-2-3_1",
    "13-3/post-transition": "13-3-2_2",
    "13-3/post-wireframe": "13-3-3_2",
    "13-3/cafe-transition": "13-3-5_1",
    "13-3/cafe-wireframe": "13-3-5_2",
    "13-5/post-er": "13-5-2_2",
    "13-5/cafe-er": "13-5-5_1",
    "13-6/post-sequence": "13-6-1_2",
    "13-6/post-state": "13-6-2_2",
    "13-6/cafe-sequence": "13-6-4_1",
    "13-6/cafe-state": "13-6-4_2",
    "13-7/post-class": "13-7-1_2",
    "13-7/post-structure": "13-7-2_2",
}

KEEP = ("|", "#", "- ", "```", "> ", "（", "  - ", "  1. ", "  2. ", "  3. ",
        "  4. ", "  5. ", "  6. ", "1. ", "2. ", "3. ", "4. ", "5. ", "6. ")


def section_text(key):
    hits = list(CUR.glob(f"tutorial-13*/*/{key}_*.md"))
    if not hits:
        raise SystemExit(f"節が見つかりません: {key}")
    t = hits[0].read_text()
    return "\n".join(m.group(1) for m in
                     re.finditer(r"<summary>📖[^<]*</summary>(.*?)</details>", t, re.S))


def extract(key, heading):
    a = section_text(key)
    m = re.search(r"\*\*" + re.escape(heading) + r"\*\*\n\n(.*?)(?=\n\*\*[^*]|\n次の観点|\n📋|\n---|\Z)",
                  a, re.S)
    if not m:
        raise SystemExit(f"解答例が見つかりません: {key} / {heading}")
    body = m.group(1).strip()
    # ```markdown は中身がそのまま設計書なので剥がす。それ以外のコードブロック
    # （```php 等）は教材が根拠として見せているものなので、丸ごと落とす。
    body = re.sub(r"```markdown\n(.*?)\n```", r"\1", body, flags=re.S)
    body = re.sub(r"```\w*\n.*?\n```", "", body, flags=re.S)
    out = []
    for line in body.split("\n"):
        if not line.strip() or line.startswith(KEEP):
            out.append(line[2:] if line.startswith("> ") else line)
    text = re.sub(r"\n{3,}", "\n\n", "\n".join(out)).strip()
    return text


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    dest = pathlib.Path(sys.argv[1])
    n_md = n_fig = 0
    for path, (title, parts) in DOCS.items():
        chunks = [f"# {title}"]
        for key, heading, sub in parts:
            if sub:
                chunks.append(sub)
            chunks.append(extract(key, heading))
        f = dest / path
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("\n\n".join(chunks) + "\n")
        n_md += 1
    for path, num in FIGS.items():
        f = dest / path
        f.parent.mkdir(parents=True, exist_ok=True)
        src_d, src_p = IMG / "diagram-src" / f"{num}.drawio", IMG / f"{num}.png"
        if not src_d.exists() or not src_p.exists():
            raise SystemExit(f"図が見つかりません: {num}")
        shutil.copy(src_d, f.with_suffix(".drawio"))
        shutil.copy(src_p, f.with_suffix(".png"))
        n_fig += 1
    print(f"{dest}: Markdown {n_md}件 / 図 {n_fig}組")


if __name__ == "__main__":
    main()
