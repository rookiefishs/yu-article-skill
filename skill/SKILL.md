---
name: yu-article-skill
description: Create content production outputs for 长文、图文、视频 in a consistent AI 编程内容风格. Use when the user wants topic planning, preview drafting, 正文 writing, 封面提示词, 配图提示词, 视频大纲, 配音文本, or structured content directories. If the user has not specified the output form, default to 长文. If the user chooses 视频 but has not specified the visual design direction, ask first before generating video outputs. When the user provides a short-video share link or copied share text, first read the visible/shared video information, then search the web for related materials, and then generate content in the requested output form.
---

# yu-article-skill

## Overview

用这套规则做内容产出。
目标不是一上来补齐一整套旧式稿件，而是按用户当前要的输出形式，走一套更稳的内容生产流程。

支持的输出形式只有三类：
- 长文
- 图文
- 视频

优先处理这几类任务：
- 给一个主题做内容策划和预览
- 按指定形式产出目录和文件
- 把现有稿子改成当前账号风格
- 生成封面提示词
- 生成正文配图提示词
- 生成视频大纲、配音文本、素材清单

## Mandatory gating rules

这几条是硬规则，不能跳：

1. 如果用户没明确说输出形式是 `长文 / 图文 / 视频`，默认按 `长文` 继续，不再反复追问。
2. 如果用户要做视频，但没明确视频样式方向，先问清楚，再继续。
3. 如果用户说视频“用默认”，再读取 `assets/design-default/DESIGN.md`。
4. 如果用户要图文，且内容需要配图，默认补 `配图提示词/` 目录，封面提示词放在 `配图提示词/封面提示词.md`，所有正文配图提示词合并到一个 `配图提示词/配图提示词.md`，不要再额外保留根目录 `标题-封面提示词.md`。
5. 如果用户要长文，且内容需要配图，默认补 `标题-配图提示词.md`。
6. 不要默认补 `README.md`、`标题-发布文案.md`、`标题-长文.md`、`标题-纯正文.md` 这类旧产物。
7. 如果用户粘贴短视频分享链接或复制分享文案，先阅读分享文案和公开页面能看到的视频信息，再联网搜索相关背景资料，最后按用户指定形式生成内容；如果用户没有指定形式，默认生成长文。

## Workflow

按这个顺序执行：
1. 接收主题、标题、链接、视频分享文案或已有素材
2. 如果包含视频分享链接，先解析分享文案和链接中的公开信息
3. 尝试读取公开视频页面可见内容，包括标题、简介、标签、作者、页面文本和公开结构化信息
4. 如果视频页面信息不足，根据标题、简介、标签和关键词联网搜索相关资料
5. 整理主题标题
6. 内容 / 大纲确定
7. 生成预览版本
8. 获取输出形式；如果用户未指定，默认使用长文
9. 生成对应目录
10. 如果是视频，询问用户是否现在开始制作

不要跳步骤。
用户没有指定输出形式时，可以按默认长文生成最终目录。

## Short-video share link workflow

当用户粘贴抖音、TikTok、小红书、B站或其他短视频分享链接时，先按这个流程处理：

1. 先读取用户复制出来的分享文案，提取标题、简介、话题标签、作者信息、短链和用户额外要求。
2. 打开短链或公开页面，读取页面可见信息；能看到什么就用什么，不假装拿到了完整口播。
3. 优先提取公开视频页面里的标题、描述、标签、发布时间、作者、页面文本和公开结构化数据。
4. 如果视频没有公开字幕或页面限制访问，就把“已确认的信息”和“无法确认的信息”分开。
5. 根据视频标题、标签、工具名、项目名、关键词联网搜索更多资料，优先查官方文档、GitHub、项目主页、可信教程和更新日志。
6. 不直接搬运原视频顺序和原句，而是把视频方向、公开信息和联网资料重新组织成适合账号风格的内容。
7. 根据用户指定的 `长文 / 图文 / 视频` 继续生成；如果用户没指定，默认按 `长文` 生成。
8. 生成前仍然遵守当前形式的正文、封面、配图、视频和平台安全规则。

## Directory naming rules

目录名只用这两种：
- `序号-标题`
- `待-标题`

如果用户没有指定序号，默认用：
- `待-标题`

目录名直接跟最终标题走，不要改写成别的说法。

## Output form selection

### 长文

默认产物：
- `标题-正文.md`
- `标题-封面提示词.md`
- `标题-配图提示词.md`（如果需要配图则补）
- `image/`

具体写法、排版与约束见：
- `references/output-longform.md`

### 图文

默认产物：
- `标题-正文.md`
- 不生成根目录 `标题-封面提示词.md`
- `配图提示词/`
  - `封面提示词.md`
  - `配图提示词.md`
  - `配图参考图.png`
  - `封面参考图.png`
- `image/`

具体写法、排版与约束见：
- `references/output-graphic-post.md`

### 视频

默认产物：
- `素材文件/`
  - `DESIGN.md`
  - `标题-大纲.md`
  - `标题-配音文件.md`
  - `标题-配音.mp3`（通过脚本生成）
- `视频工程/`
- `标题.mp4`（最终成品视频，直接放文章文件夹根目录）

具体写法、排版与约束见：
- `references/output-video.md`
- `references/video-assets-rules.md`
- `references/tts-rules.md`

## Reference navigation

按需要读取这些文件：
- `references/video-production-workflow.md`：视频生产完整流程（拆页、排版、动画、渲染）
- `references/tts-rules.md`：TTS 配音规范（SSML 标签、多音字、停顿、脚本用法）
- `references/output-longform.md`：长文规则
- `references/output-graphic-post.md`：图文规则
- `references/output-video.md`：视频规则
- `references/cover-prompt-rules.md`：封面提示词规则
- `references/illustration-prompt-rules.md`：正文配图提示词规则
- `references/video-assets-rules.md`：视频素材规则
- `references/style-rules.md`：通用写作硬规则
- `references/article-archetypes.md`：题型与组织方式
- `references/account-context.md`：账号定位与用户上下文
- `references/platform-safety.md`：平台安全边界

## Working principles

默认遵守这些总原则：
- 先讲结论，再讲原因，再讲动作或例子
- 不写说明书口吻
- 具体风格规则看 `references/style-rules.md`
- 平台发布安全边界看 `references/platform-safety.md`
