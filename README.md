# AI-Native Infrastructure Framework

> 一个可移植的 IDE 平台，为 AI 辅助开发提供稳定的工具库和灵活的项目工作区。

**[English](README.en.md) | 简体中文 | [日本語](README.ja.md)**

```
       ✩           ·  ★                    *          ☆     ★
   *        ★                    ✩                ·               *
  ╭──────────────────────────────────────────────────────────────────────╮
  │    ▄▄▄▄▄▄▄      ▄▄▄▄▄▄▄                                              │
  │   █       █    █       █   ██╗███╗   ██╗███████╗██████╗  █████╗ ██╗  │
  │   █   ▄▄▄▄█    █▄▄▄▄   █   ██║████╗  ██║██╔════╝██╔══██╗██╔══██╗██║  │
  │   █                    █   ██║██╔██╗ ██║█████╗  ██████╔╝███████║██║  │
  │   █   ██          ██   █   ██║██║╚██╗██║██╔══╝  ██╔══██╗██╔══██║██║  │
  │   █   ██    ▄▄    ██   █   ██║██║ ╚████║██║     ██║  ██║██║  ██║██║  │
  │   █        █  █        █   ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  │
  │    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀            AI-Native Infrastructure          │
  ╰──────────────────────────────────────────────────────────────────────╯
        ☆      *           ✩          ★      ·            ★       .
```

## 🎯 核心理念

**用户说人话 → AI 按 Skills 编程 → 工具辅助执行**

这是一个为 AI 辅助开发设计的工作环境框架：
- **用户**：使用自然语言下达命令，无需了解技术细节
- **AI**：根据 Skills 指导进行编程，调用 SDK 工具辅助执行
- **工具**：提供稳定、可预测的辅助能力

## 🏗️ 架构定位

这是一个**可移植的 IDE 平台**，包含两层：

### 📦 框架层（稳定，不随意修改）
- `sdks/` - SDK 工具包
- `scripts/` - 框架工具
- `.claude/` - Claude Code 配置
- `docs/` - 规范文档
- `core/` - 框架核心（可移植模板）
- `registry/` - 工具注册表

### 💼 项目层（用户工作区，灵活开发）
- 在根目录下创建项目子目录
- 例如：`my-web-app/`、`data-analysis/`
- 调用框架层的 SDK 工具
- 灵活实现业务逻辑

**架构类比**：
- SDK 框架 = npm 包库（提供可复用的工具）
- 用户项目 = 使用 npm 包的应用（调用工具，不修改工具源码）

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 初始化项目

在 Claude Code 中运行：

```
/init
```

或者手动运行：

```bash
python scripts/list_tools.py    # 查看可用工具
python scripts/list_skills.py   # 查看可用技能
python scripts/audit_all.py     # 健康检查
```

### 3. 创建你的第一个项目

直接用自然语言告诉 AI：

```
"帮我创建一个 Web 应用"
"创建一个数据分析项目"
"实现用户登录功能"
```

AI 会自动：
1. 询问项目名称
2. 在根目录下创建项目子目录
3. 在项目目录中搭建项目
4. 调用 SDK 工具辅助开发

## 🎯 工作模式

### 🟢 项目开发模式（默认）

AI 默认处于此模式，会在项目子目录中工作：

```
"创建一个新项目"
"实现用户登录功能"
"添加数据验证"
"修复这个 bug"
```

### 🔧 SDK 开发模式（明确触发）

只有在明确说明时才进入此模式：

```
"修改 infra-core SDK"
"创建一个新的 SDK 工具"
"扩展框架功能"
```

## 📁 目录结构

```
infra_demo/                      # 可移植 IDE 平台
│
├── [框架层 - 稳定，不随意修改]
├── sdks/                        # SDK 工具包
│   └── infra-core/              # 框架核心 SDK
│       ├── api/                 # Python API
│       ├── cli/                 # CLI 入口
│       ├── skills/              # Skills 实现
│       └── tests/               # 测试
│
├── scripts/                     # 框架工具
├── .claude/                     # Claude Code 配置
│   ├── commands/                # 自定义命令
│   └── skills/                  # Skills 入口
│
├── docs/                        # 规范文档
├── core/                        # 框架核心（可移植模板）
├── registry/                    # 工具注册表
│
├── [项目层 - 用户工作区]
├── my-web-app/                  # 用户项目示例 1
│   ├── src/
│   └── ...
│
├── data-analysis/               # 用户项目示例 2
│   ├── notebooks/
│   └── ...
│
└── <project-name>/              # 其他用户项目
    └── ...
```

## 🛠️ 核心原则

### 1. SDK 稳定性原则

- **框架层是稳定的**：SDK 工具包不随意修改
- **项目层是灵活的**：用户项目可以自由开发
- **新功能先在项目中实现**：验证成熟后再考虑迁移到 SDK

### 2. 工作模式识别

- **默认项目开发模式**：AI 在项目子目录中工作
- **明确触发 SDK 开发模式**：只有在明确说明时才修改框架层
- **不确定时询问用户**：AI 会先确认用户意图

### 3. 请求 → 工具 → 集成

- 每个请求都应该产生可执行的工具
- 不允许只输出文档而不创建工具
- 工具必须支持 `--help`，错误输出到 stderr

## 📚 文档索引

| 文档 | 用途 |
|------|------|
| `CLAUDE.md` | AI 项目上下文（自动加载） |
| `BOOTSTRAP.md` | 新项目初始化指南 |
| `docs/60_sdk_specification.md` | SDK 规范 |
| `docs/TROUBLESHOOTING.md` | 故障排查 |
| `core/docs/00_operating_manual.md` | 操作原则 |
| `core/docs/10_tooling_conventions.md` | CLI 规范 |
| `core/docs/50_skills_system.md` | Skills 系统 |

## 🔧 常用命令

### SDK CLI（新架构）

```bash
# 审查 SDK
python sdks/infra-core/cli/main.py audit-sdk sdks/infra-core

# 审查文档
python sdks/infra-core/cli/main.py audit-docs docs

# 审查 Skills
python sdks/infra-core/cli/main.py audit-skills .claude/skills
```

### 独立工具（兼容旧架构）

```bash
# 查看工具
python scripts/list_tools.py

# 查看技能
python scripts/list_skills.py

# 健康检查
python scripts/audit_all.py
```

## 💡 使用示例

### 创建新项目

```
用户: "帮我创建一个 Web 应用"

AI: "好的，请问项目名称是什么？"

用户: "my-web-app"

AI:
1. 创建项目目录：mkdir my-web-app
2. 切换到项目目录：cd my-web-app
3. 在项目中搭建 Web 应用
4. 调用 SDK 工具（如果需要）
```

### 实现功能

```
用户: "实现用户登录功能"

AI:
1. 查看现有 SDK 能力
2. 在项目中实现登录功能
3. 调用 SDK 工具辅助开发
4. 不修改框架层文件
```

### 修改 SDK（明确触发）

```
用户: "修改 infra-core SDK，添加新的审计功能"

AI:
1. 识别到明确的 SDK 修改命令
2. 进入 SDK 开发模式
3. 修改 sdks/infra-core/api/audit.py
4. 更新相关的 tests 和文档
5. 运行 audit-sdk 验证
```

## 🎓 最佳实践

### 对于用户

1. **创建项目时**：直接说"创建一个 XXX 项目"
2. **开发功能时**：直接说"实现 XXX 功能"
3. **修改框架时**：明确说"修改 SDK"或"扩展框架"
4. **不确定时**：直接用自然语言表达意图，AI 会引导你

### 对于 AI

1. **默认项目开发模式**：在项目子目录中工作
2. **优先使用 SDK 工具**：而不是重新实现
3. **功能成熟后询问迁移**：不擅自将项目代码迁移到 SDK
4. **不确定时询问用户**：而不是擅自假设

## 🤝 贡献指南

### 添加新工具

1. 在项目中实现和验证
2. 功能成熟后，考虑迁移到 SDK
3. 遵循 `docs/60_sdk_specification.md` 规范
4. 运行 `audit-sdk` 验证

### 创建新 SDK

1. 遵循 SDK 包规范
2. 包含 API、CLI、Skills、Tests
3. 更新 manifest.yaml
4. 创建对应的入口 skills

## 📄 许可证

MIT License

## 🔗 相关资源

- [Claude Code 文档](https://docs.anthropic.com/claude/docs)
- [SDK 规范](docs/60_sdk_specification.md)
- [Skills 系统指南](core/docs/50_skills_system.md)

---

**提示**：这是一个 AI-Native 的开发环境，直接用自然语言告诉 AI 你想做什么，它会引导你完成！
