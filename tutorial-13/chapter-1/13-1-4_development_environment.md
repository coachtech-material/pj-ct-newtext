# Tutorial 13-1-4: 開発環境の準備

## 🎯 このセクションで学ぶこと

- Docker環境を構築し、Laravelプロジェクトをセットアップする方法を学ぶ
- Tailwind CSS（Vite）を導入し、モダンなフロントエンド環境を構築する
- phpMyAdminでデータベースに接続する方法を学ぶ

---

## 導入：なぜDocker環境が必要なのか

**Docker**とは、**アプリケーションをコンテナという単位で実行する技術**です。

Docker環境を使うことで、以下のようなメリットがあります。

- **環境の統一**: 開発環境、本番環境を同じ構成にできる
- **セットアップが簡単**: 複雑な環境構築を自動化できる
- **チーム開発がスムーズ**: 全員が同じ環境で開発できる

---

## 詳細解説

## Step 1: 必要なツール

開発環境を構築するために、以下のツールが必要です。

- **Docker Desktop**: Dockerを実行するためのツール
- **Git**: バージョン管理システム
- **テキストエディタ**: VS Code推奨

---

## Step 2: Laravelプロジェクトの作成（Laravel 10.x）

以下のDockerコマンドを実行して、Laravel 10.xを明示的に指定してプロジェクトを作成します。

```bash
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 book-review-app
```

> 💡 **ポイント**: `laravel/laravel:^10.0`を指定することで、Laravel 10系の最新バージョンがインストールされます。

---

## Step 3: Laravel Sailのインストール

プロジェクト作成後、`book-review-app`ディレクトリに移動し、Laravel Sailをインストールします。

```bash
# プロジェクトディレクトリに移動
cd book-review-app

# Laravel Sailをインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev

# Sailの設定ファイルをパブリッシュ（MySQLを選択）
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql
```

---

## Step 4: フロントエンドのセットアップ（Vite & Tailwind CSS）

### 4-1. Sailの起動

まず、Sailを起動します。

```bash
./vendor/bin/sail up -d
```

### 4-2. NPM依存パッケージのインストール

```bash
sail npm install
```

### 4-3. Tailwind CSSのインストール

```bash
sail npm install -D tailwindcss@^3.4.0 postcss autoprefixer
```

### 4-4. 設定ファイルの生成

```bash
sail npx tailwindcss init -p
```

### 4-5. Tailwind CSSのテンプレートパス設定

`tailwind.config.js`を開き、`content`プロパティを以下のように設定します。

**ファイル**: `tailwind.config.js`

```javascript
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./resources/**/*.blade.php",
    "./resources/**/*.js",
    "./resources/**/*.vue",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

### 4-6. CSSファイルにTailwindディレクティブを追加

`resources/css/app.css`の中身を以下の3行に置き換えます。

**ファイル**: `resources/css/app.css`

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 4-7. Vite開発サーバーの起動

新しいターミナルを開いて実行します。**このコマンドは開発中、常に実行したままにしてください。**

```bash
sail npm run dev
```

> 🚨 **注意**: Tailwindのスタイルが適用されない場合は、`sail npm run dev`が実行されているか確認してください。

---

## Step 5: .envファイルとphpMyAdminの設定

### 5-1. .envファイルの確認

`.env`ファイルを開き、データベース接続情報が以下と一致していることを確認します。

**ファイル**: `.env`

```env
DB_CONNECTION=mysql
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=sail
DB_PASSWORD=password
```

### 5-2. phpMyAdminの追加

`compose.yaml`（または`docker-compose.yml`）を開き、`mysql`サービスの後に以下の設定を追加します。

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

---

## Step 6: Sailの起動とエイリアス設定

### 6-1. Sailの再起動

phpMyAdminを追加したので、Sailを再起動します。

```bash
sail down
sail up -d
```

### 6-2. エイリアス設定

毎回`./vendor/bin/sail`と入力するのは面倒なので、エイリアスを設定します。

**Zsh（Mac）の場合**:

```bash
echo "alias sail='[ -f sail ] && bash sail || bash vendor/bin/sail'" >> ~/.zshrc
exec $SHELL
```

**Bash（Linux）の場合**:

```bash
echo "alias sail='[ -f sail ] && bash sail || bash vendor/bin/sail'" >> ~/.bashrc
exec $SHELL
```

### 6-3. アプリケーションキーの生成

```bash
sail artisan key:generate
```

---

## Step 7: 動作確認

### 7-1. Laravelの動作確認

ブラウザで `http://localhost` にアクセスし、Laravelのウェルカムページが表示されることを確認します。

### 7-2. phpMyAdminの動作確認

ブラウザで `http://localhost:8080` にアクセスし、phpMyAdminが表示されることを確認します。

**ログイン情報**:
- **ユーザー名**: `sail`
- **パスワード**: `password`

### 7-3. マイグレーションの実行

```bash
sail artisan migrate
```

phpMyAdminで、`users`テーブルなどが作成されていることを確認します。

---

### 💡 TIP: Sailコマンド一覧

よく使うSailコマンドをまとめます。

| コマンド | 説明 |
|:---|:---|
| `sail up -d` | Docker環境を起動（バックグラウンド） |
| `sail down` | Docker環境を停止 |
| `sail artisan` | Artisanコマンドを実行 |
| `sail composer` | Composerコマンドを実行 |
| `sail npm` | npmコマンドを実行 |
| `sail npm run dev` | Vite開発サーバーを起動 |
| `sail mysql` | MySQLに接続 |

---

### 🚨 よくある間違い

#### 間違い1: Tailwindのスタイルが適用されない

**対処法**: `sail npm run dev`が実行されているか確認します。Vite開発サーバーが起動していないと、Tailwindのスタイルは適用されません。

```bash
# 別のターミナルで実行
sail npm run dev
```

---

#### 間違い2: Docker Desktopが起動していない

**対処法**: Docker Desktopを起動します。

---

#### 間違い3: ポートが既に使用されている

**エラーメッセージ**:

```
Error: Port 80 is already in use
```

**対処法**: `.env`ファイルで、`APP_PORT`を変更します。

```env
APP_PORT=8000
```

---

## ✨ まとめ

このセクションでは、開発環境の準備について学びました。

- Docker環境を構築し、Laravel 10.xプロジェクトを作成した
- Tailwind CSS（Vite）を導入し、モダンなフロントエンド環境を構築した
- phpMyAdminを追加し、データベースを視覚的に管理できるようにした

次のセクションでは、Git/GitHubの準備について学びます。

---
