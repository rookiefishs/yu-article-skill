# Changelog

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
