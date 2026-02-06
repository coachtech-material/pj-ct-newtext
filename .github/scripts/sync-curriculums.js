const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const CURRICULUMS_DIR = path.join(process.cwd(), 'curriculums');

/**
 * ディレクトリ内のサブディレクトリ一覧を取得（ソート済み）
 */
function getDirectories(dirPath) {
  if (!fs.existsSync(dirPath)) {
    return [];
  }
  return fs.readdirSync(dirPath, { withFileTypes: true })
    .filter(dirent => dirent.isDirectory())
    .map(dirent => dirent.name)
    .sort();
}

/**
 * ディレクトリ内の .md ファイル一覧を取得（ソート済み）
 */
function getMarkdownFiles(dirPath) {
  if (!fs.existsSync(dirPath)) {
    return [];
  }
  return fs.readdirSync(dirPath, { withFileTypes: true })
    .filter(dirent => dirent.isFile() && dirent.name.endsWith('.md'))
    .map(dirent => dirent.name)
    .sort();
}

/**
 * カリキュラム情報を収集
 */
function collectCurriculums() {
  const curriculums = [];

  const curriculumDirs = getDirectories(CURRICULUMS_DIR);

  for (const curriculumTitle of curriculumDirs) {
    const curriculumPath = path.join(CURRICULUMS_DIR, curriculumTitle);
    const chapters = [];

    const chapterDirs = getDirectories(curriculumPath);

    for (const chapterTitle of chapterDirs) {
      const chapterPath = path.join(curriculumPath, chapterTitle);
      const sections = [];

      const markdownFiles = getMarkdownFiles(chapterPath);

      for (const mdFile of markdownFiles) {
        const sectionTitle = mdFile.replace(/\.md$/, '');
        const filePath = path.join(chapterPath, mdFile);
        const text = fs.readFileSync(filePath, 'utf-8');

        sections.push({
          title: sectionTitle,
          text: text
        });
      }

      if (sections.length > 0) {
        chapters.push({
          title: chapterTitle,
          sections: sections
        });
      }
    }

    if (chapters.length > 0) {
      curriculums.push({
        title: curriculumTitle,
        chapters: chapters
      });
    }
  }

  return curriculums;
}

/**
 * API に JSON データを送信
 */
function sendToApi(data, apiUrl, apiKey) {
  return new Promise((resolve, reject) => {
    const jsonData = JSON.stringify(data);
    const url = new URL(apiUrl + '/api/deploy/sections/upsert');
    const isHttps = url.protocol === 'https:';
    const client = isHttps ? https : http;

    const options = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname + url.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(jsonData),
        ...(apiKey && { 'Authorization': `Bearer ${apiKey}` })
      }
    };

    const req = client.request(options, (res) => {
      let responseBody = '';

      res.on('data', (chunk) => {
        responseBody += chunk;
      });

      res.on('end', () => {
        resolve({
          statusCode: res.statusCode,
          body: responseBody
        });
      });
    });

    req.on('error', (error) => {
      reject(error);
    });

    req.write(jsonData);
    req.end();
  });
}

/**
 * メイン処理
 */
async function main() {
  const apiUrl = process.env.API_URL;
  const apiKey = process.env.API_KEY;
  const workspaceId = process.env.WORKSPACE_ID;

  if (!apiUrl) {
    console.error('Error: API_URL is not set');
    process.exit(1);
  }

  if (!apiKey) {
    console.error('Error: API_KEY is not set');
    process.exit(1);
  }

  if (!workspaceId) {
    console.error('Error: WORKSPACE_ID is not set');
    process.exit(1);
  }

  console.log('=== Collecting curriculum data ===');
  const curriculums = collectCurriculums();

  const totalCurriculums = curriculums.length;
  const totalChapters = curriculums.reduce((sum, c) => sum + c.chapters.length, 0);
  const totalSections = curriculums.reduce(
    (sum, c) => sum + c.chapters.reduce((s, ch) => s + ch.sections.length, 0),
    0
  );

  console.log(`Collected: ${totalCurriculums} curriculums, ${totalChapters} chapters, ${totalSections} sections`);

  const payload = {
    workspaceId: workspaceId,
    curriculums: curriculums
  };

  console.log('\n=== Sending data to API ===');
  console.log(`API URL: ${apiUrl}`);

  try {
    const response = await sendToApi(payload, apiUrl, apiKey);

    console.log('\n=== API Response ===');
    console.log(`HTTP Status Code: ${response.statusCode}`);
    console.log('Response Body:');
    console.log(response.body);

    if (response.statusCode >= 200 && response.statusCode < 300) {
      console.log('\n✅ Successfully synced curriculums');
      process.exit(0);
    } else {
      console.error('\n❌ API request failed');
      process.exit(1);
    }
  } catch (error) {
    console.error('\n❌ Error sending data to API:');
    console.error(error.message);
    process.exit(1);
  }
}

main();
