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
