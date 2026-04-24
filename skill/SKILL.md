---
name: yu-article-skill
description: Create content production outputs for 长文、图文、视频 in a consistent AI 编程内容风格. Use when the user wants topic planning, preview drafting, 正文 writing, 封面提示词, 配图提示词, 视频大纲, 配音文本, or structured content directories. If the user has not specified the output form, ask them to choose 长文、图文、视频 before continuing. If the user chooses 视频 but has not specified the visual design direction, ask first before generating video outputs.
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

1. 如果用户没明确说输出形式是 `长文 / 图文 / 视频`，先问清楚，再继续。
2. 如果用户要做视频，但没明确视频样式方向，先问清楚，再继续。
3. 如果用户说视频“用默认”，再读取 `assets/design-default/DESIGN.md`。
4. 如果用户要图文，且内容需要配图，默认补 `配图提示词/` 目录，封面提示词统一放在 `配图提示词/封面提示词.md`，不要再额外保留根目录 `标题-封面提示词.md`。
5. 如果用户要长文，且内容需要配图，默认补 `标题-配图提示词.md`。
6. 不要默认补 `README.md`、`标题-发布文案.md`、`标题-长文.md`、`标题-纯正文.md` 这类旧产物。

## Workflow

按这个顺序执行：
1. 主题标题
2. 内容 / 大纲确定
3. 生成预览版本
4. 获取输出形式
5. 生成对应目录
6. 如果是视频，询问用户是否现在开始制作

不要跳步骤。
不要在没确认输出形式时直接生成最终目录。

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
  - `01-配图提示词.md`
  - `02-配图提示词.md`
  - `...`
  - `配图参考图.png`
  - `封面参考图.png`
- `image/`

具体写法、排版与约束见：
- `references/output-graphic-post.md`

### 视频

默认产物：
- `DESIGN.md`
- `标题-大纲.md`
- `标题-配音文件.md`
- `标题-配音.mp3`（通过脚本生成）
- `素材文件/`
- `视频工程/`

具体写法、排版与约束见：
- `references/output-video.md`
- `references/video-assets-rules.md`
- `references/tts-rules.md`

## Reference navigation

按需要读取这些文件：
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
