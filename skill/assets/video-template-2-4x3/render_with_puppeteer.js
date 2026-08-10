const fs = require('fs');
const fsp = fs.promises;
const path = require('path');
const { execFileSync } = require('child_process');

function loadPuppeteer() {
  const moduleIds = ['puppeteer', 'puppeteer-core'];
  if (process.env.CODEX_NODE_MODULES) {
    moduleIds.push(path.join(process.env.CODEX_NODE_MODULES, 'puppeteer-core'));
  }
  for (const moduleId of moduleIds) {
    try {
      return require(moduleId);
    } catch (error) {
      if (error.code !== 'MODULE_NOT_FOUND') throw error;
    }
  }
  throw new Error('Puppeteer is unavailable. Install puppeteer or set CODEX_NODE_MODULES.');
}

function findChrome() {
  const candidates = [
    process.env.PUPPETEER_EXECUTABLE_PATH,
    process.env.CHROME_PATH,
    process.env.PROGRAMFILES && path.join(process.env.PROGRAMFILES, 'Google', 'Chrome', 'Application', 'chrome.exe'),
    process.env['PROGRAMFILES(X86)'] && path.join(process.env['PROGRAMFILES(X86)'], 'Google', 'Chrome', 'Application', 'chrome.exe'),
    process.env.LOCALAPPDATA && path.join(process.env.LOCALAPPDATA, 'Google', 'Chrome', 'Application', 'chrome.exe'),
  ].filter(Boolean);
  return candidates.find(candidate => fs.existsSync(candidate));
}

const puppeteer = loadPuppeteer();

const ROOT = __dirname;
const ARTICLE_ROOT = path.dirname(ROOT);
function topicFromDir(dir) {
  return path.basename(dir)
    .replace(/^待\d*[-_ ]*/, '')
    .replace(/^\d+[-_ ]*/, '')
    .replace(/[\\/:*?"<>|]/g, '')
    .trim() || 'output-video';
}
const FPS = 24;
const WIDTH = 1440;
const HEIGHT = 1080;
const META = JSON.parse(fs.readFileSync(path.join(ROOT, 'build_meta.json'), 'utf8'));
const TOTAL = META.total_duration;
const PREVIEW_SECONDS = Number(process.env.PREVIEW_SECONDS || 0);
const RENDER_SECONDS = PREVIEW_SECONDS > 0 ? Math.min(TOTAL, PREVIEW_SECONDS) : TOTAL;
const FRAME_COUNT = Math.ceil(RENDER_SECONDS * FPS);
const FRAMES_DIR = path.join(ROOT, 'renders', 'frames');
const OUTPUT_DIR = path.join(ROOT, 'renders');
const FINAL_MP4 = path.join(ARTICLE_ROOT, `${topicFromDir(ARTICLE_ROOT)}.mp4`);
const COMPAT_OUTPUT_MP4 = path.join(OUTPUT_DIR, 'output-video.mp4');
const PREVIEW_MP4 = path.join(OUTPUT_DIR, `preview-${String(RENDER_SECONDS).replace('.', '_')}s.mp4`);
const OUTPUT_PREVIEW = path.join(OUTPUT_DIR, 'preview-frame-001.jpg');
const AUDIO = path.join(ROOT, 'assets', 'narration.mp3');
const INDEX = `file:///${path.join(ROOT, 'index.html').replace(/\\/g, '/')}`;

(async () => {
  await fsp.mkdir(FRAMES_DIR, { recursive: true });
  for (const file of await fsp.readdir(FRAMES_DIR)) {
    if (file.endsWith('.jpg')) await fsp.unlink(path.join(FRAMES_DIR, file));
  }

  const launchOptions = {
    headless: 'new',
    defaultViewport: { width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 },
    args: ['--allow-file-access-from-files', '--autoplay-policy=no-user-gesture-required']
  };
  const chromePath = findChrome();
  if (chromePath) launchOptions.executablePath = chromePath;
  const browser = await puppeteer.launch(launchOptions);
  const page = await browser.newPage();
  await page.setCacheEnabled(false);
  await page.goto(`${INDEX}?v=${Date.now()}`, { waitUntil: 'load', timeout: 60000 });
  for (let i = 0; i < FRAME_COUNT; i++) {
    const t = Math.min(RENDER_SECONDS - 0.001, i / FPS + (i === 0 ? 0.001 : 0));
    await page.evaluate((tt) => window.__hfSeek(tt), t);
    await new Promise(r => setTimeout(r, 8));
    const out = path.join(FRAMES_DIR, `frame_${String(i + 1).padStart(6, '0')}.jpg`);
    await page.screenshot({ path: out, type: 'jpeg', quality: 92 });
    if (i === 0) await fsp.copyFile(out, OUTPUT_PREVIEW);
    if ((i + 1) % 120 === 0 || i === FRAME_COUNT - 1) console.log(`frames ${i + 1}/${FRAME_COUNT}`);
  }
  await browser.close();

  const targetOutput = PREVIEW_SECONDS > 0 ? PREVIEW_MP4 : FINAL_MP4;
  execFileSync('ffmpeg', [
    '-y',
    '-framerate', String(FPS),
    '-i', path.join(FRAMES_DIR, 'frame_%06d.jpg'),
    '-i', AUDIO,
    '-c:v', 'libx264',
    '-preset', 'medium',
    '-crf', '20',
    '-pix_fmt', 'yuv420p',
    '-c:a', 'aac',
    '-b:a', '192k',
    '-shortest',
    targetOutput
  ], { stdio: 'inherit' });

  await fsp.copyFile(targetOutput, COMPAT_OUTPUT_MP4);
  console.log(JSON.stringify({
    output: targetOutput,
    compatOutput: COMPAT_OUTPUT_MP4,
    preview: OUTPUT_PREVIEW,
    frames: FRAME_COUNT,
    fps: FPS,
    width: WIDTH,
    height: HEIGHT,
    renderedSeconds: RENDER_SECONDS
  }, null, 2));
})().catch(err => {
  console.error(err);
  process.exit(1);
});
