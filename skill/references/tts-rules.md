# TTS 配音规范

## 适用场景
- 视频配音文案需要生成音频
- 需要控制多音字读音、停顿等细节
- 使用 `scripts/tts-generate.js` 脚本生成音频并合并到视频

## 技术基础
底层使用微软 Azure TTS 引擎，支持 SSML 标签。
通过 `scripts/tts-generate.js` 脚本调用，脚本会自动分段、逐段生成、合并音频，支持直接合并到视频。

## 推荐语音模型

### 男声（视频旁白首选）
| 模型 | ID | 特点 |
|------|-----|------|
| 云希 | zh-CN-YunxiNeural | 年轻男声，自然清晰，适合科技/教程类旁白 |
| 云健 | zh-CN-YunjianNeural | 成年男声，沉稳有力，适合正式解说 |
| 云扬 | zh-CN-YunyangNeural | 成年男声，新闻播报感 |
| 云枫 | zh-CN-YunfengNeural | 成年男声，磁性低沉 |

### 女声
| 模型 | ID | 特点 |
|------|-----|------|
| 晓晓 | zh-CN-XiaoxiaoNeural | 年轻女声，活泼自然，适合短视频 |
| 晓伊 | zh-CN-XiaoyiNeural | 年轻女声，温柔知性 |
| 晓柔 | zh-CN-XiaorouNeural | 年轻女声，柔和舒缓 |
| 晓梦 | zh-CN-XiaomengNeural | 年轻女声，甜美清亮 |

默认使用 `云希 (zh-CN-YunxiNeural)`，适合账号定位的 AI 编程教程内容。

## 基础参数
| 参数 | 默认值 | 说明 |
|------|--------|------|
| rate | `0` | 语速，范围 -100 到 100。视频旁白建议 -5 到 5 之间 |
| pitch | `0` | 音调，范围 -100 到 100 |
| volume | `125` | 音量，范围 0 到 100；本脚本实测支持高于 100 的增益值，视频旁白默认用 125，避免后期手动调高 |
| kbitrate | `audio-48khz-192kbitrate-mono-mp3` | 高质量输出，视频用 |

## 多音字标注

用 SSML `<phoneme>` 标签标注多音字读音。

格式：`<phoneme alphabet="sapi" ph="拼音 声调">字</phoneme>`

声调规则：1 = 一声，2 = 二声，3 = 三声，4 = 四声，5 = 轻声。

### 常见多音字示例

```
<phoneme alphabet="sapi" ph="hai 2">还</phoneme>有
<phoneme alphabet="sapi" ph="huan 2">还</phoneme>给你
无法<phoneme alphabet="sapi" ph="zhuo 2">着</phoneme>手对付
让他<phoneme alphabet="sapi" ph="gan 1">干</phoneme><phoneme alphabet="sapi" ph="zhao 1">着</phoneme>急
木<phoneme alphabet="sapi" ph="tou 5">头</phoneme>
这个<phoneme alphabet="sapi" ph="jiao 3">角</phoneme>度
扮演<phoneme alphabet="sapi" ph="jue 2">角</phoneme>色
<phoneme alphabet="sapi" ph="chu 3">处</phoneme>理问题
```

原则：
- 只标注需要纠正的多音字，其余正常书写
- 一个 phoneme 标签只包裹一个字
- ph 属性中拼音和声调之间用空格分隔

## 停顿控制

用 `<break>` 标签插入停顿。

格式：`<break time="毫秒ms" />`

### 常用停顿
| 场景 | 写法 | 时长 |
|------|------|------|
| 句间换气 | `<break time="300ms" />` | 0.3秒 |
| 场景切换 | `<break time="500ms" />` | 0.5秒 |
| 段落结束 | `<break time="800ms" />` | 0.8秒 |
| 重点强调前 | `<break time="1000ms" />` | 1秒 |
| 长停顿/转场 | `<break time="2000ms" />` | 2秒 |
| 特殊停顿 | `<break time="5000ms" />` | 5秒 |

## 配音文案文件规范

### 文件名
`标题-配音文件.md`

### 文件结构
- 按场景分段，每段用时间轴标注
- 段落之间保留一个空行
- 每段文案直接可用于生成音频
- 多音字和停顿标签直接写在文案文本里

### 结构示例

```markdown
[00:00:00] 开场

大家好，今天我们来聊一个很实用的话题。<break time="500ms" />

[00:00:05] 核心观点

很多人觉得 AI 写代码就是自动补全，但实际上它能<phoneme alphabet="sapi" ph="gan 4">干</phoneme>的事比你想的多得多。<break time="300ms" />关键不是工具本身，而是你怎么用它。

[00:00:15] 结尾

好了，今天就聊到这里。<break time="1000ms" />觉得有用的话点个关注，下期再见。
```

### 文末附完整连续文案
在分段文案之后，附一份去掉时间轴标注的完整连续文案，方便直接复制使用：

```markdown
---

## 完整文案

大家好，今天我们来聊一个很实用的话题。<break time="500ms" />

很多人觉得 AI 写代码就是自动补全，但实际上它能<phoneme alphabet="sapi" ph="gan 4">干</phoneme>的事比你想的多得多。<break time="300ms" />关键不是工具本身，而是你怎么用它。

好了，今天就聊到这里。<break time="1000ms" />觉得有用的话点个关注，下期再见。
```

## 脚本使用方法

脚本路径：`scripts/tts-generate.js`

### 从配音文件生成音频
```bash
node scripts/tts-generate.js --input 标题-配音文件.md --output 标题-配音.mp3
```

### 指定语音模型
```bash
node scripts/tts-generate.js --input 配音文件.md --voice 云健 --output output.mp3
```

### 生成音频并合并到视频
```bash
node scripts/tts-generate.js --input 配音文件.md --output dubbing.mp3 --video 原视频.mp4 --video-output 成品视频.mp4
```

### 短文本直接生成
```bash
node scripts/tts-generate.js --text "你好，这是一段测试" --output test.mp3
```

### 查看可用语音
```bash
node scripts/tts-generate.js --list-voices
```
