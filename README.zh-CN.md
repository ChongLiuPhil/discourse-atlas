# Discourse Atlas

[English](README.md) | [中文](README.zh-CN.md)

[![CI](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/ci.yml/badge.svg)](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/ci.yml)
[![Pages](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/pages.yml/badge.svg)](https://github.com/ChongLiuPhil/discourse-atlas/actions/workflows/pages.yml)

**Discourse Atlas** 是一个开源协议与工具集，用于重建复杂文本的层级论证结构——从整部作品的总体架构一直分析到局部论证。

它面向哲学、随笔、学术论文、理论著作、法律推理、政策报告以及其他复杂文本。在这些文本中，理解**哪些部分支持、要求、细化、挑战或回应哪些其他部分**，与理解各部分分别说了什么同样重要。

> 状态：**v1.0.0 hosted research release。** 主要分析入口无需安装：只需把一个公开的 Discourse Atlas 协议 URL 和源文档交给 AI Agent。随后即可在托管的 Interactive Atlas 中检查和修正规范 JSON。仓库还包含正式 Agent Skill、规范 JSON schema、验证／评估 CLI、确定性的 PDF 文本摄取、交互式阅读器与对齐工作台。

托管版 Interactive Atlas：

<https://chongliuphil.github.io/discourse-atlas/>

## 零安装：把这个 URL 交给 AI Agent

如果你的 AI Agent 能读取公开 URL，也能访问源文档，**就不需要安装 Discourse Atlas**。

把下面的协议交给 Agent：

```text
https://raw.githubusercontent.com/ChongLiuPhil/discourse-atlas/main/AGENT.md
```

然后使用类似下面的提示词：

```text
读取并遵循 Discourse Atlas 协议：
https://raw.githubusercontent.com/ChongLiuPhil/discourse-atlas/main/AGENT.md

分析这个来源：
<SOURCE URL OR ATTACHED DOCUMENT>

先生成一个可读的整部作品论证图。识别每个主要部分／章节的核心主张与论证功能，
然后只在有用时递归展开到小节与局部论证层级。保留作者原有标题，标记推断出的结构，
用证据支撑主要关系，并在可能时返回规范的 Discourse Atlas JSON。
```

远程协议被有意设计为自包含。它告诉 Agent 如何恢复层级结构、区分主张与摘要、推断关系方向、保留不确定性、附加证据，以及如何从宏观到微观地呈现结构图。

远程 URL **不等于**已经安装的 Agent Skill。符合标准的 Skill 仍位于 `skills/discourse-structure/`；`AGENT.md` 是给具备网页读取能力的 Agent 使用的便携式指令入口。详见 `docs/zero-install-agent.md`。

## 最终结构图表示什么

Discourse Atlas 区分两种结构：

1. **包含层级（Containment hierarchy）** — 作品 → 部分 → 章节 → 小节 → 子小节 → 段落／论证单元。
2. **话语依赖图（Discourse dependency graph）** — `requires`、`supports`、`derives`、`refines`、`contrasts`、`objects_to`、`responds_to` 等关系。

一个节点可以区分：

- `title` — 文本单元叫什么；
- `main_claim` — 如果该单元推进一个命题，它所推进的命题；
- `summary` — 该单元讨论了什么或做了什么；
- `function` — 它的话语功能；
- `role_in_parent` — 为什么它在上一层结构中是必要的。

`main_claim` 被刻意设计为可选字段：定义、问题陈述、例子或综述不应被强行压成虚假的论题。

默认可视化策略采用渐进展开：

```text
Work Map -> Part / Chapter Map -> Section Map -> Local Argument Map
```

因此，一部长篇著作应先呈现可读的总体问题、核心论题、主要章节、章节级主张以及最重要的相互关系，而不是一开始就展示数百个句子级节点。

## 设计原则

- **结构先于摘要。** 先恢复架构，再写全局结论。
- **宏观先于微观。** 在展开局部论证之前，先让整部作品的构成变得可理解。
- **保留作者结构。** 已存在的章节／小节优先于推断分段。
- **明确标记推断结构。** AI 生成的小节绝不能伪装成作者原有标题。
- **区分层级与依赖。** 包含关系不等于逻辑支持。
- **区分主张、摘要与功能。** 它们回答不同的分析问题。
- **重要边必须有证据。** 主要推断关系应能回指源文本。
- **比较之前先对齐。** 不同分段方案必须先进行对齐，才能比较结构差异。
- **显式处理来源准备。** PDF 提取、OCR、清理与解释不能被悄然混为一谈。
- **重建，而不是揭示唯一真相。** 输出是一种可批评的解释，不宣称存在唯一真实结构。

## 仓库布局

```text
discourse-atlas/
├── AGENT.md                       # 零安装远程 Agent 协议
├── skills/discourse-structure/    # 便携、符合标准的 Agent Skill
├── schemas/                       # 图结构 + 单元对齐 schema
├── src/discourse_atlas/           # 验证、PDF 摄取、对齐、评估 CLI
├── apps/web/                      # 交互阅读器 + 对齐工作台
├── examples/mini-essay/           # 小型端到端示例
├── benchmark/                     # 合成 + 公共领域评估案例
├── tests/                         # schema、摄取、锚点、对齐、评估测试
├── docs/                          # 协议、架构、摄取、评估、托管 Atlas 文档
└── .github/workflows/             # CI + GitHub Pages 部署
```

## 正式 Agent Skill

对于支持 Agent Skills `SKILL.md` 格式的客户端，把 `skills/discourse-structure/` 载入或复制到客户端的 Skill 目录即可。该 Skill 与模型、供应商无关，遵循与 `AGENT.md` 相同的方法，并按需加载额外参考资料。

Skill 现在会从 `main_claim`、`summary`、`function`、`role_in_parent`、来源证据和置信度等维度分析每一个有用单元，并明确要求先建立整部作品层面的结构图，再向下钻取。

## 规范表示

规范表示使用 JSON。可视化只是派生视图，不是权威来源。

规范 schema：

```text
https://raw.githubusercontent.com/ChongLiuPhil/discourse-atlas/main/schemas/discourse-graph.schema.json
```

可选的 `main_claim` 字段向后兼容；图 schema 仍保持在 `0.1.0`，因此已有 v0.1–v0.9 分析文件仍然有效。

## 交互阅读器

无需安装即可使用托管版 Interactive Atlas：

<https://chongliuphil.github.io/discourse-atlas/>

`apps/web/` 中的 Web 应用会把规范图结构转换为同步阅读环境，使用嵌套 React Flow 节点与 ELK 布局。

它支持：

- 可嵌套／折叠的 作品 → 章节 → 小节 结构；
- 跨层级逻辑箭头；
- 以主张为首要信息的节点卡，并兼容旧版摘要回退；
- 区分作者结构与 AI 推断结构的来源标记；
- 源文本 ↔ 图结构证据追踪；
- 段落／行／页／Unicode 字符锚点；
- 节点／边检查与人工修正；
- 导出修正后的 JSON；
- 用于审阅一对一与拆分／合并对应关系的 Alignment 工作区。

```bash
cd apps/web
npm install
npm run dev
```

生产部署与版本验证见 `docs/hosted-atlas.md`。

## 可选安装与 CLI

零安装 Agent 工作流**不需要**安装 Python 包。只有在需要本地验证、导出、评估、对齐或确定性 PDF 文本层摄取时才需要安装。

核心安装：

```bash
python -m pip install .
```

可选 PDF 依赖：

```bash
python -m pip install '.[pdf]'
```

开发安装：

```bash
python -m pip install -e '.[dev]'
```

命令：

```bash
discourse-atlas validate examples/mini-essay/analysis.json
discourse-atlas mermaid examples/mini-essay/analysis.json
discourse-atlas dot examples/mini-essay/analysis.json

discourse-atlas ingest-pdf book.pdf

discourse-atlas align reference.json candidate.json -o alignment.json
discourse-atlas evaluate reference.json candidate.json --alignment alignment.json
discourse-atlas multi-evaluate candidate.json ref-a.json ref-b.json --auto-align
discourse-atlas agreement ref-a.json ref-b.json --alignment alignment.json
```

## 关系本体

| 关系 | 含义 |
|---|---|
| `requires` | source 是理解或建立 target 的前提 |
| `supports` | source 为 target 提供理由／证据 |
| `derives` | target 从 source 发展或推导出来 |
| `refines` | source 使 target 更精确、受限定、更受约束或更清楚地表达 |
| `contrasts` | source 与 target 被有意对照（语义上对称） |
| `objects_to` | source 对 target 提出反对 |
| `responds_to` | source 回应 target 中的问题或反对意见 |
| `illustrates` | source 举例说明或应用 target |
| `sequence` | 仅表示文本／组织顺序，不表示逻辑依赖 |

详见 `skills/discourse-structure/references/relation-ontology.md`。

## PDF 文本摄取与学术锚点

`discourse-atlas ingest-pdf book.pdf` 会生成：

- `book.txt` — 使用 `\n\f\n` 分隔页面的规范化 Unicode 文本；
- `book.pages.json` — PDF 的 SHA-256、页数、空白页数以及每页准确的 Unicode code-point 范围。

该命令只读取 PDF 文本层。它不会静默执行 OCR、修复版式、去除断词或对来源进行语义清理。

来源锚点可使用：

- 段落范围：1 起始、包含端点；
- 行范围：1 起始、包含端点；
- 页范围：1 起始、包含端点；
- `char_start`：0 起始、包含的 Unicode code-point 偏移；
- `char_end`：0 起始、不包含的 Unicode code-point 偏移。

详见 `docs/pdf-ingestion.md` 与 `docs/scholarly-anchors.md`。

## 评估与解释多元性

Discourse Atlas 不假设解释性文本总有唯一正确的分段。评估层支持在结构评分之前明确建立一对一、拆分、合并与多对多的单元对齐；多参考评估也可以保留多个合理的重建方案。

benchmark 包含跨体裁的合成案例，以及一个公共领域的 John Stuart Mill《论自由》案例；后者提供两个被接受的重建版本与一个经过审阅的拆分／合并对齐。

详见 `benchmark/README.md`、`docs/alignment.md`、`docs/alignment-workbench.md` 与 `docs/evaluation.md`。

## 已完成里程碑

- **v0.1** — 规范优先的 Skill、schema、关系本体、验证器、Mermaid/DOT 导出。
- **v0.2** — React Flow + ELK 嵌套交互图。
- **v0.3** — 同步源文本阅读与人工修正。
- **v0.4** — benchmark 与结构／证据评估。
- **v0.5** — 显式对齐、多参考评估、公共领域 Mill 案例。
- **v0.6** — 浏览器对齐裁决工作台。
- **v0.7** — 学术页码与 Unicode 字符锚点。
- **v0.8** — 确定性 PDF 文本层摄取与来源清单。
- **v0.9** — 零安装远程 Agent 协议、支持主张字段的 schema/Skill，以及以主张为中心的宏观到微观查看器。
- **v1.0** — 部署到 GitHub Pages 的 Hosted Interactive Atlas，包含对子路径安全的生产资源与自动部署。

## v1.0 之后的研究方向

v1.0 研究核心已经支持零安装 AI 使用、托管浏览器 Atlas 与本地研究工具。后续工作属于扩展／研究，而不是基础使用所必需的配置：

- 更多经过审阅、属于公共领域或获得许可的长篇哲学语料；
- 仅作为明确、保留来源信息的适配器加入 OCR；
- 把校准后的语义对齐提案作为可选、可独立审计的层；
- 可深链接的 Agent → Viewer 交接格式，使生成后的结构图能够直接在托管 Atlas 中打开。

## 非目标

Discourse Atlas 不旨在取代细读，不宣称解释性文本只有唯一正确结构，不把所有关系压扁为前提／结论对，不默认把文本顺序当作逻辑依赖，也不会静默地把文本提取／OCR 当作解释中立过程。

## 贡献

见 [CONTRIBUTING.md](CONTRIBUTING.md)。版本历史记录在 [CHANGELOG.md](CHANGELOG.md)。

## 许可证

MIT。见 [LICENSE](LICENSE)。
