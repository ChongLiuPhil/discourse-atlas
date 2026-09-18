# START HERE — Discourse Atlas 仓库接管入口

[English](START_HERE.md) | [中文](START_HERE.zh-CN.md)

本文件面向**维护 Discourse Atlas 仓库**的人类贡献者与零上下文 AI Agent。

> `AGENT.md` 是给最终用户/分析 Agent 使用的 Discourse Atlas 文本分析协议。  
> `AGENTS.md` 是维护 Discourse Atlas 仓库时使用的协作契约。  
> 两者职责不同，不应混淆。

## 强制读取顺序

在进行实质性仓库修改之前，先读取：

1. `PROJECT_MANIFEST.yaml`
2. `PROJECT_CONTEXT_INTERFACE.yaml`
3. `PROJECT_STATUS.md`
4. `AGENTS.md`
5. `ROADMAP.md`
6. 先给任务分类，再按 route 选择性读取 `required_refs`
7. 与当前请求相关的 canonical 文件
8. 涉及 schema、protocol 或 release 时读取 `docs/versioning.md` 与 `docs/compatibility.md`
9. `docs/decisions/` 中相关的 Decision Record

仓库是权威项目状态。聊天记录、模型记忆和旧摘要都只是临时上下文。

## 先给变更分类

一个请求可以属于多个类别：**SEMANTICS**、**SCHEMA**、**IMPLEMENTATION**、**WEB**、**BENCHMARK**、**DOCS**、**RELEASE**、**GOVERNANCE**。

`PROJECT_CONTEXT_INTERFACE.yaml` 定义每个 route 必须/可选读取的仓库引用。只读取当前任务真正需要的内容，不把整个仓库复制进会话上下文。

写入前必须重新读取目标文件最新版本。仓库写入后，先前缓存的受影响文件摘录立即视为 stale。语义或 schema 变更还必须读取对应 ontology/schema 与 Decision Record。

## 完成标准

只有 canonical source、依赖实现/文档/示例、兼容性/版本声明以及测试都完成同步，变更才算完成。

仓库技术治理以英文为 canonical。中文 README、START_HERE 与 AGENTS 是同步的 onboarding mirror。
