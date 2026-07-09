---
name: lms-sync
description: 教材をLMS（学習管理システム）に反映・公開するときの運用手順。「LMSに反映したい」「教材を公開／デプロイして」「stagingに同期して」「本番に反映して」「画像をS3にアップして」「GitHub Actionを回して教材を更新して」などで必ず使う。main=本番LMS / staging=Staging LMS の対応、GitHub Actions 4本（画像S3置換×2・教材同期×2）の実行順序・実行方法・確認方法を案内する。教材の反映・同期・公開・画像URL置換に関わる依頼なら、明示的にワークフロー名を言われなくても使うこと。
---

# 教材のLMS公開（同期）手順 (lms-sync)

教材は GitHub Actions を手動実行して LMS に反映します。**必ず staging で確認してから main（本番）に反映**します。事故を防ぐため、順番と確認を省かないでください。

## ブランチと環境の対応

| ブランチ | 反映先 |
|:--|:--|
| `staging` | Staging（検証用）LMS |
| `main` | 本番（Production）LMS |

`main` と `staging` は自動同期されません。手動でPR/マージして反映を進めます。

## ワークフロー一覧（すべて手動実行 = workflow_dispatch）

| ワークフローファイル | 対象ブランチ | 役割 |
|:--|:--|:--|
| `replace-image-links-staging.yml` | staging | 画像をS3にアップし `src=""` をURLに置換 |
| `sync-curriculums-staging.yml` | staging | 教材をStaging LMSに登録・更新 |
| `replace-image-links-main.yml` | main | 画像をS3にアップし `src=""` をURLに置換 |
| `sync-curriculums-production.yml` | main | 教材を本番LMSに登録・更新 |

- **画像置換**は `image/{alt}` を S3 にアップし、本文の `<img src="">` を S3 URL に書き換えます。変更があると **`chore/replace-image-links-*` ブランチを作って push する**ので、そのPRを手動で確認・マージする必要があります（対象画像が無ければPRは作られません）。
- **教材同期**は `curriculums/` 配下を読み、LMSのAPIに送信します。
- AWS認証・S3・LMS APIのURL/キー等の Secrets / Variables は**管理者がGitHubに設定済み**です。新メンバーが値を触る必要はありません。

## 推奨手順（staging で検証 → main へ）

1. 修正内容のPRを **staging** にマージする。
2. 「画像リンク置換（staging）」を実行する。
   ```bash
   gh workflow run replace-image-links-staging.yml
   gh run watch   # 実行状況を確認
   ```
   → 自動作成された `chore/replace-image-links-*` のPRを確認し、**staging にマージ**する。
3. 「教材同期（staging）」を実行する。
   ```bash
   gh workflow run sync-curriculums-staging.yml
   ```
   → **Staging LMS で表示を確認**する。
4. 問題なければ **staging の内容を main に反映**する（PR/マージ）。
5. 「画像リンク置換（main）」を実行し、`chore/replace-image-links-*` PR を **main にマージ**する。
   ```bash
   gh workflow run replace-image-links-main.yml
   ```
6. 「教材同期（main）」を実行し、**本番LMSで表示を確認**する。
   ```bash
   gh workflow run sync-curriculums-production.yml
   ```

> 画面から実行する場合: GitHub の「Actions」タブ → 対象ワークフロー → 「Run workflow」→ ブランチを選択 → 実行。

## 実行結果の確認

```bash
gh run list --workflow=sync-curriculums-staging.yml   # 実行履歴
gh run view {RUN_ID} --log                            # ログ
```

同期ログには収集件数（`Collected: X curriculums, Y chapters, Z sections`）とAPIのHTTPステータスコードが出ます。

## つまずきやすい点

- 画像置換が失敗する主因は「`alt` が空」または「`image/` に対応ファイルが無い」。エラーログに該当ファイルが出るので、`image/` にファイルを追加するか `alt` を修正して再実行する。
- 画像を追加・変更したら、**教材同期の前に必ず画像置換を実行**する（本文の `src` が空のまま同期されるのを防ぐ）。
- 詳細は `.github/README.md` を参照。
