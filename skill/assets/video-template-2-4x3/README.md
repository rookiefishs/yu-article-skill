# 2号视频模板（4:3）

这是 `yu-article-skill` 的 2号视频规范模板。

适用场景：
- 用户指定 `2号视频规范`
- 用户指定 `2号视频模板`
- 用户要求 4:3 横版浅色科技图文风
- 用户说要用上次 superpowers 那种效果

## 使用方法
1. 复制整个 `video-template-2-4x3` 目录到新视频项目的 `视频工程/`
2. 修改 `build_hyperframes_video.py` 中的 `TITLE` 和 `SCENES` 数组
3. 准备 `../image/` 中的配图素材
4. 先生成 HTML 和音频
5. 先导出 4 秒预览确认视觉
6. 预览通过后再渲染整片

## 命令流程
```bash
# 1. 生成 HTML / 元数据 / 整条旁白
python build_hyperframes_video.py

# 2. 先导出 4 秒预览
PREVIEW_SECONDS=4 node render_with_puppeteer.js

# 3. 预览通过后渲染整片
node render_with_puppeteer.js
```

Windows PowerShell：
```powershell
python build_hyperframes_video.py
$env:PREVIEW_SECONDS='4'
node render_with_puppeteer.js
Remove-Item Env:PREVIEW_SECONDS
node render_with_puppeteer.js
```

## 默认视觉规范
- 1440x1080，4:3，24fps
- 主体卡片整体边距：72px
- 浅色科技图文风
- 浅蓝和暖白为主，浅紫辅助
- 左文案、右素材截图、底部字幕条
- 整页滑动覆盖转场
- 首帧直接在位，不空白开场
- 截图容器优先完整展示，不裁掉关键信息

## 文件说明
- `build_hyperframes_video.py`：生成 HTML、元数据、整条旁白
- `render_with_puppeteer.js`：导出预览或整片
- `build_meta.json`：场景元数据
- `assets/narration.mp3`：整条旁白音频
- `renders/preview-4s.mp4`：4 秒预览
- `../当前主题.mp4`：最终成片

## 注意事项
- `assets/gsap.min.js` 需要手动放置
- 需要可用的 `puppeteer` 或 `puppeteer-core`；使用 Codex 捆绑依赖时设置 `CODEX_NODE_MODULES`
- Chrome 默认从 `PUPPETEER_EXECUTABLE_PATH`、`CHROME_PATH` 或系统安装目录发现
- MiMo 脚本默认从已安装的 `yu-article-skill` 查找；自定义位置时设置 `YU_ARTICLE_TTS_SCRIPT`
- 预览阶段默认先看 4 秒，不要一开始直接整片渲染
- 本模板只在用户指定 2号视频规范时使用
- 如果用户没有指定新样式，直接沿用 skill 默认竖屏视频规范
