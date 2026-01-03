# Tutorial 6-2-6: PHP実行環境の構築 - ハンズオン

## 🎯 このセクションで学ぶこと

*   Docker Composeを使って、実際にPHP実行環境を構築する。
*   `docker-compose.yml`を作成し、PHPコンテナを起動する。
*   ブラウザからPHPの動作を確認する。

---

## 導入

これまでのセクションで、Dockerの基本概念、コマンド、Docker Composeについて学んできました。このセクションでは、実際に手を動かして、**PHPが動作する環境**をDocker Composeで構築してみましょう。

このハンズオンを通じて、Docker Composeの設定ファイルの書き方と、コンテナの起動・停止の流れを、実践的に理解することができます。

---

## ハンズオン

### Step 1: プロジェクトフォルダの作成

まず、作業用のフォルダを作成します。ターミナル（Windowsの場合はPowerShell）を開き、以下のコマンドを実行してください。

```bash
# ホームディレクトリに移動
cd ~

# プロジェクトフォルダを作成
mkdir docker-php-demo

# フォルダに移動
cd docker-php-demo
```

### Step 2: PHPファイルの作成

次に、PHPの動作確認用のファイルを作成します。`docker-php-demo`フォルダ内に、`src`フォルダを作成し、その中に`index.php`ファイルを作成します。

```bash
# srcフォルダを作成
mkdir src
```

VSCodeなどのエディタで、`src/index.php`ファイルを作成し、以下の内容を記述してください。

```php
<?php
echo "<h1>Hello from Docker!</h1>";
echo "<p>PHPが正常に動作しています。</p>";
echo "<p>PHPバージョン: " . phpversion() . "</p>";
echo "<p>現在時刻: " . date("Y-m-d H:i:s") . "</p>";
?>
```

### Step 3: docker-compose.ymlの作成

`docker-php-demo`フォルダ直下に、`docker-compose.yml`ファイルを作成し、以下の内容を記述してください。

```yaml
version: '3.8'

services:
  php:
    image: php:8.2-apache
    ports:
      - "8080:80"
    volumes:
      - ./src:/var/www/html
```

この設定ファイルの意味を確認しましょう。

| 項目 | 説明 |
| :--- | :--- |
| `version: '3.8'` | Composeファイルのバージョン |
| `services:` | コンテナの定義を開始 |
| `php:` | サービス名（任意の名前） |
| `image: php:8.2-apache` | PHP 8.2とApache（Webサーバー）が含まれた公式イメージを使用 |
| `ports: - "8080:80"` | ホストの8080番ポートをコンテナの80番ポートに接続 |
| `volumes: - ./src:/var/www/html` | ホストの`src`フォルダをコンテナの`/var/www/html`に同期 |

### Step 4: フォルダ構成の確認

この時点で、フォルダ構成は以下のようになっているはずです。

```
docker-php-demo/
├── docker-compose.yml
└── src/
    └── index.php
```

### Step 5: コンテナの起動

いよいよコンテナを起動します。`docker-php-demo`フォルダで、以下のコマンドを実行してください。

```bash
docker-compose up -d
```

初回実行時は、PHPのイメージをダウンロードするため、少し時間がかかります。

**出力例:**
```
Creating network "docker-php-demo_default" with the default driver
Pulling php (php:8.2-apache)...
8.2-apache: Pulling from library/php
...
Creating docker-php-demo_php_1 ... done
```

### Step 6: 動作確認

Webブラウザを開き、以下のURLにアクセスしてください。

```
http://localhost:8080
```

「**Hello from Docker!**」というメッセージと、PHPのバージョン、現在時刻が表示されれば、成功です！

### Step 7: Docker Desktopでの確認

Docker Desktopを開いて、**Containers**メニューをクリックしてください。`docker-php-demo`というグループの中に、`php`コンテナが**緑色のアイコン（Running）**で表示されているはずです。

ここで、以下のことを確認してみましょう。

*   コンテナ名をクリックすると、**ログ**が表示される
*   「■」ボタンでコンテナを**停止**できる
*   「▶」ボタンでコンテナを**再起動**できる

### Step 8: ファイルの編集とリアルタイム反映

`volumes`の設定により、ホストOSのファイルとコンテナ内のファイルが同期されています。試しに、`src/index.php`を編集してみましょう。

```php
<?php
echo "<h1>Hello from Docker!</h1>";
echo "<p>PHPが正常に動作しています。</p>";
echo "<p>PHPバージョン: " . phpversion() . "</p>";
echo "<p>現在時刻: " . date("Y-m-d H:i:s") . "</p>";
echo "<p style='color: blue;'>ファイルを編集しました！</p>";
?>
```

ファイルを保存した後、ブラウザをリロードしてください。**コンテナを再起動することなく**、変更が反映されるはずです。これが`volumes`の便利なところです。

### Step 9: コンテナの停止

作業が終わったら、コンテナを停止しましょう。

```bash
docker-compose down
```

**出力例:**
```
Stopping docker-php-demo_php_1 ... done
Removing docker-php-demo_php_1 ... done
Removing network docker-php-demo_default
```

Docker Desktopを確認すると、コンテナが消えている（または停止状態になっている）ことがわかります。

---

## ✨ まとめ

このハンズオンでは、Docker Composeを使って、PHPの実行環境を構築しました。

| 手順 | 内容 |
| :--- | :--- |
| **Step 1-4** | プロジェクトフォルダ、PHPファイル、docker-compose.ymlを作成 |
| **Step 5** | `docker-compose up -d`でコンテナを起動 |
| **Step 6** | ブラウザで`http://localhost:8080`にアクセスして動作確認 |
| **Step 7** | Docker Desktopでコンテナの状態を確認 |
| **Step 8** | ファイルを編集し、リアルタイムで反映されることを確認 |
| **Step 9** | `docker-compose down`でコンテナを停止 |

**学んだこと:**

*   `docker-compose.yml`を作成し、サービスを定義する方法
*   `docker-compose up -d`でコンテナを起動する方法
*   `docker-compose down`でコンテナを停止する方法
*   Docker Desktopでコンテナの状態を確認する方法
*   `volumes`を使ってファイルを同期する方法

---
