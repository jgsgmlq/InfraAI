# AI-Native Infrastructure Framework

> 本文件是 Claude Code 的项目上下文，会自动加载到 AI 对话中。

## 项目概述

这是一个**可移植的 AI 工作环境框架**，用于将资深工程师的规范、工具和工作流封装起来，让 AI 能以高质量、低成本的方式工作。

**核心理念**：工具驱动 → AI 可读 → 自我维护 → 可移植

**架构**：SDK 包架构 + Skills 分层设计

---

## 目录结构

```
infra_demo/
├── CLAUDE.md              # 本文件 - AI 项目上下文
├── BOOTSTRAP.md           # 新项目初始化指南
├── README.md              # 人类可读的项目说明
├── requirements.txt       # Python 依赖
│
├── .claude/
│   └── skills/            # Skills 入口（Claude Code 自动识别）
│       └── <sdk>-<skill>.md
│
├── sdks/                  # SDK 包目录
│   └── infra-core/        # 框架核心 SDK
│       ├── __init__.py
│       ├── version.py
│       ├── manifest.yaml
│       ├── api/           # Python API
│       ├── cli/           # CLI 入口
│       ├── skills/        # Skills 实现
│       └── tests/
│
├── docs/                  # 项目级文档
│   ├── 00_operating_manual.md
│   ├── 50_skills_system.md
│   ├── 60_sdk_specification.md
│   └── plans/             # 实施计划
│
├── scripts/               # 独立工具脚本（兼容旧架构）
└── registry/              # 工具注册表（兼容旧架构）
```

**架构说明**：
- `sdks/`: SDK 包，每个 SDK 自包含（API + CLI + skills + tests）
- `.claude/skills/`: Skills 入口层，Claude Code 自动识别
- `scripts/`, `registry/`: 保留用于后向兼容

---

## 关键规则（HARD RULES）

### MUST（必须遵守）

1. **SDK 规范**：新功能 MUST 以 SDK 包形式组织
2. **Skills 分层**：入口在 `.claude/skills/`，实现在 SDK 内
3. **测试覆盖**：每个 SDK MUST 有 `tests/` 目录
4. **CLI 规范**：所有工具 MUST 支持 `--help`，错误输出到 stderr
5. **退出码**：使用标准退出码 - 0(成功), 2(参数错误), 3(运行时错误)

### FORBIDDEN（禁止行为）

1. **禁止纯文档**：不允许只输出文档而不创建可执行工具
2. **禁止硬编码**：配置项不允许硬编码在脚本中
3. **禁止跳过测试**：不允许提交未经测试的工具
4. **禁止假设**：模糊需求必须先确认，不允许擅自假设

---

## 启动时

每次对话开始时，运行 `/init` 完成项目初始化。

## 常用命令

```bash
# SDK CLI（新架构）
python sdks/infra-core/cli/main.py audit-sdk sdks/infra-core
python sdks/infra-core/cli/main.py audit-docs docs
python sdks/infra-core/cli/main.py audit-skills .claude/skills

# 独立工具（兼容旧架构）
python scripts/list_tools.py           # 查看工具
python scripts/list_skills.py          # 查看技能
python scripts/audit_registry.py       # 健康检查
```

---

## 工作流程

当收到新需求时，按以下顺序执行：

```
1. 查看现有 SDK → ls sdks/
   ↓
2. 有现成能力？ → 调用 SDK API 或 CLI
   ↓ 没有
3. 确认需求细节（不假设）
   ↓
4. 按规范创建/扩展 SDK：
   - [ ] sdks/<sdk>/api/<module>.py
   - [ ] sdks/<sdk>/tests/test_<module>.py
   - [ ] sdks/<sdk>/skills/<skill>.md
   - [ ] .claude/skills/<sdk>-<skill>.md
   - [ ] 更新 manifest.yaml
   ↓
5. 运行 audit-sdk 验证
   ↓
6. 完成
```

---

## AI 行为约束

### 创建 SDK 前

- 先检查是否已有类似 SDK 或能力
- 与用户确认 SDK 名称、API 设计
- 不要一口气写完再问，要分步确认

### 创建 SDK 时

- 遵循 `docs/60_sdk_specification.md` 规范
- 遵循 `docs/50_skills_system.md` 的 Skills 分层设计
- 错误信息要清晰、可操作

### 创建 SDK 后

- 立即运行 `audit-sdk` 验证
- 创建对应的入口 skills
- 补充 README 和 CHANGELOG

---

## 文档索引

| 文档 | 用途 | 何时阅读 |
|------|------|----------|
| `docs/00_operating_manual.md` | 操作原则 | 理解项目核心理念 |
| `docs/10_tooling_conventions.md` | CLI 规范 | 创建新工具前 |
| `docs/11_error_handling.md` | 错误处理 | 工具执行失败时 |
| `docs/50_skills_system.md` | Skills 系统 | 编写或导入 skills 时 |
| `docs/60_sdk_specification.md` | SDK 规范 | 创建新 SDK 时 |
| `BOOTSTRAP.md` | 初始化指南 | 新项目启动时 |

---

## 快速参考

### 退出码

| 代码 | 含义 | 场景 |
|------|------|------|
| 0 | 成功 | 正常完成 |
| 2 | 参数错误 | --help, 无效参数 |
| 3 | 运行时错误 | 文件不存在, 网络错误 |

### 命名规范

| 类型 | 规则 | 示例 |
|------|------|------|
| SDK 目录名 | kebab-case | `infra-core` |
| Python 模块 | snake_case | `infra_core` |
| CLI 命令 | kebab-case | `audit-sdk` |
| Skill ID | kebab-case | `infra-core-audit-sdk` |
| 入口 Skill | `<sdk>-<skill>.md` | `infra-core-audit-sdk.md` |

---

## Skills 快速参考

### infra-core SDK 能力

| Skill | 触发短语 | 用途 |
|-------|----------|------|
| infra-core-audit-sdk | "检查 SDK", "audit SDK" | 审查 SDK 完整性 |
| infra-core-audit-docs | "检查文档", "audit docs" | 审查文档一致性 |
| infra-core-create-sdk | "创建 SDK", "create SDK" | 创建新 SDK 包 |

### Skills 存放位置

| 位置 | 用途 |
|------|------|
| `.claude/skills/` | 入口 skills（Claude Code 自动识别） |
| `sdks/<sdk>/skills/` | 实现 skills（完整逻辑） |

运行 `python scripts/list_skills.py --verbose` 查看完整列表。
