# Tutorial 6-2-5: Laravel開発環境の構築

## 🎯 このセクションで学ぶこと

*   Docker Composeを使って、Laravelアプリケーションを動かすための、完全な開発環境を構築する。
*   Webサーバー（Nginx）、PHP実行環境（PHP-FPM）、データベース（MySQL）の、3つのコンテナが、どのように連携して動作するのかを理解する。
*   Laravel Sailという、Laravel公式のDocker環境構築ツールについて知る。

---

## 導入

お待たせしました！これまでのセクションで学んだ、DockerとDocker Composeの知識を総動員して、いよいよ、このカリキュラムの主役である、**Laravel**のための、開発環境を構築します。

ここで行う作業は、この先の、全てのチュートリアルで、基本となる、非常に重要なステップです。一つ一つの設定の意味を、しっかりと理解しながら、進めていきましょう。

目標は、`docker-compose up -d` というコマンド一発で、Nginx, PHP, MySQLの、3つのコンテナが起動し、ブラウザでアクセスすると、Laravelの、初期画面が表示される状態を作ることです。

---

## 詳細解説

### 📂 プロジェクトの準備

まず、`laravel-project`のような、プロジェクト用のディレクトリを、作成し、その中に移動します。

```bash
mkdir laravel-project
cd laravel-project
```

このディレクトリの中に、`docker-compose.yml`ファイルと、各サービスの設定ファイルを、作成していきます。

### 📝 `docker-compose.yml` の作成

プロジェクトのルートに、`docker-compose.yml`という名前のファイルを作成し、以下の内容を記述します。これは、Laravel開発環境のための、典型的な構成です。

```yaml
# docker-compose.yml

version: '3.8'

services:
  # Webサーバー (Nginx)
  nginx:
    image: nginx:latest
    ports:
      - "8000:80"
    volumes:
      - ./src:/var/www/html
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - php

  # PHP実行環境 (PHP-FPM)
  php:
    build:
      context: ./docker/php
    volumes:
      - ./src:/var/www/html

  # データベース (MySQL)
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: laravel_db
      MYSQL_USER: user
      MYSQL_PASSWORD: password
      MYSQL_ROOT_PASSWORD: root_password
    ports:
      - "3306:3306"
    volumes:
      - db-data:/var/lib/mysql

volumes:
  db-data:
```

**ポイント解説:**

*   `nginx`サービス:
    *   ホストの**8000番ポート**を、コンテナの80番ポートに繋ぎます。
    *   `volumes`で、2つのものをマウントしています。
        1.  `./src`ディレクトリを、`/var/www/html`にマウント。ここに、Laravelのソースコードを配置します。
        2.  `./docker/nginx/default.conf`という、Nginxの設定ファイルを、コンテナ内の設定ファイルに上書きします。
*   `php`サービス:
    *   `build`コンテキストを指定し、`./docker/php`ディレクトリにある`Dockerfile`を使って、カスタムイメージをビルドするように設定しています。これは、PHPに、Laravelが必要とする拡張機能（例: `pdo_mysql`）をインストールするためです。
*   `db`サービス:
    *   `environment`で、データベース名、ユーザー名、パスワードなどを設定しています。Laravel側で、この情報を使って、データベースに接続します。
    *   ホストの**3306番ポート**を、コンテナの3306番ポートに繋ぎます。これにより、TablePlusなどの、GUIツールから、データベースに接続できるようになります。

### 🛠️ 各サービスの設定ファイル

次に、`docker-compose.yml`から参照されている、設定ファイルを作成します。

1.  **Nginxの設定ファイル**

    `docker/nginx/default.conf` を作成します。

    ```nginx
    # docker/nginx/default.conf
    server {
        listen 80;
        server_name localhost;
        root /var/www/html/public;
        index index.php index.html;

        location / {
            try_files $uri $uri/ /index.php?$query_string;
        }

        location ~ \.php$ {
            fastcgi_pass php:9000;
            fastcgi_index index.php;
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        }
    }
    ```

    これは、全てのリクエストを、Laravelの入り口である、`public/index.php`に集めるための、お決まりの設定です。

2.  **PHPのDockerfile**

    `docker/php/Dockerfile` を作成します。

    ```dockerfile
    # docker/php/Dockerfile
    FROM php:8.1-fpm

    # Laravelが必要とするPHP拡張機能をインストール
    RUN docker-php-ext-install pdo_mysql
    ```

    ここでは、PHPの公式イメージをベースに、MySQLに接続するための、`pdo_mysql`拡張機能を、インストールしています。

### 🚀 Laravelのインストールと起動

全ての準備が整いました。いよいよ、Laravelをインストールし、環境を起動します。

1.  **Laravelのインストール**

    `docker-compose.yml`の`php`サービス定義を使って、`composer create-project`コマンドを実行し、`src`ディレクトリに、Laravelプロジェクトを作成します。

    ```bash
    docker-compose run --rm php composer create-project --prefer-dist laravel/laravel .
    ```

    `--rm`は、コマンド実行後に、一時的なコンテナを削除するオプションです。

2.  **環境の起動**

    いよいよ、アプリケーション全体を起動します。

    ```bash
    docker-compose up -d
    ```

3.  **動作確認**

    Webブラウザで、`http://localhost:8000` にアクセスしてください。Laravelの、美しい初期画面が表示されれば、大成功です！

### ⛵ Laravel Sailについて

実は、Laravel 8以降、**Laravel Sail**という、素晴らしいツールが、公式に提供されています。Sailは、Dockerベースの、Laravel開発環境を、コマンド一つで、自動的に構築してくれる、コマンドラインインターフェースです。

Sailを使えば、今回、手動で作成した、`docker-compose.yml`や、各設定ファイルを、ほぼ、自動で生成してくれます。

**では、なぜ、このカリキュラムでは、Sailを使わずに、手動で環境を構築したのでしょうか？**

それは、「**魔法の裏側を理解するため**」です。Sailは、非常に便利ですが、その裏側で、Nginx, PHP, MySQLのコンテナが、どのように連携しているのか、`docker-compose.yml`が、どのように書かれているのかを、理解しないまま使うと、何か問題が起きた時に、全く、手が出せなくなってしまいます。

今回、手動で、環境を構築した経験があるからこそ、あなたは、Sailが、何をしているのかを、深く理解し、必要に応じて、カスタマイズする力を、手に入れることができるのです。

---

## ✨ まとめ

このセクションでは、Docker Composeを使って、Laravelのための、完全な開発環境を、ゼロから構築しました。

*   **3つのコンテナ**: Webサーバー（Nginx）、PHP実行環境（PHP-FPM）、データベース（MySQL）の、3つのサービスを、`docker-compose.yml`で定義した。
*   **設定ファイルの役割**: Nginxに、リクエストを、PHPに流すように設定し、PHPに、MySQLと通信するための拡張機能をインストールした。
*   **ボリュームマウント**: ホストOSのソースコードや設定ファイルを、コンテナに同期させることで、柔軟な開発を可能にした。
*   **Laravel Sail**: Laravel公式の、Docker環境構築ツール。便利だが、その裏側の仕組みを理解することが、より重要である。

これで、あなたは、どんなPC上でも、コマンド一発で、同じLaravel開発環境を、再現できる、強力な武器を手に入れました。これこそが、Dockerがもたらす、最大のメリットの一つです。

---

## 📝 学習のポイント

- [ ] `docker-compose.yml`を使って、Nginx, PHP, MySQLの、3つのサービスを定義できる。
- [ ] 各サービスが、ボリュームマウントや、`depends_on`によって、どのように連携しているのかを説明できる。
- [ ] `docker-compose run`コマンドを使って、Laravelプロジェクトをインストールできる。
- [ ] `docker-compose up -d`コマンドで、環境を起動し、ブラウザで、Laravelの初期画面を表示できる。
- [ ] Laravel Sailが、どのようなツールであるかを説明できる。
