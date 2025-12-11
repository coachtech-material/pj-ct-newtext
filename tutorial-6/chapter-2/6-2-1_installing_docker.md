# Tutorial 6-2-1: Dockerのインストール

## 🎯 このセクションで学ぶこと

*   自分のOS（WindowsまたはMac）に、Docker Desktopをインストールする方法を学ぶ。
*   インストールが、正しく完了したことを、コマンドを使って確認する方法を学ぶ。
*   Docker Desktopの、基本的な画面構成と役割を理解する。

---

## 導入

Dockerの概念とメリットを理解したところで、いよいよ、あなたのPCに、Dockerをインストールし、コンテナの世界への第一歩を踏み出しましょう。

Dockerを、PC上で手軽に利用するために、Docker社は、「**Docker Desktop**」という、便利なアプリケーションを提供しています。Docker Desktopには、Docker本体（Docker Engine）だけでなく、コマンドラインツールや、コンテナを視覚的に管理するためのGUIツールなどが、オールインワンで含まれています。

このセクションでは、WindowsとMac、それぞれのOSごとに、Docker Desktopのインストール手順を、詳しく解説します。

**【重要】Docker Desktopのライセンスについて**

2022年1月31日より、Docker Desktopの利用規約が変更され、**大企業（従業員250人以上、または、年間売上1000万ドル以上）**での商用利用は、有料サブスクリプションが必要になりました。しかし、**個人での利用、学習目的での利用、小規模な組織での利用は、引き続き、無料で利用できます**。このカリキュラムの学習者は、安心して、無料プランのまま、利用してください。[1]

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

## ✨ まとめ

このセクションでは、お使いのPCに、Docker Desktopをインストールし、正常に動作することを確認するまでの手順を学びました。

*   **Docker Desktop**: Dockerを、手軽に利用するための、オールインワン・アプリケーション。
*   **Windowsへのインストール**: **WSL 2** の有効化が前提となる。`wsl --install` コマンドで、簡単にセットアップできる。
*   **Macへのインストール**: **Intelチップ**か、**Apple Silicon**かによって、インストーラーが異なるので、注意が必要。
*   **動作確認**: `docker --version` と `docker run hello-world` の、2つのコマンドを実行し、バージョン情報と、「Hello from Docker!」のメッセージが表示されることを確認する。

これで、あなたのPCは、コンテナを自在に操るための、準備が整いました。次のセクションでは、Dockerを操作するための、基本的なコマンドについて、学んでいきましょう。

---

## 📝 学習のポイント

- [ ] 自分のPCに、Docker Desktopをインストールできる。
- [ ] `docker --version` コマンドで、インストールが成功したことを確認できる。
- [ ] `docker run hello-world` コマンドを実行し、Dockerが正常に動作していることを確認できる。

---

## 参考文献

[1] Docker. (2022). *Docker is Updating and Extending Our Product Subscriptions*. [https://www.docker.com/blog/updating-product-subscriptions/](https://www.docker.com/blog/updating-product-subscriptions/)
