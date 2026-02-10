const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CURRICULUMS_DIR = path.join(process.cwd(), 'curriculums');
const IMAGE_DIR = path.join(process.cwd(), 'image');

const S3_BUCKET = process.env.S3_BUCKET;
const S3_PUBLIC_BASE_URL = process.env.S3_PUBLIC_BASE_URL;
const AWS_REGION = process.env.AWS_REGION;

const IMG_TAG_REGEX = /<img\s[^>]*?>/gi;

/**
 * img タグから指定属性の値を取得する
 */
function extractAttribute(tag, attrName) {
  const regex = new RegExp(`${attrName}\\s*=\\s*["']([^"']*)["']`, 'i');
  const match = tag.match(regex);
  return match ? match[1] : null;
}

/**
 * ディレクトリを再帰走査して .md ファイルのパスを返す
 */
function collectMarkdownFiles(dirPath) {
  const results = [];
  const entries = fs.readdirSync(dirPath, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(dirPath, entry.name);
    if (entry.isDirectory()) {
      results.push(...collectMarkdownFiles(fullPath));
    } else if (entry.isFile() && entry.name.endsWith('.md')) {
      results.push(fullPath);
    }
  }
  return results;
}

/**
 * Markdown コンテンツから src="" または src='' の img タグを抽出する
 */
function findEmptySrcImgTags(content) {
  const matches = [];
  let match;
  IMG_TAG_REGEX.lastIndex = 0;
  while ((match = IMG_TAG_REGEX.exec(content)) !== null) {
    const tag = match[0];
    const src = extractAttribute(tag, 'src');
    const alt = extractAttribute(tag, 'alt');
    if (src === '') {
      matches.push({ fullMatch: tag, src, alt });
    }
  }
  return matches;
}

/**
 * 画像ファイルを S3 にアップロードし、公開 URL を返す
 */
function uploadToS3(localPath, filename) {
  const s3Uri = `s3://${S3_BUCKET}/${filename}`;

  try {
    execSync(`aws s3 cp "${localPath}" "${s3Uri}" --region "${AWS_REGION}"`, {
      stdio: 'pipe',
    });
  } catch (error) {
    throw new Error(
      `S3アップロード失敗: ${filename} - ${error.stderr?.toString().trim() || error.message}`
    );
  }

  const baseUrl = S3_PUBLIC_BASE_URL.replace(/\/+$/, '');
  return `${baseUrl}/${filename}`;
}

function main() {
  // 1. 環境変数バリデーション
  if (!S3_BUCKET || !S3_PUBLIC_BASE_URL || !AWS_REGION) {
    console.error('エラー: S3_BUCKET, S3_PUBLIC_BASE_URL, AWS_REGION が必要です');
    process.exit(1);
  }

  // 2. Markdown ファイルを収集
  const mdFiles = collectMarkdownFiles(CURRICULUMS_DIR);
  console.log(`\n=== 対象Markdownファイル数: ${mdFiles.length} ===\n`);

  let totalImgTags = 0;
  let totalUploads = 0;
  let totalReplacements = 0;
  const errors = [];

  // 重複アップロード防止用 Map（filename -> s3Url）
  const uploadedFiles = new Map();

  // 3. 各ファイルを処理
  for (const filePath of mdFiles) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const imgTags = findEmptySrcImgTags(content);

    if (imgTags.length === 0) continue;

    const relPath = path.relative(process.cwd(), filePath);
    console.log(`処理中: ${relPath} (${imgTags.length}件の src="" の img タグ)`);
    totalImgTags += imgTags.length;

    let updatedContent = content;

    for (const { fullMatch, src, alt } of imgTags) {
      // alt 属性の検証
      if (!alt) {
        errors.push(`alt属性なし: ${relPath} 内の img タグ`);
        continue;
      }

      // image/ 配下に対応ファイルがあるか確認
      const imagePath = path.join(IMAGE_DIR, alt);
      if (!fs.existsSync(imagePath)) {
        errors.push(`画像ファイルが見つかりません: image/${alt} (${relPath})`);
        continue;
      }

      // S3 アップロード（重複はスキップ）
      let s3Url;
      if (uploadedFiles.has(alt)) {
        s3Url = uploadedFiles.get(alt);
      } else {
        try {
          s3Url = uploadToS3(imagePath, alt);
          uploadedFiles.set(alt, s3Url);
          totalUploads++;
          console.log(`  S3アップロード成功: ${alt}`);
        } catch (err) {
          errors.push(err.message);
          continue;
        }
      }

      // src を S3 URL に置換（src="" / src='' を正規表現で置換）
      const newTag = fullMatch.replace(/src\s*=\s*["'][^"']*["']/, `src="${s3Url}"`);
      updatedContent = updatedContent.split(fullMatch).join(newTag);
      totalReplacements++;
    }

    // 変更があればファイルに書き戻す
    if (updatedContent !== content) {
      fs.writeFileSync(filePath, updatedContent, 'utf-8');
      console.log(`  ファイル更新完了: ${relPath}`);
    }
  }

  // 4. サマリーログ
  console.log('\n=== 処理結果サマリー ===');
  console.log(`対象Markdownファイル数: ${mdFiles.length}`);
  console.log(`対象imgタグ数(src=""): ${totalImgTags}`);
  console.log(`S3アップロード成功数: ${totalUploads}`);
  console.log(`置換成功数: ${totalReplacements}`);

  // 5. エラーがあれば失敗終了
  if (errors.length > 0) {
    console.error('\n=== エラー一覧 ===');
    for (const err of errors) {
      console.error(`  - ${err}`);
    }
    process.exit(1);
  }

  console.log('\n処理完了');
}

main();
