# Tutorial 9-1-2: Docker環境でLaravelを動かそう（Laravel Sail）

## 🎯 このセクションで学ぶこと

*   **Laravel Sail**とは何か、なぜ使うのかを理解する。
*   Laravel Sailを使って、Laravel開発環境（PHP、MySQL、phpMyAdmin）を構築できるようになる。
*   Laravelプロジェクトを作成し、ブラウザで「Welcome」画面を表示できるようになる。
*   Sailコマンドの使い方と、エイリアス設定を理解する。

---

## 導入：Laravel Sailとは？

**Laravel Sail**は、LaravelがDocker環境を簡単に構築・管理するために提供する**公式ツール**です。Tutorial 6で学んだDockerの知識をベースに、Laravelに最適化された開発環境をコマンド一つで構築できます。

### なぜLaravel Sailを使うのか？

従来のDocker環境構築では、以下のような作業が必要でした。

*   `docker-compose.yml`を自分で書く
*   Nginx/ApacheのDockerfileを作成する
*   PHP拡張機能を手動でインストールする
*   各種設定ファイルを用意する

Laravel Sailを使えば、これらの作業が**全て自動化**されます。

| 比較項目 | 従来のDocker構築 | Laravel Sail |
|:---|:---|:---|
| 設定ファイル作成 | 手動で複数ファイル作成 | 自動生成 |
| PHP拡張機能 | 手動インストール | 事前に最適化済み |
| コマンド実行 | `docker compose exec php php artisan ...` | `sail artisan ...` |
| 学習コスト | 高い | 低い |
| Laravel最適化 | 自分で調整 | 公式が最適化済み |

> 💡 **ポイント**: Laravel Sailは、Dockerの複雑さを隠蔽しつつ、Laravelに最適化された環境を提供します。実務でも広く使われている標準的な開発環境です。ではなぜ、docker-copose.ymlを利用した環境構築を学んだかというと、チーム開発を行なっていく前提では最初からプロジェクトを立ち上げるsailよりも、途中からプロジェクトに参画した上で共有されたプロジェクトにあるdocker環境を利用することが多いです。したがって、docker-copose.ymlに記載されている内容や実行方法を学ぶ必要があったのです。

---

## 詳細解説

### 🏗️ Laravel Sail環境の全体像

Laravel Sailで構築される環境は、以下のコンテナで構成されます。

| コンテナ | 役割 | ポート |
|:---|:---|:---|
| `laravel.test` | PHP + Webサーバー（Laravelアプリケーション） | 80 |
| `mysql` | データベース（MySQLサーバー） | 3306 |
| `phpmyadmin` | データベース管理ツール（後で追加） | 8080 |

これらのコンテナは、`sail up`コマンド一つで全て起動します。

---

## 🚀 環境構築手順

### Step 1: Laravelプロジェクトの作成

まず、Laravelプロジェクトを管理するためのディレクトリを作成します。ホームディレクトリ直下にプロジェクトを作成すると散らかりやすいので、`laravel-practice`という専用ディレクトリを作成してその中で作業します。

```bash
# ホームディレクトリに移動
cd ~

# Laravelプロジェクト用のディレクトリを作成
mkdir laravel-practice

# 作成したディレクトリに移動
cd laravel-practice
```

> 💡 **ポイント**: `laravel-practice`ディレクトリの中に複数のLaravelプロジェクトを作成できます。今後、練習用のプロジェクトを作成する際も、このディレクトリ内で作業すると整理されます。

以下のDockerコマンドを実行して、**Laravel 10.x**を明示的に指定してプロジェクトを作成します。

```bash
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 laravel-project
```

**コマンドの解説**

| オプション | 説明 |
|:---|:---|
| `--rm` | コマンド実行後、コンテナを自動削除 |
| `-u "$(id -u):$(id -g)"` | ホストマシンのユーザー権限でファイルを作成（権限問題を防ぐ） |
| `-v "$(pwd):/var/www/html"` | 現在のディレクトリをコンテナ内にマウント |
| `-w /var/www/html` | コンテナ内の作業ディレクトリを指定 |
| `-e COMPOSER_CACHE_DIR=/tmp/composer_cache` | Composerのキャッシュディレクトリを指定 |
| `laravelsail/php82-composer:latest` | Laravel Sail公式のPHP 8.2 + Composerイメージ |
| `composer create-project laravel/laravel:^10.0 laravel-project` | Laravel 10.xをインストール |

> ⚠️ **注意**: このコマンドは初回実行時に数分かかることがあります。Dockerイメージのダウンロードと、Laravelの依存パッケージのインストールが行われます。

**[ここに、コマンド実行中のスクリーンショットを挿入]**

---

### Step 2: Laravel Sailのインストール

作成・移動したプロジェクトディレクトリ（laravel-practice）にて、Laravel Sailをインストールします。

```bash
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev
```

このコマンドは、Laravel Sailパッケージを**開発用依存関係**（`--dev`）としてインストールします。

---

### Step 3: Sailの設定ファイルをパブリッシュ

次に、Sailの設定ファイル（`docker-compose.yml`）を生成します。MySQLを使用するように指定します。

```bash
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql
```

このコマンドを実行すると、以下のファイルが生成されます。

*   `docker-compose.yml`: Docker Composeの設定ファイル
*   `.env`ファイルの更新: データベース接続情報が自動設定される

> 💡 **ポイント**: `--with=mysql`オプションで、MySQLを使用することを指定しています。他にも`pgsql`（PostgreSQL）、`redis`、`memcached`などを指定できます。

---

### Step 4: `.env`ファイルの確認

`.env`ファイルを開き、データベース接続情報が以下と一致していることを確認します。

```env
DB_CONNECTION=mysql
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=sail
DB_PASSWORD=password
```

**重要なポイント**

*   `DB_HOST=mysql`: Docker Composeでは、サービス名（`mysql`）がホスト名として使えます。`localhost`ではないことに注意してください。
*   `DB_USERNAME=sail`、`DB_PASSWORD=password`: Sailのデフォルト設定です。

---

### Step 5: phpMyAdminの追加

データベースをブラウザで管理できるように、phpMyAdminを追加します。

`docker-compose.yml`（または`compose.yaml`）を開き、`mysql`サービスの後に以下の設定を追加します。

```yaml
    phpmyadmin:
        image: 'phpmyadmin:latest'
        ports:
            - '${FORWARD_PHPMYADMIN_PORT:-8080}:80'
        environment:
            PMA_HOST: mysql
            PMA_USER: '${DB_USERNAME}'
            PMA_PASSWORD: '${DB_PASSWORD}'
        networks:
            - sail
        depends_on:
            - mysql
```

**設定の解説**

| 項目 | 説明 |
|:---|:---|
| `image: 'phpmyadmin:latest'` | phpMyAdminの公式イメージを使用 |
| `ports: '${FORWARD_PHPMYADMIN_PORT:-8080}:80'` | ホストの8080番ポートでアクセス可能に |
| `PMA_HOST: mysql` | 接続先のMySQLサーバーを指定 |
| `PMA_USER`, `PMA_PASSWORD` | `.env`ファイルの値を使用 |
| `networks: - sail` | Sailのネットワークに参加 |
| `depends_on: - mysql` | MySQLが起動してから起動 |

---

### Step 6: Sailの起動

いよいよSailを起動します。

```bash
./vendor/bin/sail up -d
```

*   `./vendor/bin/sail`: Sailの実行ファイル
*   `up`: コンテナを起動
*   `-d`: バックグラウンドで実行（デタッチモード）

**[ここに、`sail up -d`実行後のスクリーンショットを挿入]**

初回起動時は、Dockerイメージのビルドが行われるため、数分かかることがあります。

コンテナの状態を確認するには、以下のコマンドを実行します。

```bash
./vendor/bin/sail ps
```

全てのコンテナが`Up`状態になっていればOKです。

---

### Step 7: エイリアス設定（推奨）

毎回`./vendor/bin/sail`と入力するのは面倒なので、エイリアスを設定しましょう。

**Zshの場合**（macOS Catalina以降のデフォルト）

```bash
echo "alias sail='[ -f sail ] && bash sail || bash vendor/bin/sail'" >> ~/.zshrc
```

**Bashの場合**

```bash
echo "alias sail='[ -f sail ] && bash sail || bash vendor/bin/sail'" >> ~/.bashrc
```

設定を反映するために、シェルを再起動します。

```bash
exec $SHELL
```

これで、`sail`コマンドだけでSailを実行できるようになります。

```bash
# エイリアス設定前
./vendor/bin/sail up -d

# エイリアス設定後
sail up -d
```

---

### Step 8: アプリケーションキーの生成

Laravelのアプリケーションキーを生成します。

```bash
sail artisan key:generate
```

このコマンドは、`.env`ファイルの`APP_KEY`に暗号化キーを設定します。このキーは、セッションや暗号化データの保護に使用されます。

---

## 🌐 動作確認

### Laravelアプリケーションにアクセス

ブラウザで以下のURLにアクセスしてください。

```
http://localhost
```

Laravelのウェルカム画面が表示されれば、環境構築は成功です！

**[ここに、Laravelのウェルカム画面のスクリーンショットを挿入]**

### phpMyAdminにアクセス

次に、phpMyAdminにアクセスして、データベースが正しく作成されているか確認しましょう。

```
http://localhost:8080
```

phpMyAdminの画面が表示され、`laravel`データベースが確認できればOKです。

**[ここに、phpMyAdminの画面のスクリーンショットを挿入]**

---

## 🛠️ Sailコマンドリファレンス

Laravel Sailでは、様々なコマンドを簡単に実行できます。

### 基本コマンド

| コマンド | 説明 |
|:---|:---|
| `sail up` | コンテナを起動（フォアグラウンド） |
| `sail up -d` | コンテナを起動（バックグラウンド） |
| `sail down` | コンテナを停止・削除 |
| `sail stop` | コンテナを停止（削除しない） |
| `sail restart` | コンテナを再起動 |
| `sail ps` | コンテナの状態を確認 |

### Artisanコマンド

```bash
# マイグレーション実行
sail artisan migrate

# キャッシュクリア
sail artisan cache:clear

# ルート一覧表示
sail artisan route:list
```

### Composerコマンド

```bash
# パッケージインストール
sail composer require パッケージ名

# オートローダー再生成
sail composer dump-autoload
```

### NPMコマンド

```bash
# 依存パッケージインストール
sail npm install

# 開発サーバー起動
sail npm run dev

# 本番ビルド
sail npm run build
```

### データベース操作

```bash
# MySQLに接続
sail mysql

# データベースをリフレッシュ（全テーブル削除＆再作成）
sail artisan migrate:fresh
```

---

## 💡 TIP: よくあるトラブルと解決方法

### ポートが既に使用されている場合

エラーメッセージ: `Bind for 0.0.0.0:80 failed: port is already allocated`

**解決方法**: `.env`ファイルでポートを変更します。

```env
APP_PORT=8000
```

その後、`sail down`して`sail up -d`で再起動します。

### 権限エラーが発生する場合

エラーメッセージ: `Permission denied`

**解決方法**: 以下のコマンドで権限を修正します。

```bash
sail artisan storage:link
sudo chown -R $USER:$USER storage bootstrap/cache
```

### コンテナが起動しない場合

**解決方法**: ログを確認します。

```bash
sail logs
```

特定のコンテナのログを見る場合:

```bash
sail logs mysql
```

---

## 🔄 開発の流れ

Laravel Sailを使った開発の基本的な流れは以下の通りです。

```
1. sail up -d          # 開発開始時にコンテナを起動
2. コードを編集        # VSCodeなどでコードを編集
3. sail artisan ...    # 必要に応じてArtisanコマンドを実行
4. ブラウザで確認      # http://localhost で動作確認
5. sail down           # 開発終了時にコンテナを停止
```

---

## ✨ まとめ

このセクションでは、Laravel Sailを使ってLaravel開発環境を構築しました。

*   **Laravel Sail**は、Laravelが提供する公式のDocker開発環境ツールである。
*   `composer create-project`でLaravelプロジェクトを作成し、`composer require laravel/sail --dev`でSailをインストールした。
*   `php artisan sail:install --with=mysql`でSailの設定ファイルを生成し、MySQLを使用するように設定した。
*   `docker-compose.yml`にphpMyAdminを追加して、データベースをブラウザで管理できるようにした。
*   `sail up -d`でコンテナを起動し、`http://localhost`でLaravelのウェルカム画面を表示できた。
*   エイリアス設定により、`sail`コマンドで簡単にSailを操作できるようになった。

これで、Laravel開発の準備が整いました。次のセクションでは、Laravelのディレクトリ構成を理解し、どのファイルが何の役割を持っているのかを学んでいきます。

---

## 📚 参考リンク

*   [Laravel Sail 公式ドキュメント](https://laravel.com/docs/10.x/sail)
*   [Docker 公式ドキュメント](https://docs.docker.com/)
