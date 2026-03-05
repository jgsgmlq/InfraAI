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
