# Error Handling Conventions

本文档定义了工具错误处理的标准流程和 AI 的恢复策略。

## Exit Codes 标准

| Code | 名称 | 含义 | AI 应对策略 |
|------|------|------|-------------|
| 0 | Success | 执行成功 | 继续下一步 |
| 2 | Parameter Error | 参数错误 | 检查命令语法，运行 `--help` |
| 3 | Runtime Error | 运行时错误 | 根据错误信息诊断，见下方策略 |

## 常见 Exit 3 场景及恢复策略

### 文件不存在

```
Error: File not found at path/to/file
```

**恢复策略**：
1. 检查文件路径是否正确
2. 使用 `ls` 或 Glob 确认文件位置
3. 如果是配置文件，检查是否需要先初始化

### 配置文件格式错误

```
Error: Invalid YAML syntax
```

**恢复策略**：
1. 读取文件内容
2. 检查 YAML 语法（缩进、冒号、引号）
3. 使用 `yaml.safe_load()` 测试

### 依赖缺失

```
ModuleNotFoundError: No module named 'xxx'
```

**恢复策略**：
1. 检查 `requirements.txt` 是否包含该依赖
2. 运行 `pip install -r requirements.txt`
3. 如果是新依赖，添加到 requirements.txt

### 权限错误

```
PermissionError: [Errno 13] Permission denied
```

**恢复策略**：
1. 检查文件/目录权限
2. 确认是否在正确的工作目录
3. 询问用户是否需要提权

## AI 通用恢复流程

```
工具执行失败
    ↓
读取 stderr 输出
    ↓
识别错误类型
    ↓
┌─ 参数错误 (Exit 2)
│   → 检查命令语法
│   → 运行 --help
│   → 修正参数后重试
│
├─ 运行时错误 (Exit 3)
│   → 诊断具体原因
│   → 应用对应恢复策略
│   → 修复后重试（最多 1 次）
│
└─ 持续失败
    → 向用户报告错误
    → 提供诊断信息
    → 建议可能的解决方案
```

## 重试原则

1. **最多重试 1 次**：避免无限循环
2. **修复后再重试**：不要简单地重复相同命令
3. **记录每次尝试**：便于诊断
4. **超过重试次数后报告**：让用户决定下一步

## 错误报告格式

向用户报告错误时，使用以下格式：

```markdown
**执行失败**: <工具名>

**错误信息**:
<stderr 输出>

**尝试的恢复措施**:
1. <措施 1>
2. <措施 2>

**建议**:
- <可能的解决方案>
```

## Skill 文档要求

每个 skill 文档 MUST 包含 `## Recovery Strategy` 章节，定义：

1. 每种退出码的具体恢复步骤
2. 是否可以安全重试
3. 需要用户介入的情况
