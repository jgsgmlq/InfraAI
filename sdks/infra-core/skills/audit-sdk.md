# SDK 审查 - 实现文档

## 概述

SDK 审查工具检查 SDK 包的完整性和规范性，确保所有必需组件都存在且格式正确。

## 审查项目

### 结构检查

| 检查项 | 级别 | 说明 |
|--------|------|------|
| `__init__.py` | ERROR | 必须存在 |
| `version.py` | ERROR | 必须存在 |
| `manifest.yaml` | ERROR | 必须存在 |
| `README.md` | ERROR | 必须存在 |
| `CHANGELOG.md` | ERROR | 必须存在 |
| `api/` | ERROR | 必须存在 |
| `tests/` | ERROR | 必须存在 |
| `cli/` | WARNING | 推荐存在 |
| `skills/` | WARNING | 推荐存在 |
| `examples/` | WARNING | 推荐存在 |

### manifest.yaml 检查

必需字段：
- `name`: SDK 名称（kebab-case）
- `version`: 语义化版本号
- `description`: 功能描述

推荐字段：
- `author`: 作者
- `license`: 许可证
- `dependencies`: 依赖声明
- `exports`: 导出声明

### Skills 完整性检查

- 每个 `exports.skills` 条目必须有：
  - 对应的入口文件在 `.claude/skills/`
  - 对应的实现文件在 `skills/`

## 执行步骤

### Step 1: 检查目录存在

```python
from sdks.infra_core.api import audit_sdk

result = audit_sdk("sdks/target-sdk")
```

### Step 2: 分析结果

```python
if result.passed:
    print("SDK 审查通过")
else:
    print("SDK 审查失败")
    for error in result.errors:
        print(f"  - {error.message}")
        if error.suggestion:
            print(f"    建议: {error.suggestion}")
```

### Step 3: 修复问题

根据错误信息，创建缺失的文件或修复格式问题。

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| SDK directory not found | 路径错误 | 检查 SDK 路径是否正确 |
| Missing required file | 文件缺失 | 按规范创建缺失文件 |
| Invalid YAML | manifest 格式错误 | 修复 YAML 语法 |

## 相关 Skills

- `infra-core-audit-docs`: 文档审查
- `infra-core-create-sdk`: 创建新 SDK（自动符合规范）
