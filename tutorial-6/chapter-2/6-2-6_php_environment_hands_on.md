# Tutorial 6-2-6: PHP実行環境の構築 - ハンズオン

## 🎯 このセクションで学ぶこと

*   Docker Composeを使って、実際にPHP実行環境を構築する。
*   `docker-compose.yml`を作成し、PHPコンテナを起動する。
*   ブラウザからPHPの動作を確認する。

---

## 導入

これまでのセクションで、Dockerの基本概念、コマンド、Docker Composeについて学んできました。このセクションでは、実際に手を動かして、**PHPが動作する環境**をDocker Composeで構築してみましょう。

このハンズオンを通じて、Docker Composeの設定ファイルの書き方と、コンテナの起動・停止の流れを、実践的に理解することができます。

> 📌 **重要**: このハンズオンで作成する`php-practice`ディレクトリは、**Tutorial 7以降のPHP学習でも継続して使用**します。削除しないように注意してください。

---

## ハンズオン

### Step 1: プロジェクトフォルダの作成

まず、作業用のフォルダを作成します。ターミナル（Windowsの場合はPowerShell）を開き、以下のコマンドを実行してください。

```bash
# ホームディレクトリに移動
cd ~

# プロジェクトフォルダを作成
mkdir -p php-practice/src
mkdir -p php-practice/docker/nginx

# フォルダに移動
cd php-practice
```

### Step 2: Nginxの設定ファイルを作成

VSCodeなどのエディタで、`docker/nginx/default.conf`ファイルを作成し、以下の内容を記述してください。

```nginx
# docker/nginx/default.conf
server {
    listen 80;
    server_name localhost;
    root /var/www/html;
    index index.php index.html;

    location / {
        try_files $uri $uri/ /index.php?$query_string;
    }

    location ~ \.php$ {
        fastcgi_pass php:9000;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }
}
```

> 💡 **ポイント**: この設定ファイルは、「`.php`ファイルへのアクセスがあったら、PHP実行環境に処理を依頼する」という設定です。中身を完全に理解する必要はありません。

### Step 3: PHPファイルの作成

`src/index.php`ファイルを作成し、以下の内容を記述してください。

```php
<?php
echo "<h1>Hello from Docker!</h1>";
echo "<p>PHPが正常に動作しています。</p>";
echo "<p>PHPバージョン: " . phpversion() . "</p>";
echo "<p>現在時刻: " . date("Y-m-d H:i:s") . "</p>";
?>
```

### Step 4: docker-compose.ymlの作成

`php-practice`フォルダ直下に、`docker-compose.yml`ファイルを作成し、以下の内容を記述してください。

```yaml
version: '3.8'

services:
  nginx:
    image: nginx:latest
    ports:
      - "8000:80"
    volumes:
      - ./src:/var/www/html
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - php

  php:
    image: php:8.2-fpm
    volumes:
      - ./src:/var/www/html
```

この設定ファイルの意味を確認しましょう。

| 項目 | 説明 |
| :--- | :--- |
| `version: '3.8'` | Composeファイルのバージョン |
| `services:` | コンテナの定義を開始 |
| `nginx:` | Webサーバーのコンテナ |
| `php:` | PHP実行環境のコンテナ |
| `ports: - "8000:80"` | ホストの8000番ポートをコンテナの80番ポートに接続 |
| `volumes:` | ホストのファイルをコンテナ内で使えるようにする |
| `depends_on:` | nginxがphpコンテナに依存していることを示す |

### Step 5: フォルダ構成の確認

この時点で、フォルダ構成は以下のようになっているはずです。

```
php-practice/
├── docker/
│   └── nginx/
│       └── default.conf
├── docker-compose.yml
└── src/
    └── index.php
```

### Step 6: コンテナの起動

いよいよコンテナを起動します。`php-practice`フォルダで、以下のコマンドを実行してください。

```bash
docker-compose up -d
```

初回実行時は、イメージをダウンロードするため、少し時間がかかります。

**出力例:**
```
Creating network "php-practice_default" with the default driver
Pulling nginx (nginx:latest)...
Pulling php (php:8.2-fpm)...
Creating php-practice_php_1   ... done
Creating php-practice_nginx_1 ... done
```

### Step 7: 動作確認

Webブラウザを開き、以下のURLにアクセスしてください。

```
http://localhost:8000
```

「**Hello from Docker!**」というメッセージと、PHPのバージョン、現在時刻が表示されれば、成功です！

### Step 8: Docker Desktopでの確認

Docker Desktopを開いて、**Containers**メニューをクリックしてください。`php-practice`というグループの中に、`nginx`と`php`の2つのコンテナが**緑色のアイコン（Running）**で表示されているはずです。

ここで、以下のことを確認してみましょう。

*   コンテナ名をクリックすると、**ログ**が表示される
*   「■」ボタンでコンテナを**停止**できる
*   「▶」ボタンでコンテナを**再起動**できる

### Step 9: ファイルの編集とリアルタイム反映

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

### Step 10: コンテナの停止

作業が終わったら、コンテナを停止しましょう。

```bash
docker-compose down
```

**出力例:**
```
Stopping php-practice_nginx_1 ... done
Stopping php-practice_php_1   ... done
Removing php-practice_nginx_1 ... done
Removing php-practice_php_1   ... done
Removing network php-practice_default
```

Docker Desktopを確認すると、コンテナが消えている（または停止状態になっている）ことがわかります。

---

## ✨ まとめ

このハンズオンでは、Docker Composeを使って、PHPの実行環境を構築しました。

| 手順 | 内容 |
| :--- | :--- |
| **Step 1-5** | プロジェクトフォルダ、設定ファイル、PHPファイル、docker-compose.ymlを作成 |
| **Step 6** | `docker-compose up -d`でコンテナを起動 |
| **Step 7** | ブラウザで`http://localhost:8000`にアクセスして動作確認 |
| **Step 8** | Docker Desktopでコンテナの状態を確認 |
| **Step 9** | ファイルを編集し、リアルタイムで反映されることを確認 |
| **Step 10** | `docker-compose down`でコンテナを停止 |

**学んだこと:**

*   `docker-compose.yml`を作成し、サービスを定義する方法
*   `docker-compose up -d`でコンテナを起動する方法
*   `docker-compose down`でコンテナを停止する方法
*   Docker Desktopでコンテナの状態を確認する方法
*   `volumes`を使ってファイルを同期する方法

> 📌 **次のステップ**: この`php-practice`ディレクトリは、**Tutorial 7のPHP学習で継続して使用**します。削除せずに保持しておいてください。

---
