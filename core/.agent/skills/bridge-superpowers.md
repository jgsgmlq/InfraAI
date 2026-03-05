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

---

**用户**："帮我规划一下这个大功能怎么实现"

**AI**："这个功能比较复杂，我来调用 superpowers 的 brainstorming 插件，帮你深入分析需求和方案。"

然后调用：`Skill: superpowers:brainstorming`

## Principles

1. **透明告知**：调用外部插件前告知用户
2. **合理升级**：简单任务用本地 Skills，复杂任务才升级到 superpowers
3. **遵循流程**：调用后按插件的指导流程执行
