# Changelog

## 2026/05/17

- Docs: 将 TTS 配音规范默认音量从 `75` 调整为 `125`，补充高于 100 的增益说明，减少视频旁白生成后还需手动调高音量的情况。
- Fix: 更新 `scripts/tts-generate.js` 默认 `volume` 为 `125`，并同步修改命令行帮助文案中的默认音量说明。

## 2026/05/15

- Refactor: 将视频模式默认行为从“先追问样式方向”调整为“直接套用内置默认视频规范”，统一使用浅色简约、浅蓝主色、浅紫辅助、整页滑动覆盖转场与统一页面壳。
- Docs: 重写视频输出规范、视频生产流程、默认设计说明与模板 README，明确主体卡片 100px 外边距、4 秒预览优先、源文件归档规则与整片渲染流程。
- Feat: 更新视频模板工程示例内容与构建脚本，补充默认场景字段、预览时序参数和模板使用说明，降低后续复用与出片成本。

## 2026/05/13

- Feat: 新增默认视频工程模板，统一为温暖纸感 editorial 风格、统一页面壳与整页横向覆盖式过渡，避免内容替换式换页抖动。
- Docs: 更新视频产物规范，明确最终成品视频输出到文章根目录并按当前主题命名，`DESIGN.md`、`*-大纲.md`、`*-配音文件.md` 统一归档到 `素材文件/`。

- Fix: 修复视频模板 CSS 双大括号转义问题，改为单大括号。
- Fix: 修复配图路径检查逻辑，从硬编码列表改为动态检测文件是否存在。
- Refactor: 移除 GSAP 动画中冗余的 opacity: 0 参数。
- Docs: 新增 SCENES 字段规范，定义 title/accent/caption/kinder/series/kicker 字数约束。
- Docs: 新增音频参数规范，明确 ffmpeg 必须使用 44.1kHz stereo 升采样。
- Docs: 更新安全区尺寸，适配抖音 UI 遮挡（左右 150px、底部 500px）。
- Docs: 新增卡片与容器样式规范，边框 opacity ≤ 0.08、双层阴影。
- Docs: 更新 meta-bar 规范，左侧显示系列名、右侧显示页码。
- Docs: 优化动画时序，首个正文页 enterAt 设为 1.7s 避免闪烁。
## 2026/05/07

- Docs: 补充短视频分享链接处理流程，明确先读取分享文案与公开页面信息，再联网补资料，并在未指定输出形式时默认按长文生成。
- Docs: 调整图文输出规范，明确开头段固定写 4 行，并同步补充内容写法、排版要求与当前图文库节奏说明。

## 2026/05/06

- Docs: 收紧图文正文表达约束，新增每段 4 到 5 行的节奏要求，减少空泛判断句式与重复辨析表达。
- Docs: 在 `references/output-graphic-post.md` 与 `references/style-rules.md` 中补充禁用表达，包括 `xx值得xx`、`xx清楚xx`、`xx更稳xx`、`xx划算xx` 等写法，统一后续图文稿件口径。

## 2026/04/25

- Assets: 图文参考图资源拆分为 `配图参考图.png` 与 `封面参考图.png`，同步替换旧的 `参考图.png` 与 `封面图.png` 命名，并更新相关规则与示例引用。
- Docs: 补充图文封面提示词迁移约束，明确图文场景下封面提示词只保留 `配图提示词/封面提示词.md`，不再生成或保留根目录 `标题-封面提示词.md`。
- Refactor: 调整图文产物结构，封面提示词改为统一放入 `配图提示词/封面提示词.md`，不再单独生成根目录 `标题-封面提示词.md`。
- Docs: 收紧图文配图提示词默认口径，默认仅保留基础提示词骨架，不再自动追加“补充风格约束”段落。
- Docs: 同步更新 `skill/SKILL.md`、图文输出规则、封面规则、配图规则与示例提示词，统一图文模式下的目录结构和生成行为。

## 2026/04/22

- Docs: 新增 `references/tts-rules.md`，包含 TTS 语音模型推荐、SSML 多音字与停顿标签规范、配音文案文件结构说明。
- Feat: 新增 `scripts/tts-generate.js`，支持从配音文件分段生成音频、合并音频、直接合并到视频。
- Refactor: `references/illustration-prompt-rules.md` 区分图文/长文配图数量规则，更新提示词格式为固定引导语加段落原文。
- Refactor: `references/output-graphic-post.md` 调整段落字数要求为 5 句左右，更新排版规则，配图改为图文每段一图。
- Feat: `references/output-video.md` 配音文件要求补充 SSML 标签说明，新增 TTS 音频生成章节与脚本用法。
- Docs: `references/output-longform.md` 排版补充段落序号规则。
- Docs: `skill/SKILL.md` 新增 `tts-rules.md` 引用与配音 mp3 产物说明。

## 2026/04/15

- Refactor: 将 skill 本体整体收口到 `skill/` 目录，根目录改为工作区说明，不再混放打包文件与工作区文档。
- Refactor: 重写 `skill/SKILL.md`，把流程收口为按 `长文 / 图文 / 视频` 分支驱动，并明确两个强制提问点，未指定输出形式先问、视频未指定设计方向先问。
- Docs: 新增 `output-longform.md`、`output-graphic-post.md`、`output-video.md`、`cover-prompt-rules.md`、`illustration-prompt-rules.md`、`video-assets-rules.md`，把正文、封面、配图、视频素材规则拆开维护。
- Assets: 内置默认视频设计模板、封面参考图、正文配图参考图，避免继续依赖外部绝对路径。
- Docs: 更新 `examples/prompt-examples.md` 与 `agents/openai.yaml`，让示例和元数据对齐新的内容生产流程定位。
- Docs: 调整图文写法规则，强化短判断、短段落、少解释、少配图的输出倾向，并补充配图提示词默认口径。

## 2026/04/09

- Docs: 明确 `纯正文.md` 默认用于直接复制发布，不混入 Markdown 标记符号、代码块、引用块、无序列表标记与强调语法。
- Docs: 在 `README.md`、`SKILL.md` 与 `references/style-rules.md` 中同步补充纯正文输出约束，统一 Skill 使用说明与风格规则。
