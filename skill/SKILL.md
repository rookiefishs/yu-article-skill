---
name: yu-article-skill
description: Create content production outputs for 长文、图文、视频 in a consistent AI 编程内容风格. Use when the user wants topic planning, preview drafting, 正文 writing, 封面提示词, 配图提示词, 视频大纲, 配音文本, or structured content directories. If the user has not specified the output form, default to 长文. If the user chooses 视频 and does not provide a visual direction, use the built-in default video spec in this skill: 浅色简约、紫蓝渐变、整页滑动转场、统一页面壳； only ask follow-up questions when the user explicitly wants a different visual style. When the user provides a short-video share link or copied share text, first read the visible/shared video information, then search the web for related materials, and then generate content in the requested output form.
---

# yu-article-skill

## 目标
按固定流程产出长文、图文、视频内容，优先保证：
- 输出结构稳定
- 目录命名统一
- 内容风格贴合 AI 编程账号
- 视频默认直接套用已验证的模板规范，不再从零试样式

## 默认输出形态
- 用户没指定输出形态：默认产出`长文`
- 用户指定`图文`：按图文目录规范输出
- 用户指定`视频`：按本 skill 的默认视频规范输出

## 视频硬规则
1. 用户明确说“视频默认”或未给视觉方向时，直接使用内置默认视频规范，不反复追问样式。
2. 用户明确给了新的视觉方向，再覆盖默认视频规范。
3. 视频默认控制在 1 分钟左右；除非用户明确要求长视频，最好不要超过 2 分钟。
4. 视频相关源文件统一放进`素材文件/`，最终成片直接放文章根目录。
5. 视频工程默认从`assets/video-template/`复制，不要临时重新搭一套新模板。
6. 视频排版、边距、颜色、转场、预览方式，统一遵守：
   - `references/output-video.md`
   - `references/video-production-workflow.md`
   - `assets/design-default/DESIGN.md`
7. 做视频时，优先先出 4 秒预览确认视觉，再决定是否批量渲染整条视频。

## 工作流
按这个顺序执行：
1. 接收主题、标题、链接、已有草稿或现成素材
2. 如果有短视频分享链接，先读分享文案和公开页面信息，再联网补背景资料
3. 整理主题标题与内容方向
4. 生成预览大纲
5. 根据用户要求选择输出形态；未指定则默认长文
6. 创建对应目录和文件
7. 如果是视频：
   - 先写`素材文件/DESIGN.md`
   - 再写`素材文件/标题-大纲.md`
   - 再写`素材文件/标题-配音文件.md`
   - 配音稿和页面数量按 1 分钟左右控制，通常不要超过 2 分钟
   - 再准备`image/`
   - 再复制并修改`视频工程/`
   - 先导出 4 秒预览，确认后再继续整条

## 目录规则
目录名只用两种：
- `序号-标题`
- `待-标题`

如果用户没指定序号，默认用：
- `待-标题`

## 输出规范导航
按需读取：
- `references/output-longform.md`：长文输出规则
- `references/output-graphic-post.md`：图文输出规则
- `references/output-video.md`：视频结构、边距、配色、转场规则
- `references/video-production-workflow.md`：视频落地流程、预览、渲染与验收
- `references/tts-rules.md`：配音文本与 SSML 规则
- `references/video-assets-rules.md`：视频素材准备规则
- `references/style-rules.md`：通用写作风格规则
- `references/platform-safety.md`：平台安全边界

## 工作原则
- 先给可执行结果，再补说明
- 默认最小可交付，不做无关扩写
- 视频模板一旦确认样式，后续优先复用，不要每次重新发明版式
