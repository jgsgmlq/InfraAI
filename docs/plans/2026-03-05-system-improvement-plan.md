# 系统改进实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 增强系统的用户体验和 AI 编程指导能力，让用户清楚知道能说什么，让 AI 有更好的编程指导。

**Architecture:** 三个模块并行改进：/init 初始化体验增强、Skills 能力补充、工具辅助能力增强。Skills 采用混合模式，核心场景自写，复杂场景桥接 superpowers。

**Tech Stack:** Python 3.8+, PyYAML, Markdown Skills

---

## 模块一：/init 初始化体验增强

### Task 1: 更新 /init 命令定义

**Files:**
- Modify: `.claude/commands/init.md`

**Step 1: 阅读当前 init.md**

阅读 `.claude/commands/init.md` 了解当前结构。

**Step 2: 重写 init.md 内容**

更新为新的初始化流程，包含：
1. 能力清单展示（按场景分类）
2. 上下文感知（项目状态）
3. 外部插件透明化

新内容：

```markdown
# /init - 项目初始化

当用户输入 `/init` 或启动新会话时，执行以下初始化流程。

---

## 阶段一：静默检查

按顺序运行以下命令，捕获输出供后续使用：

### 1.1 健康检查

```bash
python scripts/audit_all.py --quiet
```

记录退出码（0=健康，非0=有问题）。

### 1.2 获取最近提交

```bash
git log -1 --oneline
```

### 1.3 获取工具列表

```bash
python scripts/list_tools.py --compact
```

### 1.4 获取技能列表

```bash
python scripts/list_skills.py --compact
```

---

## 阶段二：集中输出展示

### 2.1 输出 Logo

使用 ANSI 颜色输出 Logo（与之前相同）。

### 2.2 项目状态

```
📊 项目状态：
   • 最近修改：<git log 输出>
   • 系统健康：✅ 正常 / ⚠️ 有问题，运行 `python scripts/audit_all.py` 查看
```

### 2.3 能力清单

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 我能帮你做
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔧 框架维护
   • "创建新工具" / "帮我写一个脚本"
   • "创建 SDK" / "新建一个 SDK 包"
   • "检查工具" / "审查 SDK"
   • "部署框架到新项目"

💻 日常编程
   • "我有个想法..." → 引导你整理需求
   • "修一下这个 bug" → 简单 bug 快速修复
   • "添加一个功能" → 功能开发指南

🚀 复杂任务（调用 superpowers 插件）
   • "帮我深入分析这个需求" → brainstorming
   • "这个 bug 很难定位" → systematic-debugging
   • "用 TDD 方式开发" → test-driven-development
   • "帮我做代码审查" → code-reviewer
```

### 2.4 工具速查

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 工具速查
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<list_tools.py --compact 输出>
```

### 2.5 就绪声明

```
✅ 初始化完成

💡 提示：直接用自然语言告诉我你想做什么，我会引导你完成。
```

---

## 注意事项

- 如果 `--compact` 选项不可用，使用原有输出并精简展示
- 外部插件能力明确标注来源
- 保持输出简洁，避免信息过载
```

**Step 3: 验证 init.md 格式正确**

确认文件格式正确，无语法错误。

**Step 4: Commit**

```bash
git add .claude/commands/init.md
git commit -m "feat: enhance /init with capability showcase and context awareness"
```

---

## 模块二：Skills 能力补充

### Task 2: 创建 clarify-requirements Skill

**Files:**
- Create: `core/.agent/skills/clarify-requirements.md`

**Step 1: 创建 clarify-requirements.md**

```markdown
# Clarify Requirements

## Purpose

当用户需求不明确时，通过提问引导用户整理和明确需求。

## When to Use

- 用户表达的需求比较模糊
- 需要在开始实现前确认细节
- 用户说"我有个想法"但不确定具体要什么

## Trigger Phrases

When the user says:
- "我有个想法..."
- "我想做一个..."
- "帮我想想怎么..."
- "I have an idea..."
- "I want to build..."

## Process

### Step 1: 确认目标

问用户：**"你想解决什么问题？"** 或 **"这个功能要达到什么效果？"**

### Step 2: 确认范围

问用户：**"需要实现哪些具体功能？"** 列出 2-4 个核心功能点。

### Step 3: 确认约束

问用户：**"有哪些限制条件？"** 例如：
- 技术栈限制
- 时间限制
- 兼容性要求

### Step 4: 输出需求摘要

整理为结构化的需求摘要：

```
📋 需求摘要

目标：[一句话描述]

功能点：
1. [功能 1]
2. [功能 2]
3. [功能 3]

约束：
- [约束 1]
- [约束 2]

确认以上理解是否正确？
```

## When to Escalate to superpowers:brainstorming

当出现以下情况时，建议用户使用 superpowers:brainstorming：

- 需要探索多种技术方案
- 需要权衡不同架构的取舍
- 需求复杂，涉及多个系统或模块
- 用户不确定最佳实现方式

**告知用户**："这个需求比较复杂，建议我们用 brainstorming 来深入分析，我会调用 superpowers 插件来帮助。"

## Principles

1. **一次一个问题**：不要同时问多个问题
2. **简单优先**：能 3 个问题内明确的需求，就不要问更多
3. **确认理解**：在开始实现前，确保用户认可需求摘要
```

**Step 2: Commit**

```bash
git add core/.agent/skills/clarify-requirements.md
git commit -m "feat: add clarify-requirements skill for guiding users"
```

---

### Task 3: 创建 quick-fix Skill

**Files:**
- Create: `core/.agent/skills/quick-fix.md`

**Step 1: 创建 quick-fix.md**

```markdown
# Quick Fix

## Purpose

指导简单 bug 的快速修复流程。

## When to Use

- 错误信息明确，原因清晰
- 单文件或少量文件的修复
- 不需要深入调试分析

## Trigger Phrases

When the user says:
- "这里有个 bug"
- "修一下这个错误"
- "fix this"
- "这个报错了"
- "帮我修复"

## Process

### Step 1: 定位问题

问用户或查看：
- 错误信息是什么？
- 在哪个文件/哪一行？

### Step 2: 复现问题

确认问题可以复现：
- 运行相关测试或命令
- 确认看到相同错误

### Step 3: 修复

- 分析错误原因
- 编写修复代码
- 保持修改最小化，只修复问题本身

### Step 4: 验证

- 运行测试确认修复有效
- 确认没有引入新问题

### Step 5: 提交

```bash
git add <modified files>
git commit -m "fix: <简短描述修复内容>"
```

## When to Escalate to superpowers:systematic-debugging

当出现以下情况时，建议使用 superpowers:systematic-debugging：

- 错误原因不明确
- 问题难以复现
- 涉及多个模块的复杂交互
- 修复后问题仍然存在

**告知用户**："这个 bug 比较复杂，需要系统性调试。我会调用 superpowers 的 systematic-debugging 来分析。"

## Principles

1. **理解再修**：先确保理解问题，再动手修复
2. **最小修改**：只修复问题，不顺手重构
3. **验证修复**：修复后必须验证
```

**Step 2: Commit**

```bash
git add core/.agent/skills/quick-fix.md
git commit -m "feat: add quick-fix skill for simple bug fixes"
```

---

### Task 4: 创建 add-feature Skill

**Files:**
- Create: `core/.agent/skills/add-feature.md`

**Step 1: 创建 add-feature.md**

```markdown
# Add Feature

## Purpose

指导添加新功能的标准流程。

## When to Use

- 用户要求添加新功能
- 功能需求相对明确
- 不需要复杂的架构设计

## Trigger Phrases

When the user says:
- "添加一个功能"
- "实现这个需求"
- "add feature"
- "帮我加一个..."
- "新增功能"

## Process

### Step 1: 确认需求

如果需求不够明确，先使用 @clarify-requirements 整理需求。

确认：
- 功能要做什么？
- 输入和输出是什么？
- 有哪些边界情况？

### Step 2: 确认实现位置

- 在哪个文件/模块实现？
- 是新建文件还是修改现有文件？
- 需要修改哪些相关文件？

### Step 3: 编写测试（推荐）

先写测试，明确功能的预期行为：

```python
def test_new_feature():
    result = new_function(input)
    assert result == expected
```

### Step 4: 实现功能

- 编写实现代码
- 保持代码简洁，遵循项目规范
- 参考 `core/docs/10_tooling_conventions.md`

### Step 5: 运行测试

```bash
python -m pytest <test_file> -v
```

确认测试通过。

### Step 6: 提交

```bash
git add <files>
git commit -m "feat: <功能描述>"
```

## When to Escalate to superpowers

当出现以下情况时：

- **需求复杂** → superpowers:brainstorming
- **需要详细计划** → superpowers:writing-plans
- **想用 TDD** → superpowers:test-driven-development

**告知用户**："这个功能比较复杂，建议我们先做详细规划。我会调用 superpowers 插件来帮助。"

## Principles

1. **先测试后实现**：尽量 TDD
2. **小步提交**：功能可拆分时，分多次提交
3. **不过度设计**：实现当前需求即可，不预设未来扩展
```

**Step 2: Commit**

```bash
git add core/.agent/skills/add-feature.md
git commit -m "feat: add add-feature skill for feature development"
```

---

### Task 5: 创建 bridge-superpowers Skill

**Files:**
- Create: `core/.agent/skills/bridge-superpowers.md`

**Step 1: 创建 bridge-superpowers.md**

```markdown
# Bridge to Superpowers

## Purpose

告知 AI 和用户 superpowers 插件提供的能力，以及何时应该使用它们。

## When to Use

- 用户任务超出本地 Skills 能力范围
- 需要更系统化的方法论支持
- 用户明确要求使用某个 superpowers 能力

## Superpowers 能力清单

### 需求与设计

| 能力 | 用途 | 触发场景 |
|------|------|----------|
| `brainstorming` | 深入分析需求，探索方案 | "帮我深入分析"、复杂需求 |
| `writing-plans` | 编写详细实施计划 | 需要分步骤的大任务 |

### 编码与调试

| 能力 | 用途 | 触发场景 |
|------|------|----------|
| `test-driven-development` | TDD 方式开发 | "用 TDD"、"先写测试" |
| `systematic-debugging` | 系统性调试 | 复杂 bug、原因不明 |

### 代码质量

| 能力 | 用途 | 触发场景 |
|------|------|----------|
| `code-reviewer` | 代码审查 | 完成开发后、合并前 |
| `verification-before-completion` | 完成前验证 | 即将提交或合并 |

### 工作流

| 能力 | 用途 | 触发场景 |
|------|------|----------|
| `executing-plans` | 执行实施计划 | 有现成计划需要执行 |
| `finishing-a-development-branch` | 完成开发分支 | 功能完成，准备合并 |
| `using-git-worktrees` | 使用 Git Worktree | 需要隔离开发环境 |

## How to Use

当识别到需要 superpowers 能力时：

1. **告知用户**："这个任务适合用 superpowers 的 [能力名] 来处理。"
2. **调用对应 Skill**：使用 Skill 工具调用 `superpowers:<skill-name>`
3. **按插件流程执行**：遵循插件的指导完成任务

## 示例对话

**用户**："这个 bug 我查了半天找不到原因"

**AI**："这种情况适合用系统性调试方法。我来调用 superpowers 的 systematic-debugging 插件帮你分析。"

然后调用：`Skill: superpowers:systematic-debugging`
```

**Step 2: Commit**

```bash
git add core/.agent/skills/bridge-superpowers.md
git commit -m "feat: add bridge-superpowers skill for plugin integration"
```

---

## 模块三：工具辅助能力增强

### Task 6: 为 list_tools.py 添加输出选项

**Files:**
- Modify: `scripts/list_tools.py`

**Step 1: 阅读当前 list_tools.py**

了解当前代码结构。

**Step 2: 添加 --json 和 --compact 选项**

在 argparse 中添加参数：

```python
parser.add_argument('--json', action='store_true', help='Output in JSON format')
parser.add_argument('--compact', action='store_true', help='Output in compact table format')
```

添加输出函数：

```python
def output_json(tools):
    """Output tools in JSON format."""
    import json
    result = {
        "tools": [
            {
                "id": t.get("id", ""),
                "name": t.get("name", ""),
                "version": t.get("version", ""),
                "command": t.get("entry", "")
            }
            for t in tools
        ],
        "count": len(tools)
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def output_compact(tools):
    """Output tools in compact table format."""
    print(f"{'ID':<20} {'NAME':<25} {'VERSION':<10}")
    print("-" * 55)
    for t in tools:
        print(f"{t.get('id', ''):<20} {t.get('name', ''):<25} {t.get('version', ''):<10}")
```

修改 main 函数根据参数选择输出格式。

**Step 3: 测试新选项**

```bash
python scripts/list_tools.py --json
python scripts/list_tools.py --compact
python scripts/list_tools.py  # 默认格式仍然工作
```

**Step 4: Commit**

```bash
git add scripts/list_tools.py
git commit -m "feat: add --json and --compact output options to list_tools.py"
```

---

### Task 7: 为 list_skills.py 添加输出选项

**Files:**
- Modify: `scripts/list_skills.py`

**Step 1: 阅读当前 list_skills.py**

了解当前代码结构。

**Step 2: 添加 --json 和 --compact 选项**

与 Task 6 类似，添加 JSON 和 compact 输出支持。

**Step 3: 测试新选项**

```bash
python scripts/list_skills.py --json
python scripts/list_skills.py --compact
```

**Step 4: Commit**

```bash
git add scripts/list_skills.py
git commit -m "feat: add --json and --compact output options to list_skills.py"
```

---

### Task 8: 增强 audit_all.py 错误提示

**Files:**
- Modify: `scripts/audit_all.py`

**Step 1: 阅读当前 audit_all.py**

了解当前代码结构。

**Step 2: 添加 --json 选项**

添加 JSON 格式输出支持。

**Step 3: 增强错误提示**

为每种错误类型添加：
- 可能原因
- 修复建议
- 相关文档链接

示例：

```python
ERROR_SUGGESTIONS = {
    "manifest_not_found": {
        "causes": ["SDK 目录结构不完整", "manifest.yaml 文件名拼写错误"],
        "fix": "运行: python sdks/infra-core/cli/main.py create-sdk <name>",
        "doc": "docs/60_sdk_specification.md"
    },
    # ... 其他错误类型
}
```

**Step 4: 测试增强的错误提示**

故意创建一个错误场景，验证错误提示是否包含修复建议。

**Step 5: Commit**

```bash
git add scripts/audit_all.py
git commit -m "feat: enhance audit_all.py with --json and better error messages"
```

---

### Task 9: 更新 REQUIREMENTS.md

**Files:**
- Modify: `docs/REQUIREMENTS.md`

**Step 1: 添加新完成的需求**

在 REQUIREMENTS.md 中添加：

```markdown
### P5 - 系统改进（已完成）

| ID | 功能 | 状态 | 说明 | 交付物 |
|----|------|------|------|--------|
| R-023 | /init 体验增强 | ✅ 完成 | 能力清单、上下文感知、插件透明化 | `.claude/commands/init.md` |
| R-024 | 需求整理 Skill | ✅ 完成 | 引导用户明确需求 | `clarify-requirements.md` |
| R-025 | 快速修复 Skill | ✅ 完成 | 简单 bug 修复指南 | `quick-fix.md` |
| R-026 | 添加功能 Skill | ✅ 完成 | 功能开发指南 | `add-feature.md` |
| R-027 | Superpowers 桥接 | ✅ 完成 | 外部插件能力索引 | `bridge-superpowers.md` |
| R-028 | 工具输出增强 | ✅ 完成 | --json, --compact 选项 | `list_tools.py`, `list_skills.py` |
| R-029 | 错误提示增强 | ✅ 完成 | 包含修复建议 | `audit_all.py` |
```

**Step 2: Commit**

```bash
git add docs/REQUIREMENTS.md
git commit -m "docs: update REQUIREMENTS.md with P5 system improvements"
```

---

### Task 10: 最终验证和推送

**Step 1: 运行完整审查**

```bash
python scripts/audit_all.py
```

确认所有检查通过。

**Step 2: 测试 /init 流程**

在 Claude Code 中运行 `/init`，确认新的输出格式正确。

**Step 3: 推送到远程**

```bash
git push origin master
```

---

## 验收标准

1. ✅ `/init` 输出包含能力清单和项目状态
2. ✅ 4 个新 Skills 创建完成且格式正确
3. ✅ `list_tools.py` 和 `list_skills.py` 支持 `--json` 和 `--compact`
4. ✅ `audit_all.py` 错误提示包含修复建议
5. ✅ 所有审查通过
6. ✅ 代码已推送到远程仓库
