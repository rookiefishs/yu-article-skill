# yu-article-skill

这是 `yu-article-skill` 的工作区目录。

这里现在分成两层：
- 根目录：放工作区级文档
- `skill/`：放真正给 Claude 使用的 skill 核心内容

## 当前结构

```text
yu-article-skill/
├─ .git/
├─ .gitignore
├─ README.md
├─ CHANGELOG.md
├─ LICENSE
└─ skill/
   ├─ SKILL.md
   ├─ agents/
   ├─ assets/
   ├─ examples/
   └─ references/
```

## 各部分作用

### 根目录
- `README.md`：工作区说明
- `CHANGELOG.md`：工作区级变更记录
- `LICENSE`：许可证
- `.git/`：仓库元数据

### skill/
这是 skill 的真正核心目录，只放 Claude 执行时需要的内容：
- `SKILL.md`：skill 主入口与规则总览
- `agents/`：界面元数据
- `assets/`：默认模板、封面参考图、配图参考图
- `examples/`：调用示例
- `references/`：长文、图文、视频、封面、配图、素材等细则

## 现在这个 skill 解决什么问题

这个 skill 用来做内容生产，不再是旧版本那种默认补齐一整套 README / 长文 / 纯正文 / 发布文案 的写作模板。

它当前主要服务三种输出形式：
- 长文
- 图文
- 视频

## 工作方式

真实规则和执行逻辑，以：
- `skill/SKILL.md`
- `skill/references/*`

为准。

**真正用于后续打包、复用、迁移的 skill 根目录是 `skill/`，不是当前仓库根目录。**

如果后面继续调整规则，优先改 skill 目录里的内容，不要把详细规则再写回根目录 README，避免双份说明打架。

## 一句话说明

根目录是工作区说明，`skill/` 才是实际 skill 本体。
