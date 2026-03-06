# AI-Native Infrastructure Framework

> 本文件是 Claude Code 的项目上下文，会自动加载到 AI 对话中。

**最高指令**：`.claude/PRIME_DIRECTIVE.md` - 定义项目核心定位和设计原则

## 项目定位

这是一个 **AI 工作环境框架**：
- **用户**：使用自然语言下达命令，无需了解技术细节
- **AI**：根据 Skills 指导进行编程，调用 SDK 工具辅助执行
- **工具**：提供稳定、可预测的辅助能力

**核心理念**：用户说人话 → AI 按 Skills 编程 → 工具辅助执行

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
│   ├── PRIME_DIRECTIVE.md # 最高指令 - 项目核心定位
│   ├── commands/          # Claude Code 自定义命令
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
│   ├── 60_sdk_specification.md  # SDK 规范
│   ├── TROUBLESHOOTING.md       # 故障排查
│   └── plans/             # 实施计划
│
├── core/                  # 框架核心（可移植模板）
│   ├── docs/              # 规范文档 (00-50)
│   ├── .agent/skills/     # 核心 skills
│   └── ...
│
├── scripts/               # 独立工具脚本（兼容旧架构）
├── registry/              # 工具注册表（兼容旧架构）
│
├── [项目层 - 用户工作区]
├── my-web-app/            # 用户项目示例 1
│   ├── src/
│   └── ...
├── data-analysis/         # 用户项目示例 2
│   ├── notebooks/
│   └── ...
└── <project-name>/        # 其他用户项目
    └── ...
```

**架构说明**：
- **框架层**：`sdks/`、`scripts/`、`.claude/`、`docs/`、`core/`、`registry/` - 稳定的工具库，不随意修改
- **项目层**：根目录下的项目子目录（如 `my-app/`）- 用户工作区，灵活开发
- Skills 入口层：`.claude/skills/` - Claude Code 自动识别
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

### SDK 稳定性原则（CRITICAL）

**D:\infra_demo\ 是一个可移植的 IDE 平台，包含框架层和项目层。**

#### 架构定位

- **框架层**（稳定，不随意修改）：`sdks/`、`scripts/`、`.claude/`、`docs/`、`core/`、`registry/`
- **项目层**（用户工作区）：在根目录下创建的项目子目录（如 `my-app/`、`data-analysis/`）

**架构类比**：
- SDK 框架 = npm 包库（提供可复用的工具）
- 用户项目 = 使用 npm 包的应用（调用工具，不修改工具源码）

#### 工作模式识别

AI 有两种工作模式：

1. **项目开发模式（默认）**：
   - 在 `D:\infra_demo\<project-name>\` 子目录中工作
   - 调用 SDK 的 API 和 CLI 工具
   - 不修改框架层文件
   - 新功能先在项目中实现和验证

2. **SDK 开发模式（受限触发）**：
   - 只有在以下**任一条件**满足时才进入：
     - 当前工作目录是 `D:\infra_demo\` 且用户命令涉及修改框架层
     - 用户明确下达命令（包含"修改 SDK"、"扩展 SDK"、"创建 SDK 工具"、"更新 SDK"、"SDK 开发"、"编写 SDK"、"修改框架工具"、"扩展框架"等关键词）
     - 用户的命令意图明确表示要修改框架层文件（`sdks/`、`scripts/`、`.claude/`、`docs/`、`core/`、`registry/`）

#### SDK 稳定性 HARD GATES

**MUST（必须遵守）**：
- 默认项目开发模式，除非明确触发 SDK 开发模式
- 用户项目必须在独立子目录中，不得与框架目录冲突（不能命名为 `sdks`、`scripts`、`docs`、`.claude`、`core`、`registry` 等）
- 新功能优先在项目中实现，成熟后再询问用户是否迁移到 SDK
- 不确定当前模式时，必须先询问用户
- 创建项目时，必须先询问项目名称，然后在 `D:\infra_demo\<project-name>\` 下创建项目目录

**FORBIDDEN（禁止行为）**：
- 禁止在项目开发模式下修改框架层文件（`sdks/`、`scripts/`、`.claude/`、`docs/`、`core/`、`registry/`）
- 禁止在没有明确触发条件的情况下进入 SDK 开发模式
- 禁止在根目录 `D:\infra_demo\` 直接创建项目文件（如 `index.js`、`main.py`、`app.py` 等）
- 禁止擅自将项目代码迁移到 SDK（必须先询问用户）

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

### 1. 判断工作模式

- **默认**：项目开发模式
- **检查**：是否满足 SDK 开发模式的触发条件（满足**任一条件**即可）？
  - 当前工作目录是项目根目录且命令涉及修改框架层（`sdks/`、`scripts/`、`.claude/`、`docs/`、`core/`、`registry/`）？
  - 用户明确下达修改 SDK 的命令（包含"修改 SDK"、"扩展 SDK"等关键词）？
  - 用户的命令意图明确表示要修改框架层文件？
- **不确定时**：询问用户

### 2. 项目开发模式流程

```
1. 确认项目目录 → 是否已有项目目录？
   ↓ 没有
2. 询问项目名称 → 用户提供项目名称（如 my-web-app）
   ↓
3. 创建项目目录 → mkdir <project-name>
   ↓
4. 切换到项目目录 → cd <project-name>
   ↓
5. 查看现有 SDK → python scripts/list_tools.py
   ↓
6. 有现成能力？ → 调用 SDK API 或 CLI
   ↓ 没有
7. 在项目中实现功能
   ↓
8. 功能成熟后，询问是否迁移到 SDK
```

### 3. SDK 开发模式流程

```
1. 确认用户意图 → 确实要修改 SDK？
   ↓ 是
2. 查看现有 SDK → ls sdks/
   ↓
3. 按规范创建/扩展 SDK：
   - [ ] sdks/<sdk>/api/<module>.py
   - [ ] sdks/<sdk>/tests/test_<module>.py
   - [ ] sdks/<sdk>/skills/<skill>.md
   - [ ] .claude/skills/<sdk>-<skill>.md
   - [ ] 更新 manifest.yaml
   ↓
4. 运行 audit-sdk 验证
   ↓
5. 完成
```

---

## AI 行为约束

### 判断工作模式时

- 默认处于项目开发模式
- 检查是否满足 SDK 开发模式的触发条件
- 不确定时，必须先询问用户
- 不要擅自进入 SDK 开发模式

### 创建项目前

- 询问项目名称和用途
- 确认项目名称不与框架目录冲突
- 在项目根目录下创建项目子目录
- 不要在根目录直接创建项目文件

### 创建项目时

- 先切换到项目目录
- 查看现有 SDK 能力（运行 `python scripts/list_tools.py`）
- 优先使用 SDK 工具，而不是重新实现

### 创建项目后

- 如果实现了通用功能，询问用户是否迁移到 SDK
- 不要擅自修改框架层文件
- 不要擅自将项目代码迁移到 SDK

### 创建 SDK 前

- 先检查是否已有类似 SDK 或能力
- 与用户确认 SDK 名称、API 设计
- 不要一口气写完再问，要分步确认

### 创建 SDK 时

- 遵循 `docs/60_sdk_specification.md` 规范
- 遵循 `core/docs/50_skills_system.md` 的 Skills 分层设计
- 错误信息要清晰、可操作

### 创建 SDK 后

- 立即运行 `audit-sdk` 验证
- 创建对应的入口 skills
- 补充 README 和 CHANGELOG

---

## 文档索引

| 文档 | 用途 | 何时阅读 |
|------|------|----------|
| `core/docs/00_operating_manual.md` | 操作原则 | 理解项目核心理念 |
| `core/docs/10_tooling_conventions.md` | CLI 规范 | 创建新工具前 |
| `core/docs/11_error_handling.md` | 错误处理 | 工具执行失败时 |
| `core/docs/50_skills_system.md` | Skills 系统 | 编写或导入 skills 时 |
| `docs/60_sdk_specification.md` | SDK 规范 | 创建新 SDK 时 |
| `docs/TROUBLESHOOTING.md` | 故障排查 | 遇到问题时 |
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
