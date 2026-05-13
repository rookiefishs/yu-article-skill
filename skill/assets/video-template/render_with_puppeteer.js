const fs = require('fs');
const fsp = fs.promises;
const path = require('path');
const { execFileSync } = require('child_process');
const puppeteer = require('C:/Users/王志宇/AppData/Local/npm-cache/_npx/702923228c2ce1e6/node_modules/puppeteer-core');

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
const WIDTH = 1080;
const HEIGHT = 1920;
const META = JSON.parse(fs.readFileSync(path.join(ROOT, 'build_meta.json'), 'utf8'));
const TOTAL = META.total_duration;
const FRAME_COUNT = Math.ceil(TOTAL * FPS);
const FRAMES_DIR = path.join(ROOT, 'renders', 'frames');
const OUTPUT_DIR = path.join(ROOT, 'renders');
const FINAL_MP4 = path.join(ARTICLE_ROOT, `${topicFromDir(ARTICLE_ROOT)}.mp4`);
const COMPAT_OUTPUT_MP4 = path.join(OUTPUT_DIR, 'output-video.mp4');
const OUTPUT_PREVIEW = path.join(OUTPUT_DIR, 'preview-frame-001.jpg');
const AUDIO = path.join(ROOT, 'assets', 'narration.mp3');
const INDEX = `file:///${path.join(ROOT, 'index.html').replace(/\\/g, '/')}`;

(async () => {
  await fsp.mkdir(FRAMES_DIR, { recursive: true });
  for (const file of await fsp.readdir(FRAMES_DIR)) {
    if (file.endsWith('.jpg')) await fsp.unlink(path.join(FRAMES_DIR, file));
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe',
    defaultViewport: { width: WIDTH, height: HEIGHT, deviceScaleFactor: 1 },
    args: ['--allow-file-access-from-files', '--autoplay-policy=no-user-gesture-required']
  });

  const page = await browser.newPage();
  await page.setCacheEnabled(false);
  await page.goto(`${INDEX}?v=${Date.now()}`, { waitUntil: 'load', timeout: 60000 });
  for (let i = 0; i < FRAME_COUNT; i++) {
    const t = Math.min(TOTAL - 0.001, i / FPS + (i === 0 ? 0.001 : 0));
    await page.evaluate((tt) => {
      window.__hfSeek(tt);
    }, t);
    await new Promise(r => setTimeout(r, 12));
    const out = path.join(FRAMES_DIR, `frame_${String(i + 1).padStart(6, '0')}.jpg`);
    await page.screenshot({ path: out, type: 'jpeg', quality: 92 });
    if (i === 0) await fsp.copyFile(out, OUTPUT_PREVIEW);
    if ((i + 1) % 60 === 0 || i === FRAME_COUNT - 1) {
      console.log(`frames ${i + 1}/${FRAME_COUNT}`);
    }
  }
  await browser.close();

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
    FINAL_MP4
  ], { stdio: 'inherit' });

  await fsp.copyFile(FINAL_MP4, COMPAT_OUTPUT_MP4);

  console.log(JSON.stringify({ output: FINAL_MP4, compatOutput: COMPAT_OUTPUT_MP4, preview: OUTPUT_PREVIEW, frames: FRAME_COUNT, fps: FPS, total: TOTAL }, null, 2));
})().catch(err => {
  console.error(err);
  process.exit(1);
});
