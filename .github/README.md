# GitHub Actions ワークフロー

このディレクトリには、カリキュラムをLMSに同期するためのGitHub Actionsワークフローが含まれています。

## ワークフロー一覧

### 1. 教材の同期（Staging / Production）

| ワークフロー                      | 対象ブランチ | 内容                          |
| --------------------------------- | ------------ | ----------------------------- |
| `sync-curriculums-production.yml` | `main`       | 本番環境に教材を登録・更新    |
| `sync-curriculums-staging.yml`    | `staging`    | Staging環境に教材を登録・更新 |

**処理内容:**

- `curriculums/` 配下のMarkdownファイルを収集
- 教材データをJSON形式に整形
- LMS APIに送信して登録・更新

### 2. 画像リンクのS3置換

| ワークフロー                      | 対象ブランチ | 内容                                                |
| --------------------------------- | ------------ | --------------------------------------------------- |
| `replace-image-links-main.yml`    | `main`       | 画像をS3にアップロードしてリンクを置換（本番用）    |
| `replace-image-links-staging.yml` | `staging`    | 画像をS3にアップロードしてリンクを置換（staging用） |

**処理内容:**

- Markdown内の `<img src="" alt="ファイル名">` を検出
- `image/` ディレクトリから該当画像をS3にアップロード
- `src` をS3の公開URLに置換してPRを作成

## 実行方法

### 手動実行の手順

1. GitHubリポジトリの **「Actions」** タブを開く
2. 実行したいワークフローを選択
3. **「Run workflow」** ボタンをクリック
4. ブランチを選択（staging or main）
5. **「Run workflow」** をクリック

### 実行結果の確認

1. 「Actions」タブで実行したワークフローをクリック
2. ジョブの詳細を開いてログを確認
3. 主なログ出力:
   - 収集された教材数（Collected: X curriculums, Y chapters, Z sections）
   - API送信結果（HTTPステータスコード、レスポンス）

## 教材の構造

```
curriculums/
└── {チュートリアル名}/
    └── {チャプター名}/
        └── {セクション名}.md
```

**例:**

```
curriculums/
└── react-basics/              ← チュートリアル
    └── getting-started/        ← チャプター
        └── introduction.md     ← セクション
```
