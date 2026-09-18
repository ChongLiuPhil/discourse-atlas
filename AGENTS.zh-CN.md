# AGENTS.md — Discourse Atlas 仓库协作契约

[English](AGENTS.md) | [中文](AGENTS.zh-CN.md)

本文件约束**维护 Discourse Atlas 仓库**的人类贡献者与 AI Agent；它不取代给最终用户使用的 `AGENT.md` 文本重建协议。

## 仓库作为权威状态

GitHub 仓库是项目状态的权威来源。聊天历史、账号记忆、隐藏 scratchpad、本地摘要以及旧 Agent 报告都不是 canonical state。高影响修改或写入前，应重新读取最新目标文件、`PROJECT_MANIFEST.yaml` 与 `PROJECT_STATUS.md`。

## 产品协议与仓库契约分离

- `AGENT.md`：告诉 Agent **如何使用** Discourse Atlas。
- `skills/discourse-structure/SKILL.md`：同一重建方法的模块化 Skill。
- `AGENTS.md`：告诉协作者**如何维护**仓库。

## Canonical authority

| 问题 | Canonical authority |
|---|---|
| graph JSON 结构 | versioned graph schema |
| alignment JSON 结构 | versioned alignment schema |
| relation 含义/方向 | `skills/discourse-structure/references/relation-ontology.md` |
| 来源坐标语义 | `skills/discourse-structure/references/source-anchors.md` |
| 分段方法 | `skills/discourse-structure/references/segmentation-rules.md` |
| 重建流程 | `AGENT.md` + Skill，保持语义同步 |
| 实现行为 | tests + source code |
| 架构理由 | `docs/architecture.md` + Decision Records |
| release/version 规则 | `docs/versioning.md` |
| 当前项目状态 | `PROJECT_STATUS.md` |
| 公开介绍 | README；属于解释层而非规范层 |

README 不得静默重新定义 schema 或 ontology。

## 变更传播

语义变更应同步 canonical reference、`AGENT.md`、Skill、tests/examples，以及受影响的 schema/evaluation logic。不得无记录地扩张 relation 含义。

当可接受文档集合发生变化时，Schema 必须产生新的 immutable versioned schema，并同步 latest alias、packaged resources、fixtures、兼容性测试与 migration/version 文档。不得重复使用同一个 schema version 表示不同契约。

Web/CLI 行为变化要同步测试和用户文档。Benchmark 必须保留 provenance，不得为了提高指标而改写参考解释。

## 多版本域

Toolkit/release、remote Agent protocol、graph schema、alignment schema 是独立版本域。以 `docs/versioning.md` 为准。

## 双语治理

技术治理以英文为 canonical。README、START_HERE、AGENTS 是同步双语入口。代码、schema、数据以及多数技术文档保持单份即可。

## Pull Request

PR 应保持聚焦，并说明 change class、rationale、canonical source、schema/ontology impact、compatibility/version impact、必要时的 security/privacy impact，以及已完成的验证。

## AI 提议

AI Agent 可以提出架构与语义方案，但只有通过仓库修改与正常审查，提议才成为持久项目决定。长期架构选择在适当时应创建 Decision Record。

本治理层借鉴 HARC 的 repository-backed continuity 原则，但不复制 HARC 的完整研究记忆架构。
