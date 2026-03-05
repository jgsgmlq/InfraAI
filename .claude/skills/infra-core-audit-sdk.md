---
name: infra-core-audit-sdk
description: 审查 SDK 包的完整性和规范性
triggers:
  - "检查 SDK"
  - "审查 SDK"
  - "audit SDK"
  - "validate SDK"
sdk: infra-core
implementation: sdks/infra-core/skills/audit-sdk.md
---

# SDK 审查

审查 SDK 包是否符合框架规范。

## 用途

- 检查必需文件是否存在
- 验证 manifest.yaml 格式
- 确认 skills 入口与实现匹配

## 调用方式

```python
from sdks.infra_core.api import audit_sdk

result = audit_sdk("sdks/my-sdk")
if not result.passed:
    for finding in result.errors:
        print(f"[ERROR] {finding.message}")
```

或 CLI:

```bash
infra-core audit-sdk sdks/my-sdk
```

## 详细文档

完整实现逻辑请参考：`sdks/infra-core/skills/audit-sdk.md`
