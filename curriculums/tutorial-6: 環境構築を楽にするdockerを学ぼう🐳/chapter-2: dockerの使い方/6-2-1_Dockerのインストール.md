# 6-2-1: Dockerのインストール

## 🎯 このセクションで学ぶこと

*   自分のOS（WindowsまたはMac）に、Docker Desktopをインストールする方法を学ぶ。
*   インストールが、正しく完了したことを、コマンドを使って確認する方法を学ぶ。
*   Docker Desktopの、基本的な画面構成と、GUIでの操作方法を理解する。

---

## 導入

Dockerの概念とメリットを理解したところで、いよいよ、あなたのPCに、Dockerをインストールし、コンテナの世界への第一歩を踏み出しましょう。

Dockerを、PC上で手軽に利用するために、Docker社は、「**Docker Desktop**」という、便利なアプリケーションを提供しています。Docker Desktopには、Docker本体（Docker Engine）だけでなく、コマンドラインツールや、コンテナを視覚的に管理するためのGUIツールなどが、オールインワンで含まれています。

このセクションでは、WindowsとMac、それぞれのOSごとに、Docker Desktopのインストール手順を、詳しく解説します。

**【重要】Docker Desktopのライセンスについて**

2022年1月31日より、Docker Desktopの利用規約が変更され、大企業（従業員250人以上、または、年間売上1000万ドル以上）での商用利用は、有料サブスクリプションが必要になりました。しかし、**個人での利用、学習目的での利用、小規模な組織での利用は、引き続き、無料で利用できます**。このカリキュラムの学習者は、安心して、無料プランのまま、利用してください。[1]

---

## 詳細解説

### 🪟 Windowsへのインストール

WindowsでDocker Desktopを利用するには、**WSL 2 (Windows Subsystem for Linux 2)** という機能が、有効になっている必要があります。WSL 2は、Windows上で、Linuxの実行環境を、シームレスに利用するための仕組みです。

1.  **WSL 2の有効化**: ほとんどの、最近のWindows 10/11では、WSL 2は、簡単に有効化できます。管理者権限で、PowerShellまたはコマンドプロンプトを開き、以下のコマンドを実行してください。

    ```powershell
    wsl --install
    ```

    このコマンドが、必要なコンポーネントの有効化や、デフォルトのLinuxディストリビューション（通常はUbuntu）のインストールなどを、自動的に行ってくれます。完了後、PCの再起動を求められる場合があります。

2.  **Docker Desktopのダウンロード**: 公式サイトの、[Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/) のページにアクセスし、「Docker Desktop for Windows」のボタンをクリックして、インストーラーをダウンロードします。

3.  **インストーラーの実行**: ダウンロードした `.exe` ファイルをダブルクリックして、インストーラーを起動します。設定画面では、「Use WSL 2 instead of Hyper-V (recommended)」のチェックボックスが、オンになっていることを確認し、OKボタンを押します。インストールが完了したら、「Close and restart」ボタンで、PCを再起動します。

4.  **初回起動**: 再起動後、Docker Desktopが自動的に起動します。初回起動時には、利用規約への同意を求める画面が表示されるので、「I accept the terms」にチェックを入れ、「Accept」ボタンをクリックします。

### 🍎 Macへのインストール

Macへのインストールは、Windowsよりも、シンプルです。

1.  **Docker Desktopのダウンロード**: 公式サイトの、[Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/) のページにアクセスします。お使いのMacのチップに応じて、「**Mac with Intel chip**」または「**Mac with Apple silicon**」の、どちらかのボタンをクリックして、インストーラー（`.dmg` ファイル）をダウンロードします。

    *   **チップの確認方法**: 画面左上の、Appleメニュー >「このMacについて」を選択すると、プロセッサの項目に、「Intel」または「Apple M1/M2」などのチップ名が表示されます。

2.  **インストーラーの実行**: ダウンロードした `.dmg` ファイルをダブルクリックして開きます。Dockerのアイコンを、Applicationsフォルダに、ドラッグ＆ドロップします。

3.  **初回起動**: Applicationsフォルダから、Dockerを起動します。初回起動時には、管理者パスワードの入力を求められる場合があります。また、利用規約への同意画面が表示されたら、同様に、Acceptしてください。

### ✅ インストールの確認

Docker Desktopが、正しくインストールされ、起動していることを確認するために、ターミナル（Windowsの場合は、PowerShellまたはコマンドプロンプト）を開き、以下のコマンドを実行してみましょう。

```bash
docker --version
```

`Docker version 20.10.21, build ...` のように、Dockerのバージョン情報が表示されれば、インストールは成功です。

次に、以下のコマンドも実行してみましょう。

```bash
docker run hello-world
```

このコマンドは、「hello-world」という、Dockerの動作確認用の、非常に小さなコンテナを、ダウンロードして、実行するものです。ターミナルに、`Hello from Docker!` というメッセージが表示されれば、Dockerが、正常に動作していることの、完璧な証明になります。

---

### 🪟 Windowsの方へ：これからの開発は「WSL（Ubuntu）」で行います

ここまでで、WindowsにWSL 2（Linuxの実行環境）がインストールされました。**Windowsの方は、これ以降のコマンド操作を、PowerShellではなく「WSL（Ubuntu）」のターミナルで行います。** 少しだけ準備をしておきましょう。

#### なぜWSL（Ubuntu）を使うのか？

この教材で登場するコマンド（`docker run ...` や `sail ...` など）は、Linux/Macで使われる書き方で書かれています。WindowsのPowerShellでは、この書き方の一部（改行の `\` や `$(...)` など）が動きません。

WSLは「Windowsの中で動く本物のLinux」なので、**教材のコマンドをそのまま、書き換えずに実行できます**。実務でも、WindowsでWeb開発をする際はWSLを使うのが一般的です。ここで慣れておきましょう。

> 💡 **TIP**: Macの方は、お使いの「ターミナル」をそのまま使えます。この節は読み飛ばして、次の「Docker Desktopの使い方」に進んでください。

#### 1. Ubuntu（WSL）のターミナルを開く

スタートメニューで「**Ubuntu**」と検索し、起動します。初回起動時は、WSL内で使う**ユーザー名**と**パスワード**の設定を求められるので、入力してください（このパスワードは、後で `sudo` コマンドを使うときに必要になります）。

> 💡 **TIP**: ここで作るユーザー名・パスワードは、Windowsのログイン情報とは別物です。WSL（Ubuntu）専用のものとして、忘れないようにメモしておきましょう。

#### 2. VSCodeをWSLに接続する

WSL内のファイルを、いつものVSCodeで編集できるようにします。

1. VSCodeを開き、拡張機能から「**WSL**」を検索し、Microsoft製の「WSL」拡張機能をインストールします。
2. Ubuntuのターミナルで、以下を実行します。

   ```bash
   code .
   ```

   初回は必要なコンポーネントが自動でインストールされ、WSLに接続された状態のVSCodeが開きます。VSCodeの左下に「**WSL: Ubuntu**」と表示されていれば成功です。

> 💡 **TIP**: 左下が「WSL: Ubuntu」のとき、VSCode内のターミナル（`Ctrl + @`）は自動的にUbuntuのbashになります。つまり、**VSCode内のターミナルがそのままWSLの操作画面になります**。

#### 3. 作業フォルダはWSL（Linux）側に置く

WSLで開発するときは、**ファイルをWSL側のホームディレクトリ（`~`）に置く**のがおすすめです。WindowsのCドライブ（`/mnt/c/...`）に置くと、動作が遅くなったり、改行コードの違いで不具合が出ることがあります。

```bash
# WSLのホームに移動（ここが今後の作業の拠点）
cd ~
```

> ⚠️ **注意**: Docker Desktopを開き、「Settings」>「Resources」>「WSL Integration」で「Ubuntu」がオンになっていることを確認してください。これがオフだと、Ubuntu内で `docker` コマンドが使えません。

#### 4. Git設定とSSHキーを、WSL側にも用意する（重要）

Tutorial 4で行ったGitの初期設定やSSHキーは、**Windows側**に保存されています。WSL（Ubuntu）は別の環境なので、**そのままではGitHubへpushできません**（`git push` 時に `Permission denied (publickey)` というエラーになります）。WSL内で、もう一度だけ設定しておきましょう。

**(1) Gitの名前とメールを設定**（Tutorial 4-2-2と同じ内容）

```bash
git config --global user.name "Your Name"
git config --global user.email "your_email@example.com"
```

**(2) SSHキーをWSL内で新しく作成**（Tutorial 4-2-3と同じ手順）

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

保存場所・パスフレーズの確認では、そのままEnterを押せばOKです。鍵は `~/.ssh/id_ed25519`（WSL側）に作られます。

**(3) 公開鍵を表示してGitHubに登録**

```bash
cat ~/.ssh/id_ed25519.pub
```

表示された文字列をすべてコピーし、GitHubの「Settings」>「SSH and GPG keys」>「New SSH key」に貼り付けて登録します（Tutorial 4-2-3と同じ操作です）。

**(4) 接続を確認**

```bash
ssh -T git@github.com
```

`Hi <ユーザー名>! You've successfully authenticated...` と表示されれば成功です。これで、WSL内からGitHubへpushできるようになりました。

> 💡 **TIP**: なぜ作り直すの？ … SSHキーは「環境ごと」に持つのが基本です。Windows側とWSL側は別の場所なので、WSLで作業するならWSL側にも鍵が必要、というだけのことです。

---

## 🖥️ Docker Desktopの使い方

Docker Desktopは、コマンドラインだけでなく、GUI（グラフィカルユーザーインターフェース）でも、コンテナを管理することができます。特に、「コンテナが動いているかどうか」を確認したい時に、非常に便利です。

### 画面の基本構成

Docker Desktopを起動すると、以下のような画面が表示されます。

| メニュー | 役割 |
| :--- | :--- |
| **Containers** | 現在のコンテナの一覧を表示。起動中・停止中のコンテナを確認できる |
| **Images** | ダウンロード済みのイメージの一覧を表示 |
| **Volumes** | データの永続化に使用するボリュームの一覧を表示 |

### コンテナの状態を確認する

**Containers** メニューをクリックすると、現在のコンテナの一覧が表示されます。

*   **緑色のアイコン**: コンテナが**起動中（Running）**
*   **グレーのアイコン**: コンテナが**停止中（Stopped）**

環境構築で「うまく動かない」と感じた時は、まず、Docker Desktopを開いて、コンテナが起動しているかどうかを確認しましょう。

### GUIでのコンテナ操作

Docker Desktopでは、以下の操作をGUIで行うことができます。

| 操作 | 方法 |
| :--- | :--- |
| **コンテナの起動** | 停止中のコンテナの横にある「▶」ボタンをクリック |
| **コンテナの停止** | 起動中のコンテナの横にある「■」ボタンをクリック |
| **コンテナの削除** | コンテナを選択し、ゴミ箱アイコンをクリック |
| **ログの確認** | コンテナ名をクリックすると、ログが表示される |

### ログの確認方法

コンテナが正常に動作しているかどうかを確認するために、**ログ**を見ることは非常に重要です。

1.  **Containers** メニューを開く
2.  確認したいコンテナの名前をクリック
3.  **Logs** タブをクリック

ログには、コンテナ内で実行されているアプリケーションの出力が表示されます。エラーが発生している場合は、ここにエラーメッセージが表示されるので、問題解決の手がかりになります。

> 📝 **コマンドとGUI、どちらを使うべき？**
> 
> 慣れてくると、コマンドの方が速く操作できますが、最初のうちは、Docker DesktopのGUIを使って、「今、何が動いているのか」を視覚的に確認することをおすすめします。特に、環境構築でトラブルが発生した時は、GUIでコンテナの状態を確認することで、問題の原因を特定しやすくなります。

---

## ✨ まとめ

このセクションでは、お使いのPCに、Docker Desktopをインストールし、正常に動作することを確認するまでの手順を学びました。

*   **Docker Desktop**: Dockerを、手軽に利用するための、オールインワン・アプリケーション。GUIでのコンテナ管理も可能。
*   **Windowsへのインストール**: **WSL 2** の有効化が前提となる。`wsl --install` コマンドで、簡単にセットアップできる。
*   **Macへのインストール**: **Intelチップ**か、**Apple Silicon**かによって、インストーラーが異なるので、注意が必要。
*   **動作確認**: `docker --version` と `docker run hello-world` の、2つのコマンドを実行し、バージョン情報と、「Hello from Docker!」のメッセージが表示されることを確認する。
*   **Docker DesktopのGUI**: コンテナの状態確認、起動/停止、ログの確認などを、視覚的に行うことができる。

これで、あなたのPCは、コンテナを自在に操るための、準備が整いました。次のセクションでは、Dockerを操作するための、基本的なコマンドについて、学んでいきましょう。

---
## 参考文献

[1] Docker. (2022). *Docker is Updating and Extending Our Product Subscriptions*. [https://www.docker.com/blog/updating-product-subscriptions/](https://www.docker.com/blog/updating-product-subscriptions/)
