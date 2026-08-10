# TTS 配音规范

## 适用场景

- 视频配音文案需要生成音频
- 需要生成无标点、无格式符号、空白分隔的正常朗读文本
- 使用 `scripts/mimo-tts-bingtang.py` 生成小米 MiMo 冰糖音色配音

## 配音文本硬规则

- 只写正常朗读内容，不写 SSML、HTML、Markdown、时间轴或格式符号。
- 不使用标点符号；句子和停顿只用空白隔开。
- 数字直接写成期望读法，例如把 `第 2 期` 写成 `第二期`。
- 英文技术词可以保留原文，例如 `GSAP`、`AI`、`HTML`、`HyperFrames`。
- 配音文件默认只保留一段完整纯文本，方便直接送入 TTS。

## 默认技术路线

| 项目 | 默认值 |
| --- | --- |
| 脚本 | `scripts/mimo-tts-bingtang.py` |
| 接口 | `https://token-plan-cn.xiaomimimo.com/v1` |
| 模型 | `mimo-v2.5-tts` |
| 音色 | `冰糖` |
| 凭据 | 环境变量 `MIMO_API_KEY` |

不要把 API Key、会话令牌、Cookie 或其他凭据写入 Skill、脚本、命令示例或生成文件。

## 配音文案文件

文件名使用 `标题-配音文件.md`。

示例：

```text
大家好 今天我们来聊一个很实用的话题 很多人觉得 AI 写代码就是自动补全 但它能做的事比你想的多得多 关键不是工具本身 是你怎么用它
```

## 使用方法

从配音文件生成音频：

```powershell
python scripts/mimo-tts-bingtang.py --input "标题-配音文件.md" --output "标题-小米TTS-冰糖.wav"
```

直接传入短文本：

```powershell
python scripts/mimo-tts-bingtang.py --text "你好 这是一段小米冰糖音色测试" --output "test-bingtang.wav"
```

可选参数：

- `--style`：自然语言风格，例如“中文科技短视频旁白 清晰自然 语速略快”。
- `--voice`：默认 `冰糖`，需要测试其他 MiMo 内置音色时再覆盖。
- `--base-url`：覆盖默认接口地址。
- `--save-text`：保存从配音文件中提取的朗读文本。

脚本会清理旧文件中的格式符号和标点，但新配音文件必须直接符合本规范，不依赖脚本兜底。

## 失败处理

- 缺少 `MIMO_API_KEY`：停止调用并提示配置环境变量。
- 接口失败或返回无音频：保留原始错误，不自动切换到未经验证的第三方接口。
- 用户明确要求其他 TTS：先确认目标服务、凭据来源和调用成本，再使用对应的官方或已授权实现。
