# 视频模板工程

## 使用方法

1. 复制整个 `video-template` 目录到新视频项目
2. 修改 `build_hyperframes_video.py` 中的 `SCENES` 数组
3. 修改封面和场景内容
4. 准备配图到 `../image/` 目录（从 `2.png` 开始）
5. 运行生成脚本，最终视频会输出到文章目录根目录

## 命令流程

```bash
# 1. 生成HTML和音频
python build_hyperframes_video.py

# 2. 渲染视频
node render_with_puppeteer.js
```

## 文件说明

- `build_hyperframes_video.py`: 主构建脚本，生成HTML和音频
- `render_with_puppeteer.js`: Puppeteer渲染脚本，截帧合成视频
- `index.html`: 生成的视频页面（自动更新）
- `build_meta.json`: 场景元数据（自动生成）
- `assets/gsap.min.js`: GSAP动画库（需要手动放置）
- `assets/narration.mp3`: 合并后的音频（自动生成）
- `../当前主题.mp4`: 最终视频，直接放文章文件夹根目录
- `renders/output-video.mp4`: 兼容/中间输出，不作为默认交付位置

## 配图要求

- 封面页面不显示配图
- 从第二个场景开始使用配图
- 配图文件放在上级目录的 `image/` 文件夹
- 文件命名：`2.png`, `3.png`, `4.png`...
- 建议尺寸：1080x720 或类似比例

## 自定义

修改 `SCENES` 数组中的以下字段：
- `title`: 场景标题（支持换行）
- `accent`: 副标题
- `caption`: 底部字幕
- `voice`: 配音文本
- `kind`: 场景类型（hook/terminal/checklist等）

## 注意事项

- 需要安装 Node.js 和 Python
- 需要安装 puppeteer-core 和 edge-tts
- 需要安装 ffmpeg
- GSAP库需要手动下载放到 assets 目录
