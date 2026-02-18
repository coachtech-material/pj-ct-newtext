# 6-1-1: HTTPリクエスト/レスポンス

## リサーチ結果

**検索キーワード**: HTTP request response cycle diagram flow

**標準的な構図パターン**:
- Client（ブラウザ）と Server の2つの主体
- Request: Client → Server（右向き矢印）
- Response: Server → Client（左向き矢印）
- メソッド（GET, POST等）とステータスコード（200, 404等）

**参考**: [Turing School - Request/Response Cycle](https://backend.turing.edu/module2/lessons/how_the_web_works_http), [GeeksforGeeks - Request Response in Express.js](https://www.geeksforgeeks.org/web-tech/request-and-response-cycle-in-express-js/)

---

## プロンプト

```
HTTPリクエスト/レスポンスサイクルを図解してください。

## 構成要素
左側: Client（クライアント）
- パソコン/ブラウザのアイコン
- 「ユーザーのブラウザ」

右側: Server（サーバー）
- サーバーラックのアイコン
- 「Webサーバー」

## 矢印とデータフロー
上の矢印（右向き）: HTTP Request
- 「GET /users HTTP/1.1」
- メソッド: GET, POST, PUT, DELETE
- URL, Headers, Body

下の矢印（左向き）: HTTP Response
- 「HTTP/1.1 200 OK」
- ステータスコード: 200, 404, 500
- Headers, Body（HTML/JSON）

## スタイル
- シンプルな通信図
- 背景は白
- Request矢印は青
- Response矢印は緑
- 各要素のラベルは英語で大きく
```

## 構図イメージ

```
                          HTTP Request
                    GET /users HTTP/1.1
            ─────────────────────────────────→
┌─────────────┐                              ┌─────────────┐
│   Client    │                              │   Server    │
│     🖥️      │                              │     🖧      │
│  ブラウザ    │                              │  Webサーバー │
└─────────────┘                              └─────────────┘
            ←─────────────────────────────────
                    HTTP/1.1 200 OK
                      HTML / JSON
                          HTTP Response
```

## 挿入情報

- ファイル: `curriculums/tutorial-6.../6-1-1_http_basics.md`
- 画像ファイル名: `6-1-1_c1.png`
