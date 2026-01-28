# Tutorial 9-1-7: 環境構築ハンズオン

## 📝 このセクションの目的

Tutorial 9と10のハンズオンで使用する`laravel-practice`ディレクトリを作成し、Laravel Sailを使った開発環境の構築手順を実践します。

> 💡 **このハンズオンのポイント**: 9-1-2で学んだLaravel Sailの知識を実際に手を動かして確認します。ここで構築する環境は、今後のハンズオンで繰り返し使用します。

---

## 📁 laravel-practiceディレクトリの全体像

`~/laravel-practice/`は、Tutorial 9〜10の全ハンズオンで使用するディレクトリです。各ハンズオンごとにサブディレクトリを作成し、プロジェクトを管理します。

```
~/laravel-practice/
├── 9-1-7_hands-on/                       ← このハンズオン（環境構築確認用）
│   └── setup-app-practice/               ← 環境構築確認用プロジェクト
│
├── 9-1-8_hands-on/                       ← 次のハンズオン（Laravel基礎）
│   ├── profile-app-practice/             ← 自分で作成する用
│   └── profile-app-sample/               ← 実践で一緒に作成する用
│
├── 9-2-4_hands-on/                       ← Bladeハンズオン
│   ├── blade-app-practice/
│   └── blade-app-sample/
│
├── 9-3-5_hands-on/                       ← Eloquentハンズオン
│   ├── eloquent-app-practice/
│   └── eloquent-app-sample/
│
├── 9-4-5_hands-on/                       ← ルーティングハンズオン
│   ├── routing-app-practice/
│   └── routing-app-sample/
│
├── 9-5-5_hands-on/                       ← リレーションハンズオン
│   ├── relation-app-practice/
│   └── relation-app-sample/
│
├── 9-6-5_hands-on/                       ← バリデーションハンズオン
│   ├── validation-app-practice/
│   └── validation-app-sample/
│
└── 10-1-6_hands-on/                      ← 認証ハンズオン
    ├── auth-app-practice/
    └── auth-app-sample/
```

> 💡 **ポイント**: 各ハンズオンには「自分で作成する用（practice）」と「解答を確認する用（sample）」の2つのプロジェクトを作成します。自分で考えて作成したコードと、解答を見ながら作成したコードを比較することで、理解が深まります。

---

## 🎯 このハンズオンで作るもの

このハンズオンでは、環境構築が正しく行えることを確認するために、シンプルなLaravelプロジェクト（`setup-app-practice`）を作成します。

**完成の確認方法**:
- ブラウザで `http://localhost` にアクセスして、Laravelのウェルカムページが表示されればOK
- ブラウザで `http://localhost:8080` にアクセスして、phpMyAdminが表示されればOK

---

## 📝 ステップバイステップで環境構築

### 💭 実装の思考プロセス

Laravel Sailで環境を構築する際、以下の順番で進めます：

| 順番 | 作業 | 説明 |
|------|------|------|
| Step 1 | ディレクトリ作成 | `laravel-practice`ディレクトリを作成 |
| Step 2 | プロジェクト作成 | Laravel 10.xプロジェクトを作成 |
| Step 3 | Sailインストール | Laravel Sailをインストール |
| Step 4 | 設定ファイル生成 | `docker-compose.yml`を生成 |
| Step 5 | .env確認 | データベース接続情報を確認 |
| Step 6 | phpMyAdmin追加 | データベース管理ツールを追加 |
| Step 7 | Sail起動 | コンテナを起動 |
| Step 8 | エイリアス設定 | `sail`コマンドを短く使えるように設定 |
| Step 9 | キー生成 | アプリケーションキーを生成 |
| Step 10 | 動作確認 | ブラウザで表示を確認 |

---

### Step 1: laravel-practiceディレクトリを作成する

**何を考えているか**：
- 「Tutorial 9〜10のハンズオン用ディレクトリを作成しよう」
- 「ホームディレクトリ直下に`laravel-practice`を作成しよう」

> **📌 Dockerが起動していることを確認**
> 
> 以下のコマンドを実行する前に、Docker Desktop（またはDocker Engine）が起動していることを確認してください。

```bash
# ホームディレクトリに移動
cd ~

# laravel-practiceディレクトリを作成
mkdir -p laravel-practice

# 作成したディレクトリに移動
cd laravel-practice

# このハンズオン用のディレクトリを作成
mkdir -p 9-1-7_hands-on
cd 9-1-7_hands-on
```

**コマンド解説**：

| コマンド | 説明 |
|----------|------|
| `mkdir -p laravel-practice` | `laravel-practice`ディレクトリを作成します。`-p`オプションで、既に存在していてもエラーになりません。 |
| `mkdir -p 9-1-7_hands-on` | このハンズオン用のサブディレクトリを作成します。 |

---

### Step 2: Laravelプロジェクトを作成する

**何を考えているか**：
- 「Laravel 10.xのプロジェクトを作成しよう」
- 「プロジェクト名は`setup-app-practice`にしよう」

```bash
# Laravel 10.xプロジェクトを作成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer create-project laravel/laravel:^10.0 setup-app-practice
```

**コマンド解説**：

| オプション | 説明 |
|:---|:---|
| `--rm` | コマンド実行後、コンテナを自動削除 |
| `-u "$(id -u):$(id -g)"` | ホストマシンのユーザー権限でファイルを作成（権限問題を防ぐ） |
| `-v "$(pwd):/var/www/html"` | 現在のディレクトリをコンテナ内にマウント |
| `-w /var/www/html` | コンテナ内の作業ディレクトリを指定 |
| `-e COMPOSER_CACHE_DIR=/tmp/composer_cache` | Composerのキャッシュディレクトリを指定 |
| `laravelsail/php82-composer:latest` | Laravel Sail公式のPHP 8.2 + Composerイメージ |
| `composer create-project laravel/laravel:^10.0 setup-app-practice` | Laravel 10.xをインストール |

> ⚠️ **注意**: このコマンドは初回実行時に数分かかることがあります。Dockerイメージのダウンロードと、Laravelの依存パッケージのインストールが行われます。

---

### Step 3: Laravel Sailをインストールする

**何を考えているか**：
- 「作成したプロジェクトにLaravel Sailをインストールしよう」
- 「開発用の依存関係として追加しよう」

```bash
# プロジェクトディレクトリに移動
cd setup-app-practice

# Laravel Sailのインストール
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    composer require laravel/sail --dev
```

**コマンド解説**：

| コマンド | 説明 |
|----------|------|
| `composer require laravel/sail --dev` | Laravel Sailパッケージを**開発用依存関係**としてインストールします。 |

---

### Step 4: Sailの設定ファイルを生成する

**何を考えているか**：
- 「Sailの設定ファイル（docker-compose.yml）を生成しよう」
- 「MySQLを使用するように指定しよう」

```bash
# Sailの設定ファイルを生成
docker run --rm \
    -u "$(id -u):$(id -g)" \
    -v "$(pwd):/var/www/html" \
    -w /var/www/html \
    -e COMPOSER_CACHE_DIR=/tmp/composer_cache \
    laravelsail/php82-composer:latest \
    php artisan sail:install --with=mysql
```

このコマンドを実行すると、以下のファイルが生成されます：

- `docker-compose.yml`: Docker Composeの設定ファイル
- `.env`ファイルの更新: データベース接続情報が自動設定される

---

### Step 5: .envファイルを確認する

**何を考えているか**：
- 「データベース接続情報が正しく設定されているか確認しよう」

`.env`ファイルを開き、データベース接続情報が以下と一致していることを確認します：

```env
DB_CONNECTION=mysql
DB_HOST=mysql
DB_PORT=3306
DB_DATABASE=laravel
DB_USERNAME=sail
DB_PASSWORD=password
```

**重要なポイント**：

- `DB_HOST=mysql`: Docker Composeでは、サービス名（`mysql`）がホスト名として使えます。`localhost`ではないことに注意してください。
- `DB_USERNAME=sail`、`DB_PASSWORD=password`: Sailのデフォルト設定です。

---

### Step 6: phpMyAdminを追加する

**何を考えているか**：
- 「データベースをブラウザで管理できるようにphpMyAdminを追加しよう」

`docker-compose.yml`を開き、`mysql`サービスの後に以下の設定を追加します：

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

**設定の解説**：

| 項目 | 説明 |
|:---|:---|
| `image: 'phpmyadmin:latest'` | phpMyAdminの公式イメージを使用 |
| `ports: '${FORWARD_PHPMYADMIN_PORT:-8080}:80'` | ホストの8080番ポートでアクセス可能に |
| `PMA_HOST: mysql` | 接続先のMySQLサーバーを指定 |
| `PMA_USER`, `PMA_PASSWORD` | `.env`ファイルの値を使用 |
| `networks: - sail` | Sailのネットワークに参加 |
| `depends_on: - mysql` | MySQLが起動してから起動 |

---

### Step 7: Sailを起動する

**何を考えているか**：
- 「いよいよSailを起動しよう」
- 「バックグラウンドで実行しよう」

```bash
# Sailの起動
./vendor/bin/sail up -d
```

**コマンド解説**：

| コマンド | 説明 |
|----------|------|
| `./vendor/bin/sail` | Sailの実行ファイル |
| `up` | コンテナを起動 |
| `-d` | バックグラウンドで実行（デタッチモード） |

初回起動時は、Dockerイメージのビルドが行われるため、数分かかることがあります。

コンテナの状態を確認するには、以下のコマンドを実行します：

```bash
./vendor/bin/sail ps
```

全てのコンテナが`Up`状態になっていればOKです。

---

### Step 8: エイリアスを設定する（推奨）

**何を考えているか**：
- 「毎回`./vendor/bin/sail`と入力するのは面倒だ」
- 「エイリアスを設定して`sail`だけで実行できるようにしよう」

**Zshの場合**（macOS Catalina以降のデフォルト）

```bash
echo "alias sail='[ -f sail ] && bash sail || bash vendor/bin/sail'" >> ~/.zshrc
```

**Bashの場合**

```bash
echo "alias sail='[ -f sail ] && bash sail || bash vendor/bin/sail'" >> ~/.bashrc
```

設定を反映するために、シェルを再起動します：

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

### Step 9: アプリケーションキーを生成する

**何を考えているか**：
- 「Laravelのアプリケーションキーを生成しよう」
- 「これはセキュリティのために必要だ」

```bash
# アプリケーションキーの生成
./vendor/bin/sail artisan key:generate
```

> 💡 **ポイント**: エイリアスを設定済みの場合は、`sail artisan key:generate`と短く書けます。

このコマンドは、`.env`ファイルの`APP_KEY`に暗号化キーを設定します。このキーは、セッションや暗号化データの保護に使用されます。

---

### Step 10: 動作確認

**何を考えているか**：
- 「環境構築が正しく行えたか確認しよう」
- 「ブラウザでアクセスして表示を確認しよう」

**Laravelアプリケーションにアクセス**

ブラウザで以下のURLにアクセスしてください：

```
http://localhost
```

Laravelのウェルカム画面が表示されれば、環境構築は成功です！

**phpMyAdminにアクセス**

次に、phpMyAdminにアクセスして、データベースが正しく作成されているか確認しましょう：

```
http://localhost:8080
```

phpMyAdminの画面が表示され、`laravel`データベースが確認できればOKです。

---

## ✅ ディレクトリ構造の確認

環境構築が完了すると、以下のようなディレクトリ構造になっています：

```
~/laravel-practice/
└── 9-1-7_hands-on/
    └── setup-app-practice/     ← 今ここ
        ├── app/
        ├── bootstrap/
        ├── config/
        ├── database/
        ├── public/
        ├── resources/
        ├── routes/
        ├── storage/
        ├── tests/
        ├── vendor/
        ├── .env
        ├── artisan
        ├── composer.json
        ├── docker-compose.yml
        └── ...
```

---

## 🚀 まとめ

**ハンズオンお疲れ様でした！**

このハンズオンで、以下のことができるようになりました：

| 学んだこと | 説明 |
|------------|------|
| ディレクトリ構成の理解 | `laravel-practice`ディレクトリの全体像を把握 |
| Laravelプロジェクトの作成 | `docker run`コマンドでLaravel 10.xプロジェクトを作成 |
| Laravel Sailのインストール | `composer require laravel/sail --dev`でSailをインストール |
| Sailの設定ファイル生成 | `php artisan sail:install --with=mysql`で設定ファイルを生成 |
| phpMyAdminの追加 | `docker-compose.yml`にphpMyAdminを追加 |
| Sailの起動 | `sail up -d`でDockerコンテナを起動 |
| エイリアス設定 | `sail`コマンドを短く使えるように設定 |
| アプリケーションキー生成 | `sail artisan key:generate`でキーを生成 |

これで、Tutorial 9〜10のハンズオンで使用する環境が整いました。次のハンズオン（9-1-8）では、この環境を使ってLaravelの基礎（ルーティング → コントローラー → ビュー）を実践します。

---

## 🛑 Sailの停止

次のセクションに進む前に、Sailを停止しておきましょう。

```bash
./vendor/bin/sail down
```

> 💡 **なぜ停止するの？**: Sailを起動したままだと、次のセクションで別のプロジェクトを起動する際にポートが競合してエラーになることがあります。セクションの終わりには必ずSailを停止する習慣をつけましょう。

---
