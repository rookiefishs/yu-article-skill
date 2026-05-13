# 视频输出规则

## 适用场景
- 用户要做视频策划
- 用户要视频大纲、配音稿、素材清单、视频工程准备
- 用户明确要按视频形式产出

## 强制前置判断
- 如果没指定输出形式，不要默认走视频
- 如果指定视频但没说设计方向，先问
- 如果用户说“用默认”，读取 `assets/design-default/DESIGN.md`

## 默认产物
- `素材文件/`
  - `DESIGN.md`
  - `标题-大纲.md`
  - `标题-配音文件.md`
  - `标题-配音.mp3`（通过 TTS 脚本生成）
  - 其他素材说明或素材清单
- `视频工程/`
- `标题.mp4`（最终成品视频，直接放文章文件夹根目录）

## 文件归档规则
- 视频相关的规划与源文档统一放入 `素材文件/`
- `DESIGN.md` 不再放文章根目录，放到 `素材文件/DESIGN.md`
- `*-大纲.md` 不再放文章根目录，放到 `素材文件/`
- `*-配音文件.md` 不再放文章根目录，放到 `素材文件/`
- 最终视频成品必须放文章文件夹根目录
- 最终视频命名为当前主题：`当前主题.mp4`
- 如果文章目录名带 `待-`、`待3-`、`001-` 这类状态/序号前缀，视频文件名去掉这些前缀，只保留主题本身

## 大纲文件要求
- 用时间轴片段格式
- 例如：`[00:00:05] 这里讲什么`
- 每一段都要写清楚对应内容
- 节奏上要能支持后续配音和画面对齐

## 配音文件要求
- 按段落拆分，每段用时间轴标注
- 一段一段写清楚
- 语言适合直接拿去生成音频
- 不要把整篇连成一整坨
- 多音字使用 SSML `<phoneme>` 标签标注
- 需要停顿的位置使用 `<break time="500ms" />` 标签
- 文末附完整连续文案供直接使用
- 具体 SSML 标签格式和脚本用法见 `references/tts-rules.md`

## 排版要求
- 视频文稿中，段落与段落之间保留一个空行
- 同一段内部不要为了断句再额外换行
- 不要出现连续多个空行
- 整体排版要清楚，方便后续配音和视频工程继续使用

## DESIGN.md 要求
- 如果用户有明确设计方向，按用户要求写
- 如果用户说用默认，就基于 `assets/design-default/DESIGN.md`
- 默认视频风格现在是：**温暖纸感 editorial + 统一页面壳 + 整页横向过渡**
- 不要在没确认设计方向时自己乱定视觉路线

## 素材规则
- 专有素材必须向用户要
- 通用素材可以自行建议或补充
- 如果缺关键素材，就直接列清素材清单，让用户放到 `素材文件/`

## TTS 音频生成
- 配音文件写好后，使用 `scripts/tts-generate.js` 脚本生成音频
- 默认语音模型：`云希 (zh-CN-YunxiNeural)`，适合教程类旁白
- 脚本会自动按段落分段生成，然后合并为一个完整音频文件
- 如果已有目标视频，脚本可以直接把音频合并到视频中

生成命令：
```bash
node scripts/tts-generate.js --input 标题-配音文件.md --output 标题-配音.mp3
```

合并到视频：
```bash
node scripts/tts-generate.js --input 标题-配音文件.md --output 标题-配音.mp3 --video 原视频.mp4 --video-output 成品视频.mp4
```

## 视频工程说明
- `视频工程/` 基于 `assets/video-template/` 模板搭建
- 模板包含：构建脚本、渲染脚本、HTML框架、CSS主题、GSAP动画
- 默认模板使用统一页面壳，正文页共享同一布局骨架
- 默认转场必须是整页 push / slide，下一页完整覆盖上一页
- 渲染完成后，最终 `.mp4` 直接输出到文章根目录，并按当前主题命名
- 制作流程详见 `references/video-production-workflow.md`
- 本 skill 当前阶段先负责把内容和结构准备好
- 是否现在开始制作视频，要继续问用户

## SCENES 字段规范

每个场景必须包含以下字段：

| 字段 | 说明 | 约束 |
|------|------|------|
| title | 主标题 | ≤8 个字，不要用 
 换行 |
| accent | 副标题 | ≤15 个字 |
| caption | 底部金句 | ≤20 个字，每页不同 |
| voice | 配音文案 | 口语化，8-15秒时长 |
| kind | 场景类型 | intro-cover / hook / hero / terminal / checklist / warning / closing |
| series | 系列名称 | 所有页面统一，显示在 meta-bar 左侧 |
| kicker | 分类标签 | ≤4 个字，显示在 meta-bar 下方 |

## 音频参数规范

渲染时 ffmpeg 必须使用以下音频滤镜：
```
-af volume=12dB,aresample=44100,aformat=channel_layouts=stereo
```
原因：edge-tts 默认输出 24kHz mono MP3，直接编码为 AAC 会导致部分播放器无法解码。必须先升采样到 44.1kHz stereo 再编码。

## 视频模板快速启动
1. 复制 `assets/video-template/` 到 `视频工程/`
2. 修改 `build_hyperframes_video.py` 中的 `SCENES` 数组（每个场景必须有 `series` 和 `kicker` 字段）
3. 把配图放到 `../image/` 目录（从 `2.png` 开始）
4. 运行 `python build_hyperframes_video.py` 生成 HTML 和音频
5. 确认 `render_with_puppeteer.js` 中 ffmpeg 命令包含音频滤镜：`-af volume=12dB,aresample=44100,aformat=channel_layouts=stereo`
6. 运行 `node render_with_puppeteer.js` 渲染视频，成品会输出到文章根目录：`当前主题.mp4`
