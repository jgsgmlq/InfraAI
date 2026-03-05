# 文档审查 - 实现文档

## 概述

文档审查工具检查项目文档的一致性、完整性和格式规范。

## 审查项目

### 文件检查

| 检查项 | 级别 | 说明 |
|--------|------|------|
| 空文件 | WARNING | 文件内容少于 10 字符 |
| 无语言代码块 | INFO | 代码块缺少语言标签 |
| 断裂链接 | WARNING | 内部链接指向不存在的文件 |

### 内容检查

- Markdown 语法有效性
- 标题层级合理（不跳级）
- 代码示例可执行

## 执行步骤

### Step 1: 执行审查

```python
from sdks.infra_core.api import audit_docs

result = audit_docs("docs/")
```

### Step 2: 查看结果

```python
print(f"审查结果: {'通过' if result.passed else '失败'}")
print(f"错误: {len(result.errors)}")
print(f"警告: {len(result.warnings)}")

for finding in result.findings:
    print(f"[{finding.severity.value}] {finding.path}: {finding.message}")
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| Directory not found | 路径错误 | 检查文档目录路径 |
| Empty file | 文档未完成 | 补充内容或删除空文件 |

## 相关 Skills

- `infra-core-audit-sdk`: SDK 审查
