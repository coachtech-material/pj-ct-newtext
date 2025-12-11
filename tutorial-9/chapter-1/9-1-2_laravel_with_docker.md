# Tutorial 9-1-2: Docker環境でLaravelを動かそう

## 🎯 このセクションで学ぶこと

*   Docker Composeを使って、Laravel開発環境（Nginx、PHP、MySQL、phpMyAdmin）を構築できるようになる。
*   Laravelプロジェクトを作成し、ブラウザで「Welcome」画面を表示できるようになる。
*   Docker環境でのLaravel開発の流れ（コンテナの起動・停止、コマンド実行）を理解する。

---

## 導入：なぜDockerでLaravelを動かすのか？

Tutorial 6で学んだDockerは、開発環境を「コンテナ」という独立した箱の中で動かす技術でした。Laravelを動かすには、以下のような複数のソフトウェアが必要です。

*   **Webサーバー**（Nginx または Apache）
*   **PHPの実行環境**（PHP-FPM）
*   **データベース**（MySQL または PostgreSQL）
*   **データベース管理ツール**（phpMyAdmin）

これらを自分のPCに直接インストールすると、バージョンの違いや設定の複雑さで環境構築に失敗したり、他のプロジェクトと干渉したりする問題が起こります。しかし、Dockerを使えば、これらの環境を「設定ファイル1つ」で再現でき、チーム全員が同じ環境で開発できるようになります。

このセクションでは、Docker Composeを使って、Laravel開発に必要な環境を一気に構築し、実際にLaravelを動かしてみましょう。

---

## 詳細解説

### 🏗️ Laravel開発環境の全体像

今回構築する環境は、以下の4つのコンテナで構成されます。

| コンテナ名 | 役割 | ポート |
|:---|:---|:---|
| `nginx` | Webサーバー（HTTPリクエストを受け取り、PHPに渡す） | 8080 |
| `php` | PHPの実行環境（Laravelのコードを実行） | - |
| `mysql` | データベース（データを保存） | 3306 |
| `phpmyadmin` | データベース管理ツール（ブラウザでDBを操作） | 8081 |

これらのコンテナは、Docker Composeで一括管理され、`docker compose up`コマンド一つで全て起動します。

### 📁 プロジェクトディレクトリの作成

まず、Laravelプロジェクトを格納するディレクトリを作成します。

```bash
mkdir ~/laravel-tutorial
cd ~/laravel-tutorial
```

このディレクトリの中に、以下のファイルを作成していきます。

### 📝 `docker-compose.yml`の作成

Docker Composeの設定ファイルを作成します。VSCodeで`docker-compose.yml`を開き、以下の内容を記述してください。

```yaml
version: '3.8'

services:
  # Nginx（Webサーバー）
  nginx:
    image: nginx:latest
    container_name: laravel_nginx
    ports:
      - "8080:80"
    volumes:
      - ./src:/var/www/html
      - ./docker/nginx/default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - php
    networks:
      - laravel_network

  # PHP-FPM（PHPの実行環境）
  php:
    build:
      context: ./docker/php
    container_name: laravel_php
    volumes:
      - ./src:/var/www/html
    networks:
      - laravel_network

  # MySQL（データベース）
  mysql:
    image: mysql:8.0
    container_name: laravel_mysql
    environment:
      MYSQL_ROOT_PASSWORD: root
      MYSQL_DATABASE: laravel_db
      MYSQL_USER: laravel_user
      MYSQL_PASSWORD: laravel_pass
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
    networks:
      - laravel_network

  # phpMyAdmin（データベース管理ツール）
  phpmyadmin:
    image: phpmyadmin/phpmyadmin
    container_name: laravel_phpmyadmin
    environment:
      PMA_HOST: mysql
      PMA_USER: root
      PMA_PASSWORD: root
    ports:
      - "8081:80"
    depends_on:
      - mysql
    networks:
      - laravel_network

networks:
  laravel_network:
    driver: bridge

volumes:
  mysql_data:
```

**このファイルの重要なポイント**

*   `ports`: ホストマシン（あなたのPC）のポートと、コンテナ内のポートを紐付けます。`8080:80`は、「PCの8080番ポートにアクセスすると、コンテナの80番ポート（Nginx）に転送される」という意味です。
*   `volumes`: ホストマシンのディレクトリと、コンテナ内のディレクトリを同期します。`./src:/var/www/html`は、「PCの`src`ディレクトリと、コンテナの`/var/www/html`を同期する」という意味で、これによりPCでコードを編集すると、即座にコンテナ内に反映されます。
*   `depends_on`: コンテナの起動順序を制御します。`nginx`は`php`が起動してから起動するように設定されています。
*   `networks`: 全てのコンテナが同じネットワーク（`laravel_network`）に所属し、互いに通信できるようにします。

### 📝 Nginxの設定ファイル

Nginxの設定ファイルを作成します。以下のディレクトリ構造を作成してください。

```bash
mkdir -p docker/nginx
```

`docker/nginx/default.conf`を作成し、以下の内容を記述します。

```nginx
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
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        include fastcgi_params;
    }

    location ~ /\.ht {
        deny all;
    }
}
```

**このファイルの重要なポイント**

*   `root /var/www/html/public;`: Laravelの公開ディレクトリ（`public`）をドキュメントルートに設定します。
*   `try_files $uri $uri/ /index.php?$query_string;`: 存在しないURLへのアクセスを全て`index.php`にリダイレクトします。これにより、Laravelのルーティング機能が動作します。
*   `fastcgi_pass php:9000;`: PHPファイルの処理を、`php`コンテナの9000番ポート（PHP-FPM）に転送します。

### 📝 PHPのDockerfile

PHPコンテナのDockerfileを作成します。

```bash
mkdir -p docker/php
```

`docker/php/Dockerfile`を作成し、以下の内容を記述します。

```dockerfile
FROM php:8.2-fpm

# 必要なPHP拡張機能をインストール
RUN apt-get update && apt-get install -y \
    git \
    unzip \
    libpq-dev \
    libzip-dev \
    && docker-php-ext-install pdo_mysql zip

# Composerのインストール
COPY --from=composer:latest /usr/bin/composer /usr/bin/composer

# 作業ディレクトリの設定
WORKDIR /var/www/html
```

**このファイルの重要なポイント**

*   `FROM php:8.2-fpm`: PHP 8.2のFPM（FastCGI Process Manager）イメージをベースにします。
*   `docker-php-ext-install pdo_mysql zip`: LaravelがMySQLに接続するために必要な`pdo_mysql`拡張と、Composerが使う`zip`拡張をインストールします。
*   `COPY --from=composer:latest`: Composer（PHPの依存関係管理ツール）をインストールします。

### 🚀 Laravelプロジェクトの作成

Docker環境を起動する前に、まずLaravelプロジェクトを作成します。

```bash
# PHPコンテナをビルド（初回のみ）
docker compose build

# PHPコンテナを一時的に起動してLaravelをインストール
docker compose run --rm php composer create-project --prefer-dist laravel/laravel .
```

このコマンドは、`php`コンテナ内でComposerを実行し、Laravelの最新版を`src`ディレクトリにインストールします。

**⚠️ 注意**: このコマンドは数分かかることがあります。気長に待ちましょう。

**[ここに、コマンド実行中のスクリーンショットを挿入]**

インストールが完了すると、`src`ディレクトリにLaravelのファイルが展開されます。

### ⚙️ `.env`ファイルの設定

Laravelの環境設定ファイル`.env`を編集します。`src/.env`を開き、データベース接続の設定を以下のように変更してください。

```env
DB_CONNECTION=mysql
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE=laravel_db
DB_USERNAME=laravel_user
DB_PASSWORD=laravel_pass
```

**重要なポイント**

*   `DB_HOST=mysql`: Docker Composeでは、サービス名（`mysql`）がホスト名として使えます。
*   `DB_DATABASE`、`DB_USERNAME`、`DB_PASSWORD`は、`docker-compose.yml`で設定した値と一致させます。

### 🚀 Docker環境の起動

全ての設定が完了したら、Docker環境を起動します。

```bash
docker compose up -d
```

`-d`オプションは、バックグラウンドで起動することを意味します。

**[ここに、`docker compose up -d`実行後のスクリーンショットを挿入]**

コンテナが起動したら、以下のコマンドで状態を確認できます。

```bash
docker compose ps
```

全てのコンテナが`Up`状態になっていればOKです。

### 🌐 ブラウザでLaravelにアクセス

ブラウザで以下のURLにアクセスしてください。

```
http://localhost:8080
```

Laravelのウェルカム画面が表示されれば、環境構築は成功です！

**[ここに、Laravelのウェルカム画面のスクリーンショットを挿入]**

### 🗄️ phpMyAdminでデータベースを確認

次に、phpMyAdminにアクセスして、データベースが正しく作成されているか確認しましょう。

```
http://localhost:8081
```

ログイン情報は以下の通りです。

*   **サーバー**: `mysql`
*   **ユーザー名**: `root`
*   **パスワード**: `root`

ログインすると、`laravel_db`というデータベースが作成されていることが確認できます。

**[ここに、phpMyAdminのログイン画面とデータベース一覧のスクリーンショットを挿入]**

### 🛑 Docker環境の停止

作業が終わったら、以下のコマンドでコンテナを停止できます。

```bash
docker compose down
```

再度起動したい場合は、`docker compose up -d`を実行すればOKです。

---

## 💡 TIP: Docker環境でのコマンド実行

Laravelの開発では、`php artisan`コマンドを頻繁に使います。Docker環境では、コンテナ内でコマンドを実行する必要があります。

```bash
# 例：マイグレーションを実行
docker compose exec php php artisan migrate

# 例：キャッシュをクリア
docker compose exec php php artisan cache:clear
```

`docker compose exec php`は、「`php`コンテナ内でコマンドを実行する」という意味です。この後のセクションでは、この形式でコマンドを実行していきます。

---

## ✨ まとめ

このセクションでは、Docker Composeを使ってLaravel開発環境を構築しました。

*   Docker Composeの`docker-compose.yml`で、Nginx、PHP、MySQL、phpMyAdminの4つのコンテナを定義した。
*   Nginxの設定ファイルで、Laravelの`public`ディレクトリをドキュメントルートに設定し、PHPファイルの処理をPHP-FPMに転送するように設定した。
*   PHPのDockerfileで、LaravelがMySQLに接続するために必要な拡張機能とComposerをインストールした。
*   Composerを使ってLaravelプロジェクトを作成し、`.env`ファイルでデータベース接続を設定した。
*   `docker compose up -d`でコンテナを起動し、ブラウザで`http://localhost:8080`にアクセスして、Laravelのウェルカム画面を表示できた。

これで、Laravel開発の準備が整いました。次のセクションでは、Laravelのディレクトリ構成を理解し、どのファイルが何の役割を持っているのかを学んでいきます。

---

## 📝 学習のポイント

- [ ] Docker Composeで、複数のコンテナを一括管理できることを理解した。
- [ ] `docker compose up -d`でコンテナを起動し、`docker compose down`で停止できる。
- [ ] `docker compose exec php`を使って、コンテナ内でコマンドを実行できる。
- [ ] ブラウザで`http://localhost:8080`にアクセスし、Laravelのウェルカム画面を表示できた。
- [ ] phpMyAdminで、データベース`laravel_db`が作成されていることを確認できた。
