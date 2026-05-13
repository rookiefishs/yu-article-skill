# -*- coding: utf-8 -*-
from pathlib import Path
import asyncio, subprocess, json, textwrap
import edge_tts

ROOT = Path(__file__).resolve().parent
ARTICLE_ROOT = ROOT.parent
SOURCE_DIR = ARTICLE_ROOT / '素材文件'
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
VOICE = 'zh-CN-YunyangNeural'
RATE = '+24%'

# 替换为实际视频内容
SCENES = [
    {
        'title': '标题第一行\n标题第二行',
        'accent': '副标题',
        'caption': '底部字幕/重点句',
        'voice': '配音内容，需要与标题对应。',
        'kind': 'hook'
    },
    # 继续添加更多场景...
]

DESIGN = textwrap.dedent('''
# Video Design

## Colors
- Background: #f5f4ed
- Surface: rgba(255, 255, 255, 0.42)
- Surface Border: rgba(118, 180, 224, 0.18)
- Text Primary: #141413
- Text Secondary: #5e5d59
- Accent Terracotta: #c96442
- Accent Coral: #d97757
- Ambient Blue: rgba(145,195,255,.24)
- Ambient Mint: rgba(136,224,199,.20)

## Typography
- Headline Font: Microsoft YaHei
- Body Font: Microsoft YaHei
- Numeric / Mono Accent: Consolas
- Weight: Headline 800-900, Body 400-800

## Motion
- 温暖纸感 editorial 风格
- 统一页面壳（scene shell）
- 整页横向 push / slide 过渡
- 下一页必须完整覆盖上一页，不做内容替换式切换
''').strip() + '\n'

async def synth(scene, path):
    communicate = edge_tts.Communicate(scene['voice'], VOICE, rate=RATE)
    await communicate.save(str(path))

def ffprobe_duration(path):
    res = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)], capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

async def main():
    SOURCE_DIR.mkdir(exist_ok=True)
    (SOURCE_DIR / 'DESIGN.md').write_text(DESIGN, encoding='utf-8')
    gsap = ASSETS / 'gsap.min.js'
    if not gsap.exists():
        raise SystemExit('Missing assets/gsap.min.js，请先放置GSAP库文件')
    audio_files = []
    for i, scene in enumerate(SCENES):
        p = ASSETS / f'scene_{i:02d}.mp3'
        await synth(scene, p)
        audio_files.append(p)
    for scene, p in zip(SCENES, audio_files):
        scene['audio_duration'] = ffprobe_duration(p)
        scene['duration'] = round(scene['audio_duration'] + 0.45, 2)
    overlap = 0.55
    starts = []
    t = 0.0
    for i, scene in enumerate(SCENES):
        starts.append(round(t, 2))
        if i < len(SCENES) - 1:
            t += scene['duration'] - overlap
        else:
            t += scene['duration']
    total = round(t + 0.4, 2)
    concat = ASSETS / 'concat.txt'
    concat.write_text(''.join([f"file '{p.as_posix()}'\n" for p in audio_files]), encoding='utf-8')
    narration = ASSETS / 'narration.mp3'
    subprocess.run(['ffmpeg','-y','-f','concat','-safe','0','-i',str(concat),'-c','copy',str(narration)], check=True)

    html = build_html(SCENES, starts, total)
    (ROOT / 'index.html').write_text(html, encoding='utf-8')
    meta = {'total_duration': total, 'starts': starts, 'scenes': [{k:v for k,v in s.items() if k in ('title','accent','caption','duration','audio_duration','kind')} for s in SCENES]}
    (ROOT / 'build_meta.json').write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(meta, ensure_ascii=False, indent=2))


def build_scene_card(scene):
    kind = scene['kind']
    if kind == 'terminal':
        return '''
            <div class="card terminal-card">
              <div class="window-bar"><span></span><span></span><span></span><b>终端示例</b></div>
              <div class="terminal-lines">
                <div>$ 命令1</div>
                <div>$ 命令2</div>
                <div>$ 命令3</div>
              </div>
            </div>'''
    if kind == 'checklist':
        return '''
            <div class="card checklist-card">
              <div class="check-item"><i></i><span>项目1</span></div>
              <div class="check-item"><i></i><span>项目2</span></div>
              <div class="check-item"><i></i><span>项目3</span></div>
            </div>'''
    chip = scene.get('chip', '动作')
    stat = scene.get('stat', scene['accent'])
    desc = scene.get('desc', scene['caption'])
    return f'''
            <div class="card hero-card">
              <div class="hero-chip">{chip}</div>
              <div class="hero-stat">{stat}</div>
              <div class="hero-desc">{desc}</div>
            </div>'''


def build_html(scenes, starts, total):
    scene_divs = []
    js_data = []
    total_pages = len(scenes)

    for i, (scene, start) in enumerate(zip(scenes, starts), start=1):
        dur = scene['duration']
        title_html = '<br>'.join(scene['title'].split('\n'))
        track = i
        image_file = ARTICLE_ROOT / 'image' / f'{i}.png'
        image_src = f'../image/{i}.png' if image_file.exists() else None
        section_classes = f"clip scene scene-{scene['kind']}" + (" with-visual" if image_src else "")
        visual_html = f'<div class="scene-visual"><div class="visual-frame"><img class="visual-image" src="{image_src}" alt="scene-{i}-image" /></div></div>' if image_src else ''
        middle = build_scene_card(scene)
        page_label = scene.get('series', '视频主题')
        kicker = scene.get('kicker', '分类标签')
        scene_divs.append(f'''
        <section id="scene-{i}" class="{section_classes}" data-start="{start}" data-duration="{dur}" data-track-index="{track}" style="z-index:{20+i}">
          <div class="scene-bg scene-bg-{i%3}"></div>
          <div class="grid"></div>
          <div class="glow glow-a"></div>
          <div class="glow glow-b"></div>
          {visual_html}
          <div class="scene-shell"></div>
          <div class="meta-bar"><span class="meta-pill">{page_label}</span><span class="meta-index">{i:02d}/{total_pages:02d}</span></div>
          <div class="scene-content">
            <div class="kicker">{kicker}</div>
            <h1 class="title">{title_html}</h1>
            <h2 class="accent">{scene['accent']}</h2>
            {middle}
          </div>
          <div class="bottom-caption"><span>{scene['caption']}</span></div>
          <div class="progress-shell"><div class="progress-fill"></div></div>
        </section>
        ''')
        js_data.append({'id': i, 'start': start, 'duration': dur, 'kind': scene['kind']})

    first = scenes[0] if scenes else {'title': '主标题\n第二行', 'accent': '副标题'}
    intro_brand = first.get('brand', '视频主题')
    intro_tag = first.get('tag', '分类标签')
    intro_kicker = first.get('intro_kicker', '系列标签')
    intro_title = '<br>'.join(first['title'].split('\n'))
    intro_summary = first.get('summary', '视频简介内容，1-2句话说明视频核心价值。')
    intro_problem = first.get('problem', '问题描述，说明痛点。')
    intro_points = first.get('points', ['内容点1', '内容点2', '内容点3'])
    if not isinstance(intro_points, list):
        intro_points = ['内容点1', '内容点2', '内容点3']
    intro_points_html = ''.join(f'<span>{p}</span>' for p in intro_points[:3])

    html = '''<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="./assets/gsap.min.js"></script>
    <style>
      * { margin:0; padding:0; box-sizing:border-box; }
      html, body { width:1080px; height:1920px; overflow:hidden; background:#f5f4ed; font-family:"Microsoft YaHei","Segoe UI",sans-serif; color:#141413; }
      body { position:relative; background:
        radial-gradient(circle at 20% 15%, rgba(145,195,255,.34), transparent 26%),
        radial-gradient(circle at 80% 70%, rgba(136,224,199,.24), transparent 24%),
        linear-gradient(180deg,#f5f4ed 0%,#faf9f5 42%,#f0eee6 100%); }
      #root { position:relative; width:100%; height:100%; overflow:hidden; }
      .ambient { position:absolute; inset:0; width:100%; height:100%; overflow:hidden; }
      .scene { position:absolute; inset:0; width:100%; height:100%; overflow:hidden; opacity:0; visibility:hidden; transform-origin:center center; will-change:transform, opacity; background:#f5f4ed; }
      .intro-cover { position:absolute; inset:0; z-index:120; overflow:hidden; background:
        radial-gradient(circle at 18% 22%, rgba(145,195,255,.36), transparent 28%),
        radial-gradient(circle at 82% 78%, rgba(136,224,199,.24), transparent 24%),
        linear-gradient(180deg,#f5f4ed 0%,#faf9f5 42%,#f0eee6 100%); }
      .intro-ring, .intro-ring-two { position:absolute; border-radius:50%; border:2px solid rgba(97,157,205,.20); }
      .intro-ring { width:720px; height:720px; left:-160px; top:220px; }
      .intro-ring-two { width:520px; height:520px; right:-120px; bottom:340px; border-color:rgba(129,207,190,.22); }
      .intro-grid { position:absolute; inset:0; background-image: linear-gradient(rgba(97,140,178,.08) 1px, transparent 1px), linear-gradient(90deg, rgba(97,140,178,.08) 1px, transparent 1px); background-size: 84px 84px; opacity:.22; }
      .intro-noise { position:absolute; inset:-20%; background:radial-gradient(circle, rgba(255,255,255,.06) 0 1px, transparent 1px); background-size: 22px 22px; opacity:.1; }
      .intro-panel { position:absolute; left:76px; right:76px; top:92px; bottom:120px; border-radius:46px; border:2px solid rgba(118,180,224,.28); background:linear-gradient(180deg, rgba(255,255,255,.58), rgba(250,249,245,.38)); box-shadow: inset 0 1px 0 rgba(255,255,255,.6), 0 24px 80px rgba(88,134,171,.14); }
      .intro-topline { position:absolute; top:132px; left:120px; right:120px; display:flex; align-items:center; justify-content:space-between; }
      .intro-brand { display:flex; align-items:center; gap:16px; padding:16px 26px; border-radius:999px; border:2px solid rgba(118,180,224,.24); background:rgba(255,255,255,.58); }
      .intro-brand-dot { width:56px; height:16px; border-radius:999px; background:linear-gradient(90deg,#c96442,#d97757,#d97757); }
      .intro-brand-text { font-size:30px; font-weight:800; letter-spacing:.5px; color:#141413; }
      .intro-tag { font-size:22px; letter-spacing:2px; color:#c96442; }
      .intro-content { position:absolute; left:120px; right:120px; top:320px; }
      .intro-kicker { font-size:28px; letter-spacing:3px; color:#c96442; margin-bottom:26px; }
      .intro-title { font-size:112px; line-height:.98; font-weight:900; max-width:760px; color:#141413; text-shadow:none; }
      .intro-summary { margin-top:36px; max-width:740px; font-size:34px; line-height:1.45; color:#5e5d59; }
      .intro-callout { position:absolute; left:120px; right:120px; bottom:330px; display:grid; grid-template-columns:1.1fr .9fr; gap:24px; }
      .intro-box { min-height:210px; padding:28px 30px; border-radius:34px; border:2px solid rgba(118,180,224,.18); background:rgba(255,255,255,.35); }
      .intro-box strong { display:block; font-size:34px; color:#3E83AD; margin-bottom:16px; }
      .intro-box p { font-size:28px; line-height:1.45; color:#5e5d59; }
      .intro-mini-list { display:flex; flex-direction:column; gap:14px; }
      .intro-mini-list span { display:block; padding:14px 18px; border-radius:18px; background:rgba(255,255,255,.42); font-size:24px; color:#5e5d59; }
      .ambient-line { position:absolute; left:-10%; width:120%; height:2px; background:linear-gradient(90deg, transparent, rgba(99,167,192,.7), transparent); opacity:.28; transform-origin:left center; }
      .ambient-dot { position:absolute; width:8px; height:8px; border-radius:50%; background:#71C9BE; box-shadow:0 0 18px rgba(113,201,190,.38); opacity:.55; }
      .scene-bg { position:absolute; inset:0; }
      .scene-bg-1, .scene-bg-2, .scene-bg-0 { background:
        radial-gradient(circle at 18% 18%, rgba(145,195,255,.24), transparent 28%),
        radial-gradient(circle at 82% 78%, rgba(136,224,199,.20), transparent 24%),
        linear-gradient(180deg, rgba(255,255,255,.12) 0%, rgba(255,255,255,0) 58%),
        linear-gradient(180deg,#f5f4ed 0%,#faf9f5 42%,#f0eee6 100%); }
      .grid { position:absolute; inset:0; background-image: linear-gradient(rgba(97,140,178,.08) 1px, transparent 1px), linear-gradient(90deg, rgba(97,140,178,.08) 1px, transparent 1px); background-size: 70px 70px; mask-image: linear-gradient(180deg, transparent 0%, black 18%, black 82%, transparent 100%); opacity:.24; }
      .glow { position:absolute; border-radius:50%; filter:blur(80px); opacity:.55; }
      .glow-a { width:360px; height:360px; left:-80px; top:190px; background:rgba(145,195,255,.28); }
      .glow-b { width:380px; height:380px; right:-90px; bottom:260px; background:rgba(113,201,190,.22); }
      .scene-shell { position:absolute; inset:44px 42px 72px; border-radius:48px; border:2px solid rgba(118,180,224,.18); background:linear-gradient(180deg, rgba(255,255,255,.48), rgba(250,249,245,.24)); box-shadow:0 26px 80px rgba(88,134,171,.12), inset 0 1px 0 rgba(255,255,255,.58); backdrop-filter: blur(10px); }
      .meta-bar { position:absolute; top:76px; left:76px; right:76px; height:76px; border:2px solid rgba(118,180,224,.28); border-radius:36px; background:rgba(255,255,255,.42); display:flex; align-items:center; justify-content:space-between; padding:0 34px; backdrop-filter: blur(10px); }
      .meta-bar::before { content:''; width:56px; height:12px; border-radius:10px; background:linear-gradient(90deg,#c96442,#d97757,#d97757); box-shadow:0 0 12px rgba(255,183,77,.24); }
      .meta-pill { font-size:24px; color:#141413; letter-spacing:.5px; margin-left:-220px; }
      .meta-index { font-size:24px; color:#87867f; font-family:Consolas, monospace; }
      .scene-content { position:absolute; inset:0; padding:228px 108px 430px; display:flex; flex-direction:column; gap:20px; z-index:1; }
      .scene.with-visual .card { display:none; }
      .scene.with-visual .scene-content { padding-bottom:300px; }
      .scene-visual { position:absolute; left:98px; right:98px; top:760px; height:520px; z-index:1; }
      .visual-frame { position:relative; width:100%; height:100%; border-radius:28px; overflow:hidden; border:2px solid rgba(118,180,224,.16); background:rgba(229,244,255,.12); box-shadow:0 20px 60px rgba(88,134,171,.12); backdrop-filter: blur(6px); }
      .visual-image { width:100%; height:100%; object-fit:contain; display:block; background:transparent; }
      .kicker { font-size:24px; color:#c96442; letter-spacing:2px; text-transform:uppercase; }
      .title { font-size:86px; line-height:1.04; font-weight:900; max-width:760px; color:#141413; text-shadow:none; }
      .accent { font-size:44px; line-height:1.1; font-weight:800; color:#5e5d59; }
      .card { margin-top:34px; border-radius:42px; border:2px solid rgba(118,180,224,.16); background:rgba(255,255,255,.30); box-shadow:0 18px 40px rgba(88,134,171,.10), inset 0 1px 0 rgba(255,255,255,.5); backdrop-filter: blur(10px); }
      .hero-card { padding:40px 42px; display:flex; flex-direction:column; gap:16px; }
      .hero-chip { align-self:flex-start; padding:12px 22px; border-radius:999px; font-size:28px; color:#141413; background:linear-gradient(90deg,#85D9D6,#B8D7FF); font-weight:800; }
      .hero-stat { font-size:72px; font-weight:900; color:#141413; }
      .hero-desc { font-size:30px; color:#48627C; }
      .terminal-card { padding:0; overflow:hidden; }
      .window-bar { height:74px; display:flex; align-items:center; gap:12px; padding:0 24px; background:rgba(118,180,224,.10); color:#506A84; font-size:24px; }
      .window-bar span { width:14px; height:14px; border-radius:50%; background:#c96442; }
      .window-bar span:nth-child(2){background:#d97757;} .window-bar span:nth-child(3){background:#d97757;}
      .window-bar b { margin-left:12px; font-weight:700; }
      .terminal-lines { padding:34px 34px 38px; font-family:Consolas, monospace; font-size:28px; line-height:1.8; color:#29425A; }
      .checklist-card { padding:30px 28px; display:flex; flex-direction:column; gap:18px; }
      .check-item { display:flex; align-items:center; gap:18px; padding:16px 16px; border-radius:24px; background:rgba(255,255,255,.30); font-size:28px; color:#141413; }
      .check-item i { width:24px; height:24px; border-radius:50%; background:#d97757; box-shadow:0 0 16px rgba(217,119,87,.38); }
      .bottom-caption { position:absolute; left:108px; right:108px; bottom:224px; padding:26px 30px; border-radius:30px; background:rgba(255,255,255,.42); border:2px solid rgba(118,180,224,.16); color:#141413; font-size:28px; font-weight:800; line-height:1.4; box-shadow:0 14px 30px rgba(88,134,171,.08); z-index:1; }
      .progress-shell { position:absolute; left:108px; right:108px; bottom:160px; height:14px; border-radius:999px; background:rgba(118,180,224,.18); overflow:hidden; z-index:1; }
      .progress-fill { width:100%; height:100%; transform-origin:left center; background:linear-gradient(90deg,#74CFC9,#8FB8FF); }
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="__TOTAL__" data-width="1080" data-height="1920">
      <audio id="narration" src="./assets/narration.mp3" data-start="0" data-duration="__TOTAL__" data-track-index="20" data-volume="1"></audio>
      <section id="intro-cover" class="intro-cover">
        <div class="intro-grid"></div>
        <div class="intro-noise"></div>
        <div class="intro-ring"></div>
        <div class="intro-ring-two"></div>
        <div class="intro-panel"></div>
        <div class="intro-topline">
          <div class="intro-brand"><span class="intro-brand-dot"></span><span class="intro-brand-text">__INTRO_BRAND__</span></div>
          <div class="intro-tag">__INTRO_TAG__</div>
        </div>
        <div class="intro-content">
          <div class="intro-kicker">__INTRO_KICKER__</div>
          <h1 class="intro-title">__INTRO_TITLE__</h1>
          <div class="intro-summary">__INTRO_SUMMARY__</div>
        </div>
        <div class="intro-callout">
          <div class="intro-box">
            <strong>解决什么问题？</strong>
            <p>__INTRO_PROBLEM__</p>
          </div>
          <div class="intro-box">
            <strong>这条视频会讲</strong>
            <div class="intro-mini-list">__INTRO_POINTS_HTML__</div>
          </div>
        </div>
      </section>
      <div class="ambient">
        <div class="ambient-line" style="top:140px"></div>
        <div class="ambient-line" style="top:580px"></div>
        <div class="ambient-line" style="top:1030px"></div>
        <div class="ambient-line" style="top:1470px"></div>
        <div class="ambient-dot" style="left:80px; top:420px"></div>
        <div class="ambient-dot" style="left:920px; top:290px; width:6px; height:6px"></div>
        <div class="ambient-dot" style="left:780px; top:1610px; width:10px; height:10px"></div>
      </div>
      __SCENE_DIVS__
    </div>

    <script>
      window.__timelines = window.__timelines || {};
      const tl = gsap.timeline({ paused: true });
      const SCENES = __SCENES_JSON__;
      const totalDuration = __TOTAL__;

      gsap.set('.progress-fill', { scaleX: 0 });
      gsap.set('#intro-cover', { autoAlpha: 1 });
      tl.to('.ambient-line', { x: -120, duration: totalDuration, ease: 'none', stagger: 0.12 }, 0);
      tl.to('.ambient-dot', { y: -140, x: 20, duration: totalDuration, ease: 'none', stagger: 0.2 }, 0);
      tl.to('.glow-a', { x: 40, y: 22, duration: totalDuration, repeat: 0, ease: 'sine.inOut' }, 0);
      tl.to('.glow-b', { x: -35, y: -18, duration: totalDuration, repeat: 0, ease: 'sine.inOut' }, 0);
      tl.from('.intro-brand', { y: -34, duration: .38, ease: 'power3.out' }, 0.02);
      tl.from('.intro-tag', { x: 30, duration: .32, ease: 'power2.out' }, 0.1);
      tl.from('.intro-kicker', { x: -26, duration: .32, ease: 'power2.out' }, 0.16);
      tl.from('.intro-title', { y: 66, scale: .96, duration: .62, ease: 'expo.out' }, 0.22);
      tl.from('.intro-summary', { y: 30, duration: .38, ease: 'power2.out' }, 0.48);
      tl.from('.intro-box', { y: 46, duration: .45, stagger: .1, ease: 'back.out(1.08)' }, 0.62);
      tl.to('.intro-ring', { rotation: 22, scale: 1.06, duration: 1.8, ease: 'sine.inOut' }, 0);
      tl.to('.intro-ring-two', { rotation: -18, scale: .94, duration: 1.8, ease: 'sine.inOut' }, 0);
      tl.to('#intro-cover', { scale: 1.03, filter: 'blur(12px)', opacity: 0, duration: .44, ease: 'power2.in' }, 1.58);
      tl.set('#intro-cover', { autoAlpha: 0 }, 2.04);

      SCENES.forEach((scene, idx) => {
        const s = scene.start;
        const d = scene.duration;
        const root = `#scene-${scene.id}`;
        const enterAt = idx === 0 ? Math.max(2.02, s + 0.02) : s + 0.18;
        const exitAt = s + d - 0.24;

        tl.set(root, { autoAlpha: 1, x: 0, opacity: 1, scale: 1, filter: 'blur(0px)' }, enterAt - 0.02);
        tl.fromTo(
          root,
          {
            x: idx === 0 ? 0 : 1080,
            opacity: idx === 0 ? 0 : 1,
            scale: 1,
            filter: idx === 0 ? 'blur(8px)' : 'blur(0px)'
          },
          {
            x: 0,
            opacity: 1,
            scale: 1,
            filter: 'blur(0px)',
            duration: idx === 0 ? 0.58 : 0.34,
            ease: idx === 0 ? 'expo.out' : 'power2.out'
          },
          enterAt
        );

        tl.from(`${root} .meta-bar`, { y: -28, opacity: 0, duration: 0.28, ease: 'power2.out' }, s + 0.12);
        tl.from(`${root} .kicker`, { x: -20, opacity: 0, duration: 0.28, ease: 'power2.out' }, s + 0.18);
        tl.from(`${root} .title`, { y: 24, opacity: 0, duration: 0.34, ease: 'power2.out' }, s + 0.22);
        tl.from(`${root} .accent`, { y: 18, opacity: 0, duration: 0.28, ease: 'power2.out' }, s + 0.32);
        tl.from(`${root} .scene-visual`, { y: 18, opacity: 0, duration: 0.28, ease: 'power2.out' }, s + 0.36);
        tl.from(`${root} .card`, { y: 20, opacity: 0, duration: 0.3, ease: 'power2.out' }, s + 0.38);
        tl.from(`${root} .bottom-caption`, { y: 16, opacity: 0, duration: 0.24, ease: 'power2.out' }, s + 0.44);
        tl.to(`${root} .progress-fill`, { scaleX: 1, duration: Math.max(0.1, d - 0.72), ease: 'none' }, s + 0.52);

        if (scene.kind === 'terminal') {
          tl.from(`${root} .terminal-lines div`, { x: -18, opacity: 0, duration: 0.24, stagger: 0.08, ease: 'power2.out' }, s + 0.5);
        }
        if (scene.kind === 'checklist') {
          tl.from(`${root} .check-item`, { x: -18, opacity: 0, duration: 0.22, stagger: 0.08, ease: 'power2.out' }, s + 0.5);
        }

        if (idx < SCENES.length - 1) {
          tl.to(root, { x: -1080, opacity: 1, scale: 1, filter: 'blur(0px)', duration: 0.34, ease: 'power2.inOut' }, exitAt);
        } else {
          tl.to(root, { opacity: 0, duration: 0.45, ease: 'power2.in' }, totalDuration - 0.45);
        }

        tl.set(root, { autoAlpha: 0, x: 0, opacity: 1, scale: 1, filter: 'blur(0px)' }, s + d + 0.06);
      });
      window.__hfSeek = (t) => { tl.pause(); tl.seek(t, false); };
      window.__timelines['main'] = tl;
    </script>
  </body>
</html>
'''
    return (html
        .replace('__TOTAL__', str(total))
        .replace('__INTRO_BRAND__', intro_brand)
        .replace('__INTRO_TAG__', intro_tag)
        .replace('__INTRO_KICKER__', intro_kicker)
        .replace('__INTRO_TITLE__', intro_title)
        .replace('__INTRO_SUMMARY__', intro_summary)
        .replace('__INTRO_PROBLEM__', intro_problem)
        .replace('__INTRO_POINTS_HTML__', intro_points_html)
        .replace('__SCENE_DIVS__', ''.join(scene_divs))
        .replace('__SCENES_JSON__', json.dumps(js_data, ensure_ascii=False)))

if __name__ == '__main__':
    asyncio.run(main())
