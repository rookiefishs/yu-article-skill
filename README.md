# yu-article-skill

一个从现有内容体系里提炼出来的个人写作 Skill。

它不是通用文案模板，也不是单纯的语气模仿工具。  
它更像一套可执行的写作规则：把标题习惯、结构习惯、禁用句式、目录格式、文件格式、发布文案口径，全部沉淀成可复用的 Skill。

这个 Skill 主要服务这类内容：
- `Claude Code`
- `OpenCode`
- `vibe coding`
- AI 编程协作流程
- 短视频图文选题
- 内容策划目录下的一整套稿件产出

## 这个项目解决什么问题

很多“个人风格写作”最后都会变成两种情况：
- 只有语气像，但结构和节奏不像
- 偶尔像，连续写几篇就开始漂

`yu-article-skill` 想解决的，就是把“像不像我现在这套写法”这件事，从感觉变成规则。

它会约束这些东西：
- 标题怎么起
- 开头怎么进
- 正文怎么推进
- 哪些句式不要再出现
- README、长文、纯正文、发布文案、封面提示词怎么分开写
- 目录名和文件名怎么统一

## 核心特点

- 先结论，后原因，再落场景和动作
- 口语化、短句、接地气
- 少空概念，多真实场景、真实动作、真实后果
- 默认产出完整内容目录，不只是一段正文
- 明确禁用一些模板味很重的句式
- 把前 20 篇文章沉淀成题型模板，而不是只抓语气
- 补了一套抖音 / 小红书发布安全边界，写完还能顺手过一遍平台风险

## 明确约束

Skill 内已经写入这些硬规则：
- 不要写：`为什么值得xxx`
- 不要写：`有价值的地方是xxx`
- 不要写：`不是xxx，而是xxx`
- 不要写：`很多人以为xxx，其实xxx`
- 不要写：`我现在越来越觉得xxx`
- 不要写：`我这两天xxxx的时候，第一反应xx：xxxx`
- 不要写：`xx真的xx`
- 不要写：`这个项目真正值钱的地方`

另外，这个 Skill 也把 `真的、太、非常、特别` 这类高频强化词纳入了“谨慎使用”范围。
它们不是完全不能用，但不能靠重复抬语气来撑内容。

## 项目结构

```text
yu-article-skill/
├─ README.md
├─ LICENSE
├─ SKILL.md
├─ .gitignore
├─ agents/
│  └─ openai.yaml
├─ references/
│  ├─ account-context.md
│  ├─ article-archetypes.md
│  ├─ style-rules.md
│  └─ platform-safety.md
└─ examples/
   └─ prompt-examples.md
```

## 各文件作用

- `SKILL.md`：Skill 主体，定义触发条件、写作规则、目录规则、文件规则
- `references/account-context.md`：账号定位、人设、目标用户、内容支柱
- `references/style-rules.md`：写作硬规则、禁用表达、自检清单
- `references/article-archetypes.md`：从前 20 篇文章提炼出的题型模板
- `references/platform-safety.md`：抖音 / 小红书高风险内容边界，发布前自检用
- `agents/openai.yaml`：Skill 的界面元数据
- `examples/prompt-examples.md`：实际调用这个 Skill 时可直接复用的提示词示例

另外，`纯正文.md` 默认按“可直接复制发布”处理，不混入 Markdown 标记符号，避免复制到平台后台后还要手动清理。

## 适合怎么用

### 1. 写一整套内容目录

```text
用 yu-article-skill，写一个新选题目录。
标题是：XXX
需要 README、长文、纯正文、发布文案、封面提示词。
```

### 2. 改写现有稿子

```text
用 yu-article-skill，把这篇稿子改得更像我现在的写法。
重点清掉模板味重的反转句，保留信息密度。
```

### 3. 只做标题和结构整理

```text
用 yu-article-skill，给这个选题出 5 个更贴近当前内容风格的标题，
再给一版目录结构。
```

## 安装方式

如果想让 Codex 或本地环境直接发现这个 Skill，可以把整个目录放到：

```text
~/.codex/skills/yu-article-skill
```

或者复制其中的 `SKILL.md + references + agents` 到你自己的 Skill 目录。

## 开源协议

本项目使用 MIT License。

## 项目定位一句话

`yu-article-skill` 是一个把“个人写作风格 + 内容目录结构 + 文件产出规则”一起沉淀下来的写作 Skill。
