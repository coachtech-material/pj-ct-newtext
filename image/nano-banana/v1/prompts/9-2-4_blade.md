# 9-2-4: Bladeレイアウトとコンポーネント（B2: 関係図）

**Gem**: v4.1 | **テンプレート**: B2 | **ステータス**: ドラフト

---

## c1: レイアウト継承の全体構成図

### プロンプト本文

```
Bladeのレイアウト継承の仕組みを、「共通部分をまとめる」構成図として図解してください。

## 内容
教材ではレイアウトを「全ページで共通の部分（ヘッダー、フッター、ナビ）をまとめたファイル」として説明している:
- Webサイトでは全ページ共通のヘッダー・フッター・ナビがある
- 毎回書くのは非効率なのでレイアウトファイルとしてまとめる
- 子ビューはレイアウトを継承して、個別のコンテンツだけを書く
- 実際の開発では「ゼロから作る」より「既存のものを読み解いて使う」ことが多い

## 描いてほしいもの
Webページの構造を視覚的に分解し、共通部分と個別部分を色分けして描く:

【画面上段: 完成したWebページの見た目】
- ヘッダー（ナビゲーション付き）
- メインコンテンツエリア
- フッター

【画面下段: ファイル構成の関係図】

レイアウトファイル（layouts/app.blade.php）:
- 青色の枠で囲む
- ヘッダー（固定）、@yield('content')（穴が空いている）、フッター（固定）
- キャラクターが「共通部分は僕が管理するよ！」

子ビュー（users/index.blade.php）:
- 緑色の枠で囲む
- @extends('layouts.app')で継承宣言
- @section('content')で個別コンテンツを差し込む
- キャラクターが「僕はコンテンツだけ書けばOK！」

矢印で「子ビューのコンテンツがレイアウトの@yieldに差し込まれる」流れを示す。

タイトル: 「Bladeレイアウト〜共通部分をまとめる仕組み〜」

## 概念の強調
- 「@extends」「@yield」「@section」のBlade構文を最も大きく太い文字で描く
- 共通部分（ヘッダー・フッター）と個別部分（コンテンツ）の色分けを明確にする
- 「穴（@yield）」に「中身（@section）」が差し込まれるイメージを直感的に表現
- ファイルパスを正確に記載（layouts/app.blade.php, users/index.blade.php）
```

### 構図イメージ（ASCIIアート）

```
┌──────────────────────────────────────────────────────────────┐
│       「Bladeレイアウト〜共通部分をまとめる仕組み〜」            │
│                                                               │
│  【完成ページ】              【ファイル構成】                    │
│  ┌──────────────┐                                            │
│  │ 🔵 Header     │   ← 共通    layouts/app.blade.php         │
│  │ 🔵 Nav        │                ┌─ 🔵 ──────────────┐     │
│  ├──────────────┤              │ <header>...</header> │     │
│  │              │              │ <nav>...</nav>       │     │
│  │ 🟢 Content   │   ← 個別    │ @yield('content')    │ ◀── 穴 │
│  │              │              │ <footer>...</footer> │     │
│  ├──────────────┤              └────────────────────┘     │
│  │ 🔵 Footer    │   ← 共通                                   │
│  └──────────────┘              users/index.blade.php         │
│                                  ┌─ 🟢 ──────────────┐     │
│                                  │ @extends('layouts.app')│    │
│                                  │ @section('content')  │──▶差込│
│                                  │  <h2>ユーザー一覧</h2>│     │
│                                  │ @endsection          │     │
│                                  └────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
```

### 挿入情報

- ファイル: `curriculums/tutorial-9: webフレームワークLaravelの基礎的な使い方を学ぼう🪛/chapter-2: Laravelにおける見た目の仕組み/9-2-4_blade_layouts_components.md`
- 挿入位置: 「📐 レイアウト継承」セクション、「レイアウトとは？」の説明直後（L30付近、既存の`<img alt="9-2-4_c1.png">`の位置）
- 画像ファイル名: `9-2-4_c1.png`

### 確認項目

- [ ] Blade構文のラベルが正確か（@extends, @yield, @section, @endsection）
- [ ] ファイルパスが正確か（layouts/app.blade.php, users/index.blade.php）
- [ ] 共通部分と個別部分の色分けが明確か
- [ ] 「穴に差し込む」仕組みが直感的に伝わるか

---

## c2: @extends/@section/@yieldの具体的な関係図

### プロンプト本文

```
@extends, @section, @yield のBladeディレクティブの具体的な対応関係を図解してください。

## 内容
教材では以下の対応関係を解説している:
- レイアウト側の @yield('title') ← 子ビュー側の @section('title', 'ユーザー一覧')
- レイアウト側の @yield('content') ← 子ビュー側の @section('content')...@endsection
- @yield('title', 'My App') はデフォルト値を持てる（子ビューが値を渡さなければ 'My App' が使われる）

## 描いてほしいもの
左右にレイアウトファイルと子ビューファイルを並べ、対応関係を色付きの矢印で結ぶ:

【左側: レイアウトファイル（layouts/app.blade.php）】
HTMLの構造をコードブロック風に表示:
- <title>@yield('title', 'My App')</title> ← 🟡 黄色でハイライト
- <header>...</header>
- <main>@yield('content')</main> ← 🟢 緑色でハイライト
- <footer>...</footer>

【右側: 子ビュー（users/index.blade.php）】
- @extends('layouts.app') ← 継承の宣言
- @section('title', 'ユーザー一覧') ← 🟡 黄色
- @section('content') ← 🟢 緑色
  - <h2>ユーザー一覧</h2>
  - @forelse...
- @endsection

矢印で対応関係を結ぶ:
- 🟡 @section('title') ──▶ @yield('title') に「ユーザー一覧」が入る
- 🟢 @section('content') ──▶ @yield('content') にHTMLコンテンツが入る

キャラクターが「@yieldは穴、@sectionは差し込む中身！」と説明。

タイトル: 「@extends / @section / @yield の対応関係」

## 概念の強調
- 「@extends」「@section」「@yield」の3つのディレクティブを最も大きく太い文字で描く
- 色付き矢印で対応関係を明確に示す（titleは黄色、contentは緑色）
- デフォルト値の仕組み（@yield('title', 'My App')）にも小さく触れる
- 「穴（@yield）」と「中身（@section）」のメタファーを視覚的に表現
```

### 構図イメージ（ASCIIアート）

```
┌──────────────────────────────────────────────────────────────┐
│        「@extends / @section / @yield の対応関係」              │
│                                                               │
│  layouts/app.blade.php           users/index.blade.php        │
│  ┌─────────────────────┐       ┌─────────────────────┐      │
│  │ <html>               │       │ @extends('layouts    │      │
│  │  <head>              │       │          .app')      │      │
│  │   <title>            │       │                      │      │
│  │    🟡@yield('title', │◀─ 🟡─│ @section('title',   │      │
│  │       'My App')      │       │  'ユーザー一覧')     │      │
│  │   </title>           │       │                      │      │
│  │  </head>             │       │ @section('content')  │      │
│  │  <body>              │       │   <h2>ユーザー一覧   │      │
│  │   <header>...</header>│       │   </h2>             │      │
│  │   <main>             │       │   @forelse...        │      │
│  │    🟢@yield('content')│◀─ 🟢─│   @endforelse       │      │
│  │   </main>            │       │ @endsection          │      │
│  │   <footer>...</footer>│       │                      │      │
│  │  </body>             │       └─────────────────────┘      │
│  │ </html>              │                                     │
│  └─────────────────────┘                                     │
│                                                               │
│  💬「@yieldは穴、@sectionは差し込む中身！」                     │
└──────────────────────────────────────────────────────────────┘
```

### 挿入情報

- ファイル: `curriculums/tutorial-9: webフレームワークLaravelの基礎的な使い方を学ぼう🪛/chapter-2: Laravelにおける見た目の仕組み/9-2-4_blade_layouts_components.md`
- 挿入位置: 「継承の仕組み（図解）」セクション（L84付近、既存の`<img alt="9-2-4_c2.png">`の位置）
- 画像ファイル名: `9-2-4_c2.png`

### 確認項目

- [ ] Blade構文のラベルが正確か（@extends, @section, @yield, @endsection）
- [ ] 対応関係の矢印が正しいペアを結んでいるか（title→title, content→content）
- [ ] デフォルト値（'My App'）の仕組みが示されているか
- [ ] ファイルパスが正確か（layouts/app.blade.php, users/index.blade.php）
- [ ] 色分けが一貫しているか（titleとcontentで異なる色）
