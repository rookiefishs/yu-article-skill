# TTS 配音规范

## 适用场景
- 视频配音文案需要生成音频
- 需要生成无标点、无格式符号、空白分隔的正常朗读文本
- 使用 `scripts/tts-generate.js` 脚本生成音频并合并到视频
- 使用 `scripts/mimo-tts-bingtang.py` 脚本生成小米 MiMo 冰糖音色配音

## 配音文本硬规则
- 配音文本只写正常朗读内容，不写 SSML、HTML、Markdown、时间轴或任何格式符号。
- 不使用 `<break time="300ms" />`、`<phoneme>`、`[00:00:00]`、`---`、代码块、标题标记。
- 不使用任何标点符号，包括逗号、句号、顿号、冒号、问号、感叹号、括号、引号、斜杠、连接号。
- 句子和停顿只用空白隔开。
- 数字读音要直接写成期望读法。比如 `第 2 期` 必须写成 `第二期`，不要写成阿拉伯数字，避免读成“两”。
- 英文技术词可以保留英文原文，比如 `GSAP`、`AI`、`HTML`、`HyperFrames`。
- 配音文件可以只保留一段完整纯文本，方便直接送入 TTS。

## 技术基础
默认使用小米 MiMo TTS 生成视频旁白：
- 默认使用 `mimo-v2.5-tts`
- 默认音色使用 `冰糖`
- 默认接口使用 `https://token-plan-cn.xiaomimimo.com/v1`
- API Key 从环境变量 `MIMO_API_KEY` 读取

旧的微软 Azure TTS 路线仍保留：
- 通过 `scripts/tts-generate.js` 脚本调用
- 支持 SSML 标签、分段生成、合并音频和直接合并到视频
- 只在用户明确要求微软/Azure 音色，或 MiMo 不可用且用户接受降级时使用

## 推荐语音模型

### 小米 MiMo（默认视频旁白）
| 模型 | 音色 | 特点 |
|------|------|------|
| mimo-v2.5-tts | 冰糖 | 中文女声，自然清晰，适合短视频口播和 AI 编程教程内容 |

默认使用小米 MiMo `冰糖` 音色，通过 `scripts/mimo-tts-bingtang.py` 生成。

### 微软男声（备用）
| 模型 | ID | 特点 |
|------|-----|------|
| 云希 | zh-CN-YunxiNeural | 年轻男声，自然清晰，适合科技/教程类旁白 |
| 云健 | zh-CN-YunjianNeural | 成年男声，沉稳有力，适合正式解说 |
| 云扬 | zh-CN-YunyangNeural | 成年男声，新闻播报感 |
| 云枫 | zh-CN-YunfengNeural | 成年男声，磁性低沉 |

### 微软女声（备用）
| 模型 | ID | 特点 |
|------|-----|------|
| 晓晓 | zh-CN-XiaoxiaoNeural | 年轻女声，活泼自然，适合短视频 |
| 晓伊 | zh-CN-XiaoyiNeural | 年轻女声，温柔知性 |
| 晓柔 | zh-CN-XiaorouNeural | 年轻女声，柔和舒缓 |
| 晓梦 | zh-CN-XiaomengNeural | 年轻女声，甜美清亮 |

如果用户明确选择微软 TTS，优先使用 `云希 (zh-CN-YunxiNeural)`。

## 微软 TTS 基础参数
以下参数仅适用于 `scripts/tts-generate.js` 微软 TTS 备用路线。

| 参数 | 默认值 | 说明 |
|------|--------|------|
| rate | `0` | 语速，范围 -100 到 100。视频旁白建议 -5 到 5 之间 |
| pitch | `0` | 音调，范围 -100 到 100 |
| volume | `125` | 音量，范围 0 到 100；本脚本实测支持高于 100 的增益值，视频旁白默认用 125，避免后期手动调高 |
| kbitrate | `audio-48khz-192kbitrate-mono-mp3` | 高质量输出，视频用 |

## 配音文案文件规范

### 文件名
`标题-配音文件.md`

### 文件结构
- 默认只保留一段完整纯文本
- 文本里不写标题、时间轴、SSML、Markdown 或标点
- 停顿通过空白自然分隔，不写标签
- 多音字和数字读法直接改写成想要朗读的汉字

### 结构示例

```markdown
大家好 今天我们来聊一个很实用的话题 很多人觉得 AI 写代码就是自动补全 但它能做的事比你想的多得多 关键不是工具本身 是你怎么用它
```

## 脚本使用方法

### 小米 MiMo 冰糖音色
脚本路径：`scripts/mimo-tts-bingtang.py`

默认从配音文件生成冰糖音色：
```bash
python scripts/mimo-tts-bingtang.py --input 标题-配音文件.md --output 标题-小米TTS-冰糖.wav
```

直接传入短文本：
```bash
python scripts/mimo-tts-bingtang.py --text "你好，这是一段小米冰糖音色测试。" --output test-bingtang.wav
```

可选参数：
- `--style`：传入自然语言风格，比如“中文科技短视频旁白，清晰自然，语速略快”
- `--voice`：默认 `冰糖`，如需测试其他 MiMo 内置音色再覆盖
- `--base-url`：默认 `https://token-plan-cn.xiaomimimo.com/v1`
- `--save-text`：保存从配音文件中提取出来的朗读文本

脚本会自动清理旧文件中的格式符号和标点，但新生成的配音文件必须直接写成纯文本，不要依赖脚本兜底。

### 微软 TTS 备用脚本
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
