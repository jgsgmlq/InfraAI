# 需求清单

## 一、现有功能（已完成）

| ID | 功能 | 状态 | 说明 |
|----|------|------|------|
| F-001 | 工具注册机制 | ✅ 完成 | `registry/tools.yaml` |
| F-002 | 命令面板工具 | ✅ 完成 | `scripts/list_tools.py` |
| F-003 | CLI 规范文档 | ✅ 完成 | `docs/10_tooling_conventions.md` |
| F-004 | 技能系统框架 | ✅ 完成 | `.agent/skills/` |
| F-005 | 烟雾测试机制 | ✅ 完成 | `scripts/smoke/` |
| F-006 | 任务规范模板 | ✅ 完成 | `docs/20_task_spec_template.md` |

---

## 二、新增需求

### P0 - 立即需要（基础设施）

| ID | 功能 | 说明 | 交付物 |
|----|------|------|--------|
| R-001 | CLAUDE.md 项目上下文 | Claude Code 自动加载的项目说明文件，让 AI 理解项目背景和规则 | `CLAUDE.md` |
| R-002 | 自检工具 | 检查工具注册完整性、文档一致性、测试覆盖 | `scripts/audit_registry.py` |
| R-003 | 工具版本控制 | registry 中增加 version 字段，追踪工具变化 | 更新 `registry/tools.yaml` 结构 |

### P1 - 核心功能（提升 AI 效率）

| ID | 功能 | 说明 | 交付物 |
|----|------|------|--------|
| R-004 | 工具依赖声明 | 声明工具间的前置依赖关系 | 更新 registry schema |
| R-005 | 示例工具模板 | 带详细注释的参考实现，AI 学习用 | `scripts/_example_tool.py` |
| R-006 | 自然语言别名 | 支持中英文别名调用工具 | 更新 registry schema |
| R-007 | 错误恢复策略 | 在 skill/工具文档中定义失败后的处理方式 | 更新 skill 模板 |

### P2 - 增强功能（Vibe Coding 友好）

| ID | 功能 | 说明 | 交付物 |
|----|------|------|--------|
| R-008 | 意图触发短语 | 定义哪些用户表达应触发哪个 skill | 更新 skill 模板 |
| R-009 | 渐进式确认机制 | 关键步骤前 AI 应确认，避免方向错误 | 更新 skill 模板 |
| R-010 | 容错解析规则 | 定义模糊请求的处理方式 | 新增 `docs/30_ambiguity_resolution.md` |

### P3 - 架构优化（可移植性）

| ID | 功能 | 说明 | 交付物 |
|----|------|------|--------|
| R-011 | 目录结构重组 | 分层设计：core / skills / project | 目录重构 |
| R-012 | 核心/扩展分离 | 明确哪些可移植，哪些项目特定 | 更新文档 |
| R-013 | 项目初始化工具 | 自动化新项目的框架部署 | `scripts/init_project.py` |
| R-014 | 框架打包机制 | 一键导出可移植的框架包 | `scripts/export_framework.py` |

### P4 - SDK 架构（已完成）

| ID | 功能 | 状态 | 说明 | 交付物 |
|----|------|------|------|--------|
| R-015 | SDK 包架构 | ✅ 完成 | 自包含的功能包：API + CLI + Skills + Tests | `sdks/infra-core/` |
| R-016 | SDK 规范文档 | ✅ 完成 | 定义 SDK 包结构和命名规范 | `docs/60_sdk_specification.md` |
| R-017 | Skills 分层设计 | ✅ 完成 | 入口层（.claude/skills/）+ 实现层（SDK 内部） | `docs/50_skills_system.md` |
| R-018 | SDK 审查工具 | ✅ 完成 | 检查 SDK 包完整性和规范性 | `sdks/infra-core/api/audit.py` |
| R-019 | SDK CLI 工具 | ✅ 完成 | audit-sdk, audit-docs, audit-skills 命令 | `sdks/infra-core/cli/main.py` |
| R-020 | Registry API | ✅ 完成 | 加载和验证工具注册表 | `sdks/infra-core/api/registry.py` |
| R-021 | SDK 单元测试 | ✅ 完成 | registry 和 audit 模块的完整测试 | `sdks/infra-core/tests/` |
| R-022 | pyproject.toml | ✅ 完成 | 使 SDK 可通过 pip 安装 | `sdks/infra-core/pyproject.toml` |

---

## 三、非功能性需求

| ID | 类型 | 要求 |
|----|------|------|
| NF-001 | AI 可读性 | 所有文档必须结构化，使用明确的指令词（MUST/FORBIDDEN） |
| NF-002 | 自描述性 | AI 仅通过阅读文档即可理解如何使用框架 |
| NF-003 | 最小依赖 | Python 标准库 + PyYAML，无重型依赖 |
| NF-004 | 跨平台 | 支持 Windows / macOS / Linux |
| NF-005 | 幂等性 | 工具可重复执行，结果一致 |
