# -*- coding: utf-8 -*-
from pathlib import Path
import html
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ARTICLE_ROOT = ROOT.parent
SOURCE_DIR = ARTICLE_ROOT / "素材文件"
IMAGE_DIR = ARTICLE_ROOT / "image"
ASSETS = ROOT / "assets"
ASSETS.mkdir(exist_ok=True)

# 复制模板后先修改 TITLE 和 SCENES。
TITLE = "示例标题：2号视频规范"
WIDTH = 1440
HEIGHT = 1080
FPS = 24
BASE_DURATION = 58.0
TTS_STYLE = "中文科技短视频旁白，清晰、自然、口语化，语速略快但不要急。"


def resolve_tts_script() -> Path:
    candidates = []
    configured = os.environ.get("YU_ARTICLE_TTS_SCRIPT")
    if configured:
        candidates.append(Path(configured))
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
    candidates.extend(
        [
            ROOT.parent.parent / "scripts" / "mimo-tts-bingtang.py",
            codex_home / "skills" / "yu-article-skill" / "scripts" / "mimo-tts-bingtang.py",
        ]
    )
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise SystemExit(
        "Missing MiMo TTS script. Set YU_ARTICLE_TTS_SCRIPT or install yu-article-skill."
    )

SCENES = [
    {
        "kicker": "SKILLS 推荐 01",
        "title": "superpowers",
        "accent": "先让 AI 有工程纪律",
        "caption": "它管的是工作习惯",
        "image": "1.png",
        "points": ["读规则", "拆任务", "按流程执行", "做验证"],
        "voice": "Skills 推荐第 1 期，先看 superpowers。如果你用 AI 写代码经常返工，可以先装这个 Skill。它主要管的是 AI 的工作习惯。",
    },
    {
        "kicker": "常见问题",
        "title": "AI 最容易跳步骤",
        "accent": "该读项目时直接开改",
        "caption": "返工往往从起手开始",
        "image": "2.png",
        "points": ["没读目录", "没确认边界", "没跑验证", "提前说完成"],
        "voice": "很多人用 AI 写代码，问题不在它不会写，而在它容易跳步骤。该先读项目时，它直接开改。该验证时，它只说自己改好了。",
    },
    {
        "kicker": "核心规则",
        "title": "先判断该用哪个 Skill",
        "accent": "让流程自动触发",
        "caption": "调 bug 走调试，写计划走计划",
        "image": "3.png",
        "points": ["任务到来", "判断场景", "读取 Skill", "按规则做"],
        "voice": "superpowers 会要求 AI 在开始任务前，先判断有没有适合当前场景的 Skill。调 bug 就走调试流程，写计划就走计划流程。",
    },
    {
        "kicker": "工作流程",
        "title": "先读规则，再做任务",
        "accent": "不要想到哪做到哪",
        "caption": "流程感会直接减少乱改",
        "image": "4.png",
        "points": ["Check", "Read", "Execute", "Verify"],
        "voice": "它会把读规则、拆任务、执行和验证放进同一条流程里。这样 AI 不容易想到哪做到哪，也不容易改完就提前交差。",
    },
    {
        "kicker": "适用场景",
        "title": "复杂任务更适合用它",
        "accent": "修 bug、做功能、改页面、写文档",
        "caption": "越复杂，越需要流程约束",
        "image": "5.png",
        "points": ["复杂调试", "功能开发", "页面改造", "文档交付"],
        "voice": "简单问题用它可能显得慢一点。但只要任务变成修 bug、做功能、改页面、写文档，它带来的流程感就很有用。",
    },
    {
        "kicker": "我的建议",
        "title": "放进基础配置",
        "accent": "先让 AI 会做事",
        "caption": "再谈让它做得快",
        "image": "1.png",
        "points": ["少凭感觉", "多按流程", "少提前交差", "少返工"],
        "voice": "我会把 superpowers 放进基础配置。它不会让模型能力突然暴涨，但会让 AI 少凭感觉，多按流程。先让 AI 会做事，再谈让它做得快。",
    },
]


def extract_full_voice() -> str:
    voice_file = SOURCE_DIR / f"{TITLE}-配音文件.md"
    text = voice_file.read_text(encoding="utf-8")
    if "## 完整文案" in text:
        return re.sub(r"\s+", " ", text.split("## 完整文案", 1)[1]).strip()
    return " ".join(scene["voice"] for scene in SCENES)


def create_audio() -> float:
    narration = ASSETS / "narration.mp3"
    voice_file = SOURCE_DIR / f"{TITLE}-配音文件.md"
    try:
        tts_script = resolve_tts_script()
        wav = ASSETS / "narration-mimo-bingtang.wav"
        subprocess.run([sys.executable, str(tts_script), "--input", str(voice_file), "--output", str(wav), "--style", TTS_STYLE], check=True)
        subprocess.run(["ffmpeg", "-y", "-i", str(wav), "-ar", "44100", "-ac", "2", "-b:a", "192k", str(narration)], check=True)
        return ffprobe_duration(narration)
    except Exception as exc:
        print(f"TTS unavailable, using silent audio: {exc}")
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", str(TOTAL_DURATION), "-b:a", "192k", str(narration)], check=True)
    return TOTAL_DURATION


def ffprobe_duration(path: Path) -> float:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)], capture_output=True, text=True, check=True)
    return float(result.stdout.strip())


def copy_images():
    for image in IMAGE_DIR.glob("*.png"):
        shutil.copy2(image, ASSETS / image.name)


def scene_start(index: int, total_duration: float) -> float:
    return round(index * (total_duration / len(SCENES)), 3)


def build_html(total_duration: float) -> str:
    scene_len = total_duration / len(SCENES)
    scenes_html = []
    for index, scene in enumerate(SCENES):
        start = scene_start(index, total_duration)
        points = "".join(f"<span>{html.escape(point)}</span>" for point in scene["points"])
        scenes_html.append(f"""
        <section class="scene" data-start="{start}" data-duration="{scene_len}">
          <div class="shell">
            <div class="copy">
              <div class="kicker">{html.escape(scene['kicker'])}</div>
              <h1>{html.escape(scene['title'])}</h1>
              <p class="accent">{html.escape(scene['accent'])}</p>
              <div class="points">{points}</div>
            </div>
            <div class="visual">
              <img src="assets/{html.escape(scene['image'])}" />
              <div class="visual-label">{html.escape(scene['caption'])}</div>
            </div>
            <div class="caption">{html.escape(scene['voice'])}</div>
            <div class="progress"><i></i></div>
          </div>
        </section>
        """)
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{html.escape(TITLE)}</title>
<style>
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  width: {WIDTH}px;
  height: {HEIGHT}px;
  overflow: hidden;
  font-family: "Microsoft YaHei", "PingFang SC", system-ui, sans-serif;
  background:
    radial-gradient(circle at 12% 18%, rgba(113, 178, 255, .32), transparent 30%),
    radial-gradient(circle at 86% 22%, rgba(163, 124, 255, .18), transparent 28%),
    linear-gradient(135deg, #eef7ff 0%, #f7fbff 48%, #f3f0ff 100%);
  color: #172033;
}}
.stage {{ position: relative; width: 100%; height: 100%; overflow: hidden; }}
.scene {{ position: absolute; inset: 0; transform: translateX(100%); opacity: 0; }}
.shell {{
  position: absolute;
  inset: 72px;
  border-radius: 34px;
  padding: 48px 52px 38px;
  background: linear-gradient(145deg, rgba(255,255,255,.82), rgba(235,247,255,.74));
  border: 1px solid rgba(78, 143, 211, .22);
  box-shadow: 0 28px 80px rgba(40, 83, 145, .16);
  display: grid;
  grid-template-columns: 0.9fr 1.1fr;
  grid-template-rows: 1fr auto auto;
  gap: 30px 44px;
}}
.copy {{ align-self: center; padding-left: 8px; }}
.kicker {{
  display: inline-flex;
  padding: 9px 14px;
  border-radius: 999px;
  background: rgba(50, 112, 205, .09);
  color: #3568b8;
  font-size: 22px;
  font-weight: 800;
  letter-spacing: .04em;
}}
h1 {{
  margin: 24px 0 0;
  font-size: 74px;
  line-height: 1.02;
  letter-spacing: 0;
  color: #111827;
}}
.accent {{
  margin: 22px 0 0;
  font-size: 32px;
  line-height: 1.35;
  color: #506078;
  font-weight: 700;
}}
.points {{
  margin-top: 34px;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
}}
.points span {{
  min-height: 54px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 16px;
  border-radius: 18px;
  background: rgba(255,255,255,.68);
  border: 1px solid rgba(70, 130, 205, .14);
  color: #22304a;
  font-size: 24px;
  font-weight: 800;
}}
.visual {{
  position: relative;
  align-self: center;
  height: 600px;
  border-radius: 28px;
  overflow: hidden;
  background: transparent;
  border: 1px solid rgba(21, 47, 91, .16);
  box-shadow: 0 20px 50px rgba(33, 73, 140, .18);
}}
.visual img {{
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}}
.visual-label {{
  position: absolute;
  left: 22px;
  right: auto;
  bottom: 20px;
  z-index: 2;
  max-width: calc(100% - 44px);
  padding: 9px 14px;
  border-radius: 16px;
  background: rgba(255,255,255,.78);
  border: 1px solid rgba(78, 143, 211, .16);
  color: #233047;
  font-size: 24px;
  font-weight: 800;
  text-shadow: none;
}}
.caption {{
  grid-column: 1 / -1;
  min-height: 86px;
  padding: 20px 26px;
  border-radius: 22px;
  background: rgba(16, 35, 68, .86);
  color: #f8fbff;
  font-size: 26px;
  line-height: 1.38;
  font-weight: 700;
}}
.progress {{
  grid-column: 1 / -1;
  height: 8px;
  border-radius: 999px;
  overflow: hidden;
  background: rgba(82, 126, 192, .16);
}}
.progress i {{
  display: block;
  width: 0;
  height: 100%;
  background: linear-gradient(90deg, #4f8dde, #8e6be8);
  border-radius: inherit;
}}
</style>
</head>
<body>
  <div class="stage">
    {''.join(scenes_html)}
  </div>
<script>
const scenes = [...document.querySelectorAll('.scene')];
const total = {total_duration};
function clamp(v, a, b) {{ return Math.max(a, Math.min(b, v)); }}
function easeOut(t) {{ return 1 - Math.pow(1 - t, 3); }}
window.__hfSeek = function(time) {{
  scenes.forEach((scene, index) => {{
    const start = Number(scene.dataset.start);
    const duration = Number(scene.dataset.duration);
    const local = time - start;
    const enter = index === 0 ? 1 : clamp(local / 0.8, 0, 1);
    const exit = clamp((local - duration + 0.65) / 0.65, 0, 1);
    let x = (1 - easeOut(enter)) * 100 - easeOut(exit) * 100;
    let visible = local > -0.8 && local < duration + 0.65;
    scene.style.transform = `translateX(${{x}}%)`;
    scene.style.opacity = visible ? 1 : 0;
    const shell = scene.querySelector('.shell');
    const visual = scene.querySelector('.visual');
    shell.style.transform = `scale(${{0.985 + easeOut(enter) * 0.015}})`;
    visual.style.transform = `translateY(${{(1 - easeOut(enter)) * 18}}px) scale(${{1 + Math.sin(Math.max(0, local) * 0.8) * 0.006}})`;
    scene.querySelector('.progress i').style.width = `${{clamp(time / total, 0, 1) * 100}}%`;
  }});
}};
window.__hfSeek(0.001);
</script>
</body>
</html>
"""


def main():
    copy_images()
    narration_duration = create_audio()
    total_duration = max(BASE_DURATION, narration_duration + 0.8)
    (ROOT / "index.html").write_text(build_html(total_duration), encoding="utf-8")
    meta = {
        "title": TITLE,
        "width": WIDTH,
        "height": HEIGHT,
        "fps": FPS,
        "total_duration": round(total_duration, 2),
        "narration_duration": round(narration_duration, 2),
        "scenes": [{"title": scene["title"], "start": scene_start(i, total_duration)} for i, scene in enumerate(SCENES)],
    }
    (ROOT / "build_meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
