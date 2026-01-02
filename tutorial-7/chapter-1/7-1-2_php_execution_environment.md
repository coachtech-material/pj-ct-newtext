# Tutorial 7-1-2: PHPの実行環境

## 🎯 このセクションで学ぶこと

*   PHPのコードが、どのようにして実行され、ブラウザに表示されるのか、その一連の流れを理解する。
*   Dockerを使って、PHPを動かすための環境を構築する。
*   実際に、PHPのコードを書いて、ブラウザで確認してみる。

---

## 導入

前のセクションで、PHPがサーバーサイドで実行される言語であることを学びました。では、具体的に、「サーバーサイドで実行される」とは、どういうことなのでしょうか？

HTMLファイルであれば、PC上のファイルを、直接ブラウザで開けば、その内容が表示されました。しかし、PHPファイルは、同じように、直接ブラウザで開いても、`<?php ... ?>` というコードが、そのまま表示されてしまうだけで、意図した通りには動作しません。

PHPのコードを実行するには、**Webサーバー**と**PHP実行環境**という、2つの要素が必要です。このセクションでは、Dockerを使って、この環境を簡単に構築し、PHPを動かしてみましょう。

---

## 詳細解説

### 🎭 PHPが実行されるまでの流れ

ユーザーが、ブラウザで、PHPのページ（例: `index.php`）にアクセスしてから、その結果が、画面に表示されるまで、以下のような流れで処理が行われます。

1.  **リクエスト**: ユーザーのブラウザが、Webサーバーに対して、「`index.php`のページをください」という、リクエストを送信します。

2.  **PHPの実行**: Webサーバーは、アクセスされたファイルが `.php` であることを認識し、PHP実行環境に処理を依頼します。PHP実行環境は、`index.php`ファイルの内容を、上から順に解釈・実行します。

3.  **HTMLの生成**: PHPコードの実行結果（例: `echo`で出力された文字列など）が、HTMLに変換されます。

4.  **レスポンス**: 生成されたHTMLが、ユーザーのブラウザに送信されます。

5.  **表示**: ブラウザは、受け取ったHTMLを解釈し、画面に表示します。ブラウザから見れば、それが、元々、PHPファイルだったのか、静的なHTMLファイルだったのかは、区別がつきません。

```
[ブラウザ] → リクエスト → [Webサーバー] → [PHP実行環境] → HTMLを生成 → [ブラウザ]
```

### 🐳 Dockerで環境を構築しよう

PHPを動かすには、WebサーバーとPHP実行環境が必要ですが、Dockerを使えば、これらを簡単に用意できます。

今回は、以下の2つのコンテナを使います：

| コンテナ | 役割 |
|---------|------|
| **nginx** | Webサーバー。ブラウザからのリクエストを受け付けます |
| **php** | PHP実行環境。PHPコードを実行してHTMLを生成します |

難しい設定は不要です。以下の手順に従って、環境を構築しましょう。

### ✍️ 最初のPHPコードを書いてみよう

それでは、実際に、この環境で、PHPのコードを書いて、動かしてみましょう。

#### Step 1: プロジェクトの準備

まず、PHPを実行するための環境を準備します。以下の手順で、プロジェクトディレクトリを作成してください。

```bash
# プロジェクトディレクトリを作成
mkdir -p ~/php-practice/src
mkdir -p ~/php-practice/docker/nginx
cd ~/php-practice
```

次に、`docker-compose.yml`ファイルを作成します。

```yaml
# docker-compose.yml
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

**コードリーディング**：

| 設定 | 意味 |
|------|------|
| `nginx` | Webサーバーのコンテナです |
| `ports: "8000:80"` | ブラウザから`localhost:8000`でアクセスできるようにします |
| `volumes: ./src:/var/www/html` | `src`フォルダの中身をコンテナ内で使えるようにします |
| `php` | PHP実行環境のコンテナです |
| `depends_on: php` | nginxがphpコンテナに依存していることを示します |

次に、Nginxの設定ファイル（`docker/nginx/default.conf`）を作成します。

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

> 💡 **ポイント**: この設定ファイルは、「`.php`ファイルへのアクセスがあったら、PHP実行環境に処理を依頼する」という設定です。中身を完全に理解する必要はありません。「こういう設定が必要なんだな」程度で大丈夫です。

**✅ ディレクトリ構造の確認**

ここまでの作業が完了すると、以下のようなディレクトリ構造になっているはずです。確認してみましょう。

```
php-practice/
├── docker/
│   └── nginx/
│       └── default.conf    # Nginxの設定ファイル
├── src/                    # PHPファイルを置くディレクトリ（まだ空）
└── docker-compose.yml      # Dockerの設定ファイル
```

#### Step 2: 環境の起動

以下のコマンドで、環境を起動します。

```bash
cd ~/php-practice
docker-compose up -d
```

初回は、Dockerイメージのダウンロードに数分かかる場合があります。起動が完了したら、`docker-compose ps`コマンドで、コンテナが正常に起動していることを確認してください。

#### Step 3: PHPファイルの作成

`src`ディレクトリの中に、`index.php`というファイルを作成します。

```php
<?php
// src/index.php
?>
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>はじめてのPHP</title>
</head>
<body>
    <h1>PHPの世界へようこそ！</h1>
    <p>PHPを使って、動的なコンテンツを表示してみましょう。</p>
    <p>1 + 1 は、<?php echo 1 + 1; ?> です。</p>
    <p>現在の日時は、<?php echo date("Y年m月d日 H時i分s秒"); ?> です。</p>
</body>
</html>
```

#### Step 4: ブラウザで確認

Webブラウザで、`http://localhost:8000/index.php` にアクセスします。

画面に、「1 + 1 は、2 です。」や、現在の日時が、正しく表示されていれば、成功です！ブラウザの「ページのソースを表示」機能で、ソースコードを確認してみてください。`<?php ... ?>`の部分は、完全に消え、その実行結果である「2」や、日時の文字列に、置き換わっていることが、確認できるはずです。

> 💡 **環境の停止**: 作業が終わったら、`docker-compose down`コマンドで環境を停止できます。次回作業するときは、再び`docker-compose up -d`で起動してください。

**✅ 最終的なディレクトリ構造**

すべての作業が完了すると、以下のようなディレクトリ構造になります。この構造になっていれば正解です！

```
php-practice/
├── docker/
│   └── nginx/
│       └── default.conf    # Nginxの設定ファイル
├── src/
│   └── index.php           # 作成したPHPファイル
└── docker-compose.yml      # Dockerの設定ファイル
```

今後、Tutorial 7のハンズオン演習では、この`src/`ディレクトリ内にPHPファイルを作成していきます。

---

## ✨ まとめ

このセクションでは、PHPのコードが、サーバーの裏側で、どのように実行されるのか、その流れを学びました。

*   **PHPの実行フロー**: `ブラウザ → Webサーバー → PHP実行環境 → HTMLを生成 → ブラウザ` という流れで、処理が進む。
*   **Docker環境**: DockerでWebサーバー（nginx）とPHP実行環境（php）の2つのコンテナを起動することで、PHPを動かす環境を構築できる。
*   **動作確認**: `src`ディレクトリに、PHPファイルを作成し、`localhost:8000`にアクセスすることで、PHPが、正常に動作していることを確認した。

次のセクションから、いよいよ、PHPの、具体的な文法について、学んでいきましょう。

---
