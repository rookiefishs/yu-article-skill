# -*- coding: utf-8 -*-
from pathlib import Path
import subprocess, json, textwrap, sys

ROOT = Path(__file__).resolve().parent
ARTICLE_ROOT = ROOT.parent
SOURCE_DIR = ARTICLE_ROOT / '素材文件'
ASSETS = ROOT / 'assets'
ASSETS.mkdir(exist_ok=True)
TTS_PROVIDER = 'xiaomi-mimo'
TTS_MODEL = 'mimo-v2.5-tts'
TTS_VOICE = '冰糖'
TTS_SCRIPT = Path(r'E:\project\个人skill\yu-article-skill\skill\scripts\mimo-tts-bingtang.py')
TTS_STYLE = '中文科技短视频旁白，清晰、自然、口语化，语速略快但不要急，避免播音腔。'
PREVIEW_TRANSITION_START = 1.68

# 替换为实际视频内容
SCENES = [
    {
        'title': '先让它读懂项目',
        'accent': '改项目之前先读一遍',
        'caption': '入口 目录 命令 规则 风险',
        'voice': '用 Codex 改项目之前，先让它把项目读一遍。让它说清入口文件、目录分工、运行命令和容易改错的位置。这一轮看起来慢一点，后面能少很多误改和返工。',
        'kind': 'intro-cover',
        'series': 'Codex工作流',
        'kicker': '系列',
        'brand': 'Codex工作流',
        'tag': '第一期',
        'intro_kicker': '系列教程',
        'summary': '这一轮看起来慢一点，后面能少很多误改和返工。',
        'problem': '如果你接手的是陌生项目，这一步比直接提需求更重要。',
        'points': ['先找项目入口', '让它讲目录分工', '补上运行命令', '写下项目规则', '标出风险位置']
    },
    {
        'title': '先找项目入口',
        'accent': '别急着让 Codex 写功能',
        'caption': '前端后端配置分别从哪里看',
        'voice': '第一轮不要急着让 Codex 写功能，先让它找入口。让它说明前端从哪里启动，后端从哪里进来，配置文件放在哪里。如果是网页项目，就让它找路由、页面目录、组件目录和接口调用位置。如果是后端项目，就让它找服务入口、接口层、数据层和测试目录。这一步能帮你知道后面该把任务交给哪个范围。',
        'kind': 'hook',
        'series': 'Codex工作流',
        'kicker': '核心'
    },
    {
        'title': '让它讲目录分工',
        'accent': 'AI 最容易把文件改散',
        'caption': '目录讲清后面改动范围更稳',
        'voice': '项目目录一多，AI 最容易把文件改散。你可以先让 Codex 用简单语言解释每个核心目录负责什么。重点看它有没有识别出页面、组件、工具函数、配置、测试和文档。如果它说不清，说明上下文还不够，先补文件路径或让它继续读取。目录分工讲清之后，后面的改动范围会更稳。',
        'kind': 'hero',
        'series': 'Codex工作流',
        'kicker': '分工'
    },
    {
        'title': '补上运行命令',
        'accent': '读完代码还要知道怎么启动',
        'caption': '每次改代码都能做最小检查',
        'voice': 'Codex 读懂代码还不够，它还要知道怎么启动和验证。让它从 package.json、README、脚本文件或配置里找运行命令。同时让它区分开发启动、构建、测试、格式化和类型检查。如果命令跑不通，要让它记录报错和可能原因。后面每次改代码，都可以让它按这些命令做最小检查。',
        'kind': 'terminal',
        'series': 'Codex工作流',
        'kicker': '命令'
    },
    {
        'title': '写下项目规则',
        'accent': '给 AI 写一份规则文件',
        'caption': '贴近日常操作的规则最管用',
        'voice': '项目里最好有一份给 AI 看的规则文件，比如 AGENTS.md。里面写清代码风格、测试要求、不要碰的目录、常用命令和提交习惯。这样 Codex 每次进项目，不需要你重复讲一遍规矩。规则不用写得很长，越贴近日常操作越有用。只要团队习惯变了，就顺手把这份规则更新掉。',
        'kind': 'checklist',
        'series': 'Codex工作流',
        'kicker': '规则'
    },
    {
        'title': '标出风险位置',
        'accent': '标出容易出问题的位置',
        'caption': '风险提前暴露省得改完再查',
        'voice': '读项目时，还要让 Codex 标出容易出问题的地方。比如老代码、复杂状态、接口兼容、数据库字段、鉴权逻辑和构建脚本。这些位置可以改，但动手前要先说清影响面。如果它准备改这些文件，最好先让它给出改动理由和回滚方式。风险提前暴露，比改完再找问题省时间。',
        'kind': 'warning',
        'series': 'Codex工作流',
        'kicker': '避坑'
    },
    {
        'title': '读完再开任务',
        'accent': '地基清楚了才像在项目里工作',
        'caption': '地基搭好后面才少走弯路',
        'voice': '当 Codex 能说清入口、目录、命令、规则和风险，再让它做具体任务。你可以让它先输出计划，再确认是否开始修改。如果计划里出现大范围重构、顺手优化、无关文件变动，要及时拦住。第一期的目标是把后面的协作地基搭好，不追求一次产出很多代码。地基清楚了，Codex 后面才更像在项目里工作。',
        'kind': 'closing',
        'series': 'Codex工作流',
        'kicker': '总结'
    }
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

def voice_text(scene):
    return scene.get('voice', '').strip()

def synth_full_narration(voice_file, path):
    if not TTS_SCRIPT.exists():
        raise SystemExit(f'Missing MiMo TTS script: {TTS_SCRIPT}')
    wav_path = ASSETS / 'narration-mimo-bingtang.wav'
    subprocess.run([
        sys.executable,
        str(TTS_SCRIPT),
        '--input',
        str(voice_file),
        '--output',
        str(wav_path),
        '--style',
        TTS_STYLE,
    ], check=True)
    subprocess.run([
        'ffmpeg',
        '-y',
        '-i',
        str(wav_path),
        '-ar',
        '44100',
        '-ac',
        '2',
        '-b:a',
        '192k',
        str(path),
    ], check=True)

def allocate_scene_durations(scenes, narration_duration):
    overlap = 0.55
    target_sum = max(narration_duration + overlap * max(0, len(scenes) - 1), len(scenes) * 4.2)
    weights = [max(1, len(voice_text(scene))) for scene in scenes]
    weight_sum = sum(weights) or len(scenes)
    durations = [round(max(4.2, target_sum * weight / weight_sum), 2) for weight in weights]
    diff = round(target_sum - sum(durations), 2)
    if durations:
        durations[-1] = round(max(4.2, durations[-1] + diff), 2)
    return durations

def format_ts(seconds):
    seconds = max(0, int(round(seconds)))
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f'{h:02d}:{m:02d}:{s:02d}'

def ffprobe_duration(path):
    res = subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','default=nw=1:nk=1',str(path)], capture_output=True, text=True, check=True)
    return float(res.stdout.strip())

def topic_title():
    name = ARTICLE_ROOT.name
    for prefix in ('待-', '待_', '待 '):
        if name.startswith(prefix):
            return name[len(prefix):]
    if '-' in name and name.split('-', 1)[0].isdigit():
        return name.split('-', 1)[1]
    return name

def write_source_docs(starts=None):
    title = topic_title()
    outline_lines = [f'# {title} - 视频大纲', '']
    voice_lines = ['# 配音文件', '']
    full_voice = []
    for i, scene in enumerate(SCENES, start=1):
        outline_lines.append(f"- [{scene.get('kind', 'scene')}] {scene.get('title', '')}｜{scene.get('accent', '')}｜{scene.get('caption', '')}")
        if starts:
            voice_lines.append(f"[{format_ts(starts[i - 1])}] {scene.get('title', '')}")
        else:
            voice_lines.append(f"## 场景{i} {scene.get('title', '')}")
        voice = voice_text(scene)
        voice_lines.append(voice)
        voice_lines.append('')
        if voice:
            full_voice.append(voice)
    voice_lines.append('---')
    voice_lines.append('')
    voice_lines.append('## 完整文案')
    voice_lines.append('\n\n'.join(full_voice))
    (SOURCE_DIR / f'{title}-大纲.md').write_text('\n'.join(outline_lines).strip() + '\n', encoding='utf-8')
    (SOURCE_DIR / f'{title}-配音文件.md').write_text('\n'.join(voice_lines).strip() + '\n', encoding='utf-8')

def main():
    SOURCE_DIR.mkdir(exist_ok=True)
    (SOURCE_DIR / 'DESIGN.md').write_text(DESIGN, encoding='utf-8')
    gsap = ASSETS / 'gsap.min.js'
    if not gsap.exists():
        raise SystemExit('Missing assets/gsap.min.js，请先放置GSAP库文件')
    for old_scene_audio in ASSETS.glob('scene_*.mp3'):
        old_scene_audio.unlink()
    narration = ASSETS / 'narration.mp3'
    write_source_docs()
    voice_file = SOURCE_DIR / f'{topic_title()}-配音文件.md'
    synth_full_narration(voice_file, narration)
    narration_duration = ffprobe_duration(narration)
    for scene, duration in zip(SCENES, allocate_scene_durations(SCENES, narration_duration)):
        scene['duration'] = duration
    overlap = 0.55
    starts = []
    t = 0.0
    for i, scene in enumerate(SCENES):
        starts.append(round(t, 2))
        if i < len(SCENES) - 1:
            t += scene['duration'] - overlap
        else:
            t += scene['duration']
    total = round(max(t + 0.4, narration_duration + 0.35), 2)
    write_source_docs(starts)

    html = build_html(SCENES, starts, total)
    (ROOT / 'index.html').write_text(html, encoding='utf-8')
    meta = {'total_duration': total, 'narration_duration': round(narration_duration, 2), 'tts_provider': TTS_PROVIDER, 'tts_model': TTS_MODEL, 'voice': TTS_VOICE, 'starts': starts, 'scenes': [{k:v for k,v in s.items() if k in ('title','accent','caption','duration','kind')} for s in SCENES]}
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
      html, body { width:1080px; height:1920px; overflow:hidden; background:#f4f6fb; font-family:"Microsoft YaHei","Segoe UI",sans-serif; color:#141413; }
      body { position:relative; background:
        radial-gradient(circle at 18% 16%, rgba(205,193,255,.46), transparent 28%),
        radial-gradient(circle at 82% 78%, rgba(179,225,255,.44), transparent 26%),
        linear-gradient(180deg,#f7f8fc 0%,#eef4fb 52%,#e9f2fb 100%); }
      #root { position:relative; width:100%; height:100%; overflow:hidden; }
      .ambient { position:absolute; inset:0; width:100%; height:100%; overflow:hidden; }
      .scene { position:absolute; inset:0; width:100%; height:100%; overflow:hidden; opacity:0; visibility:hidden; transform-origin:center center; will-change:transform, opacity; background:#f5f4ed; }
      .intro-cover { position:absolute; inset:0; z-index:120; overflow:hidden; background:
        radial-gradient(circle at 18% 22%, rgba(205,193,255,.42), transparent 30%),
        radial-gradient(circle at 82% 78%, rgba(179,225,255,.38), transparent 26%),
        linear-gradient(180deg,#f7f8fc 0%,#eef4fb 52%,#e9f2fb 100%); }
      .intro-ring, .intro-ring-two { position:absolute; border-radius:50%; border:2px solid rgba(97,157,205,.20); }
      .intro-ring { width:720px; height:720px; left:-160px; top:220px; }
      .intro-ring-two { width:520px; height:520px; right:-120px; bottom:340px; border-color:rgba(129,207,190,.22); }
      .intro-grid { position:absolute; inset:0; background-image: linear-gradient(rgba(140,160,210,.08) 1px, transparent 1px), linear-gradient(90deg, rgba(140,160,210,.08) 1px, transparent 1px); background-size: 84px 84px; opacity:.2; }
      .intro-noise { position:absolute; inset:-20%; background:radial-gradient(circle, rgba(255,255,255,.06) 0 1px, transparent 1px); background-size: 22px 22px; opacity:.1; }
      .intro-panel { position:absolute; inset:100px; border-radius:44px; border:1px solid rgba(170,184,225,.9); background:
        radial-gradient(circle at 16% 18%, rgba(232,220,255,.52), transparent 30%),
        radial-gradient(circle at 82% 24%, rgba(255,228,239,.42), transparent 22%),
        radial-gradient(circle at 84% 82%, rgba(194,230,255,.66), transparent 30%),
        linear-gradient(135deg, rgba(247,243,255,.98) 0%, rgba(233,242,255,.96) 52%, rgba(226,237,247,.96) 100%); box-shadow: inset 0 1px 0 rgba(255,255,255,.86), 0 28px 88px rgba(112,132,186,.18); }
      .intro-topline { position:absolute; top:154px; left:150px; right:150px; display:flex; align-items:center; justify-content:space-between; }
      .intro-brand { display:flex; align-items:center; gap:16px; padding:16px 26px; border-radius:999px; border:2px solid rgba(118,180,224,.24); background:rgba(255,255,255,.58); }
      .intro-brand-dot { width:56px; height:16px; border-radius:999px; background:linear-gradient(90deg,#c96442,#d97757,#d97757); }
      .intro-brand-text { font-size:30px; font-weight:800; letter-spacing:.5px; color:#141413; }
      .intro-tag { font-size:22px; letter-spacing:2px; color:#c96442; }
      .intro-content { position:absolute; left:156px; right:156px; top:398px; }
      .intro-kicker { font-size:28px; letter-spacing:3px; color:#c96442; margin-bottom:26px; }
      .intro-title { font-size:100px; line-height:.98; font-weight:900; max-width:700px; color:#141413; text-shadow:none; }
      .intro-summary { margin-top:28px; max-width:620px; font-size:30px; line-height:1.42; color:#5e5d59; }
      .intro-callout { position:absolute; left:156px; right:156px; bottom:280px; display:grid; grid-template-columns:1fr; gap:18px; }
      .intro-box { min-height:156px; padding:24px 26px; border-radius:30px; border:1px solid rgba(176,191,230,.78); background:
        linear-gradient(135deg, rgba(239,232,255,.86) 0%, rgba(220,236,255,.88) 58%, rgba(242,235,255,.8) 100%); box-shadow:0 16px 30px rgba(112,132,186,.1), inset 0 1px 0 rgba(255,255,255,.6); }
      .intro-box strong { display:block; font-size:30px; color:#3E83AD; margin-bottom:14px; }
      .intro-box p { font-size:25px; line-height:1.42; color:#4f5c7a; }
      .intro-mini-list { display:flex; flex-direction:column; gap:14px; }
      .intro-mini-list span { display:block; padding:12px 16px; border-radius:16px; background:linear-gradient(135deg, rgba(255,255,255,.54) 0%, rgba(241,246,255,.34) 100%); font-size:22px; color:#4f5c7a; }
      .ambient-line { position:absolute; left:-10%; width:120%; height:2px; background:linear-gradient(90deg, transparent, rgba(152,170,227,.6), transparent); opacity:.24; transform-origin:left center; }
      .ambient-dot { position:absolute; width:8px; height:8px; border-radius:50%; background:#9cb8ff; box-shadow:0 0 18px rgba(156,184,255,.3); opacity:.5; }
      .scene-bg { position:absolute; inset:0; }
      .scene-bg-1, .scene-bg-2, .scene-bg-0 { background:
        radial-gradient(circle at 18% 18%, rgba(205,193,255,.26), transparent 30%),
        radial-gradient(circle at 82% 78%, rgba(179,225,255,.22), transparent 26%),
        linear-gradient(180deg, rgba(255,255,255,.14) 0%, rgba(255,255,255,0) 58%),
        linear-gradient(180deg,#f7f8fc 0%,#eef4fb 52%,#e9f2fb 100%); }
      .grid { position:absolute; inset:0; background-image: linear-gradient(rgba(140,160,210,.08) 1px, transparent 1px), linear-gradient(90deg, rgba(140,160,210,.08) 1px, transparent 1px); background-size: 70px 70px; mask-image: linear-gradient(180deg, transparent 0%, black 18%, black 82%, transparent 100%); opacity:.2; }
      .glow { position:absolute; border-radius:50%; filter:blur(90px); opacity:.58; }
      .glow-a { width:380px; height:380px; left:-70px; top:160px; background:rgba(208,193,255,.34); }
      .glow-b { width:420px; height:420px; right:-60px; bottom:180px; background:rgba(182,227,255,.30); }
      .scene-shell { position:absolute; inset:100px; border-radius:44px; border:1px solid rgba(168,183,223,.92); background:
        radial-gradient(circle at 16% 16%, rgba(232,220,255,.5), transparent 30%),
        radial-gradient(circle at 82% 22%, rgba(255,226,239,.4), transparent 22%),
        radial-gradient(circle at 84% 84%, rgba(194,230,255,.62), transparent 30%),
        linear-gradient(135deg, rgba(246,242,255,.98) 0%, rgba(231,242,255,.96) 58%, rgba(222,236,247,.96) 100%); box-shadow:0 30px 96px rgba(112,132,186,.18), inset 0 1px 0 rgba(255,255,255,.88); backdrop-filter: blur(12px); }
      .meta-bar { position:absolute; top:126px; left:126px; right:126px; height:68px; border:1px solid rgba(176,190,228,.84); border-radius:34px; background:linear-gradient(135deg, rgba(244,239,255,.68) 0%, rgba(228,241,255,.74) 100%); display:flex; align-items:center; justify-content:space-between; padding:0 30px; backdrop-filter: blur(10px); }
      .meta-bar::before { content:''; width:56px; height:12px; border-radius:10px; background:linear-gradient(90deg,#c96442,#d97757,#d97757); box-shadow:0 0 12px rgba(255,183,77,.24); }
      .meta-pill { font-size:22px; color:#3f4a68; letter-spacing:.5px; margin-left:-220px; }
      .meta-index { font-size:24px; color:#87867f; font-family:Consolas, monospace; }
      .scene-content { position:absolute; inset:0; padding:258px 156px 486px; display:flex; flex-direction:column; gap:18px; z-index:1; }
      .scene.with-visual .card { display:none; }
      .scene.with-visual .scene-content { padding-bottom:410px; }
      .scene-visual { position:absolute; left:156px; right:156px; top:710px; height:540px; z-index:1; }
      .visual-frame { position:relative; width:100%; height:100%; border-radius:28px; overflow:hidden; border:1px solid rgba(178,193,230,.84); background:
        linear-gradient(135deg, rgba(239,232,255,.82) 0%, rgba(216,235,255,.86) 62%, rgba(244,237,255,.74) 100%); box-shadow:0 20px 52px rgba(112,132,186,.12); backdrop-filter: blur(8px); }
      .visual-image { width:100%; height:100%; object-fit:contain; display:block; background:transparent; }
      .kicker { font-size:24px; color:#9c6fdd; letter-spacing:2px; text-transform:uppercase; }
      .title { font-size:76px; line-height:1.04; font-weight:900; max-width:700px; color:#141413; text-shadow:none; }
      .accent { font-size:38px; line-height:1.1; font-weight:800; color:#5f6986; }
      .card { margin-top:28px; border-radius:34px; border:1px solid rgba(176,191,229,.86); background:
        linear-gradient(135deg, rgba(239,231,255,.84) 0%, rgba(216,235,255,.88) 60%, rgba(244,236,255,.76) 100%); box-shadow:0 18px 36px rgba(112,132,186,.12), inset 0 1px 0 rgba(255,255,255,.5); backdrop-filter: blur(10px); }
      .hero-card { padding:34px 36px; display:flex; flex-direction:column; gap:12px; }
      .hero-chip { align-self:flex-start; padding:12px 22px; border-radius:999px; font-size:28px; color:#141413; background:linear-gradient(90deg,#85D9D6,#B8D7FF); font-weight:800; }
      .hero-stat { font-size:60px; font-weight:900; color:#141413; }
      .hero-desc { font-size:26px; color:#48627C; }
      .terminal-card { padding:0; overflow:hidden; }
      .window-bar { height:74px; display:flex; align-items:center; gap:12px; padding:0 24px; background:rgba(118,180,224,.10); color:#506A84; font-size:24px; }
      .window-bar span { width:14px; height:14px; border-radius:50%; background:#c96442; }
      .window-bar span:nth-child(2){background:#d97757;} .window-bar span:nth-child(3){background:#d97757;}
      .window-bar b { margin-left:12px; font-weight:700; }
      .terminal-lines { padding:34px 34px 38px; font-family:Consolas, monospace; font-size:28px; line-height:1.8; color:#29425A; }
      .checklist-card { padding:30px 28px; display:flex; flex-direction:column; gap:18px; }
      .check-item { display:flex; align-items:center; gap:18px; padding:16px 16px; border-radius:24px; background:rgba(255,255,255,.30); font-size:28px; color:#141413; }
      .check-item i { width:24px; height:24px; border-radius:50%; background:#d97757; box-shadow:0 0 16px rgba(217,119,87,.38); }
      .bottom-caption { position:absolute; left:156px; right:156px; bottom:232px; padding:24px 28px; border-radius:26px; background:
        linear-gradient(135deg, rgba(239,231,255,.84) 0%, rgba(216,235,255,.88) 60%, rgba(244,236,255,.74) 100%); border:1px solid rgba(176,191,229,.86); color:#263148; font-size:25px; font-weight:800; line-height:1.4; box-shadow:0 14px 28px rgba(112,132,186,.1); z-index:1; }
      .progress-shell { position:absolute; left:156px; right:156px; bottom:186px; height:12px; border-radius:999px; background:rgba(180,196,235,.36); overflow:hidden; z-index:1; }
      .progress-fill { width:100%; height:100%; transform-origin:left center; background:linear-gradient(90deg,#b79cff,#8dc8ff); }
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
      const firstSceneTransitionStart = __FIRST_SCENE_TRANSITION_START__;

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
      tl.set('#scene-1', { autoAlpha: 1, x: 1080, opacity: 1, scale: 1, filter: 'blur(0px)' }, firstSceneTransitionStart - 0.06);
      tl.to('#intro-cover', { x: -1080, duration: .42, ease: 'power2.inOut' }, firstSceneTransitionStart);
      tl.fromTo('#scene-1', { x: 1080, opacity: 1, scale: 1, filter: 'blur(0px)' }, { x: 0, opacity: 1, scale: 1, filter: 'blur(0px)', duration: .42, ease: 'power2.inOut' }, firstSceneTransitionStart);
      tl.set('#intro-cover', { autoAlpha: 0, x: 0 }, firstSceneTransitionStart + 0.44);

      SCENES.forEach((scene, idx) => {
        const s = scene.start;
        const d = scene.duration;
        const root = `#scene-${scene.id}`;
        const enterAt = idx === 0 ? firstSceneTransitionStart : s + 0.18;
        const exitAt = s + d - 0.24;

        if (idx > 0) {
          tl.set(root, { autoAlpha: 1, x: 0, opacity: 1, scale: 1, filter: 'blur(0px)' }, enterAt - 0.02);
          tl.fromTo(
            root,
            {
              x: 1080,
              opacity: 1,
              scale: 1,
              filter: 'blur(0px)'
            },
            {
              x: 0,
              opacity: 1,
              scale: 1,
              filter: 'blur(0px)',
              duration: 0.34,
              ease: 'power2.out'
            },
            enterAt
          );
        }

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
        .replace('__SCENES_JSON__', json.dumps(js_data, ensure_ascii=False))
        .replace('__FIRST_SCENE_TRANSITION_START__', str(PREVIEW_TRANSITION_START)))

if __name__ == '__main__':
    main()
