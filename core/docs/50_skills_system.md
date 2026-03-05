# Skills System Guide

本文档说明如何使用、编写和导入 skills。

## 什么是 Skill？

Skill 是一个 Markdown 文档，定义了 AI 在特定场景下应该如何行动。它包括：
- 触发条件（什么时候使用）
- 执行步骤（怎么做）
- 恢复策略（出错了怎么办）
- 硬性要求（必须满足的条件）

---

## Skills 存放位置

### 分层结构

```
项目根目录/
├── core/.agent/skills/        # 框架核心 skills（可移植）
├── project/.agent/skills/     # 项目自定义 skills（不移植）
└── project/.agent/external/   # 外部导入的 skills（不移植）
```

### 各层级说明

| 位置 | 用途 | 可移植 | 修改建议 |
|------|------|--------|----------|
| `core/.agent/skills/` | 框架通用 skills | ✅ | 谨慎修改，影响所有项目 |
| `project/.agent/skills/` | 项目专属 skills | ❌ | 自由修改 |
| `project/.agent/external/` | 外部导入 | ❌ | 不建议直接修改 |

---

## 如何编写 Skill

### Step 1: 复制模板

```bash
cp core/.agent/skills/_skill_template.md project/.agent/skills/my_skill.md
```

### Step 2: 填写内容

```markdown
# My Skill Name

## Purpose
[这个 skill 做什么？]

## When to Use
[什么情况下触发？]

## Trigger Phrases
When the user says:
- "触发短语 1"
- "trigger phrase 2"

## Command
```bash
# 具体要执行的命令
python scripts/my_tool.py --flag value
```

## Principles
1. [核心原则 1]
2. [核心原则 2]

## Checkpoints
执行前确认：
1. [ ] [需要确认的事项]

## Recovery Strategy

### Exit 0 (Success)
- [成功后的操作]

### Exit 3 (Runtime Error)
- [失败后的恢复步骤]

## HARD GATES (Non-Negotiable)
- [ ] [必须满足的条件]
```

### Step 3: 关联工具（可选）

如果 skill 对应一个工具，在 `project/registry/tools.yaml` 中注册：

```yaml
- id: my-tool
  name: My Tool
  version: "1.0.0"
  entry: python project/tools/my_tool.py
  # ...
```

---

## 如何导入外部 Skill

### 方法 1: 直接复制

```bash
# 从其他项目
cp /other/project/.agent/skills/useful.md project/.agent/external/

# 从 URL
curl -o project/.agent/external/skill.md https://example.com/skill.md
```

### 方法 2: 从框架包导入

```bash
unzip framework.zip -d /tmp/fw
cp /tmp/fw/core/.agent/skills/desired.md project/.agent/external/
```

### 导入后的处理

1. **添加来源注释**（推荐）：
   ```markdown
   <!--
   Source: https://github.com/example/repo
   Version: 1.0.0
   Imported: 2024-01-15
   -->
   ```

2. **检查依赖**：
   - Skill 是否依赖特定工具？
   - 工具是否已安装/注册？

3. **调整触发短语**（如需要）：
   - 适应项目的语言习惯
   - 避免与现有 skills 冲突

---

## Skill 类型

### 1. 工具类 Skill

对应一个 CLI 工具，定义如何调用它。

```markdown
# list-tools

## Purpose
列出所有可用工具

## Command
python scripts/list_tools.py
```

### 2. 流程类 Skill

定义一个多步骤的工作流程。

```markdown
# Deploy Production

## Purpose
部署到生产环境

## Steps
1. 运行测试
2. 构建项目
3. 部署到服务器
4. 验证部署
```

### 3. 决策类 Skill

帮助 AI 做出正确决策。

```markdown
# Choose Database

## Purpose
帮助选择合适的数据库

## Decision Tree
- 需要关系型？→ PostgreSQL
- 需要文档型？→ MongoDB
- 需要缓存？→ Redis
```

---

## 最佳实践

### DO（推荐）

- ✅ 使用清晰的触发短语
- ✅ 提供详细的恢复策略
- ✅ 包含实际的命令示例
- ✅ 定义明确的 HARD GATES
- ✅ 外部 skills 保持原样，修改时复制到 skills/

### DON'T（避免）

- ❌ 触发短语过于通用（如"帮我"）
- ❌ 缺少错误恢复策略
- ❌ HARD GATES 过于模糊
- ❌ 直接修改 external/ 中的文件

---

## 与其他系统的关系

| 系统 | 关系 |
|------|------|
| Tools | Skill 可以调用注册的工具 |
| Registry | 工具在 registry 注册，skill 定义如何使用 |
| Docs | Skill 可以引用规范文档 |
| CLAUDE.md | 定义全局规则，skill 定义具体行为 |
