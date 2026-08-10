const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

const CURRICULUMS_DIR = path.join(process.cwd(), 'curriculums');

/** リネーム台帳（任意）。存在すれば payload に renames を同梱する */
const RENAMES_FILE = path.join(process.cwd(), 'curriculum-renames.json');

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
 * リネーム台帳を読み込む
 *
 * ディレクトリ名・ファイル名を変更すると、title 基準の upsert では新規レコードになり
 * 学習進捗が引き継がれない。台帳を同梱すると LMS 側が upsert の前に title だけを
 * 更新する（行 ID は不変）。適用済みの指示は LMS 側で冪等にスキップされる。
 *
 * 台帳が無い場合は null を返し、従来どおり renames なしで送信する。
 */
function loadRenames() {
  if (!fs.existsSync(RENAMES_FILE)) {
    return null;
  }

  let parsed;
  try {
    parsed = JSON.parse(fs.readFileSync(RENAMES_FILE, 'utf-8'));
  } catch (error) {
    throw new Error(`curriculum-renames.json のJSONが不正です: ${error.message}`);
  }

  const renames = parsed.renames;
  if (!Array.isArray(renames)) {
    throw new Error('curriculum-renames.json に配列の renames がありません');
  }

  for (const [index, entry] of renames.entries()) {
    const where = `renames[${index}]`;
    if (entry === null || typeof entry !== 'object') {
      throw new Error(`${where} がオブジェクトではありません`);
    }
    if (entry.type === 'curriculum') {
      requireStrings(entry, ['from', 'to'], where);
    } else if (entry.type === 'section_prefix') {
      requireStrings(entry, ['curriculum', 'from_prefix', 'to_prefix'], where);
    } else {
      throw new Error(
        `${where}.type「${entry.type}」は未対応です（curriculum / section_prefix のみ）`
      );
    }
  }

  return renames;
}

/**
 * 指定キーがすべて空でない文字列であることを確認する
 */
function requireStrings(entry, keys, where) {
  for (const key of keys) {
    if (typeof entry[key] !== 'string' || entry[key] === '') {
      throw new Error(`${where}.${key} が空でない文字列ではありません`);
    }
  }
}

/**
 * API に JSON データを送信
 */
function sendToApi(data, apiUrl, apiKey) {
  return new Promise((resolve, reject) => {
    const jsonData = JSON.stringify(data);
    const url = new URL(apiUrl + '/deploy/sections/upsert');
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

  let renames;
  try {
    renames = loadRenames();
  } catch (error) {
    console.error(`Error: ${error.message}`);
    process.exit(1);
  }

  const totalCurriculums = curriculums.length;
  const totalChapters = curriculums.reduce((sum, c) => sum + c.chapters.length, 0);
  const totalSections = curriculums.reduce(
    (sum, c) => sum + c.chapters.reduce((s, ch) => s + ch.sections.length, 0),
    0
  );

  console.log(`Collected: ${totalCurriculums} curriculums, ${totalChapters} chapters, ${totalSections} sections`);

  if (renames) {
    console.log(`Renames: ${renames.length} entries (curriculum-renames.json)`);
    for (const entry of renames) {
      if (entry.type === 'curriculum') {
        console.log(`  curriculum: "${entry.from}" -> "${entry.to}"`);
      } else {
        console.log(
          `  section_prefix: "${entry.from_prefix}" -> "${entry.to_prefix}" in "${entry.curriculum}"`
        );
      }
    }
  } else {
    console.log('Renames: none (curriculum-renames.json が無いため従来どおり送信します)');
  }

  const payload = {
    workspaceId: workspaceId,
    ...(renames && { renames: renames }),
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
