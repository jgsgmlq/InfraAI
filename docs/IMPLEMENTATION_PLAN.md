# 实施计划

## 总览

```
Phase 0 (基础)     Phase 1 (核心)     Phase 2 (增强)     Phase 3 (架构)
    │                  │                  │                  │
    ▼                  ▼                  ▼                  ▼
┌─────────┐      ┌─────────┐      ┌─────────┐      ┌─────────┐
│CLAUDE.md│      │依赖声明 │      │意图触发 │      │目录重构 │
│自检工具 │  →   │示例模板 │  →   │确认机制 │  →   │打包工具 │
│版本控制 │      │别名系统 │      │容错解析 │      │初始化   │
└─────────┘      └─────────┘      └─────────┘      └─────────┘
   1-2天            2-3天            2-3天            3-5天
```

---

## Phase 0：基础设施（预计 1-2 天）

### 目标
建立 AI 工作的基础环境，让 Claude Code 能理解项目并进行自检。

### 任务清单

#### Task 0.1: 创建 CLAUDE.md
**优先级**: P0 | **预计**: 0.5 天

```markdown
交付物:
- [ ] /CLAUDE.md（项目根目录）

内容要点:
- 项目背景和核心理念
- 目录结构说明
- 关键规则（Hard Rules）
- 常用命令速查
- AI 行为约束
```

#### Task 0.2: 创建自检工具 audit_registry.py
**优先级**: P0 | **预计**: 1 天

```markdown
交付物:
- [ ] scripts/audit_registry.py
- [ ] scripts/smoke/smoke_audit_registry.sh
- [ ] registry/tools.yaml 新增条目
- [ ] .agent/skills/audit_registry.md

功能:
- 检查每个注册工具是否有对应脚本文件
- 检查每个工具是否有 smoke test
- 检查每个工具是否有 skill 文档
- 输出健康报告（Markdown 格式）
- 支持 --fix 自动修复（生成缺失文件的模板）
```

#### Task 0.3: 工具版本控制
**优先级**: P0 | **预计**: 0.5 天

```markdown
交付物:
- [ ] 更新 registry/tools.yaml schema
- [ ] 更新 docs/10_tooling_conventions.md
- [ ] 更新现有工具条目

新增字段:
  version: "1.0.0"
  changelog: "Initial release"
  deprecated: false
```

### Phase 0 完成标准
- [ ] `CLAUDE.md` 存在且 AI 能正确理解项目
- [ ] `python scripts/audit_registry.py` 能执行并输出报告
- [ ] 所有工具都有 version 字段

---

## Phase 1：核心功能（预计 2-3 天）

### 目标
提升 AI 使用工具的效率和准确性。

### 任务清单

#### Task 1.1: 工具依赖声明
**优先级**: P1 | **预计**: 0.5 天

```markdown
交付物:
- [ ] 更新 registry schema 文档
- [ ] audit_registry.py 支持依赖检查

新增字段:
  depends_on:
    - tool-id-1
    - tool-id-2
```

#### Task 1.2: 示例工具模板
**优先级**: P1 | **预计**: 0.5 天

```markdown
交付物:
- [ ] scripts/_example_tool.py（带详细注释）

内容:
- 标准 argparse 结构
- stderr 错误处理
- 退出码使用
- 日志输出模式
- 每行都有注释说明"为什么这样写"
```

#### Task 1.3: 自然语言别名
**优先级**: P1 | **预计**: 0.5 天

```markdown
交付物:
- [ ] 更新 registry schema
- [ ] list_tools.py 支持显示别名
- [ ] 更新现有工具条目

新增字段:
  aliases:
    - "查看工具"
    - "show tools"
    - "命令面板"
```

#### Task 1.4: 错误恢复策略
**优先级**: P1 | **预计**: 1 天

```markdown
交付物:
- [ ] 更新 .agent/skills/_skill_template.md
- [ ] 更新现有 skill 文档
- [ ] 新增 docs/11_error_handling.md

新增章节:
  ## Recovery Strategy
  - Exit 2: [参数错误的处理方式]
  - Exit 3: [运行时错误的处理方式]
  - Retry: [是否可重试，重试条件]
```

### Phase 1 完成标准
- [ ] 工具可声明依赖，audit 能检查依赖完整性
- [ ] `_example_tool.py` 可作为新工具的复制模板
- [ ] 用户可用中文调用工具
- [ ] 每个 skill 都有错误恢复策略

---

## Phase 2：Vibe Coding 增强（预计 2-3 天）

### 目标
让框架对自然语言交互更友好，支持渐进式工作流。

### 任务清单

#### Task 2.1: 意图触发短语
**优先级**: P2 | **预计**: 0.5 天

```markdown
交付物:
- [ ] 更新 skill 模板
- [ ] 更新现有 skill 文档

新增章节:
  ## Trigger Phrases
  当用户说以下内容时，应触发此 skill:
  - "我需要一个工具来..."
  - "帮我自动化..."
  - "写个脚本..."
```

#### Task 2.2: 渐进式确认机制
**优先级**: P2 | **预计**: 1 天

```markdown
交付物:
- [ ] 更新 skill 模板
- [ ] 更新 build_cli_tool.md

新增章节:
  ## Checkpoints
  执行前必须与用户确认:
  1. □ 工具名称和存放路径
  2. □ CLI 参数设计
  3. □ 预期输出格式
  确认后方可开始实现。
```

#### Task 2.3: 容错解析规则
**优先级**: P2 | **预计**: 1 天

```markdown
交付物:
- [ ] docs/30_ambiguity_resolution.md

内容:
- 模糊请求的识别方法
- 澄清问题的标准流程
- 假设规则（什么情况可以假设，什么必须确认）
- 示例对话
```

### Phase 2 完成标准
- [ ] Skill 文档包含触发短语
- [ ] 关键 skill 有明确的确认检查点
- [ ] AI 知道如何处理模糊请求

---

## Phase 3：架构优化（预计 3-5 天）

### 目标
实现框架的可移植性，支持快速部署到新项目。

### 任务清单

#### Task 3.1: 目录结构重组
**优先级**: P3 | **预计**: 1 天

```markdown
新结构:
infra_foundation/
├── core/                     # 核心框架（可移植）
│   ├── docs/                 # 核心规范
│   ├── registry/             # 注册机制
│   ├── scripts/              # 基础工具
│   └── .agent/               # 核心 skills
├── project/                  # 项目特定（不移植）
│   ├── tools/                # 项目工具
│   └── config/               # 项目配置
├── CLAUDE.md
└── BOOTSTRAP.md              # 新项目初始化指南
```

#### Task 3.2: 核心/扩展分离
**优先级**: P3 | **预计**: 0.5 天

```markdown
交付物:
- [ ] docs/40_portability.md
- [ ] 更新 CLAUDE.md

内容:
- 明确标注哪些是 core（可移植）
- 明确标注哪些是 project（不移植）
- 扩展点说明
```

#### Task 3.3: 项目初始化工具
**优先级**: P3 | **预计**: 1.5 天

```markdown
交付物:
- [ ] scripts/init_project.py
- [ ] smoke test
- [ ] registry 条目
- [ ] skill 文档

功能:
  python scripts/init_project.py --target /path/to/new/project

  执行:
  1. 复制 core/ 目录
  2. 创建 project/ 目录结构
  3. 生成项目 CLAUDE.md（基于模板）
  4. 初始化 git（可选）
  5. 输出"下一步"指引
```

#### Task 3.4: 框架打包工具
**优先级**: P3 | **预计**: 1 天

```markdown
交付物:
- [ ] scripts/export_framework.py
- [ ] smoke test
- [ ] registry 条目
- [ ] skill 文档

功能:
  python scripts/export_framework.py --out framework.zip

  执行:
  1. 收集所有 core/ 内容
  2. 排除 project/ 和临时文件
  3. 打包为 zip
  4. 生成 manifest.json（内容清单）
```

### Phase 3 完成标准
- [ ] 目录结构清晰分层
- [ ] 可一键初始化新项目
- [ ] 可导出框架包供他人使用

---

## 里程碑总结

| 里程碑 | 完成标准 | 预计时间 |
|--------|----------|----------|
| M0: 基础就绪 | CLAUDE.md + 自检工具 + 版本控制 | 第 2 天 |
| M1: 核心可用 | 依赖 + 模板 + 别名 + 错误恢复 | 第 5 天 |
| M2: Vibe 友好 | 意图触发 + 确认机制 + 容错 | 第 8 天 |
| M3: 可移植 | 重构 + 初始化工具 + 打包 | 第 13 天 |

---

## 执行建议

1. **Phase 0 必须先完成**：CLAUDE.md 是后续所有工作的基础
2. **每完成一个工具，立即用 audit 自检**：确保符合规范
3. **边做边用**：在实施过程中使用框架本身，发现问题立即修复
4. **AI 参与维护**：让 Claude Code 帮助编写文档和检查一致性
