# Registry Audit Tool

## Purpose
检查工具注册表的健康状态，确保每个注册的工具都有完整的配套文件（脚本、测试、文档）。

## When to Use
- 创建新工具后，验证是否符合规范
- 定期检查项目健康度
- 排查"工具找不到"类问题
- 准备移植框架前的完整性检查

## Trigger Phrases
当用户说以下内容时，应使用此工具：
- "检查一下工具是否完整"
- "audit the registry"
- "工具健康检查"
- "有哪些工具缺少文档/测试"

## Command
```bash
# 基本检查
python scripts/audit_registry.py

# 自动生成缺失文件的模板
python scripts/audit_registry.py --fix

# 只显示问题，不显示通过项
python scripts/audit_registry.py --quiet
```

## Principles
1. **非破坏性**：只检查，不删除任何文件
2. **可修复**：`--fix` 只生成模板，不覆盖已有文件
3. **全面性**：检查脚本、测试、文档、版本四个维度

## Recovery Strategy

### Exit 0 (Success)
- 所有检查通过，无需操作
- 可以继续下一步工作

### Exit 2 (Parameter Error)
- 检查命令语法
- 运行 `--help` 查看正确用法

### Exit 3 (Checks Failed)
- 阅读报告，识别失败的检查项
- 使用 `--fix` 生成缺失文件的模板
- 手动补充缺失内容
- 重新运行 audit 验证

### When to Escalate to User
- 工具设计需要用户确认时
- 不确定如何修复时

## Checkpoints
执行前确认：
1. 当前目录是否为项目根目录
2. registry/tools.yaml 是否存在

## HARD GATES (Non-Negotiable)
- [ ] 必须输出 Markdown 格式报告
- [ ] 必须检查所有四个维度（脚本、测试、文档、版本）
- [ ] `--fix` 不能覆盖已有文件
