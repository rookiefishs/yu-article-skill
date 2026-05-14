# 视频生产流程规范

基于已验证模板的固定流程，后续同类视频默认按此执行。

## 总流程
主题确认 → 拆页 → 配音稿 → 归档到素材文件 → 准备配图 → 复制视频模板 → 生成 HTML/音频 → 导出 4 秒预览 → 用户确认 → 渲染整片

## 1. 内容拆页
- 默认拆成 5-8 页
- 每页只讲一个点
- 所有正文页共用同一页面骨架
- 每页都要有不同的 caption

## 2. 配音稿
- 给每页写对应旁白
- 口语化，不要写成念稿腔
- 配音文件写入：`素材文件/标题-配音文件.md`
- 整条连贯版文案放在文件末尾，便于直接合成整条旁白

## 3. 视觉规范落盘
- `素材文件/DESIGN.md`写明默认视频风格
- 如果用户没有给新样式，直接写默认规范：
  - 1080x1920
  - 主体卡片边距 100px
  - 浅色简约
  - 浅蓝主色 + 浅紫辅助
  - 整页滑动覆盖转场

## 4. 素材准备
- 配图放在`image/`
- 按页命名：`1.png`、`2.png`、`3.png`...
- 如果封面也要图，就允许 `1.png`
- 配图尺寸建议接近 16:9 或适合容器展示

## 5. 视频工程初始化
- 从 `assets/video-template/`复制到文章目录下的`视频工程/`
- 不要重新手写新工程
- 修改：
  - `build_hyperframes_video.py`
  - 必要时修改 `README.md`

## 6. 工程脚本规则
### build_hyperframes_video.py
默认要求：
- 生成 `index.html`
- 生成 `build_meta.json`
- 生成 `assets/narration.mp3`
- 把默认 `DESIGN.md`写入`素材文件/`
- 主体卡片样式按默认规范输出

### render_with_puppeteer.js
默认要求：
- 支持整片渲染
- 支持通过环境变量导出 4 秒预览：`PREVIEW_SECONDS=4`
- 最终视频输出到文章根目录
- 同时保留 `renders/output-video.mp4` 兼容路径

## 7. 预览流程（固定）
先跑：
```bash
python build_hyperframes_video.py
```
再跑 4 秒预览：
```bash
PREVIEW_SECONDS=4 node render_with_puppeteer.js
```
Windows PowerShell：
```powershell
$env:PREVIEW_SECONDS='4'
node render_with_puppeteer.js
```

## 8. 预览验收点
至少检查：
- 主体卡片边距是否正确
- 渐变是否太重 / 太浅
- 紫色是否喧宾夺主
- 切页是否整页覆盖
- 首屏是否闪烁
- 配图容器和底部字幕条是否和主卡片统一

## 9. 整片渲染
预览通过后，再跑：
```bash
node render_with_puppeteer.js
```

## 10. 默认验收清单
- [ ] 主体卡片边距 = 100px
- [ ] 主体卡片不是纯白板
- [ ] 紫色比蓝色更克制
- [ ] 边框清晰但不过重
- [ ] 整页滑动覆盖转场正常
- [ ] 4 秒预览通过后再整片渲染
- [ ] 成片输出在文章根目录
