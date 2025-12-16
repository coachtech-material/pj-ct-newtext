# Tutorial 11-1-4: 開発環境の準備

## 🎯 このセクションで学ぶこと

*   Docker環境を構築し、Laravelプロジェクトをセットアップする方法を学ぶ。
*   phpMyAdminでデータベースに接続する方法を学ぶ。
*   開発環境の動作確認を行う。

---

## 導入：なぜDocker環境が必要なのか

**Docker**とは、**アプリケーションをコンテナという単位で実行する技術**です。

Docker環境を使うことで、以下のようなメリットがあります。

*   **環境の統一**: 開発環境、本番環境を同じ構成にできる
*   **セットアップが簡単**: 複雑な環境構築を自動化できる
*   **チーム開発がスムーズ**: 全員が同じ環境で開発できる

---

## 詳細解説

## Step 1: 必要なツール

開発環境を構築するために、以下のツールが必要です。

*   **Docker Desktop**: Dockerを実行するためのツール
*   **Git**: バージョン管理システム
*   **テキストエディタ**: VS Code、PhpStormなど

---

## Step 2: Docker Desktopのインストール

Docker Desktopをインストールします。

**Windows / Mac**:

1. [Docker Desktop](https://www.docker.com/products/docker-desktop)の公式サイトからダウンロード
2. インストーラーを実行
3. Docker Desktopを起動

**Linux**:

```bash
# Docker Engineをインストール
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io
```

---

## Step 3: Laravelプロジェクトの作成

Laravelプロジェクトを作成します。

```bash
composer create-project laravel/laravel task-manager
cd task-manager
```

---

## Step 4: Laravel Sailのインストール

**Laravel Sail**は、**Laravelの公式Docker環境**です。

Sailを使うことで、簡単にDocker環境を構築できます。

```bash
composer require laravel/sail --dev
```

---

## Step 5: Sailの初期化

Sailを初期化します。

```bash
php artisan sail:install
```

以下のサービスを選択します（スペースキーで選択、Enterで決定）。

*   `mysql`: データベース
*   `redis`: キャッシュ（オプション）
*   `meilisearch`: 検索エンジン（オプション）
*   `mailpit`: メールテスト（オプション）

このセクションでは、`mysql`のみを選択します。

---

## Step 6: docker-compose.ymlの確認

`docker-compose.yml`ファイルが作成されます。

**ファイル**: `docker-compose.yml`

```yaml
services:
    laravel.test:
        build:
            context: ./vendor/laravel/sail/runtimes/8.3
            dockerfile: Dockerfile
            args:
                WWWGROUP: '${WWWGROUP}'
        image: sail-8.3/app
        extra_hosts:
            - 'host.docker.internal:host-gateway'
        ports:
            - '${APP_PORT:-80}:80'
            - '${VITE_PORT:-5173}:${VITE_PORT:-5173}'
        environment:
            WWWUSER: '${WWWUSER}'
            LARAVEL_SAIL: 1
            XDEBUG_MODE: '${SAIL_XDEBUG_MODE:-off}'
            XDEBUG_CONFIG: '${SAIL_XDEBUG_CONFIG:-client_host=host.docker.internal}'
            IGNITION_LOCAL_SITES_PATH: '${PWD}'
        volumes:
            - '.:/var/www/html'
        networks:
            - sail
        depends_on:
            - mysql
    mysql:
        image: 'mysql/mysql-server:8.0'
        ports:
            - '${FORWARD_DB_PORT:-3306}:3306'
        environment:
            MYSQL_ROOT_PASSWORD: '${DB_PASSWORD}'
            MYSQL_ROOT_HOST: '%'
            MYSQL_DATABASE: '${DB_DATABASE}'
            MYSQL_USER: '${DB_USERNAME}'
            MYSQL_PASSWORD: '${DB_PASSWORD}'
            MYSQL_ALLOW_EMPTY_PASSWORD: 1
        volumes:
            - 'sail-mysql:/var/lib/mysql'
        networks:
            - sail
        healthcheck:
            test:
                - CMD
                - mysqladmin
                - ping
                - '-p${DB_PASSWORD}'
            retries: 3
            timeout: 5s
networks:
    sail:
        driver: bridge
volumes:
    sail-mysql:
        driver: local
```

---

## Step 7: phpMyAdminの追加

**phpMyAdmin**は、**データベースを視覚的に管理するツール**です。

`docker-compose.yml`にphpMyAdminを追加します。

**ファイル**: `docker-compose.yml`

```yaml
services:
    laravel.test:
        # ...（既存の設定）
    mysql:
        # ...（既存の設定）
    phpmyadmin:
        image: phpmyadmin/phpmyadmin
        ports:
            - '8080:80'
        environment:
            PMA_HOST: mysql
            PMA_USER: '${DB_USERNAME}'
            PMA_PASSWORD: '${DB_PASSWORD}'
        networks:
            - sail
        depends_on:
            - mysql
networks:
    sail:
        driver: bridge
volumes:
    sail-mysql:
        driver: local
```

---

## Step 8: .envファイルの設定

`.env`ファイルで、データベースの設定を確認します。

**ファイル**: `.env`

```env
DB_CONNECTION=mysql
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE=task_manager
DB_USERNAME=sail
DB_PASSWORD=password
```

---

## Step 9: Docker環境の起動

Docker環境を起動します。

```bash
./vendor/bin/sail up -d
```

`-d`オプションは、バックグラウンドで実行するオプションです。

---

## Step 10: エイリアスの設定（オプション）

毎回`./vendor/bin/sail`と入力するのは面倒なので、エイリアスを設定します。

**Bash（Linux / Mac）**:

```bash
echo "alias sail='./vendor/bin/sail'" >> ~/.bashrc
source ~/.bashrc
```

**Zsh（Mac）**:

```bash
echo "alias sail='./vendor/bin/sail'" >> ~/.zshrc
source ~/.zshrc
```

これで、`sail up -d`と入力するだけで起動できます。

---

## Step 11: Laravelの動作確認

ブラウザで `http://localhost` にアクセスし、Laravelのウェルカムページが表示されることを確認します。

---

## Step 12: phpMyAdminの動作確認

ブラウザで `http://localhost:8080` にアクセスし、phpMyAdminが表示されることを確認します。

**ログイン情報**:

*   **ユーザー名**: `sail`
*   **パスワード**: `password`

ログイン後、`task_manager`データベースが表示されることを確認します。

---

## Step 13: マイグレーションの実行

データベースにテーブルを作成します。

```bash
sail artisan migrate
```

phpMyAdminで、`users`テーブルなどが作成されていることを確認します。

---

## Step 14: Docker環境の停止

Docker環境を停止します。

```bash
sail down
```

---

### 💡 TIP: Sailコマンド一覧

よく使うSailコマンドをまとめます。

| コマンド | 説明 |
|---|---|
| `sail up -d` | Docker環境を起動（バックグラウンド） |
| `sail down` | Docker環境を停止 |
| `sail artisan` | Artisanコマンドを実行 |
| `sail composer` | Composerコマンドを実行 |
| `sail npm` | npmコマンドを実行 |
| `sail mysql` | MySQLに接続 |
| `sail shell` | コンテナ内のシェルに接続 |

---

### 🚨 よくある間違い

#### 間違い1: Docker Desktopが起動していない

**対処法**: Docker Desktopを起動します。

---

#### 間違い2: ポートが既に使用されている

**エラーメッセージ**:

```
Error: Port 80 is already in use
```

**対処法**: `.env`ファイルで、`APP_PORT`を変更します。

```env
APP_PORT=8000
```

---

#### 間違い3: データベースに接続できない

**対処法**: `.env`ファイルの`DB_HOST`が`mysql`になっていることを確認します。

---

## ✨ まとめ

このセクションでは、開発環境の準備について学びました。

*   Docker Desktopをインストールし、Laravel Sailを使ってDocker環境を構築した。
*   phpMyAdminを追加し、データベースを視覚的に管理できるようにした。
*   マイグレーションを実行し、データベースにテーブルを作成した。

次のセクションでは、Git/GitHubの準備について学びます。

---

## 📝 学習のポイント

- [ ] Docker環境を構築した。
- [ ] phpMyAdminでデータベースに接続した。
- [ ] マイグレーションを実行した。
- [ ] Sailコマンドを使えるようになった。
